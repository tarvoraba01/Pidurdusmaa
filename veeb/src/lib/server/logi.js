/* Logi (Supabase või failid) ja lihtne sagedusepiir.
 *
 * Kui Supabase on seadistatud (SUPABASE_URL + SUPABASE_SECRET_KEY, vt
 * supabase.js), lähevad read tabelitesse kasutuslogi ja kontakt. Read
 * kogutakse ~2 s kaupa kokku ja saadetakse ühe päringuga.
 * Kui Supabase'i pole või päring ebaõnnestub, kirjutatakse read nagu enne
 * JSONL-failidesse kausta LOG_DIR (vaikimisi ./data) — midagi ei kao.
 * Failidest saab need hiljem üle tõsta: node scripts/supabase-import.mjs.
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
import { sbSees, lisa as sbLisa, sb } from './supabase.js';

/* fail → Supabase'i tabel */
const TABELID = { 'logi.jsonl': 'kasutuslogi', 'kontakt.jsonl': 'kontakt' };

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
	if (TABELID[fail] && sbSees()) {
		jarjekorda(fail, obj);
		return true;
	}
	return lisaFaili(fail, obj);
}

function lisaFaili(fail, obj) {
	tagaKaust();
	try {
		appendFileSync(join(DIR, fail), JSON.stringify(obj) + '\n');
		return true;
	} catch {
		return false;
	}
}

/* ---- Supabase'i järjekord ----
   Read kogutakse mällu ja saadetakse 2 s pärast korraga. Kui saatmine
   ebaõnnestub, lähevad need read faili (sama mis enne Supabase'i). */
const jarjekord = new Map(); // fail -> [read]
const MAX_JARJEKORDA = 5000;
let taimer = null;
export const sbLogiOlek = { saadetud: 0, failiKirjutatud: 0, viga: null, vigaAeg: null };

function jarjekorda(fail, obj) {
	const l = jarjekord.get(fail) || [];
	l.push(obj);
	jarjekord.set(fail, l);
	/* liiga pikk järjekord (Supabase maas) → vanimad kohe faili */
	while (l.length > MAX_JARJEKORDA) {
		lisaFaili(fail, l.shift());
		sbLogiOlek.failiKirjutatud++;
	}
	if (!taimer) {
		taimer = setTimeout(saadaJarjekord, 2000);
		taimer.unref?.();
	}
}

export async function saadaJarjekord() {
	taimer = null;
	for (const [fail, read] of jarjekord) {
		if (!read.length) continue;
		const pakk = read.splice(0, read.length);
		try {
			await sbLisa(TABELID[fail], pakk.map((o) => vormista(fail, o)));
			sbLogiOlek.saadetud += pakk.length;
		} catch (e) {
			sbLogiOlek.viga = String(e.message || e).slice(0, 200);
			sbLogiOlek.vigaAeg = new Date().toISOString();
			for (const o of pakk) lisaFaili(fail, o);
			sbLogiOlek.failiKirjutatud += pakk.length;
		}
	}
}

/* JSONL rida → tabeli veerud (ainult teadaolevad väljad) */
function vormista(fail, o) {
	if (fail === 'logi.jsonl') return { t: o.t, k: o.k ?? null, s: Number(o.s) || 0, e: String(o.e), v: o.v ?? null };
	return { aeg: o.aeg || o.t, teema: o.teema ?? null, nimi: o.nimi ?? null, email: o.email ?? null, firma: o.firma ?? null, sonum: o.sonum ?? null };
}
export { vormista as _vormista };

/** Serveri sulgemisel (SIGTERM): saatmata read sünkroonselt faili, et midagi ei kaoks. */
export function tuhjendaFaili() {
	for (const [fail, read] of jarjekord) {
		while (read.length) lisaFaili(fail, read.shift());
	}
}

/** IP → lühike räsi päeva soolaga: sama masina read on seotud ainult ühe
 *  päeva piires (külastuse teekond), eri päevi siduda ei saa ja pärast
 *  päeva lõppu ei saa räsi enam kellegi IP-ga seostada. */
/** Külastaja IP. Server on Coolify proksi (Traefik) taga: ilma selleta näeks
 *  getClientAddress() kõigi päringute puhul proksi IP-d ja kõik piirangud
 *  oleksid ühised (audit 6.10). Proksi lisab X-Forwarded-For lõppu päris
 *  kliendi aadressi — võtame VIIMASE (eespool olevaid saab klient ise võltsida). */
export function kliendiIp(event) {
	try {
		const xff = event.request?.headers?.get('x-forwarded-for');
		if (xff) {
			const osad = xff.split(',').map((x) => x.trim()).filter(Boolean);
			if (osad.length) return osad[osad.length - 1];
		}
	} catch {}
	try {
		return event.getClientAddress();
	} catch {
		return 'tundmatu';
	}
}

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
	if (sbSees()) {
		sb('kontakt?aeg=lt.' + encodeURIComponent(new Date(piir).toISOString()), { method: 'DELETE', prefer: 'return=minimal' }).catch((e) =>
			console.log('Supabase: vanade kontaktikirjade kustutamine ebaõnnestus:', String(e.message || e).slice(0, 160))
		);
	}
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
