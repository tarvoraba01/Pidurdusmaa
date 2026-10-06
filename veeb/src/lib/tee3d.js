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
const KAAM_X = TEE_L / 2; /* kaamera sinu raja keskel (paremal) */
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
		? { t: 'parkauto', x: pool * (TEE_L + 1.3) }
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

export function joonista(ctx, W, H, tee, o) {
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
	const z0 = Math.max(0, o.z || 0), base = Math.floor(z0 / SEG), frac = (z0 % SEG) / SEG;
	const sg = (n) => tee.seg[((n % N) + N) % N];
	const P = [];
	let x = 0, dx = -sg(base).k * frac;
	for (let n = 0; n <= NAHE; n++) {
		const s = sg(base + n);
		const zr = n * SEG - frac * SEG; /* kaugus kaamerast lõigu alguseni */
		P.push({ zr: Math.max(0.1, zr), x, s, n: base + n });
		x += dx; dx += s.k;
	}
	const proj = (wx, wy, zr) => { const sc = D / Math.max(0.3, zr); return [W / 2 + (wx - KAAM_X) * sc, hor + (KAAM_H - wy) * sc, sc]; };
	/* laternate valgus lõikudes (küla, öö) */
	const lampL = (n) => {
		if (!oo || tee.maastik !== 'kula') return 0;
		const k = ((n % 12) + 12) % 12, d = Math.min(Math.abs(k - 6), 12 - Math.abs(k - 6));
		return d < 3 ? 0.28 * (1 - d / 3) : 0;
	};

	/* ---- tee (kaugelt lähedale) ---- */
	for (let i = P.length - 2; i >= 0; i--) {
		const a = P[i], b = P[i + 1];
		if (a.zr < 0.5 && i > 0) continue;
		const [ax, ay, as] = proj(a.x, 0, a.zr), [bx, by, bs] = proj(b.x, 0, b.zr);
		if (by >= ay) continue;
		const L = valgus(a.zr, oo, lampL(a.n)), udu = kl(a.zr * uduK, 0, 0.85);
		const tri = (x1, w1, x2, w2, c) => { ctx.fillStyle = c; ctx.beginPath(); ctx.moveTo(ax + x1 * as, ay); ctx.lineTo(ax + (x1 + w1) * as, ay); ctx.lineTo(bx + (x2 + w2) * bs, by); ctx.lineTo(bx + x2 * bs, by); ctx.fill(); };
		/* serv (muru/lumi) vöödena */
		const vood = Math.floor(a.n / 2) % 2;
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
		const i = Math.max(0, Math.min(P.length - 2, Math.floor((zr + frac * SEG) / SEG)));
		const a = P[i], b = P[i + 1], k = kl((zr - a.zr) / Math.max(0.01, b.zr - a.zr), 0, 1);
		return a.x + (b.x - a.x) * k;
	};
	if (o.ees && o.ees.gap < 520) asjad.push({ zr: o.ees.gap + 0.5, x: xAt(o.ees.gap + 0.5) + KAAM_X, ob: { t: 'auto', pidur: o.ees.pidur }, n: 0 });
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
		ctx.strokeStyle = 'rgba(190,205,230,0.45)';
		for (let i = 0; i < n; i++) {
			const sx = (Math.sin(i * 12.9898) * 43758.5453) % 1, sy = (Math.sin(i * 78.233) * 12345.678) % 1;
			let px = ((Math.abs(sx) + t * (talv ? 0.03 : 0.01) * (i % 3 - 1)) % 1) * W;
			let py = ((Math.abs(sy) + t * (talv ? 0.25 + kiir * 0.4 : 1.6)) % 1) * H;
			/* kiirusega laiali keskelt */
			px = W / 2 + (px - W / 2) * (1 + ((py / H) * kiir) * 0.3);
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

	/* ---- oma auto kapott + kiirus ---- */
	kapott(ctx, W, H, o, oo);

	/* ---- kokkupõrge ---- */
	if (o.crash) {
		ctx.fillStyle = 'rgba(255,255,255,0.12)'; ctx.fillRect(0, 0, W, H);
		ctx.strokeStyle = 'rgba(255,255,255,0.75)'; ctx.lineWidth = 1.5;
		const cx = W * 0.55, cy = H * 0.38;
		for (let i = 0; i < 11; i++) { const a = i * 0.57 + 0.2, l = H * (0.18 + (i % 4) * 0.08); ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(a) * l * 0.5, cy + Math.sin(a) * l * 0.5 + 6); ctx.lineTo(cx + Math.cos(a) * l, cy + Math.sin(a) * l); ctx.stroke(); }
		ctx.beginPath(); ctx.arc(cx, cy, H * 0.05, 0, 7); ctx.stroke();
	}
}

function kapott(ctx, W, H, o, oo) {
	const y0 = H * 0.9;
	ctx.fillStyle = oo ? '#07080b' : '#15171c';
	ctx.beginPath(); ctx.moveTo(0, H); ctx.lineTo(0, y0 + H * 0.03); ctx.quadraticCurveTo(W / 2, y0 - H * 0.035, W, y0 + H * 0.03); ctx.lineTo(W, H); ctx.fill();
	ctx.fillStyle = 'rgba(255,255,255,0.05)';
	ctx.beginPath(); ctx.moveTo(W * 0.2, y0 + H * 0.02); ctx.quadraticCurveTo(W / 2, y0 - H * 0.02, W * 0.8, y0 + H * 0.02); ctx.lineTo(W * 0.8, y0 + H * 0.03); ctx.quadraticCurveTo(W / 2, y0 - H * 0.01, W * 0.2, y0 + H * 0.03); ctx.fill();
	/* spidomeeter */
	const kmh = Math.round(o.kmh || 0);
	ctx.fillStyle = 'rgba(0,0,0,0.55)'; const bw = W * 0.15, bh = H * 0.075;
	ctx.fillRect(W / 2 - bw / 2, H - bh - H * 0.015, bw, bh);
	ctx.fillStyle = kmh < 3 ? '#4ade80' : '#ffc20e'; ctx.font = `700 ${Math.round(H * 0.05)}px "Barlow Condensed", "Arial Narrow", sans-serif`; ctx.textAlign = 'center';
	ctx.fillText(kmh + ' km/h', W / 2, H - H * 0.03); ctx.textAlign = 'left';
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
		case 'parkauto': auto(ctx, sx, sy, sc, L, V, { varv: '#46505e', pidur: false, oo: e.oo, kulg: true }); break;
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
	const ere = o.pidur ? 1 : o.oo ? 0.45 : 0;
	ctx.fillStyle = ere ? `rgba(255,${o.pidur ? 40 : 30},${o.pidur ? 40 : 30},${0.55 + ere * 0.45})` : V('#5a1c1c');
	tuli(-w * 0.49, 0.42, 0.14, 0.78); tuli(w * 0.49 - 0.42, 0.42, 0.14, 0.78);
	if (o.pidur) tuli(-0.25, 0.5, 0.05, h - 0.02);
	if (ere) {
		for (const xx of [-w * 0.28, w * 0.28]) {
			const gg = ctx.createRadialGradient(sx + m(xx), sy - m(0.72), 0, sx + m(xx), sy - m(0.72), m(o.pidur ? 1.1 : 0.6));
			gg.addColorStop(0, `rgba(255,40,40,${o.pidur ? 0.55 : 0.25})`); gg.addColorStop(1, 'rgba(255,40,40,0)');
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
