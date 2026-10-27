/* Koondab kõigi sisse lülitatud pakkujate andmed meie rehvide külge.
 *
 *   hinnadMoodus('20555R16') → { available, hinnad: { 'slug@20555R16': [ {myyja, hind, url, laos} ] }, kasutatud: { sama kuju, kasutatud: true, muster } }
 *   pilt('michelin-pilot-sport-5') → { pakkuja, url } | null   (URL jääb serverisse)
 *   olek() → mis on sees, mis puudu, viimased vead (ilma saladusteta)
 *
 * Brauser ei räägi kunagi pakkujaga otse: kõik käib meie serveri kaudu,
 * seega ei näe keegi võtmeid ega pakkuja API aadresse.
 */
import { PAKKUJAD } from './pakkujad/index.js';
import { muutuja, koikOlemas } from './seaded.js';
import { jsonParing, paring, voog, lubatud } from './http.js';
import { vahemalus, stat as vmStat, suurus as vmSuurus } from './vahemalu.js';
import { leiaRehv, normMoot } from './sobitus.js';
import { eprelSize, core } from '$lib/server/andmed.js';
import { sbSees, failsafeOlek } from '$lib/server/supabase.js';
import { sbLogiOlek } from '$lib/server/logi.js';
import { pusivusOlek } from './pusivus.js';

/* Testitud rehvid (sh naastrehvid, millel EL-i märgist ja seega EPREL-i
   rida pole) samal kujul nagu eprelSize read: [slug, mark, mudel]. */
let _testRead = null, _naastRead = null;
function testRead() {
	if (!_testRead) {
		/* kahesõnalised margid („GT Radial IcePro3“ — mark ei ole „GT“) */
		const MARK2 = /^(GT Radial|Nokian Tyres|General Tire|BF Goodrich|Double Coin|Tri Ace|Star Performer)\s/i;
		const rida = (t) => {
			const nimi = String(t.name), m2 = MARK2.exec(nimi);
			if (m2) return [t.slug, m2[1], nimi.slice(m2[0].length)];
			const [mark, ...m] = nimi.split(' ');
			return [t.slug, mark, m.join(' ')];
		};
		const koik = (core().tyres || []).filter((t) => t.slug && t.name);
		_testRead = koik.filter((t) => t.category !== 'WINTER_STUDDED').map(rida);
		_naastRead = koik.filter((t) => t.category === 'WINTER_STUDDED').map(rida);
	}
	return _testRead;
}
/* Naastrehvid (EL-i märgist pole): ainult meie testitud/tuletatud naastrehvide seast */
function naastRead() {
	testRead();
	return _naastRead;
}

const ctx = { muutuja, jsonParing, paring, voog };
const olekud = new Map(); // id -> { viga, vigaAeg, edu, tooteid, sobitatud }
const pildid = new Map(); // slug -> [{ pakkuja, url }, …] (kuni 3 pakkujat)
const MAX_PILTE = 20000;

export const aktiivsed = () => PAKKUJAD.filter((p) => koikOlemas(p.env || []));

function olek(p) {
	if (!olekud.has(p.id)) olekud.set(p.id, { viga: null, vigaAeg: null, edu: null, tooteid: 0, sobitatud: 0 });
	return olekud.get(p.id);
}

function poeLink(p, url) {
	try {
		const u = new URL(url);
		if (u.protocol !== 'https:') return null;
		const ok = [...(p.poeHostid || []), ...(p.hostid || [])].some((h) =>
			h.startsWith('*.') ? u.host.endsWith(h.slice(1)) : u.host === h
		);
		return ok ? u.toString() : null;
	} catch {
		return null;
	}
}

/* Pakkuja võib anda poe nime rea kaupa (nt Awini fail, kus on mitu poodi).
   Ainult lühike lihttekst — see läheb lehele. */
function myyjaNimi(v) {
	if (typeof v !== 'string') return null;
	const s = v.replace(/[<>\u0000-\u001f]/g, '').replace(/\s+/g, ' ').trim();
	return s && s.length <= 60 ? s : null;
}

/** Käivita pakkujate eellaadimine (nt suur tootefail) serveri käivitumisel.
 *  Ei oota ära ja vead ei kuku läbi — need jõuavad olekusse. */
export function soojenda() {
	const tood = [];
	for (const p of aktiivsed()) {
		if (typeof p.soojenda !== 'function') continue;
		tood.push(
			Promise.resolve()
				.then(() => p.soojenda(ctx))
				.catch((e) => {
					const o = olek(p);
					o.viga = String(e.message || e).slice(0, 200);
					o.vigaAeg = new Date().toISOString();
				})
		);
	}
	/* kui vood on laetud, ehita pildikataloog; siis iga 6 h uuesti (vood värskenevad ise) */
	Promise.all(tood).then(() => pildiKataloog()).catch(() => {});
	if (!_kataloogiTaimer) {
		_kataloogiTaimer = setInterval(() => pildiKataloog().catch(() => {}), 6 * 3600 * 1000);
		_kataloogiTaimer.unref?.();
	}
}
let _kataloogiTaimer = null;

/** Ühe pakkuja ühe mõõdu tooted (vahemälus). */
async function tooted(p, moot) {
	return vahemalus(`h:${p.id}:${moot}`, p.ttlHinnad || 3600, async () => {
		const list = await p.hinnadMoodus(moot, ctx);
		return Array.isArray(list) ? list : [];
	});
}

export async function hinnadMoodus(moot) {
	const pakkujad = aktiivsed();
	if (!pakkujad.length) return { available: false, hinnad: {} };
	/* lamell/suverehv: märgise read + testitud mitte-naastrehvid; naastrehv (pakkuja paneb
	   t.naast = true): AINULT naastrehvide seast — muidu saaks naastrehv sama nimega
	   lamellrehvi märgise andmed (nt „Vanpro Winter“ naastuga vs ilma) */
	/* 1) pakkujate tootenimekirjad (vahemälus) */
	const listid = await Promise.all(
		pakkujad.map(async (p) => {
			const o = olek(p);
			try {
				const list = await tooted(p, moot);
				o.edu = new Date().toISOString();
				return list;
			} catch (e) {
				o.viga = String(e.message || e).slice(0, 200);
				o.vigaAeg = new Date().toISOString();
				return null;
			}
		})
	);
	/* 2) sobitamine (leiaRehv) on CPU-raske: 30–110 ms mõõdu ja pakkuja kohta (audit 17.10).
	   Kui ühegi pakkuja nimekiri pole muutunud (sama vahemälu objekt), anname eelmise tulemuse. */
	const eel = _sobitatud.get(moot);
	if (eel && eel.listid.length === listid.length && eel.listid.every((l, i) => l === listid[i])) return eel.tulemus;
	const read = eprelSize(moot).concat(testRead());
	const readNaast = naastRead();
	const hinnad = {};
	/* kasutatud rehvid eraldi (Tarvo 24.10): vanad tarbijad (hinnad) näevad ainult uusi;
	   lehel tulevad need nähtavale ainult linnukesega „Näita ka kasutatud rehve“ */
	const kasutatud = {};
	pakkujad.forEach((p, pi) => {
			const o = olek(p);
			const list = listid[pi];
			if (!list) return;
			o.tooteid = list.length;
			let sob = 0;
			for (const t of list) {
				/* ainult mõistlik hind ja õige mõõt — muu visatakse ära */
				const hind = Number(t.hind);
				if (!(hind > 5 && hind < 5000)) continue;
				if (normMoot(t.moot) !== moot) continue;
				const slug = leiaRehv(t, t.naast ? readNaast : read);
				if (!slug) continue;
				sob++;
				const id = slug + '@' + moot;
				const siht = t.kasutatud ? kasutatud : hinnad;
				(siht[id] = siht[id] || []).push({
					myyja: myyjaNimi(t.myyja) || p.nimi,
					hind: Math.round(hind * 100) / 100,
					url: t.url ? poeLink(p, t.url) : null,
					laos: t.laos === undefined ? undefined : !!t.laos,
					/* laoseis tükkides (kui pakkuja annab) ja „u X €“ märge */
					...(Number.isInteger(t.kogus) && t.kogus >= 0 ? { kogus: Math.min(t.kogus, 99) } : {}),
					/* ostukogus (Minurattad 25.10): hind on alati 1 tk kohta; min = müük alates N tk,
					   komplekt = müüakse ainult N-kaupa (kasutatud komplektid). Ainult 2..8. */
					...(Number.isInteger(t.min) && t.min > 1 && t.min <= 8 ? { min: t.min } : {}),
					...(Number.isInteger(t.komplekt) && t.komplekt > 1 && t.komplekt <= 8 ? { komplekt: t.komplekt } : {}),
					...(t.umbes ? { umbes: true } : {}),
					/* kaardil saab näidata pilti /api/pilt/<slug> kaudu */
					...(t.pilt && lubatud(p, t.pilt) ? { pilt: true } : {}),
					...(t.kasutatud ? { kasutatud: true, ...(t.muster ? { muster: t.muster } : {}), ...(/^\d{4}$/.test(String(t.dot || '')) ? { dot: String(t.dot) } : {}) } : {})
				});
				if (t.kasutatud) continue; /* kasutatud rehvi foto ei sobi rehvi pildiks */
				/* iga rehvi kohta kuni 3 pildiallikat eri pakkujatelt: kui esimese pilt on katki
				   (Tarvo 22.10: Ventus Prime 4 jäi pildita), proovib /api/pilt järgmist */
				if (t.pilt && lubatud(p, t.pilt)) lisaPildiAllikas(p, slug, t.pilt);
			}
			o.sobitatud = sob;
	});
	/* odavaim ees; üks rida müüja kohta */
	for (const H of [hinnad, kasutatud])
		for (const id of Object.keys(H)) {
			const parim = new Map();
			for (const r of H[id]) if (!parim.has(r.myyja) || r.hind < parim.get(r.myyja).hind) parim.set(r.myyja, r);
			H[id] = [...parim.values()].sort((a, b) => a.hind - b.hind);
		}
	const tulemus = { available: true, hinnad, kasutatud };
	_sobitatud.set(moot, { listid, tulemus });
	while (_sobitatud.size > 600) _sobitatud.delete(_sobitatud.keys().next().value);
	return jagaPilte(tulemus);
}

/* poe voos pilti pole (nt Extensa) või selles mõõdus pole sama rehvi ühelgi poel pilti,
   aga sama rehvi pilt on olemas (teiselt poelt või TEISEST MÕÕDUST, pildikataloog) →
   näita seda (/api/pilt/<slug> on rehvi, mitte poe pilt).
   Tehakse iga kord väljundis, sest kataloog täieneb taustal pärast sobitamist (Tarvo 27.10). */
function jagaPilte(tulemus) {
	const jaga = (H) => {
		const out = {};
		for (const [id, read] of Object.entries(H || {}))
			out[id] = pildid.has(id.split('@')[0]) && read.some((r) => !r.pilt) ? read.map((r) => (r.pilt ? r : { ...r, pilt: true })) : read;
		return out;
	};
	/* ka kasutatud rehvi kaart saab rehvi (mitte selle konkreetse rehvi) pildi, v118 teine sessioon */
	return { ...tulemus, hinnad: jaga(tulemus.hinnad), kasutatud: jaga(tulemus.kasutatud) };
}

function lisaPildiAllikas(p, slug, url) {
	const list = pildid.get(slug) || [];
	if (list.length >= 3 || list.some((x) => x.pakkuja === p.id)) return;
	list.push({ pakkuja: p.id, url: String(url) });
	pildid.set(slug, list);
	while (pildid.size > MAX_PILTE) pildid.delete(pildid.keys().next().value);
}

/* Pildikataloog: käib läbi KÕIK mõõdud pakkujatelt, kel voog on mälus (koikMoodud), ja
   jätab meelde iga rehvi pildi. Nii saab rehv pildi ka mõõdus, kus seda pilti ühelgi poel
   pole (Giti GitiPremium H1 235/55 R17 Extensas). Taustal, mõõt korraga, sündmustsüklit
   blokeerimata; uuesti iga 6 h. */
let _kataloog = null;
const kataloogiOlek = { mootudeid: 0, rehve: 0, valmis: null, kestusMs: 0 };
async function pildiKataloog() {
	if (_kataloog) return _kataloog;
	_kataloog = (async () => {
		const algus = Date.now();
		let moote = 0;
		for (const p of aktiivsed()) {
			if (typeof p.koikMoodud !== 'function') continue;
			for (const [moot, list] of p.koikMoodud()) {
				const pildiga = list.filter((t) => !t.kasutatud && t.pilt && lubatud(p, t.pilt));
				if (!pildiga.length) continue;
				const read = eprelSize(moot).concat(testRead());
				const readNaast = naastRead();
				for (const t of pildiga) {
					const slug = leiaRehv(t, t.naast ? readNaast : read);
					if (slug) lisaPildiAllikas(p, slug, t.pilt);
				}
				moote++;
				await new Promise((r) => setImmediate(r));
			}
		}
		Object.assign(kataloogiOlek, { mootudeid: moote, rehve: pildid.size, valmis: new Date().toISOString(), kestusMs: Date.now() - algus });
	})().finally(() => {
		_kataloog = null;
	});
	return _kataloog;
}
const _sobitatud = new Map(); // moot -> { listid, tulemus }

/** ids = ['slug@20555R16', …] */
export async function hinnadIdd(ids) {
	const mood = [...new Set(ids.map((i) => i.split('@')[1]))];
	const out = { available: aktiivsed().length > 0, hinnad: {}, kasutatud: {} };
	for (const m of mood) {
		const r = await hinnadMoodus(m);
		for (const id of ids) if (id.endsWith('@' + m)) {
			if (r.hinnad[id]) out.hinnad[id] = r.hinnad[id];
			if (r.kasutatud && r.kasutatud[id]) out.kasutatud[id] = r.kasutatud[id];
		}
	}
	return out;
}

/** Pildi allikas rehvile — URL ei lähe kunagi brauserisse, ainult /api/pilt/<slug>. */
export async function pilt(slug) {
	return (await pildiAllikad(slug))[0] || null;
}
/** Kõik teadaolevad pildiallikad (eri pakkujatelt), parim ees. */
export async function pildiAllikad(slug) {
	if (pildid.has(slug)) return pildid.get(slug);
	/* pakkuja võib pakkuda ka eraldi pildiotsingut (valikuline) */
	for (const p of aktiivsed()) {
		if (typeof p.pilt !== 'function') continue;
		try {
			const url = await vahemalus(`p:${p.id}:${slug}`, 7 * 86400, () => p.pilt(slug, ctx));
			if (url && lubatud(p, url)) {
				const v = [{ pakkuja: p.id, url }];
				pildid.set(slug, v);
				return v;
			}
		} catch (e) {
			const o = olek(p);
			o.viga = String(e.message || e).slice(0, 200);
			o.vigaAeg = new Date().toISOString();
		}
	}
	return [];
}

export const pakkujaId = (id) => PAKKUJAD.find((p) => p.id === id) || null;

/** Olek administraatorile. Muutujate NIMED, mitte väärtused. */
export function olekKoond() {
	return {
		pakkujad: PAKKUJAD.map((p) => ({
			id: p.id,
			nimi: p.nimi,
			sees: koikOlemas(p.env || []),
			puuduvadMuutujad: (p.env || []).filter((n) => !muutuja(n)),
			...olek(p),
			...(typeof p.lisaOlek === 'function' ? { fail: p.lisaOlek() } : {})
		})),
		vahemalu: { ...vmStat, kirjeid: vmSuurus() },
		pilte: pildid.size,
		pildiKataloog: kataloogiOlek,
		supabase: { sees: sbSees(), failsafe: { ...failsafeOlek }, logi: { ...sbLogiOlek }, puhver: { ...pusivusOlek } }
	};
}
