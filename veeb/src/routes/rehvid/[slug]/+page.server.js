import { error } from '@sveltejs/kit';
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
	markSlug
} from '$lib/server/andmed.js';

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

	const cars = core()
		.vehicles.filter((v) => String(v.oemSize || '').toUpperCase().replace(/[/ ]/g, '') === size.m)
		.slice(0, 12)
		.map((v) => v.name);

	return {
		liik: 'moot',
		size,
		grupid,
		klassid: Object.keys(klassid).sort().map((g) => [g, klassid[g]]),
		cars,
		n: rows.length,
		noindex: rows.length < SIZE_MIN_MODELS
	};
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

	const aqua = t.tested && t.tested.aqua
		? { ...t.tested.aqua, nimi: (source(t.tested.aqua.src) || {}).nimi || '' }
		: null;

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
			oletus: !!(t.model && String(t.model.katAlus || '').startsWith('OLETUS'))
		},
		sizes,
		/* ühe mõõdu kohta võib olla mitu rida (koormusindeks, tootjavariant AO/MO/XL) */
		mootudeArv: new Set(sizes.map((z) => z.m)).size,
		mootudUnik: sizes.filter((z, i) => sizes.findIndex((y) => y.m === z.m) === i),
		tests,
		aqua,
		vs,
		/* Indekseerimise reegel on andmed.js-is (rehviIndeks) */
		noindex: !(tests.length || sizes.length) || !ix.index,
		canonical: ix.canonical ? 'rehvid/' + ix.canonical + '/' : null,
		desc: kirjeldus(t, sizes, tests),
		ogPilt: ix.sitemap
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
	return {
		liik: 'vs',
		a: { slug: a.slug, name: a.name },
		b: { slug: b.slug, name: b.name },
		plokid
	};
}
