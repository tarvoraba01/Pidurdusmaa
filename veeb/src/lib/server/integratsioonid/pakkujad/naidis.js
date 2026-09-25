/* NÄIDISPAKKUJA — testimiseks ja arenduseks. Loeb hinnad kohalikust
 * JSON-failist, mitte internetist. Sees AINULT siis, kui on seatud
 *   PAKKUJA_NAIDIS_FAIL = /tee/naidis-hinnad.json
 * Live-lehel ära seda sea: need on väljamõeldud hinnad.
 *
 * Faili kuju: { "tooted": [ { "mark", "mudel", "moot", "hind", "laos", "url", "pilt" } ] }
 */
import { readFileSync } from 'node:fs';

export default {
	id: 'naidis',
	nimi: 'Näidispood (TEST)',
	hostid: ['127.0.0.1:4599', 'localhost:4599'],
	poeHostid: ['naidispood.invalid'],
	lubaHttp: true,
	env: ['PAKKUJA_NAIDIS_FAIL'],
	ttlHinnad: 60,
	async hinnadMoodus(moot, { muutuja }) {
		const d = JSON.parse(readFileSync(muutuja('PAKKUJA_NAIDIS_FAIL'), 'utf-8'));
		return (d.tooted || []).filter((t) => t.moot && t.moot.replace(/[^0-9RC]/gi, '').toUpperCase() === moot);
	}
};
