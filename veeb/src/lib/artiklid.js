/* Artiklid (/teadmine/artiklid/) — uusim esimesena.
 * Uue artikli lisamine: tee kaust src/routes/teadmine/artiklid/<slug>/
 * (vt talverehvi-valimine) ja lisa siia üks rida. Sitemap, artiklite
 * leht ja Teadmine leht loevad nimekirja siit. */
export const ARTIKLID = [
	{
		slug: 'talverehvide-testid-2026',
		title: 'Talverehvide testid 2025–2026: mida mõõtmised näitavad',
		desc: 'Jääl üle kahe korra pikem pidurdusmaa, märjal 15 meetrit vahet, lumel alla meetri. Viimaste talverehvitestide mõõdetud pidurdusmaad ühest kohast.',
		kuupaev: '2026-09-30',
		silt: 'Testid'
	},
	{
		slug: 'peatumisteekonna-kalkulaator',
		title: 'Uus tasuta kalkulaator: kui pika maa pealt auto peatub?',
		desc: 'Muuda kiirust, reaktsiooniaega, teeolusid ja rehve ning vaata kohe, kuidas peatumisteekond muutub. Kaks olukorda kõrvuti — tasuta ja ilma reklaamita.',
		kuupaev: '2026-09-29',
		silt: 'Tööriist'
	},
	{
		slug: 'talverehvi-valimine',
		title: 'Talverehvi valimine: mida numbrid ütlevad',
		desc: 'Suverehv lumel, Põhjamaade vs Kesk-Euroopa talverehv, naast vs lamell, mustri sügavus ja millal vahetada — pidurdusmaad meetrites.',
		kuupaev: '2026-09-26',
		silt: 'Talverehvid'
	}
];

export const artikliTee = (a) => '/teadmine/artiklid/' + a.slug + '/';

/** 2026-09-26 → 26.09.2026 */
export const kuup = (iso) => iso.split('-').reverse().join('.');
