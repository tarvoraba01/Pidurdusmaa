/* /ru/… ja /en/… näitavad sama lehte mis eestikeelne aadress —
   keel tuleb aadressist (vt $lib/i18n.js). Tõlkimata lehti vene ja
   inglise aadressi all ei ole (404). */
import { TOLGITUD } from '$lib/i18n.js';

export function reroute({ url }) {
	const m = /^\/(ru|en)(\/.*)?$/.exec(url.pathname);
	if (!m) return;
	const p = m[2] || '/';
	if (TOLGITUD.includes(p)) return p;
	/* SvelteKiti enda andmepäring (…/__data.json) */
	if (p.endsWith('/__data.json') && TOLGITUD.includes(p.slice(0, -'__data.json'.length))) return p;
}
