/* Pikivahe: eesolev auto pidurdab järsult (või peatub kohe, nt sõidab millelegi otsa).
 * Sina sõidad sama kiirusega tema taga, vahe = kiirus × sekundid. Sina hakkad pidurdama
 * alles pärast reageerimisaega. Kas jõuad peatuda, ja kui ei, siis millise kiirusega
 * sõidad talle sisse?
 *
 * Pidurdamine tuleb samast mootorist (stoppingDistance, reaktsiooniaeg 0): sama auto,
 * samad rehvid ja tee mõlemal autol. trace = [[pidurdusteekond m, kiirus km/h], …].
 */

/** trace → ajatelg: [[t s, teekond m, kiirus m/s], …] */
function ajatelg(trace) {
	const out = [[0, trace[0][0], trace[0][1] / 3.6]];
	for (let i = 1; i < trace.length; i++) {
		const [s0, v0] = trace[i - 1], [s1, v1] = trace[i];
		const vk = (v0 + v1) / 2 / 3.6;
		const dt = vk > 0.05 ? (s1 - s0) / vk : 0;
		out.push([out[i - 1][0] + dt, s1, v1 / 3.6]);
	}
	return out;
}
function hetkel(tl, t) {
	if (t <= 0) return [0, tl[0][2]];
	for (let i = 1; i < tl.length; i++) {
		if (tl[i][0] >= t) {
			const [t0, s0, v0] = tl[i - 1], [t1, s1, v1] = tl[i];
			const k = t1 > t0 ? (t - t0) / (t1 - t0) : 1;
			return [s0 + (s1 - s0) * k, v0 + (v1 - v0) * k];
		}
	}
	const l = tl[tl.length - 1];
	return [l[1], 0];
}

/**
 * @param traceF  sinu pidurdusjälg (reaktsioonita) stoppingDistance'ist
 * @param kmh     sinu kiirus
 * @param vaheS   pikivahe sekundites (sinu kiiruse järgi)
 * @param reaktS  sinu reageerimisaeg
 * @param ees     'pidurdab' — eesolev auto pidurdab järsult; 'seisab' — peatub kohe
 * @param traceL  eesoleva auto pidurdusjälg (kui puudub, pidurdab ta nagu sina)
 */
export function pikivahe(traceF, kmh, vaheS, reaktS, ees = 'pidurdab', traceL = null) {
	const v = kmh / 3.6;
	const vaheM = v * vaheS;
	const tf = ajatelg(traceF);
	const tl = traceL ? ajatelg(traceL) : tf;
	const tLopp = Math.max(tl[tl.length - 1][0], tf[tf.length - 1][0] + reaktS) + 1;
	const eesKoht = ees === 'seisab' ? vaheM : vaheM + tl[tl.length - 1][1];
	for (let t = 0; t <= tLopp; t += 0.005) {
		const [sL, vL] = ees === 'seisab' ? [0, 0] : hetkel(tl, t);
		const xL = vaheM + sL;
		let xF, vF;
		if (t < reaktS) { xF = v * t; vF = v; } else { const [s, vv] = hetkel(tf, t - reaktS); xF = v * reaktS + s; vF = vv; }
		if (xF >= xL) {
			return { vaheM, kokkuporge: true, loogKmh: Math.max(0, (vF - vL) * 3.6), sinuKmh: vF * 3.6, temaKmh: vL * 3.6 };
		}
		if (vF <= 0 && t > reaktS) break;
	}
	const [sF] = hetkel(tf, tLopp);
	return { vaheM, kokkuporge: false, jaabM: eesKoht - (v * reaktS + sF) };
}
