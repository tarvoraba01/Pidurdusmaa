# Pidurdusmaa arvutuse QA-audit — lõpparuanne

Kuupäev: 2026-09-28. Ulatus: Pythoni mootor (`mudel/model.py`, tõe allikas),
veebimootor (`veeb/src/lib/engine.js`), lehe loogika (`veeb/src/lib/app.js`),
andmed (`core.json`, EPREL-i failid, `presets.py`).

Neli asja on hoitud lahus:

- **Tarkvara korrektsus**: kas kood teeb seda, mida kavatseti.
- **Matemaatiline järjepidevus**: kas valemid on sisemiselt kooskõlas.
- **Füüsikaline usutavus**: kas tulemus on füüsikaliselt võimalik.
- **Empiiriline valideerimine**: kas tulemus klapib mõõtmistega.

Mudelit ei ole numbrite ilustamiseks muudetud. Iga muudatus parandab tõestatud
viga, ja nende mõju mõõdetud ankrutele on allpool kirjas.

---

## A. Üldseis

**Tulemus: valmis kasutamiseks, teadaolevate piirangutega.**

| Kiht | Seis |
|---|---|
| Tarkvara korrektsus | Leitud 7 kriitilist viga, kõik parandatud ja testidega lukus. Python ↔ JS: 400 juhtumit on identsed (ka ehitatud lehe bundle'is, suurim erinevus 2·10⁻¹⁶). |
| Matemaatiline järjepidevus | Integraatori viga < 0,012 % (5–250 km/h). Pidurdusmaa kasvab kiirusega alati, märgise klasside järjestus peab alati, NaN-e ega negatiivseid tulemusi ei ole. |
| Füüsikaline usutavus | Üks sisuline viga parandatud: märg asfalt oli kuivast haardevam. Teadaolev ja lukustatud kõrvalekalle: vt G. |
| Empiiriline valideerimine | 369 ankrut, kõik pinnad on veapiiri sees (audit OK). Kiirusvahemik on ankrutega kaetud kitsalt (asfalt 80–100 km/h, lumi 30 km/h), ülejäänu on ekstrapolatsioon. |

## B. Kriitilised vead (kõik parandatud)

1. **Vaikne 60 s ajapiir.** Pikk pidurdus lõigati 60 s juures pooleli ja
   tulemus oli liiga lühike. Näiteks suverehv jääl 200 km/h juures andis
   1488 m, kuigi auto veel liikus.
2. **Võlts lõplik tulemus allamäge.** Aeglustuse põrand `max(0.05, a)` andis
   autole, mis tegelikult ei peatu (järsk langus jääl), lõpliku numbri
   (743 m, 910 m). Nüüd on tulemus `Infinity`, lisandub hoiatus „Auto ei
   peatu…“ ja usaldus on „madal“.
3. **Vigane sisend andis numbri.**
   - NaN, ∞ või negatiivne kiirus andis 0 m.
   - Negatiivne koorem viis kompleksarvuni ja arvutus jooksis kokku.
   - Mass 0 andis nulliga jagamise.
   - G = 0 andis 541 m.
   - Rehvimõõt „000/00 R00“ andis nulliga jagamise.
   - Piduri võimekus 0 andis 1215 m.
   - Negatiivne reaktsiooniaeg andis negatiivse kogumaa.

   Nüüd kontrollitakse iga sisendit (`validate_inputs` / `Pidurdus.validate`)
   ja vigane väärtus annab selge vea.
4. **Temperatuurikõver ekstrapoleeris.** Suverehv andis −40 °C juures
   kuival asfaldil mu 0,12. Nüüd hoitakse kõverat mõõdetud otspunktides.
5. **Kaldel puudus cos(θ).** Hõõrdejõud peab olema võrdeline normaaljõuga.
   10 % kallakul oli viga 0,5 %, 30 % kallakul 4 %.
6. **Märg haare oli kuivast suurem.** Talverehvil oli märg pidurdusmaa
   20–60 km/h juures kuni 11 % lühem kui kuiv. See on füüsikaliselt võimatu.
   - Parandus: märg haare ≤ sama rehvi täielik kuiv haare samas kohas.
   - Esimene versioon piiras haaret enne rõhu- ja mustriliiget ning jättis
     naastrehvile (Pirelli Ice Zero 2) 0,1 % vahe.
   - Lõplik versioon piirab funktsiooni lõpus, kutsudes sama funktsiooni
     kuiva teega.
7. **Sama rehv näitas eri lehel eri numbrit.** Tulemuste leht arvutas
   testitud rehvi testimõõduga, võrdluse leht autol oleva mõõduga (vahe kuni
   3,9 %). Nüüd arvutavad mõlemad autol oleva mõõduga (`size`), ja mõõdu
   ülekande veapiir tuleb testimõõdust (`gSize`). Kontrollitud brauseris:
   Nokian Hakka Blue 3 + Golf 8 + 90 km/h märg annab mõlemal lehel 41,7 m.

**Mõju mõõdetud ankrutele:** 369-st muutus 4, kõik talverehvi märjad ankrud
ja kõik viga väiksemaks:

| Ankur | Enne | Pärast |
|---|---|---|
| alpin5 asfalt | −5,32 % | −5,26 % |
| alpin5 betoon | −1,34 % | −1,28 % |
| ugp3 asfalt | −3,83 % | −3,77 % |
| ugp3 betoon | −0,53 % | −0,47 % |

## C. Andmete probleemid

Kontrollitud: 759 autot, 88 testitud rehvi ja 57 100 EPREL-i rida 844 failis.

- **Parandatud:** VW Transporter T6.1 ABS-klass MODERN → LATEST. Teiste
  sama aja kaubikutega oli see vastuolus.
- **Korras:**
  - Duplikaate ega tühje välju ei ole.
  - Võimatuid mõõte ega läbimõõte ei ole.
  - Võtmed on unikaalsed ja valija kombinatsioonid ei kattu.
  - Igal EPREL-i real on klass A–E ja kategooria 0–3.
- **Kontrollitud ja aktsepteeritud:**
  - 111 autol ei klapi ABS-klass algusaastaga. Kõik on põhjendatavad
    tootmisperioodi enamuse järgi, välja arvatud T6.1 (parandatud).
  - 1,7 baari rõhk Ladal, Moskvitšil ja GAZ-il on ajalooliselt õige.
  - Renault Masteri teljevahe 4,332 m on õige.
  - UAZ-i ja G-klassi CdA 1,75–1,79 on usutav.
- **Lünk:** 10 autol ei ole baasmõõdu kohta EPREL-i andmeid, nii et märgise
  klasside read jäävad tühjaks. Need autod on:
  - bmw_ix, bmw_ix1
  - toyota_lc_90, toyota_lc_100, toyota_lc_200, toyota_lc_250,
    toyota_aygo_x
  - honda_crv_2, civic_typer_fk8
  - citroen_c4_3
- **Vana tööriist oli katki:** `mudel/parity.py` luges vananenud faili
  `web/data.js` (573 autot) ja jooksis uute autode peal kokku. Asendatud
  failiga `parity_core.py`, mis loeb sama `core.json`-i, mida leht kasutab.

## D. Valemi probleemid

- **Parandatud:** vt B4, B5 ja B6.
- **Kontrollitud ja korras:**
  - Integraator (Euler, dt 0,004 s) klapib analüütilise lahendiga, viga
    < 0,012 %.
  - Kuival kasvab pidurdusmaa kiirusega umbes ruudus.
  - Mass mõjutab tulemust vähe, sest a ≈ μ·g. Koormustundlikkus ja
    õhutakistus annavad füüsikaliselt õige väikese mõju.
  - Kalle: ülesmäge lühem, allamäge pikem.
- **Lahtised küsimused (mitte vead):**
  - Veeretakistus liidetakse rehvi hõõrdele. Kalibreerimine neelab selle,
    aga see on topeltarvestuse risk, kui kalibreerimist kunagi muudetakse.
  - Haarde põrand on 0,03. Tavakasutuses see ei aktiveeru (audit 3: ükski
    klamber ei aktiveeru −30…+2 °C juures).

## E. Tehtud parandused (failid)

| Fail | Muudatus |
|---|---|
| `mudel/model.py` | `InputError`, `validate_inputs`, temperatuuriklamber, märg ≤ kuiv (funktsiooni lõpus), cos(θ), peatumistsükkel ilma põranda ja 60 s piirita (`stopped`, `inf`), `Tyre.g_size` |
| `veeb/src/lib/engine.js` | Samad parandused, `Pidurdus.validate`, tulemuses väli `stopped` |
| `veeb/src/lib/app.js` | `onCar()`: testitud rehv autol oleva mõõduga kõigil kolmel lehel (tulemused, simulatsioon, rehvileht) |
| `mudel/presets.py` | T6.1 ABS LATEST |
| `mudel/parity_core.py` | Uus paarsusfikstuuri generaator `core.json`-i pealt |
| `mudel/test_mudel.py` | Uus, 22 testi |
| `veeb/tests/engine.test.mjs` | Uus, 15 testi |
| `veeb/tests/parity_fixture.json` | 400 juhtumit Pythoni tulemustega |
| `veeb/package.json` | `npm test` |

## F. Tehtud testid

**Automaatsed testid (jäävad projekti):**

- `python3 -m unittest mudel.test_mudel`: 22/22 OK. Testiklassid:
  - Valem: integraator vs analüütiline lahend.
  - Sisend: vigane sisend annab vea.
  - Äärmus: ei peatu, pikk pidurdus, null kiirus.
  - Füüsika: kiirusega kasvav, pindade järjestus samal temperatuuril,
    G-järjestus, halvenemine pikendab, kalle.
  - Andmed.
  - Regressioon:

    | Olud | Tulemus |
    |---|---|
    | Golf kuiv 100 km/h | 36,644 m |
    | Golf märg 80 km/h | 32,785 m |
    | Golf lumi 50 km/h | 26,176 m |
    | Golf jää 50 km/h | 47,647 m |
- `cd veeb && npm test`: 15/15 OK, kestus ~18 min.
  - Paarsus Pythoniga.
  - Kõigi autode ja rehvide sisendikontroll.
  - Andmete terviklus.
  - Kõik 759 autot × 4 kategooriat × 3 klassi × 4 olu × 5 kiirust.
  - Äärmused ja füüsika.
- `python3 -m mudel.audit`, osad 1–4: kõik OK. Osa 5 (tundlikkus, väga
  aeglane) jäi seekord lõpuni jooksutamata. Muudatused seda ei mõjuta.

**Ühekordsed kontrollid:**

- **Maatriks enne parandusi:** 729 600 arvutust. Leidis B6 (1269 juhtu).
- **Maatriks pärast parandusi:** 910 800 arvutust (759 autot × 4
  kategooriat × 5 klassi × 4 olu + kuiv 10 °C × 12 kiirust).
  - 0 NaN-i, lõpmatut ega negatiivset tulemust; vahemik katab tulemuse alati.
  - 0 kohta, kus pidurdusmaa kiirusega ei kasva.
  - 0 märgise klasside järjestuse viga.
  - 0 kohta, kus kuiv oleks samal temperatuuril pikem kui märg.
  - Võrreldes vanaga muutus C-klassi tulemus ainult VW Transporteril (T6.1
    ABS-i parandus, 20–30 km/h kuni −8 %, 192 punkti). Kõigil teistel
    autodel on muutus 0,000 %: parandused puudutavad ainult äärmusi ja
    talverehvi A/B klassi madalal kiirusel.
- **Äärmuste rünnak (Python):** NaN, ∞, negatiivsed väärtused, nullid,
  võimatud mõõdud, 300 km/h, ±50 % kalle, −50…+60 °C. Selle käigus leitud
  B1–B5.
- **Leht:** `npm run build` õnnestus. SEO kontroll läbis 3992 lehte, turva
  kontroll leidis 0 saladust.
- **Brauser (Chromium, ehitatud leht):**
  - Avaleht, võrdlus, rehvileht ja `?olud=snow` link: 0 JS-viga, tekstis
    pole NaN, Infinity ega undefined.
  - Lehe bundle'i mootor annab paarsusfikstuuri 400 juhtumil sama tulemuse.
  - Sama rehv annab võrdlus- ja tulemuste lehel sama numbri.
- **Mõistlikkus ADAC-i vahemike vastu:**
  - Golf 8 kuiv 100→0 km/h: 36,6 m.
  - Golf 8 märg 80→0 km/h: 32,8 m.

## G. Jäävad riskid

Tähtsuse järjekorras:

1. **Märg ≥ lumi üle 110 km/h laiadel talverehvidel.**
   - Maatriksis 184 juhtu 910 800-st, kõik Põhjala talverehvid,
     120–130 km/h (157 neist 130 km/h juures), kõigis klassides A–E.
   - Mudel ennustab 1 mm vees osalist vesiliugu. See tugineb kahele
     eeldusele:
     - veesügavuse astendaja 0,42, mille ankrud on ~7,8 mm sügavuses vees;
     - laiuse astendaja 1,0, millel on üks allikas.
   - Füüsikaliselt võimalik, empiiriliselt kinnitamata.
   - Ma ei peitnud seda: test lukustab ulatuse (ainult talverehvid, ainult
     üle 110 km/h). Kui see hakkab levima, kukub test.
2. **Kiirusvahemik on suures osas ekstrapolatsioon.** Ankrud katavad kitsa
   ala, mujal on tulemus ekstrapolatsioon:

   | Pind | Ankrud | Lehel lubatud |
   |---|---|---|
   | Asfalt | 80–100 km/h | 40–130 km/h |
   | Lumi | 30 km/h | kuni 80 km/h |
   | Jää | 20–50 km/h | kuni 80 km/h |
   | Kobe lumi | puuduvad | – |
3. **Märgise klasside väärtused.**
   - Põhjala A/B ja Kesk-Euroopa talverehvi A on teiste kategooriate
     pealt ühendatud.
   - C ja D on peaaegu võrdsed (1,226 vs 1,225).
   - E on nominaalne, mõõtmisi ei ole.
4. **EPREL-i rehvid kuival, lumel ja jääl.** Tulemus on kategooria
   keskmine, sest märgis ei ütle nende olude kohta midagi. Leht ütleb seda,
   aga kasutaja võib seda lugeda rehvi omaduseks.
5. **Lehe eelseadete temperatuurid erinevad** (kuiv 15 °C, märg 10 °C).
   Talverehvil võib madalal kiirusel märg tulla kuni 0,8 % lühem kui kuiv
   (maatriksis 8750 punkti, kõik talverehvid, ≤ 100 km/h), ja põhjus on
   temperatuur, mitte pind. Mudel on õige, aga kõrvuti
   vaadates on see segadusttekitav.
6. **Veeretakistus on hõõrdele liidetud** (vt D).
7. **10 autol puuduvad EPREL-i andmed** baasmõõdu kohta. 130 autot on veel
   lisamata (`JARGMISED_AUTOD.md`).
8. **Surnud tagavara `app.js`-is.** `eprelTyre` vaikimisi klass C ei
   aktiveeru praegu kunagi, aga peidaks tulevase andmevea.

## H. Soovitatav järgmine valideerimine

1. **Märja ja lume piir suurel kiirusel.** Leida või tellida mõõtmisi
   laiadel Põhjala talverehvidel madalas vees (0,5–2 mm) 100–130 km/h
   juures. See kinnitab või lükkab ümber G1 ja veesügavuse astendaja.
2. **Kiirusankrud väljaspool 80–100 km/h.** Asfalt 40–60 ja 120–130 km/h,
   lumi 50–80 km/h, kobe lumi üldse. Kõige odavam allikas on ADAC-i ja
   Auto Bildi testid, kus on mitu algkiirust.
3. **Märgise klassimõõtmised.** Põhjala A/B ja E-klass, et asendada
   ühendatud ja nominaalsed väärtused.
4. **Naastrehv märjal vs kuival madalal kiirusel.** Kontrollida, kas lagi
   (märg = kuiv) on seal realistlik.
5. **Käivitada `mudel.audit` osa 5 (tundlikkus) lõpuni.** Kulub üle 30
   min.
6. **CI.** `npm test` ja `python3 -m unittest` iga pushi ette; paarsus-
   fikstuuri uuendada iga mudelimuudatuse järel
   (`python3 -m mudel.parity_core`).
7. **Kaaluda eelseadete ühtlustamist.** Kuiv ja märg samal temperatuuril
   või temperatuur lehel nähtavaks (G5). See on toote otsus, mitte
   mudeliviga.
