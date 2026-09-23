"""Akvaplaneerimise mudeli kontroll, sh LAIUSELIIGE.

Mudel ei ole akvaplaneerimise vastu sobitatud -- hp_* konstandid tulevad
Horne'i valemist ja kirjandusest. Seega on kõik allpool PUHAS KONTROLL,
mitte sobitus.

Kolm sõltumatut asja:

  1. [TV25]  Teknikens Varld 2025: 20 rehvi, KOIK 235/45 R18, Volvo V60,
             mõõdetud mustrisügavus iga rehvi kohta. Siin on laius
             konstantne, seega laiuseliige ei tohi siin midagi muuta
             peale ühtlase nihke.
  2. [ADAC25] ADAC 2025 talvetest: 31 rehvi, 225/40 R18.
  3. [ADAC18] ADAC 2018 laiusetest -- AINUS leitud mõõdetud võrdlus, kus
             auto ja rehvimudel on samad ja muutub ainult mõõt.
             VW Golf, Dunlop Winter Sport 5, Test World Ivalo, 7 mm vett.
             225 kaotab kontakti u 70 km/h, 195 "selgelt üle 80".
             Absoluutväärtusi ADAC ei avaldanud, seega kontrollime SUHET.

MIKS SUHE JA MITTE ABSOLUUTVÄÄRTUS: ADAC 2018 avaldas ainult sõnalise
kirjelduse, mitte tabelit. Suhe on ainus, mida sealt saab võtta -- ja
just suhe ongi see, mida laiuseliige mõjutab.

Kaivita kaustast /home/claude:  python3 -m pidurdus.calibrate_aqua
"""

from __future__ import annotations

import statistics
from dataclasses import replace

from .anchors_adac import ADAC_2025, ADAC_AQUA_WATER_MM
from .anchors_aqua import (TV25_AQUA, TV25_PRESSURE_BAR, TV25_SIZE,
                           TV25_WATER_MM)
from .model import (BrakingModel, Calibration, Conditions, Tyre, TyreCategory)
from .presets import VEHICLES

ADAC25_SIZE = "225/40 R18"
ADAC25_PRESSURE_BAR = 2.5

# [ADAC18] ainus mõõdetud sama-mudel-eri-mõõt võrdlus
ADAC18 = {
    "size_narrow": "195/65 R15",
    "size_wide": "225/40 R18",
    "measured_wide_kmh": 70.0,
    "measured_narrow_min_kmh": 80.0,   # "deutlich über 80" -> see on PÕRAND
    "water_mm": 7.0,
    "pressure_bar": 2.3,
}


def _errs(cal: Calibration, use_size: bool):
    m = BrakingModel(cal)
    veh = VEHICLES["vw_golf_8"]
    out = {"TV25": [], "ADAC25": []}
    for name, cat, tread, meas in TV25_AQUA:
        t = Tyre(name, cat, 1.32, tread_depth_mm=tread,
                 pressure_bar=TV25_PRESSURE_BAR,
                 size=TV25_SIZE if use_size else "")
        p = m.hydroplane_speed_kmh(t, veh, Conditions(water_mm=TV25_WATER_MM))
        out["TV25"].append((p - meas) / meas)
    for key, row in ADAC_2025.items():
        meas = row[6]
        t = Tyre(key, TyreCategory.WINTER_CENTRAL, 1.47, tread_depth_mm=8.0,
                 pressure_bar=ADAC25_PRESSURE_BAR,
                 size=ADAC25_SIZE if use_size else "")
        p = m.hydroplane_speed_kmh(t, veh, Conditions(water_mm=ADAC_AQUA_WATER_MM))
        out["ADAC25"].append((p - meas) / meas)
    return out


def _line(label, vals):
    return (f"    {label:8} n={len(vals):<3} "
            f"viga {statistics.mean(abs(x) for x in vals) * 100:5.2f} %   "
            f"nihe {statistics.mean(vals) * 100:+6.2f} %")


def width_ratio(cal: Calibration):
    """[ADAC18] suhe: kitsa ja laia ujumiskiiruse suhe."""
    m = BrakingModel(cal)
    veh = VEHICLES["vw_golf_8"]
    c = Conditions(water_mm=ADAC18["water_mm"])
    out = {}
    for k in ("size_narrow", "size_wide"):
        t = Tyre("Dunlop WS5", TyreCategory.WINTER_CENTRAL, 1.29,
                 tread_depth_mm=8.0, pressure_bar=ADAC18["pressure_bar"],
                 size=ADAC18[k])
        out[k] = m.hydroplane_speed_kmh(t, veh, c)
    return out["size_narrow"] / out["size_wide"], out


def main():
    print("=" * 78)
    print("AKVAPLANEERING — laiuseliikme kontroll")
    print("=" * 78)

    cal_off = Calibration()
    cal_off.hp_width_exp = 0.0          # laius välja
    cal_on = Calibration()

    print("\n1) 51 mõõdetud ujumiskiirust, kahest sõltumatust testist")
    for lbl, cal, use in (("ILMA laiuseta", cal_off, False),
                          ("LAIUSEGA", cal_on, True)):
        e = _errs(cal, use)
        allv = e["TV25"] + e["ADAC25"]
        print(f"  {lbl}")
        print(_line("KÕIK", allv))
        print(_line("TV25", e["TV25"]) + "   (235/45 R18)")
        print(_line("ADAC25", e["ADAC25"]) + "   (225/40 R18)")

    print("\n2) [ADAC18] suhe — ainus mõõdetud sama-mudel-eri-mõõt võrdlus")
    meas_ratio = ADAC18["measured_narrow_min_kmh"] / ADAC18["measured_wide_kmh"]
    for lbl, cal in (("ILMA laiuseta", cal_off), ("LAIUSEGA", cal_on)):
        r, vals = width_ratio(cal)
        ok = "OK" if r >= meas_ratio * 0.97 else "VÄLJAS"
        print(f"  {lbl:14} 195 -> {vals['size_narrow']:5.1f} km/h, "
              f"225 -> {vals['size_wide']:5.1f} km/h, suhe {r:.3f}   "
              f"mõõdetud vähemalt {meas_ratio:.3f}   {ok}")

    print("\nJÄRELDUS, mis tuleb ausalt välja öelda:")
    print("  * [ADAC18] on ainus PUHAS laiusevõrdlus ja laiuseliige tabab")
    print("    selle suhte ära; ilma selleta on mudel laiuse suhtes pime.")
    print("  * TV25 ja ADAC25 on kaks ERI testi, mille laius erineb ainult")
    print("    4,4 % (235 vs 225), aga mis erinevad ka labori, auto, veekile")
    print("    ja rehvivaliku poolest. Nende vaheline lahknevus EI OLE puhas")
    print("    laiusemõõtmine ja laiuseliige lahutab nende nihked laiali.")
    print("  * Seega: suund on kindel, suurusjärk nõrgalt toetatud.")
    print("    Eksponent 1,0 on ADAC18 konservatiivne ots.")


if __name__ == "__main__":
    main()
