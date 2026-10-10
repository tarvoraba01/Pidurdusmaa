import { core } from '$lib/server/andmed.js';

/** /testid/ — rehvitestid, mille tulemusi mudel kasutab.
 *  Iga testi juures 3 lühimat märja asfaldi pidurdusmaad (testi enda mõõtmine,
 *  mitte testi üldhinne — sõnastus lehel ütleb seda). */
export function load() {
	const c = core();
	const sources = Object.entries(c.sources).map(([code, s]) => {
		const tulemus = [];
		for (const t of c.tyres)
			for (const x of t.tests)
				if (x.src === code && x.surf === 'ASPHALT' && x.wet) tulemus.push({ slug: t.slug, name: t.name, m: x.m, v0: x.v0, v1: x.v1 || 0 });
		tulemus.sort((a, b) => a.m - b.m);
		const nimi = s.nimi.toLowerCase();
		const hooaeg = s.aasta < 2020 ? 'vana' : /talve|naast|naelu/.test(nimi) && !/aastaring/.test(nimi) ? 'talv' : 'suvi';
		return { ...s, slug: code.toLowerCase(), hooaeg, top: tulemus.slice(0, 3) };
	});
	return { sources };
}
