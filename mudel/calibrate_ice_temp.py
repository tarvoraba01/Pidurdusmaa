"""Jää temperatuurikõvera valideerimine.

ice_temp_curve EI OLE ankrutest sobitatud -- ankrud on ainult -4 ja
-5 °C juures, mis on temperatuurikõvera jaoks sisuliselt üks punkt.
Kõver on ehitatud kirjandusest ja seda kontrollitakse siin nelja
avaldatud SÕIDUKI- ja VÄLITÖÖ-mõõtmise vastu (labori tribomeetrite
numbreid teadlikult EI kasutata, vt allpool).

Kaivita kaustast /home/claude:  python3 -m pidurdus.calibrate_ice_temp
"""

from __future__ import annotations

from .model import (BrakingModel, Calibration, Conditions, Surface, Tyre,
                    TyreCategory, _clamp, _interp)

# --- Kontrollid ------------------------------------------------------------
# (kirjeldus, temp_c, oodatav mu vahemik, allikas)
#
# NB: kõik allpool on GLARE ICE / paljas jää tüüpilise talverehviga.
# Mudelis vastab sellele WINTER_CENTRAL (Kesk-Euroopa talverehv) --
# Põhjamaade naelutu ja naastrehv on selgelt paremad ja neid siin ei
# kontrollita, sest tsiteeritud välitööd on tehtud tavarehvidega.
FIELD_MU = [
    ("Balmer (TRB SR115), glare ice, 0 °C",
     0.0, (0.05, 0.10),
     "At 32 deg on glare ice, you may get a skid resistance value "
     "between 0.05 and 0.1"),
    ("Balmer (TRB SR115), glare ice, -17,8 °C",
     -17.8, (0.20, 0.25),
     "As the temperature gets colder and drops to 0 F, the skid "
     "resistance value may increase to 0.2 or 0.25"),
    ("ICAO Cir 329, märg jää (mu_max)",
     0.0, (0.04, 0.10),
     "a very low friction (mu_max dropping to as low as 0.05)"),
]

# Suhtelised kontrollid: mitu korda muutub haare kahe temperatuuri vahel.
RATIOS = [
    ("Martin et al. (Bhoopalam et al. ülevaate kaudu): 0 -> -20 °C",
     0.0, -20.0, (1.8, 3.5),
     "a doubling of deceleration rate as ice temperature dropped "
     "from 0 to -20 C"),
    ("Kandeva & Dishovsky 2019: -4,5 -> +0,5 °C",
     -4.5, 0.5, (0.45, 0.70),
     "kineetilise mu keskmised: 0,20 (märg jää) -> 0,11 (sulav jää)"),
    ("Balmer: alla -18 °C kõver tasandub",
     -20.0, -30.0, (1.00, 1.15),
     "At temperatures below 0 F, it seems to level out"),
]


def mu_at(cal: Calibration, temp_c: float) -> float:
    """Kesk-Euroopa talverehvi mu paljal jääl antud temperatuuril,
    ilma rõhu-, muster- ja koormusparanditeta (kõik nominaalis)."""
    m = BrakingModel(cal)
    ty = Tyre(name="ref", category=TyreCategory.WINTER_CENTRAL,
              wet_grip_index=1.32, tread_depth_mm=8.0)
    from .presets import VEHICLES
    veh = VEHICLES["vw_golf_8"]
    cond = Conditions(speed_kmh=30.0, surface=Surface.ICE,
                      temp_c=temp_c, payload_kg=75.0)
    return m.mu_at_speed(ty, veh, cond, 30.0 / 3.6)


def main():
    cal = Calibration()
    print("=" * 78)
    print("JÄÄ — temperatuurikõvera valideerimine")
    print("=" * 78)
    print("\nKõver (kordaja, 1,00 = -5 °C):")
    for t in (2, 0, -2, -5, -10, -15, -20, -25, -30):
        k = _clamp(_interp(cal.ice_temp_curve, t),
                   cal.ice_temp_min, cal.ice_temp_max)
        print(f"  {t:>4.0f} °C   x{k:.2f}   mu = {mu_at(cal, t):.3f}")

    print("\nABSOLUUTKONTROLL (Kesk-Euroopa talverehv, paljas jää):")
    ok_n = 0
    for label, t, (lo, hi), quote in FIELD_MU:
        v = mu_at(cal, t)
        ok = lo <= v <= hi
        ok_n += ok
        print(f"  {'OK    ' if ok else 'VÄLJAS'} {label}")
        print(f"         mudel mu = {v:.3f}   oodatud {lo:.2f}-{hi:.2f}")
        print(f"         \"{quote}\"")

    print("\nSUHTEKONTROLL:")
    for label, t1, t2, (lo, hi), quote in RATIOS:
        r = mu_at(cal, t2) / mu_at(cal, t1)
        ok = lo <= r <= hi
        ok_n += ok
        print(f"  {'OK    ' if ok else 'VÄLJAS'} {label}")
        print(f"         mudel x{r:.2f}   oodatud x{lo:.2f}-{hi:.2f}")
        print(f"         \"{quote}\"")

    total = len(FIELD_MU) + len(RATIOS)
    print(f"\n>>> {ok_n}/{total} kontrolli läbitud")
    print("\nMIDA SIIN EI KONTROLLITA: laboritribomeetrite kalle (Lahayne,")
    print("Kandeva, Tada/Persson annavad 11-14 %/K) on TEADLIKULT kõrvale")
    print("jäetud kõvera KALDE allikana. Päris auto pidurduskontaktis tekib")
    print("hõõrdesoojus, mis ise reguleerib pinna temperatuuri, ja sõiduki")
    print("skaalal mõõdetud kalle on 3,5-6 %/K. Laborinumbreid kasutatakse")
    print("ainult kõvera KUJU kontrollimiseks (monotoonne, tiputa,")
    print("külmas tasanduv).")


if __name__ == "__main__":
    main()
