/* AWIN TOOTEFAIL — rehvipoodide hinnad Awini partnerprogrammidest.
 *
 * Kuidas töötab:
 *   Awinis teed "Create-a-Feed" all tootefaili (CSV). Awin annab selle
 *   jaoks allalaadimise aadressi, mille SEES on sinu isiklik võti. See
 *   aadress läheb AINULT Coolifysse:
 *      PAKKUJA_AWIN_FEED = https://productdata.awin.com/datafeed/download/apikey/…/
 *   (mitu faili: mitu aadressi tühikuga eraldatult)
 *
 *   Server laeb faili alla käivitumisel ja siis iga 6 tunni järel, hoiab
 *   mälus ainult need tooted, mille mõõt on meie andmetes olemas, ja
 *   vastab hinnapäringutele mälust — iga külastaja ei tee Awinisse päringut.
 *   Kui värskendus ebaõnnestub, jääb kehtima eelmine fail (kuni 48 h).
 *
 * Mida failist kasutatakse (muud veerud jäetakse vahele):
 *   product_name, brand_name, search_price, currency, aw_deep_link,
 *   merchant_name, in_stock / stock_quantity / stock_status, aw_image_url, ean
 *
 * Link poodi on Awini oma jälgimislink (aw_deep_link) — ost käib poes ja
 * vahendustasu jälgib Awin.
 */
import { createGunzip } from 'node:zlib';
import { Readable } from 'node:stream';
import { normMoot } from '../sobitus.js';
import { core } from '$lib/server/andmed.js';

const VARSKE_MS = 6 * 3600 * 1000; // uus allalaadimine iga 6 h
const MAX_VANUS_MS = 48 * 3600 * 1000; // vanemat faili enam ei kasutata
const OOTA_VEA_JAREL_MS = 10 * 60 * 1000; // pärast viga ei proovi 10 min
const MAX_PAKITUD = 150_000_000; // allalaaditav fail
const MAX_LAHTI = 800_000_000; // lahtipakitud sisu
const MAX_RIDU = 2_000_000;

let indeks = null; // Map moot -> [toode]
let laetud = 0;
let laadib = null;
let viimaneViga = null; // { aeg, teade }
const info = { ridu: 0, hoitud: 0, poode: 0, laetud: null, kestusMs: 0 };

/* --- CSV (voona, jutumärgid ja reavahetused väljades lubatud) --- */
function csvLugeja(onRida) {
	let eraldaja = null;
	let valjad = [];
	let vali = '';
	let jm = false; // jutumärkide sees
	let eelmineJm = false; // eelmine märk oli sulgev jutumärk
	let esimene = '';
	const rea_lopp = () => {
		valjad.push(vali);
		vali = '';
		if (valjad.length > 1 || valjad[0] !== '') onRida(valjad);
		valjad = [];
	};
	function tykk(s) {
		if (eraldaja === null) {
			/* eraldaja päiserea järgi: koma, | või tab */
			esimene += s;
			const nl = esimene.indexOf('\n');
			if (nl < 0 && esimene.length < 20000) return;
			const pais = nl < 0 ? esimene : esimene.slice(0, nl);
			const loe = (c) => pais.split(c).length;
			eraldaja = [',', '|', '\t', ';'].sort((a, b) => loe(b) - loe(a))[0];
			s = esimene;
			esimene = '';
		}
		for (let i = 0; i < s.length; i++) {
			const c = s[i];
			if (jm) {
				if (c === '"') {
					jm = false;
					eelmineJm = true;
				} else vali += c;
				continue;
			}
			if (c === '"') {
				if (eelmineJm) vali += '"'; // "" = jutumärk
				jm = true;
				eelmineJm = false;
				continue;
			}
			eelmineJm = false;
			if (c === eraldaja) {
				valjad.push(vali);
				vali = '';
			} else if (c === '\n') rea_lopp();
			else if (c !== '\r') vali += c;
		}
	}
	function lopp() {
		if (eraldaja === null && esimene) {
			const s = esimene;
			esimene = '';
			eraldaja = ',';
			tykk(s);
		}
		if (vali !== '' || valjad.length) rea_lopp();
	}
	return { tykk, lopp };
}

const jahEi = (v) => {
	const s = String(v || '').trim().toLowerCase();
	if (!s) return undefined;
	if (['1', 'y', 'yes', 'true', 'in stock', 'instock', 'available', 'jah'].includes(s)) return true;
	if (['0', 'n', 'no', 'false', 'out of stock', 'outofstock', 'unavailable', 'ei'].includes(s)) return false;
	return undefined;
};

const hinnaArv = (v) => {
	const n = Number(String(v || '').replace(/[^\d.,]/g, '').replace(',', '.'));
	return Number.isFinite(n) ? n : NaN;
};

/** Ühe faili lugemine → lisab tooted kaarti `uus`. */
async function loeFail(pakkuja, url, voog, uus, meieMoodud, poed) {
	const { keha } = await voog(pakkuja, url, { maxBaite: MAX_PAKITUD, aegMs: 180_000 });

	/* gzip tuvastatakse sisu järgi (1f 8b), mitte päise järgi */
	const iter = keha[Symbol.asyncIterator]();
	const alg = await iter.next();
	if (alg.done) throw new Error('awin: tühi fail');
	const esimene = Buffer.from(alg.value);
	async function* koos() {
		yield esimene;
		for (;;) {
			const x = await iter.next();
			if (x.done) return;
			yield x.value;
		}
	}
	const onGzip = esimene[0] === 0x1f && esimene[1] === 0x8b;
	if (esimene[0] === 0x50 && esimene[1] === 0x4b) throw new Error('awin: ZIP ei sobi — vali Awinis tihendus "gzip" või "none"');
	const allikas = onGzip ? Readable.from(koos()).pipe(createGunzip()) : Readable.from(koos());

	let veerud = null;
	let ridu = 0;
	let lahti = 0;
	const ix = {};
	const lugeja = csvLugeja((v) => {
		if (!veerud) {
			veerud = v.map((x) => x.trim().toLowerCase().replace(/^﻿/, ''));
			const leia = (...nimed) => {
				for (const n of nimed) {
					const i = veerud.indexOf(n);
					if (i >= 0) return i;
				}
				return -1;
			};
			ix.nimi = leia('product_name');
			ix.mark = leia('brand_name');
			ix.hind = leia('search_price', 'store_price', 'display_price');
			ix.valuuta = leia('currency');
			ix.link = leia('aw_deep_link');
			ix.pood = leia('merchant_name');
			ix.laos = leia('in_stock');
			ix.kogus = leia('stock_quantity');
			ix.laoOlek = leia('stock_status');
			ix.pilt = leia('aw_image_url');
			ix.ean = leia('ean', 'product_gtin');
			if (ix.nimi < 0 || ix.hind < 0 || ix.link < 0)
				throw new Error('awin: failis puudub veerg product_name, search_price või aw_deep_link');
			return;
		}
		if (++ridu > MAX_RIDU) throw new Error('awin: liiga palju ridu');
		const nimi = v[ix.nimi] || '';
		const moot = normMoot(nimi);
		if (!moot || !meieMoodud.has(moot)) return;
		if (ix.valuuta >= 0 && v[ix.valuuta] && v[ix.valuuta].trim().toUpperCase() !== 'EUR') return;
		const hind = hinnaArv(v[ix.hind]);
		if (!(hind > 5 && hind < 5000)) return;
		let mark = ix.mark >= 0 ? (v[ix.mark] || '').trim() : '';
		if (!mark) mark = nimi.trim().split(/\s+/)[0] || '';
		let laos = ix.laos >= 0 ? jahEi(v[ix.laos]) : undefined;
		if (laos === undefined && ix.laoOlek >= 0) laos = jahEi(v[ix.laoOlek]);
		if (laos === undefined && ix.kogus >= 0 && v[ix.kogus] !== '') {
			const k = Number(v[ix.kogus]);
			if (Number.isFinite(k)) laos = k > 0;
		}
		const pood = ix.pood >= 0 ? (v[ix.pood] || '').trim() : '';
		if (pood) poed.add(pood);
		const t = {
			mark,
			mudel: nimi,
			moot,
			hind,
			laos,
			url: v[ix.link] || undefined,
			pilt: ix.pilt >= 0 ? v[ix.pilt] || undefined : undefined,
			ean: ix.ean >= 0 ? v[ix.ean] || undefined : undefined,
			myyja: pood || undefined
		};
		const l = uus.get(moot);
		if (l) l.push(t);
		else uus.set(moot, [t]);
	});

	const dek = new TextDecoder('utf-8');
	for await (const tk of allikas) {
		lahti += tk.length;
		if (lahti > MAX_LAHTI) throw new Error('awin: fail liiga suur');
		lugeja.tykk(dek.decode(tk, { stream: true }));
	}
	lugeja.tykk(dek.decode());
	lugeja.lopp();
	if (!veerud) throw new Error('awin: failis pole päiserida');
	return ridu;
}

async function laeKoik(pakkuja, { muutuja, voog }) {
	const aadressid = String(muutuja('PAKKUJA_AWIN_FEED') || '')
		.split(/\s+/)
		.filter(Boolean);
	if (!aadressid.length) throw new Error('awin: PAKKUJA_AWIN_FEED puudub');
	const algus = Date.now();
	const meieMoodud = new Set((core().eprelSizes || []).filter((m) => /^\d{5}R\d{2}C?$/.test(m)));
	const uus = new Map();
	const poed = new Set();
	let ridu = 0;
	for (const url of aadressid) ridu += await loeFail(pakkuja, url, voog, uus, meieMoodud, poed);
	let hoitud = 0;
	for (const l of uus.values()) hoitud += l.length;
	if (!hoitud) throw new Error(`awin: failis ${ridu} rida, aga ükski ei sobinud meie mõõtudega`);
	/* kaitse poolikute failide eest: kui uues on alla 20% eelmisest, jäta vana alles */
	if (indeks && info.hoitud > 200 && hoitud < info.hoitud * 0.2)
		throw new Error(`awin: uues failis ainult ${hoitud} sobivat toodet (enne ${info.hoitud}) — jätsin vana`);
	indeks = uus;
	laetud = Date.now();
	Object.assign(info, {
		ridu,
		hoitud,
		poode: poed.size,
		laetud: new Date(laetud).toISOString(),
		kestusMs: Date.now() - algus
	});
	viimaneViga = null;
}

function lae(pakkuja, ctx) {
	if (laadib) return laadib;
	if (viimaneViga && Date.now() - viimaneViga.aeg < OOTA_VEA_JAREL_MS) return Promise.reject(new Error(viimaneViga.teade));
	laadib = laeKoik(pakkuja, ctx)
		.catch((e) => {
			viimaneViga = { aeg: Date.now(), teade: String(e.message || e).slice(0, 200) };
			throw e;
		})
		.finally(() => {
			laadib = null;
		});
	return laadib;
}

export default {
	id: 'awin',
	nimi: 'Awin',
	/* tootefail ja Awini pildiserver */
	hostid: ['productdata.awin.com', '*.productserve.com'],
	/* poe lingid on Awini jälgimislingid */
	poeHostid: ['www.awin1.com', 'awin1.com'],
	env: ['PAKKUJA_AWIN_FEED'],
	/* koond hoiab mõõdu vastust 30 min; fail ise uueneb iga 6 h */
	ttlHinnad: 1800,

	/** Serveri käivitumisel: laadi fail kohe, et esimene külastaja ei ootaks. */
	async soojenda(ctx) {
		await lae(this, ctx);
	},

	async hinnadMoodus(moot, ctx) {
		if (!indeks) await lae(this, ctx);
		else if (Date.now() - laetud > VARSKE_MS) lae(this, ctx).catch(() => {}); // taustal; seni vana
		if (Date.now() - laetud > MAX_VANUS_MS) throw new Error('awin: fail on üle 48 h vana ja värskendus ei õnnestu');
		return indeks.get(moot) || [];
	},

	/** Admini olekusse (ilma aadressita). */
	lisaOlek() {
		return { ...info, viga: viimaneViga ? viimaneViga.teade : null, laadib: !!laadib };
	}
};

/* testideks */
export const _csvLugeja = csvLugeja;
