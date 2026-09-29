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
from .export_web import _tyre, _veh, veh_alias
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
        "nimi": "ADAC aastaringsete rehvide test 2025", "aasta": 2025,
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
        "nimi": "UTAC / Aftonbladet suve- ja aastaringsete rehvide test 2025", "aasta": 2025,
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


# Mitmesõnalised mudelinimed: (esimene sõna, järgmine sõna) -> üks mudel
_MUDEL2 = {("Golf", "Plus"), ("Passat", "CC"), ("Transit", "Custom"),
           ("Transit", "Connect"), ("Discovery", "Sport"), ("Xsara", "Picasso"),
           ("Q4", "e-tron"), ("718", "Cayman"), ("718", "Boxster"),
           ("Sealion", "7"), ("Ioniq", "5"), ("Ioniq", "6"), ("Ioniq", "9"),
           ("Golf", "Sportsvan"), ("Tiguan", "Allspace"), ("Corolla", "Verso"),
           ("Proace", "City"), ("Q8", "e-tron"), ("e-tron", "GT"), ("A6", "allroad"),
           ("A4", "allroad"), ("C5", "X"), ("C4", "Cactus"), ("Seal", "U")}
_MUDEL_NIMI = {"Cee'd": "Ceed"}
# Üksikud read, mille nimi ei ütle põlvkonda/aastaid õigesti (vanad
# üheaastased näidisread jms): võti -> (põlvkond, aastad, variant | None)
_VALIK_PARANDUS = {
    "vw_golf_8": ("8", "2020+", None), "vw_golf_4": ("IV", "1997-2006", None),
    "passat_b5": ("B5", "1996-2005", None), "vw_passat_b8": ("B8", "2014-2023", None),
    "bmw_320d": ("G20", "2019+", None), "bmw_330e_g20": ("G20", "2019+", None),
    "skoda_octavia": ("IV", "2020+", None), "toyota_corolla": ("E210", "2019+", None),
    "audi_a3": ("8Y", "2020+", "Sportback"), "vw_transporter": ("T6.1", "2019+", "—"),
    "volvo_xc60": ("II", "2017+", "B4"), "tesla_model3": ("", "2019-2023", "Long Range"),
    "mb_sprinter_906": ("906", "2006-2018", "313 CDI"), "mb_sprinter_907": ("907", "2018+", "—"),
    "mb_sprinter_901": ("901", "1995-2006", "2.2 CDI"), "opel_zafira_life": ("Life", "2019+", "2.0 diisel"),
    "opel_corsa_d": ("D", "2006-2014", "—"), "opel_combo_d": ("D", "2011-2018", "—"),
    "porsche_macan_95b": ("95B", "2013+", "S Diesel"), "lexus_rx_al10": ("AL10", "2009-2015", "450h"),
    "hyundai_ioniq5": ("", "2021+", "77 kWh"), "mg4_ev": ("", "2022+", "64 kWh"),
    "skoda_elroq": ("", "2025+", "85"), "audi_etron": ("", "2019-2022", "55"),
    "audi_q4_etron": ("", "2021+", "40"), "bmw_330e_f30": ("F30", "2012-2019", None),
    "vw_golf_gti_7": ("VII", "2012-2019", "GTI 2.0 TSI"), "vw_golf_r_8": ("8", "2020+", "R 2.0 TSI"),
    # ABS-ita ja ABS-iga read samasse põlvkonda (variandina)
    "mb_e230_w124": ("W124", "1984-1996", None),
    "bmw_520i_e34": ("E34", "1988-1996", None),
    "opel_vectra_a": ("A", "1988-1995", None),
    "opel_omega_a": ("A", "1986-1994", None),
    "toyota_carina_e": ("E", "1992-1997", None),
    "nissan_almera_n15": ("N15", "1995-2000", None), "nissan_almera_n15_abs": ("N15", "1995-2000", None),
    "mitsu_lancer_evo_x": ("X", "2007-2017", "Evolution"), "honda_civic_typer_fk8": ("X", "2017-2022", "Type-R FK8"),
}


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
    # margisona(d) eest ara; "Range Rover" jääb mudelinimeks
    for pre in sorted({make, "VW", "Mercedes", "Lada", "VAZ",
                       "Land Rover", "Škoda", "Citroën"}, key=len,
                      reverse=True):
        if rest.startswith(pre + " "):
            rest = rest[len(pre) + 1:]
            break
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
    elif model == "Range" and tail[:1] == ["Rover"]:
        tail = tail[1:]
        if tail and tail[0] in ("Sport", "Evoque", "Velar"):
            model, tail = "Range Rover " + tail[0], tail[1:]
        else:
            model = "Range Rover"
    elif model in ("Grand", "Model", "Land", "Santa", "Space",
                   "Grande", "Atto") and tail:
        model, tail = model + " " + tail[0], tail[1:]
    elif tail and (model, tail[0]) in _MUDEL2:
        model, tail = model + " " + tail[0], tail[1:]
    elif tail[:2] == ["Cross", "Country"]:
        model, tail = model + " Cross Country", tail[2:]
    elif model in ("C3", "C4", "C5") and tail and tail[0] in ("Picasso", "Aircross"):
        model, tail = model + " " + tail[0], tail[1:]
    elif tail and tail[0] in ("Cross", "S-Cross", "Mach-E"):
        # Yaris Cross, Corolla Cross, Eclipse Cross, SX4 S-Cross, Mustang Mach-E
        model, tail = model + " " + tail[0], tail[1:]
    model = _MUDEL_NIMI.get(model, model)
    # polvkonnakood (roomlane, taht, W212, B8, E46, 8V...) voib olla KUS
    # TAHES sabas -- ta laheb aasta juurde, mootor jaab variandiks.
    # NB: kahetäheline kood (BK, GH, KF, TM ...) on põlvkond, aga EV / SR /
    # LR / SW ei ole; Volvo D4/D5 on mootor; 4S (Taycan) on variant.
    GEN = re.compile(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X|[A-CE-Z]|"
                     r"(?!EV$|SR$|LR$|GT$|RS$|ST$|SW$)[A-Z]{2}|"
                     + (r"(?![BDPT]\d$)" if make == "Volvo" else "") +
                     r"[A-Z]{1,2}\d{1,3}[A-Z]?|\d{1,3}|Mk\d|"
                     r"(?!4S$)\d[A-Z])$")
    pinned = []
    # 520d / E220 on variant; aga BMW X1 E84 / Mercedes A-klass W169 on põlvkond
    SASSII = {"BMW": r"^[EFGU]\d{2}$", "Mercedes-Benz": r"^[WXHV]\d{3}$"}
    if make in SASSII and tail and not re.match(SASSII[make], tail[0]):
        pinned = [tail.pop(0)]
    gen = [t for t in tail if GEN.match(t)]
    tail = pinned + [t for t in tail if not GEN.match(t)]
    variant = " ".join(tail)
    fix = _VALIK_PARANDUS.get(v.get("key"))
    if fix:
        gen = [fix[0]] if fix[0] else []
        years = fix[1]
        if fix[2] is not None:
            variant = fix[2]
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

    # --- variandid ja mõõt-nimega "mudelid" emamudelisse (SEO samm 5)
    from pidurdus.koondamine import koonda
    suunamised = koonda(mud, slugify)
    with open(os.path.join(OUT, "suunamised.json"), "w", encoding="utf-8") as f:
        json.dump(dict(sorted(suunamised.items())), f, ensure_ascii=False,
                  separators=(",", ":"))

    # --- moodud
    sizes = Counter(r["mootN"] for r in rows)
    size_list = [{"m": s, "label": pretty_size(s), "slug": size_slug(s),
                  "n": n} for s, n in sizes.most_common() if size_slug(s)]

    # --- EPREL moodu kaupa
    per = defaultdict(list)
    for k, m in mud.items():
        for z in m["sizes"]:
            per[z["m"]].append([
                m["slug"], m["mark"],
                m["nimi"] + (" " + z["v"] if z.get("v") else ""),
                KAT_NR.index(m["kat"]),
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
    alias = veh_alias()
    for k, v in VEHICLES.items():
        if k in alias:          # ABS-iga paaririda -> baasrea absOpt
            continue
        d = _veh(k, v)
        d.update(parse_vehicle(d))
        vehicles.append(d)

    # --- tehase mootorid põlvkonna kaupa (mootorid.py)
    from .mootorid_eksport import attach as _mootorid
    print("mootorid:", _mootorid(vehicles))

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
        "vehAlias": alias,
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
          f"{len(per)} moodu faili, {len(suunamised)} vana aadressi suunatud")
    return core


if __name__ == "__main__":
    main()
