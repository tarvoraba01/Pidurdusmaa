import { error } from '@sveltejs/kit';
import { autod, polveLeht } from '$lib/server/autod.js';

export function entries() {
	return [...autod().polved.values()].map((p) => ({ mark: p.mk, polv: p.slug }));
}

export function load({ params }) {
	const p = autod().polved.get(params.mark + '/' + params.polv);
	if (!p) error(404, 'Autot ei leitud');
	return polveLeht(p);
}
