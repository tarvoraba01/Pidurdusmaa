import { autod } from '$lib/server/autod.js';

export function load() {
	const margid = [...autod().margid.values()]
		.map((m) => ({ slug: m.slug, nimi: m.nimi, n: m.polved.length, mudelid: [...new Set(m.polved.map((p) => p.model))].length }))
		.sort((a, b) => a.nimi.localeCompare(b.nimi, 'et'));
	return { margid, kokku: autod().polved.size };
}
