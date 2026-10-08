import { error } from '@sveltejs/kit';
import { arvuta, klassiVahe } from '$lib/server/jaga.js';
import {
	core,
	eprelSize,
	sizeBySlug,
	sizeModelCount,
	SIZE_MIN_MODELS,
	source,
	tyrePage,
	sharedSources,
	rankInTest,
	vsPairs,
	vsLinksFor,
	models,
	titleCase,
	pretty,
	sizeSlug,
	rehviIndeks,
	mark,
	markSlug,
	extTests
} from '$lib/server/andmed.js';
import { autodMoodus } from '$lib/server/autod.js';
import { talveMoot } from '$lib/server/talv.js';

/* Kolm lehte ühe aadressimustri all — täpselt nagu PHP-s pm_ctx():
   /rehvid/205-55-r16/          → mõõdu leht
   /rehvid/michelin-…/          → rehvi leht
   /rehvid/<a>-vs-<b>/          → kahe rehvi võrdlus samas testis
   Järjekord loeb: mõne rehvi nimes ENDAS on „vs" (maxxis-vs-ev). */

export function entries() {
	const out = [];
	for (const s of core().sizes) {
		if (sizeModelCount(s.m) >= SIZE_MIN_MODELS) out.push({ slug: s.slug });
	}
	for (const slug of Object.keys(models())) out.push({ slug });
	for (const t of core().tyres) if (t.slug && !models()[t.slug]) out.push({ slug: t.slug });
	for (const [a, b] of vsPairs()) out.push({ slug: a + '-vs-' + b });
	return out;
}

export function load({ params }) {
	const slug = params.slug;

	/* 1) mõõt */
	const size = sizeBySlug(slug);
	if (size) return mootLeht(size);

	/* 2) rehv (ka siis, kui nimes on „vs") */
	const t = tyrePage(slug);
	if (t) return rehvLeht(t);

	/* 3) võrdlus */
	const m = /^(.+)-vs-(.+)$/.exec(slug);
	if (m) {
		const a = tyrePage(m[1]);
		const b = tyrePage(m[2]);
		const shared = a && b ? sharedSources(a, b) : [];
		/* Ainult sama testi rehvid saavad oma „vs" lehe — muidu oleks see
		   kahe märgise kõrvutus, mida võrdlustööriist teeb paremini. */
		if (shared.length) return vsLeht(a, b, shared);
	}
	error(404, 'Lehte ei leitud');
}

/* ------------------------------------------------------------ mõõdu leht */
function mootLeht(size) {
	const rows = eprelSize(size.m);
	const by = {};
	for (const r of rows) (by[r[3]] = by[r[3]] || []).push(r);
	const grupid = Object.keys(by)
		.sort()
		.map((ci) => ({
			ci: +ci,
			list: by[ci]
				.map((r) => ({
					slug: r[0],
					nimi: titleCase(r[1] + ' ' + r[2]),
					g: r[4],
					f: r[5],
					db: r[6],
					tested: !!r[9]
				}))
				.sort((a, b) => (a.g < b.g ? -1 : a.g > b.g ? 1 : (a.db ?? 99) - (b.db ?? 99)))
		}));

	const klassid = {};
	for (const r of rows) klassid[r[4]] = (klassid[r[4]] || 0) + 1;

	/* autod, millel see on tehasemõõt → lingid autolehtedele */
	const koikAutod = autodMoodus(size.m);
	const cars = koikAutod.slice(0, 24);

	/* KKK ja sissejuhatus: ainult andmetest (märgis, testid, autod) */
	const kl = Object.keys(klassid).filter((g) => 'ABCDE'.includes(g)).sort();
	const parimG = kl[0] || null;
	const parimRead = parimG
		? rows
				.filter((r) => r[4] === parimG)
				.filter((r, i, a) => a.findIndex((x) => x[0] === r[0]) === i)
				.sort((a, b) => (b[9] ? 1 : 0) - (a[9] ? 1 : 0) || (a[6] ?? 99) - (b[6] ?? 99))
		: [];
	const parimad = parimRead.slice(0, 3).map((r) => titleCase(r[1] + ' ' + r[2]));
	/* ItemList (AI-otsing): parima märghaardeklassi rehvid, testitud ees */
	const parimadLd = parimRead.slice(0, 10).map((r) => ({ slug: r[0], nimi: titleCase(r[1] + ' ' + r[2]) }));
	/* klassivahe arvutatakse auto peal, millel see mõõt päriselt on; kui ühtki pole, jääb see küsimus ära */
	const pohiAuto = koikAutod.find((c) => c.pohi) || koikAutod[0];
	return {
		liik: 'moot',
		size,
		parimG,
		parimN: parimG ? klassid[parimG] : 0,
		parimad,
		parimadLd,
		nTest: rows.filter((r) => r[9]).length,
		vahe: ((v) => (v && pohiAuto && v.autoKey === pohiAuto.key ? { ...v, auto: pohiAuto.nimi } : null))(pohiAuto ? klassiVahe(size.m, pohiAuto.key) : null),
		sarnased: sarnasedMoodud(size),
		grupid,
		klassid: Object.keys(klassid).sort().map((g) => [g, klassid[g]]),
		cars,
		autosid: koikAutod.length,
		n: rows.length,
		noindex: rows.length < SIZE_MIN_MODELS,
		talv: talveMoot(size.slug) ? size.slug : null
	};
}


/* Sama välisläbimõõduga mõõdud (±1,5 %), millel on oma leht. C (kaubiku)
   mõõdud ainult C-mõõtudega ja vastupidi. */
const labimoot = (m) => {
	const x = /^(\d{3})(\d{2})R(\d{2})(C?)$/.exec(m);
	return x ? { d: +x[3] * 25.4 + (2 * +x[1] * +x[2]) / 100, c: !!x[4] } : null;
};
function sarnasedMoodud(size) {
	const a = labimoot(size.m);
	if (!a) return [];
	const out = [];
	for (const s of core().sizes) {
		if (s.m === size.m) continue;
		const b = labimoot(s.m);
		if (!b || b.c !== a.c) continue;
		const v = (b.d / a.d - 1) * 100;
		if (Math.abs(v) <= 1.5 && sizeModelCount(s.m) >= SIZE_MIN_MODELS) out.push({ label: s.label, slug: s.slug, v: Math.round(v * 10) / 10 });
	}
	return out.sort((p, q) => Math.abs(p.v) - Math.abs(q.v)).slice(0, 8);
}

/* Kirjeldus otsingutulemuse jaoks: konkreetsed numbrid, mitte mall.
   „Kleber Dynaxer HP3 suverehv: märjal haardumise klass B, müra 69 dB,
   17 mõõtu. Vaata, kui pikk on pidurdusmaa sinu autoga." */
const KAT_FRAAS = {
	SUMMER_UHP: 'sportlik suverehv',
	SUMMER_TOURING: 'suverehv',
	ALL_SEASON: 'aastaringne rehv',
	WINTER_CENTRAL: 'Kesk-Euroopa talverehv',
	WINTER_NORDIC: 'Põhjamaade lamell-talverehv',
	WINTER_STUDDED: 'naastrehv'
};
function vahemik(arr, jarj) {
	const u = [...new Set(arr.filter((x) => x !== null && x !== undefined && x !== ''))];
	if (!u.length) return '';
	u.sort(jarj);
	return u.length === 1 ? String(u[0]) : u[0] + '–' + u[u.length - 1];
}
function kirjeldus(t, sizes, tests) {
	const osad = [];
	if (tests.length) osad.push('sõltumatu testi pidurdusmaad');
	const g = vahemik(sizes.map((z) => z.g), (a, b) => String(a).localeCompare(String(b)));
	if (g) osad.push('märjal haardumise klass ' + g);
	const db = vahemik(sizes.map((z) => z.db), (a, b) => a - b);
	if (db) osad.push('müra ' + db + ' dB');
	const n = new Set(sizes.map((z) => z.m)).size;
	if (n) osad.push(n + (n === 1 ? ' mõõt' : ' mõõtu'));
	const fraas = KAT_FRAAS[t.cat] ? ' ' + KAT_FRAAS[t.cat] : '';
	return t.name + fraas + (osad.length ? ': ' + osad.join(', ') : '') + '. Vaata, kui pikk on pidurdusmaa sinu autoga.';
}

/* ------------------------------------------------------------- rehvileht */
function rehvLeht(t) {
	const ix = rehviIndeks(t.slug);
	const sizes = (t.model ? t.model.sizes : [])
		.slice()
		.sort((a, b) => String(a.m).localeCompare(String(b.m), 'et', { numeric: true }))
		.map((z) => ({ ...z, slug: sizeSlug(z.m), label: pretty(z.m) }));

	const tests = t.tested
		? t.tested.tests.map((x) => {
				const [pos, n, best] = rankInTest(x);
				return { ...x, src_nimi: (source(x.src) || {}).nimi || x.src, src_slug: x.src.toLowerCase(), pos, n, best };
			})
		: [];

	const ext = extTests(t.slug);

	const aqua = t.tested && t.tested.aqua
		? { ...t.tested.aqua, nimi: (source(t.tested.aqua.src) || {}).nimi || '' }
		: null;

	const vastus = vastusLause(t, sizes);
	/* talve- ja aastaringsel rehvil teine tsiteeritav fakt: jääl (või lumel) 50 km/h pealt,
	   AINULT siis, kui rehv on sellel pinnal päriselt testitud (märgis jää kohta ei ütle midagi) */
	const vastusTalv = vastus && /^(WINTER_|ALL_SEASON)/.test(t.cat) ? vastusTalvLause(t, sizes, vastus) : null;

	const vs = vsLinksFor(t.slug)
		.map((p) => {
			const other = tyrePage(p[0] === t.slug ? p[1] : p[0]);
			return other ? { url: '/rehvid/' + p[0] + '-vs-' + p[1] + '/', name: other.name } : null;
		})
		.filter(Boolean);

	return {
		liik: 'rehv',
		tyre: {
			slug: t.slug,
			name: t.name,
			brand: t.brand,
			brandSlug: mark(markSlug(t.brand)) ? markSlug(t.brand) : null,
			cat: t.cat,
			testedKey: t.tested ? t.tested.key : '',
			testSize: t.tested ? t.tested.size : '',
			oletus: !!(t.model && String(t.model.katAlus || '').startsWith('OLETUS')),
			/* mudel on poe kataloogist (EPREL-i korjes puudub): märgis müüja andmetel */
			pood: t.model && t.model.allikas === 'pood' ? String(t.model.pood || 'pood') : null
		},
		sizes,
		/* ühe mõõdu kohta võib olla mitu rida (koormusindeks, tootjavariant AO/MO/XL) */
		mootudeArv: new Set(sizes.map((z) => z.m)).size,
		mootudUnik: sizes.filter((z, i) => sizes.findIndex((y) => y.m === z.m) === i),
		/* autod, mille PÕHImõõt on selle rehvi mõõtude hulgas */
		sobib: (() => {
			const nahtud = new Set(), out = [];
			for (const z of sizes) for (const c of autodMoodus(z.m)) if (c.pohi && !nahtud.has(c.url)) { nahtud.add(c.url); out.push({ ...c, moot: z.label }); }
			out.sort((a, b) => b.aasta - a.aasta || a.nimi.localeCompare(b.nimi, 'et'));
			return { n: out.length, list: out.slice(0, 12) };
		})(),
		tests,
		ext,
		aqua,
		vs,
		/* Indekseerimise reegel on andmed.js-is (rehviIndeks) */
		noindex: !(tests.length || ext.length || sizes.length) || !ix.index,
		canonical: ix.canonical ? 'rehvid/' + ix.canonical + '/' : null,
		desc: kirjeldus(t, sizes, tests),
		/* sama kirjeldus tükkidena — vene lehel pannakse see kokku tõlgitult */
		descOsad: {
			fraas: KAT_FRAAS[t.cat] || '',
			testid: !!tests.length,
			g: vahemik(sizes.map((z) => z.g), (a, b) => String(a).localeCompare(String(b))),
			db: vahemik(sizes.map((z) => z.db), (a, b) => a - b),
			n: new Set(sizes.map((z) => z.m)).size
		},
		ogPilt: ix.sitemap,
		vastus,
		vastusTalv,
		/* KKK: testide kokkuvõte (parim koht) ainult lehe andmetest */
		parimTest: parimTestKoht(tests)
	};
}

/* Talverehvi fakt: „jääl 50 km/h pealt umbes X m“ (sama auto ja mõõt mis märja lausel).
   Kui jäätesti pole, proovime lund. Mõlema puudumisel lauset ei tule. */
function vastusTalvLause(t, sizes, v) {
	const moot = sizes.find((z) => z.label === v.moot);
	const auto = moot ? (autodMoodus(moot.m).find((c) => c.nimi === v.auto) || autodMoodus(moot.m)[0]) : null;
	if (!moot || !auto || !auto.key) return null;
	for (const o of ['ice', 'snow']) {
		const x = arvuta({ a: auto.key, ab: false, m: moot.m, o, v: 50, r: 'e:' + t.slug, mm: null, rt: 0, l: 'et' });
		if (x && !x.autoVaikimisi && x.alla === 'Sõltumatu test' && x.d > 3 && x.d < 200) return { pind: o, d: Math.round(x.d * 10) / 10 };
	}
	return null;
}

/* Parim koht sõltumatutes testides: { src, pos, n, pind } (1 = lühim pidurdusmaa) */
function parimTestKoht(tests) {
	const k = tests.filter((x) => x.pos && x.n > 1).sort((a, b) => a.pos / a.n - b.pos / b.n || a.pos - b.pos)[0];
	return k ? { src: k.src_nimi, pos: k.pos, n: k.n, surf: k.surf, wet: k.wet, v0: k.v0, m: k.m } : null;
}

/* GEO: üks tsiteeritav fakt rehvilehe päisesse.
   „<Rehv> <mõõt>: pidurdusmaa märjal 90 km/h pealt umbes X m (<auto> …)“
   Mõõt = kõige levinum tehase põhimõõt, auto = uusim selle mõõduga auto. Arvutus on
   SAMA mis kalkulaatoris ja jagamislehel (jaga.js arvuta): testitud rehvil
   testi järgi, muidu EL-i märgise klassi järgi. */
function vastusLause(t, sizes) {
	if (!sizes.length) return null;
	/* mõõt, mis on kõige rohkemate autode tehase PÕHImõõt; auto = uusim neist.
	   Kui ühelgi autol pole ükski mõõt põhimõõt, võta lisamõõduga auto.
	   Ilma päris autota lauset ei tehta — ebarealistlik kombinatsioon
	   (nt 275/35 R21 Golfil) annaks eksitava numbri. */
	let parim = null, auto = null, parimN = -1;
	for (const z of sizes) {
		const autod = autodMoodus(z.m);
		const pohi = autod.filter((c) => c.pohi);
		const n = pohi.length * 1000 + autod.length;
		if (autod.length && n > parimN) { parim = z; auto = (pohi[0] || autod[0]); parimN = n; }
	}
	if (!parim || !auto || !auto.key) return null;
	const x = arvuta({ a: auto.key, ab: false, m: parim.m, o: 'wet', v: 90, r: 'e:' + t.slug, mm: null, rt: 0, l: 'et' });
	if (!x || x.autoVaikimisi || !(x.d > 10 && x.d < 150)) return null;
	return {
		moot: parim.label,
		d: Math.round(x.d),
		auto: auto.nimi,
		/* mida arvutus päriselt kasutas: testi mõõtmist või märgise klassi */
		test: x.alla === 'Sõltumatu test',
		g: parim.g || null
	};
}

/* ------------------------------------------------------------- vs-leht */
function vsLeht(a, b, shared) {
	const plokid = shared.map((code) => {
		const src = source(code) || {};
		const read = a.tested.tests
			.filter((x) => x.src === code)
			.map((x) => {
				const y = b.tested.tests.find(
					(z) => z.src === code && z.surf === x.surf && z.wet === x.wet && z.v0 === x.v0
				);
				return y ? { x, y, d: y.m - x.m } : null;
			})
			.filter(Boolean);
		return { src, read };
	});
	/* kokkuvõte (vastus + KKK): mitmel pinnal kumb oli lühem; pealkirjaks märg asfalt, muidu esimene rida */
	const read = plokid.flatMap((p) => p.read.map((r) => ({ ...r, src: p.src })));
	const pea = read.find((r) => r.x.surf === 'ASPHALT' && r.x.wet) || read.find((r) => r.x.surf === 'ASPHALT') || read[0] || null;
	const kokku = read.length
		? {
				a: read.filter((r) => r.d > 0).length,
				b: read.filter((r) => r.d < 0).length,
				n: read.length,
				pea: pea ? { surf: pea.x.surf, wet: !!pea.x.wet, v0: pea.x.v0, am: pea.x.m, bm: pea.y.m, d: Math.round(Math.abs(pea.d) * 10) / 10, src: pea.src.nimi || '', aasta: pea.src.aasta || '' } : null
			}
		: null;
	return {
		liik: 'vs',
		a: { slug: a.slug, name: a.name },
		b: { slug: b.slug, name: b.name },
		plokid,
		kokku
	};
}
