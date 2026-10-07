/* Koolitus: õpetaja grupid ja õpilaste vastused (Supabase: koolitus_grupid, koolitus_vastused).
 *
 *   POST /api/koolitus  { tegu:'loo', nimi, teemad[], kysimusi }          → { kood, voti }
 *   GET  /api/koolitus?kood=X                                            → { nimi, teemad, kysimusi }
 *   POST /api/koolitus  { tegu:'vastused', kood, sessioon, etapp, read:[[id, õige]] }
 *   GET  /api/koolitus?kood=X&tulemused=1  + Authorization: Bearer <voti> → koondtulemus
 *
 * Isikuandmeid pole: grupp = koodi + nime + teemadega, õpilane = juhuslik sessiooni-id.
 * Õpetaja võtit ei hoita, ainult sha256 räsi. Võti käib päises, mitte aadressis. */
import { createHash, randomBytes, timingSafeEqual } from 'node:crypto';
import { sb, sbSees } from '$lib/server/supabase.js';
import { piirang, vastus, liigaPalju, vigane, keelatud } from '$lib/server/integratsioonid/kaitse.js';
import { KYSIMUSED, TEEMAD } from '$lib/koolitus/kysimused.js';

export const prerender = false;
export const trailingSlash = 'ignore';

const KOOD_RE = /^[A-Z0-9]{2,12}-[A-Z0-9]{3}$/;
const SESS_RE = /^[a-z0-9]{8,32}$/;
const TEEMA = new Set(TEEMAD.map((t) => t[0]));
const KYS = new Map(KYSIMUSED.map((q) => [q.id, q]));
const rasi = (s) => createHash('sha256').update(String(s)).digest('hex');
const puudub = () => vastus({ ok: false, viga: 'Koolituse andmebaas pole praegu saadaval' }, { status: 503 });

/* kood nimest: „Viiking Autokool“ → VIIKING-7K3 (täpitähed lahti, juhuslik lõpp) */
function teeKood(nimi) {
	const alus = String(nimi).normalize('NFKD').replace(/[̀-ͯ]/g, '').toUpperCase().replace(/[^A-Z0-9 ]/g, ' ').trim().split(/\s+/)[0] || 'KOOL';
	const t = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
	const b = randomBytes(3);
	return alus.slice(0, 10) + '-' + [...b].map((x) => t[x % t.length]).join('');
}

export async function GET(event) {
	const { url, request } = event;
	if (!piirang('koolitus-get', event, 120, 60)) return liigaPalju();
	const kood = String(url.searchParams.get('kood') || '').toUpperCase();
	if (!KOOD_RE.test(kood)) return vigane('Vigane kood');
	if (!sbSees()) return puudub();
	let g;
	try {
		g = (await sb('koolitus_grupid?kood=eq.' + encodeURIComponent(kood) + '&select=kood,nimi,teemad,kysimusi,voti_rasi'))?.[0];
	} catch {
		return puudub();
	}
	if (!g) return vastus({ ok: false, viga: 'Sellist koodi ei ole' }, { status: 404 });
	if (!url.searchParams.has('tulemused')) return vastus({ ok: true, kood: g.kood, nimi: g.nimi, teemad: g.teemad, kysimusi: g.kysimusi });

	/* õpetaja: võti päises, võrdlus räsi kaudu */
	const h = request.headers.get('authorization') || '';
	const antud = h.startsWith('Bearer ') ? h.slice(7).trim() : '';
	if (!antud || !timingSafeEqual(Buffer.from(rasi(antud)), Buffer.from(g.voti_rasi))) return keelatud();
	let read = [];
	try {
		read = (await sb('koolitus_vastused?kood=eq.' + encodeURIComponent(kood) + '&select=sessioon,etapp,kysimus,oige&order=aeg.asc&limit=20000', { aegMs: 15000 })) || [];
	} catch {
		return puudub();
	}
	/* koond: sessioonid, keskmine enne/pärast, teemade ja küsimuste kaupa */
	const sess = new Map();
	const kys = new Map();
	const teemad = new Map();
	for (const r of read) {
		const s = sess.get(r.sessioon) || { eel: [0, 0], jarel: [0, 0] };
		s[r.etapp][0] += r.oige ? 1 : 0;
		s[r.etapp][1] += 1;
		sess.set(r.sessioon, s);
		const q = kys.get(r.kysimus) || { eel: [0, 0], jarel: [0, 0] };
		q[r.etapp][0] += r.oige ? 1 : 0;
		q[r.etapp][1] += 1;
		kys.set(r.kysimus, q);
		const tid = KYS.get(r.kysimus)?.teema;
		if (tid) {
			const t = teemad.get(tid) || { eel: [0, 0], jarel: [0, 0] };
			t[r.etapp][0] += r.oige ? 1 : 0;
			t[r.etapp][1] += 1;
			teemad.set(tid, t);
		}
	}
	const prots = (x) => (x[1] ? Math.round((x[0] / x[1]) * 100) : null);
	const kokku = (et) => [...sess.values()].reduce((a, s) => [a[0] + s[et][0], a[1] + s[et][1]], [0, 0]);
	return vastus({
		ok: true,
		kood: g.kood,
		nimi: g.nimi,
		osalejaid: { eel: [...sess.values()].filter((s) => s.eel[1]).length, jarel: [...sess.values()].filter((s) => s.jarel[1]).length },
		oigeid: { eel: prots(kokku('eel')), jarel: prots(kokku('jarel')) },
		teemad: [...teemad].map(([id, t]) => ({ id, eel: prots(t.eel), jarel: prots(t.jarel) })),
		kysimused: [...kys]
			.map(([id, q]) => ({ id, vastajaid: q.eel[1] + q.jarel[1], oige: prots([q.eel[0] + q.jarel[0], q.eel[1] + q.jarel[1]]) }))
			.filter((q) => q.vastajaid >= 2 && q.oige < 100)
			.sort((a, b) => a.oige - b.oige)
			.slice(0, 8)
	});
}

export async function POST(event) {
	const { request } = event;
	let b;
	try {
		b = await request.json();
	} catch {
		return vigane();
	}
	if (!sbSees()) return puudub();

	if (b?.tegu === 'loo') {
		if (!piirang('koolitus-loo', event, 10, 3600)) return liigaPalju();
		const nimi = String(b.nimi || '').replace(/[\u0000-\u001f<>]/g, '').trim().slice(0, 80);
		const teemad = [...new Set((Array.isArray(b.teemad) ? b.teemad : []).filter((t) => TEEMA.has(t)))];
		const kysimusi = [5, 10, 15].includes(+b.kysimusi) ? +b.kysimusi : 10;
		if (nimi.length < 2) return vigane('Lisa tunni või grupi nimi');
		if (!teemad.length) return vigane('Vali vähemalt üks teema');
		const voti = randomBytes(18).toString('base64url');
		for (let katse = 0; katse < 4; katse++) {
			const kood = teeKood(nimi);
			try {
				await sb('koolitus_grupid', { method: 'POST', prefer: 'return=minimal', body: { kood, nimi, teemad, kysimusi, voti_rasi: rasi(voti) } });
				return vastus({ ok: true, kood, voti, nimi, teemad, kysimusi });
			} catch (e) {
				if (!/409|duplicate/i.test(String(e.message))) return puudub();
			}
		}
		return puudub();
	}

	if (b?.tegu === 'vastused') {
		if (!piirang('koolitus-vastused', event, 60, 600)) return liigaPalju();
		const kood = String(b.kood || '').toUpperCase();
		const sessioon = String(b.sessioon || '');
		const etapp = b.etapp === 'jarel' ? 'jarel' : b.etapp === 'eel' ? 'eel' : '';
		if (!KOOD_RE.test(kood) || !SESS_RE.test(sessioon) || !etapp || !Array.isArray(b.read)) return vigane();
		const read = b.read
			.slice(0, 20)
			.filter((r) => Array.isArray(r) && KYS.has(r[0]))
			.map(([id, oige]) => ({ kood, sessioon, etapp, kysimus: id, oige: !!oige }));
		if (!read.length) return vigane();
		try {
			await sb('koolitus_vastused', { method: 'POST', prefer: 'return=minimal', body: read });
		} catch (e) {
			/* tundmatu kood (FK) → 400, muu → 503 */
			return /23503|foreign/i.test(String(e.message)) ? vigane('Sellist koodi ei ole') : puudub();
		}
		return vastus({ ok: true });
	}
	return vigane();
}
