"""
Teine kalibreerimisetapp: ADAC 2025 andmed + rehvirõhu kõver.

Miks eraldi failis: see etapp toob mudelisse asju, mida esimeses etapis
üldse ei olnud (lumi, märg betoon, rõhukõver), ja kasutab teistsugust
loogikat — rehvi G tuletatakse ÜHEST katsest ja seda kasutatakse siis
NELJA ülejäänu ennustamiseks. See on tugev valideerimine, sest ühest
vabast parameetrist tuleb neli sõltumatut ennustust.

Käivita:  python3 -m pidurdus.calibrate_adac
"""

from __future__ import annotations

import math
import statistics
from dataclasses import replace

from .anchors import (ANCHORS, MDPI_NOABS, SNOW_SUMMER_WINTER_RATIO,
                      pressure_relations)
from .anchors_adac import ADAC_2025, ADAC_AQUA_WATER_MM
from .calibrate import build_tyre, errors, optimise, predict, print_summary, summarise
from .model import (AbsClass, BrakingModel, Calibration, Conditions, Surface,
                    Tyre, TyreCategory)
from .presets import ALL_VEHICLES as VEHICLES

ADAC = [a for a in ANCHORS if a.source == "ADAC25"]


def by_tag(tag):
    return [a for a in ADAC if a.note == tag]


# ---------------------------------------------------------------------------
# 1. Tuleta iga ADAC-i rehvi G MÄRJA ASFALDI katsest
# ---------------------------------------------------------------------------

def solve_grip(model: BrakingModel) -> dict:
    """Iga rehvi kohta: milline G annab täpselt mõõdetud märja pidurdusmaa?"""
    out = {}
    for a in by_tag("wet"):
        lo, hi = 0.40, 2.60
        for _ in range(44):
            mid = (lo + hi) / 2
            d = predict(model, a, replace(build_tyre(a), wet_grip_index=mid))
            if d > a.measured_m:
                lo = mid
            else:
                hi = mid
        out[a.tyre_key] = (lo + hi) / 2
    return out


def with_grip(grip):
    """tyre_fn, mis annab igale ankrule tema märjast katsest tuletatud G."""
    def fn(a):
        ty = build_tyre(a)
        g = grip.get(a.tyre_key)
        return replace(ty, wet_grip_index=g) if g else ty
    return fn


# ---------------------------------------------------------------------------
# 2. Rehvirõhu kõver PASSAT-i suhtarvude vastu
# ---------------------------------------------------------------------------

_SURF = {"dry": (Surface.ASPHALT, 0.0, 15.0),
         "wet": (Surface.ASPHALT, 1.0, 12.0),
         "snow": (Surface.SNOW_PACKED, 0.0, -3.0)}
_CAT = {"summer": TyreCategory.SUMMER_TOURING, "winter": TyreCategory.WINTER_CENTRAL}


def pressure_cost(cal: Calibration) -> float:
    """Keskmine absoluutviga PASSAT-i 30 suhtarvu peal."""
    m = BrakingModel(cal)
    veh = VEHICLES["passat_b5"]
    errs = []
    for tyre_type, surf_key, p, ratio in pressure_relations():
        surf, water, temp = _SURF[surf_key]
        ty = Tyre("x", _CAT[tyre_type], 1.47, pressure_bar=p)
        base = Tyre("x", _CAT[tyre_type], 1.47, pressure_bar=2.0)
        c = Conditions(speed_kmh=50, surface=surf, water_mm=water, temp_c=temp,
                       payload_kg=150)
        d = m.stopping_distance(ty, veh, c).distance_m
        d0 = m.stopping_distance(base, veh, c).distance_m
        errs.append(abs(d / d0 - ratio))
    return statistics.mean(errs)


def fit_pressure(cal: Calibration) -> Calibration:
    params = [
        ("press_k_dry", 0.005, 0.30),
        ("press_k_wet_under", 0.005, 0.40),
        ("press_k_wet_over", 0.005, 0.40),
        ("press_opt_offset_dry", -0.30, 0.40),
    ]
    best = pressure_cost(cal)
    for it in range(9):
        for name, lo, hi in params:
            cur = getattr(cal, name)
            span = (hi - lo) / (2 ** (it + 1))
            for cand in (cur - span, cur + span):
                cand = max(lo, min(hi, cand))
                setattr(cal, name, cand)
                c = pressure_cost(cal)
                if c < best - 1e-12:
                    best, cur = c, cand
                else:
                    setattr(cal, name, cur)
    return cal


def fit_abs_scale(cal: Calibration) -> Calibration:
    """ABS-ita rõhutundlikkus [MDPI25] vastu: 2.413 -> 1.689 bar = +15,0 %."""
    m_lo, m_hi = MDPI_NOABS["p_lo"], MDPI_NOABS["p_hi"]
    veh = replace(VEHICLES["passat_b5"], abs_class=AbsClass.NONE,
                  recommended_pressure_bar=m_hi)
    c = Conditions(speed_kmh=MDPI_NOABS["speed_kmh"], temp_c=21, payload_kg=150)

    def ratio(scale):
        cal.press_abs_scale[AbsClass.NONE] = scale
        m = BrakingModel(cal)
        d1 = m.stopping_distance(Tyre("x", TyreCategory.SUMMER_TOURING, 1.47,
                                      pressure_bar=m_lo), veh, c).distance_m
        d0 = m.stopping_distance(Tyre("x", TyreCategory.SUMMER_TOURING, 1.47,
                                      pressure_bar=m_hi), veh, c).distance_m
        return d1 / d0

    lo, hi = 0.5, 30.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if ratio(mid) < MDPI_NOABS["ratio_new"]:
            lo = mid
        else:
            hi = mid
    cal.press_abs_scale[AbsClass.NONE] = (lo + hi) / 2
    return cal


# ---------------------------------------------------------------------------
# 3. Akvaplaneering ADAC-i ujumiskiiruste vastu
# ---------------------------------------------------------------------------

def check_aqua(model: BrakingModel, grip):
    veh = VEHICLES["vw_golf_8"]
    rows = []
    for key, row in ADAC_2025.items():
        measured = row[6]
        ty = Tyre(key, TyreCategory.WINTER_CENTRAL, grip.get(key, 1.47),
                  tread_depth_mm=8.0)
        c = Conditions(water_mm=ADAC_AQUA_WATER_MM)
        pred = model.hydroplane_speed_kmh(ty, veh, c)
        rows.append((key, measured, pred, (pred - measured) / measured))
    return rows


# ---------------------------------------------------------------------------

def main():
    print("=" * 100)
    print("ETAPP 2 — ADAC 2025 (31 rehvi x 5 pinda) + rehvirõhu kõver")
    print("=" * 100)

    cal = Calibration()
    model = BrakingModel(cal)

    print("\n1) Tuletan iga rehvi G märja asfaldi katsest (31 rehvi)")
    grip = solve_grip(model)
    gs = sorted(grip.values())
    print(f"   G vahemik {gs[0]:.2f} … {gs[-1]:.2f}, mediaan {gs[len(gs)//2]:.2f}")
    print("   -> need G-d on nüüd AINUS rehvipõhine sisend. Kõik ülejäänud")
    print("      neli pinda ennustatakse nendest + globaalsetest konstantidest.")

    fn = with_grip(grip)

    print("\n2) Sobitan globaalsed konstandid (üks parameeter pinna kohta)")
    for tag, label, params in [
        ("dry", "kuiv asfalt", [((lambda c: c.mu_dry_base[TyreCategory.WINTER_CENTRAL]),
                                 (lambda c, v: c.mu_dry_base.__setitem__(
                                     TyreCategory.WINTER_CENTRAL, v)), 0.60, 1.30)]),
        # NB: concrete_factor on kategooriapõhine dict, mitte float. See
        # skript kirjutas talle varem float'i peale ja jooksis kokku --
        # getter võtab ühe esindaja, setter kirjutab kõigile sama väärtuse,
        # sest ankrud ei erista kategooriaid betooni peal niikuinii.
        ("concrete", "märg betoon", [((lambda c: next(iter(c.concrete_factor.values()))),
                                      (lambda c, v: c.concrete_factor.update(
                                          dict.fromkeys(c.concrete_factor, v))),
                                      0.60, 1.10)]),
        ("snow", "lumi", [((lambda c: c.mu_snow_base[TyreCategory.WINTER_CENTRAL]),
                           (lambda c, v: c.mu_snow_base.__setitem__(
                               TyreCategory.WINTER_CENTRAL, v)), 0.10, 0.70)]),
        ("ice", "jää", [((lambda c: c.mu_ice_base[TyreCategory.WINTER_CENTRAL]),
                         (lambda c, v: c.mu_ice_base.__setitem__(
                             TyreCategory.WINTER_CENTRAL, v)), 0.03, 0.40)]),
    ]:
        subset = by_tag(tag)
        cal, _ = optimise_fn(cal, params, subset, fn, grid=True)
        m = BrakingModel(cal)
        s = summarise(errors(m, subset, fn), label)
        val = (next(iter(cal.concrete_factor.values())) if tag == "concrete" else
               cal.mu_dry_base[TyreCategory.WINTER_CENTRAL] if tag == "dry" else
               cal.mu_snow_base[TyreCategory.WINTER_CENTRAL] if tag == "snow" else
               cal.mu_ice_base[TyreCategory.WINTER_CENTRAL])
        print(f"   {label:<14} = {val:.3f}   ", end="")
        print(f"n={s['n']}, keskmine viga {s['mae']*100:.1f} %, "
              f"halvim {s['worst']*100:.1f} %")

    model = BrakingModel(cal)

    print("\n" + "-" * 100)
    print("VALIDEERIMINE — üks vaba parameeter rehvi kohta (G märjast katsest),")
    print("neli sõltumatut ennustust. Betoon, lumi ja jää EI OLE G sobitamises.")
    print("-" * 100)
    for tag, label in [("wet", "märg asfalt (G siit tuletatud)"),
                       ("dry", "kuiv asfalt  (ENNUSTUS)"),
                       ("concrete", "märg betoon  (ENNUSTUS)"),
                       ("snow", "lumi         (ENNUSTUS)"),
                       ("ice", "jää          (ENNUSTUS)")]:
        print_summary(summarise(errors(model, by_tag(tag), fn), label))
    print_summary(summarise(errors(model, ADAC, fn), "KÕIK ADAC25"))

    print("\n" + "-" * 100)
    print("AKVAPLANEERING — mudel vs ADAC-i mõõdetud ujumiskiirus (31 rehvi)")
    print("  Mudel ei ole selle vastu kalibreeritud: hp_* konstandid on")
    print("  Horne'i valemist ja kirjanduse lävedest. See on puhas kontroll.")
    print("-" * 100)
    rows = check_aqua(model, grip)
    errsA = [abs(r[3]) for r in rows]
    meas = [r[1] for r in rows]
    print(f"  mõõdetud vahemik {min(meas):.1f} – {max(meas):.1f} km/h, "
          f"mudel {rows[0][2]:.1f} km/h (sama kõigile, sest muster on sama)")
    print(f"  keskmine viga {statistics.mean(errsA)*100:.1f} %, "
          f"halvim {max(errsA)*100:.1f} %")
    print("  NB: mudel ei erista mustri KUJU, ainult sügavust — seepärast on")
    print("  ennustus kõigile sama. Rehvide vahelist järjestust see ei anna.")

    print("\n" + "-" * 100)
    print("REHVIRÕHK — sobitan PASSAT-i 30 mõõdetud suhtarvu vastu")
    print("  (2 rehvitüüpi x 3 pinda x 5 rõhku, 6 kordust punkti kohta)")
    print("-" * 100)
    before = pressure_cost(cal)
    cal = fit_pressure(cal)
    after = pressure_cost(cal)
    print(f"  enne:  keskmine viga {before*100:.2f} %")
    print(f"  pärast: keskmine viga {after*100:.2f} %")
    print(f"  press_k_dry        = {cal.press_k_dry:.4f}")
    print(f"  press_k_wet_under  = {cal.press_k_wet_under:.4f}")
    print(f"  press_k_wet_over   = {cal.press_k_wet_over:.4f}")
    print(f"  press_opt_offset   = {cal.press_opt_offset_dry:+.3f} bar")
    cal = fit_abs_scale(cal)
    print(f"  press_abs_scale[ABS puudub] = "
          f"{cal.press_abs_scale[AbsClass.NONE]:.2f}  [MDPI25, ABS väljas]")

    m = BrakingModel(cal)
    veh = VEHICLES["passat_b5"]
    print(f"\n  {'rõhk':>6}" + "".join(f"{s:>22}" for s in
                                       ("kuiv", "märg", "lumi")))
    print(f"  {'':>6}" + "".join(f"{'mudel / mõõdetud':>22}" for _ in range(3)))
    meas_map = {(t, s, p): r for t, s, p, r in pressure_relations()}
    for p in (1.0, 1.5, 2.0, 2.5, 3.0):
        cells = []
        for surf_key in ("dry", "wet", "snow"):
            surf, water, temp = _SURF[surf_key]
            c = Conditions(speed_kmh=50, surface=surf, water_mm=water,
                           temp_c=temp, payload_kg=150)
            d = m.stopping_distance(Tyre("x", TyreCategory.WINTER_CENTRAL, 1.47,
                                         pressure_bar=p), veh, c).distance_m
            d0 = m.stopping_distance(Tyre("x", TyreCategory.WINTER_CENTRAL, 1.47,
                                          pressure_bar=2.0), veh, c).distance_m
            cells.append(f"{(d/d0-1)*100:+6.1f} % / "
                         f"{(meas_map[('winter',surf_key,p)]-1)*100:+6.1f} %")
        print(f"  {p:>4.1f} b" + "".join(f"{x:>22}" for x in cells))

    print("\n" + "-" * 100)
    print("LUME RISTKONTROLL — suverehv vs talverehv lumel")
    print("-" * 100)
    c = Conditions(speed_kmh=50, surface=Surface.SNOW_PACKED, temp_c=-3, payload_kg=150)
    ds = m.stopping_distance(Tyre("s", TyreCategory.SUMMER_TOURING, 1.60), veh, c).distance_m
    dw = m.stopping_distance(Tyre("w", TyreCategory.WINTER_CENTRAL, 1.47), veh, c).distance_m
    print(f"  mudel: suverehv / talverehv = {ds/dw:.3f}")
    print(f"  PASSAT mõõtis:                {SNOW_SUMMER_WINTER_RATIO:.3f}")
    print(f"  viga {abs(ds/dw - SNOW_SUMMER_WINTER_RATIO)/SNOW_SUMMER_WINTER_RATIO*100:.1f} %")

    print("\n" + "=" * 100)
    print("UUED KONSTANDID (kopeeri model.py Calibration-isse):")
    print(f"  concrete_factor      = {next(iter(cal.concrete_factor.values())):.4f}")
    print(f"  mu_dry_base[WINTER_CENTRAL]  = {cal.mu_dry_base[TyreCategory.WINTER_CENTRAL]:.4f}")
    print(f"  mu_snow_base[WINTER_CENTRAL] = {cal.mu_snow_base[TyreCategory.WINTER_CENTRAL]:.4f}")
    print(f"  mu_ice_base[WINTER_CENTRAL]  = {cal.mu_ice_base[TyreCategory.WINTER_CENTRAL]:.4f}")
    print(f"  press_k_dry          = {cal.press_k_dry:.4f}")
    print(f"  press_k_wet_under    = {cal.press_k_wet_under:.4f}")
    print(f"  press_k_wet_over     = {cal.press_k_wet_over:.4f}")
    print(f"  press_opt_offset_dry = {cal.press_opt_offset_dry:.4f}")
    print(f"  press_abs_scale[NONE]= {cal.press_abs_scale[AbsClass.NONE]:.4f}")
    print("=" * 100)
    return cal, grip


def optimise_fn(cal, params, anchors, tyre_fn, iters=7, grid=False):
    """optimise(), aga tyre_fn-iga (rehvipõhine G)."""
    def cost(c):
        m = BrakingModel(c)
        return statistics.mean(abs(e) for _, _, e in errors(m, anchors, tyre_fn))
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
                    best, cur = c, cand
                else:
                    setr(cal, cur)
    return cal, best


if __name__ == "__main__":
    main()
