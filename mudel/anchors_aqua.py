"""
Akvaplaneerimise ankrud: Teknikens Varld 2025 talverehvitest.

MIKS SEE TEST ON ERILINE
------------------------
20 rehvi, KOIK samas mootmes 235/45 R18, sama auto (Volvo V60 T6),
ja iga rehvi kohta on avaldatud MOODETUD MUSTRISUGAVUS. See lubab
akvaplaneerimise mudelit kontrollida nii, et mustrisugavus on
kontrolli all -- mida uhegi teise testiga teha ei saa.

MIDA SEE PALJASTAS
------------------
Mudel eeldas, et akvaplaneerimise lavi soltub mustri SUGAVUSEST.
Need andmed utlevad, et selles vahemikus (7,6-10 mm) sugavus ei
seleta peaaegu midagi, kull aga seletab palju mustri KUJU:

  Kesk-Euroopa talverehv:  keskmine muster 7,98 mm -> ujumine 73,1 km/h
  Pohjamaade naelutu:      keskmine muster 8,37 mm -> ujumine 60,7 km/h
  Naastrehv:               keskmine muster 8,95 mm -> ujumine 62,0 km/h

Ehk sugavamad Pohjamaade rehvid ujuvad 17 % VARASEMALT. Mudel utles
enne vastupidist. Pohjus on fuusikaline: Pohjamaade rehvi muster on
tehtud lume ja jaa jaoks (palju lamelle, pehme segu), mitte vee
valjajuhtimiseks -- kanalite maht ja kuju on teistsugused.

See on Eesti kasutaja jaoks oluline: naelutu Pohjamaade rehv on siin
levinuim talvevalik ja mudel ULEHINDAS tema akvaplaneerimiskindlust.

Allikas: Teknikens Varld 2025, kajastus Tyre Reviews
  tyrereviews.com/Tyre-Tests/2025-Studded-Friction-and-European-Winter-Tyre-Test.htm
"""

from .model import TyreCategory as C

# nimi, kategooria, mustrisugavus mm, akvaplaneerimise ujumiskiirus km/h
TV25_AQUA = [
    ("Pirelli P Zero Winter 2",           C.WINTER_CENTRAL, 7.9, 75.9),
    ("Goodyear UltraGrip Performance 3",  C.WINTER_CENTRAL, 7.9, 76.8),
    ("Continental WinterContact TS 870 P",C.WINTER_CENTRAL, 7.9, 76.6),
    ("Falken EUROWINTER HS02 Pro",        C.WINTER_CENTRAL, 8.6, 69.1),
    ("Goodride Z507",                     C.WINTER_CENTRAL, 7.6, 67.2),
    ("Continental VikingContact 8",       C.WINTER_NORDIC,  8.3, 56.7),
    ("Goodyear UltraGrip Ice 3",          C.WINTER_NORDIC,  8.4, 64.6),
    ("Pirelli Ice Friction",              C.WINTER_NORDIC,  7.9, 60.4),
    ("Michelin X-Ice Snow",               C.WINTER_NORDIC,  8.2, 62.0),
    ("Nokian Hakkapeliitta R5",           C.WINTER_NORDIC,  8.2, 55.7),
    ("Falken Winterpeak F-Snow 1",        C.WINTER_NORDIC,  8.6, 61.4),
    ("Toyo Observe GSi-6 HP",             C.WINTER_NORDIC,  9.0, 63.8),
    ("Goodyear UltraGrip Ice Arctic 2",   C.WINTER_STUDDED,10.0, 66.8),
    ("Nokian Hakkapeliitta 10",           C.WINTER_STUDDED, 8.8, 57.6),
    ("Continental IceContact 3",          C.WINTER_STUDDED, 8.4, 63.2),
    ("Pirelli Ice Zero 2",                C.WINTER_STUDDED, 9.0, 66.8),
    ("Michelin X-Ice North 4",            C.WINTER_STUDDED, 8.5, 62.5),
    ("Kumho WinterCraft ice Wi32",        C.WINTER_STUDDED, 8.9, 57.6),
    ("Toyo Observe Ice Freezer",          C.WINTER_STUDDED, 8.9, 58.8),
    ("Mazzini Ice Leopard",               C.WINTER_STUDDED, 9.1, 62.6),
]

TV25_SIZE = "235/45 R18"
TV25_CAR = "Volvo V60 T6"
TV25_PRESSURE_BAR = 2.5
# Teknikens Varldi sirge akvaplaneerimise katse veekile paksus ei ole
# avaldatud; kasutame sama lahendit mis ADAC-il (u 7 mm) ja sobitame
# kategooriakordajad SUHTELISENA, nii et absoluutne tase jaab ADAC-i
# vastu valideerituks.
TV25_WATER_MM = 7.0

# ADAC-i testide kategooriapohised keskmised (samast laborist, sama
# meetodiga). Suverehv vs Kesk-Euroopa talverehv on molemad 225/40 R18.
ADAC_AQUA_MEANS = {
    C.SUMMER_UHP: 77.0,        # ADAC 2025 suvetest, 18 rehvi
    C.WINTER_CENTRAL: 72.5,    # ADAC 2025 talvetest, 31 rehvi
    C.ALL_SEASON: 73.6,        # ADAC 2025 lamellitest, 225/45 R17
}
