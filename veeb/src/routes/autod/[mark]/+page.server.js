import { error } from '@sveltejs/kit';
import { autod, polveNimi } from '$lib/server/autod.js';
import { pretty } from '$lib/server/andmed.js';

export function entries() {
	return [...autod().margid.keys()].map((mark) => ({ mark }));
}

export function load({ params }) {
	const m = autod().margid.get(params.mark);
	if (!m) error(404, 'Marki ei leitud');
	const mudelid = [];
	for (const p of m.polved) {
		let x = mudelid.find((y) => y.model === p.model);
		if (!x) mudelid.push((x = { model: p.model, polved: [] }));
		x.polved.push({ slug: p.slug, yearLabel: p.yearLabel, nimi: polveNimi(p), moot: pretty(String(p.rows[0].oemSize).toUpperCase().replace(/[/ ]/g, '')) });
	}
	return { mark: { slug: m.slug, nimi: m.nimi }, mudelid, n: m.polved.length };
}
