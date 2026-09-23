# -*- coding: utf-8 -*-
"""EPREL-i korje -> mudeli rehvinimekiri.

SISEND   eprel2.json (moot x mark korje, vt eprel_harvest.py)
VALJUND  pidurdus/eprel_tyres.json, mille presets.py laeb sisse

MIDA EPREL ANNAB JA MIDA MITTE -- see maarab kogu teisenduse
------------------------------------------------------------
ANNAB:  marghaardumise KLASS (A-E), moot, mark, kaubanduslik nimi,
        3PMSF-i linnuke, jaamargis, koormus- ja kiirusindeks, mura.
EI ANNA: numbrilist G-d, kuiva haaret, lume/jaa MEETREID, mustrisugavust.

Seega saavad need rehvid:
  * G = klassi KESKPUNKT (g_from_class), mitte oma moodetud number
  * g_source="label", millest jareldub sigma_label_only (+4,5 %)
  * kuiv ja lumi/jaa kategooria keskmisest, mitte oma mootmisest
Lehel tahendab see tarni ja laiemat veapiiri. See ei ole puudus, mida
peita -- see on tapselt see, mida margis teab.

KOLM OTSUST, MIS ON MOODETUD, MITTE PAKUTUD
-------------------------------------------
1. MARGI KIRJUVIIS. Korjes oli 103 kirjuviisi ("MICHELIN", "Michelin",
   "KUMHO WP52" -- margi valjas oli mudelikood kaasa kirjutatud).
   Normaliseerimine viib need 31 margile. Kahesonalised margid
   (Nokian Tyres, GT Radial, Point S) on eraldi nimekirjas, muidu
   loikaks esimene sona neid valesti.

2. VASTUOLULINE KLASS. 7 % mudel+moot paaridest andis KAKS eri
   marghaardumise klassi (nt Bridgestone Ecopia EP150 195/65R15 oli
   A, B ja C). Pohjus on paris: sama mudel sama moodu sees eri koormus-
   ja kiirusindeksiga on eri registreering ja voib olla eri klassiga.
   Mudel votab HALVIMA klassi ja jatab meelde koik klassid. Halvim,
   sest ohutusnumbri juures on alahindamine parem kui ulehindamine, ja
   sest kasutaja ei tea poes, kumma variandi ta kaes hoiab.

3. KATEGOORIA. Margis EI UTLE suvi/talv/lamell. Ta utleb ainult kaks
   linnukest: 3PMSF ja jaamargis. Sellest tuleb:
       jaamargis          -> Pohjamaade talverehv   (margisest)
       3PMSF + nimi utleb -> lamell voi talv        (NIMEST, noorem tond)
       3PMSF + ei utle    -> talverehv              (oletus, margitud)
       ei kumbagi         -> suverehv               (margisest)
   Iga rehv kannab kaasa valja `kat_alus`, mis utleb, kumb tee teda tõi.
   Nii ei ole oletus ja mootmine samas kastis.
"""
import json
import re
import sys
from collections import defaultdict

CLASS_MID = {"A": 1.60, "B": 1.47, "C": 1.32, "D": 1.17, "E": 1.05}   # nominaalsed

# MÕÕDETUD klassi väärtused (vt kalibreeri_gklass.py). Kui mõõdetud rehve
# selle klassi ja kategooria kohta on, kasutame neid -- muidu nominaalset.
try:
    from .g_class_measured import G_CLASS_MEASURED
except ImportError:                                   # skriptina jooksutades
    from g_class_measured import G_CLASS_MEASURED


def g_mid(klass, kat):
    t = G_CLASS_MEASURED.get(klass) or {}
    if kat in t:
        return t[kat][0]
    if "_" in t and t["_"][1]:
        return t["_"][0]
    return CLASS_MID[klass]
HALVIM = ["A", "B", "C", "D", "E"]          # jarjekord: A parim

KAKSSONA = {
    "NOKIAN TYRES": "Nokian", "HANKOOK TIRE": "Hankook",
    "GT RADIAL": "GT Radial", "POINT S": "Point S",
    "STAR PERFORMER": "Star Performer", "TOYO TIRES": "Toyo",
    "NEXENTIRE": "Nexen", "DOUBLE COIN": "Double Coin",
    "BFGOODRICH": "BFGoodrich", "GITI": "Giti",
}

# Nimemustrid. Need EI OLE fuusika -- need on sonatuvastus ja neid
# hoitakse eraldi, et oleks nahtav, mis tuli nimest ja mis margiselt.
LAMELL = re.compile(
    r"ALL.?SEASON|ALL.?WEATHER|4.?SEASON|FOUR.?SEASON|CROSSCLIMATE|"
    r"QUATRAC|QUADRAXER|VECTOR|SEASONPROOF|MULTI.?ACTION|MULTISEASON|"
    r"\bAS\s?\d|\bA/S\b|CINTURATO ALL|WEATHER.?CONTROL|WEATHER.?READY|"
    r"CROSS.?SEASON|CITY.?4S|CAMPER.?4|CRUGEN.?HP71", re.I)
TALV = re.compile(
    r"WINTER|SNOW|\bICE\b|ALPIN|BLIZZAK|HAKKA|FROST|NORDIC|"
    r"ULTRA.?GRIP|SOTTOZERO|KRISALP|\bWP\s?\d|\bWS\s?\d|\bWI\s?\d|"
    r"SNOWPROOF|LATITUDE ALPIN|PILOT ALPIN|SPEED.?GRIP|"
    r"NORTH|POLAR|GLACIER|EVEREST|WINTERHAWK|IZ\d|SPIKE", re.I)


def mark_norm(m):
    s = re.sub(r"\s+", " ", str(m or "").strip()).upper()
    for k, v in KAKSSONA.items():
        if s.startswith(k):
            return v
    if not s:
        return "?"
    p = s.split()[0]
    return p if p.isupper() and len(p) <= 3 else p.title()


def _halvim(klassid):
    k = sorted((c for c in klassid if c in HALVIM),
               key=HALVIM.index)
    return k[-1] if k else None


def kategooria(nimi, lumi, jaa):
    """-> (kategooria, millele see tugineb)"""
    if jaa:
        return "WINTER_NORDIC", "margis (jaamargis)"
    if not lumi:
        return "SUMMER_TOURING", "margis (3PMSF puudub)"
    n = str(nimi or "")
    if LAMELL.search(n):
        return "ALL_SEASON", "nimi"
    if TALV.search(n):
        return "WINTER_CENTRAL", "nimi"
    return "WINTER_CENTRAL", "OLETUS (3PMSF, nimi ei utle)"


def main(path_in, path_out):
    rows = json.load(open(path_in, encoding="utf-8"))["rehvid"]
    grp = defaultdict(list)
    for r in rows:
        if r.get("blok") or r.get("staatus") != "PUBLISHED":
            continue
        nimi = (r.get("nimi") or "").strip()
        if not nimi:
            continue                       # ilma nimeta ei ole valijale kasu
        grp[(mark_norm(r.get("mark")), nimi.upper(), r.get("mootN"))].append(r)

    out, stat = [], defaultdict(int)
    for (mark, nimi_up, mootN), g in sorted(grp.items()):
        klassid = sorted({x.get("marg") for x in g if x.get("marg")},
                         key=lambda c: HALVIM.index(c) if c in HALVIM else 9)
        if not klassid:
            continue
        halvim = klassid[-1]
        nimi = g[0].get("nimi")
        kat, alus = kategooria(nimi, g[0].get("lumi"), g[0].get("jaa"))
        stat[alus] += 1
        if len(klassid) > 1:
            stat["vastuoluline klass"] += 1
        out.append({
            "mark": mark,
            "nimi": nimi,
            "moot": g[0].get("moot"),
            "mootN": mootN,
            "kat": kat,
            "kat_alus": alus,
            "klass": halvim,
            "klassid": klassid,
            "G": g_mid(halvim, kat),
            "lumi": bool(g[0].get("lumi")),
            "jaa": bool(g[0].get("jaa")),
            "tyreClass": g[0].get("klass"),
            "koormus": sorted({x.get("koormus") for x in g if x.get("koormus")}),
            "kiirus": sorted({x.get("kiirus") for x in g if x.get("kiirus")}),
            "regid": sorted({x.get("reg") for x in g})[:4],
            # AMETLIKUD margiseandmed rehvivordluse jaoks. Kutuseklass ja
            # mura EI LAHE pidurdusmudelisse (kytus_katse.py naitas, et
            # kutuseklass ei seleta G-d) -- nad on siin ainult selleks, et
            # vordlusleht saaks naidata margise enda arve.
            # Halvim voidab, nagu marghaardeklassi puhul: kasutaja ei tea
            # poes, millist koormus-/kiirusindeksi varianti ta kaes hoiab.
            "kytus": _halvim({x.get("kytus") for x in g}),
            "kytused": sorted({x.get("kytus") for x in g if x.get("kytus")}),
            "muraDb": max((x.get("muraDb") for x in g
                           if isinstance(x.get("muraDb"), (int, float))),
                          default=None),
            "muraKl": _halvim({x.get("muraKl") for x in g}),
        })

    json.dump({"allikas": "EPREL (Euroopa Komisjon)",
               "teisendatud": __doc__.splitlines()[0],
               "rehve": len(out), "rehvid": out},
              open(path_out, "w", encoding="utf-8"), ensure_ascii=False)

    print(f"{len(rows)} kirjet -> {len(out)} eristuvat mark+nimi+moot")
    for k, v in sorted(stat.items(), key=lambda x: -x[1]):
        print(f"   {k:<34} {v}")
    kat = defaultdict(int)
    for o in out:
        kat[o["kat"]] += 1
    print("   ---")
    for k, v in sorted(kat.items(), key=lambda x: -x[1]):
        print(f"   {k:<34} {v}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2
         else "pidurdus/eprel_tyres.json")
