/* Vahemälu välistele API-dele.
 *
 * Miks: rehvipoe API-l on päringupiirang ja iga päring võtab aega.
 * Sama mõõdu hinnad küsitakse pakkujalt kord TTL-i jooksul, mitte iga
 * külastaja jaoks. Kui pakkuja on maas, antakse vana (aegunud) vastus
 * kuni 24 tundi, mitte tühi leht.
 *
 *  - üks päring korraga sama võtme kohta (10 külastajat = 1 päring pakkujale)
 *  - piiratud suurus: vanimad kirjed kukuvad välja
 */
const MAX = 3000;
const VANA_MAX_MS = 24 * 3600 * 1000;
const kirjed = new Map(); // voti -> { v, aegub, loodud }
const pooleli = new Map(); // voti -> Promise
export const stat = { tabamus: 0, moodas: 0, vanaVastus: 0, viga: 0 };

function pane(voti, v, ttlSek) {
	kirjed.delete(voti);
	kirjed.set(voti, { v, aegub: Date.now() + ttlSek * 1000, loodud: Date.now() });
	while (kirjed.size > MAX) kirjed.delete(kirjed.keys().next().value);
}

/**
 * @template T
 * @param {string} voti
 * @param {number} ttlSek
 * @param {() => Promise<T>} too  päris päring
 * @returns {Promise<T>}
 */
export async function vahemalus(voti, ttlSek, too) {
	const k = kirjed.get(voti);
	if (k && k.aegub > Date.now()) {
		stat.tabamus++;
		return k.v;
	}
	if (pooleli.has(voti)) return pooleli.get(voti);
	stat.moodas++;
	const p = (async () => {
		try {
			const v = await too();
			pane(voti, v, ttlSek);
			return v;
		} catch (e) {
			stat.viga++;
			if (k && Date.now() - k.loodud < VANA_MAX_MS) {
				stat.vanaVastus++;
				return k.v;
			}
			throw e;
		} finally {
			pooleli.delete(voti);
		}
	})();
	pooleli.set(voti, p);
	return p;
}

export const suurus = () => kirjed.size;
