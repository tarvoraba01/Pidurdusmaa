# -*- coding: utf-8 -*-
"""Poe kataloogist tulnud rehvimudelid, mida EPREL-is (meie korjes) ei ole.

  python3 mudel/pood_rakenda.py veeb/static/data

Allikas: mudel/pood_rehvid.json — read kujul
  {"pood": "rehvivahetus.ee", "mark": "Nordexx", "mudel": "NS9200",
   "moot": "23550R17", "eu": "c c b 72dB", "lisi": "100W XL FR"}
EL-i märgist kannab iga alates 2012 müüdud rehv ja pood peab seda näitama;
EPREL on 2021. aastast ainult sama deklaratsiooni register. Seega on poe
`eu` väli sama tootja deklaratsioon — aga käsitsi sisestatud, mitte registrist.
Sellepärast:
  * mudel saab `allikas: "pood"` ja `pood: "<pood>"`, leht ütleb selle välja
  * mõõdurea lipp 16 = märgis poe andmetel
  * märghaardeklass: HALVIM, kui sama mõõdu read erinevad (nagu EPREL-is)
  * ilma märghaardeklassita rida (naastrehv, „-“) jäetakse vahele — naastud
    tulevad ainult testidega (core.json), mitte siit
  * mudel, mille slug on juba olemas (EPREL või test), jäetakse vahele —
    sidumine (sobitus.js) peab selle poe toote niikuinii olemasolevaga kokku viima
Kategooria tuleb NIMEST (eprel_convert LAMELL/TALV + Põhjamaade muster) või
käsitsi tabelist KAT_KASITSI — poe voos lume-/jäämärgist ei ole.
"""
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from eprel_convert import LAMELL, TALV  # noqa: E402
from eprel_dedup import koonda_read  # noqa: E402

SRC = os.path.join(os.path.dirname(__file__), "pood_rehvid.json")
OK = re.compile(r"^\d{5}R\d{2}C?$")
KAT_NR = ["SUMMER_TOURING", "ALL_SEASON", "WINTER_CENTRAL", "WINTER_NORDIC"]
LIPP_POOD = 16
# Põhjamaade lamell: nimi ütleb jääd/põhja. „UG Ice“, „IceGuard“, „Nord Frost“ jne
NORDIC = re.compile(r"\bICE\b|ICE\s?\d|ICEGUARD|NORD|ARCTIC|VIKING|HAKKAPELIITTA R|\bIZ\d|G075|\bIG\d\d|SIBERIA|X-ICE", re.I)  # „EuroFrost“ on Kesk-Euroopa, „NordFrost“ püüab NORD
# Mudelid, mille nimi ei ütle tüüpi (tootja lehe järgi)
KAT_KASITSI = {
    "triangle|pl01": "WINTER_NORDIC",       # Triangle SnowLink PL01, Põhjamaade lamell
    "triangle|pl02": "WINTER_NORDIC",       # SnowLink PL02 SUV
    "rotalla|w race s330": "WINTER_CENTRAL",
    "goodride|sw612": "WINTER_CENTRAL",      # kaubiku talverehv
    "nordexx|wintersafe n2": "WINTER_NORDIC",  # N = Nordic, kiirusklass S/T
    "general tire|grabber at3": "ALL_SEASON",  # all-terrain, 3PMSF, aastaringne
    "general tire|grabber at3 lt": "ALL_SEASON",
    "continental|vancofourseasons2": "ALL_SEASON",
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9+/ ]", " ", s.lower())).strip()


def slugify(s):
    s = norm(s).replace("+", " plus ").replace("/", " ")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def kategooria(mark, mudel):
    k = KAT_KASITSI.get(norm(mark) + "|" + norm(mudel))
    if k:
        return k, "POOD kasitsi"
    n = mudel
    if NORDIC.search(n):
        return "WINTER_NORDIC", "POOD nimi"
    if LAMELL.search(n):
        return "ALL_SEASON", "POOD nimi"
    if TALV.search(n):
        return "WINTER_CENTRAL", "POOD nimi"
    return "SUMMER_TOURING", "POOD nimi (talve/lamelli sõna puudub)"


def loe_eu(eu):
    """'c b b 70dB' | 'c b 70' | 'DCB' | 'C B B' -> (kytus, marg, muraKl, dB) või None.
    Vana märgis (2012): kütus, märg, dB. Uus (2021): kütus, märg, müraklass [dB]."""
    s = str(eu or "").strip().upper().replace("DB", "")
    if not s or s == "-":
        return None
    s = re.sub(r"\s+", " ", s)
    if re.fullmatch(r"[A-G]{2,3}", s):           # „DCB“
        s = " ".join(s)
    osad = s.split(" ")
    tahed = [o for o in osad if re.fullmatch(r"[A-G]", o)]
    arvud = [int(o) for o in osad if re.fullmatch(r"\d{2}", o)]
    if len(tahed) < 2:
        return None
    kytus, marg = tahed[0], tahed[1]
    if marg in "FG":
        marg = "E"      # vana (2012) märgise F/G: meie skaala lõpeb E-ga, võtame halvima teadaoleva
    mura_kl = tahed[2] if len(tahed) > 2 else None
    db = arvud[0] if arvud else None
    return kytus, marg, mura_kl, db


def loe_lisi(lisi):
    m = re.match(r"\s*(\d{2,3})(?:/(\d{2,3}))?\s*([A-Z])\b", str(lisi or "").upper())
    if not m:
        return [], []
    li = [int(m.group(1))]
    return li, [m.group(3)]


def main(data):
    read = json.load(open(SRC, encoding="utf-8"))["read"]
    mp = os.path.join(data, "models.json")
    models = json.load(open(mp, encoding="utf-8"))
    cp = os.path.join(data, "core.json")
    core = json.load(open(cp, encoding="utf-8"))
    test_slugs = {t.get("slug") for t in core.get("tyres", [])}
    edir = os.path.join(data, "eprel")

    # vanad poe-mudelid välja: skript on idempotentne (sama sisend -> sama tulemus)
    vanad = {s for s, m in models.items() if m.get("allikas") == "pood"}
    for s in vanad:
        del models[s]
    for f in os.listdir(edir):
        if not f.endswith(".json"):
            continue
        p = os.path.join(edir, f)
        lst = json.load(open(p, encoding="utf-8"))
        uus = [r for r in lst if not (len(r) > 8 and isinstance(r[8], int) and r[8] & LIPP_POOD)]
        if len(uus) != len(lst):
            if uus:
                json.dump(uus, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
            else:
                os.remove(p)

    grp = defaultdict(list)
    for r in read:
        if not OK.match(r.get("moot") or ""):
            continue
        if not loe_eu(r.get("eu")):
            continue
        grp[(r["mark"].strip(), r["mudel"].strip(), r.get("pood", "pood"))].append(r)

    stat = Counter()
    uued = {}
    per = defaultdict(list)
    for (mark, mudel, pood), g in sorted(grp.items()):
        slug = slugify(mark + " " + mudel)
        if slug in models or slug in test_slugs:
            stat["juba olemas"] += 1
            continue
        kat, alus = kategooria(mark, mudel)
        moodud = defaultdict(list)
        for r in g:
            moodud[r["moot"]].append(r)
        sizes = []
        for moot, rr in sorted(moodud.items()):
            lab = [loe_eu(r["eu"]) for r in rr]
            margid = sorted({x[1] for x in lab}, key="ABCDEFG".index)
            marg = margid[-1]                       # halvim
            esimene = next(x for x in lab if x[1] == marg)
            li, si = set(), set()
            for r in rr:
                a, b = loe_lisi(r.get("lisi"))
                li.update(a)
                si.update(b)
            sizes.append({"m": moot, "g": marg, "gAll": margid, "f": esimene[0],
                          "db": esimene[3], "nk": esimene[2], "li": sorted(li), "si": sorted(si),
                          "snow": kat != "SUMMER_TOURING", "ice": False})
        uued[slug] = {"mark": mark, "kat": kat, "katAlus": alus, "sizes": sizes,
                      "nimi": mudel, "allikas": "pood", "pood": pood}
        stat[kat] += 1
        for z in sizes:
            per[z["m"]].append([slug, mark, mudel, KAT_NR.index(kat), z["g"], z["f"], z["db"], z["nk"],
                                LIPP_POOD | (2 if len(z["gAll"]) > 1 else 0) | (4 if z["snow"] else 0), None])

    models.update(uued)
    json.dump(models, open(mp, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

    uued_moodud = []
    for moot, lisa in per.items():
        p = os.path.join(edir, moot + ".json")
        vana = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
        if not vana:
            uued_moodud.append(moot)
        uus = koonda_read(vana + lisa)
        uus.sort(key=lambda r: ("ABCDE".index(r[4]) if r[4] in "ABCDE" else 9, r[1], r[2]))
        json.dump(uus, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

    # core.json: eprelSizes ja sizes[].n (sama loogika nagu eprel_moot_rakenda)
    n = Counter()
    for m in models.values():
        for z in m.get("sizes", []):
            n[z["m"]] += 1
    sizes = core["sizes"]
    on = {s["m"] for s in sizes}
    for s in sizes:
        s["n"] = n[s["m"]]
    for m in uued_moodud:
        if m not in on:
            x = re.match(r"^(\d{3})(\d{2})R(\d{2})(C?)$", m)
            sizes.append({"m": m, "label": f"{x[1]}/{x[2]} R{x[3]}{x[4]}",
                          "slug": f"{x[1]}-{x[2]}-r{x[3]}{'c' if x[4] else ''}", "n": n[m]})
    core["sizes"] = sorted(sizes, key=lambda s: -s["n"])
    core["eprelSizes"] = sorted(f[:-5] for f in os.listdir(edir) if f.endswith(".json"))
    json.dump(core, open(cp, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

    print(f"poe mudeleid juurde {len(uued)} ({sum(len(m['sizes']) for m in uued.values())} mõõturida, "
          f"{len(per)} mõõtu, uusi mõõdufaile {len(uued_moodud)}); vahele: {dict(stat)}")
    for s, m in sorted(uued.items()):
        print(f"  {m['mark']} {m['nimi']}: {m['kat']} [{m['katAlus']}] {len(m['sizes'])} mõõtu")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "veeb/static/data")
