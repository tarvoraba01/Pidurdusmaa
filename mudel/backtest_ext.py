"""Backtest välismaa rehvitestide vastu (2026-09-28).

MIS SEE ON
----------
testid_ext/*.json on ~2000 avaldatud pidurdusmaad (Auto Bild, Za Rulem,
auto motor und sport, Auto Zeitung, ADAC, evo, TÜV SÜD jt), mida mudel
EI OLE NÄINUD: ükski neist ei ole kalibreerimisel kasutatud. See on
seega päris väljaspool-valimi kontroll.

Kolm küsimust, kolm mõõdikut:

  A) MÄRGISE-REŽIIM ("mida leht ütleb testimata rehvi kohta"):
     rehvist teame ainult EPREL-i märgise klassi ja kategooriat, täpselt
     nagu veebileht. Viga = (ennustus - mõõdetud) / mõõdetud.

  B) TESTISISENE JÄRJESTUS: iga testi+ala sees eemaldatakse testi
     keskmine nihe (tundmatu temperatuur, katte haare). Järele jääb, kui
     hästi märgise klass seletab rehvide VAHET samas testis.
     + Spearmani korrelatsioon ennustatud ja mõõdetud järjestuse vahel.

  C) ÜLEKANNE: rehv, mis esineb kahes eri testis. Tema suhe
     mõõdetud/ennustatud ühest testist -> parandus teise testi
     ennustusele. Kas testitulemus kandub üle teisele mõõdule/autole/
     aastale? (see on see, mida leht teeb testitud rehvidega)

Andmekvaliteedi reeglid (vt SKIP): välja jäetakse tuletatud väärtused,
rühmakeskmised ja allika enda poolt kahtlaseks märgitud distsipliinid.
Kiirus, mis on "Auto Bildi tavaprotokolli järgi oletatud", on eraldi
lipuga ja tulemused näidatakse ka ilma nendeta.

Käivita:  python3 -m mudel.backtest_ext
"""
from __future__ import annotations

import glob
import json
import math
import os
import re
import statistics
from collections import defaultdict

from .model import BrakingModel, Conditions, Surface, Tyre, TyreCategory
from .presets import ALL_VEHICLES as VEHICLES

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "testid_ext")
CORE = os.path.join(HERE, "..", "veeb", "static", "data")
if not os.path.isdir(CORE):
    CORE = "veeb/static/data"

# --- välja jäetavad distsipliinid (test_id, distsipliin) ----------------
SKIP = {
    ("AUTOBILD-2023-S-225-45R18", "dry"): "allikas andis kuiv+märg summa; kuiv tuletatud",
    ("ViBilagare-2019-W-225-50R17", "dry"): "märgitud 80 km/h, väärtused sobivad 100 km/h-ga",
    ("EVO-2023-S-225-40R18", "wet"): "24-27 m 80 km/h-st, lõppkiirus teadmata",
}
# temperatuurid, mis on allikas (artiklis) antud, aga mitte distsipliini märkuses
TEMP_OVERRIDE = {("ZaRulem-2021-W-205-55R16-studded", "ice"): -9.0,   # -5...-13 °C
                 ("ZaRulem-2021-W-205-55R16-studded", "snow"): -9.0}
SKIP_TESTS = {"ZaRulem-2008-W-ICETEMP-mixed": "ainult rühmakeskmised"}

CAT = {"summer": TyreCategory.SUMMER_TOURING, "summer_uhp": TyreCategory.SUMMER_UHP,
       "allseason": TyreCategory.ALL_SEASON, "winter_central": TyreCategory.WINTER_CENTRAL,
       "winter_nordic": TyreCategory.WINTER_NORDIC, "winter_studded": TyreCategory.WINTER_STUDDED}
EKAT = [TyreCategory.SUMMER_TOURING, TyreCategory.ALL_SEASON,
        TyreCategory.WINTER_CENTRAL, TyreCategory.WINTER_NORDIC]
SURF = {"asphalt": Surface.ASPHALT, "concrete": Surface.CONCRETE, "snow": Surface.SNOW_PACKED,
        "ice": Surface.ICE, "gravel": Surface.GRAVEL}
CARS = [("golf gti", "vw_golf_8"), ("golf vii", "vw_golf_7"), ("golf", "vw_golf_8"),
        ("t-roc", "vw_troc"), ("tiguan", "vw_tiguan_2"), ("passat", "vw_passat_b8"),
        ("t6.1", "vw_transporter"), ("octavia", "skoda_octavia"), ("q5", "audi_q5_fy"),
        ("e-tron", "audi_etron"), ("q2", "audi_q2"), ("a6", "audi_a6_c8"), ("s4", "audi_a4_b9"),
        ("a4", "audi_a4_b9"), ("s3", "vw_golf_8"), ("320d", "bmw_320d"), ("3 series", "bmw_320d"),
        ("52", "bmw_520d_g30"), ("i20", "hyundai_i20_3"), ("astra", "opel_astra_k")]


def car_key(name):
    n = (name or "").lower()
    for pat, k in CARS:
        if pat in n and k in VEHICLES:
            return k
    return "vw_golf_8"


def size_key(size):
    m = re.search(r"(\d{3})/(\d{2}) ?Z?R ?(\d{2})", size or "")
    return (f"{m[1]}/{m[2]} R{m[3]}", f"{m[1]}{m[2]}R{m[3]}") if m else (None, None)


# --- EPREL-i märgise leidmine nime järgi ------------------------------------
_EPREL = {}
BRAND_ALIAS = {"conti": "continental", "vredestein": "vredestein", "bf goodrich": "bfgoodrich"}
SUFFIX_OK = {"xl", "suv", "ao", "mo", "ms", "seal", "sealinside", "elect", "plus", "s", "e", "rf", "rft",
             "runflat", "ssr", "driveguard", "contiseal", "fr", "nf0", "n0", "vol", "t0"}


def _tok(s):
    s = s.lower().replace("+", " plus ").replace("*", "")
    return [t for t in re.split(r"[^a-z0-9]+", s) if t]


def eprel_lookup(name, skey):
    """-> (klass, EPREL kategooria) või None. Nõuab, et KÕIK testinime
    mudeli-sõnad oleksid EPREL-i nimes; mitme kandidaadi korral valitakse
    lühim (kõige vähem lisasõnu) ja nõutakse, et klass oleks üheselt sama."""
    if skey not in _EPREL:
        p = os.path.join(CORE, "eprel", skey + ".json")
        _EPREL[skey] = json.load(open(p)) if os.path.exists(p) else []
    rows = _EPREL[skey]
    t = _tok(name)
    if not t or not rows:
        return None
    brand = BRAND_ALIAS.get(t[0], t[0])
    cands = []
    for r in rows:
        bt = _tok(r[1])
        if not bt or bt[0] != brand:
            continue
        # testinimes brändi järel olevad sõnad; mitmesõnaline bränd (BF Goodrich)
        model = t[len(bt):] if t[:len(bt)] == bt else t[1:]
        tm, rn = "".join(model), "".join(_tok(r[2]))
        if not tm or not rn:
            continue
        if tm == rn:
            d = 0
        elif rn.startswith(tm) and rn[len(tm):] in SUFFIX_OK:
            d = 1       # EPREL-i nimes lisa-tähis (XL, SUV, AO ...)
        elif tm.startswith(rn) and re.fullmatch(r"[a-z]{0,2}\d{2,4}|suv|xl", tm[len(rn):]):
            d = 2       # testinimes mustrikood (nt W462)
        elif tm.endswith(rn) and len(rn) >= 3 and len(tm) - len(rn) <= 10:
            d = 3       # EPREL jätab alambrändi ära (Ecsta HS52 -> HS52)
        else:
            continue
        cands.append((d, r))
    if not cands:
        return None
    best = min(c[0] for c in cands)
    top = [r for d, r in cands if d == best]
    gs = {r[4] for r in top}
    if len(gs) != 1:
        return None
    return top[0][4], EKAT[top[0][3]] if 0 <= top[0][3] < 4 else None


def gmid(core, g, cat):
    t = core["gClass"].get(g)
    if t:
        if cat.name in t:
            return t[cat.name][0]
        if t.get("_") and t["_"][1]:
            return t["_"][0]
    return {"A": 1.60, "B": 1.47, "C": 1.32, "D": 1.17, "E": 1.05}[g]


# --- vaatlused ---------------------------------------------------------------
def default_temp(season, surface, note):
    n = (note or "").replace("−", "-").replace("–", "-")
    m = re.search(r"(-?\d+(?:[.,]\d+)?)\s*(?:…|\.\.\.|\bto\b|/)\s*(-?\d+(?:[.,]\d+)?)\s*°?\s*C\b", n) \
        or re.search(r"(-\d+(?:[.,]\d+)?)\s*-\s*(-?\d+(?:[.,]\d+)?)\s*°?\s*C\b", n)
    if m and surface in ("snow", "ice"):
        a, b = (float(x.replace(",", ".")) for x in m.groups())
        if a < 0 < b:          # "-20...25 °C" tähendab -20...-25
            b = -b
        return (a + b) / 2, "vahemiku keskpunkt"
    m1 = re.search(r"(-\d+(?:[.,]\d+)?)\s*°?\s*C\b", n)
    if m1 and surface in ("snow", "ice"):
        return float(m1[1].replace(",", ".")), "allika märkus"
    if surface == "snow":
        return -5.0, "oletus"
    if surface == "ice":
        return -5.0, "oletus"
    return (20.0 if season == "summer" else 8.0), "oletus"


def load():
    obs, skipped = [], defaultdict(int)
    for f in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        for t in json.load(open(f, encoding="utf-8")):
            if t["test_id"] in SKIP_TESTS:
                skipped["rühmakeskmine"] += 1
                continue
            size, skey = size_key(t["size"])
            veh = car_key(t.get("car"))
            ds = {x["id"]: x for x in t["disciplines"]}
            for ty in t["tyres"]:
                for did, val in (ty.get("results") or {}).items():
                    x = ds.get(did)
                    if val is None or x is None:
                        continue
                    if (t["test_id"], did) in SKIP:
                        skipped["allikas kahtlane/tuletatud"] += 1
                        continue
                    if x.get("v_from") is None or x.get("v_to") is None:
                        skipped["kiirus teadmata"] += 1
                        continue
                    if x["surface"] not in SURF:
                        continue
                    note = (x.get("note") or "")
                    temp = x.get("temp_c")
                    tsrc = "allikas"
                    if temp is None and (t["test_id"], x["surface"]) in TEMP_OVERRIDE:
                        temp, tsrc = TEMP_OVERRIDE[(t["test_id"], x["surface"])], "artikkel"
                    if temp is None:
                        temp, tsrc = default_temp(t["season"], x["surface"], note)
                    wet = bool(x.get("wet")) and x["surface"] in ("asphalt", "concrete")
                    water = 1.0
                    mw = re.search(r"(\d+(?:\.\d+)?)\s*mm", note)
                    if wet and mw and 0.3 <= float(mw[1]) <= 3:
                        water = float(mw[1])
                    obs.append(dict(
                        test=t["test_id"], pub=t["publication"], year=t["year"], season=t["season"],
                        size=size, skey=skey, veh=veh, tyre=ty["name"].strip(),
                        cat=CAT.get(ty.get("category"), TyreCategory.SUMMER_TOURING),
                        label=ty.get("label_wet"), surface=x["surface"], wet=wet, water=water,
                        v0=float(x["v_from"]), v1=float(x["v_to"]), temp=temp, tsrc=tsrc,
                        measured=float(val), disc=did,
                        speed_assumed=any(k in note.lower() for k in ("verify", "assum")),
                    ))
    return obs, skipped


def kind(o):
    return ("märg " if o["wet"] else "kuiv ") + o["surface"] if o["surface"] in ("asphalt", "concrete") else o["surface"]


def predict_label(model, core, o):
    """Märgise-režiim: G EPREL-ist (klassi keskpunkt kategooria kaupa)."""
    if o["cat"] is TyreCategory.WINTER_STUDDED:
        g, cat = "D", TyreCategory.WINTER_STUDDED     # naastrehvil märgist ei ole
    else:
        hit = eprel_lookup(o["tyre"], o["skey"]) if o["skey"] else None
        if not hit:
            return None, None
        g, ecat = hit
        cat = ecat or o["cat"]
    if o["size"] is None:
        return None, None
    ty = Tyre(name=o["tyre"], category=cat, wet_grip_index=gmid(core, g, cat), size=o["size"])
    veh = VEHICLES[o["veh"]]
    cond = Conditions(speed_kmh=o["v0"], surface=SURF[o["surface"]], water_mm=o["water"] if o["wet"] else 0.0,
                      temp_c=o["temp"], payload_kg=150.0)
    o["sig"] = model.stopping_distance(ty, veh, cond).sigma_rel
    return model.distance_between(ty, veh, cond, o["v0"], o["v1"]), g


def spearman(a, b):
    def rank(x):
        s = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x)
        i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and x[s[j + 1]] == x[s[i]]:
                j += 1
            for k in range(i, j + 1):
                r[s[k]] = (i + j) / 2
            i = j + 1
        return r
    ra, rb = rank(a), rank(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else float("nan")


def norm_name(n):
    return " ".join(_tok(n))


def run(verbose=True):
    core = json.load(open(os.path.join(CORE, "core.json"), encoding="utf-8"))
    model = BrakingModel()
    obs, skipped = load()
    for o in obs:
        o["pred"], o["g"] = predict_label(model, core, o)
    got = [o for o in obs if o["pred"]]
    out = {"n_obs": len(obs), "n_pred": len(got), "skipped": dict(skipped)}

    def stats(rows):
        e = [(o["pred"] - o["measured"]) / o["measured"] for o in rows]
        cov = [abs(o["pred"] - o["measured"]) / o["pred"] <= o["sig"] for o in rows]
        return dict(n=len(e), mae=statistics.mean(abs(x) for x in e), bias=statistics.mean(e),
                    cover=sum(cov) / len(cov), sig=statistics.mean(o["sig"] for o in rows),
                    p90=sorted(abs(x) for x in e)[int(0.9 * (len(e) - 1))])

    # A) märgise-režiim
    A = defaultdict(list)
    for o in got:
        A[kind(o)].append(o)
    out["A"] = {k: stats(v) for k, v in sorted(A.items())}
    out["A_confirmed_speed"] = {k: stats([o for o in v if not o["speed_assumed"]])
                                for k, v in sorted(A.items()) if any(not o["speed_assumed"] for o in v)}
    byCat = defaultdict(list)
    for o in got:
        byCat[(kind(o), o["cat"].name)].append(o)
    out["A_by_cat"] = {f"{k[0]} | {k[1]}": stats(v) for k, v in sorted(byCat.items()) if len(v) >= 8}

    # B) testisisene: testi nihe eemaldatud
    grp = defaultdict(list)
    for o in got:
        grp[(o["test"], o["disc"])].append(o)
    within, rhos, offsets = defaultdict(list), defaultdict(list), defaultdict(list)
    for (tid, did), rows in grp.items():
        if len(rows) < 4:
            continue
        ratio = statistics.median(o["measured"] / o["pred"] for o in rows)
        offsets[kind(rows[0])].append(ratio - 1)
        for o in rows:
            within[kind(o)].append(abs(o["pred"] * ratio - o["measured"]) / o["measured"])
        if len({o["g"] for o in rows}) > 1:
            rhos[kind(rows[0])].append(spearman([o["pred"] for o in rows], [o["measured"] for o in rows]))
    out["B"] = {k: dict(n=len(v), mae_within=statistics.mean(v),
                        test_offset_sd=statistics.pstdev(offsets[k]) if len(offsets[k]) > 1 else None,
                        test_offset_mean=statistics.mean(offsets[k]),
                        n_tests=len(offsets[k]),
                        spearman_median=statistics.median(rhos[k]) if rhos[k] else None)
                for k, v in sorted(within.items())}

    # C) ülekanne sama rehvi kahe testi vahel
    by = defaultdict(list)
    for o in got:
        by[(norm_name(o["tyre"]), kind(o))].append(o)
    med = {key: statistics.median(o["measured"] / o["pred"] for o in rows)
           for key, rows in grp.items() if len(rows) >= 4}
    base_e, tr_e, rb_e, rt_e = [], [], [], []
    for (_, k), rows in by.items():
        tests = {o["test"] for o in rows}
        if len(tests) < 2:
            continue
        for i in rows:
            for j in rows:
                if i["test"] == j["test"]:
                    continue
                f = i["measured"] / i["pred"]
                base_e.append(abs(j["pred"] - j["measured"]) / j["measured"])
                tr_e.append(abs(j["pred"] * f - j["measured"]) / j["measured"])
                mi, mj = med.get((i["test"], i["disc"])), med.get((j["test"], j["disc"]))
                if mi and mj:
                    # testi tingimused teada (teiste rehvide järgi); kas rehvi
                    # SUHTELINE koht testis i ennustab tema kohta testis j?
                    rb_e.append(abs(j["pred"] * mj - j["measured"]) / j["measured"])
                    rt_e.append(abs(j["pred"] * mj * (f / mi) - j["measured"]) / j["measured"])
    out["C"] = dict(pairs=len(tr_e), mae_label=statistics.mean(base_e) if base_e else None,
                    mae_transfer=statistics.mean(tr_e) if tr_e else None,
                    pairs_rel=len(rt_e), mae_label_rel=statistics.mean(rb_e) if rb_e else None,
                    mae_transfer_rel=statistics.mean(rt_e) if rt_e else None)
    out["eprel_found"] = sum(1 for o in obs if o["pred"]) / max(1, len(obs))
    if verbose:
        report(out)
    return out, obs


def report(o):
    pct = lambda x: f"{x*100:5.1f} %" if x is not None else "   -  "
    print(f"Vaatlusi {o['n_obs']}, ennustatud {o['n_pred']} (EPREL leitud {o['eprel_found']*100:.0f} %). "
          f"Välja jäetud: {o['skipped']}")
    print("\nA) MÄRGISE-REŽIIM (nagu leht testimata rehvi kohta)")
    for k, s in o["A"].items():
        print(f"   {k:<16} n={s['n']:<4} keskm. viga {pct(s['mae'])}  nihe {pct(s['bias'])}  p90 {pct(s['p90'])}  "
              f"lehe vahemik (±{s['sig']*100:.0f} %) katab {s['cover']*100:.0f} % (1 sigma, oodatav 68 %)")
    print("   -- ainult kinnitatud kiirusega:")
    for k, s in o["A_confirmed_speed"].items():
        print(f"   {k:<16} n={s['n']:<4} keskm. viga {pct(s['mae'])}  nihe {pct(s['bias'])}")
    print("   -- kategooria kaupa:")
    for k, s in o["A_by_cat"].items():
        print(f"   {k:<34} n={s['n']:<4} keskm. viga {pct(s['mae'])}  nihe {pct(s['bias'])}")
    print("\nB) TESTISISENE (testi nihe eemaldatud) — kui hästi märgis seletab rehvide vahet")
    for k, s in o["B"].items():
        print(f"   {k:<16} n={s['n']:<4} viga {pct(s['mae_within'])}  testide nihe keskm {pct(s['test_offset_mean'])} "
              f"sd {pct(s['test_offset_sd'])} ({s['n_tests']} testi)  Spearman {s['spearman_median'] if s['spearman_median'] is None else round(s['spearman_median'],2)}")
    c = o["C"]
    print(f"\nC) ÜLEKANNE: {c['pairs']} paari (sama rehv, eri test). Märgise järgi {pct(c['mae_label'])}, "
          f"teise testi tulemusega {pct(c['mae_transfer'])}")
    print(f"   testi nihe teada ({c['pairs_rel']} paari): märgise järgi {pct(c['mae_label_rel'])}, "
          f"rehvi suhteline koht teisest testist {pct(c['mae_transfer_rel'])}")


if __name__ == "__main__":
    run()
