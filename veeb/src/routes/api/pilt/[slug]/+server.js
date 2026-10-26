/* GET /api/pilt/<slug> — rehvi pilt pakkujalt, meie serveri kaudu.
 *
 * Miks mitte otse pakkuja URL: pildi aadressis võib olla võti, pakkuja
 * võib keelata otselingid ja nii ei jälgi pakkuja meie külastajaid.
 * Server laeb pildi ainult pakkuja lubatud aadressilt, kontrollib, et see
 * on päriselt pilt (jpeg/png/webp/avif, kuni 3 MB), hoiab mälus ja annab
 * edasi pika vahemäluga. */
import { piirang, liigaPalju, PAISED, SLUG_RE } from '$lib/server/integratsioonid/kaitse.js';
import { pildiAllikad, pakkujaId } from '$lib/server/integratsioonid/koond.js';
import { paring } from '$lib/server/integratsioonid/http.js';

export const prerender = false;
/* API aadressid töötavad nii kaldkriipsuga kui ilma (lehtedel on alati kaldkriips) */
export const trailingSlash = 'ignore';

const TYYBID = ['image/jpeg', 'image/png', 'image/webp', 'image/avif'];
/* pildi tüüp failialguse („maagiliste baitide“) järgi; muu kui pilt → null */
function nuusi(b) {
	if (!b || b.length < 12) return null;
	if (b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff) return 'image/jpeg';
	if (b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4e && b[3] === 0x47) return 'image/png';
	const a = String.fromCharCode(...b.subarray(0, 12));
	if (a.startsWith('RIFF') && a.slice(8, 12) === 'WEBP') return 'image/webp';
	if (a.slice(4, 12) === 'ftypavif') return 'image/avif';
	return null;
}
const MAX_MALUS = 300;
const malu = new Map(); // slug -> { tyyp, andmed, aeg }
const PAEV = 86400 * 1000;

/* pilti pole: lühike vahemälu (pärast serveri restarti tekib pildi allikas alles hinnapäringuga) */
const puudub = () => new Response('Pilti ei ole', { status: 404, headers: { ...PAISED, 'Cache-Control': 'public, max-age=300' } });
/* ajutine viga (pakkuja aeglane/maas): ära jäta brauserisse meelde */
const ajutine = () => new Response('Pilt ajutiselt kättesaamatu', { status: 503, headers: { ...PAISED, 'Cache-Control': 'no-store' } });

export async function GET(event) {
	if (!piirang('pilt', event, 120, 60)) return liigaPalju();
	const slug = event.params.slug;
	if (!SLUG_RE.test(slug)) return puudub();

	let k = malu.get(slug);
	if (!k || Date.now() - k.aeg > 7 * PAEV) {
		/* proovi pakkujate pilte järjest: esimene, mis annab päris pildi, jääb meelde */
		const allikad = await pildiAllikad(slug).catch(() => []);
		let ajutiseltMaas = false;
		k = null;
		for (const allikas of allikad) {
			const p = pakkujaId(allikas.pakkuja);
			if (!p) continue;
			try {
				const r = await paring(p, allikas.url, { maxBaite: 3_000_000, aegMs: 8000 });
				/* Inter Carsi CDN annab osale piltidest tüübi application/octet-stream (Tarvo 26.10:
				   Nexen N'Blue 4Season 2 pildita; 205/55 R16 mõõdus 19 intercars-pilti 34-st). Siis
				   otsustame failialguse järgi — ainult päris jpeg/png/webp/avif läheb läbi. */
				let tyyp = r.tyyp.split(';')[0].trim().toLowerCase();
				if (r.status === 200 && !TYYBID.includes(tyyp)) tyyp = nuusi(r.andmed) || tyyp;
				if (r.status >= 500 || r.status === 429) { ajutiseltMaas = true; continue; }
				if (r.status !== 200 || !TYYBID.includes(tyyp)) continue;
				k = { tyyp, andmed: r.andmed, aeg: Date.now() };
				break;
			} catch {
				ajutiseltMaas = true;
			}
		}
		if (!k) return ajutiseltMaas ? ajutine() : puudub();
		malu.delete(slug);
		malu.set(slug, k);
		while (malu.size > MAX_MALUS) malu.delete(malu.keys().next().value);
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
