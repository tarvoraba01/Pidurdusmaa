"""
Kalibreerimine ja valideerimine.

Kaks eraldi režiimi, sest nad vastavad kahele eri küsimusele:

  A) "MÄRGISE-REŽIIM" — mudel teab rehvist ainult seda, mida EPREL annab:
     kategooria + märghaardumise indeks G. Ei mingeid rehvipõhiseid
     testandmeid. See on see täpsus, mida veebileht saab pakkuda IGA
     rehvi kohta, mida keegi küsib.

  B) "ANKRU-REŽIIM" — rehvi kohta on olemas üks päris testitulemus,
     millest tuletatakse tema mu. Mudel peab siis üle kandma teistele
     kiirustele, temperatuuridele, rõhkudele ja mustrisügavustele.
     See on see täpsus, mida saab pakkuda testitud rehvide kohta.

Käivita:  python3 -m pidurdus.calibrate
"""

from __future__ import annotations

import math
import statistics
from dataclasses import replace

from .anchors import ANCHORS, Anchor
from .model import (BrakingModel, Calibration, Conditions, Surface, Tyre,
                    TyreCategory)
from .presets import ALL_VEHICLES as VEHICLES, G_CLASS

# ---------------------------------------------------------------------------


def build_tyre(a: Anchor, tread_mm: float = None) -> Tyre:
    """Rehv AINULT märgise info põhjal (režiim A).
    Kui ankrul on G juba teada (nt sama testi märjast katsest tuletatud),
    kasutatakse seda."""
    return Tyre(name=a.tyre_key, category=a.category,
                wet_grip_index=(a.wet_grip_index if a.wet_grip_index is not None
                                else G_CLASS[a.wet_grip_class]),
                tread_depth_mm=tread_mm if tread_mm else a.tread_mm,
                tread_depth_new_mm=8.0, size=a.size)


def predict(model: BrakingModel, a: Anchor, tyre: Tyre = None) -> float:
    veh = VEHICLES[a.vehicle_key]
    ty = tyre or build_tyre(a)
    cond = Conditions(speed_kmh=a.v_from_kmh, surface=a.surface,
                      texture=a.texture, water_mm=a.water_mm,
                      temp_c=a.temp_c, payload_kg=150.0)
    return model.distance_between(ty, veh, cond, a.v_from_kmh, a.v_to_kmh)


def errors(model: BrakingModel, anchors=ANCHORS, tyre_fn=None):
    out = []
    for a in anchors:
        ty = tyre_fn(a) if tyre_fn else None
        p = predict(model, a, ty)
        out.append((a, p, (p - a.measured_m) / a.measured_m))
    return out


def summarise(rows, label: str) -> dict:
    errs = [abs(e) for _, _, e in rows]
    bias = [e for _, _, e in rows]
    n = len(errs)
    within10 = sum(1 for e in errs if e <= 0.10) / n
    within15 = sum(1 for e in errs if e <= 0.15) / n
    return dict(label=label, n=n,
                mae=statistics.mean(errs),
                bias=statistics.mean(bias),
                p90=sorted(errs)[int(0.9 * (n - 1))],
                worst=max(errs),
                within10=within10, within15=within15)


def print_summary(s):
    print(f"  {s['label']:<34} n={s['n']:<3} "
          f"keskmine viga {s['mae']*100:5.1f} %   "
          f"nihe {s['bias']*100:+5.1f} %   "
          f"90% kvantiil {s['p90']*100:5.1f} %   "
          f"halvim {s['worst']*100:5.1f} %   "
          f"±10% sees {s['within10']*100:3.0f} %   "
          f"±15% sees {s['within15']*100:3.0f} %")


# ---------------------------------------------------------------------------
# Lihtne koordinaatotsing (ei taha numpy/scipy sõltuvust)
# ---------------------------------------------------------------------------

def optimise(cal: Calibration, params, anchors, iters=6, grid=False):
    """params: list of (getter, setter, lo, hi)."""
    model = BrakingModel(cal)

    def cost(c):
        m = BrakingModel(c)
        return statistics.mean(abs(e) for _, _, e in errors(m, anchors))

    # jäme võrguotsing, et mitte kohalikku miinimumi kinni jääda
    if grid and len(params) == 1:
        get, setr, lo, hi = params[0]
        best_v, best_c = get(cal), cost(cal)
        for i in range(41):
            v = lo + (hi - lo) * i / 40
            setr(cal, v)
            c = cost(cal)
            if c < best_c:
                best_c, best_v = c, v
        setr(cal, best_v)

    best = cost(cal)
    for it in range(iters):
        for get, setr, lo, hi in params:
            cur = get(cal)
            span = (hi - lo) / (3 ** (it + 1))
            for cand in (cur - span, cur + span):
                cand = max(lo, min(hi, cand))
                setr(cal, cand)
                c = cost(cal)
                if c < best - 1e-9:
                    best = c
                    cur = cand
                else:
                    setr(cal, cur)
    return cal, best


# ---------------------------------------------------------------------------


def main():
    print("=" * 100)
    print("PIDURDUSMAA MUDEL — kalibreerimine ja valideerimine")
    print("=" * 100)

    dry = [a for a in ANCHORS if a.surface is Surface.ASPHALT and a.water_mm == 0]
    wet = [a for a in ANCHORS if a.surface is Surface.ASPHALT and a.water_mm > 0]
    ice = [a for a in ANCHORS if a.surface is Surface.ICE]

    cal = Calibration()

    # --- 1. sobita märja mudeli põhikonstant k_G --------------------------
    print("\n1) Märghaardumine: sobitan k_G (mu_märg = k_G · G)")
    print("   NB: märja kiirusesõltuvus (wet_lift_b) ja akvaplaneerimise")
    print("   lävi (hp_*) EI OLE siin sobitatavad — ankrutes on ainult üks")
    print("   märja katse alguskiirus (80 km/h) ja üks veekile paksus.")
    print("   Need tulevad kirjandusest ja vajavad eraldi valideerimist")
    print("   (vt README, 'Teadaolevad puudujäägid').")
    params = [
        (lambda c: c.k_g, lambda c, v: setattr(c, "k_g", v), 0.30, 0.70),
    ]
    cal, _ = optimise(cal, params, wet, iters=8, grid=True)
    print(f"   k_G = {cal.k_g:.4f}   (ehk A-klassi rehv, G=1.60 -> "
          f"mu_ref = {cal.k_g*1.60:.3f} asfaldil 20 °C, 1 mm vett, 80 km/h)")
    print(f"   hüdrodünaamiline tegur wet_lift_b = {cal.wet_lift_b:.2f} "
          f"[kirjandusest, fikseeritud]")

    # --- 2. sobita kuivade kategooriate baas ------------------------------
    print("\n2) Kuivhaardumine: sobitan kategooriapõhise baasi")
    cats = sorted({a.category for a in dry}, key=lambda c: c.name)
    dparams = []
    for cat in cats:
        dparams.append((
            (lambda c, k=cat: c.mu_dry_base[k]),
            (lambda c, v, k=cat: c.mu_dry_base.__setitem__(k, v)),
            0.60, 1.45))
    cal, _ = optimise(cal, dparams, dry, iters=7)
    for cat in cats:
        print(f"   {cat.value:<38} mu_kuiv = {cal.mu_dry_base[cat]:.3f}")

    # --- 3. sobita jää ----------------------------------------------------
    print("\n3) Jää: sobitan kategooriapõhise baasi (-5 °C)")
    icats = sorted({a.category for a in ice}, key=lambda c: c.name)
    iparams = []
    for cat in icats:
        iparams.append((
            (lambda c, k=cat: c.mu_ice_base[k]),
            (lambda c, v, k=cat: c.mu_ice_base.__setitem__(k, v)),
            0.05, 0.45))
    cal, _ = optimise(cal, iparams, ice, iters=7)
    for cat in icats:
        print(f"   {cat.value:<38} mu_jää  = {cal.mu_ice_base[cat]:.3f}")

    model = BrakingModel(cal)

    # --- 4. režiim A: ainult märgise info ---------------------------------
    print("\n" + "-" * 100)
    print("REŽIIM A — mudel teab ainult EPREL-i infot (kategooria + G-klass)")
    print("-" * 100)
    all_rows = errors(model, ANCHORS)
    print_summary(summarise([r for r in all_rows if r[0] in dry], "kuiv asfalt"))
    print_summary(summarise([r for r in all_rows if r[0] in wet], "märg asfalt"))
    print_summary(summarise([r for r in all_rows if r[0] in ice], "jää"))
    print_summary(summarise(all_rows, "KÕIK"))

    # --- 5. AUS VALIDEERIMINE ---------------------------------------------
    # Ülal olev on sobitus, mitte valideerimine. Kaks päris testi:
    print("\n" + "-" * 100)
    print("VALIDEERIMINE 1 — ristkontroll kahe sõltumatu testi vahel")
    print("  k_G sobitatakse AINULT talvetestile (TM25, VW Golf, 205/55 R16)")
    print("  ja seda kasutatakse ennustamaks suvetesti (UT25, Audi A3,")
    print("  225/45 R17) — teine labor, teine auto, teine rehvitüüp.")
    print("-" * 100)
    tm_wet = [a for a in wet if a.source == "TM25"]
    ut_wet = [a for a in wet if a.source == "UT25"]

    cal_tm = Calibration()
    cal_tm.mu_dry_base = dict(cal.mu_dry_base)
    cal_tm.mu_ice_base = dict(cal.mu_ice_base)
    cal_tm, _ = optimise(cal_tm, [
        (lambda c: c.k_g, lambda c, v: setattr(c, "k_g", v), 0.30, 0.70),
    ], tm_wet, iters=8, grid=True)
    m_tm = BrakingModel(cal_tm)
    print(f"   ainult TM25 pealt sobitatud k_G = {cal_tm.k_g:.4f} "
          f"(kõigi andmete peal {cal.k_g:.4f})")
    print_summary(summarise(errors(m_tm, tm_wet), "TM25 (sobitatud, in-sample)"))
    print_summary(summarise(errors(m_tm, ut_wet), "UT25 (ENNUSTUS, out-of-sample)"))

    cal_ut = Calibration()
    cal_ut.mu_dry_base = dict(cal.mu_dry_base)
    cal_ut.mu_ice_base = dict(cal.mu_ice_base)
    cal_ut, _ = optimise(cal_ut, [
        (lambda c: c.k_g, lambda c, v: setattr(c, "k_g", v), 0.30, 0.70),
    ], ut_wet, iters=8, grid=True)
    m_ut = BrakingModel(cal_ut)
    print(f"   ainult UT25 pealt sobitatud k_G = {cal_ut.k_g:.4f}")
    print_summary(summarise(errors(m_ut, ut_wet), "UT25 (sobitatud, in-sample)"))
    print_summary(summarise(errors(m_ut, tm_wet), "TM25 (ENNUSTUS, out-of-sample)"))

    print("\n" + "-" * 100)
    print("VALIDEERIMINE 2 — leave-one-out: iga rehv jäetakse sobitusest välja")
    print("  ja seejärel ennustatakse. Näitab, kui palju veast tuleb sellest,")
    print("  et märgise klass ei erista ühe klassi sees olevaid rehve.")
    print("-" * 100)
    loo = leave_one_out(cal, ANCHORS)
    for name, subset in (("kuiv asfalt", dry), ("märg asfalt", wet), ("jää", ice)):
        print_summary(summarise([r for r in loo if r[0] in subset], name))
    print_summary(summarise(loo, "KÕIK (leave-one-out)"))

    # --- 5c. miks kaks testi ei ühti? -------------------------------------
    print("\n" + "-" * 100)
    print("VALIDEERIMINE 3 — kust tuleb testidevaheline nihe?")
    print("  Talverehvide märghaardumise klass on siin ANDMESTIKUS OLETUS.")
    print("  Skaneerime, millise G juures kaks sõltumatut testi ühte k_G-d")
    print("  annavad. Kui vastus on realistlik klass, siis mudeli struktuur")
    print("  on korras ja puudu on ainult päris EPREL-i andmed.")
    print("-" * 100)
    print(f"  {'talverehvi G':>13}{'klass':>7}{'k_G TM25':>11}"
          f"{'k_G UT25':>11}{'erinevus':>11}")
    k_ut = cal_ut.k_g
    for g_w, cls in ((1.47, "B"), (1.32, "C"), (1.17, "D"), (1.05, "E")):
        tm_scaled = [replace(a, wet_grip_class="X") for a in tm_wet]
        c = Calibration()
        c.mu_dry_base, c.mu_ice_base = dict(cal.mu_dry_base), dict(cal.mu_ice_base)
        G_CLASS["X"] = g_w
        c, _ = optimise(c, [(lambda x: x.k_g,
                             lambda x, v: setattr(x, "k_g", v), 0.30, 0.80)],
                        tm_scaled, iters=8, grid=True)
        diff = (c.k_g - k_ut) / k_ut * 100
        flag = "  <-- ühtivad" if abs(diff) < 3 else ""
        print(f"  {g_w:>13.2f}{cls:>7}{c.k_g:>11.4f}{k_ut:>11.4f}"
              f"{diff:>10.1f} %{flag}")
    G_CLASS.pop("X", None)

    # --- 6. seosekontrollid ----------------------------------------------
    print("\n" + "-" * 100)
    print("SEOSEKONTROLLID — kas mudel reprodutseerib teadaolevaid seoseid?")
    print("-" * 100)
    check_relations(model)

    # --- 7. halvimad üksikvead -------------------------------------------
    print("\n" + "-" * 100)
    print("REŽIIM A — 8 halvimat üksikpunkti")
    print("-" * 100)
    worst = sorted(all_rows, key=lambda r: -abs(r[2]))[:8]
    print(f"  {'rehv':<24}{'test':<7}{'pind':<10}"
          f"{'mõõdetud':>10}{'mudel':>9}{'viga':>9}")
    for a, p, e in worst:
        print(f"  {a.tyre_key:<24}{a.source:<7}"
              f"{('märg' if a.water_mm else a.surface.value):<10}"
              f"{a.measured_m:>9.1f} m{p:>8.1f} m{e*100:>8.1f} %")

    print("\n" + "=" * 100)
    return cal, model


def leave_one_out(cal_full: Calibration, anchors):
    """Iga ankru jaoks: sobita kategooria baas ilma selle punktita, siis ennusta.
    Kiiruse huvides sobitatakse ainult see üks parameeter, mis punkti mõjutab."""
    rows = []
    for a in anchors:
        rest = [b for b in anchors
                if not (b.tyre_key == a.tyre_key and b.surface is a.surface
                        and (b.water_mm > 0) == (a.water_mm > 0))
                and b.surface is a.surface
                and (b.water_mm > 0) == (a.water_mm > 0)
                and b.category is a.category
                and b.source == a.source]
        if not rest:
            continue
        c = Calibration()
        c.k_g = cal_full.k_g
        c.mu_dry_base = dict(cal_full.mu_dry_base)
        c.mu_ice_base = dict(cal_full.mu_ice_base)
        if a.surface is Surface.ICE:
            par = [((lambda x, k=a.category: x.mu_ice_base[k]),
                    (lambda x, v, k=a.category: x.mu_ice_base.__setitem__(k, v)),
                    0.05, 0.45)]
        elif a.water_mm > 0:
            par = [(lambda x: x.k_g, lambda x, v: setattr(x, "k_g", v), 0.30, 0.70)]
        else:
            par = [((lambda x, k=a.category: x.mu_dry_base[k]),
                    (lambda x, v, k=a.category: x.mu_dry_base.__setitem__(k, v)),
                    0.60, 1.45)]
        c, _ = optimise(c, par, rest, iters=5)
        m = BrakingModel(c)
        p = predict(m, a)
        rows.append((a, p, (p - a.measured_m) / a.measured_m))
    return rows


def solve_per_tyre(model: BrakingModel, anchors) -> dict:
    """Lahenda iga (rehv, pind) kohta mu, mis annab mõõdetud pidurdusmaa."""
    out = {}
    for a in anchors:
        key = (a.tyre_key, a.surface, a.water_mm > 0)
        lo, hi = 0.02, 1.8
        for _ in range(40):
            mid = (lo + hi) / 2
            ty = build_tyre(a)
            if a.surface is Surface.ICE:
                ty = replace(ty, mu_ice_override=mid)
            elif a.water_mm > 0:
                ty = replace(ty, wet_grip_index=mid / model.cal.k_g)
            else:
                ty = replace(ty, mu_dry_override=mid)
            d = predict(model, a, ty)
            if d > a.measured_m:
                lo = mid
            else:
                hi = mid
        out[key] = (lo + hi) / 2
    return out


def check_relations(model: BrakingModel):
    from .presets import ALL_VEHICLES as VEHICLES
    veh = VEHICLES["vw_golf_8"]
    base = Tyre("test", TyreCategory.SUMMER_TOURING, G_CLASS["A"],
                tread_depth_mm=8.0)
    worn = replace(base, tread_depth_mm=2.5)

    # märg, 100 km/h, 1 mm vett
    cw = Conditions(speed_kmh=100, water_mm=1.0, temp_c=20)
    r_new = model.stopping_distance(base, veh, cw).distance_m
    r_worn = model.stopping_distance(worn, veh, cw).distance_m
    _rel("Mustrisügavus märjal 8 -> 2,5 mm", r_worn / r_new, 1.17, 0.03,
         "DEKRA: +16…18 %")

    cd = Conditions(speed_kmh=100, water_mm=0.0, temp_c=20)
    d_new = model.stopping_distance(base, veh, cd).distance_m
    d_worn = model.stopping_distance(worn, veh, cd).distance_m
    _rel("Mustrisügavus kuival 8 -> 2,5 mm", d_worn / d_new, 1.055, 0.035,
         "DEKRA: +2,4…8,5 %")

    d50 = model.stopping_distance(base, veh, replace(cd, speed_kmh=50)).distance_m
    d100 = model.stopping_distance(base, veh, replace(cd, speed_kmh=100)).distance_m
    _rel("Kiiruse ruut 50 -> 100 km/h", d100 / d50, 4.0, 0.5,
         "puhas füüsika: 4x (pluss pidurite viide)")

    # R117 mfdd kontroll
    s = model.distance_between(base, veh, Conditions(speed_kmh=80, water_mm=1.0,
                                                     temp_c=20), 80, 20)
    mfdd = 231.48 / s
    mu_impl = mfdd / 9.80665
    print(f"  R117 mfdd kontroll: S(80->20) = {s:.1f} m -> "
          f"mfdd = {mfdd:.2f} m/s²  (μ_ekv = {mu_impl:.2f})")

    # rõhk
    for dp in (-0.6, -0.3, 0.0, 0.3, 0.6):
        t = replace(base, pressure_bar=veh.recommended_pressure_bar + dp)
        dw = model.stopping_distance(t, veh, cw).distance_m
        dd = model.stopping_distance(t, veh, cd).distance_m
        print(f"  rõhk {veh.recommended_pressure_bar+dp:.1f} bar "
              f"({dp:+.1f}): märg {dw:5.1f} m ({(dw/r_new-1)*100:+4.1f} %), "
              f"kuiv {dd:5.1f} m ({(dd/d_new-1)*100:+4.1f} %)")


def _rel(name, got, exp, tol, src):
    ok = "OK " if abs(got - exp) <= tol else "!! "
    print(f"  {ok}{name:<38} mudel {got:.3f}  oodatud {exp:.3f} ±{tol:.3f}   ({src})")


if __name__ == "__main__":
    main()
