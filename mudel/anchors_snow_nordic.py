"""Põhjamaade naelutu ja naastrehvi pidurdusmaa TALLATUD LUMEL.

MIKS SEE FAIL OLEMAS ON
-----------------------
Mudelil oli 47 mõõdetud lumepidurdust ja KÕIK olid Kesk-Euroopa
talverehvid või lamellrehvid (ADAC 2025). Kaks kategooriat, mis Eestis
ja Põhjamaades tegelikult domineerivad -- Põhjamaade naelutu ja naast --
olid lumel NULLI mõõtmisega. Nende lumehaarde väärtused olid mudelis
puhtad oletused: ainsad kaks arvu mu_snow_base sõnastikus, millel ei
olnud ühtegi allikaviidet juures.

Ja need oletused olid ka füüsiliselt kahtlased. Vana seis:

    ALL_SEASON      0,3925   (sobitatud, ADACA25)
    WINTER_CENTRAL  0,375    (sobitatud, ADAC25)
    WINTER_NORDIC   0,34     <- oletus
    WINTER_STUDDED  0,33     <- oletus

See ütles, et Põhjamaade talverehv haarab lumel HALVEMINI kui
Kesk-Euroopa talverehv ja halvemini kui lamellrehv. Põhjamaade rehv on
lume ja jää jaoks ehitatud; see ei ole usutav. Oletus ei olnud lihtsalt
ebatäpne, ta oli vale suunaga.

Selles failis on kaks mõõtmist, mis selle asendavad.

=============================================================================
[UTAC25N]  Põhjamaade NAELUTU, 5 rehvi
=============================================================================
Allikas: Pirelli avaldatud UTAC-i võrdlusaruanne, viide RD5090, 11.02.2025
  https://tyre24.pirelli.com/dynamic_engine/assets/global/RD5090_benchmarking_report.pdf

Kontrollitud KAKS KORDA sõltumatult (uurija + minu enda päring): samad
arvud, sama kiirusvahemik, sama temperatuur. Aruanne trükib nii indeksi
kui ka veeru "Distance [m]" -- allpool on trükitud meetrid, mitte
indeksist tagasi arvutatud väärtused.

  sõiduk        Audi Q5 TDI 2.0 (nelivedu)
  mõõt          235/60 R18 107T XL, kõigil viiel sama
  koht          Arctic Falls, "Indoor two", Flurheden, Rootsi
  pinnatemp     -8 °C   (õhk -7 °C)
  kiirus        35 -> 10 km/h

MIS SIIN ON HALVASTI, ja seda tuleb kaasas kanda:
  * SISETINGIMUSED. Lumehall ei ole välirada. Pinna ettevalmistus on
    teistsugune ja aruanne EI ÜTLE, kas lumi oli tallatud.
  * MAASTUR JA NELIVEDU. Kõik ülejäänud lumeankrud on sõiduauto.
  * MAASTURIMÕÕT. "X-ICE Snow SUV" ja "Hakkapeliitta R5 SUV" ei ole
    samad tooted, mis mudeli andmebaasis olevad sõiduautorehvid.
  * ÜKS TEST, ÜKS KOHT. Absoluuttaset ei kinnita miski teine.

NIMELT SELLEPÄRAST EI PANDUD SIIT REHVIPÕHISEID VÄÄRTUSI. Viie rehvi
vahe on 11,86...12,34 m ehk 4 %. See oleks ahvatlev kasutada
rehvipõhiseks eristuseks -- aga kolm viiest on maasturivariandid ja
üks on VikingContact 7, samas kui andmebaasis on VikingContact 8.
4 % vahe kahe ERI TOOTE vahel ei kandu üle. Võetakse ainult KATEGOORIA
KESKMINE, mis on see osa, mis kannab.
"""

from __future__ import annotations

# (nimi nii, nagu aruandes trükitud, indeks, pidurdusmaa m)
UTAC25N_ROWS = [
    ("Pirelli Ice Friction",              100.0, 11.86),
    ("Michelin X-ICE Snow SUV",           100.0, 11.87),
    ("Goodyear UltraGrip Ice 3",           99.8, 11.89),
    ("Nokian Tyres Hakkapeliitta R5 SUV",  99.5, 11.92),
    ("Continental VikingContact 7",        96.1, 12.34),
]
UTAC25N = dict(
    vehicle_key="audi_q5_fy",     # lisatud selle ankru jaoks, vt vehicles_ee.py
    size="235/60 R18",
    v_from_kmh=35.0,
    v_to_kmh=10.0,
    temp_c=-8.0,
    venue="Arctic Falls, Indoor two",
    date="2025-02-11",
    url=("https://tyre24.pirelli.com/dynamic_engine/assets/global/"
         "RD5090_benchmarking_report.pdf"),
)

# =============================================================================
# [ZR24]  NAASTREHV, 4 rehvi 12-st
# =============================================================================
# Allikas: Za Rulem (За рулем), "Восток против Запада", katse 2024
#   https://www.zr.ru/content/articles/913840-vostok-protiv-zapada/
#
# Kontrollitud kaks korda sõltumatult. Uurija esimene läbimine kahtles
# kiirusvahemikus; minu oma kinnitas artikli enda metoodikalauset:
#   "На льду эта величина составляет 20 км/ч, а на снегу – 40 км/ч"
# ehk jääl 20 km/h, lumel 40 km/h. Ülemine piir on seega 40, alumine 5.
#
#   sõiduk      Volkswagen Golf
#   mõõt        195/65 R15
#   koht        Continentali katserada, Arvidsjaur, Rootsi
#   temp        -7 ... -14 °C  (PERIOODI vahemik, MITTE pinna lugem --
#               ära kasuta seda temperatuurikõvera ankruna)
#   kiirus      40 -> 5 km/h
#
# MIS SIIN ON HALVASTI:
#   * Testis oli 12 rehvi, avalikult loetavas osas ainult 4 pidurdusmaad.
#     Need neli on siiski nii parim (Hankook 16,9) kui halvim
#     (Firestone 19,1), seega vahemik on kaetud, aga keskmine on
#     4 punkti peal, mitte 12.
#   * ÜKSKI neist neljast ei ole mudeli andmebaasis. Seega saab siit
#     ainult kategooria taseme, mitte rehvipõhist midagi.
#   * Testisisene hajuvus (16,9-19,1 ehk ±6 %) on suurem kui kogu
#     parandus, mille see ankur teeb (+4,5 %). Nõrk ankur -- aga
#     mõõdetud nõrk ankur on parem kui oletus.
ZR24_ROWS = [
    ("Hankook Winter i*Pike RS 2", True, 16.9),
    ("Gislaved Nord*Frost 200",    True, 17.2),
    ("GT Radial IcePro 3",         True, 19.0),
    ("Firestone Ice Cruiser 7",    True, 19.1),
]
ZR24 = dict(
    vehicle_key="vw_golf_8",
    size="195/65 R15",
    v_from_kmh=40.0,
    v_to_kmh=5.0,
    temp_c=-10.0,                  # perioodi -7..-14 keskpunkt, EI OLE lugem
    venue="Continental Arvidsjaur",
    url="https://www.zr.ru/content/articles/913840-vostok-protiv-zapada/",
)

# =============================================================================
# MIDA OTSITI JA EI LEITUD -- et keegi seda uuesti ei otsiks
# =============================================================================
NOT_FOUND = """
Otsiti soome, rootsi, saksa, vene ja eesti keeles.

  * Tekniikan Maailma 18/2025 -- 7 naast + 7 naelutu, VW Golf,
    205/55 R16, katsetaja UTAC Finland. TÄPSELT see tabel, mida oleks
    vaja. TASULINE, numbrid ei ole avalikud. Metaandmed on.
  * NAF 2025, Vi Bilägare 2025, dekkproff, rengasvertailu, tiresvote --
    KÕIK annavad ainult punkte või pingerida, mitte meetreid.
  * UTAC Ivalo 2024 naelutute test (10 rehvi, VW Golf, 205/55 R16) --
    numbrid on ainult JS-graafikus, teksti neid ei ole.
  * Goodyear / Test World Ivalo aruanded (2013, 2023) -- meetreid ei
    ole, ainult indeks referentsrehvi suhtes. Kasutamatu.
  * tyrereviews.com -- 403 igal katsel.

Ehk: lumepidurduse MEETRID Põhjamaade rehvide kohta on avalikult
haruldased. Enamik Põhjamaade teste avaldab punktid, mitte mõõdud.
"""
