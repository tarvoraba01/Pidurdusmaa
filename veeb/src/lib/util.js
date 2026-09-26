/* Vormindus ja tabelid — töötavad nii ehituse ajal kui brauseris.
   Siin ei tohi olla ühtegi node:-importi, muidu ei saa neid komponendid
   kasutada. Failide lugemine on $lib/server/andmed.js sees. */

export const KAT_NIMI = {
	SUMMER_UHP: 'Suverehv (sportlik)',
	SUMMER_TOURING: 'Suverehv',
	ALL_SEASON: 'Aastaringne rehv',
	WINTER_CENTRAL: 'Talverehv (Kesk-Euroopa)',
	WINTER_NORDIC: 'Talverehv (Põhjamaade, naelutu)',
	WINTER_STUDDED: 'Naastrehv'
};
export const KAT_LYHI = {
	SUMMER_UHP: 'Suvi',
	SUMMER_TOURING: 'Suvi',
	ALL_SEASON: 'Aastaringne',
	WINTER_CENTRAL: 'Talv',
	WINTER_NORDIC: 'Talv (Põhjamaa)',
	WINTER_STUDDED: 'Naast'
};
export const EPREL_KAT = ['SUMMER_TOURING', 'ALL_SEASON', 'WINTER_CENTRAL', 'WINTER_NORDIC'];


/** EPREL-i nimed on sageli SUURTÄHTEDES. Ilusamaks, aga mudelikoodid jäävad. */
export function titleCase(s) {
	s = String(s || '');
	const min = /\p{Ll}/u.test(s) ? 4 : 3;
	const re = new RegExp(
		'(?<![\\p{L}\\d])(\\p{Lu})(\\p{Lu}{' + (min - 1) + ',})(?![\\p{L}\\d])',
		'gu'
	);
	return s.replace(re, (_m, a, b) => a + b.toLowerCase());
}

/** 20555R16 → 205/55 R16 */
export function pretty(m) {
	const x = /^(\d{3})(\d{2})R(\d{2})(C?)$/.exec(String(m || ''));
	return x ? `${x[1]}/${x[2]} R${x[3]}${x[4]}` : String(m || '');
}
/** 20555R16 → 205-55-r16 */
export function sizeSlug(m) {
	const x = /^(\d{3})(\d{2})R(\d{2})(C?)$/.exec(String(m || ''));
	return x ? `${x[1]}-${x[2]}-r${x[3]}${x[4] ? 'c' : ''}` : null;
}

/** Eesti arvuvorming: koma, mitte punkt. */
export function num(v, dec = 1) {
	return Number(v)
		.toFixed(dec)
		.replace('.', ',')
		.replace(/\B(?=(\d{3})+(?!\d))/, ' ');
}

/** +48 % või +5,8 % (alla 10 % ühe komakohaga). */
export function pct(val, base) {
	const v = (100 * (val - base)) / base;
	return (v >= 0 ? '+' : '') + num(v, Math.abs(v) < 10 ? 1 : 0) + ' %';
}

/** Mõõdetud testitulemuse inimloetav kirjeldus. */
export function testLabel(t) {
	const s =
		{
			ASPHALT: t.wet ? 'märg asfalt' : 'kuiv asfalt',
			CONCRETE: 'märg betoon',
			ICE: 'jää',
			SNOW_PACKED: 'lumi'
		}[t.surf] || String(t.surf).toLowerCase();
	return s + ', ' + Math.round(t.v0) + '→' + Math.round(t.v1) + ' km/h';
}


/** Rehvi valimise küsimused — sama nii /rehvi-valimine/ lehel kui avalehel. */
export const VALIK_Q = {
	drive: [
		'Kus sõidad kõige rohkem?',
		{ city: 'Linnas', road: 'Maanteel', hwy: 'Kiirteel', mix: 'Linn + maantee' }
	],
	km: [
		'Kui palju sõidad aastas?',
		{ lo: 'alla 10 000 km', mid: '10–20 000 km', hi: '20–30 000 km', vhi: 'üle 30 000 km' }
	],
	main: [
		'Mis on sulle kõige tähtsam? (kuni 3)',
		{
			safe: 'Ohutus märjal',
			brake: 'Lühike pidurdusmaa',
			price: 'Soodne hind',
			quiet: 'Vaikne sõit',
			fuel: 'Väike kütusekulu',
			winter: 'Talvised omadused'
		}
	],
	/* kolmas element = infomulli tekst */
	rft: [
		'Run-flat',
		{ only: 'Ainult run-flat', no: 'Ilma run-flatita' },
		'Run-flat (RFT) rehviga saab pärast torget või rõhu kadu edasi sõita, tavaliselt kuni 80 km kiirusega kuni 80 km/h — et jõuda remonti. Külgseinad on tugevdatud, sõit on veidi jäigem ja auto vajab rehvirõhu andurit. Levinud eriti BMW ja Mini autodel, kus varurehvi pole. Märjal ja lumel pidurdab ta sama moodi nagu tavaline sama mudeli rehv.'
	]
};

/** Teeolud — sama tabel oli PHP-s PM_CONDS ja on ka metoodika tekstis. */
export const CONDS = {
	wet: ['Märg', 'märg asfalt, veekiht 1 mm, +10 °C'],
	dry: ['Kuiv', 'kuiv asfalt, +15 °C'],
	snow: ['Lumi', 'tallatud lumi, −5 °C'],
	ice: ['Jää', 'jää, −5 °C']
};
