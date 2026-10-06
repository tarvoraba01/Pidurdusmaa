# -*- coding: utf-8 -*-
"""Rakendab eprel_moot.puhas_moot olemasolevatele veebi andmefailidele
ilma kogu eksporti uuesti jooksutamata (öövahetus 7.10.2026).

  python3 mudel/eprel_moot_rakenda.py veeb/static/data

* eprel/<vigane võti>.json read liidetakse õige mõõdu faili (koonda_read:
  üks rida mudeli kohta), vigane fail eemaldatakse
* LT- ja 17,5-tolliste (veoauto) mõõtude failid jäävad nagu olid (neil pole
  mõõdulehte; mudel ja tema leht jäävad alles)
* core.json: eprelSizes ja sizes[].n arvutatakse uuesti
* models.json: mudeli mõõtude võti parandatakse (LT jm jääb, nagu oli)
Tulevased ekspordid (export_wp.py) kasutavad sama funktsiooni.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from eprel_moot import puhas_moot  # noqa: E402
from eprel_dedup import koonda_read  # noqa: E402

OK = re.compile(r"^\d{5}R\d{2}C?$")
SRC = os.path.join(os.path.dirname(__file__), "eprel_tyres.json")


def votti(r):
    return r["mootN"] if OK.match(r["mootN"]) else puhas_moot(r["moot"])


def label(m):
    x = re.match(r"^(\d{3})(\d{2})R(\d{2})(C?)$", m)
    return f"{x[1]}/{x[2]} R{x[3]}{x[4]}"


def slug(m):
    x = re.match(r"^(\d{3})(\d{2})R(\d{2})(C?)$", m)
    return f"{x[1]}-{x[2]}-r{x[3]}{'c' if x[4] else ''}"


def dump(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def main(data):
    rows = json.load(open(SRC, encoding="utf-8"))["rehvid"]
    kaart = {}
    for r in rows:
        if not OK.match(r["mootN"]):
            kaart[r["mootN"]] = puhas_moot(r["moot"])
    edir = os.path.join(data, "eprel")
    olemas = {f[:-5] for f in os.listdir(edir) if f.endswith(".json")}
    liidetud, eemaldatud, lisaread = 0, 0, Counter()
    sihtread = defaultdict(list)
    for vigane, siht in sorted(kaart.items()):
        if vigane not in olemas:
            continue
        if not siht:
            eemaldatud += 1  # jääb alles
            continue
        sihtread[siht].extend(json.load(open(os.path.join(edir, vigane + ".json"), encoding="utf-8")))
        liidetud += 1
        os.remove(os.path.join(edir, vigane + ".json"))
    for siht, lisa in sihtread.items():
        p = os.path.join(edir, siht + ".json")
        vana = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
        uus = koonda_read(vana + lisa)
        uus.sort(key=lambda r: ("ABCDE".index(r[4]) if r[4] in "ABCDE" else 9, r[1], r[2]))
        lisaread[siht] = len(uus) - len(vana)
        dump(p, uus)

    n = Counter(votti(r) or r["mootN"] for r in rows)
    cp = os.path.join(data, "core.json")
    core = json.load(open(cp, encoding="utf-8"))
    sizes = core["sizes"]
    on = {s["m"] for s in sizes}
    for s in sizes:
        s["n"] = n[s["m"]]
    uued = [m for m in sihtread if m not in on and OK.match(m)]
    for m in uued:
        sizes.append({"m": m, "label": label(m), "slug": slug(m), "n": n[m]})
    core["sizes"] = sorted(sizes, key=lambda s: -s["n"])
    core["eprelSizes"] = sorted(f[:-5] for f in os.listdir(edir) if f.endswith(".json"))
    dump(cp, core)

    mp = os.path.join(data, "models.json")
    models = json.load(open(mp, encoding="utf-8"))
    mm = 0
    for m in models.values():
        for z in m.get("sizes", []):
            if not OK.match(z["m"]) and kaart.get(z["m"]):
                z["m"] = kaart[z["m"]]
                mm += 1
    dump(mp, models)
    print(f"liidetud {liidetud} vigast mõõdufaili, jäetud alles {eemaldatud} (LT/veoauto), "
          f"uusi mõõte {len(uued)} {uued}, mudelite mõõduvõtmeid parandatud {mm}; "
          f"ridu juurde {sum(lisaread.values())} ({len(lisaread)} mõõtu), "
          f"mõõdufaile nüüd {len(core['eprelSizes'])}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "veeb/static/data")
