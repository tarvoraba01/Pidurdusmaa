"""Ühe mõõdu EPREL-ridade koondamine: üks rida iga rehvimudeli (slug) kohta.

Koondamine (koondamine.py) paneb variandid (nt "ADVANTAGE" ja "ADVANTAGE DT1")
sama slugi alla. Ühes mõõdus jäi siis mitu rida sama slugiga — vahel erineva
märghaardeklassiga — ja leht näitas sama rehvi mitu korda (audit 6.10.2026).

Rida: [slug, mark, nimi, katNr, märg, kütus, dB, müraKl, lipud, testKey]
Reegel:
  * märghaardeklass = kõige sagedasem; viigi korral HALVEM (konservatiivne)
  * kütus, dB, müra = esimeselt realt, millel on see märghaardeklass
  * nimi = lühim (põhimudel ilma variandi lisata)
  * lipud: lumi/jää (4/8) VÕI, 1 (oletuslik kategooria) kui kõigil,
    2 (mitu klassi) kui klasse oli rohkem kui üks
  * testKey = esimene olemasolev
"""
from collections import Counter, OrderedDict

KL = "ABCDE"


def koonda_read(read):
    grupid = OrderedDict()
    for r in read:
        grupid.setdefault(r[0], []).append(r)
    valja = []
    for slug, g in grupid.items():
        if len(g) == 1:
            valja.append(g[0])
            continue
        loend = Counter(r[4] for r in g)
        top = max(loend.values())
        klassid = [k for k, n in loend.items() if n == top]
        klass = max(klassid, key=lambda k: KL.index(k) if k in KL else 9)
        alus = next(r for r in g if r[4] == klass)
        nimi = min((r[2] for r in g), key=lambda x: (len(x.strip()), x))
        lipud = 0
        for r in g:
            lipud |= r[8] & (4 | 8)
        if all(r[8] & 1 for r in g):
            lipud |= 1
        if len(set(r[4] for r in g)) > 1 or any(r[8] & 2 for r in g):
            lipud |= 2
        test = next((r[9] for r in g if r[9]), None)
        valja.append([slug, alus[1], nimi, alus[3], klass, alus[5], alus[6], alus[7], lipud, test])
    return valja
