/* Saidi seaded, mida võib vaja minna muuta. Kõik siin on AVALIK —
 * need väärtused on niikuinii iga lehe lähtekoodis näha. Salasõnu
 * (API võtmeid, paroole) siia EI panda.
 */

/** Saidi põhiaadress (canonical, sitemap). Ilma kaldkriipsuta lõpus. */
export const SAIT_URL = 'https://pidurdusmaa.ee';

/**
 * Google Analytics 4 mõõtmis-ID, kujul "G-XXXXXXXXXX".
 * Leiad: analytics.google.com → Admin → Data streams → sinu veebivoog.
 * Tühi = GA ei lae ja küpsiste riba ei näidata.
 */
export const GA4_ID = 'G-4P203ND0VV';

/**
 * Google Search Console'i kinnituskood (ainult HTML-sildi meetodi jaoks).
 * Search Console → Lisa atribuut → URL-i eesliide → HTML-silt → kopeeri
 * content="..." seest ainult kood. Kui kinnitad DNS-iga (soovitatav),
 * jäta tühjaks.
 */
export const GSC_VERIFY = '';
