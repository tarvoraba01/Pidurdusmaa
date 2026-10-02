# Rehvivahetus.ee partner API — ühendamise plaan

Staatus: ehitatud (`pakkujad/rehvivahetus.js`). Käivitub, kui Coolifys on `PAKKUJA_REHVIVAHETUS_URL` ja `PAKKUJA_REHVIVAHETUS_VOTI`.
Andmed hoitakse serveri mälus (kataloog laetakse käivitumisel ja iga 6 h); PocketBase ei ole selleks vajalik.
Kontroll: `curl -H "Authorization: Bearer $ADMIN_KEY" https://pidurdusmaa.ee/api/integratsioonid/olek`

Sidumine (test 02.10.2026, 2349 toodet): meie mõõtudes 2299, neist meie rehviga seotud ~1570 (68%).
Seostamata on peamiselt brändid, mida meie andmetes pole (Nordexx, General Tire, Landspider) ja
naastrehvid, millel EL-i märgist pole (seotakse ainult testitud naastrehvidega).

## API
- `GET https://partner.rehvivahetus.ee/api`
- Parameetrid: `output=json`, `in_stock=1`, `brand`, `limit`, `offset`, `key`, `format_output=1` (ainult XML).
- Mõõdu järgi filtrit EI ole → tõmba kogu kataloog lehekaupa (`limit`/`offset`).
- Võti käib URL-i parameetris `key` → täis-URL-i EI TOHI logida ega brauserisse saata.
- `POST /api/checkout` (tellimused) on KEELATUD. Kasutame ainult lugemist.
- Viga võib tulla HTTP 200-ga → kontrolli alati vastuse `status` välja. Vea korral jäta eelmised andmed alles.
- Timeout kohustuslik.

## Väljad
`id, code, brand, name, size ("205/55 R16"), size_inch, size_width, size_ratio, season ("Talv"/"Suvi"), mode, car_type, eu (EL märgis, nt "C B B (70 dB)"), notes, is_sc, is_cs, is_sil_sct (müra), is_ssr_rof (run-flat), lisi ("94T XL FR"), img (HTTPS), stock, price, mass`

Hind:
- ilma võtmeta `price` = tavahind;
- võtmega JSON-is `price` = partnerhind (−22%) ≈ e-poe hind (käibemaksu ja keskkonnatasuga);
- võtmega XML-is `price` = tavahind ja `client_price` = partnerhind.

Lehel näidata partnerhinda kujul „u X €“ (e-poe allahindlused erinevad brändi kaupa veidi).
Kontroll: Sailun IceBlazer Arctic 2 205/55R16 — tavahind 80 €, partnerhind 62,40 €, e-poes 61,60 €.

Portaali tüübid: Suverehv / Lamell / Lamell SC / Naast → meie kategooriad summer / winter / naast.

## E-poe lingid
- Mõõdu nimekiri (carType 1 = sõiduauto/maastur, 2 = kaubik; lehed /page/N/): `https://www.rehvivahetus.ee/?s=tires&carType=1&tireWidth=205&tireHeight=55&tireDiameter=16`
- Toote leht: `https://www.rehvivahetus.ee/product/<e-poe nr>/` — see nr ≠ API `id`/`code`.
  Seotud (`loeKaardid`, `lisaTooteLingid`): e-poe mõõdu nimekirja lugemisega (tootja + mudel + indeks). Viisakalt: ainult vajalikud mõõdud,
  paar korda päevas, pausidega, User-Agent sisaldab „Pidurdusmaa.ee“.
- Kõik lingid läbi `poeLink()` (lib/app.js) → UTM.

## Plaan
1. PocketBase (Coolify teenus, püsiv köide): kollektsioonid pakkumistele ja piltidele. Env: `PB_URL`, `PB_ADMIN_EMAIL`, `PB_ADMIN_PASS`.
2. Serveri sünk 2–4× päevas.
3. Sidumine meie rehvidega: tootja + mudel (normaliseeritud) + mõõt + LI/SI + EL märgis.
4. Rehvi kaardile: „u X € · rehvivahetus.ee · laos N tk · Vaata poes →“, pilt. Pingerida EI muutu.
5. Plausible: `Poe klikk`, pood = rehvivahetus.ee.

## Reeglid
- Lehel ja koodis nimi „rehvivahetus.ee“, mitte isikunimi.
- Awini osa võib koodist eemaldada.
