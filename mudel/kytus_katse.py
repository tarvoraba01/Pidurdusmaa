# -*- coding: utf-8 -*-
"""KATSE: kas EPREL-i kutuseklass seletab moodetud G jaakviga?

MIKS SEE KATSE ULDSE VOIMALIK ON
--------------------------------
Veeretakistus ja marghaare tulevad samast asjast -- kummi hustereesist,
lihtsalt eri sagedusel. Seetottu on nad vastukaivad ("volukolmnurk").
Kahe SAMA marghaardeklassiga rehvi puhul peaks see, mille kutuseklass
on parem, olema tehnoloogiliselt parema seguga: ta sai sama haarde
odavama husteresiga katte.

See on HUPOTEES. Käesolev fail ei eelda seda -- ta MOODAB selle.

KOLM AUSAT PIIRANGUT, MIS TULEB ENNE VALJA OELDA
------------------------------------------------
1. MOOT EI KATTU. ADAC testis olid 225/40 R18 ja 225/45 R17. Korjes
   neid moote EI OLE. Seega seotakse moodetud rehv EPREL-i ridadega
   TEISTES mootudes. Kutuseklass on mudelitasandi omadus rohkem kui
   marghaardeklass, aga see ei ole tasuta -- vt tulemuse hajuvust.

2. MEIL EI OLE SOLTUMATUT AMETLIKKU MARGISEKLASSI. anchors_adac.py
   real 84 on kirjas, et klass on TULETATUD sellesama testi margjast
   tulemusest. Seega ei saa ma kusida "kas kutuseklass seletab
   klassisisest hajuvust" nii, et klass oleks soltumatu. Selle asemel
   kusin otse: kas kutuseklass seletab G hajuvust, KUI kategooria on
   juba arvesse voetud.

3. NIMEDE SIDUMINE ON EBAKINDEL. Varem andis hagus sobitamine 11-st
   5 valet vastet. Siin on reegel range (koik margid + koik numbrid
   peavad klappima) ja IGA vaste trukitakse valja ule vaatamiseks.
"""
import json
import re
import sys
from collections import defaultdict

sys.path.insert(0, "/home/claude")
from pidurdus import presets                                    # noqa: E402

KL = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}      # A parim -> suur number

# Margisonad, mis tuleb mudelinimest ara visata enne vordlemist.
MARGID = ("CONTINENTAL", "BRIDGESTONE", "MICHELIN", "GOODYEAR", "KUMHO",
          "FALKEN", "FIRESTONE", "NORAUTO", "NEXEN", "TOYO", "VREDESTEIN",
          "YOKOHAMA", "DUNLOP", "NOKIAN", "SYRON", "CEAT", "GITI",
          "DOUBLE COIN", "PIRELLI", "HANKOOK", "NORDMAN", "VIKING",
          "BFGOODRICH", "BARUM", "PETLAS", "CST", "SUPERIA", "APLUS",
          "ARIVO", "MOMO", "LANDSAIL", "UNIROYAL", "SEMPERIT", "APOLLO",
          "MATADOR", "KLEBER", "POINT S", "NANKANG", "FULDA", "GT RADIAL",
          "MAXXIS", "RADAR", "IMPERIAL", "GOODRIDE", "STAR PERFORMER",
          "TOMKET", "EVERGREEN")


def norm(s):
    """Nimi -> ainult tahed ja numbrid, suurtahtedega."""
    return re.sub(r"[^0-9A-Z]", "", str(s or "").upper())


def mudel(nimi, mark=None):
    """Vota AINULT selle rehvi enda margisona nime eest ara.

    VIGA, MIS SIIN JUBA UHE KORRA TEHTUD SAI: kui vottes prooviti koiki
    marginimesid jarjest, siis Continentali reast "VikingContact 7" loigati
    ara "VIKING" (sest Viking on ka mark) ja jarele jai "CONTACT7", mis on
    "SPORTCONTACT7" sisestring -> Continental SportContact 7 sai vasteks
    Continental VikingContact 7. Seetottu: ainult oma mark.
    """
    u = str(nimi or "").upper()
    kand = [str(mark or "").upper()] if mark else sorted(
        MARGID, key=len, reverse=True)
    for m in kand:
        if m and u.startswith(m):
            return u[len(m):]
    return u


def numbrid(s):
    return tuple(re.findall(r"\d+", str(s or "").upper()))


def seo(moodetud_nimi, read):
    """Range sidumine: normaliseeritud mudelinimi peab olema TAPSELT sama.

    Sisestring EI KOLBA. Proovitud sai ja see andis:
       Vredestein Ultrac Pro   -> Ultrac          (teine toode)
       Michelin Pilot Alpin 5  -> Alpin 5         (teine toode)
       Apollo Aspire XP Winter -> Aspire XP       (suverehv!)
       BFGoodrich Advantage All Season -> Advantage
    Koigil neil on luhem nimi pikema sisestring, aga tegu on eri rehviga.
    Range vordus jatab vahem vasteid, aga need on kontrollitavad.
    """
    a = norm(mudel(moodetud_nimi))
    if len(a) < 5:
        return []
    return [r for r in read if norm(mudel(r["nimi"], r.get("mark"))) == a]


def main(korje):
    read = json.load(open(korje, encoding="utf-8"))["rehvid"]
    mark_read = defaultdict(list)
    for r in read:
        if r.get("blok") or r.get("staatus") != "PUBLISHED" or not r.get("nimi"):
            continue
        mark_read[norm(r.get("mark", "").split()[0] if r.get("mark") else "")].append(r)

    tyres = [(k, t) for k, t in presets.TYRES.items() if t.g_source == "test"]
    leitud, puudu = [], []

    for key, t in tyres:
        mk = norm(t.name.split()[0])
        kand = mark_read.get(mk, [])
        # kahesonalised margid
        if not kand:
            kand = mark_read.get(norm(" ".join(t.name.split()[:2])), [])
        v = seo(t.name, kand)
        if not v:
            puudu.append((key, t))
            continue
        kytus = sorted({r["kytus"] for r in v if r.get("kytus")})
        marg = sorted({r["marg"] for r in v if r.get("marg")})
        leitud.append({
            "key": key, "nimi": t.name, "kat": t.category.name,
            "G": t.wet_grip_index, "n_rida": len(v),
            "kytus": kytus, "marg": marg,
            "eprel_nimed": sorted({r["nimi"] for r in v})[:3],
            "mootud": sorted({r["mootN"] for r in v})[:4],
        })

    print(f"MOODETUD REHVE {len(tyres)}   VASTE LEITUD {len(leitud)}   "
          f"PUUDU {len(puudu)}\n")
    print("--- IGA VASTE ULEVAATAMISEKS ---")
    for x in sorted(leitud, key=lambda y: (y["kat"], -y["G"])):
        print(f"{x['G']:.3f} {x['kat']:<15} {x['nimi']:<40} -> "
              f"kytus={'/'.join(x['kytus']):<5} marg={'/'.join(x['marg']):<7} "
              f"({x['n_rida']} rida) EPREL: {x['eprel_nimed'][0][:34]}")
    print("\n--- VASTETA ---")
    for key, t in puudu:
        print(f"      {t.category.name:<15} {t.name}")

    json.dump(leitud, open("/tmp/kytus_seos.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
