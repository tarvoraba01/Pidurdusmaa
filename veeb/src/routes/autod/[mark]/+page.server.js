import { error } from '@sveltejs/kit';
import { autod, polveNimi } from '$lib/server/autod.js';
import { pretty, sizeSlug, sizeModelCount, SIZE_MIN_MODELS } from '$lib/server/andmed.js';
import { marg80 } from '$lib/server/jaga.js';

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
	/* sissejuhatus ainult andmetest: kerede tüübid, tehase mõõdud, mass,
	   pidurdusmaa sama mudeliga mis kalkulaator */
	const keha = {}, moodud = new Map(), massid = [], pid = [];
	for (const p of m.polved) {
		const v0 = p.rows[0];
		if (v0.body) keha[v0.body] = (keha[v0.body] || 0) + 1;
		const pohi = String(v0.oemSize).toUpperCase().replace(/[/ ]/g, '');
		moodud.set(pohi, (moodud.get(pohi) || 0) + 1);
		for (const v of p.rows) if (v.kerbMassKg) massid.push(v.kerbMassKg);
		const d = marg80(v0.key);
		if (d) pid.push({ d, nimi: polveNimi(p) });
	}
	pid.sort((a, b) => a.d - b.d);
	const sissejuhatus = {
		keha: Object.entries(keha).sort((a, b) => b[1] - a[1]).map(([k]) => k),
		moodud: [...moodud.entries()]
			.sort((a, b) => b[1] - a[1])
			.slice(0, 6)
			.map(([z, k]) => ({ label: pretty(z), slug: sizeModelCount(z) >= SIZE_MIN_MODELS ? sizeSlug(z) : null, k })),
		moote: moodud.size,
		massMin: massid.length ? Math.min(...massid) : null,
		massMax: massid.length ? Math.max(...massid) : null,
		pidMin: pid[0] || null,
		pidMax: pid.length > 1 && pid[pid.length - 1].d - pid[0].d >= 0.5 ? pid[pid.length - 1] : null
	};
	return { mark: { slug: m.slug, nimi: m.nimi }, mudelid, n: m.polved.length, sissejuhatus };
}
