"""
Ankurpunktid: päris, avaldatud pidurdustestide tulemused.

Need on mudeli "reaalsuskontroll". Iga kirje on üks mõõdetud pidurdusmaa
koos testi tingimustega. Mudel peab need suutma taastoota.

Allikad:
  [TM25]  Tekniikan Maailma 2025 talverehvitest (UTAC), 205/55 R16,
          VW Golf. Kuiv 80->0, märg 80->0, jää 50->0.
          Kajastus: tyrereviews.com/Tyre-Tests/2025-Friction-and-Studded-
          Winter-Tyre-Test.htm
  [UT25]  UTAC / Aftonbladet 2025 suve- ja lamellrehvitest, 225/45 R17.
          Kuiv 100->5, märg 80->5 (keskmine temperatuuridel +2…+17 °C).
          Kajastus: tyrereviews.com/Tyre-Tests/2025-Summer-and-All-Season-
          Combined-Tyre-Test.htm
  [DEKRA] DEKRA mustrisügavuse test, 100 km/h: 2-3 mm muster annab märjal
          16-18 % ja kuival 2,4-8,5 % pikema pidurdusmaa kui 7-8 mm.
  [ADAC25] ADAC 2025 talverehvitest, 225/40 R18, VW Golf, 31 rehvi.
          Kuiv 100->0, märg asfalt 80->0, MÄRG BETOON 80->0, LUMI 30->0,
          JÄÄ 20->0, akvaplaneerimise ujumiskiirus. Vt anchors_adac.py.
          Kajastus: tyrereviews.com/Tyre-Tests/2025-ADAC-Winter-Tyre-Test.htm
  [ADACS25] ADAC 2025 suverehvitest, 225/40 R18, 18 rehvi x 3 pinda.
  [ADACA25] ADAC 2025 lamellrehvitest, 225/45 R17, 16 rehvi x 5 pinda.
          NB: siin on marg pidurdus 100 -> 0 km/h, teistes 80 -> 0.
          See on ainus koht, kus marja kiirusesoltuvust saab valideerida.
          Vt anchors_adac2.py.
  [PASSAT] Influence of tire pressure on the vehicle braking distance.
          2 x VW Passat B5, suverehv GoodYear DuraGrip ja talverehv
          Debica Frigo 2 195/65 R15, 50 km/h, rõhud 1,0-3,0 bar,
          kuiv / märg / lumi, 6 kordust punkti kohta.
          Kasutatakse SUHTARVUDENA (vt PRESSURE_RELATIONS).
  [MDPI25] Machines 14(9):1002 — pidurdusmaa 4 rõhul, 50 km/h, kuiv,
          ABS VÄLJAS, uus vs vananenud rehv.
  [R117]  UNECE R117: märghaardumise testi metoodika, mfdd = 231,48 / S
          (S = pidurdusmaa 80->20 km/h), veekile 0,5-1,5 mm, katte pbfc
          0,6-0,8, temperatuuriparandus pbfc += 0,0035·(t-20).

Märkus testitingimuste kohta: magazinid ei avalda alati täpset teekatte
temperatuuri ja veekile paksust. Allpool on kasutatud metoodikale
tüüpilisi väärtusi ja need on eraldi väljadena nähtaval, et neid saaks
hiljem täpsustada.
"""

from dataclasses import dataclass
from typing import Optional

from .model import Surface, Texture, TyreCategory


@dataclass
class Anchor:
    source: str
    tyre_key: str
    category: TyreCategory
    wet_grip_class: str          # hinnang; päris süsteemis EPREL-ist
    vehicle_key: str
    size: str
    surface: Surface
    water_mm: float
    temp_c: float
    v_from_kmh: float
    v_to_kmh: float
    measured_m: float
    texture: Texture = Texture.NORMAL
    tread_mm: float = 8.0
    note: str = ""
    # Kui rehvi G on juba teada (nt tuletatud sama testi märja katsest),
    # kasutatakse seda klassi keskpunkti asemel.
    wet_grip_index: Optional[float] = None


S, T = Surface, Texture
C = TyreCategory

# --- [TM25] talverehvid, VW Golf, 205/55 R16 -------------------------------
# NB! Märghaardumise klassid siin on TULETATUD, mitte EPREL-ist kontrollitud.
# Algselt oletati klassiks C; ristkontroll UT25 testiga (vt calibrate.py,
# "VALIDEERIMINE 3") näitas, et kaks sõltumatut testi annavad sama k_G ainult
# siis, kui Põhjamaade talverehvide klass on D (X-Ice Snow'l E). See on
# realistlik — Põhjamaade naelutud ja naastrehvid on EL-i märgisel märjal
# tüüpiliselt C-E. PÄRIS SÜSTEEMIS TULEB SEE VÄLI EPREL-IST.
# Kuiv 80->0 km/h, katte temp u +10 °C (Nurmijärvi / UTAC oktoober)
_TM_DRY = [
    ("nokian_r5", C.WINTER_NORDIC, "D", 30.80),
    ("falken_wpfs1", C.WINTER_NORDIC, "D", 30.80),
    ("hankook_iz3", C.WINTER_NORDIC, "D", 31.30),
    ("conti_vc8", C.WINTER_NORDIC, "D", 31.40),
    ("goodyear_ugice3", C.WINTER_NORDIC, "D", 31.50),
    ("michelin_xicesnow", C.WINTER_NORDIC, "E", 32.20),
    ("radar_dimax_ice", C.WINTER_NORDIC, "D", 32.60),
    ("conti_ic3", C.WINTER_STUDDED, "D", 31.50),
    ("pirelli_iz2", C.WINTER_STUDDED, "D", 31.60),
    ("goodyear_ugarctic2", C.WINTER_STUDDED, "D", 31.90),
    ("michelin_xin4", C.WINTER_STUDDED, "D", 32.10),
    ("kumho_wi32", C.WINTER_STUDDED, "D", 32.20),
    ("nokian_hkpl10", C.WINTER_STUDDED, "D", 32.40),
    ("bridgestone_spike3", C.WINTER_STUDDED, "D", 33.40),
]
# Märg 80->0 km/h
_TM_WET = [
    ("falken_wpfs1", C.WINTER_NORDIC, "D", 37.50),
    ("hankook_iz3", C.WINTER_NORDIC, "D", 37.50),
    ("goodyear_ugice3", C.WINTER_NORDIC, "D", 37.70),
    ("nokian_r5", C.WINTER_NORDIC, "D", 37.90),
    ("radar_dimax_ice", C.WINTER_NORDIC, "D", 39.40),
    ("conti_vc8", C.WINTER_NORDIC, "D", 39.50),
    ("michelin_xicesnow", C.WINTER_NORDIC, "E", 41.10),
    ("pirelli_iz2", C.WINTER_STUDDED, "D", 34.30),
    ("conti_ic3", C.WINTER_STUDDED, "D", 35.50),
    ("goodyear_ugarctic2", C.WINTER_STUDDED, "D", 36.00),
    ("bridgestone_spike3", C.WINTER_STUDDED, "D", 36.30),
    ("nokian_hkpl10", C.WINTER_STUDDED, "D", 37.30),
    ("michelin_xin4", C.WINTER_STUDDED, "D", 37.80),
    ("kumho_wi32", C.WINTER_STUDDED, "D", 40.80),
]
# Jää 50->0 km/h, jää temp u -5 °C
_TM_ICE = [
    ("michelin_xicesnow", C.WINTER_NORDIC, "E", 45.60),
    ("conti_vc8", C.WINTER_NORDIC, "D", 47.10),
    ("nokian_r5", C.WINTER_NORDIC, "D", 47.90),
    ("falken_wpfs1", C.WINTER_NORDIC, "D", 47.90),
    ("goodyear_ugice3", C.WINTER_NORDIC, "D", 50.20),
    ("radar_dimax_ice", C.WINTER_NORDIC, "D", 53.30),
    ("hankook_iz3", C.WINTER_NORDIC, "D", 53.50),
    ("bridgestone_spike3", C.WINTER_STUDDED, "D", 32.30),
    ("kumho_wi32", C.WINTER_STUDDED, "D", 33.10),
    ("nokian_hkpl10", C.WINTER_STUDDED, "D", 33.90),
    ("goodyear_ugarctic2", C.WINTER_STUDDED, "D", 36.90),
    ("michelin_xin4", C.WINTER_STUDDED, "D", 37.70),
    ("pirelli_iz2", C.WINTER_STUDDED, "D", 41.60),
    ("conti_ic3", C.WINTER_STUDDED, "D", 42.50),
]

# --- [UT25] suve- ja lamellrehvid, 225/45 R17 ------------------------------
# Kuiv 100->5 km/h, katte temp u +25 °C (Vizzola)
_UT_DRY = [
    ("pirelli_p7c2", C.SUMMER_TOURING, "A", 34.20),
    ("conti_pc7", C.SUMMER_TOURING, "A", 34.20),
    ("nokian_hakkablue3", C.SUMMER_TOURING, "A", 34.60),
    ("goodyear_f1a6", C.SUMMER_UHP, "A", 35.10),
    ("hankook_prime4", C.SUMMER_TOURING, "B", 35.10),
    ("falken_ze320", C.SUMMER_TOURING, "B", 35.20),
    ("bridgestone_t6", C.SUMMER_TOURING, "A", 35.70),
    ("michelin_primacy5", C.SUMMER_TOURING, "A", 36.00),
    ("vredestein_ultrac", C.SUMMER_TOURING, "B", 36.90),
    ("nordman_south", C.SUMMER_TOURING, "C", 37.40),
    ("pirelli_as_sf3", C.ALL_SEASON, "B", 37.90),
    ("bridgestone_as6", C.ALL_SEASON, "B", 38.00),
    ("conti_asc2", C.ALL_SEASON, "A", 39.70),
    ("goodyear_v4s3", C.ALL_SEASON, "B", 40.80),
]
# Märg 80->5 km/h, tulemus on keskmine +2 / +7 / +12 / +17 °C juurest
# -> mudelis kasutame ekvivalentset ~+9,5 °C
_UT_WET = [
    ("michelin_primacy5", C.SUMMER_TOURING, "A", 33.00),
    ("pirelli_p7c2", C.SUMMER_TOURING, "A", 33.10),
    ("nokian_hakkablue3", C.SUMMER_TOURING, "A", 33.20),
    ("bridgestone_as6", C.ALL_SEASON, "B", 33.50),
    ("pirelli_as_sf3", C.ALL_SEASON, "B", 33.80),
    ("vredestein_ultrac", C.SUMMER_TOURING, "B", 36.50),
]


def _mk(src, rows, veh, size, surf, water, temp, v0, v1, tread=8.0, tex=T.NORMAL):
    return [Anchor(src, k, cat, cls, veh, size, surf, water, temp,
                   v0, v1, m, tex, tread)
            for (k, cat, cls, m) in rows]


# --- [ADAC25] ---------------------------------------------------------------

def _adac():
    from .anchors_adac import ADAC_2025, ADAC_CONDS, ADAC_CLASS
    out = []
    for key, row in ADAC_2025.items():
        name = row[0]
        for i, (tag, surf, water, temp, v0, v1) in enumerate(ADAC_CONDS):
            out.append(Anchor("ADAC25", key, C.WINTER_CENTRAL, ADAC_CLASS[key],
                              "vw_golf_8", "225/40 R18", surf, water, temp,
                              v0, v1, row[1 + i], T.NORMAL, 8.0,
                              note=tag))
    return out


def _adac2():
    """ADAC suve- ja lamellrehvitestid. Klass tuletatakse hiljem
    (vt calibrate_adac2), esialgu klassi keskpunkt kategooria jargi."""
    from .anchors_adac2 import SETS
    from .anchors_adac2 import ADAC_CLASS2
    out = []
    for src, table, conds, cat, size in SETS:
        for key, row in table.items():
            for i, (tag, surf, water, temp, v0, v1) in enumerate(conds):
                out.append(Anchor(src, key, cat, ADAC_CLASS2.get(key, "B"),
                                  "vw_golf_8", size, surf, water, temp,
                                  v0, v1, row[1 + i], T.NORMAL, 8.0, note=tag))
    return out


def _gravel():
    """Kruusa ankrud. Andmed on anchors_gravel.py-s, kus on ka selgitus,
    MIKS kruusal ABS pidurdusmaad PIKENDAB."""
    from .anchors_gravel import SA4X4_ROWS, SATC_ROWS
    out = []
    # [SATC19] VW Polo Vivo, tihe kruusatee, kuiv, 3 kiirust x 3 mustrit
    # x ABS sees/väljas. Rehvid on suverehvid, rõhk 2,2 bar.
    for v, td, abs_on, m in SATC_ROWS:
        out.append(Anchor(
            "SATC19", "satc_gravel", C.SUMMER_TOURING, "C",
            "polo_vivo" if abs_on else "polo_vivo_noabs", "175/70 R14",
            S.GRAVEL, 0.0, 22.0, v, 0.0, m, T.NORMAL, td,
            note="tihe kruusatee, ABS " + ("sees" if abs_on else "väljas")))
    # [SA4X4] on TEADLIKULT ankrute seast VÄLJAS. Seal on hoopis teine
    # pind (kõva, tihe kruusarada) ja hoopis teine sõiduk (pikap, mille
    # parameetrid on minu hinnang, mitte tehase andmed). Kui ta ankruks
    # panna, kisub ta mu_gravel'i üles ja rikub SATC-i sobituse.
    # Ta on gravel_validation() all: mudel ennustab seal u 41 % pikemat
    # pidurdusmaad kui mõõdeti, ehk kõva kruusa peal on mudel
    # KONSERVATIIVNE. Nii see olgu -- kruus on mudelis üks pind, aga
    # päris elus on lahtise ja kõvaks sõidetud kruusa vahe suur.
    return out


def gravel_validation():
    """Sobitusest välja jäetud kruusa mõõtmised.

    Vt kommentaari _gravel()-is: kõva kruusarada + pikap, mille
    parameetrid on hinnangulised. Kasutatakse ainult valideerimiseks."""
    from .anchors_gravel import SA4X4_ROWS
    return [Anchor("SA4X4", key, C.SUMMER_TOURING, "C", "ford_ranger_fx4",
                   "265/65 R17", S.GRAVEL, 0.0, 21.0, 80.0, 0.0, m,
                   T.NORMAL, 8.0, note="kõva tihe kruus, ABS sees, all-terrain")
            for key, m in SA4X4_ROWS]


ANCHORS = (
    _mk("TM25", _TM_DRY, "vw_golf_8", "205/55 R16", S.ASPHALT, 0.0, 10.0, 80, 0)
    + _mk("TM25", _TM_WET, "vw_golf_8", "205/55 R16", S.ASPHALT, 1.0, 8.0, 80, 0)
    + _mk("TM25", _TM_ICE, "vw_golf_8", "205/55 R16", S.ICE, 0.0, -5.0, 50, 0)
    + _mk("UT25", _UT_DRY, "audi_a3", "225/45 R17", S.ASPHALT, 0.0, 25.0, 100, 5)
    + _mk("UT25", _UT_WET, "audi_a3", "225/45 R17", S.ASPHALT, 1.0, 9.5, 80, 5)
    + _adac()
    + _adac2()
    + _gravel()
)


# --- [PASSAT] rehvirõhu suhtarvud -------------------------------------------
# Mõõdetud pidurdusmaad 50 km/h juurest, 6 kordust punkti kohta, VW Passat B5.
# Absoluutväärtusi EI kasutata (testi metoodika täpne definitsioon on lahtine),
# küll aga SUHTARVE ühe ja sama seansi sees -- need on usaldusväärsed ka siis,
# kui absoluutne nulltase on nihkes.
#
# See on seni AINUS avalik andmestik, mis mõõdab rõhu mõju pidurdusmaale
# mitmel pinnal korraga. Enne seda oli rõhukõver mudelis puhtalt kirjandusest.
_PASSAT_RAW = {
    ("summer", "dry"):  {1.0: 11.46, 1.5: 11.76, 2.0: 11.27, 2.5: 11.25, 3.0: 11.57},
    ("summer", "wet"):  {1.0: 17.37, 1.5: 16.88, 2.0: 16.82, 2.5: 17.08, 3.0: 17.30},
    ("summer", "snow"): {1.0: 60.40, 1.5: 59.70, 2.0: 58.05, 2.5: 61.80, 3.0: 62.32},
    ("winter", "dry"):  {1.0:  9.99, 1.5: 10.10, 2.0:  9.67, 2.5:  9.75, 3.0: 10.18},
    ("winter", "wet"):  {1.0: 15.87, 1.5: 15.18, 2.0: 15.02, 2.5: 15.33, 3.0: 15.68},
    ("winter", "snow"): {1.0: 25.10, 1.5: 24.48, 2.0: 24.45, 2.5: 25.83, 3.0: 26.08},
}
PASSAT_NOMINAL_BAR = 2.0

def pressure_relations():
    """[(rehvitüüp, pind, rõhk_bar, suhtarv nominaali suhtes), ...]"""
    out = []
    for (tyre, surf), row in _PASSAT_RAW.items():
        base = row[PASSAT_NOMINAL_BAR]
        for p, d in sorted(row.items()):
            out.append((tyre, surf, p, d / base))
    return out


# Sama uuring annab ka summa/talve suhte lumel nominaalrõhul:
SNOW_SUMMER_WINTER_RATIO = (_PASSAT_RAW[("summer","snow")][2.0]
                            / _PASSAT_RAW[("winter","snow")][2.0])   # 2.374

# [MDPI25] ABS VÄLJAS: rõhu langus 2.413 -> 1.689 bar pikendas
# pidurdusmaad uuel rehvil 15,0 % ja vananenud rehvil 17,3 %.
# ABS-iga (PASSAT) on sama suurusjärgu langus ainult ~3-5 %.
# Järeldus: rõhutundlikkus on ABS-ita oluliselt suurem.
MDPI_NOABS = dict(p_hi=2.413, p_lo=1.689, ratio_new=1.150, ratio_aged=1.173,
                  speed_kmh=50, surface="dry")


# --- eraldi seosekontrollid (mitte üksikpunktid, vaid suhted) --------------

RELATIONS = [
    dict(name="Mustrisügavus, märg (DEKRA)",
         desc="8 mm -> 2,5 mm, 100 km/h, ~1 mm vett",
         expected_ratio=1.17, tol=0.03),
    dict(name="Mustrisügavus, kuiv (DEKRA)",
         desc="8 mm -> 2,5 mm, 100 km/h, kuiv",
         expected_ratio=1.055, tol=0.035),
    dict(name="Kiiruse ruut (füüsika)",
         desc="50 -> 100 km/h kuival peab pidurdusmaa kasvama ~4x",
         expected_ratio=4.0, tol=0.45),
    dict(name="R117 mfdd (metoodika)",
         desc="mfdd = 231,48 / S, S = pidurdusmaa 80->20 km/h",
         expected_ratio=1.0, tol=0.08),
]
