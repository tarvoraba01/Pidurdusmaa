/* Supabase (Postgres) REST-klient — ilma lisateegita, ainult fetch.
 *
 * Coolify → Environment Variables:
 *   SUPABASE_URL         = https://<projekt>.supabase.co
 *   SUPABASE_SECRET_KEY  = salajane võti (sb_secret_… või vana service_role JWT)
 *
 * Kui muutujaid pole, on Supabase välja lülitatud ja kõik töötab vanaviisi
 * (failid LOG_DIR kaustas). Kõik vead on pehmed: leht töötab edasi.
 *
 * TURVA: see fail on kaustas src/lib/server — SvelteKit ei lase seda
 * brauserisse. Võtit ei logita kunagi; veateates on ainult tabeli nimi ja
 * HTTP kood.
 */
import { env } from '$env/dynamic/private';

const aadress = () => String(env.SUPABASE_URL || '').trim().replace(/\/+$/, '');
const voti = () => String(env.SUPABASE_SECRET_KEY || '').trim();

/** Kas Supabase on seadistatud? */
export const sbSees = () => /^https:\/\//.test(aadress()) && voti().length > 20;

function pais(lisa = {}) {
	const k = voti();
	const h = { apikey: k, 'Content-Type': 'application/json', ...lisa };
	/* vana service_role võti on JWT ja vajab ka Authorization päist;
	   uus sb_secret_… võti töötab ainult apikey päisega */
	if (k.startsWith('eyJ')) h.Authorization = 'Bearer ' + k;
	return h;
}

/**
 * Üks REST-päring. tee = 'kasutuslogi', 'kontakt?aeg=lt.2025-01-01', 'rpc/failsafe_bump' …
 * Viskab vea, kui vastus pole 2xx — kutsuja otsustab, mis edasi.
 */
export async function sb(tee, { method = 'GET', body, prefer, aegMs = 8000 } = {}) {
	if (!sbSees()) throw new Error('supabase: pole seadistatud');
	const ac = new AbortController();
	const taimer = setTimeout(() => ac.abort(), aegMs);
	const tabel = String(tee).split('?')[0];
	try {
		const r = await fetch(aadress() + '/rest/v1/' + tee, {
			method,
			headers: pais(prefer ? { Prefer: prefer } : {}),
			body: body === undefined ? undefined : JSON.stringify(body),
			signal: ac.signal
		});
		if (!r.ok) {
			/* vastuse tekst võib sisaldada päringu kaja — ainult lühike puhastatud osa */
			const t = (await r.text().catch(() => '')).replace(/[^\p{L}\p{N} .,:;()_"'-]/gu, ' ').slice(0, 160);
			throw new Error(`supabase ${method} ${tabel}: HTTP ${r.status} ${t}`.trim());
		}
		if (r.status === 204) return null;
		const s = await r.text();
		return s ? JSON.parse(s) : null;
	} catch (e) {
		if (e.name === 'AbortError') throw new Error(`supabase ${method} ${tabel}: aeg sai täis`);
		throw e;
	} finally {
		clearTimeout(taimer);
	}
}

/** Lisa read tabelisse (kuni 500 korraga). */
export async function lisa(tabel, read) {
	const list = Array.isArray(read) ? read : [read];
	for (let i = 0; i < list.length; i += 500) {
		await sb(tabel, { method: 'POST', body: list.slice(i, i + 500), prefer: 'return=minimal' });
	}
}

/** Lisa või asenda rida primaarvõtme järgi. */
export async function upsert(tabel, rida) {
	await sb(tabel, { method: 'POST', body: rida, prefer: 'resolution=merge-duplicates,return=minimal', aegMs: 20000 });
}

/** Andmebaasi funktsioon (Postgres function) → tulemus. */
export async function rpc(nimi, args = {}, aegMs = 15000) {
	return sb('rpc/' + nimi, { method: 'POST', body: args, aegMs });
}

/* ---- Failsafe -------------------------------------------------------------
 * Supabase'i tasuta projekt pannakse pausile pärast 7 päeva vaikust.
 * failsafe_bump() kirjutab tabelisse "supabase-free-failsafe" ja suurendab
 * write_count'i +1 kord ISO nädalas. Server kutsub seda käivitumisel ja
 * iga 24 h; GitHub Actions eraldi 2× nädalas (kui server peaks seisma). */
export const failsafeOlek = { viimane: null, writeCount: null, viga: null };
export async function failsafe() {
	if (!sbSees()) return;
	try {
		failsafeOlek.writeCount = await rpc('failsafe_bump', { p_allikas: 'server' });
		failsafeOlek.viimane = new Date().toISOString();
		failsafeOlek.viga = null;
	} catch (e) {
		failsafeOlek.viga = String(e.message || e).slice(0, 200);
		console.log('Supabase failsafe:', failsafeOlek.viga);
	}
}
