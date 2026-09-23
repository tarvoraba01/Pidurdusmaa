"""
Pidurdusmaa füüsikamootor.
==========================

Kihiline mudel, mis arvutab sõiduauto pidurdusmaa etteantud
auto + rehvi + tee + ilma + kiiruse kombinatsiooni jaoks.

Ülesehitus (vt README.md):

  Layer 1  fundamentaalne füüsika ..... d = ∫ v dv / a(v)
  Layer 2  rehv ...................... mu_ref(G, kategooria) x rõhk x muster x temp
  Layer 3  tee ....................... pinnas x tekstuur x veekile x akvaplaneering
  Layer 4  auto ...................... ABS x koormus x aero x kalle x pidurite viide

Kood on teadlikult ainult standardteegil (ei numpy'd) -- see mudel on
mõeldud hiljem 1:1 TypeScripti porditavaks, et seesama mootor jookseks
ka brauseris.

Kõik ühikud on SI või selgelt nimetatud (kmh, bar, mm, °C).
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Optional, Sequence

G_ACC = 9.80665          # raskuskiirendus, m/s^2
RHO_AIR = 1.225          # õhutihedus 15 °C, kg/m^3


# ---------------------------------------------------------------------------
# Loendid
# ---------------------------------------------------------------------------

class TyreCategory(Enum):
    """Rehvi kategooria. Määrab kummisegu temperatuurikäitumise ja talvevõimed."""
    SUMMER_UHP = "suverehv (UHP / sport)"
    SUMMER_TOURING = "suverehv (touring)"
    ALL_SEASON = "lamellrehv / all-season"
    WINTER_CENTRAL = "talverehv (Kesk-Euroopa)"
    WINTER_NORDIC = "talverehv (Põhjamaade, naelutu)"
    WINTER_STUDDED = "naastrehv"


class Surface(Enum):
    """Teekate."""
    ASPHALT = "asfalt"
    CONCRETE = "betoon"
    GRAVEL = "kruus"
    SNOW_PACKED = "tallatud lumi"
    SNOW_LOOSE = "lahtine lumi"
    ICE = "jää"


class Texture(Enum):
    """Katte mikro-/makrotekstuur. Mõjutab peamiselt märga haardumist."""
    COARSE_NEW = "uus / kare"
    NORMAL = "tavaline"
    WORN_SMOOTH = "kulunud / sile / roopad"
    POLISHED = "poleeritud (nt vana betoon, teekattemärgistus)"


class AbsClass(Enum):
    """Pidurisüsteemi põlvkond -- kui suure osa tipphaardest ABS reaalselt ära kasutab."""
    NONE = "ABS puudub"
    EARLY = "varane ABS (u 1990-2003)"
    MODERN = "kaasaegne ABS + EBD (u 2004-2014)"
    LATEST = "kaasaegne ABS + pidurdusabi (2015+)"


# ---------------------------------------------------------------------------
# Sisendid
# ---------------------------------------------------------------------------

@dataclass
class Tyre:
    """Rehv.

    `wet_grip_index` on EL rehvimärgise märghaardumise indeks G
    (UNECE R117 / EL 2020/740). See on ANDMEMUDELI SÜDA: G tuleb EPREL-ist
    ja on ainus avalik, iga rehvi kohta olemasolev haardumise number.

    Klassi keskpunktid C1-rehvidele:
        A: G >= 1.55   (kasutame 1.60)
        B: 1.40-1.54   (1.47)
        C: 1.25-1.39   (1.32)
        D: 1.10-1.24   (1.17)
        E: G <= 1.09   (1.05)
    """
    name: str
    category: TyreCategory
    wet_grip_index: float                     # EPREL G
    tread_depth_mm: float = 8.0               # praegune mustrisügavus
    tread_depth_new_mm: float = 8.0           # sama rehvi sügavus uuena
    pressure_bar: Optional[float] = None      # None -> kasuta auto soovitust
    load_capacity_kg: Optional[float] = None  # koormusindeksist, ühe rehvi kohta
    age_years: float = 1.0
    studded: bool = False
    # Kuivhaardumist EL-märgis EI kata. Kui on olemas päris test, pane siia.
    mu_dry_override: Optional[float] = None
    # Sama lume/jää kohta (nt ADAC / TM testist tuletatud).
    mu_snow_override: Optional[float] = None
    mu_ice_override: Optional[float] = None
    # Mõõdetud ujumiskiirus / mudeli ujumiskiirus (ADAC-i protokoll). 1.0 =
    # rehvitüübi keskmine. Veebis kasutatakse ainult sügava vee real.
    hp_factor: float = 1.0
    size: str = ""
    # KUST G TULEB. See ei ole kosmeetika -- sellest sõltub veapiir.
    #   "test"  = tuletatud päris avaldatud testi pidurdusmaast, seega
    #             SELLE rehvi oma number
    #   "label" = EL-i märgise klassi keskpunkt (EPREL annab ainult klassi,
    #             mitte numbrit). Klass on 0,15 laiune vahemik, nii et kaks
    #             sama klassi rehvi võivad päriselt erineda kuni 10 %
    #             pidurdusmaas -- see lisatakse veapiirile.
    g_source: str = "label"

    @property
    def wet_grip_class(self) -> str:
        g = self.wet_grip_index
        if g >= 1.55:
            return "A"
        if g >= 1.40:
            return "B"
        if g >= 1.25:
            return "C"
        if g >= 1.10:
            return "D"
        return "E"


@dataclass
class Vehicle:
    """Sõiduk."""
    name: str
    kerb_mass_kg: float
    abs_class: AbsClass = AbsClass.LATEST
    cda_m2: float = 0.65                 # Cd * A, õhutakistuse pindala
    cog_height_m: float = 0.55           # raskuskeskme kõrgus
    wheelbase_m: float = 2.70
    recommended_pressure_bar: float = 2.3
    oem_size: str = ""
    # Kas pidurid ise suudavad rehvi tipphaarde välja nõuda. Tänapäeval
    # praktiliselt alati jah; erand on ülekoormatud või ülekuumenenud pidurid.
    brake_capacity_g: float = 1.3


@dataclass
class Conditions:
    """Olukord."""
    speed_kmh: float = 90.0
    surface: Surface = Surface.ASPHALT
    texture: Texture = Texture.NORMAL
    water_mm: float = 0.0                # veekile paksus (ainult asfalt/betoon)
    temp_c: float = 20.0                 # teepinna temperatuur
    payload_kg: float = 75.0             # juht + kraam
    gradient_pct: float = 0.0            # + = ülesmäge (aitab), - = allamäge
    reaction_time_s: float = 0.0         # 0 = ainult pidurdusmaa; 1.0 = koos reaktsiooniga
    # Pidurite VÕIMEKUS osakaaluna terve auto omast (1.0 = korras).
    # NB: see EI OLE klotside kulumine. Normaalselt kulunud, aga korras
    # klotsid annavad endiselt 1.0 -- klots hõõrdub sama hästi kuni
    # metallini. Alla 1.0 tähendab tegelikku riket või kuumenemist.
    brake_condition: float = 1.0


# ---------------------------------------------------------------------------
# Mudeli konstandid (kalibreeritavad)
# ---------------------------------------------------------------------------

@dataclass
class Calibration:
    """Kõik empiirilised konstandid ühes kohas, et neid saaks päris
    testandmete vastu numbriliselt sobitada (vt calibrate.py)."""

    # --- Layer 2: rehv ---
    # mu_wet_ref = k_G * G   (asfalt, 20 °C, 1.0 mm vett, 80 km/h, uus muster)
    k_g: float = 0.6727     # sobitatud 85 märja ankru vastu
    # kuiva haarde baas kategooria kohta, asfalt, 20 °C, 80 km/h
    mu_dry_base: dict = field(default_factory=lambda: {
        TyreCategory.SUMMER_UHP: 1.314,      # sobitatud (ADACS25, 18 rehvi)
        TyreCategory.SUMMER_TOURING: 1.208,  # sobitatud (UT25)
        TyreCategory.ALL_SEASON: 1.039,      # sobitatud (ADACA25 + UT25)
        TyreCategory.WINTER_CENTRAL: 0.934,  # sobitatud (ADAC25)
        TyreCategory.WINTER_NORDIC: 0.842,   # sobitatud (TM25)
        TyreCategory.WINTER_STUDDED: 0.823,  # sobitatud
    })
    # lume ja jää baas, -5 °C
    mu_snow_base: dict = field(default_factory=lambda: {
        TyreCategory.SUMMER_UHP: 0.14,
        TyreCategory.SUMMER_TOURING: 0.15,
        TyreCategory.ALL_SEASON: 0.3925,     # sobitatud (ADACA25) - uus ankur
        TyreCategory.WINTER_CENTRAL: 0.375,  # sobitatud (ADAC25) - esimene lumeankur
        # Need kaks olid varem 0,34 ja 0,33 -- AINSAD arvud selles
        # sõnastikus ilma allikaviiteta, ehk minu enda oletused. Nad
        # ütlesid, et Põhjamaade rehv haarab lumel HALVEMINI kui
        # Kesk-Euroopa oma. See ei ole lihtsalt ebatäpne, vaid vale
        # suunaga: Põhjamaade rehv on just lume jaoks tehtud.
        # Nüüd mõõtmistest, vt anchors_snow_nordic.py.
        TyreCategory.WINTER_NORDIC: 0.377,   # sobitatud (UTAC25N, lumi -8 C)
        TyreCategory.WINTER_STUDDED: 0.345,  # sobitatud (ZR24, 4 rehvi 12-st)
    })
    mu_ice_base: dict = field(default_factory=lambda: {
        TyreCategory.SUMMER_UHP: 0.06,
        TyreCategory.SUMMER_TOURING: 0.06,
        TyreCategory.ALL_SEASON: 0.107,      # sobitatud (ADACA25), uus temp-kõveraga
        TyreCategory.WINTER_CENTRAL: 0.096,  # sobitatud (ADAC25, jää u -4 C)
        TyreCategory.WINTER_NORDIC: 0.203,   # sobitatud (TM25, jää -5 C)
        TyreCategory.WINTER_STUDDED: 0.270,  # sobitatud (TM25, jää -5 C)
    })
    # KRUUS. Lukustatud ratas kaevub kruusa sisse ja lükkab enda ette valli
    # -- see on omaette pidurdusjõud, mida asfaldil ei ole. Seetõttu on
    # kruusal ABS-iga auto pidurdusmaa PIKEM kui ABS-ita, vastupidi kõigile
    # teistele pindadele. Mõõdetud: ESV 98-S2-W-36 (6 autot, ABS sisse ja
    # välja, G-analyst: ABS väljas 0,59-0,66 g, ABS sees 0,37-0,52 g) ja
    # sõltumatult SATC 2019 (VW Polo Vivo, 40/60/80 km/h, VBox).
    # NHTSA SAE 1999-01-1287 kinnitab sama 9 autol: ABS pikendas kruusal
    # pidurdusmaad KÕIGIL üheksal, keskmiselt +25 %.
    mu_gravel_base: float = 0.694   # sobitatud [SATC19] 18 mõõtmise vastu

    # kiiruse mõju: mu(v) = mu_ref * exp(-k * (v - v_ref))     v [m/s]
    v_ref_ms: float = 22.222             # 80 km/h
    k_speed_dry: float = 0.0022
    k_speed_snow: float = 0.0035
    k_speed_ice: float = 0.0010
    # märjal: hüdrodünaamiline tõstejõud, mu /= 1 + b·(v/v_hp)²
    # sobitatud korraga kolme teadaoleva seose vastu: DEKRA mustrisügavuse
    # suhe (+17 % märjal), mu langus 40->100 km/h (24 %, kirjanduse 20-30 %)
    # ja realistlikud akvaplaneerimise lävid
    wet_lift_b: float = 1.154

    # temperatuurikäitumine: kordaja, normeeritud 1.0 juurde 20 °C juures.
    # Talverehvide külmavõitu on vähendatud teguriga 0,35, sest algne
    # kirjandusest võetud kõver ei läbinud Test Worldi tunnelitesti
    # järjestuskontrolli: seal peatub +2 °C märjal lamellrehv LÜHEMALT
    # kui nii suve- kui Kesk-Euroopa talverehv, mudel aga pani talverehvi
    # esimeseks. Vt calibrate_temp.py.
    temp_curves: dict = field(default_factory=lambda: {
        TyreCategory.SUMMER_UHP: [(-10, .52), (0, .70), (5, .81), (10, .89),
                                  (15, .95), (20, 1.00), (30, 1.02), (45, .99)],
        TyreCategory.SUMMER_TOURING: [(-10, .58), (0, .74), (5, .84), (10, .91),
                                      (15, .96), (20, 1.00), (30, 1.01), (45, .98)],
        TyreCategory.ALL_SEASON: [(-10, .84), (0, .92), (5, .95), (10, .97),
                                  (15, .99), (20, 1.00), (30, .99), (45, .94)],
        TyreCategory.WINTER_CENTRAL: [(-20, 1.025), (-10, 1.035), (0, 1.0325), (5, 1.025), (10, 1.0175), (20, 1.0), (30, 0.92), (45, 0.84)],
        TyreCategory.WINTER_NORDIC: [(-20, 1.03), (-10, 1.04), (0, 1.0375), (5, 1.0275), (10, 1.0175), (20, 1.0), (30, 0.9), (45, 0.8)],
        TyreCategory.WINTER_STUDDED: [(-20, 1.03), (-10, 1.04), (0, 1.0375), (5, 1.0275), (10, 1.0175), (20, 1.0), (30, 0.9), (45, 0.8)],
    })

    # rõhu mõju (Δp = p - p_soovitatud, bar)
    # Rõhukõver on sobitatud PASSAT-i 30 mõõdetud suhtarvu vastu (viga 1,3 %).
    # Varem oli see puhtalt kirjandusest ja ALAHINDAS optimumi ning
    # YLEHINDAS alarõhu karistust märjal ligi 30x.
    press_opt_offset_dry: float = -0.132
    press_k_dry: float = 0.0511
    press_k_wet_under: float = 0.0050    # peaaegu null: märja rõhumõju kannab v_hp
    press_k_wet_over: float = 0.0659     # sobitatud (PASSAT)
    # ABS-ita lukustub alarõhuga rehv varem ja libiseb -- rõhutundlikkus
    # on siis oluliselt suurem. [MDPI25] vs [PASSAT], vt anchors.py
    press_abs_scale: dict = field(default_factory=lambda: {
        AbsClass.NONE: 9.16, AbsClass.EARLY: 1.0,   # [MDPI25] - AINULT 1 allikas
        AbsClass.MODERN: 1.0, AbsClass.LATEST: 1.0})

    # mustrisügavus
    # (märjal käib põhimõju v_hp kaudu; siin ainult jääk)
    # KRUUSA MUSTRIMÕJU SÕLTUB SELLEST, KAS RATAS VEERLEB VÕI ON LUKUS.
    # [SATC19] mõõtis kolme mustrisügavust (7,7 / 2,9 / 1,1 mm) kolmel
    # kiirusel, ABS sees ja väljas. Suhted uue rehvi kohta:
    #
    #            ABS SEES                  ABS VÄLJAS (ratas lukus)
    #   km/h   2,9 mm   1,1 mm           2,9 mm   1,1 mm
    #     40    1,238    1,397            1,169    1,172
    #     60    1,006    1,110            1,103    1,097
    #     80    1,077    1,128            1,166    1,143
    #
    # ABS-iga kasvab kadu mustri kulumisega EDASI (1,1 mm on igal kolmel
    # kiirusel halvem kui 2,9 mm). Lukus rattaga see KÜLLASTUB: 2,9 ja
    # 1,1 mm on praktiliselt sama, kahel kiirusel kolmest on sile isegi
    # pisut PAREM. Erinevus on järjekindel kõigil kolmel kiirusel, mitte
    # ühe punkti müra.
    #
    # Mehhanism on teada ja vana. Moyer, HRB 1934, kruusa kohta:
    # "the wheels plow into the gravel as the skid progresses, thus
    # providing mechanical resistance in addition to frictional
    # resistance". Kui ratas on lukus ja kaevub, tuleb pidurdusjõud
    # kruusavallist, mitte kummi ja kivi vahelisest hõõrdest -- ja
    # vallile on ükskõik, mis muster rehvil on. ABS hoiab ratta
    # veerlemas, valli ei teki, ja siis muster JÄLLE loeb.
    # KAS SEE ON ÜLESOBITAMINE? Küllastuspunkt on lisaparameeter 18
    # ankru peal, seega küsimus on õigustatud. Leave-one-out vastab:
    #     1 parameeter (ilma küllastuseta)  LOO viga 3,83 %
    #     2 parameetrit (küllastusega)      LOO viga 3,06 %
    # Lisaparameeter parandab ENNUSTUST andmetel, mida ta ei näinud,
    # 20 %. Ülesobitamine teeks vastupidist. Kadu ise jääb mõlemal
    # harul samaks (0,148) -- erineb ainult see, kas ta küllastub.
    tread_loss_gravel: float = 0.148         # ABS: proportsionaalne
    tread_loss_gravel_locked: float = 0.148  # lukus ratas: küllastuv
    tread_gravel_sat_frac: float = 0.70      # sobitatud [SATC19] vastu
    tread_loss_wet_residual: float = 0.030
    tread_loss_dry_full: float = 0.055     # 8 -> 1.6 mm kuival

    # vanus (kummi kõvenemine)
    age_free_years: float = 5.0
    age_loss_per_year: float = 0.011
    age_loss_max: float = 0.13

    # koormustundlikkus
    load_exp: float = -0.070
    load_ref_ratio: float = 0.55

    # --- Layer 3: tee ---
    # TEEKATTE TEKSTUUR -- siin oli mudeli KUJU vale, mitte ainult arvud.
    #
    # Varem oli siin kaks sõnastikku, kaks lamedat kordajat: märjal
    # 1,09 / 1,00 / 0,88 / 0,76 ja kuival 1,02 / 1,00 / 0,96 / 0,92.
    # Audit näitas, et see liigutab vastust kuni 10 %, ja et mitte ükski
    # 369-st ankrust ei varieeri tekstuuri -- kõik on NORMAL. Ehk
    # kümneprotsendine hoob ilma ühegi mõõtmiseta.
    #
    # Kirjandusest otsides selgus, et probleem ei ole arvudes. NCHRP
    # "Guide for Pavement Friction" ütleb otse:
    #   "micro-texture influences the magnitude of tire friction, while
    #    macro-texture impacts the friction-speed gradient"
    # Ehk MAKROTEKSTUUR EI OLE TASEMEKORDAJA. Ta määrab, kui kiiresti
    # haare KIIRUSEGA langeb, sest tema ülesanne on vett ära juhtida.
    #
    # Sama ütleb PIARC-i rahvusvaheline hõõrdeindeks (IFI):
    #     F(S) = F60 * exp((60 - S) / Sp),   Sp = a + b * MPD
    # ja TRL 367 (133 katselõiku, lukustatud ratta haagis, 20-130 km/h):
    #   "Friction on surfaces with a low texture depth falls more rapidly
    #    with speed than for high-textured surfaces."
    #
    # Ja mõõdetud tõend, et lame kordaja EI SAA töötada. Jackson (FHWA
    # 2008), 10 katselõiku, sile rehv, märg, MPD 0,40-1,88 mm. Kareda ja
    # sileda katte haarde SUHE:
    #     30 mph  1,027      40 mph  1,245      50 mph  1,444
    # Üks arv ei kata seda. Ja alla 60 km/h SUHE PÖÖRDUB: kare kate on
    # seal HALVEM, sest vett ei ole vaja ära juhtida ja tegelik
    # kontaktpind on väiksem.
    #
    # POLEERITUD on hoopis teine mehhanism. Poleerimine hävitab
    # MIKROtekstuuri, makro jääb alles. Wehner/Schulze mõõtis:
    #     enne 0,431  ->  90 000 poleerimiskäigu järel 0,393  (x0,912)
    #     liivapritsiga mikrotekstuur tagasi -> 0,679  (+73 %)
    # Seega poleerimise kadu on TASEMEKADU ja ta on x0,912, mitte 0,76.
    #
    # KUIVAL: ühtegi mõõdetud kuiva hõõrde ja makrotekstuuri seost ei
    # leitud. Kõik haardestandardid (E274, SCRIM, GripTester, DFT, W/S)
    # nõuavad veekilet; kuiva lihtsalt ei mõõdeta. Seepärast on kuiv
    # makroliige nüüd TÄPSELT 1,00 -- varasemad 1,02/0,96/0,92 olid
    # välja mõeldud ja nende kaotamine ei maksa midagi, mida saaks
    # kaitsta. Kuival jääb ainult poleerituse tasemekadu.
    #
    # MPD väärtused tasemete kohta on FHWA "Pavement Friction for Road
    # Safety" tüüpvahemikest (tihe asfalt 0,40-0,80 mm, avatud
    # 0,80-1,40 mm). AUS HOIATUS: just see vastendus on OLETUS -- keegi
    # ei ole mõõtnud, mis MPD on "kulunud siledal" Eesti maanteel.
    # Kuju on tõendatud, vastendus mitte, ja seepärast lisandub
    # mitte-NORMAL tekstuuri korral sigma_texture.
    texture_mpd_mm: dict = field(default_factory=lambda: {
        Texture.COARSE_NEW: 1.40,     # avatud/uus, FHWA ülemine ots
        Texture.NORMAL: 0.70,         # tihe asfalt, keskosa = võrdluspunkt
        Texture.WORN_SMOOTH: 0.45,    # tihe asfalt, alumine ots
        Texture.POLISHED: 0.35,       # alla soovitusliku miinimumi
    })
    # mikrotekstuuri (poleerituse) tasemekadu -- kehtib NII märjal KUI kuival
    texture_micro: dict = field(default_factory=lambda: {
        Texture.COARSE_NEW: 1.000,
        Texture.NORMAL: 1.000,
        Texture.WORN_SMOOTH: 1.000,
        Texture.POLISHED: 0.912,      # Wehner/Schulze, mõõdetud
    })
    ifi_sp_a: float = 14.2               # Sp = a + b*MPD  (PIARC IFI)
    ifi_sp_b: float = 89.7
    ifi_ref_speed_kmh: float = 60.0      # IFI pöördepunkt
    # Marg betoon vs marg asfalt. Sobitatud 65 punkti peal kolmes ADAC-i
    # testis (talv / suvi / lamell). Katsetasin ka kategooriapohist jaotust
    # (talv 0,870 vs muud 0,853), aga vahe on nii vaike, et uks vaartus on
    # ausam. Dict-struktuur on alles, kui hiljem peaks vahe ilmnema.
    concrete_factor: dict = field(default_factory=lambda: {
        TyreCategory.SUMMER_UHP: 0.825,
        TyreCategory.SUMMER_TOURING: 0.825,
        TyreCategory.ALL_SEASON: 0.825,
        TyreCategory.WINTER_CENTRAL: 0.825,
        TyreCategory.WINTER_NORDIC: 0.825,
        TyreCategory.WINTER_STUDDED: 0.825,
    })
    water_k_deep: float = 0.030          # h > 1 mm  (staatiline osa)
    water_k_shallow: float = 0.055       # h < 1 mm  (niiske on parem kui märg)
    # JÄÄ JA TEMPERATUUR. Kordaja, normeeritud 1,00 juurde -5 °C juures
    # (seal on ADAC-i jääankrud). Varem oli siin lineaarne 2,1 %/°C koos
    # klambritega 0,62...1,55; see oli sobitatud kahe punkti peal, mis on
    # teineteisest 1 °C kaugusel, ehk sisuliselt müra peal.
    #
    # Kirjandus ütleb kolme asja, mida vana kuju ei kajastanud:
    #  1) Kummi ja jää hõõre EI OLE maksimumiga kõver. Kõik leitud rubber-
    #     on-ice mõõtmised (-38...-2 °C) näitavad monotoonset kasvu külma
    #     poole ilma tiputa. "Maksimum -10...-30 °C juures" tuleb kõva
    #     libiseja (uisk, suusk) kirjandusest ja rehvile ei kandu üle.
    #  2) Alla u -18...-20 °C kõver TASANDUB (Hodgkinson HRR477; Balmer
    #     TRB SR115: "below 0 F it seems to level out").
    #  3) 0 °C juures on kadu palju suurem, kui vana kuju lubas. Kandeva &
    #     Dishovsky mõõtsid -4,5 -> +0,5 °C kohta x0,55; Balmer annab
    #     välitöödest 0 °C juures mu 0,05-0,10 vs -18 °C juures 0,20-0,25.
    #
    # Kalle on võetud SÕIDUKI, mitte laboriproovi skaalalt: laborites
    # 11-14 %/K, päris autodel 3,5-6 %/K (Balmer, Martin). Vahe tuleb
    # sellest, et päris pidurduskontaktis tekib hõõrdesoojus, mis ise
    # reguleerib pinna temperatuuri. Allpool on u 5 %/K -5 °C ümbruses.
    ice_temp_curve: list = field(default_factory=lambda: [
        (2.0, 0.42), (0.0, 0.55), (-2.0, 0.72), (-5.0, 1.00),
        (-10.0, 1.32), (-15.0, 1.58), (-20.0, 1.78), (-35.0, 1.92),
    ])
    ice_temp_min: float = 0.40           # ohutusklamber, mitte mõõdetud
    ice_temp_max: float = 2.00
    # JÄÄ TEMPERATUURITUNDLIKKUS EI OLE KÕIGILE ÜKS. Ülaltoodud kõver on
    # ehitatud TAVAREHVI välitöödest (Balmer, Kandeva, Martin) -- vt
    # calibrate_ice_temp.py, kus on eraldi kirjas, et need allikad EI
    # KÄI naastrehvi ega Põhjamaade rehvi kohta. Kuni 2026-09 rakendati
    # seda ühte kõverat sellegipoolest kõigile.
    #
    # Vi Bilägare 2010 naastrehvitest mõõtis SAMA ÜHEKSA REHVI jääl
    # KAHEL temperatuuril samal päeval (-3...-2 °C ja +0,5...+1 °C).
    # See on paarismõõtmine: rehvi enda haare taandub suhtest välja.
    # Mõõdetud pidurdusmaa suhe soe/külm:
    #     naastrehv     1,23   (n=7, vahemik 1,10-1,33)
    #     hõõrdrehv     1,69   (n=2: Põhjamaa ja Kesk-Euroopa, MÕLEMAD 1,69)
    # Vana mudel andis kõigile 1,41-1,46.
    #
    # Mehhanism seletab suuna: nael lõikab jäässe MEHAANILISELT ja see ei
    # sõltu temperatuurist eriti; kummi haare sulamislähedasel jääl kukub
    # kokku veekile tõttu. Seda, et Põhjamaade ja Kesk-Euroopa rehv andsid
    # TÄPSELT sama suhte, ei ole siin oletatud -- see on mõõdetud, ja just
    # seepärast on neil ühine tegur, mitte kaks eraldi.
    #
    # Rakendus: kõver astmes KAOPOOLEL. f_kat(T) = f_alus(T) ** exp[kat],
    # kui f_alus < 1 (soojem kui -5 °C); külmal pool muutmata. Aste sobib
    # siia sellepärast, et kõver on normeeritud 1,0-le -5 °C juures, kus
    # on TÄPSELT KÕIK Põhjamaa ja naastrehvi jääankrud (7 + 7, TM25) --
    # aste ei liiguta neid seal üldse, ja ülejäänud 47 jääankrut on
    # ALL_SEASON ja WINTER_CENTRAL, mille aste jääb 1,0. Seetõttu ei
    # vaja ükski mu_ice_base järelesobitust. Vt calibrate_ice_exp.py.
    #
    # MIKS AINULT NAASTREHV SAI OMA ASTME. Hõõrdrehvi pool tuli samast
    # testist n=2 pealt ja nõuaks suhet 1,69 -- selle rakendamiseks tuleks
    # lõdvendada ohutusklambrit ice_temp_min = 0,40, mis tähendaks, et
    # sula jää vastuse annaks klamber, mitte mõõtmine. Kahe rehvi pealt
    # seda ei tehta. Number on kirjas README 7i-s ja ootab andmeid.
    ice_temp_exp: dict = field(default_factory=lambda: {
        TyreCategory.SUMMER_UHP: 1.0,
        TyreCategory.SUMMER_TOURING: 1.0,
        TyreCategory.ALL_SEASON: 1.0,
        TyreCategory.WINTER_CENTRAL: 1.0,
        TyreCategory.WINTER_NORDIC: 1.0,
        TyreCategory.WINTER_STUDDED: 0.545,   # [VIB10D] n=7, suhe 1,23
    })
    # LUMI JA TEMPERATUUR. Mudelis oli lumel temperatuurikõver PUUDU --
    # -20 °C ja -1 °C andsid täpselt sama vastuse. Jääl oli kõver olemas.
    # See asümmeetria oli kaitsmatu, aga õige parandus EI OLE jää kõvera
    # kopeerimine. Lumi käitub teisiti ja kirjandus ütleb seda selgelt:
    #
    #  * KÜLMA POOL ON VAIELDAV. FAA annab tallatud lumele -15 °C piiril
    #    astme 1,25, AGA see on TALPA töörühma KONSENSUSVÄÄRTUS, mitte
    #    mõõtmine ("based on their experience"). Päris sõidukikatse ütleb
    #    vastupidist: Lu / WSDOT mõõtis -29 °C ja 0 °C juures pickup'iga
    #    tallatud lumel, et talverehviga oli vahe NULL ja lamellrehviga oli
    #    KÜLMAS 12 % PIKEM. Seega jätame külma poole tasaseks.
    #  * TEMPERATUUR EI OLEGI PEAMINE MUUTUJA. Virginia Techi ASTM F1805
    #    regressioon: lume temperatuur seletab veojõu varieeruvusest
    #    0,7-2,2 %, lume TIHEDUS JA KÕVADUS (CTI penetromeeter) 84,6-94,8 %.
    #  * MIS 0 °C JUURES JUHTUB, ON VESI. Vaba vesi pinnakihis teeb lume
    #    libedaks, mitte termomeetri number. Transport Canada hoiatab
    #    eraldi: "-3 °C ja soojemal võib pind olla libedam kui kood näitab."
    #
    # Ja üks asi, mis seletab, MIKS meil ankruid mujalt ei ole: ASTM F1805
    # NÕUAB, et katselume temperatuur oleks -4...-15 °C. Iga sertifitseeritud
    # lumehaarde number maailmas on seega KÜLMA lume number. 0 °C lähedal ei
    # ole standardiseeritud andmeid, sest standard keelab seal katsetamise.
    #
    # Seepärast: tasane -30...-3 °C, langus alles 0 °C suunas, ja seal
    # KÕIGE LAIEM veapiir kogu mudelis (vt sigma_snow_warm).
    snow_temp_curve: list = field(default_factory=lambda: [
        (-30.0, 1.00), (-3.0, 1.00), (0.0, 0.90), (2.0, 0.84),
    ])
    snow_temp_min: float = 0.60
    snow_temp_max: float = 1.05
    # Lisaebamäärasus sula lume juures -- see on mudeli kõige nõrgem koht.
    snow_warm_from_c: float = -3.0
    sigma_snow_warm: float = 0.120

    # LAHTINE LUMI. Varem oli siin 1,12 ehk lahtine lumi oli mudelis
    # PAREM kui tallatud -- puhas oletus lumevallist, mille taga ei olnud
    # ühtegi mõõtmist.
    #
    # ÜLE KONTROLLITUD 2026-09, MÕLEMAD ALLIKAD LOETI UUESTI. Varem oli
    # siin kirjas, et "kaks sõltumatut allikat" kinnitavad 0,85. Ei
    # kinnita -- nad ei mõõda sama asja ja nad ei ole nõus:
    #
    #   FAA AC 25-31 tabel 2 (lennuk, lennurada). Sügavam kui 3 mm kuiv
    #   lumi = 0,161. Tallatud lumi = 0,161 soojemal kui -15 °C ja 0,201
    #   külmemal. Suhe on seega 1,00 SIIN, kus meie kasutaja sõidab, ja
    #   0,80 alles alla -15 °C. Meie tegur on konstantne -- ta ei järgi
    #   kumbagi otsa. Ja see koefitsient on lennunduses TAHTLIKULT ilma
    #   lume lükkamise takistuseta (AC käsitleb "contaminant drag" eraldi
    #   jaos) -- autol see takistus aeglustab ka, mis on täpselt see,
    #   miks vana 1,12 ei olnud absurdne, ainult tõendamata.
    #
    #   Ichihara & Mizoguchi (TRB SR115) tabel 1, auto pidurdus 30-40
    #   km/h: "New snow 0.2 to 0.25", "Old snow 0.25 to 0.30" -> suhe
    #   0,82. AGA see telg on lume VANUS, mitte sügavus: vana lume terad
    #   on suuremad ja purunemistakistus suurem. Sama töö ütleb tallatud
    #   lume kohta eraldi "around 0.2 to 0.3", mis KATAB uue lume vahemiku
    #   tervenisti. See allikas ei mõõda lahtist vs tallatud.
    #
    # Seega: 0,85 seisab praktikas ÜHEL auto-allikal (SR115, 0,82) ja
    # lennundusallikas ütleb siinsel temperatuuril 1,00. Number jääb --
    # auto-allikas on autole lähem -- aga ta ei ole kinnitatud, ta on
    # valitud. Kontrollitud, et sigma katab lahkarvamuse: 50 km/h, -5 °C,
    # teguriga 0,85 tuleb 34,3 m vahemikuga 27,9-40,7 m, ja FAA 1,00
    # annaks 29,6 m, mis on selle vahemiku SEES.
    #
    # Mida mudel ikka veel EI TEE: lumekihi sügavus ei ole sisend. Päris
    # vastus on sügavusest sõltuv (õhuke lahtine kiht tallatu peal on
    # libe, sügav lumi hakkab lükkamistakistusega aeglustama) ja seda
    # telge siin lihtsalt ei ole. Seepärast on selle pinna sigma kõige
    # suurem kogu mudelis.
    snow_loose_factor: float = 0.85

    # --- akvaplaneering ---
    # Horne'i valem: v_hp [km/h] = hp_c * sqrt(p [bar]) sileda rehvi ja
    # sügava vee kohta; mustri ja madalama vee peal nihkub see ülespoole.
    # Akvaplaneerimise lävi ei sõltu ainult mustri SÜGAVUSEST, vaid ka
    # mustri KUJUST. Teknikens Värld 2025 mõõtis 20 rehvi samas mõõdus
    # (235/45 R18) koos iga rehvi mustrisügavusega: Põhjamaade naelutud
    # ja naastrehvid ujuvad u 19 % varem kui Kesk-Euroopa talverehvid,
    # HOOLIMATA sellest, et nende muster on SÜGAVAM. Vt anchors_aqua.py.
    hp_category_factor: dict = field(default_factory=lambda: {
        TyreCategory.SUMMER_UHP: 1.062,
        TyreCategory.SUMMER_TOURING: 1.062,
        TyreCategory.ALL_SEASON: 1.015,
        TyreCategory.WINTER_CENTRAL: 1.000,
        TyreCategory.WINTER_NORDIC: 0.825,
        TyreCategory.WINTER_STUDDED: 0.825,
    })
    hp_c: float = 63.5
    hp_tread_gain: float = 0.085         # iga mm mustrit tõstab läve
    # LAIUS. Lai rehv peab sama ajaga rohkem vett kõrvale lükkama, nii et
    # ta ujub VAREM. Ainus leitud mõõdetud võrdlus, kus auto ja rehvimudel
    # on samad ja muutub ainult mõõt: ADAC 2018 talverehvide laiusetest
    # (VW Golf, Dunlop Winter Sport 5, Test World Ivalo, 7 mm vett) --
    # 225-sed kaotavad kontakti u 70 km/h juures, 195-sed "selgelt üle 80".
    #
    # Eksponent 1,0 on selle võrdluse KONSERVATIIVNE ots (70/80 üle
    # 195->225 annab 0,93; 1,0 annab 0,87) ja ühtlasi füüsikaliselt kõige
    # lihtsam kuju: kõrvale lükatava vee hulk ajaühikus on võrdeline
    # laiusega. Aus hoiatus: see on ÜKS allikas, mille sees muutub ka
    # profiil ja velg. Suund on kindel, suurusjärk mitte.
    hp_width_ref_mm: float = 230.0       # ankrute keskmine (225 ja 235)
    hp_width_exp: float = 1.0
    hp_water_ref_mm: float = 1.15   # kalibreeritud ADAC-tüüpi akvaplaneeringu
                                    # lävede vastu (u 110 km/h, 8 mm muster, 3 mm vett)
    mu_hydroplane: float = 0.08

    # --- Layer 4: auto ---
    abs_eff: dict = field(default_factory=lambda: {
        AbsClass.NONE: 0.74, AbsClass.EARLY: 0.88,
        AbsClass.MODERN: 0.94, AbsClass.LATEST: 0.965})
    # Kruusal on see VASTUPIDINE, vt mu_gravel_base kommentaari.
    # Lukustatud ratas = 1,00 (kogu mõõdetud 0,59-0,66 g on tema),
    # ABS kaotab sellest u veerandi.
    abs_eff_gravel: dict = field(default_factory=lambda: {
        AbsClass.NONE: 1.00, AbsClass.EARLY: 0.698,
        AbsClass.MODERN: 0.698, AbsClass.LATEST: 0.698})
    brake_buildup_s: dict = field(default_factory=lambda: {
        AbsClass.NONE: 0.35, AbsClass.EARLY: 0.28,
        AbsClass.MODERN: 0.22, AbsClass.LATEST: 0.17})
    crr: float = 0.011                   # veeretakistus

    # --- ebamäärasus (1 sigma, suhteline) ---
    sigma_base: dict = field(default_factory=lambda: {
        Surface.ASPHALT: 0.070, Surface.CONCRETE: 0.085,
        Surface.GRAVEL: 0.220, Surface.SNOW_PACKED: 0.130,
        Surface.SNOW_LOOSE: 0.180, Surface.ICE: 0.170})
    # Millises KIIRUSEVAHEMIKUS võib mudelit selle pinna peal usaldada?
    # Väljaspool seda on tulemus ekstrapolatsioon ja veapiir peab kasvama.
    #
    # Lumi ja jää: OTSESED auto pidurdusmõõtmised ulatuvad ainult 60 km/h-ni
    # (Ichihara & Mizoguchi 20-60 km/h, Chalmers AVEC'22 35 ja 55 km/h).
    # AGA kolm sõltumatut mõõtmistraditsiooni ütlevad, et haare on nendel
    # pindadel kiirusest praktiliselt SÕLTUMATU:
    #   - Chalmers, päris auto ABS-pidurdustega: dmu = -0,02...+0,02
    #     35 ja 55 km/h vahel, märgi kohta järjekindlust ei ole
    #   - Ichihara & Mizoguchi, 3 rehvitüüpi, 20-60 km/h: "does not change
    #     much with increasing speed... completely different from wet"
    #   - FAA/NASA lennuraja mõõteseadmed 32-95 km/h tallatud lumel ja
    #     jääl: "speed effect is negligible"; FAA 1995 ütleb otse, et
    #     lava on ~37 km/h kuni ~185 km/h
    # Seetõttu on ülempiir tõstetud 80 km/h-ni. See EI ole "meil on
    # ankrud 80 km/h-ni", vaid "meil on kolm sõltumatut tõendit, et
    # nende kahe vahel midagi ei juhtu". Üle 80 km/h läheb veapiir laiaks.
    #
    # Kruus: SATC 2019 mõõtis 40, 60 ja 80 km/h, seega päris vahemik.
    speed_range: dict = field(default_factory=lambda: {
        Surface.ASPHALT: (40.0, 130.0),
        Surface.CONCRETE: (40.0, 120.0),
        Surface.SNOW_PACKED: (15.0, 80.0),
        Surface.SNOW_LOOSE: (15.0, 60.0),   # lahtisel lumel ankruid ei ole
        Surface.ICE: (15.0, 80.0),
        Surface.GRAVEL: (40.0, 80.0),
    })
    sigma_speed_extrap: float = 0.25     # lisandub (kiirus/lubatud - 1) kohta
    sigma_speed_extrap_max: float = 0.40
    sigma_wet_extra: float = 0.020
    sigma_label_only: float = 0.045      # kui G tuleb ainult märgise klassist
    # MÕÕDU MITTEVASTAVUS. Märghaardumise indeks G on MÕÕDUPÕHINE: sama
    # rehvimudel võib olla ühes mõõdus A ja teises B. Kui kasutame 225/40 R18
    # peal mõõdetud G-d autol, mille tehasemõõt on 175/70 R13, siis on see
    # ülekanne, mitte mõõtmine -- ja veapiir peab seda tunnistama.
    # HOIATUS: see kordaja EI OLE ankrute vastu sobitatud, sest ankruid
    # sama rehvi kohta eri mõõtudes ei ole. See on hinnang, mis lähtub
    # sellest, et klassivahetus mõõtude vahel tähendab u 10 % pidurdusmaas.
    sigma_size_rim_inch: float = 0.015   # veljediameetri tolli kohta
    sigma_size_max: float = 0.080
    size_warn_inch: float = 2.0          # sellest alates ütle ka sõnadega
    sigma_extrapolation: float = 0.060   # kui väljaspool valideeritud ala
    # ÜHE ALLIKA LUMI. Kesk-Euroopa talverehvi ja lamellrehvi lumebaas
    # tuleb kahest ADAC-i testist, kokku 47 mõõtmisest. Põhjamaade
    # naelutu ja naastrehvi oma tuleb ÜHEST testist kummalgi -- 5 ja 4
    # mõõtmist, eri autod, eri kohad, üks neist sisehallis. Sama
    # pinnanimi, aga tõenduse kaal erineb kümnekordselt. Veapiir peab
    # seda ütlema, muidu näeb kasutaja kaht ühesugust "±13 %", mille
    # taga on täiesti eri hulk tööd.
    # Suurus: testisisene hajuvus oli naelutul 4 % ja naastul 6 %, ning
    # absoluuttaset ei kinnita kummalgi miski teine. 6 % on sellest
    # konservatiivne ots, mitte sobitatud arv.
    sigma_snow_single_source: float = 0.060
    # TEKSTUUR. Kuju on tõendatud (NCHRP, PIARC IFI, TRL 367), aga
    # vastendus "kulunud sile" -> MPD 0,45 mm on OLETUS: keegi ei ole
    # mõõtnud, mis MPD on selle nimega Eesti teel. Lisaks on Jacksoni
    # mõõtmistes näha, et tekstuuri mõju on SILEDA rehviga suur ja
    # mustriga rehviga väike -- muster teeb sama tööd mis makrotekstuur.
    # Mudelis on mustril oma liige, seega need kaks on osaliselt
    # kollineaarsed. Mõlemat piirangut kannab see lisand.
    sigma_texture: float = 0.070


DEFAULT_CAL = Calibration()


# ---------------------------------------------------------------------------
# Abifunktsioonid
# ---------------------------------------------------------------------------

def parse_size(size: str) -> Optional[tuple]:
    """Rehvimõõt "225/40 R18" või "165/70R13" -> (laius_mm, profiil, velg_toll).

    Tagastab None, kui ei õnnestu -- kutsuja peab sellega arvestama, sest
    kõigil rehvidel ja autodel ei ole mõõtu teada."""
    if not size:
        return None
    m = re.match(r"\s*(\d{3})\s*/\s*(\d{2})\s*R?\s*(\d{2})", size)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def size_gap_inch(tyre_size: str, oem_size: str) -> float:
    """Kui kaugel on rehvi testimõõt auto tehasemõõdust, tollides.
    0.0 tähendab kas kokkulangevust või seda, et üht neist ei tea."""
    a, b = parse_size(tyre_size), parse_size(oem_size)
    if not a or not b:
        return 0.0
    return abs(a[2] - b[2])


def _interp(points: Sequence[tuple], x: float) -> float:
    """Lineaarne interpolatsioon (ekstrapoleerib äärmistel lõikudel)."""
    pts = sorted(points)
    if x <= pts[0][0]:
        (x0, y0), (x1, y1) = pts[0], pts[1]
    elif x >= pts[-1][0]:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
    else:
        for i in range(len(pts) - 1):
            if pts[i][0] <= x <= pts[i + 1][0]:
                (x0, y0), (x1, y1) = pts[i], pts[i + 1]
                break
    if x1 == x0:
        return y0
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


# ---------------------------------------------------------------------------
# Tulemus
# ---------------------------------------------------------------------------

@dataclass
class Result:
    distance_m: float                # ainult pidurdusmaa (kiirusest 0-ni)
    total_distance_m: float          # peatumistee = reaktsioonitee + pidurdusmaa
    reaction_m: float                # reaktsioonitee = v0 * reaktsiooniaeg
    sigma_rel: float                 # suhteline 1-sigma
    # NB: vahemik kaib PEATUMISTEE umber, mitte pidurdusmaa umber.
    # Reaktsioonitee ise on maaramatuseta (puhas korrutis v0 * t_react),
    # aga kasutajale naidatav number on peatumistee, nii et vahemik peab
    # kaima sama suuruse umber. Kui vordled mudeli sisemisi asju, vordle
    # distance_m -- kui naitad kasutajale, naita total_distance_m.
    low_m: float                     # ~68% vahemik peatumistee umber
    high_m: float
    mu_effective: float              # keskmine ärakasutatud haardetegur
    peak_decel_g: float
    time_s: float
    hydroplane_speed_kmh: Optional[float]
    hydroplane_risk: float           # 0..1
    limiter: str                     # "rehv" voi "pidurid" -- kumb piirab
    confidence: str                  # "kõrge" / "keskmine" / "madal"
    warnings: list
    # -- reaalsuse kontroll: sama haare piirab ka kiirendamist -----------
    accel_time_s: float = 0.0        # parim voimalik 0 -> v0 aeg samal pinnal
    accel_dist_m: float = 0.0        # ja selleks kuluv maa
    accel_reachable: bool = True     # kas see kiirus on seal ulepea saavutatav
    extreme: bool = False            # kas tulemus on fuusika aarmus

    def __str__(self) -> str:
        s = (f"{self.total_distance_m:.1f} m  "
             f"(±{(self.high_m - self.low_m) / 2:.1f} m, "
             f"{self.low_m:.1f}–{self.high_m:.1f} m)\n"
             f"  = reaktsioonitee {self.reaction_m:.1f} m "
             f"+ pidurdusmaa {self.distance_m:.1f} m\n"
             f"  keskmine haardetegur μ = {self.mu_effective:.2f}, "
             f"aeglustus kuni {self.peak_decel_g:.2f} g, kestus {self.time_s:.1f} s\n"
             f"  piiraja: {self.limiter}\n"
             f"  usaldus: {self.confidence}")
        for w in self.warnings:
            s += f"\n  ⚠ {w}"
        return s


# ---------------------------------------------------------------------------
# Mootor
# ---------------------------------------------------------------------------

class BrakingModel:
    def __init__(self, cal: Calibration = DEFAULT_CAL, dt: float = 0.004):
        self.cal = cal
        self.dt = dt   # integreerimissamm, s

    # -- Layer 2+3: haardetegur antud hetkkiirusel -----------------------

    def mu_at_speed(self, tyre: Tyre, veh: Vehicle, cond: Conditions,
                    v_ms: float) -> float:
        cal = self.cal
        surf = cond.surface
        wet = surf in (Surface.ASPHALT, Surface.CONCRETE) and cond.water_mm > 0.02

        # --- baashaare -------------------------------------------------
        if surf in (Surface.ASPHALT, Surface.CONCRETE):
            if wet:
                mu = cal.k_g * tyre.wet_grip_index
            else:
                mu = (tyre.mu_dry_override
                      if tyre.mu_dry_override is not None
                      else cal.mu_dry_base[tyre.category])
            if surf is Surface.CONCRETE:
                mu *= cal.concrete_factor[tyre.category]
        elif surf in (Surface.SNOW_PACKED, Surface.SNOW_LOOSE):
            mu = (tyre.mu_snow_override
                  if tyre.mu_snow_override is not None
                  else cal.mu_snow_base[tyre.category])
            if surf is Surface.SNOW_LOOSE:
                mu *= cal.snow_loose_factor
            mu *= _clamp(_interp(cal.snow_temp_curve, cond.temp_c),
                         cal.snow_temp_min, cal.snow_temp_max)
        elif surf is Surface.ICE:
            mu = (tyre.mu_ice_override
                  if tyre.mu_ice_override is not None
                  else cal.mu_ice_base[tyre.category])
            # _interp ekstrapoleerib äärmistel lõikudel, jää aga ei muutu
            # enam +2 °C juures libedamaks (ta on siis vesi) ega -35 °C
            # juures lõputult krabisemaks -- klamber hoiab kuju paigas.
            # Kategooria tundlikkus astmena -- vt ice_temp_exp. Aste mõjub
            # AINULT KAOPOOLEL (f < 1, ehk soojemal kui -5 °C). Külmal
            # pool jääb kirjanduse kõver puutumata, sest mõõdetud tõend
            # (-2,5...+0,75 °C) ei ulatu sinna ja aste paisutaks külma
            # otsa klambrini välja -- see tähendaks, et -20 °C vastuse
            # annab ohutusklamber, mitte mõõtmine.
            f_ice = _interp(cal.ice_temp_curve, cond.temp_c)
            e_ice = cal.ice_temp_exp.get(tyre.category, 1.0)
            if e_ice != 1.0 and 0.0 < f_ice < 1.0:
                f_ice = f_ice ** e_ice
            mu *= _clamp(f_ice, cal.ice_temp_min, cal.ice_temp_max)
        else:  # kruus
            mu = cal.mu_gravel_base

        # --- temperatuur (asfaldil; lumel/jääl on see juba sees) --------
        if surf in (Surface.ASPHALT, Surface.CONCRETE):
            mu *= _interp(cal.temp_curves[tyre.category], cond.temp_c)

        # --- katte tekstuur --------------------------------------------
        # Kaks ERI mehhanismi, mitte üks kordaja. Vt Calibration.
        #   MAKRO (vee äravool) -> kiiruse gradient, AINULT märjal.
        #   MIKRO (poleeritus)  -> taseme kadu, märjal ja kuival.
        # NORMAL annab makroliikmeks täpselt 1,000 igal kiirusel, sest
        # ta ongi võrdluspunkt -- nii ei muuda see ümberehitus ühtegi
        # 369-st ankrust, mis kõik on NORMAL. Seda kontrollib audit.
        if surf in (Surface.ASPHALT, Surface.CONCRETE):
            mu *= cal.texture_micro[cond.texture]
            if wet:
                v_kmh = v_ms * 3.6
                sp_t = cal.ifi_sp_a + cal.ifi_sp_b * cal.texture_mpd_mm[cond.texture]
                sp_r = cal.ifi_sp_a + cal.ifi_sp_b * cal.texture_mpd_mm[Texture.NORMAL]
                d = cal.ifi_ref_speed_kmh - v_kmh
                mu *= math.exp(d / sp_t - d / sp_r)

        # --- veekile paksus (staatiline osa, väike) ---------------------
        if wet:
            h = cond.water_mm
            if h >= 1.0:
                mu *= 1.0 / (1.0 + cal.water_k_deep * (h - 1.0))
            else:
                mu *= 1.0 + cal.water_k_shallow * (1.0 - h)

        # --- kiirus ------------------------------------------------------
        # MÄRJAL: kiiruse, veekile paksuse, mustrisügavuse ja rehvirõhu
        # ühismõju käib ÜHE hüdrodünaamilise liikme kaudu. Rehvi ette
        # kogunev vesi tekitab tõstejõu, mis on võrdeline v² ja pöördvõrdeline
        # rehvi veeärajuhtimise võimega. Viimane on täpselt see, mida
        # akvaplaneerimiskiirus v_hp kirjeldab. Seega:
        #
        #     mu(v) = mu_staatiline / (1 + b · (v / v_hp)²)
        #
        # See asendab varasema eraldi "kiiruse exp" + "mustri kadu" +
        # "veekile kadu" kolmiku, mis topeltarvestas sama füüsikat ja
        # andis absurdse tulemuse, kus sügavam vesi madalal kiirusel
        # oleks olnud parem kui õhuke.
        if wet:
            v_hp_ms = self.hydroplane_speed_kmh(tyre, veh, cond) / 3.6
            mu /= 1.0 + cal.wet_lift_b * (v_ms / v_hp_ms) ** 2
            k = 0.0
        elif surf in (Surface.ASPHALT, Surface.CONCRETE):
            k = cal.k_speed_dry
        elif surf is Surface.ICE:
            k = cal.k_speed_ice
        elif surf in (Surface.SNOW_PACKED, Surface.SNOW_LOOSE):
            k = cal.k_speed_snow
        else:
            k = cal.k_speed_dry
        mu *= math.exp(-k * (v_ms - cal.v_ref_ms))

        # --- mustrisügavus ----------------------------------------------
        td, td_new = tyre.tread_depth_mm, tyre.tread_depth_new_mm
        worn_frac = _clamp((td_new - td) / max(0.1, td_new - 1.0), 0.0, 1.0)
        if wet:
            # Märjal käib mustrisügavus juba v_hp kaudu (vt ülal) -- siia
            # jääb ainult väike jääkmõju (kulunud rehvi kontaktpind ja
            # lamellide vähenemine), mis ei ole veeärajuhtimine.
            mu *= 1.0 - cal.tread_loss_wet_residual * worn_frac
        elif surf in (Surface.ASPHALT, Surface.CONCRETE):
            mu *= (1.0 - cal.tread_loss_dry_full * worn_frac)
        elif surf in (Surface.SNOW_PACKED, Surface.SNOW_LOOSE):
            mu *= (1.0 - 0.30 * worn_frac)     # lumel on muster kõige tähtsam
        elif surf is Surface.ICE:
            mu *= (1.0 - 0.15 * worn_frac)
        elif surf is Surface.GRAVEL:
            # Kruusal on mustri mõju OLEMAS, aga väiksem kui asfaldil:
            # [SATC19] mõõtis uue (7,7 mm), kulunud (2,9 mm) ja sileda
            # (1,1 mm) rehviga, kolmel kiirusel, ABS sees ja väljas --
            # uuelt siledale kasvas pidurdusmaa u 13 %.
            # vt Calibration.tread_loss_gravel* -- lukus ratas kaevub ja
            # mustri mõju küllastub, ABS-iga ratas veerleb ja muster loeb
            if veh.abs_class is AbsClass.NONE:
                f = min(worn_frac / max(1e-6, cal.tread_gravel_sat_frac), 1.0)
                mu *= (1.0 - cal.tread_loss_gravel_locked * f)
            else:
                mu *= (1.0 - cal.tread_loss_gravel * worn_frac)

        # --- rehvirõhk ---------------------------------------------------
        p = tyre.pressure_bar if tyre.pressure_bar is not None else veh.recommended_pressure_bar
        dp = p - veh.recommended_pressure_bar
        scale = cal.press_abs_scale.get(veh.abs_class, 1.0)
        if wet:
            k_p = cal.press_k_wet_under if dp < 0 else cal.press_k_wet_over
            mu *= _clamp(1.0 - scale * k_p * dp * dp, 0.45, 1.02)
        else:
            d = dp - cal.press_opt_offset_dry
            mu *= _clamp(1.0 - scale * cal.press_k_dry * d * d, 0.45, 1.02)

        # --- vanus -------------------------------------------------------
        over = max(0.0, tyre.age_years - cal.age_free_years)
        mu *= 1.0 - min(cal.age_loss_max, cal.age_loss_per_year * over)

        # --- koormustundlikkus -------------------------------------------
        mass = veh.kerb_mass_kg + cond.payload_kg
        load_per_tyre = mass / 4.0
        cap = tyre.load_capacity_kg or (veh.kerb_mass_kg / 4.0 / cal.load_ref_ratio)
        ratio = load_per_tyre / cap
        mu *= (ratio / cal.load_ref_ratio) ** cal.load_exp

        # --- akvaplaneering ----------------------------------------------
        if wet:
            v_hp = self.hydroplane_speed_kmh(tyre, veh, cond)
            v_kmh = v_ms * 3.6
            if v_hp and v_kmh > 0.72 * v_hp:
                # sujuv üleminek: 0.72*v_hp juures 0, v_hp juures täielik
                t = _clamp((v_kmh - 0.72 * v_hp) / (0.28 * v_hp), 0.0, 1.0)
                blend = t * t                      # ruutkõver, mitte lineaarne
                mu = mu * (1.0 - blend) + cal.mu_hydroplane * blend

        return max(0.03, mu)

    # -- akvaplaneerimiskiirus -------------------------------------------

    def hydroplane_speed_kmh(self, tyre: Tyre, veh: Vehicle,
                             cond: Conditions) -> Optional[float]:
        """Horne'i valem, kohandatud mustrisügavuse ja veekile paksusega."""
        if cond.surface not in (Surface.ASPHALT, Surface.CONCRETE):
            return None
        if cond.water_mm <= 0.02:
            return None
        cal = self.cal
        p = tyre.pressure_bar if tyre.pressure_bar is not None else veh.recommended_pressure_bar
        v = cal.hp_c * math.sqrt(max(0.5, p))
        # muster juhib vett ära -> lävi tõuseb
        v *= 1.0 + cal.hp_tread_gain * tyre.tread_depth_mm
        v *= cal.hp_category_factor[tyre.category]
        v *= tyre.hp_factor
        # lai rehv ujub varem (vt hp_width_exp)
        sz = parse_size(tyre.size)
        if sz:
            v *= (cal.hp_width_ref_mm / sz[0]) ** cal.hp_width_exp
        # õhuke veekile -> lävi tõuseb järsult
        v *= (cal.hp_water_ref_mm / max(0.15, cond.water_mm)) ** 0.42
        return v

    # -- Layer 1 + 4: integreerimine --------------------------------------

    def stopping_distance(self, tyre: Tyre, veh: Vehicle,
                          cond: Conditions) -> Result:
        cal = self.cal
        warnings: list = []
        v0 = cond.speed_kmh / 3.6
        mass = veh.kerb_mass_kg + cond.payload_kg
        slope_a = G_ACC * math.sin(math.atan(cond.gradient_pct / 100.0))

        # Kruusal on ABS-i mõju vastupidine (vt abs_eff_gravel).
        eta = (cal.abs_eff_gravel if cond.surface is Surface.GRAVEL
               else cal.abs_eff)[veh.abs_class]
        t_build = cal.brake_buildup_s[veh.abs_class]

        dt = self.dt
        v = v0
        s = 0.0
        t = 0.0
        peak_a = 0.0
        mu_sum = 0.0
        mu_n = 0
        brake_limited_steps = 0

        while v > 0.05 and t < 60.0:
            mu = self.mu_at_speed(tyre, veh, cond, v)
            mu_sum += mu
            mu_n += 1

            # pidurite ülesehitusaeg: aeglustus kasvab lineaarselt
            ramp = _clamp(t / t_build, 0.0, 1.0) if t_build > 0 else 1.0

            a_tyre = mu * G_ACC * eta
            # pidurite lagi -- kui see jääb rehvi omast allapoole, siis
            # ei piira pidurdusmaad enam rehv, vaid pidur
            a_brake_max = veh.brake_capacity_g * cond.brake_condition * G_ACC
            if a_brake_max < a_tyre:
                brake_limited_steps += 1
            a_tyre = min(a_tyre, a_brake_max)
            a_aero = 0.5 * RHO_AIR * veh.cda_m2 * v * v / mass
            a_roll = cal.crr * G_ACC
            a = a_tyre * ramp + a_aero + a_roll + slope_a
            a = max(0.05, a)
            peak_a = max(peak_a, a)

            v -= a * dt
            s += max(0.0, v) * dt
            t += dt

        mu_eff = mu_sum / max(1, mu_n)
        s_react = v0 * cond.reaction_time_s

        # --- ebamäärasus ---------------------------------------------------
        sigma = cal.sigma_base[cond.surface]
        if cond.surface in (Surface.ASPHALT, Surface.CONCRETE) and cond.water_mm > 0.02:
            sigma = math.hypot(sigma, cal.sigma_wet_extra)
        # Märgise ebamäärasus AINULT nendele rehvidele, mille G tuleb
        # klassi keskpunktist. Varem lisati see kõigile, ka nendele 91-le,
        # mille G on päris testist tuletatud -- see oli viga ja tegi
        # testitud rehvide veapiiri asjatult laiaks.
        if tyre.g_source != "test":
            sigma = math.hypot(sigma, cal.sigma_label_only)

        # Lumi, mille kategooria taga on ainult üks test. Vt
        # sigma_snow_single_source ja anchors_snow_nordic.py.
        if cond.surface in (Surface.SNOW_PACKED, Surface.SNOW_LOOSE) \
                and tyre.category in (TyreCategory.WINTER_NORDIC,
                                      TyreCategory.WINTER_STUDDED):
            sigma = math.hypot(sigma, cal.sigma_snow_single_source)

        # Tekstuur: ükski ankur ei varieeri seda, vt sigma_texture.
        if cond.texture is not Texture.NORMAL and \
                cond.surface in (Surface.ASPHALT, Surface.CONCRETE):
            sigma = math.hypot(sigma, cal.sigma_texture)

        # Sula lumi: mudeli kõige nõrgem koht, sest temperatuur on siin
        # ainult ASENDUSNÄITAJA vaba vee jaoks pinnakihis.
        if cond.surface in (Surface.SNOW_PACKED, Surface.SNOW_LOOSE) \
                and cond.temp_c > cal.snow_warm_from_c:
            ramp = _clamp((cond.temp_c - cal.snow_warm_from_c) / 3.0, 0.0, 1.0)
            sigma = math.hypot(sigma, cal.sigma_snow_warm * ramp)
            warnings.append(
                "Lumi nulli lähedal on mudeli kõige ebakindlam koht. Haaret ei "
                "määra siin mitte termomeeter, vaid see, kas pinnakihis on "
                "vaba vett — ja seda kalkulaator ei küsi. Kuiv tallatud lumi "
                "-1 °C juures ja sama lumi päikese käes sulamas erinevad "
                "rohkem kui kogu see temperatuurikõver.")

        # Rehvi mõõt vs auto tehasemõõt
        gap = size_gap_inch(tyre.size, veh.oem_size)
        if gap > 0.0:
            sigma = math.hypot(sigma, min(cal.sigma_size_rim_inch * gap,
                                          cal.sigma_size_max))
            if gap >= cal.size_warn_inch:
                warnings.append(
                    f"Rehvi andmed on mõõdust {tyre.size}, auto tehasemõõt on "
                    f"{veh.oem_size} — {gap:.0f} tolli vahet. Märghaardumise "
                    "klass on mõõdupõhine, nii et see on ülekanne teiselt "
                    "mõõdult, mitte selle mõõdu mõõtmine. Kontrolli ka, kas "
                    "see rehv sellele autole üldse sobib.")

        if (cond.temp_c < -25 or cond.temp_c > 45 or cond.water_mm > 5.0):
            sigma = math.hypot(sigma, cal.sigma_extrapolation)
            warnings.append("Temperatuur või veekile on väljaspool valideeritud "
                            "vahemikku — tulemus on ekstrapolatsioon.")

        # kiirus väljaspool selle pinna ankruvahemikku
        lo_v, hi_v = cal.speed_range[cond.surface]
        if hi_v <= 0:
            sigma = math.hypot(sigma, cal.sigma_extrapolation)
        elif cond.speed_kmh > hi_v:
            f = cond.speed_kmh / hi_v
            sigma = math.hypot(sigma, min(cal.sigma_speed_extrap * (f - 1.0),
                                          cal.sigma_speed_extrap_max))
            warnings.append(
                f"{cond.speed_kmh:.0f} km/h on sellel pinnal ekstrapolatsioon: "
                f"mudeli mõõdetud ankrud ulatuvad {hi_v:.0f} km/h-ni. "
                f"Pidurdusmaa kasvab kiiruse RUUDUS, nii et viga kasvab kiiresti.")
        elif cond.speed_kmh < lo_v:
            sigma = math.hypot(sigma, cal.sigma_speed_extrap * (lo_v / max(1.0, cond.speed_kmh) - 1.0))

        # akvaplaneering
        v_hp = self.hydroplane_speed_kmh(tyre, veh, cond)
        hp_risk = 0.0
        if v_hp:
            hp_risk = _clamp((cond.speed_kmh - 0.72 * v_hp) / (0.28 * v_hp), 0.0, 1.0)
            if hp_risk > 0.05:
                sigma = math.hypot(sigma, 0.10 + 0.25 * hp_risk)
            if hp_risk > 0.5:
                warnings.append(
                    f"Akvaplaneerimise oht: hinnanguline lävi ~{v_hp:.0f} km/h. "
                    "Sellises olukorras pole pidurdusmaa enam usaldusväärselt ennustatav.")
            elif hp_risk > 0.05:
                warnings.append(
                    f"Lähened akvaplaneerimise lävele (~{v_hp:.0f} km/h).")

        # tervemõistuse kontrollid
        if tyre.category in (TyreCategory.SUMMER_UHP, TyreCategory.SUMMER_TOURING) \
                and cond.temp_c < 7:
            warnings.append("Suverehv alla +7 °C: kummisegu on kõva, "
                            "haare langeb kiiresti.")
        if cond.surface in (Surface.ICE, Surface.SNOW_PACKED, Surface.SNOW_LOOSE) \
                and tyre.category in (TyreCategory.SUMMER_UHP, TyreCategory.SUMMER_TOURING):
            warnings.append("Suverehv lumel/jääl — tulemus on orienteeruv ja "
                            "reaalne käitumine on ettearvamatu.")
        if tyre.tread_depth_mm < 1.6:
            warnings.append("Mustrisügavus alla seadusliku 1,6 mm.")

        # tervemõistuse kontroll: kas see on üldse sõidetav olukord?
        # Sama haare, mis piirab pidurdamist, piirab ka kiirendamist.
        acc_t, acc_s, acc_ok = self.accel_to_speed(tyre, veh, cond)
        extreme = (s > 150.0) or (not acc_ok) or (acc_s > 400.0)
        if s > 150.0:
            warnings.append(
                f"Füüsika äärmus: {s:.0f} m on pikem kui nähtavus enamikul teedel. "
                "Number on matemaatiliselt õige — pidurdusmaa kasvab kiiruse "
                "ruudus — aga see kirjeldab pigem suletud ala või jäärada kui "
                "tavalist liiklust.")
        if not acc_ok:
            warnings.append(
                f"Sellel pinnal ei jõuaks auto {cond.speed_kmh:.0f} km/h-ni ka siis, "
                "kui kogu rehvi haare läheks veole: ratas kaotaks haarde enne. "
                "Sama haare, mis piirab pidurdamist, piirab ka kiirendamist.")
        elif acc_s > 400.0:
            warnings.append(
                f"Hoovõtt: {cond.speed_kmh:.0f} km/h-ni jõudmine võtaks sellel pinnal "
                f"parimal juhul {acc_t:.0f} s ja {acc_s:.0f} m. Tavateel sellist "
                "hoovõtumaad ei ole, pikal jäärajasirgel on.")

        # kumb piirab: rehv voi pidur?
        brake_frac = brake_limited_steps / max(1, mu_n)
        if brake_frac > 0.5:
            limiter = "pidurid"
            warnings.append(
                "Pidurid ei suuda rehvi haaret ära kasutada — piirajaks on "
                "pidurisüsteem, mitte rehv. Parem rehv siin ei aitaks.")
        elif brake_frac > 0.05:
            limiter = "rehv (osaliselt pidurid)"
        else:
            limiter = "rehv"

        if sigma <= 0.10:
            conf = "kõrge"
        elif sigma <= 0.16:
            conf = "keskmine"
        else:
            conf = "madal"

        # USALDUSE LAGI: ULEKANNE EI OLE MOOTMINE.
        # Kui rehvi haardenumber tuleb TEISEST modust kui auto tehasemodu,
        # siis ei ole see selle modu mootmine vaid ulekanne. Sigma kasvab
        # sellest kull (sigma_size_rim_inch), aga see konstant on registris
        # ise margitud "ei ole ankrute vastu sobitatud -- sama rehvi
        # motmisi eri modus ei ole olemas". Ehk taht "korge" tuleks
        # valideerimata liikme pealt.
        # Seeparast on siin LAGI, mitte uus fuusikakonstant: number ise ei
        # muutu uhtegi sentimeetrit, muutub ainult see, kui enesekindlalt
        # leht tohib raakida. Kasutaja leidis selle ules: vana Passat
        # (195/65 R15) sai 225/45 R17 rehvi numbri ja korval seisis
        # "usaldus korge".
        if gap >= cal.size_warn_inch and conf == "kõrge":
            conf = "keskmine"

        # SAMA LAGI MARGISELT TULNUD G-le.
        # Kui G tuleb margise KLASSIST, siis ei kirjelda see arv MITTE
        # SEDA rehvi vaid tervet klassi: koik 35 A-klassi rehvi selles
        # modus annavad tapselt sama vastuse. Sigma kasvab sellest kull
        # (sigma_label_only), aga taht "korge" jataks mulje, et mudel
        # teab selle konkreetse rehvi kohta midagi. Ta ei tea.
        if tyre.g_source != "test" and conf == "kõrge":
            conf = "keskmine"

        return Result(
            distance_m=s,
            total_distance_m=s + s_react,
            reaction_m=s_react,
            sigma_rel=sigma,
            low_m=(s + s_react) * (1 - sigma),
            high_m=(s + s_react) * (1 + sigma),
            mu_effective=mu_eff,
            peak_decel_g=peak_a / G_ACC,
            time_s=t + cond.reaction_time_s,
            hydroplane_speed_kmh=v_hp,
            hydroplane_risk=hp_risk,
            limiter=limiter,
            confidence=conf,
            warnings=warnings,
            accel_time_s=acc_t,
            accel_dist_m=acc_s,
            accel_reachable=acc_ok,
            extreme=extreme,
        )

    def accel_to_speed(self, tyre: Tyre, veh: Vehicle,
                       cond: Conditions) -> tuple:
        """Parim voimalik kiirendus 0 -> v0 SAMAL pinnal.

        Eeldab, et kogu rehvi haare laheb veole (nagu oleks nelikvedu ja
        piiramatu mootor) ega arvesta ohutakistust. See on seega ALAHINNANG:
        paris auto on aeglasem. Motte on lihtne -- kui isegi see parim juhus
        annab absurdse aja voi maa, siis seda kiirust sellel pinnal ei teki
        ja pidurdusmaa number on puhas fuusika, mitte liiklusolukord."""
        v_target = cond.speed_kmh / 3.6
        if v_target <= 0.05:
            return 0.0, 0.0, True
        dt = self.dt
        v = 0.0
        s = 0.0
        t = 0.0
        while v < v_target and t < 300.0:
            mu = self.mu_at_speed(tyre, veh, cond, max(v, 1.0))
            a = max(0.02, mu * G_ACC)
            v += a * dt
            s += v * dt
            t += dt
        return t, s, v >= v_target - 1e-6

    # -- mugavusfunktsioonid ---------------------------------------------

    def distance_between(self, tyre: Tyre, veh: Vehicle, cond: Conditions,
                         v_from_kmh: float, v_to_kmh: float) -> float:
        """Pidurdusmaa kiiruselt A kiiruseni B (testiprotokollide jaoks,
        nt 100 -> 5 km/h või 80 -> 20 km/h)."""
        if v_to_kmh <= 0.05:
            return self.stopping_distance(
                tyre, veh, replace(cond, speed_kmh=v_from_kmh)).distance_m
        cal = self.cal
        v0 = v_from_kmh / 3.6
        v_end = v_to_kmh / 3.6
        mass = veh.kerb_mass_kg + cond.payload_kg
        slope_a = G_ACC * math.sin(math.atan(cond.gradient_pct / 100.0))
        # Kruusal on ABS-i mõju vastupidine (vt abs_eff_gravel).
        eta = (cal.abs_eff_gravel if cond.surface is Surface.GRAVEL
               else cal.abs_eff)[veh.abs_class]
        t_build = cal.brake_buildup_s[veh.abs_class]
        dt, v, s, t = self.dt, v0, 0.0, 0.0
        while v > v_end and t < 60.0:
            mu = self.mu_at_speed(tyre, veh, replace(cond, speed_kmh=v_from_kmh), v)
            ramp = _clamp(t / t_build, 0.0, 1.0) if t_build > 0 else 1.0
            a_tyre = min(mu * G_ACC * eta,
                         veh.brake_capacity_g * cond.brake_condition * G_ACC)
            a = a_tyre * ramp + 0.5 * RHO_AIR * veh.cda_m2 * v * v / mass \
                + cal.crr * G_ACC + slope_a
            a = max(0.05, a)
            v -= a * dt
            s += max(0.0, v) * dt
            t += dt
        return s

    def compare_tyres(self, tyres: Sequence[Tyre], veh: Vehicle,
                      cond: Conditions) -> list:
        """Rehvide pingerida antud olukorras."""
        rows = []
        for ty in tyres:
            r = self.stopping_distance(ty, veh, cond)
            rows.append((ty, r))
        rows.sort(key=lambda x: x[1].distance_m)
        return rows
