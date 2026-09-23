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
    ("toyota_yariscross","Toyota Yaris Cross Hybrid (2021+)",1175,0.35,1.765,1.590, 2.560, 2.3, "215/50 R18", A.LATEST, 1.27, ""),
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
