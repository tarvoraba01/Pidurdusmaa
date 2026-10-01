/* Rehvivahetuse kuupäevad Eestis (seaduse järgi) ja tänane seis.
 *
 * Allikas: Transpordiamet
 *   - naastrehvid 15.10–31.03, talviste tee- ja ilmastikuolude korral 1.10–30.04
 *   - talverehvid kohustuslikud 1.12–1.03
 *   - talvisel perioodil kasutatavatel lamellrehvidel kolme mäetipu ja lumehelbe tähis
 *   - talverehvi muster > 3 mm, suverehvi muster ≥ 1,6 mm
 * https://www.transpordiamet.ee/uudised/homsest-lubatud-kasutada-naastrehve (14.10.2024)
 * https://www.transpordiamet.ee/uudised/talverehvide-vahetamisega-voib-veel-oodata (27.03.2024)
 *
 * Kõik kuupäevad arvutatakse antud päeva järgi, nii et leht ei vanane:
 * mai–detsember → eelseisev talv (S = sel aastal), jaanuar–aprill → käimasolev (S = eelmine aasta).
 */

export const ALLIKAD = [
	'https://www.transpordiamet.ee/uudised/homsest-lubatud-kasutada-naastrehve',
	'https://www.transpordiamet.ee/uudised/talverehvide-vahetamisega-voib-veel-oodata'
];

const P = (y, m, d) => new Date(y, m - 1, d);
const paev = (x) => new Date(x.getFullYear(), x.getMonth(), x.getDate());

/** Hooaja kuupäevad päeva `nyyd` järgi. */
export function hooaeg(nyyd = new Date()) {
	const t = paev(nyyd);
	const S = t.getMonth() + 1 >= 5 ? t.getFullYear() : t.getFullYear() - 1;
	return {
		S,
		naastTalv: P(S, 10, 1), //       naastrehvid talveoludes alates
		naast: P(S, 10, 15), //          naastrehvid lubatud alates
		kohustus: P(S, 12, 1), //        talverehvid kohustuslikud alates
		kohustusLopp: P(S + 1, 3, 1), // … kuni (k.a)
		naastLopp: P(S + 1, 3, 31), //   naastrehvid lubatud kuni
		naastTalvLopp: P(S + 1, 4, 30) // naastrehvid talveoludes kuni
	};
}

/** Tänane seis: naast 'lubatud' | 'talveoludes' | 'keelatud'; talv 'kohustuslik' | 'vabatahtlik'. */
export function tana(nyyd = new Date()) {
	const t = paev(nyyd);
	const h = hooaeg(t);
	const sees = (a, b) => t >= a && t <= b;
	const naast = sees(h.naast, h.naastLopp)
		? 'lubatud'
		: sees(h.naastTalv, h.naastTalvLopp)
			? 'talveoludes'
			: 'keelatud';
	const talv = sees(h.kohustus, h.kohustusLopp) ? 'kohustuslik' : 'vabatahtlik';
	return { t, h, naast, talv, suvi: talv === 'kohustuslik' ? 'keelatud' : 'lubatud' };
}

const KUU = {
	et: ['jaanuar', 'veebruar', 'märts', 'aprill', 'mai', 'juuni', 'juuli', 'august', 'september', 'oktoober', 'november', 'detsember'],
	ru: ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
};
/* eesti käänded: g omastav (märtsi), st seestütlev (märtsist), ni rajav (märtsini), ks saav (märtsiks) */
const TYVI = ['jaanuari', 'veebruari', 'märtsi', 'aprilli', 'mai', 'juuni', 'juuli', 'augusti', 'septembri', 'oktoobri', 'novembri', 'detsembri'];
const LOPP = { g: '', st: 'st', ni: 'ni', ks: 'ks' };
/** „15. oktoober 2026“ / „15 октября 2026“. kaane: 'g' | 'st' | 'ni' | 'ks' (ainult eesti). ilmaAastata → „15. oktoobrist“. */
export function kp(d, lang = 'et', ilmaAastata = false, kaane = '') {
	const m = d.getMonth();
	const k = lang === 'ru' ? KUU.ru[m] : kaane && kaane in LOPP ? TYVI[m] + LOPP[kaane] : KUU.et[m];
	const s = lang === 'ru' ? `${d.getDate()} ${k}` : `${d.getDate()}. ${k}`;
	return ilmaAastata ? s : `${s} ${d.getFullYear()}`;
}
/** „15.10.2026“ */
export const kpl = (d) => `${d.getDate()}.${String(d.getMonth() + 1).padStart(2, '0')}.${d.getFullYear()}`;
