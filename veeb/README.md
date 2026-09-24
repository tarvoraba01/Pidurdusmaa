# Pidurdusmaa.ee — sait (SvelteKit, staatiline)

Kogu sait ehitatakse **päris HTML-failideks** — 5948 aadressi, igaüks oma
fail. Käitamisel ei ole PHP-d, andmebaasi, API võtmeid ega keskkonnamuutujaid:
nginx serveerib valmis faile.

```
npm install
npm run build      # → build/ (5948 lehte + sitemap.xml)
npm run preview    # kohalik eelvaade
```

## Miks staatiline

Saidi väärtus on selles, et iga rehv ja iga mõõt on Google'i jaoks **oma
leht** omaenda pealkirja, kirjelduse ja sisuga. Seepärast renderdatakse
kõik ehituse ajal ära; brauseris käivitub peale selle kalkulaator ja
rehvide võrdlus (`src/lib/app.js`), aga lehe sisu on olemas ka ilma
JavaScriptita.

## Kaustad

| Tee | Sisu |
|---|---|
| `src/routes/` | lehed — `+page.svelte` (vaade), `+page.server.js` (andmed ehituse ajal) |
| `src/lib/server/andmed.js` | andmekiht: loeb `static/data/*.json` (ainult ehituse ajal) |
| `src/lib/util.js` | vormindus ja tabelid (töötab ka brauseris) |
| `src/lib/engine.js` | arvutusmootor — `pidurdus/model.py` port, paarsust kontrollib `parity.py` |
| `src/lib/app.js` | kalkulaator, rehvide nimekiri, võrdlus, anonüümne kasutuslugu |
| `static/data/` | andmed: `core.json`, `models.json`, `eprel/<MÕÕT>.json` |

Andmed genereerib Python: `python3 -m mudel.export_wp` ja `export_web`.
Siin neid käsitsi ei muudeta.

## Aadressid

```
/                                  kalkulaator (avaleht)
/rehvid/                           mõõdud, testitud rehvid, margid
/rehvid/205-55-r16/                ühe mõõdu kõik rehvid
/rehvid/<rehv>/                    rehvileht (märgis + testid)
/rehvid/<a>-vs-<b>/                kaks rehvi samas testis
/rehvi-valimine/  /vordle-rehve/   valik ja võrdlus
/testid/  /testid/<kood>/          sõltumatud testid
/teadmine/…  /kasutustingimused/  /kontakt/
/sitemap.xml  /robots.txt
```

`/rehvid/[slug]` on üks marsruut kolme lehetüübi jaoks — järjekord loeb,
sest mõne rehvi nimes ENDAS on „vs" (`maxxis-vs-ev`).

## Docker / Coolify

```
docker build -t pidurdusmaa .
docker run -p 8080:80 pidurdusmaa
```

- Port: **80**, healthcheck `/`
- Keskkonnamuutujaid ei ole vaja, `.env` faili ei ole
- Püsivat ketast (volume) ei ole vaja — sait on ainult lugemiseks
- Võrku on vaja ainult ehituse ajal (npm)
- Kui ehitus katkeb veaga `EMFILE: too many open files`, anna ehitusele
  rohkem faile: `docker build --ulimit nofile=65535 …`

## Mida veel teha

- **Kontaktivorm** vajab endpoint'i (praegu avab kasutaja e-posti programmi).
- **Kasutuslugu** (`PM_CFG.track`) on välja lülitatud; sisse lülitamiseks
  on vaja aadressi, kuhu sündmused saata.
- **Hinnad** (`PM_CFG.prices`) — rehvimüüjate API, praegu ühendamata.
