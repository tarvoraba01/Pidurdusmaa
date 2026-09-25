/* Koondab kõigi sisse lülitatud pakkujate andmed meie rehvide külge.
 *
 *   hinnadMoodus('20555R16') → { available, hinnad: { 'slug@20555R16': [ {myyja, hind, url, laos} ] } }
 *   pilt('michelin-pilot-sport-5') → { pakkuja, url } | null   (URL jääb serverisse)
 *   olek() → mis on sees, mis puudu, viimased vead (ilma saladusteta)
 *
 * Brauser ei räägi kunagi pakkujaga otse: kõik käib meie serveri kaudu,
 * seega ei näe keegi võtmeid ega pakkuja API aadresse.
 */
import { PAKKUJAD } from './pakkujad/index.js';
import { muutuja, koikOlemas } from './seaded.js';
import { jsonParing, paring, lubatud } from './http.js';
import { vahemalus, stat as vmStat, suurus as vmSuurus } from './vahemalu.js';
import { leiaRehv, normMoot } from './sobitus.js';
import { eprelSize } from '$lib/server/andmed.js';

const ctx = { muutuja, jsonParing, paring };
const olekud = new Map(); // id -> { viga, vigaAeg, edu, tooteid, sobitatud }
const pildid = new Map(); // slug -> { pakkuja, url }
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
	const read = eprelSize(moot);
	const hinnad = {};
	await Promise.all(
		pakkujad.map(async (p) => {
			const o = olek(p);
			let list = [];
			try {
				list = await tooted(p, moot);
				o.edu = new Date().toISOString();
			} catch (e) {
				o.viga = String(e.message || e).slice(0, 200);
				o.vigaAeg = new Date().toISOString();
				return;
			}
			o.tooteid = list.length;
			let sob = 0;
			for (const t of list) {
				/* ainult mõistlik hind ja õige mõõt — muu visatakse ära */
				const hind = Number(t.hind);
				if (!(hind > 5 && hind < 5000)) continue;
				if (normMoot(t.moot) !== moot) continue;
				const slug = leiaRehv(t, read);
				if (!slug) continue;
				sob++;
				const id = slug + '@' + moot;
				(hinnad[id] = hinnad[id] || []).push({
					myyja: p.nimi,
					hind: Math.round(hind * 100) / 100,
					url: t.url ? poeLink(p, t.url) : null,
					laos: t.laos === undefined ? undefined : !!t.laos
				});
				if (t.pilt && lubatud(p, t.pilt) && !pildid.has(slug)) {
					pildid.set(slug, { pakkuja: p.id, url: String(t.pilt) });
					while (pildid.size > MAX_PILTE) pildid.delete(pildid.keys().next().value);
				}
			}
			o.sobitatud = sob;
		})
	);
	/* odavaim ees; üks rida müüja kohta */
	for (const id of Object.keys(hinnad)) {
		const parim = new Map();
		for (const r of hinnad[id]) if (!parim.has(r.myyja) || r.hind < parim.get(r.myyja).hind) parim.set(r.myyja, r);
		hinnad[id] = [...parim.values()].sort((a, b) => a.hind - b.hind);
	}
	return { available: true, hinnad };
}

/** ids = ['slug@20555R16', …] */
export async function hinnadIdd(ids) {
	const mood = [...new Set(ids.map((i) => i.split('@')[1]))];
	const out = { available: aktiivsed().length > 0, hinnad: {} };
	for (const m of mood) {
		const r = await hinnadMoodus(m);
		for (const id of ids) if (id.endsWith('@' + m) && r.hinnad[id]) out.hinnad[id] = r.hinnad[id];
	}
	return out;
}

/** Pildi allikas rehvile — URL ei lähe kunagi brauserisse, ainult /api/pilt/<slug>. */
export async function pilt(slug) {
	if (pildid.has(slug)) return pildid.get(slug);
	/* pakkuja võib pakkuda ka eraldi pildiotsingut (valikuline) */
	for (const p of aktiivsed()) {
		if (typeof p.pilt !== 'function') continue;
		try {
			const url = await vahemalus(`p:${p.id}:${slug}`, 7 * 86400, () => p.pilt(slug, ctx));
			if (url && lubatud(p, url)) {
				const v = { pakkuja: p.id, url };
				pildid.set(slug, v);
				return v;
			}
		} catch (e) {
			const o = olek(p);
			o.viga = String(e.message || e).slice(0, 200);
			o.vigaAeg = new Date().toISOString();
		}
	}
	return null;
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
			...olek(p)
		})),
		vahemalu: { ...vmStat, kirjeid: vmSuurus() },
		pilte: pildid.size
	};
}
