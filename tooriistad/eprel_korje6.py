# -*- coding: utf-8 -*-
"""Pidurdusmaa.ee — EPREL-i rehvikorje, 6. ring (uute autode tehasemõõdud).

MIDA TA TEEB
------------
Täiendab faili eprel2.json (samas kaustas) 137 rehvimõõduga, mis on lehe
1057 auto tehasemõõtude hulgas, aga registrist veel korjamata (peamiselt
vanade autode 13-15" mõõdud, kaubikute C-mõõdud ja uute autode suured
veljed), lisaks 47 sportmõõtu ZR-kujul. Varem korjatu jääb alles.

EPREL ei lehitse (iga päring annab kuni 25 rida), seega küsitakse
MÕÕT + MARK paaride kaupa. See on ~13432 päringut; skript teeb kolm
korraga ja võtab u 1,5-2 tundi.

KATKESTADA VÕIB (Ctrl-C) — järgmine käivitus jätkab poolelijäänud kohast.
Vahetulemus salvestatakse iga 100 päringu järel.

VÕTI
----
Loetakse failist, mille nimi antakse käsureal. Seda EI TRÜKITA, EI
PANDA URL-i ega väljundfaili — ainult päringu päisesse X-API-KEY.

KASUTAMINE (Terminalis)
-----------------------
    cd ~/Downloads
    python3 eprel_korje6.py eprel-key.txt
"""
import concurrent.futures as cf
import json
import os
import re
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://eprel.ec.europa.eu/api/products/tyres"
FAIL = "eprel2.json"
LAGI = 25
TOOLISI = 3

MOODUD = [
    "205/70 R15", "195/60 R14", "195/70 R14", "205/55 R15", "145/80 R13", "225/75 R16",
    "195/65 R14", "205/65 R17", "225/75 R15", "195/60 R18", "235/80 R16", "275/50 R21",
    "205/50 R15", "255/55 R20", "145/70 R13", "185/70 R13", "135/80 R13", "255/45 R21",
    "235/75 R15", "235/60 R20", "275/70 R16", "215/75 R15", "285/40 R20", "285/60 R18",
    "265/70 R18", "175/65 R17", "245/30 R20", "215/80 R16", "195/55 R20", "235/50 R21",
    "235/85 R16", "275/55 R20", "265/30 R19", "245/50 R17", "235/40 R17", "265/75 R15",
    "195/50 R19", "185/80 R14", "295/40 R21", "265/40 R22", "175/60 R14", "245/55 R17",
    "285/35 R21", "285/45 R21", "275/40 R22", "285/45 R22", "215/60 R18", "265/70 R16",
    "165/65 R13", "195/45 R15", "165/80 R14", "205/70 R14", "285/40 R19", "285/35 R20",
    "285/30 R19", "235/65 R19", "295/35 R20", "165/60 R15", "255/65 R16", "265/40 R18",
    "285/35 R19", "295/35 R22", "255/65 R18", "245/55 R16", "215/40 R16", "185/55 R14",
    "175/60 R13", "285/30 R21", "325/30 R21", "275/45 R18", "315/30 R21", "305/30 R21",
    "255/30 R19", "295/30 R20", "295/35 R19", "255/40 R22", "285/40 R23", "245/45 R21",
    "235/70 R17", "235/50 R16", "215/75 R15C", "175/70 R15", "245/45 R18C", "175/65 R19",
    "205/80 R16C", "195/70 R13", "215/90 R15", "315/30 R23", "315/35 R22", "275/35 R23",
    "255/50 R21", "285/35 R18", "325/40 R22", "275/50 R19", "275/65 R17", "275/60 R18",
    "285/65 R17", "285/50 R20", "275/45 R22", "255/60 R20", "255/65 R19", "265/45 R19",
    "295/40 R19", "265/35 R22", "275/55 R17", "285/50 R18", "265/60 R20", "175/60 R18",
    "305/30 R20", "235/40 R21", "265/45 R18", "225/40 R20", "205/60 R18", "295/40 R22",
    "285/70 R17", "265/70 R17", "225/50 R19", "185/45 R17", "275/70 R17", "235/60 R19",
    "175/80 R15", "295/30 R19", "245/60 R18", "245/50 R20", "275/65 R18", "275/70 R18",
    "265/40 R17", "225/55 R15", "225/45 R16", "155/65 R13", "155/80 R14", "265/70 R15",
    "255/70 R17", "205/75 R15", "285/30 R18", "215/70 R17", "195/80 R14C", "255/45ZR21",
    "285/40ZR20", "245/30ZR20", "265/30ZR19", "235/40ZR17", "295/40ZR21", "265/40ZR22",
    "285/35ZR21", "285/45ZR21", "275/40ZR22", "285/45ZR22", "285/40ZR19", "285/35ZR20",
    "285/30ZR19", "295/35ZR20", "265/40ZR18", "285/35ZR19", "295/35ZR22", "285/30ZR21",
    "325/30ZR21", "275/45ZR18", "315/30ZR21", "305/30ZR21", "255/30ZR19", "295/30ZR20",
    "295/35ZR19", "255/40ZR22", "285/40ZR23", "245/45ZR21", "315/30ZR23", "315/35ZR22",
    "275/35ZR23", "285/35ZR18", "325/40ZR22", "275/45ZR22", "265/45ZR19", "295/40ZR19",
    "265/35ZR22", "305/30ZR20", "235/40ZR21", "265/45ZR18", "225/40ZR20", "295/40ZR22",
    "185/45ZR17", "295/30ZR19", "265/40ZR17", "285/30ZR18",
]

MARGID = [
    "Michelin", "Continental", "Nokian", "Bridgestone", "Goodyear", "Pirelli", "Dunlop",
    "Hankook", "Kumho", "Toyo", "Yokohama", "Falken", "Nexen", "Vredestein",
    "Uniroyal", "Semperit", "Barum", "Matador", "Kleber", "Fulda", "Firestone",
    "BFGoodrich", "Viking", "Apollo", "Maxxis", "Nankang", "GT Radial", "Giti",
    "Petlas", "Ceat", "Landsail", "Radar", "Imperial", "Syron", "Aplus",
    "Arivo", "Evergreen", "Goodride", "Tomket", "Superia", "CST", "Momo",
    "Norauto", "Nordman", "Point S", "Star Performer", "Sava", "Debica", "Kormoran",
    "Riken", "Tigar", "Rosava", "Marshal", "Laufenn", "Roadstone", "Sailun",
    "Triangle", "Linglong", "Kenda", "Marangoni", "Mabor", "Orium", "Taurus",
    "Zeetex", "Autogrip", "Rotalla", "Minerva", "Berlin", "Fortuna", "Tracmax",
    "Wanli", "Roadmarch", "Gripmax",
]


def loe_voti(tee):
    t = open(tee, encoding="utf-8", errors="replace").read()
    c = [x.strip("-_") for x in re.findall(r"[A-Za-z0-9][A-Za-z0-9_\-]{15,}", t)]
    c = [x for x in c if not x.isalpha()]
    if not c:
        sys.exit("Võtit ei leitud failist " + tee)
    return max(c, key=len)


def paring(params, voti, katseid=4):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json", "X-API-KEY": voti})
    for i in range(katseid):
        try:
            with urllib.request.urlopen(req, timeout=60, context=ssl.create_default_context()) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < katseid - 1:
                time.sleep(4 * (i + 1)); continue
            return {"_viga": "HTTP %d" % e.code}
        except Exception as e:  # noqa: BLE001
            if i < katseid - 1:
                time.sleep(2 * (i + 1)); continue
            return {"_viga": type(e).__name__}
    return {"_viga": "?"}


def rida(h):
    """EPREL-i vastus -> eprel2.json rea kuju (sama mis varasemal korjel)."""
    moot = h.get("sizeDesignation") or ""
    lisa = h.get("additionalDetails") or {}
    return {
        "reg": h.get("eprelRegistrationNumber"),
        "mark": h.get("supplierOrTrademark"),
        "nimi": lisa.get("commercialName") or h.get("commercialName"),
        "kood": h.get("modelIdentifier"),
        "moot": moot,
        "mootN": re.sub(r"[^0-9A-Z]", "", moot.upper()).replace("ZR", "R"),
        "tahis": h.get("tyreDesignation"),
        "lai": h.get("tyreSection"), "prof": h.get("aspectRatio"), "velg": h.get("rimDiameter"),
        "marg": h.get("wetGripClass"), "kytus": h.get("energyClass"),
        "muraDb": h.get("externalRollingNoiseValue"), "muraKl": h.get("externalRollingNoiseClass"),
        "lumi": bool(h.get("severeSnowTyre")), "jaa": bool(h.get("iceTyre")),
        "klass": h.get("tyreClass"), "koormus": h.get("loadCapacityIndex"),
        "koormusT": h.get("loadCapacityIndex2"), "kiirus": h.get("speedCategorySymbol"),
        "staatus": h.get("status"), "blok": bool(h.get("blocked")),
        "viimane": bool(h.get("lastVersion")), "ver": h.get("versionNumber"),
        "coreId": h.get("productModelCoreId"), "turultLahkub": h.get("onMarketEndDate"),
    }


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    voti = loe_voti(argv[1])
    if not os.path.exists(FAIL):
        sys.exit("Faili %s ei ole selles kaustas. Käivita skript kaustas, kus see on." % FAIL)
    d = json.load(open(FAIL, encoding="utf-8"))
    tehtud = set(tuple(x) for x in d.get("_tehtud", []))
    rehvid = {r["reg"]: r for r in d.get("rehvid", []) if r.get("reg")}
    kahtlased = d.get("kahtlased", [])
    vead = []
    lukk = threading.Lock()

    def salvesta():
        d.update({"korjatud": time.strftime("%Y-%m-%d"), "kahtlased": kahtlased, "vead": vead,
                  "_tehtud": [list(x) for x in tehtud], "rehvid": list(rehvid.values())})
        tmp = FAIL + ".tmp"
        json.dump(d, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
        os.replace(tmp, FAIL)

    tood = [(m, k) for m in MOODUD for k in MARGID if (m, k) not in tehtud]
    print("Tehtud varem %d paari, rehve %d. Teha %d päringut." % (len(tehtud), len(rehvid), len(tood)))
    t0, n = time.time(), 0

    def uks(paar):
        moot, mark = paar
        r = paring({"sizeDesignation": moot, "supplierOrTrademark": mark, "limit": LAGI}, voti)
        time.sleep(0.2)
        return paar, r

    try:
        with cf.ThreadPoolExecutor(TOOLISI) as ex:
            for paar, r in ex.map(uks, tood):
                with lukk:
                    n += 1
                    if "_viga" in r:
                        vead.append([paar[0], paar[1], r["_viga"]])
                    else:
                        hits = r.get("hits") or []
                        for h in hits:
                            x = rida(h)
                            if x["reg"]:
                                rehvid[x["reg"]] = x
                        if len(hits) >= LAGI:
                            kahtlased.append([paar[0], paar[1], r.get("size")])
                        tehtud.add(paar)
                    if n % 100 == 0:
                        salvesta()
                        kulu = (time.time() - t0) / 60
                        jaanud = kulu / n * (len(tood) - n)
                        print("  %d/%d  %-12s  rehve kokku %d   (%.0f min, u %.0f min jäänud)"
                              % (n, len(tood), paar[0], len(rehvid), kulu, jaanud))
    except KeyboardInterrupt:
        print("\nKatkestatud — salvestan. Järgmine käivitus jätkab siit.")
    salvesta()
    print("\nVALMIS. %d rehvi, %d paari tehtud, vigu %d." % (len(rehvid), len(tehtud), len(vead)))
    if vead:
        print("Vigadega paarid proovitakse järgmisel käivitusel uuesti.")
    print("Tulemus on failis %s (võtit seal ei ole). Anna Claude'ile teada, et korje on tehtud." % FAIL)


if __name__ == "__main__":
    main(sys.argv)
