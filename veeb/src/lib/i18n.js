/* Keeled: eesti on põhikeel ja jääb aadressita (/). Vene ja inglise
   versioon on /ru/ ja /en/ all — ainult tööriistalehtedel (TOLGITUD).
   Tõlke võti on eestikeelne lähtetekst ise: kui tõlget pole, näidatakse
   eestikeelset. Sõnastikud ($lib/i18n/ru.js, en.js) laeb +layout.js ainult
   vene/inglise lehel, nii et eesti lehe kasutaja neid alla ei laadi. */
import { getContext } from 'svelte';
import RU_REHVID from './i18n/ru_rehvid.js';
import { ARTIKLID, artikliTee } from './artiklid.js';

export const KEELED = ['et', 'ru', 'en'];
export const KEEL_NIMI = { et: 'Eesti', ru: 'Русский', en: 'English' };
export const OG_LOCALE = { et: 'et_EE', ru: 'ru_RU', en: 'en_GB' };

/** Lehed, millel on vene ja inglise versioon (tee ilma keele eesliiteta). */
export const TOLGITUD = ['/', '/rehvi-valimine/', '/vordle-rehve/', '/liiklusohutus/'];

/* Lisaks ainult vene keeles:
   - autolehed (terve haru /autod/),
   - rehvilehed, mis on saidikaardis (nimekiri: scripts/ru-rehvid.mjs),
   - artiklid, millel on artiklid.js-is `ru` väli, ja artiklite nimekiri. */
const HARUD = { ru: ['/autod/', '/talverehvid/'], en: [] };
const RU_REHV = new Set(RU_REHVID);
const TAPSED = {
	ru: new Set([
		'/rehvid/',
		'/teadmine/artiklid/',
		'/teadmine/pidurdusteekond-ja-peatumisteekond/',
		'/teadmine/rehvivahetus/',
		...ARTIKLID.filter((a) => a.ru).map((a) => a.ruTee || artikliTee(a))
	]),
	en: new Set()
};

/** Kas see (keeleta) tee on antud keeles olemas? */
export function onTolgitud(lang, p) {
	if (!lang || lang === 'et') return true;
	if (TOLGITUD.includes(p) || (TAPSED[lang] && TAPSED[lang].has(p))) return true;
	if ((HARUD[lang] || []).some((h) => p.startsWith(h))) return true;
	if (lang === 'ru') {
		const m = /^\/rehvid\/([^/]+)\/$/.exec(p);
		if (m && RU_REHV.has(m[1])) return true;
	}
	return false;
}

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
	return onTolgitud(lang, p) ? '/' + lang + p + rest : path;
}
function splitPath(path) {
	const i = path.search(/[?#]/);
	return i < 0 ? [path, ''] : [path.slice(0, i), path.slice(i)];
}

/* Tõlgitud HTML-i sees olevad lingid tõlgitud lehtedele saavad keele eesliite */
const HREF = /href="(\/[^"?#]*)(?=["?#])/g;

/** Tõlge: sõnastikus olemas → tõlge, muidu eestikeelne lähtetekst. */
export function tr(lang, dict, s) {
	if (!lang || lang === 'et' || typeof s !== 'string') return s;
	const v = (dict && dict[s]) || s;
	return v.indexOf('href="/') >= 0 ? v.replace(HREF, (m, p) => (onTolgitud(lang, p) ? 'href="/' + lang + p : m)) : v;
}

/** Tõlgitud HTML-i (nt artikli sisu) sisemised lingid: tõlgitud lehtedele keele eesliide */
export function lingid(lang, html) {
	if (!lang || lang === 'et' || !html) return html;
	return String(html).replace(HREF, (m, p) => (onTolgitud(lang, p) ? 'href="/' + lang + p : m));
}

/** Tõlge kohatäidetega: tf(lang, dict, 'Mõõt {m}', { m: '205/55 R16' }) */
export function tf(lang, dict, s, vars) {
	return String(tr(lang, dict, s)).replace(/\{(\w+)\}/g, (m, k) => (vars && vars[k] != null ? vars[k] : m));
}

/** Jagamispilt keeles: /og/sait/avaleht.png → /og/sait/avaleht.ru.png (kui on tehtud) */
export function ogLang(lang, image) {
	if (!lang || lang === 'et') return image;
	const m = /^\/og\/(sait|auto)\/(.+)\.png$/.exec(image || '');
	if (!m) return image;
	if (m[1] === 'sait' && !['avaleht', 'liiklusohutus', 'millal-talverehvid-alla'].includes(m[2])) return image;
	if (m[1] === 'sait' && m[2] === 'millal-talverehvid-alla' && lang !== 'ru') return image;
	if (m[1] === 'auto' && lang !== 'ru') return image;
	return '/og/' + m[1] + '/' + m[2] + '.' + lang + '.png';
}

/** Automudeli nimi vene keeles: E-klass → E-Класс, 3-seeria → 3 серии, kaubik → фургон.
 *  NB: ainult kuvamiseks — aadressid (slug) tehakse alati eestikeelsest nimest. */
export function autoNimi(lang, s) {
	if (lang !== 'ru' || !s) return s;
	return String(s)
		.replace(/\b([A-Z])-klass\b/g, '$1-Класс')
		.replace(/\b(\d)-seeria\b/g, '$1 серии')
		.replace(/\bkaubik\b/g, 'фургон')
		.replace(/\buniversaal\b/g, 'универсал');
}

/** Komponendis: const t = useT(); … {t('Eestikeelne tekst')} */
export function useT() {
	const c = getContext('i18n');
	const f = (s, vars) => (vars ? tf(c ? c.lang : 'et', c ? c.dict : null, s, vars) : c ? tr(c.lang, c.dict, s) : s);
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
