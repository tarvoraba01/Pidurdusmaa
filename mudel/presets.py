"""
Valmis autod ja rehvid.

TÄHTIS: `wet_grip_index` väärtused siin on KLASSI KESKPUNKTID ehk hinnangud.
Päris süsteemis tuleb G iga konkreetse rehvi ja mõõdu kohta EPREL-ist
(EL-i ametlik rehviregister, ~310 000 registreeringut). Sama rehvimudel
võib eri mõõdus olla eri klassis — seepärast on see väli siin selgelt
"asendatav kohatäide", mitte lõplik andmestik.

Kuiv-, lume- ja jäähaardumist EL-i märgis ei kata. Nende jaoks on
kategooriapõhine baas mudelis (model.py) ja siin on üksikutel rehvidel
`mu_*_override`, mis on tuletatud päris testidest (vt anchors.py).
"""

from .model import AbsClass, Tyre, TyreCategory, Vehicle

C = TyreCategory

# G klassi keskpunktid C1-rehvidele (EL 2020/740, Lisa I osa B)
G_CLASS = {"A": 1.60, "B": 1.47, "C": 1.32, "D": 1.17, "E": 1.05}


# ---------------------------------------------------------------------------
# Autod
# ---------------------------------------------------------------------------

VEHICLES = {
    # --- võrdlusautod, mida kasutatakse ankrutestides ---------------------
    "vw_golf_8": Vehicle(
        name="VW Golf 8 1.5 TSI (2020)", kerb_mass_kg=1320,
        abs_class=AbsClass.LATEST, cda_m2=0.63, cog_height_m=0.55,
        wheelbase_m=2.62, recommended_pressure_bar=2.3,
        oem_size="205/55 R16", brake_capacity_g=1.3),
    "audi_a3": Vehicle(
        name="Audi A3 Sportback 8Y (2021)", kerb_mass_kg=1345,
        abs_class=AbsClass.LATEST, cda_m2=0.64, cog_height_m=0.55,
        wheelbase_m=2.64, recommended_pressure_bar=2.4,
        oem_size="225/45 R17", brake_capacity_g=1.3),
    "skoda_octavia": Vehicle(
        name="Škoda Octavia IV 2.0 TDI (2021)", kerb_mass_kg=1425,
        abs_class=AbsClass.LATEST, cda_m2=0.65, cog_height_m=0.55,
        wheelbase_m=2.69, recommended_pressure_bar=2.4,
        oem_size="225/45 R17", brake_capacity_g=1.3),
    "toyota_corolla": Vehicle(
        name="Toyota Corolla 1.8 Hybrid (2021)", kerb_mass_kg=1375,
        abs_class=AbsClass.LATEST, cda_m2=0.63, cog_height_m=0.55,
        wheelbase_m=2.7, recommended_pressure_bar=2.3,
        oem_size="205/55 R16", brake_capacity_g=1.3),
    "passat_b5": Vehicle(
        name="VW Passat B5 1.9 TDI (1999)", kerb_mass_kg=1380,
        abs_class=AbsClass.EARLY, cda_m2=0.66, cog_height_m=0.56,
        wheelbase_m=2.7, recommended_pressure_bar=2.0,
        oem_size="195/65 R15", brake_capacity_g=1.3),

    # --- Eesti sõidukipark (vt vehicles_ee.py: allikad ja meetod) --------
    "bmw_320d_e90": Vehicle(
        name="BMW 320d E90 (2005-2012)", kerb_mass_kg=1450,
        abs_class=AbsClass.MODERN, cda_m2=0.6, cog_height_m=0.59,
        wheelbase_m=2.76, recommended_pressure_bar=2.3,
        oem_size="205/55 R16", brake_capacity_g=1.3),
    "bmw_320d_f30": Vehicle(
        name="BMW 320d F30 (2012-2019)", kerb_mass_kg=1495,
        abs_class=AbsClass.LATEST, cda_m2=0.58, cog_height_m=0.59,
        wheelbase_m=2.81, recommended_pressure_bar=2.4,
        oem_size="225/50 R17", brake_capacity_g=1.3),
    "bmw_520d_e60": Vehicle(
        name="BMW 520d E60 (2003-2010)", kerb_mass_kg=1585,
        abs_class=AbsClass.MODERN, cda_m2=0.608, cog_height_m=0.61,
        wheelbase_m=2.888, recommended_pressure_bar=2.4,
        oem_size="225/55 R16", brake_capacity_g=1.28),
    "bmw_520d_f10": Vehicle(
        name="BMW 520d F10 (2010-2017)", kerb_mass_kg=1615,
        abs_class=AbsClass.LATEST, cda_m2=0.61, cog_height_m=0.61,
        wheelbase_m=2.968, recommended_pressure_bar=2.5,
        oem_size="225/55 R17", brake_capacity_g=1.3),
    "bmw_520d_g30": Vehicle(
        name="BMW 520d G30 (2017-2023)", kerb_mass_kg=1610,
        abs_class=AbsClass.LATEST, cda_m2=0.5, cog_height_m=0.61,
        wheelbase_m=2.975, recommended_pressure_bar=2.5,
        oem_size="225/55 R17", brake_capacity_g=1.32),
    "vw_passat_b6": Vehicle(
        name="VW Passat B6 2.0 TDI (2005-2010)", kerb_mass_kg=1440,
        abs_class=AbsClass.MODERN, cda_m2=0.645, cog_height_m=0.61,
        wheelbase_m=2.709, recommended_pressure_bar=2.4,
        oem_size="205/55 R16", brake_capacity_g=1.28),
    "vw_passat_b7": Vehicle(
        name="VW Passat B7 2.0 TDI (2010-2014)", kerb_mass_kg=1450,
        abs_class=AbsClass.MODERN, cda_m2=0.644, cog_height_m=0.61,
        wheelbase_m=2.712, recommended_pressure_bar=2.4,
        oem_size="215/55 R16", brake_capacity_g=1.28),
    "vw_golf_5": Vehicle(
        name="VW Golf V 1.9 TDI (2003-2008)", kerb_mass_kg=1310,
        abs_class=AbsClass.MODERN, cda_m2=0.694, cog_height_m=0.61,
        wheelbase_m=2.578, recommended_pressure_bar=2.3,
        oem_size="195/65 R15", brake_capacity_g=1.28),
    "vw_golf_6": Vehicle(
        name="VW Golf VI 1.6 TDI (2008-2012)", kerb_mass_kg=1320,
        abs_class=AbsClass.MODERN, cda_m2=0.677, cog_height_m=0.61,
        wheelbase_m=2.578, recommended_pressure_bar=2.3,
        oem_size="205/55 R16", brake_capacity_g=1.28),
    "vw_golf_7": Vehicle(
        name="VW Golf VII 1.6 TDI (2012-2019)", kerb_mass_kg=1280,
        abs_class=AbsClass.LATEST, cda_m2=0.629, cog_height_m=0.6,
        wheelbase_m=2.637, recommended_pressure_bar=2.3,
        oem_size="205/55 R16", brake_capacity_g=1.3),
    "skoda_octavia_2": Vehicle(
        name="Škoda Octavia II 1.9 TDI (2004-2013)", kerb_mass_kg=1315,
        abs_class=AbsClass.MODERN, cda_m2=0.644, cog_height_m=0.6,
        wheelbase_m=2.578, recommended_pressure_bar=2.2,
        oem_size="195/65 R15", brake_capacity_g=1.28),
    "skoda_octavia_3": Vehicle(
        name="Škoda Octavia III 2.0 TDI (2013-2020)", kerb_mass_kg=1280,
        abs_class=AbsClass.LATEST, cda_m2=0.616, cog_height_m=0.6,
        wheelbase_m=2.686, recommended_pressure_bar=2.4,
        oem_size="205/55 R16", brake_capacity_g=1.3),
    "skoda_superb_3": Vehicle(
        name="Škoda Superb III 2.0 TDI (2015-2023)", kerb_mass_kg=1450,
        abs_class=AbsClass.LATEST, cda_m2=0.636, cog_height_m=0.61,
        wheelbase_m=2.841, recommended_pressure_bar=2.4,
        oem_size="215/55 R17", brake_capacity_g=1.3),
    "audi_a4_b8": Vehicle(
        name="Audi A4 B8 2.0 TDI (2008-2015)", kerb_mass_kg=1470,
        abs_class=AbsClass.MODERN, cda_m2=0.584, cog_height_m=0.59,
        wheelbase_m=2.808, recommended_pressure_bar=2.4,
        oem_size="225/50 R17", brake_capacity_g=1.3),
    "audi_a6_c7": Vehicle(
        name="Audi A6 C7 2.0 TDI (2011-2018)", kerb_mass_kg=1575,
        abs_class=AbsClass.LATEST, cda_m2=0.588, cog_height_m=0.6,
        wheelbase_m=2.912, recommended_pressure_bar=2.5,
        oem_size="225/55 R17", brake_capacity_g=1.3),
    "mb_e220_w212": Vehicle(
        name="Mercedes E220 CDI W212 (2009-2016)", kerb_mass_kg=1660,
        abs_class=AbsClass.MODERN, cda_m2=0.567, cog_height_m=0.61,
        wheelbase_m=2.874, recommended_pressure_bar=2.4,
        oem_size="225/55 R16", brake_capacity_g=1.3),
    "toyota_corolla_e120": Vehicle(
        name="Toyota Corolla E120 (2002-2007)", kerb_mass_kg=1180,
        abs_class=AbsClass.MODERN, cda_m2=0.628, cog_height_m=0.61,
        wheelbase_m=2.6, recommended_pressure_bar=2.2,
        oem_size="195/65 R15", brake_capacity_g=1.25),
    "toyota_avensis_t25": Vehicle(
        name="Toyota Avensis T25 (2003-2008)", kerb_mass_kg=1390,
        abs_class=AbsClass.MODERN, cda_m2=0.605, cog_height_m=0.61,
        wheelbase_m=2.7, recommended_pressure_bar=2.3,
        oem_size="205/60 R16", brake_capacity_g=1.26),
    "toyota_avensis_t27": Vehicle(
        name="Toyota Avensis T27 (2009-2018)", kerb_mass_kg=1430,
        abs_class=AbsClass.LATEST, cda_m2=0.623, cog_height_m=0.61,
        wheelbase_m=2.7, recommended_pressure_bar=2.4,
        oem_size="205/60 R16", brake_capacity_g=1.28),
    "toyota_rav4_4": Vehicle(
        name="Toyota RAV4 IV (2013-2018)", kerb_mass_kg=1560,
        abs_class=AbsClass.LATEST, cda_m2=0.813, cog_height_m=0.68,
        wheelbase_m=2.66, recommended_pressure_bar=2.3,
        oem_size="225/65 R17", brake_capacity_g=1.25),
    "toyota_rav4_5": Vehicle(
        name="Toyota RAV4 V Hybrid (2019+)", kerb_mass_kg=1660,
        abs_class=AbsClass.LATEST, cda_m2=0.83, cog_height_m=0.69,
        wheelbase_m=2.69, recommended_pressure_bar=2.4,
        oem_size="225/65 R17", brake_capacity_g=1.27),
    "vw_tiguan_1": Vehicle(
        name="VW Tiguan I 2.0 TDI (2007-2016)", kerb_mass_kg=1600,
        abs_class=AbsClass.MODERN, cda_m2=0.937, cog_height_m=0.69,
        wheelbase_m=2.604, recommended_pressure_bar=2.3,
        oem_size="215/65 R16", brake_capacity_g=1.24),
    "vw_tiguan_2": Vehicle(
        name="VW Tiguan II 2.0 TDI (2016-2023)", kerb_mass_kg=1585,
        abs_class=AbsClass.LATEST, cda_m2=0.792, cog_height_m=0.69,
        wheelbase_m=2.681, recommended_pressure_bar=2.4,
        oem_size="215/65 R17", brake_capacity_g=1.28),
    "nissan_qashqai_j11": Vehicle(
        name="Nissan Qashqai J11 (2013-2021)", kerb_mass_kg=1400,
        abs_class=AbsClass.LATEST, cda_m2=0.763, cog_height_m=0.66,
        wheelbase_m=2.646, recommended_pressure_bar=2.3,
        oem_size="215/60 R17", brake_capacity_g=1.26),
    "volvo_xc60_1": Vehicle(
        name="Volvo XC60 I (2008-2017)", kerb_mass_kg=1770,
        abs_class=AbsClass.MODERN, cda_m2=0.941, cog_height_m=0.71,
        wheelbase_m=2.774, recommended_pressure_bar=2.4,
        oem_size="235/60 R18", brake_capacity_g=1.24),
    "volvo_v70_3": Vehicle(
        name="Volvo V70 III (2007-2016)", kerb_mass_kg=1600,
        abs_class=AbsClass.MODERN, cda_m2=0.716, cog_height_m=0.64,
        wheelbase_m=2.816, recommended_pressure_bar=2.4,
        oem_size="215/55 R16", brake_capacity_g=1.28),
    "kia_sportage_3": Vehicle(
        name="Kia Sportage III (2010-2016)", kerb_mass_kg=1500,
        abs_class=AbsClass.MODERN, cda_m2=0.881, cog_height_m=0.67,
        wheelbase_m=2.64, recommended_pressure_bar=2.3,
        oem_size="215/70 R16", brake_capacity_g=1.24),
    "honda_crv_3": Vehicle(
        name="Honda CR-V III (2007-2012)", kerb_mass_kg=1560,
        abs_class=AbsClass.MODERN, cda_m2=0.863, cog_height_m=0.69,
        wheelbase_m=2.62, recommended_pressure_bar=2.3,
        oem_size="225/65 R17", brake_capacity_g=1.24),
    "mitsubishi_outlander_3": Vehicle(
        name="Mitsubishi Outlander III (2012-2021)", kerb_mass_kg=1520,
        abs_class=AbsClass.LATEST, cda_m2=0.828, cog_height_m=0.69,
        wheelbase_m=2.67, recommended_pressure_bar=2.3,
        oem_size="225/55 R18", brake_capacity_g=1.25),
    "subaru_forester_sj": Vehicle(
        name="Subaru Forester SJ (2013-2018)", kerb_mass_kg=1520,
        abs_class=AbsClass.LATEST, cda_m2=0.905, cog_height_m=0.71,
        wheelbase_m=2.64, recommended_pressure_bar=2.3,
        oem_size="225/60 R17", brake_capacity_g=1.25),
    "opel_astra_h": Vehicle(
        name="Opel Astra H (2004-2010)", kerb_mass_kg=1250,
        abs_class=AbsClass.MODERN, cda_m2=0.68, cog_height_m=0.6,
        wheelbase_m=2.614, recommended_pressure_bar=2.2,
        oem_size="195/65 R15", brake_capacity_g=1.25),
    "ford_focus_2": Vehicle(
        name="Ford Focus II (2004-2011)", kerb_mass_kg=1250,
        abs_class=AbsClass.MODERN, cda_m2=0.732, cog_height_m=0.62,
        wheelbase_m=2.64, recommended_pressure_bar=2.3,
        oem_size="195/65 R15", brake_capacity_g=1.26),
    "ford_mondeo_4": Vehicle(
        name="Ford Mondeo IV (2007-2014)", kerb_mass_kg=1520,
        abs_class=AbsClass.MODERN, cda_m2=0.704, cog_height_m=0.62,
        wheelbase_m=2.85, recommended_pressure_bar=2.4,
        oem_size="215/55 R16", brake_capacity_g=1.28),
    "mazda_6_gh": Vehicle(
        name="Mazda 6 GH (2008-2012)", kerb_mass_kg=1420,
        abs_class=AbsClass.MODERN, cda_m2=0.601, cog_height_m=0.6,
        wheelbase_m=2.725, recommended_pressure_bar=2.3,
        oem_size="205/60 R16", brake_capacity_g=1.27),
    "peugeot_308_1": Vehicle(
        name="Peugeot 308 I (2007-2013)", kerb_mass_kg=1330,
        abs_class=AbsClass.MODERN, cda_m2=0.7, cog_height_m=0.62,
        wheelbase_m=2.608, recommended_pressure_bar=2.3,
        oem_size="205/55 R16", brake_capacity_g=1.25),
    "renault_megane_3": Vehicle(
        name="Renault Mégane III (2008-2016)", kerb_mass_kg=1280,
        abs_class=AbsClass.MODERN, cda_m2=0.684, cog_height_m=0.61,
        wheelbase_m=2.641, recommended_pressure_bar=2.3,
        oem_size="205/55 R16", brake_capacity_g=1.25),
    "hyundai_i30_2": Vehicle(
        name="Hyundai i30 II (2011-2016)", kerb_mass_kg=1300,
        abs_class=AbsClass.MODERN, cda_m2=0.652, cog_height_m=0.61,
        wheelbase_m=2.65, recommended_pressure_bar=2.3,
        oem_size="195/65 R15", brake_capacity_g=1.26),

    # --- uuemad ja erijuhud ----------------------------------------------
    "bmw_320d": Vehicle(
        name="BMW 320d G20 (2020)", kerb_mass_kg=1545,
        abs_class=AbsClass.LATEST, cda_m2=0.6, cog_height_m=0.54,
        wheelbase_m=2.85, recommended_pressure_bar=2.4,
        oem_size="225/45 R18", brake_capacity_g=1.3),
    "tesla_model3": Vehicle(
        name="Tesla Model 3 LR (2022)", kerb_mass_kg=1830,
        abs_class=AbsClass.LATEST, cda_m2=0.53, cog_height_m=0.47,
        wheelbase_m=2.88, recommended_pressure_bar=2.9,
        oem_size="235/45 R18", brake_capacity_g=1.3),
    "vw_passat_b8": Vehicle(
        name="VW Passat B8 2.0 TDI (2019)", kerb_mass_kg=1520,
        abs_class=AbsClass.LATEST, cda_m2=0.63, cog_height_m=0.55,
        wheelbase_m=2.79, recommended_pressure_bar=2.4,
        oem_size="215/55 R17", brake_capacity_g=1.3),
    "volvo_xc60": Vehicle(
        name="Volvo XC60 B4 (2021)", kerb_mass_kg=1900,
        abs_class=AbsClass.LATEST, cda_m2=0.85, cog_height_m=0.68,
        wheelbase_m=2.87, recommended_pressure_bar=2.5,
        oem_size="235/60 R18", brake_capacity_g=1.3),
    "vw_transporter": Vehicle(
        name="VW Transporter T6.1 (2020)", kerb_mass_kg=2050,
        abs_class=AbsClass.MODERN, cda_m2=1.25, cog_height_m=0.85,
        wheelbase_m=3.0, recommended_pressure_bar=3.0,
        oem_size="215/65 R16", brake_capacity_g=1.1),
    "vw_golf_4": Vehicle(
        name="VW Golf IV 1.9 TDI (2001)", kerb_mass_kg=1240,
        abs_class=AbsClass.EARLY, cda_m2=0.68, cog_height_m=0.55,
        wheelbase_m=2.51, recommended_pressure_bar=2.2,
        oem_size="195/65 R15", brake_capacity_g=1.3),
    "lada_2107": Vehicle(
        name="VAZ 2107 (ABS puudub)", kerb_mass_kg=1060,
        abs_class=AbsClass.NONE, cda_m2=0.75, cog_height_m=0.58,
        wheelbase_m=2.42, recommended_pressure_bar=1.9,
        oem_size="175/70 R13", brake_capacity_g=0.85),
}


# Autod, mis on olemas AINULT selleks, et ankrutestid arvutuda. Neid ei
# panda veebilehe nimekirja -- keegi Eestis ei otsi VW Polo Vivo't ega
# Lõuna-Aafrika Ford Rangeri. Kalibreerimine kasutab VEHICLES + neid.
ANCHOR_VEHICLES = {
    "polo_vivo": Vehicle(
        name="VW Polo Vivo (2019, SATC kruusatest)", kerb_mass_kg=1030,
        abs_class=AbsClass.LATEST, cda_m2=0.63, cog_height_m=0.54,
        wheelbase_m=2.47, recommended_pressure_bar=2.2,
        oem_size="175/70 R14", brake_capacity_g=1.3),
    # Sama auto, ABS füüsiliselt välja lülitatud (testis tehti nii).
    "polo_vivo_noabs": Vehicle(
        name="VW Polo Vivo, ABS väljas (SATC kruusatest)", kerb_mass_kg=1030,
        abs_class=AbsClass.NONE, cda_m2=0.63, cog_height_m=0.54,
        wheelbase_m=2.47, recommended_pressure_bar=2.2,
        oem_size="175/70 R14", brake_capacity_g=1.3),
    "ford_ranger_fx4": Vehicle(
        name="Ford Ranger FX4 (SA4x4 kruusatest)", kerb_mass_kg=2200,
        abs_class=AbsClass.LATEST, cda_m2=1.05, cog_height_m=0.78,
        wheelbase_m=3.22, recommended_pressure_bar=2.4,
        oem_size="265/65 R17", brake_capacity_g=1.15),
}

EE_SHADOWED = []


def _load_ee_vehicles():
    """Teise laine autod ehitatakse OTSE vehicles_ee.py tabelist.

    Esimese laine omad on ülal käsitsi kirja pandud (ajalooline põhjus);
    uued tulevad tabelist, et need kaks faili ei saaks lahku triivida.
    Juba olemasolevaid võtmeid ei kirjutata üle."""
    from .vehicles_ee import EE_VEHICLES, FRONTAL_AREA_K
    # VALVUR. Sõnastikku ehitades kirjutab hilisem rida varasema vaikselt
    # üle -- lisasin kogemata Tesla Model 3 teist korda ja ta lihtsalt
    # kadus ära, ilma et miski oleks piiksatanud. Nüüd piiksatab.
    _seen = {}
    for _r in EE_VEHICLES:
        if _r[0] in _seen:
            raise ValueError(
                f"vehicles_ee.py: võti {_r[0]!r} on kaks korda — "
                f"{_seen[_r[0]]!r} ja {_r[1]!r}")
        _seen[_r[0]] = _r[1]
    added = {}
    for row in EE_VEHICLES:
        key, name, mass, cd, width, height, wb, press, size, abs_cls, brake = row[:11]
        if key in VEHICLES or key in added:
            # VARJATUD RIDA. Baasnimekiri (ülalpool selles failis) VÕIDAB,
            # ja varem kadus selline rida siit lihtsalt ära -- vaikselt,
            # ilma märgita. Nii kadus üks Tesla Model 3 rida, mille ma
            # kogemata teist korda lisasin, ja ma ei saanud sellest teada
            # enne, kui liidesest vale nime nägin.
            #
            # Praegu on kõik 37 varjatud rida baasiga IDENTSED, seega
            # andmeviga ei ole. Aga kui keegi neist mõnda siin failis
            # muudab, siis muudatus EI JÕUA kuhugi. audit.py kontrollib
            # seda invarianti ja kukub läbi, kui varjatud rida hakkab
            # baasist erinema -- siis tuleb muuta baasi, mitte seda rida.
            EE_SHADOWED.append((key, name))
            continue
        added[key] = Vehicle(
            name=name, kerb_mass_kg=mass, abs_class=abs_cls,
            cda_m2=round(cd * FRONTAL_AREA_K * width * height, 3),
            # raskuskeskme kõrgus ei osale pidurdusmaa arvutuses (see on
            # koormuse ülekande jaoks, mida mudel ei kasuta) -- hoiame
            # lihtsa lähendi 0,38 x kere kõrgus
            cog_height_m=round(0.38 * height, 2),
            wheelbase_m=wb, recommended_pressure_bar=press,
            oem_size=size, brake_capacity_g=brake)
    return added


VEHICLES.update(_load_ee_vehicles())

# TEHASEMÕÕDUD veebist (oem_sizes.py). Baasmõõt kirjutab siinse üle, sest
# see on allikaga kontrollitud; ülejäänud tehasemõõdud lähevad lehele
# valikusse. Vt oem_sizes.py päist: mis on "kinnitatud" ja mis "osaline".
def _apply_oem_sizes():
    from .oem_sizes import OEM_SIZES
    for _k, _row in OEM_SIZES.items():
        _v = VEHICLES.get(_k)
        if _v is not None and _row[0]:
            _v.oem_size = _row[0]


_apply_oem_sizes()

# Iga auto kohta märkus: mis väli on hinnang, mitte tootja andmed.
VEHICLE_NOTES = {
    row[0]: row[11] for row in __import__(
        "pidurdus.vehicles_ee", fromlist=["EE_VEHICLES"]).EE_VEHICLES
    if len(row) > 11 and row[11]
}

# ---------------------------------------------------------------------------
# Mark ja keretüüp -- ainult valiku jaoks, füüsikas neid ei kasutata
# ---------------------------------------------------------------------------
# Keretüüp on TEADLIKULT jäme, ainult neli rühma. Peenem jaotus (sedaan /
# luukpära / universaal) nõuaks kerekuju andmeid, mida mul kõigi 116 auto
# kohta ei ole, ja ma ei taha seda välja mõelda. Neli rühma on piisav,
# et nimekiri ei paistaks kolme reana.

_MAKE_BY_PREFIX = {
    "citroen_": "Citroën", "seat_": "SEAT", "lexus_": "Lexus",
    "chrysler_": "Chrysler",
    "jeep_": "Jeep", "lr_": "Land Rover", "porsche_": "Porsche",
    "mini_": "MINI", "fiat_": "Fiat", "saab_": "Saab",
    "alfa_": "Alfa Romeo", "chevrolet_": "Chevrolet",
    "ssangyong_": "SsangYong", "jaguar_": "Jaguar",
    "polestar_": "Polestar", "mg4_": "MG", "mg_": "MG",
    "cupra_": "Cupra", "isuzu_": "Isuzu", "yld_": "Ei leia oma autot",
    "vw": "Volkswagen", "passat": "Volkswagen", "audi": "Audi",
    "skoda": "Škoda", "toyota": "Toyota", "bmw": "BMW",
    "mb": "Mercedes-Benz", "nissan": "Nissan", "volvo": "Volvo",
    "kia": "Kia", "honda": "Honda", "mitsubishi": "Mitsubishi",
    "mitsu": "Mitsubishi", "subaru": "Subaru", "opel": "Opel",
    "ford": "Ford", "mazda": "Mazda", "peugeot": "Peugeot",
    "renault": "Renault", "hyundai": "Hyundai", "tesla": "Tesla",
    "lada": "Lada / VAZ", "dacia": "Dacia", "suzuki": "Suzuki", "byd": "BYD",
}

_BODY_SMALL = {
    "skoda_fabia_2", "skoda_fabia_3", "vw_polo_5", "renault_clio_4",
    "peugeot_206", "toyota_yaris_3", "toyota_yaris_4", "mitsu_imiev",
    "lada_2110",
    # 2026-09-17
    "fiat_500_312", "citroen_c3_2", "seat_ibiza_4", "opel_corsa_d",
    "mini_r56", "dacia_sandero_2",
    # 2026-09-18
    "ford_fiesta_6", "toyota_corolla_e110",
    # 2026-09-18 teine ring
    "kia_rio_3", "mitsu_colt_6", "suzuki_swift_3", "skoda_rapid",
    "toyota_aygo_1", "nissan_note_e11", "honda_jazz_2",
    # 2026-09-22 kolmas ring
    "yld_vaike", "vw_up", "vw_polo_4", "vw_polo_6", "skoda_citigo", "skoda_fabia_1",
    "skoda_fabia_4", "audi_a1_8x", "toyota_yaris_xp90", "ford_fiesta_7",
    "opel_corsa_e", "opel_corsa_f", "peugeot_207", "peugeot_208_1",
    "peugeot_208_2", "citroen_c3_3", "renault_clio_3", "renault_clio_5",
    "renault_zoe", "dacia_logan_2", "dacia_sandero_3", "nissan_micra_k12",
    "hyundai_i10_2", "hyundai_i20_2", "kia_picanto_2", "kia_rio_4", "mazda_2_dj",
    "mitsu_spacestar", "suzuki_swift_4", "suzuki_ignis_3", "seat_ibiza_5",
    "fiat_panda_3", "fiat_punto_3", "mini_f56", "chevrolet_aveo_t300",
    "chevrolet_spark_m300", "lada_granta", "bmw_i3",
}

_BODY_SUV = {
    "toyota_rav4_4", "toyota_rav4_5", "vw_tiguan_1", "vw_tiguan_2",
    "nissan_qashqai_j11", "volvo_xc60_1", "volvo_xc60", "kia_sportage_3",
    "honda_crv_3", "mitsubishi_outlander_3", "subaru_forester_sj",
    "bmw_x5_e53", "bmw_x5_e70", "bmw_x3_e83", "bmw_x3_f25", "volvo_xc90_1",
    "skoda_kodiaq_1", "skoda_kamiq", "vw_troc", "renault_captur_2",
    "dacia_duster_2", "mazda_cx5_ke", "toyota_yariscross", "toyota_chr_1",
    "toyota_lc120", "toyota_bz4x", "nissan_qashqai_j10", "honda_crv_4",
    "mitsu_pajero_4", "hyundai_tucson_tl", "hyundai_tucson_nx4",
    "suzuki_gv", "tesla_modely", "hyundai_ioniq5", "byd_sealion7",
    "lada_niva", "subaru_outback_br", "subaru_outback_bs",
    # 2026-09-17 lisatud maasturid
    "audi_q5_fy", "seat_ateca", "peugeot_3008_1", "peugeot_5008_2",
    "lexus_rx_al10", "lexus_nx_az10", "jeep_gc_wk2", "jeep_compass_mp",
    "jeep_wrangler_jk", "lr_rrs_l320", "lr_disco_sport", "lr_freelander_2",
    "porsche_cayenne_958", "porsche_macan_95b", "mini_countryman_r60",
    "chevrolet_captiva", "ssangyong_rexton",
    # 2026-09-18
    "skoda_yeti", "hyundai_santafe_cm",
    # 2026-09-18 teine ring
    "nissan_xtrail_t31", "ford_kuga_2", "hyundai_ix35", "kia_sorento_2",
    "mitsu_asx", "suzuki_sx4_1", "opel_antara", "bmw_x1_e84",
    "audi_q7_4l", "mb_ml_w164", "vw_touareg_1", "volvo_xc70_3",
    # 2026-09-22 kolmas ring
    "yld_maastur", "vw_tcross", "vw_tiguan_3", "vw_touareg_2", "vw_id4", "skoda_karoq",
    "skoda_enyaq", "audi_q3_8u", "audi_q3_f3", "audi_q5_8r", "audi_q7_4m",
    "audi_etron", "bmw_x1_f48", "bmw_x3_g01", "bmw_x5_f15", "bmw_x5_g05",
    "mb_gla_x156", "mb_glc_x253", "mb_ml_w166", "mb_gle_w167", "toyota_chr_2",
    "toyota_rav4_3", "toyota_lc150", "toyota_hilux_7", "toyota_hilux_8",
    "lexus_rx_al20", "lexus_ux", "ford_kuga_1", "ford_kuga_3", "ford_puma_2",
    "ford_ranger_3", "opel_mokka_a", "opel_grandland", "peugeot_2008_1",
    "peugeot_2008_2", "peugeot_3008_2", "citroen_c5_aircross", "renault_kadjar",
    "dacia_duster_1", "nissan_juke_f15", "nissan_qashqai_j12", "nissan_xtrail_t32",
    "nissan_navara_d40", "nissan_pathfinder_r51", "hyundai_kona_1", "hyundai_kona_ev",
    "hyundai_tucson_jm", "hyundai_santafe_tm", "kia_sportage_4", "kia_sportage_5",
    "kia_sorento_3", "kia_niro_1", "kia_ev6", "mazda_cx3", "mazda_cx30",
    "mazda_cx5_kf", "mazda_cx60", "honda_crv_5", "honda_hrv_2", "mitsu_outlander_2",
    "mitsu_l200_5", "subaru_forester_sh", "subaru_xv_1", "subaru_outback_bp",
    "suzuki_vitara_4", "suzuki_sx4_scross", "suzuki_jimny_4", "volvo_xc40",
    "volvo_xc90_2", "seat_arona", "seat_tarraco", "cupra_formentor",
    "jeep_renegade", "jeep_cherokee_kl", "lr_disco_4", "lr_evoque_1",
    "ssangyong_korando_3", "isuzu_dmax_2", "mg_zs_ev", "byd_atto3",
}
_BODY_VAN = {
    "vw_transporter", "vw_caddy_3", "vw_t5", "ford_transit_custom",
    "mb_sprinter_906", "renault_master_3", "vw_touran_1", "opel_zafira_b",
    # 2026-09-17 lisatud kaubikud ja mahtuniversaalid
    "citroen_jumpy_2", "peugeot_partner_2", "fiat_ducato_3", "fiat_doblo_2",
    "citroen_berlingo_2", "seat_alhambra_2",
    # 2026-09-18 pere-mahtukad
    "vw_sharan_1", "opel_zafira_a", "ford_galaxy_2", "toyota_verso",
    "renault_scenic_2", "mb_b180_w245",
    # 2026-09-18 teine ring
    "mb_vito_w639", "chrysler_voyager_4", "renault_kangoo_2",
    "renault_trafic_2", "vw_caddy_4", "ford_connect_1", "opel_vivaro_a",
    "peugeot_boxer_3", "ford_cmax_1", "mazda_5_cr", "opel_meriva_b",
    "skoda_roomster",
    # 2026-09-22 kolmas ring
    "yld_kaubik", "vw_golf_plus", "vw_touran_2", "vw_sharan_2", "vw_caddy_5", "vw_t4",
    "vw_crafter_2", "bmw_218d_f45", "mb_b180_w246", "mb_vito_w447",
    "mb_sprinter_907", "toyota_proace", "ford_smax_1", "ford_transit_7",
    "opel_zafira_c", "opel_combo_d", "peugeot_rifter", "citroen_c4_picasso_2",
    "citroen_berlingo_3", "renault_scenic_3", "dacia_jogger", "hyundai_ix20",
    "kia_venga",
}


def vehicle_make(key: str) -> str:
    for pre in sorted(_MAKE_BY_PREFIX, key=len, reverse=True):
        if key.startswith(pre):
            return _MAKE_BY_PREFIX[pre]
    return "Muu"


def vehicle_body(key: str) -> str:
    if key in _BODY_VAN:
        return "KAUBIK"
    if key in _BODY_SUV:
        return "MAASTUR"
    if key in _BODY_SMALL:
        return "VAIKEAUTO"
    return "SOIDUAUTO"


ALL_VEHICLES = {**VEHICLES, **ANCHOR_VEHICLES}


# ---------------------------------------------------------------------------
# Rehvid
# ---------------------------------------------------------------------------

# Väärtused allpool on TULETATUD päris testitulemustest (anchors*.py):
# mudel lahendab iga rehvi ja iga pinna jaoks mu, mis annab TÄPSELT
# mõõdetud pidurdusmaa. G tuleb märja asfaldi katsest.
# Vana kommentaar:
# (calibrate.solve_per_tyre): mudel lahendab iga rehvi jaoks mu, mis annab
# täpselt mõõdetud pidurdusmaa. Kus testi pole, on kasutatud märgise
# klassi keskpunkti (G_CLASS) ja kategooria baasi.
#   G      = märghaardumise indeks (testist tuletatud või klassi keskpunkt)
#   dry    = kuivhaardumine, asfalt 20 °C, 80 km/h
#   ice    = jääl -5 °C
# Lume kohta ankruandmeid EI OLE -> kasutatakse kategooria baasi.

TYRES = {
    # --- suverehvid, sport (UHP) — ADAC 2025, 225/40 R18 -----
    "conti_sc7": Tyre("Continental SportContact 7", C.SUMMER_UHP,
        1.795, mu_dry_override=1.367, size="225/40 R18", g_source="test"),
    "bridgestone_potsport": Tyre("Bridgestone Potenza Sport", C.SUMMER_UHP,
        1.768, mu_dry_override=1.380, size="225/40 R18", g_source="test"),
    "michelin_ps5": Tyre("Michelin Pilot Sport 5", C.SUMMER_UHP,
        1.742, mu_dry_override=1.355, size="225/40 R18", g_source="test"),
    "goodyear_f1a6": Tyre("Goodyear Eagle F1 Asymmetric 6", C.SUMMER_UHP,
        1.722, mu_dry_override=1.355, size="225/40 R18", g_source="test"),
    "kumho_ps71": Tyre("Kumho Ecsta PS71", C.SUMMER_UHP,
        1.679, mu_dry_override=1.384, size="225/40 R18", g_source="test"),
    "falken_fk520": Tyre("Falken Azenis FK520", C.SUMMER_UHP,
        1.661, mu_dry_override=1.342, size="225/40 R18", g_source="test"),
    "firestone_fhsport": Tyre("Firestone Firehawk Sport", C.SUMMER_UHP,
        1.638, mu_dry_override=1.338, size="225/40 R18", g_source="test"),
    "norauto_prevensys4": Tyre("Norauto Prevensys 4", C.SUMMER_UHP,
        1.638, mu_dry_override=1.244, size="225/40 R18", g_source="test"),
    "nexen_nfera_su2": Tyre("Nexen N'Fera Sport SU2", C.SUMMER_UHP,
        1.632, mu_dry_override=1.314, size="225/40 R18", g_source="test"),
    "toyo_proxes_sport2": Tyre("Toyo Proxes Sport 2", C.SUMMER_UHP,
        1.632, mu_dry_override=1.359, size="225/40 R18", g_source="test"),
    "vredestein_ultracpro": Tyre("Vredestein Ultrac Pro", C.SUMMER_UHP,
        1.632, mu_dry_override=1.310, size="225/40 R18", g_source="test"),
    "yokohama_v107": Tyre("Yokohama Advan Sport V107", C.SUMMER_UHP,
        1.620, mu_dry_override=1.384, size="225/40 R18", g_source="test"),
    "dunlop_sportmaxx_rt2": Tyre("Dunlop SportMaxx RT 2", C.SUMMER_UHP,
        1.604, mu_dry_override=1.284, size="225/40 R18", g_source="test"),
    "nokian_powerproof1": Tyre("Nokian Powerproof 1", C.SUMMER_UHP,
        1.604, mu_dry_override=1.265, size="225/40 R18", g_source="test"),
    "syron_premiumperf": Tyre("Syron Premium Performance", C.SUMMER_UHP,
        1.561, mu_dry_override=1.276, size="225/40 R18", g_source="test"),
    "ceat_sportdrive": Tyre("Ceat SportDrive", C.SUMMER_UHP,
        1.510, mu_dry_override=1.287, size="225/40 R18", g_source="test"),
    "giti_sports2": Tyre("Giti GitiSportS2", C.SUMMER_UHP,
        1.448, mu_dry_override=1.209, size="225/40 R18", g_source="test"),
    "doublecoin_dc100": Tyre("Double Coin DC 100", C.SUMMER_UHP,
        1.088, mu_dry_override=1.206, size="225/40 R18", g_source="test"),
    # --- suverehvid, touring — UTAC/Aftonbladet 2025 + naidised 
    "michelin_primacy5": Tyre("Michelin Primacy 5", C.SUMMER_TOURING,
        1.491, mu_dry_override=1.178, size="225/45 R17", g_source="test"),
    "pirelli_p7c2": Tyre("Pirelli Cinturato P7 C2", C.SUMMER_TOURING,
        1.486, mu_dry_override=1.246, size="225/45 R17", g_source="test"),
    "nokian_hakkablue3": Tyre("Nokian Hakka Blue 3", C.SUMMER_TOURING,
        1.481, mu_dry_override=1.231, size="225/45 R17", g_source="test"),
    "vredestein_ultrac": Tyre("Vredestein Ultrac", C.SUMMER_TOURING,
        1.337, mu_dry_override=1.147, size="225/45 R17", g_source="test"),
    "conti_pc7": Tyre("Continental PremiumContact 7", C.SUMMER_TOURING,
        1.470, mu_dry_override=1.246, size="225/45 R17", g_source="test"),
    "hankook_prime4": Tyre("Hankook Ventus Prime 4", C.SUMMER_TOURING,
        1.470, mu_dry_override=1.212, size="225/45 R17", g_source="test"),
    "falken_ze320": Tyre("Falken Ziex ZE320", C.SUMMER_TOURING,
        1.470, mu_dry_override=1.208, size="225/45 R17", g_source="test"),
    "bridgestone_t6": Tyre("Bridgestone Turanza 6", C.SUMMER_TOURING,
        1.470, mu_dry_override=1.189, size="225/45 R17", g_source="test"),
    "nordman_south": Tyre("Nordman South", C.SUMMER_TOURING,
        1.470, mu_dry_override=1.131, size="225/45 R17", g_source="test"),
    "budget_c": Tyre("Odavklassi suverehv (märgis C)", C.SUMMER_TOURING,
        1.320, mu_dry_override=1.080),
    "budget_e": Tyre("Odavklassi suverehv (märgis E)", C.SUMMER_TOURING,
        1.050, mu_dry_override=0.980),
    # --- lamellrehvid — ADAC 2025, 225/45 R17 ----------------
    "conti_asc2": Tyre("Continental AllSeasonContact 2", C.ALL_SEASON,
        1.496, mu_dry_override=1.068, mu_snow_override=0.398, mu_ice_override=0.097, size="225/45 R17", g_source="test"),
    "bridgestone_as6": Tyre("Bridgestone Turanza All Season 6", C.ALL_SEASON,
        1.480, mu_dry_override=1.138, mu_snow_override=0.380, mu_ice_override=0.097, size="225/45 R17", g_source="test"),
    "pirelli_as_sf3": Tyre("Pirelli Cinturato All Season SF3", C.ALL_SEASON,
        1.436, mu_dry_override=1.154, mu_snow_override=0.371, mu_ice_override=0.098, size="225/45 R17", g_source="test"),
    "goodyear_v4s3": Tyre("Goodyear Vector 4Seasons Gen-3", C.ALL_SEASON,
        1.403, mu_dry_override=1.014, mu_snow_override=0.403, mu_ice_override=0.103, size="225/45 R17", g_source="test"),
    "vredestein_quatracpp": Tyre("Vredestein Quatrac Pro+", C.ALL_SEASON,
        1.394, mu_dry_override=1.007, mu_snow_override=0.380, mu_ice_override=0.091, size="225/45 R17", g_source="test"),
    "michelin_cc2": Tyre("Michelin CrossClimate 2", C.ALL_SEASON,
        1.385, mu_dry_override=1.125, mu_snow_override=0.408, mu_ice_override=0.103, size="225/45 R17", g_source="test"),
    "nexen_4season2": Tyre("Nexen N'Blue 4Season 2", C.ALL_SEASON,
        1.385, mu_dry_override=1.074, mu_snow_override=0.408, mu_ice_override=0.108, size="225/45 R17", g_source="test"),
    "dunlop_as2": Tyre("Dunlop All Season 2", C.ALL_SEASON,
        1.380, mu_dry_override=1.004, mu_snow_override=0.398, mu_ice_override=0.103, size="225/45 R17", g_source="test"),
    "viking_fourtech": Tyre("Viking FourTech Plus", C.ALL_SEASON,
        1.363, mu_dry_override=0.987, mu_snow_override=0.384, mu_ice_override=0.096, size="225/45 R17", g_source="test"),
    "bfg_advantage_as": Tyre("BFGoodrich Advantage All Season", C.ALL_SEASON,
        1.354, mu_dry_override=1.113, mu_snow_override=0.393, mu_ice_override=0.099, size="225/45 R17", g_source="test"),
    "barum_quartaris5": Tyre("Barum Quartaris 5", C.ALL_SEASON,
        1.301, mu_dry_override=0.954, mu_snow_override=0.408, mu_ice_override=0.097, size="225/45 R17", g_source="test"),
    "petlas_multiaction": Tyre("Petlas Multi Action PT 565", C.ALL_SEASON,
        1.274, mu_dry_override=0.987, mu_snow_override=0.283, mu_ice_override=0.081, size="225/45 R17", g_source="test"),
    "cst_allseason_acp1": Tyre("CST Medallion All Season ACP1", C.ALL_SEASON,
        1.262, mu_dry_override=0.968, mu_snow_override=0.380, mu_ice_override=0.078, size="225/45 R17", g_source="test"),
    "superia_ecoblue4s": Tyre("Superia Ecoblue2 4S", C.ALL_SEASON,
        1.226, mu_dry_override=1.038, mu_snow_override=0.398, mu_ice_override=0.100, size="225/45 R17", g_source="test"),
    "aplus_as909": Tyre("Aplus AS909", C.ALL_SEASON,
        1.175, mu_dry_override=1.030, mu_snow_override=0.389, mu_ice_override=0.103, size="225/45 R17", g_source="test"),
    "arivo_carlorful": Tyre("Arivo Carlorful AS", C.ALL_SEASON,
        1.072, mu_dry_override=1.030, mu_snow_override=0.380, mu_ice_override=0.098, size="225/45 R17", g_source="test"),
    "michelin_cc3": Tyre("Michelin CrossClimate 3", C.ALL_SEASON,
        1.600, mu_dry_override=1.120),
    # --- talverehvid, Kesk-Euroopa — ADAC 2025, 225/40 R18 ---
    "goodyear_ugp3": Tyre("Goodyear UltraGrip Performance 3", C.WINTER_CENTRAL,
        1.411, mu_dry_override=0.979, mu_snow_override=0.375, mu_ice_override=0.089, size="225/40 R18", g_source="test"),
    "michelin_alpin5": Tyre("Michelin Pilot Alpin 5", C.WINTER_CENTRAL,
        1.387, mu_dry_override=1.003, mu_snow_override=0.389, mu_ice_override=0.092, size="225/40 R18", g_source="test"),
    "bridgestone_blizzak6": Tyre("Bridgestone Blizzak 6", C.WINTER_CENTRAL,
        1.382, mu_dry_override=0.943, mu_snow_override=0.380, mu_ice_override=0.092, size="225/40 R18", g_source="test"),
    "momo_northpole": Tyre("Momo North Pole W 20 EUROPA", C.WINTER_CENTRAL,
        1.364, mu_dry_override=0.960, mu_snow_override=0.371, mu_ice_override=0.089, size="225/40 R18", g_source="test"),
    "landsail_winter": Tyre("Landsail Winter Lander", C.WINTER_CENTRAL,
        1.360, mu_dry_override=0.974, mu_snow_override=0.291, mu_ice_override=0.089, size="225/40 R18", g_source="test"),
    "hankook_iceptevo3": Tyre("Hankook Winter i*cept evo3", C.WINTER_CENTRAL,
        1.355, mu_dry_override=0.946, mu_snow_override=0.375, mu_ice_override=0.085, size="225/40 R18", g_source="test"),
    "uniroyal_winterexpert": Tyre("Uniroyal WinterExpert", C.WINTER_CENTRAL,
        1.355, mu_dry_override=0.941, mu_snow_override=0.375, mu_ice_override=0.085, size="225/40 R18", g_source="test"),
    "conti_ts870p": Tyre("Continental WinterContact TS 870 P", C.WINTER_CENTRAL,
        1.351, mu_dry_override=0.972, mu_snow_override=0.371, mu_ice_override=0.081, size="225/40 R18", g_source="test"),
    "firestone_winterhawk4": Tyre("Firestone Winterhawk 4", C.WINTER_CENTRAL,
        1.351, mu_dry_override=0.912, mu_snow_override=0.375, mu_ice_override=0.093, size="225/40 R18", g_source="test"),
    "semperit_speedgrip5": Tyre("Semperit Speed Grip 5", C.WINTER_CENTRAL,
        1.337, mu_dry_override=0.932, mu_snow_override=0.380, mu_ice_override=0.087, size="225/40 R18", g_source="test"),
    "nokian_snowproofp": Tyre("Nokian Snowproof P", C.WINTER_CENTRAL,
        1.333, mu_dry_override=0.982, mu_snow_override=0.363, mu_ice_override=0.094, size="225/40 R18", g_source="test"),
    "apollo_aspire_xp": Tyre("Apollo Aspire XP Winter", C.WINTER_CENTRAL,
        1.299, mu_dry_override=0.943, mu_snow_override=0.371, mu_ice_override=0.090, size="225/40 R18", g_source="test"),
    "dunlop_ws5": Tyre("Dunlop Winter Sport 5", C.WINTER_CENTRAL,
        1.291, mu_dry_override=0.939, mu_snow_override=0.384, mu_ice_override=0.089, size="225/40 R18", g_source="test"),
    "ceat_winterdrive": Tyre("Ceat WinterDrive", C.WINTER_CENTRAL,
        1.287, mu_dry_override=0.987, mu_snow_override=0.375, mu_ice_override=0.097, size="225/40 R18", g_source="test"),
    "giti_winterw2": Tyre("Giti GitiWinterW2", C.WINTER_CENTRAL,
        1.279, mu_dry_override=0.912, mu_snow_override=0.363, mu_ice_override=0.083, size="225/40 R18", g_source="test"),
    "matador_mp93": Tyre("Matador MP93 Nordicca", C.WINTER_CENTRAL,
        1.271, mu_dry_override=0.914, mu_snow_override=0.375, mu_ice_override=0.089, size="225/40 R18", g_source="test"),
    "kleber_krisalp_hp3": Tyre("Kleber Krisalp HP3", C.WINTER_CENTRAL,
        1.267, mu_dry_override=0.934, mu_snow_override=0.389, mu_ice_override=0.089, size="225/40 R18", g_source="test"),
    "points_winters": Tyre("Point S Winter S", C.WINTER_CENTRAL,
        1.267, mu_dry_override=0.927, mu_snow_override=0.375, mu_ice_override=0.089, size="225/40 R18", g_source="test"),
    "cst_medallion_wcp1": Tyre("CST Medallion Winter WCP1", C.WINTER_CENTRAL,
        1.256, mu_dry_override=0.955, mu_snow_override=0.330, mu_ice_override=0.075, size="225/40 R18", g_source="test"),
    "petlas_snowmaster2": Tyre("Petlas SnowMaster 2 Sport", C.WINTER_CENTRAL,
        1.248, mu_dry_override=0.941, mu_snow_override=0.347, mu_ice_override=0.088, size="225/40 R18", g_source="test"),
    "nankang_activa_sv4": Tyre("Nankang Winter Activa SV 4", C.WINTER_CENTRAL,
        1.244, mu_dry_override=0.921, mu_snow_override=0.351, mu_ice_override=0.076, size="225/40 R18", g_source="test"),
    "fulda_kristall_hp2": Tyre("Fulda Kristall Control HP2", C.WINTER_CENTRAL,
        1.233, mu_dry_override=0.910, mu_snow_override=0.375, mu_ice_override=0.087, size="225/40 R18", g_source="test"),
    "gtradial_winterpro2": Tyre("GT Radial WinterPro2 Sport", C.WINTER_CENTRAL,
        1.218, mu_dry_override=0.916, mu_snow_override=0.375, mu_ice_override=0.087, size="225/40 R18", g_source="test"),
    "maxxis_wp6": Tyre("Maxxis Premitra Snow WP6", C.WINTER_CENTRAL,
        1.215, mu_dry_override=0.912, mu_snow_override=0.375, mu_ice_override=0.085, size="225/40 R18", g_source="test"),
    "radar_dimax_winter": Tyre("Radar Dimax Winter", C.WINTER_CENTRAL,
        1.204, mu_dry_override=0.936, mu_snow_override=0.384, mu_ice_override=0.095, size="225/40 R18", g_source="test"),
    "imperial_snowdragon": Tyre("Imperial Snowdragon UHP", C.WINTER_CENTRAL,
        1.166, mu_dry_override=0.925, mu_snow_override=0.351, mu_ice_override=0.085, size="225/40 R18", g_source="test"),
    "goodride_sw608": Tyre("Goodride SW608", C.WINTER_CENTRAL,
        1.143, mu_dry_override=0.916, mu_snow_override=0.344, mu_ice_override=0.081, size="225/40 R18", g_source="test"),
    "starperf_stratos": Tyre("Star Performer Stratos UHP", C.WINTER_CENTRAL,
        1.100, mu_dry_override=0.929, mu_snow_override=0.367, mu_ice_override=0.085, size="225/40 R18", g_source="test"),
    "tomket_snowroad3": Tyre("Tomket Snowroad Pro 3", C.WINTER_CENTRAL,
        1.085, mu_dry_override=0.921, mu_snow_override=0.363, mu_ice_override=0.095, size="225/40 R18", g_source="test"),
    "evergreen_ew66": Tyre("Evergreen Winter EW66", C.WINTER_CENTRAL,
        1.033, mu_dry_override=0.890, mu_snow_override=0.375, mu_ice_override=0.068, size="225/40 R18", g_source="test"),
    "syron_everest2": Tyre("Syron Everest 2", C.WINTER_CENTRAL,
        0.920, mu_dry_override=0.895, mu_snow_override=0.398, mu_ice_override=0.100, size="225/40 R18", g_source="test"),
    # --- talverehvid, Pohjamaade naelutu — Tekniikan Maailma 2025 
    "falken_wpfs1": Tyre("Falken Winterpeak F-Snow 1", C.WINTER_NORDIC,
        1.232, mu_dry_override=0.860, mu_ice_override=0.203, size="205/55 R16", g_source="test"),
    "hankook_iz3": Tyre("Hankook Winter i*cept iZ3", C.WINTER_NORDIC,
        1.232, mu_dry_override=0.845, mu_ice_override=0.180, size="205/55 R16", g_source="test"),
    "goodyear_ugice3": Tyre("Goodyear UltraGrip Ice 3", C.WINTER_NORDIC,
        1.225, mu_dry_override=0.840, mu_ice_override=0.193, size="205/55 R16", g_source="test"),
    "nokian_r5": Tyre("Nokian Hakkapeliitta R5", C.WINTER_NORDIC,
        1.218, mu_dry_override=0.860, mu_ice_override=0.203, size="205/55 R16", g_source="test"),
    "radar_dimax_ice": Tyre("Radar Dimax Ice (odavklass)", C.WINTER_NORDIC,
        1.109, mu_dry_override=0.769, mu_ice_override=0.180, size="205/55 R16", g_source="test"),
    "conti_vc8": Tyre("Continental VikingContact 8", C.WINTER_NORDIC,
        1.165, mu_dry_override=0.842, mu_ice_override=0.206, size="205/55 R16", g_source="test"),
    "michelin_xicesnow": Tyre("Michelin X-Ice Snow", C.WINTER_NORDIC,
        1.116, mu_dry_override=0.820, mu_ice_override=0.214, size="205/55 R16", g_source="test"),
    # --- naastrehvid — Tekniikan Maailma 2025 ----------------
    "pirelli_iz2": Tyre("Pirelli Ice Zero 2", C.WINTER_STUDDED,
        1.357, mu_dry_override=0.837, mu_ice_override=0.236, studded=True, size="205/55 R16", g_source="test"),
    "conti_ic3": Tyre("Continental IceContact 3", C.WINTER_STUDDED,
        1.308, mu_dry_override=0.840, mu_ice_override=0.231, studded=True, size="205/55 R16", g_source="test"),
    "goodyear_ugarctic2": Tyre("Goodyear UltraGrip Arctic 2", C.WINTER_STUDDED,
        1.288, mu_dry_override=0.828, mu_ice_override=0.269, studded=True, size="205/55 R16", g_source="test"),
    "bridgestone_spike3": Tyre("Bridgestone Blizzak Spike 3", C.WINTER_STUDDED,
        1.276, mu_dry_override=0.788, mu_ice_override=0.311, studded=True, size="205/55 R16", g_source="test"),
    "nokian_hkpl10": Tyre("Nokian Hakkapeliitta 10", C.WINTER_STUDDED,
        1.239, mu_dry_override=0.814, mu_ice_override=0.295, studded=True, size="205/55 R16", g_source="test"),
    "michelin_xin4": Tyre("Michelin X-Ice North 4", C.WINTER_STUDDED,
        1.222, mu_dry_override=0.822, mu_ice_override=0.263, studded=True, size="205/55 R16", g_source="test"),
    "kumho_wi32": Tyre("Kumho WinterCraft ice Wi32", C.WINTER_STUDDED,
        1.125, mu_dry_override=0.820, mu_ice_override=0.303, studded=True, size="205/55 R16", g_source="test"),
}


def tyre(key: str, **overrides) -> Tyre:
    """Võta valmisrehv ja muuda vajalikke välju (rõhk, mustrisügavus, vanus)."""
    from dataclasses import replace
    return replace(TYRES[key], **overrides)


def vehicle(key: str, **overrides) -> Vehicle:
    from dataclasses import replace
    return replace(VEHICLES[key], **overrides)
