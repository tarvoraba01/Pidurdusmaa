/* Pseudo-3D tee mängu jaoks (/liiklusohutus/reaktsioon/).
 * Klassikaline segmentprojektsioon (nagu vanad sõidumängud): tee koosneb
 * 5 m lõikudest, igal oma kurvatuur ja teeäärsed objektid. Füüsika EI ole
 * siin — siin ainult joonistamine. Kaugused meetrites, kaamera sinu sõidurajal.
 *
 * looTee({ maastik: 'mets'|'kula', seed }) → tee
 * joonista(ctx, W, H, tee, olek) — olek: { z, kmh, oo, ilm, ees, jk, crash, aeg }
 *   ees = { gap, pidur } eesolev auto (gap = vahe meetrites tema tagaotsani)
 *   jk  = { z, x, riie, kond } jalakäija (z absoluutne, x külgnihe m teeteljest)
 */

const SEG = 5; /* lõigu pikkus, m */
const N = 400; /* lõike (2 km, korduv) */
const TEE_L = 3.5; /* sõiduraja laius */
const KAAM_H = 1.25; /* silmade kõrgus */
const KAAM_X = TEE_L / 2; /* auto sinu raja keskel (paremal) */
const JUHT_X = 0.37; /* juht istub auto keskjoonest vasakul (vasakpoolne rool) */
const NAHE = 110; /* joonistatavaid lõike (550 m) */

/* deterministlik juhuarv, et sama seed annaks sama tee */
function rng(seed) {
	let s = seed >>> 0 || 1;
	return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

export function looTee({ maastik = 'mets', seed = 1 } = {}) {
	const r = rng(seed);
	const seg = [];
	/* kurvid: sirged ja kaared vaheldumisi, sujuv sisse/välja */
	let i = 0;
	while (i < N) {
		const pikk = 20 + Math.floor(r() * 40);
		const k = r() < 0.3 ? 0 : (r() < 0.5 ? -1 : 1) * (0.06 + r() * (maastik === 'kula' ? 0.08 : 0.2));
		for (let j = 0; j < pikk && i < N; j++, i++) {
			const sujuv = Math.min(1, j / 8, (pikk - j) / 8);
			seg.push({ k: k * sujuv, obj: [] });
		}
	}
	/* teeäärsed objektid */
	for (let n = 0; n < N; n++) {
		const s = seg[n];
		if (n % 10 === 0) { s.obj.push({ t: 'post', x: -TEE_L - 1.2 }); s.obj.push({ t: 'post', x: TEE_L + 1.2 }); }
		if (maastik === 'mets') {
			for (const pool of [-1, 1]) {
				if (r() < 0.75) s.obj.push({ t: r() < 0.8 ? 'kuusk' : 'kask', x: pool * (TEE_L + 4 + r() * 14), h: 9 + r() * 9, v: r() });
				if (r() < 0.35) s.obj.push({ t: 'kuusk', x: pool * (TEE_L + 3 + r() * 3), h: 7 + r() * 6, v: r() });
			}
		} else {
			if (n % 8 === 0) for (const pool of [-1, 1]) if (r() < 0.85) s.obj.push({ t: 'maja', x: pool * (TEE_L + 9 + r() * 6), w: 8 + r() * 4, h: 5 + r() * 3, v: r(), aken: r() });
			if (n % 12 === 6) s.obj.push({ t: 'lamp', x: TEE_L + 1.6 });
			if (n % 8 === 4) for (const pool of [-1, 1]) if (r() < 0.6) s.obj.push({ t: r() < 0.5 ? 'kask' : 'poos', x: pool * (TEE_L + 4.5 + r() * 2), h: 4 + r() * 6, v: r() });
			if (n % 2 === 0) for (const pool of [-1, 1]) s.obj.push({ t: 'aed', x: pool * (TEE_L + 5.2) });
			/* pargitud autod mõlemal pool tänavat (jalakäija võib tulla ükskõik millise tagant) */
			if (n % 3 === 1) for (const pool of [-1, 1]) if (r() < 0.45) s.obj.push({ t: 'parkauto', x: pool * (TEE_L + 1.3), varv: ['#46505e', '#6b2f2f', '#2f4a6b', '#7a7d82', '#1f2428'][Math.floor(r() * 5)] });
		}
	}
	/* tähed */
	const tahed = Array.from({ length: 70 }, () => [r(), r() * 0.42, r()]);
	return { seg, maastik, tahed, seed };
}

/* varjaja jalakäija ette: suur puu / maja / pargitud auto lõigus n, poolel */
export function lisaVarjaja(tee, n, pool) {
	const s = tee.seg[((n % N) + N) % N];
	s.obj.push(tee.maastik === 'kula'
		? { t: 'parkauto', x: pool * (TEE_L + 1.3), varv: ['#46505e', '#6b2f2f', '#2f4a6b', '#7a7d82'][n % 4] }
		: { t: 'kuusk', x: pool * (TEE_L + 2.6), h: 11, v: 0.5, suur: 1 });
}

const kl = (x, a, b) => Math.max(a, Math.min(b, x));
function hex(c) { return [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)]; }
/* värv valgusega L (0 = pime, 1 = täis) ja udu/ilma toon */
function v(c, L, udu = 0, uduVarv = [0, 0, 0]) {
	const [r, g, b] = typeof c === 'string' ? hex(c) : c;
	const m = (x, u) => Math.round(x * L * (1 - udu) + u * udu);
	return `rgb(${m(r, uduVarv[0])},${m(g, uduVarv[1])},${m(b, uduVarv[2])})`;
}

/* valgus kaugusel z (m): päeval 1; öösel lähituled ~60 m, + kuu ja laternad */
function valgus(z, oo, lampL = 0) {
	if (!oo) return 1;
	const tuled = z < 0 ? 0 : 0.95 * Math.pow(kl(1 - z / 62, 0, 1), 1.25);
	return kl(0.05 + tuled + lampL, 0, 1);
}

const SILM = 2; /* juhi silmad auto esiotsast tagapool (m) */
export function joonista(ctx, W, H, tee, o) {
	let P = null;
	try { P = joonistaStseen(ctx, W, H, tee, o); } catch (e) { /* üks vigane kaader ei tohi salongi ära viia */ }
	const k = kokpit(W, H);
	k.tee = P; /* navigatsiooniekraanile: tee telg eespool (zr, x) */
	try {
		kapott(ctx, W, H, k, o);
		klaasIlm(ctx, W, H, k, o);
		if (o.crash) klaas(ctx, W, H);
		salong(ctx, W, H, k, o);
	} catch (e) { /* salong ei tohi mängu katki teha */ }
}
function joonistaStseen(ctx, W, H, tee, o) {
	const oo = !!o.oo, talv = o.ilm === 'talv', vihm = o.ilm === 'vihm';
	const hor = Math.round(H * 0.44);
	const D = (W / 2) / Math.tan((68 * Math.PI) / 360); /* fookus pikslites */
	const uduVarv = oo ? [6, 8, 12] : talv ? [214, 222, 232] : vihm ? [150, 160, 170] : [190, 210, 228];
	const uduK = oo ? 0 : talv ? 1 / 220 : vihm ? 1 / 180 : 1 / 650;

	/* ---- taevas ---- */
	const g = ctx.createLinearGradient(0, 0, 0, hor);
	if (oo) { g.addColorStop(0, '#04060c'); g.addColorStop(1, '#0d1220'); }
	else if (talv) { g.addColorStop(0, '#a9b6c6'); g.addColorStop(1, '#dde4ec'); }
	else if (vihm) { g.addColorStop(0, '#6d7884'); g.addColorStop(1, '#a6b0ba'); }
	else { g.addColorStop(0, '#5d9bd8'); g.addColorStop(1, '#cfe3f3'); }
	ctx.fillStyle = g; ctx.fillRect(0, 0, W, hor + 1);
	if (oo) {
		ctx.fillStyle = '#cfd6e6';
		for (const [x, y, b] of tee.tahed) { ctx.globalAlpha = 0.3 + b * 0.6; ctx.fillRect(x * W, y * H, b > 0.8 ? 2 : 1, b > 0.8 ? 2 : 1); }
		ctx.globalAlpha = 1;
		/* kuu */
		const kx = W * 0.78, ky = H * 0.12, kr = H * 0.035;
		const kg = ctx.createRadialGradient(kx, ky, kr * 0.5, kx, ky, kr * 4);
		kg.addColorStop(0, 'rgba(230,236,255,0.35)'); kg.addColorStop(1, 'rgba(230,236,255,0)');
		ctx.fillStyle = kg; ctx.fillRect(kx - kr * 4, ky - kr * 4, kr * 8, kr * 8);
		ctx.fillStyle = '#eef1fa'; ctx.beginPath(); ctx.arc(kx, ky, kr, 0, 7); ctx.fill();
		ctx.fillStyle = 'rgba(160,170,190,0.35)';
		for (const [a, b, c] of [[-0.3, -0.2, 0.22], [0.25, 0.1, 0.16], [-0.05, 0.35, 0.12], [0.35, -0.35, 0.1]]) { ctx.beginPath(); ctx.arc(kx + a * kr, ky + b * kr, c * kr, 0, 7); ctx.fill(); }
	} else if (!vihm && !talv) {
		ctx.fillStyle = 'rgba(255,255,255,0.75)';
		for (let i = 0; i < 4; i++) { const cx = ((i * 0.31 + tee.seed * 0.07) % 1) * W, cy = H * (0.08 + (i % 2) * 0.07); ctx.beginPath(); ctx.ellipse(cx, cy, W * 0.08, H * 0.025, 0, 0, 7); ctx.ellipse(cx + W * 0.04, cy - H * 0.015, W * 0.05, H * 0.022, 0, 0, 7); ctx.fill(); }
	}
	/* maapind horisondist alla */
	const maa = oo ? '#05070a' : talv ? '#e9eef3' : tee.maastik === 'kula' ? '#6f8f4e' : '#4f6b3a';
	ctx.fillStyle = v(maa, oo ? 0.25 : 1, oo ? 0 : 0.35, uduVarv); ctx.fillRect(0, hor, W, H - hor);

	/* ---- projektsioon ---- */
	/* o.z ja kaugused (ees.gap) on auto esiotsast; kaamera = juhi silmad SILM m tagapool.
	   Muidu kadus vahetult ette jäänud jalakäija pildilt (paistis, nagu sõidaks läbi). */
	const z0 = Math.max(0, (o.z || 0) - SILM), base = Math.floor(z0 / SEG), frac = (z0 % SEG) / SEG;
	const sg = (n) => tee.seg[((n % N) + N) % N];
	/* Tee telg kaamera teljestikus, PIDEVALT: kõverus κ = k/SEG² on lõigu sees
	   konstantne; integreerime kaamerast edasi (kaamera suund = tee puutuja).
	   Varem nihkus kogu tee iga 5 m järel järsult külje peale (nõksud kurvis). */
	const P = [];
	const kap = (n) => sg(n).k / (SEG * SEG);
	const kb = kap(base);
	P.push({ zr: 0.1, x: 0, s: sg(base), n: base });
	let zr = (1 - frac) * SEG, th = kb * zr, x = 0.5 * kb * zr * zr;
	for (let n = 1; n <= NAHE; n++) {
		const s = sg(base + n);
		/* kaamerale liiga lähedal (< 0,6 m) lõigupiir jäetakse välja: muidu jäi
		   iga 5 m järel auto ette hetkeks tühi riba (maa „vilkus“ sõites) */
		if (n > 1 || zr > 0.6) P.push({ zr, x, s, n: base + n });
		const kn = kap(base + n);
		x += th * SEG + 0.5 * kn * SEG * SEG; th += kn * SEG; zr += SEG;
	}
	const proj = (wx, wy, zr) => { const sc = D / Math.max(0.3, zr); return [W / 2 + (wx - KAAM_X + JUHT_X) * sc, hor + (KAAM_H - wy) * sc, sc]; };
	/* laternate valgus lõikudes (küla, öö) */
	const lampL = (n) => {
		if (!oo || tee.maastik !== 'kula') return 0;
		const k = ((n % 12) + 12) % 12, d = Math.min(Math.abs(k - 6), 12 - Math.abs(k - 6));
		return d < 3 ? 0.28 * (1 - d / 3) : 0;
	};

	/* ---- tee (kaugelt lähedale) ---- */
	for (let i = P.length - 2; i >= 0; i--) {
		const a = P[i], b = P[i + 1];
		const [ax, ay, as] = proj(a.x, 0, a.zr), [bx, by, bs] = proj(b.x, 0, b.zr);
		if (by >= ay) continue;
		const L = valgus(a.zr, oo, lampL(a.n)), udu = kl(a.zr * uduK, 0, 0.85);
		const tri = (x1, w1, x2, w2, c) => { ctx.fillStyle = c; ctx.beginPath(); ctx.moveTo(ax + x1 * as, ay + 1); ctx.lineTo(ax + (x1 + w1) * as, ay + 1); ctx.lineTo(bx + (x2 + w2) * bs, by - 1); ctx.lineTo(bx + x2 * bs, by - 1); ctx.fill(); };
		/* serv (muru/lumi) vöödena */
		const vood = a.zr < 40 ? Math.floor(a.n / 2) % 2 : 0; /* kaugel triibud virvendaksid */
		const serv = talv ? (vood ? '#eef2f6' : '#e3e8ee') : tee.maastik === 'kula' ? (vood ? '#78985a' : '#6f8f50') : (vood ? '#55723f' : '#4c6838');
		tri(-60, 120, -60, 120, v(serv, L, udu, uduVarv));
		/* asfalt + õlad */
		const asf = talv ? (vood ? '#c9cfd6' : '#c2c8cf') : vihm ? (vood ? '#3a3f46' : '#363a40') : (vood ? '#55595f' : '#50545a');
		tri(-TEE_L - 0.6, 2 * TEE_L + 1.2, -TEE_L - 0.6, 2 * TEE_L + 1.2, v(asf, L, udu, uduVarv));
		/* äärejooned */
		const joon = v(talv ? '#f4f6f8' : '#e6e6e0', Math.min(1, L * 1.15), udu, uduVarv);
		tri(-TEE_L - 0.1, 0.15, -TEE_L - 0.1, 0.15, joon);
		tri(TEE_L - 0.05, 0.15, TEE_L - 0.05, 0.15, joon);
		/* keskjoon katkendlik */
		if (Math.floor(a.n / 2) % 3 !== 0) tri(-0.07, 0.14, -0.07, 0.14, v(talv ? '#dfe3e8' : '#f0f0ea', Math.min(1, L * 1.2), udu, uduVarv));
		/* talvel rattarööpad */
		if (talv) { const r = v('#aab2bb', L, udu, uduVarv); tri(0.85, 0.32, 0.85, 0.32, r); tri(2.55, 0.32, 2.55, 0.32, r); tri(-2.85, 0.32, -2.85, 0.32, r); tri(-1.15, 0.32, -1.15, 0.32, r); }
		/* vihmas peegeldus */
		if (vihm && oo && a.zr < 45) { ctx.fillStyle = `rgba(255,240,200,${0.05 * (1 - a.zr / 45)})`; ctx.fillRect(ax - 0.5 * as, by, 4 * as, ay - by); }
	}

	/* ---- objektid ja liikujad (kaugelt lähedale) ---- */
	const asjad = [];
	for (let i = P.length - 1; i >= 1; i--) {
		const a = P[i];
		for (const ob of a.s.obj) asjad.push({ zr: a.zr, x: a.x + ob.x, ob, n: a.n });
	}
	const xAt = (zr) => { /* tee telje x kaugusel zr (interpolatsioon) */
		let i = 0; while (i < P.length - 2 && P[i + 1].zr < zr) i++;
		const a = P[i], b = P[i + 1], k = kl((zr - a.zr) / Math.max(0.01, b.zr - a.zr), 0, 1);
		return a.x + (b.x - a.x) * k;
	};
	if (o.ees && o.ees.gap < 520) asjad.push({ zr: o.ees.gap + SILM, x: xAt(o.ees.gap + SILM) + KAAM_X, ob: { t: 'auto', pidur: o.ees.pidur }, n: 0 });
	if (o.jk && o.jk.z - z0 > 0.2 && o.jk.z - z0 < 520) { const zr = o.jk.z - z0; asjad.push({ zr, x: xAt(zr) + o.jk.x, ob: { t: 'inim', riie: o.jk.riie, kond: o.jk.kond }, n: 0 }); }
	asjad.sort((p, q) => q.zr - p.zr);
	for (const a of asjad) {
		if (a.zr < 1.2) continue;
		const [sx, sy, sc] = proj(a.x, 0, a.zr);
		if (sx < -W * 0.6 || sx > W * 1.6) continue;
		const L = valgus(a.zr, oo, lampL(a.n)) * (Math.abs(a.x - KAAM_X) > 8 && oo ? 0.55 : 1), udu = kl(a.zr * uduK, 0, 0.85);
		objekt(ctx, a.ob, sx, sy, sc, L, udu, uduVarv, { oo, talv, aeg: o.aeg, zr: a.zr });
	}

	/* ---- ilm ---- */
	if (talv || vihm) {
		const t = o.aeg || 0, n = talv ? 140 : 110, kiir = (o.kmh || 0) / 90;
		ctx.fillStyle = talv ? 'rgba(255,255,255,0.85)' : 'rgba(200,215,235,0.45)';
		ctx.strokeStyle = 'rgba(190,205,230,0.45)'; ctx.lineWidth = 1;
		for (let i = 0; i < n; i++) {
			const sx = (Math.sin(i * 12.9898) * 43758.5453) % 1, sy = (Math.sin(i * 78.233) * 12345.678) % 1;
			const mod = (x) => ((x % 1) + 1) % 1;
			const kiirI = 0.6 + ((i * 7) % 5) / 10; /* igal helbel oma kiirus */
			const px = mod(Math.abs(sx) + t * (talv ? 0.02 : 0.004) * ((i % 3) - 1)) * W;
			const py = mod(Math.abs(sy) + t * kiirI * (talv ? 0.18 + kiir * 0.25 : 1.4)) * H;
			if (talv) { ctx.beginPath(); ctx.arc(px, py, 1 + (i % 3) * 0.7, 0, 7); ctx.fill(); }
			else { ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px - 2, py + 12); ctx.stroke(); }
		}
	}

	/* ---- öine pimendus servades (esitulede koonus) ---- */
	if (oo) {
		const rg = ctx.createRadialGradient(W / 2, H * 0.95, H * 0.15, W / 2, H * 0.8, W * 0.75);
		rg.addColorStop(0, 'rgba(0,0,0,0)'); rg.addColorStop(1, 'rgba(0,0,0,0.55)');
		ctx.fillStyle = rg; ctx.fillRect(0, 0, W, H);
	}
	return P;
}
function klaas(ctx, W, H) {
	{
		ctx.fillStyle = 'rgba(255,255,255,0.12)'; ctx.fillRect(0, 0, W, H);
		ctx.strokeStyle = 'rgba(255,255,255,0.75)'; ctx.lineWidth = 1.5;
		const cx = W * 0.55, cy = H * 0.38;
		for (let i = 0; i < 11; i++) { const a = i * 0.57 + 0.2, l = H * (0.18 + (i % 4) * 0.08); ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(a) * l * 0.5, cy + Math.sin(a) * l * 0.5 + 6); ctx.lineTo(cx + Math.cos(a) * l, cy + Math.sin(a) * l); ctx.stroke(); }
		ctx.beginPath(); ctx.arc(cx, cy, H * 0.05, 0, 7); ctx.stroke();
	}
}

/* ---------- salong: juhi vaade (esiklaas, piilarid, armatuur, rool) ----------
   u = „maastikukaadri“ kõrgus: laial ekraanil H, kitsal (telefon püsti) W/1,6.
   Kõik salongi mõõdud u järgi, all keskel; nii ei kata armatuur telefonis pool pilti. */
function kokpit(W, H) {
	/* telefon püsti (kõrge ja kitsas): armatuur suuremaks, muidu jääb näidikud pisikeseks */
	const u = H > W ? Math.min(H * 0.55, W / 1.05) : Math.min(H, W / 1.6), cx = W / 2;
	const yd = H - 0.27 * u; /* armatuurlaua ülaserv */
	/* auto keskjoon ~0,8 m ees: juhist 0,37 m paremal */
	return { u, cx, yd, katus: 0.055 * u, ak: cx + 0.34 * W };
}

/* kapott paistab läbi klaasi armatuuri kohal */
function kapott(ctx, W, H, k, o) {
	const { u, yd } = k, cx = k.ak, oo = !!o.oo;
	const y1 = yd - 0.05 * u, y2 = yd + 0.02 * u;
	const g = ctx.createLinearGradient(0, y1, 0, y2);
	g.addColorStop(0, oo ? '#121821' : '#3d4f66'); g.addColorStop(1, oo ? '#07090c' : '#1f2a38');
	ctx.fillStyle = g;
	ctx.beginPath(); ctx.moveTo(0, y2); ctx.lineTo(0, yd - 0.005 * u); ctx.quadraticCurveTo(cx, y1 - 0.02 * u, W, yd - 0.005 * u); ctx.lineTo(W, y2); ctx.fill();
	/* läige kapoti serval */
	ctx.strokeStyle = oo ? 'rgba(255,255,255,0.06)' : 'rgba(255,255,255,0.22)'; ctx.lineWidth = Math.max(1, 0.004 * u);
	ctx.beginPath(); ctx.moveTo(W * 0.08, yd - 0.008 * u); ctx.quadraticCurveTo(cx, y1 - 0.012 * u, W, yd - 0.02 * u); ctx.stroke();
}

/* vihm / lumi esiklaasil + kojamehed. Olek moodulis: piisad jäävad klaasile, kuni klaasipuhasti üle käib. */
const KL = { piisad: [], t: null, ilm: '', nurk: 0 };
const KOJA_MAX = 1.75; /* kojamehe pöördenurk (rad) */
/* vasakpoolse rooliga autol on kojamehe teljed keskel ja paremal; rahuasendis näitavad vasakule
   ja tõusevad üles juhi poole */
function kojamehed(k, W) {
	const L = Math.min(0.62 * W, k.yd * 1.05);
	return [[W * 0.76, k.yd + 0.012 * k.u, L], [W * 1.2, k.yd + 0.012 * k.u, L * 0.92]];
}
function koja(t) {
	/* üles-alla 1,3 s, rahuasendis 0,3 s */
	const T = 1.6, p = (t % T) / T;
	if (p > 0.8125) return 0;
	const q = p / 0.8125;
	return KOJA_MAX * (1 - Math.cos(2 * Math.PI * q)) / 2;
}
function klaasIlm(ctx, W, H, k, o) {
	const t = o.aeg || 0, ilm = o.ilm, vihm = ilm === 'vihm', talv = ilm === 'talv', oo = !!o.oo;
	if (KL.t === null || t < KL.t || ilm !== KL.ilm) { KL.piisad = []; KL.t = t; KL.ilm = ilm; KL.nurk = Math.PI; }
	const dt = Math.min(0.1, t - KL.t); KL.t = t;
	const sadu = vihm || talv, kmh = o.kmh || 0, u = k.u;
	const nurk = Math.PI - (sadu ? koja(t) : 0), eel = KL.nurk || Math.PI; KL.nurk = nurk;
	const P = kojamehed(k, W);
	if (sadu) {
		/* uued piisad: sõites tabab klaasi rohkem */
		const kiirus = (vihm ? 26 : 9) * (0.5 + kmh / 70);
		let n = kiirus * dt; if (Math.random() < n % 1) n = Math.ceil(n); else n = Math.floor(n);
		for (let i = 0; i < n && KL.piisad.length < 320; i++) {
			KL.piisad.push({ x: Math.random() * W, y: k.katus + Math.random() * (k.yd - k.katus), r: (vihm ? 1.5 + Math.random() * 3 : 1.6 + Math.random() * 2.8) * u / 400, a: 1, s: t });
		}
		/* õhuvool lükkab piisku kiirel sõidul üles, lumi sulab vaikselt */
		const lukka = kmh > 45 ? (kmh - 45) * 0.0016 * u * dt : 0;
		const lo = Math.min(eel, nurk), hi = Math.max(eel, nurk);
		KL.piisad = KL.piisad.filter((d) => {
			d.y -= lukka * (d.r / (2 * u / 400));
			if (talv) d.a = Math.max(0, 1 - (t - d.s) / 9);
			if (d.y < k.katus || d.a <= 0) return false;
			for (const [px, py, L] of P) {
				const dx = d.x - px, dy = py - d.y, r = Math.hypot(dx, dy);
				if (r < L * 0.2 || r > L) continue;
				const f = Math.atan2(dy, dx); /* 0 = paremale, π/2 = üles */
				if (f >= lo - 0.03 && f <= hi + 0.03 && hi - lo > 0.0001) return false;
			}
			return true;
		});
		for (const d of KL.piisad) {
			if (talv) {
				ctx.fillStyle = `rgba(245,248,252,${0.75 * d.a})`;
				ctx.beginPath(); ctx.arc(d.x, d.y, d.r, 0, 7); ctx.fill();
			} else {
				ctx.fillStyle = oo ? 'rgba(200,215,240,0.10)' : 'rgba(225,235,245,0.20)';
				ctx.beginPath(); ctx.arc(d.x, d.y, d.r, 0, 7); ctx.fill();
				ctx.strokeStyle = 'rgba(0,0,0,0.28)'; ctx.lineWidth = Math.max(0.8, d.r * 0.35);
				ctx.beginPath(); ctx.arc(d.x, d.y, d.r * 0.8, 0.2 * Math.PI, 0.85 * Math.PI); ctx.stroke();
				ctx.fillStyle = oo ? 'rgba(255,240,210,0.55)' : 'rgba(255,255,255,0.8)';
				ctx.fillRect(d.x - d.r * 0.45, d.y - d.r * 0.5, Math.max(1, d.r * 0.35), Math.max(1, d.r * 0.35));
			}
		}
	} else KL.piisad = [];
	/* kojamehed (ka seistes on rahuasendis klaasi alaservas näha) */
	ctx.lineCap = 'round';
	for (const [px, py, L] of P) {
		const c = Math.cos(nurk), sn = -Math.sin(nurk);
		const ex = px + c * L, ey = py + sn * L;
		ctx.strokeStyle = '#0c0d10'; ctx.lineWidth = Math.max(2, 0.009 * u);
		ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(ex, ey); ctx.stroke();
		ctx.lineWidth = Math.max(3, 0.016 * u);
		ctx.beginPath(); ctx.moveTo(px + c * L * 0.22, py + sn * L * 0.22); ctx.lineTo(ex, ey); ctx.stroke();
	}
	ctx.lineCap = 'butt';
	/* armatuuri peegeldus klaasi alaosas (päeval) */
	if (!oo) {
		const g = ctx.createLinearGradient(0, k.yd - 0.12 * u, 0, k.yd);
		g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(255,255,255,0.07)');
		ctx.fillStyle = g; ctx.fillRect(0, k.yd - 0.12 * u, W, 0.12 * u);
	}
}

function salong(ctx, W, H, k, o) {
	const { u, cx, yd, katus } = k, oo = !!o.oo;
	const sis = oo ? '#0a0b0e' : '#1b1e24', sis2 = oo ? '#121419' : '#2a2e36';
	/* katus ja piilarid */
	ctx.fillStyle = sis;
	ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(W, 0); ctx.lineTo(W, katus * 1.5); ctx.quadraticCurveTo(cx, katus * 0.6, 0, katus * 1.5); ctx.fill();
	const pg = ctx.createLinearGradient(0, 0, W * 0.17, 0);
	pg.addColorStop(0, sis); pg.addColorStop(1, sis2);
	ctx.fillStyle = pg;
	ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(W * 0.17, 0); ctx.lineTo(W * 0.05, yd); ctx.lineTo(0, yd); ctx.fill();
	/* tahavaatepeegel */
	const mx = k.ak, mw = 0.3 * u, mh = 0.07 * u, my = katus + 0.035 * u;
	ctx.fillStyle = sis; ctx.fillRect(mx - 0.006 * u, katus * 0.8, 0.012 * u, my - katus * 0.8);
	ruut(ctx, mx - mw / 2, my, mw, mh, mh * 0.35); ctx.fillStyle = '#111317'; ctx.fill();
	const mg = ctx.createLinearGradient(0, my, 0, my + mh);
	if (oo) { mg.addColorStop(0, '#0b0e15'); mg.addColorStop(1, '#05060a'); }
	else if (o.ilm === 'talv') { mg.addColorStop(0, '#c9d2dc'); mg.addColorStop(1, '#8e98a3'); }
	else { mg.addColorStop(0, o.ilm === 'vihm' ? '#8a949e' : '#a9c8e6'); mg.addColorStop(0.55, '#5f6a62'); mg.addColorStop(1, '#3d4248'); }
	ruut(ctx, mx - mw / 2 + 0.008 * u, my + 0.008 * u, mw - 0.016 * u, mh - 0.016 * u, mh * 0.28); ctx.fillStyle = mg; ctx.fill();

	/* armatuurlaud */
	const dg = ctx.createLinearGradient(0, yd - 0.04 * u, 0, H);
	dg.addColorStop(0, sis2); dg.addColorStop(0.18, sis); dg.addColorStop(1, oo ? '#050607' : '#121418');
	ctx.fillStyle = dg;
	const bw = 0.42 * u; /* näidikuploki kapuuts */
	ctx.beginPath(); ctx.moveTo(0, H); ctx.lineTo(0, yd + 0.01 * u); ctx.quadraticCurveTo(W * 0.2, yd - 0.006 * u, cx - bw - 0.04 * u, yd);
	ctx.bezierCurveTo(cx - bw, yd - 0.005 * u, cx - bw * 0.85, yd - 0.06 * u, cx, yd - 0.06 * u);
	ctx.bezierCurveTo(cx + bw * 0.85, yd - 0.06 * u, cx + bw, yd - 0.005 * u, cx + bw + 0.04 * u, yd);
	ctx.quadraticCurveTo(W * 0.8, yd - 0.006 * u, W, yd + 0.01 * u); ctx.lineTo(W, H); ctx.fill();
	/* õhuavad servades ja keskel */
	ctx.fillStyle = oo ? '#040506' : '#0d0f12';
	for (const ax of [W * 0.04, k.ak - 0.07 * u]) { ruut(ctx, ax, yd + 0.05 * u, Math.min(W * 0.08, 0.14 * u), 0.035 * u, 0.012 * u); ctx.fill(); }

	/* keskekraan auto keskel (juhist paremal) */
	{
		const ew = 0.3 * u, eh = 0.15 * u, ey = yd - 0.07 * u, ex = Math.min(k.ak - 0.02 * u, W - ew / 2 - 0.02 * u); /* kitsal ekraanil ei lõigu servast ära */
		ruut(ctx, ex - ew / 2 - 0.008 * u, ey - 0.008 * u, ew + 0.016 * u, eh + 0.016 * u, 0.02 * u); ctx.fillStyle = '#050608'; ctx.fill();
		const eg = ctx.createLinearGradient(ex - ew / 2, ey, ex + ew / 2, ey + eh);
		eg.addColorStop(0, oo ? '#0c1422' : '#13202f'); eg.addColorStop(1, oo ? '#070b12' : '#0b121b');
		ruut(ctx, ex - ew / 2, ey, ew, eh, 0.014 * u); ctx.fillStyle = eg; ctx.fill();
		/* navigatsioon: päris tee eespool pealtvaates (sama tee, mis klaasist paistab), auto nool all keskel */
		const ox = ex, oy = ey + eh - 0.035 * u, sc = (eh * 0.85) / 220;
		ctx.save();
		ruut(ctx, ex - ew / 2, ey, ew, eh, 0.014 * u); ctx.clip();
		if (k.tee && k.tee.length > 2) {
			const tee = k.tee.filter((p) => p.zr <= 260);
			const joon = (laius, varv) => {
				ctx.strokeStyle = varv; ctx.lineWidth = laius; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
				ctx.beginPath();
				tee.forEach((p, i) => { const x = ox + p.x * sc, y = oy - p.zr * sc; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
				ctx.stroke();
			};
			joon(0.03 * u, oo ? '#1d2a3c' : '#22344a'); /* tee */
			joon(0.012 * u, oo ? '#2f6fb8' : '#3b82d6'); /* marsruut */
		}
		ctx.restore();
		ctx.lineCap = 'butt';
		ctx.fillStyle = '#4da3ff'; ctx.beginPath(); ctx.moveTo(ox, oy - 0.03 * u); ctx.lineTo(ox - 0.016 * u, oy + 0.004 * u); ctx.lineTo(ox + 0.016 * u, oy + 0.004 * u); ctx.fill();
		const kell = new Date(); ctx.fillStyle = '#c9d3e0'; ctx.textAlign = 'left';
		ctx.font = `600 ${Math.round(0.026 * u)}px "Barlow Condensed", "Arial Narrow", sans-serif`;
		ctx.fillText(String(kell.getHours()).padStart(2, '0') + ':' + String(kell.getMinutes()).padStart(2, '0'), ex - ew / 2 + 0.015 * u, ey + 0.035 * u);
		if (!oo) { ctx.fillStyle = 'rgba(255,255,255,0.05)'; ctx.beginPath(); ctx.moveTo(ex - ew / 2, ey); ctx.lineTo(ex, ey); ctx.lineTo(ex - ew / 2, ey + eh); ctx.fill(); }
	}
	/* näidikuplokk */
	const nx = cx, ny = yd + 0.115 * u, R = 0.1 * u;
	ruut(ctx, cx - 0.37 * u, yd + 0.004 * u, 0.74 * u, 0.25 * u, 0.06 * u); ctx.fillStyle = '#07080a'; ctx.fill();
	const kmh = Math.max(0, o.kmh || 0);
	const rpm = kmh < 2 ? 0.8 : (() => { const g = [0, 18, 38, 62, 88, 118, 999]; let i = 1; while (kmh > g[i]) i++; const lo = g[i - 1], hi = Math.min(g[i], lo + 40); return 1.3 + Math.min(1, (kmh - lo) / (hi - lo)) * 1.6 + i * 0.12; })();
	naidik(ctx, nx - 0.205 * u, ny, R, rpm, 8, 1, 1, 6.5, '×1000 rpm', oo);
	naidik(ctx, nx + 0.205 * u, ny, R, kmh, 220, 10, 40, 0, 'km/h', oo);
	/* keskmine ekraan: kiirus numbrina, käik, välistemperatuur */
	const tmp = o.ilm === 'talv' ? -6 : o.ilm === 'vihm' ? 7 : 14;
	ruut(ctx, nx - 0.085 * u, ny - 0.07 * u, 0.17 * u, 0.14 * u, 0.02 * u); ctx.fillStyle = '#0e1116'; ctx.fill();
	ctx.textAlign = 'center';
	ctx.fillStyle = kmh < 2.5 ? '#4ade80' : '#f4f6fa';
	ctx.font = `700 ${Math.round(0.07 * u)}px "Barlow Condensed", "Arial Narrow", sans-serif`;
	ctx.fillText(String(Math.round(kmh)), nx, ny + 0.02 * u);
	ctx.fillStyle = '#9aa3b2'; ctx.font = `600 ${Math.round(0.022 * u)}px "Barlow Condensed", "Arial Narrow", sans-serif`;
	ctx.fillText('km/h', nx, ny + 0.045 * u);
	ctx.fillText('D', nx - 0.06 * u, ny - 0.045 * u);
	ctx.fillStyle = tmp <= 3 ? '#7cc4ff' : '#9aa3b2';
	ctx.fillText((tmp <= 3 ? '❄ ' : '') + (tmp < 0 ? '−' + Math.abs(tmp) : tmp) + '°C', nx + 0.045 * u, ny - 0.045 * u);
	/* märgutuled: lähituled (Eestis alati), ohutuled pärast avariid / seisma jäädes */
	const ly = yd + 0.215 * u, ls = 0.016 * u;
	lahituli(ctx, nx - 0.03 * u, ly, ls);
	if (o.crash && (o.aeg || 0) % 1 < 0.6) ohutuli(ctx, nx + 0.03 * u, ly, ls);

	/* rool: ülemine kaar paistab, näidikud selle vahelt */
	const rx = cx, ry = H + 0.42 * u, rr = 0.74 * u;
	ctx.strokeStyle = oo ? '#08090b' : '#141518'; ctx.lineWidth = 0.07 * u;
	ctx.beginPath(); ctx.arc(rx, ry, rr, Math.PI * 1.15, Math.PI * 1.85); ctx.stroke();
	ctx.strokeStyle = oo ? 'rgba(255,255,255,0.04)' : 'rgba(255,255,255,0.10)'; ctx.lineWidth = Math.max(1, 0.006 * u);
	ctx.beginPath(); ctx.arc(rx, ry, rr + 0.025 * u, Math.PI * 1.2, Math.PI * 1.8); ctx.stroke();
	ctx.textAlign = 'left';
}

function ruut(ctx, x, y, w, h, r) {
	ctx.beginPath(); ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r);
	ctx.lineTo(x + w, y + h - r); ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h); ctx.lineTo(x + r, y + h);
	ctx.quadraticCurveTo(x, y + h, x, y + h - r); ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y); ctx.closePath();
}
/* ümar näidik: 0 all vasakul, max all paremal (270°) */
function naidik(ctx, x, y, R, val, max, peen, silt, punane, yhik, oo) {
	const a0 = Math.PI * 0.75, a1 = Math.PI * 2.25, nurk = (v) => a0 + (Math.min(max, Math.max(0, v)) / max) * (a1 - a0);
	ctx.fillStyle = '#0a0c10'; ctx.beginPath(); ctx.arc(x, y, R, 0, 7); ctx.fill();
	ctx.strokeStyle = '#2c313a'; ctx.lineWidth = R * 0.05; ctx.beginPath(); ctx.arc(x, y, R * 0.97, 0, 7); ctx.stroke();
	if (punane) { ctx.strokeStyle = '#d63a2a'; ctx.lineWidth = R * 0.07; ctx.beginPath(); ctx.arc(x, y, R * 0.84, nurk(punane), a1); ctx.stroke(); }
	const hele = oo ? '#f4f1ea' : '#dfe3ea';
	ctx.strokeStyle = hele; ctx.fillStyle = hele; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
	ctx.font = `600 ${Math.round(R * 0.2)}px "Barlow Condensed", "Arial Narrow", sans-serif`;
	for (let v = 0; v <= max + 1e-6; v += peen) {
		const a = nurk(v), suur = Math.abs(v / silt - Math.round(v / silt)) < 1e-6;
		ctx.lineWidth = suur ? R * 0.035 : R * 0.018;
		ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * R * (suur ? 0.76 : 0.82), y + Math.sin(a) * R * (suur ? 0.76 : 0.82)); ctx.lineTo(x + Math.cos(a) * R * 0.9, y + Math.sin(a) * R * 0.9); ctx.stroke();
		if (suur) ctx.fillText(String(v), x + Math.cos(a) * R * 0.6, y + Math.sin(a) * R * 0.6);
	}
	ctx.fillStyle = '#7d8696'; ctx.font = `600 ${Math.round(R * 0.13)}px "Barlow Condensed", "Arial Narrow", sans-serif`;
	ctx.fillText(yhik, x, y + R * 0.42);
	/* nõel */
	const a = nurk(val);
	ctx.strokeStyle = '#ff6a2a'; ctx.lineWidth = R * 0.045; ctx.lineCap = 'round';
	ctx.beginPath(); ctx.moveTo(x - Math.cos(a) * R * 0.12, y - Math.sin(a) * R * 0.12); ctx.lineTo(x + Math.cos(a) * R * 0.86, y + Math.sin(a) * R * 0.86); ctx.stroke();
	ctx.lineCap = 'butt';
	ctx.fillStyle = '#20242b'; ctx.beginPath(); ctx.arc(x, y, R * 0.09, 0, 7); ctx.fill();
	ctx.textBaseline = 'alphabetic';
}
function lahituli(ctx, x, y, s) {
	ctx.strokeStyle = '#3ddc68'; ctx.fillStyle = '#3ddc68'; ctx.lineWidth = Math.max(1, s * 0.16);
	ctx.beginPath(); ctx.moveTo(x - s * 0.1, y - s * 0.55); ctx.quadraticCurveTo(x - s * 0.8, y, x - s * 0.1, y + s * 0.55); ctx.closePath(); ctx.fill();
	for (const d of [-0.4, 0, 0.4]) { ctx.beginPath(); ctx.moveTo(x + s * 0.1, y + d * s); ctx.lineTo(x + s * 0.75, y + d * s + s * 0.18); ctx.stroke(); }
}
function ohutuli(ctx, x, y, s) {
	ctx.strokeStyle = '#ff4b3a'; ctx.lineWidth = Math.max(1, s * 0.18);
	ctx.beginPath(); ctx.moveTo(x, y - s * 0.6); ctx.lineTo(x + s * 0.65, y + s * 0.5); ctx.lineTo(x - s * 0.65, y + s * 0.5); ctx.closePath(); ctx.stroke();
}

function objekt(ctx, ob, sx, sy, sc, L, udu, uduVarv, e) {
	const V = (c, l = L) => v(c, l, udu, uduVarv);
	const m = (x) => x * sc; /* meetrid → pikslid */
	switch (ob.t) {
		case 'post': {
			ctx.fillStyle = V('#e8e8e2'); ctx.fillRect(sx - m(0.06), sy - m(1), m(0.12), m(1));
			ctx.fillStyle = e.oo && e.zr < 110 ? `rgba(255,${ob.x < 0 ? 255 : 120},${ob.x < 0 ? 255 : 60},${kl(1 - e.zr / 110, 0.2, 1)})` : V('#333');
			ctx.fillRect(sx - m(0.05), sy - m(0.95), m(0.1), m(0.12));
			break;
		}
		case 'kuusk': {
			const h = ob.h, w = h * 0.38;
			ctx.fillStyle = V('#3b2a1c'); ctx.fillRect(sx - m(0.2), sy - m(h * 0.18), m(0.4), m(h * 0.18));
			const c = e.talv ? ['#2f4a3a', '#e9eef3'] : [ob.v < 0.5 ? '#1f3d26' : '#24472b', null];
			for (let k = 0; k < 4; k++) {
				const yb = sy - m(h * (0.12 + k * 0.2)), ww = w * (1 - k * 0.2);
				ctx.fillStyle = V(c[0]); ctx.beginPath(); ctx.moveTo(sx - m(ww / 2), yb); ctx.lineTo(sx + m(ww / 2), yb); ctx.lineTo(sx, yb - m(h * 0.34)); ctx.fill();
				if (c[1]) { ctx.fillStyle = V(c[1]); ctx.beginPath(); ctx.moveTo(sx - m(ww * 0.25), yb - m(h * 0.12)); ctx.lineTo(sx + m(ww * 0.25), yb - m(h * 0.12)); ctx.lineTo(sx, yb - m(h * 0.34)); ctx.fill(); }
			}
			break;
		}
		case 'kask': case 'poos': {
			const h = ob.h;
			ctx.fillStyle = V(ob.t === 'kask' ? '#e8e4da' : '#4a3a2a'); ctx.fillRect(sx - m(0.15), sy - m(h * 0.55), m(0.3), m(h * 0.55));
			ctx.fillStyle = V(e.talv ? '#c9d0d6' : ob.t === 'kask' ? '#5d8a3c' : '#3f6b33');
			ctx.beginPath(); ctx.ellipse(sx, sy - m(h * 0.7), m(h * 0.28), m(h * 0.32), 0, 0, 7); ctx.fill();
			break;
		}
		case 'maja': {
			const w = ob.w, h = ob.h;
			const sein = ['#c9b79c', '#9fb0a6', '#b98d6f', '#d9d4c6'][Math.floor(ob.v * 4)];
			ctx.fillStyle = V(sein); ctx.fillRect(sx - m(w / 2), sy - m(h), m(w), m(h));
			ctx.fillStyle = V(e.talv ? '#eef2f6' : '#5a3b32'); ctx.beginPath(); ctx.moveTo(sx - m(w / 2 + 0.4), sy - m(h)); ctx.lineTo(sx + m(w / 2 + 0.4), sy - m(h)); ctx.lineTo(sx, sy - m(h + 2.6)); ctx.fill();
			for (let k = 0; k < 3; k++) {
				const lit = e.oo && (ob.aken * 3 + k) % 3 < 1.6;
				ctx.fillStyle = lit ? '#ffd27a' : V('#2b3440');
				ctx.fillRect(sx - m(w / 2) + m(w * (0.15 + k * 0.28)), sy - m(h * 0.68), m(w * 0.16), m(h * 0.26));
			}
			break;
		}
		case 'aed': {
			ctx.fillStyle = V('#8a6e4e'); ctx.fillRect(sx - m(0.05), sy - m(1.1), m(0.1), m(1.1));
			ctx.fillRect(sx - m(2.5), sy - m(0.85), m(5), m(0.08));
			break;
		}
		case 'lamp': {
			ctx.fillStyle = V('#5d636d', Math.max(L, 0.35)); ctx.fillRect(sx - m(0.08), sy - m(7), m(0.16), m(7));
			ctx.fillRect(sx - m(1.4), sy - m(7), m(1.4), m(0.15));
			if (e.oo) { const lg = ctx.createRadialGradient(sx - m(1.3), sy - m(6.9), 0, sx - m(1.3), sy - m(6.9), m(2.5)); lg.addColorStop(0, 'rgba(255,214,140,0.9)'); lg.addColorStop(1, 'rgba(255,214,140,0)'); ctx.fillStyle = lg; ctx.fillRect(sx - m(4), sy - m(9.5), m(5.5), m(5)); }
			break;
		}
		case 'parkauto': auto(ctx, sx, sy, sc, L, V, { varv: ob.varv || '#46505e', pidur: false, oo: e.oo, kulg: true }); break;
		case 'auto': auto(ctx, sx, sy, sc, L, V, { varv: '#9aa4b0', pidur: ob.pidur, oo: e.oo }); break;
		case 'inim': inimene(ctx, sx, sy, sc, L, V, ob, e); break;
	}
}

/* eesolev auto tagantvaates: kere varjundiga, tagaklaas, tuled, numbrimärk */
function auto(ctx, sx, sy, sc, L, V, o) {
	const m = (x) => x * sc, w = 1.8, h = 1.45;
	ctx.fillStyle = 'rgba(0,0,0,0.35)'; ctx.beginPath(); ctx.ellipse(sx, sy, m(w * 0.62), m(0.18), 0, 0, 7); ctx.fill();
	ctx.fillStyle = V('#14161a'); ctx.fillRect(sx - m(w * 0.46), sy - m(0.32), m(0.32), m(0.32)); ctx.fillRect(sx + m(w * 0.46 - 0.32), sy - m(0.32), m(0.32), m(0.32));
	const kg = ctx.createLinearGradient(0, sy - m(h), 0, sy - m(0.2));
	kg.addColorStop(0, V(o.varv, L * 0.8)); kg.addColorStop(0.5, V(o.varv)); kg.addColorStop(1, V(o.varv, L * 0.6));
	ctx.fillStyle = kg;
	const r = m(0.18);
	ctx.beginPath(); ctx.moveTo(sx - m(w / 2) + r, sy - m(0.85)); ctx.lineTo(sx + m(w / 2) - r, sy - m(0.85)); ctx.quadraticCurveTo(sx + m(w / 2), sy - m(0.85), sx + m(w / 2), sy - m(0.7));
	ctx.lineTo(sx + m(w / 2), sy - m(0.3)); ctx.lineTo(sx - m(w / 2), sy - m(0.3)); ctx.lineTo(sx - m(w / 2), sy - m(0.7)); ctx.quadraticCurveTo(sx - m(w / 2), sy - m(0.85), sx - m(w / 2) + r, sy - m(0.85)); ctx.fill();
	ctx.beginPath(); ctx.moveTo(sx - m(w * 0.42), sy - m(0.85)); ctx.lineTo(sx - m(w * 0.32), sy - m(h)); ctx.lineTo(sx + m(w * 0.32), sy - m(h)); ctx.lineTo(sx + m(w * 0.42), sy - m(0.85)); ctx.fill();
	/* tagaklaas */
	ctx.fillStyle = V('#1d2733', Math.max(L, 0.2)); ctx.beginPath(); ctx.moveTo(sx - m(w * 0.37), sy - m(0.9)); ctx.lineTo(sx - m(w * 0.29), sy - m(h - 0.06)); ctx.lineTo(sx + m(w * 0.29), sy - m(h - 0.06)); ctx.lineTo(sx + m(w * 0.37), sy - m(0.9)); ctx.fill();
	/* numbrimärk */
	ctx.fillStyle = V('#e9edf1'); ctx.fillRect(sx - m(0.26), sy - m(0.55), m(0.52), m(0.12));
	ctx.fillStyle = V('#1f4fb3'); ctx.fillRect(sx - m(0.26), sy - m(0.55), m(0.05), m(0.12));
	if (o.kulg) return;
	/* tagatuled: öösel alati põlevad, pidurdades eredad + kolmas pidurituli */
	const tuli = (x, w2, h2, y) => { ctx.fillRect(sx + m(x), sy - m(y), m(w2), m(h2)); };
	/* tagatuled põlevad alati (ka päeval), pidurdades veidi eredamad — nagu päriselt, et kohe aru ei saaks */
	const ere = o.pidur ? 1 : 0.62;
	ctx.fillStyle = `rgba(255,${o.pidur ? 45 : 35},${o.pidur ? 40 : 30},${0.6 + ere * 0.4})`;
	tuli(-w * 0.49, 0.42, 0.14, 0.78); tuli(w * 0.49 - 0.42, 0.42, 0.14, 0.78);
	if (o.pidur) tuli(-0.25, 0.5, 0.05, h - 0.02);
	if (ere) {
		for (const xx of [-w * 0.28, w * 0.28]) {
			const gg = ctx.createRadialGradient(sx + m(xx), sy - m(0.72), 0, sx + m(xx), sy - m(0.72), m(o.pidur ? 0.8 : 0.6));
			gg.addColorStop(0, `rgba(255,40,40,${(o.pidur ? 0.42 : 0.3) * (o.oo ? 1 : 0.6)})`); gg.addColorStop(1, 'rgba(255,40,40,0)');
			ctx.fillStyle = gg; ctx.fillRect(sx + m(xx) - m(1.2), sy - m(1.9), m(2.4), m(2.4));
		}
	}
}

/* jalakäija kõnnib (kond = sammu faas), riietus: tume | hele | helkur */
function inimene(ctx, sx, sy, sc, L, V, ob, e) {
	const m = (x) => x * sc;
	const tume = ob.riie !== 'hele';
	const keha = tume ? '#2c2f36' : '#d9d5c7', jalad = tume ? '#24262b' : '#bdb8a8', pea = '#c9a58a';
	const f = Math.sin(ob.kond || 0);
	ctx.strokeStyle = V(jalad); ctx.lineWidth = Math.max(1, m(0.14)); ctx.lineCap = 'round';
	ctx.beginPath(); ctx.moveTo(sx, sy - m(0.9)); ctx.lineTo(sx + m(0.25 * f), sy); ctx.moveTo(sx, sy - m(0.9)); ctx.lineTo(sx - m(0.25 * f), sy); ctx.stroke();
	ctx.fillStyle = V(keha); ctx.fillRect(sx - m(0.22), sy - m(1.5), m(0.44), m(0.65));
	ctx.strokeStyle = V(keha); ctx.lineWidth = Math.max(1, m(0.11));
	ctx.beginPath(); ctx.moveTo(sx - m(0.2), sy - m(1.42)); ctx.lineTo(sx - m(0.2 + 0.15 * f), sy - m(0.95)); ctx.moveTo(sx + m(0.2), sy - m(1.42)); ctx.lineTo(sx + m(0.2 - 0.15 * f), sy - m(0.95)); ctx.stroke();
	ctx.fillStyle = V(pea); ctx.beginPath(); ctx.arc(sx, sy - m(1.66), m(0.13), 0, 7); ctx.fill();
	if (ob.riie === 'helkur' && e.oo && e.zr < 150) {
		const a = kl(1.15 - e.zr / 150, 0.35, 1);
		ctx.fillStyle = `rgba(255,252,220,${a})`;
		ctx.beginPath(); ctx.arc(sx + m(0.24), sy - m(1.0), Math.max(2.5, m(0.09)), 0, 7); ctx.fill();
		ctx.beginPath(); ctx.arc(sx - m(0.1), sy - m(0.3), Math.max(2, m(0.06)), 0, 7); ctx.fill();
		ctx.fillRect(sx - m(0.22), sy - m(1.12), m(0.44), Math.max(1, m(0.05)));
		const gg = ctx.createRadialGradient(sx + m(0.24), sy - m(1), 0, sx + m(0.24), sy - m(1), Math.max(14, m(0.5)));
		gg.addColorStop(0, `rgba(255,252,220,${a * 0.6})`); gg.addColorStop(1, 'rgba(255,252,220,0)');
		ctx.fillStyle = gg; ctx.fillRect(sx + m(0.24) - Math.max(14, m(0.6)), sy - m(1) - Math.max(14, m(0.6)), 2 * Math.max(14, m(0.6)), 2 * Math.max(14, m(0.6)));
	}
}

export const TEE = { SEG, N, TEE_L, KAAM_X };
