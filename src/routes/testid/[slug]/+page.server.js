import { error } from '@sveltejs/kit';
import { core, source, testLabel } from '$lib/server/andmed.js';

export function entries() {
	return Object.keys(core().sources).map((code) => ({ slug: code.toLowerCase() }));
}

/** /testid/<kood>/ — ühe testi kõik mõõdetud tulemused ühes tabelis. */
export function load({ params }) {
	const code = params.slug.toUpperCase();
	const src = source(code);
	if (!src) error(404, 'Sellist testi ei ole');

	/* Veerud: kõik selles testis mõõdetud pind+kiirus kombinatsioonid */
	const cols = new Map();
	const rows = new Map();
	for (const t of core().tyres) {
		for (const x of t.tests) {
			if (x.src !== code) continue;
			const k = [x.surf, x.wet ? 1 : 0, x.v0, x.v1].join('|');
			cols.set(k, testLabel(x));
			if (!rows.has(t.key)) rows.set(t.key, { slug: t.slug, name: t.name, v: {} });
			rows.get(t.key).v[k] = x.m;
		}
	}
	const colKeys = [...cols.keys()];
	const wetk = colKeys.find((k) => k.startsWith('ASPHALT|1')) || null;
	let list = [...rows.values()];
	if (wetk) list.sort((a, b) => (a.v[wetk] ?? 999) - (b.v[wetk] ?? 999));

	const best = {};
	for (const k of colKeys) {
		const vals = list.map((r) => r.v[k]).filter((v) => v != null);
		best[k] = vals.length ? Math.min(...vals) : null;
	}

	return {
		src: { ...src, slug: params.slug, host: hostOf(src.kajastus) },
		cols: colKeys.map((k) => [k, cols.get(k)]),
		list,
		best,
		wet: !!wetk,
		vib: (core().vib || {})[code] || null
	};
}

function hostOf(u) {
	try {
		return new URL(u).host;
	} catch {
		return u;
	}
}
