/* /ru/… ja /en/… näitavad sama lehte mis eestikeelne aadress —
   keel tuleb aadressist (vt $lib/i18n.js). Tõlkimata lehti vene ja
   inglise aadressi all ei ole (404). */
import { browser } from '$app/environment';
import { onTolgitud, laeRuRehvid } from '$lib/i18n.js';

export async function reroute({ url }) {
	const m = /^\/(ru|en)(\/.*)?$/.exec(url.pathname);
	if (!m) return;
	const p = m[2] || '/';
	/* Vene rehvileht: kas see on olemas, ütleb ~100 KB nimekiri, mida brauser igale lehele
	   kaasa ei saa (vt $lib/i18n.js laeRuRehvid). Serveris (ehitus) kontrollime täpselt.
	   Brauseris viivad /ru/rehvid/…-lingid ainult olemasolevatele lehtedele (linkLang teeb
	   need nimekirja järgi) ja puuduvale lehele annab server 404. */
	if (m[1] === 'ru' && /^\/rehvid\/[^/]+\/(__data\.json)?$/.test(p)) {
		if (browser) return p;
		await laeRuRehvid();
	}
	if (onTolgitud(m[1], p)) return p;
	/* SvelteKiti enda andmepäring (…/__data.json) */
	if (p.endsWith('/__data.json') && onTolgitud(m[1], p.slice(0, -'__data.json'.length))) return p;
}
