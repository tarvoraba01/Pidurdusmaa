import { core, models } from '$lib/server/andmed.js';
import { autod } from '$lib/server/autod.js';

/** /meist/ — kes teeb, kust andmed tulevad, kuidas me sõltumatuks jääme. */
export function load() {
	const c = core();
	const allikad = Object.entries(c.sources)
		.map(([kood, s]) => ({ kood: kood.toLowerCase(), nimi: s.nimi, aasta: s.aasta, tegija: s.tegija || '' }))
		.sort((a, b) => b.aasta - a.aasta || a.nimi.localeCompare(b.nimi, 'et'));
	return {
		allikad,
		mudeleid: Object.keys(models()).length,
		mootusid: c.eprelSizes.length,
		testitud: c.tyres.length,
		/* sama arv ja mõiste mis /autod/ lehel (üks leht põlvkonna kohta) */
		autosid: autod().polved.size
	};
}
