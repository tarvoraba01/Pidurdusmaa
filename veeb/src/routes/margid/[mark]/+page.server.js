import { error } from '@sveltejs/kit';
import { margid, mark, model, source, titleCase, KAT_NIMI, MARK_MIN_INDEKS, rehviIndeks, pretty, sizeSlug, sizeModelCount, SIZE_MIN_MODELS } from '$lib/server/andmed.js';

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
			nimi: KAT_NIMI[k] || k,
			list: grupid[k].sort((a, b) => b.testitud - a.testitud || b.n - a.n || a.nimi.localeCompare(b.nimi, 'et', { numeric: true }))
		}));

	const testitud = m.testitud.map((t) => ({
		slug: t.slug,
		name: t.name,
		category: t.category,
		srcs: [...new Set(t.tests.map((x) => (source(x.src) || {}).nimi || x.src))].join(', ')
	}));

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
		testitud,
		mudeleid: m.mudelid.length,
		mootudKokku,
		noindex: m.mudelid.length < MARK_MIN_INDEKS
	};
}
