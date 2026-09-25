"""Rehvimudelite koondamine (SEO samm 5).

EPREL-is on sama rehv sageli mitme "mudelina":

  1. tootjavariant   PILOT SPORT 4 AO, CONTIPREMIUMCONTACT 5 SSR
                     -> liidetakse emamudelisse (michelin-pilot-sport-4),
                        mõõdu juurde jääb märge "AO"
  2. mõõt nimes      Nankang "145/65R15 72V AS-1", "155/65R14 75V AS-1" ...
     (SKU)           -> iga mõõt oli eraldi 1-mõõduline leht; nüüd üks
                        leht "Nankang AS-1" kõigi mõõtudega

Vana aadress -> uus aadress läheb faili suunamised.json; server teeb
sealt 301-suunamise (veeb/server.js), et vanad lingid ja Google'i
indeks liiguksid uuele lehele.

Mõõdetud (testitud) rehve ei puutu — nende nimi on testiga seotud.
"""
import re
from collections import Counter

# ainult tootja märgistuse koodid -- mitte "suv", "plus", "4x4", mis on
# päris eri mudelid. Sama nimekiri on veeb/src/lib/server/andmed.js-is.
VARIANT = set((
    "a ao ao1 ao2 n0 n1 n2 n3 n4 n5 n6 mo mo1 mos moe vol j jlr lr ro1 ro2 "
    "r01 r02 t0 t1 t2 xl rf rft runflat ssr zp dt dt1 dt2 star seal "
    "sealinside acoustic contisilent contiseal silent nf0 nd0 ng0 ne0 nh0 "
    "hl elt mfs").split())

SKU_RE = re.compile(r"\d{3}-?\d{2}-?z?r\d{2}")
# 145/65R15, 195/45ZR17, 185/65 R15C, 235/35ZR19 (ka kokku kirjutatud indeksiga)
SUURUS = re.compile(r"(?:P|LT)?\d{3}\s*/\s*\d{2}\s*Z?R\s*F?\s*\d{2}C?", re.I)
# koormus/kiirus: 72V, 104/102R, 91W
INDEKS = re.compile(r"(?<![A-Za-z0-9-])\d{2,3}(?:/\d{2,3})?[A-Z]{1,2}(?![A-Za-z0-9])")
# märgistus, mis ei ole mudeli nimi (jääb mõõdu juurde märkeks)
MARKER = re.compile(
    r"(?<![A-Za-z0-9])(XLL|XL|RF|RFT|SSR|ZP|TL|M\+S|MS|3PMSF|FR|MFS)(?![A-Za-z0-9+])", re.I)
# tootja sisekoodid ja külje kirjad, mis ei ole mudeli nimi:
# EUHA/ESHA/HUHA/CNHA/CNSE/EURF/EU10 (tehase/turu koodid), SY1H/SY80 (Nankangi
# alaseeriad), OWL/WL/RWL/WR/WWL... (valged tähed küljel), üksik L ja P
MYRA = re.compile(
    r"(?<![A-Za-z0-9])(EUHA|ESHA|HUHA|CNHA|CNSE|EURF|EU10|SY[0-9A-Z]{2}|"
    r"OWXLL|OWXL|WWXL|OWL|OW|RWL|WLL|WL|WRL|WR|WWL|BSW|L|P)(?![A-Za-z0-9])", re.I)
# kokku kirjutatud paarisindeks: "104/102QICE-1"
INDEKS_KOKKU = re.compile(r"(?<![A-Za-z0-9-])\d{2,3}/\d{2,3}[A-Z](?=[A-Z]{2})")


def _puhas_nimi(nimi):
    """'145/65R15 72V AS-1 XL L EUHA' -> ('AS-1', 'XL')"""
    s = SUURUS.sub(" ", nimi)
    s = INDEKS_KOKKU.sub(" ", s)
    s = INDEKS.sub(" ", s)
    s = re.sub(r"[()\[\]]", " ", s)
    markerid = [m.upper().replace("XLL", "XL") for m in MARKER.findall(s)]
    s = MARKER.sub(" ", s)
    s = MYRA.sub(" ", s)
    # lõpus kulumisindeks ("AR-1 80", "NS-2R 240") -- ainult koodi-stiilis nime järel
    s = re.sub(r"^(.*\S-\S+)\s+\d{2,3}\s*$", r"\1", s.strip())
    s = re.sub(r"\s+", " ", s).strip(" -")
    return s, " ".join(dict.fromkeys(markerid))


def _ema_slug(slug, olemas):
    t = slug.split("-")
    lisad = []
    while len(t) > 2 and t[-1] in VARIANT:
        lisad.insert(0, t[-1])
        t = t[:-1]
        p = "-".join(t)
        if p in olemas:
            return p, " ".join(lisad).upper()
    return None, ""


def koonda(mud, slugify):
    """Muudab `mud` (võti -> mudel, mudelil "slug") kohapeal.
    Tagastab {vana_slug: uus_slug}."""
    suun = {}
    by_slug = {m["slug"]: k for k, m in mud.items()}

    def lisa(siht_k, laps_k, marge):
        siht, laps = mud[siht_k], mud[laps_k]
        for z in laps["sizes"]:
            z = dict(z)
            if marge:
                z["v"] = marge
            siht["sizes"].append(z)
        suun[laps["slug"]] = siht["slug"]
        # varasemad suunamised lapsele -> otse sihile (ahelaid ei teki)
        for a, b in list(suun.items()):
            if b == laps["slug"]:
                suun[a] = siht["slug"]
        del mud[laps_k]
        del by_slug[laps["slug"]]

    # 1) tootjavariandid emamudelisse
    for k in sorted(list(mud), key=lambda k: -len(mud[k]["slug"])):
        if k not in mud:
            continue
        m = mud[k]
        if m.get("tested") or SKU_RE.search(m["slug"]):
            continue
        p, marge = _ema_slug(m["slug"], by_slug)
        if p and p != m["slug"] and mud[by_slug[p]]["kat"] == m["kat"]:
            lisa(by_slug[p], k, marge)

    # 2) mõõt nimes: rühmita puhta nime järgi
    rühmad = {}
    for k, m in mud.items():
        if m.get("tested") or not SKU_RE.search(m["slug"]):
            continue
        nimi, marge = _puhas_nimi(m["nimi"])
        if not re.search(r"[A-Za-z]", nimi):
            continue  # nimes ainult mõõt (nt "Autogrip 175/65R15") -- jääb nagu on
        s = slugify(m["mark"] + " " + nimi)
        if not s or SKU_RE.search(s):
            continue
        rühmad.setdefault(s, []).append((k, nimi, marge))

    # sama nimi eri kirjapildiga (XR-611 / XR611) -> üks rühm, levinum kirjapilt
    kompakt = {}
    for s in sorted(rühmad, key=lambda s: -len(rühmad[s])):
        kompakt.setdefault(s.replace("-", ""), s)
    for s in list(rühmad):
        sihts = kompakt[s.replace("-", "")]
        if sihts != s:
            rühmad[sihts].extend(rühmad.pop(s))

    for s, liikmed in rühmad.items():
        siht_k = by_slug.get(s)
        if siht_k is None:
            # emamudel variandi kaudu (nt "SP-9 XL" -> nankang-sp-9)?
            p, _ = _ema_slug(s, by_slug)
            siht_k = by_slug.get(p) if p else None
        if siht_k is None:
            # uus koondleht: esimese liikme andmetest, nimi puhas
            k0, nimi0, _ = liikmed[0]
            m0 = mud[k0]
            kat = Counter(mud[k]["kat"] for k, _, _ in liikmed).most_common(1)[0][0]
            alus = Counter(mud[k]["katAlus"] for k, _, _ in liikmed).most_common(1)[0][0]
            uus_k = "KOOND|" + s
            mud[uus_k] = {"mark": m0["mark"].strip(), "kat": kat, "katAlus": alus,
                          "sizes": [], "nimi": nimi0, "slug": s}
            by_slug[s] = uus_k
            siht_k = uus_k
        for k, _, marge in liikmed:
            if k in mud and k != siht_k:
                lisa(siht_k, k, marge)

    return suun
