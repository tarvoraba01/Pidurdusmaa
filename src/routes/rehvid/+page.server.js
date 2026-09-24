import { core, models, titleCase, source, sizeModelCount, SIZE_MIN_MODELS } from '$lib/server/andmed.js';

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

	const brands = {};
	for (const [slug, m] of Object.entries(models())) {
		const b = titleCase(m.mark);
		(brands[b] = brands[b] || []).push([slug, titleCase(m.nimi)]);
	}
	const brandList = Object.keys(brands)
		.sort((a, b) => a.localeCompare(b, 'et'))
		.map((b) => [b, brands[b].sort((x, y) => x[1].localeCompare(y[1], 'et', { numeric: true }))]);

	return { sizes, tested, brandList, mudeleid: Object.keys(models()).length };
}
