/* GET /api/rehv/<slug>[?moot=20555R16]
 * Ühe rehvi lisaandmed pakkujatelt: hinnad ja pilt.
 * { available, hinnad: [...], pilt: '/api/pilt/<slug>' | null } */
import { piirang, vastus, liigaPalju, vigane, MOOT_RE, SLUG_RE } from '$lib/server/integratsioonid/kaitse.js';
import { hinnadMoodus, aktiivsed, pilt } from '$lib/server/integratsioonid/koond.js';
import { model, sizeModelCount } from '$lib/server/andmed.js';
import { poeLinkMoodule } from '$lib/server/integratsioonid/pakkujad/rehvivahetus.js';

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
	/* mõõt antud → selle mõõdu hinnad. Muidu käime läbi kuni 10 mõõtu, kõige
	   levinumad ees (iga mõõdu vastus on vahemälus, nii et pakkujat ei koormata
	   iga lehe avamisega). Varem jäi otsing pärast esimest mõõtu pildi tõttu
	   pooleli ja hinnad jäid tihti tühjaks. */
	const mood = q ? [q] : m.sizes.map((z) => z.m).sort((a, b) => sizeModelCount(b) - sizeModelCount(a)).slice(0, 10);
	const hinnad = [];
	await Promise.all(
		mood.map(async (moot) => {
			try {
				const r = await hinnadMoodus(moot);
				for (const x of r.hinnad[slug + '@' + moot] || []) hinnad.push({ ...x, moot });
			} catch {
				/* pakkuja maas — teised mõõdud ja pilt võivad ikka tulla */
			}
		})
	);
	hinnad.sort((a, b) => a.hind - b.hind);
	const p = await pilt(slug).catch(() => null);
	/* täpset toodet poes pole → link partneri e-poe selle mõõdu nimekirja (levinuim mõõt) */
	const otsi = !hinnad.length && mood[0] && aktiivsed().some((x) => x.id === 'rehvivahetus')
		? { myyja: 'Rehvivahetus.ee', moot: mood[0], url: poeLinkMoodule({ moot: mood[0] }) }
		: null;
	return vastus({ available: true, hinnad, otsi, pilt: p ? '/api/pilt/' + slug : null }, { vahemalu: 300 });
}
