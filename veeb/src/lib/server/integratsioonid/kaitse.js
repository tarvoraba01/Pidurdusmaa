/* Ühine kaitse KÕIGILE API otspunktidele (src/routes/api/**).
 *
 *  - piirang(): päringute arv IP kohta ajaaknas. Mälus, piiratud suurusega
 *    (vanimad kirjed kukuvad välja — piirangut ei saa "üle ujutada").
 *  - votiOnOige(): salajase võtme kontroll konstantse ajaga (ajastusrünnak
 *    ei aita). Võti tuleb päisest "Authorization: Bearer …".
 *  - vastus(): JSON koos turvapäistega (ei vahemällu, ei MIME-arvamist,
 *    teised saidid ei saa vastust oma lehele laadida).
 *  - sisend: rangete mustritega kontroll — API ei võta vastu midagi, mida
 *    ta ei oota.
 */
import { json } from '@sveltejs/kit';
import { timingSafeEqual, createHash } from 'node:crypto';
import { ipHash } from '$lib/server/logi.js';

/* ------------------------------------------------------------ piirang */
const MAX_KIRJEID = 20000;
const kirjed = new Map(); // voti -> { algus, n }

/**
 * @param {string} nimi   otspunkti nimi (eraldi loendur)
 * @param {Request|any} event  SvelteKit'i event (getClientAddress)
 * @param {number} mitu   lubatud päringuid aknas
 * @param {number} sek    akna pikkus sekundites
 */
export function piirang(nimi, event, mitu, sek) {
	let ip = 'tundmatu';
	try {
		ip = ipHash(event.getClientAddress());
	} catch {
		/* ehituse ajal IP-d ei ole */
	}
	const voti = nimi + ':' + ip;
	const nyyd = Date.now();
	let k = kirjed.get(voti);
	if (!k || nyyd - k.algus > sek * 1000) {
		k = { algus: nyyd, n: 0 };
	}
	k.n += 1;
	kirjed.delete(voti); // Map hoiab lisamise järjekorda → viime lõppu
	kirjed.set(voti, k);
	while (kirjed.size > MAX_KIRJEID) kirjed.delete(kirjed.keys().next().value);
	return k.n <= mitu;
}

/* ------------------------------------------------------------ võti */
const rasi = (s) => createHash('sha256').update(String(s)).digest();

/** Kas päringus on õige võti? Tühi/seadmata võti = alati EI. */
export function votiOnOige(request, oige) {
	if (!oige || String(oige).length < 16) return false; // liiga lühike võti = välja lülitatud
	const h = request.headers.get('authorization') || '';
	const antud = h.startsWith('Bearer ') ? h.slice(7).trim() : '';
	if (!antud) return false;
	return timingSafeEqual(rasi(antud), rasi(oige));
}

/* ------------------------------------------------------------ vastus */
const PAISED = {
	'X-Content-Type-Options': 'nosniff',
	'Cross-Origin-Resource-Policy': 'same-origin',
	'Referrer-Policy': 'no-referrer',
	'X-Robots-Tag': 'noindex'
};

/** JSON-vastus turvapäistega. `vahemalu` sekundites (avalik), 0 = no-store. */
export function vastus(data, { status = 200, vahemalu = 0 } = {}) {
	return json(data, {
		status,
		headers: {
			...PAISED,
			'Cache-Control': vahemalu > 0 ? `public, max-age=${vahemalu}` : 'no-store'
		}
	});
}
export const liigaPalju = () => vastus({ ok: false, viga: 'Liiga palju päringuid. Proovi hiljem.' }, { status: 429 });
export const vigane = (viga = 'Vigane päring') => vastus({ ok: false, viga }, { status: 400 });
export const keelatud = () => vastus({ ok: false, viga: 'Ligipääs keelatud' }, { status: 401 });

export { PAISED };

/* ------------------------------------------------------------ sisend */
export const MOOT_RE = /^\d{5}R\d{2}C?$/; // 20555R16, 21565R16C
export const SLUG_RE = /^[a-z0-9]+(?:-[a-z0-9]+){0,15}$/; // rehvi slug
export const PID_RE = /^[a-z0-9-]{1,120}@\d{5}R\d{2}C?$/; // slug@MÕÕT
