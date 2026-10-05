/* Tõsta olemasolevad logifailid Supabase'i (ühekordne, ja ka hiljem, kui
 * Supabase oli vahepeal maas ja read jäid faili).
 *
 * Käivita SERVERIS (Coolify → rakendus → Terminal), kus on LOG_DIR ja
 * Supabase'i muutujad juba olemas:
 *
 *   node scripts/supabase-import.mjs          # näitab, mida teeks (ei muuda midagi)
 *   node scripts/supabase-import.mjs --tee    # impordib päriselt
 *
 * Pärast õnnestunud importi nimetatakse fail ümber (logi.jsonl →
 * logi.jsonl.imporditud-2026-10-05T…), et sama rida teist korda ei läheks.
 * Midagi ei kustutata.
 */
import { readFileSync, renameSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const DIR = process.env.LOG_DIR || join(process.cwd(), 'data');
const URL_ = String(process.env.SUPABASE_URL || '').trim().replace(/\/+$/, '');
const VOTI = String(process.env.SUPABASE_SECRET_KEY || '').trim();
const TEE = process.argv.includes('--tee');

if (!/^https:\/\//.test(URL_) || VOTI.length < 20) {
	console.error('SUPABASE_URL või SUPABASE_SECRET_KEY puudub.');
	process.exit(1);
}
const pais = { apikey: VOTI, 'Content-Type': 'application/json', Prefer: 'return=minimal' };
if (VOTI.startsWith('eyJ')) pais.Authorization = 'Bearer ' + VOTI;

const FAILID = {
	'logi.jsonl': {
		tabel: 'kasutuslogi',
		rida: (o) => ({ t: o.t, k: o.k ?? null, s: Number(o.s) || 0, e: String(o.e), v: o.v ?? null }),
		ok: (o) => o && o.t && typeof o.e === 'string'
	},
	'kontakt.jsonl': {
		tabel: 'kontakt',
		rida: (o) => ({ aeg: o.aeg || o.t, teema: o.teema ?? null, nimi: o.nimi ?? null, email: o.email ?? null, firma: o.firma ?? null, sonum: o.sonum ?? null }),
		ok: (o) => o && (o.aeg || o.t)
	}
};

for (const [fail, f] of Object.entries(FAILID)) {
	const tee = join(DIR, fail);
	if (!existsSync(tee)) {
		console.log(`${fail}: faili pole`);
		continue;
	}
	const read = [];
	let vigaseid = 0;
	for (const r of readFileSync(tee, 'utf-8').split('\n')) {
		if (!r.trim()) continue;
		try {
			const o = JSON.parse(r);
			if (f.ok(o)) read.push(f.rida(o));
			else vigaseid++;
		} catch {
			vigaseid++;
		}
	}
	console.log(`${fail}: ${read.length} rida → ${f.tabel}` + (vigaseid ? ` (${vigaseid} vigast jäeti vahele)` : ''));
	if (!TEE || !read.length) continue;
	for (let i = 0; i < read.length; i += 500) {
		const r = await fetch(`${URL_}/rest/v1/${f.tabel}`, { method: 'POST', headers: pais, body: JSON.stringify(read.slice(i, i + 500)) });
		if (!r.ok) {
			console.error(`  viga reast ${i}: HTTP ${r.status} — fail jäi alles, midagi ei nimetatud ümber`);
			process.exit(1);
		}
		process.stdout.write(`  ${Math.min(i + 500, read.length)}/${read.length}\r`);
	}
	const uus = `${tee}.imporditud-${new Date().toISOString().replace(/[:.]/g, '-')}`;
	renameSync(tee, uus);
	console.log(`\n  valmis → ${uus}`);
}
if (!TEE) console.log('\nProovijooks. Päriselt importimiseks: node scripts/supabase-import.mjs --tee');
