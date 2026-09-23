# Pidurdusmaa füüsikamootor

Esimene versioon sellest, mida ChatGPT-vestluses nimetati "kõige tähtsamaks
osaks": **arvutusmootor**, mis võtab sisse auto + rehvi + tee + ilma + kiiruse
ja annab välja pidurdusmaa koos ausa veapiiriga.

Ei UI-d, ei affiliate-linke, ei ilu. Ainult see, kas number tuleb õige.

**Lühivastus: tuleb.** **369 mõõdetud pidurdusmaa** peal on keskmine viga
**4,06 %**, 92 % tulemustest jääb ±10 % sisse ja **98 % ±15 % sisse**.
Lisaks on eraldi valideeritud **85 mõõdetud akvaplaneerimise ujumiskiirust**.

**Aus täpsustus nende 369 kohta:** nad EI OLE 369 sõltumatut fakti. Nad
tulevad kaheksast testiseansist, ja üks neist (ADAC 2025 talv) annab üksi
155 mõõtmist — 31 rehvi × 5 pinda, üks auto, üks mõõt, üks testipäev. Kui
selle päeva rada oli 5 % nihkes, on 155 "sõltumatut ankrut" koos 5 %
nihkes. Õigem on öelda **kaheksa sõltumatut testi, 369 mõõtmist**.

Kaetud on kuus teekatet, sh **lumi, märg betoon ja kruus**, mille kohta
mudelil esimeses versioonis ühtegi mõõtmist ei olnud.

Iga mudeli konstant peab deklareerima oma tõenduse ja `python3 -m
pidurdus.audit` kukub läbi, kui mõni ei tee seda või kui mõni liigutab
vastust ilma et ükski stsenaarium teda kontrolliks. Vt 7c.

---

## 1. Põhiidee

Vestluses jäi õhku küsimus: kas pidurdusmaad saab füüsikast välja arvutada?
Jah — valem on triviaalne:

```
d = v² / (2 · μ · g)
```

Kogu probleem on **μ**. Ja siin on see, mis selle projekti tööle paneb:

> **EL-i rehvimärgise märghaardumise indeks G ONGI μ, teisendustegurini
> täpsusega.**

G ei ole turundusnumber. See on UNECE R117 järgi mõõdetud suhe: kandidaatrehvi
pidurdusvõime jagatud standardse referentsrehvi (SRTT16, ASTM F2493,
P225/60R16) omaga, samal kattel, 1,0 ± 0,5 mm vee peal. Pidurdus algab
**85 ± 2 km/h** juurest, aga aeglustus arvutatakse aknas **80 → 20 km/h**
(kontrollitud R117 konsolideeritud tekstist 15.09.2026 — vt
[standardid.md](standardid.md)). Selle kohta on olemas ka täpne definitsioon:

```
mfdd = 231,48 / S          S = pidurdusmaa 80 → 20 km/h [m]
G    = mfdd_kandidaat / mfdd_SRTT
```

Kaks asja, mida R117 tekstist kätte EI saanud ja mida seega ei tohi eeldada:
kas G on rangelt mfdd suhe või pidurdusjõu koefitsiendi suhe, ja kas lubatud
sõiduki- ja haagismeetod annavad sama indeksi. Ühtegi lauset samaväärsuse
kohta ei leitud.

Ja EPREL-is (EL-i ametlik rehviregister) on see number **iga rehvi kohta,
mida Euroopas müüakse** — ~310 000 registreeringut.

Nii et mudeli süda on üks rida:

```
μ_märg = k_G · G
```

kus `k_G = 0,636` on sobitatud päris pidurdustestide vastu. Ehk A-klassi
rehv (G = 1,60) annab standardsel märjal asfaldil 20 °C juures μ ≈ 1,02
staatilise väärtusena, millest kiirus ja veekile siis maha võtavad.

**See tähendab, et rehvide osas ei ole andmeprobleemi.** Pole vaja
tyre.info API-t €500/kuus. EPREL on tasuta ja katab kõik rehvid.

---

## 2. Mudeli ülesehitus

Neli kihti, iga kiht üks selge vastutus:

### Layer 1 — füüsika

Pidurdusmaad ei arvutata valemiga, vaid **integreeritakse ajas**, sest μ
sõltub hetkkiirusest:

```
dv/dt = −( μ(v)·g·η_ABS + F_õhk(v)/m + F_veere/m + g·sin θ )
d     = ∫ v dt
```

Sisse on arvestatud ka pidurite ülesehitusaeg (aeglustus ei teki hetkega,
vaid kasvab 0,17–0,35 s jooksul olenevalt süsteemi põlvkonnast).

### Layer 2 — rehv

```
μ_staatiline = μ_baas × f_temp × f_rõhk × f_muster × f_vanus × f_koormus
```

| tegur | kust tuleb |
|---|---|
| `μ_baas` märjal | `k_G · G` — EPREL |
| `μ_baas` kuival | kategooria baas (EL-märgis kuiva EI kata) |
| `μ_baas` lumel/jääl | kategooria baas (EL-märgis ei kata) |
| `f_temp` | kummisegu kõver: suverehv kaotab 0 °C juures ~26 %, talverehv võidab külmaga |
| `f_rõhk` | paraboolne trahv soovituslikust hälbimise eest, märjal alarõhk hullem |
| `f_muster` | märjal käib peamiselt akvaplaneerimise liikme kaudu (vt allpool) |
| `f_vanus` | kummi kõvenemine üle 5 aasta |
| `f_koormus` | rehvi koormustundlikkus, μ ~ F_z^−0,07 |

### Layer 3 — tee

**Kuival** on lihtne: tekstuur (uus/kare · tavaline · kulunud/sile ·
poleeritud) ja väike kiirusesõltuvus.

**Märjal** oli algne versioon vale ja seda tuli ümber teha. Esimene katse
korrutas kokku eraldi "kiiruse", "veekile paksuse" ja "mustrisügavuse"
tegurid — mis topeltarvestas sama füüsikat ja andis absurdse tulemuse, kus
3 mm vesi oleks madalal kiirusel olnud peaaegu sama hea kui 1 mm.

Õige mudel: kiirus, veekile paksus, mustrisügavus ja rehvirõhk on **ühe ja
sama nähtuse osad** — rehvi ette koguneva vee hüdrodünaamiline tõstejõud.
See tõstejõud on võrdeline v²-ga ja pöördvõrdeline sellega, kui hästi rehv
vett ära juhib. Viimast kirjeldab täpselt akvaplaneerimiskiirus v_hp. Seega:

```
μ(v) = μ_staatiline / ( 1 + b · (v / v_hp)² )          b = 1,154

v_hp = 63,5 · √p · (1 + 0,085 · muster_mm) · (1,15 / vesi_mm)^0,42   [km/h]
```

Alusvalem `v_hp ∝ √p` on Horne'i klassikaline akvaplaneerimisvalem
(NASA); mustri ja veekile kordajad on kalibreeritud teadaolevate lävede
vastu. Üle ~0,72·v_hp läheb mudel sujuvalt üle täieliku akvaplaneeringu
peale (μ → 0,08) ja märgib tulemuse madala usaldusega.

See üks liige annab korraga:

| kontroll | mudel | oodatud |
|---|---|---|
| muster 8 → 2,5 mm, märg, 100 km/h | **+17,1 %** | DEKRA: +16…18 % |
| μ langus 40 → 100 km/h märjal | **−24 %** | kirjandus: −20…30 % |
| akvaplaneering, 8 mm muster, 3 mm vett | **108 km/h** | ~100–110 km/h |
| akvaplaneering, 1,6 mm muster, 3 mm vett | **73 km/h** | ~70–80 km/h |

Kolm sõltumatut kontrolli, üks parameeter. See on mudeli kõige tugevam koht.

### Layer 4 — auto

ABS-i põlvkond (kui suure osa tipphaardest süsteem reaalselt kätte saab:
ABS-ita 0,74 … kaasaegne pidurdusabiga 0,965), pidurite ülesehitusaeg,
õhutakistus (CdA), veeretakistus, tee kalle, koormus.

**Auto mass on tahtlikult väikese mõjuga**, sest füüsikas ta taandub
(a = μg). Ta tuleb sisse ainult kaudselt: rehvi koormustundlikkuse ja
õhutakistuse/massi suhte kaudu. Nii et vestluses tekkinud kahtlus oli õige
— auto valik ei ole nii tähtis, kui esmapilgul tundub. Tähtsam on ABS-i
põlvkond.

---

## 3. Valideerimine

Käivita ise: `python3 -m pidurdus.calibrate`
(Täisväljund: [`VALIDEERIMINE.txt`](VALIDEERIMINE.txt))

Ankurandmed: kaks sõltumatut avaldatud testi, kokku 62 mõõdetud
pidurdusmaad ([`anchors.py`](anchors.py)):

* **ADACS25** — ADAC 2025 suverehvitest, 225/40 R18, 18 rehvi × 3 pinda
* **ADACA25** — ADAC 2025 lamellrehvitest, 225/45 R17, 16 rehvi × 5 pinda.
  Ainus allikas, kus lumi ja jää on kaetud teise kummisegu peal.
* **ADAC25** — ADAC 2025 talverehvitest, VW Golf, 225/40 R18, **31 rehvi ×
  5 pinda** = 155 mõõtmist: kuiv 100→0, märg asfalt 80→0, märg betoon 80→0,
  lumi 30→0, jää 20→0, pluss akvaplaneerimise ujumiskiirus
* **TM25** — Tekniikan Maailma / UTAC 2025 talverehvitest, VW Golf,
  205/55 R16, 14 rehvi × (kuiv 80→0, märg 80→0, jää 50→0)
* **UT25** — UTAC / Aftonbladet 2025 suve- ja lamellrehvitest, Audi A3,
  225/45 R17, kuiv 100→5 ja märg 80→5
* **PASSAT** — rehvirõhu uuring: 2 × VW Passat B5, suve- ja talverehv,
  50 km/h, rõhud 1,0–3,0 bar, kuiv / märg / lumi, 6 kordust punkti kohta.
  30 mõõdetud suhtarvu.
* **MDPI25** — rõhutundlikkus ABS-ita (Machines 14(9):1002)

### Tulemus: mudel teab ainult EPREL-i infot

| pind | n | keskm, viga | 90 % kvantiil | halvim | ±10 % sees | ±15 % sees |
|---|---|---|---|---|---|---|
| kuiv asfalt | 93 | **2,9 %** | 6,8 % | 10,2 % | 99 % | 100 % |
| märg asfalt | 85 | **4,3 %** | 7,9 % | 11,7 % | 95 % | 100 % |
| märg betoon | 65 | **5,4 %** | 10,2 % | 15,5 % | 88 % | 97 % |
| lumi | 47 | **3,2 %** | 6,7 % | 25,5 % | 94 % | 96 % |
| jää | 61 | **5,0 %** | 12,3 % | 20,6 % | 80 % | 95 % |
| kruus | 18 | **3,1 %** | 8,0 % | 12,1 % | 94 % | 100 % |
| **kõik** | **369** | **4,06 %** | 8,9 % | 25,5 % | 92 % | **98 %** |

Testiseansi kaupa:

| allikas | n | keskm. viga |
|---|---|---|
| ADAC 2025 talv (31 rehvi × 5 pinda) | 155 | 3,4 % |
| ADAC 2025 lamell (16 × 5) | 80 | 3,9 % |
| ADAC 2025 suvi (18 × 3) | 54 | 6,0 % |
| Tekniikan Maailma 2025 | 42 | 3,8 % |
| UTAC / Aftonbladet 2025 | 20 | 2,6 % |

Vestluses seatud eesmärk oli "±10–15 %". Asfaldil on tulemus tegelikult
kordades parem.

### Tugevaim valideerimine: üks parameeter, neli ennustust

ADAC-i andmestikus tuletatakse iga rehvi märghaardumise indeks G **ainult
märja asfaldi katsest** — üks vaba parameeter rehvi kohta. Sellest ennustatakse
siis neli ülejäänud pinda, ilma ühegi lisaparameetrita rehvi kohta:

| pind | n | keskm. viga |
|---|---|---|
| märg asfalt (siit G tuletatud) | 31 | 0,0 % |
| **kuiv asfalt (ennustus)** | 31 | **2,1 %** |
| **märg betoon (ennustus)** | 31 | **1,3 %** |
| **lumi (ennustus)** | 31 | **2,9 %** |
| **jää (ennustus)** | 31 | **4,5 %** |

Ühest mõõtmisest neli ennustust, kõik alla 5 % — see on tugevaim tõend, et
mudeli struktuur on õige, mitte lihtsalt andmetele sobitatud.

### Akvaplaneering: kontroll ilma kalibreerimiseta

ADAC mõõdab ka akvaplaneerimise ujumiskiirust. Mudeli `hp_*` konstandid on
Horne'i valemist ja kirjanduse lävedest — **mitte nende andmete vastu
sobitatud**. Mudel ütleb 75,8 km/h, ADAC mõõtis 61,6–78,9 km/h, keskmine
viga **5,8 %**. Mudel ei erista mustri KUJU, ainult sügavust, nii et rehvide
omavahelist järjestust ta siin ei anna.

### Ristkontroll — kas see on lihtsalt ülesobitamine?

Ei. `k_G` sobitati **ainult talvetesti peale** (teine labor, teine auto,
teine rehvimõõt, teine rehvitüüp) ja sellega ennustati suvetesti:

| | n | keskm. viga |
|---|---|---|
| TM25 (sobitatud) | 14 | 3,2 % |
| **UT25 (puhas ennustus)** | **6** | **0,6 %** |

Ja vastupidi: UT25 pealt sobitatud mudel ennustab TM25 3,2 % täpsusega.
Ehk `k_G` ei ole ühe testi juhus — G → μ teisendus kehtib laborite üleselt.

### Leave-one-out

Iga rehv jäetakse sobitusest välja ja siis ennustatakse. Asfaldil 2,4 %,
jääl 8,5 %. Vahe näitab täpselt seda, mille EL-märgis kinni püüab (asfalt)
ja mida ta üldse ei kata (jää).

### Boonus 2: mudel leidis teise andmevea

Lamellrehvitesti kajastus märgib märja pidurduse "100 → 0 km/h". Mudel
eksis seal +50 %. Põhjus oli andmes, mitte mudelis: 31,3 m 100 km/h pealt
tähendaks märjal haardetegurit **1,26**, mis ületab isegi parimate rehvide
KUIVA haaret. 80 → 0 km/h juures annab sama arv μ = 0,80, mis klapib täpselt
sama labori suve- (0,89) ja talvetestiga (0,79). Silt on vale, katse on
80 km/h pealt.

See on teine kord, kui piisavalt jäik füüsikamudel andmevea välja tõi —
seda ei oleks juhtunud, kui mudel oleks lihtsalt andmetele sobitatud kõver.

### Boonus: mudel leidis andmestikust vea

Algselt panin talverehvide märghaardumise klassiks C. Kaks testi ei
ühtinud — 11 % süstemaatiline nihe. Skaneerides selgus, et need ühtivad
0,1 % täpsusega, kui talverehvide klass on **D**. Mis on realistlik —
Põhjamaade naelutud ja naastrehvid ongi märjal tüüpiliselt C–E.

See on hea märk: mudel on piisavalt jäik, et vale sisend välja paista.
Ja see näitab, miks päris EPREL-i andmed on hädavajalikud — klassi
oletamine maksab kohe ~11 % täpsust.

---

## 4. Mida see kõik tähendab veebilehe jaoks

**Hea uudis.** Andmeprobleemi, mida ChatGPT kartis, ei ole:

* rehvi märghaardumine → **EPREL, tasuta, kõik rehvid**
* rehvi käitumine muudel tingimustel → **füüsika, mitte andmed**
* tyre.info €500/kuu API → **MVP jaoks pole vaja**

**Halb uudis, ehk kus andmeid päriselt puudu on:**

1. **Kuivhaardumine.** EL-märgis ei kata seda üldse. Praegu on
   kategooriapõhine baas (suverehv 1,21, lamell 1,11, talverehv 0,80).
   Kategooria sees on rehvide vahe ±5 %. Iga päris kuivtesti tulemus,
   mis andmebaasi lisada, kaotab selle vea ühe rehvi jaoks ära.

2. **Lumi ja jää.** EL-märgis annab ainult 3PMSF ja jäärehvi linnukese —
   ehk "jah/ei", mitte numbrit. Jääl on kategooria sees vahe **kuni 65 %**
   (naastrehvid selles testis 32,3–42,5 m). Ilma testandmeteta ei saa
   jääd usaldusväärselt ennustada, ja mudel ütleb seda ise ka
   ("usaldus: madal").

   15.09.2026 sai kontrollitud, et see ei ole ajutine puudus, vaid
   struktuurne. Numbrilised lume- ja jäähaarde indeksid jäävad EPREL-i
   **vastavusossa**, mis ei ole avalik. Pealegi ei ole C1 3PMSF üks
   suurus: rehv võib märgise saada kas pidurdustestist indeksiga 1,07
   või kiirendustestist indeksiga 1,10, ja need ei ole võrreldavad.
   Jäämärgist ei reguleeri R117 üldse, vaid ISO 19447, mis katab ainult
   C1 ja lubab katsetada ainult −15…−5 °C juures. Vt
   [standardid.md](standardid.md).

3. **Kiirusesõltuvus märjal.** Ankrutes on ainult üks märja katse
   alguskiirus (80 km/h), nii et `wet_lift_b` tuleb kirjandusest, mitte
   andmetest. Vaja oleks teste eri kiirustelt.

4. **Rehvirõhk — LAHENDATUD.** Vt allpool: rõhukõver on nüüd sobitatud
   30 mõõdetud suhtarvu vastu ja keskmine viga on 1,3 %.

---

## 5. Teadaolevad puudujäägid

Ausalt kirja pandud, et keegi ei arvaks, et mudel teab rohkem kui teab:

* **Rõhukõver on nüüd valideeritud**, aga ainult ühe auto ja kahe rehviga
  (VW Passat B5). Rohkem autosid annaks kindluse, et kõver on üldine.
* **ABS-ita rõhutundlikkus toetub ühele allikale** (MDPI25, osaliselt
  simulatsioon) ja kordaja 9,16 on suur ekstrapolatsioon. Kasuta ettevaatlikult.
* **Temperatuurikõverad** on kirjandusest ja üldistatud kategooria kaupa.
  Konkreetsete segude vahel on vahesid.
* **Lumi: 47 ankrut Kesk-Euroopa talve- ja lamellrehvidele, 5 + 4 ülejäänutele.**
  Põhjamaade naelutu ja naastrehv said oma esimesed lumemõõtmised alles
  hiljuti (UTAC 2025, viis rehvi; Za Rulem 2024, neli rehvi 12-st) — enne
  seda olid nende lumeväärtused oletused, ja **vale suunaga**: nad ütlesid,
  et Põhjamaade rehv on lumel halvem kui Kesk-Euroopa oma. Vt
  [anchors_snow_nordic.py](anchors_snow_nordic.py) ja
  `calibrate_snow_nordic.py`. Nende kahe kategooria veapiir on nüüd
  teadlikult laiem (`sigma_snow_single_source`), sest ühe testi taga ei
  ole sama kaalu kui 47 mõõtmise taga.
* **Lahtisel lumel ankruid ei ole**, ja 2026-09 üle kontrollides selgus,
  et ka allikad ei ole nii tugevad, kui siin varem kirjas oli — vt
  [7h](#7h-lahtine-lumi--kaks-allikat-ei-olnud-kaks-allikat). Lörtsi ei
  modelleerita üldse.
  Lörtsi kohta leiti üks mõõtmine (KIT-i trummistend, 205/55 R16
  talverehv, 20 ja 40 mm lörtsi, 0…1 °C: piduri tipp-μ ≈ 0,26) — stend,
  mitte tee, ja seetõttu veel kasutamata.
* **Kruusal on 18 ankrut, aga KÕIK kuival kokkupressitud kruusal ja
  KÕIK suverehviga.** Märga kruusa, külmunud kruusa ja talverehvi kruusal
  otsiti soome, rootsi, saksa, vene ja eesti keeles — **mõõdetud andmeid
  ei ole avalikult olemas.** Kaks uuringut, mis neid kindlasti sisaldavad
  (Koorey & Cenek 1999 teekattega katmata teede kohta; Shoop & Kestler
  2015, TRR 2472), on ligipääsu taga. Levinud käsiraamatuväärtust
  μ = 0,35 "kruusa ja pinnastee" kohta EI KASUTATA: seda ei õnnestunud
  jälitada kaugemale kui Noon (1994), tal ei ole tingimusi juures, ja ta
  on ligi poole väiksem kui see, mida SATC 2019 tegelikult mõõtis.
* **Pidurite kuumenemist ajas ei modelleerita.** Pidurite võimekust saab
  ette anda (`Conditions.brake_condition`), aga see on kogu pidurduse
  jooksul konstantne. Päris fade läheb iga järgmise pidurdusega hullemaks.
  Vigaste piduritega ei ole ka ühtegi ankrut — protsendid on hinnangud,
  arvutus ise on korrektne.
* **Kurvis pidurdamist ei modelleerita.** Kõik on sirge tee.
* **Veekile paksus on kasutaja sisend, mitte vihmasadu.** See on teadlik
  valik: 20 mm/h vihma uuel dreenival asfaldil võib jätta õhema veekihi
  kui 5 mm/h roopalisel teel. UI peab kasutajalt küsima tee märgust
  (kuiv / niiske / märg / väga märg / seisev vesi), mitte sademeid.
* **`SUMMER_UHP` ja `SUMMER_TOURING` kuivbaas tulid sobitusel praktiliselt
  võrdseks** (1,206 vs 1,208), sest ankrutes on ainult üks UHP-rehv.
  Rohkem UHP-teste eristaks need ära.

---

## 6. Failid

```
pidurdus/
  model.py        mootor — kõik neli kihti, kogu füüsika
  presets.py      91 rehvi, 49 autot (kõik väärtused ülekirjutatavad)
  anchors.py      62 päris mõõdetud pidurdusmaad + allikad
  calibrate.py    sobitus + kolm valideerimist + seosekontrollid
  demo.py         9 näidet, mida mootor oskab
  anchors_adac.py  ADAC 2025 talvetest: 31 rehvi x 5 pinda + akvaplaneering
  anchors_adac2.py ADAC 2025 suve- ja lamellrehvitest (18x3 ja 16x5)
  vehicles_ee.py   Eesti sõidukipargi autod: valiku alus, allikad ja meetod
  anchors_aqua.py  Teknikens Värld 2025: 20 rehvi, sama mõõt, mõõdetud muster
  calibrate_adac.py  teine kalibreerimisetapp (lumi, betoon, rõhukõver)
  selgitused.json 28 infomullikest -- iga sisendvälja ja valiku kohta,
                  mida see tähendab ja kui hästi mudel seda teab
  selgitused.py   mullikeste laadimine + kontroll, et ükski valideerimata
                  koht ei oleks märgitud kõrge usaldusega
  VALIDEERIMINE.txt   viimase kalibreerimise täisväljund
```

Käivita:

```bash
python3 -m pidurdus.demo         # näited
python3 -m pidurdus.calibrate       # peakalibreerimine + valideerimine (~3 min)
python3 -m pidurdus.calibrate_adac  # ADAC-i etapp + rõhukõver (~2 min)
python3 -m pidurdus.selgitused   # mullikeste kontroll
python3 -m pidurdus.parity       # Python <-> JS, 15 välja, 60 juhtumit
python3 -m pidurdus.audit        # päritolu- ja tundlikkusaudit (~10 min)
node web/check-numbers.js        # lehe numbrite kooskõla, 108 olukorda
```

Kasutus koodist:

```python
from pidurdus.model import BrakingModel, Conditions, Surface
from pidurdus.presets import VEHICLES, tyre

m = BrakingModel()
r = m.stopping_distance(
        tyre("michelin_ps5", pressure_bar=2.1, tread_depth_mm=4.0),
        VEHICLES["bmw_320d"],
        Conditions(speed_kmh=90, water_mm=1.0, temp_c=8))

print(r.total_distance_m, r.low_m, r.high_m, r.confidence, r.warnings)
```

**NB kahe välja kohta:** `r.distance_m` on ainult pidurdusmaa,
`r.total_distance_m` on peatumistee (reaktsioonitee + pidurdusmaa) ja
`r.low_m` / `r.high_m` käivad PEATUMISTEE ümber. Kasutajale näita
`total_distance_m`; kalibreerimisel ja ankrutega võrreldes kasuta
`distance_m`, sest ankrud on pidurdusmaad. Vt 7e.

Sõltuvusi ei ole — ainult Pythoni standardteek. See on **tahtlik**: kogu
mootor on kirjutatud nii, et selle saab 1:1 TypeScripti portida ja
brauseris jooksutada. Ei mingit backendi, ei serverikulu, tulemus tuleb
hetkega ja kasutaja saab liugureid reaalajas nihutada.

---

## 5b. Kaks mehhanismi, mis said päris aluse

### Akvaplaneering sõltub mustri KUJUST, mitte ainult sügavusest

Teknikens Värld 2025 mõõtis 20 talverehvi **samas mõõdus** (235/45 R18,
Volvo V60) ja avaldas iga rehvi kohta ka **mõõdetud mustrisügavuse**. See
lubab akvaplaneerimise mudelit kontrollida nii, et sügavus on kontrolli all —
mida ükski teine test ei võimalda.

| kategooria | keskm. muster | ujumiskiirus |
|---|---|---|
| Kesk-Euroopa talverehv | 7,98 mm | **73,1 km/h** |
| Põhjamaade naelutu | 8,37 mm | **60,7 km/h** |
| naastrehv | 8,95 mm | **62,0 km/h** |

Põhjamaade rehvide muster on **sügavam**, aga nad ujuvad **19 % varem**.
Mudel ütles enne täpselt vastupidist. Põhjus on füüsikaline: Põhjamaade
rehvi muster on tehtud lume ja jää, mitte vee väljajuhtimise jaoks.

Pärast kategooriakordaja lisamist langes akvaplaneerimise viga
**25 % → 8,2 %** ja ADAC-i absoluutne tase jäi paika (5,6–7,7 %).

Eesti kasutaja jaoks on see oluline: naelutu Põhjamaade rehv on siin
levinuim talvevalik ja mudel **ülehindas** tema akvaplaneerimiskindlust.

### Temperatuurikõver: mudel kukkus järjestuskontrollis läbi

Test World mõõtis tunnelis (VW Golf, 205/55 R16) märga pidurdust 0, 2, 6,
10 ja 15 °C juures. Täpseid meetreid avaldatud ei ole — need on ainult
videos ja graafikutel, ja neid ma välja ei mõtle. Küll aga on avaldatud
selge **järjestus**: +2 °C juures peatub lamellrehv lühemalt kui nii
suverehv kui Kesk-Euroopa talverehv.

Mudel pani talverehvi esimeseks. Kirjandusest võetud kõver andis
talverehvile külmas liiga suure võidu. Vähendasin külmavõitu teguriga
0,25, kuni järjestus klapib, ja sobitasin baasid ümber.

**Hind: 351 ankru keskmine viga 4,0 % → 4,2 %.** See on teadlik vahetus —
väike arvuline täpsus ühe avaldatud kvalitatiivse tulemuse vastu. Kirjutasin
selle nii koodi kui mullikesse, et otsus oleks nähtav, mitte peidetud.

---

## 5a. Mida uued andmed muutsid

Kolm mudeli konstanti osutusid päris andmete vastu selgelt valeks:

| konstant | vana | uus | mille vastu |
|---|---|---|---|
| `concrete_factor` | 0,97 | **0,863** | ADAC, 31 punkti |
| `mu_snow_base` (K-Euroopa talverehv) | 0,30 | **0,375** | ADAC, 31 punkti |
| `press_k_wet_under` | 0,170 | **0,0050** | PASSAT, 30 suhtarvu |
| `mu_snow_base` (lamellrehv) | 0,26 | **0,3925** | ADAC lamell, 16 punkti |
| `mu_dry_base` (suverehv UHP) | 1,206 | **1,316** | ADAC suvi, 18 punkti |

Kõige suurem üllatus on viimane: **alarõhu karistus märjal oli mudelis ligi
30 korda liiga suur.** Mõõdetud andmed ütlevad, et ±1 bar nihe soovituslikust
maksab tavalisel märjal teel ainult 3–7 % pidurdusmaas, mitte 15–20 %.

Põhjus, miks see nüüd õigeks läks, on struktuurne: rõhu mõju märjal käib juba
akvaplaneerimise liikme kaudu (v_hp ∝ √p), nii et eraldi staatilist trahvi
peaaegu ei olegi vaja. Ehk füüsika oli õige, aga sinna oli lisaks kirjandusest
võetud kordaja, mis sama asja teist korda arvestas.

Erand: **ABS-ita autol** on rõhutundlikkus mitmekordne, sest alarõhuga rehv
lukustub varem. See tuleb ühest uuringust, kus ABS oli teadlikult välja
lülitatud — seal andis rõhu langus 2,41 → 1,69 bar 15 % pikema pidurdusmaa,
ABS-iga autol sama suurusjärgus langus ainult ~4 %.

---

## 6a. Pidurid: miks mõju ei ole lineaarne

Mootor võtab vastu pidurite võimekuse osakaaluna tervest autost
(`Conditions.brake_condition`). Mõju ei ole aga see, mida liugur intuitiivselt
lubaks — ja see on füüsikaliselt oluline:

| pidurid | võimekus | kuiv | märg 1 mm |
|---|---|---|---|
| korras | 1,30 g | 34,3 m | 50,6 m |
| nõrgenenud 85 % | 1,10 g | 37,2 m (+8 %) | 50,6 m (**+0 %**) |
| vigane 65 % | 0,85 g | 47,7 m (+39 %) | 51,3 m (+1 %) |
| kriitiline 45 % | 0,59 g | 67,1 m (+96 %) | 67,1 m (+33 %) |

Terve auto pidurid suudavad ~1,3 g, aga rehv suudab teele edasi anda ainult
~1,15 g kuival ja ~0,75 g märjal. Ehk **piirajaks on rehv, mitte pidur**, ja
pidurite nõrgenemine ei muuda mitte midagi seni, kuni nad langevad rehvi
võimekusest allapoole. Kuival juhtub see u 90 % juures, märjal alles u 65 %
juures.

Sellest järeldub kaks asja:

1. Ühtlane 25/50/75/100 % liugur annaks kasutajale vale mudeli peas. Kõver
   on lame, lame, lame, siis järsk.
2. **Osaliselt vigased pidurid annavad end esimesena üles kuival, mitte
   vihmaga** — vastupidi sellele, mida enamik eeldab.

Kui pidur langeb rehvist allapoole, näitab mootor tulemuses
`piiraja: pidurid` ja hoiatab, et parem rehv siin ei aitaks.

NB: normaalselt kulunud klotsid on **100 %**. Klots hõõrdub sama hästi kuni
metallini — kulumine mõjutab soojusmahtuvust, mitte pidurdusjõudu.

---

## 7. Järgmised sammud, minu järjekorras

1. **EPREL-i andmete allalaadimine.** Kõik `wet_grip_index` väärtused
   praegustes presettides on kas klassi keskpunktid või testist tuletatud.
   Päris süsteemis tulevad need EPREL-ist rehvi + mõõdu kaupa. See on
   üks öö tööd ja pärast seda katab mudel kõik Euroopas müüdavad rehvid.
2. **Rohkem ankruid.** Iga lisatud test parandab kalibratsiooni ja, mis
   tähtsam, annab ausama veapiiri. Eriti vaja: kuivtestid, lumetestid,
   testid eri kiirustelt.
3. ~~**Autode andmebaas.**~~ Tehtud: 49 autot, valitud Eesti kasutatud
   turu ja sõidukipargi järgi (vt `vehicles_ee.py`).
4. **Alles siis UI.** Ja siis on igal liuguril päris füüsika taga, mitte
   väljamõeldud koefitsient.

---

## 7a. Autode valik

Eesti sõidukipark on vana — ACEA järgi keskmiselt **16,6 aastat**, teel
liikuvatel u 13. Uute autode müügi edetabel ei kirjelda seda parki, nii et
autode valik on tehtud kasutatud turu ja pargi järgi.

Kaks allikat määrasid nimekirja:

* **Autoportaal, kasutatud turg (veebruar 2026):** 6031 omanikuvahetust.
  Margid BMW 842, VW 608, Toyota 491. Mudelid: BMW 3-seeria 293,
  BMW 5-seeria 262, VW Passat 232. Kuni 10 a vanad: Octavia 129,
  RAV4 86, Corolla 80. Imporditud autode keskmine vanus 7,38 a.
* **AutoReport.ee "Eesti levinuimad kasutatud autod"** — 16 mudelijuhendit,
  mis on nimekirjas kõik esindatud.

ABS-i põlvkonna piirid tulevad EL-i tähtaegadest: ABS kohustuslik uutel
sõiduautodel alates **2004**, ESC uutel tüüpidel **1.11.2011** ja kõigil
uutel **1.11.2014**. Sellest tuleb ka pargi jaotus mudelis: 24 autot
klassis 2004-2014, 22 klassis 2015+, 2 varasemat ja üks ABS-ita.

Mis on tootja andmed ja mis hinnang, on `vehicles_ee.py` päises kirjas.
Lühidalt: mass, mõõdud, teljevahe, rõhk ja OEM-mõõt on tootjalt;
õhutakistustegur kirjandusest; otsapindala arvutatud lähendiga
A = 0,83 · laius · kõrgus. **Pidurdusmaa jaoks on nendest oluline
peamiselt ABS-i põlvkond** — mass taandub füüsikas peaaegu välja.

---

## 7c. Päritoluaudit — kas iga konstant tuleb millestki päris?

`paritolu.py` + `audit.py`. See tekkis ühest ebamugavast tähelepanekust:
iga kord, kui mudelist leiti oletus, mis oli VALE SUUNAGA — lahtise lume
kordaja, kruusa ABS, Põhjamaade rehvi lumebaas — leiti ta juhuslikult,
mitte protsessiga. Kommentaar koodis ei ole tõendus; kommentaari saab
kirjutada ka väljamõeldud arvu kohta.

`paritolu.py` nõuab, et **iga** `Calibration`-i väli deklareeriks oma
tõenduse: FITTED (sobitatud nimetatud ankrute vastu), LITERATURE
(nimetatud avaldatud allikas), DERIVED (definitsioon), RESIDUAL
(tuletatud mudeli enda jääkvigadest), CLAMP (teadlik ohutuspiir).
`UNSOURCED` paneb auditi läbi kukkuma. Uus konstant ei saa enam
vaikselt sisse tulla.

`audit.py` ei usu registrit sõna-sõnalt, vaid mõõdab:

1. **Kate.** Iga väli peab registris olema.
2. **Tundlikkus.** Iga konstanti nihutatakse ±10 % ja mõõdetakse, kui
   palju muutub (a) ankruviga PINNA KAUPA ja (b) tüüpiline kasutaja
   vastus ning veapiir. Ohtlik ruut on (b) suur ja (a) null.
3. **Kaetus.** Kui ükski stsenaarium konstanti ei aktiveeri, KUKUB
   audit läbi — audit, mis annab valerahustuse, on halvem kui audit,
   mida ei ole. Erand: klamber, mille kohta audit ise TÕESTAB, et ta
   liidese lubatud alas ei saa rakenduda.
4. **Sigma ausus.** `sigma_base` ei ole vaba parameeter: ta peab olema
   vähemalt sama suur kui selle pinna ankrute tegelik jääkhajuvus.
   Praegu ASPHALT jääk 4,41 % vs lubatud 7,00 %; ICE 6,90 % vs 17,00 %.
5. **Kiirusevahemik.** Kas lubatud ala on ankrutega kaetud.

**Mida audit ise leidis, kui ta esimest korda ausalt jooksis:**

* 12 konstanti ei aktiveerinud ühtegi stsenaariumi — auditi enda viga,
  mitte hea uudis. Vanuse konstandid näitasid nulli, sest kõik
  stsenaariumid kasutasid uusi rehve. Nüüd on stsenaariume 40.
* Ankruviga võeti kõigi 369 keskmisena, mis summutas pinnapõhised
  konstandid ära: kruusa konstant liigutab 18 kruusaankrut palju, aga
  369 keskmises on see nähtamatu. Nüüd mõõdetakse pinna kaupa.
* Akvaplaneerimise 85 mõõtmist ei olnud `ANCHORS`-is, seega `hp_*`
  nägid välja kitsendamata, kuigi on just nende vastu sobitatud.
* Sõnastike nihutamine skaleeris ka NORMEERIMISPUNKTE (texture NORMAL
  = 1,00), mis andis võltsilt kõrge tundlikkuse.

**Mida audit MUDELIST leidis:** vt 7d.

## 7d. Tekstuur — mudeli KUJU oli vale, mitte arvud

Audit näitas, et teekatte tekstuur liigutab vastust kuni 10 %, samas kui
**mitte ükski 369-st ankrust ei varieeri tekstuuri** — kõik on
NORMAL. Kümneprotsendine hoob nulli peal.

Kirjandusest otsides selgus, et probleem ei olnud arvudes. NCHRP
*Guide for Pavement Friction*: "micro-texture influences the magnitude
of tire friction, while macro-texture impacts the friction–speed
gradient". Makrotekstuur EI OLE tasemekordaja — ta on veeärajuhtimine
ja määrab, kui kiiresti haare KIIRUSEGA langeb.

Mõõdetud tõend, et lame kordaja ei saa töötada (Jackson, FHWA 2008,
10 katselõiku, sile rehv, märg): kareda ja sileda katte haarde suhe on
48 km/h juures 1,03, 64 km/h juures 1,25 ja 80 km/h juures 1,44.

Mudel kasutab nüüd PIARC-i rahvusvahelise hõõrdeindeksi kuju
`F(v) = F60 · exp((60 − v)/Sp)`, `Sp = 14,2 + 89,7 · MPD`, mida toetavad
NCHRP, PIARC ja TRL 367 (133 katselõiku). NORMAL annab kordajaks täpselt
1,000 igal kiirusel, seega **ankruviga ei muutunud: 4,06 %**.

Poleeritus läks omaette mehhanismi: ta hävitab MIKROtekstuuri ja on
tasemekadu, mis kehtib ka kuival. Wehner/Schulze mõõtis 0,431 → 0,393
ehk ×0,912; liivapritsiga mikrotekstuuri taastamine andis 0,679 (+73 %).
Mudelis oli varem 0,76 — välja mõeldud ja veel vales mehhanismis.

**Kuival on tekstuuri makroliige nüüd täpselt 1,00.** Ühtegi mõõdetud
kuiva hõõrde ja makrotekstuuri seost ei leitud; kõik haardestandardid
nõuavad veekilet. Varasemad 1,02 / 0,96 / 0,92 olid välja mõeldud.

## 7e. Kaks suurust, üks ekraan — kasutaja leitud viga

Kasutaja saatis ekraanipildi, kus sama rehv seisis samal ekraanil kahe
erineva numbriga: suur number ütles **87,6 m**, võrdlusriba sama rehvi
kohta **62,6 m**. Kumbki arv ei olnud vale ja mootoris ei olnud viga —
87,6 = 25,0 (reaktsioonitee) + 62,6 (pidurdusmaa). Viga oli selles, et
leht võttis kahest eri suurusest numbrid kõrvuti ja ei öelnud kuskil,
et need on eri suurused. See on esitlusviga, aga kasutaja jaoks on ta
sama halb kui arvutusviga: number kaotab usaldusväärsuse.

**Esimene parandus oli vale parandus.** Ma viisin kõik peatumisteele:
suur number, ribad, redel, hoiatus. Numbrid klappisid, aga iga riba sai
ühise tumeda alguse ja selle alla joonealuse selgituse, miks ta seal on.
Kasutaja vastus oli: *"see liiga keeruline, reaktsiooniaega ei tohiks
sinna üldse arvutada, liiga palju infot"*. Ta oli täpselt õigel jäljel.
Viga oli kadunud ja segadus alles.

**Lõplik lahendus on lahutamine, mitte lisamine.** Reaktsioonitee EI
TULE rehvist ega autost — ta on inimene. Leht on rehvide võrdlemiseks,
ja seal ühine liidetav ainult lahjendab vahet ning lisab numbri, mille
kohta keegi ei küsinud. Leht arvutab nüüd ainult **pidurdusmaad**:
`condObj()` annab mootorile `reactionTimeS: 0`, liugur on ära, mullike
on kustutatud, `drawTrack` ei joonista reaktsiooniosa. Sellest järeldub
`total_distance_m === distance_m`, ehk **lehel ei saagi enam olla kahte
erinevat numbrit** — see ei ole enam kokkulepe, mida peab valvama, vaid
identsus. Kogu lehel on üks funktsioon `stopM()`, kust see arv tuleb.

Mootor oskab reaktsiooniteed endiselt (`reaction_time_s`,
`Result.reaction_m`) — maha võeti leht, mitte füüsika. Ausus elab ühes
jalus jaluses: number algab hetkest, mil pidur on põhjas, ja 90 km/h
juures lisandub päris elus veel ~25 m sekundi kohta.

Mootori enda väljundis oli sama auk: `Result.__str__` trükkis
`distance_m`, aga vahemiku `low_m…high_m` kõrvale — ja vahemik on
arvutatud peatumistee ümber. Nüüd trükib ta peatumistee ja lisab
lahtikirjutuse. `Result` sai välja `reaction_m` (JS-il oli `reactionM`
juba olemas).

**Miks paarsuskontroll seda ei püüdnud:** `parity.py` võrdles ainult
`distance_m`, `accel_*`, `limiter`, `confidence`, hoiatuste arvu ja
`extreme` — ehk täpselt seda ühte suurust, mis oli korras. Kõik lehel
nähtavad väljundid (`total_distance_m`, `reaction_m`, `low_m`, `high_m`,
`sigma_rel`, `mu_effective`, `peak_decel_g`, `time_s`) olid
kontrollimata. Nüüd võrdleb ta 15 välja, 60 juhtumil, bitilise täpsusega.

Uus kontroll `web/check-numbers.js` käib päris brauseris läbi **108
olukorda** (6 pinda × 6 kiirust × 3 rehvikategooriat) ja nõuab, et:

1. suur number == valitud rehvi riba number;
2. sõna "reaktsioon" ei esine tulemuses ja liugurit ei ole — **aga
   mootor oskab reaktsiooniteed endiselt arvutada** (25,0 m @ 90 km/h,
   1 s), ehk kontroll valvab korraga eemaldamist ja alleshoidmist;
3. kiiruseredeli valitud rida == suur number;
4. vahemik `lo…hi` ümbritseb suurt numbrit;
5. lehel ei ole ühtegi JS-viga.

Kontroll ise sai negatiivse testi: ajutiselt lisatud sõna "reaktsioon"
tulemuseplokki pani ta punaseks. Test, mis kunagi ei kuku läbi, ei ole
test.

Sama töö käigus tulid välja kolm viga, mis olid varem märkamata:

* **Kiiruseredeli ribad olid kolmandiku pikkused.** Klassinimi `.bar` on
  redelil ja võrdlusel sama, nii et redeli riba päris võrdluse
  `display:grid` + kolm veergu. Riba sisu `<i>` istus esimeses veerus
  ja tema protsent käis selle veeru, mitte kogu riba laiuse kohta.
  Arvud olid õiged, pilt vale.
* **Telefonis oli võrdlusriba ~10 px lai.** Kolm veergu (nimi 170 px +
  rada + arv 104 px) ei mahu 390 px ekraanile. Kitsal ekraanil läheb
  rada nüüd omaette ritta, üle kogu laiuse.
* **`build.py` ehitas lehe vanade andmetega.** `data.js` ja `engine.js`
  on genereeritud failid, aga build luges neid lihtsalt kettalt. Kui
  Pythoni pool oli muutunud ja `export_web` jooksmata, ehitas build
  vaikselt vananenud lehe. Avastasin selle siis, kui kustutatud mullike
  jäi lehele alles. Nüüd käivitab `build.py` `export_web`-i ise.

## 7f. EPREL — 91 rehvist 3744-ni, ja mida see maksis

Kasutaja kaebus oli praktiline: *"praegu ei leiaks ühtegi rehvi nt
rehvidpluss valikust enda vanale passatile"*. Mõõtmine andis talle
õiguse ja rängemalt, kui ta arvas: **231 autost oli 36-l mõni rehv oma
tehasemõõdus.** Kõige levinum Eesti mõõt 195/65 R15 (35 autot) oli
täiesti tühi.

Põhjus on struktuurne. Iga arv selles mudelis tuleb avaldatud testist;
test mõõdab **ühe mõõdu** ja testib seda, mis on **sel aastal uus**.
Nii oli nimekirjas kolm mõõtu ja ainult praeguse põlvkonna tipumudelid
(Primacy **5**, PremiumContact **7**, Turanza **6**). Vana Passati
195/65 R15 ei olnud seal kunagi olnudki.

### Mis EPREL-ist päriselt kätte saab — mõõdetud, mitte oletatud

| küsimus | vastus | kuidas teada |
|---|---|---|
| kas otsing filtreerib mõõdu järgi | **jah**, `sizeDesignation` | 4264 vastet vs 303 867 |
| mitu rida lehel | **25**, kõvasti lukus | `limit=1000` andis ikka 25 |
| kas saab lehitseda | **EI** | vt allpool |
| kas nimi on olemas | **jah**, 99 % | `additionalDetails.commercialName` |

**Lehitsemist ei ole ja seda oli vaja tõestada.** `page=170` andis sama
vastuse mis `page=0`, `page=50` sama mis `page=5`. Kolmteist eri
parameetrinime andsid kokku kolm erinevat vastust. Seletus: parameeter
visatakse minema ja kolm taustaserverit annavad igaüks oma "esimesed
25"; URL-i vahemälu seob sama päringu sama serveriga, mistõttu kordustest
näitas ekslikult "stabiilne".

Sellest järeldub kogu korje kuju: **päring tuleb teha nii kitsaks, et
vastus mahub 25 sisse.** Mõõt × mark annab tüüpiliselt 5–25 vastet;
kärbituks jäänud paarid tükeldatakse veel kiirusindeksi kaupa. 10 mõõtu
× 30 marki = 300 päringut, **7308 registreeringut, neist 3653 eristuvat
mark+nimi+mõõt**.

### Kolm otsust, mis on mõõdetud

1. **Margi kirjuviis.** Korjes oli 103 kuju — `MICHELIN`/`Michelin`, ja
   `KUMHO WP52`, kus margi väljas oli mudelikood kaasa kirjutatud.
   Normaliseerimine → 31 marki.
2. **Vastuoluline klass.** 7 % mudel+mõõt paaridest andis kaks või kolm
   eri märghaardumise klassi (Bridgestone Ecopia EP150 195/65R15 oli A,
   B ja C). Põhjus on päris: sama mudel sama mõõdu sees eri koormus- ja
   kiirusindeksiga on eri registreering. Mudel võtab **halvima**, sest
   ohutusnumbri juures on alahindamine parem kui ülehindamine ja poes ei
   tea ostja, kumba varianti ta käes hoiab.
3. **Kategooria.** Märgis EI ÜTLE suvi/talv/lamell — ainult 3PMSF ja
   jäämärgis. Sellest: jäämärgis → Põhjamaade talverehv; 3PMSF + nimi
   ütleb → talv või lamell; 3PMSF + nimi vaikib → talverehv, **märgitud
   oletuseks** (562 tükki, 15 %). Iga rehv kannab välja `kat_alus`, nii
   et oletus ja märgiselt loetu ei ole samas kastis.

### Mida see MAKSAB — ja miks see lehel näha on

EPREL annab märghaardumise **klassi**, mitte numbrit. Mudel võtab klassi
keskpunkti, seega **kaks sama klassi rehvi on eristamatud**. Esimene
katse pani nad tavalisse võrdlusse ja tulemus oli üheksa riba ühe ja
sama numbriga — täpselt see teesklus, mida lumel ja kruusal juba korra
parandati. Nüüd:

* **mõõdetud rehvid** (91) võrreldakse rehvi kaupa;
* **märgiserehvid** võrreldakse **klassi kaupa** ("Klass A · 35 rehvi"),
  ja ribade all on üks lause, miks;
* märgiselt tulnud G katab usalduse **"keskmise"** peale — sama reegel
  nagu mõõdu ülekandel. Number kirjeldab klassi, mitte seda rehvi.

Kui auto mõõdus on rehve olemas, näidatakse **ainult selle mõõdu omi**:
märghaardumise klass on mõõdupõhine, nii et teise mõõdu numbri kõrvale
panek oleks ülekanne seal, kus ülekannet pole vaja.

### Mida ma valesti tegin, ja mis selle parandas

Ma pakkusin väljanimesid ühekaupa — `registrationNumber`, siis
`modelIdentifier` — ja kolmesaja päringu järel teatasin, et nime ei ole
olemas. `modelIdentifier` on tarnija **artiklikood** (85 % puhtad
numbrid). Nimi oli kogu aeg olemas, ühe taseme võrra sügavamal:
`additionalDetails.commercialName`.

Kasutaja ütles: *"sa ei saa lihtsalt vaadata ühest kohast mida see fail
sisaldab"*. Sai küll — ja fail oli tema masinas juba olemas, esimesest
proovipäringust. Üks pilk kõigile väljadele korraga andis vastuse, mille
kümme oletust ei andnud. **Reegel edaspidiseks: tundmatu andmeallika
puhul dumpi kõik väljad korra välja ja vaata, mitte ära paku nimesid.**

### Mis on veel katmata

10 mõõtu 59-st. Ülejäänud on sama korje, ainult pikem nimekiri.
73-margine nimekiri on käsitsi koostatud — mark, mida seal ei ole, jääb
puudu, ja skript ütleb selle välja. 47 mõõt+mark+kiirus lõiget jäi
kärbituks ka pärast tükeldamist.

## 7i. Vi Bilägare 2010 — esimene päris väljaspool-valimi kontroll

Kõik senised ankrud on ühest aastast (2025), kahest mõõdust ja kahest
kiirusest. Auditi 4. jagu ütleb selle välja: iga pind peale kruusa on
**ekstrapolatsioon**. Vi Bilägare 2010 kaks talverehvitesti on teisest
aastakümnest, teisest riigist, mõõdust **205/55 R16** ja kiirustelt
**80→5, 45→5, 40→5, 35→5, 30→5 km/h** — ükski neist ei ole mudeli
kalibreerimisalas.

Meetod on sama, mis README 3. jaos: **G tuletatakse ainult märjast
tulemusest, kõik ülejäänud pinnad on ennustused.** Mudelit ei muudetud.

| | kuiv | jää | lumi |
|---|---|---|---|
| **[VIB10F]** naelutud, Ivalo, 6 rehvi | **3,2 %** | **5,8 %** | +24,9 % |
| **[VIB10D]** naastrehvid, Arvidsjaur, 9 rehvi | **5,7 %** | −29 % / −18 % | −41 % |

**Kuiv kandis välja.** 3,2 % ja 5,7 % viieteistkümne aasta, teise mõõdu
ja teise kiiruse taga — see on tugevaim tõend seni, et mudeli tuum ei
ole 2025. aasta ADAC-i testi ülesobitus.

### Leid: jää temperatuurikõver ei tohi olla kõigile üks

Naastrehvitestis on **sama üheksa rehvi mõõdetud jääl kahel
temperatuuril samal päeval** (−3…−2 °C ja +0,5…+1 °C). Mudelil ei ole
ühtegi teist sellist paari. Suhe (soe pidurdusmaa / külm pidurdusmaa):

| | mõõdetud | mudel |
|---|---|---|
| naastrehv (n=7) | **1,23** (1,10–1,33) | 1,46 |
| Põhjamaa naelutu (n=1) | **1,69** | 1,45 |
| Kesk-Euroopa (n=1) | **1,69** | 1,41 |

Mudel annab kõigile kolmele ühe kõvera. Mõõdetud andmed lahknevad
**selgelt kaheks**: nael umbes 1,23, kumm umbes 1,69. Mehhanism on
tagantjärele ilmne — **nael lõikab jäässe mehaaniliselt ja see ei hooli
temperatuurist eriti; kummi haare sulamislähedasel jääl kukub kokku
veekile tõttu.** Mudel on naastrehvile ~19 % liiga järsk ja
hõõrdrehvile ~14 % liiga lame.

See on sama kuju-viga, mis leiti tekstuuri juures (7d): arvud olid
sättimise kaugusel, aga kõvera **kuju** oli vale.

### Parandus: `ice_temp_exp`, ja miks ta ei liiguta ühtegi ankrut

Kõver on **normeeritud 1,0-le −5 °C juures**. Vaatasin järele, kus
jääankrud on:

| kategooria | n | temp |
|---|---|---|
| WINTER_STUDDED | 7 | −5,0 °C |
| WINTER_NORDIC | 7 | −5,0 °C |
| WINTER_CENTRAL | 31 | −4,0 °C |
| ALL_SEASON | 16 | −4,0 °C |

**Kõik 14 naastrehvi- ja Põhjamaa ankrut on täpselt −5 °C juures, kus
f = 1,0** — aste ei liiguta neid seal üldse. Ülejäänud 47 on kategooriad,
mille aste jääb 1,0. Seega ei vajanud **ükski** `mu_ice_base`
järelesobitust, ja auditi jää jääkhajuvus jäi täpselt samaks (6,90 %).
Harva juhtub, et parandus mahub nii puhtalt olemasoleva vahele.

Rakendus: `f_kat(T) = f_alus(T) ** exp[kat]`, **ainult kaopoolel**
(f < 1, ehk soojemal kui −5 °C). Külmal pool jääb kirjanduse kõver
puutumata, sest mõõdetud tõend katab −2,5…+0,75 °C. Terve kõvera
astendamine paisutaks külma otsa ohutusklambrini — siis annaks −20 °C
vastuse klamber, mitte mõõtmine, ja see on projektis keelatud.

Tulemus naastrehvi suhtele (mõõdetud vs mudel):

| | enne | pärast |
|---|---|---|
| keskmine absoluutviga (n=7) | ≈ 19 % (ühesuunaline) | **5,5 %** (±12 %) |

**Hõõrdrehvi poolt EI muudetud.** Ta nõuaks suhet 1,69, mille
rakendamiseks tuleks lõdvendada ohutusklambrit `ice_temp_min = 0,40` —
siis annaks sula jää vastuse klamber, mitte mõõtmine. **Kahe rehvi
pealt seda ei tee.** Teadaolev viga jääb −14…−17 % ja ootab andmeid.

**NB — miks sobitati suhe, mitte pidurdusmaa.** Absoluutne jääpidurdusmaa
selles testis on kõigil rehvidel ~30 % lühem kui mudel ennustab, ja oli
seda juba enne muudatust. Põhjus on pind, mitte mudel: `mu_ice_base`
tuli Ivalo jäält (TM25), see test tehti Arvidsjauris. **Suhe on ainus
suurus, millest pind välja taandub** — sama rehv, sama päev, sama jää,
kaks temperatuuri.

### Teine leid: lumi ja jää on mudelis kategooria konstandid

Mudel ennustab kõigile ühe kategooria rehvidele **täpselt sama** jää- ja
lumepidurdusmaa (G mõjutab ainult märga ja kuiva). Mõõdetud hajuvus ühe
kategooria sees selles testis: **jääl 23,0–28,2 m (23 %)**, lumel
36,3–43,0 m (18 %). Mudel ei näe sellest midagi. Veapiir katab selle,
aga rehvide **pingerida** jääl ja lumel on mudelis olematu.

### Lahendamata vastuolu — miks lumeread kalibreerimisse ei läinud

Kahe testi lumepidurdus ei klapi omavahel:

| | protokoll | mõõdetud | aeglustus |
|---|---|---|---|
| naelutu (Ivalo) | 40→5 km/h | 13,2–15,3 m | ≈ 0,43 g |
| naastrehvid (Arvidsjaur) | 45→5 km/h | 36,3–43,0 m | ≈ 0,22 g |

Sama ajakiri, sama aasta, sama mõõt, **kahekordne vahe**. See ei saa
olla rehvide vahe. Mudel jääb täpselt nende kahe vahele (+25 % ühest,
−41 % teisest), mis on ise vihje, et erinevus on **lumes**, mitte
mudelis. Kuni see ei ole lahendatud, ei lähe lumeread kalibreerimisse.

**Boonus, mis jäi kõrvale ootama:** naastrehvitestis on veerg
*"Snöslask, km/tim"* — **lörtsi ujumiskiirus** üheksale rehvile. Lörtsi
mudelis ei ole üldse. Andmed on nüüd `anchors_vib10.py`-s alles.

Failid: [anchors_vib10.py](anchors_vib10.py),
[validate_vib10.py](validate_vib10.py).

## 7h. Lahtine lumi — "kaks allikat" ei olnud kaks allikat

`snow_loose_factor = 0,85` oli mudeli ainus konstant, mille kohta oli
kirjas, et teda kinnitavad **kaks sõltumatut allikat**, ja millel samal
ajal ei ole ühtegi ankrut. Mõlemad allikad loeti 2026-09 uuesti läbi.
Väide ei pidanud paika.

**Allikas 1 — Ichihara & Mizoguchi, TRB SR115 tabel 1** (auto pidurdus,
30–40 km/h). Verbatim: *"New snow 0.2 to 0.25"*, *"Old snow 0.25 to
0.30"* → suhe 0,82. See on see, kust 0,83 tuli. Aga tabeli telg on lume
**vanus**, mitte sügavus — vana lume terad on suuremad ja
purunemistakistus suurem. Sama töö ütleb tallatud lume kohta eraldi
*"around 0.2 to 0.3"*, mis **katab uue lume vahemiku tervenisti**.
Allikas ei mõõda lahtist vs tallatud.

**Allikas 2 — FAA AC 25-31 tabel 2** (lennuk, lennurada). Sügavam kui
3 mm kuiv lumi = 0,161; tallatud lumi = 0,161 soojemal kui −15 °C ja
0,201 külmemal. **Suhe on seega 1,00 selles temperatuurivahemikus, kus
Eestis sõidetakse**, ja 0,80 alles alla −15 °C. Meie tegur on
konstantne 0,85 — ta ei järgi kumbagi otsa. Lisaks on see koefitsient
lennunduses **tahtlikult ilma lume lükkamise takistuseta** (AC käsitleb
contaminant drag'i eraldi jaos), mis autol aeglustab ka — täpselt see,
miks vana 1,12 ei olnud absurdne, ainult tõendamata.

**Otsus: number jääb, põhjendus muutub.** 0,85 seisab praktikas ÜHEL
auto-allikal ja lennundusallikas ütleb siinsel temperatuuril 1,00.
Auto-allikas on autole lähem, nii et 0,85 jääb — aga ta on **valitud,
mitte kinnitatud**, ja päritoluregistris on see nüüd nii kirjas.

Kontrollitud, et veapiir katab lahkarvamuse (Passat B8, talverehv,
50 km/h, −5 °C):

| tegur | pidurdusmaa | vahemik |
|---|---|---|
| 1,00 (FAA) | 29,6 m | |
| **0,85 (mudel)** | **34,3 m** | **27,9–40,7 m** |
| 0,82 (SR115) | 35,4 m | |

FAA tulemus mahub meie vahemikku. σ = 18,6 % on kogu mudeli laiem
veapiir ja ta teenib siin oma leiba ära.

**Mida mudel ikka veel ei tee:** lumekihi **sügavus ei ole sisend**.
Päris vastus on sügavusest sõltuv — õhuke lahtine kiht tallatu peal on
libe, sügav lumi hakkab lükkamistakistusega aeglustama — ja seda telge
mudelis lihtsalt ei ole.

## 7g. Kütuseklass kummisegu asendajana — katse, mis läbi kukkus

Kummisegu on ainus suur sisend, mida meil ei ole ega tule. Tekkis
hüpotees, et **EPREL-i kütuseklass on tema proksi**: veeretakistus ja
märghaardumine tulevad mõlemad kummi hüstereesist, lihtsalt eri
sagedusel, nii et sama märghaardeklassi juures peaks parem kütuseklass
tähendama paremat segu. Andmed olid juba käes — korje päris `kytus`
välja algusest peale (100 % täidetud, 7308 kirjet), ainult
`eprel_convert.py` ei kandnud teda edasi.

**Tulemus: ei seleta midagi.** `kytus_katse.py` + `kytus_regress.py`:

| | |
|---|---|
| seotud rehve | 41 / 88 |
| kaldenurk | +0,015 G kütuseklassi sammu kohta |
| korrelatsioon (kategooria sees) | r = +0,157, R² = 2,5 % |
| leave-one-out ruutviga | 0,0603 → **0,0605** (halvem) |

Ja märk ei püsi paigal: lamellrehvidel +0,51, talverehvidel +0,50,
UHP-l −0,05, Põhjamaa talverehvidel −0,46. Ainult üheselt määratud
kütuseklassiga alamhulk annab −0,245, terve hulk +0,157. **Märgi
kõikumine alamhulkade vahel ongi see, mille järgi müra tunneb ära.**
Mudel jääb muutmata.

### Kaks sidumisviga, mis oleksid vaikselt läbi läinud

1. **`mudel()` lõikas ära VÕÕRA margi nime.** Continentali rida
   "VikingContact 7" → "Viking" on ka mark → järele jäi "CONTACT7",
   mis on "SPORTCONTACT7" sisestring. **Continental SportContact 7
   (G = 1,795, parim rehv kogu hulgas) sai vasteks Continental
   VikingContact 7** — Põhjamaa talverehv, märghaare D. Parandus:
   maha tohib lõigata ainult **selle rea enda** margi.

2. **Sisestring ei kõlba nimede sidumiseks.** Lühem nimi on pikema
   sisestring ka siis, kui tegu on eri tootega: Ultrac Pro → Ultrac,
   Pilot Alpin 5 → Alpin 5, Aspire XP Winter → Aspire XP (suverehv!),
   Advantage All Season → Advantage. Parandus: **täpne võrdus**. Jättis
   45-st 41 vastet, aga kõik 41 on ükshaaval üle vaadatud.

### Mida katse siiski andis: `sigma_label_only` on nüüd mõõdetud

Sidumise kõrvalsaadusena sai küsida seda, mida varem ei saanud: **kui
lai on mõõdetud G hajuvus ühe EPREL-i märghaardeklassi sees?**

| kategooria | klass | n | suhteline hajuvus |
|---|---|---|---|
| Lamell | B | 5 | 3,9 % |
| Suvi (tava) | A | 5 | 3,9 % |
| Suvi (UHP) | A | 5 | 3,6 % |
| Talv | B | 5 | 3,2 % |
| Põhjamaa talv | D | 3 | 2,4 % |

Mudelis on `sigma_label_only = 4,5 %` ja see oli seni **oletus** —
tuletatud klassi laiusest, mitte mõõdetud. Nüüd on ta järelkontrollitud
ja **konservatiivne**, mis on ohutusnumbri juures õige suund. Pealegi
**ülehindab see mõõtmine hajuvust**, sest EPREL-i klass tuli teistest
mõõtudest kui ADAC-i test — korjes ei ole 225/40 R18 ega 225/45 R17.
Päris hajuvus sama mõõdu sees on ≤ 3,9 %.

## 8. Allikad

* EL määrus 2020/740 (rehvide märgistamine) — märghaardumise klassid A–E
  ja veeretakistuse klassid
  <https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A02020R0740-20200605>
* NCHRP Web-Only Document 108, *Guide for Pavement Friction* — mikro- vs
  makrotekstuuri roll; "macro-texture impacts the friction-speed gradient"
* PIARC rahvusvaheline hõõrdeindeks (IFI), Sp = a + b·MPD
* TRL 367 — 133 katselõiku, lukustatud ratta haagis, 20-130 km/h
* Jackson, FHWA 2008, *Harmonization of texture and skid-resistance
  measurements* — tabel 10, MPD ja hõõre kolmel kiirusel
  <https://rosap.ntl.bts.gov/view/dot/17075>
* Wehner/Schulze poleerimiskatse — mikrotekstuuri kadu ja taastamine
* UNECE R117 — märghaardumise testi metoodika, mfdd = 231,48/S,
  sisenemine 85 ± 2 km/h, aken 80 → 20 km/h, veekile 1,0 ± 0,5 mm,
  katte pbfc 0,6–0,8, temperatuuriparandus. Loetud kujul:
  <https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:42016X0812(01)>
  (EUR-Lexi HTML-kuju on robots-blokeeritud, unece.org PDF-id annavad 403)
* UNECE R117 lisa 7 — 3PMSF lumelävendid ja kolm meetodit (brake on snow /
  spin traction / acceleration), C1 referents SRTT14 (ASTM E1136)
  <https://www.marklines.com/statics/unece/pdf_202102/R117r4am3e.pdf>
* ISO 19447:2021 — jäähaarde ABS-pidurdustest, referents SRTT16,
  jää −15…−5 °C. Jää EI OLE R117-s.
  <https://cdn.standards.iteh.ai/samples/73917/623fee1c9321482ba348926c397f3527/ISO-19447-2021.pdf>
* Euroopa Komisjoni KKK — jäämärgis ainult C1 rehvidele
  <https://energy-efficient-products.ec.europa.eu/faqs-0/ice-grip-performance-can-c2-or-c3-tyres-labels-bear-pictogram_en>
* DEKRA — mustrisügavuse mõju pidurdusmaale (märjal +16…18 %,
  kuival +2,4…8,5 % kui 7–8 mm → 2–3 mm)
  <https://www.dekra.us/en/stopping-distance-on-wet-surfaces-tread-depth-can-decide-about-crashing/>
* Tekniikan Maailma 2025 talverehvitest (UTAC), kajastus Tyre Reviews
  <https://www.tyrereviews.com/Tyre-Tests/2025-Friction-and-Studded-Winter-Tyre-Test.htm>
* UTAC / Aftonbladet 2025 suve- ja lamellrehvitest, kajastus Tyre Reviews
  <https://www.tyrereviews.com/Tyre-Tests/2025-Summer-and-All-Season-Combined-Tyre-Test.htm>
* Teknikens Värld 2025 talverehvitest (20 rehvi, 235/45 R18, mõõdetud
  mustrisügavused), kajastus Tyre Reviews
  <https://www.tyrereviews.com/Tyre-Tests/2025-Studded-Friction-and-European-Winter-Tyre-Test.htm>
* Test World / Tyre Reviews — suve-, lamell- ja talverehvid 0-15 °C juures
  <https://www.tyrereviews.com/Article/Summer-All-Season-and-Winter-Tyres-Tested-at-0c-15c.htm>
* ADAC 2025 talve-, suve- ja lamellrehvitestid, kajastus Tyre Reviews
  <https://www.tyrereviews.com/Tyre-Tests/2025-ADAC-Winter-Tyre-Test.htm>
  <https://www.tyrereviews.com/Tyre-Tests/2025-ADAC-Summer-Tyre-Test.htm>
  <https://www.tyrereviews.com/Tyre-Tests/2025-ADAC-All-Season-Tyre-Test.htm>
* Rievaj, Vrábel, Hudák — Tire Inflation Pressure Influence on a Vehicle
  Stopping Distances, Int. J. Traffic and Transportation Engineering 2(2)
  <http://article.sapub.org/10.5923.j.ijtte.20130202.01.html>
* Influence of tire pressure on the vehicle braking distance (VW Passat B5,
  kuiv / märg / lumi, 1,0-3,0 bar)
  <http://www.aaejournal.com/Influence-of-tire-pressure-on-the-vehicle-braking-distance,155136,0,2.html>
* Effects of Tire Dynamics on Vehicle Safety, Machines 14(9):1002
  <https://doi.org/10.3390/machines14091002>
* NASA — rehvi akvaplaneerimise hüdrodünaamika (Horne)
  <https://ntrs.nasa.gov/api/citations/19660026826/downloads/19660026826.pdf>
* Autoportaal — Eesti kasutatud autode turg ja uute autode müük
  <https://autoportaal.ee/en/news/314/used-car-market-in-estonia-in-february-number-of-transactions-declined-but-bmw-remains-the-leader>
* AutoReport.ee — Eesti levinuimate kasutatud autode mudelijuhendid
  <https://autoreport.ee/en/mudelid>
* ERR / ACEA — Eesti sõidukipargi keskmine vanus
  <https://www.err.ee/1609258389/seisvad-autod-kergitavad-soiduki-keskmist-vanust-eestis-nelja-aasta-vorra>
* EPREL — EL-i rehviregister
  <https://eprel.ec.europa.eu/>

---

*Mudel annab hinnangu, mitte mõõtmistulemuse. Päris pidurdusmaa sõltub ka
katte konkreetsest tekstuurist, rehvi temperatuurist, pidurite seisukorrast
ja ABS-i häälestusest. Iga tulemus tuleb koos veapiiriga — kasuta seda.*

## 9. WordPressi teema (theme/pidurdusmaa)

Pidurdusmaa.ee toodanguversioon on WordPressi teema, mis **ei oma ühtegi
oma arvutust ega andmebaasi**. `build.py` genereerib teemale:

* `data/core.json`, `data/models.json`, `data/eprel/<MÕÕT>.json` —
  `export_wp.py`, samadest allikatest kui `web/data.js`
* `assets/js/engine.js` — sama fail, mis `web/engine.js` (paarsus: `parity.py`)

EPREL-i korjest kantakse nüüd edasi ka kütuseklass, müra dB ja klass.
Nad on ainult VÕRDLUSLEHE jaoks — pidurdusmudelisse nad ei lähe (vt 7g).

Leht ei näita omadusi, mida andmetes ei ole (juhitavus, mugavus,
kulumine, hind): seal on „Andmed puuduvad“. Märgisega rehvid on
klassi kaupa, mitte eraldi ribadena. Testitud rehv on tulemuste seas
ainult siis, kui sama mudel on EPREL-is kasutaja mõõdus olemas.

**Teadaolev lahtine küsimus, mille teema nähtavaks tegi:** mitu
märgise klassiga A testitud suverehvi (Primacy 5, Hakka Blue 3, Ziex
ZE320) on mõõdetud G-ga 1,47–1,49, ehk klassi A keskpunktist (1,60)
allpool. Kalkulaatoris paistab „Märgise klass A“ rida seetõttu parem
kui iga testitud A-klassi rehv. `CLASS_MID` on nominaalne, mõõtmata —
vt 7f pakkumine korjata 225/45 R17 ja 225/40 R18, et klassi keskpunkt
päriselt ära mõõta.
