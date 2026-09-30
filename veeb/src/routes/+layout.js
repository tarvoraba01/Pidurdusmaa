/* Kogu sait on staatiline: iga leht kirjutatakse ehituse ajal HTML-failiks. */
import { langOf } from '$lib/i18n.js';

export const prerender = true;
export const trailingSlash = 'always';

/* Vene/inglise lehel laetakse sõnastik; eesti lehel mitte midagi. */
export async function load({ url }) {
	const lang = langOf(url.pathname);
	if (lang === 'et') return { lang, dict: null };
	const dict = lang === 'ru' ? (await import('$lib/i18n/ru.js')).default : (await import('$lib/i18n/en.js')).default;
	return { lang, dict };
}
