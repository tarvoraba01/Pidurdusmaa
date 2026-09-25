/* Failipõhine logi ja lihtne sagedusepiir.
 *
 * Andmebaasi siin ei ole: ridu kirjutatakse JSONL-failidesse kausta,
 * mille annab LOG_DIR (vaikimisi ./data). Docker'is peab see olema
 * volume, muidu kaob sisu uue versiooniga.
 *
 * Isikuandmeid ei salvestata: IP-st hoitakse ainult soolatud räsi ja
 * sedagi ainult selleks, et üks masin ei saaks vormi tuhat korda täita.
 */
import { appendFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { createHash, randomBytes } from 'node:crypto';

const DIR = process.env.LOG_DIR || join(process.cwd(), 'data');
const SOOL = process.env.IP_SALT || randomBytes(16).toString('hex');

let valmis = false;
function tagaKaust() {
	if (valmis) return;
	try {
		mkdirSync(DIR, { recursive: true });
		valmis = true;
	} catch {
		/* kirjutamisõigust ei ole — logi jääb vahele, leht töötab edasi */
	}
}

export function lisaRida(fail, obj) {
	tagaKaust();
	try {
		appendFileSync(join(DIR, fail), JSON.stringify(obj) + '\n');
		return true;
	} catch {
		return false;
	}
}

/** IP → lühike räsi. Soolaga, nii et tagasi arvutada ei saa. */
export function ipHash(ip) {
	return createHash('sha256').update(SOOL + '|' + String(ip)).digest('hex').slice(0, 16);
}

/* Sagedusepiir mälus: lihtne ja piisav ühe protsessi kohta. Piiratud
   suurusega: kui kirjeid on liiga palju, kukuvad VANIMAD välja (varem
   tühjendati kogu tabel — siis sai piirangu paljude IP-dega nullida). */
const loendur = new Map();
const MAX_KIRJEID = 20000;
export function kasLubatud(voti, mitu, sekundit) {
	const nyyd = Date.now();
	let kirje = loendur.get(voti);
	if (!kirje || nyyd - kirje.algus > sekundit * 1000) kirje = { algus: nyyd, n: 0 };
	kirje.n += 1;
	loendur.delete(voti);
	loendur.set(voti, kirje);
	while (loendur.size > MAX_KIRJEID) loendur.delete(loendur.keys().next().value);
	return kirje.n <= mitu;
}
