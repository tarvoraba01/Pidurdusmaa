# -*- coding: utf-8 -*-
"""Tüüpilise jää tegur (Calibration.ice_road_factor) ajakirjatestidest.

Iga jäätesti (testid_ext) mediaanne log(mõõdetud / ennustatud) on selle testi raja tase.
Tegur valitakse nii, et testide mediaantase on 0 ehk mudel ennustab TÜÜPILIST testijääd
(iga test üks hääl, mitte iga rehv). Väljund: tegur + testide jaotus.
Käivita:  python3 -m mudel.jaa_tase
"""
import collections, json, math, os, statistics
from . import backtest_ext as B
from .model import BrakingModel, Calibration, Conditions
import dataclasses


def tasemed(k):
    cal = dataclasses.replace(Calibration(), ice_road_factor=k, ice_road_add=0.0)
    m = BrakingModel(cal)
    orig = B.Conditions
    B.Conditions = lambda *a, **kw: orig(*a, **{**kw, "ice_road": True})
    try:
        core = json.load(open(os.path.join(B.CORE, "core.json"), encoding="utf-8"))
        obs, _ = B.load()
        g = collections.defaultdict(list)
        for o in obs:
            if o["surface"] != "ice" or o["speed_assumed"]:
                continue
            p, _ = B.predict_label(m, core, o)
            if p:
                g[(o["test"], o["cat"].name)].append(math.log(o["measured"] / p))
    finally:
        B.Conditions = orig
    return {t: statistics.median(v) for t, v in g.items() if len(v) >= 2}


def main():
    lo, hi = 0.5, 1.2
    for _ in range(18):
        k = (lo + hi) / 2
        med = statistics.median(tasemed(k).values())
        # med > 0: mõõdetud pikem kui ennustus -> haare väiksemaks
        if med > 0:
            hi = k
        else:
            lo = k
    t = tasemed(k)
    v = sorted(t.values())
    print(f"ice_road_factor = {k:.3f}  ({len(v)} testi, mediaan {statistics.median(v):+.3f})")
    print(f"  testide tase: p10 {math.exp(v[len(v)//10]):.2f}  p90 {math.exp(v[9*len(v)//10]):.2f} (mõõdetud/ennustatud)")
    c = collections.defaultdict(list)
    for (tst, kat), x in t.items():
        c[kat].append(x)
    for kat, x in sorted(c.items()):
        print(f"  {kat:16} {len(x):3} testi  mediaan {math.exp(statistics.median(x)):.3f}")


if __name__ == "__main__":
    main()
