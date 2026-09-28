/* Partnerid (/teadmine/partnerid/) — ruudukesed logoga, klikk viib poodi
 * sinu partnerlingiga. Uue partneri lisamiseks lisa siia üks rida ja pane
 * logo kausta static/img/partnerid/ (logo annab partner ise).
 *
 * Awini partneri link:  awin(<poe mid>, 'https://www.pood.ee/')
 *   mid = poe (advertiser) number Awinis, AWIN_ID = sinu kirjastaja number.
 *   Mõlemad on avalikud (on igas lingis näha) — see EI ole salajane võti.
 *
 * Näide:
 * { nimi: 'ReifenDirekt.ee', kirjeldus: 'Rehvid ja veljed, kohaletoimetus Eestisse',
 *   link: awin(10747, 'https://www.reifendirekt.ee/'), logo: 'reifendirekt.svg' }
 */
export const AWIN_ID = ''; // sinu Awini kirjastaja ID (Publisher ID), nt '1234567'

export function awin(mid, url) {
	if (!AWIN_ID) return url;
	return 'https://www.awin1.com/cread.php?awinmid=' + mid + '&awinaffid=' + AWIN_ID + '&ued=' + encodeURIComponent(url);
}

export const PARTNERID = [];
