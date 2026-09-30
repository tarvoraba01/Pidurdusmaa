/* Automudelite lehed (/autod/…): üks leht auto PÕLVKONNA kohta.
 *
 * Kõik numbrid tulevad samadest andmetest, mis kalkulaator:
 *   core.json      põlvkonna read (mass, pidurid, ABS, tehase mõõdud)
 *   mootorid.json  tehase mootorid (+ mootori enda rehvimõõt ja mass)
 *   eprel/<mõõt>   rehvid selles mõõdus (EL-i märgis, testid)
 * Pidurdusmaa arvutatakse ehituse ajal sama mootoriga (engine.js).
 */
import '$lib/engine.js';
import { core, mootoridJson, eprelSize, sizeModelCount, SIZE_MIN_MODELS, markSlug, titleCase, pretty, sizeSlug } from './andmed.js';
import { EPREL_KAT, KAT_NIMI } from '../util.js';

export const slugify = (s) => markSlug(s);
const P = () => globalThis.Pidurdus;

const KYTUS = { b: 'bensiin', d: 'diisel', h: 'hübriid', p: 'pistikhübriid', e: 'elekter', g: 'gaas', bg: 'bensiin/gaas' };
const norm = (m) => String(m || '').toUpperCase().replace(/[/ ]/g, '');

let _idx = null;
/** { margid: Map(markSlug → {slug, nimi, polved: [...]}), polved: Map('mark/polv' → polv) } */
export function autod() {
	if (_idx) return _idx;
	const margid = new Map();
	const polved = new Map();
	const grupp = new Map();
	for (const v of core().vehicles) {
		if (v.make === 'Ei leia oma autot' || !v.model) continue;
		const g = v.make + '|' + v.model + '|' + v.yearLabel;
		if (!grupp.has(g)) grupp.set(g, []);
		grupp.get(g).push(v);
	}
	for (const rows of grupp.values()) {
		const v0 = rows[0];
		const mk = slugify(v0.make.split(' /')[0]);
		const makeNimi = v0.make.split(' /')[0];
		const slug = slugify(v0.model + ' ' + v0.yearLabel);
		const aasta = +((/(\d{4})/.exec(v0.yearLabel) || [0, 0])[1]);
		const p = { mk, slug, make: makeNimi, model: v0.model, yearLabel: v0.yearLabel, years: v0.years, aasta, rows };
		if (!margid.has(mk)) margid.set(mk, { slug: mk, nimi: makeNimi, polved: [] });
		margid.get(mk).polved.push(p);
		const voti = mk + '/' + slug;
		if (polved.has(voti)) throw new Error('Autolehe aadress kordub: ' + voti);
		polved.set(voti, p);
	}
	for (const m of margid.values())
		m.polved.sort((a, b) => a.model.localeCompare(b.model, 'et', { numeric: true }) || b.aasta - a.aasta);
	_idx = { margid, polved };
	return _idx;
}

export const polveNimi = (p) => `${p.make} ${p.model} ${p.yearLabel}`.replace(/\s+/g, ' ').trim();

/* EPREL-i ridadest parimad rehvid: testitud ees, siis märghaare, siis müra */
function parimad(mootN, kat, n = 6) {
	const ki = EPREL_KAT.indexOf(kat);
	return eprelSize(mootN)
		.filter((r) => r[3] === ki)
		.sort((a, b) => (b[9] ? 1 : 0) - (a[9] ? 1 : 0) || String(a[4]).localeCompare(String(b[4])) || (a[6] ?? 99) - (b[6] ?? 99))
		/* sama mudel mitme koormus-/kiirusindeksiga -> üks rida */
		.filter((r, i, arr) => arr.findIndex((x) => x[0] === r[0]) === i)
		.slice(0, n)
		.map((r) => ({ slug: r[0], nimi: titleCase(r[1] + ' ' + r[2]), g: r[4], db: r[6], testitud: !!r[9] }));
}

/* Pidurdusmaa: tüüpiline C-klassi rehv, uus muster, reaktsioon 1 s */
const OLUD = [
	['kuiv', 'Kuiv asfalt', 'SUMMER_TOURING', { surface: 'ASPHALT', waterMm: 0, tempC: 15 }],
	['marg', 'Märg asfalt', 'SUMMER_TOURING', { surface: 'ASPHALT', waterMm: 1, tempC: 10 }],
	['lumiT', 'Tallatud lumi, talverehv', 'WINTER_NORDIC', { surface: 'SNOW_PACKED', waterMm: 0, tempC: -5 }],
	['lumiS', 'Tallatud lumi, suverehv', 'SUMMER_TOURING', { surface: 'SNOW_PACKED', waterMm: 0, tempC: -5 }]
];
function pidurdus(veh) {
	const gc = core().gClass || {};
	const rida = gc.C || {};
	const out = [];
	for (const [id, nimi, kat, c] of OLUD) {
		const g = (rida[kat] || rida._ || [1.3])[0];
		const tyre = { key: 'x', name: 'x', category: kat, wetGripIndex: g, treadDepthMm: 8, treadDepthNewMm: 8, ageYears: 1,
			pressureBar: null, loadCapacityKg: null, studded: false, size: veh.oemSize, gSource: 'label' };
		const r = {};
		for (const kmh of [50, 90]) {
			try {
				const x = P().stoppingDistance(tyre, veh, { speedKmh: kmh, texture: 'NORMAL', payloadKg: 75, gradientPct: 0,
					reactionTimeS: 1, brakeCondition: 1, ...c });
				r[kmh] = { peatumine: x.stopped ? x.totalDistanceM : null, pidurdus: x.stopped ? x.distanceM : null };
			} catch {
				r[kmh] = null;
			}
		}
		out.push({ id, nimi, r });
	}
	return out;
}

const r1 = (x) => (x == null ? null : Math.round(x * 10) / 10);

export function polveLeht(p) {
	const rows = p.rows;
	const baas = rows[0];
	const M = mootoridJson();
	/* mootorid: päris read + nende "eng" valikud */
	const mootorid = [];
	for (const v of rows) {
		const hp = /(\d+) hj/.exec(v.variant || '');
		mootorid.push({ silt: v.variant === '—' ? '' : v.variant, kytus: KYTUS[v.fuel] || '', aastad: v.years, ord: v.engOrd ?? 0,
			moot: v.oemSize, mass: v.kerbMassKg, key: v.key, hp: hp ? +hp[1] : null });
		for (const e of M[v.key] || []) {
			const o = e[5] || {};
			mootorid.push({ silt: e[0], kytus: KYTUS[e[1]] || '', aastad: e[2] || v.years, ord: e[4], moot: o.o || v.oemSize,
				mass: o.m || v.kerbMassKg, key: v.key + '~' + e[3], oma: !!o.o });
		}
	}
	mootorid.sort((a, b) => a.ord - b.ord);
	/* tehase mõõdud: põlvkonna kõik + mootorite omad */
	const kogu = new Set();
	for (const v of rows) for (const z of v.oemSizes && v.oemSizes.length ? v.oemSizes : [v.oemSize]) kogu.add(norm(z));
	for (const m of mootorid) kogu.add(norm(m.moot));
	kogu.delete('');
	const pohiN = norm(baas.oemSize);
	const moodud = [...kogu]
		.map((m) => ({ m, label: pretty(m), slug: sizeModelCount(m) >= SIZE_MIN_MODELS ? sizeSlug(m) : null, pohi: m === pohiN }))
		.sort((a, b) => (b.pohi ? 1 : 0) - (a.pohi ? 1 : 0) || a.m.localeCompare(b.m));

	const absTekst = baas.absOpt
		? 'ABS oli selle põlvkonna lisavarustus — kalkulaatoris saad märkida, kas sinu autol on.'
		: baas.absClass === 'NONE'
			? 'Sellel autol ABS-i ei olnud — järsul pidurdamisel võivad rattad lukustuda.'
			: 'ABS on standardvarustuses.';

	const muudPolved = autod().margid.get(p.mk).polved.filter((x) => x.model === p.model && x.slug !== p.slug)
		.map((x) => ({ slug: x.slug, nimi: polveNimi(x) }));

	const allikad = [...new Set([baas.oemSrc, ...rows.flatMap(() => [])].filter(Boolean))];

	return {
		auto: { mk: p.mk, slug: p.slug, make: p.make, model: p.model, yearLabel: p.yearLabel, nimi: polveNimi(p), key: baas.key },
		pohimoot: pretty(pohiN),
		pohimootSlug: sizeModelCount(pohiN) >= SIZE_MIN_MODELS ? sizeSlug(pohiN) : null,
		moodud,
		mootorid,
		mass: baas.kerbMassKg,
		absTekst,
		pidurdus: pidurdus(baas).map((x) => ({ ...x, r: Object.fromEntries(Object.entries(x.r).map(([k, v]) => [k, v && { peatumine: r1(v.peatumine), pidurdus: r1(v.pidurdus) }])) })),
		suvi: parimad(pohiN, 'SUMMER_TOURING'),
		talv: parimad(pohiN, 'WINTER_NORDIC'),
		aastaring: parimad(pohiN, 'ALL_SEASON', 4),
		muudPolved,
		allikad,
		katNimi: { suvi: KAT_NIMI.SUMMER_TOURING, talv: KAT_NIMI.WINTER_NORDIC, aastaring: KAT_NIMI.ALL_SEASON }
	};
}
