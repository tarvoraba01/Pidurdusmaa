# Mis on ametlikult mõõdetud ja mis mitte

Kontrollitud 15.09.2026. Iga väide allpool on loetud päris dokumendist,
mitte mälust. Kus allikat kätte ei saanud, on see KINNITAMATA ja seda EI
TOHI mudelis kasutada.

Miks see fail olemas on: mudel tugineb ühele ametlikule numbrile (märghaarde
indeks G) ja väldib teisi. See fail ütleb, MIKS just nii — ja mis oleks
teoreetiliselt veel saadaval, kui EPREL-i võti kunagi rohkem avaks.

---

## 1. MÄRG HAARE — UNECE R117 lisa 5. See on mudeli sisend.

**Kontrollitud allikas:**
https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:42016X0812(01)
(R117 konsolideeritud tekst, täiendus 8)

| Mida | Mis on kirjas |
|---|---|
| Sisenemiskiirus | **85 ± 2 km/h** |
| Mõõteaken | "The average deceleration is calculated between 80 km/h and 20 km/h" |
| Veekile | "water depth shall be 1,0 ± 0,5 mm, measured from the peak of the pavement" |
| Pinnatemperatuur | 5–35 °C tavarehvil, 2–20 °C talverehvil |
| Referentsrehv | SRTT16, ASTM F2493-08, P225/60R16 |
| G määratlus (§2.17.4) | "the ratio between the performance of the candidate tyre and the performance of the standard reference test tyre" |
| Meetodid | (a) sõidukimeetod, instrumenteeritud sõiduauto; (b) haagis või rehvikatsesõiduk |

**PARANDUS varasemale:** mudeli dokumentatsioon ütles kohati "80 → 20 km/h
pidurdus". Täpsem on: pidurdus algab 85 km/h juurest, aga aeglustus
arvutatakse aknas 80 → 20. See ei muuda mudeli arvutust (G on suhe), aga
teksti tuleb parandada seal, kus see valesti kirjas on.

**KINNITAMATA, oluline:**
* Kas G on mfdd suhe või pidurdusjõu koefitsiendi suhe — Annex 5 valem jäi
  PDF-i katkemise taha. Mudel eeldab mfdd suhet (`mfdd = 231,48 / S`).
* Kas sõiduki- ja haagismeetod annavad sama indeksi. **Ühtegi lauset ei
  leitud, mis ütleks, et nad on samaväärsed.** See on tõendi puudumine,
  mitte tõend samaväärsuse kohta.

---

## 2. LUMI — R117 lisa 7, 3PMSF-märgis. KOLM PARANDUST.

**Kontrollitud allikas:**
https://www.marklines.com/statics/unece/pdf_202102/R117r4am3e.pdf
(R117 rev. 4, muudatus 3, täiendus 11, jõus 25.09.2020)

**(a) Referentsrehv ei ole see, mida ma varem ütlesin.** C1 klassi
referents on **SRTT14** (ASTM E1136-17, P195/75R14), mitte SRTT16C.
SRTT16C käib C2 kohta.

**(b) C1 3PMSF ON PIDURDUSTEST — aga teid on kaks.** Määruses on kolm
meetodit nimepidi: *"brake on snow method"*, *"spin traction method"*,
*"acceleration method"*.

**(c) Lävendid (p 6.4.1.1):**

| Klass | Pidurdus lumel | Spin traction | Kiirendus |
|---|---|---|---|
| C1 | **1,07** | ei kohaldu | 1,10 |
| C2 | — | 1,02 | 1,10 |
| C3 | — | — | 1,25 |

**Mida see mudelile tähendab:** C1 rehv võib 3PMSF-i saada KAS 1,07-ga
pidurdusest VÕI 1,10-ga kiirendusest. Need ei ole sama füüsikaline suurus.
Kaks 3PMSF-rehvi võivad olla saanud märgise eri katsest. Seega 3PMSF on
mudelis endiselt ainult binaarne "talvevõimekas", mitte haardenumber — ja
nüüd on teada, miks seda ei saakski numbriks teha.

**KINNITAMATA:** R117 lisa 7 nõutav lume temperatuurivahemik. Mudeli
dokumentatsioonis viidatud ASTM F1805 vahemik (−4…−15 °C) jääb kehtima
selle standardi kohta, aga R117 enda vahemikku ei õnnestunud kontrollida.

---

## 3. JÄÄ — EI OLE R117-s ÜLDSE. MINU EELDUS OLI VALE.

R117 lisad on 1–7 ja lõpevad lumega. **Lisa 9 ei ole olemas ja jäähaarde
sätet R117-s ei ole.**

Jäämärgise määrab **ISO 19447**, millele viitab EL määrus 2020/740.

**Kontrollitud allikas 1 (komisjoni KKK):**
https://energy-efficient-products.ec.europa.eu/faqs-0/ice-grip-performance-can-c2-or-c3-tyres-labels-bear-pictogram_en
> "only C1 tyres with ice braking performance level above the threshold as
> from ISO 19447 can display the 'ice pictogram' on the label"

ISO 19447 "only covers the testing method for C1 tyres" — ehk C2/C3 rehvil
EI SAAGI jäämärgist olla, isegi kui ta on jääl hea.

**Kontrollitud allikas 2 (ISO 19447:2021 eelvaade):**
https://cdn.standards.iteh.ai/samples/73917/623fee1c9321482ba348926c397f3527/ISO-19447-2021.pdf

| Mida | Mis on kirjas |
|---|---|
| Mis mõõdetakse | "the mean fully developed deceleration of a candidate tyre in an ABS braking test on a flat surface made of ice" |
| Indeks | "ratio between the mean fully developed deceleration of a test tyre and that of the reference tyre" |
| Referentsrehv | SRTT P225/60R16 97S, ASTM F2493 |
| Jää temperatuur | **−15 °C kuni −5 °C** |

**SEE ON MUDELI JAOKS OLULINE.** Jää temperatuurikõver
(`ice_temp_curve`) ulatub −35…+2 °C. Sertifitseeritud jäähaarde andmeid
on olemas AINULT vahemikus −15…−5 °C, sest standard ise lubab katsetada
ainult seal. Kõver on väljaspool seda vahemikku ekstrapolatsioon — sama
loogika, mis lumel ASTM F1805-ga. Kasutajale näidatav tekst peab seda
ütlema.

**KINNITAMATA:** kiirusvahemik ja lävendindeks. Väärtust **1,18** EI
LEITUD ühestki allikast — seda ei tohi kusagil kasutada.

---

## 4. KUIV PIDURDUS — REHVIL EI OLE, AUTOL ON

Siin tuleb kaks asja lahus hoida, ja ma ajasin nad esimeses versioonis
kokku.

### 4a. REHVI kohta kuiva numbrit ei ole. See jääb kehtima.

**Kontrollitud allikas:** EL 2020/740 täistekst.

EL-i rehvimärgise deklareeritavad näitajad on täpselt: veeretakistus,
märghaare, väline veeremismüra, lumehaare, jäähaare. Sõna "dry" esineb
määruses ainult ühes põhjenduspunktis tallatud lume kohta, mitte kunagi
jõudlusnäitajana.

Kontrollitud ka väljaspool EL-i (16.09.2026) — **kusagil maailmas ei ole
rehvi kuiva pidurduse hinnet:**

* **USA UTQG** (49 CFR 575.104) "traction" hinne AA/A/B/C on **MÄRG**,
  mitte kuiv. Määrus ütleb: pind "shall be wetted in accordance with
  ASTM E 274". Lisaks on see lukustatud ratta hõõrdetegur 40 mph juures,
  mitte pidurdusmaa, ja määrus ütleb ise, et ta ei kata "peak traction".
  "Temperature" hinne on soojuse tekke katse laboriratta peal, mitte
  haare. "Treadwear" on kulumine.
  <https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-575/subpart-B/section-575.104>
* **Jaapan (JATMA)** — veeretakistus AAA-C ja märghaare a-d (sama G
  indeks). Kuiva kriteeriumi ei ole.
* **Hiina** — veeretakistus, märghaare (pidurdusmaa 80 km/h juures),
  müra. Kuiva ei ole.

### 4b. AUTO kohta ON — ja see oli mul kahe silma vahele jäänud.

**UN R13-H** reguleerib sõiduauto (M1) pidurdust **kuival heas haardes
teel**. See ei ole rehvinõue vaid SÕIDUKINÕUE, ja seepärast ei anna ta
ühtegi rehvipõhist arvu — aga ta annab PÕRANDA.

**Kontrollitud kahest sõltumatust EUR-Lexi dokumendist**
(CELEX:42015X1222(01) ja ELI reg/2023/401), mis annavad sama arvu:

| Type-0, M1 | mootor lahutatud | mootor ühendatud |
|---|---|---|
| katsekiirus | 100 km/h | 80 % v_max, ≤160 km/h |
| pidurdusmaa | s ≤ 0,1v + 0,0060v² | s ≤ 0,1v + 0,0067v² |
| **keskmine väljaarenenud aeglustus** | **≥ 6,43 m/s²** | ≥ 5,76 m/s² |
| pedaalijõud | 6,5–50 daN | 6,5–50 daN |

**6,43 / 9,80665 = 0,656 g.** Katse tehakse nii koormatud kui tühjalt.

**PARANDUS:** levinud tsitaat `s ≤ 0,1v + v²/150` EI OLE R13-H mootor
lahutatud nõue — see vastab kordajale 0,0067 ehk mootor ühendatud
juhule. Mootor lahutatud on v²/166,7.

**Ja kaks kriteeriumi ei ole samaväärsed.** Pidurdusmaa valem annab
100 km/h juures s ≤ 70 m, mis ühtlase aeglustuse eeldusel oleks ainult
5,51 m/s² — vahe tuleb liikmest 0,1v, mis katab pidurite ülesehitusaega.
Aeglustust mõõdetakse aknas 0,8v...0,1v, mis ehitusaja teadlikult välja
jätab. **Mudel peab kasutama aeglustusnõuet, mitte pidurdusmaa valemit.**

**Mudelile:** `brake_capacity_g` on `presets.py`-s ainus sõidukiväli, mis
on HINNANG klassi järgi. Seda ei saa ankrute vastu sobitada, sest
pidurivõimekus piirab ainult siis, kui ta on haardest väiksem, ja
ankrutestides ta ei ole. Nüüd on tal vähemalt regulatiivne alumine piir
ja `audit.py` kontrollib seda iga jooksuga. Madalaim mudelis on 0,85 g,
põrand on 0,656 g.

**Katsepinna kohta** ütleb R13-H ainult kvalitatiivselt: "The road must
have a surface affording good adhesion". Numbrilist hõõrdenõuet
Type-0 katsele EI OLE. ABS-i lisas (Annex 6) on kH ≥ 0,5 ja kH/kL ≥ 2.
KINNITAMATA: väide, et kusagil nõutakse PBC ≥ 0,9 — Annex 9-ni ei
õnnestunud jõuda.

### 4c. Rehvitootjad avaldavad kuiva pidurdust MEETRITES

**See parandab minu varasemat väidet.** Ütlesin selles projektis varem,
et tootjad avaldavad ainult indekseid, mitte meetreid. Lume ja jää
kohta leitud aruannete puhul oli see õige, aga **TÜV SÜD-i aruanded,
mida tootjad ise oma lehel hostivad, annavad absoluutsed meetrid ja
keskmise aeglustuse.** Ühine protokoll: ABS-pidurdus, 100 → 0 km/h,
kuiv asfalt.

| allikas | rehv | kuiv pidurdus | ehk |
|---|---|---|---|
| Goodyear, TÜV SÜD 2019, 713171748-01 | EfficientGrip Performance 2 | 33,3 m / 11,59 m/s² | 1,18 g |
| Goodyear, TÜV SÜD 2021/22, 713234277-BM | UltraGrip Performance 3, 205/55 R16 | 39,8 m / 9,69 m/s² | 0,99 g |
| Bridgestone, TÜV SÜD 2023 | Turanza All Season 6, 205/55 R16 | 38,6 m | ~1,02 g |

**Miks neid siiski ankrutena EI kasutata:** katsesõidukit ei avaldata,
seega see on SÕIDUK+REHV tulemus, mitte rehvi omadus; konkurendid on
näidatud ainult protsentides; veapiiri ei ole; ja aruanded on tootja
tellitud. Kasutatav usutavusvahemikuna (moodne sõiduauto kuival
1,0–1,2 g), mitte rehvipõhise koefitsiendina.

**Aga üks asi sealt tuleb üle kontrollida:** sama Goodyeari aruanne
annab ka LUME pidurduse meetrites (26,9 m / 3,55 m/s², mis tagasi
arvutades on 50 → 0 km/h). Kui neid aruandeid on rohkem, võib see olla
lumeankrute allikas, mida ma varem valesti välistasin.

---

## 5. MIS EPREL-IST TEGELIKULT KÄTTE SAAB

**Numbriline G: ei, ainult klassivahemik.** C1 piirid (2020/740 lisa I):

| Klass | G |
|---|---|
| A | 1,55 ≤ G |
| B | 1,40–1,54 |
| C | 1,25–1,39 |
| D | 1,10–1,24 |
| E | G ≤ 1,09 |

Klass piirab G ligikaudu ±0,07-ni. See on kasutatav, aga jämedam kui
mudeli praegused testidest tuletatud G-d.

**Lumi ja jää: ainult piktogramm.** Numbrilised lume- ja jäähaarde
indeksid jäävad **vastavusosasse** (compliance part), mis ei ole avalik.
EPREL-i avalikus osas on kaubanimi, rehvi identifikaator, elektrooniline
märgis, klassid ja tooteinfo leht. Mõõdetud tehnilised parameetrid ja
arvutused ei ole avalikud.

**Järeldus EPREL-i võtme jaoks:** võti annab OTSINGU ja klassid. Ta EI
anna numbrilist G-d ega lume/jää indekseid. Seega hübriidplaan jääb
samaks: EPREL katab rehvide NIMEKIRJA ja tähed, numbrilised G-d jäävad
testidest tuletatuks.

---

## 6. MIS JÄI KÄTTE SAAMATA

* `https://unece.org/sites/default/files/2025-09/R117r5e.pdf` — **403
  igal katsel**, nagu kõik unece.org PDF-id. Määratud esmane allikas jäi
  lugemata. Kõik ülalolev on R117 EUR-Lexi (2016, täiendus 8) ja
  peegeldatud 2020 täienduse 11 põhjal. **Revisjon 5 (2025) on seega
  kontrollimata** — kui jäähaare on pärast 2020. aastat R117-sse lisatud,
  siis seda ei nähtud.
* EUR-Lexi HTML-otspunktid on robots-blokeeritud; töötab ainult
  `/TXT/PDF/` kuju.
* CELEX:42025X1453 ja OJ:L_202501453 tagastasid mõlemad 2016. aasta
  teksti, mitte 2025. oma.
* etrma.org suunab ümber tyreseurope.org-i, vana R117 PDF on kadunud.

---

## Kokkuvõte mudelile ühe lausega

Ainus rehvimudeli kaupa numbriline haardenäitaja, mille EL-i raamistik
üldse annab, on märghaare G — ja seegi ainult tähe kaudu. Lumi ja jää on
binaarsed märgised, mille taga on kaks eri füüsikalist katset (C1 lumi:
pidurdus 1,07 VÕI kiirendus 1,10), ja kuiva pidurdust ei mõõdeta üldse.
Mudeli praegune ülesehitus — G märjal, kategooriapõhised baasid mujal,
sõltumatud testid ankruteks — on selle tõttu ainuvõimalik, mitte valik.
