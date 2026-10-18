import { error } from '@sveltejs/kit';
import { margid, mark, model, source, titleCase, KAT_NIMI, MARK_MIN_INDEKS, rehviIndeks, pretty, sizeSlug, sizeModelCount, SIZE_MIN_MODELS, extTests, tyrePage } from '$lib/server/andmed.js';
const KAT_MITMUS = {
	SUMMER_UHP: 'Suverehvid (sportlikud)',
	SUMMER_TOURING: 'Suverehvid',
	ALL_SEASON: 'Aastaringsed rehvid',
	WINTER_CENTRAL: 'Talverehvid (Kesk-Euroopa)',
	WINTER_NORDIC: 'Talverehvid (Põhjamaade)',
	WINTER_STUDDED: 'Naastrehvid'
};

export function entries() {
	return [...margid().keys()].map((m) => ({ mark: m }));
}

/* Kategooriate järjekord lehel */
const JARJEKORD = ['SUMMER_UHP', 'SUMMER_TOURING', 'ALL_SEASON', 'WINTER_CENTRAL', 'WINTER_NORDIC', 'WINTER_STUDDED'];
const KLASSID = 'ABCDE';

function vahemik(klassid) {
	const k = [...new Set(klassid.filter((x) => KLASSID.includes(x)))].sort();
	if (!k.length) return '';
	return k.length === 1 ? k[0] : k[0] + '–' + k[k.length - 1];
}

/** /margid/<mark>/ — tootja mudelid kategooria kaupa. */
export function load({ params }) {
	const m = mark(params.mark);
	if (!m) error(404, 'Marki ei leitud');

	const grupid = {};
	for (const slug of m.mudelid) {
		const x = model(slug);
		const mootud = new Set(x.sizes.map((z) => z.m));
		const rida = {
			slug,
			nimi: titleCase(x.nimi),
			n: mootud.size,
			g: vahemik(x.sizes.map((z) => z.g)),
			testitud: !!x.tested,
			/* lingime igale mudelile; väga õhukesed (≤2 mõõtu) on noindex */
			index: rehviIndeks(slug).index
		};
		(grupid[x.kat] = grupid[x.kat] || []).push(rida);
	}
	const kategooriad = Object.keys(grupid)
		.sort((a, b) => JARJEKORD.indexOf(a) - JARJEKORD.indexOf(b))
		.map((k) => ({
			kat: k,
			/* pealkiri on loendi kohal → mitmus („Suverehvid · 16“), mitte üks rehv */
			nimi: KAT_MITMUS[k] || KAT_NIMI[k] || k,
			list: grupid[k].sort((a, b) => b.testitud - a.testitud || b.n - a.n || a.nimi.localeCompare(b.nimi, 'et', { numeric: true }))
		}));

	const testitud = m.testitud.map((t) => ({
		slug: t.slug,
		name: t.name,
		category: t.category,
		/* massiivina: iga testi nime saab lehel eraldi tõlkida (koos ühendatuna ei leidnud sõnastik vastet) */
		srcs: [...new Set(t.tests.map((x) => (source(x.src) || {}).nimi || x.src))]
	}));

	/* ajakirjatestid (testid_ext.json): ilma nendeta ütles KKK „ükski mudel pole olnud testis“ ka margil,
	   mille rehve ADAC ja Vi Bilägare on testinud (audit 18.10). Testikohad: parim ja kehvim ala, et pilt
	   oleks aus (sama rehv võib olla lumel 1. ja märjal viimane). */
	const ALA = { 'jää': 'jääl', lumi: 'lumel', 'märg asfalt': 'märjal asfaldil', 'kuiv asfalt': 'kuival asfaldil', 'märg betoon': 'märjal betoonil' };
	const testiNimi = (src) => String(src.pub || '').split(/ \/ | \(/)[0].trim() + (src.year ? ' ' + src.year : '');
	const nahtud = new Map(testitud.map((x) => [x.slug, x]));
	const kohad = [];
	for (const slug of new Set([...m.mudelid, ...m.hinnang.map((h) => h.slug), ...testitud.map((x) => x.slug)].filter(Boolean))) {
		const rows = extTests(slug).filter((r) => r.src && r.src.pub);
		if (!rows.length) continue;
		const srcs = [...new Set(rows.map((r) => testiNimi(r.src)))];
		if (nahtud.has(slug)) nahtud.get(slug).srcs = [...new Set([...nahtud.get(slug).srcs, ...srcs])];
		else {
			const p = tyrePage(slug);
			if (!p || !rehviIndeks(slug).index) continue;
			const x = { slug, name: p.name, category: p.cat, srcs };
			testitud.push(x);
			nahtud.set(slug, x);
		}
		/* uusim test, kus on kohad; selles testis parim ja kehvim ala */
		const koha = rows.filter((r) => r.pos > 0 && r.n > 2 && ALA[r.d]);
		if (!koha.length) continue;
		const aasta = Math.max(...koha.map((r) => r.src.year || 0));
		const uus = koha.filter((r) => (r.src.year || 0) === aasta);
		const test = testiNimi(uus[0].src);
		const sama = uus.filter((r) => testiNimi(r.src) === test).sort((a, b) => a.pos / a.n - b.pos / b.n);
		const parim = sama[0], kehvim = sama[sama.length - 1];
		kohad.push({ slug, name: nahtud.get(slug).name, test, aasta, parim: { pos: parim.pos, n: parim.n, ala: ALA[parim.d] }, kehvim: sama.length > 1 && kehvim.pos !== parim.pos ? { pos: kehvim.pos, n: kehvim.n, ala: ALA[kehvim.d] } : null });
	}
	kohad.sort((a, b) => b.aasta - a.aasta || a.parim.pos / a.parim.n - b.parim.pos / b.parim.n);

	const mootudKokku = new Set(m.mudelid.flatMap((s) => model(s).sizes.map((z) => z.m))).size;

	/* sissejuhatus andmetest: märghaardeklasside jaotus (mudel × mõõt) ja
	   mõõdud, milles tootjal on kõige rohkem mudeleid */
	const klassiArv = {}, mootMudelid = new Map();
	let klassiKokku = 0;
	for (const slug of m.mudelid) {
		const nahtud = new Set();
		for (const z of model(slug).sizes) {
			if (KLASSID.includes(z.g)) { klassiArv[z.g] = (klassiArv[z.g] || 0) + 1; klassiKokku++; }
			if (!/^\d{5}R\d{2}C?$/.test(z.m) || nahtud.has(z.m)) continue;
			nahtud.add(z.m);
			mootMudelid.set(z.m, (mootMudelid.get(z.m) || 0) + 1);
		}
	}
	const jaotus = klassiKokku >= 10 ? KLASSID.split('').filter((g) => klassiArv[g]).map((g) => [g, Math.round((100 * klassiArv[g]) / klassiKokku)]).filter(([, p]) => p > 0) : [];
	const topMoodud = [...mootMudelid.entries()]
		.filter(([, k]) => k >= 2)
		.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
		.slice(0, 5)
		.map(([z, k]) => ({ label: pretty(z), slug: sizeModelCount(z) >= SIZE_MIN_MODELS ? sizeSlug(z) : null, k }));

	return {
		jaotus,
		topMoodud,
		mark: { slug: m.slug, nimi: m.nimi },
		kategooriad,
		hinnang: m.hinnang.filter((t) => rehviIndeks(t.slug).index).map((t) => ({ slug: t.slug, name: t.name, n: (t.moodud || []).length })).sort((a, b) => a.name.localeCompare(b.name, 'et')),
		testitud,
		kohad: kohad.slice(0, 3),
		mudeleid: m.mudelid.length,
		mootudKokku,
		noindex: m.mudelid.length < MARK_MIN_INDEKS
	};
}
