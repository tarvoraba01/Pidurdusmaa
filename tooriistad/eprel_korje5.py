# -*- coding: utf-8 -*-
"""Pidurdusmaa.ee — EPREL-i rehvikorje, 5. ring (ZR-tähisega sportrehvid).

MIDA TA TEEB
------------
Täiendab faili eprel2.json (samas kaustas) ZR-tähisega mõõtudega.

MIKS: EPREL-i otsing on tähise suhtes tähttäheline. Päring "225/40 R18"
EI ANNA neid rehve, mille tähis on "225/40ZR18" -- ja just nii on
registreeritud enamik kiireid sportrehve (Continental SportContact 7,
Michelin Pilot Sport 5 jt). Seetõttu on nad lehelt praegu puudu. See ring
küsib sama 130 mõõtu ZR-kujul.

EPREL ei lehitse (iga päring annab kuni 25 rida), seega küsitakse
MÕÕT + MARK paaride kaupa. See on ~9490 päringut; skript teeb kolm
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
    python3 eprel_korje5.py eprel-key.txt
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
    "195/40ZR17", "195/45ZR17", "205/40ZR17", "205/45ZR17", "205/50ZR17", "205/55ZR17",
    "215/40ZR17", "215/45ZR17", "215/50ZR17", "215/55ZR17", "225/45ZR17", "225/50ZR17",
    "225/55ZR17", "235/45ZR17", "235/50ZR17", "235/55ZR17", "245/40ZR17", "245/45ZR17",
    "255/40ZR17", "255/45ZR17", "205/40ZR18", "205/45ZR18", "215/40ZR18", "215/45ZR18",
    "215/50ZR18", "215/55ZR18", "225/35ZR18", "225/40ZR18", "225/45ZR18", "225/50ZR18",
    "225/55ZR18", "235/40ZR18", "235/45ZR18", "235/50ZR18", "235/55ZR18", "245/35ZR18",
    "245/40ZR18", "245/45ZR18", "245/50ZR18", "255/35ZR18", "255/40ZR18", "255/45ZR18",
    "255/50ZR18", "255/55ZR18", "265/35ZR18", "275/35ZR18", "275/40ZR18", "205/55ZR19",
    "215/50ZR19", "225/35ZR19", "225/40ZR19", "225/45ZR19", "225/55ZR19", "235/35ZR19",
    "235/40ZR19", "235/45ZR19", "235/50ZR19", "235/55ZR19", "245/35ZR19", "245/40ZR19",
    "245/45ZR19", "245/50ZR19", "255/35ZR19", "255/40ZR19", "255/45ZR19", "255/50ZR19",
    "255/55ZR19", "265/35ZR19", "265/40ZR19", "265/50ZR19", "265/55ZR19", "275/30ZR19",
    "275/35ZR19", "275/40ZR19", "275/45ZR19", "275/55ZR19", "285/45ZR19", "295/45ZR19",
    "215/45ZR20", "225/35ZR20", "235/35ZR20", "235/40ZR20", "235/45ZR20", "235/50ZR20",
    "235/55ZR20", "245/35ZR20", "245/40ZR20", "245/45ZR20", "255/30ZR20", "255/35ZR20",
    "255/40ZR20", "255/45ZR20", "255/50ZR20", "265/30ZR20", "265/35ZR20", "265/40ZR20",
    "265/45ZR20", "265/50ZR20", "275/30ZR20", "275/35ZR20", "275/40ZR20", "275/45ZR20",
    "275/50ZR20", "285/30ZR20", "285/45ZR20", "295/40ZR20", "295/45ZR20", "305/40ZR20",
    "315/35ZR20", "235/45ZR21", "245/35ZR21", "245/40ZR21", "255/35ZR21", "255/40ZR21",
    "265/35ZR21", "265/40ZR21", "265/45ZR21", "275/30ZR21", "275/35ZR21", "275/40ZR21",
    "275/45ZR21", "285/40ZR21", "295/35ZR21", "315/35ZR21", "315/40ZR21", "275/35ZR22",
    "285/35ZR22", "285/40ZR22", "315/30ZR22", "325/35ZR22",
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
