# -*- coding: utf-8 -*-
"""Testimata naastrehvid (gSource "hinnang") veebi core.json-i.

  python3 mudel/hinnang_rakenda.py <export_wp väljund>/core.json veeb/static/data

Võtab export_wp core.json-ist read gSource == "hinnang" ja paneb need veebi
core.json-i tyres-loendisse (vanad hinnangud asendatakse, muud read jäävad
puutumata). Slug, mis on juba models.json-is (EPREL või poe mudel = sama rehv
NAASTUDETA, päris märgisega), saab lõpu „-naastrehv“, et märgisega leht jääks
alles. Idempotentne.

Lisaks: igale rehvile (naast, lamell, ...), millel models.json-is rida pole (märgist pole), pannakse
`moodud` = mõõdud, mida poed müüvad (mudel/naastud_moodud.json). Rehvileht
näitab siis mõõte ja „Kus osta“ kasti, /api/rehv/<slug>/ leiab hinnad.
"""
import json
import os
import sys


def main(src, data):
    uus = [t for t in json.load(open(src, encoding="utf-8"))["tyres"] if t.get("gSource") == "hinnang"]
    p = os.path.join(data, "core.json")
    core = json.load(open(p, encoding="utf-8"))
    models = json.load(open(os.path.join(data, "models.json"), encoding="utf-8"))
    vanad = [t for t in core["tyres"] if t.get("gSource") != "hinnang"]
    slugid = {t.get("slug") for t in vanad} | set(models)
    for t in uus:
        if t["slug"] in slugid and not t["slug"].endswith("-naastrehv"):
            t["slug"] += "-naastrehv"
        slugid.add(t["slug"])
    core["tyres"] = vanad + uus
    mp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "naastud_moodud.json")
    moodud = json.load(open(mp, encoding="utf-8"))["moodud"] if os.path.exists(mp) else {}
    n_m = 0
    for t in core["tyres"]:
        t.pop("moodud", None)
        if t.get("slug") not in models and moodud.get(t.get("slug")):
            t["moodud"] = moodud[t["slug"]]
            n_m += 1
    print(f"mõõdud poodidest: {n_m} rehvil")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(core, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{p}: {len(uus)} testimata naastrehvi (hinnang), kokku {len(core['tyres'])} rehvi")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
