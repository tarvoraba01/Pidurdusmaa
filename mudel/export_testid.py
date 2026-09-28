"""Välismaa rehvitestide tulemused rehvilehtedele (testid_ext.json).

Andmed: testid_ext/*.json (vt backtest_ext.py). Siin need ainult
NÄIDATAKSE, mitte ei arvutata nendega: backtest näitas, et ühe testi
tulemus ei ennusta sama rehvi tulemust teises testis/mõõdus märjal
paremini kui selle mõõdu EL-i märgis (4,7 % vs 4,2 %). Seepärast jääb
arvutus märgise (ja testitud rehvide) peale ning välistestid on lehel
mõõdetud faktina: kus, mis mõõdus, mis kiiruselt, mitu meetrit, mitmes.

Rehv seotakse EPREL-i mudeliga (models.json) margi + nime järgi; kui
vaste ei ole üheselt kindel, jäetakse rehv lehelt välja (test ise jääb
allikate nimekirja).

Käivita:  python3 -m mudel.export_testid
"""
from __future__ import annotations

import collections
import json
import os
import re

from . import backtest_ext as B

HERE = os.path.dirname(__file__)
OUTS = [os.path.join(HERE, "..", "veeb", "static", "data", "testid_ext.json")]
DISC = {("asphalt", True): "märg asfalt", ("asphalt", False): "kuiv asfalt",
        ("concrete", True): "märg betoon", ("snow", False): "lumi", ("ice", False): "jää"}


def model_index():
    p = os.path.join(B.CORE, "models.json")
    models = json.load(open(p, encoding="utf-8"))
    idx = collections.defaultdict(list)
    for slug, m in models.items():
        bt = B._tok(m["mark"])
        if bt:
            idx[bt[0]].append((slug, bt, "".join(B._tok(m["nimi"]))))
    return idx


def match(idx, name):
    t = B._tok(name)
    if not t:
        return None
    cands = []
    for slug, bt, rn in idx.get(B.BRAND_ALIAS.get(t[0], t[0]), []):
        model = t[len(bt):] if t[:len(bt)] == bt else t[1:]
        tm = "".join(model)
        if not tm:
            continue
        if tm == rn:
            cands.append((0, slug))
        elif rn.startswith(tm) and rn[len(tm):] in B.SUFFIX_OK:
            cands.append((1, slug))
        elif tm.startswith(rn) and re.fullmatch(r"[a-z]{0,2}\d{2,4}|suv|xl", tm[len(rn):]):
            cands.append((2, slug))
    if not cands:
        return None
    best = min(d for d, _ in cands)
    top = sorted({s for d, s in cands if d == best})
    return top[0] if len(top) == 1 else None


def main():
    obs, _ = B.load()
    idx = model_index()
    # koht testis: sama test + distsipliin
    grp = collections.defaultdict(list)
    for o in obs:
        grp[(o["test"], o["disc"])].append(o["measured"])
    tests, per = {}, collections.defaultdict(list)
    raw = {}
    for f in sorted(os.listdir(B.DATA)):
        if f.endswith(".json"):
            for t in json.load(open(os.path.join(B.DATA, f), encoding="utf-8")):
                raw[t["test_id"]] = t
    unmatched = 0
    for o in obs:
        t = raw[o["test"]]
        tests[o["test"]] = {"pub": t["publication"], "year": t["year"], "season": t["season"],
                            "size": o["size"] or t["size"], "car": t.get("car"), "url": t.get("url")}
        slug = match(idx, o["tyre"])
        if not slug:
            unmatched += 1
            continue
        allv = sorted(grp[(o["test"], o["disc"])])
        per[slug].append({"t": o["test"], "d": DISC.get((o["surface"], o["wet"]), o["surface"]),
                          "v0": o["v0"], "v1": o["v1"], "m": o["measured"],
                          "pos": allv.index(o["measured"]) + 1, "n": len(allv), "best": allv[0],
                          "nimi": o["tyre"]})
    for v in per.values():
        v.sort(key=lambda x: (-tests[x["t"]]["year"], x["t"], x["d"]))
    out = {"allikad": tests, "rehvid": per}
    for p in OUTS:
        json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"testid_ext.json: {len(tests)} testi, {len(per)} rehvimudelit, "
          f"{sum(len(v) for v in per.values())} tulemust; sidumata {unmatched}")


if __name__ == "__main__":
    main()
