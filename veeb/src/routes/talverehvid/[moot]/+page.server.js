import { error } from '@sveltejs/kit';
import { talveMoodud, talveLeht } from '$lib/server/talv.js';

export function entries() {
	return talveMoodud().map((x) => ({ moot: x.slug }));
}

export function load({ params }) {
	const d = talveLeht(params.moot);
	if (!d) error(404, 'Mõõtu ei leitud');
	return d;
}
