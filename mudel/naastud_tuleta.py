# -*- coding: utf-8 -*-
"""Ajakirjatestidest tuletatud rehvid (presets_tuletatud.py).

MIKS. Naastrehvil ei ole EL-i märgist ja EPREL-is teda pole; vanadel
mudelitel (Hakkapeliitta 8/9, X-Ice North 3, IceContact 2, Nord Frost 200,
i*Pike RS2 …) ei ole ka meie oma ankrutestides (TM25) rida. Küll aga on
nad aastaid 2013–2026 ajakirjatestides koos rehvidega, mille mu me juba
teame (testid_ext/*.json). Sama testi sees on pidurdusmaade suhe sama mis
haardetegurite pöördsuhe: d ∝ 1/mu. See suhe EI SÕLTU algkiirusest ega
autost, seega sobivad ka testid, mille kiirust allikas ei trüki.

KUIDAS. Iga pinna (jää, lumi, märg, kuiv) kohta lahendatakse
    log d[rehv, test] = a[test] + b[rehv],      b = −log mu
vähimruutudega, kus b on FIKSEERITUD rehvidel, mis on juba presets.py-s
(mõõdetud rehvid, mu nende enda ankrutest või kategooria baas), ja vaba
ülejäänutel. Test annab a (tema raja haardetase), rehv annab b. Testid
kaaluga 0,5^((2026−aasta)/6): 12 aastat vana test loeb veerandi.
Viiteväärtus ilma oma mõõtmiseta (kategooria baas) kaaluga 0,3.

TULEMUS on mu, mille abil mootor taastoodab selle rehvi KOHA tema enda
testides, mitte ühe testi absoluutnumbri. Veapiir on sama mis mõõdetud
rehvil, pluss testidevaheline hajuvus (jääl ~15 %, vt BACKTEST_VALISTESTID).

Käivita: python3 -m mudel.naastud_tuleta   → kirjutab mudel/presets_tuletatud.py
"""
from __future__ import annotations

import collections
import glob
import json
import math
import os
import re

from .model import BrakingModel, TyreCategory
from .presets import TYRES as _TYRES
from .rehvinimi import kanooniline, voti

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "testid_ext")
OUT = os.path.join(HERE, "presets_tuletatud.py")
AASTA_NYYD = 2026
CAT = {"summer": TyreCategory.SUMMER_TOURING, "summer_uhp": TyreCategory.SUMMER_UHP,
       "allseason": TyreCategory.ALL_SEASON, "winter_central": TyreCategory.WINTER_CENTRAL,
       "winter_nordic": TyreCategory.WINTER_NORDIC, "winter_studded": TyreCategory.WINTER_STUDDED}
# pind: (surface, wet)
PINNAD = {"ice": ("ice", False), "snow": ("snow", False), "wet": ("asphalt", True), "dry": ("asphalt", False)}
SKIP_TESTS = {"ZaRulem-2008-W-ICETEMP-mixed"}
# allikas ise kahtlane: vt backtest_ext.SKIP
try:
    from .backtest_ext import SKIP as _SKIP
except Exception:  # pragma: no cover
    _SKIP = {}


def kaal_aasta(y):
    return 0.5 ** (max(0, AASTA_NYYD - int(y)) / 6.0)


def loe_testid():
    """-> vaatlused {pind: [(test_id, aasta, kaal, võti, nimi, kat, meetrid)]}, nimed {võti: (nimi, kat, mõõt, aasta)}"""
    obs = collections.defaultdict(list)
    nimed = {}
    for f in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        for t in json.load(open(f, encoding="utf-8")):
            if t["test_id"] in SKIP_TESTS or t.get("season") != "winter":
                continue
            ds = {d["id"]: d for d in t["disciplines"]}
            for ty in t["tyres"]:
                kat = CAT.get(ty.get("category"))
                if kat not in (TyreCategory.WINTER_STUDDED, TyreCategory.WINTER_NORDIC):
                    continue
                k = voti(ty["name"])
                for did, val in (ty.get("results") or {}).items():
                    d = ds.get(did)
                    if val is None or d is None or (t["test_id"], did) in _SKIP:
                        continue
                    pind = None
                    for p, (surf, wet) in PINNAD.items():
                        if d["surface"] == surf and bool(d.get("wet")) == wet:
                            pind = p
                    if not pind or not (val > 0):
                        continue
                    w = kaal_aasta(t["year"])
                    # jää 20–30 km/h pealt (Za Rulem) võimendab naastude osa: pool kaalu
                    if pind == "ice" and d.get("v_from") is not None and d["v_from"] <= 30:
                        w *= 0.5
                    obs[pind].append((t["test_id"], t["year"], w, k, ty["name"].strip(), kat, float(val)))
                    best = nimed.get(k)
                    if not best or t["year"] > best[3]:
                        nimed[k] = (ty["name"].strip(), kat, t["size"], t["year"])
    return obs, nimed


def viited():
    """Juba mõõdetud rehvid: võti -> {pind: (log mu, kaal)}"""
    cal = BrakingModel().cal
    out = {}
    for key, t in _TYRES.items():
        if t.g_source != "test":
            continue
        k = voti(t.name)
        v = {}
        v["wet"] = (math.log(cal.k_g * t.wet_grip_index), 1.0)
        if t.mu_dry_override is not None:
            v["dry"] = (math.log(t.mu_dry_override), 1.0)
        else:
            v["dry"] = (math.log(cal.mu_dry_base[t.category]), 0.3)
        if t.mu_ice_override is not None:
            v["ice"] = (math.log(t.mu_ice_override), 1.0)
        else:
            v["ice"] = (math.log(cal.mu_ice_base[t.category]), 0.3)
        if t.mu_snow_override is not None:
            v["snow"] = (math.log(t.mu_snow_override), 1.0)
        else:
            v["snow"] = (math.log(cal.mu_snow_base[t.category]), 0.3)
        out[k] = (key, v)
    return out, cal


def _komponendid(rows):
    """Testid ja rehvid on graaf: rehv seob testid, kus ta oli. Eraldi komponente
    (nt ainult-naastu testid ilma ühegi ühise rehvita lamelli-testidega) ei saa
    omavahel skaalale panna — igaüks saab oma nihke oma viidetest."""
    parent = {}
    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)
    for test, w, k, d in rows:
        union(("t", test), ("r", k))
    comp = collections.defaultdict(list)
    for r in rows:
        comp[find(("t", r[0]))].append(r)
    return list(comp.values())


def _sobita(rows):
    tyres = {r[2] for r in rows}
    b = {k: 0.0 for k in tyres}
    a = {}
    for _ in range(500):
        num, den = collections.defaultdict(float), collections.defaultdict(float)
        for test, w, k, d in rows:
            num[test] += w * (math.log(d) - b[k]); den[test] += w
        a = {t: num[t] / den[t] for t in num}
        num2, den2 = collections.defaultdict(float), collections.defaultdict(float)
        for test, w, k, d in rows:
            num2[k] += w * (math.log(d) - a[test]); den2[k] += w
        b_new = {k: num2[k] / den2[k] for k in num2}
        m = sum(b_new.values()) / len(b_new)
        b_new = {k: v - m for k, v in b_new.items()}
        muutus = max(abs(b_new[k] - b[k]) for k in b_new)
        b = b_new
        if muutus < 1e-9:
            break
    return a, b


def lahenda(rows, viited):
    """rows: [(test, kaal, võti, meetrid)]; viited: võti -> (b_mootor, kaal).
    Iga seotud komponendi sees: kõik rehvid vabad, log d = a[test] + b[rehv]
    (vaheldumisi vähimruudud); skaala = viiterehvide kaalutud mediaan
    (b_mootor − b_sobitatud). Komponent ilma viideta jääb välja.
    -> b vabadele, info, diagnostika."""
    out, info = {}, {}
    diag = {"komponente": 0, "viiteid": 0, "valja": 0, "jaagid": []}
    for comp in _komponendid(rows):
        a, b = _sobita(comp)
        paarid = sorted((viited[k][0] - b[k], viited[k][1]) for k in b if k in viited)
        if not paarid:
            diag["valja"] += len({r[2] for r in comp}); continue
        kaal = sum(w for _, w in paarid); acc = 0.0; nihe = paarid[-1][0]
        for v, w in paarid:
            acc += w
            if acc >= kaal / 2:
                nihe = v; break
        diag["komponente"] += 1; diag["viiteid"] += len(paarid)
        diag["jaagid"] += [v - nihe for v, _ in paarid]
        diag.setdefault("read", []).extend((k, round((viited[k][0] - b[k]) - nihe, 3), viited[k][1]) for k in b if k in viited)
        for test, w, k, d in comp:
            if k not in viited:
                info.setdefault(k, {"n": 0, "testid": set(), "kaal": 0.0})
                info[k]["n"] += 1; info[k]["testid"].add(test); info[k]["kaal"] += w
        for k in b:
            if k not in viited:
                out[k] = b[k] + nihe
    j = diag["jaagid"]
    diag["sd"] = (sum(x * x for x in j) / len(j)) ** 0.5 if len(j) > 1 else 0.0
    return out, info, None, diag


def main():
    obs, nimed = loe_testid()
    ref, cal = viited()
    tulemus = collections.defaultdict(dict)   # võti -> pind -> (mu, n, testid)
    for pind, rows in obs.items():
        r = [(t, w, k, d) for (t, y, w, k, n, kat, d) in rows]
        fix = {k: v[pind] for k, v in ((kk, vv[1]) for kk, vv in ref.items()) if pind in v}
        b, info, a, diag = lahenda(r, fix)
        if diag:
            print(f"{pind:5s}: komponente {diag['komponente']}, viiterehve {diag['viiteid']}, viidete jääkide hälve {diag['sd']*100:.1f} % (log), ilma viiteta rehve välja {diag['valja']}")
            if os.environ.get("DIAG"):
                for k, j, w in sorted(diag.get("read", []), key=lambda x: x[1]): print(f"       {k:40s} jääk {j:+.3f} kaal {w}")
        for k, bb in b.items():
            tulemus[k][pind] = (math.exp(bb), info[k]["n"], sorted(info[k]["testid"]), info[k]["kaal"])

    # ainult rehvid, mida presets.py-s veel pole ja millel on vähemalt jää VÕI märg + kuiv
    read = []
    for k, pinnad in sorted(tulemus.items()):
        if k in ref or k in VALJA or k.split("|")[0] in VALJA_BRAND:
            continue
        nimi, kat, moot, aasta = nimed[k]
        nimi = ilus(nimi)
        if "ice" not in pinnad and not ("wet" in pinnad and "dry" in pinnad):
            continue
        read.append((k, nimi, kat, moot, aasta, pinnad))

    # mõistlikkuse piirid: mu jääl 0,08–0,45, lumel 0,2–0,6, kuival 0,6–1,1, G 0,8–1,7
    def ok(pind, mu):
        lo, hi = {"ice": (0.08, 0.45), "snow": (0.20, 0.60), "dry": (0.60, 1.10), "wet": (0.80 * cal.k_g, 1.70 * cal.k_g)}[pind]
        return lo <= mu <= hi

    def key_of(nimi):
        return "t_" + re.sub(r"[^a-z0-9]+", "_", nimi.lower()).strip("_")

    out = ["# -*- coding: utf-8 -*-",
           '"""GENEREERITUD — mudel/naastud_tuleta.py. ÄRA MUUDA KÄSITSI.',
           "",
           "Ajakirjatestidest (testid_ext/*.json) tuletatud rehvid: mu on lahendatud",
           "sama testi sees mõõdetud rehvide suhtes (d ∝ 1/mu). Vt naastud_tuleta.py.",
           '"""',
           "from .model import Tyre, TyreCategory as C",
           "",
           "TYRES_TULETATUD = {"]
    meta = {}
    n_ok = 0
    for k, nimi, kat, moot, aasta, pinnad in read:
        kw = []
        tests_all = set()
        m = {}
        if "wet" in pinnad and ok("wet", pinnad["wet"][0]):
            G = pinnad["wet"][0] / cal.k_g
        else:
            G = 1.17 if kat is TyreCategory.WINTER_STUDDED else 1.17   # D-klassi keskpunkt (TM25 sama eeldus)
        for pind in ("ice", "snow", "dry", "wet"):
            if pind in pinnad and ok(pind, pinnad[pind][0]):
                mu, n, tests, w = pinnad[pind]
                m[pind] = {"mu": round(mu if pind != "wet" else mu / cal.k_g, 4), "n": n, "testid": tests, "kaal": round(w, 2)}
                tests_all.update(tests)
        if "ice" not in m and "wet" not in m:
            continue
        if "dry" in m:
            kw.append(f"mu_dry_override={m['dry']['mu']}")
        if "snow" in m:
            kw.append(f"mu_snow_override={m['snow']['mu']}")
        if "ice" in m:
            kw.append(f"mu_ice_override={m['ice']['mu']}")
        if kat is TyreCategory.WINTER_STUDDED:
            kw.append("studded=True")
        key = key_of(nimi)
        out.append(f'    "{key}": Tyre({nimi!r}, C.{kat.name}, {round(G, 3)}, {", ".join(kw)}, size={moot!r}, g_source="test"),')
        meta[key] = {"nimi": nimi, "pinnad": m, "testid": sorted(tests_all), "viimane": aasta,
                     "g_allikas": "test" if "wet" in m else "D-klassi keskpunkt (märg mõõtmata)"}
        n_ok += 1
    out.append("}")
    out.append("")
    out.append("# mis testidest ja mitme vaatlusega iga väärtus tuli (leht näitab)")
    out.append("TULETUS = " + json.dumps(meta, ensure_ascii=False, indent=1))
    out.append("")
    open(OUT, "w", encoding="utf-8").write("\n".join(out))
    print(f"presets_tuletatud.py: {n_ok} rehvi ({sum(1 for v in meta.values() if 'ice' in v['pinnad'])} jääga)")
    for key, v in meta.items():
        p = v["pinnad"]
        print(f"  {v['nimi']:42s} " + " ".join(f"{pind}={p[pind]['mu']}({p[pind]['n']})" for pind in ("ice", "snow", "wet", "dry") if pind in p) + f"  [{v['viimane']}]")
    return meta


if __name__ == "__main__":
    main()
