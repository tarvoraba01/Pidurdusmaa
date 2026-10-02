/* Partnerid (/teadmine/partnerid/) — ruudukesed logoga, klikk viib poodi
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

export const PARTNERID = [];
