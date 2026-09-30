/* Failipõhine logi ja lihtne sagedusepiir.
 *
 * Andmebaasi siin ei ole: ridu kirjutatakse JSONL-failidesse kausta,
 * mille annab LOG_DIR (vaikimisi ./data). Docker'is peab see olema
 * volume, muidu kaob sisu uue versiooniga.
 *
 * Kasutuslogis (logi.jsonl) IP-d ei ole: ainult räsi päeva soolaga, mida
 * pärast päeva lõppu enam ei ole -- anonüümne, hoitakse tähtajatult.
 * kontakt.jsonl sisaldab kontaktivormi kirju (nimi, e-post, sõnum) -- need
 * on isikuandmed ja kustutatakse 12 kuu pärast (kustutaVanad).
 * Vt privaatsusteade /privaatsus/.
 */
import { appendFileSync, mkdirSync, readFileSync, writeFileSync, renameSync } from 'node:fs';
import { join } from 'node:path';
import { createHash, randomBytes } from 'node:crypto';

const DIR = process.env.LOG_DIR || join(process.cwd(), 'data');
/* Päeva sool: juhuslik, ainult mälus, vahetub UTC keskööl. Eilset soola ei
   hoita kuskil alles, nii et pärast päeva lõppu ei saa ka meie ise ühtki
   logirida IP-aadressiga seostada -- read on anonüümsed ja neid võib hoida
   aastaid (pikaajaline statistika). */
let paevaSool = '';
let soolaPaev = '';
function sool() {
	const paev = new Date().toISOString().slice(0, 10);
	if (paev !== soolaPaev) {
		soolaPaev = paev;
		paevaSool = randomBytes(16).toString('hex');
	}
	return paevaSool;
}

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

/** IP → lühike räsi päeva soolaga: sama masina read on seotud ainult ühe
 *  päeva piires (külastuse teekond), eri päevi siduda ei saa ja pärast
 *  päeva lõppu ei saa räsi enam kellegi IP-ga seostada. */
export function ipHash(ip) {
	return createHash('sha256').update(sool() + '|' + String(ip)).digest('hex').slice(0, 16);
}

/* Säilitamine: kontaktivormi kirjad (isikuandmed) kuni 12 kuud. Vanemad
   read kustutatakse serveri käivitumisel ja siis kord ööpäevas
   (hooks.server.js). Anonüümset kasutuslogi (logi.jsonl) hoitakse
   tähtajatult. Kõik on sünkroonne, nii et samal ajal lisatud rida kaotsi
   ei lähe. */
export const HOIA_PAEVI = 365;
export function kustutaVanad(paevi = HOIA_PAEVI) {
	const piir = Date.now() - paevi * 864e5;
	for (const fail of ['kontakt.jsonl']) {
		const tee = join(DIR, fail);
		let read;
		try {
			read = readFileSync(tee, 'utf-8').split('\n').filter(Boolean);
		} catch {
			continue;
		}
		const alles = read.filter((r) => {
			try {
				const o = JSON.parse(r);
				const t = Date.parse(o.t || o.aeg);
				return !(t < piir);
			} catch {
				return false;
			}
		});
		if (alles.length === read.length) continue;
		try {
			writeFileSync(tee + '.tmp', alles.length ? alles.join('\n') + '\n' : '');
			renameSync(tee + '.tmp', tee);
		} catch {
			/* kirjutamisõigust ei ole — proovime järgmisel korral */
		}
	}
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
