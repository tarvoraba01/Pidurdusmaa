# -*- coding: utf-8 -*-
"""Kas EPREL-i kutuseklass seletab moodetud G hajuvust?

SISEND  /tmp/kytus_seos.json (kytus_katse.py valjund, 41 kontrollitud vastet)
MEETOD  Kategooria on alati sees (ta seletab enamiku hajuvusest). Kusimus
        on, kas kutuseklass lisab MIDAGI kategooria peale.

KAKS MUDELIT, VORDLUS LEAVE-ONE-OUT RUUTVEAGA
    M0:  G = kategooria keskmine
    M1:  G = kategooria keskmine + b * kutus
M1 on parem ainult siis, kui ta LOO-viga on vaiksem. Mitte siis, kui
tema R2 on suurem -- R2 kasvab alati, kui parameeter lisada.

MARK: EPREL-i marghaardeklassi ei saa siin kontrollmuutujana kasutada,
sest meie moodetud rehvidel EI OLE soltumatut ametlikku klassi
(anchors_adac.py rida 84: klass on tuletatud sellestsamast testist) ja
korjes ei ole neid moote, milles ADAC testis. Seega on kusimus siin
kitsam kui ideaalis: kas kutuseklass seletab G-d kategooria sees.
"""
import json
from collections import defaultdict
from statistics import mean

KL = {"A": 5.0, "B": 4.0, "C": 3.0, "D": 2.0, "E": 1.0}


def lae(path="/tmp/kytus_seos.json"):
    rows = json.load(open(path, encoding="utf-8"))
    out = []
    for r in rows:
        k = [KL[c] for c in r["kytus"] if c in KL]
        m = [KL[c] for c in r["marg"] if c in KL]
        if not k:
            continue
        out.append({"nimi": r["nimi"], "kat": r["kat"], "G": r["G"],
                    "kytus": mean(k), "marg": mean(m) if m else None,
                    "n": r["n_rida"], "hajub": len(r["kytus"]) > 1})
    return out


def sobita(tr):
    """Kategooria keskmine + uhine kaldenurk kutuse jaoks (OLS kahes samus)."""
    kesk = defaultdict(list)
    for r in tr:
        kesk[r["kat"]].append(r["G"])
    kesk = {k: mean(v) for k, v in kesk.items()}
    xs = [r["kytus"] for r in tr]
    ys = [r["G"] - kesk[r["kat"]] for r in tr]
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return kesk, 0.0, mx
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return kesk, b, mx


def ennusta(mudel, r, kasuta_kytust):
    kesk, b, mx = mudel
    g = kesk.get(r["kat"])
    if g is None:
        return None
    return g + (b * (r["kytus"] - mx) if kasuta_kytust else 0.0)


def loo(data, kasuta_kytust):
    vead = []
    for i in range(len(data)):
        tr = data[:i] + data[i + 1:]
        p = ennusta(sobita(tr), data[i], kasuta_kytust)
        if p is None:
            continue
        vead.append((p - data[i]["G"]) ** 2)
    return (sum(vead) / len(vead)) ** 0.5, len(vead)


def main():
    d = lae()
    print(f"VASTEID {len(d)}   (neist {sum(1 for r in d if r['hajub'])} "
          f"puhul andis EPREL mitu kutuseklassi -> voeti keskmine)\n")

    kat = defaultdict(list)
    for r in d:
        kat[r["kat"]].append(r)
    for k, v in sorted(kat.items()):
        print(f"  {k:<16} n={len(v):<3} G {min(x['G'] for x in v):.3f}"
              f"..{max(x['G'] for x in v):.3f}   kutus keskm "
              f"{mean(x['kytus'] for x in v):.2f}")

    kesk, b, mx = sobita(d)
    print(f"\nKALDENURK   b = {b:+.4f} G-uhikut kutuseklassi sammu kohta")
    print(f"            (A->B->C->D->E samm = {abs(b):.4f} G)")

    # korrelatsioon kategooria sees
    xs = [r["kytus"] for r in d]
    ys = [r["G"] - kesk[r["kat"]] for r in d]
    mxx, myy = mean(xs), mean(ys)
    sx = sum((x - mxx) ** 2 for x in xs) ** 0.5
    sy = sum((y - myy) ** 2 for y in ys) ** 0.5
    rr = (sum((x - mxx) * (y - myy) for x, y in zip(xs, ys)) / (sx * sy)
          if sx and sy else 0.0)
    print(f"KORRELATSIOON r = {rr:+.3f}   (R2 = {rr*rr:.3f})")

    r0, n0 = loo(d, False)
    r1, n1 = loo(d, True)
    print(f"\nLEAVE-ONE-OUT RUUTVIGA")
    print(f"   M0 ainult kategooria      {r0:.4f} G")
    print(f"   M1 kategooria + kutus     {r1:.4f} G")
    vahe = 100 * (r1 - r0) / r0
    print(f"   vahe                      {vahe:+.1f} %")
    print("\nOTSUS: " + ("KUTUSEKLASS PARANDAB" if r1 < r0 else
                         "KUTUSEKLASS EI PARANDA -- M1 jaab valja"))


if __name__ == "__main__":
    main()
