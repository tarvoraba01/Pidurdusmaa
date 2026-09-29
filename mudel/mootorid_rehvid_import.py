"""Mootori kaupa tehase rehvimõõdud ja tühimass: agentide JSON -> mootorid_rehvid.py.

    python3 -m pidurdus.mootorid_rehvid_import <kaust>/out/*.json

Sisend (üks objekt põlvkonna kohta):
  {"group": "<mootorid.py võti>", "engines": [{"label","hp","drive","kg",
   "tyres": ["225/45 R17", ...], "src": "<auto-data modifikatsiooni leht>"}]}

Allikas: auto-data.net modifikatsiooni leht ("Kerb Weight", "Tires size").
Tühjad ("tyres": [] ja "kg": null) jäetakse vahele. Olemasolevad kirjed
jäävad alles, kui uus fail sama mootorit ei kata.
"""
import json
import os
import re
import sys

from .mootorid_eksport import _slug

OUT = os.path.join(os.path.dirname(__file__), "mootorid_rehvid.py")
RX = re.compile(r"(\d{3})\s*/\s*(\d{2})\s*Z?R?F?\s*(\d{2})\b")


def norm(s):
    m = RX.search(str(s or "").upper())
    if not m:
        return None
    w, a, r = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not (125 <= w <= 355 and 25 <= a <= 85 and 12 <= r <= 23):
        return None
    return f"{w}/{a} R{r}"


def _load_existing():
    try:
        from .mootorid_rehvid import RATTAD
        return {g: dict(v) for g, v in RATTAD.items()}
    except Exception:
        return {}


def main(paths):
    data = _load_existing()
    n_new = 0
    for p in paths:
        try:
            items = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print("VIGA", p, e)
            continue
        for it in items:
            g = it.get("group")
            for e in it.get("engines") or []:
                lab, hp = " ".join(str(e.get("label") or "").split()), e.get("hp")
                if not lab or not isinstance(hp, int):
                    continue
                kg = e.get("kg")
                kg = kg if isinstance(kg, int) and 500 <= kg <= 4000 else None
                sz = []
                for s in e.get("tyres") or []:
                    n = norm(s)
                    if n and n not in sz:
                        sz.append(n)
                if not kg and not sz:
                    continue
                data.setdefault(g, {})[_slug(lab, hp, e.get("drive") or "")] = (
                    kg, tuple(sz[:8]), str(e.get("src") or "")[:200])
                n_new += 1
    with open(OUT, "w", encoding="utf-8") as f:
        f.write('# -*- coding: utf-8 -*-\n"""MOOTORI KAUPA tehase rehvimõõdud ja tühimass -- loodud automaatselt.\n\n'
                "Tee uuesti: python3 -m pidurdus.mootorid_rehvid_import <agentide JSON-id>\n"
                "Allikas: auto-data.net modifikatsiooni lehed (Kerb Weight, Tires size).\n"
                "Kogutud sportlikele ja elektrifitseeritud versioonidele, mille rehvid ja\n"
                "mass erinevad põlvkonna põhireast kõige rohkem.\n\n"
                "RATTAD[põlvkond][mootori slug] = (tühimass kg | None, (mõõdud...), allikas)\n"
                "Esimene mõõt = selle versiooni põhimõõt (auto-data järjekord).\n\"\"\"\n\nRATTAD = {\n")
        for g in sorted(data):
            f.write(f"    {g!r}: {{\n")
            for s in sorted(data[g]):
                f.write(f"        {s!r}: {tuple(data[g][s])!r},\n")
            f.write("    },\n")
        f.write("}\n")
    print(n_new, "kirjet imporditud;", len(data), "põlvkonda,",
          sum(len(v) for v in data.values()), "mootorit ->", OUT)


if __name__ == "__main__":
    main(sys.argv[1:])
