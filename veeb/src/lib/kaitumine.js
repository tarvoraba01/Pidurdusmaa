/* Auto käitumine pidurdamisel: esi- ja tagarehvid eraldi, sirgel ja kurvis.
 *
 * LIHTSUSTATUD FÜÜSIKAMUDEL (õppe jaoks), mitte mõõtmine:
 *  - iga silla haare tuleb sama mootori rehvimudelist (Pidurdus.muAtSpeed), nii et
 *    mustrisügavus, vesi, temperatuur ja kiirus mõjuvad täpselt nagu kalkulaatoris;
 *  - pidurdades kandub koormus esisillale: N_esi = m(g·f0 + a·h/L), N_taga = m(g·(1−f0) − a·h/L)
 *    (h = raskuskeskme kõrgus, L = teljevahe, f0 = esisilla osa massist seisval autol);
 *  - kurvis vajab iga sild külgjõudu m·v²/R oma massiosa järgi (püsiv kurv);
 *  - hõõderingi reegel: rehv jagab ühe haarde pikijõu (pidurdus) ja külgjõu (pööre) vahel —
 *    mis kulub kurvi hoidmiseks, seda pidurdamiseks ei jää;
 *  - pidurdusjõud jaguneb ~72 % ette, ~28 % taha; ABS hoiab rattad piiril. ESP-d mudel ei arvesta:
 *    ESP aitab autot hoida, aga haaret juurde ei tee.
 * Kui külgjõu vajadus ületab silla haarde, see sild libiseb:
 *    tagasild → auto pöörab ringi (ülejuhitavus), esisild → auto ei pööra (alajuhitavus).
 * Taust: ADAC, TCS ja ÖAMTC katsed näitasid, et paremad rehvid peavad olema tagasillal.
 */

const g = 9.81;

/** Esisilla osa massist (seisval autol). Tagaveolised premium-sõiduautod ~52 %, muud ~60 %. */
export function esiOsa(veh) {
	const k = String(veh.key || '');
	if (veh.body === 'KAUBIK') return 0.55;
	if (/^(bmw_(?!2\d\d[a-z]*_f4|2\d\d[a-z]*_u|x1|x2|i3)|mb_(?!a|b|cla|gla|glb|vito|v_|viano|citan|eq[ab])|porsche_|lexus_(is|gs|ls)|jaguar_(xe|xf|xj|s|f)|tesla_|ford_mustang|dodge_(challenger|charger)|alfa_giulia|volvo_(240|740|940|960))/.test(k)) return 0.52;
	if (veh.body === 'MAASTUR') return 0.57;
	return 0.6;
}

/**
 * @param P Pidurdus (engine.js)
 * @param o { veh, cond, tyreF, tyreR, R (m, Infinity = sirge), reactionS }
 *   cond: sama kuju mis stoppingDistance (speedKmh, surface, waterMm, tempC, payloadKg, gradientPct, …)
 */
export function kaitumine(P, o) {
	const { veh, cond, tyreF, tyreR } = o;
	const R = o.R > 0 ? o.R : Infinity;
	const C = P.CAL;
	const m = veh.kerbMassKg + (cond.payloadKg || 0);
	const L = veh.wheelbaseM, h = veh.cogHeightM;
	const f0 = esiOsa(veh);
	const eta = C.absEff[veh.absClass] ?? 1;
	const tBuild = C.brakeBuildup[veh.absClass] ?? 0.2;
	const aBrakeMax = (veh.brakeCapacityG || 1.2) * (cond.brakeCondition ?? 1) * g;
	const muF = (v) => P.muAtSpeed(tyreF, veh, cond, Math.max(0.5, v));
	const muR = (v) => P.muAtSpeed(tyreR, veh, cond, Math.max(0.5, v));

	/* kurvi piirkiirus ilma pidurdamata: v²/R = μ·g kummalgi sillal */
	let piir = Infinity, piirSild = null;
	if (isFinite(R)) {
		let v = Math.sqrt(Math.min(muF(20), muR(20)) * g * R);
		for (let i = 0; i < 30; i++) v = Math.sqrt(Math.min(muF(v), muR(v)) * g * R);
		piir = v * 3.6;
		piirSild = muR(v) < muF(v) ? 'taga' : 'esi';
	}

	/* Pidurdusjõu jaotus: tagasild saab ~28 % (tüüpiline sõiduauto; EBD hoiab tagarattad
	   lukustumast). ABS hoiab esirattad haarde piiril, tagasild pidurdab jaotuse järgi,
	   kuni ka tema haarde piir tuleb ette. */
	const BR = 0.28, kR = BR / (1 - BR);
	/* üks hetk: pidurdusaeglustus ja kummagi silla külghaarde kasutus */
	function hetk(v, ramp) {
		const ay = isFinite(R) ? (v * v) / R : 0;
		const mf = muF(v), mr = muR(v);
		const FyF = m * ay * f0, FyR = m * ay * (1 - f0);
		let ax = 0, uF = 0, uR = 0, kaotus = null;
		for (let i = 0; i < 40; i++) {
			const NF = m * (g * f0 + (ax * h) / L), NR = Math.max(1, m * (g * (1 - f0) - (ax * h) / L));
			const capF = mf * NF, capR = mr * NR;
			if (FyF >= capF || FyR >= capR) {
				/* võrdse haarde korral libiseb esimesena esiots (autod on nii häälestatud) */
				kaotus = FyR / capR > FyF / capF + 1e-6 ? 'taga' : 'esi';
				uF = FyF / capF; uR = FyR / capR;
				break;
			}
			const FxF = Math.sqrt(capF * capF - FyF * FyF) * ramp;
			const FxR = Math.min(Math.sqrt(capR * capR - FyR * FyR), kR * FxF);
			/* varu = kui suur osa silla haardest on veel kurvi hoidmiseks vaba
			   (pidurdus võtab koormuse tagant ära, nii et taga varu väheneb) */
			uF = FyF / capF;
			uR = FyR / capR;
			const axN = Math.min((eta * (FxF + FxR)) / m, aBrakeMax * ramp);
			if (Math.abs(axN - ax) < 1e-4) { ax = axN; break; }
			ax = 0.5 * ax + 0.5 * axN;
		}
		return { ax, uF, uR, kaotus };
	}

	const v0 = cond.speedKmh / 3.6;
	const sReakt = v0 * (o.reactionS ?? cond.reactionTimeS ?? 1);
	/* reageerimise ajal sõidab auto kurvis täiskiirusel */
	const alg = hetk(v0, 0);
	let s = 0, v = v0, t = 0, maxF = alg.uF, maxR = alg.uR, kaotus = alg.kaotus, kaotusKmh = alg.kaotus ? v0 * 3.6 : null, kaotusM = alg.kaotus ? 0 : null;
	const dt = 0.005;
	if (!kaotus) {
		while (v > 0.05 && t < 60) {
			const ramp = tBuild > 0 ? Math.min(1, t / tBuild) : 1;
			const x = hetk(v, ramp);
			if (x.uF > maxF) maxF = x.uF;
			if (x.uR > maxR) maxR = x.uR;
			if (x.kaotus) { kaotus = x.kaotus; kaotusKmh = v * 3.6; kaotusM = sReakt + s; break; }
			const drag = (0.5 * 1.2 * (veh.cdaM2 || 0.7) * v * v) / m + (C.crr || 0.012) * g;
			v -= (x.ax + drag) * dt;
			s += Math.max(0, v) * dt;
			t += dt;
		}
	}
	return {
		f0,
		piirKmh: piir,
		piirSild,
		kaotus, //               null | 'taga' | 'esi'
		kaotusKmh,
		kaotusM, //               kui kaugel (m) haare kaob; 0 = juba kurvi sisenedes
		peatumineM: kaotus ? null : sReakt + s,
		reaktM: sReakt,
		varuEsi: Math.max(0, 1 - maxF), // väikseim haardevaru pidurduse ajal (esisild on ABS-iga piiril)
		varuTaga: Math.max(0, 1 - maxR) // tagasilla varu: kui see kaob, pöörab auto ringi
	};
}
