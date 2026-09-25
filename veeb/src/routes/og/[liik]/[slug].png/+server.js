/* Jagamispildid (og:image), tehakse ehituse ajal valmis:
 *   /og/sait/avaleht.png        üldine pilt (avaleht ja muud lehed)
 *   /og/m/205-55-r16.png        mõõdu leht
 *   /og/r/<rehv>.png            testitud rehvi leht
 *   /og/vs/<a>-vs-<b>.png       kahe rehvi võrdlus samas testis
 * Pilte tehakse ainult saidikaardis olevatele lehtedele — ülejäänud
 * kasutavad üldist pilti.
 */
import { error } from '@sveltejs/kit';
import { ogPilt } from '$lib/server/ogpilt.js';
import {
	core,
	models,
	sizeBySlug,
	sizeModelCount,
	SIZE_MIN_MODELS,
	eprelSize,
	tyrePage,
	rehviIndeks,
	vsPairs,
	sharedSources,
	source,
	num,
	KAT_NIMI
} from '$lib/server/andmed.js';

export const prerender = true;

export function entries() {
	const out = [{ liik: 'sait', slug: 'avaleht' }];
	for (const s of core().sizes) if (sizeModelCount(s.m) >= SIZE_MIN_MODELS) out.push({ liik: 'm', slug: s.slug });
	const rehvid = new Set([...Object.keys(models()), ...core().tyres.map((t) => t.slug).filter(Boolean)]);
	for (const slug of rehvid) if (rehviIndeks(slug).sitemap) out.push({ liik: 'r', slug });
	for (const [a, b] of vsPairs()) out.push({ liik: 'vs', slug: a + '-vs-' + b });
	return out;
}

function lyhenda(s, n) {
	s = String(s);
	return s.length <= n ? s : s.slice(0, n - 1).trimEnd() + '…';
}
function vahemik(arr) {
	const u = [...new Set(arr.filter((x) => x !== null && x !== undefined && x !== ''))].sort((a, b) =>
		typeof a === 'number' ? a - b : String(a).localeCompare(String(b))
	);
	return !u.length ? '' : u.length === 1 ? String(u[0]) : u[0] + '–' + u[u.length - 1];
}
/* esimene mõõdetud märja asfaldi tulemus, muidu esimene üldse */
function mootmine(tested) {
	const x = tested.tests.find((t) => t.surf === 'ASPHALT' && t.wet) || tested.tests[0];
	if (!x) return '';
	const pind = x.surf === 'ASPHALT' ? (x.wet ? 'Märg' : 'Kuiv') : x.surf === 'CONCRETE' ? 'Märg betoon' : x.surf === 'ICE' ? 'Jää' : 'Lumi';
	const src = source(x.src) || {};
	const kes = src.tegija ? String(src.tegija).split(' (')[0] + ' ' + (src.aasta || '') : '';
	/* noolt → fondis ei ole — kirjutame sõnadega */
	const kiirus = x.v1 ? `${x.v0}–${x.v1} km/h` : `${x.v0} km/h pealt`;
	return `${pind}: ${kiirus} ${num(x.m)} m` + (kes ? ' · ' + kes.trim() : '');
}

function andmed(liik, slug) {
	if (liik === 'sait' && slug === 'avaleht') {
		return {
			kicker: 'Pidurdusmaa kalkulaator',
			pealkiri: 'Kui kiiresti sinu auto peatub?',
			alapealkiri: 'Päris rehviandmed: EL-i märgis ja sõltumatud testid',
			sildid: [
				num(Object.keys(models()).length, 0) + ' rehvimudelit',
				num(core().vehicles.length, 0) + ' autot',
				'Tasuta'
			]
		};
	}
	if (liik === 'm') {
		const s = sizeBySlug(slug);
		if (!s) return null;
		const rows = eprelSize(s.m);
		const a = rows.filter((r) => r[4] === 'A').length;
		return {
			kicker: 'Rehvimõõt',
			pealkiri: 'Rehvid ' + s.label,
			alapealkiri: rows.length + ' rehvimudelit EL-i märgise andmetega',
			sildid: [a ? a + ' A-klassi märjal' : '', 'Võrdle pidurdusmaad']
		};
	}
	if (liik === 'r') {
		const t = tyrePage(slug);
		if (!t || !rehviIndeks(slug).sitemap) return null;
		const sizes = t.model ? t.model.sizes : [];
		const g = vahemik(sizes.map((z) => z.g));
		const db = vahemik(sizes.map((z) => z.db));
		return {
			kicker: (KAT_NIMI[t.cat] || 'Rehv') + (t.tested ? ' · sõltumatult testitud' : ''),
			pealkiri: t.name,
			alapealkiri: lyhenda(t.tested ? mootmine(t.tested) : '', 54),
			sildid: [g ? 'Märghaare ' + g : '', db ? 'Müra ' + db + ' dB' : '', sizes.length ? sizes.length + ' mõõtu' : '']
		};
	}
	if (liik === 'vs') {
		const m = /^(.+)-vs-(.+)$/.exec(slug);
		if (!m) return null;
		const a = tyrePage(m[1]);
		const b = tyrePage(m[2]);
		const shared = a && b ? sharedSources(a, b) : [];
		if (!shared.length) return null;
		const src = source(shared[0]) || {};
		return {
			kicker: 'Mõõdetud samas testis',
			pealkiri: a.name + ' vs ' + b.name,
			alapealkiri: lyhenda(src.nimi || '', 54),
			sildid: ['Sama auto, sama päev']
		};
	}
	return null;
}

export function GET({ params }) {
	const d = andmed(params.liik, params.slug);
	if (!d) error(404, 'Pilti ei ole');
	return new Response(ogPilt(d), {
		headers: { 'Content-Type': 'image/png', 'Cache-Control': 'public, max-age=86400' }
	});
}
