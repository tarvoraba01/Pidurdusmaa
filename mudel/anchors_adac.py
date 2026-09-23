"""
ADAC 2025 talverehvitest — 31 rehvi, 225/40 R18, viis pinda.

See on suurim üksik andmehulk mudelis ja toob esimest korda sisse
kaks asja, mida varem üldse ei olnud:

  * LUMI   — varem null ankrut, ainult kategooria hinnang kirjandusest
  * MÄRG BETOON — varem üks kalibreerimata kordaja (0,97)

ADAC teeb ka jääteste, mida enamik väljaandeid ei tee, ning avaldab
akvaplaneerimise ujumiskiiruse, mille vastu saab hüdrodünaamilise
mudeli otse kontrollida.

Allikas: ADAC 2025 talverehvitest, kajastus Tyre Reviews
  tyrereviews.com/Tyre-Tests/2025-ADAC-Winter-Tyre-Test.htm

Testitingimused, mida ADAC avaldab:
  kuiv asfalt      100 -> 0 km/h
  märg asfalt       80 -> 0 km/h
  märg betoon       80 -> 0 km/h
  lumi              30 -> 0 km/h
  jää               20 -> 0 km/h
  akvaplaneering    ujumiskiirus km/h

TEMPERATUURID ON OLETUS, mitte ADAC-i avaldatud arv: asfaldi testid
u +10 °C (sügis), lumi -5 °C, jää -4 °C. Need on väljadena nähtaval,
et neid saaks hiljem täpsustada, kui ADAC-i originaalprotokoll käes on.

Testauto: 225/40 R18 klassi ADAC-i talvetestis on VW Golf.
"""

from .model import Surface, Texture, TyreCategory

# rehv: [kuiv 100->0, märg asfalt 80->0, märg betoon 80->0, lumi 30->0,
#        jää 20->0, akvaplaneerimise ujumiskiirus km/h]
ADAC_2025 = {
    "michelin_alpin5":      ("Michelin Pilot Alpin 5",              41.40, 32.20, 36.90,  9.40, 16.30, 75.2),
    "goodyear_ugp3":        ("Goodyear UltraGrip Performance 3",    42.30, 31.70, 36.60,  9.70, 16.70, 77.1),
    "bridgestone_blizzak6": ("Bridgestone Blizzak 6",               43.80, 32.30, 36.50,  9.60, 16.20, 74.9),
    "conti_ts870p":         ("Continental WinterContact TS 870 P",  42.60, 33.00, 38.00,  9.80, 18.10, 75.2),
    "hankook_iceptevo3":    ("Hankook Winter i*cept evo3",          43.70, 32.90, 37.50,  9.70, 17.40, 74.0),
    "nokian_snowproofp":    ("Nokian Snowproof P",                  42.20, 33.40, 37.70, 10.00, 16.00, 67.8),
    "dunlop_ws5":           ("Dunlop Winter Sport 5",               44.00, 34.40, 38.90,  9.50, 16.80, 73.2),
    "uniroyal_winterexpert":("Uniroyal WinterExpert",               43.90, 32.90, 38.10,  9.70, 17.40, 72.1),
    "semperit_speedgrip5":  ("Semperit Speed Grip 5",               44.30, 33.30, 37.60,  9.60, 17.00, 74.2),
    "firestone_winterhawk4":("Firestone Winterhawk 4",              45.20, 33.00, 38.20,  9.70, 16.10, 73.8),
    "kleber_krisalp_hp3":   ("Kleber Krisalp HP3",                  44.20, 35.00, 40.70,  9.40, 16.80, 76.9),
    "fulda_kristall_hp2":   ("Fulda Kristall Control HP2",          45.30, 35.90, 40.00,  9.70, 17.00, 74.0),
    "matador_mp93":         ("Matador MP93 Nordicca",               45.10, 34.90, 40.90,  9.70, 16.80, 72.3),
    "apollo_aspire_xp":     ("Apollo Aspire XP Winter",             43.80, 34.20, 38.90,  9.80, 16.60, 72.6),
    "giti_winterw2":        ("Giti GitiWinterW2",                   45.20, 34.70, 40.00, 10.00, 17.80, 78.9),
    "maxxis_wp6":           ("Maxxis Premitra Snow WP6",            45.20, 36.40, 41.00,  9.70, 17.50, 74.6),
    "momo_northpole":       ("Momo North Pole W 20 EUROPA",         43.10, 32.70, 36.60,  9.80, 16.70, 71.1),
    "landsail_winter":      ("Landsail Winter Lander",              42.50, 32.80, 36.90, 12.20, 16.70, 71.1),
    "ceat_winterdrive":     ("Ceat WinterDrive",                    42.00, 34.50, 39.70,  9.70, 15.50, 71.5),
    "points_winters":       ("Point S Winter S",                    44.50, 35.00, 40.40,  9.70, 16.70, 73.5),
    "gtradial_winterpro2":  ("GT Radial WinterPro2 Sport",          45.00, 36.30, 40.80,  9.70, 17.00, 73.4),
    "petlas_snowmaster2":   ("Petlas SnowMaster 2 Sport",           43.90, 35.50, 41.00, 10.40, 16.90, 65.8),
    "nankang_activa_sv4":   ("Nankang Winter Activa SV 4",          44.80, 35.60, 41.40, 10.30, 19.10, 71.9),
    "cst_medallion_wcp1":   ("CST Medallion Winter WCP1",           43.30, 35.30, 40.20, 10.90, 19.30, 75.1),
    "radar_dimax_winter":   ("Radar Dimax Winter",                  44.10, 36.70, 41.70,  9.50, 15.80, 67.7),
    "imperial_snowdragon":  ("Imperial Snowdragon UHP",             44.60, 37.80, 43.60, 10.30, 17.40, 68.7),
    "goodride_sw608":       ("Goodride SW608",                      45.00, 38.50, 44.70, 10.50, 18.20, 72.1),
    "starperf_stratos":     ("Star Performer Stratos UHP",          44.40, 39.90, 47.10,  9.90, 17.40, 66.8),
    "tomket_snowroad3":     ("Tomket Snowroad Pro 3",               44.80, 40.40, 47.30, 10.00, 15.90, 67.9),
    "evergreen_ew66":       ("Evergreen Winter EW66",               46.20, 42.30, 47.70,  9.70, 21.10, 70.8),
    "syron_everest2":       ("Syron Everest 2",                     46.00, 47.10, 53.00,  9.20, 15.20, 61.6),
}

# Testitingimused pinna kaupa: (Surface, veekile mm, temp °C, v0, v1)
ADAC_CONDS = [
    ("dry",      Surface.ASPHALT,  0.0,  10.0, 100, 0),
    ("wet",      Surface.ASPHALT,  1.0,  10.0,  80, 0),
    ("concrete", Surface.CONCRETE, 1.0,  10.0,  80, 0),
    ("snow",     Surface.SNOW_PACKED, 0.0, -5.0, 30, 0),
    ("ice",      Surface.ICE,      0.0,  -4.0,  20, 0),
]

# ADAC-i avaldatud akvaplaneerimise ujumiskiirus. ADAC-i sirge
# akvaplaneerimise katses on veekile paksus u 7 mm.
ADAC_AQUA_WATER_MM = 7.0


# Märgise klass, TULETATUD selle sama testi märja asfaldi tulemusest.
# EI OLE EPREL-ist kontrollitud — päris süsteemis tuleb see sealt.
# Vahemik B..E on talverehvidele realistlik.
ADAC_CLASS = {
    "apollo_aspire_xp": "C",  # G≈1.31
    "bridgestone_blizzak6": "C",  # G≈1.40
    "ceat_winterdrive": "C",  # G≈1.30
    "conti_ts870p": "C",  # G≈1.36
    "cst_medallion_wcp1": "C",  # G≈1.27
    "dunlop_ws5": "C",  # G≈1.30
    "evergreen_ew66": "E",  # G≈1.04
    "firestone_winterhawk4": "C",  # G≈1.36
    "fulda_kristall_hp2": "D",  # G≈1.24
    "giti_winterw2": "C",  # G≈1.29
    "goodride_sw608": "D",  # G≈1.15
    "goodyear_ugp3": "B",  # G≈1.42
    "gtradial_winterpro2": "D",  # G≈1.23
    "hankook_iceptevo3": "C",  # G≈1.37
    "imperial_snowdragon": "D",  # G≈1.18
    "kleber_krisalp_hp3": "C",  # G≈1.28
    "landsail_winter": "C",  # G≈1.37
    "matador_mp93": "C",  # G≈1.28
    "maxxis_wp6": "D",  # G≈1.23
    "michelin_alpin5": "B",  # G≈1.40
    "momo_northpole": "C",  # G≈1.38
    "nankang_activa_sv4": "C",  # G≈1.26
    "nokian_snowproofp": "C",  # G≈1.35
    "petlas_snowmaster2": "C",  # G≈1.26
    "points_winters": "C",  # G≈1.28
    "radar_dimax_winter": "D",  # G≈1.22
    "semperit_speedgrip5": "C",  # G≈1.35
    "starperf_stratos": "D",  # G≈1.11
    "syron_everest2": "E",  # G≈0.93
    "tomket_snowroad3": "E",  # G≈1.10
    "uniroyal_winterexpert": "C",  # G≈1.37
}
