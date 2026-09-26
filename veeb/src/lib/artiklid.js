/* Artiklid (/teadmine/artiklid/) — uusim esimesena.
 * Uue artikli lisamine: tee kaust src/routes/teadmine/artiklid/<slug>/
 * (vt talverehvi-valimine) ja lisa siia üks rida. Sitemap, artiklite
 * leht ja Teadmine leht loevad nimekirja siit. */
export const ARTIKLID = [
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
