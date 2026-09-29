"""Mootorite nimekirja import: agentide JSON-failid -> mootorid.py.

    python3 -m mudel.mootorid_import <kaust>/out/*.json

Sisend (üks objekt põlvkonna kohta, vt mootorid.py päist):
  {"group": "<võti>", "src": [...], "engines": [{"label","hp","kw","fuel",
   "years","drive"}], "note": "..."}

Tühjad ("engines": []) jäetakse vahele -- see tähendab "ei saadud kätte",
mitte "mootoreid pole". Olemasolevad kirjed mootorid.py-s jäävad alles,
kui uus fail sama põlvkonda ei kata.
"""
import json
import os
import sys

FUEL = {"bensiin": "b", "diisel": "d", "hübriid": "h", "pistikhübriid": "p",
        "elekter": "e", "gaas": "g", "bensiin/gaas": "bg"}
# Elektriauto eraldi read, mille allikaleht on ühine sisepõlemismootoriga
# mudeliga: neile ainult elektrilised versioonid.
AINULT_ELEKTER = {"volvo_xc40_p8", "hyundai_kona_ev"}
OUT = os.path.join(os.path.dirname(__file__), "mootorid.py")


def _load_existing():
    try:
        from .mootorid import MOOTORID
        return dict(MOOTORID)
    except Exception:
        return {}


def main(paths):
    data = _load_existing()
    for p in paths:
        for it in json.load(open(p, encoding="utf-8")):
            eng = it.get("engines") or []
            if not eng:
                continue
            rows, seen = [], set()
            for e in eng:
                lab = " ".join(str(e.get("label") or "").split())
                hp = e.get("hp")
                if not lab or not isinstance(hp, int) or hp <= 0:
                    continue
                kw = e.get("kw") if isinstance(e.get("kw"), int) else round(hp * 0.7355)
                if abs(kw - hp * 0.7355) > 3:      # allikas segas hj/PS ja kW-d
                    kw = round(hp * 0.7355)
                fu = FUEL.get((e.get("fuel") or "").strip().lower(), "b")
                drv = e.get("drive") or ""
                k = (lab.lower(), hp, drv)
                if k in seen:
                    continue
                seen.add(k)
                rows.append((lab, hp, kw, fu, str(e.get("years") or ""), drv))
            if it["group"] in AINULT_ELEKTER:
                rows = [r for r in rows if r[3] == "e"]
            if rows:
                data[it["group"]] = {"src": [s for s in (it.get("src") or []) if s][:6],
                                     "eng": rows}
    with open(OUT, "w", encoding="utf-8") as f:
        f.write('# -*- coding: utf-8 -*-\n"""TEHASE MOOTORID põlvkonna kaupa -- loodud automaatselt.\n\n'
                "Tee uuesti: python3 -m mudel.mootorid_import <agentide JSON-id>\n"
                "Allikas: auto-data.net generatsioonilehed (Euroopa mootorid), vajadusel\n"
                "Wikipedia; iga kirje juures 'src'. Võti = põlvkonna esimene rida\n"
                "(presets/vehicles_ee järjekorras).\n\n"
                "eng: (nimi, hj, kW, kütus, aastad, vedu)\n"
                "kütus: b bensiin, d diisel, h hübriid, p pistikhübriid, e elekter,\n"
                "       g gaas, bg bensiin/gaas\n\n"
                "NB: mootor muudab arvutuses ainult nime. Mass, pidurid ja rehvid tulevad\n"
                "põlvkonna reast (vt mootorid_eksport.py) -- mootorite massi ei ole\n"
                "siia kogutud.\n\"\"\"\n\nMOOTORID = {\n")
        for g in sorted(data):
            d = data[g]
            f.write(f"    {g!r}: {{\n        'src': {d['src']!r},\n        'eng': [\n")
            for r in d["eng"]:
                f.write(f"            {tuple(r)!r},\n")
            f.write("        ]},\n")
        f.write("}\n")
    print(len(data), "põlvkonda,", sum(len(d["eng"]) for d in data.values()), "mootorit ->", OUT)


if __name__ == "__main__":
    main(sys.argv[1:])
