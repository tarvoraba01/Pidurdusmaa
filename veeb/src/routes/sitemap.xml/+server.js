import {
	core,
	models,
	sizeModelCount,
	SIZE_MIN_MODELS,
	tyrePage,
	vsPairs
} from '$lib/server/andmed.js';

export const prerender = true;

const BASE = 'https://pidurdusmaa.ee';

/* Sitemap sisaldab ainult indekseeritavaid lehti: mõõdud, kus on
   vähemalt 10 mudelit, ja rehvilehed, kus on kas märgise andmed või
   mõõdetud test. Tühja lehte Google'ile ei paku. */
export function GET() {
	const urls = [
		['/', '1.0'],
		['/rehvi-valimine/', '0.9'],
		['/vordle-rehve/', '0.9'],
		['/rehvid/', '0.8'],
		['/testid/', '0.8'],
		['/teadmine/', '0.6'],
		['/teadmine/kuidas-pidurdusmaa-arvutatakse/', '0.6'],
		['/teadmine/rehvimargis/', '0.6'],
		['/kontakt/', '0.4'],
		['/kasutustingimused/', '0.3'],
		['/privaatsus/', '0.3']
	];

	for (const s of core().sizes) {
		if (sizeModelCount(s.m) >= SIZE_MIN_MODELS) urls.push(['/rehvid/' + s.slug + '/', '0.7']);
	}
	for (const slug of Object.keys(models())) {
		const t = tyrePage(slug);
		if (t && ((t.model && t.model.sizes.length) || t.tested)) urls.push(['/rehvid/' + slug + '/', '0.6']);
	}
	for (const t of core().tyres) {
		if (t.slug && !models()[t.slug]) urls.push(['/rehvid/' + t.slug + '/', '0.6']);
	}
	for (const [a, b] of vsPairs()) urls.push(['/rehvid/' + a + '-vs-' + b + '/', '0.5']);
	for (const code of Object.keys(core().sources)) urls.push(['/testid/' + code.toLowerCase() + '/', '0.5']);

	const xml =
		'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
		urls
			.map(([u, p]) => `<url><loc>${BASE}${u}</loc><priority>${p}</priority></url>`)
			.join('\n') +
		'\n</urlset>\n';

	return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
