/* Eesti rehvilehe keelevahetus ja hreflang peavad teadma, kas sellel lehel on vene versioon.
   Vene rehvilehtede nimekirja brauser eesti lehel ei lae (vt $lib/i18n.js laeRuRehvid):
   vastus tuleb lehe andmetest (+page.server.js `ru`). Universaalne load jookseb enne
   joonistamist nii serveris kui brauseris. */
import { ruRehvOlemas } from '$lib/i18n.js';

export function load({ data, params }) {
	if (data.ru) ruRehvOlemas(params.slug);
	return data;
}
