import { core } from '$lib/server/andmed.js';
import { arvuta } from '$lib/server/jaga.js';

/** Avalehe numbrid (demo) tulevad ehituse ajal core.json-ist — samast
 *  mudelist, mis kalkulaator. Ei ühtki käsitsi kirjutatud arvu. */
export function load() {
	return { demo: core().demo || null, hero: heroNumbrid() };
}

/* Hero animatsiooni kolm rada: VW Golf 8, 205/55 R16, 90 km/h, uus tüüpiline
   rehv — täpselt see, mida kalkulaator samade valikutega näitab
   (märjal märgise klass C, kuival suverehvi ja lumel Põhjamaade talverehvi
   kategooria keskmine). Varem olid numbrid käsitsi kirjutatud. */
function heroNumbrid() {
	const v = (o, r) => {
		const x = arvuta({ a: 'vw_golf_8', ab: false, m: '20555R16', o, v: 90, r, mm: null, rt: 0, l: 'et' });
		return x ? Math.round(x.d * 10) / 10 : null;
	};
	const h = { kuiv: v('dry', 'k:SUMMER_TOURING'), marg: v('wet', 'c:SUMMER_TOURINGC'), lumi: v('snow', 'k:WINTER_NORDIC') };
	if (!h.kuiv || !h.marg || !h.lumi) throw new Error('Hero pidurdusmaad ei saanud arvutada');
	return h;
}
