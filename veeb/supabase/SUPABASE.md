# Supabase — seadistamine

Mis läheb Supabase'i (kõik, mida server jooksvalt kirjutab või hoiab):

| Tabel | Mis | Enne |
|---|---|---|
| `kasutuslogi` | anonüümne kasutuslugu | `LOG_DIR/logi.jsonl` |
| `kontakt` | kontaktivormi kirjad (kustuvad 12 kuu pärast) | `LOG_DIR/kontakt.jsonl` |
| `pakkumised_hetktommis` | rehvivahetus.ee puhver, taastub restardil | ainult RAM |
| `hinnaajalugu` | rida iga hinnamuutuse kohta | polnud |
| `seis` | IndexNow: mis aadressid on teatatud | `LOG_DIR/indexnow.json` |
| `supabase-free-failsafe` | `write_count` +1 kord nädalas | — |

Rehvide ja autode põhiandmed (`static/data/*.json`) jäävad ehitusse: neist
tehakse ehitusel 7763 valmis lehte (kiirus + Google).

## 1. Projekt
1. supabase.com → New project. **Region: Central EU (Frankfurt)** — privaatsusteade ütleb nii.
2. SQL Editor → kleebi `supabase/schema.sql` → Run.
3. Project Settings → API Keys: kopeeri **Project URL**, **secret** võti ja **publishable** võti.

## 2. Coolify (server)
Environment Variables:
```
SUPABASE_URL=https://<projekt>.supabase.co
SUPABASE_SECRET_KEY=<secret võti>
```
Redeploy. Kontroll: `curl -H "Authorization: Bearer $ADMIN_KEY" https://pidurdusmaa.ee/api/integratsioonid/olek`
→ `supabase.sees: true`, `failsafe.writeCount` on number.

Olemasolevad logifailid üle (Coolify → Terminal):
```
node scripts/supabase-import.mjs        # proovijooks
node scripts/supabase-import.mjs --tee  # päriselt
```

## 3. GitHub (sõltumatu failsafe)
Repo → Settings → Secrets and variables → Actions:
```
SUPABASE_URL              https://<projekt>.supabase.co
SUPABASE_PUBLISHABLE_KEY  <publishable võti>
```
Actions → „Supabase failsafe" → Run workflow (esimene test).
Edaspidi käib ise E ja N 06:17 UTC.

## Kuidas failsafe töötab
- `failsafe_bump()` kirjutab alati (uuendab `uuendatud`) ja tõstab `write_count`'i +1, kui ISO nädal on vahetunud.
- Server kutsub seda käivitumisel ja iga 24 h; GitHub Actions 2× nädalas.
- Avaliku võtmega saab kutsuda ainult seda funktsiooni — tabeleid ei näe (RLS).

## Kui Supabase on maas
Kõik töötab edasi: logiread lähevad faili (`LOG_DIR`), hinnad tulevad RAM-ist.
Hiljem saab failid `supabase-import.mjs`-iga üle tõsta.
