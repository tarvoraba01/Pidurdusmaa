# Pidurdusmaa — WordPressi teema

Pidurdusmaa.ee avaleht, pidurdusmaa kalkulaator, rehvivõrdlus, rehvilehed, testid.

## Paigaldus

1. Lae `pidurdusmaa-theme.zip` üles: **Välimus → Teemad → Lisa uus → Lae teema üles**, ja aktiveeri.
2. Aktiveerimisel luuakse lehed **Avaleht** ja **Teadmine** (+ „Kuidas pidurdusmaa arvutatakse“, „EL-i rehvimärgis“), püsiviited seatakse ise. Blogi ei ole; WordPressi muutmata näidispostitus ja -leht viiakse prügikasti. Olemasolevaid samanimelisi lehti ei kirjutata üle.
3. **Asenda hero pilt:** Välimus → Kohanda → Avalehe hero. Praegune pilt on ajutine — kärbitud sinu kujunduskavandist, madala resolutsiooniga. Soovitus: auto märjal teel, tume taust, vähemalt 1200 × 1200 px, auto keskel-vasakul.

Vajab: WordPress 6.4+, PHP 8.0+. Pluginaid ei vaja.

## URL-id

| URL | Leht |
|---|---|
| `/` | Avaleht = pidurdusmaa kalkulaator + tulemus (`/pidurdusmaa/` suunab siia) |
| `/rehvi-valimine/` | Vali rehv enda tingimuste järgi: kus/kui palju sõidad, mis on oluline → järjestus + põhjused |
| `/vordle-rehve/` | Valitud 2–4 rehvi kõrvuti tabelis |
| `/rehvid/` | Mõõdud, testitud rehvid, margid |
| `/rehvid/205-55-r16/` | Ühe mõõdu kõik rehvid |
| `/rehvid/continental-premiumcontact-7/` | Rehvileht |
| `/rehvid/a-vs-b/` | Ainult kahe **samas testis** olnud rehvi jaoks, muidu 404 |
| `/testid/`, `/testid/adac25/` | Testid |
| `/teadmine/…` | Tavalised WP lehed |

Sitemap: `/wp-sitemap.xml` (WP tuum + teema pakkuja). Indekseeritakse ainult lehed, millel on unikaalset sisu: testitud rehvid, EPREL-i mudelid vähemalt 3 mõõdus, mõõdud vähemalt 10 mudeliga. Ülejäänud rehvilehed on `noindex, follow`.

## Kust andmed tulevad

Teema **ei oma andmeid ega arvutust**. Kõik tuleb samast projektist, kust varasem kalkulaator:

```
pidurdus/ (Python)                          theme/pidurdusmaa/
  presets.py, anchors*.py      ─┐
  eprel_tyres.json  (EPREL)     ├─ export_wp.py ─→ data/core.json
                                │                  data/models.json
                                │                  data/eprel/<MÕÕT>.json
  model.py ─ export_web.py ─→ web/engine.js ──copy──→ assets/js/engine.js
```

`python3 build.py` teeb kõik korraga. Mootor on sama fail, mille paarsust Pythoniga kontrollib `pidurdus/parity.py`.

**EPREL-i API võti ei ole teemas.** Korje jookseb ehituse ajal sinu masinas (`eprel_harvest.py`), teema saab ainult tulemuse. Uute mõõtude lisamiseks: korja → `eprel_convert.py` → `build.py` → lae teema uuesti üles (või asenda ainult `data/` kaust).

## Mida leht näitab ja mida mitte

| Omadus | Allikas |
|---|---|
| Märghaardumine, veeretakistus, müra, lume- ja jäämärk | Ametlik (EPREL), sinu mõõdus |
| Märja/kuiva/lume/jää pidurdusmaa testis, akvaplaneering | Sõltumatu test (88 rehvi) |
| Pidurdusmaa sinu autoga | Arvutus |
| Juhitavus, mugavus, kulumine, hind | **Andmed puuduvad** — leht ütleb seda, ei arva |

Märgisega (testimata) rehve ei näidata eraldi ribadena — sama klassi rehvid on mudelis identsed, seepärast näidatakse klassi rida koos arvuga. Kuival, lumel ja jääl järjestatakse ainult rehve, mille see pind on päriselt mõõdetud.

## Failid

```
functions.php            seadistus, skriptid, menüü, kohandaja
inc/data.php             JSON-failide lugemine (objektipuhvriga)
inc/routes.php           virtuaalsed URL-id, 404, body class
inc/seo.php              pealkirjad, kirjeldus, canonical, robots, JSON-LD
inc/sitemap.php, vs.php  sitemap ja "vs" paarid
inc/setup-content.php    aktiveerimisel loodavad lehed
front-page.php           avaleht
template-parts/          kalkulaatori kaart, tulemus, "Kuidas arvutatakse"
templates/               /rehvi-valimine, /vordle-rehve, /rehvid, rehv, mõõt, vs, testid
assets/js/app.js         kasutajaliides (ei sisalda füüsikat)
assets/js/engine.js      GENEREERITUD — ära muuda käsitsi
data/                    GENEREERITUD — ära muuda käsitsi
assets/fonts/            Inter, Barlow Condensed (OFL), oma serveris — Google'i päringuid ei ole
```
