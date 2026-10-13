# -*- coding: utf-8 -*-
"""Põhjamaade lamellrehvid õigesse kategooriasse olemasolevates andmefailides.

Enne 12.10.2026 läks 3PMSF-märgisega talverehv, mille nimi ei öelnud „talv“, Kesk-Euroopa
kategooriasse — ka VikingContact 8, X-Ice Xi3, Nordtrac 2, WinGuard Ice jt. Jääl arvutati neile
siis Kesk-Euroopa haare (0,096 vs 0,203) ehk kaks korda pikem pidurdusmaa. Lisaks oli osal
mõõdureal jäämärk (lipp 8), aga kategooria tuli mudelilt.

Reegel (sama mis eprel_convert.kategooria):
  * talve-/aastaringsel real on jäämärk  -> WINTER_NORDIC
  * mudeli nimi on Põhjamaade lamelli sari (eprel_convert.POHJA) -> WINTER_NORDIC
Idempotentne.   python3 mudel/kat_pohja.py veeb/static/data
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from eprel_convert import POHJA  # noqa: E402

KAT_NR = ["SUMMER_TOURING", "ALL_SEASON", "WINTER_CENTRAL", "WINTER_NORDIC"]


def main(data):
    mp = os.path.join(data, "models.json")
    models = json.load(open(mp, encoding="utf-8"))
    pohja = set()
    for slug, m in models.items():
        if m.get("kat") not in ("WINTER_CENTRAL", "ALL_SEASON"):
            continue
        jaa = any(z.get("ice") for z in m.get("sizes", []))
        if jaa or POHJA.search(m.get("nimi") or ""):
            m["kat"] = "WINTER_NORDIC"
            m["katAlus"] = "margis (jaamargis osal moodudel)" if jaa else "nimi (Pohjamaade lamelli sari)"
            pohja.add(slug)
    json.dump(models, open(mp, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    ed = os.path.join(data, "eprel")
    muudetud = 0
    for f in sorted(os.listdir(ed)):
        if not f.endswith(".json"):
            continue
        p = os.path.join(ed, f)
        rows = json.load(open(p, encoding="utf-8"))
        ch = False
        for r in rows:
            if r[3] in (1, 2) and (r[0] in pohja or (isinstance(r[8], int) and r[8] & 8)):
                r[3] = 3
                r[8] = (r[8] or 0) & ~1      # kategooria ei ole enam oletus
                ch = True
                muudetud += 1
        if ch:
            json.dump(rows, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"Pohjamaade lamelliks: {len(pohja)} mudelit, {muudetud} mooturida")
    for s in sorted(pohja):
        print("  ", s, "|", models[s]["nimi"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "veeb/static/data")
