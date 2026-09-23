"""
EPREL-i adapter.

EPREL on EL-i energiamärgise tooteregister. Iga Euroopas müüdav rehv peab
alates 2021. maist seal olema. See on ainus koht, kus on IGA rehvi
märghaardumise klass -- seega ainus tee sellest, et kalkulaatoris on 91
testitud rehvi, sinna, et seal on kõik rehvid, mida keegi osta saab.

MIDA EPREL ANNAB JA MIDA MITTE
------------------------------
Annab:      märghaardumise KLASS (A-E), mõõt, tootja, mudeli nimi,
            koormus- ja kiirusindeks, kütuseklass, müra, 3PMSF ja jäämärgis
EI anna:    numbrilist G-indeksit. Kontrollitud: tooteinfo lehel on
            "Wet grip class D" ja numbrit ei ole.
EI anna:    kuivhaardumist ega lume/jää pidurdusmaad -- märgis neid ei kata

Sellest tuleneb kogu HÜBRIIDI mõte, vt g_from_class() allpool.

API
---
Baas:       https://eprel.ec.europa.eu/
Detailvaade GET /api/products/tyres/{registrationNumber}
            -- see töötab ILMA võtmeta (kontrollitud 611511 peal)
Otsing      GET /api/products/tyres?...   -- NÕUAB võtit (403 ilma)
Autentimine päis  X-API-KEY: <votme>
Võti        https://eprel.ec.europa.eu/screen/requestpublicapikey

MIS ON KONTROLLITUD JA MIS EI OLE
---------------------------------
Kontrollitud otse päris vastuse pealt (reg nr 611511, SAVA PERFECTA):
kõik allpool olevad väljanimed FIELD_MAP-is.

EI OLE kontrollitud, sest otsingu endpoint nõuab võtit:
  * otsinguparameetrite nimed peale `modelIdentifier`
  * kas mõõdu järgi saab üldse otsida
  * lehitsemise ümbrik -- kaks avatud lähtekoodiga klienti on eri meelt
    (OCA loeb võtit `hits`, PHP klient räägib `content` + `totalElements`)
Need tuleb võtme saabudes päris vastuse vastu üle kontrollida. Kuni
selleni kasutab see moodul fikstuure.

TINGIMUSTEST TULENEVAD KOHUSTUSED (API_TERMS_AND_CONDITIONS, art 4)
-------------------------------------------------------------------
 4§3  atributsioon Euroopa Komisjonile peab lehel nähtav olema
 4§2  ei tohi teisendada nii, et see eksitab -- meie puhul tähendab see,
      et KLASS näidatakse muutmata kujul ja meie arvutatud meetrid on
      sellest selgelt eraldi, hinnanguna koos veapiiriga
 4§2f kui andmeid hoitakse lokaalselt, peab parandused JA KUSTUTAMISED
      kajastuma -- seega ei tohi neid staatilisse data.js-i küpsetada,
      vaid vahemälul peab olema aegumine (vt CACHE_TTL_H)
 7§6  ei tohi jätta muljet, et komisjon meid toetab
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .model import TyreCategory

API_BASE = "https://eprel.ec.europa.eu/"
DETAIL_PATH = "api/products/tyres/{reg}"
SEARCH_PATH = "api/products/tyres"
API_KEY_HEADER = "X-API-KEY"

# Vahemälu eluiga tundides. Art 4§2f nõuab, et parandused ja kustutamised
# jõuaksid meieni -- lõpmatu vahemälu oleks rikkumine.
CACHE_TTL_H = 24

# Kuidas end tingimuste art 4§3 järgi lehel nimetada.
ATTRIBUTION_ET = ("Rehvide märghaardumise klass: EPREL, Euroopa Komisjoni "
                  "energiamärgise tooteregister.")
ATTRIBUTION_EN = ("Tyre wet grip class: EPREL, the European Commission's "
                  "product registry for energy labelling.")

# EPREL-i väljanimi -> meie nimi. KÕIK vasakpoolsed on kontrollitud päris
# vastuse pealt. Kolm neist on nimega, mida ei oskaks arvata:
#   energyClass      = kütuseklass (MITTE fuelEfficiencyClass)
#   severeSnowTyre   = 3PMSF (MITTE snowGrip)
#   iceTyre          = jäämärgis (MITTE iceGrip)
FIELD_MAP = {
    "eprelRegistrationNumber": "reg_no",
    "supplierOrTrademark": "brand",
    "sizeDesignation": "size",
    "tyreDesignation": "designation",
    "tyreClass": "tyre_class",          # C1 / C2 / C3
    "wetGripClass": "wet_grip_class",
    "energyClass": "fuel_class",
    "externalRollingNoiseClass": "noise_class",
    "externalRollingNoiseValue": "noise_db",
    "loadCapacityIndex": "load_index",
    "speedCategorySymbol": "speed_symbol",
    "severeSnowTyre": "snow_3pmsf",
    "iceTyre": "ice_marked",
    "tyreSection": "section_mm",
    "aspectRatio": "aspect",
    "rimDiameter": "rim_in",
    "status": "status",
}
# mudeli nimi on pesastatud
NESTED_NAME = ("additionalDetails", "commercialName")


@dataclass
class EprelTyre:
    """Üks EPREL-i rehvikirje, meie väljanimedega."""
    reg_no: str
    brand: str
    name: str
    size: str
    wet_grip_class: str
    tyre_class: str = "C1"
    fuel_class: Optional[str] = None
    noise_class: Optional[str] = None
    noise_db: Optional[int] = None
    load_index: Optional[int] = None
    speed_symbol: Optional[str] = None
    snow_3pmsf: bool = False
    ice_marked: bool = False
    section_mm: Optional[int] = None
    aspect: Optional[int] = None
    rim_in: Optional[int] = None
    status: str = "PUBLISHED"
    designation: str = ""

    @property
    def label(self) -> str:
        return f"{self.brand} {self.name}".strip()


def parse(raw: dict) -> EprelTyre:
    """EPREL-i JSON -> EprelTyre. Tundmatud väljad jäetakse vahele."""
    out = {}
    for src, dst in FIELD_MAP.items():
        if src in raw and raw[src] is not None:
            out[dst] = raw[src]
    nested = raw.get(NESTED_NAME[0]) or {}
    out["name"] = nested.get(NESTED_NAME[1]) or raw.get("modelIdentifier", "")
    out.setdefault("reg_no", "")
    out.setdefault("brand", "")
    out.setdefault("size", "")
    out.setdefault("wet_grip_class", "")
    return EprelTyre(**out)


# ---------------------------------------------------------------------------
# Klass -> G. SIIN ON KOGU HÜBRIIDI TUUM.
# ---------------------------------------------------------------------------

# EL 2020/740 C1-rehvide klassipiirid. Keskpunktid on need, mida kasutame,
# kui rehvi kohta EI OLE päris testitulemust.
CLASS_BOUNDS = {
    "A": (1.55, 1.70),   # ülemine ots on praktiline lagi, mitte seaduses
    "B": (1.40, 1.54),
    "C": (1.25, 1.39),
    "D": (1.10, 1.24),
    "E": (0.00, 1.09),
}
CLASS_MID = {"A": 1.60, "B": 1.47, "C": 1.32, "D": 1.17, "E": 1.05}


def g_from_class(cls: str) -> Optional[float]:
    """Märgise klass -> G keskpunkt.

    NB: see on KLASSI keskpunkt, mitte selle rehvi päris G. Klass on 0,15
    laiune vahemik, seega kaks sama klassi rehvi võivad päriselt erineda
    kuni 0,15 võrra -- ja mudelis tähendaks see u 10 % pidurdusmaad.
    Just selle ebamäärasuse jaoks on Calibration.sigma_label_only olemas
    ja seda rakendatakse AINULT nendele rehvidele, mille G tuleb siit.
    """
    return CLASS_MID.get((cls or "").strip().upper())


def category_from(t: EprelTyre) -> TyreCategory:
    """Rehvikategooria märgise põhjal, nii hästi kui märgis lubab.

    AUS PIIRANG: märgis EI ERISTA Kesk-Euroopa ja Põhjamaade talverehvi,
    ega sport- ja tavalist suverehvi. 3PMSF ütleb ainult "talvevõimekas"
    ja jäämärgis ainult "jääle mõeldud". Seega:
        jäämärgis            -> Põhjamaade naelutu (lähim, mis meil on)
        3PMSF ilma jäämärgita-> ei tea, kas talve- või lamellrehv
        kumbagi ei ole       -> suverehv, tavaline
    Naastrehvi märgis üldse ei kajasta.

    Seepärast tagastab see AINULT esialgse pakkumise ja kasutaja peab
    saama seda üle valida. Ära kasuta seda vaikimisi ainsa tõena.

    KAKS KONTROLLITUD ASJA (15.09.2026, vt standardid.md), mis teevad
    selle veel nõrgemaks, kui ülal kirjas:

    1. Jäämärgise annab ISO 19447, mitte R117, ja see standard katab
       AINULT C1 ehk sõiduautorehve. C2/C3 rehvil ei saagi jäämärgist
       olla, ka siis, kui ta on jääl hea. Seega `ice_marked=False` ei
       tähenda kaubikurehvi puhul mitte midagi.
    2. C1 3PMSF-i saab kahest eri katsest -- pidurdus lumel indeksiga
       1,07 VÕI kiirendus indeksiga 1,10. Kaks 3PMSF-rehvi võivad olla
       mõõdetud eri füüsikalise suuruse peal. Seega `snow_3pmsf=True`
       ei ole isegi ühtlane lävend, rääkimata haardenumbrist.

    Numbrilisi lume- ja jäähaarde indekseid EPREL-i avalik osa EI ANNA
    -- need on vastavusosas, mis ei ole avalik. Ära otsi neid API-st.
    """
    if t.ice_marked:
        return TyreCategory.WINTER_NORDIC
    if t.snow_3pmsf:
        return TyreCategory.WINTER_CENTRAL
    return TyreCategory.SUMMER_TOURING


# ---------------------------------------------------------------------------
# Klient. Võti tuleb konfiguratsioonist; ilma võtmeta töötab ainult
# detailvaade ja fikstuurid.
# ---------------------------------------------------------------------------

class EprelClient:
    """Õhuke kiht API ümber.

    Ehitatud nii, et päris API ühendamine oleks LOKAALNE muudatus: kogu
    ülejäänud kood räägib ainult EprelTyre-objektidega. Praegu on taga
    fikstuurid, sest otsingu endpoint nõuab võtit ja selle vastuse kuju
    ei ole veel kontrollitud.
    """

    def __init__(self, api_key: Optional[str] = None, fetch=None):
        self.api_key = api_key
        self._fetch = fetch          # süstitav, et testida ilma võrguta

    @property
    def can_search(self) -> bool:
        return bool(self.api_key)

    def headers(self) -> dict:
        h = {"Accept": "application/json"}
        if self.api_key:
            h[API_KEY_HEADER] = self.api_key
        return h

    def detail_url(self, reg_no: str) -> str:
        return API_BASE + DETAIL_PATH.format(reg=reg_no)

    def get(self, reg_no: str) -> Optional[EprelTyre]:
        if self._fetch is None:
            return None
        raw = self._fetch(self.detail_url(reg_no), self.headers())
        return parse(raw) if raw else None
