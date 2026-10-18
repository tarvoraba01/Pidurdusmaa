/* Kogu sait on staatiline: iga leht kirjutatakse ehituse ajal HTML-failiks. */
import { langOf, laeRuRehvid } from '$lib/i18n.js';

export const prerender = true;
export const trailingSlash = 'always';

/* Vene/inglise lehel laetakse sõnastik; eesti lehel mitte midagi.
   Vene lehel ka vene rehvilehtede nimekiri (lingid /ru/rehvid/… ainult
   olemasolevatele lehtedele), paralleelselt sõnastikuga. */
export async function load({ url }) {
	const lang = langOf(url.pathname);
	if (lang === 'et') return { lang, dict: null };
	if (lang === 'ru') {
		const [d] = await Promise.all([import('$lib/i18n/ru.js'), laeRuRehvid()]);
		return { lang, dict: d.default };
	}
	return { lang, dict: (await import('$lib/i18n/en.js')).default };
}
