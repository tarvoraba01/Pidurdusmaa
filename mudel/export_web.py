"""Ekspordib presets + selgitused veebilehe jaoks failiks web/data.js
ja genereerib engine.js CAL-ploki Calibration-i pealt.

Kaivita kaustast /home/claude:  python3 -m pidurdus.export_web
"""
import json
import os
import re
from dataclasses import fields

from .model import Calibration
from .presets import (TYRES, VEHICLE_NOTES, VEHICLES, vehicle_body,
                      vehicle_make)

# valjad, mille nimi on JS-is teine
NAME_MAP = {
    "mu_dry_base": "muDry", "mu_snow_base": "muSnow", "mu_ice_base": "muIce",
    "mu_gravel_base": "muGravel", "v_ref_ms": "vRef",
    "brake_buildup_s": "brakeBuildup",
}

OUT_DATA = "web/data.js"
OUT_ENGINE = "web/engine.js"
TIPS = "pidurdus/selgitused.json"


def _tyre(key, t):
    d = {
        "key": key, "name": t.name, "category": t.category.name,
        "wetGripIndex": t.wet_grip_index, "treadDepthMm": t.tread_depth_mm,
        "treadDepthNewMm": t.tread_depth_new_mm, "pressureBar": t.pressure_bar,
        "loadCapacityKg": t.load_capacity_kg, "ageYears": t.age_years,
        "studded": t.studded, "size": t.size, "muDry": t.mu_dry_override,
        "gSource": t.g_source,
    }
    if t.mu_snow_override is not None:
        d["muSnow"] = t.mu_snow_override
    if t.mu_ice_override is not None:
        d["muIce"] = t.mu_ice_override
    return d


from .oem_sizes import OEM_SIZES as _OEM


def _veh(key, v):
    d = {
        "key": key, "name": v.name, "kerbMassKg": v.kerb_mass_kg,
        "absClass": v.abs_class.name, "cdaM2": v.cda_m2,
        "cogHeightM": v.cog_height_m, "wheelbaseM": v.wheelbase_m,
        "recommendedPressureBar": v.recommended_pressure_bar,
        "oemSize": v.oem_size, "brakeCapacityG": v.brake_capacity_g,
        "make": vehicle_make(key), "body": vehicle_body(key),
        # kõik tehasemõõdud + allikas (oem_sizes.py)
        "oemSizes": _OEM.get(key, (None, []))[1],
        "oemConf": _OEM.get(key, (None, [], ""))[2] if key in _OEM else "",
        "oemSrc": _OEM.get(key, (None, [], "", ""))[3] if key in _OEM else "",
    }
    if VEHICLE_NOTES.get(key):
        d["note"] = VEHICLE_NOTES[key]
    return d


def _eprel():
    """EPREL-i rehvid KOMPAKTSES kujus.

    Miks eraldi massiiv ja mitte "tyres" hulka: need kaks nimekirja on
    ERI TUGEVUSEGA ja seda ei tohi ara peita. "tyres" on 91 rehvi, mille
    G on tuletatud avaldatud testi MOODETUD pidurdusmaast. EPREL-i omadel
    on ainult margise KLASS, ehk klassi keskpunkt -- sama klassi rehvid on
    mudelis eristamatud. Kui nad oleksid uhes potis, naeks leht valja
    nagu 3744 vordset rehvi.

    Kuju on massiiv massiivides, mitte objektid, sest nimed korduksid
    3653 korda: [mark, nimi, moot_normaliseeritud, kategooria_nr, klass,
    lipud]. Lipud: bitt0 = kategooria on OLETUS (3PMSF on, aga nimi ei
    utle, kas talve- voi lamellrehv), bitt1 = sama mudel samas moodus
    andis mitu marghaarde klassi ja siin on HALVIM.
    """
    src = os.path.join(os.path.dirname(__file__), "eprel_tyres.json")
    if not os.path.exists(src):
        return []
    KAT = {"SUMMER_TOURING": 0, "ALL_SEASON": 1,
           "WINTER_CENTRAL": 2, "WINTER_NORDIC": 3}
    out = []
    for r in json.load(open(src, encoding="utf-8"))["rehvid"]:
        f = (1 if r["kat_alus"].startswith("OLETUS") else 0) \
            | (2 if len(r["klassid"]) > 1 else 0)
        out.append([r["mark"], r["nimi"], r["mootN"],
                    KAT[r["kat"]], r["klass"], f])
    return out


def main():
    data = {
        "tyres": [_tyre(k, t) for k, t in TYRES.items()],
        "vehicles": [_veh(k, v) for k, v in VEHICLES.items()],
        "tips": json.load(open(TIPS, encoding="utf-8")),
        "eprel": _eprel(),
    }
    with open(OUT_DATA, "w", encoding="utf-8") as f:
        f.write("var PIDURDUS_DATA = ")
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write(";\n")
    print(f"{OUT_DATA}: {len(data['tyres'])} moodetud rehvi, "
          f"{len(data['eprel'])} EPREL-i rehvi, "
          f"{len(data['vehicles'])} autot, {len(data['tips'])} mullikest")

    # kontroll, et JS-i CAL ei triiviks Python-i Calibration-ist lahku
    #
    # VAREM kontrolliti siin ainult, kas VÄLJA NIMI esineb engine.js-is.
    # See andis vale kindlustunde: kui Pythonis muutus ARV, ütles see
    # kontroll endiselt "CAL katab koik valjad", ja muudatus ei jõudnud
    # kunagi kasutajani. Nii juhtuski mu_snow_base-ga -- ainult juhuslik
    # paarsustest (parity.py) püüdis selle kinni. Nüüd võrreldakse ka
    # VÄÄRTUSI, skalaaride ja lamedate arvusõnastike puhul.
    src = open(OUT_ENGINE, encoding="utf-8").read()
    cal = Calibration()
    missing, drift, unchecked = [], [], []
    for fl in fields(cal):
        js = NAME_MAP.get(fl.name) or re.sub(
            r"_(\w)", lambda m: m.group(1).upper(), fl.name)
        if js not in src:
            missing.append(fl.name)
            continue
        py = getattr(cal, fl.name)
        if isinstance(py, bool) or not isinstance(py, (int, float, dict)):
            unchecked.append(fl.name)
            continue
        if isinstance(py, float) or isinstance(py, int):
            m = re.search(re.escape(js) + r"\s*:\s*(-?\d+(?:\.\d+)?)", src)
            if m and abs(float(m.group(1)) - float(py)) > 1e-9:
                drift.append(f"{fl.name}: py={py} js={m.group(1)}")
            elif not m:
                unchecked.append(fl.name)
            continue
        # lame sõnastik, mille väärtused on arvud
        if not all(isinstance(v, (int, float)) for v in py.values()):
            unchecked.append(fl.name)
            continue
        m = re.search(re.escape(js) + r"\s*:\s*\{([^{}]*)\}", src)
        if not m:
            unchecked.append(fl.name)
            continue
        got = dict(re.findall(r"(\w+)\s*:\s*(-?\d+(?:\.\d+)?)", m.group(1)))
        for k, v in py.items():
            key = k.name if hasattr(k, "name") else str(k)
            if key not in got:
                drift.append(f"{fl.name}.{key}: JS-is puudub")
            elif abs(float(got[key]) - float(v)) > 1e-9:
                drift.append(f"{fl.name}.{key}: py={v} js={got[key]}")

    if missing:
        print("HOIATUS: JS-i CAL-plokist puuduvad:", ", ".join(missing))
    if drift:
        print(f"HOIATUS: {len(drift)} VÄÄRTUST on lahku triivinud:")
        for d in drift:
            print("   ", d)
    if not missing and not drift:
        print(f"{OUT_ENGINE}: CAL katab koik {len(fields(cal))} valja, "
              f"{len(fields(cal)) - len(unchecked)} ka vaartuse tasemel")
    if unchecked:
        print(f"   ({len(unchecked)} valja vaartust ei saa siit kontrollida: "
              f"{', '.join(unchecked)})")


if __name__ == "__main__":
    main()
