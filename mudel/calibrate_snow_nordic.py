"""Põhjamaade naelutu ja naastrehvi lumebaasi kontroll.

See ei ole optimeerija. Siin on kaks ülesannet:

  1. Näidata, MIDA kaks uut mõõtmist ütlevad ja kui hästi mudel neid
     pärast parandust taastoodab.
  2. Näidata, MIS OLEKS OLNUD, kui oleks jäänud vana oletuse juurde --
     sest muidu jääb mulje, et parandus oli kosmeetiline.

Kaivita kaustast /home/claude:  python3 -m pidurdus.calibrate_snow_nordic
"""

from __future__ import annotations

import statistics

from .anchors_snow_nordic import (NOT_FOUND, UTAC25N, UTAC25N_ROWS, ZR24,
                                  ZR24_ROWS)
from .model import (BrakingModel, Calibration, Conditions, Surface, Tyre,
                    TyreCategory)
from .presets import VEHICLES

VANA = {TyreCategory.WINTER_NORDIC: 0.34, TyreCategory.WINTER_STUDDED: 0.33}


def _pred(cal, cat, meta, size=None):
    """Kategooria tüüpiline pidurdusmaa selle testi tingimustes."""
    m = BrakingModel(cal)
    t = Tyre("kategooria tüüpiline", cat, 1.25, tread_depth_mm=8.0,
             size=size if size is not None else meta["size"])
    c = Conditions(surface=Surface.SNOW_PACKED,
                   speed_kmh=meta["v_from_kmh"], temp_c=meta["temp_c"])
    return m.distance_between(t, VEHICLES[meta["vehicle_key"]], c,
                              meta["v_from_kmh"], meta["v_to_kmh"])


def _block(nimi, cat, meta, meas, note):
    cal_uus = Calibration()
    cal_vana = Calibration()
    cal_vana.mu_snow_base[cat] = VANA[cat]

    mean = statistics.mean(meas)
    d_uus = _pred(cal_uus, cat, meta)
    d_vana = _pred(cal_vana, cat, meta)

    print(f"\n{'=' * 74}\n{nimi}\n{'=' * 74}")
    print(f"  sõiduk {VEHICLES[meta['vehicle_key']].name}, mõõt {meta['size']}")
    print(f"  {meta['v_from_kmh']:.0f} -> {meta['v_to_kmh']:.0f} km/h, "
          f"{meta['temp_c']:+.0f} °C, {meta['venue']}")
    print(f"  {meta['url']}")
    print(f"\n  mõõdetud n={len(meas)}  "
          f"vahemik {min(meas):.2f}-{max(meas):.2f} m  keskmine {mean:.2f} m")
    print(f"\n  VANA (oletus mu={VANA[cat]:.3f})   {d_vana:6.2f} m   "
          f"viga {(d_vana - mean) / mean * 100:+6.1f} %")
    print(f"  UUS  (mõõdetud mu={Calibration().mu_snow_base[cat]:.3f})  "
          f"{d_uus:6.2f} m   viga {(d_uus - mean) / mean * 100:+6.1f} %")
    print(f"\n  {note}")


def main():
    print("=" * 74)
    print("LUMI: PÕHJAMAADE NAELUTU JA NAAST — kaks esimest mõõtmist")
    print("=" * 74)
    print("""
Enne seda tööd oli mudelis 47 lumemõõtmist ja KÕIK olid Kesk-Euroopa
talverehvid või lamellrehvid. Kaks kategooriat, mida Eestis kõige
rohkem kasutatakse, olid lumel nulli mõõtmisega ja nende väärtused
olid minu enda oletused -- ainsad kaks arvu mu_snow_base-s ilma
allikaviiteta.""")

    _block("[UTAC25N] Põhjamaade naelutu, 5 rehvi",
           TyreCategory.WINTER_NORDIC, UTAC25N,
           [r[2] for r in UTAC25N_ROWS],
           "Esmaallikas, kontrollitud kaks korda sõltumatult.")

    _block("[ZR24] Naastrehv, 4 rehvi 12-st",
           TyreCategory.WINTER_STUDDED, ZR24,
           [r[2] for r in ZR24_ROWS],
           "Nõrgem ankur: 4 punkti 12-st ja ükski rehv ei ole andmebaasis.\n"
           "  Testisisene hajuvus (±6 %) on suurem kui parandus ise (+4,5 %).")

    print(f"\n{'=' * 74}\nKAS PARANDUS ON AINULT NENDE KAHE TESTI PEALE ISTUMINE?"
          f"\n{'=' * 74}")
    print("""
Ei -- ja seda saab näidata. Uus väärtus paneb kategooriad järjekorda,
mis vastab sellele, milleks rehvid on ehitatud:""")
    cal = Calibration()
    for c in (TyreCategory.ALL_SEASON, TyreCategory.WINTER_NORDIC,
              TyreCategory.WINTER_CENTRAL, TyreCategory.WINTER_STUDDED):
        old = VANA.get(c)
        mark = f"  (varem {old:.3f})" if old else ""
        print(f"    {c.name:16} {cal.mu_snow_base[c]:.4f}{mark}")
    print("""
Vana seis ütles, et Põhjamaade rehv on lumel HALVEM kui Kesk-Euroopa
oma (0,34 vs 0,375). Uus ütleb, et ta on pisut parem (0,377 vs 0,375).
Teine on usutav, esimene ei olnud.""")

    print(f"\n{'=' * 74}\nKAS MASS LOEB? (Q5 quattro on katses raskem kui meie kirje)"
          f"\n{'=' * 74}")
    import dataclasses
    veh = VEHICLES[UTAC25N["vehicle_key"]]
    for dm in (0, 80, 160):
        v2 = dataclasses.replace(veh, kerb_mass_kg=veh.kerb_mass_kg + dm)
        m = BrakingModel(Calibration())
        t = Tyre("x", TyreCategory.WINTER_NORDIC, 1.25, tread_depth_mm=8.0,
                 size=UTAC25N["size"])
        d = m.distance_between(t, v2, Conditions(
            surface=Surface.SNOW_PACKED, speed_kmh=35.0, temp_c=-8.0), 35.0, 10.0)
        print(f"  tühimass {veh.kerb_mass_kg + dm:.0f} kg  ->  {d:.3f} m")
    print("  Ehk 160 kg muudab tulemust alla promilli. Quattro lisamass ei ole\n"
          "  põhjus seda ankrut mitte kasutada.")

    print(f"\n{'=' * 74}\nVEAPIIR\n{'=' * 74}")
    m = BrakingModel(Calibration())
    for cat in (TyreCategory.WINTER_CENTRAL, TyreCategory.WINTER_NORDIC,
                TyreCategory.WINTER_STUDDED):
        t = Tyre("x", cat, 1.25, tread_depth_mm=8.0, size="205/55 R16")
        r = m.stopping_distance(t, VEHICLES["vw_golf_8"], Conditions(
            surface=Surface.SNOW_PACKED, speed_kmh=50.0, temp_c=-5.0))
        print(f"  {cat.name:16} {r.distance_m:5.1f} m  ±{r.sigma_rel * 100:4.1f} %"
              f"   usaldus {r.confidence}")
    print("  Naelutu ja naast saavad laiema piiri, sest nende taga on ÜKS\n"
          "  test kummalgi, Kesk-Euroopa oma taga 47 mõõtmist. Sama pinnanimi,\n"
          "  kümme korda erinev tõenduse kaal -- ja nüüd on see ka näha.")

    print(f"\n{'=' * 74}\nMIDA OTSITI JA EI LEITUD\n{'=' * 74}")
    print(NOT_FOUND)


if __name__ == "__main__":
    main()
