/* GET /api/rehv/<slug>[?moot=20555R16]
 * Ühe rehvi lisaandmed pakkujatelt: hinnad ja pilt.
 * { available, hinnad: [...], pilt: '/api/pilt/<slug>' | null } */
import { piirang, vastus, liigaPalju, vigane, MOOT_RE, SLUG_RE } from '$lib/server/integratsioonid/kaitse.js';
import { hinnadMoodus, aktiivsed, pilt } from '$lib/server/integratsioonid/koond.js';
import { model } from '$lib/server/andmed.js';

export const prerender = false;
/* API aadressid töötavad nii kaldkriipsuga kui ilma (lehtedel on alati kaldkriips) */
export const trailingSlash = 'ignore';

export async function GET(event) {
	if (!piirang('rehv', event, 60, 60)) return liigaPalju();
	const slug = event.params.slug;
	if (!SLUG_RE.test(slug)) return vigane('Vigane rehv');
	const m = model(slug);
	if (!m) return vastus({ ok: false, viga: 'Rehvi ei ole' }, { status: 404 });
	if (!aktiivsed().length) return vastus({ available: false, hinnad: [], pilt: null }, { vahemalu: 300 });

	const q = event.url.searchParams.get('moot');
	if (q && !MOOT_RE.test(q)) return vigane('Vigane mõõt');
	/* mõõt antud → selle mõõdu hinnad. Muidu käime läbi kuni 8 mõõtu, kuni
	   mõni pakkuja on rehvi pildi andnud (iga mõõdu vastus on vahemälus, nii et
	   pakkujat ei koormata iga lehe avamisega). */
	const mood = q ? [q] : m.sizes.slice(0, 8).map((z) => z.m);
	const hinnad = [];
	for (const moot of mood) {
		try {
			const r = await hinnadMoodus(moot);
			for (const x of r.hinnad[slug + '@' + moot] || []) hinnad.push({ ...x, moot });
		} catch {
			/* pakkuja maas — proovi järgmist mõõtu, pilt võib ikka tulla */
		}
		if (!q && (await pilt(slug).catch(() => null))) break;
	}
	hinnad.sort((a, b) => a.hind - b.hind);
	const p = await pilt(slug).catch(() => null);
	return vastus({ available: true, hinnad, pilt: p ? '/api/pilt/' + slug : null }, { vahemalu: 300 });
}
