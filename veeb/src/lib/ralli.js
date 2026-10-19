/* Päeva etapp v2: rada ja sõidumudel (puhtad funktsioonid, testitavad node'is).
 * Joonistamine: $lib/ralli3d.js (three.js), mäng: $lib/Etapp.svelte.
 *
 * Juhtimine on arkaadlik, nagu rallimängudes (rally52 jt): auto keerab sinna, kuhu rooli keerad,
 * piisava kiirusega kurvis läheb tagaots välja ja auto driftib. Gaas hoiab drifti, gaasi
 * vabastamine keerab nina rohkem sisse, vasturool toob sirgeks. Pidurdus kurvis viskab
 * tagaotsa välja, käsipidur veel rohkem.
 * Pidurdusjõud tuleb samast mootorist mis kalkulaatoris (kruus, ABS): see on õpetlik osa.
 *
 * Koordinaadid (three.js): x, z maas, y üles. Suund h: ettepoole vektor (sin h, cos h).
 * Paremale pööramine vähendab h-d. Roolisisend +1 = paremale.
 */
export const G = 9.80665;
export const ALGUS = 40; /* stardijoon (m raja algusest) */
export const PIKKUS = 1850; /* stardist finišini (m) */
export const KP_VAHE = 370; /* kontrollpunktid iga 370 m (4 tk + finiš) */
export const POOL = 4.6; /* tee poollaius (m) */
export const SEG = 5; /* kaardilugeja lõik (m) */
export const DS = 2.5; /* keskjoone punktide vahe (m) */

/* päeva number Tallinna aja järgi; nr 1 = 19.10.2026 */
export function paevaNr(d = new Date()) {
	const s = d.toLocaleDateString('en-CA', { timeZone: 'Europe/Tallinn' });
	return Math.max(1, Math.round((Date.parse(s + 'T00:00:00Z') - Date.parse('2026-10-19T00:00:00Z')) / 864e5) + 1);
}
export function rng(seed) {
	let s = seed >>> 0 || 1;
	return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

/* ---------- rada ---------- */
const RAADIUS = [26, 34, 45, 60, 80, 110, 160, 240];
function looKurvid(r) {
	const k = []; /* kõverus lõigu kaupa (1/m, + = paremale) */
	const kurvid = [];
	const lisa = (x, n) => { for (let j = 0; j < n; j++) k.push(x); };
	lisa(0, Math.round((ALGUS + 50) / SEG));
	const lopp = Math.round((ALGUS + PIKKUS) / SEG);
	let eelmSuund = 0;
	while (k.length < lopp - 8) {
		if (r() < 0.3) { lisa(0, 5 + Math.floor(r() * 14)); continue; }
		const R = RAADIUS[Math.floor(r() * RAADIUS.length)];
		/* vahelduv suund on rallis tavaline (vasak-parem kombinatsioonid) */
		const suund = eelmSuund && r() < 0.62 ? -eelmSuund : r() < 0.5 ? -1 : 1;
		eelmSuund = suund;
		const nurk = (35 + r() * 75) * (Math.PI / 180);
		const n = Math.max(6, Math.round((R * nurk) / SEG));
		const n0 = k.length, sis = 3;
		for (let j = 0; j < n; j++) k.push((suund * Math.min(1, (j + 1) / sis, (n - j) / sis)) / R);
		kurvid.push({ n0, n1: k.length, R, suund, aste: R < 30 ? 1 : R < 40 ? 2 : R < 55 ? 3 : R < 75 ? 4 : R < 120 ? 5 : 6 });
		if (r() < 0.55) lisa(0, 2 + Math.floor(r() * 6));
	}
	lisa(0, Math.round(160 / SEG)); /* finiši järel pidurdusala */
	return { k, kurvid };
}
function keskjoon(k, r) {
	const n = k.length * (SEG / DS) + 1;
	const x = new Float64Array(n), z = new Float64Array(n), y = new Float64Array(n), h = new Float64Array(n);
	/* kõrgus: sujuvad künkad (kalle alla ~6%) */
	const lained = [[330, 7], [170, 3], [75, 0.9]].map(([l, a]) => [l, a * (0.6 + r() * 0.6), r() * 6.283]);
	let px = 0, pz = 0, ph = 0;
	for (let i = 0; i < n; i++) {
		x[i] = px; z[i] = pz; h[i] = ph;
		const s = i * DS;
		y[i] = lained.reduce((t, [l, a, f]) => t + a * Math.sin((s / l) * 6.283 + f), 0) * Math.min(1, s / 120);
		const kap = k[Math.min(k.length - 1, Math.floor(s / SEG))] || 0;
		ph -= kap * DS;
		px += Math.sin(ph) * DS; pz += Math.cos(ph) * DS;
	}
	return { x, z, y, h, n };
}
/* tee ei tohi iseennast ristuda ega liiga lähedalt mööda minna */
function ristub(c) {
	const rakk = 30, m = new Map();
	for (let i = 0; i < c.n; i += 2) {
		const key = Math.floor(c.x[i] / rakk) + ',' + Math.floor(c.z[i] / rakk);
		(m.get(key) || m.set(key, []).get(key)).push(i);
	}
	for (let i = 0; i < c.n; i += 2) {
		const cx = Math.floor(c.x[i] / rakk), cz = Math.floor(c.z[i] / rakk);
		for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) {
			for (const j of m.get(cx + a + ',' + (cz + b)) || []) {
				if (Math.abs(i - j) < 60) continue;
				if (Math.hypot(c.x[i] - c.x[j], c.z[i] - c.z[j]) < 46) return true;
			}
		}
	}
	return false;
}
export function looRada(nr) {
	for (let katse = 0; katse < 60; katse++) {
		const r = rng(nr * 7919 + 13 + katse * 104729);
		const { k, kurvid } = looKurvid(r);
		const c = keskjoon(k, r);
		if (katse < 59 && ristub(c)) continue;
		return { nr, k, kurvid, ...c, pikkus: (c.n - 1) * DS, seeme: nr * 31 + katse };
	}
}

/* lähim keskjoone punkt (otsib eelmise ümbrusest) → { i, s, d } ; d > 0 = paremal */
export function asukoht(rada, x, z, i0 = 0) {
	const a = Math.max(0, i0 - 40), b = Math.min(rada.n - 1, i0 + 40);
	let parim = i0, pd = Infinity;
	for (let i = a; i <= b; i++) {
		const dd = (rada.x[i] - x) ** 2 + (rada.z[i] - z) ** 2;
		if (dd < pd) { pd = dd; parim = i; }
	}
	const h = rada.h[parim], fx = Math.sin(h), fz = Math.cos(h);
	const ex = x - rada.x[parim], ez = z - rada.z[parim];
	const pikk = ex * fx + ez * fz;
	const d = ex * -fz + ez * fx; /* parem = (-cos h, sin h) */
	return { i: parim, s: parim * DS + pikk, d };
}
/* maastiku profiil tee teljest kaugusel d (m): tee, peenar, kraav, nõlv */
export function profiil(d) {
	const a = Math.abs(d);
	if (a <= POOL) return 0.06 * (1 - (a / POOL) ** 2); /* kumer tee */
	if (a <= POOL + 1.4) return -((a - POOL) / 1.4) * 0.15;
	if (a <= POOL + 3.2) return -0.15 - Math.sin(((a - POOL - 1.4) / 1.8) * Math.PI) * 0.55;
	return -0.15 + Math.min(4, (a - POOL - 3.2) * 0.14);
}
export function korgus(rada, i, d, s) {
	const j = Math.max(0, Math.min(rada.n - 2, Math.floor(s / DS)));
	const f = Math.max(0, Math.min(1, s / DS - j));
	return rada.y[j] * (1 - f) + rada.y[j + 1] * f + profiil(d);
}

/* kurvi piirkiirus (km/h) kruusal: v²/R = a(v) */
export function piirkiirus(aFn, R) {
	let v = 20;
	for (let k = 0; k < 30; k++) v = Math.sqrt(aFn(v) * 1.05 * R);
	return v * 3.6;
}

/* ---------- auto ---------- */
const L = 2.6;
/* häälestus (vt testid) */
export const K = { esi: 1.6, kickEsi: 2.2, kasiEsi: 2.2, stabGaas: 1.1, stabLahti: 0.75, stabKasi: 0.15, kickStab: 0.8, tagaGaas: 0.82, tagaKasi: 0.4, kickTaga: 0.45, suun: 0.2, kraap: 0.5, lin: 7 };
export function uusAuto(rada, s) {
	const i = Math.max(0, Math.min(rada.n - 1, Math.round(s / DS)));
	return { x: rada.x[i], z: rada.z[i], y: rada.y[i], h: rada.h[i], vx: 0, vz: 0, w: 0, rool: 0, i, s: i * DS, d: 0,
		v: 0, vF: 0, libis: 0, kaik: 1, prr: 900, kick: 0, maas: 0, along: 0, alat: 0, ratas: 0, pidur: false };
}

/* üks samm. sis: { gaas, pidur, kasi, rool (-1..1) }, aFn(v): mootori aeglustus kruusal (m/s²).
   Tagastab 'puu' | 'kaugel' | null */
export function samm(o, sis, dt, aFn, rada, puud) {
	const fx = Math.sin(o.h), fz = Math.cos(o.h), rx = -fz, rz = fx;
	let vF = o.vx * fx + o.vz * fz, vR = o.vx * rx + o.vz * rz;
	const v = Math.hypot(vF, vR);
	const pos = asukoht(rada, o.x, o.z, o.i);
	o.i = pos.i; o.s = pos.s; o.d = pos.d;
	const a = Math.abs(pos.d);
	o.maas = a <= POOL + 0.4 ? 0 : a <= POOL + 1.5 ? 1 : 2;
	/* haare: mootori pidurdus kruusal (ABS) ≈ µg; mängus veidi rohkem, et oleks lõbus */
	const mu = aFn(Math.min(50, v)) / 0.94 / G;
	const pind = o.maas === 0 ? 1 : o.maas === 1 ? 0.85 : 0.6;
	const aMax = mu * G * pind * 1.12;

	/* rool: sujuv (klahv ei ole kohe täis), suurel kiirusel väiksem rataste nurk */
	const roolSiht = Math.max(-1, Math.min(1, sis.rool));
	const kiirus = roolSiht === 0 || Math.sign(roolSiht) !== Math.sign(o.rool) ? 7 : 3.2;
	o.rool += Math.max(-kiirus * dt, Math.min(kiirus * dt, roolSiht - o.rool));
	const delta = o.rool * (0.6 / (1 + Math.max(0, v - 3) / 11));

	/* pidur kurvis: koormus ette, tagaots kergeks (lühike „kick“) */
	if (sis.pidur && vF > 6 && Math.abs(o.rool) > 0.3) o.kick = Math.min(0.6, o.kick + dt * 3);
	else o.kick = Math.max(0, o.kick - dt * 1.5);

	const libis = v > 2 ? Math.atan2(vR, Math.abs(vF)) : 0; /* + = libiseb paremale */
	o.libis = libis;
	/* pöörlemine: rataste järgi + tagaotsa stabiilsus (nina pöörab sõidusuuna poole) */
	const wKin = (vF * Math.tan(delta)) / L; /* + = paremale */
	const esiPiir = (aMax * (K.esi + o.kick * K.kickEsi + (sis.kasi ? K.kasiEsi : 0))) / Math.max(4, v);
	let wSiht = Math.max(-esiPiir, Math.min(esiPiir, wKin));
	let stab = sis.kasi ? K.stabKasi : sis.gaas ? K.stabGaas : K.stabLahti; /* gaas hoiab drifti, gaasi vabastus keerab sisse */
	stab *= 1 - o.kick * K.kickStab;
	if (v > 2) wSiht += stab * Math.sin(libis) * Math.min(1, v / 8) * (vF < 0 ? -1 : 1);
	o.w += (wSiht - o.w) * Math.min(1, dt * 6);
	o.h -= o.w * dt;

	/* külghaare: libisemine sumbub, kuid mitte kiiremini kui haare lubab */
	const tagaPiir = aMax * (sis.kasi ? K.tagaKasi : sis.gaas ? K.tagaGaas : 1) * (1 - o.kick * K.kickTaga);
	const dvR = Math.min(Math.abs(vR) * K.lin, tagaPiir) * dt;
	const vR2 = Math.abs(vR) <= dvR ? 0 : vR - Math.sign(vR) * dvR;
	/* osa külgkiirusest pöördub driftis edasiliikumiseks (arkaadlik, hoiab hoogu) */
	vF += Math.sign(vF || 1) * Math.abs(vR - vR2) * K.suun;
	vR = vR2;

	/* pikisuund: mootor, pidur, takistus */
	const vfa = Math.abs(vF);
	let ax = 0;
	/* haardering: kurvis kulub haare küljele, kiirenduseks jääb vähem */
	const kulu = Math.min(1, Math.abs(vF * o.w) / aMax);
	if (sis.gaas && vF > -0.5) ax += Math.min(mu * G * 0.95 * pind, 150 / Math.max(4, vfa)) * (o.maas === 2 ? 0.7 : 1) * (0.25 + 0.75 * Math.sqrt(1 - kulu * kulu));
	if (sis.pidur) {
		if (vF > 0.5) ax -= Math.min(aFn(Math.min(50, vF)) * pind, mu * G * pind);
		else if (!sis.gaas) ax -= 3.2; /* tagurpidi */
	}
	if (sis.kasi && vF > 0.5) ax -= mu * G * 0.35;
	const takistus = 0.0016 * vF * vfa + Math.sign(vF) * (0.25 + (o.maas === 1 ? 1 : o.maas === 2 ? 2.4 : 0)) + vF * Math.abs(Math.sin(libis)) * K.kraap;
	if (vfa < 0.3 && !sis.gaas && !(sis.pidur && vF <= 0.5)) vF = 0;
	else vF += (ax - takistus) * dt;
	if (vF < -5) vF = -5;

	/* tagasi maailma */
	/* kiirus jääb maailma teljestikku (vana suuna järgi): kere pööre tekitab järgmisel sammul libisemise */
	o.vx = fx * vF + rx * vR; o.vz = fz * vF + rz * vR;
	o.x += o.vx * dt; o.z += o.vz * dt;
	o.y = korgus(rada, o.i, o.d, o.s);
	o.along += ((ax - takistus) - o.along) * Math.min(1, dt * 5);
	o.alat += (vF * o.w - o.alat) * Math.min(1, dt * 5);
	o.v = Math.hypot(vF, vR); o.vF = vF; o.pidur = !!sis.pidur;
	o.ratas += (vF / 0.33) * dt;
	/* käik ja pöörded (heli ja näidik): 6 käiku */
	const kaigud = [0, 13, 21, 29, 36, 43, 99];
	let k = 1; while (k < 6 && vfa > kaigud[k] * 1.0) k++;
	o.kaik = vF < -0.3 ? -1 : k;
	const lo = kaigud[k - 1], hi = kaigud[k] > 90 ? 50 : kaigud[k];
	const prrSiht = 1000 + Math.min(1, (vfa - lo) / Math.max(1, hi - lo)) * 6200 + (sis.gaas && Math.abs(libis) > 0.25 ? 900 : 0);
	o.prr += ((sis.gaas || vfa > 1 ? Math.max(1800, prrSiht) : 900) - o.prr) * Math.min(1, dt * 8);

	/* kokkupõrked: puud (ring), kaugel teest */
	if (puud) {
		const lahim = puud(o.x, o.z);
		const kaug = lahim ? Math.hypot(lahim[0] - o.x, lahim[1] - o.z) : 99;
		if (lahim && kaug < lahim[2] + 1.1) {
			if (lahim[3] !== 'pall') return 'puu';
			/* heinapall: pehme. Pallide suunaline kiirus kaob, muu kiirus väheneb, auto lükatakse välja */
			const nx = (o.x - lahim[0]) / (kaug || 1), nz = (o.z - lahim[1]) / (kaug || 1);
			const vn = o.vx * nx + o.vz * nz;
			if (vn < 0) { o.vx -= 1.2 * vn * nx; o.vz -= 1.2 * vn * nz; }
			o.vx *= 0.93; o.vz *= 0.93; o.w *= 0.9;
			o.x = lahim[0] + nx * (lahim[2] + 1.1); o.z = lahim[1] + nz * (lahim[2] + 1.1);
			return 'pall';
		}
	}
	if (a > 22) return 'kaugel';
	return null;
}

/* kaardilugeja: järgmine kurv ees */
export function noot(rada, s) {
	const n = s / SEG;
	const k = rada.kurvid.find((x) => x.n1 > n + 2);
	if (!k) return null;
	const d = k.n0 * SEG - s;
	return { ...k, d: Math.max(0, d), sees: d <= 0 };
}

/* ---------- haare mootorist (sama mis kalkulaatoris) ----------
 * Pidurdusjäljest aeglustus kiiruse kaupa a(v) (m/s², v m/s). ABS ja koormus on sees. */
export function rehv(kat, veh, gClass) {
	return { key: 'x', name: 'x', category: kat, wetGripIndex: gClass?.C?.[kat]?.[0] || 1.32, treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: kat === 'WINTER_STUDDED', size: veh.oemSize, gSource: 'label' };
}
export function haardeTabel(P, tyre, veh, cond) {
	const r = P.stoppingDistance(tyre, veh, { speedKmh: 160, texture: 'NORMAL', payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1, ...cond });
	const tr = r.trace || [];
	const tabel = new Array(51).fill(0), lugeja = new Array(51).fill(0);
	for (let i = 1; i < tr.length; i++) {
		const v1 = tr[i - 1][1] / 3.6, v2 = tr[i][1] / 3.6, ds = tr[i][0] - tr[i - 1][0];
		if (ds <= 1e-6 || v1 > 160 / 3.6 - 2.5) continue; /* pidurite rakendumise algus välja */
		const a = (v1 * v1 - v2 * v2) / (2 * ds), b = Math.min(50, Math.round((v1 + v2) / 2));
		if (a > 0) { tabel[b] += a; lugeja[b]++; }
	}
	let viim = 0;
	for (let b = 0; b <= 50; b++) if (lugeja[b]) tabel[b] /= lugeja[b];
	for (let b = 50; b >= 0; b--) { if (lugeja[b]) viim = tabel[b]; else tabel[b] = viim; }
	for (let b = 0; b <= 50; b++) if (!tabel[b]) tabel[b] = viim || 1;
	return { a: (v) => { const x = Math.max(0, Math.min(50, v)), i = Math.floor(x), f = x - i; return tabel[i] * (1 - f) + tabel[Math.min(50, i + 1)] * f; } };
}
