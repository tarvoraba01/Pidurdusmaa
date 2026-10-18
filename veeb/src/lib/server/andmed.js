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

/* Ajakirja nimes olevad märkused on eesti/inglise keeles („mõõtis Test World“, „commissioned by …“)
   ja paistsid vene lehtedel tõlkimata (audit 18.10). Näitame ainult nimesid, mis on igas keeles samad. */
const PUB_PUHAS = [
	[/\s*\(Michelini pressiüritus, mõõtis Test World\)/, ' / Test World (Michelin)'],
	[/\s*\(koostöös (NAF Motor)\)/, ' / $1'],
	[/\s*\(mõõtis (Test World)\)/, ' / $1'],
	[/\s*\(commissioned by ([^)]+)\)/, ' / $1']
];
export function pubPuhas(p) {
	let s = String(p || '');
	for (const [re, asend] of PUB_PUHAS) s = s.replace(re, asend);
	return s;
}

function json(rel) {
	if (_mem.has(rel)) return _mem.get(rel);
	let v = null;
	try {
		/* töötavas serveris on brauseri core.json kärbitud (scripts/kliendi-andmed.mjs);
		   server loeb täisfaili */
		const taisfail = join(process.cwd(), 'build/andmed', rel);
		const fail = rel === 'core.json' && DATA.endsWith(join('build', 'client', 'data')) && existsSync(taisfail) ? taisfail : join(DATA, rel);
		v = JSON.parse(readFileSync(fail, 'utf-8'));
		if (rel === 'testid_ext.json' && v && v.allikad) for (const a of Object.values(v.allikad)) a.pub = pubPuhas(a.pub);
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
/** mootorid.json: { reaVõti: [[silt, kütus, aastad, slug, jrk, oma?], …] } (export_wp) */
export const mootoridJson = () => json('mootorid.json') || {};

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
export const SITEMAP_MUDEL_MIN_MOOTE = 3; // 2. partii: kõik indekseeritavad rehvilehed (≤2 mõõtu on noindex)

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
const _ixMemo = new Map();
export function rehviIndeks(slug) {
	if (!_ixMemo.has(slug)) _ixMemo.set(slug, rehviIndeks0(slug));
	return _ixMemo.get(slug);
}
function rehviIndeks0(slug) {
	const t = tyrePage(slug);
	if (!t) return { index: false, sitemap: false, canonical: null };
	const n = t.model ? t.model.sizes.length : 0;
	if (t.tested) {
		/* sama reegel mis lehel (+page.server.js noindex): testimata hinnangurehv, millel pole
		   teste, ajakirjateste ega ühtki mõõtu (ka poodidest), on õhuke leht → noindex, mitte saidikaardis */
		const sisu = (t.tested.tests || []).length || n || (t.tested.moodud || []).length || extTests(slug).length;
		return sisu ? { index: true, sitemap: true, canonical: null } : { index: false, sitemap: false, canonical: null };
	}
	if (SKU_RE.test(slug)) return { index: false, sitemap: false, canonical: null };
	const ema = emamudel(slug);
	if (ema) return { index: true, sitemap: false, canonical: ema };
	/* ajakirjade testides mõõdetud rehv (testid_ext.json): lehel on päris mõõtmised → saidikaardis */
	if (extTests(slug).length) return { index: true, sitemap: true, canonical: null };
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
	const m2 = /^(GT Radial|Nokian Tyres|General Tire|BF Goodrich|Double Coin)\s/i.exec(String(tested ? tested.name : ''));
	const brand = m ? m.mark : m2 ? m2[1] : String(tested.name).split(' ')[0];
	return {
		slug,
		name: titleCase(name),
		brand: titleCase(brand),
		cat: (tested && tested.category) || (m && m.kat) || '',
		model: m,
		tested
	};
}

/** Välismaa ajakirjade testid (export_testid.py) — ainult näitamiseks. */
export function extTests(slug) {
	const d = json('testid_ext.json');
	if (!d || !d.rehvid || !d.rehvid[slug]) return [];
	return d.rehvid[slug].map((x) => ({ ...x, src: d.allikad[x.t] || {} }));
}

/* ------------------------------------------------ talvetestide parimad
 * Artikli „Talverehvide test 2026“ tabel: iga talvetest (minAasta → uuemad) ja
 * igal alal (jää, lumi, märg asfalt) see rehv, mis oli testis ise 1. kohal
 * (pos === 1). Kui testi võitja pole meie andmetes (sobitamata rehv), jääb lahter
 * tühjaks — nime ei arva. Meie ankrutestid (core.json, nt Tekniikan Maailma)
 * tulevad kaasa, kui sama testi testid_ext-is pole; need sisaldavad kõiki testi
 * rehve, nii et lühim pidurdusmaa on võitja. */
const TALV_ALAD = ['jää', 'lumi', 'märg asfalt'];
const coreAla = (x) => (x.surf === 'ICE' ? 'jää' : x.surf === 'SNOW_PACKED' ? 'lumi' : x.surf === 'ASPHALT' && x.wet ? 'märg asfalt' : null);
export function talveTestideParimad(minAasta = 2025) {
	const d = json('testid_ext.json') || {};
	const testid = new Map();
	const pubNimi = (p) => String(p || '').replace(/^AUTO BILD\b/, 'Auto Bild').trim();
	const autoNimi = (a) => String(a || '').split(/ \(|;| \/ /)[0].trim();
	for (const [id, a] of Object.entries(d.allikad || {})) {
		if (a.season !== 'winter' || !(a.year >= minAasta) || /PARTIAL/i.test(id)) continue;
		testid.set(id, { id, pub: pubNimi(a.pub), aasta: a.year, moot: a.size || '', auto: autoNimi(a.car), n: 0, alad: {} });
	}
	/* võrdne tulemus → mõlemad võitjad */
	const pane = (t, ala, o) => {
		const vana = t.alad[ala];
		const r = { slug: o.slug, nimi: o.nimi };
		if (!vana || o.m < vana.m) t.alad[ala] = { m: o.m, v0: o.v0, v1: o.v1, rehvid: [r] };
		else if (o.m === vana.m && !vana.rehvid.some((x) => x.slug === o.slug)) vana.rehvid.push(r);
	};
	/* rehvitüübid testis (kõik testi rehvid, mitte ainult võitjad): naast / lamell / Kesk-Euroopa */
	const tyyp = (t, slug) => {
		const kat = (tyrePage(slug) || {}).cat || '';
		t.kat.add(/STUDDED/.test(kat) ? 'naast' : /NORDIC/.test(kat) ? 'lamell' : /CENTRAL|WINTER/.test(kat) ? 'kesk' : '');
	};
	for (const t of testid.values()) t.kat = new Set();
	for (const [slug, rows] of Object.entries(d.rehvid || {})) {
		for (const x of rows) {
			const t = testid.get(x.t);
			if (!t) continue;
			t.n = Math.max(t.n, x.n || 0);
			tyyp(t, slug);
			if (x.pos === 1 && TALV_ALAD.includes(x.d) && x.m > 0) pane(t, x.d, { slug, nimi: x.nimi, m: x.m, v0: x.v0, v1: x.v1 || 0 });
		}
	}
	const ext = [...testid.values()];
	for (const [src, s] of Object.entries(core().sources || {})) {
		if (!/talverehvi|naastrehvi|naelutute/i.test(s.nimi || '') || !(s.aasta >= minAasta)) continue;
		const pub = String(s.nimi).replace(/\s+(talverehvitest|naastrehvitest|naelutute talverehvide test).*$/i, '').trim();
		const esim = pub.split(' ')[0].toLowerCase();
		if (ext.some((t) => t.aasta === s.aasta && t.moot === s.moot && t.pub.toLowerCase().startsWith(esim))) continue;
		const t = { id: src, pub, aasta: s.aasta, moot: s.moot || '', auto: autoNimi(s.auto), n: s.rehve || 0, alad: {}, kat: new Set() };
		for (const o of core().tyres) {
			for (const x of o.tests || []) {
				const ala = x.src === src ? coreAla(x) : null;
				if (!ala || !o.slug || !(x.m > 0)) continue;
				t.kat.add(o.studded ? 'naast' : /NORDIC/.test(o.category) ? 'lamell' : 'kesk');
				pane(t, ala, { slug: o.slug, nimi: o.name, m: x.m, v0: x.v0, v1: x.v1 || 0 });
			}
		}
		testid.set(src, t);
	}
	return [...testid.values()]
		.filter((t) => Object.keys(t.alad).length)
		.map((t) => ({
			...t,
			/* 'naast' | 'lamell' | 'kesk' | 'naast+lamell' | 'segu' */
			kat: ((k) => (k.length === 1 ? k[0] : k.length === 2 && !k.includes('kesk') ? 'naast+lamell' : 'segu'))([...t.kat].filter(Boolean).sort()),
			alad: Object.fromEntries(
				Object.entries(t.alad).map(([k, o]) => [k, { ...o, rehvid: o.rehvid.map((r) => ({ ...r, ix: rehviIndeks(r.slug).index })) }])
			)
		}))
		.sort((a, b) => b.aasta - a.aasta || !!b.alad['jää'] - !!a.alad['jää'] || a.pub.localeCompare(b.pub) || a.moot.localeCompare(b.moot));
}

/* ------------------------------------------------ testid selles mõõdus
 * Mõõdulehe esimene lause (päring „205/55 R16“): selles mõõdus tehtud uusimad testid ja nende
 * võitjad — suverehvidest märjal, talverehvidest jääl (kui jääd polnud, siis märjal).
 * Ainult 2020+ testid (vanemad mudelid pole enam müügil) ja ainult testi enda 1. koht. */
const HOOAJA_KAT = { suvi: /^SUMMER/, talv: /^WINTER/, aastaring: /^ALL_SEASON/ };
export function testidMoodus(label, minAasta = 2020) {
	const d = json('testid_ext.json') || {};
	const testid = [];
	for (const [id, a] of Object.entries(d.allikad || {})) {
		if (a.size !== label || !(a.year >= minAasta) || /PARTIAL/i.test(id)) continue;
		const hooaeg = a.season === 'summer' ? 'suvi' : a.season === 'winter' ? 'talv' : a.season === 'allseason' ? 'aastaring' : null;
		if (hooaeg) testid.push({ id, pub: String(a.pub || '').split(/ \/ | \(/)[0].trim(), aasta: a.year, hooaeg, n: 0, alad: {} });
	}
	const byId = new Map(testid.map((x) => [x.id, x]));
	for (const [slug, rows] of Object.entries(d.rehvid || {})) {
		for (const x of rows) {
			const t = byId.get(x.t);
			if (!t) continue;
			t.n = Math.max(t.n, x.n || 0);
			if (x.pos !== 1 || !(x.m > 0)) continue;
			const vana = t.alad[x.d];
			if (!vana || x.m < vana.m) t.alad[x.d] = { m: x.m, v0: x.v0, v1: x.v1 || 0, rehvid: [{ slug, nimi: x.nimi }] };
			else if (x.m === vana.m && !vana.rehvid.some((r) => r.slug === slug)) vana.rehvid.push({ slug, nimi: x.nimi });
		}
	}
	/* meie ankrutestid (core.json): kõik testi rehvid on andmetes, lühim = võitja; segatestis (suvi + aastaring) eraldi hooaja kaupa */
	for (const [src, s] of Object.entries(core().sources || {})) {
		if (s.moot !== label || !(s.aasta >= minAasta)) continue;
		const nimi = String(s.nimi || '');
		const hooajad = /talverehvi|naast|naelutute/i.test(nimi) ? ['talv'] : [/suve/i.test(nimi) ? 'suvi' : null, /aastaring/i.test(nimi) ? 'aastaring' : null].filter(Boolean);
		const pub = nimi.replace(/\s+(talverehvitest|suverehvitest|aastaringsete rehvide test|suve- ja aastaringsete rehvide test|naastrehvitest).*$/i, '').trim();
		if (testid.some((x) => x.aasta === s.aasta && x.pub.split(' ')[0].toLowerCase() === pub.split(' ')[0].toLowerCase())) continue;
		for (const hooaeg of hooajad) {
			const t = { id: src + ':' + hooaeg, pub, aasta: s.aasta, hooaeg, n: 0, alad: {} };
			const loetud = new Set();
			for (const o of core().tyres) {
				if (!o.slug || !HOOAJA_KAT[hooaeg].test(o.category || '')) continue;
				for (const x of o.tests || []) {
					if (x.src !== src || !(x.m > 0)) continue;
					const ala = coreAla(x);
					if (!ala) continue;
					loetud.add(o.slug);
					const vana = t.alad[ala];
					if (!vana || x.m < vana.m) t.alad[ala] = { m: x.m, v0: x.v0, v1: x.v1 || 0, rehvid: [{ slug: o.slug, nimi: o.name }] };
				}
			}
			t.n = loetud.size;
			if (Object.keys(t.alad).length) testid.push(t);
		}
	}
	const uusim = (hooaeg, alad) => {
		/* esimene ala on eelistatud (talvel jää: Eesti talvel loeb see kõige rohkem), siis uusim, siis suurim test */
		const sobivad = testid.filter((x) => x.hooaeg === hooaeg && alad.some((a) => x.alad[a])).sort((a, b) => !!b.alad[alad[0]] - !!a.alad[alad[0]] || b.aasta - a.aasta || b.n - a.n);
		if (!sobivad.length) return null;
		const x = sobivad[0], ala = alad.find((a) => x.alad[a]);
		const o = x.alad[ala];
		return { pub: x.pub, aasta: x.aasta, n: x.n, ala, m: o.m, v0: o.v0, v1: o.v1, rehvid: o.rehvid.map((r) => ({ ...r, ix: rehviIndeks(r.slug).index })) };
	};
	const suvi = uusim('suvi', ['märg asfalt']);
	const talv = uusim('talv', ['jää', 'märg asfalt']);
	const aastaring = suvi ? null : uusim('aastaring', ['märg asfalt']);
	return suvi || talv || aastaring ? { suvi, talv, aastaring } : null;
}

/** Ajakirjatestide kokkuvõte llms.txt jaoks: testide arv, aastad, väljaanded (sagedamad ees). */
export function extKokkuvote() {
	const d = json('testid_ext.json');
	if (!d || !d.allikad) return { teste: 0, mudeleid: 0, min: '', max: '', pub: '' };
	const a = Object.values(d.allikad), aastad = a.map((x) => x.year).filter(Boolean);
	const c = new Map();
	for (const x of a) {
		const p = String(x.pub || '').split(/ \/ | \(/)[0].trim();
		if (p) c.set(p, (c.get(p) || 0) + 1);
	}
	const pub = [...c.entries()].sort((x, y) => y[1] - x[1]).slice(0, 8).map((x) => x[0]).join(', ');
	return { teste: a.length, mudeleid: Object.keys(d.rehvid || {}).length, min: Math.min(...aastad), max: Math.max(...aastad), pub };
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
	/* ajakirjatestid (testid_ext.json, 2022+): samuti märja pidurduse naabrid samas testis.
	   Otsingud „<rehv> vs <rehv>“ toovad kõige parema CTR-i (Search Console 10/2026). */
	const ext = json('testid_ext.json');
	if (ext && ext.rehvid) {
		for (const [slug, rows] of Object.entries(ext.rehvid)) {
			if (!tyrePage(slug)) continue;
			for (const x of rows) {
				const al = ext.allikad[x.t] || {};
				if (x.d !== 'märg asfalt' || !(al.year >= VS_EXT_MIN_AASTA)) continue;
				const k = 'x:' + x.t + '@' + x.v0;
				(by[k] = by[k] || []).push([slug, x.m]);
			}
		}
	}
	const seen = new Map();
	for (const list of Object.values(by)) {
		list.sort((a, b) => a[1] - b[1]);
		for (let i = 0; i + 1 < list.length; i++) {
			const a = list[i][0], b = list[i + 1][0];
			if (a === b) continue;
			const k = a < b ? [a, b] : [b, a];
			seen.set(k[0] + '|' + k[1], k);
		}
	}
	_pairs = [...seen.values()];
	return _pairs;
}
export const VS_EXT_MIN_AASTA = 2022;

/* ajakirjatesti pind → sama kuju mis core testis (testLabel, vs-tabel) */
const EXT_PIND = {
	'märg asfalt': { surf: 'ASPHALT', wet: true },
	'kuiv asfalt': { surf: 'ASPHALT', wet: false },
	'märg betoon': { surf: 'CONCRETE', wet: true },
	'jää': { surf: 'ICE', wet: false },
	'lumi': { surf: 'SNOW_PACKED', wet: false }
};
/** Kahe rehvi ühised ajakirjatestid: [{ src, read: [{x, y, d}] }] (vs-leht). */
export function extShared(aSlug, bSlug) {
	if (!aSlug || !bSlug || aSlug === bSlug) return [];
	const ext = json('testid_ext.json');
	if (!ext || !ext.rehvid) return [];
	const A = ext.rehvid[aSlug] || [], B = ext.rehvid[bSlug] || [];
	const testid = [...new Set(A.map((x) => x.t))].filter((t) => B.some((y) => y.t === t));
	return testid
		.map((t) => {
			const al = ext.allikad[t] || {};
			const auto = String(al.car || '').split(/\s*[(;]/)[0].trim();
			const src = { nimi: [al.pub, al.year].filter(Boolean).join(' '), aasta: al.year, moot: al.size || '', auto, tegija: al.pub || '', kajastus: al.url || '' };
			const read = A.filter((x) => x.t === t && EXT_PIND[x.d])
				.map((x) => {
					const y = B.find((z) => z.t === t && z.d === x.d && z.v0 === x.v0);
					if (!y) return null;
					const p = EXT_PIND[x.d];
					return { x: { ...p, v0: x.v0, v1: x.v1 || 0, m: x.m }, y: { ...p, v0: y.v0, v1: y.v1 || 0, m: y.m }, d: Math.round((y.m - x.m) * 100) / 100 };
				})
				.filter(Boolean);
			return { src, read };
		})
		.filter((p) => p.read.length)
		.sort((p, q) => (q.src.aasta || 0) - (p.src.aasta || 0));
}
export function vsLinksFor(slug) {
	return vsPairs().filter((p) => p[0] === slug || p[1] === slug);
}

/* ------------------------------------------------------------ margid
 * /margid/<mark>/ — ühe tootja kõik mudelid. Mark tuleb EPREL-ist eri
 * kirjapildiga ("NOKIAN", "Nokian ", "Nokian Tyres"), seetõttu võti on
 * slug ja nimeks võetakse kõige levinum kirjapilt.
 *   ≥ MARK_MIN_INDEKS mudelit -> indeksis
 *   ≥ MARK_MIN_SAIDIKAART     -> ka saidikaardis
 */
export const MARK_MIN_INDEKS = 3;
export const MARK_MIN_SAIDIKAART = 5;

export function markSlug(mark) {
	return String(mark || '')
		.normalize('NFKD')
		.replace(/[̀-ͯ]/g, '')
		.toLowerCase()
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-+|-+$/g, '');
}

let _margid = null;
/** Map markSlug → { slug, nimi, mudelid: [slug…], testitud: [tyre…] } */
export function margid() {
	if (_margid) return _margid;
	const kirjad = new Map();
	_margid = new Map();
	for (const [slug, m] of Object.entries(models())) {
		const nimi = titleCase(String(m.mark || '').trim());
		const ms = markSlug(nimi);
		if (!ms || !/[a-z]/.test(ms)) continue;
		if (!_margid.has(ms)) {
			_margid.set(ms, { slug: ms, nimi, mudelid: [], testitud: [], hinnang: [] });
			kirjad.set(ms, new Map());
		}
		_margid.get(ms).mudelid.push(slug);
		const k = kirjad.get(ms);
		k.set(nimi, (k.get(nimi) || 0) + 1);
	}
	for (const [ms, k] of kirjad) {
		_margid.get(ms).nimi = [...k.entries()].sort((a, b) => b[1] - a[1])[0][0];
	}
	/* testitud rehvid: EPREL-i mudeli kaudu või nime esimese sõna järgi */
	for (const t of core().tyres) {
		const m = t.slug ? model(t.slug) : null;
		const ms = markSlug(m ? titleCase(String(m.mark).trim()) : String(t.name).split(' ')[0]);
		if (!_margid.has(ms)) continue;
		/* testimata naastrehv ei ole margi „testitud“ rehv, aga margilehelt peab ta leitav olema
		   (muidu on leht orb: saidikaardis, aga ükski leht ei lingi) */
		if (t.gSource === 'hinnang') {
			if (t.slug) _margid.get(ms).hinnang.push(t);
			continue;
		}
		_margid.get(ms).testitud.push(t);
	}
	return _margid;
}

export const mark = (slug) => margid().get(slug) || null;

/* ------------------------------------------------------------ müügil samas testis
 * Testitud rehv, mida partnerpoed praegu ei müü (pole mõõte = pole „Kus osta“):
 * näita samas testis olnud rehve, mida saab osta, nende mõõdetud tulemusega.
 * Nii on inimesel lehelt kuhugi minna, ja võrdlus on aus (sama test, sama päev). */
export function myygil(slug) {
	if (!slug) return false;
	const m = model(slug);
	if (m && m.sizes && m.sizes.length) return true;
	const t = testedBySlug(slug);
	return !!(t && t.moodud && t.moodud.length);
}
let _extIdx = null;
function extIndeks() {
	if (_extIdx) return _extIdx;
	_extIdx = new Map();
	const d = json('testid_ext.json');
	for (const [slug, rows] of Object.entries((d && d.rehvid) || {})) {
		for (const x of rows) {
			const k = x.t + '|' + x.d + '|' + x.v0;
			if (!_extIdx.has(k)) _extIdx.set(k, []);
			_extIdx.get(k).push({ slug, m: x.m });
		}
	}
	return _extIdx;
}
/** [{ slug, name, m, oma, pind, v0, test, aasta }] — kuni `n` rehvi, lühim pidurdusmaa ees. */
export function samasTestisMyygil(slug, n = 6) {
	const t = testedBySlug(slug) || (model(slug) && model(slug).tested ? testedByKey(model(slug).tested) : null);
	const kat = (t && t.category) || (model(slug) && model(slug).kat) || '';
	const jaaEes = /WINTER_(NORDIC|STUDDED)/.test(kat); /* Põhjamaade ja naastrehvil loeb jää */
	const eelista = (x, uus) => (jaaEes ? (uus.surf === 'ICE' || uus.d === 'jää') : (uus.surf === 'ASPHALT' && uus.wet) || uus.d === 'märg asfalt');
	const out = new Map();
	const lisa = (o) => {
		if (o.slug === slug || !myygil(o.slug)) return;
		const p = tyrePage(o.slug);
		if (!p) return;
		const vana = out.get(o.slug);
		if (!vana || o.aasta > vana.aasta) out.set(o.slug, { ...o, name: p.name });
	};
	/* meie ankrutestid: märg asfalt, muidu esimene mõõtmine */
	if (t) {
		const by = new Map();
		for (const x of t.tests || []) if (!by.has(x.src) || eelista(by.get(x.src), x)) by.set(x.src, x);
		for (const [src, x] of by) {
			const s = source(src) || {};
			for (const o of core().tyres) {
				const y = (o.tests || []).find((z) => z.src === src && z.surf === x.surf && z.wet === x.wet && z.v0 === x.v0);
				if (y && o.slug) lisa({ slug: o.slug, m: y.m, oma: x.m, pind: x.surf === 'ASPHALT' ? (x.wet ? 'märg asfalt' : 'kuiv asfalt') : x.surf === 'ICE' ? 'jää' : x.surf === 'SNOW_PACKED' ? 'lumi' : 'märg betoon', v0: x.v0, test: s.nimi || src, aasta: s.aasta || 0 });
			}
		}
	}
	/* ajakirjatestid */
	const d = json('testid_ext.json');
	const oma = ((d && d.rehvid) || {})[slug] || [];
	const by = new Map();
	for (const x of oma) if (!by.has(x.t) || eelista(by.get(x.t), x)) by.set(x.t, x);
	for (const [tid, x] of by) {
		const al = (d.allikad || {})[tid] || {};
		for (const o of extIndeks().get(tid + '|' + x.d + '|' + x.v0) || [])
			lisa({ slug: o.slug, m: o.m, oma: x.m, pind: x.d, v0: x.v0, test: [al.pub, al.year].filter(Boolean).join(' '), aasta: al.year || 0 });
	}
	return [...out.values()].sort((a, b) => b.aasta - a.aasta || a.m - b.m).slice(0, n);
}

