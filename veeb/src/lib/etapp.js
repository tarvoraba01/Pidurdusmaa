/* „Päeva etapp“ (/liiklusohutus/etapp/): võidusõit aja peale, õpetlik.
 *
 *  - Rada on päeva järgi sama kõigile (seeme = päeva number): kurvid, ilm, öö/päev.
 *  - Takistused (põder, jäälaik, sügav lomp) tulevad teele JUHUSLIKUL hetkel, igal sõidul erinevalt.
 *  - Avarii või teelt väljasõit: alustad eelmisest kontrollpunktist, kell käib edasi.
 *  - Haare tuleb samast mootorist mis kalkulaatoris (engine.js): pidurdusjälje järgi
 *    aeglustus kiiruse kaupa; kurvis sama haare küljele (haardering: pidurdus + kurv).
 * Siin ainult puhtad funktsioonid (testitavad node'is); joonistamine $lib/tee3d.js, mäng Etapp.svelte.
 */
import { TEE } from './tee3d.js';

const { SEG, N, TEE_L } = TEE;
export const G = 9.80665;
export const ALGUS_Z = 30; /* stardijoon (m) */
export const PIKKUS = 1850; /* etapi pikkus stardist finišini (m) */
export const KP_VAHE = 370; /* kontrollpunktide vahe (m): 4 vahepunkti + finiš */

/* päeva number Tallinna aja järgi; nr 1 = 19.10.2026 */
export function paevaNr(d = new Date()) {
	const s = d.toLocaleDateString('en-CA', { timeZone: 'Europe/Tallinn' });
	return Math.max(1, Math.round((Date.parse(s + 'T00:00:00Z') - Date.parse('2026-10-19T00:00:00Z')) / 864e5) + 1);
}

function rng(seed) {
	let s = seed >>> 0 || 1;
	return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

/* päeva olud: tee kate, mootori tingimused, pilt (ilm tee3d jaoks), mis takistused sobivad */
export const OLUD = [
	{ id: 'kuiv', nimi: 'Kuiv asfalt', cond: { surface: 'ASPHALT', waterMm: 0, tempC: 14 }, ilm: 'kuiv', takistused: ['poder', 'poder', 'siga'] },
	{ id: 'vihm', nimi: 'Märg asfalt, sajab', cond: { surface: 'ASPHALT', waterMm: 1, tempC: 8 }, ilm: 'vihm', takistused: ['poder', 'lomp', 'lomp'] },
	{ id: 'kruus', nimi: 'Kruusatee', cond: { surface: 'GRAVEL', waterMm: 0, tempC: 10 }, ilm: 'kuiv', kate: 'kruus', takistused: ['poder', 'siga'] },
	{ id: 'lumi', nimi: 'Lumine tee, −5 °C', cond: { surface: 'SNOW_PACKED', waterMm: 0, tempC: -5 }, ilm: 'talv', takistused: ['poder', 'jaa', 'jaa'] },
	{ id: 'jaa', nimi: 'Lumi ja jäälaigud, −1 °C', cond: { surface: 'SNOW_PACKED', waterMm: 0, tempC: -1 }, ilm: 'talv', takistused: ['jaa', 'jaa', 'poder'] }
];
export const REHVID = [
	['SUMMER_TOURING', 'Suverehv'],
	['WINTER_NORDIC', 'Lamellrehv'],
	['WINTER_STUDDED', 'Naastrehv']
];

/* päeva rada: kurvid (raadius meetrites), sirged; algus ja lõpp sirged */
export function looEtapp(nr) {
	const r = rng(nr * 7919 + 13);
	const olud = OLUD[Math.floor(r() * OLUD.length)];
	const oo = r() < 0.3;
	const maastik = r() < 0.75 ? 'mets' : 'kula';
	const seg = [];
	const kurvid = [];
	const RAADIUS = [28, 40, 55, 70, 90, 120, 170, 250];
	let i = 0;
	const lisa = (k, n, ob) => { for (let j = 0; j < n && i < N; j++, i++) seg.push({ k, obj: [] }); };
	lisa(0, Math.round((ALGUS_Z + 60) / SEG));
	const lopp = Math.round((ALGUS_Z + PIKKUS) / SEG);
	while (i < lopp - 10) {
		if (r() < 0.35) { lisa(0, 6 + Math.floor(r() * 14)); continue; }
		const R = RAADIUS[Math.floor(r() * RAADIUS.length)];
		const suund = r() < 0.5 ? -1 : 1;
		const kaar = Math.max(8, Math.round((R * (0.6 + r() * 1.2)) / SEG)); /* 35..100° pööre */
		const n0 = i, sis = 4;
		for (let j = 0; j < kaar && i < lopp - 10; j++, i++) {
			const sujuv = Math.min(1, (j + 1) / sis, (kaar - j) / sis);
			seg.push({ k: (suund * SEG * SEG * sujuv) / R, obj: [] });
		}
		kurvid.push({ n0, n1: i, R, suund });
		lisa(0, 3 + Math.floor(r() * 5));
	}
	while (i < N) seg.push({ k: 0, obj: [] }), i++;

	/* teeäärne: mets või küla (sama stiil mis reaktsioonimängus), postid, kurvimärgid */
	for (let n = 0; n < N; n++) {
		const s = seg[n];
		if (n % 8 === 0) { s.obj.push({ t: 'post', x: -TEE_L - 1.2 }); s.obj.push({ t: 'post', x: TEE_L + 1.2 }); }
		for (const pool of [-1, 1]) {
			if (maastik === 'mets') {
				if (r() < 0.7) s.obj.push({ t: r() < 0.8 ? 'kuusk' : 'kask', x: pool * (TEE_L + 4 + r() * 14), h: 9 + r() * 9, v: r() });
				if (r() < 0.3) s.obj.push({ t: 'kuusk', x: pool * (TEE_L + 3.2 + r() * 3), h: 7 + r() * 6, v: r() });
			} else {
				if (n % 9 === 0 && r() < 0.7) s.obj.push({ t: 'maja', x: pool * (TEE_L + 10 + r() * 6), w: 8 + r() * 4, h: 5 + r() * 3, v: r(), aken: r() });
				if (n % 5 === 2 && r() < 0.6) s.obj.push({ t: r() < 0.5 ? 'kask' : 'poos', x: pool * (TEE_L + 4.5 + r() * 3), h: 4 + r() * 6, v: r() });
			}
		}
	}
	for (const k of kurvid) if (k.R <= 90 && k.n0 > 14) seg[k.n0 - 12].obj.push({ t: 'mark', x: TEE_L + 1.8, suund: k.suund });
	const nStart = Math.round(ALGUS_Z / SEG), nFin = Math.round((ALGUS_Z + PIKKUS) / SEG);
	seg[nStart].obj.push({ t: 'kaar', x: 0, tekst: 'START' });
	seg[nFin].obj.push({ t: 'kaar', x: 0, tekst: 'FINIŠ' });
	for (let k = 1; k * KP_VAHE < PIKKUS; k++) seg[Math.round((ALGUS_Z + k * KP_VAHE) / SEG)].obj.push({ t: 'kp', x: TEE_L + 1.6, nr: k });
	const tahed = Array.from({ length: 70 }, () => [r(), r() * 0.42, r()]);
	return { nr, olud, oo, kurvid, tee: { seg, maastik, tahed, seed: nr } };
}

/* tee kõverus (1/m, + = paremale) kohal z */
export function koverus(tee, z) {
	const n = Math.floor(z / SEG);
	return (tee.seg[((n % N) + N) % N].k || 0) / (SEG * SEG);
}

/* ---------- haare mootorist ----------
 * Pidurdusjäljest (kiirus teepikkuse kaupa) aeglustus kiiruse kaupa: a(v), m/s².
 * Sama mudel, mis annab kalkulaatori pidurdusmaa; ABS ja koormus on sees. */
export function rehv(kat, veh, gClass) {
	return { key: 'x', name: 'x', category: kat, wetGripIndex: gClass?.C?.[kat]?.[0] || 1.32, treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: kat === 'WINTER_STUDDED', size: veh.oemSize, gSource: 'label' };
}
export function haardeTabel(P, tyre, veh, cond) {
	const r = P.stoppingDistance(tyre, veh, { speedKmh: 160, texture: 'NORMAL', payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1, ...cond });
	const tr = r.trace || [];
	const tabel = new Array(51).fill(0);
	const lugeja = new Array(51).fill(0);
	for (let i = 1; i < tr.length; i++) {
		const v1 = tr[i - 1][1] / 3.6, v2 = tr[i][1] / 3.6, ds = tr[i][0] - tr[i - 1][0];
		if (ds <= 1e-6 || v1 > 160 / 3.6 - 2.5) continue; /* pidurite rakendumise algus välja */
		const a = (v1 * v1 - v2 * v2) / (2 * ds), b = Math.min(50, Math.round((v1 + v2) / 2));
		if (a > 0) { tabel[b] += a; lugeja[b]++; }
	}
	let viim = 0;
	for (let b = 0; b <= 50; b++) { if (lugeja[b]) tabel[b] /= lugeja[b]; }
	for (let b = 50; b >= 0; b--) { if (lugeja[b]) viim = tabel[b]; else tabel[b] = viim; }
	for (let b = 0; b <= 50; b++) if (!tabel[b]) tabel[b] = viim || 1;
	return { a: (v) => { const x = Math.max(0, Math.min(50, v)), i = Math.floor(x), f = x - i; return tabel[i] * (1 - f) + tabel[Math.min(50, i + 1)] * f; }, pidurdusmaa: (kmh) => P.stoppingDistance(tyre, veh, { speedKmh: Math.max(5, kmh), texture: 'NORMAL', payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1, ...cond }).distanceM };
}

/* kurvi piirkiirus (km/h): v² / R = a(v) */
export function piirkiirus(H, R) {
	let v = 20;
	for (let k = 0; k < 30; k++) v = Math.sqrt(H.a(v) * 1.05 * R);
	return v * 3.6;
}

/* ohutu kiirus nähtavusel d (m): 1 s reaktsioon + pidurdusmaa ≤ d */
export function ohutuKiirus(H, d) {
	let lo = 5, hi = 200;
	for (let k = 0; k < 25; k++) {
		const m = (lo + hi) / 2;
		if ((m / 3.6) * 1 + H.pidurdusmaa(m) <= d) lo = m; else hi = m;
	}
	return lo;
}

/* sõidufüüsika üks samm (dt s). o: { z, v, x, w, rool }, sisend: { gaas, pidur, roolSiht }
 * aKate(v) = haare praegusel pinnal. Tagastab sündmuse: null | 'teelt' | 'libiseb' */
export function samm(o, sis, dt, kov, aKate, maas) {
	o.rool += Math.max(-dt * 4, Math.min(dt * 4, sis.roolSiht - o.rool));
	const v = o.v;
	let aMax = aKate(v);
	if (maas) aMax *= 0.55; /* ratas teepervel / murul */
	/* pikisuund */
	const eng = Math.min(3.4, 78 / Math.max(1, v)); /* ~110 kW auto */
	const drive = sis.gaas ? Math.min(eng, aMax * 0.58) : 0; /* esivedu: veoteljel ~58% massist */
	const brake = sis.pidur ? aMax : 0;
	const takistus = 0.00028 * v * v + 0.12 + (maas ? 1.8 : 0);
	const ax = drive - brake - takistus;
	/* küljesuund: haardering. Vaja kurvi läbimiseks a = v²·κ; rool annab kuni allesjäänud haarde */
	const pikkKasutus = Math.max(drive, brake);
	const aLat = Math.sqrt(Math.max(0, (aMax * 1.05) ** 2 - pikkKasutus * pikkKasutus));
	const vaja = v * v * kov;
	const kask = o.rool * aLat;
	o.w += (kask - vaja - 1.6 * o.w) * dt;
	const wMax = 0.45 * v + 0.3;
	o.w = Math.max(-wMax, Math.min(wMax, o.w));
	o.x += o.w * dt;
	o.v = Math.max(0, v + ax * dt);
	if (o.v === 0) o.w *= 0.5;
	o.z += o.v * dt;
	o.libiseb = Math.abs(vaja) > aLat * 0.98 && v > 4;
	if (Math.abs(o.x) > TEE_L + 2.4) return 'teelt';
	return o.libiseb ? 'libiseb' : null;
}
