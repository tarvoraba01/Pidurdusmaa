/* Keeled: eesti on põhikeel ja jääb aadressita (/). Vene ja inglise
   versioon on /ru/ ja /en/ all — ainult tööriistalehtedel (TOLGITUD).
   Tõlke võti on eestikeelne lähtetekst ise: kui tõlget pole, näidatakse
   eestikeelset. Sõnastikud ($lib/i18n/ru.js, en.js) laeb +layout.js ainult
   vene/inglise lehel, nii et eesti lehe kasutaja neid alla ei laadi. */
import { getContext } from 'svelte';
import { ARTIKLID, artikliTee } from './artiklid.js';

export const KEELED = ['et', 'ru', 'en'];
export const KEEL_NIMI = { et: 'Eesti', ru: 'Русский', en: 'English' };
export const OG_LOCALE = { et: 'et_EE', ru: 'ru_RU', en: 'en_GB' };

/** Lehed, millel on vene ja inglise versioon (tee ilma keele eesliiteta). */
export const TOLGITUD = ['/', '/rehvi-valimine/', '/vordle-rehve/', '/liiklusohutus/', '/liiklusohutus/pimedas/', '/liiklusohutus/pikivahe/', '/liiklusohutus/kurv/', '/liiklusohutus/reaktsioon/', '/rehvi-vanus/', '/rehvi-kalkulaator/', '/kontakt/', '/kasutustingimused/', '/privaatsus/', '/teadmine/partnerid/'];

/* Lisaks ainult vene keeles:
   - autolehed (terve haru /autod/),
   - rehvilehed, mis on saidikaardis (nimekiri: scripts/ru-rehvid.mjs),
   - artiklid, millel on artiklid.js-is `ru` väli, ja artiklite nimekiri. */
const HARUD = { ru: ['/autod/', '/talverehvid/', '/margid/'], en: [] };
/* Vene rehvilehtede nimekiri (≈3600 slugi, ~100 KB) ei ole siin staatiliselt imporditud:
   muidu laeks iga leht (ka eesti oma) selle alla (audit 18.10: −100 KB JS-i igal lehel).
   Selle laeb laeRuRehvid(): +layout.js vene lehel (serveris ja brauseris) ja hooks.js reroute
   serveris. Eesti rehvilehe keelevahetus ja hreflang vajavad ainult lehe enda vastust; selle
   annab lehe andmeväli `ru` (rehvid/[slug]/+page.js). REEGEL: teiste rehvide vene versiooni
   küsida (L('/rehvid/…'), onTolgitud('ru', …)) ainult vene lehel, kus nimekiri on laetud. */
let RU_REHV = null;
let ruLaadimine = null;
const RU_TEADA = new Set();
export function laeRuRehvid() {
	return (ruLaadimine ??= import('./i18n/ru_rehvid.js').then((m) => {
		RU_REHV = new Set(m.default);
	}));
}
/** Selle rehvilehe vene versioon on olemas (lehe andmetest, vt rehvid/[slug]/+page.js). */
export function ruRehvOlemas(slug) {
	RU_TEADA.add(slug);
}
const TAPSED = {
	ru: new Set([
		'/rehvid/',
		'/naastrehvid/' /* märksõnade jaoturlehed (19.10) */,
		'/lamellrehvid/',
		'/suverehvid/',
		'/teadmine/artiklid/',
		'/teadmine/pidurdusteekond-ja-peatumisteekond/',
		'/teadmine/rehvivahetus/',
		'/teadmine/rehvimargis/',
		'/teadmine/kuidas-pidurdusmaa-arvutatakse/',
		...ARTIKLID.filter((a) => a.ru).map((a) => a.ruTee || artikliTee(a)),
		'/liiklusohutus/koolitus/',
		'/liiklusohutus/koolitus/tulemused/',
		'/jaga/' /* jagatud tulemus (noindex, serveris) */
	]),
	en: new Set(['/jaga/'])
};

/** Kas see (keeleta) tee on antud keeles olemas? */
export function onTolgitud(lang, p) {
	if (!lang || lang === 'et') return true;
	if (TOLGITUD.includes(p) || (TAPSED[lang] && TAPSED[lang].has(p))) return true;
	if ((HARUD[lang] || []).some((h) => p.startsWith(h))) return true;
	if (lang === 'ru') {
		const m = /^\/rehvid\/([^/]+)\/$/.exec(p);
		if (m && (RU_TEADA.has(m[1]) || (RU_REHV !== null && RU_REHV.has(m[1])))) return true;
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

/** Tõlge kohatäidetega: tf(lang, dict, 'Mõõt {m}', { m: '205/55 R16' })
 *  Vene ainsus/mitmus sõnastiku väärtuses: {k|модель|модели|моделей} → „21 модель“, „32 модели“, „45 моделей“
 *  (Intl.PluralRules: one | few | many; murdarv → few). Eesti võtmes jääb lihtsalt {k}. */
const _pl = new Map();
function mitmus(lang, n, vormid) {
	if (!_pl.has(lang)) _pl.set(lang, new Intl.PluralRules(lang));
	const r = Number.isFinite(n) ? _pl.get(lang).select(n) : 'many';
	const [one, few, many] = vormid;
	return (r === 'one' ? one : r === 'few' ? few : r === 'many' ? many : few) || many || one || '';
}
export function tf(lang, dict, s, vars) {
	return String(tr(lang, dict, s)).replace(/\{(\w+)(?:\|([^{}]*))?\}/g, (m, k, vormid) => {
		if (!vars || vars[k] == null) return m;
		if (!vormid) return vars[k];
		const n = Number(String(vars[k]).replace(/[\s\u00a0\u202f]/g, '').replace(',', '.'));
		return vars[k] + ' ' + mitmus(lang, n, vormid.split('|'));
	});
}

/** Jagamispilt keeles: /og/sait/avaleht.png → /og/sait/avaleht.ru.png (kui on tehtud) */
export function ogLang(lang, image) {
	if (!lang || lang === 'et') return image;
	const m = /^\/og\/(sait|auto)\/(.+)\.png$/.exec(image || '');
	if (!m) return image;
	if (m[1] === 'sait' && !(OG_KEELED[m[2]] || []).includes(lang)) return image;
	if (m[1] === 'auto' && lang !== 'ru') return image;
	return '/og/' + m[1] + '/' + m[2] + '.' + lang + '.png';
}
/* millistes keeltes on saidi pilt tehtud (vt routes/og) */
const OG_KEELED = {
	avaleht: ['ru', 'en'],
	liiklusohutus: ['ru', 'en'],
	'liiklus-kurv': ['ru', 'en'],
	'liiklus-pimedas': ['ru', 'en'],
	'liiklus-pikivahe': ['ru', 'en'],
	'liiklus-reaktsioon': ['ru', 'en'],
	'rehvi-vanus': ['ru', 'en'],
	'rehvi-kalkulaator': ['ru', 'en'],
	'millal-talverehvid-alla': ['ru'],
	rehvivahetus: ['ru'],
	'talverehvide-nouded': ['ru'],
	'talverehvid-valismaal': ['ru'],
	'naastrehvid-liiga-vara-voi-hilja': ['ru'],
	'talverehvi-margistus-3pmsf': ['ru'],
	'nelja-aastaaja-rehvid': ['ru'],
	'kasutatud-talverehvid': ['ru'],
	'rehvi-kulje-margistus': ['ru'],
	'odav-voi-kallis-talverehv': ['ru']
};

/** Automudeli nimi vene keeles: E-klass → E-Класс, 3-seeria → 3 серии, kaubik → фургон.
 *  NB: ainult kuvamiseks — aadressid (slug) tehakse alati eestikeelsest nimest. */
export function autoNimi(lang, s) {
	if (lang !== 'ru' || !s) return s;
	return String(s)
		.replace(/\b([A-Z])-klass\b/g, '$1-Класс')
		.replace(/\b(\d)-seeria\b/g, '$1 серии')
		.replace(/\bkaubik\b/g, 'фургон')
		.replace(/\buniversaal\b/g, 'универсал')
		.replace(/\bMoskvitš/g, 'Москвич')
		.replace(/\bZaporožets\b/g, 'Запорожец');
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
