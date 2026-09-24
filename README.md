# Pidurdusmaa.ee

Eestikeelne leht, mis näitab, kui pika maa pealt auto peatub — konkreetse
auto, rehvi, kiiruse ja teeoluga. Andmed tulevad EL-i rehvimärgiselt
(EPREL) ja avalikest sõltumatutest testidest; arvutuse teeb üks mudel,
mida kasutavad nii serveripool kui brauser.

**Repo on privaatne.** Siin ei ole ega tohi olla ühtegi API-võtit ega
parooli — vt [Saladused](#saladused).

---

## Mis kaustas mis on

| Kaust | Sisu |
|---|---|
| `mudel/` | Python: füüsikamudel, kalibreerimine, EPREL-i teisendus, eksport |
| `teema/pidurdusmaa/` | WordPressi teema — **terve sait**, koos andmefailidega |
| `eelvaade/` | Ühe failina eelvaate ehitus (Pagelive) ja brauseritestid |
| `tooriistad/` | EPREL-i korjeskriptid (jätkatavad, 3 lõime) |

### `mudel/`

- `model.py` — pidurdusmaa arvutus. Ainus koht, kus on füüsikakonstandid.
- `presets.py`, `vehicles_ee.py` — autod (mark, mudel, põlvkond, mass, ABS-i põlvkond).
- `oem_sizes.py` — 424 auto tehasemõõdud, igaühel allikalink ja kindluse märge.
- `eprel_convert.py` — EPREL-i read → mudeli rehviobjektid.
- `kalibreeri_gklass.py` → `g_class_measured.py` — märgise klassi (A–E)
  esindusväärtus MÕÕDETUD rehvide mediaanina, kategooria kaupa.
- `calibrate_*.py`, `anchors_*.py` — kalibreerimine avalike testide vastu.
- `audit.py` — läbiv kontroll (peab lõppema "AUDIT LÄBITUD").
- `parity.py` — kontroll, et JS-mootor annab sama tulemuse mis Python.
- `export_wp.py`, `export_web.py` — andmefailide genereerimine teema jaoks.

### `teema/pidurdusmaa/`

Klassikaline WordPressi teema. Kogu sait (5948 aadressi) tekib
virtuaalsetest marsruutidest — WordPressi postitusi ega lehti nende
jaoks ei ole.

- `inc/routes.php` — virtuaalsed aadressid (`/rehvid/205-55-r16/`,
  `/rehvid/<rehv>/`, `/rehvid/<a>-vs-<b>/`, `/testid/…`).
- `data/core.json` — autod, testitud rehvid, allikad, klassitabel.
- `data/eprel/<MÕÕT>.json` — märgise andmed mõõdu kaupa (laetakse vajadusel).
- `assets/js/engine.js` — `model.py` port. Muudad ühte, pead muutma teist
  ja `parity.py` peab läbi minema.
- `assets/js/app.js` — liides, ja `Track` — anonüümne kasutuslugu.

### `eelvaade/`

`crawl_bfs.py` kroolib kohaliku WordPressi läbi ja `build2.py` paneb kõik
ühte HTML-faili (gzip + base64, 64 sorteeritud kildu, kahendotsing).
See on testversioon Pagelive'i jaoks, mitte päris sait — otsingumootorid
seda ei indekseeri.

---

## Kuidas uuesti ehitada

```bash
# 1) andmed teema jaoks
python3 -m mudel.export_wp
python3 -m mudel.export_web

# 2) kontrollid
python3 -m mudel.audit      # peab ütlema: AUDIT LÄBITUD
python3 -m mudel.parity     # JS ja Python peavad kokku langema

# 3) eelvaatefail (kohalik WP peab jooksma pordil 8080)
python3 eelvaade/crawl_bfs.py
TAGASISIDE_URL="<google forms link>" python3 eelvaade/build2.py
```

---

## Saladused

EPREL-i API võti **ei ole** ja ei tohi olla üheski selle repo failis.

- `mudel/eprel_key.py` loeb võtme käivitamisel kohalikust failist, hoiab
  seda ainult mälus ega trüki seda kunagi.
- Võti käib ainult päise `X-API-KEY` sees — mitte kunagi URL-is, sest
  URL-id jõuavad logidesse ja puhvritesse.
- Enne iga commit'i tasub üle vaadata, et uus fail ei sisalda võtit,
  parooli ega andmebaasi ligipääsu.

## Andmete päritolu

- EPREL — Euroopa Komisjoni tooteregister, EL-i rehvimärgise ametlikud andmed.
- ADAC, Tekniikan Maailma, UTAC, Vi Bilägare — avalikud sõltumatud testid.
- UNECE R117 — märgise mõõtmismetoodika.
- Tehasemõõdud — tootjate juhendid ja avalikud andmebaasid, iga rida oma
  allikaviitega `oem_sizes.py`-s.

Lehel näidatakse arvutatud hinnangut, mitte mõõtmistulemust. Iga arv on
seotud sellega, kust ta tuli.
