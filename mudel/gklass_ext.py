"""Märgise klass -> G uuesti, päris EPREL-i märgistega välistestidest.

MIKS
----
g_class_measured.py (kalibreeri_gklass.py) võttis iga (klass, kategooria)
lahtri väärtuseks testitud rehvide tuletatud G mediaani. Rehve oli
lahtris 3-13, peaaegu kõik kahest 2025. aasta testist. Välistestide
backtest (backtest_ext.py) näitas süstemaatilist nihet:

  Kesk-Euroopa talverehv märjal: mõõdetud 7-9 % PIKEM kui ennustus,
      9 testi 12-st samas suunas;
  lamellrehv (B, C):             mõõdetud ~8 % LÜHEM, 8 testi 10-st.

Siin tehakse täpselt sama arvutus mis kalibreeri_gklass.py-s, aga
rohkemate rehvidega: iga välistesti märja asfaldi tulemuse kohta
lahendatakse G, mis annab mudelis täpselt mõõdetud pidurdusmaa (testi
kiirusel, autol ja temperatuuril), ja lahtri väärtus on mediaan üle
rehvide (iga rehv kõigepealt oma testide mediaaniks, et üks sageli
testitud rehv ei kaaluks üle).

KONTROLL (ilma selleta ei kirjutata midagi)
  * jäta-üks-test-välja: iga test ennustatakse tabeliga, mis on
    ehitatud ILMA selle testita. Uus tabel peab olema parem kui
    praegune tabel (mis nende testide peal on niikuinii väljaspool
    valimit).
  * vanad 369 ankrut peavad jääma samaks (märgise klass mõjutab ainult
    lehe klassiridu, mitte ankruid -- kontrollitakse igaks juhuks).

Käivita:  python3 -m mudel.gklass_ext           (ainult aruanne)
          python3 -m mudel.gklass_ext --write   (kirjutab g_class_measured.py)
"""
from __future__ import annotations

import collections
import statistics as st
import sys
import time

from . import backtest_ext as B
from .kalibreeri_gklass import MIN_N, OUT, measure as measure_old
from .model import BrakingModel, Conditions, Tyre, TyreCategory
from .presets import ALL_VEHICLES as VEHICLES, G_CLASS


def _dist(model, o, cat, G):
    ty = Tyre(name=o["tyre"], category=cat, wet_grip_index=G, size=o["size"])
    cond = B.Conditions(ice_road=False, speed_kmh=o["v0"], surface=B.SURF[o["surface"]], water_mm=o["water"],
                        temp_c=o["temp"], payload_kg=150.0)
    return model.distance_between(ty, VEHICLES[o["veh"]], cond, o["v0"], o["v1"])


def solve_G(model, o, cat, lo=0.6, hi=2.4):
    """G, mille korral mudel annab täpselt mõõdetud pidurdusmaa."""
    dlo, dhi = _dist(model, o, cat, lo), _dist(model, o, cat, hi)
    if not (dhi <= o["measured"] <= dlo):
        return None          # väljaspool mudeli ulatust (nt vesiliug) -- ei kasutata
    for _ in range(14):
        mid = (lo + hi) / 2
        if _dist(model, o, cat, mid) > o["measured"]:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def wet_obs():
    obs, _ = B.load()
    out = []
    for o in obs:
        if not (o["wet"] and o["surface"] == "asphalt") or o["cat"] is TyreCategory.WINTER_STUDDED:
            continue
        if not o["skey"]:
            continue
        hit = B.eprel_lookup(o["tyre"], o["skey"])
        if not hit:
            continue
        o["g"], ecat = hit
        o["ecat"] = ecat or o["cat"]
        out.append(o)
    return out


def build_table(cells):
    """cells: (klass, kategooria) -> {rehv: [G, ...]} -> sama kuju mis G_CLASS_MEASURED."""
    per_cell = {k: [st.median(v) for v in tyres.values()] for k, tyres in cells.items()}
    out = {}
    for g in "ABCDE":
        kat = {c: v for (gg, c), v in per_cell.items() if gg == g and len(v) >= MIN_N}
        allv = [x for (gg, _c), v in per_cell.items() if gg == g for x in v]
        base = min(round(st.median(v), 3) for v in kat.values()) if kat else G_CLASS[g]
        out[g] = {"_": [base, len(allv) if kat else 0]}
        for c, v in sorted(kat.items()):
            out[g][c] = [round(st.median(v), 3), len(v)]
    # KLASSIDE JÄRJESTUS kategooria sees: parem klass ei tohi anda väiksemat
    # G-d kui halvem. Puuduv lahter läheb "_" varuväärtusele (klassi kõige
    # kehvem kategooria), mis võib olla VÄIKSEM kui sama kategooria järgmise
    # klassi mõõdetud väärtus (nt Põhjamaade C varu 1,166 < Põhjamaade D
    # 1,225). Siis kirjutatakse lahter välja halvema klassi väärtusega
    # (ja selle n-iga). Mõõdetud lahtrite vastuolu korral keskmistatakse
    # naabrid (isotooniline regressioon, kaalud = n).
    cats = sorted({c for g in out for c in out[g] if c != "_"})
    for c in cats:
        seq = []
        for g in "ABCDE":
            if c in out[g]:
                seq.append([g, out[g][c][0], out[g][c][1], True])
            else:
                seq.append([g, gval(out, g, c), 0, False])
        # alt üles: puuduv lahter vähemalt nii hea kui halvem klass
        for i in range(3, -1, -1):
            if not seq[i][3] and seq[i][1] < seq[i + 1][1]:
                seq[i][1], seq[i][2] = seq[i + 1][1], seq[i + 1][2]
                out[seq[i][0]][c] = [seq[i][1], seq[i][2]]
        # mõõdetud lahtrite vastuolud: kaalutud keskmine (PAV)
        changed = True
        while changed:
            changed = False
            for i in range(4):
                a, b = seq[i], seq[i + 1]
                if a[1] < b[1] and a[3] and b[3]:
                    w = max(1, a[2]) + max(1, b[2])
                    m = round((a[1] * max(1, a[2]) + b[1] * max(1, b[2])) / w, 3)
                    a[1] = b[1] = m
                    out[a[0]][c][0] = out[b[0]][c][0] = m
                    changed = True
    return out


def gval(tbl, g, cat):
    t = tbl.get(g, {})
    if cat in t:
        return t[cat][0]
    if t.get("_") and t["_"][1]:
        return t["_"][0]
    return G_CLASS[g]


def main(write=False):
    model = BrakingModel()
    t0 = time.time()
    obs = wet_obs()
    for o in obs:
        o["G"] = solve_G(model, o, o["ecat"])
    obs = [o for o in obs if o["G"]]
    print(f"{len(obs)} märga tulemust päris märgisega, G lahendatud ({time.time()-t0:.0f} s)")

    old_by, _miss = measure_old()          # praegused (klass, kat) -> [G ...] testitud rehvidest
    def cells_from(rows):
        c = collections.defaultdict(lambda: collections.defaultdict(list))
        for (g, cat), vals in old_by.items():
            for i, v in enumerate(vals):
                c[(g, cat)][f"_vana_{g}_{cat}_{i}"].append(v)
        for o in rows:
            c[(o["g"], o["ecat"].name)][B.norm_name(o["tyre"])].append(o["G"])
        return c

    from .g_class_measured import G_CLASS_MEASURED as CUR
    # jäta-üks-test-välja
    tests = sorted({o["test"] for o in obs})
    e_cur, e_new = [], []
    by_cat = collections.defaultdict(lambda: [[], []])
    for tid in tests:
        train = [o for o in obs if o["test"] != tid]
        tbl = build_table(cells_from(train))
        for o in (x for x in obs if x["test"] == tid):
            cat = o["ecat"]
            dc = _dist(model, o, cat, gval(CUR, o["g"], cat.name))
            dn = _dist(model, o, cat, gval(tbl, o["g"], cat.name))
            ec, en = (dc - o["measured"]) / o["measured"], (dn - o["measured"]) / o["measured"]
            e_cur.append(ec); e_new.append(en)
            by_cat[cat.name][0].append(ec); by_cat[cat.name][1].append(en)
    mae = lambda e: st.mean(abs(x) for x in e)
    print(f"\nJÄTA-ÜKS-TEST-VÄLJA ({len(tests)} testi, {len(e_cur)} tulemust)")
    print(f"   praegune tabel: keskm. viga {mae(e_cur)*100:5.2f} %  nihe {st.mean(e_cur)*100:+5.2f} %")
    print(f"   uus tabel:      keskm. viga {mae(e_new)*100:5.2f} %  nihe {st.mean(e_new)*100:+5.2f} %")
    for c, (a, b) in sorted(by_cat.items()):
        print(f"   {c:<16} n={len(a):<4} praegu {mae(a)*100:5.2f} % ({st.mean(a)*100:+5.1f})  "
              f"uus {mae(b)*100:5.2f} % ({st.mean(b)*100:+5.1f})")
    full = build_table(cells_from(obs))
    print("\nUUS TABEL (vs praegune)")
    for g in "ABCDE":
        for c, v in full[g].items():
            cur = CUR.get(g, {}).get(c)
            print(f"   {g} {c:<16} {v[0]:.3f} (n={v[1]:<3})   praegu {cur[0] if cur else '-'} (n={cur[1] if cur else '-'})")
    ok = mae(e_new) < mae(e_cur)
    print("\nOTSUS:", "uus tabel on väljaspool valimit parem" if ok else "uus tabel EI OLE parem -- ei kirjutata")
    if write and ok:
        src = ['# -*- coding: utf-8 -*-',
               '"""MÕÕDETUD klassi keskmised -- loodud automaatselt.',
               '',
               'Tee see uuesti:  python3 -m mudel.gklass_ext --write',
               'Allikad: testitud rehvid (kalibreeri_gklass.py) + välistestid',
               '(testid_ext/, päris EPREL-i märgised, vt gklass_ext.py).',
               f'Jäta-üks-test-välja: praegune {mae(e_cur)*100:.2f} % -> uus {mae(e_new)*100:.2f} %.',
               '',
               'Kuju: klass -> {"_": [G, n]} pluss (kategooria: [G, n]) seal, kus',
               'mõõdetud rehve on vähemalt %d. n = mitu mõõdetud rehvi väärtuse taga.' % MIN_N,
               'Loodud: %s' % time.strftime("%Y-%m-%d"),
               '"""', '', 'G_CLASS_MEASURED = {']
        for g in "ABCDE":
            src.append(f"    '{g}': {full[g]!r},")
        src.append('}')
        open(OUT, "w", encoding="utf-8").write("\n".join(src) + "\n")
        print("kirjutatud:", OUT)
    return full


if __name__ == "__main__":
    main(write="--write" in sys.argv)
