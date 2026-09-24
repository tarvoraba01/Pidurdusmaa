# Pidurdusmaa.ee — sait (SvelteKit, adapter-node)

Kõik 5948 aadressi renderdatakse **ehituse ajal** valmis HTML-iks; Node
server annab need välja ja teenindab lisaks kaht otspunkti (kontaktivorm
ja anonüümne kasutuslugu). Andmebaasi ei ole — andmed on JSON-failides,
kirjad ja logi JSONL-failides.

```
npm install
npm run build      # → build/ (5948 lehte + sitemap.xml)
npm run preview    # kohalik eelvaade
```

## Miks eelrenderdatud

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

## Otspunktid

| Aadress | Mida teeb |
|---|---|
| `POST /api/kontakt` | kontaktivorm → `data/kontakt.jsonl` (+ teade, kui `TEADE_URL` on seatud) |
| `POST /api/logi` | anonüümne kasutuslugu → `data/logi.jsonl` |
| `GET /api/kokkuvote?key=…&paevi=7` | koondstatistika: mida kõige rohkem tehti |

Kontaktivorm saadab **JSON-i**, mitte vormi: SvelteKit blokeerib
teiselt saidilt tulevad vormipostitused ja JSON on sellest reeglist väljas.

## Keskkonnamuutujad

Kõik on **valikulised** — ilma nendeta sait töötab, ainult kirjad jäävad
faili ja statistika otspunkt on kinni.

| Muutuja | Mille jaoks |
|---|---|
| `PORT` | vaikimisi 3000 |
| `LOG_DIR` | kuhu kirjutatakse kirjad ja logi (vaikimisi `./data`) |
| `TEADE_URL` | aadress, kuhu POSTitatakse teade uuest kirjast (Discord/Slack webhook, n8n vms) |
| `STATS_KEY` | võti `/api/kokkuvote` jaoks; seadmata = otspunkt on välja lülitatud |
| `IP_SALT` | sool IP-räside jaoks (seadmata = juhuslik iga käivitusega) |
| `ORIGIN` | avalik aadress, nt `https://pidurdusmaa.ee` — vaja pöördproksi taga |

Isikuandmeid ei salvestata: IP-st hoitakse ainult soolatud räsi ja sedagi
ainult sagedusepiiri jaoks.

## Docker / Coolify

```
docker build --ulimit nofile=65535 -t pidurdusmaa .
docker run -p 3000:3000 -v pidurdusmaa-data:/app/data pidurdusmaa
```

- Port: **3000**, healthcheck `/`
- **Volume `/app/data`** — siin on kontaktikirjad ja kasutuslogi. Ilma
  selleta kaovad need iga uue versiooniga.
- Pöördproksi taga seatakse `ORIGIN=https://pidurdusmaa.ee`
- Võrku on vaja ainult ehituse ajal (npm)
- Kui ehitus katkeb veaga `EMFILE: too many open files`, anna ehitusele
  rohkem faile: `docker build --ulimit nofile=65535 …`

## Mida veel teha

- **E-kiri**. Praegu jõuab kiri faili ja valikulisse `TEADE_URL`-i.
  Otse e-postile saatmiseks lisa nodemailer ja asenda `src/lib/server/post.js`.
- **Hinnad** (`PM_CFG.prices`) — rehvimüüjate API, praegu ühendamata.
