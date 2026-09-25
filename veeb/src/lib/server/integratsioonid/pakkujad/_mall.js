/* MALL UUELE PAKKUJALE — kopeeri see fail, nt `rehvipood.js`, ja lisa
 * see nimekirja failis ./index.js.
 *
 * Reeglid:
 *  1. Võti, parool ja API aadress tulevad AINULT muutuja()-st, mitte
 *     siia kirjutatuna. Muutuja pannakse Coolifys:
 *        PAKKUJA_REHVIPOOD_URL = https://api.rehvipood.ee/v1
 *        PAKKUJA_REHVIPOOD_VOTI = …
 *  2. Võti läheb PÄISESSE (Authorization / X-Api-Key), mitte URL-i —
 *     URL-id satuvad logidesse.
 *  3. hostid = ainult need aadressid, kuhu pakkuja kohta päringuid tohib
 *     teha (API ja piltide server). Muud aadressid blokeeritakse.
 *  4. Tagasta ainult need väljad, mis all kirjas. Lehele jõuavad ainult
 *     mark, mudel, mõõt, hind, laos, url ja pilt — mitte kogu vastus.
 *
 * Pärast lisamist: sea Coolifys muutujad → Redeploy → kontrolli
 *   curl -H "Authorization: Bearer $ADMIN_KEY" https://pidurdusmaa.ee/api/integratsioonid/olek
 */
export default {
	id: 'mall',
	nimi: 'Rehvipood (mall)',
	/* lubatud aadressid: API, pildid ja poe lingid */
	hostid: ['api.rehvipood.ee', 'pildid.rehvipood.ee'],
	poeHostid: ['www.rehvipood.ee'],
	/* sees ainult siis, kui KÕIK need muutujad on seatud */
	env: ['PAKKUJA_MALL_URL', 'PAKKUJA_MALL_VOTI'],
	/* hinnad vahemälus 1 tund, pildi URL 7 päeva */
	ttlHinnad: 3600,

	/**
	 * Kõik selle mõõdu rehvid pakkujalt.
	 * @param {string} moot  kujul 20555R16
	 * @param {{ muutuja: Function, jsonParing: Function }} ctx
	 * @returns {Promise<Array<{mark:string, mudel:string, moot:string, hind:number, laos?:boolean, url?:string, pilt?:string, ean?:string}>>}
	 */
	async hinnadMoodus(moot, { muutuja, jsonParing }) {
		const baas = muutuja('PAKKUJA_MALL_URL');
		const m = /^(\d{3})(\d{2})R(\d{2})/.exec(moot);
		const vastus = await jsonParing(
			this,
			`${baas}/tyres?width=${m[1]}&profile=${m[2]}&rim=${m[3]}`,
			{ headers: { Authorization: 'Bearer ' + muutuja('PAKKUJA_MALL_VOTI'), Accept: 'application/json' } }
		);
		/* teisenda pakkuja kuju meie kujule */
		return (vastus.items || []).map((x) => ({
			mark: x.brand,
			mudel: x.model,
			moot: `${x.width}/${x.profile} R${x.rim}`,
			hind: Number(x.price),
			laos: x.stock > 0,
			url: x.product_url,
			pilt: x.image_url,
			ean: x.ean
		}));
	}
};
