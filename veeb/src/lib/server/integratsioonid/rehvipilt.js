/* Rehvi pilt pakkujalt → väike webp, mälus ja kettal (LOG_DIR/pildid).
 *
 * Miks (Tarvo 27.10 audit): Inter Carsi pildiserver vastab 429 („liiga palju päringuid“),
 * kui leht küsib korraga ~20 kaardi pilti; osa originaale on kuni 7 MB. Nüüd:
 *   - ühe pakkuja juurde korraga kuni 2 päringut, 429 korral oodatakse ja proovitakse uuesti
 *   - pilt vähendatakse 480 px webp-ks (~15–40 kB) ja salvestatakse kettale (püsib üle restardi)
 *   - taustal soojendatakse kõik teadaolevad rehvipildid aeglaselt ette (soojendaPildid)
 * Pakkuja aadress ei lähe kunagi brauserisse. */
import { mkdir, readFile, writeFile, stat } from 'node:fs/promises';
import { join } from 'node:path';
import { pildiAllikad, pakkujaId, teadaolevadPildid } from './koond.js';
import { paring } from './http.js';

const TYYBID = ['image/jpeg', 'image/png', 'image/webp', 'image/avif'];
const KAUST = join(process.env.LOG_DIR || join(process.cwd(), 'data'), 'pildid');
const KEHTIB_MS = 14 * 86400 * 1000;
const MAX_MALUS = 2000;
const malu = new Map(); // slug -> { tyyp, andmed, aeg }

let _sharp;
async function sharp() {
	if (_sharp === undefined) _sharp = await import('sharp').then((m) => m.default).catch(() => null);
	return _sharp;
}

/* pildi tüüp failialguse järgi; muu kui pilt → null */
export function nuusi(b) {
	if (!b || b.length < 12) return null;
	if (b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff) return 'image/jpeg';
	if (b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4e && b[3] === 0x47) return 'image/png';
	const a = String.fromCharCode(...b.subarray(0, 12));
	if (a.startsWith('RIFF') && a.slice(8, 12) === 'WEBP') return 'image/webp';
	if (a.slice(4, 12) === 'ftypavif') return 'image/avif';
	return null;
}

/* lihtne järjekord pakkuja kohta: korraga kuni 2 päringut */
const jarjekorrad = new Map(); // pakkuja id -> { kaib, ootel: [] }
async function jarjekorras(id, fn) {
	let j = jarjekorrad.get(id);
	if (!j) jarjekorrad.set(id, (j = { kaib: 0, ootel: [] }));
	if (j.kaib >= 2) await new Promise((r) => j.ootel.push(r));
	j.kaib++;
	try {
		return await fn();
	} finally {
		j.kaib--;
		const jarg = j.ootel.shift();
		if (jarg) jarg();
	}
}
const oota = (ms) => new Promise((r) => setTimeout(r, ms));

async function laeAllikast(p, url) {
	for (let katse = 0; katse < 3; katse++) {
		const r = await jarjekorras(p.id, () => paring(p, url, { maxBaite: 10_000_000, aegMs: 15000 }));
		if (r.status === 429 || r.status === 503) {
			await oota(1500 * (katse + 1));
			continue;
		}
		return r;
	}
	return { status: 429 };
}

async function vahenda(andmed, tyyp) {
	const s = await sharp();
	if (!s) return { tyyp, andmed };
	try {
		const out = await s(andmed, { failOn: 'none' }).rotate().resize({ width: 480, height: 480, fit: 'inside', withoutEnlargement: true }).flatten({ background: '#ffffff' }).webp({ quality: 80 }).toBuffer();
		return { tyyp: 'image/webp', andmed: out };
	} catch {
		return { tyyp, andmed };
	}
}

const failitee = (slug) => join(KAUST, slug + '.webp');

async function kettalt(slug) {
	try {
		const f = failitee(slug);
		const st = await stat(f);
		if (Date.now() - st.mtimeMs > KEHTIB_MS) return null;
		const andmed = await readFile(f);
		return nuusi(andmed) ? { tyyp: nuusi(andmed), andmed, aeg: st.mtimeMs } : null;
	} catch {
		return null;
	}
}
async function kettale(slug, k) {
	if (k.tyyp !== 'image/webp') return;
	try {
		await mkdir(KAUST, { recursive: true });
		await writeFile(failitee(slug), k.andmed);
	} catch {
		/* ketas pole kirjutatav: jääb mällu */
	}
}
function malusse(slug, k) {
	malu.delete(slug);
	malu.set(slug, k);
	while (malu.size > MAX_MALUS) malu.delete(malu.keys().next().value);
}

const pooleli = new Map(); // slug -> Promise (sama pilti ei laeta korraga kaks korda)

/** → { tyyp, andmed } | { puudub: true } | { ajutine: true, pohjus } */
export async function rehviPilt(slug) {
	const m = malu.get(slug);
	if (m && Date.now() - m.aeg < KEHTIB_MS) return m;
	const d = await kettalt(slug);
	if (d) {
		malusse(slug, d);
		return d;
	}
	if (pooleli.has(slug)) return pooleli.get(slug);
	const t = (async () => {
		const allikad = await pildiAllikad(slug).catch(() => []);
		let pohjus = '';
		for (const allikas of allikad) {
			const p = pakkujaId(allikas.pakkuja);
			if (!p) continue;
			try {
				const r = await laeAllikast(p, allikas.url);
				let tyyp = String(r.tyyp || '').split(';')[0].trim().toLowerCase();
				/* Inter Carsi CDN annab osale tüübi application/octet-stream: otsusta failialguse järgi */
				if (r.status === 200 && !TYYBID.includes(tyyp)) tyyp = nuusi(r.andmed) || tyyp;
				if (r.status >= 500 || r.status === 429) {
					pohjus += `${p.id}:HTTP${r.status} `;
					continue;
				}
				if (r.status !== 200 || !TYYBID.includes(tyyp)) continue;
				const k = { ...(await vahenda(r.andmed, tyyp)), aeg: Date.now() };
				malusse(slug, k);
				kettale(slug, k);
				return k;
			} catch (e) {
				const s = String((e && (e.name === 'TimeoutError' ? 'aeg' : e.message)) || '');
				pohjus += `${p.id}:${/liiga suur/.test(s) ? 'suur' : /aeg|abort|timeout/i.test(s) ? 'aeg' : 'viga'} `;
			}
		}
		return pohjus ? { ajutine: true, pohjus: pohjus.trim().slice(0, 120) } : { puudub: true };
	})().finally(() => pooleli.delete(slug));
	pooleli.set(slug, t);
	return t;
}

/* Taustal: kõik teadaolevad rehvipildid ette kettale, üks korraga ja aeglaselt,
   et pakkuja pildiserver ei hakkaks keelduma. Kutsub koond.js pärast pildikataloogi. */
let _soojendab = false;
export const pildiSoojendus = { tehtud: 0, uusi: 0, vigu: 0, kokku: 0, valmis: null };
export async function soojendaPildid() {
	if (_soojendab) return;
	_soojendab = true;
	try {
		const slugid = teadaolevadPildid();
		Object.assign(pildiSoojendus, { tehtud: 0, uusi: 0, vigu: 0, kokku: slugid.length });
		for (const slug of slugid) {
			const oli = malu.has(slug) || (await kettalt(slug));
			if (!oli) {
				const k = await rehviPilt(slug).catch(() => ({ ajutine: true }));
				if (k.andmed) pildiSoojendus.uusi++;
				else pildiSoojendus.vigu++;
				await oota(700);
			}
			pildiSoojendus.tehtud++;
		}
		pildiSoojendus.valmis = new Date().toISOString();
	} finally {
		_soojendab = false;
	}
}
