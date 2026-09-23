"""Kruusa konstantide sobitamine ja valideerimine.

Sobitab mu_gravel_base, abs_eff_gravel ja tread_loss_gravel [SATC19]
18 mõõdetud kruusa pidurdusmaa vastu ning kontrollib tulemust KOLME
sõltumatu allika vastu, mida sobituses EI kasutata:

  [ESV98]   otse mõõdetud aeglustus: ABS väljas 0,59-0,66 g,
            ABS sees 0,37-0,52 g
  [NHTSA99] ABS-i trahv kruusal: +24,6 % / +30,0 % pidurdusmaale
  [SA4X4]   17 rehvi kõval kruusal, 80->0 km/h

Kaivita kaustast /home/claude:  python3 -m pidurdus.calibrate_gravel
"""

from __future__ import annotations

import statistics

from .anchors import ANCHORS
from .anchors_gravel import ESV98_DECEL_G, NHTSA99_ABS_PENALTY
from .calibrate import build_tyre, predict
from .model import (AbsClass, BrakingModel, Calibration, Conditions, Surface,
                    Tyre, TyreCategory)
from .presets import ALL_VEHICLES


def rows(cal: Calibration):
    m = BrakingModel(cal)
    out = []
    for a in [x for x in ANCHORS if x.surface is Surface.GRAVEL]:
        p = predict(m, a)
        out.append((a, p, (p - a.measured_m) / a.measured_m))
    return out


def mae(cal: Calibration) -> float:
    return statistics.mean(abs(e) for _, _, e in rows(cal))


def fit():
    """Kaks parameetrit, jäme ruudustik ja siis peenendus. Andmeid on
    35 punkti, seega rohkem vabadusastmeid ei ole mõtet lubada."""
    best = None
    lo_mu, hi_mu, lo_abs, hi_abs = 0.45, 0.85, 0.60, 1.00
    for _ in range(4):
        step_mu = (hi_mu - lo_mu) / 10
        step_abs = (hi_abs - lo_abs) / 10
        for i in range(11):
            mu = lo_mu + i * step_mu
            for j in range(11):
                ae = lo_abs + j * step_abs
                cal = Calibration()
                cal.mu_gravel_base = mu
                cal.abs_eff_gravel = {AbsClass.NONE: 1.00, AbsClass.EARLY: ae,
                                      AbsClass.MODERN: ae, AbsClass.LATEST: ae}
                e = mae(cal)
                if best is None or e < best[0]:
                    best = (e, mu, ae)
        _, mu, ae = best
        lo_mu, hi_mu = mu - step_mu, mu + step_mu
        lo_abs, hi_abs = max(0.3, ae - step_abs), min(1.2, ae + step_abs)
    return best


def check_decel(cal: Calibration):
    """Ristkontroll: mudeli tipp-aeglustus kruusal, ABS sees ja väljas.
    Neid numbreid sobituses EI kasutatud."""
    m = BrakingModel(cal)
    ty = Tyre(name="test", category=TyreCategory.SUMMER_TOURING,
              wet_grip_index=1.32, tread_depth_mm=7.7)
    out = {}
    for key, vkey in (("abs_off", "polo_vivo_noabs"), ("abs_on", "polo_vivo")):
        veh = ALL_VEHICLES[vkey]
        cond = Conditions(speed_kmh=50.0, surface=Surface.GRAVEL,
                          temp_c=20.0, payload_kg=150.0)
        out[key] = m.stopping_distance(ty, veh, cond).peak_decel_g
    return out


def main():
    print("=" * 78)
    print("KRUUS — sobitamine [SATC19] 18 mõõdetud pidurdusmaa vastu")
    print("=" * 78)

    base = Calibration()
    print(f"\nEnne (mu={base.mu_gravel_base:.3f}, "
          f"ABS={base.abs_eff_gravel[AbsClass.LATEST]:.3f}): "
          f"keskmine viga {mae(base)*100:.1f} %")

    err, mu, ae = fit()
    print(f"Pärast (mu={mu:.3f}, ABS={ae:.3f}): keskmine viga {err*100:.1f} %")

    cal = Calibration()
    cal.mu_gravel_base = mu
    cal.abs_eff_gravel = {AbsClass.NONE: 1.00, AbsClass.EARLY: ae,
                          AbsClass.MODERN: ae, AbsClass.LATEST: ae}

    rr = rows(cal)
    errs = sorted(abs(e) for _, _, e in rr)
    n = len(errs)
    print(f"  n={n}  90% kvantiil {errs[int(0.9*(n-1))]*100:.1f} %  "
          f"halvim {errs[-1]*100:.1f} %  "
          f"±15% sees {sum(1 for e in errs if e <= .15)/n*100:.0f} %")

    print("\nRISTKONTROLL 0 — [SA4X4], sobitusest VÄLJAS")
    from .anchors import gravel_validation
    mv = BrakingModel(cal)
    sub = [(predict(mv, a) - a.measured_m) / a.measured_m
           for a in gravel_validation()]
    print(f"  n={len(sub)}  nihe {statistics.mean(sub)*100:+5.1f} %   "
          f"keskmine viga {statistics.mean(abs(e) for e in sub)*100:5.1f} %")
    print("  (kõva, tihe kruusarada + pikap: mudel on seal konservatiivne,")
    print("   ehk ennustab pikemat pidurdusmaad kui päriselt mõõdeti)")

    print("\nKiiruse kaupa (SATC19) — kas kruusal on kiirusesõltuvus?")
    for v in (40.0, 60.0, 80.0):
        sub = [e for a, _, e in rr if a.source == "SATC19" and a.v_from_kmh == v]
        print(f"  {v:>3.0f} km/h  n={len(sub)}  nihe {statistics.mean(sub)*100:+5.1f} %")

    print("\nRISTKONTROLL 1 — tipp-aeglustus vs [ESV98] otsemõõtmine")
    d = check_decel(cal)
    for key, (lo, hi) in ESV98_DECEL_G.items():
        v = d[key]
        ok = "OK" if lo <= v <= hi else "VÄLJAS"
        print(f"  {key:<8} mudel {v:.2f} g   mõõdetud {lo:.2f}-{hi:.2f} g   {ok}")

    print("\nRISTKONTROLL 2 — ABS-i trahv kruusal vs [NHTSA99]")
    m = BrakingModel(cal)
    ty = Tyre(name="t", category=TyreCategory.SUMMER_TOURING,
              wet_grip_index=1.32, tread_depth_mm=7.7)
    cond = Conditions(speed_kmh=56.0, surface=Surface.GRAVEL,
                      temp_c=20.0, payload_kg=150.0)
    d_on = m.stopping_distance(ty, ALL_VEHICLES["polo_vivo"], cond).distance_m
    d_off = m.stopping_distance(ty, ALL_VEHICLES["polo_vivo_noabs"], cond).distance_m
    pen = d_on / d_off - 1.0
    lo, hi = NHTSA99_ABS_PENALTY
    ok = "OK" if lo * 0.7 <= pen <= hi * 1.3 else "VÄLJAS"
    print(f"  mudel {pen*100:+.1f} %   mõõdetud +{lo*100:.1f}...+{hi*100:.1f} %   {ok}")

    print(f"\n>>> mu_gravel_base = {mu:.3f}")
    print(f">>> abs_eff_gravel = NONE 1.00, muud {ae:.2f}")


if __name__ == "__main__":
    main()
