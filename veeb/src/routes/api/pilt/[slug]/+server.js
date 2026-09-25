/* GET /api/pilt/<slug> — rehvi pilt pakkujalt, meie serveri kaudu.
 *
 * Miks mitte otse pakkuja URL: pildi aadressis võib olla võti, pakkuja
 * võib keelata otselingid ja nii ei jälgi pakkuja meie külastajaid.
 * Server laeb pildi ainult pakkuja lubatud aadressilt, kontrollib, et see
 * on päriselt pilt (jpeg/png/webp/avif, kuni 3 MB), hoiab mälus ja annab
 * edasi pika vahemäluga. */
import { piirang, liigaPalju, PAISED, SLUG_RE } from '$lib/server/integratsioonid/kaitse.js';
import { pilt, pakkujaId } from '$lib/server/integratsioonid/koond.js';
import { paring } from '$lib/server/integratsioonid/http.js';

export const prerender = false;
/* API aadressid töötavad nii kaldkriipsuga kui ilma (lehtedel on alati kaldkriips) */
export const trailingSlash = 'ignore';

const TYYBID = ['image/jpeg', 'image/png', 'image/webp', 'image/avif'];
const MAX_MALUS = 300;
const malu = new Map(); // slug -> { tyyp, andmed, aeg }
const PAEV = 86400 * 1000;

const puudub = () => new Response('Pilti ei ole', { status: 404, headers: { ...PAISED, 'Cache-Control': 'public, max-age=3600' } });

export async function GET(event) {
	if (!piirang('pilt', event, 120, 60)) return liigaPalju();
	const slug = event.params.slug;
	if (!SLUG_RE.test(slug)) return puudub();

	let k = malu.get(slug);
	if (!k || Date.now() - k.aeg > 7 * PAEV) {
		const allikas = await pilt(slug).catch(() => null);
		const p = allikas && pakkujaId(allikas.pakkuja);
		if (!p) return puudub();
		try {
			const r = await paring(p, allikas.url, { maxBaite: 3_000_000, aegMs: 8000 });
			const tyyp = r.tyyp.split(';')[0].trim().toLowerCase();
			if (r.status !== 200 || !TYYBID.includes(tyyp)) return puudub();
			k = { tyyp, andmed: r.andmed, aeg: Date.now() };
			malu.delete(slug);
			malu.set(slug, k);
			while (malu.size > MAX_MALUS) malu.delete(malu.keys().next().value);
		} catch {
			return puudub();
		}
	}
	return new Response(k.andmed, {
		headers: {
			...PAISED,
			'Content-Type': k.tyyp,
			'Content-Security-Policy': "default-src 'none'",
			'Cache-Control': 'public, max-age=86400'
		}
	});
}
