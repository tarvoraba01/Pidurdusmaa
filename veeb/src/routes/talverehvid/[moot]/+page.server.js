import { error } from '@sveltejs/kit';
import { talveMoodud, talveLeht } from '$lib/server/talv.js';
import { core } from '$lib/server/andmed.js';

export function entries() {
	return talveMoodud().map((x) => ({ moot: x.slug }));
}

export function load({ params }) {
	const d = talveLeht(params.moot);
	if (!d) error(404, 'Mõõtu ei leitud');
	/* kataloogi mõõduvalik (Kataloog.svelte) */
	return { ...d, moodud: (core().eprelSizes || []).filter((x) => /^\d{5}R\d{2}$/.test(x)) };
}
