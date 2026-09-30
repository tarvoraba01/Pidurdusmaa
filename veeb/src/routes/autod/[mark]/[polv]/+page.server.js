import { error } from '@sveltejs/kit';
import { autod, polveLeht } from '$lib/server/autod.js';
import { talveMoot } from '$lib/server/talv.js';
import { sizeSlug } from '$lib/server/andmed.js';

export function entries() {
	return [...autod().polved.values()].map((p) => ({ mark: p.mk, polv: p.slug }));
}

export function load({ params }) {
	const p = autod().polved.get(params.mark + '/' + params.polv);
	if (!p) error(404, 'Autot ei leitud');
	const d = polveLeht(p);
	const ts = sizeSlug(d.pohimoot.replace(/[/ ]/g, ''));
	return { ...d, talvSlug: ts && talveMoot(ts) ? ts : null };
}
