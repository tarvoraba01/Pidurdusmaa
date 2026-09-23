# -*- coding: utf-8 -*-
"""Pidurdusmaa.ee — EPREL-i rehvikorje, 4. ring (autode ülejäänud tehasemõõdud).

MIDA TA TEEB
------------
Täiendab faili eprel2.json (samas kaustas) 146 rehvimõõduga, mis lehe
autodel on tehasemõõduna olemas, aga registrist veel korjamata (suuremad
veljed ja kaubikumõõdud). Varem korjatu jääb alles.

EPREL ei lehitse (iga päring annab kuni 25 rida), seega küsitakse
MÕÕT + MARK paaride kaupa. See on ~10658 päringut; skript teeb kolm
korraga ja võtab u 1–1,5 tundi.

KATKESTADA VÕIB (Ctrl-C) — järgmine käivitus jätkab poolelijäänud kohast.
Vahetulemus salvestatakse iga 100 päringu järel.

VÕTI
----
Loetakse failist, mille nimi antakse käsureal. Seda EI TRÜKITA, EI
PANDA URL-i ega väljundfaili — ainult päringu päisesse X-API-KEY.

KASUTAMINE (Terminalis)
-----------------------
    cd ~/Downloads
    python3 eprel_korje4.py eprel-key.txt
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
    "235/40 R18", "205/55 R17", "225/40 R19", "245/40 R19", "245/35 R20", "245/45 R17",
    "235/45 R17", "215/45 R18", "255/35 R19", "255/40 R20", "225/45 R19", "235/35 R19",
    "235/45 R20", "255/45 R20", "255/40 R21", "235/60 R16", "235/45 R19", "195/75 R16C",
    "215/45 R16", "195/65 R16", "225/60 R16", "275/45 R20", "295/40 R20", "275/30 R20",
    "205/55 R19", "225/75 R16C", "235/50 R18", "225/55 R19", "205/75 R16C", "235/50 R20",
    "265/45 R20", "195/65 R16C", "205/45 R16", "255/35 R20", "255/50 R20", "285/35 R22",
    "275/40 R21", "295/35 R21", "245/40 R17", "255/40 R18", "275/40 R18", "275/35 R19",
    "265/35 R18", "235/60 R17C", "185/50 R16", "265/30 R20", "255/35 R21", "285/45 R20",
    "285/40 R21", "245/35 R18", "225/35 R20", "255/30 R20", "255/35 R18", "275/30 R19",
    "245/40 R20", "275/35 R20", "245/35 R21", "285/45 R19", "315/35 R20", "235/60 R17",
    "155/80 R13", "215/65 R15C", "205/70 R15C", "205/40 R18", "235/50 R17", "155/70 R13",
    "275/35 R21", "245/70 R17", "275/40 R19", "225/50 R16", "265/40 R21", "255/45 R18",
    "175/55 R15", "205/50 R16", "215/40 R18", "195/40 R17", "235/45 R21", "175/80 R14",
    "225/70 R16", "255/60 R17", "225/35 R18", "235/50 R16", "265/45 R21", "205/45 R18",
    "255/40 R17", "255/45 R17", "275/35 R18", "275/30 R21", "175/65 R19", "245/50 R18",
    "245/50 R19", "305/40 R20", "315/35 R21", "275/35 R22", "315/30 R22", "215/55 R15",
    "215/75 R15C", "285/30 R20", "265/50 R20", "295/45 R20", "245/75 R16", "245/75 R17",
    "255/70 R18", "175/50 R15", "165/80 R13", "175/80 R16", "235/55 R20", "195/60 R17",
    "265/35 R19", "265/40 R19", "265/35 R20", "185/70 R15", "245/55 R16", "235/40 R20",
    "275/55 R19", "275/50 R20", "275/45 R21", "315/40 R21", "285/40 R22", "325/35 R22",
    "295/45 R19", "255/50 R18", "265/40 R20", "285/65 R16C", "225/60 R16C", "245/45 R18C",
    "205/80 R16", "175/70 R15", "195/70 R16", "205/70 R16", "175/65 R13", "165/65 R15",
    "235/75 R16", "195/45 R17", "235/35 R20", "265/35 R21", "205/80 R16C", "225/70 R17C",
    "265/55 R19", "245/40 R21", "285/55 R16C", "205/70 R17C", "215/50 R19", "215/45 R20",
    "215/65 R15", "275/45 R19",
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
