"""Python <-> JS paarsus PÄRIS VEEBIANDMETE peal (core.json).

Miks uus fail: vana parity.py loeb web/data.js-i, mis jäi 2026-09-25
seisu (573 autot) ja kukkus uute autode peal kokku -- ehk paarsustest
oli kuu aega vaikselt katki. See fail võtab autod ja rehvid SAMAST
core.json-ist, mida leht kasutab, ehitab neist Pythoni objektid ja
kirjutab juhtumid + Pythoni tulemused faili, mida JS-i test
(veeb/tests/engine.test.mjs) võrdleb engine.js-i omadega.

Tõe allikas on Pythoni mootor (sellel on kalibreerimine ja ankrud);
engine.js on selle port ja peab andma sama.

Käivita:  python3 -m mudel.parity_core [core.json] [väljund.json]
"""
import json
import math
import random
import sys

from .model import (AbsClass, BrakingModel, Conditions, Surface, Texture,
                    Tyre, TyreCategory, Vehicle)

CORE = "veeb/static/data/core.json"
OUT = "veeb/tests/parity_fixture.json"
GNOM = {"A": 1.60, "B": 1.47, "C": 1.32, "D": 1.17, "E": 1.05}


def veh_from(d):
    return Vehicle(
        name=d["name"], kerb_mass_kg=d["kerbMassKg"],
        abs_class=AbsClass[d["absClass"]], cda_m2=d["cdaM2"],
        cog_height_m=d["cogHeightM"], wheelbase_m=d["wheelbaseM"],
        recommended_pressure_bar=d["recommendedPressureBar"],
        oem_size=d.get("oemSize") or "", brake_capacity_g=d["brakeCapacityG"])


def tyre_from(d):
    return Tyre(
        name=d.get("name", "x"), category=TyreCategory[d["category"]],
        wet_grip_index=d["wetGripIndex"],
        tread_depth_mm=d.get("treadDepthMm", 8.0),
        tread_depth_new_mm=d.get("treadDepthNewMm") or 8.0,
        pressure_bar=d.get("pressureBar"),
        load_capacity_kg=d.get("loadCapacityKg"),
        age_years=d.get("ageYears") if d.get("ageYears") is not None else 1.0,
        studded=bool(d.get("studded")),
        mu_dry_override=d.get("muDry"), mu_snow_override=d.get("muSnow"),
        mu_ice_override=d.get("muIce"),
        hp_factor=d.get("hpFactor") if d.get("hpFactor") is not None else 1.0,
        size=d.get("size") or "", g_source=d.get("gSource", "label"),
        g_size=d.get("gSize") or "")


def cond_from(c):
    return Conditions(
        speed_kmh=c["speedKmh"], surface=Surface[c["surface"]],
        texture=Texture[c["texture"]], water_mm=c["waterMm"], temp_c=c["tempC"],
        payload_kg=c["payloadKg"], gradient_pct=c["gradientPct"],
        reaction_time_s=c["reactionTimeS"],
        brake_condition=c.get("brakeCondition", 1.0),
        ice_road=c.get("iceRoad", True) is not False,
        trailer_kg=c.get("trailerKg", 0.0),
        trailer_brakes=bool(c.get("trailerBrakes", False)))


def gmid(core, g, cat):
    t = core["gClass"].get(g)
    if t:
        if cat in t:
            return t[cat][0]
        if t.get("_") and t["_"][1]:
            return t["_"][0]
    return GNOM[g]


def pretty(m):
    import re
    x = re.match(r"^(\d{3})(\d{2})R(\d{2})(C?)$", m)
    return f"{x[1]}/{x[2]} R{x[3]}{x[4]}" if x else m


def build_cases(core, n=400, seed=11):
    rnd = random.Random(seed)
    vehs = core["vehicles"]
    tyres = core["tyres"]
    cats = ["SUMMER_TOURING", "ALL_SEASON", "WINTER_CENTRAL", "WINTER_NORDIC"]
    out = []
    for i in range(n):
        v = rnd.choice(vehs)
        if rnd.random() < 0.5:
            t = dict(rnd.choice(tyres))
            t.pop("tests", None); t.pop("aqua", None)
            # nagu leht: autol olev mõõt + testimõõt eraldi
            if rnd.random() < 0.6 and v.get("oemSize"):
                t["gSize"] = t.get("size", "")
                t["size"] = v["oemSize"]
        else:
            g, cat = rnd.choice("ABCDE"), rnd.choice(cats)
            t = {"key": "c", "name": "K", "category": cat,
                 "wetGripIndex": gmid(core, g, cat), "treadDepthMm": 8,
                 "treadDepthNewMm": 8, "pressureBar": None,
                 "loadCapacityKg": None, "ageYears": 1, "studded": False,
                 "size": v.get("oemSize") or "", "gSource": "label"}
        if rnd.random() < 0.4:  # rehvi seisukord
            t["treadDepthMm"] = round(rnd.uniform(0.5, 9.0), 1)
            t["pressureBar"] = round(rnd.uniform(1.4, 3.4), 2)
            t["ageYears"] = rnd.choice([1, 4, 7, 12])
        surf = rnd.choice(["ASPHALT", "ASPHALT", "CONCRETE", "GRAVEL",
                           "SNOW_PACKED", "SNOW_LOOSE", "ICE"])
        wet = surf in ("ASPHALT", "CONCRETE") and rnd.random() < 0.55
        c = {"speedKmh": rnd.choice([0, 1, 5, 20, 40, 60, 80, 100, 130, 160, 200,
                                     round(rnd.uniform(10, 180), 1)]),
             "surface": surf,
             "texture": rnd.choice(["NORMAL", "NORMAL", "COARSE_NEW", "WORN_SMOOTH", "POLISHED"]),
             "waterMm": round(rnd.uniform(0.1, 8.0), 2) if wet else 0.0,
             "tempC": round(rnd.uniform(-40, 50), 1),
             "payloadKg": round(rnd.uniform(0, 800)),
             "gradientPct": rnd.choice([0, 0, 0, round(rnd.uniform(-25, 25), 1)]),
             "reactionTimeS": rnd.choice([0.0, 0.0, 1.0, 1.5]),
             "brakeCondition": rnd.choice([1.0, 1.0, 0.8, 0.5])}
        out.append({"veh": v, "tyre": t, "cond": c})
    # HAAGIS (6.10.2026): eraldi juhuslik jada, et vanad juhud jääksid samaks
    rt = random.Random(seed + 101)
    for x in [dict(o) for o in rt.sample(out, 60)]:
        c = dict(x["cond"])
        c["trailerKg"] = rt.choice([300, 750, 1200, 2000, 3500])
        c["trailerBrakes"] = rt.random() < 0.5
        out.append({"veh": x["veh"], "tyre": x["tyre"], "cond": c})
    return out


def run_python(cases):
    m = BrakingModel()
    res = []
    for c in cases:
        r = m.stopping_distance(tyre_from(c["tyre"]), veh_from(c["veh"]),
                                cond_from(c["cond"]))
        fin = lambda x: x if math.isfinite(x) else None
        res.append({"d": fin(r.distance_m), "tot": fin(r.total_distance_m),
                    "lo": fin(r.low_m), "hi": fin(r.high_m),
                    "sig": r.sigma_rel, "mu": r.mu_effective,
                    "g": r.peak_decel_g, "t": r.time_s, "lim": r.limiter,
                    "conf": r.confidence, "w": len(r.warnings),
                    "ex": r.extreme, "at": r.accel_time_s,
                    "ad": r.accel_dist_m})
    return res


def main(argv):
    core_p = argv[1] if len(argv) > 1 else CORE
    out_p = argv[2] if len(argv) > 2 else OUT
    core = json.load(open(core_p, encoding="utf-8"))
    cases = build_cases(core)
    res = run_python(cases)
    # autod/rehvid võtmena, et fikstuur oleks väike ja ei dubleeriks core.json-i
    slim = [{"veh": c["veh"]["key"], "tyre": c["tyre"], "cond": c["cond"]}
            for c in cases]
    json.dump({"cases": slim, "python": res}, open(out_p, "w", encoding="utf-8"),
              ensure_ascii=False)
    print(f"{out_p}: {len(cases)} juhtumit")


if __name__ == "__main__":
    main(sys.argv)
