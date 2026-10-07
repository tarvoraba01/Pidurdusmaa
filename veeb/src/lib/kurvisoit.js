/* Äkkpidurdus kurvis: auto liikumine ajas (pealtvaade), et seda saaks animeerida.
 *
 * LIHTSUSTATUD SÕIDUKIMUDEL (õppe jaoks), mitte mõõtmine:
 *  - jalgratta-mudel: üks esi- ja üks tagasild, auto saab liikuda, pöörata ja külg-
 *    suunas libiseda (vx, vy, pöördenurga kiirus r);
 *  - iga silla haare tuleb sama mootori rehvimudelist (Pidurdus.muAtSpeed) — muster,
 *    vesi, temperatuur ja kiirus mõjuvad täpselt nagu kalkulaatoris;
 *  - rehvi jõud: pikisuunaline (pidurdus) ja külgsuunaline (pööre) jagavad ühte haaret
 *    (hõõderingi reegel); mida rohkem libiseb, seda lähemal haarde piirile;
 *  - pidurdades kandub koormus esisillale; ABS hoiab esirattad haarde piiril, tagasild
 *    pidurdab ~28 % (EBD);
 *  - juht hoiab rooli nii, et püsida oma sõiduraja keskel (vaatab ~1 s ette), aga ei
 *    oska libisemist eriliselt päästa; ESP-d ei ole.
 *
 * Tee: sirge, siis paremkurv raadiusega R (90°), siis jälle sirge. Kaks 3,5 m sõidurada:
 * sinu rada paremal, vastassuunarada vasakul (kurvi välisküljel).
 * Koordinaadid meetrites, SVG-teljed (y alla). Algus (0,0) põhja suunas (−y).
 */

const g = 9.81;
export const RADA = 3.5; // sõiduraja laius, m
export const KURV_NURK = Math.PI / 2;
const POOL_AUTO = 0.9; // auto pool laiust, m

/** Tee geomeetria: s (m mööda sinu raja keskjoont) → punkt ja suund */
export function tee(R) {
	const sirge = !(R > 0) || !isFinite(R);
	const Th = KURV_NURK;
	const L = sirge ? Infinity : R * Th;
	const E = sirge ? null : [R - R * Math.cos(Th), -R * Math.sin(Th)];
	const psiE = -Math.PI / 2 + Th;
	function punkt(s) {
		if (sirge || s <= 0) return [0, -s, -Math.PI / 2];
		if (s <= L) {
			const th = s / R;
			return [R - R * Math.cos(th), -R * Math.sin(th), -Math.PI / 2 + th];
		}
		const k = s - L;
		return [E[0] + Math.cos(psiE) * k, E[1] + Math.sin(psiE) * k, psiE];
	}
	/** tee kõverus 1/m (paremale positiivne) */
	const kapp = (s) => (sirge || s < 0 || s > L ? 0 : 1 / R);
	/** auto asukoht → [s, d], d > 0 = vasakule ehk vastassuunarajale / kurvi välisküljele */
	function asend(x, y) {
		if (sirge) return [-y, -x];
		const phi = Math.atan2(y, x - R);
		const th = phi > 0 ? phi - Math.PI : phi + Math.PI;
		if (th < 0 && y > 0) return [-y, -x];
		if (th > Th) {
			const dx = x - E[0], dy = y - E[1];
			return [L + dx * Math.cos(psiE) + dy * Math.sin(psiE), dx * Math.sin(psiE) - dy * Math.cos(psiE)];
		}
		if (th < 0) return [-y, -x];
		return [R * th, Math.hypot(x - R, y) - R];
	}
	return { sirge, R, L, punkt, asend, kapp };
}

/**
 * @param P Pidurdus (engine.js)
 * @param o { veh, cond, tyreF, tyreR, R (m; 0 = sirge), reactionS, abs (false → ABS-ita, rattad lukustuvad), rada (true → salvesta teekond) }
 * @returns tulemus: vt lõppu
 */
export function kurviSoit(P, o) {
	const { veh, cond, tyreF, tyreR } = o;
	const T = tee(o.R);
	const m = veh.kerbMassKg + (cond.payloadKg || 0);
	/* HAAGIS (lihtsustatud): haagis järgneb autole jäigalt (loksumist ega „noa"
	   kokkuvoltimist ei arvestata). Pikisuunas peab auto pidurdama ka haagise
	   massi; inertspiduriga haagis pidurdab ise kuni 0,5 g (sama mis engine.js
	   trailerBrakeG / trailerTyreEff). Külgjõu kannavad haagise oma rattad.
	   Aisa surve tagasillale ~4 % haagise massist (kuni 75 kg). */
	const mT = Math.max(0, +o.trailerKg || 0), haagisPidur = !!o.trailerBrakes;
	const nina = Math.min(75, 0.04 * mT);
	const Lw = veh.wheelbaseM, h = veh.cogHeightM;
	const f0 = o.f0 ?? 0.6;
	const a = Lw * (1 - f0), b = Lw * f0; // raskuskeskmest esi- ja tagasillani
	const Iz = m * a * b;
	const abs = o.abs !== false;
	const tBuild = P.CAL.brakeBuildup[abs ? veh.absClass : 'NONE'] ?? 0.2;
	/* lukus ratas libiseb: haare on väiksem (mootori kalibratsioon: ABS-ita ~0,74 vs ABS-iga ~0,94
	   haardest) ja jõud on alati libisemisele vastu — rool ei mõju */
	const LUKK = ((P.CAL.absEff.NONE || 0.74) / (P.CAL.absEff[veh.absClass] || 0.94)) * Math.tanh(1.4);
	const aPidur = (veh.brakeCapacityG || 1.2) * g;
	const PAANIKA = 1.3; // äkkpidurdusel vajutab juht pedaali rohkem, kui rehv jaksab
	const reakt = o.reactionS ?? 1;
	const v0 = cond.speedKmh / 3.6;
	/* külgjäikus (1/rad, koormuse kohta); tagasild jäigem → auto kergelt alajuhitav nagu päris autod */
	const CYF = 9, CYR = 12;
	const SXABS = 1.4; // ABS hoiab pikilibisemise haarde tipu lähedal
	const SXTOT = 1.8, SXR = 1.1;
	const kR = 0.28 / 0.72;
	const KUS = (1 / CYF - 1 / CYR) / g; // alajuhitavuse gradient (rad·s²/m)

	const muC = [new Map(), new Map()];
	const mu = (i, v) => {
		const k = Math.round(Math.max(1, v) * 2);
		let x = muC[i].get(k);
		if (x === undefined) {
			x = P.muAtSpeed(i ? tyreR : tyreF, veh, cond, k / 2);
			muC[i].set(k, x);
		}
		return x;
	};
	/* üks sild: u, w — kiirus piki ratast ja risti; tagastab [Fx, Fy, kasutus 0…1] ratta teljestikus */
	function sild(u, w, N, muV, cy, sxF) {
		const sy = (cy * w) / Math.max(Math.abs(u), 0.5) / muV;
		const sx = sxF(Math.abs(sy));
		const s = Math.hypot(sx, sy);
		if (s < 1e-9) return [0, 0, 0];
		const F = muV * N * Math.tanh(s);
		return [-Math.sign(u || 1) * (F * sx) / s, (-F * sy) / s, Math.tanh(s)];
	}

	/* lukus ratas: jõud libisemise vastassuunas, suurus = lukus haare */
	function lukus(u, w, N, muV) {
		const sp = Math.hypot(u, w);
		if (sp < 0.05) return [0, 0, 1];
		const F = LUKK * muV * N;
		return [(-F * u) / sp, (-F * w) / sp, 1];
	}
	let lukkFKmh = null, lukkRKmh = null;

	/* algus: 30 m enne kurvi, otse ja ühtlase kiirusega; takistust näed kurvi sees */
	const s0 = -Math.min(35, Math.max(18, v0 * 1.4));
	const sNae = T.sirge ? 0 : Math.min(20, 0.15 * T.L);
	let [x, y, psi] = T.punkt(s0);
	let vx = v0, vy = 0, r = 0, delta = 0, ax = 0;
	let t = 0, tNae = null, fxF = 0;
	const rec = 0.02;
	let dt = 0.004; // samm: kiiresti sõites 4 ms, aeglaselt 2 ms (väikesel kiirusel on rehvijõud jäigem)
	const rada = o.rada ? [] : null;
	let jargmine = 0;
	let maxD = -Infinity, minD = Infinity, maxBeta = 0, maxUseF = 0, maxUseR = 0;
	let vastuKmh = null, vastuS = null, teeltKmh = null, teeltS = null, teeltPool = null;
	let libF = null, libR = null; // kiirus (km/h), kui sild esimest korda libisema hakkab
	let ringiKmh = null, sPidur = null, sLopp = null, peatus = false, tPidur = null;
	let s = s0, d = 0;

	for (let n = 0; n < 20000 && t < 40; n++) {
		const v = Math.hypot(vx, vy);
		dt = v > 3 ? 0.004 : 0.002;
		[s, d] = T.asend(x, y);
		/* faas */
		if (tNae === null && s >= sNae) tNae = t;
		const pidurdab = tNae !== null && t >= tNae + reakt;
		if (pidurdab && tPidur === null) { tPidur = t; sPidur = s; }
		const ramp = pidurdab ? (tBuild > 0 ? Math.min(1, (t - tPidur) / tBuild) : 1) : 0;

		/* juht: hoiab oma raja keskjoont — keerab kurvi järgi (vaatab ~0,3 s ette), parandab
		   suuna- ja küljevea ning summutab pöörlemist (rooli kiirus piiratud) */
		const [, , psiT] = T.punkt(s);
		const kap = T.kapp(s + 0.3 * v);
		let eps = psiT - psi;
		eps = Math.atan2(Math.sin(eps), Math.cos(eps));
		const dSoov = Math.max(-0.5, Math.min(0.5,
			kap * (Lw + KUS * v * v) + 0.8 * eps + Math.atan((0.6 * d) / (v + 2)) - 0.08 * (r - v * T.kapp(s))));
		const dMax = 0.9 * dt;
		delta += Math.max(-dMax, Math.min(dMax, dSoov - delta));

		/* koormus sildadel (pikisuunaline ülekanne pidurdades) */
		const NF = Math.max(0.05 * m * g, m * (g * f0 - (ax * h) / Lw));
		const NR = Math.max(0.05 * m * g, m * g - NF) + nina * g;
		const muF = mu(0, v), muR = mu(1, v);

		/* esisild: ratta teljestik */
		const vfy = vy + a * r;
		const cd = Math.cos(delta), sd = Math.sin(delta);
		const uF = vx * cd + vfy * sd, wF = -vx * sd + vfy * cd;
		/* ABS hoiab esirattad pikisuunas haarde tipus, aga suure külglibisemise korral laseb
		   veidi järele (rool peab mõjuma); EBD/CBC annab tagasillale pidurdust ainult nii palju,
		   kui külghaardest üle jääb */
		const sxF = pidurdab
			? (sy) => Math.min(SXABS * ramp, Math.sqrt(Math.max(0.09, SXTOT * SXTOT - sy * sy)))
			: () => -Math.max(0, Math.min(0.4, (v0 - vx) * 0.3)); // hoiab kiirust
		/* ABS-ita: paanikas pidurdus lukustab esirattad, kui pidurijõud ületab haarde;
		   tagarattad lukustuvad, kui nende osa (~28 %, rõhuregulaator vähendab umbes poole võrra)
		   ületab tagasilla haarde — pidurdades on tagasild kerge */
		const lukkF = pidurdab && !abs && ramp * PAANIKA * aPidur * 0.72 * m > muF * NF;
		const uR = vx, wR = vy - b * r;
		let FxFw, FyFw, useF, FxR, FyR, useR;
		if (lukkF) [FxFw, FyFw, useF] = lukus(uF, wF, NF, muF);
		else [FxFw, FyFw, useF] = sild(uF, wF, NF, muF, CYF, !abs && pidurdab ? () => Math.min(1.2, ramp * 1.2) : sxF);
		fxF = Math.abs(FxFw);
		/* tagasild */
		const lukkR = pidurdab && !abs && ramp * PAANIKA * aPidur * 0.28 * 0.5 * m > muR * NR;
		if (lukkR) [FxR, FyR, useR] = lukus(uR, wR, NR, muR);
		else {
			const ebd = pidurdab ? Math.min(1.2, Math.atanh(Math.min(0.85, (kR * fxF) / (muR * NR)))) : 0;
			const sxR = abs ? (sy) => Math.min(ebd, Math.sqrt(Math.max(0, SXR * SXR - sy * sy))) : () => ebd;
			[FxR, FyR, useR] = sild(uR, wR, NR, muR, CYR, sxR);
		}
		if (lukkF && lukkFKmh === null) lukkFKmh = v * 3.6;
		if (lukkR && lukkRKmh === null) lukkRKmh = v * 3.6;
		/* keresse teljestikku */
		const FxF = FxFw * cd - FyFw * sd, FyF = FxFw * sd + FyFw * cd;
		const drag = (0.5 * 1.2 * (veh.cdaM2 || 0.7) * v * vx) + (P.CAL.crr || 0.012) * m * g * Math.sign(vx) * Math.min(1, Math.abs(vx));
		const FxT = mT > 0 && pidurdab && haagisPidur && vx > 0.05 ? -ramp * Math.min(mu(1, v) * g * (P.CAL.trailerTyreEff || 0.85), (P.CAL.trailerBrakeG || 0.5) * g) * mT : 0;
		const Fx = FxF + FxR - drag + FxT, Fy = FyF + FyR;
		const axN = Fx / (m + mT);
		ax = 0.8 * ax + 0.2 * axN;
		vx += (axN + vy * r) * dt;
		vy += (Fy / m - vx * r) * dt;
		r += ((a * FyF - b * FyR) / Iz) * dt;
		x += (vx * Math.cos(psi) - vy * Math.sin(psi)) * dt;
		y += (vx * Math.sin(psi) + vy * Math.cos(psi)) * dt;
		psi += r * dt;
		t += dt;

		/* jälgimine (ainult pärast takistuse nägemist) */
		const beta = Math.abs(Math.atan2(vy, vx));
		if (tNae !== null) {
			if (d > maxD) maxD = d;
			if (d < minD) minD = d;
			if (v > 2 && beta > maxBeta) maxBeta = beta;
			if (useF > maxUseF) maxUseF = useF;
			if (useR > maxUseR) maxUseR = useR;
			if (libF === null && useF > 0.97 && Math.abs(wF) > 0.15) libF = v * 3.6;
			if (libR === null && useR > 0.97 && Math.abs(wR) > 0.15) libR = v * 3.6;
			if (ringiKmh === null && v > 2 && beta > 0.6) ringiKmh = v * 3.6;
			if (vastuKmh === null && d + POOL_AUTO > RADA / 2) {
				/* auto vasak külg ületab keskjoone */
				vastuKmh = v * 3.6; vastuS = s;
			}
			if (teeltKmh === null && (d > RADA * 1.5 || d < -RADA / 2)) {
				teeltKmh = v * 3.6; teeltS = s; teeltPool = d > 0 ? 'valja' : 'sisse';
			}
		}
		if (rada && t >= jargmine) {
			rada.push([t, x, y, psi, v * 3.6, useF, useR, pidurdab ? 2 : tNae !== null ? 1 : 0, d, (lukkF ? 1 : 0) + (lukkR ? 2 : 0)]);
			jargmine += rec;
		}
		/* lõpp: seisab, või on teelt üle 2 m väljas */
		if (pidurdab && v < 0.3) { peatus = true; break; }
		if (teeltKmh !== null && (d > RADA * 1.5 + 2.5 || d < -RADA / 2 - 2.5)) break;
	}
	sLopp = s;
	if (rada) rada.push([t, x, y, psi, Math.hypot(vx, vy) * 3.6, 0, 0, 3, d]);
	const [, , psiTee] = T.punkt(s);
	let suund = ((psi - psiTee) * 180) / Math.PI;
	suund = ((((suund + 180) % 360) + 360) % 360) - 180;
	const ringi = ringiKmh !== null || Math.abs(suund) > 60;
	const vastu = maxD > RADA / 2 - POOL_AUTO;
	const teelt = teeltKmh !== null;
	return {
		rada,
		tee: T,
		sNae,
		sPidur,
		reaktM: v0 * reakt,
		/* kui pikk teekond takistuse nägemisest peatumiseni (mööda teed) */
		peatumineM: peatus && !teelt ? sLopp - sNae : null,
		peatus,
		ringi,
		ringiKmh,
		vastu,
		vastuKmh,
		teelt,
		teeltKmh,
		teeltPool,
		maxNihe: maxD, // m raja keskjoonest vasakule (vastassuunda)
		minNihe: minD,
		lopuSuund: suund, // kraadi teesuunast
		libF,
		libR,
		maxUseF,
		maxUseR,
		maxBeta: (maxBeta * 180) / Math.PI,
		abs,
		lukkFKmh,
		lukkRKmh,
		/* piiril: auto jõuab keskjoonele lähemale kui 40 cm, libiseb külg ees üle 6° või tagarattad on haarde piiril */
		tulemus: teelt ? (ringi ? 'ringi_teelt' : 'teelt') : ringi ? 'ringi' : vastu ? 'vastu' : maxD > 0.45 || maxBeta > 0.1 || (abs && maxUseR > 0.95) ? 'piiril' : 'ok'
	};
}

/** Tulemuse raskusaste värvi jaoks: 0 hea … 4 halvim */
export const RASKUS = { ok: 0, piiril: 1, vastu: 2, ringi: 3, teelt: 4, ringi_teelt: 4 };
