import { error } from '@sveltejs/kit';
import { autod, polveLeht } from '$lib/server/autod.js';
import { talveMoot, talvParimadAutole } from '$lib/server/talv.js';
import { sizeSlug } from '$lib/server/andmed.js';

export function entries() {
	return [...autod().polved.values()].map((p) => ({ mark: p.mk, polv: p.slug }));
}

export function load({ params }) {
	const p = autod().polved.get(params.mark + '/' + params.polv);
	if (!p) error(404, 'Autot ei leitud');
	const d = polveLeht(p);
	const ts = sizeSlug(d.pohimoot.replace(/[/ ]/g, ''));
	const talvSlug = ts && talveMoot(ts) ? ts : null;
	/* KKK: jääl parim naast- ja lamellrehv selle auto põhimõõdus, pidurdusmaa selle auto andmetega */
	return { ...d, talvSlug, talvAuto: talvSlug ? talvParimadAutole(talvSlug, p.rows[0]) : null };
}
