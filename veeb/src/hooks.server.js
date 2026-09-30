/* Serveri käivitumisel: laadi pakkujate suured failid (nt Awini tootefail)
 * kohe taustal, et esimene külastaja ei peaks ootama. Ehituse ajal mitte. */
import { building } from '$app/environment';

export async function init() {
	if (building) return;
	const { soojenda } = await import('$lib/server/integratsioonid/koond.js');
	soojenda();
	/* kontaktivormi kirjade säilitamine: vanemad kui 12 kuud ära */
	const { kustutaVanad } = await import('$lib/server/logi.js');
	kustutaVanad();
	setInterval(kustutaVanad, 864e5).unref();
}

/* Vene ja inglise lehel <html lang="ru|en"> (app.html-is on "et") */
import { langOf } from '$lib/i18n.js';
export async function handle({ event, resolve }) {
	const lang = langOf(event.url.pathname);
	if (lang === 'et') return resolve(event);
	return resolve(event, {
		transformPageChunk: ({ html }) => html.replace('<html lang="et">', '<html lang="' + lang + '">')
	});
}
