/* GET /api/kataloog?moot=20555R16&tyyp=suvi|lamell|naast
 * Rehvikataloogi nimekiri ühe mõõdu ja tüübi kohta koos hindadega (vt $lib/server/kataloog.js).
 * Kasutab /rehvid/ ja mõõdulehtede kataloog (Kataloog.svelte). */
import { piirang, vastus, liigaPalju, vigane, MOOT_RE } from '$lib/server/integratsioonid/kaitse.js';
import { kataloog, TYYBID } from '$lib/server/kataloog.js';

export const prerender = false;
export const trailingSlash = 'ignore';

export async function GET(event) {
	if (!piirang('kataloog', event, 60, 60)) return liigaPalju();
	const q = event.url.searchParams;
	const moot = q.get('moot') || '', tyyp = q.get('tyyp') || '';
	if (!MOOT_RE.test(moot) || !TYYBID.includes(tyyp)) return vigane('Anna moot ja tyyp');
	try {
		const d = await kataloog(moot, tyyp);
		if (!d) return vastus({ moot, tyyp, read: [], puudub: true }, { vahemalu: 300 });
		return vastus(d, { vahemalu: 300 });
	} catch (e) {
		console.error('Kataloog:', e.message);
		return vigane('Viga');
	}
}
