# -*- coding: utf-8 -*-
"""ice_temp_exp sobitamine Vi Bilagare 2010 naastrehvitesti paaride vastu.

MIKS SEE SOBITUS ON TUGEVAM, KUI n=9 LASEB ARVATA
-------------------------------------------------
[VIB10D] mootis SAMA rehvi jaal KAHEL temperatuuril samal paeval. Rehvi
enda jaahaare (mu_ice_base, mustrisugavus, naelte arv, auto) TAANDUB
suhtest valja. Jarele jaab puhtalt see, mida me otsime: kui palju
haare temperatuuriga muutub. Seetottu ei sobitata siin MITTE
pidurdusmaid, vaid SUHTEID -- 9 paari, mitte 18 uksikmootmist.

MIS EI LIIGU
------------
Kover on normeeritud 1,0-le -5 °C juures. Koik Pohjamaa ja naastrehvi
jaaankrud (TM25) on TAPSELT -5 °C juures, seega aste ei liiguta neid
uldse. ADAC-i jaaankrud (WINTER_CENTRAL, ALL_SEASON) on -4 °C juures,
kus f = 0,907 -- seal liigutab aste paar protsenti ja mu_ice_base tuleb
jarele sobitada. Skript utleb selle valja.

Kaivita kaustast /home/claude:  python3 -m pidurdus.calibrate_ice_exp
"""
from __future__ import annotations

import math
from collections import defaultdict
from statistics import mean

from . import presets
from .anchors_vib10 import CONDS, SIZE, VEHICLE_KEY, VIB10D
from .model import (DEFAULT_CAL, BrakingModel, Conditions, Tyre,
                    TyreCategory, _clamp, _interp)

VEH = presets.VEHICLES[VEHICLE_KEY]

# Kaks ruhma, mitte kolm. Pohjus on MOODETUD, mitte valitud: Pohjamaa
# VikingContact 5 ja Kesk-Euroopa TS 830 andsid molemad suhte 1,69.
NAAST = TyreCategory.WINTER_STUDDED
KUMM = [TyreCategory.SUMMER_UHP, TyreCategory.SUMMER_TOURING,
        TyreCategory.ALL_SEASON, TyreCategory.WINTER_CENTRAL,
        TyreCategory.WINTER_NORDIC]


def m_suhted():
    """-> {'naast': [suhe...], 'kumm': [suhe...]} moodetud pidurdusmaadest."""
    out = defaultdict(list)
    for _k, r in VIB10D.items():
        kat, kulm, soe = r[1], r[3], r[4]
        out["naast" if kat is NAAST else "kumm"].append(soe / kulm)
    return out


def mudeli_suhe(kat, exp):
    """Mudeli ennustatud pidurdusmaa suhe soe/kulm antud astmega."""
    cal = DEFAULT_CAL.__class__(**{**DEFAULT_CAL.__dict__})
    cal.ice_temp_exp = dict(DEFAULT_CAL.ice_temp_exp)
    cal.ice_temp_exp[kat] = exp
    m = BrakingModel(cal)
    t = Tyre(name="x", category=kat, wet_grip_index=1.2,
             tread_depth_mm=9.0, tread_depth_new_mm=9.0, size=SIZE,
             g_source="test")
    d = {}
    for votme in ("jaa_k", "jaa_s"):
        surf, water, temp, v0, v1 = CONDS[votme]
        c = Conditions(speed_kmh=v0, surface=surf, water_mm=water,
                       temp_c=temp)
        d[votme] = m.distance_between(t, VEH, c, v0, v1)
    return d["jaa_s"] / d["jaa_k"]


def sobita(kat, siht, lo=0.20, hi=3.00):
    """Leia aste, mis annab sihtsuhte. Suhe KASVAB astmega."""
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if mudeli_suhe(kat, mid) < siht:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    s = m_suhted()
    print("MOODETUD SUHE  (pidurdusmaa +0,75 °C / -2,5 °C), [VIB10D]")
    for k, v in s.items():
        print(f"   {k:<6} n={len(v)}  keskmine {mean(v):.3f}  "
              f"({min(v):.2f}..{max(v):.2f})")

    print("\nMUDEL ENNE (aste = 1,0):")
    for nimi, kat in (("naast", NAAST), ("kumm", TyreCategory.WINTER_NORDIC)):
        print(f"   {nimi:<6} {mudeli_suhe(kat, 1.0):.3f}")

    e_naast = sobita(NAAST, mean(s["naast"]))
    e_kumm = sobita(TyreCategory.WINTER_NORDIC, mean(s["kumm"]))
    print("\nSOBITATUD ASTE:")
    print(f"   naastrehv          {e_naast:.3f}   "
          f"-> mudeli suhe {mudeli_suhe(NAAST, e_naast):.3f}")
    print(f"   koik ulejaanud     {e_kumm:.3f}   "
          f"-> mudeli suhe "
          f"{mudeli_suhe(TyreCategory.WINTER_NORDIC, e_kumm):.3f}")

    print("\nMIDA ASTE TEEB KOVERA TEISTE OTSTEGA "
          "(f = kovera vaartus, f**e = uus):")
    print(f"   {'T °C':>6} {'f':>7} {'naast':>9} {'kumm':>9}")
    for T in (2.0, 0.0, -2.0, -4.0, -5.0, -10.0, -20.0, -30.0):
        f = _clamp(_interp(DEFAULT_CAL.ice_temp_curve, T),
                   DEFAULT_CAL.ice_temp_min, DEFAULT_CAL.ice_temp_max)
        print(f"   {T:6.1f} {f:7.3f} {f**e_naast:9.3f} {f**e_kumm:9.3f}")

    print("\nANKRUTE NIHE (kui palju mu_ice_base tuleb jarele sobitada):")
    for T, sild in ((-5.0, "TM25 Pohjamaa/naast"), (-4.0, "ADAC kesk/lamell")):
        f = _interp(DEFAULT_CAL.ice_temp_curve, T)
        print(f"   {T:5.1f} °C  {sild:<22} naast {100*(f**e_naast/f - 1):+5.1f} %"
              f"   kumm {100*(f**e_kumm/f - 1):+5.1f} %")
    return e_naast, e_kumm


if __name__ == "__main__":
    main()
