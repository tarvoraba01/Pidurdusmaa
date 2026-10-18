# -*- coding: utf-8 -*-
"""Ajakirjatestidest tuletatud rehvid (gSource "tuletatud") veebi core.json-i.

  python3 mudel/tuletatud_rakenda.py <export_wp väljund>/core.json veeb/static/data

Nagu hinnang_rakenda.py, aga tuletatud ridadele (naastud_tuleta.py ->
presets_tuletatud.py -> export_wp). Veebi core.json-i ei ehitata nullist
uuesti, sest seal on peale ekspordi tehtud sammud (test_eprel_alias.py,
hinnang_rakenda.py jt), mida eksport ei korda.

  * Rehv, mis on veebi core.json-is juba olemas (sama võti või sama
    rehvinimi.voti), saab ekspordist uued haardetegurid, mõõdu ja testide
    loetelu. Tema võti, nimi, slug ja `moodud` jäävad samaks, et aadress ja
    poodide sidumine ei muutuks.
  * Uus tuletatud rehv (uus test, uus mudel) lisatakse lõppu.
  * Rehvi, keda ekspordis enam ei ole, EI kustutata (leht jääks 404-ks);
    skript ütleb selle välja.
Idempotentne.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mudel.rehvinimi import voti  # noqa: E402

HOIA = ("key", "name", "slug", "moodud")


def main(src, data):
    uued = [t for t in json.load(open(src, encoding="utf-8"))["tyres"] if t.get("gSource") == "tuletatud"]
    p = os.path.join(data, "core.json")
    core = json.load(open(p, encoding="utf-8"))
    vanad = {t["key"]: t for t in core["tyres"] if t.get("gSource") == "tuletatud"}
    voti_jargi = {voti(t["name"]): t for t in vanad.values()}
    slugid = {t.get("slug") for t in core["tyres"]}
    nahtud, lisatud, muudetud = set(), [], 0
    for u in uued:
        v = vanad.get(u["key"]) or voti_jargi.get(voti(u["name"]))
        if v is not None:
            nahtud.add(v["key"])
            enne = dict(v)
            for k, val in u.items():
                if k not in HOIA:
                    v[k] = val
            for k in [k for k in v if k not in u and k not in HOIA]:
                del v[k]
            muudetud += v != enne
        else:
            if u.get("slug") in slugid:
                print("VIGA: uue tuletatud rehvi slug on juba kasutusel:", u["key"], u.get("slug"))
                continue
            core["tyres"].append(u)
            slugid.add(u.get("slug"))
            lisatud.append(u)
    for k in vanad:
        if k not in nahtud:
            print("alles jäetud (ekspordis enam ei ole):", k, vanad[k]["name"])
    with open(p, "w", encoding="utf-8") as f:
        json.dump(core, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{p}: tuletatud {len(vanad)} -> {len(vanad) + len(lisatud)}, muudetud {muudetud}, lisatud {len(lisatud)}")
    for u in lisatud:
        print("   +", u["key"], "|", u["name"], "|", u.get("slug"), "|", u.get("category"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
