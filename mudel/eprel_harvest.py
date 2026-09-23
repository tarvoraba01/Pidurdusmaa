# -*- coding: utf-8 -*-
"""EPREL-i korje: modu x mark, sest lehitsemist EI OLE.

MIKS NII, JA MITTE LIHTSALT "TOMBA KOIK ALLA"
---------------------------------------------
Motmine naitas, et EPREL-i avalik otsing ei lehitse. page/offset/limit
visatakse minema; iga paring annab "mingi 25" ja kolme erineva
taustaserveri peale kokku ~75 -- ka siis, kui vasteid on 4264.
Seega on ainus tee teha paring nii kitsaks, et vastus MAHUB 25 sisse.
Siis ei ole see enam suvaline valim vaid taielik nimekiri.

Kitsendus on MOOT + MARK. "195/65 R15 + Michelin" on kummekond vastet.

AUSUS: see korje katab tapselt neid marke, mis on allpool MARGID-nimekirjas.
Mark, mida seal ei ole, jaab puudu -- ja skript UTLEB selle valja, mitte ei
vaiki. Iga tulemus tapselt 25 rida on kahtlane (voib olla kargitud) ja
markitakse lipuga "kahtlane".

VOTI: loetakse failist, ei trukita, kaib ainult paises X-API-KEY,
valjundfaili ei joua.

KASUTAMINE
----------
    python3 eprel_harvest.py eprel-key.txt

Jookseb ~20-40 min. KATKESTADA VOIB julgelt (Ctrl-C) -- jargmine kaivitus
jatkab sealt, kus pooleli jai, sest vahetulemus kirjutatakse jooksvalt
faili eprel_harvest.json.
"""
import json
import os
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://eprel.ec.europa.eu/api/products/tyres"
OUT = "eprel_harvest.json"
PAGE_CAP = 25            # motdetud: server ei anna rohkem

# Autode tehasemoodud, sagedasemad ees. Lisa siia julgelt juurde.
MOODUD = [
    "195/65 R15", "205/55 R16", "205/60 R16", "215/65 R16", "185/65 R15",
    "235/60 R18", "225/65 R17", "215/60 R16", "185/60 R15", "225/55 R17",
    "215/55 R16", "225/60 R17", "235/65 R17", "225/50 R17", "215/55 R17",
    "225/45 R17", "225/40 R18", "195/65 R16", "205/65 R15", "175/70 R13",
    "205/55 R17", "235/55 R17", "215/70 R16", "195/60 R15", "225/45 R18",
]

# Margid, mida Eestis muuakse. Esimesed on praeguses mudelis olemas,
# ulejaanud on levinud Eesti rehvipoodides.
MARGID = [
    "Michelin", "Continental", "Nokian", "Bridgestone", "Goodyear", "Pirelli",
    "Dunlop", "Hankook", "Kumho", "Toyo", "Yokohama", "Falken", "Nexen",
    "Vredestein", "Uniroyal", "Semperit", "Barum", "Matador", "Kleber",
    "Fulda", "Firestone", "BFGoodrich", "Viking", "Apollo", "Maxxis",
    "Nankang", "GT Radial", "Giti", "Petlas", "Ceat", "Landsail", "Radar",
    "Imperial", "Syron", "Aplus", "Arivo", "Evergreen", "Goodride", "Tomket",
    "Superia", "CST", "Momo", "Norauto", "Nordman", "Point S", "Star Performer",
    "Sava", "Debica", "Kormoran", "Riken", "Tigar", "Rosava", "Marshal",
    "Laufenn", "Roadstone", "Sailun", "Triangle", "Linglong", "Kenda",
    "Marangoni", "Mabor", "Orium", "Taurus", "Zeetex", "Autogrip", "Rotalla",
    "Minerva", "Berlin", "Fortuna", "Tracmax", "Wanli", "Roadmarch", "Gripmax",
]


def read_key(path):
    """Loeb votme failist. EI TRUKI teda kunagi."""
    if path.lower().endswith(".pdf"):
        raw = subprocess.run(["pdftotext", "-layout", path, "-"],
                             capture_output=True, check=True).stdout
        text = raw.decode("utf-8", "replace")
    else:
        text = open(path, encoding="utf-8", errors="replace").read()
    bad = re.compile(r"^(https?|eprel|europa|european|commission|registry|"
                     r"energy|labelling|public|apikey|api|key)$", re.I)
    c = [t.strip("-_") for t in
         re.findall(r"[A-Za-z0-9][A-Za-z0-9_\-]{15,}", text)]
    c = [t for t in c if len(t) >= 16 and not bad.match(t) and not t.isalpha()]
    if not c:
        sys.exit("Votit ei leidnud sellest failist.")
    c.sort(key=len, reverse=True)
    return c[0]


def get(params, key, tries=3):
    u = BASE + "?" + urllib.parse.urlencode(params)
    r = urllib.request.Request(u, headers={
        "Accept": "application/json", "X-API-KEY": key})
    for i in range(tries):
        try:
            with urllib.request.urlopen(
                    r, timeout=60,
                    context=ssl.create_default_context()) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                time.sleep(3 * (i + 1)); continue
            return {"_viga": f"HTTP {e.code}"}
        except Exception as e:                       # noqa: BLE001
            if i < tries - 1:
                time.sleep(2 * (i + 1)); continue
            return {"_viga": type(e).__name__}
    return {"_viga": "?"}


VALJAD = ("eprelRegistrationNumber", "supplierOrTrademark", "modelIdentifier",
          "sizeDesignation", "tyreSection", "aspectRatio", "rimDiameter",
          "wetGripClass", "energyClass", "externalRollingNoiseValue",
          "externalRollingNoiseClass", "severeSnowTyre", "iceTyre",
          "tyreClass", "loadCapacityIndex", "speedCategorySymbol",
          "status", "onMarketEndDate")


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    key = read_key(argv[1])

    tehtud, rehvid, kahtlased, vead = set(), {}, [], []
    if os.path.exists(OUT):                      # jatka pooleli jaanud tood
        try:
            old = json.load(open(OUT, encoding="utf-8"))
            tehtud = set(tuple(x) for x in old.get("_tehtud", []))
            rehvid = {r["reg"]: r for r in old.get("rehvid", []) if r.get("reg")}
            kahtlased = old.get("kahtlased", [])
            print(f"jatkan: {len(tehtud)} paari tehtud, "
                  f"{len(rehvid)} rehvi olemas")
        except Exception:                        # noqa: BLE001
            pass

    def salvesta():
        json.dump({"allikas": "EPREL (Euroopa Komisjon)",
                   "korjatud": time.strftime("%Y-%m-%d"),
                   "meetod": "moot x mark, sest lehitsemist ei ole",
                   "lehe_lagi": PAGE_CAP,
                   "kahtlased": kahtlased,
                   "vead": vead,
                   "_tehtud": [list(x) for x in tehtud],
                   "rehvid": list(rehvid.values())},
                  open(OUT, "w", encoding="utf-8"), ensure_ascii=False)

    kokku = len(MOODUD) * len(MARGID)
    n = 0
    t0 = time.time()
    for moot in MOODUD:
        leitud_moodus = 0
        for mark in MARGID:
            n += 1
            if (moot, mark) in tehtud:
                continue
            d = get({"sizeDesignation": moot, "supplierOrTrademark": mark,
                     "limit": PAGE_CAP}, key)
            if "_viga" in d:
                vead.append([moot, mark, d["_viga"]])
                continue
            hits = d.get("hits") or []
            for h in hits:
                reg = h.get("eprelRegistrationNumber")
                if not reg:
                    continue
                rehvid[reg] = {"reg": reg, **{v: h.get(v) for v in VALJAD
                                              if v != "eprelRegistrationNumber"}}
            if len(hits) >= PAGE_CAP:
                kahtlased.append([moot, mark, d.get("size")])
            leitud_moodus += len(hits)
            tehtud.add((moot, mark))
            if n % 25 == 0:
                salvesta()
                kulu = time.time() - t0
                print(f"  {n}/{kokku}  {moot} {mark:<14} "
                      f"kokku {len(rehvid)} rehvi  "
                      f"({kulu/60:.0f} min)")
            time.sleep(0.25)
        print(f"{moot:<14} -> {leitud_moodus} rida")
    salvesta()

    print(f"\nVALMIS. {len(rehvid)} rehvi, {len(tehtud)} paari.")
    if kahtlased:
        print(f"KAHTLASED ({len(kahtlased)}): need moot+mark paarid andsid "
              f"tapselt {PAGE_CAP} rida, ehk voisid saada kargitud:")
        for k in kahtlased[:15]:
            print(f"   {k[0]} + {k[1]}  (API utleb kokku {k[2]})")
    if vead:
        print(f"VEAD: {len(vead)}")
    print(f"\nKirjutatud {OUT}. Votit selles failis EI OLE.")


if __name__ == "__main__":
    main(sys.argv)
