# -*- coding: utf-8 -*-
"""Testitud rehv, mille nimi EPREL-is on teistsugune (export_wp ei leidnud paari).

  python3 mudel/test_eprel_alias.py veeb/static/data

„Kumho Ecsta PS71“ (test) = „Kumho PS71“ (EPREL), „CST Medallion Winter WCP1“
= „CST WCP1“ jne. Ilma sidumiseta oli testil oma leht ilma mõõtude, märgise,
hindade ja pildita („inimesel pole siin lehel midagi teha“) ja EPREL-i mudelil
teine leht ilma testita. Sidumine:
  * testitud rehv saab EPREL-i mudeli slugi (nagu export_wp seotud rehvidel),
  * EPREL-i mudel ja tema mõõduread saavad `tested` = testi võti,
  * ajakirjatestid (testid_ext.json) liiguvad uue slugi alla,
  * vana testi aadress suunatakse uuele (suunamised.json, 301).
Ainult kindlad paarid (sama mudel, tootja nimes vaid sarja- või tehasekood).
Idempotentne.
"""
import glob
import json
import os
import sys

# testi võti (core.json) -> EPREL-i mudeli slug (models.json)
ALIAS = {
    "kumho_ps71": "kumho-ps71",
    "cst_allseason_acp1": "cst-acp1",
    "cst_medallion_wcp1": "cst-wcp1",
    "maxxis_wp6": "maxxis-wp6",
    "evergreen_ew66": "evergreen-ew66",
    "pirelli_p7c2": "pirelli-cinturato-p7-p7c2",
    "nankang_activa_sv4": "nankang-sv-4",
    "t_kumho_wintercraft_ice_wi51": "kumho-wi51",
    "t_kumho_wintercraft_ws51": "kumho-ws51",
    "t_marshal_i_zen_kw31": "marshal-kw31",
    "t_nankang_ice_activa_ice_1": "nankang-ice-1",
    "t_nexen_winguard_ice_plus": "nexen-winguard-ice-plus",
}


def lae(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def kirjuta(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, separators=(",", ":"))


def main(data):
    core = lae(os.path.join(data, "core.json"))
    models = lae(os.path.join(data, "models.json"))
    sp = os.path.join(data, "suunamised.json")
    suun = lae(sp)
    ep = os.path.join(data, "testid_ext.json")
    ext = lae(ep)
    by_key = {t["key"]: t for t in core["tyres"]}
    vahetus = {}
    for key, uus in ALIAS.items():
        t = by_key.get(key)
        m = models.get(uus)
        if not t or not m:
            print("vahele:", key, uus)
            continue
        if m.get("tested") and m["tested"] != key:
            print("EPREL-i mudel juba teise testiga:", uus, m["tested"])
            continue
        vana = t.get("slug")
        m["tested"] = key
        t["slug"] = uus
        if vana and vana != uus:
            vahetus[vana] = uus
            suun[vana] = uus
    # ajakirjatestid uue slugi alla (ilma topeltridadeta)
    for vana, uus in vahetus.items():
        if vana in ext.get("rehvid", {}):
            read = ext["rehvid"].pop(vana)
            olemas = ext["rehvid"].setdefault(uus, [])
            nahtud = {(x["t"], x["d"], x["v0"]) for x in olemas}
            olemas.extend(x for x in read if (x["t"], x["d"], x["v0"]) not in nahtud)
    # EPREL-i mõõdufailides testi viide (r[9])
    sihid = {uus: key for key, uus in ALIAS.items() if models.get(uus, {}).get("tested") == key}
    n_r = 0
    for f in glob.glob(os.path.join(data, "eprel", "*.json")):
        rows = lae(f)
        muut = False
        for r in rows:
            if r[0] in sihid and r[9] != sihid[r[0]]:
                r[9] = sihid[r[0]]
                muut = True
                n_r += 1
        if muut:
            kirjuta(f, rows)
    # suunamise ahelad lühemaks (a -> b -> c  =>  a -> c)
    for k in list(suun):
        n = 0
        while suun[k] in suun and n < 5:
            suun[k] = suun[suun[k]]
            n += 1
    kirjuta(os.path.join(data, "core.json"), core)
    kirjuta(os.path.join(data, "models.json"), models)
    kirjuta(sp, dict(sorted(suun.items())))
    kirjuta(ep, ext)
    print(f"seotud {len(sihid)} testitud rehvi EPREL-iga, uusi suunamisi {len(vahetus)}, mõõduridu {n_r}")


if __name__ == "__main__":
    main(sys.argv[1])
