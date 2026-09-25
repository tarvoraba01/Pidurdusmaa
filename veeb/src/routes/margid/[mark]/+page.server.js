import { error } from '@sveltejs/kit';
import { margid, mark, model, source, titleCase, KAT_NIMI, MARK_MIN_INDEKS, rehviIndeks } from '$lib/server/andmed.js';

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

	return {
		mark: { slug: m.slug, nimi: m.nimi },
		kategooriad,
		testitud,
		mudeleid: m.mudelid.length,
		mootudKokku,
		noindex: m.mudelid.length < MARK_MIN_INDEKS
	};
}
