import { talveMoodud, talveLeht, TALV_UUENDATUD } from '$lib/server/talv.js';

/* Ülevaate numbrid Eesti kõige levinuma mõõdu (205/55 R16) tüüpilise autoga */
export function load() {
	const d = talveLeht('205-55-r16');
	const top = (list) => list.filter((x) => x.jaa != null).slice(0, 5).map((x) => ({ slug: x.slug, nimi: x.nimi, jaa: x.jaa, lumi: x.lumi }));
	return {
		moodud: talveMoodud(),
		uuendatud: TALV_UUENDATUD,
		naide: d ? { moot: d.moot.label, slug: d.moot.slug, auto: d.auto?.nimi || '', tyybid: d.tyybid, naastud: top(d.naastud), lamellid: top(d.lamellid) } : null
	};
}
