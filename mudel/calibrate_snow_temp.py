"""Lume temperatuurikõvera kontroll.

See kõver EI OLE ankrute vastu sobitatud ja seda ei saagi olla: kõik 47
lumeankrut on -5 °C juurest. Põhjus ei ole laiskus, vaid standard --
ASTM F1805 NÕUAB katselume temperatuuriks -4...-15 °C, nii et iga
sertifitseeritud lumehaarde number maailmas on külma lume number.

Seepärast on see fail teistsugune kui teised calibrate_*.py: siin ei
sobitata midagi, vaid pannakse kirja, MIS ALLIKAD ÜTLEVAD ja kus nad
omavahel VASTUOLUS on. Vastuolu on siin sisuline, mitte kosmeetiline.

Kaivita kaustast /home/claude:  python3 -m pidurdus.calibrate_snow_temp
"""

from __future__ import annotations

from .model import BrakingModel, Calibration, Conditions, Surface, _clamp, _interp
from .presets import TYRES, VEHICLES

# (kirjeldus, temp1, temp2, oodatav mu(t2)/mu(t1), tõendiklass, allikas)
CLAIMS = [
    ("FAA AC 25-31 tab 2: tallatud lumi <=-15 vs soojem",
     -20.0, -10.0, 1 / 1.249,
     "REGULAATORI KONSENSUS, mitte mõõtmine",
     "TALPA töörühm, 'based on their experience'; 0,201 vs 0,161"),

    ("Lu / WSDOT 551.1: talverehv tallatud lumel -29 vs 0 C",
     -29.0, 0.0, 1.00,
     "PÄRIS SÕIDUKI PIDURDUS (teisene tsitaat)",
     "Blizzak 22,1 m mõlemal; 'stopping distances were shorter near freezing'"),

    ("Lu / WSDOT 551.1: lamellrehv tallatud lumel -29 vs 0 C",
     -29.0, 0.0, 1.144,
     "PÄRIS SÕIDUKI PIDURDUS (teisene tsitaat)",
     "27,1 m külmas vs 23,7 m nulli juures ehk külmas 12 % PIKEM"),

    ("Transport Canada AC 300-019: -3 C ja soojem on libedam",
     -10.0, -1.0, 0.90,
     "REGULAATORI HOIATUS, suund ilma numbrita",
     "'may be more slippery than indicated' -- suund, mitte suurus"),
]

# Virginia Tech, ASTM F1805 regressioon: mis lumehaaret TEGELIKULT seletab
VT_VARIANCE = {
    "lume temperatuur": (0.007, 0.022),
    "lume kõvadus (CTI penetromeeter)": (0.846, 0.948),
}


def mult(cal: Calibration, t: float) -> float:
    return _clamp(_interp(cal.snow_temp_curve, t),
                  cal.snow_temp_min, cal.snow_temp_max)


def main():
    cal = Calibration()
    print("=" * 78)
    print("LUMI JA TEMPERATUUR — vastuoluline tõendus, kirja pandud")
    print("=" * 78)

    print("\nKÕVER (kordaja, 1,00 = -5 °C, kus kõik ankrud on):")
    for t in (-30, -20, -15, -10, -5, -3, -2, -1, 0, 2):
        print(f"  {t:>4} °C   x{mult(cal, t):.2f}")

    print("\nKAS MUDELI VAHEMIK KATAB IGA ALLIKA VÄITE?")
    print("  Allikad on omavahel VASTUOLUS, seega küsimus ei ole, kumba")
    print("  järgida. Küsimus on, kas mudeli veapiir tunnistab mõlemat.")
    m = BrakingModel(cal)
    t = TYRES["conti_ts870p"]
    v = VEHICLES["vw_golf_8"]

    def band(temp):
        r = m.stopping_distance(t, v, Conditions(
            surface=Surface.SNOW_PACKED, speed_kmh=50.0, temp_c=temp))
        return r.distance_m, r.sigma_rel

    n_ok = 0
    for desc, t1, t2, want, cls, note in CLAIMS:
        d1, _ = band(t1)
        d2, sg = band(t2)
        # allikas väidab mu-suhet; pidurdusmaa suhe on selle pöördväärtus
        want_dist_ratio = 1.0 / want
        got_ratio = d2 / d1
        lo, hi = got_ratio * (1 - sg), got_ratio * (1 + sg)
        ok = lo <= want_dist_ratio <= hi
        n_ok += ok
        print(f"\n  {desc}")
        print(f"    tõendiklass: {cls}")
        print(f"    allikas: {note}")
        print(f"    allikas ütleb pidurdusmaa suhteks x{want_dist_ratio:.3f}")
        print(f"    mudel x{got_ratio:.3f}, vahemik x{lo:.3f}-{hi:.3f}   "
              f"-> {'KATAB' if ok else 'EI KATA'}")
    print(f"\n  >>> {n_ok}/{len(CLAIMS)} allika väidet on mudeli vahemiku sees")
    print("  Kaks katmata väidet osutavad VASTASSUUNDA: FAA tahab, et külm\n"
          "  lumi oleks palju parem, Lu lamellrehv tahab, et külm oleks\n"
          "  halvem. Kõver istub nende vahel. Seda ei saa 'parandada' --\n"
          "  allikad ise ei klapi ja mudel ei tohi teeselda, et klapivad.")

    print("\nMIKS KÕVER ON KÜLMA POOL TASANE:")
    print("  FAA ütleb, et külm lumi on 25 % haardevam. Päris sõidukikatse")
    print("  ütleb, et vahet ei ole või on külm isegi halvem. FAA number on")
    print("  komitee hinnang, Lu oma on mõõtmine. Kui kaks allikat on")
    print("  vastuolus ja üks neist on mõõtmine, võidab mõõtmine -- aga")
    print("  kumbagi ei võeta täielikult, seega kõver on tasane (x1,00).")

    print("\nMIKS TEMPERATUUR ON SIIN NIIKUINII VALE MUUTUJA:")
    print("  Virginia Tech, ASTM F1805 regressioon, mis seletab lumehaarde")
    print("  varieeruvust:")
    for k, (lo, hi) in VT_VARIANCE.items():
        print(f"    {k:36} {lo*100:4.1f} - {hi*100:4.1f} %")
    print("  Ehk lume KÕVADUS seletab ~40x rohkem kui temperatuur. Meie")
    print("  kõver on tegelikult asendusnäitaja vaba vee jaoks pinnakihis,")
    print("  mitte temperatuurimudel. Seda ütleb ka kasutajale näidatav")
    print("  hoiatus, mis ilmub üle -3 °C.")

    print("\nVEAPIIR:")
    m = BrakingModel(cal)
    t = TYRES["conti_ts870p"]
    v = VEHICLES["vw_golf_8"]
    for temp in (-10.0, -3.0, -1.0, 0.0):
        r = m.stopping_distance(t, v, Conditions(
            surface=Surface.SNOW_PACKED, speed_kmh=50.0, temp_c=temp))
        print(f"  {temp:>5.0f} °C   {r.distance_m:5.1f} m   "
              f"±{r.sigma_rel*100:.1f} %   usaldus {r.confidence}")
    print("  Nulli lähedal on veapiir laiem kui ükski teine koht mudelis --")
    print("  ja see on aus, sest seal on tõendus kõige vastuolulisem.")


if __name__ == "__main__":
    main()
