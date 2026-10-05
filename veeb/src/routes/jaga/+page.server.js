/* /jaga/?… — jagatud pidurdusmaa tulemus. Number arvutatakse serveris
   uuesti (lib/server/jaga.js); lehte ei indekseerita (iga link on eri leht). */
import { loeValik, arvuta, kalkLink } from '$lib/server/jaga.js';
import { mootoridJson } from '$lib/server/andmed.js';
import { langOf } from '$lib/i18n.js';

export const prerender = false;

export function load({ url, setHeaders }) {
	const val = loeValik(url.searchParams);
	if (val) val.l = langOf(url.pathname);
	const res = val ? arvuta(val, val.a.includes('~') ? mootoridJson() : null) : null;
	setHeaders({ 'Cache-Control': 'public, max-age=3600' });
	if (!res) return { res: null, kalk: '/', pilt: null, lang: val ? val.l : 'et' };
	const p = new URLSearchParams(url.searchParams);
	p.set('l', val.l);
	return { res, kalk: kalkLink(val), pilt: '/jaga/pilt.png?' + p.toString(), lang: val.l };
}
