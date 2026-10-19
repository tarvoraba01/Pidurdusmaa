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

/* ---------- sõidufüüsika: ühe roopa mudel (bicycle model) ----------
 * Auto = kaks telge. Iga telje rehv annab külgjõu libisemisnurga järgi (Pacejka-laadne kõver,
 * tipp ~7°) kuni haardepiirini µ·Fz; pikijõud (vedu, pidur) ja külgjõud jagavad sama haaret
 * (haardering). Koormus kandub pidurdades ette, kiirendades taha. Mass, teljevahe ja
 * inertsimoment on VW Golf 8 lähedased. µ tuleb mootori pidurdusjäljest (ABS-iga aeglustus / 0,94).
 * Käsipidur lukustab tagarattad: tagatelg libiseb, haare mõjub libisemisele vastu → tagaots
 * tuleb välja (kässariga kurvi keeramine). ABS hoiab tavapidurdusel rattad veerevana.
 * Koordinaadid: x ette, y paremale; r > 0 = pöörab paremale; δ > 0 = rattad paremale.
 * Tee suhtes: s (z) mööda teed, x külgnihe (+ paremale), psi = auto nurk tee puutuja suhtes. */
const AUTO = { m: 1420, Iz: 2250, a: 1.03, b: 1.6, h: 0.55, P: 110000, Fveo: 5200, Fpidur: 16000, CdA: 0.66 };
export function uusAuto(z, x) {
	return { z, x, psi: 0, vx: 0, vy: 0, r: 0, delta: 0, v: 0, ax: 0, libiseb: false, kasi: false };
}
function pac(alfa) { /* normeeritud külgjõud 0..1 (B=11, C=1,35): tipp ~7°, edasi langeb veidi */
	return Math.sin(1.35 * Math.atan(11 * alfa));
}
export function samm(o, sis, dt, kov, mu0, maas) {
	const { m, Iz, a, b, h } = AUTO, L = a + b;
	const v = Math.hypot(o.vx, o.vy);
	let mu = mu0(v) / (G * 0.94); /* mootori aeglustus (m/s²) → haardetegur */
	if (maas) mu *= 0.5;
	/* rool: kiirusega väheneb maksimaalne rataste nurk (nagu päris roolil sõites väiksemad liigutused) */
	const dMax = 0.03 + 0.5 * (6 / (6 + v));
	const siht = sis.roolSiht * dMax;
	o.delta += Math.max(-1.2 * dt, Math.min(1.2 * dt, siht - o.delta));
	const d = o.delta;
	/* telgede koormus (pikikiirendusega ülekanne) */
	const Fzf = Math.max(0, (m * G * b - m * o.ax * h) / L), Fzr = Math.max(0, (m * G * a + m * o.ax * h) / L);
	/* pikijõud */
	const vxs = Math.max(0.5, Math.abs(o.vx));
	let Fxf = 0, Fxr = 0;
	if (sis.gaas && !sis.pidur) Fxf = Math.min(AUTO.Fveo, AUTO.P / vxs);
	if (sis.pidur && o.vx > 0.3) { Fxf -= AUTO.Fpidur * 0.7; Fxr -= AUTO.Fpidur * 0.3; }
	/* ABS: pidurijõud ei ületa haaret (ratas ei lukustu); vedu: ratas buksib, jõud piiratud */
	const maxF = mu * Fzf, maxR = mu * Fzr;
	/* veojõukontroll hoiab veoratta libisemise väikese (≤ 70% haardest), ABS pidurdusel kuni 95% */
	Fxf = Math.max(-0.95 * maxF, Math.min(0.7 * maxF, Fxf));
	Fxr = Math.max(-0.95 * maxR, Math.min(0.95 * maxR, Fxr));
	/* libisemisnurgad */
	const vxa = Math.max(1.5, o.vx);
	const af = Math.atan2(o.vy + a * o.r, vxa) - d;
	const ar = Math.atan2(o.vy - b * o.r, vxa);
	const latF = Math.sqrt(Math.max(0, maxF * maxF - Fxf * Fxf));
	let Fyf = -latF * pac(af);
	let FyrX = Fxr, Fyr;
	if (sis.kasi && o.vx > 0.5) {
		/* lukus tagarattad: libisemiskiirusele vastu, libisemishõõre ~0,8 µ */
		const vrx = o.vx, vry = o.vy - b * o.r, vr = Math.hypot(vrx, vry) || 1;
		FyrX = (-0.8 * maxR * vrx) / vr;
		Fyr = (-0.8 * maxR * vry) / vr;
	} else {
		const latR = Math.sqrt(Math.max(0, maxR * maxR - Fxr * Fxr));
		Fyr = -latR * pac(ar);
	}
	/* aeglasel kiirusel külgjõud sujuvalt maha (seisvat autot ei keera) */
	const madal = Math.min(1, v / 2);
	Fyf *= madal; Fyr *= madal;
	const takistus = 0.5 * 1.225 * AUTO.CdA * o.vx * Math.abs(o.vx) + m * G * (maas ? 0.08 : 0.012) * Math.sign(o.vx);
	const Fx = Fxf * Math.cos(d) - Fyf * Math.sin(d) + FyrX - takistus;
	const Fy = Fxf * Math.sin(d) + Fyf * Math.cos(d) + Fyr;
	const ax = Fx / m + o.vy * o.r, ay = Fy / m - o.vx * o.r;
	o.ax += (Fx / m - o.ax) * Math.min(1, dt * 8); /* koormuse ülekanne sumbub (vedrustus) */
	o.vx += ax * dt; o.vy += ay * dt;
	o.r += ((a * (Fxf * Math.sin(d) + Fyf * Math.cos(d)) - b * Fyr) / Iz) * dt;
	if (o.vx < 0.05 && !sis.gaas) { o.vx = Math.max(0, o.vx); if (o.vx === 0) { o.vy *= 0.8; o.r *= 0.8; } }
	if (v < 1.5 && !sis.kasi) { /* väga aeglaselt: kinemaatiline (rattad veerevad) */
		const k = 1 - v / 1.5;
		o.vy += (0 - o.vy) * k * 0.5;
		o.r += ((o.vx * Math.tan(d)) / L - o.r) * k * 0.5;
	}
	/* tee teljestikku */
	const sd = o.vx * Math.cos(o.psi) - o.vy * Math.sin(o.psi);
	o.z += sd * dt;
	o.x += (o.vx * Math.sin(o.psi) + o.vy * Math.cos(o.psi)) * dt;
	o.psi += (o.r - kov * sd) * dt;
	o.v = Math.hypot(o.vx, o.vy);
	o.libiseb = v > 5 && (Math.abs(af) > 0.13 || Math.abs(ar) > 0.11 || (sis.kasi && Math.abs(o.vy) > 1));
	if (Math.abs(o.x) > TEE_L + 2.4) return 'teelt';
	if (Math.abs(o.psi) > 2.4 && v < 3) return 'teelt'; /* ringi keeranud ja seisma jäänud */
	return o.libiseb ? 'libiseb' : null;
}
