import {
	core,
	models,
	sizeModelCount,
	SIZE_MIN_MODELS,
	rehviIndeks,
	vsPairs,
	margid,
	MARK_MIN_SAIDIKAART
} from '$lib/server/andmed.js';

export const prerender = true;

const BASE = 'https://pidurdusmaa.ee';

/* Saidikaart = lehed, mida tahame Google'is näha: tööriistad, mõõdud
   (vähemalt 10 mudelit), testitud rehvid, vs-lehed ja testid. Ülejäänud
   rehvilehed lisatakse partiidena (andmed.js SITEMAP_MUDEL_MIN_MOOTE),
   kui Search Console näitab, et eelmised on indekseeritud. */
export function GET() {
	const urls = [
		['/', '1.0'],
		['/rehvi-valimine/', '0.9'],
		['/vordle-rehve/', '0.9'],
		['/rehvid/', '0.8'],
		['/testid/', '0.8'],
		['/margid/', '0.7'],
		['/teadmine/', '0.6'],
		['/teadmine/pidurdusteekond-ja-peatumisteekond/', '0.7'],
		['/teadmine/kuidas-pidurdusmaa-arvutatakse/', '0.6'],
		['/teadmine/rehvimargis/', '0.6'],
		['/meist/', '0.5'],
		['/kontakt/', '0.4'],
		['/kasutustingimused/', '0.3'],
		['/privaatsus/', '0.3']
	];

	for (const s of core().sizes) {
		if (sizeModelCount(s.m) >= SIZE_MIN_MODELS) urls.push(['/rehvid/' + s.slug + '/', '0.7']);
	}
	/* Rehvilehed partiidena -- reegel ja partii suurus: andmed.js rehviIndeks */
	const rehvid = new Set([...Object.keys(models()), ...core().tyres.map((t) => t.slug).filter(Boolean)]);
	for (const slug of rehvid) {
		if (rehviIndeks(slug).sitemap) urls.push(['/rehvid/' + slug + '/', '0.6']);
	}
	for (const m of margid().values()) {
		if (m.mudelid.length >= MARK_MIN_SAIDIKAART) urls.push(['/margid/' + m.slug + '/', '0.6']);
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
