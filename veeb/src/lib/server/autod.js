/* Automudelite lehed (/autod/…): üks leht auto PÕLVKONNA kohta.
 *
 * Kõik numbrid tulevad samadest andmetest, mis kalkulaator:
 *   core.json      põlvkonna read (mass, pidurid, ABS, tehase mõõdud)
 *   mootorid.json  tehase mootorid (+ mootori enda rehvimõõt ja mass)
 *   eprel/<mõõt>   rehvid selles mõõdus (EL-i märgis, testid)
 * Pidurdusmaa arvutatakse ehituse ajal sama mootoriga (engine.js).
 */
import '$lib/engine.js';
import { core, mootoridJson, eprelSize, sizeModelCount, SIZE_MIN_MODELS, markSlug, titleCase, pretty, sizeSlug, rehviIndeks } from './andmed.js';
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
		/* ainult indekseeritavad rehvilehed (noindex-lehele lingid raiskavad roomamist) */
		.filter((r) => rehviIndeks(r[0]).index)
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
			mootorid.push({ silt: e[0], kytus: KYTUS[e[1]] || '', aastad: String(e[2] || v.years || '').replace(/\s*-\s*present\b/gi, '+'), ord: e[4], moot: o.o || v.oemSize,
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
		auto: { mk: p.mk, slug: p.slug, make: p.make, model: p.model, yearLabel: p.yearLabel, nimi: polveNimi(p), key: baas.key, keha: baas.body || 'SOIDUAUTO' },
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

/** Rehvikalkulaatori tabel: levinumad põhimõõdud ja mõõdud, mis on SAMADEL autodel ka tehasemõõt
 *  (päris asendusvõimalused, mitte ainult ±1,5 % läbimõõdu reegel, mis pakuks ka 255/30 R19 → 195/65 R15).
 *  [{ m, label, slug, d, n, alt: [{ m, label, slug, n, pct }] }] */
let _kaas = null;
/** Ühe mõõdu kaasmõõdud: mõõdud, mis on SAMADEL autodel (põlvkondadel) samuti tehasemõõt, sama
 *  läbimõõduga (±3 %), enim autosid ees. Talverehvide lehe „samadel autodel ka …“ lause ja lingid.
 *  [{ m, n, pct }] */
export function kaasMoot(mootN, k = 4) {
	if (!_kaas) {
		_kaas = new Map();
		const M = mootoridJson();
		for (const p of autod().polved.values()) {
			const koik = new Set();
			for (const v of p.rows) {
				for (const z of v.oemSizes && v.oemSizes.length ? v.oemSizes : [v.oemSize]) koik.add(norm(z));
				for (const e of M[v.key] || []) for (const z of (e[5] && e[5].s) || []) koik.add(norm(z));
			}
			koik.delete('');
			for (const a of koik) {
				if (!_kaas.has(a)) _kaas.set(a, new Map());
				const c = _kaas.get(a);
				for (const b of koik) if (b !== a) c.set(b, (c.get(b) || 0) + 1);
			}
		}
	}
	const lm = (m) => { const x = /^(\d{3})(\d{2})R(\d{2})$/.exec(m); return x ? +x[3] * 25.4 + (2 * +x[1] * +x[2]) / 100 : null; };
	const m = norm(mootN), d = lm(m);
	if (!d) return [];
	return [...(_kaas.get(m) || new Map()).entries()]
		.filter(([z]) => lm(z))
		.map(([z, n]) => ({ m: z, n, pct: Math.round(((lm(z) - d) / d) * 1000) / 10 }))
		.filter((x) => Math.abs(x.pct) <= 3)
		.sort((a, b) => b.n - a.n || Math.abs(a.pct) - Math.abs(b.pct))
		.slice(0, k);
}

export function kaasMoodud(top = 10, k = 3) {
	const M = mootoridJson();
	const lm = (m) => { const x = /^(\d{3})(\d{2})R(\d{2})$/.exec(m); return x ? +x[3] * 25.4 + (2 * +x[1] * +x[2]) / 100 : null; };
	const pohiN = new Map(), koos = new Map();
	for (const p of autod().polved.values()) {
		const pohi = norm(p.rows[0].oemSize);
		const koik = new Set();
		for (const v of p.rows) {
			for (const z of v.oemSizes && v.oemSizes.length ? v.oemSizes : [v.oemSize]) koik.add(norm(z));
			for (const e of M[v.key] || []) for (const z of (e[5] && e[5].s) || []) koik.add(norm(z));
		}
		koik.delete('');
		if (!lm(pohi)) continue;
		pohiN.set(pohi, (pohiN.get(pohi) || 0) + 1);
		if (!koos.has(pohi)) koos.set(pohi, new Map());
		for (const z of koik) if (z !== pohi && lm(z)) koos.get(pohi).set(z, (koos.get(pohi).get(z) || 0) + 1);
	}
	/* link ainult mõõdulehele, mis on olemas */
	const slug = (m) => (sizeModelCount(m) >= SIZE_MIN_MODELS ? sizeSlug(m) : null);
	return [...pohiN.entries()]
		.sort((a, b) => b[1] - a[1])
		.slice(0, top)
		.map(([m, n]) => {
			const d = lm(m);
			const alt = [...(koos.get(m) || new Map()).entries()]
				.map(([z, c]) => ({ m: z, label: pretty(z), slug: slug(z), n: c, pct: Math.round(((lm(z) - d) / d) * 1000) / 10 }))
				.filter((x) => Math.abs(x.pct) <= 3)
				.sort((a, b) => b.n - a.n || Math.abs(a.pct) - Math.abs(b.pct))
				.slice(0, k);
			return { m, label: pretty(m), slug: slug(m), d: Math.round(d), n, alt };
		})
		.filter((x) => x.alt.length);
}

let _moodus = null;
/** mõõt (nt 20555R16) → autolehed, millel see on tehasemõõt.
 *  pohi = põlvkonna põhimõõt (kõige tavalisem), muidu üks tehase mõõtudest. */
export function autodMoodus(mootN) {
	if (!_moodus) {
		_moodus = new Map();
		const M = mootoridJson();
		for (const p of autod().polved.values()) {
			const pohi = norm(p.rows[0].oemSize);
			const koik = new Set();
			for (const v of p.rows) {
				for (const z of v.oemSizes && v.oemSizes.length ? v.oemSizes : [v.oemSize]) koik.add(norm(z));
				for (const e of M[v.key] || []) for (const z of (e[5] && e[5].s) || []) koik.add(norm(z));
			}
			koik.delete('');
			for (const m of koik) {
				if (!_moodus.has(m)) _moodus.set(m, []);
				_moodus.get(m).push({ nimi: polveNimi(p), url: '/autod/' + p.mk + '/' + p.slug + '/', pohi: m === pohi, aasta: p.aasta, key: p.rows[0].key });
			}
		}
		for (const list of _moodus.values())
			list.sort((a, b) => (b.pohi ? 1 : 0) - (a.pohi ? 1 : 0) || b.aasta - a.aasta || a.nimi.localeCompare(b.nimi, 'et'));
	}
	return _moodus.get(norm(mootN)) || [];
}
