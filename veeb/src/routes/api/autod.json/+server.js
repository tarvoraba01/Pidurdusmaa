/* Autode otsingu nimekiri (AutoTee.svelte): nimi, aadress, põhimõõt, aastad.
   Tehakse ehitusel staatiliseks failiks; brauser laeb selle alles siis,
   kui kasutaja otsingulahtrisse klõpsab. */
import { json } from '@sveltejs/kit';
import { autod, polveNimi } from '$lib/server/autod.js';
import { pretty } from '$lib/server/andmed.js';

export const prerender = true;

export function GET() {
	const koik = [...autod().polved.values()].map((p) => {
		const aastad = (String(p.yearLabel).match(/\d{4}/g) || []).map(Number);
		return {
			n: polveNimi(p),
			u: '/autod/' + p.mk + '/' + p.slug + '/',
			m: pretty(String(p.rows[0].oemSize).toUpperCase().replace(/[/ ]/g, '')),
			a0: aastad[0] || null,
			a1: aastad.length > 1 ? aastad[1] : /\+/.test(p.yearLabel) ? 9999 : aastad[0] || null
		};
	});
	return json(koik);
}
