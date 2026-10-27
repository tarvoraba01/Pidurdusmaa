/* GET /api/pilt/<slug> — rehvi pilt pakkujalt, meie serveri kaudu.
 *
 * Miks mitte otse pakkuja URL: pildi aadressis võib olla võti, pakkuja
 * võib keelata otselingid ja nii ei jälgi pakkuja meie külastajaid.
 * Laadimine, vähendamine (480 px webp), mälu- ja kettavahemälu: rehvipilt.js. */
import { piirang, liigaPalju, PAISED, SLUG_RE } from '$lib/server/integratsioonid/kaitse.js';
import { rehviPilt } from '$lib/server/integratsioonid/rehvipilt.js';

export const prerender = false;
/* API aadressid töötavad nii kaldkriipsuga kui ilma (lehtedel on alati kaldkriips) */
export const trailingSlash = 'ignore';

/* pilti pole: lühike vahemälu (pärast serveri restarti tekib pildi allikas alles hinnapäringuga) */
const puudub = () => new Response('Pilti ei ole', { status: 404, headers: { ...PAISED, 'Cache-Control': 'public, max-age=300' } });
/* ajutine viga (pakkuja aeglane/maas): ära jäta brauserisse meelde. X-Pilt-Pohjus: lühike põhjus ilma aadressita */
const ajutine = (pohjus) => new Response('Pilt ajutiselt kättesaamatu', { status: 503, headers: { ...PAISED, 'Cache-Control': 'no-store', 'X-Pilt-Pohjus': pohjus || '' } });

export async function GET(event) {
	if (!piirang('pilt', event, 120, 60)) return liigaPalju();
	const slug = event.params.slug;
	if (!SLUG_RE.test(slug)) return puudub();
	const k = await rehviPilt(slug);
	if (!k.andmed) return k.ajutine ? ajutine(k.pohjus) : puudub();
	return new Response(k.andmed, {
		headers: {
			...PAISED,
			'Content-Type': k.tyyp,
			'Content-Security-Policy': "default-src 'none'",
			'Cache-Control': 'public, max-age=86400'
		}
	});
}
