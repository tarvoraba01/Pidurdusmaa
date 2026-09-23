# -*- coding: utf-8 -*-
"""MÕÕDETUD klassi keskmised: märgise klass -> märghaardumise indeks G.

MIKS SEE ON OLEMAS
------------------
Märgise klass on vahemik, mitte number. Seni kasutati ainult märgisega
rehvidel vahemiku NOMINAALSET keskpunkti (A = 1,60; B = 1,47; ...).
Testitud rehvidel tuleb G nende enda mõõdetud pidurdusmaast ja seal tuli
välja vastuolu: 225/45 R17 mõõdus testitud A-klassi suverehvide G oli
1,34-1,49, ehk tunduvalt alla nominaalse 1,60. Lehel tähendas see, et rida
"märgise klass A" nägi välja PAREM kui päris testitud A-klassi rehvid.

Nüüd on klassi esindusväärtus MÕÕDETUD: iga (klass, rehvikategooria) paari
kohta võetakse testitud rehvide tuletatud G-de MEDIAAN. Mediaan, mitte
keskmine, sest üksik erand (nt Syron) ei tohi tervet klassi nihutada.

MIKS KATEGOORIA KAASA
---------------------
Sama klass tähendab eri kategooriates eri asja: A-klassi sportrehvi (UHP)
mõõdetud G on mediaanis 1,64, A-klassi tavaline suverehv on 1,47. Klass on
mõõdupõhine ja suhteline võrdlusrehvi suhtes; see vahe on päris ja lehel
nähtav.

LANGEMISJÄRJEKORD
-----------------
  1) (klass, kategooria) mediaan, kui vähemalt MIN_N mõõdetud rehvi;
  2) kui selle kategooria kohta mõõtmisi ei ole: sama klassi mõõdetud
     kategooriate MADALAIM mediaan. Miks madalaim, mitte keskmine: kui me
     ei tea, kas A-klassi talverehv käitub nagu A-klassi sportrehv või
     nagu A-klassi tavaline suverehv, on ohutusnumbri juures aus võtta
     kehvem. Ülehindamine paneks kasutaja arvama, et ta pidurdab paremini
     kui tegelikult;
  3) kui ühtegi mõõtmist ei ole: nominaalne keskpunkt (G_CLASS presets.py).
Iga väärtuse juures on kirjas, mitu mõõdetud rehvi selle taga on -- see
läheb ka lehele nähtavale.

KASUTAMINE
    python3 -m pidurdus.kalibreeri_gklass
kirjutab faili pidurdus/g_class_measured.py.
"""
import collections
import json
import os
import re
import statistics as st
import time

from .presets import G_CLASS, TYRES

MIN_N = 3
HERE = os.path.dirname(__file__)
MODELS = os.path.join(HERE, "..", "theme", "pidurdusmaa", "data", "models.json")
OUT = os.path.join(HERE, "g_class_measured.py")


def _norm(s):
    return re.sub(r"[^0-9RC]", "", (s or "").upper())


def measure():
    models = json.load(open(MODELS, encoding="utf-8"))
    by = collections.defaultdict(list)
    miss = []
    for key, t in TYRES.items():
        if t.g_source != "test":
            continue
        m = models.get(getattr(t, "slug", None) or "")
        if m is None:
            # slug ei ole Tyre-objektil: otsi mark+nimi jargi
            mk = t.name.split()[0].upper()
            nm = re.sub(r"[^A-Z0-9]", "", " ".join(t.name.split()[1:]).upper())
            for slug, mm in models.items():
                if mm["mark"].upper() == mk and re.sub(r"[^A-Z0-9]", "", mm["nimi"].upper()) == nm:
                    m = mm
                    break
        if m is None:
            miss.append((t.name, t.size, "mudelit ei ole margises"))
            continue
        sz = [s for s in m["sizes"] if s["m"] == _norm(t.size)]
        if not sz:
            miss.append((t.name, t.size, "seda mootu ei ole margises"))
            continue
        by[(sz[0]["g"], t.category.name)].append(round(t.wet_grip_index, 4))
    return by, miss


def table(by):
    per_class = collections.defaultdict(list)
    for (g, cat), v in by.items():
        per_class[g] += v
    out = {}
    for g in "ABCDE":
        cls_n = len(per_class[g])
        kat_med = [round(st.median(v), 3) for (gg, _c), v in by.items()
                   if gg == g and len(v) >= MIN_N]
        base = min(kat_med) if kat_med else G_CLASS[g]
        out[g] = {"_": [base, cls_n if kat_med else 0]}
        for (gg, cat), v in sorted(by.items()):
            if gg != g:
                continue
            if len(v) >= MIN_N:
                out[g][cat] = [round(st.median(v), 3), len(v)]
    return out


def main():
    by, miss = measure()
    tbl = table(by)
    src = ['# -*- coding: utf-8 -*-',
           '"""MÕÕDETUD klassi keskmised -- loodud automaatselt.',
           '',
           'Tee see uuesti:  python3 -m pidurdus.kalibreeri_gklass',
           'Miks ja kuidas:  vt kalibreeri_gklass.py paist.',
           '',
           'Kuju: klass -> {"_": [G, n]} pluss (kategooria: [G, n]) seal, kus',
           'mõõdetud rehve on vähemalt %d. n = mitu mõõdetud rehvi väärtuse taga.' % MIN_N,
           'Loodud: %s' % time.strftime("%Y-%m-%d"),
           '"""',
           '',
           'G_CLASS_MEASURED = {']
    for g in "ABCDE":
        src.append('    %r: %r,' % (g, tbl[g]))
    src.append('}')
    open(OUT, "w", encoding="utf-8").write("\n".join(src) + "\n")
    print("mõõdetud rehve klasside kaupa:")
    for (g, cat), v in sorted(by.items()):
        print("   %s %-16s n=%-3d mediaan %.3f  (%.2f...%.2f)"
              % (g, cat, len(v), st.median(v), min(v), max(v)))
    print("\ntabel:")
    for g in "ABCDE":
        print("   ", g, tbl[g])
    if miss:
        print("\nvälja jäänud (%d):" % len(miss))
        for x in miss[:12]:
            print("   ", x)


if __name__ == "__main__":
    main()
