/* INTER CARS EESTI (intercars24.ee) — tootevoog (DataFeedWatch XML): hind, laoseis,
 * tootelink ja pilt rehvi kaardile.
 *
 * Coolify:
 *   PAKKUJA_INTERCARS_URL = (Inter Carsi saadetud feeds.datafeedwatch.com/… aadress)
 *
 * VÄLJAD (kontrollitud 12.10.2026 e-poe vastu):
 *   <Price>   = e-poe hind KOOS käibemaksuga (nt 162.39 = „162.39 km'ga“ tootelehel)
 *   <InStore> = „Laos“ (voos on ainult laos olevad tooted)
 *   <Name>    = „Suverehv Pilot Sport PS2 225/40R18 92Y XL N3“ → mõõt nimest
 *   <Description> algab: „624767, Pilot Sport PS2, MICHELIN, Suvine, …“ → 2. väli = mudel
 *   <URL>/<ProductURL> = otse tootelehele, <Picture> = pilt (webcdn.intercars.eu)
 *   <Category> … > Sõiduauto rehvid / Rehvid Maastur/4x4 (moto ja veoki rehvid jäetakse välja)
 *
 * Voog loetakse voona (kogu fail ei ole korraga mälus), alles jäävad ainult meie
 * mõõtudes rehvid. Värskendus iga 6 h; kui see ebaõnnestub, kehtib eelmine (kuni 48 h).
 * TURVA: ainult GET sellele ühele aadressile (http.js hostide kontroll).
 */
import { normMoot } from '../sobitus.js';
import { core } from '$lib/server/andmed.js';

const VARSKE_MS = 6 * 3600 * 1000;
const MAX_VANUS_MS = 48 * 3600 * 1000;
const OOTA_VEA_JAREL_MS = 10 * 60 * 1000;

let indeks = null; // Map moot -> [toode]
let laetud = 0;
let laadib = null;
let viimaneViga = null;
const info = { ridu: 0, hoitud: 0, laetud: null, kestusMs: 0 };

const valja = (s, t) => {
	const m = new RegExp('<' + t + '>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?</' + t + '>').exec(s);
	return m
		? m[1]
				.replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
				.replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(+d))
				.replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
				.trim()
		: '';
};
const arv = (v) => {
	const n = Number(String(v ?? '').replace(',', '.'));
	return Number.isFinite(n) ? n : NaN;
};

/* sõiduauto, maastur/4x4, kaubik — mitte moto, veok, buss, agro */
const SOBIV_KAT = /(Sõiduauto|Maastur|4x4|Kaubik|Väikebuss)/i;
const VALJA_KAT = /(Mootorratta|mopeedi|Veoauto|bussi|Agro|Põllu|Tööstus|ATV)/i;
const MOOT_RE = /(\d{3})\/(\d{2})\s?Z?R\s?(\d{2})(C?)\b/i;

/** Mudel: kirjelduse 2. väli („624767, Pilot Sport PS2, MICHELIN, …“), muidu nimest
 *  hooajasõna ja mõõdu vahelt („Talverehv 4x4WinterContact 265/60R18 110H MO“). */
export function mudelNimest(nimi, kirjeldus, mark) {
	const osad = String(kirjeldus || '').split(',').map((x) => x.trim());
	if (osad.length > 2 && osad[1] && osad[2] && osad[2].toLowerCase() === String(mark).toLowerCase()) return osad[1];
	const enne = String(nimi || '').split(MOOT_RE)[0];
	return enne.replace(/^\s*\S*rehv\S*\s+/i, '').trim();
}

/** Üks <product> → meie kuju või null. */
export function teisenda(s, meieMoodud) {
	const kat = valja(s, 'Category');
	if (!SOBIV_KAT.test(kat) || VALJA_KAT.test(kat)) return null;
	const nimi = valja(s, 'Name');
	const m = MOOT_RE.exec(nimi);
	if (!m) return null;
	const moot = normMoot(`${m[1]}/${m[2]} R${m[3]}${m[4] ? ' C' : ''}`);
	if (!moot || (meieMoodud && !meieMoodud.has(moot))) return null;
	const hind = Math.round(arv(valja(s, 'Price')) * 100) / 100;
	if (!(hind > 5 && hind < 5000)) return null;
	const markRaw = valja(s, 'Vendor');
	if (!markRaw) return null;
	/* „MICHELIN“ → „Michelin“ (sobitus võrdleb normaliseeritult, see on lihtsalt loetavus) */
	const mark = markRaw.charAt(0) + markRaw.slice(1).toLowerCase();
	const mudel = mudelNimest(nimi, valja(s, 'Description'), markRaw);
	if (!mudel) return null;
	const url = valja(s, 'URL') || valja(s, 'ProductURL');
	const pilt = valja(s, 'Picture');
	const gtin = valja(s, 'GTIN');
	const laos = /laos/i.test(valja(s, 'InStore'));
	const lisi = (nimi.slice(m.index + m[0].length).match(/^\s*(\d{2,3}(?:\/\d{2,3})?[A-Z])/) || [])[1];
	return {
		mark,
		mudel,
		moot,
		hind,
		laos,
		lisi: lisi || undefined,
		ean: /^\d{8,14}$/.test(gtin) ? gtin : undefined,
		pilt: /^https:\/\//.test(pilt) ? pilt : undefined,
		url: /^https:\/\//.test(url) ? url : undefined,
		myyja: 'intercars24.ee'
	};
}

async function laeKoik(pakkuja, { muutuja, voog }) {
	const aadress = muutuja('PAKKUJA_INTERCARS_URL');
	const algus = Date.now();
	const meieMoodud = new Set((core().eprelSizes || []).filter((m) => /^\d{5}R\d{2}C?$/.test(m)));
	const r = await voog(pakkuja, aadress, { maxBaite: 200_000_000, aegMs: 180_000 });
	const uus = new Map();
	let ridu = 0, hoitud = 0, jaak = '';
	const dek = new TextDecoder('utf-8');
	const tootle = (tekst) => {
		let i = 0;
		for (;;) {
			const a = tekst.indexOf('<product>', i);
			if (a < 0) return tekst.slice(i);
			const b = tekst.indexOf('</product>', a);
			if (b < 0) return tekst.slice(a);
			ridu++;
			const t = teisenda(tekst.slice(a + 9, b), meieMoodud);
			if (t) {
				hoitud++;
				const l = uus.get(t.moot);
				if (l) l.push(t);
				else uus.set(t.moot, [t]);
			}
			i = b + 10;
		}
	};
	for await (const tykk of r.keha) jaak = tootle(jaak + dek.decode(tykk, { stream: true }));
	tootle(jaak + dek.decode());
	if (!ridu) throw new Error('intercars: voos ei olnud ühtegi toodet');
	if (!hoitud) throw new Error(`intercars: ${ridu} rida, aga ükski ei sobinud meie mõõtudega`);
	if (indeks && info.hoitud > 200 && hoitud < info.hoitud * 0.2)
		throw new Error(`intercars: ainult ${hoitud} sobivat toodet (enne ${info.hoitud}) — jätsin vana`);
	indeks = uus;
	laetud = Date.now();
	Object.assign(info, { ridu, hoitud, laetud: new Date(laetud).toISOString(), kestusMs: Date.now() - algus });
	viimaneViga = null;
}

function lae(pakkuja, ctx) {
	if (laadib) return laadib;
	if (viimaneViga && Date.now() - viimaneViga.aeg < OOTA_VEA_JAREL_MS) return Promise.reject(new Error(viimaneViga.teade));
	laadib = laeKoik(pakkuja, ctx)
		.catch((e) => {
			viimaneViga = { aeg: Date.now(), teade: String(e.message || e).slice(0, 200) };
			throw new Error(viimaneViga.teade);
		})
		.finally(() => {
			laadib = null;
		});
	return laadib;
}

export default {
	id: 'intercars',
	nimi: 'intercars24.ee',
	/* voog (DataFeedWatch) + tootepildid (Inter Carsi CDN) */
	hostid: ['feeds.datafeedwatch.com', 'webcdn.intercars.eu'],
	poeHostid: ['www.intercars24.ee', 'intercars24.ee'],
	env: ['PAKKUJA_INTERCARS_URL'],
	ttlHinnad: 600,

	async soojenda(ctx) {
		await lae(this, ctx);
	},

	async hinnadMoodus(moot, ctx) {
		if (!indeks) await lae(this, ctx);
		else if (Date.now() - laetud > VARSKE_MS) lae(this, ctx).catch(() => {});
		if (Date.now() - laetud > MAX_VANUS_MS) throw new Error('intercars: andmed üle 48 h vanad ja värskendus ei õnnestu');
		return indeks.get(moot) || [];
	},

	lisaOlek() {
		return { ...info, viga: viimaneViga ? viimaneViga.teade : null, laadib: !!laadib };
	}
};
