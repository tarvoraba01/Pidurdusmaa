/* Partnerid (/teadmine/partnerid/) — logoseinal, klikk viib poodi.
 * ryhm: 'pood' = hinnad rehvikaartidel (ülemine rida), 'muu' = teised partnerid.
 * sinu partnerlingiga. Uue partneri lisamiseks lisa siia üks rida ja pane
 * logo kausta static/img/partnerid/ (logo annab partner ise).
 *
 * Awini partneri link:  awin(<poe mid>, 'https://www.pood.ee/')
 *   mid = poe (advertiser) number Awinis, AWIN_ID = sinu kirjastaja number.
 *   Mõlemad on avalikud (on igas lingis näha) — see EI ole salajane võti.
 *
 * Otse (ilma Awinita) partner: link: utm('https://www.pood.ee/')
 *
 * Näide:
 * { nimi: 'ReifenDirekt.ee', kirjeldus: 'Rehvid ja veljed, kohaletoimetus Eestisse',
 *   link: awin(10747, 'https://www.reifendirekt.ee/'), logo: 'reifendirekt.svg' }
 */
export const AWIN_ID = ''; // sinu Awini kirjastaja ID (Publisher ID), nt '1234567'

/* Otselink partnerile koos UTM-iga, et partner näeks oma statistikas Pidurdusmaast tulnud külastajaid. */
export function utm(url, koht = 'partnerid') {
	try {
		const u = new URL(url);
		u.searchParams.set('utm_source', 'pidurdusmaa');
		u.searchParams.set('utm_medium', 'referral');
		u.searchParams.set('utm_campaign', koht);
		return u.toString();
	} catch {
		return url;
	}
}

export function awin(mid, url) {
	if (!AWIN_ID) return url;
	return 'https://www.awin1.com/cread.php?awinmid=' + mid + '&awinaffid=' + AWIN_ID + '&ued=' + encodeURIComponent(url);
}

export const PARTNERID = [
	{ nimi: 'Rehvivahetus.ee', link: utm('https://www.rehvivahetus.ee/'), logo: 'rehvivahetus.svg',
		kirjeldus: 'Rehvid, veljed ja rehvivahetus üle 30 aasta.', ryhm: 'pood' },
	{ nimi: 'Tirespot.ee', link: utm('https://www.tirespot.ee/'), logo: 'tirespot.svg',
		kirjeldus: 'Rehvipood, rehvivahetus ja autoremont Pärnus.', ryhm: 'pood' },
	/* logo puudub veel (intercars24.ee on Cloudflare'i taga) — ruudus on nimi; lisa logo: static/img/partnerid/intercars.svg ja logo: 'intercars.svg' */
	{ nimi: 'Inter Cars', link: utm('https://www.intercars24.ee/'), logo: 'intercars.png', logoMaxH: 50, /* PNG on 142×50 — suurem oleks udune; SVG puudub */
		kirjeldus: 'Autovaruosad ja rehvid üle Eesti.', ryhm: 'pood' },
	{ nimi: 'Dignicy', link: utm('https://dignicy.ee/'), logo: 'dignicy.svg',
		kirjeldus: 'Veebilehed, e-poed ja tehisaru lahendused. Meie arenduspartner.', ryhm: 'muu' },
	/* videote eestikeelne hääl; tasuta, mitte partnerlink (TartuNLP luba 12.10.2026) */
	{ nimi: 'Neurokõne (TartuNLP)', link: 'https://neurokone.ee/', logo: 'neurokone.svg', tasuta: true,
		kirjeldus: 'Tartu Ülikooli eestikeelne kõnesüntees. Meie videote hääl.', ryhm: 'muu' }
];
