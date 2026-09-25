import { margid, MARK_MIN_INDEKS } from '$lib/server/andmed.js';

/** /margid/ — kõik rehvitootjad. */
export function load() {
	const list = [...margid().values()]
		.map((m) => ({ slug: m.slug, nimi: m.nimi, n: m.mudelid.length, t: m.testitud.length }))
		.sort((a, b) => a.nimi.localeCompare(b.nimi, 'et'));
	return { list, min: MARK_MIN_INDEKS };
}
