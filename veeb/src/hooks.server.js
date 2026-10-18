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
	/* Supabase'i failsafe: kirjuta kohe ja siis iga 24 h (write_count +1 kord nädalas) */
	const { failsafe } = await import('$lib/server/supabase.js');
	failsafe();
	setInterval(failsafe, 864e5).unref();
	/* sulgemisel: saatmata logiread faili, et midagi ei kaoks */
	const { tuhjendaFaili } = await import('$lib/server/logi.js');
	process.once('SIGTERM', tuhjendaFaili);
	process.once('SIGINT', tuhjendaFaili);
}

/* Vene ja inglise lehel <html lang="ru|en"> (app.html-is on "et") */
import { langOf } from '$lib/i18n.js';

/* (audit 18.10) Stiilifailid <head>-i algusesse, enne ~30 JS-i eellaadimist (modulepreload).
   SvelteKit paneb need <head>-i lõppu: brauser küsis CSS-i (mis blokeerib esimese
   joonistuse) viimasena ja aeglases võrgus jagas see ribalaiust kogu JS-iga.
   Stiilifailide omavaheline järjekord jääb samaks. */
const CSS_LINK = /<link href="[^"]+\.css" rel="stylesheet">/g;
const ESIMENE_JS = /<link href="[^"]+" rel="modulepreload">/;
function cssEtte(html) {
	const css = html.match(CSS_LINK);
	const j = html.search(ESIMENE_JS);
	if (!css || j < 0 || html.indexOf(css[0]) < j) return html; /* pole või on juba ees */
	const ilma = html.replace(CSS_LINK, '');
	const k = ilma.search(ESIMENE_JS);
	return ilma.slice(0, k) + css.join('') + ilma.slice(k);
}

export async function handle({ event, resolve }) {
	const lang = langOf(event.url.pathname);
	return resolve(event, {
		transformPageChunk: ({ html }) => {
			html = cssEtte(html);
			return lang === 'et' ? html : html.replace('<html lang="et">', '<html lang="' + lang + '">');
		}
	});
}
