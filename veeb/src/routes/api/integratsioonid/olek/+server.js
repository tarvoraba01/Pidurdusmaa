/* GET /api/integratsioonid/olek — millised pakkujad on sees, mis puudu,
 * viimased vead. Ainult administraatorile:
 *   curl -H "Authorization: Bearer $ADMIN_KEY" https://pidurdusmaa.ee/api/integratsioonid/olek
 * Kui ADMIN_KEY pole seatud (või on alla 16 märgi), on otspunkt suletud. */
import { piirang, vastus, liigaPalju, keelatud, votiOnOige } from '$lib/server/integratsioonid/kaitse.js';
import { adminVoti } from '$lib/server/integratsioonid/seaded.js';
import { olekKoond } from '$lib/server/integratsioonid/koond.js';

export const prerender = false;
/* API aadressid töötavad nii kaldkriipsuga kui ilma (lehtedel on alati kaldkriips) */
export const trailingSlash = 'ignore';

export function GET(event) {
	if (!piirang('olek', event, 20, 60)) return liigaPalju();
	if (!votiOnOige(event.request, adminVoti())) return keelatud();
	return vastus(olekKoond());
}
