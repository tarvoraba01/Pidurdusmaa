/* REHVIVAHETUS.EE partner API — hind, laoseis ja pilt rehvi kaardile.
 *
 * Coolify:
 *   PAKKUJA_REHVIVAHETUS_URL  = https://partner.rehvivahetus.ee/api
 *   PAKKUJA_REHVIVAHETUS_VOTI = (partneri võti)
 *
 * API ei oska mõõdu järgi filtreerida, seega laeme kogu laos oleva kataloogi
 * lehekaupa (limit/offset), hoiame mälus ainult meie mõõdud ja vastame
 * hinnapäringutele mälust. Värskendus iga 6 h; kui see ebaõnnestub, jääb
 * kehtima eelmine (kuni 48 h).
 *
 * TURVA:
 *  - Võti käib API nõudel URL-i parameetris `key`. Seda URL-i ei logita
 *    kunagi: http.js näitab veateates ainult hosti, siin ei kirjutata URL-i
 *    ega vastuse toorsisu kuhugi.
 *  - Ainult lugemine (GET /api). Tellimuse otspunkti (/api/checkout) seda
 *    koodi kaudu välja kutsuda ei saa — vt KEELATUD all.
 *  - API võib vea anda HTTP 200-ga → kontrollime vastuse `status` välja.
 *
 * Hind: võtmega JSON-päringus on `price` partnerhind, mis rehvivahetus.ee
 * sõnul vastab keskmiselt nende e-poe hinnale (km ja keskkonnatasuga).
 * E-poes on brändi kaupa veidi erinev allahindlus → lehel „u X €“.
 */
import { normMoot, normMark, norm } from '../sobitus.js';
import { core } from '$lib/server/andmed.js';

const VARSKE_MS = 6 * 3600 * 1000;
const MAX_VANUS_MS = 48 * 3600 * 1000;
const OOTA_VEA_JAREL_MS = 10 * 60 * 1000;
const LEHT = 500; // toodet päringu kohta
const MAX_LEHTI = 200; // kuni 100 000 toodet
const PAUS_MS = 400; // viisakas paus lehtede vahel
const POOD = 'https://www.rehvivahetus.ee/';

let indeks = null; // Map moot -> [toode]
let laetud = 0;
let laadib = null;
let viimaneViga = null;
const info = { tooteid: 0, hoitud: 0, lehti: 0, laetud: null, kestusMs: 0 };

/* Ainult see aadress on lubatud — tellimused jms on teised teed. */
function apiAadress(baas) {
	const u = new URL(baas);
	if (u.protocol !== 'https:') throw new Error('rehvivahetus: API aadress peab olema https');
	if (!/^\/api\/?$/.test(u.pathname)) throw new Error('rehvivahetus: lubatud on ainult GET /api');
	u.pathname = '/api';
	u.search = '';
	return u;
}

/* E-poe mõõdu nimekiri. Toote enda leht (/product/<nr>/) on e-poe number,
   mis ei ole API id — seni viib link õige mõõdu nimekirja. */
export function poeLinkMoodule(t) {
	const m = /^(\d{3})(\d{2})R(\d{2})/.exec(t.moot || '');
	if (!m) return POOD;
	const u = new URL(POOD);
	u.searchParams.set('s', 'tires');
	u.searchParams.set('carType', /kaubik/i.test(t.carType || '') ? '2' : '1');
	u.searchParams.set('tireWidth', String(+m[1]));
	u.searchParams.set('tireHeight', String(+m[2]));
	u.searchParams.set('tireDiameter', String(+m[3]));
	return u.toString();
}

const arv = (v) => {
	const n = Number(String(v ?? '').replace(',', '.'));
	return Number.isFinite(n) ? n : NaN;
};

/** API vastus → toodete massiiv; vea korral viska (ka HTTP 200 puhul). */
export function tooted(vastus) {
	if (Array.isArray(vastus)) return vastus;
	if (vastus && typeof vastus === 'object') {
		const st = String(vastus.status ?? '').toLowerCase();
		const list = vastus.products || vastus.data || vastus.items;
		if (Array.isArray(list) && (!st || ['ok', 'success', '1', 'true'].includes(st))) return list;
		/* ainult lühike puhastatud teade — vastuses võib olla päringu kaja */
		const teade = String(vastus.message || vastus.error || vastus.status || 'tundmatu viga')
			.replace(/key=[^&\s]*/gi, 'key=…')
			.replace(/[^\p{L}\p{N} .,:;()_-]/gu, '')
			.slice(0, 120);
		throw new Error('rehvivahetus: API viga — ' + teade);
	}
	throw new Error('rehvivahetus: ootamatu vastus');
}

/** Üks API toode → meie kuju (või null, kui ei sobi). */
export function teisenda(x, meieMoodud) {
	if (!x || typeof x !== 'object') return null;
	const moot = normMoot(x.size);
	if (!moot || (meieMoodud && !meieMoodud.has(moot))) return null;
	const hind = arv(x.price);
	if (!(hind > 5 && hind < 5000)) return null;
	const mark = String(x.brand || '').trim();
	const nimi = String(x.name || '').trim();
	if (!mark || !nimi) return null;
	const kogus = arv(x.stock);
	const t = {
		mark,
		mudel: nimi,
		moot,
		hind,
		laos: Number.isFinite(kogus) ? kogus > 0 : undefined,
		kogus: Number.isFinite(kogus) ? Math.max(0, Math.round(kogus)) : undefined,
		lisi: String(x.lisi || '').trim().slice(0, 30) || undefined,
		eu: String(x.eu || '').trim().slice(0, 30) || undefined,
		carType: String(x.car_type || ''),
		pilt: typeof x.img === 'string' && x.img.startsWith('https://') ? x.img : undefined,
		myyja: 'rehvivahetus.ee',
		umbes: true
	};
	t.url = poeLinkMoodule(t);
	t.ct = /kaubik/i.test(t.carType) ? 2 : 1;
	t.voti = epoeVoti(mark, nimi, moot, t.lisi);
	delete t.carType;
	return t;
}

const oota = (ms) => new Promise((r) => setTimeout(r, ms));

/* ---- E-poe tootelingid ----
 * API `id` ei ole e-poe toote number (/product/<nr>/). Seome need e-poe
 * mõõdu nimekirja järgi: tootja + mudel + mõõt + koormus/kiirusindeks.
 * Loeme ainult neid mõõte, mida meie lehel päriselt vaadatakse, ühe mõõdu
 * korraga, pausiga ja kuni 8 lehekülge. Tulemus kehtib 24 h. Kuni seda pole,
 * viib nupp e-poes sama mõõdu nimekirja. */
const EPOOD_KEHTIB_MS = 24 * 3600 * 1000;
const EPOOD_MAX_LEHTI = 8;
const EPOOD_PAUS_MS = 1500;
const epood = new Map(); // `${ct}:${moot}` -> { aeg, lingid: Map voti -> url }
const epoodJarjekord = [];
let epoodTootab = false;

const lisiTuum = (s) => {
	const m = /(\d{2,3}(?:\/\d{2,3})?)\s*([A-Z])\b/.exec(String(s || '').toUpperCase());
	return m ? m[1] + m[2] : '';
};
export function epoeVoti(mark, mudel, moot, lisi) {
	return `${normMark(mark)}|${norm(mudel).replace(/ /g, '')}|${moot}|${lisiTuum(lisi)}`;
}
const dekodeeri = (s) =>
	String(s || '')
		.replace(/<[^>]*>/g, ' ')
		.replace(/&amp;/g, '&')
		.replace(/&quot;/g, '"')
		.replace(/&#0?39;|&apos;/g, "'")
		.replace(/&nbsp;/g, ' ')
		.replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
		.replace(/\s+/g, ' ')
		.trim();

/** E-poe nimekirja HTML → [{ id, voti }]. Pealkirja märgid („Uus“, „Soovitame“) on <span>-is — need jäetakse välja. */
export function loeKaardid(html) {
	const out = [];
	const re = /<article class="card-product"[\s\S]*?<\/article>/g;
	let m;
	while ((m = re.exec(html))) {
		const a = m[0];
		const id = (/href="https:\/\/www\.rehvivahetus\.ee\/product\/(\d+)\//.exec(a) || [])[1];
		const pealkiri = /<h2 class="card-product__title">\s*<small>([\s\S]*?)<\/small>([\s\S]*?)<\/h2>/.exec(a);
		const meta = (/<p class="card-product__meta">([\s\S]*?)<\/p>/.exec(a) || [])[1];
		if (!id || !pealkiri || !meta) continue;
		const metaT = dekodeeri(meta);
		const moot = normMoot(metaT);
		if (!moot) continue;
		out.push({ id, voti: epoeVoti(dekodeeri(pealkiri[1]), dekodeeri(pealkiri[2].split('<span')[0]), moot, metaT.slice(metaT.indexOf(' '))) });
	}
	return out;
}

async function loeEpoodMoot(pakkuja, ctx, ct, moot) {
	const n = /^(\d{3})(\d{2})R(\d{2})/.exec(moot);
	if (!n) return;
	const lingid = new Map();
	for (let leht = 1; leht <= EPOOD_MAX_LEHTI; leht++) {
		const u = new URL(POOD + (leht > 1 ? `page/${leht}/` : ''));
		u.searchParams.set('s', 'tires');
		u.searchParams.set('carType', String(ct));
		u.searchParams.set('tireWidth', String(+n[1]));
		u.searchParams.set('tireHeight', String(+n[2]));
		u.searchParams.set('tireDiameter', String(+n[3]));
		const r = await ctx.paring(pakkuja, u.toString(), { maxBaite: 3_000_000, aegMs: 15_000 });
		if (r.status === 404) break;
		if (r.status !== 200) throw new Error(`rehvivahetus e-pood: HTTP ${r.status}`);
		const html = r.andmed.toString('utf-8');
		const kaardid = loeKaardid(html);
		for (const k of kaardid) if (!lingid.has(k.voti)) lingid.set(k.voti, `${POOD}product/${k.id}/`);
		if (!kaardid.length || !html.includes(`/page/${leht + 1}/`)) break;
		await oota(EPOOD_PAUS_MS);
	}
	epood.set(`${ct}:${moot}`, { aeg: Date.now(), lingid });
}

function epoodTaustal(pakkuja, ctx, ct, moot) {
	const k = `${ct}:${moot}`;
	if (epoodJarjekord.includes(k) || epoodJarjekord.length > 50) return;
	epoodJarjekord.push(k);
	if (epoodTootab) return;
	epoodTootab = true;
	(async () => {
		while (epoodJarjekord.length) {
			const [c, m] = epoodJarjekord[0].split(':');
			try {
				await loeEpoodMoot(pakkuja, ctx, +c, m);
			} catch (e) {
				/* ebaõnnestus → proovime alles 24 h pärast uuesti; seni mõõdu nimekiri */
				epood.set(epoodJarjekord[0], { aeg: Date.now(), lingid: new Map(), viga: String(e.message || e).slice(0, 120) });
			}
			epoodJarjekord.shift();
			await oota(EPOOD_PAUS_MS);
		}
		epoodTootab = false;
	})();
}

function lisaTooteLingid(pakkuja, ctx, list) {
	if (!list.length) return list;
	const vaja = new Set();
	const tulem = list.map((t) => {
		const e = epood.get(`${t.ct}:${t.moot}`);
		if (!e || Date.now() - e.aeg > EPOOD_KEHTIB_MS) vaja.add(t.ct);
		const url = e && e.lingid.get(t.voti);
		return url ? { ...t, url } : t;
	});
	for (const ct of vaja) epoodTaustal(pakkuja, ctx, ct, list[0].moot);
	return tulem;
}

async function laeKoik(pakkuja, { muutuja, jsonParing }) {
	const baas = apiAadress(muutuja('PAKKUJA_REHVIVAHETUS_URL'));
	const voti = muutuja('PAKKUJA_REHVIVAHETUS_VOTI');
	const algus = Date.now();
	const meieMoodud = new Set((core().eprelSizes || []).filter((m) => /^\d{5}R\d{2}C?$/.test(m)));
	const uus = new Map();
	let kokku = 0;
	let lehti = 0;
	for (let offset = 0; lehti < MAX_LEHTI; offset += LEHT) {
		const u = new URL(baas);
		u.searchParams.set('output', 'json');
		u.searchParams.set('in_stock', '1');
		u.searchParams.set('limit', String(LEHT));
		u.searchParams.set('offset', String(offset));
		u.searchParams.set('key', voti);
		const list = tooted(await jsonParing(pakkuja, u.toString(), { maxBaite: 20_000_000, aegMs: 30_000 }));
		lehti++;
		kokku += list.length;
		for (const x of list) {
			const t = teisenda(x, meieMoodud);
			if (!t) continue;
			const l = uus.get(t.moot);
			if (l) l.push(t);
			else uus.set(t.moot, [t]);
		}
		if (list.length < LEHT) break;
		await oota(PAUS_MS);
	}
	let hoitud = 0;
	for (const l of uus.values()) hoitud += l.length;
	if (!hoitud) throw new Error(`rehvivahetus: ${kokku} toodet, aga ükski ei sobinud meie mõõtudega`);
	if (indeks && info.hoitud > 200 && hoitud < info.hoitud * 0.2)
		throw new Error(`rehvivahetus: ainult ${hoitud} sobivat toodet (enne ${info.hoitud}) — jätsin vana`);
	indeks = uus;
	laetud = Date.now();
	Object.assign(info, { tooteid: kokku, hoitud, lehti, laetud: new Date(laetud).toISOString(), kestusMs: Date.now() - algus });
	viimaneViga = null;
}

function lae(pakkuja, ctx) {
	if (laadib) return laadib;
	if (viimaneViga && Date.now() - viimaneViga.aeg < OOTA_VEA_JAREL_MS) return Promise.reject(new Error(viimaneViga.teade));
	laadib = laeKoik(pakkuja, ctx)
		.catch((e) => {
			viimaneViga = { aeg: Date.now(), teade: String(e.message || e).replace(/key=[^&\s]*/gi, 'key=…').slice(0, 200) };
			throw new Error(viimaneViga.teade);
		})
		.finally(() => {
			laadib = null;
		});
	return laadib;
}

export default {
	id: 'rehvivahetus',
	nimi: 'rehvivahetus.ee',
	/* API + pildid; e-poe nimekiri tootelinkide jaoks */
	hostid: ['partner.rehvivahetus.ee', 'www.rehvivahetus.ee'],
	poeHostid: ['www.rehvivahetus.ee', 'rehvivahetus.ee'],
	env: ['PAKKUJA_REHVIVAHETUS_URL', 'PAKKUJA_REHVIVAHETUS_VOTI'],
	/* lühem, et e-poe tootelingid jõuaksid lehele kiiresti */
	ttlHinnad: 600,

	async soojenda(ctx) {
		await lae(this, ctx);
	},

	async hinnadMoodus(moot, ctx) {
		if (!indeks) await lae(this, ctx);
		else if (Date.now() - laetud > VARSKE_MS) lae(this, ctx).catch(() => {});
		if (Date.now() - laetud > MAX_VANUS_MS) throw new Error('rehvivahetus: andmed üle 48 h vanad ja värskendus ei õnnestu');
		return lisaTooteLingid(this, ctx, indeks.get(moot) || []);
	},

	lisaOlek() {
		let lingid = 0;
		for (const e of epood.values()) lingid += e.lingid.size;
		return { ...info, viga: viimaneViga ? viimaneViga.teade : null, laadib: !!laadib, epoodMoote: epood.size, epoodLinke: lingid, epoodJarjekord: epoodJarjekord.length };
	}
};

/* KEELATUD: tellimuse otspunkt. Kui keegi kunagi lisab siia POST-i, peab
   see läbima apiAadress() kontrolli, mis lubab ainult /api tee. */
export const KEELATUD = ['/api/checkout'];
