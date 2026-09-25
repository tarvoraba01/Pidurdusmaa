import { core, models, source, sizeModelCount, SIZE_MIN_MODELS, margid } from '$lib/server/andmed.js';

/** /rehvid/ — mõõdud, testitud rehvid, margid. */
export function load() {
	const c = core();
	const sizes = c.sizes
		.filter((s) => sizeModelCount(s.m) >= SIZE_MIN_MODELS)
		.map((s) => ({ ...s, n: sizeModelCount(s.m) }))
		.sort((a, b) => a.label.localeCompare(b.label, 'et', { numeric: true }));

	const tested = c.tyres
		.map((t) => ({
			slug: t.slug,
			name: t.name,
			category: t.category,
			srcs: [...new Set(t.tests.map((x) => (source(x.src) || {}).nimi || x.src))].join(', ')
		}))
		.sort((a, b) => a.category.localeCompare(b.category) || a.name.localeCompare(b.name, 'et'));

	/* Margid lingina margi lehele — mitte kõik 3500 mudelit siin (leht oli 440 kB) */
	const list = [...margid().values()]
		.map((m) => ({ slug: m.slug, nimi: m.nimi, n: m.mudelid.length }))
		.sort((a, b) => a.nimi.localeCompare(b.nimi, 'et'));

	return { sizes, tested, margid: list, mudeleid: Object.keys(models()).length };
}
