/* Andmekiht — sama roll, mis oli inc/data.php-l.
 *
 * Teema ei oma andmeid: kõik tuleb failidest static/data/*.json, mille
 * kirjutab pidurdus/export_wp.py samast allikast, kust tuleb mootor.
 * Siin ainult loetakse. Ehituse (prerender) ajal loeme failisüsteemist,
 * sest siis ei ole serverit, kellelt küsida.
 */
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

/* Ehituse ajal loetakse andmed projekti static/data kaustast. NB: tee
   arvutatakse töökaustast, mitte import.meta.url'ist — SSR-i ehitusel
   satub see fail kokkupakitud kausta ja suhteline tee ei viiks enam
   andmeteni. Vaikselt tühja tagastada ei tohi: siis ehitaks leht end
   ilma sisuta. */
/* Ehituse ajal: static/data. Töötavas serveris (Docker) static-kausta ei
   ole — sama sisu on build/client/data all; seda kasutavad API-d. */
const DATA = [join(process.cwd(), 'static/data'), join(process.cwd(), 'build/client/data')].find((d) =>
	existsSync(join(d, 'core.json'))
) || join(process.cwd(), 'static/data');
const _mem = new Map();

function json(rel) {
	if (_mem.has(rel)) return _mem.get(rel);
	let v = null;
	try {
		v = JSON.parse(readFileSync(join(DATA, rel), 'utf-8'));
	} catch (e) {
		if (rel === 'core.json' || rel === 'models.json') {
			throw new Error('Andmefaili ei leitud: ' + join(DATA, rel));
		}
		v = null; /* puuduv mõõt on lubatud */
	}
	_mem.set(rel, v);
	return v;
}

import { titleCase } from '../util.js';
export * from '../util.js';

export const core = () =>
	json('core.json') || { vehicles: [], tyres: [], sources: {}, sizes: [] };
export const models = () => json('models.json') || {};
export const model = (slug) => models()[slug] || null;

/** EPREL-i read ühes mõõdus: [slug, mark, nimi, katNr, märg, kütus, dB, müraKl, lipud, testKey] */
export function eprelSize(mootN) {
	if (!/^[0-9A-Za-z]+$/.test(mootN)) return [];
	return json('eprel/' + mootN + '.json') || [];
}

let _sizeBySlug = null;
export function sizeBySlug(slug) {
	if (!_sizeBySlug) {
		_sizeBySlug = new Map(core().sizes.map((s) => [s.slug, s]));
	}
	return _sizeBySlug.get(slug) || null;
}

let _testedByKey = null, _testedBySlug = null;
function testedIndex() {
	if (!_testedByKey) {
		_testedByKey = new Map();
		_testedBySlug = new Map();
		for (const t of core().tyres) {
			_testedByKey.set(t.key, t);
			if (t.slug) _testedBySlug.set(t.slug, t);
		}
	}
}
export function testedByKey(key) {
	testedIndex();
	return _testedByKey.get(key) || null;
}
export function testedBySlug(slug) {
	testedIndex();
	return _testedBySlug.get(slug) || null;
}
export const source = (code) => core().sources[code] || null;

/* ------------------------------------------------------ indekseerimine
 * Kõik rehvilehed jäävad kasutajale alles. Google'ile pakume aga ainult
 * neid, millel on päris sisu -- uuel domeenil näeksid 5 500 sarnast
 * mallilehte välja nagu masinaga toodetud sisu ("scaled content").
 *
 *   testitud rehv                         -> indeksis + saidikaardis
 *   "mudel", mille nimes on mõõt (SKU)    -> noindex (Nankang 205/45R17 …)
 *   tootjavariant (AO, MO, N0, VOL, XL …),
 *     mille emamudel on olemas            -> canonical emamudelile (mitte noindex:
 *                                            Google ei soovita neid kokku panna)
 *   ≤ 2 mõõtu ja testi pole               -> noindex
 *   ülejäänud                             -> indeksis, saidikaarti partiidena
 *
 * Partii suurendamiseks alanda SITEMAP_MUDEL_MIN_MOOTE (nt 20 → 10 → 3),
 * kui Search Console näitab, et eelmine partii on indekseeritud.
 */
export const SITEMAP_MUDEL_MIN_MOOTE = Infinity; // 1. partii: ainult testitud

const SKU_RE = /\d{3}-?\d{2}-?z?r\d{2}/;
/* ainult tootja märgistuse koodid -- mitte "suv", "plus", "4x4", mis on
   päris eri mudelid */
const VARIANT = new Set(
	('a ao ao1 ao2 n0 n1 n2 n3 n4 n5 n6 mo mo1 mos moe vol j jlr lr ro1 ro2 r01 r02 ' +
		't0 t1 t2 xl rf rft runflat ssr zp dt dt1 dt2 star seal sealinside acoustic ' +
		'contisilent contiseal silent nf0 nd0 ng0 ne0 nh0 hl elt mfs').split(' ')
);

/** Emamudel, kui slug on tootjavariant (michelin-pilot-sport-4-a-ao → michelin-pilot-sport-4). */
export function emamudel(slug) {
	const m = models();
	let toks = String(slug).split('-');
	while (toks.length > 2 && VARIANT.has(toks[toks.length - 1])) {
		toks = toks.slice(0, -1);
		const p = toks.join('-');
		if (m[p]) return p;
	}
	return null;
}

/** { index, sitemap, canonical } rehvilehe jaoks. */
export function rehviIndeks(slug) {
	const t = tyrePage(slug);
	if (!t) return { index: false, sitemap: false, canonical: null };
	if (t.tested) return { index: true, sitemap: true, canonical: null };
	const n = t.model ? t.model.sizes.length : 0;
	if (SKU_RE.test(slug)) return { index: false, sitemap: false, canonical: null };
	const ema = emamudel(slug);
	if (ema) return { index: true, sitemap: false, canonical: ema };
	if (n <= 2) return { index: false, sitemap: false, canonical: null };
	return { index: true, sitemap: n >= SITEMAP_MUDEL_MIN_MOOTE, canonical: null };
}

/** Rehvileht on olemas, kui slug on kas EPREL-i mudel või mõõdetud rehv. */
export function tyrePage(slug) {
	const m = model(slug);
	let tested = m && m.tested ? testedByKey(m.tested) : null;
	if (!tested) tested = testedBySlug(slug);
	if (!m && !tested) return null;
	const name = m ? (m.mark + ' ' + m.nimi).trim() : tested.name;
	const brand = m ? m.mark : String(tested.name).split(' ')[0];
	return {
		slug,
		name: titleCase(name),
		brand: titleCase(brand),
		cat: (tested && tested.category) || (m && m.kat) || '',
		model: m,
		tested
	};
}

/** Mõõdetud testid, kus MÕLEMAD rehvid olid koos (sama auto, sama päev). */
export function sharedSources(a, b) {
	if (!a || !b || !a.tested || !b.tested || a.slug === b.slug) return [];
	const sa = new Set(a.tested.tests.map((t) => t.src));
	return [...new Set(b.tested.tests.map((t) => t.src))].filter((s) => sa.has(s));
}


/** Koht selles testis samal pinnal (1 = parim). */
export function rankInTest(x) {
	const all = [];
	for (const o of core().tyres) {
		for (const y of o.tests) {
			if (y.src === x.src && y.surf === x.surf && y.wet === x.wet && y.v0 === x.v0) all.push(y.m);
		}
	}
	all.sort((a, b) => a - b);
	const pos = all.indexOf(x.m);
	return [pos < 0 ? null : pos + 1, all.length, all.length ? all[0] : null];
}

/** Mitu märgisega mudelit on selles mõõdus. */
export function sizeModelCount(m) {
	return eprelSize(m).length;
}
export const SIZE_MIN_MODELS = 10;

/** "vs" paarid, millel on päris sisu: kaks rehvi SAMAS testis, naabrid
 *  märja pidurduse järjestuses (mitte kõik 31×30 kombinatsiooni). */
let _pairs = null;
export function vsPairs() {
	if (_pairs) return _pairs;
	const by = {};
	for (const t of core().tyres) {
		for (const x of t.tests) {
			if (x.surf === 'ASPHALT' && x.wet) (by[x.src] = by[x.src] || []).push([t.slug, x.m]);
		}
	}
	const seen = new Map();
	for (const list of Object.values(by)) {
		list.sort((a, b) => a[1] - b[1]);
		for (let i = 0; i + 1 < list.length; i++) {
			const a = list[i][0], b = list[i + 1][0];
			const k = a < b ? [a, b] : [b, a];
			seen.set(k[0] + '|' + k[1], k);
		}
	}
	_pairs = [...seen.values()];
	return _pairs;
}
export function vsLinksFor(slug) {
	return vsPairs().filter((p) => p[0] === slug || p[1] === slug);
}
