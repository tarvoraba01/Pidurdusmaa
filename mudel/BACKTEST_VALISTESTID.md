# Backtest välismaa rehvitestide vastu (2026-09-28)

## Andmed

`testid_ext/*.json`: 51 testi, ~1950 pidurdusmaad. Mudel ei ole ühtegi neist varem näinud.

| Allikas | Testid | Pinnad | Märkus |
|---|---|---|---|
| Auto Bild 2021–2025 | 15 | kuiv, märg, lumi | eelvooru (top-20 valiku) tulemused, reifenlab.de kaudu, ristkontrollitud |
| Za Rulem 2019–2022 | 7 | jää, lumi, märg, kuiv | ZR-i PDF-tabelitest, iga arv kontrollitud punktide valemiga |
| auto motor und sport, Auto Zeitung, sport auto, ACE/GTÜ/ARBÖ, Promobil | 13 | kuiv, märg, lumi | |
| evo, TÜV SÜD (Bridgestone'i tellitud), Quattroruote | 12 | kuiv, märg, lumi | |
| ADAC 2023–2024 | 4 | kuiv, märg, betoon | 2019–2022 avaldas ADAC ainult hindeid |
| Tyre Reviews, Vi Bilägare | 5 | | osal testidel kiirused teadmata, need jäävad välja |

**Välja jäetud:**

- 221 tulemust teadmata kiirusega.
- 60 tulemust, mis on allika enda poolt kahtlased või tuletatud (nt Auto Bild 2023 kuiv, mis oli kuiv+märg summa).
- Za Rulem 2008 rühmakeskmised. Neid kasutati ainult temperatuurikõvera kujuks, vt allpool.

**Ei saadud kätte:** tyrereviews.com (403), Tekniikan Maailma ja Vi Bilägare / Teknikens Värld (tasulised).

## Meetod

EPREL-i märgise klass leitakse rehvi nime ja testi mõõdu järgi, 67 % tulemustest. Seejärel arvutatakse kolm mõõdikut:

- **A. Märgise-režiim:** sama, mida leht teeb testimata rehviga.
- **B. Testisisene:** testi keskmine nihe eemaldatud. Näitab, kui hästi märgis seletab rehvide vahet.
- **C. Ülekanne:** sama rehv kahes eri testis.

Käivitamine: `python3 -m mudel.backtest_ext`

## Tulemused

**A. Märgise-režiim.** Viga on keskmine absoluutne. Katvus näitab, mitu protsenti mõõdetud tulemustest jääb lehe 1-sigma vahemikku (oodatav 68 %).

| Pind | Enne parandusi | Pärast | Nihe pärast | Katvus |
|---|---|---|---|---|
| Kuiv asfalt (n=394) | 4,8 % | 4,8 % | −0,2 % | 84 % |
| Märg asfalt (n=603) | 9,0 % | **8,0 %** | +1,4 % | 67 % |
| Lumi (n=228) | 10,3 % | **8,8 %** | −2,7 % | 80 % |
| Jää (n=67) | 35,5 % | **26,3 %** | +0,5 % | 45 % enne sigma muutust |

**B. Testisisene viga.**

- Kuiv 3,0 %, märg 4,5 %, lumi 2,7 %, jää 15,6 %.
- Testide omavaheline nihe (standardhälve) on märjal 10 % ja lumel 9 %. See ongi suurem osa absoluutveast: iga testi väljakul on oma haardetase.

**C. Ülekanne, kui testi nihe on teada.**

| Pind | Ainult märgis | Rehvi koht teisest testist |
|---|---|---|
| Kuiv | 3,1 % | 2,6 % (aitab) |
| Märg | 4,2 % | 4,7 % (**ei aita**: selle mõõdu märgis on parem kui teise mõõdu test) |
| Lumi | 2,0 % | 2,3 % (ei aita) |
| Jää | 19,3 % | 17,0 % (aitab) |

## Tehtud muudatused

Igaüks on tõendatud mitme sõltumatu testiga. 369 vanast ankrust ei muutunud ükski.

1. **Märgise klass → G (`g_class_measured.py`, `gklass_ext.py`).** Arvutatud sama meetodiga kui varem, aga päris EPREL-i märgistega ja 549 rehviga (enne 41).
   - Kontrollitud jäta-üks-test-välja meetodil: 8,99 % → 8,31 %.
   - Kesk-Euroopa talverehv: 8,0 % → 6,5 %, nihe −5,9 % → 0,0 %.
   - Klasside järjestus on kategooria sees tagatud: puuduv lahter võtab halvema klassi väärtuse.
2. **Naastrehv lumel: 0,345 → 0,39.**
   - Kuus sõltumatut testi mõõtsid KÕIK mudelist lühema pidurdusmaa, mediaan 0,88.
   - 0,39 juures on testide mediaan 0,95, ehk ennustus on endiselt ohutuse poole.
   - Viga 14,9 % → 8,1 %.
3. **Naastrehv külmal jääl (`ice_temp_exp_cold`, uus konstant).**
   - Za Rulem 2008 mõõtis samu rehve neljal temperatuuril. Naelutu rehv käitus −19 °C juures nagu kirjanduse kõver ütleb (1,75 ×), naastrehv vastupidi (0,78 ×).
   - Parandus on aste −0,43, mis kehtib ainult külmemal kui −5 °C. See klapib ka −13 °C punktiga.
   - Kontroll Za Rulem 2019 testiga (−22 °C): vana mudel ennustas 2,9 × liiga lühikese pidurdusmaa.
4. **Jää veapiir: 0,17 → 0,25.** Väljaspool valimit oli vanas vahemikus ainult 45 % tulemustest. Jää haare sõltub väljakust rohkem kui rehvist.
5. **Sõidutee jää (2026-09-29).** Kõik ülaltoodud jäänumbrid on testiväljaku jää kohta ja backtest jookseb endiselt selles režiimis (`ice_road=False`). Leht näitab aga nüüd **sõidutee jääd**: testiväljaku haare + 0,05 (`ice_road_add`).
   - Põhjus: ajakirjade jääväljak on sile ja hooldatud. Teel on jää rööbastatud, kare või liivatatud, osalt sile kiilasjää. VTI (1997) ja Statens vegvesen: kare jää või liiv lisab u 0,1. Pool teejääst eeldatakse kare → 0,05. See jaotus on **eeldus**, mitte mõõtmine.
   - Kontroll: Põhjamaade rehv −5 °C juures annab teel 0,25. Teehoolduse mediaan on 0,15–0,25 mõõturi skaalal, VTT T244 järgi u 0,19–0,32 füüsikaliselt.
   - Mõju Golf 8-le, 50 → 0 km/h, −5 °C: suverehv 137 → 83 m, Kesk-Euroopa talverehv 93 → 64 m, Põhjamaade 48 → 39 m, naast 37 → 31 m.
   - Seega on lehe jäänumbrid ajakirjade testidest **teadlikult lühemad**. Rehvilehe kast „Ajakirjade testid“ näitab testiväljaku tulemust.
6. **Rehvilehed.** Lehel on nüüd kast „Ajakirjade testid“: 264 rehvimudelit, 1245 mõõdetud tulemust (`export_testid.py`). Arvutus neid EI kasuta, sest märjal ei ennusta need paremini kui märgis (punkt C).

## Mis jäi lahtiseks

- **Põhjamaade naelutu rehv jääl:** mudel ennustab Za Rulemi väljakutel 50 % liiga pika pidurdusmaa. Testisid on kaks ja väljaku mõju ei saa eristada, seetõttu ei muudetud.
- **Kesk-Euroopa talverehv lumel 50 km/h:** mõõdetud ~6 % pikem, eriti Auto Bildi testides. ADAC-i 30 km/h ankrud klapivad. Võimalik, et põhjus on kiirusesõltuvus, aga kiirus on osa Auto Bildi testide puhul oletatud, seega ei muudetud.
- **Suverehv kuival:** −3,9 %, lamellrehv kuival +3,0 %. See jääb väljaku nihke piiresse.
- **Temperatuurid:** peaaegu kõik on oletatud (suvi 20 °C, talv 8 °C, lumi ja jää −5 °C). Ainult Za Rulem andis temperatuurivahemikud.
