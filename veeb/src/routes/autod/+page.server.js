import { autod, polveNimi } from '$lib/server/autod.js';
import { pretty } from '$lib/server/andmed.js';

export function load() {
	const margid = [...autod().margid.values()]
		.map((m) => ({ slug: m.slug, nimi: m.nimi, n: m.polved.length, mudelid: [...new Set(m.polved.map((p) => p.model))].length }))
		.sort((a, b) => a.nimi.localeCompare(b.nimi, 'et'));
	/* otsingu jaoks kõik põlvkonnad: nimi, aadress, põhimõõt, aastad */
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
	return { margid, kokku: autod().polved.size, koik };
}
