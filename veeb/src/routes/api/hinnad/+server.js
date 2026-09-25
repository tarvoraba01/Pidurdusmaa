/* GET /api/hinnad?moot=20555R16          → kõik selle mõõdu hinnad
 * GET /api/hinnad?ids=slug@20555R16,…     → ainult need rehvid (max 40)
 * Vastus: { available, hinnad: { 'slug@MÕÕT': [ {myyja, hind, url, laos} ] } }
 * Seda kasutab kalkulaator ja võrdlus (app.js Prices). */
import { piirang, vastus, liigaPalju, vigane, MOOT_RE, PID_RE } from '$lib/server/integratsioonid/kaitse.js';
import { hinnadMoodus, hinnadIdd, aktiivsed } from '$lib/server/integratsioonid/koond.js';

export const prerender = false;
/* API aadressid töötavad nii kaldkriipsuga kui ilma (lehtedel on alati kaldkriips) */
export const trailingSlash = 'ignore';

export async function GET(event) {
	if (!piirang('hinnad', event, 60, 60)) return liigaPalju();
	if (!aktiivsed().length) return vastus({ available: false, hinnad: {} }, { vahemalu: 300 });
	const q = event.url.searchParams;
	const moot = q.get('moot');
	const ids = q.get('ids');
	try {
		if (moot) {
			if (!MOOT_RE.test(moot)) return vigane('Vigane mõõt');
			return vastus(await hinnadMoodus(moot), { vahemalu: 300 });
		}
		if (ids) {
			const list = [...new Set(ids.split(','))];
			if (list.length > 40 || !list.every((x) => PID_RE.test(x))) return vigane('Vigased rehvid');
			return vastus(await hinnadIdd(list), { vahemalu: 300 });
		}
	} catch {
		return vastus({ available: false, hinnad: {} });
	}
	return vigane('Anna moot või ids');
}
