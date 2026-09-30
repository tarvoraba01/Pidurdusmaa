/* Keeled: eesti on põhikeel ja jääb aadressita (/). Vene ja inglise
   versioon on /ru/ ja /en/ all — ainult tööriistalehtedel (TOLGITUD).
   Tõlke võti on eestikeelne lähtetekst ise: kui tõlget pole, näidatakse
   eestikeelset. Sõnastikud ($lib/i18n/ru.js, en.js) laeb +layout.js ainult
   vene/inglise lehel, nii et eesti lehe kasutaja neid alla ei laadi. */
import { getContext } from 'svelte';

export const KEELED = ['et', 'ru', 'en'];
export const KEEL_NIMI = { et: 'Eesti', ru: 'Русский', en: 'English' };
export const OG_LOCALE = { et: 'et_EE', ru: 'ru_RU', en: 'en_GB' };

/** Lehed, millel on vene ja inglise versioon (tee ilma keele eesliiteta). */
export const TOLGITUD = ['/', '/rehvi-valimine/', '/vordle-rehve/', '/liiklusohutus/'];

/** Aadressi keel: /ru/... → 'ru', /en/... → 'en', muu → 'et'. */
export function langOf(pathname) {
	const m = /^\/(ru|en)(\/|$)/.exec(pathname || '');
	return m ? m[1] : 'et';
}

/** Tee ilma keele eesliiteta (/ru/rehvi-valimine/ → /rehvi-valimine/). */
export function baseOf(pathname) {
	return (pathname || '/').replace(/^\/(ru|en)(?=\/|$)/, '') || '/';
}

/** Tõlgitud lehe aadress antud keeles; tõlkimata leht jääb eestikeelseks. */
export function linkLang(lang, path) {
	if (!lang || lang === 'et') return path;
	const [p, rest] = splitPath(path);
	return TOLGITUD.includes(p) ? '/' + lang + p + rest : path;
}
function splitPath(path) {
	const i = path.search(/[?#]/);
	return i < 0 ? [path, ''] : [path.slice(0, i), path.slice(i)];
}

/* Tõlgitud HTML-i sees olevad lingid tõlgitud lehtedele saavad keele eesliite */
const HREF = /href="(\/(?:rehvi-valimine\/|vordle-rehve\/|liiklusohutus\/)?)(?=["?#])/g;

/** Tõlge: sõnastikus olemas → tõlge, muidu eestikeelne lähtetekst. */
export function tr(lang, dict, s) {
	if (!lang || lang === 'et' || typeof s !== 'string') return s;
	const v = (dict && dict[s]) || s;
	return v.indexOf('href="/') >= 0 ? v.replace(HREF, (m, p) => 'href="/' + lang + p) : v;
}

/** Komponendis: const t = useT(); … {t('Eestikeelne tekst')} */
export function useT() {
	const c = getContext('i18n');
	const f = (s) => (c ? tr(c.lang, c.dict, s) : s);
	return f;
}

/** Komponendis: praegune keel ja lingi abiline. */
export function useLang() {
	const c = getContext('i18n');
	return {
		get lang() {
			return c ? c.lang : 'et';
		},
		L: (path) => linkLang(c ? c.lang : 'et', path)
	};
}
