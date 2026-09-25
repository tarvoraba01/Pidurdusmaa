# Rehvipakkujate API-d (hinnad, pildid, poe lingid)

Siia tulevad kõik välised rehvi-API-d. Kogu kaust on `$lib/server/` all —
SvelteKit **keelab** selle importimise brauseri koodis ja ehitus katkeb, kui
keegi seda proovib. Võtmed ei jõua kunagi brauserisse ega GitHubi.

## Kuidas see töötab

```
brauser ──► /api/hinnad?moot=22540R18 ──► koond.js ──► pakkujad/*.js ──► pakkuja API
                                            │  (võti ainult serveris, päises)
                                            ├─ sobitus.js: „MICHELIN PILOT SPORT 5 225/40 ZR18 92Y XL“
                                            │             → meie rehv michelin-pilot-sport-5 @ 22540R18
                                            └─ vahemalu.js: sama mõõt 1 h mälus (pakkujat ei koormata)
brauser ◄── { hinnad: { "michelin-pilot-sport-5@22540R18": [{ myyja, hind, url, laos }] } }
```

Kalkulaator ja võrdlus küsivad hindu juba praegu `/api/hinnad`-st — kui
pakkujaid pole, tuleb `{available:false}` ja lehel hinda ei näidata.
Rehvi lehel küsitakse `/api/rehv/<slug>/`; kui pakkujal on pilt, asendab see
joonistatud rehvi (pilt tuleb läbi `/api/pilt/<slug>`, mitte otse pakkujalt).

## Uue pakkuja lisamine (3 sammu)

1. Kopeeri `pakkujad/_mall.js` → `pakkujad/rehvipood.js`, muuda `id`, `nimi`,
   `hostid`, `poeHostid`, `env` ja `hinnadMoodus()` pakkuja API kuju järgi.
   Valikuline: `pilt(slug, ctx)`, kui pakkujal on eraldi pildiotsing.
2. Lisa see `pakkujad/index.js` nimekirja.
3. Coolifys: `PAKKUJA_REHVIPOOD_URL` ja `PAKKUJA_REHVIPOOD_VOTI` → Redeploy.
   Kontroll: `curl -H "Authorization: Bearer $ADMIN_KEY" https://pidurdusmaa.ee/api/integratsioonid/olek`

Pakkuja on sees ainult siis, kui KÕIK tema `env` muutujad on seatud.

## Kaitse

| Oht | Kaitse |
|---|---|
| Võti lekib brauserisse | `$lib/server` + `$env/dynamic/private`; ehituse lõpus `scripts/turva-kontroll.mjs` |
| Võti lekib logidesse | võti ainult päises; veateadetes URL ilma päringuosata; olekulehel ainult muutujate NIMED |
| Keegi kasutab meie serverit teiste saitide ründamiseks (SSRF) | päringud ainult pakkuja `hostid` aadressidele, ainult https, suunamised kontrollitakse uuesti |
| Rünnak / koormus | sagedusepiir IP kohta (hinnad 60/min, pildid 120/min), sisendi range kontroll, vahemälu |
| Pakkuja saadab prügi | hind 5–5000 €, mõõt peab klappima, lingid ainult pakkuja poe domeenile |
| Pilt on tegelikult skript | lubatud ainult jpeg/png/webp/avif, kuni 3 MB, `CSP: default-src 'none'`, `nosniff` |
| Pakkuja on maas | vana vastus kuni 24 h, muidu lihtsalt ilma hinnata; ülejäänud sait töötab |

## Testimine kohapeal

`pakkujad/naidis.js` loeb hinnad JSON-failist (`PAKKUJA_NAIDIS_FAIL=/tee/fail.json`).
**Live-lehel seda muutujat ära sea** — need on väljamõeldud hinnad.
