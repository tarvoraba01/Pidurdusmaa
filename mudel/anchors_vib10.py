# -*- coding: utf-8 -*-
"""Vi Bilagare 2010: kaks talverehvitesti, 205/55 R16.

MIKS NEED KAKS TESTI
--------------------
Mudeli ankrud on peaaegu koik uhest aastast (2025), kahest moodust
(225/40 R18 ja 225/45 R17) ja kahest kiirusest (80 ja 100 km/h).
Auditi 4. jagu utleb selle valja: iga pind peale kruusa on
EKSTRAPOLATSIOON. Need kaks testi on teisest aastakumnest, teisest
riigist, teisest moodust ja TEISTELT KIIRUSTELT -- ja seetottu on nad
esmajoones VALJASPOOL-VALIMI KONTROLL, mitte kalibreerimismaterjal.

Nad toovad kaasa kaks asja, mida mudelis uldse ei ole:

  1. JAA KAHEL TEMPERATUURIL, samad rehvid, sama paev. Naastrehvitestis
     on "Broms pa is 30-5 km/tim" moodetud ohutemperatuuril -3...-2 °C
     JA +0,5...+1 °C. See on otsene ice_temp_curve kontroll: uks G, kaks
     ennustust. Praegu ei ole mudelil UHTEGI sellist paari.
  2. LORTS. Veerg "Snoslask, km/tim" on lordsi ujumiskiirus. Lortsi
     mudelis ei ole uldse. Siin ta veel kasutusse ei lahe, aga ta on
     kirjas, et ta ei laheks kaduma.

ALLIKAD
  [VIB10D] "test Dubbade vinterdack", Vi Bilagare 2010.
           vibilagare.se/public/documents/2010/10/dacktest_2010_dubbdack.pdf
           Jaa ja lumi Arvidsjaur; lorts, marg ja kuiv Tampere kandis.
  [VIB10F] "test Odubbade vinterdack", Vi Bilagare 2010.
           vibilagare.se/public/documents/2010/10/
             vib_dacktest_2010_odubbade_vinterdack.pdf
           Jaa ja lumi Tammijarvi (Ivalo); asfalt Tampere kandis.
           Auto: Volvo S40/V50 (lumi/jaa), Volvo C30 (asfalt).

MIS SIIN ON OLETUS, MITTE ALLIKAS -- LOE ENNE KASUTAMIST
--------------------------------------------------------
* TEMPERATUUR. Ainsad avaldatud temperatuurid on naastrehvitesti jaa
  kaks ohutemperatuuri. Lume ja asfaldi temperatuurid EI OLE avaldatud
  kummaski testis. Allpool on need eraldi valjadena, et nad oleksid
  nahtavad ja parandatavad.
* AUTO. Testiautod olid Volvo S40/V50 ja C30; mudelis on `volvo_v50`
  (1319 kg, kaasaegne ABS). C30 on sama platvorm. See on asendus.
* KATEGOORIA. Naastrehvitestis utleb allikas kahe vorrdlusrehvi tuubi
  ise valja ("nord frikt", "kont frikt"). Naelutus testis EI UTLE
  allikas kolme rehvi kohta tuupi valja (Dayton DW 510, Maxxis Presa
  Ice, Nankang Snow Viva SV-1) -- vt KATEGOORIA_KAHTLUS allpool. Neid
  EI TOHI kalibreerimisse votta enne, kui tuup on kinnitatud.

LAHENDAMATA VASTUOLU, MIS TULEB ENNE KASUTAMIST AR LAHENDADA
------------------------------------------------------------
Kahe testi lumepidurdus ei klapi omavahel:
    naelutu test   40->5 km/h   13,2-15,3 m   ->  u 0,43 g
    naastrehvitest 45->5 km/h   36,3-43,0 m   ->  u 0,22 g
Sama ajakiri, sama aasta, sama moot. Kahekordne vahe ei saa olla
rehvide vahe. Uks kolmest peab kehtima: (a) lumi oli hoopis erinev
(Ivalo kova tallatud lumi vs Arvidsjauri pehmem), (b) uks veerg ei ole
see, mis ta pais olevat, (c) transkriptsioon eksis. Kuni see ei ole
lahendatud, EI LAHE lumeread kalibreerimisse.
"""

from .model import Surface, TyreCategory as C

# ---------------------------------------------------------------------------
# [VIB10D] NAASTREHVID + kaks vordlusrehvi. Veerud allikast sonasonalt:
#   "Broms pa sno 45-5 km/tim, m"
#   "Broms pa is 30-5 km/tim, m*"   * ohutemp -3...-2 °C
#   "Broms pa is 30-5 km/tim, m**"  ** ohutemp +0,5...+1 °C
#   "Snoslask, km/tim/betyg"        lordsi ujumiskiirus
#   "Broms vat vag 80-5 km/tim, m"
#   "Broms torr vag 80-5 km/tim, m"
# ---------------------------------------------------------------------------
VIB10D_ICE_T_COLD = -2.5      # allikast: -3...-2 °C
VIB10D_ICE_T_WARM = 0.75      # allikast: +0,5...+1 °C

VIB10D = {
    #  votmenimi           nimi                              kat  lumi   jaa_k  jaa_s  lorts marg  kuiv
    "bridgestone_noranza2":  ("Bridgestone Noranza 2 EVO",      C.WINTER_STUDDED, 42.5, 23.6, 30.4, 33.6, 42.4, 35.6),
    "conti_icecontact":      ("Continental Ice Contact",        C.WINTER_STUDDED, 43.0, 24.9, 32.2, 33.2, 40.7, 36.5),
    "gislaved_nordfrost5":   ("Gislaved Nord Frost 5",          C.WINTER_STUDDED, 36.3, 26.7, 35.5, 31.0, 36.8, 33.8),
    "goodyear_ugextreme":    ("Goodyear Ultra Grip Extreme",    C.WINTER_STUDDED, 36.8, 28.2, 35.0, 31.3, 36.4, 32.4),
    "michelin_xicenorth":    ("Michelin X-Ice North",           C.WINTER_STUDDED, 39.5, 24.3, 29.5, 28.0, 39.8, 34.5),
    "nokian_hkpl7":          ("Nokian Hakkapeliitta 7",         C.WINTER_STUDDED, 39.9, 23.0, 26.3, 32.9, 38.0, 35.2),
    "pirelli_wcarvingedge":  ("Pirelli Winter Carving Edge",    C.WINTER_STUDDED, 37.3, 26.7, 29.3, 31.5, 38.8, 36.0),
    "conti_vikingcontact5":  ("Continental VikingContact 5",    C.WINTER_NORDIC,  42.3, 28.1, 47.4, 32.5, 44.4, 35.1),
    "conti_ts830":           ("Continental WinterContact TS 830", C.WINTER_CENTRAL, 39.3, 35.2, 59.6, 41.9, 32.3, 28.0),
}

# ---------------------------------------------------------------------------
# [VIB10F] NAELUTUD talverehvid + uks naastrehv vordluseks. Veerud:
#   "Broms pa sno 40-5 km/tim, m", "Broms pa is 35-5 km/tim, m",
#   "Broms i vata 80-5 km/tim, m", "Broms torr vag 80-5 km/tim, m"
# Mustrisugavus allikast 8,5-9,7 mm (uksikud vaartused ei ole koik kaes).
# ---------------------------------------------------------------------------
VIB10F = {
    #  votmenimi            nimi                            kat  lumi  jaa   marg  kuiv
    "dayton_dw510":        ("Dayton DW 510",                None, 14.3, 25.8, 34.6, 30.9),
    "gislaved_softfrost3": ("Gislaved Soft Frost 3",     C.WINTER_NORDIC, 13.2, 23.6, 37.3, 31.3),
    "goodyear_ugiceplus":  ("Goodyear Ultra Grip Ice+",  C.WINTER_NORDIC, 15.3, 23.4, 39.2, 31.9),
    "kumho_icepower_kw21": ("Kumho Ice Power KW-21",     C.WINTER_NORDIC, 13.8, 21.2, 41.6, 31.3),
    "maxxis_presaice":     ("Maxxis Presa Ice",              None, 14.0, 24.9, 40.6, 31.3),
    "nankang_snowviva":    ("Nankang Snow Viva SV-1",        None, 13.8, 22.2, 40.6, 31.7),
    "nordman_rs":          ("Nordman RS",                C.WINTER_NORDIC, 14.1, 25.8, 35.5, 31.0),
    "nokian_hkplr":        ("Nokian Hakkapeliitta R",    C.WINTER_NORDIC, 13.9, 22.9, 41.9, 31.4),
    "nokian_hkpl7_f":      ("Nokian Hakkapeliitta 7",    C.WINTER_STUDDED, 14.1, 19.7, 36.2, 33.7),
}

# Kolm rehvi, mille tuupi allikas EI UTLE. Nende andmetes on muster, mis
# viitab Kesk-Euroopa rehvile (hea marg, halb jaa), aga see on JARELDUS
# andmetest, mitte allika vaide -- ja kui ta ette anda, hakkab ta ennast
# ise kinnitama. Seetottu: kategooria None ja valjaspool kalibreerimist.
KATEGOORIA_KAHTLUS = ("dayton_dw510", "maxxis_presaice", "nankang_snowviva")

# --- tingimused, mis EI OLE allikast (vt mooduli pais) ---------------------
TEMP_ASFALT_C = 10.0          # OLETUS: Tampere sugis
TEMP_LUMI_C = -5.0            # OLETUS
WATER_MM = 1.0                # OLETUS: R117 metoodika tuupvaartus
VEHICLE_KEY = "volvo_v50"     # asendus: S40/V50/C30 sama platvorm
SIZE = "205/55 R16"

CONDS = {
    "kuiv":   (Surface.ASPHALT, 0.0, TEMP_ASFALT_C, 80.0, 5.0),
    "marg":   (Surface.ASPHALT, WATER_MM, TEMP_ASFALT_C, 80.0, 5.0),
    "lumi_d": (Surface.SNOW_PACKED, 0.0, TEMP_LUMI_C, 45.0, 5.0),
    "lumi_f": (Surface.SNOW_PACKED, 0.0, TEMP_LUMI_C, 40.0, 5.0),
    "jaa_k":  (Surface.ICE, 0.0, VIB10D_ICE_T_COLD, 30.0, 5.0),
    "jaa_s":  (Surface.ICE, 0.0, VIB10D_ICE_T_WARM, 30.0, 5.0),
    "jaa_f":  (Surface.ICE, 0.0, -5.0, 35.0, 5.0),     # temp OLETUS
}
