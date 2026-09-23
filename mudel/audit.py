"""AUDIT: kas iga konstant tuleb millestki päris?

Kommentaar koodis ei ole tõendus -- kommentaari saab kirjutada ka
konstandi kohta, mille keegi lihtsalt välja mõtles. Seepärast ei usu
see fail ühtegi sõna, vaid mõõdab kolme asja:

  1. KATE. Kas iga Calibration-i väli on paritolu.py-s kirjas?
     Kui ei -> LÄBI KUKKUNUD. Nii ei saa uus konstant vaikselt sisse.

  2. TUNDLIKKUS. Iga konstanti nihutatakse +-10 % ja mõõdetakse KAKS
     asja:
        a) kui palju muutub 369 ankru keskmine viga  -> kas ANDMED
           teda üldse kitsendavad
        b) kui palju muutub tüüpiline kasutaja vastus -> kas ta
           üldse LOEB
     Ohtlik ruut on (b) suur ja (a) null: konstant liigutab vastust,
     aga ükski mõõtmine ei ütle, kas ta on õige. Need tuleb välja
     öelda, mitte ära peita.

  3. SIGMA AUSUS. sigma_base EI OLE vaba parameeter. Ta peab olema
     vähemalt sama suur kui selle pinna ankrute tegelik jääkhajuvus.
     Kui mudel lubab rohkem täpsust, kui ta suudab, kukub audit läbi.

Kaivita kaustast /home/claude:  python3 -m pidurdus.audit
"""

from __future__ import annotations

import statistics
import sys
from dataclasses import fields, replace

from .anchors import ANCHORS
from .calibrate import errors
from .model import (BrakingModel, Calibration, Conditions, Surface, Texture,
                    Tyre, TyreCategory)
from .paritolu import ORIGINS
from .presets import VEHICLES

# STSENAARIUMID.
#
# Esimene versioon sellest failist kasutas kuut tüüpilist olukorda ja
# andis tulemuseks, et pool mudeli konstantidest ei liiguta vastust
# üldse. See oli AUDITI enda viga, mitte hea uudis: need kuus olukorda
# lihtsalt ei aktiveerinud neid liikmeid. Vanuse konstandid näitasid
# nulli, sest kõik kuus rehvi olid uued; rõhu omad, sest ükski ei olnud
# ala- ega ülerõhus; mustri omad, sest kõigil oli uus muster.
#
# Audit, mis annab valerahustuse, on halvem kui audit, mida ei ole.
# Seepärast on iga stsenaarium siin valitud nii, et ta AKTIVEERIKS
# kindla mudeliosa, ja allpool on kontroll, mis kukub läbi, kui mõni
# konstant ei ole ühegi stsenaariumiga kaetud.
def _t(cat, **kw):
    """Rehv ILMA rehvipõhiste ülekirjutusteta -- nii et mõõdetaks
    kategooriabaasi, mitte üksiku rehvi salvestatud arvu."""
    d = dict(wet_grip_index=1.32, tread_depth_mm=8.0, size="205/55 R16")
    d.update(kw)
    return Tyre("audit", cat, **d)


_SUM = TyreCategory.SUMMER_TOURING
_WIN = TyreCategory.WINTER_CENTRAL
_NOR = TyreCategory.WINTER_NORDIC
_STD = TyreCategory.WINTER_STUDDED

SCEN = [
    # --- põhipinnad, kategooriabaas (ei tohi olla rehvipõhist ülekirjutust)
    ("kuiv asfalt 90", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8)),
    ("märg asfalt 90", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("märg betoon 90", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.CONCRETE, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("tallatud lumi 50", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.SNOW_PACKED, speed_kmh=50, temp_c=-5)),
    ("lahtine lumi 40", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.SNOW_LOOSE, speed_kmh=40, temp_c=-5)),
    ("jää 50", _t(_NOR), "skoda_octavia",
     Conditions(surface=Surface.ICE, speed_kmh=50, temp_c=-5)),
    ("kruus 60", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.GRAVEL, speed_kmh=60, temp_c=12)),
    # --- liikmed, mida tavaolukord ei aktiveeri
    ("VANA rehv 8 a", _t(_SUM, age_years=9.0), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("KULUNUD muster 1,6", _t(_SUM, tread_depth_mm=1.6), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("KULUNUD kuival", _t(_SUM, tread_depth_mm=1.6), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8)),
    ("KULUNUD kruusal", _t(_SUM, tread_depth_mm=1.6), "skoda_octavia",
     Conditions(surface=Surface.GRAVEL, speed_kmh=60, temp_c=12)),
    ("KULUNUD kruusal ABS-ita", _t(_SUM, tread_depth_mm=1.6), "lada_niva",
     Conditions(surface=Surface.GRAVEL, speed_kmh=60, temp_c=12)),
    ("ALArõhk 1,8 bar", _t(_SUM, pressure_bar=1.8), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("ÜLErõhk 3,2 bar", _t(_SUM, pressure_bar=3.2), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8)),
    ("ALArõhk ABS-ita", _t(_SUM, pressure_bar=1.8), "lada_niva",
     Conditions(surface=Surface.ASPHALT, speed_kmh=60, temp_c=8, water_mm=1.0)),
    ("SÜGAV vesi 5 mm", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=5.0)),
    ("NIISKE 0,3 mm", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=0.3)),
    ("AKVAPLANEERING 120", _t(_SUM, tread_depth_mm=2.0), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=120, temp_c=8, water_mm=6.0)),
    ("KARE kate märjal", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0,
                texture=Texture.COARSE_NEW)),
    ("POLEERITUD kate märjal", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0,
                texture=Texture.POLISHED)),
    ("POLEERITUD kuival", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8,
                texture=Texture.POLISHED)),
    ("KÜLM +2 suverehviga", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=2, water_mm=1.0)),
    ("KUUM +30 talverehviga", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=30)),
    ("JÄÄ soe -1", _t(_NOR), "skoda_octavia",
     Conditions(surface=Surface.ICE, speed_kmh=50, temp_c=-1)),
    ("JÄÄ külm -25", _t(_NOR), "skoda_octavia",
     Conditions(surface=Surface.ICE, speed_kmh=50, temp_c=-25)),
    ("LUMI soe -1", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.SNOW_PACKED, speed_kmh=50, temp_c=-1)),
    ("ABS-ita asfalt", _t(_SUM), "lada_niva",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("RASKE koorem", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0,
                payload_kg=500)),
    ("AEGLANE 40", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=40, temp_c=8, water_mm=1.0)),
    ("KIIRE 130", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=130, temp_c=8, water_mm=1.0)),
    ("MÕÕT kaugel OEM-ist", _t(_SUM, size="255/35 R20"), "lada_niva",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("MÄRGISE G (test puudub)", _t(_SUM, g_source="label"), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    # --- stsenaariumid, mille audit ise nõudis juurde.
    # Esimene aus jooks kukkus läbi teatega, et 12 konstanti ei ole
    # ühegi stsenaariumiga kaetud. Need on need kaksteist.
    ("ÜLErõhk MÄRJAL", _t(_SUM, pressure_bar=3.2), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("Poolkulunud kruusal ABS-ita", _t(_SUM, tread_depth_mm=4.0), "lada_niva",
     Conditions(surface=Surface.GRAVEL, speed_kmh=60, temp_c=12)),
    ("VÄGA vana rehv 22 a", _t(_SUM, age_years=22.0), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("Põhjamaa rehv LUMEL", _t(_NOR), "skoda_octavia",
     Conditions(surface=Surface.SNOW_PACKED, speed_kmh=50, temp_c=-5)),
    ("ÜLE kiirusvahemiku (lumi 110)", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.SNOW_PACKED, speed_kmh=110, temp_c=-5)),
    ("ALLA kiirusvahemiku (asfalt 25)", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=25, temp_c=8, water_mm=1.0)),
    ("MÕÕT väga kaugel (R20 vs R13)", _t(_SUM, size="275/30 R20"), "lada_2110",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("LUMI väga külm -28", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.SNOW_PACKED, speed_kmh=50, temp_c=-28)),
    ("JÄÄ väga külm -34", _t(_NOR), "skoda_octavia",
     Conditions(surface=Surface.ICE, speed_kmh=50, temp_c=-34)),
    ("Rehv kandevõimega", _t(_SUM, load_capacity_kg=615), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0,
                payload_kg=400)),
    ("JÄÄ sula +2", _t(_NOR), "skoda_octavia",
     Conditions(surface=Surface.ICE, speed_kmh=40, temp_c=2.0)),
    # ice_temp_exp: naastrehvi temperatuuritundlikkus mõjub ainult
    # soojemal kui -5 °C -- ilma selle stsenaariumita ei näe audit teda.
    ("JÄÄ naastrehv -1", _t(_STD), "skoda_octavia",
     Conditions(surface=Surface.ICE, speed_kmh=50, temp_c=-1)),
    ("LUMI sula +2", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.SNOW_PACKED, speed_kmh=40, temp_c=2.0)),
    ("Asfalt 125 (vahemiku serv)", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=125, temp_c=8, water_mm=1.0)),
    ("Kruus 78 (vahemiku serv)", _t(_SUM), "skoda_octavia",
     Conditions(surface=Surface.GRAVEL, speed_kmh=78, temp_c=12)),
    ("MÕÕT 1 toll erinevust", _t(_SUM, size="205/55 R17"), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    ("MÕÕT täpselt 2 tolli", _t(_SUM, size="225/45 R18"), "skoda_octavia",
     Conditions(surface=Surface.ASPHALT, speed_kmh=90, temp_c=8, water_mm=1.0)),
    # Liuguri servad: kasutaja VÕIB need valida, nii absurdne kui see on.
    # Just nende jaoks klambrid olemas ongi.
    ("LUMI +45 (liuguri serv)", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.SNOW_PACKED, speed_kmh=40, temp_c=45.0)),
    ("JÄÄ +45 (liuguri serv)", _t(_NOR), "skoda_octavia",
     Conditions(surface=Surface.ICE, speed_kmh=40, temp_c=45.0)),
    ("LUMI 160 (liuguri serv)", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.SNOW_PACKED, speed_kmh=160, temp_c=-5)),
    # Liidese koige aarmuslikum kombinatsioon: lahtine lumi (lubatud
    # vahemik 15-60) kiirusel 160. Just siin rakendub ekstrapolatsiooni
    # sigma lagi -- ja audit noudis, et see oleks tegelikult katsetatud.
    ("LAHTINE LUMI 160 (aarmus)", _t(_WIN), "skoda_octavia",
     Conditions(surface=Surface.SNOW_LOOSE, speed_kmh=160, temp_c=-5)),
]


def _scale(v, f):
    """Nihuta arv, sõnastik või kõverapunktide loend teguriga f.

    NB: sõnastikes JÄETAKSE PUUTUMATA täpselt 1,0 väärtused. Need ei ole
    vabad parameetrid, vaid NORMEERIMISPUNKTID: texture NORMAL = 1,00,
    hp_category_factor WINTER_CENTRAL = 1,00, abs_eff_gravel NONE = 1,00,
    press_abs_scale ABS-iga klassid = 1,0. Nende nihutamine skaleeriks
    kogu mudelit ja annaks võltsilt kõrge tundlikkuse -- esimene
    versioon tegi täpselt seda ja näitas texture_wet tundlikkuseks
    10 %, mis oli tegelikult mu_ref nihe.
    """
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v * f
    if isinstance(v, tuple):
        return tuple(x * f if isinstance(x, (int, float)) else x for x in v)
    if isinstance(v, dict):
        return {k: (x if isinstance(x, float) and abs(x - 1.0) < 1e-9
                    else _scale(x, f)) for k, x in v.items()}
    if isinstance(v, list):
        return [(p[0], p[1] * f) if isinstance(p, tuple) and len(p) == 2
                else p for p in v]
    return v


def anchor_err(cal):
    """Ankruviga PINNA KAUPA, mitte ühe keskmisena.

    Esimene versioon võttis kõigi 369 ankru keskmise. See summutas
    pinnapõhised konstandid ära: kruusa konstant liigutab 18 kruusaankrut
    palju, aga 369 keskmises on see 18/369 ehk peaaegu nähtamatu, ja
    audit järeldas valesti, et kruusa konstante ei kitsenda miski.
    Nüüd tagastatakse iga pinna oma viga ja tundlikkuses võetakse
    MAKSIMUM üle pindade -- nii mõõdetakse konstanti tema enda
    ankrute vastu.

    Lisaks on siin ka akvaplaneerimise 85 mõõtmist. Nemad ei ole
    pidurdusankrud ega ole ANCHORS-is, seega hp_* konstandid nägid
    samuti välja "kitsendamata", kuigi nad on just nende vastu
    sobitatud.
    """
    out = {}
    by = {}
    for a, _, e in errors(BrakingModel(cal), ANCHORS):
        by.setdefault(a.surface.name, []).append(abs(e))
    for k, v in by.items():
        out[k] = statistics.mean(v)
    try:
        from .calibrate_aqua import _errs
        e = _errs(cal, True)
        allv = e["TV25"] + e["ADAC25"]
        out["AQUA"] = statistics.mean(abs(x) for x in allv)
    except Exception:
        pass
    return out


def _maxdiff(a, b):
    return max((abs(a[k] - b[k]) for k in a if k in b), default=0.0)


def outputs(cal):
    """Iga stsenaariumi kohta NII pidurdusmaa KUI veapiir.

    Veapiir on siin eraldi sellepärast, et kõik sigma_* konstandid
    liiguvad ainult teda, mitte pidurdusmaad. Esimene versioon mõõtis
    ainult pidurdusmaad ja näitas seetõttu KÕIGI veapiiri konstantide
    tundlikkuseks 0,00 % -- justkui neid poleks olemas.
    """
    m = BrakingModel(cal)
    out = []
    for _, ty, vk, c in SCEN:
        try:
            r = m.stopping_distance(ty, VEHICLES[vk], c)
            out.append((r.distance_m, r.sigma_rel, float(len(r.warnings))))
        except Exception:
            out.append((float("nan"), float("nan"), float("nan")))
    return out


def _reldiff(a, b):
    if not b or b != b or a != a:
        return 0.0
    return abs(a - b) / b


def sensitivity(name, base_err, base_out, pct=0.10):
    """(a) ankruviga, (b) pidurdusmaa, (c) veapiir -- kui palju liiguvad.

    Tagastab ka selle, MILLINE stsenaarium reageeris kõige rohkem, et
    kaetuse kontroll saaks öelda, kas konstant on üldse aktiveeritud.
    """
    da, dd, ds, who = 0.0, 0.0, 0.0, None
    for f in (1.0 + pct, 1.0 - pct):
        cal = Calibration()
        cur = getattr(cal, name)
        new = _scale(cur, f)
        if new == cur:
            continue
        setattr(cal, name, new)
        try:
            da = max(da, _maxdiff(anchor_err(cal), base_err))
            for (d1, s1, w1), (d0, s0, w0), sc in zip(outputs(cal), base_out, SCEN):
                r = _reldiff(d1, d0)
                if r > dd:
                    dd, who = r, sc[0]
                ds = max(ds, _reldiff(s1, s0))
                if w1 != w0:
                    ds = max(ds, 0.0001)   # hoiatuste arv muutus -> loeb
        except Exception:
            pass
    return da, dd, ds, who


def check_coverage():
    missing = [f.name for f in fields(Calibration) if f.name not in ORIGINS]
    extra = [k for k in ORIGINS if k not in {f.name for f in fields(Calibration)}]
    unsourced = [k for k, o in ORIGINS.items() if o.kind == "UNSOURCED"]
    return missing, extra, unsourced


def check_sigma():
    """sigma_base peab katma tegeliku jääkhajuvuse."""
    cal = Calibration()
    rows = errors(BrakingModel(cal), ANCHORS)
    by = {}
    for a, _, e in rows:
        by.setdefault(a.surface, []).append(e)
    out = []
    for surf, es in by.items():
        if len(es) < 2:
            continue
        resid = statistics.pstdev(es)
        declared = cal.sigma_base[surf]
        out.append((surf.name, len(es), resid, declared, declared >= resid))
    return out


def check_clamps():
    """CLAMP tohib olla ainult siis, kui ta tavavahemikus ei aktiveeru."""
    from .model import _clamp, _interp
    cal = Calibration()
    hits = []
    for t in range(-30, 3):
        raw = _interp(cal.ice_temp_curve, float(t))
        if raw < cal.ice_temp_min or raw > cal.ice_temp_max:
            hits.append(("ice_temp", t, raw))
    for t in range(-30, 3):
        raw = _interp(cal.snow_temp_curve, float(t))
        if raw < cal.snow_temp_min or raw > cal.snow_temp_max:
            hits.append(("snow_temp", t, raw))
    return hits


# Kasutajaliidese liugurite PÄRIS piirid (web/page.html rowRange)
UI_TEMP = (-25.0, 45.0)
UI_SPEED = (20.0, 160.0)


def check_inert():
    """Kas klamber saab liidese lubatud alas ULDSE rakenduda?

    Konstant, mis ei aktiveeru uheski stsenaariumis, on kahte sorti:
    kas audit on puudulik (siis tuleb stsenaarium lisada), voi konstant
    on TOESTATAVALT tegevusetu (siis on aus see valja oelda, mitte
    teeselda, et ta midagi teeb). See funktsioon eristab need.
    """
    from .model import _interp
    cal = Calibration()
    res = {}
    lo, hi = UI_TEMP
    ts = [lo + i * 0.5 for i in range(int((hi - lo) / 0.5) + 1)]
    for nm, curve, cmin, cmax in (
            ("ice_temp", cal.ice_temp_curve, cal.ice_temp_min, cal.ice_temp_max),
            ("snow_temp", cal.snow_temp_curve, cal.snow_temp_min, cal.snow_temp_max)):
        raw = [_interp(curve, t) for t in ts]
        res[nm + "_min"] = any(r < cmin for r in raw)
        res[nm + "_max"] = any(r > cmax for r in raw)
    # sigma_speed_extrap_max: rakendub, kui 0,25*(v/hi - 1) > lagi
    worst = 0.0
    for surf, (slo, shi) in cal.speed_range.items():
        worst = max(worst, cal.sigma_speed_extrap * (UI_SPEED[1] / shi - 1.0))
    res["sigma_speed_extrap_max"] = worst > cal.sigma_speed_extrap_max
    res["_worst_speed_sigma"] = worst
    return res


# UN R13-H, Type-0 pidurdus, kategooria M1, mootor lahutatud.
# Kontrollitud EUR-Lexist 16.09.2026, kaks soltumatut dokumenti
# (CELEX:42015X1222(01) ja ELI reg/2023/401) annavad sama arvu:
#   katsekiirus 100 km/h, pidurdusmaa s <= 0,1v + 0,0060v^2,
#   KESKMINE VALJAARENENUD AEGLUSTUS d_m >= 6,43 m/s^2,
#   pedaalijoud 6,5-50 daN, katse tehakse nii koormatud kui tuhjalt.
# 6,43 / 9,80665 = 0,656 g.
#
# See on PORAND, mitte tuupvaartus: paris autod kuival asfaldil
# annavad TUV SUD-i aruannetes 0,99-1,18 g. Aga porand on paris
# regulatsioon ja seega paris kontroll -- uhelgi tuubikinnitatud
# M1-autol EI TOHI olla vaiksemat pidurivoimekust.
R13H_FLOOR_G = 6.43 / 9.80665


def check_brake_floor():
    """Kas monel autol on pidurivoimekus alla R13-H regulatiivse porandi?

    brake_capacity_g on presets-is HINNANG klassi jargi -- ainus
    soidukivali, mis ei tule tootja andmelehelt. Seda ei saa ankrute
    vastu sobitada (pidurivoimekus piirab ainult siis, kui ta on
    haardest VAIKSEM, ja ankrutestides ta ei ole). Aga regulatsioon
    annab talle alumise piiri, ja see on parem kui mitte midagi.
    """
    from .presets import VEHICLES
    from .model import AbsClass
    bad = []
    for k, v in VEHICLES.items():
        # R13-H kehtib tuupkinnitatud M1-autodele. ABS-ita autod on
        # sellest vanemad ja neile see porand ei kehti.
        if v.abs_class is AbsClass.NONE:
            continue
        if v.brake_capacity_g < R13H_FLOOR_G:
            bad.append((k, v.name, v.brake_capacity_g))
    return bad


def check_shadowed_vehicles():
    """Kas monda autot on vehicles_ee.py-s defineeritud, aga baas varjab ta?

    Selline rida on kahjutu ainult siis, kui ta on baasiga IDENTNE. Kui
    ta hakkab erinema, siis keegi muudab faili, mille muudatus ei jouda
    kuhugi -- ja seda ei ole kuidagi naha. Siin see kontrollitakse.
    """
    from .presets import EE_SHADOWED, VEHICLES
    from .vehicles_ee import EE_VEHICLES, FRONTAL_AREA_K
    shadowed = {k for k, _ in EE_SHADOWED}
    bad = []
    for row in EE_VEHICLES:
        k = row[0]
        if k not in shadowed:
            continue
        key, name, mass, cd, w, h, wb, press, size, acl, brake = row[:11]
        v = VEHICLES[k]
        cda = round(cd * FRONTAL_AREA_K * w * h, 3)
        d = []
        if abs(v.kerb_mass_kg - mass) > 1: d.append("mass")
        if abs(v.cda_m2 - cda) > 0.005: d.append("CdA")
        if v.oem_size != size: d.append("mot")
        if v.abs_class is not acl: d.append("ABS")
        if abs(v.recommended_pressure_bar - press) > 0.01: d.append("rohk")
        if abs(v.brake_capacity_g - brake) > 0.005: d.append("pidurid")
        if v.name != name: d.append("nimi")
        if d:
            bad.append((k, d))
    return len(shadowed), bad


def check_speed_range():
    """Kas iga pinna lubatud kiirusevahemik on ankrutega kaetud?"""
    cal = Calibration()
    have = {}
    for a in ANCHORS:
        have.setdefault(a.surface, []).append(a.v_from_kmh)
    out = []
    for surf, (lo, hi) in cal.speed_range.items():
        vs = have.get(surf, [])
        out.append((surf.name, lo, hi,
                    min(vs) if vs else None, max(vs) if vs else None, len(vs)))
    return out


def main():
    fail = []
    print("=" * 76)
    print("PÄRITOLUAUDIT — kas iga konstant tuleb millestki päris?")
    print("=" * 76)

    # --- 1. kate ---
    missing, extra, unsourced = check_coverage()
    print(f"\n1) KATE: {len(fields(Calibration))} välja, "
          f"{len(ORIGINS)} registris")
    if missing:
        fail.append("registrist puuduvad väljad")
        print("   LÄBI KUKKUNUD — registrist puudu:", ", ".join(missing))
    if extra:
        print("   HOIATUS — registris on välju, mida mudelis ei ole:",
              ", ".join(extra))
    if unsourced:
        fail.append("UNSOURCED konstandid")
        print("   LÄBI KUKKUNUD — tõenduseta:", ", ".join(unsourced))
    if not missing and not unsourced:
        print("   OK — iga väli on registris ja ükski ei ole UNSOURCED")

    kinds = {}
    for o in ORIGINS.values():
        kinds[o.kind] = kinds.get(o.kind, 0) + 1
    print("   liigiti: " + "  ".join(f"{k} {v}" for k, v in sorted(kinds.items())))

    # --- 2. sigma ausus ---
    print("\n2) SIGMA AUSUS — kas lubatud veapiir katab tegeliku hajuvuse?")
    print(f"   {'pind':14} {'n':>4} {'jääk σ':>8} {'lubatud':>8}   ")
    for name, n, resid, decl, ok in sorted(check_sigma()):
        mark = "OK" if ok else "LÄBI KUKKUNUD"
        if not ok:
            fail.append(f"sigma_base[{name}] < jääk")
        print(f"   {name:14} {n:>4} {resid*100:>7.2f}% {decl*100:>7.2f}%   {mark}")

    # --- 2b. R13-H porand ---
    print("\n2b) PIDURIVOIMEKUS — kas moni auto on alla R13-H porandi?")
    print(f"   UN R13-H Type-0, M1: d_m >= 6,43 m/s2 = {R13H_FLOOR_G:.3f} g")
    bad = check_brake_floor()
    if bad:
        fail.append("brake_capacity_g alla R13-H porandi")
        print("   LABI KUKKUNUD:")
        for k, nm, g in bad:
            print(f"      {k:22} {nm:38} {g:.3f} g")
    else:
        from .presets import VEHICLES
        lo = min(v.brake_capacity_g for v in VEHICLES.values())
        print(f"   OK — madalaim mudelis {lo:.2f} g, korgeim "
              f"{max(v.brake_capacity_g for v in VEHICLES.values()):.2f} g")
        print("   Vordluseks: TUV SUD-i aruannetes on paris sooduki kuiv")
        print("   pidurdus 100->0 km/h 0,99-1,18 g, ehk porand on porand.")

    # --- 2c. varjatud soidukiread ---
    n_sh, bad_sh = check_shadowed_vehicles()
    print(f"\n2c) VARJATUD SOIDUKIREAD — {n_sh} rida vehicles_ee.py-s, mida")
    print("    baasnimekiri varjab. Kahjutud ainult siis, kui identsed.")
    if bad_sh:
        fail.append("varjatud soidukirida erineb baasist")
        print("   LABI KUKKUNUD — need erinevad, seega muudatus ei jouagi kuhugi:")
        for k, d in bad_sh:
            print(f"      {k:24} erineb: {', '.join(d)}")
        print("   Paranda BAASI (presets.py), mitte vehicles_ee.py-d.")
    else:
        print("   OK — koik varjatud read on baasiga identsed")

    # --- 3. klambrid ---
    print("\n3) KLAMBRID — kas ohutuspiir aktiveerub tavavahemikus?")
    hits = check_clamps()
    if hits:
        print("   HOIATUS — klamber lõikab -30...+2 °C sees:")
        for nm, t, raw in hits[:6]:
            print(f"      {nm} {t:+.0f} °C  toores {raw:.3f}")
    else:
        print("   OK — ükski klamber ei aktiveeru -30...+2 °C juures,")
        print("        seega nad ei mõjuta ühtegi tavapärast vastust")

    # --- 4. kiirusevahemik ---
    print("\n4) KIIRUSEVAHEMIK — kas lubatud ala on ankrutega kaetud?")
    print(f"   {'pind':14} {'lubatud':>14} {'ankrud':>14} {'n':>4}")
    for nm, lo, hi, amin, amax, n in sorted(check_speed_range()):
        rng = f"{amin:.0f}-{amax:.0f}" if n else "PUUDUB"
        warn = "" if n and amin <= lo and amax >= hi * 0.6 else "   <- ekstrapolatsioon"
        print(f"   {nm:14} {lo:>6.0f}-{hi:<7.0f} {rng:>14} {n:>4}{warn}")

    # --- 5. tundlikkus ---
    print("\n5) TUNDLIKKUS — ±10 % nihe igale konstandile")
    print("   'ankur' = kui palju muutub 369 ankru viga (kas ANDMED kitsendavad)")
    print("   'vastus' = kui palju muutub tüüpiline kasutaja tulemus (kas LOEB)")
    base_err = anchor_err(Calibration())
    base_out = outputs(Calibration())
    print(f"   ankruhulgad: " + ", ".join(f"{k} {v*100:.2f}%"
          for k, v in sorted(base_err.items())))
    rows = []
    for f in fields(Calibration):
        o = ORIGINS.get(f.name)
        da, dd, ds, who = sensitivity(f.name, base_err, base_out)
        rows.append((max(dd, ds), dd, ds, da, f.name,
                     o.kind if o else "?", who))
    rows.sort(reverse=True)

    print(f"\n   {'konstant':28} {'liik':11} {'maa':>7} {'piir':>7} "
          f"{'ankur':>8}  aktiveeris")
    risky, dead = [], []
    for _, dd, ds, da, name, kind, who in rows:
        flag = ""
        if max(dd, ds) < 1e-9:
            dead.append(name)
            flag = "  <-- ÜKSKI STSENAARIUM EI AKTIVEERI"
        elif dd > 0.01 and da < 0.0005 and kind not in ("DERIVED", "CLAMP"):
            # eristame "uldse mitte" ja "norgalt" -- esimene on auk,
            # teine on teadaolev piirang
            weak = da >= 0.0001
            flag = ("  <-- LIIGUTAB, ANKRUD KITSENDAVAD NORGALT" if weak
                    else "  <-- LIIGUTAB, ANKRUD EI KITSENDA")
            risky.append((name, kind, dd, weak))
        print(f"   {name:28} {kind:11} {dd*100:>6.2f}% {ds*100:>6.2f}% "
              f"{da*100:>7.2f}pp  {(who or '-')[:22]}{flag}")

    inert_proof = check_inert()
    proven = [n for n in dead
              if n in inert_proof and inert_proof[n] is False]
    dead = [n for n in dead if n not in proven]
    if proven:
        print("\n   TÕESTATULT TEGEVUSETU (klamber, mis liidese lubatud alas")
        print("   ei saa kunagi rakenduda -- see EI OLE viga, aga peab")
        print("   olema valja oeldud, mitte naitama nulli vaikselt):")
        for n in proven:
            print(f"      {n}  — kaitsekiht, mis praeguste piiridega ei aktiveeru")
        print(f"      (halvim sigma kiiruse ekstrapolatsioonist liidese piires: "
              f"{inert_proof.get('_worst_speed_sigma', 0)*100:.1f} %, "
              f"lagi {Calibration().sigma_speed_extrap_max*100:.0f} %)")
    if dead:
        fail.append(f"{len(dead)} konstanti ei ole üheski stsenaariumis kaetud")
        print("\n   LÄBI KUKKUNUD — need konstandid ei mõjutanud ühtegi")
        print("   stsenaariumi, seega audit EI OLE neid tegelikult")
        print("   kontrollinud. Lisa stsenaarium või eemalda konstant:")
        for n in dead:
            print("      ", n)

    print("\n" + "=" * 76)
    if risky:
        print("KONSTANDID, MIS LIIGUTAVAD VASTUST ILMA ANKRUTETA:")
        for name, kind, dd, weak in risky:
            o = ORIGINS[name]
            print(f"\n  {name}  ({kind}, kuni {dd*100:.1f} % vastuses"
                  f"{', ankrud kitsendavad norgalt' if weak else ', ANKRUID EI OLE'})")
            print(f"     allikas: {o.source}")
            if o.note:
                print(f"     {o.note[:220]}")
        print("\n  Need EI OLE tingimata valed. Nad on need, mille puhul")
        print("  mudel tugineb kirjandusele ja mitte omaenda ankrutele --")
        print("  ja see peab olema nähtav, mitte peidus.")
    else:
        print("Ükski kirjandusest võetud konstant ei liiguta vastust üle 1 %.")

    print("\n" + "=" * 76)
    if fail:
        print("AUDIT KUKKUS LÄBI:", "; ".join(fail))
        return 1
    print("AUDIT LÄBITUD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
