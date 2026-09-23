# -*- coding: utf-8 -*-
"""Andmekiht WordPressi teemale (theme/pidurdusmaa/data/).

UKS ALLIKAS, MITTE KAKS
-----------------------
Teema EI OMA oma andmebaasi. Koik, mida ta naitab, tuleb siit ja siin
tuleb koik samast kohast kust web/data.js: presets.py (autod, moodetud
rehvid), anchors*.py (moodetud testitulemused), eprel_tyres.json
(EPREL-i korje, vt eprel_harvest.py + eprel_convert.py). Mootor on
SAMA web/engine.js -- build.py kopeerib selle teemasse, ei kirjuta uut.

EPREL-i API votit ei ole siin ega teemas kuskil. Korje jookseb ehituse
ajal kasutaja masinas; teema saab ainult tulemuse.

FAILID
------
  core.json          autod, moodetud rehvid + nende testid, allikad,
                     moodud. Laetakse avalehel.
  eprel/<MOOT>.json  EPREL-i rehvid UHES moodus. Laetakse alles siis,
                     kui kasutaja moodu valib -- 3653 rehvi korraga
                     avalehele oleks 700 kB, mida keegi ei vaata.
  models.json        rehvimudelite register (slug -> moodud, klassid,
                     testid). Ainult PHP-le, rehvilehtede jaoks.

MIS ON OLEMAS JA MIS MITTE -- see maarab, mida leht tohib naidata
-----------------------------------------------------------------
  EPREL (ametlik):  marghaardeklass, kutuseklass, mura dB + klass,
                    3PMSF, jaamargis, koormus- ja kiirusindeks
  Testid (moodetud): pidurdusmaad (marg/kuiv/lumi/jaa/betoon),
                    akvaplaneerimiskiirus -- 88 rehvile
  Arvutus (hinnang): pidurdusmaa kasutaja autole ja oludele
  PUUDUB:           juhitavus, mugavus, kulumine/labisoit, hind.
                    Neid EI tuletata millestki. Leht utleb "Andmed
                    puuduvad".
"""
import json
import os
import re
import unicodedata
from collections import Counter, defaultdict

from .anchors import ANCHORS
from .anchors_adac import ADAC_2025
from .anchors_adac2 import ADAC_ALLSEASON, ADAC_SUMMER
from .anchors_vib10 import VIB10D, VIB10F
from .export_web import _tyre, _veh
from .model import BrakingModel, Conditions, Surface, Tyre, TyreCategory, replace
from .presets import TYRES, VEHICLES

OUT = "theme/pidurdusmaa/data"
EPREL_SRC = os.path.join(os.path.dirname(__file__), "eprel_tyres.json")

KAT_NR = ["SUMMER_TOURING", "ALL_SEASON", "WINTER_CENTRAL", "WINTER_NORDIC"]

# Testide metaandmed. Tekst on votetud anchors*.py pais-kommentaaridest,
# mitte valja moeldud. "kuupaev" on testi avaldamise aasta.
SOURCES = {
    "ADAC25": {
        "nimi": "ADAC talverehvitest 2025", "aasta": 2025,
        "moot": "225/40 R18", "auto": "VW Golf 8", "rehve": 31,
        "tegija": "ADAC (Saksamaa)",
        "kajastus": "https://www.tyrereviews.com/Tyre-Tests/2025-ADAC-Winter-Tyre-Test.htm",
        "protokoll": "kuiv 100→0, märg asfalt 80→0, märg betoon 80→0, "
                     "lumi 30→0, jää 20→0 km/h, akvaplaneerimise kiirus"},
    "ADACS25": {
        "nimi": "ADAC suverehvitest 2025", "aasta": 2025,
        "moot": "225/40 R18", "auto": "VW Golf 8", "rehve": 18,
        "tegija": "ADAC (Saksamaa)",
        "kajastus": "https://www.tyrereviews.com/Tyre-Tests/2025-ADAC-Summer-Tyre-Test.htm",
        "protokoll": "kuiv 100→0, märg asfalt 80→0, märg betoon 80→0 km/h, "
                     "akvaplaneerimise kiirus"},
    "ADACA25": {
        "nimi": "ADAC lamellrehvitest 2025", "aasta": 2025,
        "moot": "225/45 R17", "auto": "VW Golf 8", "rehve": 16,
        "tegija": "ADAC (Saksamaa)",
        "kajastus": "https://www.tyrereviews.com/Tyre-Tests/2025-ADAC-All-Season-Tyre-Test.htm",
        "protokoll": "kuiv 100→0, märg asfalt 80→0, märg betoon 80→0, "
                     "lumi 30→0, jää 20→0 km/h, akvaplaneerimise kiirus"},
    "TM25": {
        "nimi": "Tekniikan Maailma talverehvitest 2025", "aasta": 2025,
        "moot": "205/55 R16", "auto": "VW Golf", "rehve": 14,
        "tegija": "Tekniikan Maailma / UTAC (Soome)",
        "kajastus": "https://www.tyrereviews.com/Tyre-Tests/2025-Friction-and-Studded-Winter-Tyre-Test.htm",
        "protokoll": "kuiv 80→0, märg 80→0, jää 50→0 km/h"},
    "UT25": {
        "nimi": "UTAC / Aftonbladet suve- ja lamellrehvitest 2025", "aasta": 2025,
        "moot": "225/45 R17", "auto": "Audi A3", "rehve": 14,
        "tegija": "UTAC / Aftonbladet (Rootsi)",
        "kajastus": "https://www.tyrereviews.com/Tyre-Tests/2025-Summer-and-All-Season-Combined-Tyre-Test.htm",
        "protokoll": "kuiv 100→5, märg 80→5 km/h"},
    "VIB10D": {
        "nimi": "Vi Bilägare naastrehvitest 2010", "aasta": 2010,
        "moot": "205/55 R16", "auto": "Volvo S40/V50, C30", "rehve": 9,
        "tegija": "Vi Bilägare (Rootsi)",
        "kajastus": "https://www.vibilagare.se/public/documents/2010/10/dacktest_2010_dubbdack.pdf",
        "protokoll": "lumi 45→5, jää 30→5 (−2,5 °C ja +0,75 °C), "
                     "märg 80→5, kuiv 80→5 km/h",
        "markus": "Kasutatakse mudelis väljaspool-valimi kontrollina ja jää "
                  "temperatuuritundlikkuse sobitamiseks, mitte rehvilehtedel."},
    "VIB10F": {
        "nimi": "Vi Bilägare naelutute talverehvide test 2010", "aasta": 2010,
        "moot": "205/55 R16", "auto": "Volvo S40/V50, C30", "rehve": 9,
        "tegija": "Vi Bilägare (Rootsi)",
        "kajastus": "https://www.vibilagare.se/public/documents/2010/10/vib_dacktest_2010_odubbade_vinterdack.pdf",
        "protokoll": "lumi 40→5, jää 35→5, märg 80→5, kuiv 80→5 km/h",
        "markus": "Kasutatakse mudelis väljaspool-valimi kontrollina."},
}

SURF_ET = {"ASPHALT": "asfalt", "CONCRETE": "betoon", "ICE": "jää",
           "SNOW_PACKED": "lumi", "GRAVEL": "kruus"}


def slugify(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-+", "-", s)


def norm(s):
    return re.sub(r"[^0-9A-Z]", "", str(s or "").upper())


def size_slug(mootN):
    m = re.match(r"^(\d{3})(\d{2})R(\d{2})(C?)$", mootN or "")
    if not m:
        return None
    return f"{m.group(1)}-{m.group(2)}-r{m.group(3)}{'c' if m.group(4) else ''}"


def pretty_size(mootN):
    m = re.match(r"^(\d{3})(\d{2})R(\d{2})(C?)$", mootN or "")
    return f"{m.group(1)}/{m.group(2)} R{m.group(3)}{m.group(4)}" if m else mootN


# ---------------------------------------------------------------- autod --
MARK_ALIAS = {"VW": "Volkswagen", "Mercedes": "Mercedes-Benz",
              "Range": "Land Rover", "VAZ": "Lada / VAZ", "Lada": "Lada / VAZ"}


def parse_vehicle(v):
    """'VW Golf 8 1.5 TSI (2020)' -> mudel 'Golf', aasta '2020', variant.

    Andmebaasis on uks rida mudeli POLVKONNA kohta (231 rida), mitte
    iga mootori kohta. Seetottu on 'Mootor / variant' enamasti uks
    valik -- leht naitab seda ausalt, mitte ei mangi rohkem valikuid ette.
    """
    name, make = v["name"], v["make"]
    ym = re.search(r"\(([^)]*)\)\s*$", name)
    years = ym.group(1) if ym else ""
    rest = name[:ym.start()].strip() if ym else name
    # margisona(d) eest ara
    for pre in sorted({make, "VW", "Mercedes", "Lada", "VAZ", "Range Rover",
                       "Land Rover", "Škoda", "Citroën"}, key=len,
                      reverse=True):
        if rest.startswith(pre + " "):
            rest = rest[len(pre) + 1:]
            break
    if rest.startswith("Rover "):
        rest = rest[6:]
    toks = rest.split()
    if not toks:
        return {"model": name, "years": years, "variant": ""}
    model = toks[0]
    tail = toks[1:]
    # BMW 320d -> 3-seeria; Mercedes E220 -> E-klass
    if make == "BMW" and re.match(r"^\d{3}[a-z]*$", model):
        tail = [model] + tail
        model = f"{model[0]}-seeria"
    elif make == "Mercedes-Benz" and re.match(r"^[A-Z]{1,3}\d{3}", model):
        tail = [model] + tail
        model = re.match(r"^([A-Z]{1,3})", model).group(1) + "-klass"
    elif model in ("Grand", "Range", "Model", "Land", "Santa", "Space",
                   "Grande", "Atto", "Ioniq") and tail:
        model, tail = model + " " + tail[0], tail[1:]
    elif model in ("C4", "C5") and tail and tail[0] in ("Picasso", "Aircross"):
        model, tail = model + " " + tail[0], tail[1:]
    # polvkonnakood (roomlane, taht, W212, B8, E46...) voib olla KUS TAHES
    # sabas -- ta laheb aasta juurde, mootor jaab variandiks.
    pinned = []
    if make in ("BMW", "Mercedes-Benz") and tail:
        pinned = [tail.pop(0)]              # 520d / E220 on variant
    # NB: kahetäheline kood (BK, GH, KF, TM ...) on põlvkond, aga EV / SR ei ole
    GEN = re.compile(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X|[A-CE-Z]|"
                     r"(?!EV$|SR$|GT$|RS$|ST$)[A-Z]{2}|"
                     r"[A-Z]{1,2}\d{1,3}[A-Z]?|\d{1,3}|Mk\d)$")
    gen = [t for t in tail if GEN.match(t)]
    tail = pinned + [t for t in tail if not GEN.match(t)]
    variant = " ".join(tail)
    label = (" ".join(gen) + " " if gen else "") + (f"({years})" if years else "")
    return {"model": model, "years": years, "gen": " ".join(gen),
            "yearLabel": label.strip() or "—", "variant": variant or "—"}


# ---------------------------------------------------------------- testid --
def measured_tests():
    """tyre_key -> [ {src, surf, wet, v0, v1, m} ... ] ainult moodetud."""
    out = defaultdict(list)
    for a in ANCHORS:
        if a.tyre_key not in TYRES or a.source not in SOURCES:
            continue
        out[a.tyre_key].append({
            "src": a.source, "surf": a.surface.name,
            "wet": a.water_mm > 0, "v0": a.v_from_kmh, "v1": a.v_to_kmh,
            "m": a.measured_m, "t": a.temp_c})
    aqua = {}
    for d, i, src in ((ADAC_2025, 6, "ADAC25"), (ADAC_SUMMER, 4, "ADACS25"),
                      (ADAC_ALLSEASON, 6, "ADACA25")):
        for k, row in d.items():
            if k in TYRES and len(row) > i:
                aqua[k] = {"src": src, "kmh": row[i]}
    return out, aqua


# ------------------------------------------------------------ demo arvud --
def demo_numbers():
    """Avalehe selgitavad arvud, ARVUTATUD samast mudelist (mitte kirjutatud).

    Tuupiline auto (VW Golf 8, 205/55 R16) ja tuupiline suverehv
    (marghaardeklass B, klassi keskpunkt).
    """
    m = BrakingModel()
    veh = VEHICLES["vw_golf_8"]
    from .g_class_measured import G_CLASS_MEASURED as _GM
    G = {k: (_GM[k].get("SUMMER_TOURING") or _GM[k]["_"])[0] for k in "ABCDE"}

    def tyre(g=G["B"], cat=TyreCategory.SUMMER_TOURING, **kw):
        return Tyre(name="x", category=cat, wet_grip_index=g, size="205/55 R16",
                    g_source="label", **kw)

    def d(t, **c):
        base = dict(speed_kmh=90, surface=Surface.ASPHALT, water_mm=1.0,
                    temp_c=10.0, reaction_time_s=0.0)
        base.update(c)
        return round(m.stopping_distance(t, veh, Conditions(**base)).distance_m, 1)

    speeds = [50, 90, 110, 130]
    out = {
        "car": "VW Golf 8, 205/55 R16, suverehv märgise klassiga B",
        "speeds": speeds,
        "wet": [d(tyre(), speed_kmh=v) for v in speeds],
        "dry": [d(tyre(), speed_kmh=v, water_mm=0.0, temp_c=15.0) for v in speeds],
        "classA": d(tyre(G["A"])), "classE": d(tyre(G["E"])),
        "tread8": d(tyre()), "tread3": d(tyre(tread_depth_mm=3.0)),
        "summerWarm": d(tyre(), water_mm=0.0, temp_c=25.0),
        "winterWarm": d(tyre(cat=TyreCategory.WINTER_CENTRAL), water_mm=0.0, temp_c=25.0),
        "snowSummer": d(tyre(), surface=Surface.SNOW_PACKED, water_mm=0.0, temp_c=-5.0, speed_kmh=50),
        "snowWinter": d(tyre(cat=TyreCategory.WINTER_CENTRAL), surface=Surface.SNOW_PACKED, water_mm=0.0, temp_c=-5.0, speed_kmh=50),
        "loaded": round(m.stopping_distance(tyre(), veh, Conditions(speed_kmh=90, surface=Surface.ASPHALT, water_mm=1.0, temp_c=10.0, payload_kg=450)).distance_m, 1),
    }
    return out


# ---------------------------------------------------------------- EPREL --
def eprel_rows():
    if not os.path.exists(EPREL_SRC):
        return []
    return json.load(open(EPREL_SRC, encoding="utf-8"))["rehvid"]


def main():
    os.makedirs(os.path.join(OUT, "eprel"), exist_ok=True)
    tests, aqua = measured_tests()
    rows = eprel_rows()

    # --- rehvimudelid (EPREL): mark+nimi normaliseeritult, ule moodude
    mud = {}
    spell = defaultdict(Counter)
    for r in rows:
        k = norm(r["mark"]) + "|" + norm(r["nimi"])
        spell[k][r["nimi"]] += 1
        m = mud.setdefault(k, {"mark": r["mark"], "kat": r["kat"],
                               "katAlus": r["kat_alus"], "sizes": []})
        m["sizes"].append({
            "m": r["mootN"], "g": r["klass"], "gAll": r["klassid"],
            "f": r["kytus"], "db": r["muraDb"], "nk": r["muraKl"],
            "li": r["koormus"], "si": r["kiirus"],
            "snow": r["lumi"], "ice": r["jaa"]})
    slugs = {}
    for k, m in mud.items():
        m["nimi"] = spell[k].most_common(1)[0][0]
        s = slugify(m["mark"] + " " + m["nimi"])
        if s in slugs.values():
            s = s + "-" + str(len(slugs))
        slugs[k] = s
        m["slug"] = s

    # --- moodetud rehvid -> EPREL-i mudel (RANGE vordus, vt kytus_katse.py)
    tested = []
    by_norm = {}
    for k, m in mud.items():
        by_norm.setdefault(norm(m["nimi"]), []).append(k)
    for key, t in TYRES.items():
        if t.g_source != "test":
            continue
        d = _tyre(key, t)
        d["tests"] = tests.get(key, [])
        if key in aqua:
            d["aqua"] = aqua[key]
        brand = t.name.split()[0]
        model_part = t.name[len(brand):].strip()
        if brand in ("Nokian", "GT", "Point", "Double", "Star"):
            pass
        hit = None
        for kk in by_norm.get(norm(model_part), []):
            if norm(mud[kk]["mark"]).startswith(norm(brand)[:5]):
                hit = kk
                break
        if hit:
            d["slug"] = mud[hit]["slug"]
            mud[hit]["tested"] = key
        else:
            d["slug"] = slugify(t.name)
        tested.append(d)

    # --- moodud
    sizes = Counter(r["mootN"] for r in rows)
    size_list = [{"m": s, "label": pretty_size(s), "slug": size_slug(s),
                  "n": n} for s, n in sizes.most_common() if size_slug(s)]

    # --- EPREL moodu kaupa
    per = defaultdict(list)
    for k, m in mud.items():
        for z in m["sizes"]:
            per[z["m"]].append([
                m["slug"], m["mark"], m["nimi"], KAT_NR.index(m["kat"]),
                z["g"], z["f"], z["db"], z["nk"],
                (1 if m["katAlus"].startswith("OLETUS") else 0)
                | (2 if len(z["gAll"]) > 1 else 0)
                | (4 if z["snow"] else 0) | (8 if z["ice"] else 0),
                m.get("tested")])
    for s, lst in per.items():
        lst.sort(key=lambda r: ("ABCDE".index(r[4]) if r[4] in "ABCDE" else 9,
                                r[1], r[2]))
        with open(os.path.join(OUT, "eprel", s + ".json"), "w",
                  encoding="utf-8") as f:
            json.dump(lst, f, ensure_ascii=False, separators=(",", ":"))

    # --- autod
    vehicles = []
    for k, v in VEHICLES.items():
        d = _veh(k, v)
        d.update(parse_vehicle(d))
        vehicles.append(d)

    # --- VIB10 testitabelid (ainult Testid-lehele; rehve mudelis ei ole)
    vib = {
        "VIB10D": {"cols": ["lumi 45→5", "jää 30→5 (−2,5 °C)",
                            "jää 30→5 (+0,75 °C)", "lörtsi ujumiskiirus km/h",
                            "märg 80→5", "kuiv 80→5"],
                   "rows": [[r[0]] + list(r[2:]) for r in VIB10D.values()]},
        "VIB10F": {"cols": ["lumi 40→5", "jää 35→5", "märg 80→5", "kuiv 80→5"],
                   "rows": [[r[0]] + list(r[2:]) for r in VIB10F.values()]},
    }

    core = {
        "demo": demo_numbers(),
        "vehicles": vehicles,
        "tyres": tested,
        "sources": SOURCES,
        "sizes": size_list,
        "surfaces": SURF_ET,
        "vib": vib,
        "eprelSizes": sorted(per.keys()),
        # märgise klassi MÕÕDETUD esindusväärtused (kalibreeri_gklass.py)
        "gClass": __import__("pidurdus.g_class_measured",
                             fromlist=["G_CLASS_MEASURED"]).G_CLASS_MEASURED,
    }
    with open(os.path.join(OUT, "core.json"), "w", encoding="utf-8") as f:
        json.dump(core, f, ensure_ascii=False, separators=(",", ":"))

    models = {m["slug"]: {k2: v2 for k2, v2 in m.items() if k2 != "slug"}
              for m in mud.values()}
    with open(os.path.join(OUT, "models.json"), "w", encoding="utf-8") as f:
        json.dump(models, f, ensure_ascii=False, separators=(",", ":"))

    linked = sum(1 for t in tested if t["slug"] in models)
    print(f"{OUT}: {len(vehicles)} autot, {len(tested)} moodetud rehvi "
          f"({linked} seotud EPREL-i mudeliga), {len(models)} EPREL-i mudelit, "
          f"{len(per)} moodu faili")
    return core


if __name__ == "__main__":
    main()
