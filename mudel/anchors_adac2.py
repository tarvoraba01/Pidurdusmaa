"""
ADAC 2025 suverehvi- ja lamellrehvitest.

Kaks asja, mida need testid mudelisse toovad ja mida varem ei olnud:

  1. TEINE MÄRJA KATSE ALGKIIRUS. Talve- ja suvetest teevad märja
     pidurduse 80 -> 0 km/h, lamellitest 100 -> 0 km/h. Seni oli
     mudelis ainult üks märg alguskiirus, mistõttu märja
     kiirusesõltuvus (wet_lift_b) ei olnud üldse valideeritav.
     Nüüd on: sobita 80 km/h peal, ennusta 100 km/h.

  2. SUVEREHVIDE KATVUS. Enne oli SUMMER_UHP kategoorias üksainus
     ankur, nüüd 18 rehvi x 3 pinda.

Lisaks saab betoonikordajat nüüd kolme eri kummisegu peal kontrollida
(talv / suvi / lamell), mitte ainult ühe.

Allikad, kajastus Tyre Reviews:
  tyrereviews.com/Tyre-Tests/2025-ADAC-Summer-Tyre-Test.htm
  tyrereviews.com/Tyre-Tests/2025-ADAC-All-Season-Tyre-Test.htm

Testitingimused nagu ADAC avaldab. TEMPERATUURID ON OLETUS (asfalt
u +10 C, lumi -5 C, jaa -4 C), nagu ka anchors_adac.py-s.
"""

from .model import Surface, TyreCategory

# --- ADAC 2025 suverehvitest, 225/40 R18, 18 rehvi -------------------------
# [kuiv 100->0, marg asfalt 80->0, marg betoon 80->0, akvaplaneering km/h]
ADAC_SUMMER = {
    "conti_sc7":            ("Continental SportContact 7",    35.20, 28.40, 34.20, 79.6),
    "bridgestone_potsport": ("Bridgestone Potenza Sport",      34.90, 28.80, 34.60, 78.9),
    "michelin_ps5":         ("Michelin Pilot Sport 5",         35.50, 29.20, 35.30, 79.9),
    "goodyear_f1a6":        ("Goodyear Eagle F1 Asymmetric 6", 35.50, 29.50, 35.80, 79.4),
    "kumho_ps71":           ("Kumho Ecsta PS71",               34.80, 30.20, 36.00, 83.7),
    "falken_fk520":         ("Falken Azenis FK520",            35.80, 30.50, 37.70, 78.7),
    "firestone_fhsport":    ("Firestone Firehawk Sport",       35.90, 30.90, 38.00, 77.5),
    "norauto_prevensys4":   ("Norauto Prevensys 4",            38.40, 30.90, 38.40, 77.1),
    "nexen_nfera_su2":      ("Nexen N'Fera Sport SU2",         36.50, 31.00, 38.50, 78.3),
    "toyo_proxes_sport2":   ("Toyo Proxes Sport 2",            35.40, 31.00, 37.80, 78.0),
    "vredestein_ultracpro": ("Vredestein Ultrac Pro",          36.60, 31.00, 37.50, 79.1),
    "yokohama_v107":        ("Yokohama Advan Sport V107",      34.80, 31.20, 37.70, 75.9),
    "dunlop_sportmaxx_rt2": ("Dunlop SportMaxx RT 2",          37.30, 31.50, 38.10, 81.2),
    "nokian_powerproof1":   ("Nokian Powerproof 1",            37.80, 31.50, 39.00, 79.1),
    "syron_premiumperf":    ("Syron Premium Performance",      37.50, 32.30, 40.90, 73.2),
    "ceat_sportdrive":      ("Ceat SportDrive",                37.20, 33.30, 42.00, 76.0),
    "giti_sports2":         ("Giti GitiSportS2",               39.40, 34.60, 44.40, 82.6),
    "doublecoin_dc100":     ("Double Coin DC 100",             39.50, 45.10, 55.20, 69.3),
}
SUMMER_CONDS = [
    ("dry",      Surface.ASPHALT,  0.0, 10.0, 100, 0),
    ("wet",      Surface.ASPHALT,  1.0, 10.0,  80, 0),
    ("concrete", Surface.CONCRETE, 1.0, 10.0,  80, 0),
]

# --- ADAC 2025 lamellrehvitest, 225/45 R17, 16 rehvi -----------------------
# [kuiv 100->0, marg asfalt 100->0, marg betoon 100->0, lumi 30->0,
#  jaa 20->0, akvaplaneering km/h]
ADAC_ALLSEASON = {
    "conti_asc2":        ("Continental AllSeasonContact 2",   40.80, 31.30, 38.40, 9.20, 15.60, 73.0),
    "bridgestone_as6":   ("Bridgestone Turanza All Season 6", 38.50, 31.60, 38.50, 9.60, 15.50, 78.5),
    "pirelli_as_sf3":    ("Pirelli Cinturato All Season SF3", 38.00, 32.50, 38.80, 9.80, 15.40, 78.3),
    "goodyear_v4s3":     ("Goodyear Vector 4Seasons Gen-3",   42.80, 33.20, 39.10, 9.10, 14.70, 74.9),
    "vredestein_quatracpp":("Vredestein Quatrac Pro+",        43.10, 33.40, 39.70, 9.60, 16.50, 70.6),
    "michelin_cc2":      ("Michelin CrossClimate 2",          38.90, 33.60, 40.50, 9.00, 14.80, 76.0),
    "nexen_4season2":    ("Nexen N'Blue 4Season 2",           40.60, 33.60, 41.00, 9.00, 14.20, 71.7),
    "dunlop_as2":        ("Dunlop All Season 2",              43.20, 33.70, 40.20, 9.20, 14.80, 75.3),
    "viking_fourtech":   ("Viking FourTech Plus",             43.90, 34.10, 39.70, 9.50, 15.70, 75.7),
    "bfg_advantage_as":  ("BFGoodrich Advantage All Season",  39.30, 34.30, 42.10, 9.30, 15.30, 77.1),
    "barum_quartaris5":  ("Barum Quartaris 5",                45.30, 35.60, 43.30, 9.00, 15.50, 73.3),
    "petlas_multiaction":("Petlas Multi Action PT 565",       43.90, 36.30, 44.00, 12.50, 18.20, 76.0),
    "cst_allseason_acp1":("CST Medallion All Season ACP1",    44.70, 36.60, 44.40, 9.60, 18.70, 75.4),
    "superia_ecoblue4s": ("Superia Ecoblue2 4S",              41.90, 37.60, 46.50, 9.20, 15.20, 70.4),
    "aplus_as909":       ("Aplus AS909",                      42.20, 39.10, 49.60, 9.40, 14.70, 66.4),
    "arivo_carlorful":   ("Arivo Carlorful AS",               42.20, 42.60, 52.60, 9.60, 15.40, 65.6),
}
# NB! Kajastuse graafikud on markinud lamellitesti MARJA pidurduse
# "100 - 0 km/h". See ei saa oiges olla: 31,3 m 100 km/h pealt tahendaks
# margal haardetegurit 1,26, mis uletab isegi parimate rehvide KUIVA
# haaret. 80 -> 0 km/h juures annab sama arv mu = 0,80, mis klapib tapselt
# sama labori suve- (0,89) ja talvetestiga (0,79). Seega on siin kasutatud
# 80 km/h. Kuiv 100 -> 0 on seevastu ootusparane (mu = 1,03) ja jaab.
# Mudel ise puudis selle vea kinni: 100 km/h eeldusel oli viga +50 %.
ALLSEASON_CONDS = [
    ("dry",      Surface.ASPHALT,     0.0,  10.0, 100, 0),
    ("wet",      Surface.ASPHALT,     1.0,  10.0,  80, 0),
    ("concrete", Surface.CONCRETE,    1.0,  10.0,  80, 0),
    ("snow",     Surface.SNOW_PACKED, 0.0,  -5.0,  30, 0),
    ("ice",      Surface.ICE,         0.0,  -4.0,  20, 0),
]

AQUA_WATER_MM = 7.0

SETS = [
    ("ADACS25", ADAC_SUMMER,    SUMMER_CONDS,    TyreCategory.SUMMER_UHP, "225/40 R18"),
    ("ADACA25", ADAC_ALLSEASON, ALLSEASON_CONDS, TyreCategory.ALL_SEASON, "225/45 R17"),
]

# Margise klass — TULETATUD selle sama testi marja asfaldi tulemusest
# (vt tools/derive_classes.py). EI OLE EPREL-ist kontrollitud.
ADAC_CLASS2 = {
    "conti_sc7": "A",  # G≈1.93
    "bridgestone_potsport": "A",  # G≈1.90
    "michelin_ps5": "A",  # G≈1.87
    "goodyear_f1a6": "A",  # G≈1.85
    "kumho_ps71": "A",  # G≈1.81
    "falken_fk520": "A",  # G≈1.79
    "firestone_fhsport": "A",  # G≈1.76
    "norauto_prevensys4": "A",  # G≈1.76
    "nexen_nfera_su2": "A",  # G≈1.75
    "toyo_proxes_sport2": "A",  # G≈1.75
    "vredestein_ultracpro": "A",  # G≈1.75
    "yokohama_v107": "A",  # G≈1.74
    "dunlop_sportmaxx_rt2": "A",  # G≈1.72
    "nokian_powerproof1": "A",  # G≈1.72
    "syron_premiumperf": "A",  # G≈1.68
    "ceat_sportdrive": "A",  # G≈1.62
    "giti_sports2": "A",  # G≈1.56
    "doublecoin_dc100": "D",  # G≈1.17
    "conti_asc2": "A",  # G≈1.59
    "bridgestone_as6": "A",  # G≈1.58
    "pirelli_as_sf3": "B",  # G≈1.53
    "goodyear_v4s3": "B",  # G≈1.49
    "vredestein_quatracpp": "B",  # G≈1.48
    "michelin_cc2": "B",  # G≈1.48
    "nexen_4season2": "B",  # G≈1.48
    "dunlop_as2": "B",  # G≈1.47
    "viking_fourtech": "B",  # G≈1.45
    "bfg_advantage_as": "B",  # G≈1.44
    "barum_quartaris5": "C",  # G≈1.39
    "petlas_multiaction": "C",  # G≈1.36
    "cst_allseason_acp1": "C",  # G≈1.34
    "superia_ecoblue4s": "C",  # G≈1.31
    "aplus_as909": "C",  # G≈1.25
    "arivo_carlorful": "D",  # G≈1.14
}
