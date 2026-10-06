import { json } from '@sveltejs/kit';
import { lisaRida, ipHash, kasLubatud, kliendiIp } from '$lib/server/logi.js';

export const prerender = false;
/* API aadressid töötavad nii kaldkriipsuga kui ilma (lehtedel on alati kaldkriips) */
export const trailingSlash = 'ignore';

/* Anonüümne kasutuslugu: MIDA lehel tehti, mitte kes tegi.
 *
 * Brauser saadab siia kogumi sündmusi (app.js Track). Iga rida on
 * {s: sekundit algusest, e: sündmus, v: väärtus}. Nime, e-posti,
 * IP-d ega küpsist ei salvestata — ainult soolatud räsi, et ühe
 * masina üleujutus ei täidaks ketast. */
export async function POST(event) {
	const { request } = event;
	const ip = ipHash(kliendiIp(event));
	if (!kasLubatud('logi:' + ip, 120, 600)) return json({ ok: false }, { status: 429 });

	let pakk;
	try {
		pakk = await request.json();
	} catch {
		return json({ ok: false }, { status: 400 });
	}
	const read = Array.isArray(pakk?.e) ? pakk.e.slice(0, 100) : [];
	if (!read.length) return json({ ok: true });

	const aeg = new Date().toISOString();
	for (const r of read) {
		/* sündmuse nimi on alati meie oma (app.js Track): väiketähed ja _ */
		if (!r || typeof r.e !== 'string' || !/^[a-z_]{1,40}$/.test(r.e)) continue;
		lisaRida('logi.jsonl', {
			t: aeg,
			k: ip, /* sessiooni umbisikuline tunnus */
			s: Number(r.s) || 0,
			e: r.e,
			v: r.v == null ? undefined : puhasta(String(r.v)).slice(0, 120)
		});
	}
	return json({ ok: true });
}

/* Otsingusõnas võib inimene kogemata kirjutada e-posti või telefoninumbri —
   neid ei salvestata (audit 6.10). Rehvimõõdud (20555R16) jäävad alles. */
function puhasta(v) {
	return v
		.replace(/[^\s@]+@[^\s@]+/g, '[e-post]')
		.replace(/\+?\d[\d\s-]{6,}\d/g, (m) => (m.replace(/\D/g, '').length >= 7 ? '[number]' : m));
}
