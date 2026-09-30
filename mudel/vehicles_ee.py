"""
Eesti sõidukipargi autod.

MIKS JUST NEED AUTOD
--------------------
Eesti sõidukipark on vana: ACEA järgi on registreeritud sõiduautode
keskmine vanus 16,6 aastat, tegelikult teel liikuvatel u 13 aastat
(ERR / Transpordiamet). Uute autode müügi edetabel ei kirjelda seda
parki üldse. Seepärast on siin valik tehtud KASUTATUD TURU ja pargi,
mitte uute autode müügi järgi.

Allikad:
  * Autoportaal, kasutatud autode turg (veebruar 2026): 6031 omanikuvahetust.
    Margid: BMW 842, Volkswagen 608, Toyota 491.
    Mudelid: BMW 3-seeria 293, BMW 5-seeria 262, VW Passat 232.
    Kuni 10 aastat vanad: Škoda Octavia 129, Toyota RAV4 86, Corolla 80.
    Imporditud autode keskmine vanus 7,38 a, peamine päritolu Saksamaa.
  * AutoReport.ee "Eesti levinuimad kasutatud autod" — 16 mudelijuhendit:
    VW Golf, VW Passat, Toyota Corolla, Toyota RAV4, BMW 320d, BMW 520d,
    Audi A4, Škoda Octavia, Škoda Superb, VW Tiguan, Audi A6,
    Mercedes E-klass, Nissan Qashqai, Volvo XC60, Toyota Avensis, Kia Sportage.
  * Autoportaal, uute autode müük 2025: Corolla 776, Octavia 712, RAV4 574.
  * Transpordiameti register (mntstat.ee, 01.07.2026): 674 747 sõiduautot.
    Margid: Volkswagen 90 537, Toyota 73 620, BMW 66 792, Audi 57 121,
    Škoda 53 116. Mudelid: Passat 20 704, Octavia 20 561, Golf 16 055,
    Corolla 15 126, RAV4 13 700.
    NB: registri mudelitasand ON avalik, aga ainult JavaScripti taga --
    server tagastab ainult top-5. Seepärast kasutati mudelivalikuks
    auto24.ee kuulutuste arvu, kalibreerituna kahe teadaoleva punkti
    vastu: Passat 321 kuulutust vs 20 704 registreeritud (64,5 autot
    kuulutuse kohta), Golf 187 vs 16 055 (85,9).
  * PARGI VANUS on vaieldav ja vahe on suur: ACEA ütleb ~17 aastat,
    Transpordiamet tegelikult liikuvate kohta 13, Liikluskindlustuse
    Fond 11,85. Vahe tuleb ~205 000 peatatud registreeringuga autost,
    mis registris on, aga teel ei ole. Autovalik on kaalutud
    TEGELIKULT LIIKUVA pargi järgi, ehk aastatele 2005-2018.

MIS ON MÕÕDETUD JA MIS HINNATUD
-------------------------------
Mõõdetud / tootja andmed:  tühimass, teljevahe, laius, kõrgus,
                           soovituslik rehvirõhk, OEM-rehvimõõt.
Kirjandusest:              õhutakistustegur Cd.
Arvutatud:                 otsapindala A = 0,83 · laius · kõrgus
                           (levinud lähend), CdA = Cd · A.
Hinnang:                   pidurite võimekus klassi järgi. Sellel on
                           nüüd regulatiivne alumine piir: UN R13-H
                           nõuab M1-sõidukilt kuival vähemalt
                           6,43 m/s² ehk 0,656 g. audit.py kontrollib.

KAKS ERI TASET MÄRKUSEGA ("note") RIDADEL:
  "hinnang" / "Cd hinnang"  -- rida tuli spetsifikatsioonilehelt, aga
                               mõni üksik väli oli seal tühi
  "mõõdud ligikaudsed"      -- 2026-09-18 lisatud tavalised pereautod.
                               Mass, Cd ja mõõdud EI OLE esmaallikast
                               kontrollitud. Mudeliaasta, ABS-i põlvkond
                               ja rehvimõõt on teada; ülejäänu on
                               suurusjärk. Auditi tundlikkusanalüüs
                               ütleb, miks see on lubatav: tühimassi
                               160 kg viga muudab vastust alla promilli.
                               Need read on grep'itavad, kui keegi tahab
                               need hiljem üle kontrollida.

MÄRKUSEGA ("note") READ on need, kus mõni väli ei tulnud esmaallikast.
2026-09-17 lisatud 42 autot on kehvemini dokumenteeritud kui varasemad
-- Cd puudus auto-data.net-il 11 juhul 15-st esimeses partiis ja kõigil
neljal kaubikul. Iga selline väärtus on märkuses hinnanguks märgitud.
Kaubikute rõhk on eraldi lugu: leitud väärtused (3,3-4,2 bar) on
TÄISKOORMA omad ja neid EI OLE siia pandud; siin on tühja sõiduki
tüüpväärtused, mis on märkuses samuti välja öeldud.

TÄHTIS: pidurdusmaa jaoks on nendest oluline peamiselt ABS-i põlvkond.
Mass taandub füüsikas peaaegu välja (a = μg) ja õhutakistus annab
130 km/h juures ainult 1-2 %. Nii et kui mõni tühimass on siin
50 kg mööda, ei muuda see tulemust praktiliselt üldse — aga vale
ABS-i põlvkond muudaks palju.

ABS-I PÕLVKONNA MÄÄRAMINE
-------------------------
Kaks EL-i tähtaega annavad piirid:
  ABS  — kohustuslik uutel sõiduautodel alates 2004
  ESC  — kohustuslik uutel tüüpidel 1.11.2011, kõigil uutel 1.11.2014
Seega:  EARLY   kuni 2003 (ABS on, aga varane)
        MODERN  2004-2014
        LATEST  2015+ (ESC + pidurdusabi standardis)
Üksik auto võib olla erand (nt BMW-l oli ESC ammu enne kohustust),
aga klassi tasemel need piirid kehtivad.
"""

from .model import AbsClass as A

# nimi, mass kg, Cd, laius m, kõrgus m, teljevahe m, rõhk bar, mõõt, ABS, pidurid g
EE_VEHICLES = [
    # --- kõige rohkem kaubeldud mudelid (BMW 3 ja 5, VW Passat) -----------
    ("bmw_320d_e90",  "BMW 320d E90 (2005-2012)",        1450, 0.28, 1.817, 1.421, 2.760, 2.3, "205/55 R16", A.MODERN, 1.30),
    ("bmw_320d_f30",  "BMW 320d F30 (2012-2019)",        1495, 0.27, 1.811, 1.429, 2.810, 2.4, "205/60 R16", A.LATEST, 1.30),
    ("bmw_520d_e60",  "BMW 520d E60 (2003-2010)",        1585, 0.27, 1.846, 1.469, 2.888, 2.4, "225/55 R16", A.MODERN, 1.28),
    ("bmw_520d_f10",  "BMW 520d F10 (2010-2017)",        1615, 0.27, 1.860, 1.464, 2.968, 2.5, "225/55 R17", A.LATEST, 1.30),
    ("bmw_520d_g30",  "BMW 520d G30 (2017-2023)",        1610, 0.22, 1.868, 1.466, 2.975, 2.5, "225/55 R17", A.LATEST, 1.32),
    ("vw_passat_b6",  "VW Passat B6 2.0 TDI (2005-2010)",1440, 0.29, 1.820, 1.472, 2.709, 2.4, "215/55 R16", A.MODERN, 1.28),
    ("vw_passat_b7",  "VW Passat B7 2.0 TDI (2010-2014)",1450, 0.29, 1.820, 1.470, 2.712, 2.4, "215/55 R16", A.MODERN, 1.28),

    # --- VW Golf, kõik levinud põlvkonnad ---------------------------------
    ("vw_golf_5",     "VW Golf V 1.9 TDI (2003-2008)",   1310, 0.32, 1.759, 1.485, 2.578, 2.3, "195/65 R15", A.MODERN, 1.28),
    ("vw_golf_6",     "VW Golf VI 1.6 TDI (2008-2012)",  1320, 0.31, 1.779, 1.479, 2.578, 2.3, "205/55 R16", A.MODERN, 1.28),
    ("vw_golf_7",     "VW Golf VII 1.6 TDI (2012-2019)", 1280, 0.29, 1.799, 1.452, 2.637, 2.3, "205/55 R16", A.LATEST, 1.30),

    # --- Škoda ------------------------------------------------------------
    ("skoda_octavia_2","Škoda Octavia II 1.9 TDI (2004-2013)",1315,0.30,1.769,1.462,2.578,2.2,"195/65 R15",A.MODERN,1.28),
    ("skoda_octavia_3","Škoda Octavia III 2.0 TDI (2013-2020)",1280,0.28,1.814,1.461,2.686,2.4,"205/55 R16",A.LATEST,1.30),
    ("skoda_superb_3", "Škoda Superb III 2.0 TDI (2015-2023)",1450,0.28,1.864,1.468,2.841,2.4,"215/55 R17",A.LATEST,1.30),

    # --- Audi -------------------------------------------------------------
    ("audi_a4_b8",    "Audi A4 B8 2.0 TDI (2008-2015)",  1470, 0.27, 1.826, 1.427, 2.808, 2.4, "225/55 R16", A.MODERN, 1.30),
    ("audi_a6_c7",    "Audi A6 C7 2.0 TDI (2011-2018)",  1575, 0.26, 1.874, 1.455, 2.912, 2.5, "225/55 R17", A.LATEST, 1.30),

    # --- Mercedes ---------------------------------------------------------
    ("mb_e220_w212",  "Mercedes E220 CDI W212 (2009-2016)",1660,0.25,1.854,1.474,2.874,2.4,"225/55 R16",A.MODERN,1.30),

    # --- Toyota -----------------------------------------------------------
    ("toyota_corolla_e120","Toyota Corolla E120 (2002-2007)",1180,0.30,1.710,1.475,2.600,2.2,"195/60 R15",A.MODERN,1.25),
    ("toyota_avensis_t25", "Toyota Avensis T25 (2003-2008)", 1390,0.28,1.760,1.480,2.700,2.3,"205/55 R16",A.MODERN,1.26),
    ("toyota_avensis_t27", "Toyota Avensis T27 (2009-2018)", 1430,0.28,1.810,1.480,2.700,2.4,"205/60 R16",A.LATEST,1.28),
    ("toyota_rav4_4",      "Toyota RAV4 IV (2013-2018)",     1560,0.32,1.845,1.660,2.660,2.3,"225/65 R17",A.LATEST,1.25),
    ("toyota_rav4_5",      "Toyota RAV4 V Hybrid (2019+)",   1660,0.32,1.855,1.685,2.690,2.4,"225/60 R18",A.LATEST,1.27),

    # --- maasturid ja mahtuniversaalid ------------------------------------
    ("vw_tiguan_1",   "VW Tiguan I 2.0 TDI (2007-2016)",  1600, 0.37, 1.809, 1.686, 2.604, 2.3, "215/65 R16", A.MODERN, 1.24),
    ("vw_tiguan_2",   "VW Tiguan II 2.0 TDI (2016-2023)", 1585, 0.31, 1.839, 1.673, 2.681, 2.4, "215/65 R17", A.LATEST, 1.28),
    ("nissan_qashqai_j11","Nissan Qashqai J11 (2013-2021)",1400, 0.32, 1.806, 1.590, 2.646, 2.3, "215/60 R17", A.LATEST, 1.26),
    ("volvo_xc60_1",  "Volvo XC60 I (2008-2017)",         1770, 0.35, 1.891, 1.713, 2.774, 2.4, "235/60 R18", A.MODERN, 1.24),
    # Q5 lisati [UTAC25N] lumeankru katsesõidukina (vt
    # anchors_snow_nordic.py) ja jäi ka valikusse, sest Eesti pargis on
    # teda palju. Mass, Cd ja mõõdud on auto-data.net-ist 2.0 TDI 150 hp
    # ESIVEOLISE kohta; katses oli quattro, mis on raskem. Massi ei ole
    # siia juurde arvatud, sest quattro tühimassi ei õnnestunud
    # esmaallikast kinnitada -- ja a = mu*g juures mass niikuinii
    # taandub, mida calibrate_snow_nordic.py ka näitab.
    ("audi_q5_fy",    "Audi Q5 II FY 2.0 TDI (2016-2024)",1660, 0.30, 1.889, 1.656, 2.820, 2.4, "235/60 R18", A.LATEST, 1.26, "mass/Cd/mõõdud auto-data.net, 150 hp esivedu; quattro on raskem"),
    ("volvo_v70_3",   "Volvo V70 III (2007-2016)",        1600, 0.30, 1.861, 1.545, 2.816, 2.4, "215/65 R16", A.MODERN, 1.28),
    ("kia_sportage_3","Kia Sportage III (2010-2016)",     1500, 0.35, 1.855, 1.635, 2.640, 2.3, "215/70 R16", A.MODERN, 1.24),
    ("honda_crv_3",   "Honda CR-V III (2007-2012)",       1560, 0.34, 1.820, 1.680, 2.620, 2.3, "225/65 R17", A.MODERN, 1.24),
    ("mitsubishi_outlander_3","Mitsubishi Outlander III (2012-2021)",1520,0.33,1.800,1.680,2.670,2.3,"225/60 R17",A.LATEST,1.25),
    ("subaru_forester_sj","Subaru Forester SJ (2013-2018)",1520, 0.35, 1.795, 1.735, 2.640, 2.3, "225/60 R17", A.LATEST, 1.25),

    # --- laiatarbe keskklass ----------------------------------------------
    ("opel_astra_h",  "Opel Astra H (2004-2010)",         1250, 0.32, 1.753, 1.460, 2.614, 2.2, "195/65 R15", A.MODERN, 1.25),
    ("ford_focus_2",  "Ford Focus II (2004-2011)",        1250, 0.32, 1.840, 1.497, 2.640, 2.3, "195/65 R15", A.MODERN, 1.26),
    ("ford_mondeo_4", "Ford Mondeo IV (2007-2014)",       1520, 0.30, 1.886, 1.500, 2.850, 2.4, "215/55 R16", A.MODERN, 1.28),
    ("mazda_6_gh",    "Mazda 6 GH (2008-2012)",           1420, 0.28, 1.795, 1.440, 2.725, 2.3, "205/60 R16", A.MODERN, 1.27),
    ("peugeot_308_1", "Peugeot 308 I (2007-2013)",        1330, 0.31, 1.815, 1.498, 2.608, 2.3, "205/55 R16", A.MODERN, 1.25),
    ("renault_megane_3","Renault Mégane III (2008-2016)", 1280, 0.31, 1.808, 1.471, 2.641, 2.3, "205/55 R16", A.MODERN, 1.25),
    ("hyundai_i30_2", "Hyundai i30 II (2011-2016)",       1300, 0.30, 1.780, 1.470, 2.650, 2.3, "195/65 R15", A.MODERN, 1.26),

    # =====================================================================
    # 2. LAINE (september 2026) — 68 autot juurde
    # =====================================================================
    # Valik on tehtud Transpordiameti pargistatistika ja kasutatud turu
    # tehingunumbrite järgi, mitte pakutavuse järgi:
    #   * Sõidukipark 1.07.2026: 674 747 sõiduautot, KESKMINE VANUS 14,5 a
    #     (mntstat.ee, Transpordiameti avaandmete peal). Ehk mediaan-auto
    #     Eesti teel on u 2011. aasta mudel -- seepärast on siin palju
    #     2000. aastate põlvkondi, mitte uusi mudeleid.
    #   * Enim kaubeldud mudelid, aprill 2026 (autoportaal.ee, 7990 tehingut):
    #     BMW 3 (349), BMW 5 (335), Passat (302), Octavia (249),
    #     Audi A6 (186), Corolla (161), Golf (153), Audi A4 (147),
    #     Mercedes E (122), BMW X5 (119).
    #   * Import on pool turgu: aprillis 1614 kasutatud autot, Saksamaa 589,
    #     Soome 216, Leedu 117. Imporditu keskmine vanus 7,4-8 aastat.
    #   * Uute müügi tipud 2026: Toyota Yaris Cross, Škoda Kodiaq, C-HR,
    #     Yaris, Kamiq, Renault Captur.
    #   * Elektriautosid on pargis u 10 000 ehk 1,3 %. Eesti erisus:
    #     Mitsubishi i-MiEV on 426 tükiga riigi SUURUSELT KOLMAS elektriauto,
    #     sest riik ostis 2011 Kyoto kvootide eest u 500 tükki sotsiaaltöö-
    #     tajatele. Mujal maailmas seda autot praktiliselt ei ole.
    #
    # ANDMETE KVALITEET SELLES PLOKIS
    # --------------------------------
    # Tühimass, mõõdud ja teljevahe on tootja andmed (peamiselt
    # auto-data.net, tootjate pressimaterjalid, Toyota UK tehnilised
    # lehed). Rehvirõhk on tootja normaalkoormuse väärtus seal, kus see
    # leidus (tpressure.com, wheel-size.com, allebandenspanning.nl).
    #
    # Kus Cd või rõhk EI OLNUD avaldatud, on kasutatud klassi tüüpväärtust
    # ja rida on märgitud: "Cd hinnang" ja/või "rõhk hinnang". Neid on
    # palju -- kaubikutel ja raamil maasturitel (Prado, Pajero, Grand
    # Vitara, Niva) ei avalda tootjad Cd-d üldse, ja Honda, Subaru ning
    # Kia ei avaldanud seda nende põlvkondade Euroopa materjalides.
    # Pidurdusmaa jaoks on see väike risk: Cd annab 130 km/h juures 1-2 %.
    # Rõhu hinnang on tõsisem, sest see on rõhukõvera nullpunkt --
    # kui kasutaja liugurit ei liiguta, on tulemus selle suhtes.

    # --- enim kaubeldud, mida seni ei olnud ------------------------------
    ("audi_a6_c5",    "Audi A6 C5 2.5 TDI (1997-2004)",   1520, 0.28, 1.810, 1.452, 2.760, 2.4, "205/60 R15", A.EARLY,  1.26, "rõhk hinnang (16-tollise pealt)"),
    ("audi_a6_c6",    "Audi A6 C6 2.0 TDI (2004-2011)",   1540, 0.29, 1.855, 1.459, 2.843, 2.3, "205/60 R16", A.MODERN, 1.28, ""),
    ("audi_a4_b6",    "Audi A4 B6 1.9 TDI (2000-2005)",   1405, 0.29, 1.772, 1.428, 2.650, 2.3, "205/55 R16", A.EARLY,  1.26, ""),
    ("audi_a4_b7",    "Audi A4 B7 2.0 TDI (2004-2008)",   1430, 0.29, 1.772, 1.427, 2.648, 2.4, "205/55 R16", A.MODERN, 1.28, ""),
    ("bmw_320i_e46",  "BMW 320i E46 (1998-2006)",         1390, 0.29, 1.740, 1.420, 2.725, 2.0, "195/65 R15", A.EARLY,  1.28, ""),
    ("bmw_525d_e39",  "BMW 525d E39 (1995-2003)",         1575, 0.27, 1.800, 1.435, 2.830, 2.2, "225/60 R15", A.EARLY,  1.28, "rõhk hinnang"),
    ("bmw_x5_e53",    "BMW X5 3.0d E53 (1999-2006)",      2170, 0.35, 1.872, 1.717, 2.820, 2.0, "235/65 R17", A.EARLY,  1.20, "Cd hinnang"),
    ("bmw_x5_e70",    "BMW X5 30d E70 (2006-2013)",       2075, 0.34, 1.933, 1.739, 2.933, 2.4, "255/55 R18", A.MODERN, 1.24, "rõhk hinnang"),
    ("bmw_x3_e83",    "BMW X3 2.0d E83 (2003-2010)",      1750, 0.35, 1.853, 1.674, 2.795, 2.0, "235/55 R17", A.MODERN, 1.22, "Cd hinnang"),
    ("bmw_x3_f25",    "BMW X3 20d F25 (2010-2017)",       1715, 0.33, 1.881, 1.661, 2.810, 2.3, "225/60 R17", A.MODERN, 1.26, ""),
    ("mb_e220_w210",  "Mercedes E220 CDI W210 (1995-2002)",1590,0.28, 1.799, 1.440, 2.833, 2.0, "195/65 R15", A.EARLY,  1.26, ""),
    ("mb_e220_w211",  "Mercedes E220 CDI W211 (2002-2009)",1610,0.27, 1.822, 1.452, 2.854, 2.1, "205/60 R16", A.MODERN, 1.28, ""),
    ("mb_c220_w203",  "Mercedes C220 CDI W203 (2000-2007)",1445,0.27, 1.728, 1.426, 2.715, 2.1, "195/65 R15", A.MODERN, 1.27, ""),
    ("mb_c220_w204",  "Mercedes C220 CDI W204 (2007-2014)",1510,0.28, 1.770, 1.447, 2.760, 2.2, "205/55 R16", A.MODERN, 1.29, "rõhk hinnang"),
    ("volvo_xc90_1",  "Volvo XC90 I D5 (2002-2014)",      2080, 0.36, 1.898, 1.743, 2.857, 2.0, "235/65 R17", A.MODERN, 1.22, "Cd hinnang"),
    ("volvo_v60_1",   "Volvo S60/V60 I D4 (2010-2018)",   1577, 0.28, 1.865, 1.484, 2.776, 2.4, "215/55 R16", A.LATEST, 1.29, "rõhk hinnang"),
    ("volvo_v50",     "Volvo V50 1.6D (2004-2012)",       1319, 0.31, 1.770, 1.457, 2.640, 2.0, "195/65 R15", A.MODERN, 1.26, ""),

    # --- Škoda, Ford, Opel, VW: pargi selgroog ---------------------------
    ("skoda_fabia_2", "Škoda Fabia II (2007-2014)",       1130, 0.33, 1.642, 1.498, 2.462, 2.1, "165/70 R14", A.MODERN, 1.22, ""),
    ("skoda_fabia_3", "Škoda Fabia III (2014-2021)",      1035, 0.324,1.732, 1.467, 2.470, 2.2, "185/60 R15", A.LATEST, 1.26, "rõhk hinnang"),
    ("skoda_kodiaq_1","Škoda Kodiaq I 2.0 TDI (2016-2024)",1639,0.33, 1.882, 1.655, 2.791, 2.3, "215/65 R17", A.LATEST, 1.27, "rõhk hinnang"),
    ("skoda_kamiq",   "Škoda Kamiq 1.0 TSI (2019+)",      1156, 0.330,1.793, 1.553, 2.651, 2.2, "205/60 R16", A.LATEST, 1.27, "rõhk hinnang"),
    ("ford_focus_3",  "Ford Focus III (2011-2018)",       1269, 0.273,1.823, 1.484, 2.648, 2.3, "205/55 R16", A.MODERN, 1.27, "rõhk hinnang"),
    ("opel_astra_j",  "Opel Astra J (2009-2015)",         1515, 0.31, 1.814, 1.510, 2.685, 2.3, "205/60 R16", A.MODERN, 1.26, ""),
    ("opel_zafira_b", "Opel Zafira B (2005-2014)",        1613, 0.31, 1.801, 1.645, 2.703, 2.3, "205/55 R16", A.MODERN, 1.24, ""),
    ("opel_vectra_c", "Opel Vectra C (2002-2008)",        1523, 0.29, 1.798, 1.460, 2.700, 2.3, "195/65 R15", A.MODERN, 1.26, "rõhk hinnang"),
    ("vw_touran_1",   "VW Touran I 1.9 TDI (2003-2015)",  1498, 0.315,1.794, 1.635, 2.677, 2.2, "195/65 R15", A.MODERN, 1.25, ""),
    ("vw_polo_5",     "VW Polo V 1.6 TDI (2009-2017)",    1107, 0.32, 1.682, 1.462, 2.470, 2.1, "185/60 R15", A.MODERN, 1.25, "rõhk hinnang"),
    ("vw_troc",       "VW T-Roc 1.5 TSI (2017-2025)",     1330, 0.34, 1.819, 1.573, 2.590, 2.2, "215/55 R17", A.LATEST, 1.27, "Cd ja rõhk hinnang"),

    # --- prantsuse ja Dacia ----------------------------------------------
    ("renault_clio_4","Renault Clio IV (2012-2019)",      1071, 0.32, 1.777, 1.448, 2.589, 2.3, "185/65 R15", A.MODERN, 1.24, "Cd hinnang"),
    ("renault_captur_2","Renault Captur II (2019+)",      1234, 0.34, 1.797, 1.585, 2.639, 2.3, "215/60 R17", A.LATEST, 1.26, "Cd ja rõhk hinnang"),
    ("dacia_duster_2","Dacia Duster II (2017-2024)",      1205, 0.37, 1.804, 1.693, 2.674, 2.2, "215/65 R16", A.LATEST, 1.22, "Cd ja rõhk hinnang"),
    ("peugeot_206",   "Peugeot 206 1.4 (1998-2010)",       950, 0.33, 1.652, 1.428, 2.442, 2.4, "175/65 R14", A.EARLY,  1.20, ""),

    # --- Mazda -----------------------------------------------------------
    ("mazda_3_bk",    "Mazda 3 BK (2003-2009)",           1185, 0.34, 1.755, 1.465, 2.640, 2.2, "205/55 R16", A.MODERN, 1.26, "rõhk parandatud: allikas andis 1,8 bar, mis on selle auto kohta ebausutav"),
    ("mazda_cx5_ke",  "Mazda CX-5 KE (2012-2017)",        1410, 0.33, 1.840, 1.710, 2.700, 2.3, "225/65 R17", A.MODERN, 1.25, "rõhk hinnang"),

    # --- Toyota: pargi teine mark ----------------------------------------
    ("toyota_auris_1","Toyota Auris E150 (2006-2012)",    1265, 0.30, 1.760, 1.515, 2.600, 2.2, "205/55 R16", A.MODERN, 1.25, "Cd hinnang"),
    ("toyota_auris_2","Toyota Auris E180 Hybrid (2012-2018)",1355,0.28,1.760,1.460, 2.600, 2.3, "195/65 R15", A.MODERN, 1.27, ""),
    ("toyota_yaris_3","Toyota Yaris XP130 (2011-2020)",   1090, 0.287,1.695, 1.510, 2.510, 2.2, "175/65 R15", A.MODERN, 1.24, ""),
    ("toyota_yaris_4","Toyota Yaris XP210 Hybrid (2020+)",1145, 0.31, 1.745, 1.500, 2.560, 2.2, "185/60 R15", A.LATEST, 1.28, ""),
    ("toyota_yariscross","Toyota Yaris Cross Hybrid (2021+)",1175,0.35,1.765,1.590, 2.560, 2.3, "205/65 R16", A.LATEST, 1.27, ""),
    ("toyota_chr_1",  "Toyota C-HR I Hybrid (2016-2023)", 1420, 0.32, 1.795, 1.555, 2.640, 2.3, "215/60 R17", A.LATEST, 1.27, ""),
    ("toyota_lc120",  "Toyota Land Cruiser 120 (2002-2009)",2130,0.40,1.875, 1.865, 2.790, 2.2, "265/65 R17", A.MODERN, 1.15, "Cd hinnang; raamil maastur"),
    ("toyota_bz4x",   "Toyota bZ4X (2022+)",              1920, 0.29, 1.860, 1.650, 2.850, 2.6, "235/60 R18", A.LATEST, 1.28, "Cd hinnang"),

    # --- muu Aasia -------------------------------------------------------
    ("nissan_qashqai_j10","Nissan Qashqai J10 (2006-2013)",1407,0.34, 1.780, 1.605, 2.630, 2.3, "215/65 R16", A.MODERN, 1.24, "Cd hinnang"),
    ("honda_crv_4",   "Honda CR-V IV (2012-2018)",        1653, 0.34, 1.820, 1.685, 2.630, 2.3, "225/65 R17", A.MODERN, 1.25, "Cd hinnang"),
    ("honda_civic_8", "Honda Civic VIII (2006-2011)",     1250, 0.31, 1.760, 1.460, 2.635, 2.1, "205/55 R16", A.MODERN, 1.26, "Cd hinnang"),
    ("subaru_outback_br","Subaru Outback BR (2009-2014)", 1571, 0.33, 1.820, 1.605, 2.745, 2.2, "225/60 R17", A.MODERN, 1.25, "Cd hinnang"),
    ("subaru_outback_bs","Subaru Outback BS (2014-2019)", 1695, 0.33, 1.840, 1.605, 2.745, 2.4, "225/65 R17", A.LATEST, 1.27, "Cd hinnang"),
    ("subaru_legacy_bp","Subaru Legacy BP (2003-2009)",   1360, 0.31, 1.730, 1.470, 2.670, 2.2, "205/55 R16", A.MODERN, 1.26, "Cd hinnang; rõhk 16-tollisele"),
    ("mitsu_pajero_4","Mitsubishi Pajero IV (2006-2021)", 2310, 0.40, 1.875, 1.870, 2.780, 2.2, "265/65 R17", A.MODERN, 1.12, "Cd hinnang; raamil maastur"),
    ("hyundai_tucson_tl","Hyundai Tucson TL (2015-2020)", 1425, 0.33, 1.850, 1.655, 2.670, 2.4, "225/60 R17", A.LATEST, 1.26, ""),
    ("hyundai_tucson_nx4","Hyundai Tucson NX4 (2020+)",   1425, 0.315,1.865, 1.651, 2.680, 2.4, "215/65 R17", A.LATEST, 1.28, ""),
    ("kia_ceed_jd",   "Kia Ceed JD (2012-2018)",          1300, 0.30, 1.780, 1.470, 2.650, 2.2, "205/55 R16", A.MODERN, 1.26, "Cd hinnang"),
    ("kia_ceed_cd",   "Kia Ceed CD (2018+)",              1313, 0.30, 1.800, 1.447, 2.650, 2.2, "205/55 R16", A.LATEST, 1.28, "Cd hinnang"),
    ("suzuki_gv",     "Suzuki Grand Vitara (2005-2015)",  1660, 0.38, 1.810, 1.695, 2.640, 2.2, "225/65 R17", A.MODERN, 1.18, "Cd hinnang; raamil maastur"),

    # --- elektriautod ----------------------------------------------------
    # Elektriautode pidurdusmaa EI ole regeneratsiooni tõttu lühem:
    # hädapidurduses teeb töö ikka hõõrdpidur ja rehv. Suurem mass ei
    # pikenda seda oluliselt (a = mu*g), aga rehvikoormus on suurem.
    ("tesla_modely",  "Tesla Model Y LR AWD (2020+)",     1979, 0.23, 1.920, 1.624, 2.890, 2.9, "255/45 R19", A.LATEST, 1.30, ""),
    ("nissan_leaf_1", "Nissan Leaf I (2010-2017)",        1505, 0.28, 1.770, 1.550, 2.700, 2.5, "205/55 R16", A.MODERN, 1.26, ""),
    ("nissan_leaf_2", "Nissan Leaf II (2017+)",           1505, 0.28, 1.788, 1.530, 2.700, 2.5, "205/55 R16", A.LATEST, 1.28, ""),
    ("hyundai_ioniq5","Hyundai Ioniq 5 77 kWh (2021+)",   1905, 0.288,1.890, 1.600, 3.000, 2.5, "235/55 R19", A.LATEST, 1.30, ""),
    ("byd_sealion7",  "BYD Sealion 7 AWD (2024+)",        2340, 0.219,1.925, 1.620, 2.930, 2.5, "245/45 R20", A.LATEST, 1.28, "Cd madala usaldusega (ainult EVKX, tootja ei kinnita)"),
    ("mitsu_imiev",   "Mitsubishi i-MiEV (2009+)",        1110, 0.35, 1.475, 1.610, 2.550, 2.2, "145/65 R15", A.MODERN, 1.15, "rõhk parandatud: USA allikas andis 2,5 bar, Euroopa plaat on u 2,2 ees / 2,4 taga (ees ja taga on eri mõõt)"),

    # --- kaubikud --------------------------------------------------------
    # HOIATUS: kaubikutel EI OLE tootja Cd-d avaldatud ühelgi ja leitud
    # rõhuväärtused olid tõenäoliselt TÄISKOORMA omad. Siin on kasutatud
    # tühja sõiduki tüüpväärtusi. Kaubiku pidurdusmaa sõltub koormusest
    # palju rohkem kui sõiduautol, sest tema pidurid on koormatud
    # sõiduki jaoks projekteeritud -- tühjalt on tagatelg kergelt
    # koormatud ja lukustub varem.
    ("vw_caddy_3",    "VW Caddy III kaubik (2004-2015)",  1500, 0.36, 1.802, 1.833, 2.682, 2.5, "195/65 R15", A.MODERN, 1.12, "Cd ja rõhk hinnang"),
    ("vw_t5",         "VW Transporter T5 kaubik (2003-2015)",1950,0.36,1.904,1.959, 3.000, 2.8, "205/65 R16C", A.MODERN, 1.10, "Cd ja rõhk hinnang"),
    ("ford_transit_custom","Ford Transit Custom (2012-2023)",1990,0.36,1.986,2.000, 2.933, 2.8, "215/65 R16C", A.MODERN, 1.10, "Cd ja rõhk hinnang (leitud 3,7 bar on täiskoorma oma)"),
    ("mb_sprinter_906","Mercedes Sprinter 313 CDI (2006-2018)",2025,0.36,1.993,2.435,3.250, 3.0, "235/65 R16C", A.MODERN, 1.05, "Cd hinnang; taga 4,5 bar"),
    ("renault_master_3","Renault Master III (2010+)",     1970, 0.36, 2.070, 2.488, 4.332, 3.0, "225/65 R16C", A.MODERN, 1.05, "Cd ja rõhk hinnang"),

    # --- nõukogude pärand ------------------------------------------------
    # Neid on pargis vähe (2024. aastal võeti arvele 13 Moskvitšit), aga
    # Niva on endiselt kasutuses ja kalkulaatoris on tal õpetlik roll:
    # ABS puudub, pidurid nõrgad, raskuskese kõrge.
    ("lada_niva",     "Lada Niva / VAZ 2121 (1977+)",     1210, 0.45, 1.680, 1.640, 2.200, 1.9, "175/80 R16", A.NONE,   0.90, "Cd hinnang; rõhk sõltub mõõdust (tehase juhend 1,8 ees / 2,1 taga 175/80 R16 peal)"),
    ("lada_2110",     "VAZ 2110 (1995-2007)",             1010, 0.34, 1.676, 1.430, 2.492, 1.9, "175/70 R13", A.NONE,   0.88, "Cd hinnang"),

    # =====================================================================
    # 2026-09-17 LISATUD: margid, mida pargis on palju, aga mudelis ei olnud
    # =====================================================================
    # Valik EI OLE tehtud tunde jargi. Transpordiameti registri jargi
    # (mntstat.ee, 01.07.2026) on Eestis 674 747 soiduautot. Registri
    # mudelitasand on avalik, aga ainult JS-i taga, seega mudelivalikuks
    # kasutati auto24.ee kuulutuste arvu. Kalibreerimiseks motdeti kaks
    # teadaolevat punkti: Passat 321 kuulutust vs 20 704 registreeritud
    # (64,5 autot kuulutuse kohta) ja Golf 187 vs 16 055 (85,9). Seega
    # mainstream-mudelitel saab kuulutuste arvu korrutada u 65-85-ga.
    #
    # HOIATUS selle meetodi kohta: kuulutused motdavad KAIVET, mitte
    # omandit. Premium-margid (Porsche, Land Rover, Jaguar) on seal
    # ulehinnatud, sest nende puhul on tegu edasimuujate impordikaibega.
    # Odavad vanad prantsuse ja itaalia autod on alahinnatud.
    #
    # VANUS: ACEA utleb Eesti pargi keskmiseks ~17 aastat, aga see sisaldab
    # ~205 000 peatatud registreeringuga autot. Transpordiamet ise utleb
    # tegelikult liikuvate kohta 13 aastat, Liikluskindlustuse Fond 11,85.
    # Seega on valik kaalutud aastatele 2005-2018, mitte uutele autodele.
    #
    # ANDMED: mass, Cd, mootmed ja OEM-mot on auto-data.net-ist,
    # ultimatespecs-ist voi L'argus-ist; rohk wheel-size.com-ist,
    # tyre-pressures.com-ist voi Pure Tyre-ist. Iga vaartus, mida
    # ESMAALLIKAST EI LEITUD, on markusega "hinnang" -- neid on siin
    # rohkem kui varasemates ridades, sest need margid on kehvemini
    # dokumenteeritud.

    # --- Citroen ---------------------------------------------------------
    ("citroen_berlingo_2", "Citroën Berlingo II Multispace (2008-2018)", 1407, 0.35, 1.810, 1.801, 2.728, 2.3, "205/65 R15", A.MODERN, 1.15),
    ("citroen_c4_2",   "Citroën C4 II (2010-2018)",        1205, 0.30, 1.789, 1.489, 2.608, 2.1, "205/55 R16", A.MODERN, 1.26, "rõhk HaynesPro andmetest 2,1 bar"),
    ("citroen_c3_2",   "Citroën C3 II (2010-2016)",        1080, 0.31, 1.728, 1.524, 2.466, 2.0, "185/65 R15", A.MODERN, 1.24, "auto-data annab mõõduks 195/55 R16, HaynesPro 185/65 R15 — kasutatud levinumat"),
    ("citroen_c5_2",   "Citroën C5 II Tourer (2008-2017)", 1655, 0.30, 1.860, 1.491, 2.815, 2.3, "225/55 R17", A.MODERN, 1.26, "Cd hinnang; rõhk leitud 161 hp variandi realt, mitte 140 hp omalt"),
    ("citroen_jumpy_2", "Citroën Jumpy II kaubik (2007-2016)", 1708, 0.36, 1.895, 1.880, 3.000, 2.6, "215/60 R16C", A.MODERN, 1.08, "Cd hinnang; rõhk hinnang tühjale sõidukile — leitud 3,3/3,7 bar on täiskoorma oma"),

    # --- SEAT ------------------------------------------------------------
    ("seat_leon_3",    "SEAT Leon III (2012-2020)",        1286, 0.30, 1.816, 1.459, 2.636, 2.0, "195/65 R15", A.LATEST, 1.28, "Cd hinnang"),
    ("seat_ibiza_4",   "SEAT Ibiza IV (2008-2017)",        1170, 0.32, 1.693, 1.445, 2.469, 2.1, "185/60 R15", A.MODERN, 1.26, "Cd ja rõhk hinnang"),
    ("seat_ateca",     "SEAT Ateca (2016+)",               1300, 0.34, 1.841, 1.601, 2.638, 2.2, "215/60 R16", A.LATEST, 1.27),
    ("seat_alhambra_2", "SEAT Alhambra II (2010-2022)",    1774, 0.32, 1.904, 1.720, 2.919, 2.3, "205/60 R16", A.MODERN, 1.22, "Cd ja rõhk hinnang; mass on 5-kohalise oma, 7-kohaline on raskem"),

    # --- Opel ------------------------------------------------------------
    ("opel_insignia_a", "Opel Insignia A Sports Tourer (2008-2017)", 1610, 0.30, 1.856, 1.498, 2.737, 2.3, "215/60 R16", A.MODERN, 1.26, "Cd ja rõhk hinnang; mass 130 hp variandi oma"),
    ("opel_corsa_d",   "Opel Corsa D (2006-2014)",         1160, 0.32, 1.737, 1.488, 2.511, 2.1, "185/65 R15", A.MODERN, 1.24, "rõhk hinnang"),

    # --- Peugeot ---------------------------------------------------------
    ("peugeot_3008_1", "Peugeot 3008 I (2009-2016)",       1422, 0.33, 1.837, 1.639, 2.613, 2.4, "215/60 R16", A.MODERN, 1.24, "Cd hinnang; auto-data annab mõõduks 215/60 R16"),
    ("peugeot_308_2",  "Peugeot 308 II (2013-2021)",       1185, 0.30, 1.804, 1.457, 2.620, 2.2, "205/55 R16", A.LATEST, 1.28, "Cd ja rõhk hinnang"),
    ("peugeot_508_1",  "Peugeot 508 I SW (2011-2018)",     1500, 0.28, 1.853, 1.476, 2.817, 2.3, "215/55 R17", A.MODERN, 1.26, "laius allikate vahel vastuoluline (1853 vs 1920 mm); rõhk hinnang"),
    ("peugeot_5008_2", "Peugeot 5008 II (2017-2024)",      1430, 0.33, 1.844, 1.646, 2.840, 2.5, "215/65 R17", A.LATEST, 1.27, "Cd hinnang"),
    ("peugeot_partner_2", "Peugeot Partner II kaubik (2008-2018)", 1374, 0.36, 1.810, 1.810, 2.730, 2.4, "185/65 R15", A.MODERN, 1.10, "Cd hinnang; rõhk leitud 205/65 R15 realt"),

    # --- Lexus -----------------------------------------------------------
    ("lexus_rx_al10",  "Lexus RX 450h (2009-2015)",        2110, 0.32, 1.885, 1.685, 2.740, 2.3, "235/60 R18", A.MODERN, 1.24),
    ("lexus_nx_az10",  "Lexus NX 300h (2014-2021)",        1790, 0.34, 1.845, 1.645, 2.660, 2.2, "225/60 R18", A.LATEST, 1.26),
    ("lexus_is_xe20",  "Lexus IS 220d (2005-2013)",        1585, 0.27, 1.800, 1.425, 2.730, 2.4, "205/55 R16", A.MODERN, 1.28, "IS250 on eesmise ja tagumise eri mõõduga; siin on IS220d ühtne mõõt"),

    # --- Jeep ------------------------------------------------------------
    ("jeep_gc_wk2",    "Jeep Grand Cherokee WK2 (2010-2021)", 2272, 0.37, 1.943, 1.781, 2.915, 2.3, "265/60 R18", A.MODERN, 1.18),
    ("jeep_compass_mp", "Jeep Compass MP (2017+)",         1500, 0.35, 1.819, 1.635, 2.636, 2.3, "215/65 R16", A.LATEST, 1.24, "Cd ja rõhk hinnang; mass on kogu perekonna vahemiku keskosa"),
    ("jeep_wrangler_jk", "Jeep Wrangler JK Unlimited (2007-2018)", 1980, 0.495, 1.877, 1.834, 2.946, 1.8, "255/75 R17", A.MODERN, 1.05, "raamil maastur, kõrge raskuskese"),

    # --- Land Rover ------------------------------------------------------
    ("lr_rrs_l320",    "Range Rover Sport L320 (2005-2013)", 2535, 0.40, 2.004, 1.784, 2.745, 2.3, "255/50 R19", A.MODERN, 1.12, "Cd hinnang; laius on peeglitega kokkupandud mõõt, seega CdA pisut ülehinnatud; mass HSE-varustuse oma"),
    ("lr_disco_sport", "Land Rover Discovery Sport (2014-2019)", 1785, 0.38, 2.069, 1.724, 2.741, 2.4, "235/65 R17", A.LATEST, 1.20, "Cd hinnang; laius peeglitega kokkupandud; mõõt allikate vahel 235 vs 225; rõhk eD4 realt"),
    ("lr_freelander_2", "Land Rover Freelander 2 (2006-2014)", 1770, 0.38, 1.910, 1.740, 2.660, 2.2, "215/75 R16", A.MODERN, 1.18, "Cd hinnang"),

    # --- Porsche ---------------------------------------------------------
    ("porsche_cayenne_958", "Porsche Cayenne Diesel (2010-2017)", 2100, 0.36, 1.939, 1.705, 2.895, 2.4, "255/55 R18", A.LATEST, 1.28),
    ("porsche_macan_95b", "Porsche Macan S Diesel (2013+)", 1880, 0.35, 1.923, 1.624, 2.807, 2.3, "235/60 R18", A.LATEST, 1.30, "tehasel on ees ja taga eri mõõt (235/60 R18 ees, 255/55 R18 taga); mudel kasutab esimõõtu"),

    # --- MINI ------------------------------------------------------------
    ("mini_r56",       "MINI Cooper D R56 (2007-2016)",    1090, 0.32, 1.683, 1.407, 2.467, 2.4, "175/65 R15", A.MODERN, 1.30),
    ("mini_countryman_r60", "MINI Countryman R60 (2010-2016)", 1310, 0.36, 1.789, 1.561, 2.595, 2.2, "205/60 R16", A.MODERN, 1.26),

    # --- Fiat ------------------------------------------------------------
    ("fiat_500_312",   "Fiat 500 (2007-2015)",             865, 0.325, 1.627, 1.488, 2.300, 2.3, "175/65 R14", A.MODERN, 1.22),
    ("fiat_doblo_2",   "Fiat Doblò II (2010-2022)",        1430, 0.36, 1.832, 1.845, 2.755, 2.5, "185/65 R15", A.MODERN, 1.12, "Cd hinnang"),
    ("fiat_ducato_3",  "Fiat Ducato III kaubik L2H2 (2006+)", 2000, 0.36, 2.050, 2.520, 3.450, 2.8, "215/70 R15C", A.MODERN, 1.05, "Cd hinnang; rõhk hinnang tühjale sõidukile — leitud 4,0 bar on täiskoorma oma"),

    # --- Saab ------------------------------------------------------------
    ("saab_93_2",      "Saab 9-3 II SportCombi (2002-2014)", 1535, 0.30, 1.782, 1.507, 2.675, 2.4, "215/55 R16", A.MODERN, 1.24, "Cd hinnang"),
    ("saab_95_1",      "Saab 9-5 I universaal (1997-2010)", 1510, 0.31, 1.792, 1.497, 2.705, 2.1, "205/65 R15", A.EARLY, 1.20, "mass on EL-i kaal koos juhiga, u 75 kg kõrgem kui teistel ridadel"),

    # --- muud ------------------------------------------------------------
    ("alfa_giulietta", "Alfa Romeo Giulietta (2010-2020)", 1395, 0.31, 1.798, 1.465, 2.634, 2.3, "205/55 R16", A.MODERN, 1.28),
    ("chevrolet_captiva", "Chevrolet Captiva (2006-2018)", 1770, 0.38, 1.850, 1.720, 2.705, 2.3, "235/60 R17", A.MODERN, 1.18, "rõhk hinnang"),
    ("chevrolet_cruze", "Chevrolet Cruze (2009-2016)",     1500, 0.31, 1.788, 1.477, 2.685, 2.4, "205/60 R16", A.MODERN, 1.24, "mass EL-i kaal koos juhiga; rõhk 215/60 R16 realt"),
    ("ssangyong_rexton", "SsangYong Rexton (2006-2012)",   1986, 0.40, 1.870, 1.830, 2.820, 2.3, "235/70 R16", A.MODERN, 1.10, "Cd ja rõhk hinnang; raamil maastur"),
    ("jaguar_xf_x250", "Jaguar XF 2.2d (2008-2015)",       1735, 0.29, 1.939, 1.468, 2.909, 2.3, "245/45 R18", A.MODERN, 1.28, "Cd hinnang"),
    ("dacia_sandero_2", "Dacia Sandero II (2012-2020)",     962, 0.35, 1.733, 1.523, 2.589, 2.4, "185/65 R15", A.MODERN, 1.22, "Cd hinnang"),
    ("polestar_2",     "Polestar 2 Long Range (2020+)",    2009, 0.278, 1.859, 1.479, 2.735, 2.8, "245/45 R19", A.LATEST, 1.30),
    ("mg4_ev",         "MG4 EV 64 kWh (2022+)",            1685, 0.29, 1.836, 1.504, 2.705, 2.6, "215/55 R17", A.LATEST, 1.28, "Cd hinnang"),

    # =====================================================================
    # 2026-09-18: TAVALISED PEREAUTOD
    # =====================================================================
    # Need on autod, mida Eesti pered päriselt endale lubada saavad --
    # vanemad Passatid ja Octaviad, E- ja C-klassi Mersud, pere-mahtukad.
    # Valik on tehtud tavateadmise järgi, MITTE registriuuringuga.
    #
    # AUS VAHE VARASEMATE RIDADEGA. Ülalolevate ridade mõõdud tulevad
    # spetsifikatsioonilehtedelt (auto-data.net, ultimatespecs, L'argus).
    # Siinsed mass-, Cd- ja mõõdunumbrid on LIGIKAUDSED ega ole
    # esmaallikast kontrollitud. Iga rida kannab märkust "mõõdud
    # ligikaudsed", et seda saaks hiljem eristada ja üle kontrollida.
    #
    # MIKS SEE ON OK. Auditi tundlikkusanalüüs ütleb, et tühimassi 160 kg
    # viga muudab vastust alla promilli ja Cd annab 130 km/h juures 1-2 %.
    # Need EI OLE numbrid, mille pärast vastus valeks läheb.
    # See, mis PEAB õige olema, on ABS-i põlvkond -- ja see tuleb
    # mudeliaastast, mida ma tean kindlalt. Rehvimõõt on samuti teada,
    # sest need on väga levinud autod.
    ("skoda_octavia_1", "Škoda Octavia I 1.9 TDI (1996-2010)", 1250, 0.32, 1.731, 1.439, 2.512, 2.2, "195/65 R15", A.EARLY, 1.22, "mõõdud ligikaudsed"),
    ("skoda_superb_2",  "Škoda Superb II 2.0 TDI (2008-2015)", 1490, 0.30, 1.817, 1.462, 2.761, 2.4, "205/55 R16", A.MODERN, 1.28, "mõõdud ligikaudsed"),
    ("skoda_yeti",      "Škoda Yeti 2.0 TDI (2009-2017)",      1450, 0.36, 1.793, 1.691, 2.578, 2.3, "215/60 R16", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("vw_sharan_1",     "VW Sharan I 1.9 TDI (1995-2010)",     1700, 0.33, 1.810, 1.759, 2.841, 2.4, "205/60 R15", A.EARLY, 1.18, "mõõdud ligikaudsed"),
    ("vw_bora",         "VW Bora 1.9 TDI (1998-2005)",         1290, 0.31, 1.735, 1.446, 2.513, 2.3, "195/65 R15", A.EARLY, 1.24, "mõõdud ligikaudsed"),
    ("audi_a3_8p",      "Audi A3 8P 2.0 TDI (2003-2012)",      1340, 0.32, 1.765, 1.421, 2.578, 2.3, "205/55 R16", A.MODERN, 1.28, "mõõdud ligikaudsed"),
    ("audi_a4_b5",      "Audi A4 B5 1.9 TDI (1994-2001)",      1320, 0.30, 1.733, 1.415, 2.617, 2.3, "195/65 R15", A.EARLY, 1.24, "mõõdud ligikaudsed"),
    ("mb_c220_w205",    "Mercedes C220 d W205 (2014-2021)",    1545, 0.24, 1.810, 1.442, 2.840, 2.4, "205/60 R16", A.LATEST, 1.30, "mõõdud ligikaudsed"),
    ("mb_e220_w213",    "Mercedes E220 d W213 (2016-2023)",    1680, 0.23, 1.852, 1.468, 2.939, 2.5, "225/55 R17", A.LATEST, 1.32, "mõõdud ligikaudsed"),
    ("mb_b180_w245",    "Mercedes B180 CDI W245 (2005-2011)",  1395, 0.31, 1.777, 1.603, 2.778, 2.4, "195/65 R15", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("mb_a170_w169",    "Mercedes A-klass W169 (2004-2012)",   1245, 0.32, 1.764, 1.595, 2.568, 2.3, "185/65 R15", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("opel_astra_g",    "Opel Astra G (1998-2009)",            1180, 0.32, 1.709, 1.425, 2.606, 2.2, "185/65 R15", A.EARLY, 1.22, "mõõdud ligikaudsed"),
    ("opel_vectra_b",   "Opel Vectra B (1995-2002)",           1290, 0.31, 1.707, 1.425, 2.637, 2.3, "195/65 R15", A.EARLY, 1.22, "mõõdud ligikaudsed"),
    ("opel_zafira_a",   "Opel Zafira A (1999-2005)",           1420, 0.33, 1.742, 1.684, 2.694, 2.4, "195/65 R15", A.EARLY, 1.20, "mõõdud ligikaudsed"),
    ("ford_mondeo_3",   "Ford Mondeo III (2000-2007)",         1400, 0.30, 1.812, 1.429, 2.754, 2.3, "205/55 R16", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("ford_focus_1",    "Ford Focus I (1998-2004)",            1150, 0.32, 1.699, 1.430, 2.615, 2.2, "195/60 R15", A.EARLY, 1.24, "mõõdud ligikaudsed"),
    ("ford_fiesta_6",   "Ford Fiesta VI (2008-2017)",          1045, 0.33, 1.722, 1.481, 2.489, 2.2, "175/65 R14", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("ford_galaxy_2",   "Ford Galaxy II (2006-2015)",          1750, 0.31, 1.884, 1.746, 2.850, 2.5, "215/60 R16", A.MODERN, 1.20, "mõõdud ligikaudsed"),
    ("toyota_avensis_t22","Toyota Avensis T22 (1997-2003)",    1280, 0.30, 1.710, 1.430, 2.630, 2.2, "195/60 R15", A.EARLY, 1.24, "mõõdud ligikaudsed"),
    ("toyota_corolla_e110","Toyota Corolla E110 (1997-2002)",  1090, 0.31, 1.690, 1.400, 2.465, 2.2, "175/65 R14", A.EARLY, 1.22, "mõõdud ligikaudsed"),
    ("toyota_verso",    "Toyota Verso (2009-2018)",            1495, 0.31, 1.790, 1.620, 2.780, 2.4, "205/60 R16", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("nissan_almera_n16","Nissan Almera N16 (2000-2006)",      1160, 0.32, 1.706, 1.460, 2.535, 2.2, "185/65 R15", A.EARLY, 1.22, "mõõdud ligikaudsed"),
    ("nissan_primera_p12","Nissan Primera P12 (2002-2008)",    1360, 0.29, 1.760, 1.482, 2.680, 2.3, "205/60 R16", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("renault_scenic_2","Renault Scénic II (2003-2009)",       1385, 0.34, 1.810, 1.620, 2.685, 2.3, "205/60 R16", A.MODERN, 1.22, "mõõdud ligikaudsed"),
    ("peugeot_407",     "Peugeot 407 (2004-2011)",             1510, 0.29, 1.811, 1.445, 2.725, 2.4, "205/60 R16", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("honda_accord_7",  "Honda Accord VII (2002-2008)",        1420, 0.28, 1.760, 1.450, 2.670, 2.3, "205/55 R16", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("mazda_6_gg",      "Mazda 6 GG (2002-2008)",              1370, 0.29, 1.780, 1.440, 2.675, 2.3, "205/55 R16", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("hyundai_santafe_cm","Hyundai Santa Fe CM (2006-2012)",   1750, 0.37, 1.890, 1.725, 2.700, 2.3, "235/60 R18", A.MODERN, 1.20, "mõõdud ligikaudsed"),
    ("kia_ceed_ed",     "Kia Cee'd ED (2006-2012)",            1300, 0.32, 1.790, 1.480, 2.650, 2.3, "195/65 R15", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("mitsu_lancer_9",  "Mitsubishi Lancer IX (2003-2007)",    1240, 0.31, 1.695, 1.445, 2.600, 2.2, "195/60 R15", A.MODERN, 1.24, "mõõdud ligikaudsed"),

    # =====================================================================
    # 2026-09-18, teine ring: veel tavalisi Eesti autosid
    # =====================================================================
    # Sama reegel mis eelmisel plokil: mõõdud on ligikaudsed ja märkusega,
    # ABS-i põlvkond ja rehvimõõt on kindlad. Vt faili päist.
    #
    # --- kaubikud ja pere-mahtukad, mida Eestis palju sõidetakse --------
    ("mb_vito_w639",   "Mercedes Vito W639 (2003-2014)",      1900, 0.36, 1.901, 1.875, 3.200, 2.7, "205/65 R16C", A.MODERN, 1.08, "mõõdud ligikaudsed"),
    ("chrysler_voyager_4","Chrysler Grand Voyager (2001-2007)",1950, 0.36, 1.998, 1.750, 3.030, 2.4, "215/65 R16", A.MODERN, 1.10, "mõõdud ligikaudsed"),
    ("renault_kangoo_2","Renault Kangoo II (2008-2021)",      1320, 0.36, 1.829, 1.818, 2.697, 2.4, "195/65 R15", A.MODERN, 1.12, "mõõdud ligikaudsed"),
    ("renault_trafic_2","Renault Trafic II (2001-2014)",      1700, 0.36, 1.904, 1.971, 3.098, 2.7, "195/65 R16C", A.MODERN, 1.08, "mõõdud ligikaudsed"),
    ("vw_caddy_4",     "VW Caddy IV (2015-2020)",             1450, 0.36, 1.793, 1.822, 2.681, 2.5, "195/65 R15", A.LATEST, 1.14, "mõõdud ligikaudsed"),
    ("ford_connect_1", "Ford Transit Connect (2002-2013)",    1450, 0.36, 1.795, 1.814, 2.664, 2.5, "195/65 R15", A.MODERN, 1.10, "mõõdud ligikaudsed"),
    ("opel_vivaro_a",  "Opel Vivaro A kaubik (2001-2014)",    1700, 0.36, 1.904, 1.971, 3.098, 2.7, "205/65 R16C", A.MODERN, 1.08, "mõõdud ligikaudsed"),
    ("peugeot_boxer_3","Peugeot Boxer kaubik (2006+)",        1960, 0.36, 2.050, 2.520, 3.450, 2.8, "215/70 R15C", A.MODERN, 1.05, "mõõdud ligikaudsed"),

    # --- levinud sõiduautod ja väikemaasturid ---------------------------
    ("toyota_prius_xw30","Toyota Prius XW30 (2009-2015)",     1380, 0.25, 1.745, 1.490, 2.700, 2.4, "195/65 R15", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("nissan_xtrail_t31","Nissan X-Trail T31 (2007-2013)",    1520, 0.36, 1.785, 1.685, 2.630, 2.3, "215/60 R17", A.MODERN, 1.22, "mõõdud ligikaudsed"),
    ("ford_kuga_2",    "Ford Kuga II (2012-2019)",            1610, 0.34, 1.838, 1.689, 2.690, 2.4, "235/55 R17", A.LATEST, 1.24, "mõõdud ligikaudsed"),
    ("ford_cmax_1",    "Ford C-Max I (2003-2010)",            1350, 0.32, 1.825, 1.585, 2.640, 2.3, "205/55 R16", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("hyundai_i30_1",  "Hyundai i30 I (2007-2012)",           1280, 0.32, 1.775, 1.480, 2.650, 2.3, "195/65 R15", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("hyundai_ix35",   "Hyundai ix35 (2010-2015)",            1520, 0.35, 1.820, 1.655, 2.640, 2.3, "225/60 R17", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("kia_sorento_2",  "Kia Sorento II (2009-2014)",          1830, 0.37, 1.885, 1.700, 2.700, 2.3, "235/65 R17", A.MODERN, 1.20, "mõõdud ligikaudsed"),
    ("kia_rio_3",      "Kia Rio III (2011-2017)",             1120, 0.31, 1.720, 1.455, 2.570, 2.2, "185/65 R15", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("mazda_5_cr",     "Mazda 5 (2005-2015)",                 1470, 0.30, 1.755, 1.615, 2.750, 2.3, "205/55 R16", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("mazda_3_bl",     "Mazda 3 BL (2009-2013)",              1290, 0.30, 1.755, 1.470, 2.640, 2.3, "205/55 R16", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("volvo_s80_2",    "Volvo S80 II (2006-2016)",            1620, 0.28, 1.861, 1.493, 2.835, 2.4, "225/50 R17", A.MODERN, 1.28, "mõõdud ligikaudsed"),
    ("volvo_xc70_3",   "Volvo XC70 III (2007-2016)",          1750, 0.33, 1.861, 1.604, 2.815, 2.4, "235/55 R17", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("volvo_v40_2",    "Volvo V40 II (2012-2019)",            1400, 0.29, 1.802, 1.445, 2.647, 2.4, "205/55 R16", A.LATEST, 1.28, "mõõdud ligikaudsed"),
    ("subaru_impreza_gd","Subaru Impreza GD (2000-2007)",     1290, 0.33, 1.730, 1.440, 2.525, 2.3, "195/60 R15", A.EARLY, 1.26, "mõõdud ligikaudsed"),
    ("mitsu_asx",      "Mitsubishi ASX (2010-2022)",          1410, 0.34, 1.770, 1.625, 2.670, 2.3, "215/60 R17", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("mitsu_colt_6",   "Mitsubishi Colt (2004-2012)",         1000, 0.33, 1.695, 1.550, 2.500, 2.2, "175/65 R14", A.MODERN, 1.22, "mõõdud ligikaudsed"),
    ("suzuki_swift_3", "Suzuki Swift (2005-2010)",            1030, 0.34, 1.690, 1.500, 2.380, 2.2, "185/60 R15", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("suzuki_sx4_1",   "Suzuki SX4 (2006-2014)",              1200, 0.36, 1.755, 1.590, 2.500, 2.3, "205/60 R16", A.MODERN, 1.22, "mõõdud ligikaudsed"),
    ("opel_meriva_b",  "Opel Meriva B (2010-2017)",           1350, 0.33, 1.812, 1.615, 2.644, 2.3, "205/55 R16", A.MODERN, 1.22, "mõõdud ligikaudsed"),
    ("opel_antara",    "Opel Antara (2006-2015)",             1770, 0.38, 1.850, 1.704, 2.707, 2.3, "235/60 R17", A.MODERN, 1.18, "mõõdud ligikaudsed"),
    ("skoda_roomster", "Škoda Roomster (2006-2015)",          1190, 0.35, 1.684, 1.607, 2.617, 2.3, "185/60 R15", A.MODERN, 1.22, "mõõdud ligikaudsed"),
    ("skoda_rapid",    "Škoda Rapid (2012-2019)",             1140, 0.31, 1.706, 1.461, 2.602, 2.2, "185/60 R15", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("bmw_118d_e87",   "BMW 118d E87 (2004-2011)",            1360, 0.31, 1.748, 1.430, 2.660, 2.3, "195/55 R16", A.MODERN, 1.30, "mõõdud ligikaudsed"),
    ("bmw_x1_e84",     "BMW X1 E84 (2009-2015)",              1545, 0.32, 1.798, 1.545, 2.760, 2.4, "225/50 R17", A.MODERN, 1.26, "mõõdud ligikaudsed"),
    ("audi_q7_4l",     "Audi Q7 4L (2005-2015)",              2240, 0.37, 1.983, 1.737, 3.002, 2.5, "235/60 R18", A.MODERN, 1.18, "mõõdud ligikaudsed"),
    ("audi_a5_8t",     "Audi A5 8T (2007-2016)",              1520, 0.30, 1.854, 1.372, 2.751, 2.4, "225/50 R17", A.MODERN, 1.30, "mõõdud ligikaudsed"),
    ("mb_ml_w164",     "Mercedes ML W164 (2005-2011)",        2100, 0.34, 1.911, 1.815, 2.915, 2.4, "255/55 R18", A.MODERN, 1.20, "mõõdud ligikaudsed"),
    ("vw_touareg_1",   "VW Touareg I (2002-2010)",            2300, 0.38, 1.928, 1.726, 2.855, 2.4, "235/65 R17", A.MODERN, 1.18, "mõõdud ligikaudsed"),
    ("peugeot_307",    "Peugeot 307 (2001-2008)",             1250, 0.31, 1.746, 1.510, 2.608, 2.3, "195/65 R15", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("citroen_xsara_picasso","Citroën Xsara Picasso (1999-2010)",1280,0.33,1.751,1.637,2.760,2.3,"185/65 R15",A.EARLY,1.20,"mõõdud ligikaudsed"),
    ("toyota_aygo_1",  "Toyota Aygo (2005-2014)",              845, 0.32, 1.615, 1.465, 2.340, 2.2, "155/65 R14", A.MODERN, 1.22, "mõõdud ligikaudsed"),
    ("nissan_note_e11","Nissan Note E11 (2006-2013)",         1150, 0.33, 1.690, 1.550, 2.600, 2.2, "185/65 R15", A.MODERN, 1.22, "mõõdud ligikaudsed"),
    ("honda_jazz_2",   "Honda Jazz II (2008-2015)",           1090, 0.33, 1.695, 1.525, 2.500, 2.2, "175/65 R15", A.MODERN, 1.24, "mõõdud ligikaudsed"),
    ("chevrolet_lacetti","Chevrolet Lacetti (2004-2011)",     1230, 0.33, 1.725, 1.445, 2.600, 2.2, "185/65 R14", A.MODERN, 1.22, "mõõdud ligikaudsed"),
]

# otsapindala lähend: A = k * laius * kõrgus. k = 0,83 on autotööstuses
# levinud väärtus (arvestab, et keretsoon ei ole täisristkülik).
FRONTAL_AREA_K = 0.83

# ---------------------------------------------------------------------------
# 2026-09-22 KOLMAS RING: laiem pargi katvus (~150 mudelipõlvkonda).
# Kõik read on "mõõdud ligikaudsed": mudeliaasta, ABS-i põlvkond (vt
# reegel ülal) ja levinuim tehase rehvimõõt on teada; mass, Cd, mõõtmed ja
# rõhk on suurusjärk. Sama põhjendus mis teisel ringil: pidurdusmaa jaoks
# loeb peamiselt ABS-i põlvkond ja rehv — tühimassi 160 kg viga muudab
# vastust alla promilli (audit.py tundlikkus). Rehvimõõt on BAASVARUSTUSE
# oma; kallimatel versioonidel on sageli suurem velg ja kasutaja saab
# mõõdu valikust ise muuta.
# ---------------------------------------------------------------------------
_L = "mõõdud ligikaudsed"
EE_VEHICLES += [
    # --- Volkswagen -------------------------------------------------------
    ("vw_up",          "VW up! (2011-2023)",                   930, 0.32, 1.641, 1.489, 2.420, 2.2, "165/70 R14", A.MODERN, 1.22, _L),
    ("vw_polo_4",      "VW Polo IV 1.4 (2001-2009)",          1100, 0.32, 1.650, 1.465, 2.460, 2.2, "185/60 R14", A.MODERN, 1.22, _L),
    ("vw_polo_6",      "VW Polo VI 1.0 TSI (2017+)",          1150, 0.30, 1.751, 1.461, 2.564, 2.3, "185/65 R15", A.LATEST, 1.28, _L),
    ("vw_jetta_6",     "VW Jetta VI 1.6 TDI (2010-2018)",     1350, 0.30, 1.778, 1.453, 2.651, 2.3, "205/55 R16", A.MODERN, 1.28, _L),
    ("vw_golf_plus",   "VW Golf Plus 1.6 (2005-2014)",        1320, 0.32, 1.759, 1.580, 2.578, 2.3, "195/65 R15", A.MODERN, 1.26, _L),
    ("vw_arteon",      "VW Arteon 2.0 TDI (2017-2024)",       1580, 0.27, 1.871, 1.450, 2.837, 2.5, "245/45 R18", A.LATEST, 1.32, _L),
    ("vw_touran_2",    "VW Touran II 2.0 TDI (2015-2025)",    1500, 0.31, 1.829, 1.628, 2.786, 2.4, "205/60 R16", A.LATEST, 1.28, _L),
    ("vw_sharan_2",    "VW Sharan II 2.0 TDI (2010-2022)",    1720, 0.30, 1.904, 1.720, 2.919, 2.5, "205/60 R16", A.MODERN, 1.26, _L),
    ("vw_tcross",      "VW T-Cross 1.0 TSI (2019+)",          1250, 0.32, 1.760, 1.584, 2.551, 2.3, "205/60 R16", A.LATEST, 1.26, _L),
    ("vw_tiguan_3",    "VW Tiguan III 1.5 eTSI (2024+)",      1600, 0.30, 1.859, 1.639, 2.680, 2.5, "235/55 R18", A.LATEST, 1.30, _L),
    ("vw_touareg_2",   "VW Touareg II 3.0 TDI (2010-2018)",   2150, 0.35, 1.940, 1.709, 2.893, 2.5, "255/55 R18", A.MODERN, 1.22, _L),
    ("vw_id3",         "VW ID.3 Pro (2020+)",              1800, 0.27, 1.809, 1.568, 2.771, 2.6, "215/55 R18", A.LATEST, 1.26, _L),
    ("vw_id4",         "VW ID.4 Pro (2021+)",              2120, 0.28, 1.852, 1.631, 2.765, 2.7, "235/60 R18", A.LATEST, 1.24, _L),
    ("vw_caddy_5",     "VW Caddy V (2020+)",                  1550, 0.31, 1.855, 1.826, 2.755, 2.5, "205/60 R16", A.LATEST, 1.24, _L),
    ("vw_t4",          "VW Transporter T4 2.5 TDI (1990-2003)",1800,0.38, 1.840, 1.940, 2.920, 3.0, "195/70 R15C", A.EARLY, 1.14, _L),
    ("vw_crafter_2",   "VW Crafter II kaubik (2017+)",        2150, 0.36, 2.040, 2.590, 3.640, 3.5, "235/65 R16C", A.LATEST, 1.12, _L),

    # --- Škoda ------------------------------------------------------------
    ("skoda_citigo",   "Škoda Citigo (2011-2020)",             930, 0.32, 1.645, 1.478, 2.420, 2.2, "165/70 R14", A.MODERN, 1.22, _L),
    ("skoda_fabia_1",  "Škoda Fabia I (1999-2007)",           1080, 0.32, 1.646, 1.451, 2.462, 2.2, "165/70 R14", A.EARLY, 1.20, _L),
    ("skoda_fabia_4",  "Škoda Fabia IV 1.0 TSI (2021+)",      1150, 0.28, 1.780, 1.460, 2.564, 2.3, "185/65 R15", A.LATEST, 1.28, _L),
    ("skoda_scala",    "Škoda Scala 1.0 TSI (2019+)",         1220, 0.29, 1.793, 1.471, 2.649, 2.3, "205/55 R16", A.LATEST, 1.28, _L),
    ("skoda_karoq",    "Škoda Karoq 1.5 TSI (2017+)",         1400, 0.32, 1.841, 1.603, 2.638, 2.4, "215/55 R17", A.LATEST, 1.28, _L),
    ("skoda_superb_1", "Škoda Superb I 1.9 TDI (2001-2008)",  1430, 0.30, 1.765, 1.469, 2.803, 2.3, "205/55 R16", A.EARLY, 1.24, _L),
    ("skoda_enyaq",    "Škoda Enyaq iV (2021+)",              2090, 0.26, 1.879, 1.616, 2.765, 2.7, "235/55 R19", A.LATEST, 1.24, _L),

    # --- Audi -------------------------------------------------------------
    ("audi_a1_8x",     "Audi A1 8X (2010-2018)",              1150, 0.32, 1.740, 1.416, 2.469, 2.3, "185/60 R15", A.MODERN, 1.28, _L),
    ("audi_a3_8v",     "Audi A3 8V 1.6 TDI (2012-2020)",      1280, 0.30, 1.785, 1.421, 2.601, 2.4, "205/55 R16", A.LATEST, 1.30, _L),
    ("audi_a4_b9",     "Audi A4 B9 2.0 TDI (2015-2024)",      1480, 0.27, 1.842, 1.427, 2.820, 2.4, "205/60 R16", A.LATEST, 1.30, _L),
    ("audi_a6_c8",     "Audi A6 C8 2.0 TDI (2018+)",           1680, 0.26, 1.886, 1.457, 2.924, 2.5, "225/55 R18", A.LATEST, 1.32, _L),
    ("audi_a6_c4",     "Audi A6 C4 2.5 TDI (1994-1997)",      1450, 0.29, 1.783, 1.431, 2.687, 2.3, "195/65 R15", A.EARLY, 1.20, _L),
    ("audi_q3_8u",     "Audi Q3 8U 2.0 TDI (2011-2018)",      1570, 0.32, 1.831, 1.608, 2.603, 2.4, "215/65 R16", A.MODERN, 1.26, _L),
    ("audi_q3_f3",     "Audi Q3 F3 1.5 TFSI (2018+)",          1500, 0.31, 1.849, 1.585, 2.680, 2.4, "215/65 R17", A.LATEST, 1.28, _L),
    ("audi_q5_8r",     "Audi Q5 8R 2.0 TDI (2008-2016)",      1800, 0.33, 1.880, 1.653, 2.807, 2.4, "235/65 R17", A.MODERN, 1.24, _L),
    ("audi_q7_4m",     "Audi Q7 4M 3.0 TDI (2015+)",          2070, 0.33, 1.968, 1.741, 2.994, 2.6, "255/60 R18", A.LATEST, 1.24, _L),
    ("audi_etron",     "Audi e-tron 55 (2019-2022)",          2490, 0.28, 1.935, 1.629, 2.928, 2.8, "255/55 R19", A.LATEST, 1.22, _L),

    # --- BMW --------------------------------------------------------------
    ("bmw_116d_f20",   "BMW 116d F20 (2011-2019)",            1400, 0.29, 1.765, 1.440, 2.690, 2.3, "205/55 R16", A.LATEST, 1.30, _L),
    ("bmw_118i_f40",   "BMW 118i F40 (2019+)",                1360, 0.29, 1.799, 1.434, 2.670, 2.4, "205/55 R16", A.LATEST, 1.30, _L),
    ("bmw_218d_f45",   "BMW 218d Active Tourer F45 (2014-2021)",1450,0.26,1.800,1.555, 2.670, 2.4, "205/60 R16", A.LATEST, 1.30, _L),
    ("bmw_316i_e36",   "BMW 316i E36 (1990-2000)",            1200, 0.31, 1.698, 1.393, 2.700, 2.2, "185/65 R15", A.EARLY, 1.22, _L),
    ("bmw_320d_e46",   "BMW 320d E46 (1998-2006)",            1450, 0.30, 1.739, 1.415, 2.725, 2.2, "205/55 R16", A.EARLY, 1.26, _L),
    ("bmw_530d_g60",   "BMW 520d G60 (2023+)",                1850, 0.23, 1.900, 1.515, 2.995, 2.6, "225/55 R18", A.LATEST, 1.32, _L),
    ("bmw_x1_f48",     "BMW X1 sDrive18d F48 (2015-2022)",    1575, 0.29, 1.821, 1.598, 2.670, 2.4, "225/55 R17", A.LATEST, 1.28, _L),
    ("bmw_x3_g01",     "BMW X3 xDrive20d G01 (2017-2024)",    1820, 0.29, 1.891, 1.676, 2.864, 2.5, "225/60 R18", A.LATEST, 1.28, _L),
    ("bmw_x5_f15",     "BMW X5 xDrive30d F15 (2013-2018)",    2070, 0.31, 1.938, 1.762, 2.933, 2.5, "255/55 R18", A.LATEST, 1.24, _L),
    ("bmw_x5_g05",     "BMW X5 xDrive30d G05 (2018+)",        2140, 0.33, 2.004, 1.745, 2.975, 2.6, "265/50 R19", A.LATEST, 1.26, _L),
    ("bmw_i3",         "BMW i3 (2013-2022)",                  1250, 0.29, 1.775, 1.578, 2.570, 2.4, "155/70 R19", A.LATEST, 1.24, _L),

    # --- Mercedes-Benz ----------------------------------------------------
    ("mb_a180_w176",   "Mercedes A180 W176 (2012-2018)",      1370, 0.27, 1.780, 1.433, 2.699, 2.4, "205/55 R16", A.LATEST, 1.30, _L),
    ("mb_a180_w177",   "Mercedes A180 W177 (2018+)",          1360, 0.25, 1.796, 1.440, 2.729, 2.4, "205/60 R16", A.LATEST, 1.30, _L),
    ("mb_b180_w246",   "Mercedes B180 W246 (2011-2018)",      1400, 0.26, 1.786, 1.557, 2.699, 2.4, "205/55 R16", A.LATEST, 1.28, _L),
    ("mb_c200_w206",   "Mercedes C200 W206 (2021+)",          1640, 0.24, 1.820, 1.438, 2.865, 2.5, "225/50 R17", A.LATEST, 1.32, _L),
    ("mb_c220_w202",   "Mercedes C220 CDI W202 (1993-2000)",  1400, 0.31, 1.720, 1.420, 2.690, 2.2, "195/65 R15", A.EARLY, 1.24, _L),
    ("mb_gla_x156",    "Mercedes GLA 200 X156 (2013-2019)",   1450, 0.29, 1.804, 1.494, 2.699, 2.4, "215/60 R17", A.LATEST, 1.28, _L),
    ("mb_glc_x253",    "Mercedes GLC 220 d X253 (2015-2022)", 1845, 0.31, 1.890, 1.639, 2.873, 2.5, "235/60 R18", A.LATEST, 1.28, _L),
    ("mb_ml_w166",     "Mercedes ML 250 W166 (2011-2015)",    2175, 0.32, 1.926, 1.796, 2.915, 2.5, "235/65 R17", A.LATEST, 1.24, _L),
    ("mb_gle_w167",    "Mercedes GLE 350 d W167 (2019+)",     2200, 0.29, 2.018, 1.772, 2.995, 2.6, "255/50 R19", A.LATEST, 1.26, _L),
    ("mb_s_w221",      "Mercedes S350 W221 (2005-2013)",      1880, 0.27, 1.871, 1.473, 3.035, 2.5, "235/55 R17", A.MODERN, 1.30, _L),
    ("mb_vito_w447",   "Mercedes Vito W447 (2014+)",          1900, 0.33, 1.928, 1.910, 3.200, 3.0, "205/65 R16C", A.LATEST, 1.18, _L),
    ("mb_sprinter_907","Mercedes Sprinter 907 (2018+)",       2100, 0.36, 2.020, 2.590, 3.665, 3.5, "235/65 R16C", A.LATEST, 1.12, _L),

    # --- Toyota / Lexus ---------------------------------------------------
    ("toyota_yaris_xp90","Toyota Yaris XP90 (2005-2011)",     1000, 0.30, 1.695, 1.530, 2.460, 2.3, "175/65 R14", A.MODERN, 1.24, _L),
    ("toyota_corolla_e150","Toyota Corolla E150 (2006-2013)", 1260, 0.29, 1.760, 1.470, 2.600, 2.3, "195/65 R15", A.MODERN, 1.26, _L),
    ("toyota_corolla_e170","Toyota Corolla E170 (2013-2019)", 1280, 0.28, 1.776, 1.465, 2.700, 2.3, "205/55 R16", A.LATEST, 1.28, _L),
    ("toyota_prius_xw50","Toyota Prius XW50 (2015-2022)",     1380, 0.24, 1.760, 1.470, 2.700, 2.5, "195/65 R15", A.LATEST, 1.26, _L),
    ("toyota_chr_2",   "Toyota C-HR II Hybrid (2023+)",       1450, 0.31, 1.832, 1.564, 2.640, 2.4, "225/50 R18", A.LATEST, 1.28, _L),
    ("toyota_rav4_3",  "Toyota RAV4 III (2006-2012)",         1500, 0.35, 1.815, 1.685, 2.560, 2.2, "225/65 R17", A.MODERN, 1.22, _L),
    ("toyota_lc150",   "Toyota Land Cruiser 150 (2009-2023)", 2300, 0.38, 1.885, 1.890, 2.790, 2.3, "265/65 R17", A.LATEST, 1.16, _L),
    ("toyota_hilux_7", "Toyota Hilux AN10 (2005-2015)",       1900, 0.42, 1.835, 1.810, 3.085, 2.3, "255/70 R15", A.MODERN, 1.12, _L),
    ("toyota_hilux_8", "Toyota Hilux AN120 (2015+)",          2050, 0.42, 1.855, 1.815, 3.085, 2.4, "265/65 R17", A.LATEST, 1.14, _L),
    ("toyota_proace",  "Toyota Proace II (2016+)",            1700, 0.34, 1.920, 1.900, 3.275, 3.0, "215/65 R16", A.LATEST, 1.18, _L),
    ("lexus_rx_al20",  "Lexus RX 450h AL20 (2015-2022)",      2100, 0.33, 1.895, 1.710, 2.790, 2.3, "235/65 R18", A.LATEST, 1.26, _L),
    ("lexus_ux",       "Lexus UX 250h (2018+)",               1540, 0.33, 1.840, 1.545, 2.640, 2.4, "215/60 R17", A.LATEST, 1.28, _L),
    ("lexus_es_xz10",  "Lexus ES 300h (2018+)",               1680, 0.26, 1.865, 1.445, 2.870, 2.4, "215/55 R17", A.LATEST, 1.30, _L),

    # --- Ford -------------------------------------------------------------
    ("ford_fiesta_7",  "Ford Fiesta VII (2017-2023)",         1100, 0.33, 1.735, 1.476, 2.493, 2.3, "195/60 R15", A.LATEST, 1.28, _L),
    ("ford_focus_4",   "Ford Focus IV (2018+)",               1320, 0.27, 1.825, 1.454, 2.700, 2.3, "205/60 R16", A.LATEST, 1.30, _L),
    ("ford_mondeo_5",  "Ford Mondeo V (2014-2022)",           1500, 0.27, 1.852, 1.482, 2.850, 2.4, "215/60 R16", A.LATEST, 1.28, _L),
    ("ford_kuga_1",    "Ford Kuga I (2008-2012)",             1600, 0.35, 1.842, 1.710, 2.690, 2.3, "235/55 R17", A.MODERN, 1.24, _L),
    ("ford_kuga_3",    "Ford Kuga III (2019+)",               1650, 0.31, 1.882, 1.666, 2.710, 2.4, "225/60 R18", A.LATEST, 1.28, _L),
    ("ford_smax_1",    "Ford S-Max I (2006-2015)",            1700, 0.31, 1.884, 1.658, 2.850, 2.4, "215/60 R16", A.MODERN, 1.26, _L),
    ("ford_puma_2",    "Ford Puma (2019+)",                   1280, 0.31, 1.805, 1.555, 2.588, 2.4, "215/55 R17", A.LATEST, 1.28, _L),
    ("ford_transit_7", "Ford Transit VII kaubik (2006-2014)", 2000, 0.38, 1.974, 2.360, 3.300, 3.3, "215/75 R16C", A.MODERN, 1.12, _L),
    ("ford_ranger_3",  "Ford Ranger T6 (2011-2022)",          2100, 0.43, 1.850, 1.815, 3.220, 2.4, "255/70 R16", A.LATEST, 1.14, _L),

    # --- Opel -------------------------------------------------------------
    ("opel_astra_k",   "Opel Astra K (2015-2021)",            1280, 0.29, 1.809, 1.485, 2.662, 2.3, "205/55 R16", A.LATEST, 1.28, _L),
    ("opel_astra_l",   "Opel Astra L (2021+)",                1350, 0.28, 1.860, 1.470, 2.675, 2.4, "205/55 R16", A.LATEST, 1.30, _L),
    ("opel_corsa_e",   "Opel Corsa E (2014-2019)",            1100, 0.32, 1.746, 1.479, 2.510, 2.2, "185/65 R15", A.LATEST, 1.26, _L),
    ("opel_corsa_f",   "Opel Corsa F (2019+)",                1150, 0.29, 1.765, 1.435, 2.538, 2.3, "195/55 R16", A.LATEST, 1.28, _L),
    ("opel_insignia_b","Opel Insignia B (2017-2022)",         1500, 0.26, 1.863, 1.455, 2.829, 2.4, "225/55 R17", A.LATEST, 1.30, _L),
    ("opel_mokka_a",   "Opel Mokka A (2012-2019)",            1350, 0.35, 1.774, 1.658, 2.555, 2.3, "215/60 R17", A.MODERN, 1.24, _L),
    ("opel_grandland", "Opel Grandland X (2017-2024)",        1400, 0.32, 1.856, 1.609, 2.675, 2.4, "225/55 R18", A.LATEST, 1.28, _L),
    ("opel_zafira_c",  "Opel Zafira C Tourer (2011-2019)",    1650, 0.32, 1.884, 1.685, 2.760, 2.4, "225/50 R17", A.MODERN, 1.26, _L),
    ("opel_combo_d",   "Opel Combo D (2011-2018)",            1400, 0.34, 1.831, 1.845, 2.755, 2.4, "195/60 R16", A.MODERN, 1.22, _L),

    # --- Peugeot / Citroën / DS -------------------------------------------
    ("peugeot_207",    "Peugeot 207 (2006-2014)",             1150, 0.31, 1.720, 1.472, 2.540, 2.2, "185/65 R15", A.MODERN, 1.24, _L),
    ("peugeot_208_1",  "Peugeot 208 I (2012-2019)",           1050, 0.31, 1.739, 1.460, 2.538, 2.2, "185/65 R15", A.LATEST, 1.26, _L),
    ("peugeot_208_2",  "Peugeot 208 II (2019+)",              1150, 0.29, 1.745, 1.430, 2.540, 2.3, "195/55 R16", A.LATEST, 1.28, _L),
    ("peugeot_2008_1", "Peugeot 2008 I (2013-2019)",          1180, 0.33, 1.739, 1.556, 2.537, 2.3, "195/60 R16", A.LATEST, 1.26, _L),
    ("peugeot_2008_2", "Peugeot 2008 II (2019+)",             1250, 0.31, 1.770, 1.530, 2.605, 2.4, "215/60 R17", A.LATEST, 1.28, _L),
    ("peugeot_3008_2", "Peugeot 3008 II (2016-2024)",         1400, 0.31, 1.841, 1.620, 2.675, 2.4, "225/55 R18", A.LATEST, 1.28, _L),
    ("peugeot_308_3",  "Peugeot 308 III (2021+)",             1350, 0.28, 1.852, 1.441, 2.675, 2.4, "205/55 R16", A.LATEST, 1.30, _L),
    ("peugeot_406",    "Peugeot 406 (1995-2004)",             1350, 0.31, 1.764, 1.425, 2.700, 2.3, "195/65 R15", A.EARLY, 1.22, _L),
    ("peugeot_508_2",  "Peugeot 508 II (2018+)",              1450, 0.26, 1.859, 1.403, 2.793, 2.4, "215/55 R17", A.LATEST, 1.30, _L),
    ("peugeot_rifter", "Peugeot Rifter (2018+)",1450, 0.33, 1.848, 1.878, 2.785, 2.5, "205/60 R16", A.LATEST, 1.24, _L),
    ("citroen_c3_3",   "Citroën C3 III (2016-2024)",          1100, 0.33, 1.749, 1.474, 2.540, 2.3, "185/65 R15", A.LATEST, 1.26, _L),
    ("citroen_c4_picasso_2","Citroën C4 Picasso II (2013-2022)",1400,0.30,1.826,1.610, 2.785, 2.4, "205/60 R16", A.LATEST, 1.26, _L),
    ("citroen_c5_aircross","Citroën C5 Aircross (2018+)",     1450, 0.32, 1.859, 1.654, 2.730, 2.4, "215/65 R17", A.LATEST, 1.28, _L),
    ("citroen_berlingo_3","Citroën Berlingo III (2018+)",     1450, 0.33, 1.848, 1.849, 2.785, 2.5, "205/60 R16", A.LATEST, 1.24, _L),
    ("citroen_c5_1",   "Citroën C5 I (2001-2008)",            1450, 0.30, 1.770, 1.480, 2.750, 2.4, "215/55 R16", A.EARLY, 1.24, _L),

    # --- Renault / Dacia --------------------------------------------------
    ("renault_clio_3", "Renault Clio III (2005-2014)",        1100, 0.33, 1.720, 1.493, 2.575, 2.2, "185/60 R15", A.MODERN, 1.24, _L),
    ("renault_clio_5", "Renault Clio V (2019+)",              1150, 0.30, 1.798, 1.440, 2.583, 2.3, "195/55 R16", A.LATEST, 1.28, _L),
    ("renault_megane_2","Renault Mégane II (2002-2009)",      1250, 0.32, 1.777, 1.457, 2.625, 2.2, "195/65 R15", A.MODERN, 1.24, _L),
    ("renault_megane_4","Renault Mégane IV (2015-2022)",      1300, 0.29, 1.814, 1.447, 2.669, 2.3, "205/55 R16", A.LATEST, 1.28, _L),
    ("renault_scenic_3","Renault Scénic III (2009-2016)",     1450, 0.32, 1.845, 1.635, 2.705, 2.3, "205/60 R16", A.MODERN, 1.24, _L),
    ("renault_laguna_3","Renault Laguna III (2007-2015)",     1450, 0.30, 1.811, 1.445, 2.756, 2.3, "205/60 R16", A.MODERN, 1.26, _L),
    ("renault_kadjar", "Renault Kadjar (2015-2022)",          1400, 0.33, 1.836, 1.607, 2.646, 2.3, "215/60 R17", A.LATEST, 1.26, _L),
    ("renault_zoe",    "Renault Zoe (2013-2024)",             1500, 0.29, 1.730, 1.562, 2.588, 2.4, "195/55 R16", A.LATEST, 1.24, _L),
    ("dacia_logan_2",  "Dacia Logan II (2012-2020)",          1000, 0.34, 1.733, 1.517, 2.634, 2.2, "185/65 R15", A.MODERN, 1.20, _L),
    ("dacia_sandero_3","Dacia Sandero III (2020+)",           1050, 0.32, 1.848, 1.499, 2.604, 2.3, "185/65 R15", A.LATEST, 1.24, _L),
    ("dacia_duster_1", "Dacia Duster I (2010-2017)",          1250, 0.40, 1.822, 1.625, 2.673, 2.2, "215/65 R16", A.MODERN, 1.18, _L),
    ("dacia_jogger",   "Dacia Jogger (2021+)",                1200, 0.33, 1.784, 1.674, 2.897, 2.4, "205/60 R16", A.LATEST, 1.22, _L),

    # --- Nissan -----------------------------------------------------------
    ("nissan_micra_k12","Nissan Micra K12 (2002-2010)",        950, 0.33, 1.660, 1.540, 2.430, 2.2, "175/60 R15", A.MODERN, 1.22, _L),
    ("nissan_juke_f15","Nissan Juke F15 (2010-2019)",         1250, 0.35, 1.765, 1.565, 2.530, 2.3, "215/55 R17", A.MODERN, 1.24, _L),
    ("nissan_qashqai_j12","Nissan Qashqai J12 (2021+)",       1450, 0.31, 1.835, 1.625, 2.665, 2.4, "215/65 R17", A.LATEST, 1.28, _L),
    ("nissan_xtrail_t32","Nissan X-Trail T32 (2014-2022)",    1600, 0.33, 1.820, 1.710, 2.705, 2.4, "225/65 R17", A.LATEST, 1.26, _L),
    ("nissan_navara_d40","Nissan Navara D40 (2005-2015)",     2000, 0.43, 1.850, 1.780, 3.200, 2.3, "255/65 R17", A.MODERN, 1.12, _L),
    ("nissan_pathfinder_r51","Nissan Pathfinder R51 (2005-2014)",2100,0.40,1.850, 1.780, 2.853, 2.3, "255/65 R17", A.MODERN, 1.14, _L),

    # --- Hyundai / Kia ----------------------------------------------------
    ("hyundai_i10_2",  "Hyundai i10 II (2013-2019)",           950, 0.32, 1.660, 1.500, 2.385, 2.3, "175/65 R14", A.LATEST, 1.24, _L),
    ("hyundai_i20_2",  "Hyundai i20 II (2014-2020)",          1100, 0.31, 1.734, 1.474, 2.570, 2.3, "185/65 R15", A.LATEST, 1.26, _L),
    ("hyundai_i30_3",  "Hyundai i30 III (2017-2024)",         1300, 0.30, 1.795, 1.455, 2.650, 2.3, "205/55 R16", A.LATEST, 1.28, _L),
    ("hyundai_i40",    "Hyundai i40 (2011-2019)",             1500, 0.29, 1.815, 1.470, 2.770, 2.3, "205/60 R16", A.MODERN, 1.28, _L),
    ("hyundai_ix20",   "Hyundai ix20 (2010-2019)",            1250, 0.34, 1.765, 1.600, 2.615, 2.3, "195/65 R15", A.MODERN, 1.22, _L),
    ("hyundai_kona_1", "Hyundai Kona I (2017-2023)",          1300, 0.33, 1.800, 1.565, 2.600, 2.4, "205/60 R16", A.LATEST, 1.26, _L),
    ("hyundai_kona_ev","Hyundai Kona Electric (2018-2023)",1700,0.29,1.800,1.570, 2.600, 2.5, "215/55 R17", A.LATEST, 1.26, _L),
    ("hyundai_tucson_jm","Hyundai Tucson JM (2004-2010)",     1600, 0.38, 1.830, 1.730, 2.630, 2.2, "215/65 R16", A.MODERN, 1.20, _L),
    ("hyundai_santafe_tm","Hyundai Santa Fe TM (2018-2024)",  1900, 0.34, 1.890, 1.680, 2.765, 2.4, "235/60 R18", A.LATEST, 1.26, _L),
    ("kia_picanto_2",  "Kia Picanto II (2011-2017)",           900, 0.32, 1.595, 1.480, 2.385, 2.2, "165/60 R14", A.MODERN, 1.24, _L),
    ("kia_rio_4",      "Kia Rio IV (2017+)",                  1150, 0.31, 1.725, 1.450, 2.580, 2.3, "185/65 R15", A.LATEST, 1.26, _L),
    ("kia_venga",      "Kia Venga (2010-2019)",               1250, 0.34, 1.765, 1.600, 2.615, 2.3, "205/55 R16", A.MODERN, 1.22, _L),
    ("kia_sportage_4", "Kia Sportage IV (2015-2021)",         1500, 0.33, 1.855, 1.645, 2.670, 2.4, "225/60 R17", A.LATEST, 1.28, _L),
    ("kia_sportage_5", "Kia Sportage V (2021+)",              1550, 0.32, 1.865, 1.650, 2.755, 2.4, "235/60 R18", A.LATEST, 1.28, _L),
    ("kia_sorento_3",  "Kia Sorento III (2014-2020)",         1900, 0.35, 1.890, 1.690, 2.780, 2.4, "235/60 R18", A.LATEST, 1.26, _L),
    ("kia_niro_1",     "Kia Niro I Hybrid (2016-2022)",       1450, 0.29, 1.805, 1.545, 2.700, 2.4, "205/60 R16", A.LATEST, 1.26, _L),
    ("kia_optima_4",   "Kia Optima IV (2015-2020)",           1550, 0.27, 1.860, 1.465, 2.805, 2.4, "215/55 R17", A.LATEST, 1.28, _L),
    ("kia_ev6",        "Kia EV6 Long Range (2021+)",              2000, 0.28, 1.890, 1.550, 2.900, 2.6, "235/55 R19", A.LATEST, 1.26, _L),

    # --- Mazda ------------------------------------------------------------
    ("mazda_2_dj",     "Mazda 2 DJ (2014+)",                  1050, 0.30, 1.695, 1.500, 2.570, 2.3, "185/65 R15", A.LATEST, 1.26, _L),
    ("mazda_3_bm",     "Mazda 3 BM (2013-2019)",              1300, 0.29, 1.795, 1.450, 2.700, 2.3, "205/60 R16", A.LATEST, 1.28, _L),
    ("mazda_3_bp",     "Mazda 3 BP (2019+)",                  1350, 0.28, 1.795, 1.435, 2.725, 2.4, "205/60 R16", A.LATEST, 1.30, _L),
    ("mazda_6_gj",     "Mazda 6 GJ (2012+)",                  1450, 0.27, 1.840, 1.450, 2.830, 2.4, "225/55 R17", A.LATEST, 1.30, _L),
    ("mazda_cx3",      "Mazda CX-3 (2015-2022)",              1250, 0.33, 1.765, 1.535, 2.570, 2.4, "215/60 R16", A.LATEST, 1.26, _L),
    ("mazda_cx30",     "Mazda CX-30 (2019+)",                 1400, 0.32, 1.795, 1.540, 2.655, 2.4, "215/65 R16", A.LATEST, 1.28, _L),
    ("mazda_cx5_kf",   "Mazda CX-5 KF (2017+)",               1550, 0.33, 1.840, 1.675, 2.700, 2.4, "225/65 R17", A.LATEST, 1.28, _L),
    ("mazda_cx60",     "Mazda CX-60 PHEV (2022+)",            2050, 0.33, 1.890, 1.680, 2.870, 2.5, "235/50 R20", A.LATEST, 1.28, _L),

    # --- Honda / Mitsubishi / Subaru / Suzuki ------------------------------
    ("honda_civic_9",  "Honda Civic IX (2011-2017)",          1250, 0.30, 1.770, 1.470, 2.595, 2.3, "205/55 R16", A.LATEST, 1.28, _L),
    ("honda_civic_10", "Honda Civic X (2017-2022)",           1300, 0.28, 1.800, 1.435, 2.700, 2.4, "215/55 R16", A.LATEST, 1.30, _L),
    ("honda_crv_5",    "Honda CR-V V (2018-2023)",            1600, 0.33, 1.855, 1.680, 2.660, 2.4, "235/60 R18", A.LATEST, 1.26, _L),
    ("honda_hrv_2",    "Honda HR-V II (2015-2021)",           1250, 0.34, 1.770, 1.605, 2.610, 2.3, "215/60 R16", A.LATEST, 1.26, _L),
    ("honda_accord_8", "Honda Accord VIII (2008-2015)",       1500, 0.29, 1.840, 1.470, 2.705, 2.3, "215/60 R16", A.MODERN, 1.28, _L),
    ("mitsu_outlander_2","Mitsubishi Outlander II (2006-2012)",1600,0.36, 1.800, 1.680, 2.670, 2.3, "215/70 R16", A.MODERN, 1.22, _L),
    ("mitsu_lancer_10","Mitsubishi Lancer X (2007-2017)",     1300, 0.31, 1.760, 1.490, 2.635, 2.3, "205/60 R16", A.MODERN, 1.26, _L),
    ("mitsu_l200_5",   "Mitsubishi L200 V (2015+)",           1900, 0.42, 1.815, 1.780, 3.000, 2.4, "245/65 R17", A.LATEST, 1.14, _L),
    ("mitsu_spacestar","Mitsubishi Space Star (2012+)",        850, 0.30, 1.665, 1.505, 2.450, 2.2, "165/65 R14", A.LATEST, 1.22, _L),
    ("subaru_forester_sh","Subaru Forester SH (2008-2013)",   1500, 0.34, 1.780, 1.700, 2.615, 2.3, "215/60 R16", A.MODERN, 1.24, _L),
    ("subaru_xv_1",    "Subaru XV (2011-2017)",               1400, 0.33, 1.780, 1.570, 2.635, 2.3, "225/55 R17", A.MODERN, 1.26, _L),
    ("subaru_outback_bp","Subaru Outback BP (2003-2009)",     1500, 0.34, 1.770, 1.545, 2.670, 2.3, "215/55 R17", A.MODERN, 1.24, _L),
    ("suzuki_swift_4", "Suzuki Swift IV (2010-2017)",          950, 0.32, 1.695, 1.510, 2.430, 2.3, "175/65 R15", A.MODERN, 1.24, _L),
    ("suzuki_vitara_4","Suzuki Vitara IV (2015+)",            1150, 0.36, 1.775, 1.610, 2.500, 2.3, "215/60 R16", A.LATEST, 1.24, _L),
    ("suzuki_sx4_scross","Suzuki SX4 S-Cross (2013-2021)",    1200, 0.34, 1.785, 1.585, 2.600, 2.3, "205/60 R16", A.LATEST, 1.24, _L),
    ("suzuki_jimny_4", "Suzuki Jimny IV (2018+)",             1100, 0.52, 1.645, 1.725, 2.250, 1.8, "195/80 R15", A.LATEST, 1.10, _L),
    ("suzuki_ignis_3", "Suzuki Ignis III (2016+)",             900, 0.35, 1.660, 1.595, 2.435, 2.3, "175/65 R15", A.LATEST, 1.22, _L),

    # --- Volvo ------------------------------------------------------------
    ("volvo_s40_2",    "Volvo S40 II (2004-2012)",      1400, 0.30, 1.770, 1.450, 2.640, 2.3, "205/55 R16", A.MODERN, 1.28, _L),
    ("volvo_v70_2",    "Volvo V70 II (2000-2007)",            1550, 0.31, 1.804, 1.490, 2.763, 2.3, "205/55 R16", A.EARLY, 1.26, _L),
    ("volvo_v60_2",    "Volvo V60 II (2018+)",                1750, 0.28, 1.850, 1.430, 2.872, 2.5, "225/50 R17", A.LATEST, 1.30, _L),
    ("volvo_xc40",     "Volvo XC40 (2017+)",                  1700, 0.32, 1.863, 1.652, 2.702, 2.5, "235/55 R18", A.LATEST, 1.28, _L),
    ("volvo_xc90_2",   "Volvo XC90 II (2015+)",               2050, 0.32, 2.008, 1.776, 2.984, 2.6, "235/55 R19", A.LATEST, 1.26, _L),
    ("volvo_v90_2",    "Volvo V90 II (2016+)",                1850, 0.29, 1.879, 1.475, 2.941, 2.5, "245/45 R18", A.LATEST, 1.30, _L),

    # --- muud ---------------------------------------------------------------
    ("seat_leon_2",    "SEAT Leon II (2005-2012)",            1300, 0.31, 1.768, 1.458, 2.578, 2.3, "205/55 R16", A.MODERN, 1.28, _L),
    ("seat_ibiza_5",   "SEAT Ibiza V (2017+)",                1150, 0.30, 1.780, 1.444, 2.564, 2.3, "185/65 R15", A.LATEST, 1.28, _L),
    ("seat_arona",     "SEAT Arona (2017+)",                  1200, 0.32, 1.780, 1.552, 2.566, 2.3, "205/60 R16", A.LATEST, 1.26, _L),
    ("seat_tarraco",   "SEAT Tarraco (2018-2024)",            1650, 0.32, 1.839, 1.674, 2.790, 2.5, "215/65 R17", A.LATEST, 1.28, _L),
    ("cupra_formentor","Cupra Formentor (2020+)",             1500, 0.30, 1.839, 1.511, 2.680, 2.5, "245/45 R18", A.LATEST, 1.32, _L),
    ("fiat_panda_3",   "Fiat Panda III (2012+)",               950, 0.33, 1.643, 1.551, 2.300, 2.2, "175/65 R14", A.LATEST, 1.22, _L),
    ("fiat_punto_3",   "Fiat Grande Punto (2005-2018)",       1100, 0.32, 1.687, 1.490, 2.510, 2.2, "185/65 R15", A.MODERN, 1.24, _L),
    ("fiat_tipo_2",    "Fiat Tipo (2015+)",                   1250, 0.31, 1.792, 1.497, 2.638, 2.3, "205/55 R16", A.LATEST, 1.26, _L),
    ("alfa_159",       "Alfa Romeo 159 (2005-2011)",          1550, 0.31, 1.828, 1.417, 2.700, 2.4, "215/55 R16", A.MODERN, 1.28, _L),
    ("mini_f56",       "MINI Cooper F56 (2014-2024)",         1200, 0.30, 1.727, 1.414, 2.495, 2.3, "175/65 R15", A.LATEST, 1.30, _L),
    ("jeep_renegade",  "Jeep Renegade (2014+)",               1400, 0.36, 1.805, 1.667, 2.570, 2.3, "215/65 R16", A.LATEST, 1.24, _L),
    ("jeep_cherokee_kl","Jeep Cherokee KL (2013-2023)",       1800, 0.34, 1.859, 1.683, 2.700, 2.4, "225/65 R17", A.LATEST, 1.24, _L),
    ("lr_disco_4",     "Land Rover Discovery 4 (2009-2016)",  2600, 0.40, 2.022, 1.887, 2.885, 2.5, "255/55 R19", A.MODERN, 1.14, _L),
    ("lr_evoque_1",    "Range Rover Evoque I (2011-2018)",    1700, 0.35, 1.965, 1.635, 2.660, 2.4, "235/60 R18", A.LATEST, 1.26, _L),
    ("chevrolet_aveo_t300","Chevrolet Aveo T300 (2011-2015)", 1150, 0.32, 1.735, 1.517, 2.525, 2.2, "185/75 R14", A.MODERN, 1.22, _L),
    ("chevrolet_spark_m300","Chevrolet Spark M300 (2010-2015)",900,0.34, 1.597, 1.522, 2.375, 2.1, "155/70 R14", A.MODERN, 1.20, _L),
    ("lada_vesta",     "Lada Vesta (2015+)",                  1250, 0.34, 1.764, 1.497, 2.635, 2.2, "185/65 R15", A.LATEST, 1.20, _L),
    ("lada_granta",    "Lada Granta (2011+)",                 1100, 0.35, 1.700, 1.500, 2.476, 2.1, "175/65 R14", A.MODERN, 1.18, _L),
    ("ssangyong_korando_3","SsangYong Korando C (2010-2019)", 1600, 0.36, 1.830, 1.675, 2.650, 2.3, "225/60 R17", A.MODERN, 1.22, _L),
    ("isuzu_dmax_2",   "Isuzu D-Max II (2012-2020)",          1950, 0.43, 1.860, 1.795, 3.095, 2.4, "255/65 R17", A.LATEST, 1.12, _L),
    ("mg_zs_ev",       "MG ZS EV (2019+)",                    1550, 0.33, 1.809, 1.620, 2.585, 2.5, "215/55 R17", A.LATEST, 1.24, _L),
    ("byd_atto3",      "BYD Atto 3 (2022+)",                  1750, 0.29, 1.875, 1.615, 2.720, 2.5, "215/55 R18", A.LATEST, 1.24, _L),
    ("tesla_model_s",  "Tesla Model S (2012-2021)",           2100, 0.24, 1.964, 1.445, 2.960, 2.9, "245/45 R19", A.LATEST, 1.30, _L),
    ("tesla_model_3_sr","Tesla Model 3 SR+ (2019-2023)",      1650, 0.23, 1.849, 1.443, 2.875, 2.9, "235/45 R18", A.LATEST, 1.30, _L),
    # 2026-09-24. Suur Ameerika sedaan: Eestis vähe, aga imporditud ja
    # otsitud. Mass, Cd ja mõõdud tootja andmetest (2012 Chrysler 300
    # ametlik spetsifikatsioonileht; ultimatespecs 300C 5.7).
    ("chrysler_300c_lx","Chrysler 300C LX (2004-2010)",       1915, 0.34, 1.881, 1.483, 3.048, 2.4, "225/60 R18", A.MODERN, 1.22, "rõhk hinnang"),
    # Touring = universaal. auto-data 3.0 CRD: sedaan 1840 kg, Touring 1875 kg (+35 kg)
    ("chrysler_300c_touring_lx","Chrysler 300C Touring LX (2004-2010)", 1950, 0.34, 1.880, 1.475, 3.048, 2.4, "225/60 R18", A.MODERN, 1.22, "rõhk hinnang; mass sedaan +35 kg (auto-data)"),
    ("chrysler_300c_ld","Chrysler 300C LD (2011-2023)",       1962, 0.32, 1.902, 1.492, 3.052, 2.4, "225/60 R18", A.MODERN, 1.26, "rõhk hinnang"),
]

# =====================================================================
# 2026-09-25 LISATUD: 1985-2005 autod, mis on Eestis päriselt kasutuses
# (Golf II-IV, Passat B3-B5, Audi 80/100, W124/W201, E30/E34, Opel, Volvo,
# Žigulid, Samara, Moskvitš, Volga jne). Andmed kogutud veebist allikatega:
# auto-data.net, ultimatespecs, ADAC autokataloog, cars-data.com,
# tpressure.com, tyre-pressures.com (HaynesPro), club.autodoc, Vikipeedia
# (de/en/ru), autoopt.ru ja catalog-vaz.ru (Nõukogude autod).
#
# ABS ON SIIN KÕIGE TÄHTSAM VÄLI. Selle ajastu autodel oli ABS sageli
# LISAVARUSTUS. Kus see oli levinud mudelil tõsiselt kahel moel (nt Golf III,
# W124, Astra F), on KAKS rida: "ABS-iga" ja "ilma ABS-ita" -- kasutaja
# teab oma autot (armatuuril põleb käivitamisel ABS-tuli). Kus ABS oli
# harvaesinev lisavarustus, on üks rida ABS.NONE ja märkus ütleb seda.
#
# Pidurite võimekus (viimane arv) on HINNANG klassi järgi, nagu kõigil
# ridadel: ABS-ita lääne autod 1,05-1,12 g, Nõukogude autod 0,75-0,90 g
# (trummelpidurid, nõrgem võimendus). ABS-ita autol piirab pidurdust
# enamasti rehv (abs_eff 0,74), mitte pidurid, seega see väärtus
# tulemust tavaliselt ei muuda.
# Mass on tootja tühimass (DIN, ilma juhita), kui märkuses ei öelda teisiti.
_ABS2 = "ABS oli lisavarustus: vali 'ABS-iga', kui armatuuril süttib käivitamisel ABS-tuli"
_ABS1 = "ABS oli harva esinev lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem"
EE_VEHICLES += [
    # --- Volkswagen -------------------------------------------------------
    ("vw_golf_2",       "VW Golf II 1.6 (1983-1992)",              880, 0.34, 1.665, 1.415, 2.475, 2.0, "175/70 R13", A.NONE,  1.08, _ABS1 + " (alates 1987, peamiselt GTI-l)"),
    ("vw_golf_3",       "VW Golf III 1.8 ilma ABS-ita (1991-1997)",1030, 0.30, 1.695, 1.425, 2.475, 2.0, "175/70 R13", A.NONE,  1.10, _ABS2 + "; standardis alates 1996"),
    ("vw_golf_3_abs",   "VW Golf III 1.8 ABS-iga (1991-1997)",    1030, 0.30, 1.695, 1.425, 2.475, 2.0, "175/70 R13", A.EARLY, 1.18, "ABS standardis GTI 16V/VR6-l ja kõigil alates 1996"),
    ("vw_jetta_2",      "VW Jetta II 1.6 (1984-1992)",             920, 0.36, 1.665, 1.415, 2.475, 1.9, "175/70 R13", A.NONE,  1.08, _ABS1),
    ("vw_vento",        "VW Vento 1.8 (1991-1998)",               1071, 0.32, 1.695, 1.425, 2.475, 2.3, "185/60 R14", A.NONE,  1.10, _ABS1 + "; ABS-i kohta eraldi allikat ei leitud, eeldatud nagu Golf III-l"),
    ("vw_passat_b3",    "VW Passat B3 1.8 ilma ABS-ita (1988-1993)",1155,0.29, 1.705, 1.430, 2.625, 2.2, "185/65 R14", A.NONE,  1.10, _ABS2),
    ("vw_passat_b3_abs","VW Passat B3 1.8 ABS-iga (1988-1993)",   1155, 0.29, 1.705, 1.430, 2.625, 2.2, "185/65 R14", A.EARLY, 1.18, "ABS oli B3-l lisavarustus"),
    ("vw_passat_b4",    "VW Passat B4 1.9 TDI (1993-1997)",       1246, 0.31, 1.720, 1.430, 2.625, 2.1, "185/65 R14", A.EARLY, 1.20, "Cd hinnang (B3 kere edasiarendus); ABS standardis"),
    ("vw_polo_3",       "VW Polo III 1.4 ilma ABS-ita (1994-2001)", 985,0.34, 1.655, 1.420, 2.400, 2.0, "175/65 R13", A.NONE,  1.08, _ABS2 + "; Saksamaal standardis alates 1996 lõpust; Cd hinnang"),
    ("vw_polo_3_abs",   "VW Polo III 1.4 ABS-iga (1994-2001)",     985, 0.34, 1.655, 1.420, 2.400, 2.0, "175/65 R13", A.EARLY, 1.16, "Cd hinnang"),

    # --- Audi -------------------------------------------------------------
    ("audi_80_b3",      "Audi 80 B3 1.8 (1986-1991)",             1020, 0.29, 1.695, 1.397, 2.546, 1.9, "175/70 R14", A.NONE,  1.10, _ABS1 + " (allikaga kinnitamata)"),
    ("audi_80_b4",      "Audi 80 B4 2.0 ilma ABS-ita (1991-1996)",1190, 0.30, 1.695, 1.406, 2.612, 2.0, "195/65 R15", A.NONE,  1.12, _ABS2 + "; enamikul standardis alates 01/1993"),
    ("audi_80_b4_abs",  "Audi 80 B4 2.0 ABS-iga (1991-1996)",     1190, 0.30, 1.695, 1.406, 2.612, 2.0, "195/65 R15", A.EARLY, 1.20, "ABS enamikul standardis alates 01/1993"),
    ("audi_100_c3",     "Audi 100 C3 1.8 (1982-1991)",            1080, 0.30, 1.814, 1.422, 2.687, 2.0, "185/70 R14", A.NONE,  1.10, _ABS1 + "; rõhk hinnang"),
    ("audi_100_c4",     "Audi 100 C4 2.0 ilma ABS-ita (1990-1994)",1430,0.32, 1.777, 1.437, 2.692, 2.2, "195/65 R15", A.NONE,  1.12, _ABS2 + " (4-silindrilistel ja TDI-l); rõhk hinnang; mass võib sisaldada juhti"),
    ("audi_100_c4_abs", "Audi 100 C4 2.0 ABS-iga (1990-1994)",    1430, 0.32, 1.777, 1.437, 2.692, 2.2, "195/65 R15", A.EARLY, 1.20, "ABS standardis 6-silindrilistel; rõhk hinnang; mass võib sisaldada juhti"),
    ("audi_a3_8l",      "Audi A3 8L 1.6 (1996-2003)",             1015, 0.31, 1.735, 1.427, 2.513, 2.2, "195/65 R15", A.EARLY, 1.22, "ABS standardis (allikaga kinnitamata)"),

    # --- Mercedes-Benz ------------------------------------------------------
    ("mb_190_w201",     "Mercedes 190E W201 2.0 ilma ABS-ita (1982-1993)",1180,0.33,1.690,1.375,2.665,2.0,"185/65 R15", A.NONE,  1.12, _ABS2 + "; standardis alates 1991 kevadest"),
    ("mb_190_w201_abs", "Mercedes 190E W201 2.0 ABS-iga (1982-1993)",1180, 0.33, 1.690, 1.375, 2.665, 2.0, "185/65 R15", A.EARLY, 1.20, "ABS standardis alates 1991 kevadest (1.8 alates 10/1992)"),
    ("mb_e230_w124",    "Mercedes E230 W124 ilma ABS-ita (1984-1988)",1360,0.29,1.740,1.428,2.800,2.0,"195/65 R15", A.NONE,  1.12, _ABS2 + "; alates 09/1988 kõigil standardis"),
    ("mb_e230_w124_abs","Mercedes E230 W124 ABS-iga (1984-1996)", 1360, 0.29, 1.740, 1.428, 2.800, 2.0, "195/65 R15", A.EARLY, 1.22, "ABS standardis kõigil alates 09/1988"),
    ("mb_s320_w140",    "Mercedes S320 W140 (1991-1998)",         1890, 0.30, 1.886, 1.486, 3.040, 2.0, "235/60 R16", A.EARLY, 1.22, "rõhk S 280 järgi (S 320 lehel puudus)"),
    ("mb_a140_w168",    "Mercedes A140 W168 (1997-2004)",         1020, 0.31, 1.719, 1.590, 2.423, 1.8, "195/50 R15", A.EARLY, 1.20, "ESP + pidurdusabi standardis alates 02/1998"),

    # --- BMW -----------------------------------------------------------------
    ("bmw_318i_e30",    "BMW 318i E30 ilma ABS-ita (1982-1994)",  1065, 0.36, 1.645, 1.380, 2.570, 1.8, "175/70 R14", A.NONE,  1.12, _ABS2 + "; Cd nõrk allikas (foorum); mass EL-i tühimass; baasmõõt 175/70 R14 (195/65 R14 kohta märgise andmeid ei ole)"),
    ("bmw_318i_e30_abs","BMW 318i E30 ABS-iga (1982-1994)",       1065, 0.36, 1.645, 1.380, 2.570, 1.8, "175/70 R14", A.EARLY, 1.20, "ABS standardis 325i-l ja M3-l; Cd nõrk allikas; mass EL-i tühimass; baasmõõt 175/70 R14 (195/65 R14 kohta märgise andmeid ei ole)"),
    ("bmw_520i_e34",    "BMW 520i E34 ilma ABS-ita (1988-1992)",  1445, 0.30, 1.751, 1.412, 2.761, 2.0, "195/65 R15", A.NONE,  1.12, _ABS2 + "; alates 05/1992 kõigil standardis; mass EL-i tühimass"),
    ("bmw_520i_e34_abs","BMW 520i E34 ABS-iga (1988-1996)",       1445, 0.30, 1.751, 1.412, 2.761, 2.0, "195/65 R15", A.EARLY, 1.22, "ABS standardis 525i-l ja suurematel, kõigil alates 05/1992; mass EL-i tühimass"),

    # --- Opel -----------------------------------------------------------------
    ("opel_kadett_e",   "Opel Kadett E 1.6 (1984-1991)",           890, 0.32, 1.663, 1.400, 2.520, 1.8, "175/70 R13", A.NONE,  1.08, _ABS1 + " (standardis ainult GSi-l); mass EL-i tühimass"),
    ("opel_astra_f",    "Opel Astra F 1.6 ilma ABS-ita (1991-1998)",940, 0.32, 1.688, 1.410, 2.517, 1.9, "175/70 R13", A.NONE,  1.10, _ABS2 + "; standardis alates mudeliaastast 1996; mass EL-i tühimass"),
    ("opel_astra_f_abs","Opel Astra F 1.6 ABS-iga (1991-1998)",    940, 0.32, 1.688, 1.410, 2.517, 1.9, "175/70 R13", A.EARLY, 1.18, "ABS standardis alates mudeliaastast 1996; mass EL-i tühimass"),
    ("opel_vectra_a",   "Opel Vectra A 1.6 ilma ABS-ita (1988-1992)",1110,0.29, 1.700, 1.400, 2.600, 1.8, "175/70 R14", A.NONE,  1.10, _ABS2 + "; kõigil standardis alates 09/1992; mass EL-i tühimass"),
    ("opel_vectra_a_abs","Opel Vectra A 1.6 ABS-iga (1988-1995)", 1110, 0.29, 1.700, 1.400, 2.600, 1.8, "175/70 R14", A.EARLY, 1.18, "ABS kõigil standardis alates 09/1992; mass EL-i tühimass"),
    ("opel_omega_a",    "Opel Omega A 2.0 ilma ABS-ita (1986-1990)",1300,0.28, 1.772, 1.447, 2.730, 2.0, "185/70 R14", A.NONE,  1.12, _ABS2 + "; standardis alates 08/1990; mass EL-i tühimass"),
    ("opel_omega_a_abs","Opel Omega A 2.0 ABS-iga (1986-1994)",   1300, 0.28, 1.772, 1.447, 2.730, 2.0, "185/70 R14", A.EARLY, 1.20, "ABS standardis alates 08/1990; mass EL-i tühimass"),
    ("opel_omega_b",    "Opel Omega B 2.0 (1994-2003)",           1410, 0.28, 1.786, 1.455, 2.730, 2.0, "195/65 R15", A.EARLY, 1.22, "Cd hinnang (Omega A järgi); mass EL-i tühimass"),
    ("opel_corsa_b",    "Opel Corsa B 1.4 (1993-2000)",            900, 0.35, 1.608, 1.420, 2.443, 2.0, "165/70 R13", A.NONE,  1.05, _ABS1 + "; mass, Cd ja mõõdud ligikaudsed"),
    ("opel_corsa_c",    "Opel Corsa C 1.2 (2000-2006)",           1000, 0.32, 1.646, 1.440, 2.491, 1.9, "175/65 R14", A.EARLY, 1.18, "mass, Cd ja mõõdud ligikaudsed; ABS eeldatud standardiks (kinnitamata)"),

    # --- Ford -----------------------------------------------------------------
    ("ford_sierra",     "Ford Sierra 2.0 (1982-1993)",            1140, 0.34, 1.690, 1.367, 2.609, 1.8, "185/65 R14", A.NONE,  1.10, _ABS1 + " (4x4 ja Cosworth); 185/70 R13 kohta märgise andmeid ei ole, arvutus 185/65 R14-ga"),
    ("ford_escort_7",   "Ford Escort 1.6 (1990-2000)",            1080, 0.35, 1.700, 1.346, 2.523, 2.0, "175/70 R13", A.NONE,  1.08, _ABS1),
    ("ford_mondeo_1",   "Ford Mondeo I 1.8 (1993-2000)",          1248, 0.32, 1.747, 1.372, 2.704, 2.1, "185/65 R14", A.EARLY, 1.20, "Cd hinnang; ABS Saksamaa turul standardis alates 09/1993 (UK-s ainult GLX-st)"),
    ("ford_fiesta_4",   "Ford Fiesta Mk4 1.25 (1995-2002)",        980, 0.36, 1.634, 1.334, 2.446, 2.1, "165/70 R13", A.NONE,  1.05, _ABS1 + "; mass ja Cd hinnang"),

    # --- Toyota ---------------------------------------------------------------
    ("toyota_corolla_e90","Toyota Corolla E90 1.3 (1987-1992)",    935, 0.34, 1.655, 1.365, 2.430, 1.9, "175/70 R13", A.NONE,  1.05, "Cd ja rõhk hinnang; ABS-i allikat ei leitud, tavalisel 1.3-l seda ei olnud"),
    ("toyota_corolla_e100","Toyota Corolla E100 1.3 (1991-1997)",  995, 0.33, 1.685, 1.383, 2.465, 2.3, "175/65 R14", A.NONE,  1.08, _ABS1 + " (standardis ainult 1.8 GXi-l)"),
    ("toyota_carina_e", "Toyota Carina E 1.6 ilma ABS-ita (1992-1996)",1099,0.30,1.695,1.410,2.580,2.2,"185/65 R14", A.NONE,  1.10, _ABS2 + "; 1996. aasta uuendusest alates kõigil standardis"),
    ("toyota_carina_e_abs","Toyota Carina E 1.6 ABS-iga (1992-1997)",1099,0.30,1.695,1.410,2.580,2.2,"185/65 R14", A.EARLY, 1.20, "ABS kõigil standardis alates 1996"),

    # --- Volvo ja Saab ------------------------------------------------------------
    ("volvo_240",       "Volvo 240 2.3 (1974-1993)",              1243, 0.45, 1.710, 1.430, 2.640, 1.9, "185/70 R14", A.NONE,  1.10, "Cd hinnang (kandiline kere); ABS ainult viimastel mudeliaastatel 1991-1993"),
    ("volvo_940",       "Volvo 940 2.3 (1990-1998)",              1445, 0.35, 1.750, 1.410, 2.770, 1.9, "185/65 R15", A.EARLY, 1.20, "ABS standardis GLE/16V/Turbo-l, baas-GL-il alguses lisavarustus; 740 on peaaegu sama (Cd 0,41)"),
    ("volvo_850",       "Volvo 850 2.5 (1991-1997)",              1375, 0.32, 1.760, 1.415, 2.664, 2.2, "195/60 R15", A.EARLY, 1.22, "ABS kõigil turgudel standardis alates 1994"),
    ("volvo_s40_1",     "Volvo S40 I 1.8 (1995-2004)",            1286, 0.32, 1.717, 1.411, 2.550, 2.2, "195/55 R15", A.EARLY, 1.22, "Cd V40 järgi"),
    ("volvo_v70_1",     "Volvo V70 I 2.5 (1996-2000)",            1470, 0.32, 1.760, 1.430, 2.660, 2.2, "195/60 R15", A.EARLY, 1.22, ""),
    ("volvo_s80_1",     "Volvo S80 I 2.4 (1998-2006)",            1489, 0.28, 1.832, 1.452, 2.791, 2.0, "205/65 R15", A.EARLY, 1.24, "ABS + EBD standardis"),
    ("saab_900_2",      "Saab 900 II 2.0 (1993-1998)",            1290, 0.34, 1.711, 1.436, 2.600, 2.2, "195/60 R15", A.EARLY, 1.20, ""),

    # --- Nissan, Mazda, Honda, Mitsubishi ----------------------------------------
    ("nissan_sunny_n14","Nissan Sunny N14 1.4 (1990-1995)",       1040, 0.33, 1.670, 1.395, 2.430, 2.0, "175/70 R13", A.NONE,  1.08, "Cd hinnang; ABS-i tavalistel versioonidel ei pakutud"),
    ("nissan_primera_p10","Nissan Primera P10 1.6 ilma ABS-ita (1990-1996)",1075,0.30,1.700,1.390,2.550,2.1,"175/70 R14", A.NONE, 1.10, _ABS2 + "; Cd hinnang"),
    ("nissan_primera_p10_abs","Nissan Primera P10 1.6 ABS-iga (1990-1996)",1075,0.30,1.700,1.390,2.550,2.1,"175/70 R14", A.EARLY,1.20, "Cd hinnang; ABS standardis GT-l, UK-s kõigil alates 1993"),
    ("nissan_primera_p11","Nissan Primera P11 1.6 (1996-2002)",   1185, 0.30, 1.715, 1.410, 2.600, 2.2, "175/70 R14", A.EARLY, 1.20, "Cd hinnang; ABS kõigil standardis"),
    ("nissan_almera_n15","Nissan Almera N15 1.4 ilma ABS-ita (1995-1998)",1065,0.33,1.690,1.395,2.535,2.1,"175/65 R14", A.NONE, 1.08, "Cd hinnang; tavalistel versioonidel ABS-i ei pakutud enne 1998. aasta uuendust"),
    ("nissan_almera_n15_abs","Nissan Almera N15 1.4 ABS-iga (1998-2000)",1065,0.33,1.690,1.395,2.535,2.1,"175/65 R14", A.EARLY,1.18, "Cd hinnang; 1998. aasta uuendusest ABS standardis"),
    ("nissan_micra_k11","Nissan Micra K11 1.0 (1992-2002)",        780, 0.34, 1.585, 1.430, 2.360, 2.0, "155/70 R13", A.NONE,  1.05, "Cd hinnang; " + _ABS1 + " (ainult 1998+ mudelitel)"),
    ("mazda_323_bj",    "Mazda 323 BJ 1.5 (1998-2003)",           1110, 0.32, 1.705, 1.410, 2.610, 2.1, "175/65 R14", A.NONE,  1.10, "mass, Cd ja mõõdud ligikaudsed; ABS oli baasversioonil lisavarustus (kinnitamata)"),
    ("mazda_626_gf",    "Mazda 626 GF 1.8 (1997-2002)",           1145, 0.31, 1.710, 1.430, 2.610, 2.0, "185/65 R14", A.NONE,  1.10, "Cd hinnang; " + _ABS1),
    ("honda_civic_6",   "Honda Civic VI 1.4 (1995-2001)",          940, 0.32, 1.695, 1.375, 2.620, 2.1, "175/70 R13", A.NONE,  1.08, "Cd hinnang; " + _ABS1),
    ("honda_accord_6",  "Honda Accord VI 1.8 (1998-2002)",        1305, 0.31, 1.750, 1.430, 2.675, 2.3, "195/60 R15", A.EARLY, 1.22, "Cd hinnang; ABS standardis"),
    ("mitsu_carisma",   "Mitsubishi Carisma 1.6 (1995-2004)",     1080, 0.30, 1.695, 1.405, 2.550, 2.2, "185/65 R14", A.NONE,  1.10, "Cd hinnang; ABS-i 1995-99 1.6-l ei pakutud, hiljem lisavarustus"),
    ("mitsu_galant_8",  "Mitsubishi Galant VIII 2.0 (1996-2003)", 1235, 0.30, 1.740, 1.420, 2.640, 2.1, "195/60 R15", A.EARLY, 1.22, "Cd hinnang; ABS eeldatud standardiks Euroopa 2.0-l (kinnitamata)"),

    # --- Prantsuse ------------------------------------------------------------------
    ("renault_megane_1","Renault Mégane I 1.6 (1995-2003)",       1070, 0.33, 1.698, 1.420, 2.580, 2.3, "175/65 R14", A.NONE,  1.08, "mass, Cd ja mõõdud ligikaudsed; " + _ABS1),
    ("peugeot_306",     "Peugeot 306 1.6 (1993-2002)",            1040, 0.33, 1.689, 1.380, 2.580, 2.0, "185/65 R14", A.NONE,  1.08, "mass, Cd ja mõõdud ligikaudsed; " + _ABS1),
    ("citroen_xantia",  "Citroën Xantia 1.8 (1993-2001)",         1210, 0.31, 1.755, 1.380, 2.740, 2.2, "185/65 R14", A.NONE,  1.10, "mass, Cd ja mõõdud ligikaudsed; ABS oli baasversioonil lisavarustus, VSX-il ja Actival standardis"),

    # --- Škoda ja SEAT ----------------------------------------------------------------
    ("skoda_favorit",   "Škoda Favorit 1.3 (1987-1995)",           840, 0.35, 1.620, 1.415, 2.450, 1.8, "165/70 R13", A.NONE,  1.00, "Cd ja rõhk hinnang; ABS-i ei olnud"),
    ("skoda_felicia",   "Škoda Felicia 1.3 (1994-2001)",           935, 0.34, 1.635, 1.415, 2.450, 2.0, "165/70 R13", A.NONE,  1.05, _ABS1),
    ("seat_ibiza_2",    "SEAT Ibiza II 1.4 (1993-2002)",           955, 0.33, 1.640, 1.422, 2.443, 2.1, "175/70 R13", A.NONE,  1.08, _ABS1),
    ("seat_toledo_1",   "SEAT Toledo I 1.6 (1991-1999)",           985, 0.31, 1.662, 1.424, 2.471, 2.1, "175/70 R13", A.NONE,  1.08, "rõhk hinnang; ABS lisavarustus, enamikul standardis alates 1997"),

    # --- Nõukogude ja Ida-Euroopa ----------------------------------------------------
    # Rõhk tehase juhendist kgf/cm² -> bar (x 0,981), esitelg.
    ("lada_2101",       "VAZ 2101 Žiguli 1.2 (1970-1988)",         955, 0.52, 1.611, 1.440, 2.424, 1.7, "165/80 R13", A.NONE,  0.88, "Cd Venemaa koondtabelist (mitte tehase ametlik); 2103 on sarnane, u 1030 kg"),
    ("lada_2106",       "VAZ 2106 1.6 (1976-2006)",               1035, 0.53, 1.611, 1.440, 2.424, 1.7, "175/70 R13", A.NONE,  0.88, "Cd hinnang (2101 ja 2107 vahel)"),
    ("lada_samara",     "Lada Samara 2108/2109 (1984-2004)",       915, 0.46, 1.650, 1.402, 2.460, 2.0, "165/70 R13", A.NONE,  0.90, "Cd Venemaa koondtabelist (2108/2109 0,463)"),
    ("moskvich_2140",   "Moskvitš 2140/412 1.5 (1967-1988)",      1080, 0.50, 1.550, 1.480, 2.400, 1.7, "165/80 R13", A.NONE,  0.85, "Cd hinnang; tehases diagonaalrehv 6.45-13"),
    ("moskvich_2141",   "Moskvitš 2141 Aleko 1.5 (1986-1998)",    1070, 0.38, 1.690, 1.400, 2.580, 1.9, "175/70 R14", A.NONE,  0.90, "Cd vaidlustatud (tehas 0,35, mõõdetud 0,38); tehasemõõt 165/80 R14, mida enam ei müüda; arvutus levinud asendusmõõduga 175/70 R14"),
    ("gaz_24",          "GAZ Volga 24 2.4 (1970-1985)",           1420, 0.47, 1.800, 1.490, 2.800, 1.7, "185/70 R14", A.NONE,  0.80, "Cd ja rõhk hinnang; trummelpidurid kõigil ratastel; tehases diagonaalrehv 7.35-14; tehasemõõt 7.35-14 / 205/70 R14, mille kohta märgise andmeid praktiliselt ei ole; arvutus lähima levinud mõõduga 185/70 R14"),
    ("gaz_31029",       "GAZ Volga 31029/3110 2.4 (1992-2004)",   1400, 0.46, 1.800, 1.476, 2.800, 2.0, "185/70 R14", A.NONE,  0.85, "Cd GAZ-3110 järgi; tehasemõõt 205/70 R14, mille kohta märgise andmeid ei ole; arvutus lähima levinud mõõduga 185/70 R14"),
    ("zaz_tavria",      "ZAZ Tavria 1102 1.1 (1987-2007)",         727, 0.40, 1.554, 1.410, 2.320, 2.0, "155/70 R13", A.NONE,  0.88, "Cd hinnang"),
    ("uaz_469",         "UAZ 469/3151 2.4 (1972-2003)",           1540, 0.60, 1.785, 2.015, 2.380, 1.8, "225/75 R16C", A.NONE,  0.75, "Cd hinnang (kandiline maastur); trummelpidurid; tehases diagonaalrehv 8.40-15, siin hilisem 3151 mõõt; arvutus C-rehviga 225/75 R16C, mida UAZ-il sageli kasutatakse"),
]

# ÜLDISED AUTOD neile, kes oma autot nimekirjast ei leia. Kerekuju järgi
# tüüpilised väärtused, ABS-i põlvkond pargi keskmise järgi (2005-2014).
# Mõõtu saab valikust muuta — rehvimõõt on kirjas rehvi küljel.
_Y = "üldine tüüpauto, mitte konkreetne mudel"
EE_VEHICLES += [
    ("yld_vaike",     "Väikeauto (tüüpiline, nt Yaris, Polo, Fabia)",  1100, 0.32, 1.720, 1.480, 2.520, 2.3, "185/65 R15", A.MODERN, 1.24, _Y),
    ("yld_kompakt",   "Kompaktauto (tüüpiline, nt Golf, Octavia, Corolla)",1350,0.30,1.790,1.460,2.650,2.3,"205/55 R16", A.MODERN, 1.28, _Y),
    ("yld_keskklass", "Keskklass / universaal (tüüpiline, nt Passat, 5-seeria)",1550,0.29,1.830,1.470,2.800,2.4,"215/55 R17",A.MODERN,1.28, _Y),
    ("yld_maastur",   "Maastur / linnamaastur (tüüpiline, nt RAV4, Tiguan)",1650,0.34,1.840,1.670,2.680,2.4,"225/65 R17",A.MODERN,1.24, _Y),
    ("yld_kaubik",    "Kaubik / mahtuniversaal (tüüpiline)",            1900, 0.35, 1.900, 1.900, 3.000, 2.8, "215/65 R16", A.MODERN, 1.18, _Y),
]

# ---------------------------------------------------------------------------
# 2026-09-28 NELJAS RING: puuduvad mudelid (BMW 7-seeria, 4-seeria, X4, X6,
# X7, iX, i4; Audi A7, A8, Q2, Q8; Mercedes S W220/W222/W223, CLA, CLS, GL,
# GLS, GLB, V-klass; Range Rover; Porsche; Toyota jt). Sama põhimõte mis
# kolmandal ringil: mudeliaasta, ABS-i põlvkond ja tehasemõõdud (allikaga,
# oem_sizes.py) on teada; mass, mõõtmed ja Cd on spetsifikatsioonilehtedelt
# (auto-data, ultimatespecs) -- mass võib olla DIN (ilma juhita), rõhk ja
# puuduv Cd on keretüübi järgi hinnatud (märkuses kirjas). Pidurdusmaa
# jaoks loeb peamiselt ABS-i põlvkond ja rehv.
# ---------------------------------------------------------------------------
_L4 = "mõõdud spetsifikatsioonilehelt, mass võib olla DIN"
EE_VEHICLES += [
    ("bmw_730d_e65", "BMW 730d E65 (2001-2008)", 1900, 0.28, 1.902, 1.492, 2.990, 2.0, "245/55 R17", A.EARLY, 1.24, _L4),
    ("bmw_730d_f01", "BMW 730d F01 (2008-2015)", 1940, 0.29, 1.902, 1.479, 3.070, 2.4, "245/55 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("bmw_730d_g11", "BMW 730d G11 (2015-2022)", 1830, 0.24, 1.902, 1.478, 3.070, 2.4, "245/50 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("bmw_740d_g70", "BMW 740d G70 (2022+)", 2255, 0.26, 1.950, 1.544, 3.215, 2.4, "245/50 R19", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("bmw_420d_f32", "BMW 420d F32 (2013-2020)", 1575, 0.28, 1.825, 1.377, 2.810, 2.4, "225/50 R17", A.MODERN, 1.3, _L4 + "; rõhk hinnang"),
    ("bmw_420d_g22", "BMW 420d G22 (2020+)", 1693, 0.25, 1.852, 1.383, 2.851, 2.4, "225/50 R17", A.LATEST, 1.32, _L4 + "; rõhk hinnang"),
    ("bmw_x4_f26", "BMW X4 xDrive20d F26 (2014-2018)", 1745, 0.33, 1.881, 1.624, 2.810, 2.4, "225/60 R17", A.MODERN, 1.26, _L4 + "; rõhk hinnang"),
    ("bmw_x4_g02", "BMW X4 xDrive20d G02 (2018+)", 1829, 0.31, 1.918, 1.621, 2.864, 2.4, "225/60 R18", A.LATEST, 1.28, _L4 + "; rõhk hinnang"),
    ("bmw_x6_e71", "BMW X6 xDrive30d E71 (2008-2014)", 2075, 0.33, 1.983, 1.690, 2.933, 2.4, "255/50 R19", A.MODERN, 1.24, _L4 + "; rõhk hinnang"),
    ("bmw_x6_f16", "BMW X6 xDrive30d F16 (2014-2019)", 2140, 0.32, 1.989, 1.702, 2.933, 2.4, "255/50 R19", A.MODERN, 1.26, _L4 + "; rõhk hinnang"),
    ("bmw_x6_g06", "BMW X6 xDrive30d G06 (2019+)", 2110, 0.32, 2.004, 1.696, 2.975, 2.4, "265/50 R19", A.LATEST, 1.28, _L4 + "; rõhk hinnang"),
    ("bmw_x7_g07", "BMW X7 xDrive40d G07 (2019+)", 2470, 0.33, 2.000, 1.805, 3.105, 2.4, "275/50 R20", A.LATEST, 1.26, _L4 + "; rõhk hinnang"),
    ("bmw_ix", "BMW iX xDrive40 (2021+)", 2440, 0.25, 1.967, 1.695, 3.000, 2.4, "235/60 R20", A.LATEST, 1.28, _L4 + "; rõhk hinnang"),
    ("bmw_i4", "BMW i4 eDrive40 G26 (2021+)", 2125, 0.24, 1.852, 1.448, 2.856, 2.4, "225/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("audi_a8_d3", "Audi A8 D3 3.0 TDI (2002-2010)", 1830, 0.28, 1.894, 1.444, 2.944, 2.2, "235/55 R17", A.EARLY, 1.24, _L4),
    ("audi_a8_d4", "Audi A8 D4 3.0 TDI (2010-2017)", 1840, 0.26, 1.949, 1.460, 2.992, 2.4, "235/60 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("audi_a8_d5", "Audi A8 D5 3.0 TDI (2017+)", 1975, 0.26, 1.945, 1.473, 2.998, 2.4, "235/55 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("audi_a7_c7", "Audi A7 C7 3.0 TDI (2010-2018)", 1785, 0.29, 1.911, 1.420, 2.914, 2.4, "255/45 R18", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("audi_a7_c8", "Audi A7 C8 3.0 TDI (2018+)", 1880, 0.27, 1.908, 1.422, 2.926, 2.4, "225/55 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("audi_q2", "Audi Q2 1.0 TFSI (2016+)", 1300, 0.31, 1.794, 1.508, 2.601, 2.4, "215/60 R16", A.LATEST, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("audi_q8", "Audi Q8 3.0 TDI (2018+)", 2145, 0.34, 1.995, 1.705, 2.995, 2.4, "265/55 R19", A.LATEST, 1.26, _L4 + "; rõhk hinnang"),
    ("mb_s_w220", "Mercedes S320 CDI W220 (1998-2005)", 1830, 0.28, 1.855, 1.444, 2.965, 2.4, "225/60 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("mb_s_w222", "Mercedes S350d W222 (2013-2020)", 1880, 0.24, 1.899, 1.496, 3.035, 2.4, "245/55 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("mb_s_w223", "Mercedes S350d W223 (2020+)", 1945, 0.22, 1.921, 1.503, 3.106, 2.4, "255/50 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("mb_cla_c117", "Mercedes CLA 200 C117 (2013-2019)", 1395, 0.23, 1.777, 1.432, 2.699, 2.4, "205/55 R16", A.MODERN, 1.3, _L4 + "; rõhk hinnang"),
    ("mb_cls_c218", "Mercedes CLS 350 CDI C218 (2011-2018)", 1740, 0.28, 1.881, 1.416, 2.874, 2.4, "245/45 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("mb_gl_x164", "Mercedes GL 350 CDI X164 (2006-2012)", 2450, 0.37, 1.920, 1.840, 3.075, 2.2, "265/60 R18", A.MODERN, 1.18, _L4),
    ("mb_gls_x166", "Mercedes GLS 350 d X166 (2012-2019)", 2380, 0.35, 1.934, 1.850, 3.075, 2.4, "265/60 R18", A.MODERN, 1.2, _L4 + "; rõhk hinnang"),
    ("mb_gls_x167", "Mercedes GLS 400 d X167 (2019+)", 2430, 0.32, 1.956, 1.823, 3.135, 2.4, "275/55 R19", A.LATEST, 1.24, _L4 + "; rõhk hinnang"),
    ("mb_glb_x247", "Mercedes GLB 200 X247 (2019+)", 1564, 0.31, 1.834, 1.658, 2.829, 2.4, "215/65 R17", A.LATEST, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_v_w447", "Mercedes V-klass 250 d W447 (2014+)", 2145, 0.33, 1.928, 1.880, 3.200, 2.6, "225/55 R17", A.MODERN, 1.18, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_amarok_1", "VW Amarok 2.0 TDI (2010-2022)", 1957, 0.4, 1.944, 1.834, 3.095, 2.0, "245/70 R16", A.MODERN, 1.16, _L4 + "; Cd hinnang"),
    ("vw_scirocco_3", "VW Scirocco III 2.0 TSI (2008-2017)", 1373, 0.34, 1.810, 1.404, 2.578, 2.3, "225/45 R17", A.MODERN, 1.3, _L4),
    ("vw_passat_cc", "VW Passat CC 2.0 TDI (2008-2016)", 1541, 0.29, 1.855, 1.417, 2.711, 2.4, "235/45 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("vw_taigo", "VW Taigo 1.0 TSI (2021+)", 1243, 0.32, 1.757, 1.494, 2.566, 2.4, "205/60 R16", A.LATEST, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_touareg_3", "VW Touareg III 3.0 TDI (2018+)", 2070, 0.32, 1.984, 1.717, 2.904, 2.4, "235/65 R18", A.LATEST, 1.26, _L4 + "; rõhk hinnang"),
    ("porsche_cayenne_9pa", "Porsche Cayenne 4.5 (2002-2010)", 2225, 0.39, 1.928, 1.699, 2.855, 2.0, "255/55 R18", A.EARLY, 1.24, _L4),
    ("porsche_cayenne_9y0", "Porsche Cayenne 3.0 (2017+)", 1985, 0.34, 1.983, 1.696, 2.895, 2.4, "255/55 R19", A.LATEST, 1.32, _L4 + "; rõhk hinnang"),
    ("toyota_camry_xv70", "Toyota Camry XV70 2.5 Hybrid (2019+)", 1570, 0.28, 1.840, 1.445, 2.825, 2.4, "215/55 R17", A.LATEST, 1.28, _L4 + "; Cd hinnang"),
    ("toyota_corolla_cross", "Toyota Corolla Cross 2.0 Hybrid (2022+)", 1470, 0.32, 1.825, 1.620, 2.640, 2.4, "215/60 R17", A.LATEST, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_highlander_4", "Toyota Highlander XU70 2.5 Hybrid (2021+)", 2107, 0.34, 1.930, 1.755, 2.850, 2.6, "235/55 R20", A.LATEST, 1.24, _L4 + "; Cd hinnang"),
    ("toyota_lc_100", "Toyota Land Cruiser 100 (1998-2007)", 2650, 0.4, 1.940, 1.860, 2.850, 2.4, "275/70 R16", A.EARLY, 1.14, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_lc_200", "Toyota Land Cruiser 200 (2007-2021)", 2600, 0.35, 1.970, 1.865, 2.850, 2.4, "285/60 R18", A.MODERN, 1.16, _L4 + "; rõhk hinnang"),
    ("kia_xceed", "Kia XCeed 1.5 T-GDi (2019+)", 1400, 0.31, 1.826, 1.495, 2.650, 2.2, "205/60 R16", A.LATEST, 1.28, _L4 + "; Cd hinnang"),
    ("kia_stonic", "Kia Stonic 1.0 T-GDi (2017+)", 1185, 0.33, 1.760, 1.520, 2.580, 2.3, "185/65 R15", A.LATEST, 1.26, _L4 + "; Cd hinnang"),
    ("hyundai_bayon", "Hyundai Bayon 1.0 T-GDi (2021+)", 1150, 0.32, 1.775, 1.500, 2.580, 2.2, "195/55 R16", A.LATEST, 1.26, _L4 + "; Cd hinnang"),
    ("lr_rr_l322", "Land Rover Range Rover L322 3.6 TDV8 (2002-2012)", 2774, 0.39, 1.923, 1.877, 2.880, 2.4, "255/55 R19", A.EARLY, 1.14, _L4 + "; rõhk hinnang"),
    ("lr_rr_l405", "Land Rover Range Rover L405 3.0 SDV6 (2012-2021)", 2235, 0.34, 1.983, 1.835, 2.922, 2.4, "235/65 R19", A.MODERN, 1.2, _L4 + "; rõhk hinnang"),
    ("lr_rrs_l494", "Range Rover Sport L494 3.0 SDV6 (2013-2022)", 2190, 0.34, 1.983, 1.780, 2.923, 2.4, "235/65 R19", A.MODERN, 1.2, _L4 + "; rõhk hinnang"),
    ("lr_defender_l663", "Land Rover Defender L663 (2020+)", 2340, 0.41, 1.996, 1.967, 3.022, 2.4, "255/65 R19", A.LATEST, 1.2, _L4 + "; rõhk hinnang"),
    ("porsche_panamera_971", "Porsche Panamera 971 2.9 (2016+)", 1865, 0.29, 1.937, 1.423, 2.950, 2.4, "265/45 R19", A.LATEST, 1.34, _L4 + "; rõhk hinnang"),
    ("porsche_taycan", "Porsche Taycan 4S (2019+)", 2140, 0.22, 1.966, 1.379, 2.900, 2.4, "225/55 R19", A.LATEST, 1.34, _L4 + "; rõhk hinnang"),
    ("tesla_modelx", "Tesla Model X Long Range (2015+)", 2352, 0.25, 1.999, 1.684, 2.965, 2.9, "255/45 R20", A.LATEST, 1.28, _L4),
    ("volvo_s90_2", "Volvo S90 II D4 (2016+)", 1800, 0.28, 1.879, 1.443, 2.941, 2.4, "245/45 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_c30", "Volvo C30 1.6 (2006-2013)", 1279, 0.3, 1.782, 1.447, 2.640, 2.4, "195/65 R15", A.MODERN, 1.26, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mitsu_eclipse_cross", "Mitsubishi Eclipse Cross 1.5 (2017+)", 1507, 0.34, 1.805, 1.685, 2.670, 2.4, "225/55 R18", A.LATEST, 1.26, _L4 + "; Cd hinnang"),
    ("ford_mach_e", "Ford Mustang Mach-E AWD (2021+)", 2182, 0.29, 1.881, 1.624, 2.984, 2.4, "225/55 R19", A.LATEST, 1.28, _L4 + "; rõhk hinnang"),
    ("peugeot_108", "Peugeot 108 1.0 (2014-2022)", 840, 0.31, 1.615, 1.460, 2.340, 2.3, "165/65 R14", A.MODERN, 1.24, _L4 + "; Cd hinnang"),
    ("citroen_c1_2", "Citroën C1 II 1.0 (2014-2022)", 840, 0.31, 1.615, 1.460, 2.340, 2.3, "165/65 R14", A.MODERN, 1.24, _L4 + "; Cd hinnang"),
    ("renault_arkana", "Renault Arkana 1.3 TCe (2021+)", 1336, 0.31, 1.820, 1.576, 2.720, 2.4, "215/60 R17", A.LATEST, 1.28, _L4 + "; Cd hinnang"),
]

# 2026-09-28: kasutajate teated puuduvatest autodest
EE_VEHICLES += [
    ("bmw_535d_e61", "BMW 535d E61 Touring (2004-2010)", 1835, 0.29, 1.846, 1.491, 2.886, 2.4, "245/45 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
]

# 2026-09-28 viies ring: levinud lüngad, uued 2022+ autod, sportautod
EE_VEHICLES += [
    ("kia_sportage_2", "Kia Sportage II 2.0 CRDi (2004-2010)", 1587, 0.34, 1.840, 1.730, 2.630, 2.2, "235/60 R16", A.MODERN, 1.25, _L4 + "; Cd hinnang"),
    ("renault_captur_1", "Renault Captur I 0.9 TCe (2013-2019)", 1164, 0.34, 1.778, 1.566, 2.606, 2.3, "205/60 R16", A.MODERN, 1.25, _L4 + "; Cd hinnang"),
    ("hyundai_santafe_dm", "Hyundai Santa Fe DM 2.2 CRDi (2012-2018)", 1770, 0.34, 1.880, 1.680, 2.700, 2.3, "235/65 R17", A.MODERN, 1.25, _L4),
    ("mazda_cx7", "Mazda CX-7 2.2 MZR-CD (2007-2012)", 1790, 0.34, 1.870, 1.645, 2.750, 2.4, "235/60 R18", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_xc70_2", "Volvo XC70 II D5 (2000-2007)", 1695, 0.34, 1.860, 1.562, 2.763, 2.4, "215/65 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("volvo_v40_1", "Volvo V40 I 1.8 (1995-2004)", 1303, 0.31, 1.720, 1.410, 2.550, 2.4, "195/55 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_ml_w163", "Mercedes ML 270 CDI W163 (1997-2005)", 2100, 0.39, 1.840, 1.820, 2.820, 2.4, "255/60 R17", A.EARLY, 1.16, _L4 + "; rõhk hinnang"),
    ("nissan_note_e12", "Nissan Note E12 1.2 (2013-2020)", 1185, 0.32, 1.695, 1.535, 2.600, 2.3, "185/65 R15", A.MODERN, 1.28, _L4 + "; Cd hinnang"),
    ("nissan_juke_f16", "Nissan Juke F16 1.0 DIG-T (2019+)", 1192, 0.34, 1.800, 1.595, 2.636, 2.4, "215/60 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_micra_k13", "Nissan Micra K13 1.2 (2010-2017)", 910, 0.32, 1.675, 1.525, 2.450, 2.3, "165/70 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("hyundai_i20_3", "Hyundai i20 III 1.0 T-GDi (2020+)", 1130, 0.32, 1.775, 1.450, 2.580, 2.2, "195/55 R16", A.LATEST, 1.3, _L4 + "; mass hinnang, Cd hinnang"),
    ("hyundai_ioniq", "Hyundai Ioniq 1.6 Hybrid (2016-2022)", 1370, 0.24, 1.820, 1.450, 2.700, 2.4, "195/65 R15", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("mazda_2_de", "Mazda 2 DE 1.3 (2007-2014)", 955, 0.31, 1.695, 1.475, 2.490, 2.3, "175/65 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("opel_meriva_a", "Opel Meriva A 1.6 (2003-2010)", 1375, 0.31, 1.694, 1.624, 2.630, 2.4, "185/60 R15", A.EARLY, 1.24, _L4 + "; Cd hinnang"),
    ("toyota_yaris_xp10", "Toyota Yaris XP10 1.0 (1999-2005)", 855, 0.32, 1.660, 1.500, 2.370, 1.9, "175/65 R14", A.EARLY, 1.24, _L4 + "; Cd hinnang"),
    ("seat_leon_4", "SEAT Leon IV 1.5 TSI (2020+)", 1322, 0.31, 1.800, 1.456, 2.686, 2.4, "205/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("suzuki_swift_5", "Suzuki Swift V 1.2 (2017-2024)", 915, 0.32, 1.735, 1.495, 2.450, 2.3, "175/65 R15", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_jazz_3", "Honda Jazz III 1.3 (2015-2020)", 1141, 0.32, 1.694, 1.525, 2.530, 2.3, "185/60 R15", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_clio_2", "Renault Clio II 1.2 (1998-2012)", 975, 0.35, 1.639, 1.417, 2.472, 2.0, "175/65 R14", A.EARLY, 1.24, _L4),
    ("subaru_impreza_gh", "Subaru Impreza GH 1.5 (2007-2011)", 1310, 0.31, 1.740, 1.475, 2.620, 2.4, "195/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_forester_sk", "Subaru Forester SK 2.0 e-Boxer (2018+)", 1655, 0.34, 1.815, 1.730, 2.670, 2.4, "225/60 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_smax_2", "Ford S-Max II 2.0 TDCi (2015-2023)", 1725, 0.31, 1.916, 1.655, 2.849, 2.4, "235/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lexus_ct", "Lexus CT 200h (2011-2022)", 1420, 0.31, 1.765, 1.440, 2.600, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("skoda_superb_4", "Škoda Superb IV 2.0 TDI (2024+)", 1662, 0.234, 1.849, 1.481, 2.841, 2.4, "215/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("skoda_kodiaq_2", "Škoda Kodiaq II 2.0 TDI (2024+)", 1730, 0.285, 1.864, 1.659, 2.791, 2.4, "215/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("skoda_elroq", "Škoda Elroq 85 (2025+)", 2119, 0.267, 1.884, 1.608, 2.769, 2.4, "235/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("mb_e_w214", "Mercedes E220 d W214 (2023+)", 1915, 0.23, 1.880, 1.468, 2.961, 2.4, "225/55 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("mb_glc_x254", "Mercedes GLC 220 d X254 (2022+)", 1925, 0.29, 1.890, 1.640, 2.888, 2.4, "235/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("mb_eqa", "Mercedes EQA 250 H243 (2021+)", 2040, 0.28, 1.834, 1.620, 2.729, 2.4, "235/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("bmw_x1_u11", "BMW X1 sDrive18d U11 (2022+)", 1575, 0.26, 1.845, 1.642, 2.692, 2.4, "205/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("bmw_x3_g45", "BMW X3 xDrive20d G45 (2024+)", 1890, 0.28, 1.920, 1.660, 2.865, 2.4, "225/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("toyota_lc_250", "Toyota Land Cruiser 250 (2024+)", 2335, 0.36, 1.980, 1.925, 2.850, 2.4, "265/70 R18", A.LATEST, 1.22, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_aygo_x", "Toyota Aygo X 1.0 (2022+)", 940, 0.32, 1.740, 1.525, 2.430, 2.6, "175/65 R17", A.LATEST, 1.3, _L4 + "; Cd hinnang"),
    ("kia_sorento_4", "Kia Sorento IV 1.6 T-GDi HEV (2020+)", 1741, 0.34, 1.900, 1.695, 2.815, 2.4, "235/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_niro_2", "Kia Niro II HEV (2022+)", 1490, 0.285, 1.825, 1.545, 2.720, 2.4, "205/60 R16", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("bmw_m3_e90", "BMW M3 4.0 E90 (2007-2013)", 1580, 0.31, 1.804, 1.418, 2.761, 2.4, "245/40 R18", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("bmw_m3_f80", "BMW M3 3.0 F80 (2014-2018)", 1520, 0.34, 1.877, 1.424, 2.812, 2.4, "255/40 R18", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("bmw_m3_g80", "BMW M3 Competition G80 (2021+)", 1730, 0.33, 1.903, 1.433, 2.857, 2.2, "275/40 R18", A.LATEST, 1.4, _L4),
    ("bmw_m5_f90", "BMW M5 4.4 F90 (2018-2024)", 1855, 0.33, 1.903, 1.473, 2.982, 2.4, "275/40 R19", A.LATEST, 1.4, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("audi_rs3_8v", "Audi RS3 8V 2.5 TFSI (2015-2020)", 1520, 0.34, 1.800, 1.411, 2.631, 2.4, "235/35 R19", A.LATEST, 1.4, _L4 + "; rõhk hinnang"),
    ("audi_rs6_c8", "Audi RS6 C8 4.0 TFSI (2019+)", 2075, 0.35, 1.886, 1.467, 2.924, 2.4, "275/35 R21", A.LATEST, 1.4, _L4 + "; rõhk hinnang"),
    ("subaru_wrx_sti_va", "Subaru WRX STI VA (2014-2021)", 1500, 0.33, 1.795, 1.475, 2.650, 2.3, "245/40 R18", A.MODERN, 1.36, _L4 + "; Cd hinnang"),
    ("mitsu_lancer_evo_x", "Mitsubishi Lancer Evolution X (2007-2016)", 1560, 0.33, 1.810, 1.480, 2.650, 2.4, "245/40 R18", A.MODERN, 1.36, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("porsche_911_991", "Porsche 911 Carrera 991 (2011-2019)", 1455, 0.29, 1.808, 1.303, 2.450, 2.3, "235/40 R19", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("porsche_911_992", "Porsche 911 Carrera 992 (2019+)", 1580, 0.29, 1.852, 1.298, 2.450, 2.3, "235/40 R19", A.LATEST, 1.4, _L4 + "; rõhk hinnang"),
]

# 2026-09-28 viies ring, teine osa (+ kasutaja soov: BMW 330e)
EE_VEHICLES += [
    ("lexus_rx_xu30", "Lexus RX 400h XU30 (2003-2009)", 2000, 0.33, 1.845, 1.680, 2.720, 2.4, "235/55 R18", A.EARLY, 1.21, _L4 + "; rõhk hinnang"),
    ("toyota_rav4_2", "Toyota RAV4 II 2.0 (2000-2005)", 1330, 0.35, 1.735, 1.705, 2.490, 1.8, "215/70 R16", A.EARLY, 1.21, _L4),
    ("honda_crv_2", "Honda CR-V II 2.0 (2001-2006)", 1485, 0.34, 1.780, 1.710, 2.620, 1.8, "205/70 R15", A.EARLY, 1.21, _L4 + "; Cd hinnang"),
    ("vw_jetta_5", "VW Jetta V 1.9 TDI (2005-2010)", 1345, 0.31, 1.781, 1.459, 2.578, 2.1, "205/55 R16", A.MODERN, 1.28, _L4 + "; Cd hinnang"),
    ("ford_fiesta_5", "Ford Fiesta V 1.4 (2002-2008)", 1030, 0.32, 1.683, 1.417, 2.487, 2.0, "175/65 R14", A.EARLY, 1.24, _L4 + "; Cd hinnang"),
    ("peugeot_5008_1", "Peugeot 5008 I 1.6 HDi (2009-2016)", 1472, 0.32, 1.837, 1.647, 2.727, 2.4, "215/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("citroen_c4_1", "Citroën C4 I 1.6 HDi (2004-2010)", 1270, 0.29, 1.773, 1.471, 2.608, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("citroen_c4_picasso_1", "Citroën C4 Picasso I 1.6 HDi (2006-2013)", 1489, 0.31, 1.830, 1.660, 2.728, 2.4, "205/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("audi_a5_f5", "Audi A5 F5 2.0 TDI (2016-2024)", 1520, 0.28, 1.843, 1.386, 2.824, 2.4, "225/50 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("opel_crossland", "Opel Crossland X 1.2 (2017-2024)", 1170, 0.34, 1.765, 1.605, 2.604, 2.4, "195/60 R16", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("audi_q4_etron", "Audi Q4 e-tron 40 (2021+)", 2050, 0.28, 1.865, 1.632, 2.764, 2.4, "235/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("volvo_ex30", "Volvo EX30 (2024+)", 1775, 0.28, 1.837, 1.549, 2.650, 2.6, "225/55 R18", A.LATEST, 1.27, _L4),
    ("vw_id7", "VW ID.7 Pro (2023+)", 2172, 0.23, 1.862, 1.538, 2.966, 2.4, "235/50 R19", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("vw_passat_b9", "VW Passat B9 2.0 TDI (2024+)", 1678, 0.25, 1.849, 1.497, 2.841, 2.4, "215/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("byd_seal", "BYD Seal AWD (2023+)", 2260, 0.219, 1.875, 1.460, 2.920, 2.4, "235/45 R19", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("byd_dolphin", "BYD Dolphin (2023+)", 1733, 0.301, 1.770, 1.570, 2.700, 2.4, "205/50 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("mg_hs", "MG HS 1.5 T-GDI (2019-2024)", 1489, 0.34, 1.876, 1.664, 2.720, 2.4, "215/60 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_ev3", "Kia EV3 Long Range (2024+)", 1885, 0.34, 1.850, 1.560, 2.680, 2.4, "215/60 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("hyundai_kona_2", "Hyundai Kona II 1.6 HEV (2023+)", 1410, 0.34, 1.825, 1.585, 2.660, 2.4, "215/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_xtrail_t33", "Nissan X-Trail T33 e-Power (2022+)", 1778, 0.34, 1.840, 1.720, 2.705, 2.4, "235/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_austral", "Renault Austral 1.2 E-Tech (2023+)", 1592, 0.34, 1.825, 1.618, 2.667, 2.4, "205/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("opel_mokka_b", "Opel Mokka B 1.2 (2020+)", 1279, 0.32, 1.791, 1.531, 2.557, 2.4, "215/65 R16", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("subaru_outback_bt", "Subaru Outback BT 2.5 (2021+)", 1757, 0.31, 1.875, 1.675, 2.745, 2.4, "225/60 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("tesla_model3_highland", "Tesla Model 3 Highland RWD (2024+)", 1836, 0.219, 1.849, 1.441, 2.875, 2.4, "235/45 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("dacia_duster_3", "Dacia Duster III 1.2 TCe (2024+)", 1379, 0.34, 1.813, 1.656, 2.657, 2.4, "215/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("cupra_born", "Cupra Born (2021+)", 1811, 0.29, 1.809, 1.540, 2.766, 2.3, "215/55 R18", A.LATEST, 1.3, _L4 + "; Cd hinnang"),
    ("peugeot_3008_3", "Peugeot 3008 III 1.2 Hybrid (2024+)", 1648, 0.28, 1.895, 1.641, 2.739, 2.4, "225/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("vw_golf_gti_7", "VW Golf GTI VII 2.0 TSI (2013-2020)", 1306, 0.33, 1.799, 1.442, 2.631, 2.4, "225/45 R17", A.MODERN, 1.36, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_golf_r_8", "VW Golf 8 R 2.0 TSI (2021+)", 1476, 0.33, 1.789, 1.458, 2.628, 2.4, "225/40 R18", A.LATEST, 1.4, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_civic_typer_fk8", "Honda Civic Type-R FK8 (2017-2021)", 1305, 0.33, 1.877, 1.434, 2.699, 2.4, "245/30 R20", A.LATEST, 1.4, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("porsche_cayman_982", "Porsche 718 Cayman 982 (2016+)", 1365, 0.3, 1.801, 1.286, 2.475, 2.3, "235/45 R18", A.LATEST, 1.4, _L4 + "; rõhk hinnang"),
    ("toyota_gr86", "Toyota GR86 2.4 (2022+)", 1276, 0.33, 1.775, 1.310, 2.575, 2.4, "215/40 R18", A.LATEST, 1.4, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_supra_a90", "Toyota Supra A90 3.0 (2019+)", 1502, 0.33, 1.854, 1.292, 2.470, 2.4, "255/35 R19", A.LATEST, 1.4, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_c63_w205", "Mercedes C63 AMG W205 (2015-2021)", 1640, 0.33, 1.839, 1.426, 2.840, 2.4, "245/40 R18", A.LATEST, 1.4, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mazda_mx5_nd", "Mazda MX-5 ND 2.0 (2015+)", 1025, 0.33, 1.735, 1.230, 2.310, 2.4, "205/45 R17", A.LATEST, 1.4, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_transit_connect_2", "Ford Transit Connect II kaubik (2013-2022)", 1382, 0.35, 1.835, 1.861, 2.662, 2.5, "205/60 R16", A.MODERN, 1.12, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("ford_transit_8", "Ford Transit VIII kaubik (2014+)", 2124, 0.37, 2.059, 2.490, 3.300, 2.8, "215/65 R15C", A.MODERN, 1.08, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("opel_vivaro_b", "Opel Vivaro B kaubik (2014-2019)", 2034, 0.37, 1.956, 1.971, 3.098, 2.8, "205/65 R16C", A.MODERN, 1.08, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("opel_vivaro_c", "Opel Vivaro C kaubik (2019+)", 1690, 0.37, 1.920, 1.895, 3.275, 2.8, "215/65 R16C", A.LATEST, 1.12, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("renault_trafic_3", "Renault Trafic III kaubik (2014+)", 1857, 0.37, 1.956, 1.971, 3.098, 2.8, "205/65 R16C", A.MODERN, 1.08, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("renault_kangoo_3", "Renault Kangoo III (2021+)", 1493, 0.35, 1.860, 1.864, 2.716, 2.5, "195/65 R15", A.LATEST, 1.16, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("citroen_jumper_3", "Citroën Jumper III kaubik (2006+)", 2113, 0.37, 2.050, 2.524, 4.035, 2.8, "215/70 R15C", A.MODERN, 1.08, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("mb_citan_w415", "Mercedes Citan 109 CDI W415 (2012-2021)", 1429, 0.35, 1.830, 1.820, 2.697, 2.5, "185/70 R14", A.MODERN, 1.12, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("peugeot_expert_3", "Peugeot Expert III kaubik (2016+)", 1725, 0.37, 1.920, 1.895, 3.275, 2.8, "215/65 R16C", A.LATEST, 1.12, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("vw_transporter_t6", "VW Transporter T6 kaubik (2015-2019)", 1722, 0.37, 1.904, 1.950, 3.000, 2.8, "205/65 R16C", A.LATEST, 1.12, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("bmw_330e_f30", "BMW 330e F30 (2012-2019)", 1660, 0.27, 1.811, 1.429, 2.810, 2.4, "205/60 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("bmw_330e_g20", "BMW 330e G20 (2020)", 1740, 0.25, 1.827, 1.444, 2.851, 2.4, "225/50 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
]

# 2026-09-28 kuues ring: mootorivariandid (kere baasrealt) ja uued mudelid
EE_VEHICLES += [
    ("bmw_330d_e90", "BMW 330d E90 (2005-2012)", 1625, 0.29, 1.817, 1.421, 2.760, 2.3, "225/45 R17", A.MODERN, 1.3, _L4 + "; kere ja mõõdud baasrealt bmw_320d_e90, rõhk baasrealt"),
    ("bmw_330d_f30", "BMW 330d F30 (2012-2019)", 1615, 0.28, 1.811, 1.429, 2.810, 2.4, "225/50 R17", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt bmw_320d_f30, rõhk baasrealt"),
    ("bmw_318d_f30", "BMW 318d F30 (2012-2019)", 1410, 0.26, 1.811, 1.429, 2.810, 2.4, "205/60 R16", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt bmw_320d_f30, rõhk baasrealt"),
    ("bmw_320i_g20", "BMW 320i G20 (2019+)", 1450, 0.278, 1.830, 1.421, 2.850, 2.4, "205/60 R16", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt bmw_320d, rõhk baasrealt"),
    ("bmw_530d_e60", "BMW 530d E60 (2003-2010)", 1595, 0.28, 1.846, 1.469, 2.888, 2.4, "225/55 R16", A.MODERN, 1.28, _L4 + "; kere ja mõõdud baasrealt bmw_520d_e60, rõhk baasrealt"),
    ("bmw_530d_f10", "BMW 530d F10 (2010-2017)", 1795, 0.28, 1.860, 1.464, 2.968, 2.5, "225/55 R17", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt bmw_520d_f10, rõhk baasrealt"),
    ("bmw_530d_g30", "BMW 530d G30 (2017-2023)", 1640, 0.24, 1.868, 1.466, 2.975, 2.5, "225/55 R17", A.LATEST, 1.32, _L4 + "; kere ja mõõdud baasrealt bmw_520d_g30, rõhk baasrealt"),
    ("bmw_530e_g30", "BMW 530e G30 (2017-2023)", 1770, 0.26, 1.868, 1.466, 2.975, 2.5, "225/55 R17", A.LATEST, 1.32, _L4 + "; kere ja mõõdud baasrealt bmw_520d_g30, rõhk baasrealt"),
    ("bmw_x5_45e_g05", "BMW X5 xDrive45e G05 (2018+)", 2435, 0.32, 2.004, 1.745, 2.975, 2.6, "265/50 R19", A.LATEST, 1.26, _L4 + "; kere ja mõõdud baasrealt bmw_x5_g05, rõhk baasrealt"),
    ("bmw_x3_30d_g01", "BMW X3 xDrive30d G01 (2017-2024)", 1820, 0.29, 1.891, 1.676, 2.864, 2.5, "225/60 R18", A.LATEST, 1.28, _L4 + "; kere ja mõõdud baasrealt bmw_x3_g01, rõhk baasrealt"),
    ("vw_passat_b6_19", "VW Passat B6 1.9 TDI (2005-2010)", 1422, 0.29, 1.820, 1.472, 2.709, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; kere ja mõõdud baasrealt vw_passat_b6, rõhk baasrealt"),
    ("vw_passat_b7_16", "VW Passat B7 1.6 TDI (2010-2014)", 1499, 0.29, 1.820, 1.470, 2.712, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; kere ja mõõdud baasrealt vw_passat_b7, rõhk baasrealt"),
    ("vw_passat_b8_14", "VW Passat B8 1.4 TSI (2014-2023)", 1387, 0.287, 1.830, 1.447, 2.790, 2.4, "215/60 R16", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt vw_passat_b8, rõhk baasrealt"),
    ("vw_passat_b8_gte", "VW Passat B8 GTE (2014-2023)", 1647, 0.287, 1.830, 1.447, 2.790, 2.4, "215/55 R17", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt vw_passat_b8, rõhk baasrealt"),
    ("vw_golf_7_14", "VW Golf VII 1.4 TSI (2012-2019)", 1225, 0.29, 1.799, 1.452, 2.637, 2.3, "205/55 R16", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt vw_golf_7, rõhk baasrealt"),
    ("vw_golf_7_20", "VW Golf VII 2.0 TDI (2012-2019)", 1354, 0.29, 1.799, 1.452, 2.637, 2.3, "205/55 R16", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt vw_golf_7, rõhk baasrealt"),
    ("vw_golf_6_14", "VW Golf VI 1.4 TSI (2008-2012)", 1215, 0.31, 1.779, 1.479, 2.578, 2.3, "205/55 R16", A.MODERN, 1.28, _L4 + "; kere ja mõõdud baasrealt vw_golf_6, rõhk baasrealt"),
    ("vw_golf_5_16", "VW Golf V 1.6 (2003-2008)", 1208, 0.32, 1.759, 1.485, 2.578, 2.3, "195/65 R15", A.MODERN, 1.28, _L4 + "; kere ja mõõdud baasrealt vw_golf_5, rõhk baasrealt"),
    ("skoda_octavia_3_16", "Škoda Octavia III 1.6 TDI (2013-2020)", 1230, 0.288, 1.814, 1.461, 2.686, 2.4, "195/65 R15", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt skoda_octavia_3, rõhk baasrealt"),
    ("skoda_octavia_3_14", "Škoda Octavia III 1.4 TSI (2013-2020)", 1180, 0.301, 1.814, 1.461, 2.686, 2.4, "195/65 R15", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt skoda_octavia_3, rõhk baasrealt"),
    ("skoda_octavia_3_rs", "Škoda Octavia III RS 2.0 TSI (2013-2020)", 1345, 0.28, 1.814, 1.461, 2.686, 2.4, "225/45 R17", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt skoda_octavia_3, rõhk baasrealt"),
    ("skoda_octavia_4_15", "Škoda Octavia IV 1.5 TSI (2020+)", 1263, 0.296, 1.830, 1.447, 2.690, 2.4, "205/60 R16", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt skoda_octavia, rõhk baasrealt"),
    ("skoda_superb_3_iv", "Škoda Superb III 1.4 TSI iV (2015-2023)", 1655, 0.268, 1.864, 1.468, 2.841, 2.4, "215/55 R17", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt skoda_superb_3, rõhk baasrealt"),
    ("skoda_superb_2_16", "Škoda Superb II 1.6 TDI (2008-2015)", 1442, 0.3, 1.817, 1.462, 2.761, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; kere ja mõõdud baasrealt skoda_superb_2, rõhk baasrealt"),
    ("skoda_kodiaq_1_15", "Škoda Kodiaq I 1.5 TSI (2016-2024)", 1582, 0.337, 1.882, 1.655, 2.791, 2.3, "215/65 R17", A.LATEST, 1.27, _L4 + "; kere ja mõõdud baasrealt skoda_kodiaq_1, rõhk baasrealt"),
    ("audi_a4_b8_18", "Audi A4 B8 1.8 TFSI (2008-2015)", 1410, 0.27, 1.826, 1.427, 2.808, 2.4, "205/60 R16", A.MODERN, 1.3, _L4 + "; kere ja mõõdud baasrealt audi_a4_b8, rõhk baasrealt"),
    ("audi_a4_b8_30", "Audi A4 B8 3.0 TDI (2008-2015)", 1655, 0.28, 1.826, 1.427, 2.808, 2.4, "225/50 R17", A.MODERN, 1.3, _L4 + "; kere ja mõõdud baasrealt audi_a4_b8, rõhk baasrealt"),
    ("audi_a6_c7_30", "Audi A6 C7 3.0 TDI (2011-2018)", 1720, 0.28, 1.874, 1.455, 2.912, 2.5, "225/55 R17", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt audi_a6_c7, rõhk baasrealt"),
    ("audi_a6_c6_30", "Audi A6 C6 3.0 TDI (2004-2011)", 1765, 0.3, 1.855, 1.459, 2.843, 2.3, "225/55 R16", A.MODERN, 1.28, _L4 + "; kere ja mõõdud baasrealt audi_a6_c6, rõhk baasrealt"),
    ("audi_q5_8r_30", "Audi Q5 8R 3.0 TDI (2008-2016)", 1865, 0.33, 1.880, 1.653, 2.807, 2.4, "235/60 R18", A.MODERN, 1.24, _L4 + "; kere ja mõõdud baasrealt audi_q5_8r, rõhk baasrealt"),
    ("mb_c200_w205", "Mercedes C200 W205 (2014-2021)", 1370, 0.24, 1.810, 1.442, 2.840, 2.4, "205/60 R16", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt mb_c220_w205, rõhk baasrealt"),
    ("mb_c200_w204", "Mercedes C200 CDI W204 (2007-2014)", 1485, 0.27, 1.770, 1.447, 2.760, 2.2, "195/60 R16", A.MODERN, 1.29, _L4 + "; kere ja mõõdud baasrealt mb_c220_w204, rõhk baasrealt"),
    ("mb_e350d_w213", "Mercedes E350 d W213 (2016-2023)", 1725, 0.27, 1.852, 1.468, 2.939, 2.5, "225/55 R17", A.LATEST, 1.32, _L4 + "; kere ja mõõdud baasrealt mb_e220_w213, rõhk baasrealt"),
    ("mb_e300de_w213", "Mercedes E300 de W213 (2016-2023)", 1985, 0.23, 1.852, 1.468, 2.939, 2.5, "245/45 R18", A.LATEST, 1.32, _L4 + "; kere ja mõõdud baasrealt mb_e220_w213, rõhk baasrealt"),
    ("mb_e350_w212", "Mercedes E350 CDI W212 (2009-2016)", 1750, 0.27, 1.854, 1.474, 2.874, 2.4, "225/55 R16", A.MODERN, 1.3, _L4 + "; kere ja mõõdud baasrealt mb_e220_w212, rõhk baasrealt"),
    ("toyota_corolla_e210_20", "Toyota Corolla E210 2.0 Hybrid (2019+)", 1340, 0.287, 1.830, 1.447, 2.700, 2.5, "205/55 R16", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt toyota_corolla"),
    ("toyota_avensis_t27_20", "Toyota Avensis T27 2.0 D-4D (2009-2018)", 1490, 0.28, 1.810, 1.480, 2.700, 2.4, "205/60 R16", A.LATEST, 1.28, _L4 + "; kere ja mõõdud baasrealt toyota_avensis_t27"),
    ("toyota_rav4_4_hyb", "Toyota RAV4 IV 2.5 Hybrid (2013-2018)", 1690, 0.32, 1.845, 1.660, 2.660, 2.2, "225/65 R17", A.LATEST, 1.25, _L4 + "; kere ja mõõdud baasrealt toyota_rav4_4"),
    ("toyota_rav4_5_phev", "Toyota RAV4 V Plug-in Hybrid (2019+)", 1910, 0.32, 1.855, 1.685, 2.690, 2.3, "225/60 R18", A.LATEST, 1.27, _L4 + "; kere ja mõõdud baasrealt toyota_rav4_5"),
    ("volvo_xc60_1_d5", "Volvo XC60 I D5 AWD (2008-2017)", 1736, 0.35, 1.891, 1.713, 2.774, 2.4, "235/65 R17", A.MODERN, 1.24, _L4 + "; kere ja mõõdud baasrealt volvo_xc60_1, rõhk baasrealt"),
    ("volvo_xc60_2_t8", "Volvo XC60 II T8 (2017+)", 2148, 0.313, 1.830, 1.789, 2.870, 2.5, "235/55 R19", A.LATEST, 1.3, _L4 + "; kere ja mõõdud baasrealt volvo_xc60, rõhk baasrealt"),
    ("volvo_xc90_2_t8", "Volvo XC90 II T8 (2015+)", 2249, 0.33, 2.008, 1.776, 2.984, 2.6, "235/55 R19", A.LATEST, 1.26, _L4 + "; kere ja mõõdud baasrealt volvo_xc90_2, rõhk baasrealt"),
    ("nissan_qashqai_j11_16", "Nissan Qashqai J11 1.6 dCi (2013-2021)", 1365, 0.32, 1.806, 1.590, 2.646, 2.3, "215/60 R17", A.LATEST, 1.26, _L4 + "; kere ja mõõdud baasrealt nissan_qashqai_j11, rõhk baasrealt"),
    ("kia_sportage_4_16", "Kia Sportage IV 1.6 T-GDi (2015-2021)", 1529, 0.33, 1.855, 1.645, 2.670, 2.4, "215/70 R16", A.LATEST, 1.28, _L4 + "; kere ja mõõdud baasrealt kia_sportage_4, rõhk baasrealt"),
    ("hyundai_tucson_nx4_phev", "Hyundai Tucson NX4 1.6 T-GDi PHEV (2020+)", 1818, 0.315, 1.865, 1.651, 2.680, 2.4, "235/50 R19", A.LATEST, 1.28, _L4 + "; kere ja mõõdud baasrealt hyundai_tucson_nx4, rõhk baasrealt"),
    ("ford_mondeo_4_20", "Ford Mondeo IV 2.0 TDCi (2007-2014)", 1456, 0.3, 1.886, 1.500, 2.850, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; kere ja mõõdud baasrealt ford_mondeo_4, rõhk baasrealt"),
    ("ford_focus_3_10", "Ford Focus III 1.0 EcoBoost (2011-2018)", 1327, 0.273, 1.823, 1.484, 2.648, 2.3, "205/55 R16", A.MODERN, 1.27, _L4 + "; kere ja mõõdud baasrealt ford_focus_3, rõhk baasrealt"),
    ("vw_id_buzz", "VW ID.Buzz Pro (2022+)", 2459, 0.285, 1.985, 1.927, 2.989, 2.4, "235/60 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("vw_id5", "VW ID.5 Pro (2021+)", 2117, 0.34, 1.852, 1.615, 2.771, 2.4, "235/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_multivan_t7", "VW Multivan T7 1.4 eHybrid (2022+)", 2120, 0.32, 1.941, 1.907, 3.124, 2.4, "235/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_golf_sportsvan", "VW Golf Sportsvan 1.4 TSI (2014-2020)", 1383, 0.32, 1.807, 1.578, 2.685, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_tiguan_allspace", "VW Tiguan Allspace 2.0 TDI (2017-2024)", 1708, 0.34, 1.839, 1.674, 2.787, 2.4, "215/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_beetle_a5", "VW Beetle A5 1.4 TSI (2011-2019)", 1347, 0.376, 1.808, 1.486, 2.537, 2.4, "215/55 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("toyota_rav4_1", "Toyota RAV4 I 2.0 (1994-2000)", 1224, 0.34, 1.700, 1.660, 2.410, 2.4, "215/70 R16", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_corolla_verso", "Toyota Corolla Verso 1.8 (2004-2009)", 1355, 0.3, 1.770, 1.620, 2.750, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("toyota_lc_90", "Toyota Land Cruiser 90 3.0 diisel (1996-2002)", 1885, 0.36, 1.820, 1.880, 2.675, 2.4, "215/80 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_prius_plus", "Toyota Prius+ 1.8 Hybrid (2012-2021)", 1575, 0.32, 1.775, 1.600, 2.780, 2.4, "205/60 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_proace_city", "Toyota Proace City (2019+)", 1347, 0.35, 1.848, 1.880, 2.785, 2.5, "205/60 R16", A.LATEST, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_prius_xw20", "Toyota Prius XW20 1.5 Hybrid (2003-2009)", 1300, 0.26, 1.725, 1.490, 2.700, 2.4, "185/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("bmw_x2_f39", "BMW X2 sDrive18d F39 (2018-2023)", 1500, 0.28, 1.824, 1.526, 2.670, 2.4, "225/55 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("bmw_218i_gc_f44", "BMW 218i Gran Coupe F44 (2019+)", 1350, 0.25, 1.800, 1.420, 2.670, 2.4, "205/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("bmw_218i_at_u06", "BMW 218i Active Tourer U06 (2022+)", 1470, 0.26, 1.824, 1.576, 2.670, 2.4, "205/60 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("bmw_i5", "BMW i5 eDrive40 G60 (2023+)", 2130, 0.23, 1.900, 1.515, 2.995, 2.4, "245/45 R19", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("bmw_ix3", "BMW iX3 G08 (2021-2024)", 2185, 0.29, 1.891, 1.668, 2.864, 2.2, "245/50 R19", A.LATEST, 1.27, _L4),
    ("bmw_ix1", "BMW iX1 xDrive30 U11 (2022+)", 2010, 0.26, 1.845, 1.616, 2.692, 2.4, "205/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("bmw_z4_g29", "BMW Z4 sDrive20i G29 (2019+)", 1430, 0.29, 1.864, 1.304, 2.470, 2.4, "225/50 R17", A.LATEST, 1.4, _L4 + "; rõhk hinnang"),
    ("bmw_630d_gt_g32", "BMW 630d GT G32 (2017-2023)", 1825, 0.25, 1.902, 1.538, 3.070, 2.4, "245/50 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("mb_gla_h247", "Mercedes GLA 200 H247 (2020+)", 1410, 0.28, 1.834, 1.611, 2.729, 2.4, "215/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("mb_cla_c118", "Mercedes CLA 200 C118 (2019+)", 1325, 0.31, 1.830, 1.439, 2.729, 2.4, "205/60 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_eqc", "Mercedes EQC 400 N293 (2019-2023)", 2420, 0.29, 1.884, 1.624, 2.873, 2.4, "235/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("mb_eqe", "Mercedes EQE 300 V295 (2022+)", 2405, 0.29, 1.906, 1.503, 3.120, 2.4, "255/45 R19", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_eqb", "Mercedes EQB 250 X243 (2021+)", 2085, 0.34, 1.834, 1.667, 2.829, 2.4, "235/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_g_w463", "Mercedes G400d W463 (2018+)", 2397, 0.54, 1.984, 1.969, 2.890, 2.4, "275/50 R20", A.LATEST, 1.22, _L4 + "; rõhk hinnang"),
    ("mb_citan_w420", "Mercedes Citan 110 CDI W420 (2021+)", 1462, 0.35, 1.859, 1.832, 2.716, 2.5, "195/65 R15", A.LATEST, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("audi_a1_gb", "Audi A1 GB 1.0 TFSI (2018+)", 1105, 0.32, 1.746, 1.422, 2.469, 2.3, "185/65 R15", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("audi_tt_8j", "Audi TT 8J 2.0 TFSI (2006-2014)", 1260, 0.3, 1.842, 1.352, 2.468, 2.4, "225/55 R16", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("audi_tt_8s", "Audi TT 8S 2.0 TFSI (2014-2023)", 1230, 0.3, 1.832, 1.353, 2.505, 2.4, "225/50 R17", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("audi_q8_etron", "Audi Q8 e-tron quattro (2023+)", 2510, 0.27, 1.937, 1.633, 2.928, 2.4, "255/55 R19", A.LATEST, 1.22, _L4 + "; rõhk hinnang"),
    ("audi_etron_gt", "Audi e-tron GT quattro (2021+)", 2276, 0.24, 1.964, 1.413, 2.900, 2.4, "225/55 R19", A.LATEST, 1.4, _L4 + "; rõhk hinnang"),
    ("audi_a6_allroad_c7", "Audi A6 allroad C7 3.0 TDI (2012-2018)", 1880, 0.31, 1.898, 1.452, 2.905, 2.4, "235/55 R18", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("audi_a4_allroad_b9", "Audi A4 allroad B9 2.0 TDI (2016+)", 1640, 0.31, 1.842, 1.493, 2.818, 2.4, "225/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_xc40_p8", "Volvo XC40 Recharge P8 (2020+)", 2188, 0.34, 1.873, 1.651, 2.702, 2.4, "235/50 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_c40", "Volvo C40 Recharge (2021+)", 2185, 0.34, 1.873, 1.596, 2.702, 2.4, "235/50 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_ex90", "Volvo EX90 (2024+)", 2754, 0.29, 1.964, 1.744, 2.985, 2.4, "265/45 R21", A.LATEST, 1.22, _L4 + "; rõhk hinnang"),
    ("volvo_v90cc", "Volvo V90 Cross Country II D5 (2017+)", 1966, 0.31, 1.879, 1.543, 2.941, 2.4, "235/55 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_v60cc", "Volvo V60 Cross Country II B4 (2019+)", 1924, 0.33, 1.850, 1.499, 2.875, 2.4, "215/55 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("volvo_s60_3", "Volvo S60 III B4 (2019+)", 1770, 0.27, 1.850, 1.431, 2.872, 2.4, "235/45 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("ford_galaxy_3", "Ford Galaxy III 2.0 TDCi (2015-2023)", 1752, 0.32, 1.916, 1.747, 2.849, 2.4, "235/55 R17", A.LATEST, 1.3, _L4 + "; Cd hinnang"),
    ("citroen_c4_3", "Citroën C4 III (2020+)", 1247, 0.31, 1.800, 1.525, 2.670, 2.4, "195/60 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("citroen_c4_cactus", "Citroën C4 Cactus (2014-2020)", 1020, 0.31, 1.729, 1.481, 2.595, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; mass hinnang (allikas andis vahemiku), rõhk hinnang, Cd hinnang"),
    ("citroen_c3_picasso", "Citroën C3 Picasso (2009-2017)", 1290, 0.32, 1.730, 1.624, 2.540, 2.4, "195/60 R15", A.MODERN, 1.28, _L4 + "; mass hinnang (allikas andis vahemiku), rõhk hinnang, Cd hinnang"),
    ("citroen_c1_1", "Citroën C1 I 1.0 (2005-2014)", 840, 0.32, 1.630, 1.470, 2.340, 2.3, "155/65 R14", A.MODERN, 1.28, _L4 + "; mass hinnang (allikas andis vahemiku), rõhk hinnang, Cd hinnang"),
    ("hyundai_i20_1", "Hyundai i20 I (2008-2014)", 1080, 0.32, 1.710, 1.490, 2.525, 2.3, "175/70 R14", A.MODERN, 1.28, _L4 + "; mass hinnang (allikas andis vahemiku), rõhk hinnang, Cd hinnang"),
    ("mitsu_l200_4", "Mitsubishi L200 IV (2005-2015)", 1850, 0.36, 1.750, 1.775, 3.000, 2.4, "205/80 R16", A.MODERN, 1.2, _L4 + "; mass hinnang, rõhk hinnang, Cd hinnang"),
    # 2026-09-28 seitsmes ring (JARGMISED_AUTOD.md)
    ("ford_ecosport", "Ford EcoSport 1.0 EcoBoost (2013-2022)", 1205, 0.34, 1.765, 1.653, 2.519, 2.4, "205/60 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_edge_2", "Ford Edge II 2.0 TDCi (2016-2020)", 1838, 0.34, 1.928, 1.707, 2.849, 2.4, "235/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_explorer_ev", "Ford Explorer EV (2024+)", 1833, 0.29, 1.872, 1.630, 2.770, 2.4, "235/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_ranger_p703", "Ford Ranger P703 2.0 EcoBlue (2022+)", 2314, 0.38, 1.968, 1.884, 3.270, 2.4, "255/70 R16", A.LATEST, 1.22, _L4 + "; laius ultimatespecs (allikad 1,92-2,03), rõhk hinnang, Cd hinnang"),
    ("opel_combo_e", "Opel Combo E 1.5 CDTI (2018+)", 1410, 0.35, 1.848, 1.841, 2.785, 2.5, "205/60 R16", A.LATEST, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("opel_grandland_2", "Opel Grandland II (2024+)", 1525, 0.34, 1.905, 1.665, 2.784, 2.4, "225/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("opel_frontera_2024", "Opel Frontera (2024+)", 1269, 0.34, 1.795, 1.635, 2.670, 2.4, "215/65 R16", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("opel_movano_b", "Opel Movano B kaubik (2010-2021)", 1970, 0.36, 2.070, 2.307, 3.182, 3.0, "225/65 R16C", A.MODERN, 1.05, _L4 + "; mass Renault Master III realt (sama auto), rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("peugeot_107", "Peugeot 107 1.0 (2005-2014)", 805, 0.32, 1.630, 1.465, 2.340, 2.3, "155/65 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("peugeot_408", "Peugeot 408 1.2 (2022+)", 1393, 0.31, 1.848, 1.478, 2.787, 2.4, "205/55 R19", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("peugeot_807", "Peugeot 807 2.0 HDi (2002-2014)", 1710, 0.32, 1.850, 1.750, 2.825, 2.4, "215/60 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("peugeot_expert_2", "Peugeot Expert II kaubik (2007-2016)", 1966, 0.36, 1.895, 1.942, 3.000, 2.8, "215/60 R16C", A.MODERN, 1.1, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("peugeot_partner_3", "Peugeot Partner III kaubik (2018+)", 1434, 0.35, 1.848, 1.796, 2.785, 2.5, "205/60 R16", A.LATEST, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("citroen_c3_aircross", "Citroën C3 Aircross (2017-2024)", 1179, 0.34, 1.756, 1.637, 2.604, 2.4, "205/60 R16", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("citroen_c5x", "Citroën C5 X 1.6 Hybrid (2021+)", 1722, 0.31, 1.865, 1.485, 2.785, 2.4, "205/55 R19", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_megane_etech", "Renault Mégane E-Tech (2022+)", 1636, 0.29, 1.768, 1.505, 2.685, 2.4, "195/60 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_scenic_4", "Renault Scénic IV (2016-2022)", 1529, 0.32, 1.866, 1.653, 2.734, 2.4, "195/55 R20", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_espace_5", "Renault Espace V (2015-2023)", 1659, 0.32, 1.888, 1.677, 2.884, 2.4, "235/60 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_koleos_2", "Renault Koleos II (2016-2023)", 1829, 0.34, 1.843, 1.673, 2.705, 2.4, "225/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_talisman", "Renault Talisman (2015-2022)", 1518, 0.27, 1.868, 1.463, 2.808, 2.4, "225/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("renault_laguna_2", "Renault Laguna II (2001-2007)", 1425, 0.31, 1.772, 1.429, 2.740, 2.4, "205/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_twingo_3", "Renault Twingo III (2014-2024)", 939, 0.32, 1.647, 1.557, 2.492, 2.3, "165/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("dacia_spring", "Dacia Spring (2021+)", 970, 0.29, 1.579, 1.516, 2.423, 2.3, "165/70 R14", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("dacia_bigster", "Dacia Bigster (2025+)", 1350, 0.34, 1.813, 1.662, 2.702, 2.4, "215/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("dacia_logan_1", "Dacia Logan I (2004-2012)", 975, 0.32, 1.740, 1.525, 2.630, 2.3, "185/70 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("dacia_lodgy", "Dacia Lodgy (2012-2022)", 1238, 0.32, 1.751, 1.679, 2.810, 2.4, "185/65 R15", A.MODERN, 1.28, _L4 + "; Cd hinnang"),
    ("dacia_dokker", "Dacia Dokker (2012-2021)", 1205, 0.35, 1.751, 1.814, 2.810, 2.4, "185/65 R15", A.MODERN, 1.16, _L4 + "; Cd hinnang"),
    ("nissan_xtrail_t30", "Nissan X-Trail T30 (2001-2007)", 1534, 0.34, 1.765, 1.675, 2.625, 2.4, "215/65 R16", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_micra_k14", "Nissan Micra K14 (2017+)", 1060, 0.32, 1.743, 1.455, 2.525, 2.3, "185/65 R15", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_navara_d23", "Nissan Navara D23 (2015+)", 1948, 0.38, 1.850, 1.805, 3.150, 2.4, "255/70 R16", A.LATEST, 1.22, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_ariya", "Nissan Ariya (2022+)", 1980, 0.29, 1.850, 1.660, 2.775, 2.4, "235/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_murano_z51", "Nissan Murano Z51 (2008-2014)", 1895, 0.34, 1.885, 1.720, 2.825, 2.4, "235/65 R18", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("hyundai_ioniq6", "Hyundai Ioniq 6 (2022+)", 1968, 0.21, 1.880, 1.495, 2.950, 2.4, "225/55 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("hyundai_santafe_mx5", "Hyundai Santa Fe MX5 (2024+)", 1845, 0.29, 1.900, 1.720, 2.815, 2.4, "255/45 R20", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("hyundai_i10_3", "Hyundai i10 III (2019+)", 921, 0.32, 1.680, 1.480, 2.425, 2.3, "175/65 R14", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("hyundai_getz", "Hyundai Getz (2002-2011)", 1130, 0.32, 1.665, 1.490, 2.455, 2.3, "175/65 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_ev9", "Kia EV9 (2023+)", 2310, 0.29, 1.980, 1.755, 3.100, 2.6, "255/60 R19", A.LATEST, 1.27, _L4 + "; Cd hinnang"),
    ("kia_picanto_3", "Kia Picanto III (2017+)", 935, 0.32, 1.595, 1.485, 2.400, 2.3, "175/65 R14", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_sorento_1", "Kia Sorento I (2002-2009)", 1985, 0.34, 1.857, 1.730, 2.710, 2.4, "245/70 R16", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_soul_2", "Kia Soul II (2014-2019)", 1212, 0.31, 1.800, 1.618, 2.570, 2.4, "205/60 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_carens_4", "Kia Carens IV (2013-2019)", 1516, 0.32, 1.805, 1.610, 2.750, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_stinger", "Kia Stinger (2017-2023)", 1703, 0.3, 1.870, 1.400, 2.905, 2.4, "225/45 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("kia_optima_3", "Kia Optima III (2010-2015)", 1500, 0.29, 1.830, 1.455, 2.795, 2.4, "215/55 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("mazda_mx5_nc", "Mazda MX-5 NC 1.8 (2005-2015)", 1110, 0.33, 1.720, 1.240, 2.330, 2.4, "205/50 R16", A.MODERN, 1.36, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mazda_cx80", "Mazda CX-80 (2024+)", 2131, 0.34, 1.890, 1.710, 3.120, 2.4, "235/50 R20", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mazda_mx30", "Mazda MX-30 (2020+)", 1675, 0.29, 1.795, 1.555, 2.655, 2.4, "215/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_civic_11", "Honda Civic XI (2022+)", 1442, 0.31, 1.801, 1.408, 2.734, 2.4, "215/50 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_crv_6", "Honda CR-V VI (2023+)", 1808, 0.34, 1.866, 1.673, 2.700, 2.4, "235/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_hrv_3", "Honda HR-V III (2021+)", 1380, 0.34, 1.790, 1.582, 2.610, 2.4, "225/50 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_jazz_4", "Honda Jazz IV (2020+)", 1228, 0.32, 1.694, 1.526, 2.517, 2.3, "185/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_zrv", "Honda ZR-V (2023+)", 1589, 0.34, 1.840, 1.620, 2.657, 2.4, "225/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_forester_sg", "Subaru Forester SG (2002-2008)", 1335, 0.34, 1.740, 1.590, 2.520, 2.4, "205/70 R15", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_xv_2", "Subaru XV II (2017-2023)", 1408, 0.34, 1.800, 1.595, 2.665, 2.4, "225/60 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_crosstrek", "Subaru Crosstrek (2023+)", 1520, 0.34, 1.800, 1.600, 2.670, 2.4, "225/60 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_legacy_bm", "Subaru Legacy BM (2009-2014)", 1495, 0.31, 1.780, 1.505, 2.750, 2.4, "205/60 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mitsu_outlander_4", "Mitsubishi Outlander IV PHEV (2024+)", 1995, 0.34, 1.862, 1.746, 2.704, 2.4, "235/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mitsu_pajero_3", "Mitsubishi Pajero III (1999-2006)", 2015, 0.38, 1.840, 1.860, 2.780, 2.4, "235/80 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mitsu_asx_2", "Mitsubishi ASX II (2023+)", 1324, 0.34, 1.797, 1.585, 2.639, 2.4, "215/60 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lexus_nx_az20", "Lexus NX 350h AZ20 (2021+)", 1730, 0.34, 1.865, 1.660, 2.690, 2.4, "235/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("lexus_is_xe30", "Lexus IS 300h XE30 (2013-2020)", 1620, 0.25, 1.810, 1.430, 2.800, 2.4, "225/45 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("lexus_gs_l10", "Lexus GS 300h L10 (2012-2020)", 1735, 0.27, 1.840, 1.455, 2.850, 2.4, "225/50 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("lexus_rx_al30", "Lexus RX 450h+ AL30 (2022+)", 2185, 0.35, 1.920, 1.695, 2.850, 2.4, "235/50 R21", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("suzuki_scross_2", "Suzuki S-Cross II (2021+)", 1160, 0.34, 1.785, 1.585, 2.600, 2.4, "215/55 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("suzuki_jimny_3", "Suzuki Jimny III (1998-2018)", 1000, 0.45, 1.600, 1.705, 2.250, 2.4, "205/70 R15", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("suzuki_swace", "Suzuki Swace (2020+)", 1400, 0.31, 1.790, 1.460, 2.700, 2.4, "205/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("suzuki_swift_6", "Suzuki Swift VI (2024+)", 940, 0.32, 1.695, 1.500, 2.450, 2.3, "185/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("tesla_modely_juniper", "Tesla Model Y Juniper RWD (2025+)", 1928, 0.29, 1.920, 1.624, 2.890, 2.4, "255/45 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("porsche_macan_ev", "Porsche Macan Electric (2024+)", 2330, 0.25, 1.938, 1.622, 2.893, 2.4, "235/55 R20", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("porsche_panamera_970", "Porsche Panamera 970 3.6 (2009-2016)", 1730, 0.3, 1.931, 1.418, 2.920, 2.4, "245/50 R18", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("porsche_911_997", "Porsche 911 Carrera 997 (2004-2012)", 1395, 0.28, 1.808, 1.310, 2.350, 2.4, "235/40 R18", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("lr_discovery_5", "Land Rover Discovery 5 (2017+)", 2109, 0.33, 2.073, 1.888, 2.923, 2.4, "255/55 R20", A.LATEST, 1.22, _L4 + "; laius peeglitega kokkupandult (kere laius puudus), CdA veidi ülehinnatud, rõhk hinnang"),
    ("lr_rr_l460", "Land Rover Range Rover L460 (2022+)", 2632, 0.38, 2.047, 1.870, 2.997, 2.4, "275/50 R21", A.LATEST, 1.22, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lr_rrs_l461", "Range Rover Sport L461 (2022+)", 2315, 0.38, 2.047, 1.820, 2.997, 2.4, "275/50 R21", A.LATEST, 1.22, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lr_evoque_2", "Range Rover Evoque II (2019+)", 2001, 0.34, 1.895, 1.649, 2.681, 2.4, "235/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lr_velar", "Range Rover Velar (2017+)", 1829, 0.34, 2.032, 1.665, 2.874, 2.4, "255/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lr_freelander_1", "Land Rover Freelander 1 (1997-2006)", 1645, 0.34, 1.809, 1.708, 2.557, 2.4, "195/80 R15", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lr_defender_110", "Land Rover Defender 110 2.4 TDCi (2007-2016)", 1750, 0.45, 1.790, 2.030, 2.790, 2.4, "235/85 R16", A.MODERN, 1.2, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jeep_gc_wl", "Jeep Grand Cherokee WL (2021+)", 2435, 0.357, 1.968, 1.799, 2.964, 2.4, "265/50 R20", A.LATEST, 1.22, _L4 + "; rõhk hinnang"),
    ("jeep_wrangler_jl", "Jeep Wrangler JL (2018+)", 2146, 0.45, 1.894, 1.838, 3.008, 2.4, "255/70 R18", A.LATEST, 1.22, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jeep_avenger", "Jeep Avenger (2023+)", 1182, 0.34, 1.776, 1.534, 2.557, 2.4, "215/60 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jeep_gc_wk", "Jeep Grand Cherokee WK (2005-2010)", 2135, 0.41, 1.870, 1.740, 2.781, 2.4, "245/65 R17", A.MODERN, 1.2, _L4 + "; rõhk hinnang"),
    ("jeep_compass_mk", "Jeep Compass MK (2006-2016)", 1605, 0.34, 1.812, 1.718, 2.635, 2.4, "215/60 R17", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mini_countryman_f60", "MINI Countryman F60 (2017-2023)", 1440, 0.34, 1.822, 1.557, 2.670, 2.4, "205/65 R16", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mini_clubman_f54", "MINI Clubman F54 (2015-2024)", 1375, 0.31, 1.800, 1.441, 2.670, 2.4, "205/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mini_cooper_r50", "MINI Cooper R50 (2001-2006)", 1125, 0.32, 1.688, 1.408, 2.467, 2.3, "175/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mini_cooper_j01", "MINI Cooper J01 Electric (2024+)", 1540, 0.29, 1.756, 1.460, 2.526, 2.3, "195/60 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mini_countryman_u25", "MINI Countryman U25 (2024+)", 1545, 0.34, 1.843, 1.661, 2.692, 2.4, "205/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("fiat_500x", "Fiat 500X (2014+)", 1320, 0.34, 1.796, 1.600, 2.570, 2.4, "215/60 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("fiat_500l", "Fiat 500L (2012-2022)", 1295, 0.32, 1.784, 1.665, 2.612, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("fiat_punto_2", "Fiat Punto II (1999-2010)", 875, 0.32, 1.660, 1.480, 2.460, 2.3, "165/70 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("fiat_bravo_2", "Fiat Bravo II (2007-2014)", 1205, 0.31, 1.792, 1.498, 2.600, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("fiat_500e", "Fiat 500e (2020+)", 1365, 0.29, 1.683, 1.527, 2.322, 2.3, "195/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("seat_altea", "SEAT Altea (2004-2015)", 1405, 0.32, 1.768, 1.568, 2.578, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("seat_toledo_4", "SEAT Toledo IV (2012-2019)", 1175, 0.31, 1.706, 1.461, 2.602, 2.4, "185/60 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("seat_mii", "SEAT Mii (2011-2021)", 854, 0.32, 1.641, 1.478, 2.420, 2.3, "165/70 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("seat_ibiza_3", "SEAT Ibiza III (2002-2008)", 1035, 0.32, 1.700, 1.440, 2.460, 2.3, "185/60 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("cupra_leon", "Cupra Leon 2.0 TSI (2020+)", 1490, 0.31, 1.799, 1.442, 2.683, 2.4, "225/40 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("cupra_tavascan", "Cupra Tavascan (2024+)", 2103, 0.29, 1.861, 1.597, 2.766, 2.4, "235/55 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("cupra_terramar", "Cupra Terramar (2024+)", 1638, 0.34, 1.869, 1.586, 2.681, 2.4, "235/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("byd_seal_u", "BYD Seal U DM-i (2024+)", 1940, 0.34, 1.890, 1.670, 2.765, 2.4, "235/50 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("byd_atto2", "BYD Atto 2 (2025+)", 1430, 0.29, 1.830, 1.675, 2.620, 2.4, "215/65 R16", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mg_zs_2", "MG ZS II Hybrid+ (2024+)", 1420, 0.34, 1.818, 1.635, 2.610, 2.4, "215/55 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mg3_hybrid", "MG3 Hybrid+ (2024+)", 1308, 0.32, 1.797, 1.502, 2.570, 2.3, "195/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("zeekr_001", "Zeekr 001 (2023+)", 2275, 0.29, 1.999, 1.560, 2.999, 2.4, "255/45 R21", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("zeekr_x", "Zeekr X (2023+)", 1930, 0.29, 1.836, 1.566, 2.750, 2.4, "235/50 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("xpeng_g6", "Xpeng G6 (2024+)", 2100, 0.29, 1.920, 1.650, 2.890, 2.4, "255/45 R20", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("xpeng_g9", "Xpeng G9 (2023+)", 2285, 0.29, 1.937, 1.680, 2.998, 2.4, "255/50 R20", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lynk_01", "Lynk & Co 01 (2021+)", 1750, 0.34, 1.857, 1.673, 2.734, 2.4, "235/50 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("polestar_3", "Polestar 3 (2024+)", 2654, 0.29, 1.968, 1.614, 2.985, 2.4, "265/45 R21", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("omoda_5", "Omoda 5 (2024+)", 1455, 0.34, 1.824, 1.588, 2.610, 2.4, "215/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jaecoo_7", "Jaecoo 7 (2024+)", 1870, 0.34, 1.865, 1.670, 2.672, 2.4, "235/50 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("leapmotor_c10", "Leapmotor C10 (2024+)", 2055, 0.29, 1.900, 1.680, 2.825, 2.4, "235/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("smart_1", "Smart #1 (2023+)", 1820, 0.29, 1.822, 1.636, 2.750, 2.4, "235/45 R19", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("smart_fortwo_453", "Smart fortwo 453 (2014-2024)", 815, 0.32, 1.663, 1.555, 1.873, 2.3, "165/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ssangyong_rexton_2", "SsangYong Rexton II (2017+)", 2153, 0.38, 1.960, 1.825, 2.865, 2.4, "255/60 R18", A.LATEST, 1.22, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ssangyong_tivoli", "SsangYong Tivoli (2015+)", 1270, 0.34, 1.798, 1.590, 2.600, 2.4, "205/60 R16", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ssangyong_kyron", "SsangYong Kyron (2005-2014)", 1904, 0.38, 1.880, 1.760, 2.740, 2.4, "225/75 R16", A.MODERN, 1.2, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("alfa_stelvio", "Alfa Romeo Stelvio (2017+)", 1659, 0.34, 1.903, 1.671, 2.818, 2.4, "235/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("alfa_giulia", "Alfa Romeo Giulia (2016+)", 1465, 0.28, 1.860, 1.438, 2.820, 2.4, "225/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("alfa_tonale", "Alfa Romeo Tonale (2022+)", 1525, 0.34, 1.841, 1.601, 2.636, 2.4, "235/50 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jaguar_fpace", "Jaguar F-Pace (2016+)", 1775, 0.34, 2.070, 1.652, 2.874, 2.4, "235/65 R18", A.LATEST, 1.27, _L4 + "; laius peeglitega kokkupandult, CdA veidi ülehinnatud, rõhk hinnang, Cd hinnang"),
    ("jaguar_xe", "Jaguar XE (2015-2024)", 1565, 0.31, 1.850, 1.416, 2.835, 2.4, "225/50 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jaguar_epace", "Jaguar E-Pace (2017+)", 1843, 0.32, 1.984, 1.649, 2.681, 2.4, "235/65 R17", A.LATEST, 1.27, _L4 + "; laius tõenäoliselt peeglitega kokkupandult, CdA veidi ülehinnatud, rõhk hinnang"),
    ("jaguar_ipace", "Jaguar I-Pace (2018-2024)", 2133, 0.29, 2.011, 1.565, 2.990, 2.4, "235/65 R18", A.LATEST, 1.27, _L4 + "; laius peeglitega kokkupandult, CdA veidi ülehinnatud, rõhk hinnang"),
    ("ram_1500_dt", "RAM 1500 DT (2019+)", 2440, 0.38, 2.084, 1.971, 3.672, 2.4, "275/55 R20", A.LATEST, 1.22, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("chevrolet_orlando", "Chevrolet Orlando (2011-2018)", 1528, 0.32, 1.836, 1.633, 2.760, 2.4, "215/60 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("isuzu_dmax_3", "Isuzu D-Max III (2020+)", 2055, 0.38, 1.870, 1.790, 3.125, 2.4, "265/60 R18", A.LATEST, 1.22, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("skoda_octavia_4_rs", "Škoda Octavia IV RS 2.0 TSI (2020+)", 1451, 0.31, 1.829, 1.470, 2.686, 2.4, "225/40 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    # 2026-09-28 kaheksas ring (puuduvad põlvkonnad 1980-2026)
    ("audi_80_b2", "Audi 80 B2 1.6 (1978-1986)", 930, 0.4, 1.682, 1.365, 2.541, 2.1, "175/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang"),
    ("audi_a6_allroad_c5", "Audi A6 allroad C5 2.5 TDI (2000-2005)", 1790, 0.32, 1.852, 1.551, 2.757, 2.4, "225/55 R17", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("audi_a6_allroad_c6", "Audi A6 allroad C6 3.0 TDI (2006-2011)", 1880, 0.34, 1.862, 1.519, 2.833, 2.4, "225/55 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("audi_a6_allroad_c8", "Audi A6 allroad C8 3.0 TDI (2019+)", 1945, 0.3, 1.902, 1.497, 2.925, 2.4, "235/55 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("audi_a8_d2", "Audi A8 D2 2.8 (1994-2002)", 1460, 0.28, 1.880, 1.440, 2.882, 2.1, "225/60 R16", A.EARLY, 1.2, _L4 + "; rõhk hinnang"),
    ("audi_tt_8n", "Audi TT 8N 1.8T (1998-2006)", 1280, 0.32, 1.760, 1.350, 2.440, 2.4, "205/55 R16", A.EARLY, 1.32, _L4 + "; rõhk hinnang"),
    ("audi_rs3_8y", "Audi RS3 8Y (2021+)", 1570, 0.34, 1.851, 1.436, 2.631, 2.4, "265/30 R19", A.LATEST, 1.4, _L4 + "; rõhk hinnang"),
    ("audi_a4_allroad_b8", "Audi A4 allroad B8 2.0 TDI (2009-2016)", 1630, 0.34, 1.841, 1.495, 2.805, 2.4, "225/55 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("audi_a5_b10", "Audi A5 B10 2.0 TFSI (2024+)", 1770, 0.28, 1.860, 1.444, 2.892, 2.4, "225/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("bmw_518i_e28", "BMW 518i E28 (1981-1988)", 1160, 0.36, 1.700, 1.415, 2.625, 2.1, "175/80 R14", A.EARLY, 1.2, _L4 + "; ABS oli osal autodel lisavarustus; arvutus eeldab ABS-i, rõhk hinnang"),
    ("bmw_730i_e32", "BMW 730i E32 (1986-1994)", 1600, 0.32, 1.845, 1.411, 2.832, 2.1, "205/65 R15", A.EARLY, 1.2, _L4 + "; rõhk hinnang"),
    ("bmw_728i_e38", "BMW 728i E38 (1994-2001)", 1670, 0.3, 1.862, 1.435, 2.930, 2.1, "215/65 R16", A.EARLY, 1.2, _L4 + "; rõhk hinnang"),
    ("bmw_630i_e63", "BMW 630i E63 (2003-2010)", 1490, 0.3, 1.855, 1.373, 2.780, 2.4, "245/50 R17", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("bmw_640d_f06", "BMW 640d F06 (2012-2018)", 1790, 0.29, 1.894, 1.392, 2.968, 2.4, "245/45 R18", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("bmw_z3", "BMW Z3 1.9 (1995-2002)", 1185, 0.33, 1.692, 1.288, 2.446, 2.1, "205/60 R15", A.EARLY, 1.32, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("bmw_z4_e85", "BMW Z4 E85 2.5i (2002-2008)", 1335, 0.35, 1.781, 1.299, 2.495, 2.4, "225/50 R16", A.EARLY, 1.32, _L4 + "; rõhk hinnang"),
    ("bmw_z4_e89", "BMW Z4 E89 sDrive23i (2009-2016)", 1480, 0.33, 1.790, 1.291, 2.496, 2.4, "225/45 R17", A.MODERN, 1.36, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("bmw_m3_e30", "BMW M3 E30 (1986-1991)", 1200, 0.33, 1.680, 1.370, 2.565, 2.1, "205/55 R15", A.EARLY, 1.32, _L4 + "; rõhk hinnang"),
    ("bmw_m3_e36", "BMW M3 E36 (1992-1999)", 1460, 0.32, 1.710, 1.335, 2.700, 2.1, "235/40 R17", A.EARLY, 1.32, _L4 + "; rõhk hinnang"),
    ("bmw_m3_e46", "BMW M3 E46 (2000-2006)", 1495, 0.32, 1.780, 1.372, 2.731, 2.4, "225/45 R18", A.EARLY, 1.32, _L4 + "; rõhk hinnang"),
    ("bmw_m5_e60", "BMW M5 E60 (2005-2010)", 1780, 0.31, 1.846, 1.469, 2.889, 2.4, "255/40 R19", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("bmw_m5_f10", "BMW M5 F10 (2011-2016)", 1870, 0.33, 1.891, 1.456, 2.964, 2.4, "265/40 R19", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("bmw_218i_f22", "BMW 218i F22 (2014-2021)", 1340, 0.29, 1.774, 1.418, 2.690, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("bmw_220i_g42", "BMW 220i G42 (2022+)", 1490, 0.26, 1.838, 1.390, 2.741, 2.4, "225/50 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("bmw_118i_f70", "BMW 118i F70 (2024+)", 1390, 0.32, 1.800, 1.459, 2.670, 2.4, "205/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("bmw_x2_u10", "BMW X2 U10 sDrive20i (2024+)", 1570, 0.27, 1.845, 1.590, 2.692, 2.4, "225/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("chevrolet_aveo_t250", "Chevrolet Aveo T250 1.2 (2006-2011)", 1105, 0.33, 1.680, 1.505, 2.480, 2.3, "185/60 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("chevrolet_spark_m200", "Chevrolet Spark M200 0.8 (2005-2010)", 776, 0.33, 1.495, 1.485, 2.340, 2.3, "145/70 R13", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("citroen_c3_1", "Citroën C3 I 1.4 (2002-2009)", 1005, 0.31, 1.667, 1.529, 2.460, 2.3, "175/65 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("citroen_c3_4", "Citroën C3 IV 1.2 (2024+)", 1151, 0.33, 1.755, 1.577, 2.540, 2.3, "205/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("citroen_berlingo_1", "Citroën Berlingo I 1.9 D (1996-2008)", 1185, 0.37, 1.698, 1.802, 2.690, 2.5, "175/70 R14", A.EARLY, 1.16, _L4 + "; ABS oli osal autodel lisavarustus; arvutus eeldab ABS-i, rõhk hinnang"),
    ("citroen_jumpy_1", "Citroën Jumpy I 1.9 D (1995-2006)", 1310, 0.35, 1.810, 1.927, 2.824, 2.8, "195/70 R14", A.EARLY, 1.1, _L4 + "; ABS oli osal autodel lisavarustus; arvutus eeldab ABS-i, rõhk hinnang tühjale sõidukile"),
    ("citroen_jumpy_3", "Citroën Jumpy III 2.0 BlueHDi (2016+)", 1604, 0.36, 1.920, 1.877, 3.275, 2.8, "215/65 R16C", A.LATEST, 1.1, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("citroen_xsara", "Citroën Xsara 1.6 (1997-2006)", 1115, 0.32, 1.698, 1.405, 2.540, 2.4, "185/65 R14", A.EARLY, 1.24, _L4 + "; ABS oli osal autodel lisavarustus; arvutus eeldab ABS-i, rõhk hinnang, Cd hinnang"),
    ("citroen_bx", "Citroën BX 1.6 (1982-1994)", 950, 0.341, 1.660, 1.358, 2.655, 2.1, "165/70 R14", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang"),
    ("dacia_logan_3", "Dacia Logan III 1.0 TCe (2020+)", 1069, 0.33, 1.848, 1.501, 2.649, 2.3, "185/65 R15", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("dacia_sandero_1", "Dacia Sandero I 1.4 (2008-2012)", 975, 0.36, 1.746, 1.534, 2.588, 2.3, "185/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("fiat_panda_2", "Fiat Panda II 1.2 (2003-2012)", 860, 0.33, 1.578, 1.540, 2.299, 2.3, "155/80 R13", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("fiat_doblo_1", "Fiat Doblò I 1.9 JTD (2000-2010)", 1365, 0.36, 1.714, 1.810, 2.566, 2.5, "175/70 R14", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("fiat_doblo_3", "Fiat Doblò III 1.5 BlueHDi (2022+)", 1388, 0.36, 1.848, 1.796, 2.785, 2.5, "205/60 R16", A.LATEST, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("fiat_uno", "Fiat Uno 1.0 (1983-1995)", 740, 0.36, 1.560, 1.420, 2.360, 2.0, "155/70 R13", A.NONE, 1.08, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("ford_fiesta_3", "Ford Fiesta Mk3 1.1 (1989-1996)", 845, 0.36, 1.606, 1.379, 2.446, 2.0, "155/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("ford_mondeo_2", "Ford Mondeo II 1.8 (1996-2000)", 1305, 0.32, 1.751, 1.427, 2.704, 2.4, "185/65 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_galaxy_1", "Ford Galaxy I 1.9 TDI (1995-2006)", 1670, 0.33, 1.810, 1.732, 2.835, 2.1, "195/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_transit_connect_3", "Ford Transit Connect III 2.0 EcoBlue (2022+)", 1477, 0.36, 1.855, 1.856, 2.755, 2.5, "215/55 R17", A.LATEST, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_cmax_2", "Ford C-Max II 1.6 (2010-2019)", 1374, 0.33, 1.828, 1.626, 2.648, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_ranger_2", "Ford Ranger II 2.5 TDCi (2006-2011)", 1955, 0.4, 1.715, 1.745, 3.000, 2.4, "245/70 R16", A.MODERN, 1.2, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_civic_7", "Honda Civic VII 1.4 (2001-2005)", 1130, 0.32, 1.695, 1.495, 2.680, 2.4, "185/70 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_crv_1", "Honda CR-V I 2.0 (1995-2001)", 1430, 0.36, 1.750, 1.710, 2.620, 2.1, "205/70 R15", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_jazz_1", "Honda Jazz I 1.2 (2001-2008)", 999, 0.33, 1.675, 1.525, 2.450, 2.3, "175/65 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_hrv_1", "Honda HR-V I 1.6 (1999-2006)", 1257, 0.36, 1.695, 1.580, 2.450, 2.4, "195/70 R15", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_accord_5", "Honda Accord V 2.0 (1993-1998)", 1295, 0.32, 1.715, 1.380, 2.720, 2.1, "185/65 R15", A.EARLY, 1.2, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("hyundai_santafe_sm", "Hyundai Santa Fe SM 2.0 CRDi (2000-2006)", 1705, 0.36, 1.820, 1.730, 2.620, 2.4, "215/70 R15", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("hyundai_i10_1", "Hyundai i10 I 1.1 (2008-2013)", 1000, 0.33, 1.595, 1.540, 2.380, 2.3, "155/70 R13", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_rio_2", "Kia Rio II 1.4 (2005-2011)", 1079, 0.33, 1.695, 1.470, 2.500, 2.3, "175/70 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_picanto_1", "Kia Picanto I 1.1 (2004-2011)", 966, 0.33, 1.595, 1.480, 2.370, 2.3, "155/70 R13", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_sportage_1", "Kia Sportage I 2.0 (1993-2004)", 1418, 0.36, 1.730, 1.650, 2.650, 2.1, "205/70 R15", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("kia_carens_3", "Kia Carens III 2.0 CRDi (2006-2013)", 1610, 0.33, 1.820, 1.650, 2.690, 2.4, "205/60 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_soul_1", "Kia Soul I 1.6 (2008-2014)", 1270, 0.32, 1.785, 1.661, 2.550, 2.4, "195/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_soul_3", "Kia Soul III e-Soul (2019+)", 1757, 0.29, 1.800, 1.605, 2.600, 2.4, "215/55 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mazda_323_ba", "Mazda 323 BA 1.5 (1994-1998)", 1115, 0.32, 1.695, 1.355, 2.605, 2.1, "175/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("mazda_626_ge", "Mazda 626 GE 2.0 (1992-1997)", 1160, 0.32, 1.750, 1.400, 2.610, 2.1, "195/65 R14", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("mazda_2_dy", "Mazda 2 DY 1.4 (2003-2007)", 1050, 0.34, 1.680, 1.545, 2.490, 2.3, "175/65 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("mazda_mx5_na", "Mazda MX-5 NA 1.6 (1989-1997)", 955, 0.38, 1.675, 1.230, 2.265, 2.1, "185/60 R14", A.NONE, 1.15, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang"),
    ("mazda_mx5_nb", "Mazda MX-5 NB 1.8 (1998-2005)", 1025, 0.33, 1.680, 1.225, 2.265, 2.4, "195/50 R15", A.EARLY, 1.32, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mazda_premacy", "Mazda Premacy 1.8 (1999-2005)", 1250, 0.33, 1.705, 1.600, 2.670, 2.4, "195/55 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_s_w126", "Mercedes-Benz S280 W126 (1979-1991)", 1560, 0.35, 1.820, 1.430, 2.930, 2.1, "195/70 R14", A.EARLY, 1.2, _L4 + "; ABS oli osal autodel lisavarustus; arvutus eeldab ABS-i, rõhk hinnang, Cd hinnang"),
    ("mb_b_w247", "Mercedes-Benz B180 W247 (2019+)", 1330, 0.33, 1.796, 1.562, 2.729, 2.4, "205/60 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_cls_c219", "Mercedes-Benz CLS 350 C219 (2004-2010)", 1655, 0.3, 1.873, 1.403, 2.854, 2.4, "245/45 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("mb_cls_c257", "Mercedes-Benz CLS 400d C257 (2018-2023)", 1860, 0.26, 1.890, 1.435, 2.939, 2.4, "245/45 R18", A.LATEST, 1.3, _L4 + "; rõhk hinnang"),
    ("mb_gle_w166", "Mercedes-Benz GLE 350d W166 (2015-2019)", 2100, 0.35, 1.935, 1.796, 2.915, 2.4, "255/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("mitsu_outlander_1", "Mitsubishi Outlander I 2.0 (2001-2006)", 1540, 0.36, 1.750, 1.605, 2.625, 2.4, "215/60 R16", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mitsu_pajero_2", "Mitsubishi Pajero II 2.5 turbodiisel (1991-1999)", 1875, 0.4, 1.695, 1.855, 2.725, 2.1, "235/75 R15", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("mitsu_l200_3", "Mitsubishi L200 III 2.5 turbodiisel (1996-2006)", 1730, 0.4, 1.695, 1.780, 2.960, 2.4, "205/80 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mitsu_colt_5", "Mitsubishi Colt V 1.3 (1996-2003)", 945, 0.33, 1.680, 1.365, 2.415, 2.3, "175/70 R13", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mitsu_spacestar_1", "Mitsubishi Space Star I 1.3 (1998-2005)", 1170, 0.33, 1.715, 1.515, 2.500, 2.3, "175/65 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_patrol_y61", "Nissan Patrol Y61 3.0 Di (1997-2010)", 2410, 0.4, 1.840, 1.855, 2.968, 2.4, "235/80 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("opel_ascona_c", "Opel Ascona C 1.6 (1981-1988)", 980, 0.39, 1.668, 1.385, 2.574, 2.1, "165/80 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang"),
    ("opel_combo_c", "Opel Combo C 1.3 CDTI (2001-2011)", 1278, 0.36, 1.684, 1.801, 2.716, 2.5, "175/65 R14C", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("opel_frontera_b", "Opel Frontera B 2.2 DTI (1998-2004)", 1780, 0.4, 1.787, 1.740, 2.702, 2.4, "245/75 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("opel_zafira_life", "Opel Zafira Life 2.0 diisel (2019+)", 1801, 0.33, 1.920, 1.890, 3.275, 2.4, "215/65 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("peugeot_205", "Peugeot 205 1.1 (1983-1998)", 765, 0.36, 1.560, 1.375, 2.420, 2.0, "145/80 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("peugeot_405", "Peugeot 405 1.6 (1987-1997)", 1090, 0.35, 1.714, 1.406, 2.669, 2.1, "175/70 R14", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("peugeot_106", "Peugeot 106 1.1 (1991-2003)", 780, 0.33, 1.590, 1.369, 2.385, 2.0, "155/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("peugeot_607", "Peugeot 607 2.2 HDi (2000-2010)", 1610, 0.32, 1.800, 1.437, 2.800, 2.4, "215/60 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("peugeot_partner_1", "Peugeot Partner I 1.9 D (1996-2008)", 1206, 0.36, 1.720, 1.870, 2.690, 2.5, "175/65 R14", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("peugeot_expert_1", "Peugeot Expert I 1.9 D (1995-2007)", 1310, 0.35, 1.810, 1.927, 2.824, 2.8, "195/70 R14", A.EARLY, 1.1, _L4 + "; rõhk hinnang tühjale sõidukile"),
    ("renault_clio_1", "Renault Clio I 1.2 (1990-1998)", 915, 0.36, 1.616, 1.395, 2.472, 2.0, "155/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("renault_19", "Renault 19 1.4 (1988-1996)", 950, 0.35, 1.694, 1.412, 2.540, 2.1, "165/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("renault_scenic_1", "Renault Scénic I 1.6 (1996-2003)", 1250, 0.33, 1.719, 1.609, 2.580, 2.4, "185/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_laguna_1", "Renault Laguna I 1.8 (1993-2001)", 1240, 0.32, 1.752, 1.432, 2.670, 2.1, "185/65 R14", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("renault_espace_3", "Renault Espace III 2.2 dCi (1997-2002)", 1737, 0.33, 1.810, 1.690, 2.702, 2.4, "225/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_espace_4", "Renault Espace IV 2.0 dCi (2002-2014)", 1900, 0.33, 1.860, 1.728, 2.803, 2.4, "225/60 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_espace_6", "Renault Espace VI E-Tech (2023+)", 1584, 0.33, 1.843, 1.645, 2.738, 2.4, "205/55 R19", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_kangoo_1", "Renault Kangoo I 1.5 dCi (1997-2008)", 1170, 0.36, 1.663, 1.827, 2.600, 2.5, "175/65 R14", A.EARLY, 1.16, _L4 + "; ABS oli osal autodel lisavarustus; arvutus eeldab ABS-i, rõhk hinnang, Cd hinnang"),
    ("renault_twingo_1", "Renault Twingo I 1.2 (1993-2007)", 855, 0.33, 1.630, 1.423, 2.340, 2.0, "155/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("renault_twingo_2", "Renault Twingo II 1.2 (2007-2014)", 1000, 0.33, 1.665, 1.470, 2.367, 2.3, "165/65 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_koleos_1", "Renault Koleos I 2.0 dCi (2008-2016)", 1730, 0.36, 1.855, 1.695, 2.690, 2.4, "225/60 R17", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("seat_leon_1", "SEAT Leon I 1.6 (1999-2005)", 1220, 0.32, 1.742, 1.439, 2.513, 2.4, "195/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("seat_toledo_2", "SEAT Toledo II 1.6 (1998-2004)", 1155, 0.32, 1.742, 1.436, 2.513, 2.4, "195/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("seat_toledo_3", "SEAT Toledo III 1.9 TDI (2004-2009)", 1429, 0.32, 1.768, 1.568, 2.578, 2.4, "205/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("seat_alhambra_1", "SEAT Alhambra I 1.9 TDI (1996-2010)", 1649, 0.33, 1.810, 1.762, 2.835, 2.4, "195/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_impreza_gc", "Subaru Impreza GC 1.6 (1992-2000)", 1115, 0.32, 1.690, 1.415, 2.520, 2.1, "175/70 R14", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("subaru_impreza_gj", "Subaru Impreza GJ 1.6i (2012-2016)", 1310, 0.32, 1.740, 1.465, 2.645, 2.4, "195/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_impreza_gt", "Subaru Impreza GK 1.6i (2017-2023)", 1359, 0.32, 1.775, 1.480, 2.670, 2.4, "205/55 R16", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_legacy_bg", "Subaru Legacy BG 2.0 (1994-1998)", 1340, 0.32, 1.695, 1.490, 2.630, 2.1, "185/70 R14", A.EARLY, 1.2, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_legacy_bh", "Subaru Legacy BH 2.0 (1998-2003)", 1410, 0.32, 1.695, 1.515, 2.650, 2.4, "185/70 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_forester_sf", "Subaru Forester SF 2.0 (1997-2002)", 1380, 0.36, 1.735, 1.590, 2.525, 2.4, "205/70 R15", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_outback_bh", "Subaru Outback BH 2.5 (1998-2003)", 1480, 0.32, 1.770, 1.545, 2.670, 2.4, "215/60 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("suzuki_vitara_1", "Suzuki Vitara I 1.6 (1988-1998)", 1020, 0.39, 1.630, 1.665, 2.200, 2.1, "195/80 R15", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("toyota_camry_xv40", "Toyota Camry XV40 2.4 (2006-2011)", 1520, 0.28, 1.820, 1.480, 2.775, 2.4, "215/60 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("toyota_lc_80", "Toyota Land Cruiser 80 4.2 turbodiisel (1990-1997)", 2296, 0.43, 1.900, 1.890, 2.850, 2.1, "265/75 R15", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("toyota_prius_xw60", "Toyota Prius XW60 2.0 Hybrid (2023+)", 1400, 0.32, 1.780, 1.430, 2.750, 2.4, "195/50 R19", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_aygo_2", "Toyota Aygo II 1.0 (2014-2022)", 900, 0.29, 1.615, 1.460, 2.340, 2.3, "165/65 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("toyota_corolla_e80", "Toyota Corolla E80 1.3 (1983-1987)", 840, 0.35, 1.635, 1.346, 2.430, 2.1, "155/80 R13", A.NONE, 1.08, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("vw_golf_1", "VW Golf I 1.3 (1974-1983)", 750, 0.35, 1.610, 1.410, 2.400, 2.1, "155/80 R13", A.NONE, 1.08, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("vw_polo_2", "VW Polo II 1.0 (1981-1994)", 765, 0.36, 1.570, 1.350, 2.335, 2.0, "135/80 R13", A.NONE, 1.08, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("vw_passat_b2", "VW Passat B2 1.6 (1981-1988)", 905, 0.35, 1.685, 1.385, 2.550, 2.1, "165/80 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("vw_t3", "VW Transporter T3 1.6 turbodiisel (1979-1992)", 1395, 0.39, 1.844, 1.928, 2.455, 2.5, "185/80 R14", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("vw_crafter_1", "VW Crafter I 2.5 TDI (2006-2016)", 2025, 0.36, 1.993, 2.365, 3.250, 3.0, "235/65 R16C", A.MODERN, 1.05, _L4 + "; mass Mercedes Sprinter 906 realt (sama platvorm), rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("vw_amarok_2", "VW Amarok II 2.0 TDI (2023+)", 2187, 0.4, 1.910, 1.871, 3.270, 2.4, "255/70 R16", A.LATEST, 1.22, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_beetle_a4", "VW Beetle A4 1.6 (1998-2010)", 1205, 0.32, 1.724, 1.498, 2.508, 2.4, "195/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_scirocco_2", "VW Scirocco II 1.6 (1981-1992)", 950, 0.35, 1.645, 1.280, 2.400, 2.1, "175/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("volvo_960", "Volvo 960 2.5 (1990-1998)", 1600, 0.35, 1.750, 1.411, 2.770, 2.1, "195/65 R15", A.EARLY, 1.2, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_s70", "Volvo S70 2.5 (1996-2000)", 1430, 0.32, 1.760, 1.400, 2.660, 2.4, "195/60 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_s60_1", "Volvo S60 I 2.4 (2000-2009)", 1501, 0.32, 1.804, 1.428, 2.715, 2.4, "205/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lada_2105", "VAZ 2105 1.3 (1980-2010)", 995, 0.35, 1.620, 1.446, 2.424, 2.1, "175/70 R13", A.NONE, 0.95, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("lada_priora", "Lada Priora 1.6 (2007-2018)", 1163, 0.32, 1.680, 1.420, 2.492, 2.4, "175/65 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lada_kalina", "Lada Kalina 1.6 (2004-2018)", 1125, 0.32, 1.700, 1.500, 2.476, 2.4, "175/65 R14", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lada_largus", "Lada Largus 1.6 (2012+)", 1260, 0.33, 1.750, 1.670, 2.905, 2.4, "185/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lr_disco_1", "Land Rover Discovery 1 200Tdi (1989-1998)", 1925, 0.48, 1.795, 1.960, 2.540, 2.1, "205/80 R16", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("lr_disco_2", "Land Rover Discovery 2 Td5 (1998-2004)", 2020, 0.45, 1.860, 1.890, 2.540, 2.4, "235/70 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lr_disco_3", "Land Rover Discovery 3 2.7 TDV6 (2004-2009)", 2494, 0.4, 2.009, 1.887, 2.885, 2.4, "255/60 R18", A.MODERN, 1.2, _L4 + "; laius peeglitega kokkupandult (kere laius puudus), CdA veidi ülehinnatud, rõhk hinnang, Cd hinnang"),
    ("lr_rr_p38", "Land Rover Range Rover P38 2.5 diisel (1994-2002)", 2115, 0.4, 1.853, 1.817, 2.745, 2.1, "235/70 R16", A.EARLY, 1.12, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jeep_gc_zj", "Jeep Grand Cherokee ZJ 4.0 (1993-1998)", 1775, 0.44, 1.800, 1.690, 2.690, 2.1, "225/75 R15", A.EARLY, 1.12, _L4 + "; rõhk hinnang"),
    ("jeep_gc_wj", "Jeep Grand Cherokee WJ 2.7 CRD (1999-2004)", 1980, 0.45, 1.836, 1.762, 2.691, 2.4, "225/75 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang"),
    ("jeep_cherokee_xj", "Jeep Cherokee XJ 2.5 turbodiisel (1984-2001)", 1630, 0.43, 1.720, 1.621, 2.575, 2.1, "225/75 R15", A.EARLY, 1.12, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jeep_cherokee_kj", "Jeep Cherokee KJ 2.8 CRD (2001-2007)", 1845, 0.4, 1.820, 1.865, 2.650, 2.4, "235/70 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jeep_wrangler_tj", "Jeep Wrangler TJ 4.0 (1997-2006)", 1495, 0.45, 1.732, 1.780, 2.373, 2.4, "215/75 R15", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("porsche_911_996", "Porsche 911 Carrera 996 (1997-2005)", 1320, 0.3, 1.765, 1.305, 2.350, 2.4, "205/50 R17", A.EARLY, 1.32, _L4 + "; rõhk hinnang"),
    ("lexus_is_xe10", "Lexus IS 2.0 XE10 (1999-2005)", 1360, 0.32, 1.720, 1.420, 2.670, 2.4, "205/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("saab_93_1", "Saab 9-3 I 2.0 (1998-2002)", 1295, 0.32, 1.711, 1.428, 2.605, 2.4, "185/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("saab_9000", "Saab 9000 2.3 (1985-1998)", 1360, 0.34, 1.764, 1.420, 2.672, 2.1, "195/65 R15", A.EARLY, 1.2, _L4 + "; rõhk hinnang"),
    # 2026-09-29 üheksas ring (varem välja jäänud; puuduvad väärtused sõsarautolt, märkusega)
    ("audi_q5_3", "Audi Q5 III 2.0 TDI (2024+)", 1955, 0.31, 1.900, 1.625, 2.820, 2.4, "235/60 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("citroen_jumper_2", "Citroën Jumper II 2.0 HDi (1994-2006)", 1850, 0.35, 2.050, 2.150, 2.850, 3.0, "195/70 R15C", A.NONE, 1.08, _L4 + "; laius hinnang Ducato III järgi, ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang tühjale sõidukile"),
    ("fiat_ducato_2", "Fiat Ducato II 2.8 JTD (1994-2006)", 1850, 0.35, 2.050, 2.150, 2.850, 3.0, "205/70 R15C", A.NONE, 1.08, _L4 + "; laius hinnang Ducato III järgi, ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang tühjale sõidukile"),
    ("ford_escort_4", "Ford Escort Mk4 1.4 (1986-1990)", 1080, 0.35, 1.700, 1.346, 2.523, 2.1, "155/80 R13", A.NONE, 1.08, _L4 + "; mass hinnang, mõõdud hinnang järgmise põlvkonna (Escort 1990-2000) järgi, ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("ford_transit_6", "Ford Transit VI 2.4 TDCi (2000-2006)", 2000, 0.36, 1.974, 2.360, 3.300, 3.0, "215/75 R16C", A.EARLY, 1.05, _L4 + "; mass ja mõõdud Transit VII realt (sama platvorm, uuendus), rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("hyundai_accent_2", "Hyundai Accent II 1.3 (1999-2006)", 990, 0.33, 1.670, 1.395, 2.440, 2.3, "175/70 R13", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_vito_w638", "Mercedes-Benz Vito W638 2.2 CDI (1996-2003)", 2010, 0.36, 1.880, 1.844, 3.000, 2.8, "195/70 R15", A.EARLY, 1.1, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("mb_sprinter_901", "Mercedes Sprinter 901 2.2 CDI (1995-2006)", 2025, 0.36, 1.933, 2.365, 3.550, 3.0, "195/70 R15C", A.EARLY, 1.05, _L4 + "; mass hinnang Sprinter 906 järgi, rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("mb_g_w463_1", "Mercedes G350d W463 (1990-2018)", 2495, 0.54, 1.760, 1.951, 2.850, 2.1, "265/60 R18", A.EARLY, 1.12, _L4 + "; rõhk hinnang"),
    ("nissan_navara_d22", "Nissan Navara D22 2.5 dCi (1997-2005)", 1760, 0.4, 1.825, 1.705, 2.950, 2.4, "205/80 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_murano_z50", "Nissan Murano Z50 3.5 (2003-2008)", 1845, 0.36, 1.880, 1.690, 2.825, 2.4, "235/65 R18", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_sunny_n13", "Nissan Sunny N13 1.6 (1986-1990)", 1050, 0.35, 1.650, 1.350, 2.410, 2.1, "175/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("opel_corsa_a", "Opel Corsa A 1.2 (1982-1993)", 740, 0.36, 1.532, 1.365, 2.343, 2.0, "145/80 R13", A.NONE, 1.08, _L4 + "; ABS puudus, rõhk hinnang"),
    ("opel_movano_a", "Opel Movano A 2.5 CDTI (1998-2010)", 1871, 0.36, 1.990, 2.489, 3.577, 3.0, "195/65 R16C", A.EARLY, 1.05, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("opel_movano_c", "Opel Movano C 2.2 BlueHDi (2021+)", 2050, 0.36, 2.050, 2.254, 3.450, 3.0, "215/70 R15C", A.LATEST, 1.05, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("peugeot_boxer_2", "Peugeot Boxer II 2.8 HDi (1994-2006)", 1850, 0.36, 2.050, 2.150, 2.850, 3.0, "205/70 R15C", A.NONE, 1.08, _L4 + "; mass Fiat Ducato II (sama kere), kõrgus Fiat Ducato II (sama kere), teljevahe Fiat Ducato II (sama kere), laius hinnang Ducato III järgi, ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("renault_master_2", "Renault Master II 2.5 dCi (1998-2010)", 1871, 0.36, 1.990, 2.489, 3.577, 3.0, "215/65 R16C", A.EARLY, 1.05, _L4 + "; mass Opel Movano A realt (sama auto), rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("renault_trafic_1", "Renault Trafic I 2.1 D (1980-2001)", 1200, 0.39, 1.905, 1.971, 3.098, 2.8, "175/80 R14C", A.NONE, 1.08, _L4 + "; kõrgus ja teljevahe hinnang Trafic II järgi, ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("suzuki_grandvitara_1", "Suzuki Grand Vitara I 2.0 (1998-2005)", 1260, 0.36, 1.780, 1.740, 2.480, 2.4, "235/60 R16", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("suzuki_swift_2", "Suzuki Swift II 1.3 (1989-2003)", 1030, 0.36, 1.575, 1.350, 2.265, 2.0, "155/70 R13", A.NONE, 1.08, _L4 + "; mass hinnang Swift 2005-2010 järgi (tõenäoliselt ülehinnatud), ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("toyota_hilux_6", "Toyota Hilux VI 2.5 D-4D (1997-2005)", 1410, 0.4, 1.690, 1.760, 2.850, 2.4, "255/70 R15", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("toyota_carina_2", "Toyota Carina II 1.6 (1987-1992)", 1032, 0.35, 1.690, 1.370, 2.525, 2.1, "165/80 R13", A.NONE, 1.08, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("vw_caddy_2", "VW Caddy II 1.9 SDI (1996-2004)", 1135, 0.36, 1.696, 1.836, 2.601, 2.5, "175/65 R14", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_740", "Volvo 740 2.3 (1984-1992)", 1315, 0.35, 1.760, 1.430, 2.770, 2.1, "185/70 R14", A.EARLY, 1.2, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("skoda_120", "Škoda 120 1.2 (1976-1990)", 900, 0.35, 1.610, 1.400, 2.400, 2.1, "165/80 R13", A.NONE, 1.08, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("ford_transit_custom_2", "Ford Transit Custom II 2.0 EcoBlue (2023+)", 1790, 0.36, 2.032, 1.984, 3.100, 2.8, "215/65 R16C", A.LATEST, 1.1, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang"),
    ("mg_hs_2", "MG HS II 1.5 T-GDI (2024+)", 1660, 0.36, 1.890, 1.664, 2.765, 2.4, "235/45 R19", A.LATEST, 1.27, _L4 + "; mass Hybrid+ versioonilt, rõhk hinnang, Cd hinnang"),
    # 2026-09-30 kümnes ring: Eesti registri (Transpordiamet, 01.01.2026) järgi puuduvad põlvkonnad ja sõsarautod
    ("chrysler_voyager_5", "Chrysler Grand Voyager RT 2.8 CRD (2008-2016)", 2100, 0.33, 1.954, 1.750, 3.078, 2.4, "225/65 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("chrysler_voyager_3", "Chrysler Grand Voyager GS 2.5 TD (1995-2001)", 1880, 0.33, 1.950, 1.740, 2.878, 2.1, "215/65 R15", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("subaru_legacy_bn", "Subaru Legacy BN 2.5 (2014-2020)", 1573, 0.32, 1.839, 1.499, 2.751, 2.4, "225/55 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_thalia_1", "Renault Thalia I 1.4 (1999-2008)", 940, 0.33, 1.639, 1.437, 2.472, 2.3, "175/65 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_thalia_2", "Renault Thalia II 1.2 (2008-2013)", 904, 0.33, 1.639, 1.430, 2.473, 2.3, "175/65 R14", A.MODERN, 1.28, _L4 + "; laius Thalia I järgi (sama Clio II platvorm), rõhk hinnang, Cd hinnang"),
    ("ford_fusion", "Ford Fusion 1.4 (2002-2012)", 1085, 0.35, 1.724, 1.543, 2.486, 2.3, "195/60 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("ford_mustang_s197", "Ford Mustang S197 4.0 V6 (2004-2014)", 1530, 0.32, 1.875, 1.385, 2.720, 2.4, "215/65 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("ford_mustang_s550", "Ford Mustang S550 2.3 EcoBoost (2015-2023)", 1655, 0.33, 1.916, 1.381, 2.720, 2.4, "255/40 R19", A.LATEST, 1.4, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lexus_gs_s160", "Lexus GS S160 3.0 (1997-2005)", 1649, 0.3, 1.800, 1.440, 2.800, 2.4, "215/60 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("lexus_gs_s190", "Lexus GS 450h S190 (2005-2011)", 1875, 0.27, 1.820, 1.425, 2.850, 2.4, "245/40 R18", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("seat_cordoba_6l", "SEAT Córdoba III 1.4 (2002-2009)", 1090, 0.32, 1.698, 1.441, 2.460, 2.4, "185/60 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("seat_cordoba_6k", "SEAT Córdoba I 1.4 (1993-2002)", 945, 0.32, 1.640, 1.408, 2.440, 2.1, "175/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("honda_frv", "Honda FR-V 1.8 (2004-2009)", 1423, 0.33, 1.810, 1.610, 2.680, 2.4, "205/55 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_carnival_1", "Kia Carnival I 2.9 CRDi (1998-2006)", 2078, 0.33, 1.900, 1.735, 2.905, 2.4, "215/65 R15", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("kia_carnival_2", "Kia Carnival II 2.9 CRDi (2006-2014)", 2093, 0.34, 1.985, 1.815, 2.890, 2.4, "225/70 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang"),
    ("chrysler_pacifica_cs", "Chrysler Pacifica CS 3.5 V6 (2003-2008)", 2015, 0.36, 2.013, 1.688, 2.954, 2.4, "235/65 R17", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("chrysler_pacifica_ru", "Chrysler Pacifica RU 3.6 V6 (2016+)", 1964, 0.3, 2.022, 1.777, 3.089, 2.4, "235/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("nissan_pulsar_c13", "Nissan Pulsar C13 1.2 DIG-T (2014-2018)", 1190, 0.32, 1.768, 1.520, 2.700, 2.4, "195/60 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_phaeton", "VW Phaeton 3.0 TDI (2002-2016)", 2255, 0.32, 1.903, 1.450, 2.881, 2.4, "235/55 R17", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("suzuki_liana", "Suzuki Liana 1.6 (2001-2007)", 1215, 0.32, 1.690, 1.550, 2.480, 2.4, "185/65 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_r_w251", "Mercedes R320 CDI W251 (2005-2013)", 2250, 0.33, 1.922, 1.659, 2.980, 2.4, "235/65 R17", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_tayron", "VW Tayron 2.0 TDI (2024+)", 1696, 0.28, 1.853, 1.668, 2.788, 2.4, "215/65 R17", A.LATEST, 1.27, _L4 + "; rõhk hinnang"),
    ("volvo_c70_1", "Volvo C70 I 2.4 T (1997-2005)", 1471, 0.32, 1.820, 1.410, 2.660, 2.4, "225/50 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("volvo_c70_2", "Volvo C70 II 2.4i (2006-2013)", 1646, 0.32, 1.820, 1.400, 2.640, 2.4, "215/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("dodge_journey", "Dodge Journey 2.0 CRD (2008-2020)", 1820, 0.36, 1.878, 1.691, 2.890, 2.4, "225/65 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("citroen_c2", "Citroën C2 1.4 (2003-2009)", 987, 0.31, 1.659, 1.461, 2.315, 2.3, "175/65 R14", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("mitsu_grandis", "Mitsubishi Grandis 2.4 (2003-2011)", 1645, 0.33, 1.795, 1.655, 2.830, 2.4, "215/60 R16", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("chrysler_pt_cruiser", "Chrysler PT Cruiser 2.0 (2000-2010)", 1410, 0.32, 1.705, 1.600, 2.616, 2.4, "205/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("hyundai_sonata_nf", "Hyundai Sonata NF 2.4 (2004-2010)", 1463, 0.32, 1.832, 1.474, 2.730, 2.4, "215/60 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("lada_2103", "VAZ 2103 1.5 (1972-1984)", 965, 0.35, 1.611, 1.440, 2.424, 2.1, "175/70 R13", A.NONE, 0.95, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("hyundai_terracan", "Hyundai Terracan 2.9 CRDi (2001-2007)", 2065, 0.4, 1.860, 1.790, 2.750, 2.4, "255/65 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("chrysler_sebring_jr", "Chrysler Sebring JR 2.0 (2001-2006)", 1450, 0.32, 1.790, 1.395, 2.745, 2.4, "205/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("chrysler_sebring_js", "Chrysler Sebring JS 2.0 CRD (2007-2010)", 1775, 0.32, 1.843, 1.482, 2.765, 2.4, "215/60 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jeep_commander", "Jeep Commander XK 3.0 CRD (2006-2010)", 2245, 0.4, 1.899, 1.826, 2.780, 2.4, "245/65 R17", A.MODERN, 1.2, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("audi_a2", "Audi A2 1.4 (1999-2005)", 995, 0.33, 1.673, 1.553, 2.405, 2.3, "175/60 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_glk_x204", "Mercedes GLK 220 CDI X204 (2008-2015)", 1715, 0.34, 1.840, 1.689, 2.755, 2.4, "235/60 R17", A.MODERN, 1.25, _L4 + "; rõhk hinnang"),
    ("toyota_previa_2", "Toyota Previa II 2.0 D-4D (2000-2006)", 1705, 0.33, 1.790, 1.770, 2.900, 2.4, "205/65 R15", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_terrano_2", "Nissan Terrano II 2.7 TD (1993-2006)", 1850, 0.4, 1.735, 1.810, 2.650, 2.1, "215/75 R15", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("toyota_celica_t200", "Toyota Celica T200 1.8 (1993-1999)", 1170, 0.32, 1.750, 1.305, 2.450, 2.1, "195/65 R14", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("toyota_celica_t230", "Toyota Celica T230 1.8 (1999-2006)", 1070, 0.32, 1.735, 1.320, 2.600, 2.4, "195/60 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("citroen_c_elysee", "Citroën C-Elysée 1.6 HDi (2012-2020)", 1090, 0.32, 1.748, 1.466, 2.652, 2.4, "185/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("opel_signum", "Opel Signum 1.9 CDTI (2003-2008)", 1545, 0.32, 1.798, 1.460, 2.830, 2.4, "215/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("jaguar_xtype", "Jaguar X-Type 2.0 D (2001-2009)", 1500, 0.32, 1.789, 1.430, 2.710, 2.4, "205/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jaguar_stype", "Jaguar S-Type 2.7 D (1999-2007)", 1722, 0.32, 1.819, 1.441, 2.909, 2.4, "235/50 R17", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jaguar_xj_x350", "Jaguar XJ X350 2.7 D (2003-2009)", 1657, 0.32, 1.860, 1.448, 3.034, 2.4, "235/55 R17", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jaguar_xj_x351", "Jaguar XJ X351 3.0 D (2009-2019)", 1796, 0.32, 1.894, 1.457, 3.032, 2.4, "245/50 R18", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_tiida_c11", "Nissan Tiida C11 1.6 (2004-2012)", 1278, 0.32, 1.695, 1.535, 2.600, 2.4, "195/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("hyundai_galloper_2", "Hyundai Galloper II 2.5 TD (1998-2003)", 1845, 0.45, 1.785, 1.890, 2.695, 2.4, "235/75 R15", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("nissan_patrol_y60", "Nissan Patrol Y60 2.8 TD (1987-1997)", 1950, 0.43, 1.800, 1.785, 2.970, 2.1, "215/80 R16", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("opel_frontera_a", "Opel Frontera A 2.3 TD (1991-1998)", 1785, 0.4, 1.764, 1.753, 2.760, 2.1, "235/70 R15", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("hyundai_coupe_gk", "Hyundai Coupe GK 2.0 (2001-2009)", 1280, 0.32, 1.760, 1.330, 2.530, 2.4, "205/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_clk_w208", "Mercedes CLK 200 W208 (1997-2002)", 1300, 0.31, 1.722, 1.371, 2.690, 2.4, "205/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("mb_clk_w209", "Mercedes CLK 200 Kompressor W209 (2002-2009)", 1465, 0.28, 1.740, 1.413, 2.715, 2.4, "205/55 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("mb_sl_r129", "Mercedes SL 500 R129 (1989-2001)", 1770, 0.36, 1.812, 1.303, 2.515, 2.1, "225/55 R16", A.EARLY, 1.32, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_sl_r230", "Mercedes SL 500 R230 (2001-2012)", 1770, 0.33, 1.815, 1.298, 2.560, 2.4, "255/45 R17", A.EARLY, 1.32, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("mb_slk_r170", "Mercedes SLK 200 R170 (1996-2004)", 1290, 0.33, 1.715, 1.274, 2.400, 2.4, "205/60 R15", A.EARLY, 1.32, _L4 + "; rõhk hinnang"),
    ("mb_slk_r171", "Mercedes SLK 200 Kompressor R171 (2004-2011)", 1315, 0.32, 1.777, 1.296, 2.430, 2.4, "205/55 R16", A.MODERN, 1.36, _L4 + "; rõhk hinnang"),
    ("mb_cl_c215", "Mercedes CL 500 C215 (1999-2006)", 1795, 0.28, 1.857, 1.398, 2.885, 2.4, "225/55 R17", A.EARLY, 1.24, _L4 + "; rõhk hinnang"),
    ("mb_cl_c216", "Mercedes CL 500 C216 (2006-2014)", 1920, 0.27, 1.871, 1.418, 2.955, 2.4, "235/55 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang"),
    ("zaz_968m", "ZAZ Zaporožets 968M 1.2 (1979-1994)", 800, 0.36, 1.490, 1.425, 2.160, 2.0, "155/70 R13", A.NONE, 0.95, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("toyota_camry_xv30", "Toyota Camry XV30 2.4 (2001-2006)", 1390, 0.32, 1.795, 1.500, 2.720, 2.4, "215/60 R16", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_fluence", "Renault Fluence 1.6 (2009-2016)", 1225, 0.32, 1.809, 1.479, 2.702, 2.4, "205/65 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("lr_defender_td5", "Land Rover Defender Td5 (1998-2006)", 2055, 0.45, 1.790, 2.059, 2.794, 2.4, "205/80 R16", A.EARLY, 1.16, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("renault_symbioz", "Renault Symbioz E-Tech 1.6 hübriid (2024+)", 1426, 0.36, 1.797, 1.575, 2.638, 2.4, "215/55 R18", A.LATEST, 1.27, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("honda_civic_5", "Honda Civic V 1.5 (1991-1995)", 950, 0.32, 1.695, 1.345, 2.570, 2.1, "175/70 R13", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("subaru_levorg", "Subaru Levorg 1.6 GT (2015-2020)", 1537, 0.32, 1.780, 1.485, 2.650, 2.4, "215/50 R17", A.LATEST, 1.3, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_eos", "VW Eos 2.0 TSI (2006-2015)", 1586, 0.32, 1.791, 1.444, 2.578, 2.4, "215/55 R16", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("smart_fortwo_450", "Smart fortwo 450 0.7 (1998-2007)", 805, 0.33, 1.515, 1.549, 1.812, 2.3, "145/65 R15", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("smart_fortwo_451", "Smart fortwo 451 1.0 (2007-2014)", 750, 0.33, 1.559, 1.542, 1.867, 2.3, "155/60 R15", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jeep_patriot", "Jeep Patriot 2.0 CRD (2007-2017)", 1515, 0.36, 1.755, 1.630, 2.635, 2.4, "215/60 R17", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("vw_lupo", "VW Lupo 1.0 (1998-2005)", 884, 0.33, 1.640, 1.460, 2.323, 2.3, "155/70 R13", A.EARLY, 1.24, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("jeep_wrangler_yj", "Jeep Wrangler YJ 4.0 (1987-1995)", 1555, 0.48, 1.740, 1.765, 2.373, 2.1, "225/75 R15", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("mb_amg_gt_c190", "Mercedes AMG GT 4.0 V8 C190 (2014-2021)", 1625, 0.33, 2.075, 1.287, 2.630, 2.4, "265/35 R19", A.MODERN, 1.36, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("hyundai_matrix", "Hyundai Matrix 1.6 (2001-2010)", 1323, 0.33, 1.740, 1.635, 2.600, 2.4, "185/65 R14", A.EARLY, 1.21, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("audi_coupe_b3", "Audi Coupé B3 2.0 (1988-1996)", 1150, 0.35, 1.716, 1.375, 2.556, 2.1, "195/65 R15", A.NONE, 1.08, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("dodge_caliber", "Dodge Caliber 2.0 CRD (2006-2012)", 1425, 0.32, 1.800, 1.535, 2.635, 2.4, "215/60 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("dodge_challenger_lc", "Dodge Challenger LC 5.7 V8 (2008-2023)", 1852, 0.33, 1.923, 1.449, 2.946, 2.4, "235/55 R18", A.MODERN, 1.36, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("dodge_durango_wd", "Dodge Durango WD 3.6 V6 (2011+)", 2157, 0.35, 1.925, 1.801, 3.043, 2.4, "265/60 R18", A.MODERN, 1.25, _L4 + "; rõhk hinnang"),
    ("dodge_nitro", "Dodge Nitro 2.8 CRD (2007-2011)", 1940, 0.36, 1.856, 1.755, 2.763, 2.4, "235/70 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("dodge_charger_ld", "Dodge Charger LD 3.6 V6 (2011-2023)", 1813, 0.32, 1.905, 1.482, 3.052, 2.4, "215/65 R17", A.MODERN, 1.28, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("cadillac_escalade_3", "Cadillac Escalade III 6.2 V8 (2006-2014)", 2609, 0.4, 2.007, 1.887, 2.946, 2.4, "265/65 R18", A.MODERN, 1.2, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("cadillac_srx_2", "Cadillac SRX II 3.0 V6 (2010-2016)", 1915, 0.36, 1.910, 1.669, 2.807, 2.4, "235/65 R18", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang"),
    ("gaz_2410", "GAZ Volga 24-10 2.4 (1985-1992)", 1400, 0.35, 1.800, 1.476, 2.800, 2.1, "205/70 R14", A.NONE, 0.95, _L4 + "; ABS oli lisavarustus; kui sinu autol on ABS, on pidurdusmaa lühem, rõhk hinnang, Cd hinnang"),
    ("gaz_21", "GAZ Volga 21 2.4 (1956-1970)", 1460, 0.35, 1.885, 1.620, 2.700, 2.1, "205/75 R15", A.NONE, 0.95, _L4 + "; ABS puudus, rõhk hinnang, Cd hinnang"),
    ("nissan_primastar", "Nissan Primastar (2002-2014)",      1700, 0.36, 1.904, 1.971, 3.098, 2.7, "195/65 R16C", A.MODERN, 1.08, "mõõdud ligikaudsed" + "; andmed sõsarautolt Renault Trafic II (2001-2014) (sama kere)"),
    ("mb_viano_w639", "Mercedes Viano 2.2 CDI W639 (2003-2014)",      1900, 0.36, 1.901, 1.875, 3.200, 2.7, "205/65 R16C", A.MODERN, 1.08, "mõõdud ligikaudsed" + "; andmed sõsarautolt Mercedes Vito W639 (2003-2014) (sama kere); sõiduauto-Viano rehvimõõt võib Vito omast erineda"),
    ("mb_v_w638", "Mercedes V-klass 220 CDI W638 (1996-2003)", 2010, 0.36, 1.880, 1.844, 3.000, 2.8, "195/70 R15", A.EARLY, 1.1, _L4 + "; rõhk hinnang tühjale sõidukile, Cd hinnang" + "; andmed sõsarautolt Mercedes-Benz Vito W638 2.2 CDI (1996-2003) (sama kere); sõiduauto-V-klassi rehvimõõt võib Vito omast erineda"),
    ("lancia_voyager", "Lancia Voyager 2.8 CRD (2011-2015)", 2100, 0.33, 1.954, 1.750, 3.078, 2.4, "225/65 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang" + "; andmed sõsarautolt Chrysler Grand Voyager RT 2.8 CRD (2008-2016) (sama kere)"),
    ("dodge_grand_caravan", "Dodge Grand Caravan RT 3.6 V6 (2008-2020)", 2100, 0.33, 1.954, 1.750, 3.078, 2.4, "225/65 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang" + "; andmed sõsarautolt Chrysler Grand Voyager RT 2.8 CRD (2008-2016) (sama kere); mass ja rehvid 2.8 CRD versioonilt (Dodge’il bensiinimootor)"),
    ("lancia_thema", "Lancia Thema 3.0 CRD (2011-2014)",       1962, 0.32, 1.902, 1.492, 3.052, 2.4, "225/60 R18", A.MODERN, 1.26, "rõhk hinnang" + "; andmed sõsarautolt Chrysler 300C LD (2011-2023) (sama kere)"),
    ("fiat_freemont", "Fiat Freemont 2.0 Multijet (2011-2016)", 1820, 0.36, 1.878, 1.691, 2.890, 2.4, "225/65 R16", A.MODERN, 1.25, _L4 + "; rõhk hinnang, Cd hinnang" + "; andmed sõsarautolt Dodge Journey 2.0 CRD (2008-2020) (sama kere)"),
    ("chevrolet_trax", "Chevrolet Trax (2013-2019)",            1350, 0.35, 1.774, 1.658, 2.555, 2.3, "215/60 R17", A.MODERN, 1.24, _L + "; andmed sõsarautolt Opel Mokka A (2012-2019) (sama kere)"),
    ("citroen_c_crosser", "Citroën C-Crosser (2007-2012)",1600,0.36, 1.800, 1.680, 2.670, 2.3, "215/70 R16", A.MODERN, 1.22, _L + "; andmed sõsarautolt Mitsubishi Outlander II (2006-2012) (sama kere)"),
    ("peugeot_4007", "Peugeot 4007 (2007-2012)",1600,0.36, 1.800, 1.680, 2.670, 2.3, "215/70 R16", A.MODERN, 1.22, _L + "; andmed sõsarautolt Mitsubishi Outlander II (2006-2012) (sama kere)"),
    ("fiat_500_fl", "Fiat 500 (2015-2024)",             865, 0.325, 1.627, 1.488, 2.300, 2.3, "175/65 R14", A.MODERN, 1.22, "andmed sõsarautolt Fiat 500 (2007-2015) (sama kere); uuendatud 500 (2015); rehvid ja mõõdud 2007-2015 realt"),
]
