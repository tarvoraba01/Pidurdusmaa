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
import { ARTIKLID, artikliTee } from '$lib/artiklid.js';
import { autod } from '$lib/server/autod.js';
import { talveMoodud } from '$lib/server/talv.js';
import { TOLGITUD } from '$lib/i18n.js';
import RU_REHVID from '$lib/i18n/ru_rehvid.js';

export const prerender = true;

const BASE = 'https://pidurdusmaa.ee';
/* ehituse kuupäev: Google kasutab lastmod-i, et otsustada, mida uuesti lugeda */
const LASTMOD = new Date().toISOString().slice(0, 10);

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
		['/teadmine/artiklid/', '0.7'],
		...ARTIKLID.map((a) => [artikliTee(a), '0.8']),
		['/teadmine/rehvivahetus/', '0.8'],
		['/teadmine/pidurdusteekond-ja-peatumisteekond/', '0.7'],
		['/teadmine/kuidas-pidurdusmaa-arvutatakse/', '0.6'],
		['/teadmine/rehvimargis/', '0.6'],
		['/teadmine/partnerid/', '0.3'],
		['/meist/', '0.5'],
		['/liiklusohutus/', '0.8'],
		['/liiklusohutus/pimedas/', '0.7'],
		['/liiklusohutus/pikivahe/', '0.7'],
		['/liiklusohutus/kurv/', '0.7'],
		['/liiklusohutus/reaktsioon/', '0.7'],
		['/rehvi-vanus/', '0.8'],
		['/rehvi-kalkulaator/', '0.8'],
		['/kontakt/', '0.4'],
		['/kasutustingimused/', '0.3'],
		['/privaatsus/', '0.3']
	];
	/* vene ja inglise versioonid (tööriistalehed, vt $lib/i18n.js) */
	for (const k of ['ru', 'en']) for (const p of TOLGITUD) urls.push(['/' + k + p, p === '/' ? '0.8' : '0.6']);

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
	/* autod: indeks, margid, põlvkonnad */
	urls.push(['/autod/', '0.7']);
	for (const m of autod().margid.values()) urls.push(['/autod/' + m.slug + '/', '0.6']);
	for (const p of autod().polved.values()) urls.push(['/autod/' + p.mk + '/' + p.slug + '/', '0.6']);
	/* „Parimad talverehvid <mõõt>“ (eesti ja vene keeles) */
	for (const k of ['', '/ru']) {
		urls.push([k + '/talverehvid/', '0.8']);
		for (const x of talveMoodud()) urls.push([k + '/talverehvid/' + x.slug + '/', '0.8']);
	}
	/* vene keeles: artiklid, rehvilehed (nimekiri: scripts/ru-rehvid.mjs) */
	urls.push(['/ru/teadmine/artiklid/', '0.5'], ['/ru/teadmine/pidurdusteekond-ja-peatumisteekond/', '0.6'], ['/ru/teadmine/rehvivahetus/', '0.7'], ['/ru/rehvid/', '0.6']);
	for (const a of ARTIKLID) if (a.ru) urls.push(['/ru' + artikliTee(a), '0.6']);
	for (const slug of RU_REHVID) urls.push(['/ru/rehvid/' + slug + '/', '0.5']);
	/* autolehed vene keeles (/ru/autod/…) */
	urls.push(['/ru/autod/', '0.5']);
	for (const m of autod().margid.values()) urls.push(['/ru/autod/' + m.slug + '/', '0.5']);
	for (const p of autod().polved.values()) urls.push(['/ru/autod/' + p.mk + '/' + p.slug + '/', '0.5']);

	const xml =
		'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
		urls
			.map(([u, p]) => `<url><loc>${BASE}${u}</loc><lastmod>${LASTMOD}</lastmod><priority>${p}</priority></url>`)
			.join('\n') +
		'\n</urlset>\n';

	return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
