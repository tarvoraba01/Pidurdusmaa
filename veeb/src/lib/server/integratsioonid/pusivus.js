/* Pakkujate puhvri püsivus Supabase'is.
 *
 *  - hetktõmmis: viimane õnnestunud kataloog (tabel pakkumised_hetktommis).
 *    Serveri restardil taastatakse see kohe, nii et hinnad on lehel ka siis,
 *    kui pakkuja API on parasjagu maas või aeglane.
 *  - hinnaajalugu: rida ainult siis, kui toote hind muutus või toode on uus
 *    (tabel hinnaajalugu). Nii jääb andmemaht väikeseks.
 *
 * Ilma Supabase'ita ei tee midagi (vt supabase.js). Vead ei kuku läbi.
 */
import { sbSees, sb, upsert, lisa } from '../supabase.js';

export const pusivusOlek = { salvestatud: null, taastatud: null, hinnamuutusi: 0, viga: null };

function viga(e) {
	pusivusOlek.viga = String(e.message || e).slice(0, 200);
	console.log('Supabase (pakkujad):', pusivusOlek.viga);
}

const tooteVoti = (t) => t.voti || [t.mark, t.mudel, t.moot, t.lisi || ''].join('|');

/** Salvesta kataloog (Map moot -> [toode]) ja hinnamuutused võrreldes vanaga. */
export async function salvesta(pakkuja, uus, vana, info) {
	if (!sbSees()) return;
	try {
		await upsert('pakkumised_hetktommis', {
			pakkuja,
			laetud: new Date().toISOString(),
			info: info || null,
			andmed: Object.fromEntries(uus)
		});
		pusivusOlek.salvestatud = new Date().toISOString();
	} catch (e) {
		viga(e);
	}
	if (!vana) return; /* esimene laadimine ilma võrdluseta — ajalugu algab järgmisest */
	try {
		const enne = new Map();
		for (const l of vana.values()) for (const t of l) enne.set(tooteVoti(t), t.hind);
		const read = [];
		for (const l of uus.values())
			for (const t of l) {
				const v = tooteVoti(t);
				if (enne.get(v) === t.hind) continue;
				read.push({
					pakkuja,
					voti: v,
					moot: t.moot,
					mark: t.mark || null,
					mudel: t.mudel || null,
					hind: Math.round(t.hind * 100) / 100,
					kogus: Number.isInteger(t.kogus) ? t.kogus : null
				});
			}
		if (read.length) await lisa('hinnaajalugu', read);
		pusivusOlek.hinnamuutusi += read.length;
	} catch (e) {
		viga(e);
	}
}

/** Viimane salvestatud kataloog → { indeks: Map, laetud: ms, info } või null. */
export async function taasta(pakkuja) {
	if (!sbSees()) return null;
	try {
		const r = await sb('pakkumised_hetktommis?pakkuja=eq.' + encodeURIComponent(pakkuja) + '&select=laetud,info,andmed', {
			aegMs: 20000
		});
		const rida = Array.isArray(r) ? r[0] : null;
		if (!rida || !rida.andmed) return null;
		pusivusOlek.taastatud = new Date().toISOString();
		return { indeks: new Map(Object.entries(rida.andmed)), laetud: Date.parse(rida.laetud), info: rida.info || {} };
	} catch (e) {
		viga(e);
		return null;
	}
}
