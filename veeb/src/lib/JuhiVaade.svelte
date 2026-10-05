<script>
	/* Pimedas: JUHI VAADE (esimese isiku vaade läbi tuuleklaasi).
	   Sama stseen mis pealtvaates (SirgeAnimatsioon): auto teekond ajas tuleb
	   samast arvutusmootorist (sõidab → märkad → reageerid → pidurdad → seisad).

	   Jalakäija nähtavus järgib sama mudelit: jalakäija sulandub taustaga, kuni
	   kaugus on suurem kui Transpordiameti märkamiskaugus D (tume 30 m, hele 45 m,
	   helkur 140 m, kaugtuled + helkur 325 m). Esitulede valgus, märg asfalt,
	   vihm, lumi ja jää on ainult pilt — need ei muuda numbreid.

	   props: stseen (pimedas-stseen), D (märkamiskaugus m), naeb ('tume'|'hele'|'helkur'|'kaug') */
	import { onMount, untrack } from 'svelte';

	let { stseen, D = 30, naeb = 'tume', vesi = 0, t, LOC = 'et-EE' } = $props();

	const kaug = $derived(naeb === 'kaug');
	const helkur = $derived(naeb === 'helkur' || naeb === 'kaug');
	const hele = $derived(naeb === 'hele');
	const pind = $derived(stseen?.pind || 'kuiv');
	const tee = $derived(stseen?.teed?.[0] || null);
	const rada = $derived(tee?.autod?.[0]?.rada || null);

	/* ---------- geomeetria (meetrites) ---------- */
	const SILM = 1.2; // silmade kõrgus
	const KAM_X = -0.35; // juht istub raja keskelt veidi vasakul
	const SILM_TAGA = 1.9; // silmad auto esiotsast tagapool
	const JK_X = 0.9; // jalakäija sinu raja paremas servas
	const SERV_P = 1.75, KESK = -1.75, SERV_V = -5.25;
	const EEL = 3.2; // eelnev sõit enne märkamiskaugust (s)

	let laius = $state(800), korgus = $state(500);
	let canvas, figEl, taust;
	const mob = $derived(laius < 560);

	/* ---------- valgus ja pinnad ---------- */
	const sujuv = (a, b, x) => { const k = Math.min(1, Math.max(0, (x - a) / (b - a))); return k * k * (3 - 2 * k); };
	/* esitulede valgustus maapinnal punktis (z ette, X külg) 0..1 */
	function valgus(z, X, h = 0) {
		if (z <= 0.6) return 0;
		const R = kaug ? 110 : 30;
		let lz = sujuv(1.2, 7, z) * Math.exp(-Math.max(0, z - 8) / R);
		const c = kaug ? -0.6 : 0.4 + z * 0.012;
		const s = (kaug ? 3.4 : 2.3) + z * (kaug ? 0.11 : 0.085);
		let lx = Math.exp(-(((X - c) / s) ** 2));
		/* lähituled: vastassuunda ei pimestata — vasak pool lõigatud */
		if (!kaug && X < -1.4) lx *= Math.exp(-Math.max(0, z - 12) / 7);
		/* lähitulede valgus jääb madalaks: kaugemal valgustab ainult jalgu */
		if (!kaug && h > 0.5) lz *= Math.exp(-Math.max(0, h - 0.5) * Math.max(0, z - 18) / 22);
		return Math.min(1, lz * lx);
	}
	const lumine = $derived(pind === 'lumi');
	const marg = $derived(pind === 'marg');
	const jaa = $derived(pind === 'jaa');
	const kruus = $derived(pind === 'kruus');
	const jooned = $derived(!lumine && !kruus);
	function pinnaAlbeedo(X) {
		if (X > SERV_V && X < SERV_P) return lumine ? [0.5, 0.52, 0.56] : jaa ? [0.2, 0.25, 0.31] : kruus ? [0.2, 0.18, 0.15] : marg ? [0.045, 0.047, 0.052] : [0.11, 0.11, 0.115];
		if ((X >= SERV_P && X < SERV_P + 1.0) || (X <= SERV_V && X > SERV_V - 1.0)) return lumine || jaa ? [0.7, 0.72, 0.76] : [0.22, 0.2, 0.17];
		return lumine || jaa ? [0.78, 0.8, 0.84] : [0.06, 0.085, 0.05];
	}
	const AMB = $derived(lumine || jaa ? 26 : 9);
	function pinnaVarv(z, X) {
		const a = pinnaAlbeedo(X), L = valgus(z, X);
		const k = AMB + 255 * 5.2 * L;
		return [tm(a[0] * k), tm(a[1] * k * 0.97), tm(a[2] * k * 0.9)];
	}
	/* pehme tooni piiramine: hele lumi ei põle valgeks, valguslaigul on üleminek */
	const tm = (v) => 255 * (1 - Math.exp(-Math.max(0, v) / 190));
	const rgb = (c, a = 1) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a})`;
	const segu = (a, b, k) => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];

	/* ---------- projektsioon ---------- */
	let f = 600, yH = 220;
	function ekraan(z, X, h = 0, nyok = 0) {
		return [laius / 2 + (f * (X - KAM_X)) / z, yH + nyok + (f * (SILM - h)) / z];
	}

	/* staatiline kiht: taevas, mets, tee koos esitulede valgusega (valgus liigub autoga kaasa) */
	function joonistaTaust() {
		if (!canvas) return;
		const dpr = Math.min(2, window.devicePixelRatio || 1);
		taust = taust || document.createElement('canvas');
		taust.width = Math.round(laius * dpr);
		taust.height = Math.round((korgus + 40) * dpr);
		const g = taust.getContext('2d');
		g.setTransform(dpr, 0, 0, dpr, 0, 0);
		const H = korgus + 40, yh = yH + 20;
		/* taevas */
		const sky = g.createLinearGradient(0, 0, 0, yh);
		sky.addColorStop(0, lumine ? '#0b1018' : '#04060a');
		sky.addColorStop(1, lumine ? '#1c2533' : marg ? '#0e131b' : '#0b111b');
		g.fillStyle = sky;
		g.fillRect(0, 0, laius, yh + 1);
		/* metsaserv silmapiiril */
		g.fillStyle = lumine ? '#0a0f12' : '#030506';
		g.beginPath();
		g.moveTo(0, yh);
		let s = 7;
		const rnd = () => ((s = (s * 9301 + 49297) % 233280) / 233280);
		for (let x = 0; x <= laius + 8; x += 4 + rnd() * 6) {
			const kaugTeest = Math.abs(x - laius / 2) / (laius / 2);
			g.lineTo(x, yh - (4 + rnd() * 16 + (rnd() > 0.85 ? 10 : 0)) * (0.5 + kaugTeest) * (laius / 800));
		}
		g.lineTo(laius, yh);
		g.closePath();
		g.fill();
		/* maapind ridade kaupa (iga rida = üks kaugus) */
		const X0 = -14, X1 = 10, n = 14;
		for (let y = yh + 0.5; y < H; y += 1) {
			const z = (f * SILM) / (y - yh);
			if (z > 600) { g.fillStyle = '#040506'; g.fillRect(0, y, laius, 1); continue; }
			const gr = g.createLinearGradient(laius / 2 + (f * (X0 - KAM_X)) / z, 0, laius / 2 + (f * (X1 - KAM_X)) / z, 0);
			for (let i = 0; i <= n; i++) {
				const X = X0 + ((X1 - X0) * i) / n;
				gr.addColorStop(i / n, rgb(pinnaVarv(z, X)));
			}
			/* teraviad servad: tee ja teeperv */
			for (const X of [SERV_V - 1.0, SERV_V, SERV_P, SERV_P + 1.0]) {
				const p = (X - X0) / (X1 - X0);
				gr.addColorStop(Math.max(0, p - 0.0005), rgb(pinnaVarv(z, X - 0.01)));
				gr.addColorStop(Math.min(1, p + 0.0005), rgb(pinnaVarv(z, X + 0.01)));
			}
			g.fillStyle = gr;
			g.fillRect(0, y, laius, 1);
			/* pidevad äärejooned (lumega kaetud teel ei paista) */
			if (jooned && z < 260) {
				for (const X of [SERV_P - 0.15, SERV_V + 0.15]) {
					const sx = laius / 2 + (f * (X - KAM_X)) / z, w = Math.max(0.6, (f * 0.12) / z);
					const L = valgus(z, X), k = 6 + 255 * 5 * L;
					g.fillStyle = rgb([tm(0.62 * k), tm(0.62 * k), tm(0.6 * k)]);
					g.fillRect(sx - w / 2, y, w, 1);
				}
			}
		}
		/* märg asfalt: läikiv peegeldus valguslaigu keskel */
		if (marg || jaa) {
			const [cx, cy] = [laius / 2 + (f * (0.4 - KAM_X)) / 16, yh + (f * SILM) / 16];
			const r = g.createRadialGradient(cx, cy, 2, cx, cy, laius * 0.28);
			r.addColorStop(0, `rgba(255,244,215,${jaa ? 0.16 : 0.22})`);
			r.addColorStop(1, 'rgba(255,244,215,0)');
			g.save();
			g.scale(1, 0.32);
			g.fillStyle = r;
			g.fillRect(0, cy / 0.32 - laius * 0.3, laius, laius * 0.6);
			g.restore();
		}
	}

	/* ---------- ajajoon ---------- */
	const t0 = $derived(rada ? rada[0][0] - EEL : 0);
	const tL = $derived(rada ? rada[rada.length - 1][0] : 0);
	function asend(tt) {
		if (!rada) return [0, 0, 0, 0];
		if (tt <= rada[0][0]) { const v = rada[0][2] / 3.6; return [tt, rada[0][1] + v * (tt - rada[0][0]), rada[0][2], 0]; }
		const L = rada.length - 1;
		if (tt >= rada[L][0]) return rada[L];
		let lo = 0, hi = L;
		while (hi - lo > 1) { const m = (lo + hi) >> 1; if (rada[m][0] <= tt) lo = m; else hi = m; }
		const a = rada[lo], b = rada[hi], k = b[0] > a[0] ? (tt - a[0]) / (b[0] - a[0]) : 0;
		return [tt, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k, a[3]];
	}

	let tSim = $state(1e9), mangib = $state(false), kordaja = $state(1), naitaKoht = $state(false);
	let vaikne = false, nahtav = false;
	const tNyyd = $derived(Math.min(Math.max(tSim, t0), tL));
	const q = $derived(asend(tNyyd));
	const loog = $derived(tee?.loog || null);
	const loodud = $derived(!!(loog && tNyyd >= loog.t));
	const kaugus = $derived(tee?.jk ? tee.jk.x - q[1] : null);
	const lopp = $derived(tSim >= tL);
	const olek = $derived.by(() => {
		if (!stseen) return ['', false];
		if (loodud) return [stseen.loogTekst(loog.kmh), true];
		if (lopp) return [t('Peatud {m} m enne jalakäijat', { m: Math.max(0, kaugus).toLocaleString(LOC, { maximumFractionDigits: 1 }) }), false];
		return [stseen.faasid[q[3]] || '', false];
	});
	const nf = (x, d = 0) => x.toLocaleString(LOC, { minimumFractionDigits: d, maximumFractionDigits: d });

	/* ---------- osakesed (vihm, lumi) ---------- */
	let osad = [];
	const vihm = $derived(marg && vesi >= 2.5);
	function looOsad() {
		osad = [];
		if (!(vihm || lumine)) return;
		const n = lumine ? 260 : 220;
		for (let i = 0; i < n; i++) osad.push({ z: 2 + Math.random() * 45, X: -9 + Math.random() * 16, h: Math.random() * 4, v: lumine ? 0.6 + Math.random() * 0.6 : 7 + Math.random() * 3, d: Math.random() * 6.28 });
	}
	let tilgad = [];
	function looTilgad() {
		tilgad = [];
		if (!vihm) return;
		for (let i = 0; i < 26; i++) tilgad.push({ x: Math.random(), y: Math.random() * 0.8, r: 1 + Math.random() * 2.2, tekk: Math.random() * 1.5 });
	}

	/* ---------- joonistamine ---------- */
	let viimane = 0, raputus = 0, paugAeg = null;
	function joonista(aeg) {
		if (!canvas || !rada) return;
		const ctx = canvas.getContext('2d');
		const dpr = Math.min(2, window.devicePixelRatio || 1);
		if (canvas.width !== Math.round(laius * dpr) || canvas.height !== Math.round(korgus * dpr)) {
			canvas.width = Math.round(laius * dpr);
			canvas.height = Math.round(korgus * dpr);
		}
		ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
		const dt = Math.min(0.05, (aeg - viimane) / 1000 || 0);
		viimane = aeg;

		const xEes = q[1], kmh = q[2], faas = q[3];
		const s = xEes - SILM_TAGA; // silmade asukoht teel
		/* pidurdades nina vajub: pilt liigub üles */
		const pidur = faas === 2 ? Math.min(1, kmh > 1 ? 1 : 0.4) : 0;
		const nyok = -pidur * korgus * 0.025 + (raputus > 0 ? (Math.random() - 0.5) * raputus * 14 : 0);
		raputus = Math.max(0, raputus - dt * 2.2);

		ctx.clearRect(0, 0, laius, korgus);
		if (taust) ctx.drawImage(taust, 0, nyok - 20, laius, korgus + 40);

		/* keskjoon (katkendlik, liigub) */
		if (jooned) {
			for (let p = Math.floor((s + 2) / 12) * 12; p < s + 260; p += 12) {
				const z1 = Math.max(1.2, p - s), z2 = p + 3 - s;
				if (z2 <= 1.2) continue;
				const [a1, b1] = ekraan(z1, KESK - 0.06, 0, nyok), [a2, b2] = ekraan(z2, KESK - 0.06, 0, nyok);
				const [c1] = ekraan(z1, KESK + 0.06, 0, nyok), [c2] = ekraan(z2, KESK + 0.06, 0, nyok);
				const L = valgus((z1 + z2) / 2, KESK), k = 6 + 255 * 5 * L;
				ctx.fillStyle = rgb([tm(0.62 * k), tm(0.62 * k), tm(0.6 * k)]);
				ctx.beginPath(); ctx.moveTo(a1, b1); ctx.lineTo(c1, b1); ctx.lineTo(c2, b2); ctx.lineTo(a2, b2); ctx.fill();
			}
		}

		/* teeäärepostid helkuritega (iga 50 m), kaugemad enne */
		const postid = [];
		for (let p = Math.floor(s / 50) * 50 + 50; p < s + 420; p += 50) postid.push(p);
		postid.sort((a, b) => b - a);
		for (const p of postid) {
			const z = p - s;
			if (z < 2) continue;
			for (const [X, hk] of [[SERV_P + 0.9, '#ffb020'], [SERV_V - 0.9, '#f4f6ff']]) {
				const [x0, yb] = ekraan(z, X, 0, nyok), [, yt] = ekraan(z, X, 1.05, nyok);
				const w = Math.max(1, (f * 0.1) / z);
				const L = valgus(z, X, 0.6);
				const kk = (lumine ? 16 : 5) + 255 * 2.6 * L;
				ctx.fillStyle = rgb([tm(0.8 * kk), tm(0.8 * kk), tm(0.78 * kk)]);
				ctx.fillRect(x0 - w / 2, yt, w, yb - yt);
				/* helkur peegeldab tulesid tagasi — paistab kaugelt */
				const hel = Math.min(1, valgus(Math.min(z, kaug ? z : z * 0.55), X * 0.2) * 9);
				if (hel > 0.02) {
					const [, yr] = ekraan(z, X, 0.9, nyok);
					const r = Math.max(1.1, (f * 0.06) / z);
					ctx.globalAlpha = Math.min(1, hel);
					ctx.fillStyle = hk;
					ctx.fillRect(x0 - r * 0.7, yr - r, r * 1.4, r * 1.6);
					if (marg) { ctx.globalAlpha = hel * 0.25; ctx.fillRect(x0 - r * 0.5, yb + 1, r, (yb - yr) * 0.9); }
					ctx.globalAlpha = 1;
				}
			}
		}

		/* jalakäija */
		if (tee?.jk && !loodud) {
			const d = tee.jk.x - xEes;
			const z = d + SILM_TAGA;
			if (z > 1.5) {
				/* nähtavus = sama märkamiskaugus mis arvutuses */
				const vis = sujuv(D * 1.3, D * 0.82, d);
				const riie = hele ? [0.62, 0.6, 0.55] : [0.05, 0.055, 0.065];
				const pyks = hele ? [0.35, 0.36, 0.4] : [0.035, 0.04, 0.05];
				const samm = (aeg / 1000) * 3.2;
				const osa = (X, h1, h2, w, alb, nihe = 0) => {
					const [xa, ya] = ekraan(z, X - w / 2 + nihe, h2, nyok), [xb, yb2] = ekraan(z, X + w / 2 + nihe, h1, nyok);
					const hk = (h1 + h2) / 2;
					const L = valgus(z, X, hk);
					const oma = alb.map((a) => tm(a * (8 + 255 * 4.6 * L)));
					const bg = pinnaVarv(z + 6, X);
					ctx.fillStyle = rgb(segu(bg, oma, vis));
					ctx.fillRect(xa, ya, Math.max(0.6, xb - xa), Math.max(0.6, yb2 - ya));
				};
				const k1 = Math.sin(samm) * 0.12, k2 = -k1;
				osa(JK_X, 0, 0.85, 0.14, pyks, -0.08 + k1 * 0.3);
				osa(JK_X, 0, 0.85, 0.14, pyks, 0.08 + k2 * 0.3);
				osa(JK_X, 0.82, 1.5, 0.44, riie);
				osa(JK_X, 0.9, 1.45, 0.1, riie, -0.27 + k2 * 0.2);
				osa(JK_X, 0.9, 1.45, 0.1, riie, 0.27 + k1 * 0.2);
				osa(JK_X, 1.5, 1.75, 0.2, hele ? [0.55, 0.45, 0.38] : [0.12, 0.1, 0.09]);
				/* helkur (ripub vöö kõrgusel liikluse poolsel küljel) */
				if (helkur) {
					const hv = sujuv(D * 1.3, D * 0.85, d);
					if (hv > 0.01) {
						const [hx, hy] = ekraan(z, JK_X - 0.24, 0.8 + Math.sin(samm * 2) * 0.02, nyok);
						const r = Math.max(1.4, (f * 0.07) / z);
						const gl = ctx.createRadialGradient(hx, hy, 0, hx, hy, r * 5);
						gl.addColorStop(0, `rgba(255,252,225,${hv})`);
						gl.addColorStop(0.25, `rgba(255,228,120,${hv * 0.7})`);
						gl.addColorStop(1, 'rgba(255,220,90,0)');
						ctx.fillStyle = gl;
						ctx.fillRect(hx - r * 5, hy - r * 5, r * 10, r * 10);
					}
				}
				/* „kus ta on?“ — näitab asukohta ka siis, kui juht teda veel ei näe */
				if (naitaKoht && vis < 0.95) {
					const [xa, ya] = ekraan(z, JK_X - 0.45, 1.95, nyok), [xb, yb2] = ekraan(z, JK_X + 0.45, 0, nyok);
					ctx.setLineDash([4, 3]);
					ctx.strokeStyle = 'rgba(255,194,14,.9)';
					ctx.lineWidth = 1.5;
					ctx.strokeRect(xa, ya, Math.max(4, xb - xa), Math.max(6, yb2 - ya));
					ctx.setLineDash([]);
					ctx.fillStyle = 'rgba(255,194,14,.95)';
					ctx.font = '600 12px Inter, system-ui, sans-serif';
					ctx.textAlign = 'center';
					ctx.fillText(nf(Math.max(0, d)) + ' ' + t('m'), (xa + xb) / 2, ya - 5);
				}
			}
		}

		/* vihm või lumi esitulede valguses */
		if (osad.length) {
			const sammM = kmh / 3.6 * dt;
			ctx.lineCap = 'round';
			for (const o of osad) {
				o.z -= sammM; o.h -= o.v * dt; if (lumine) o.X += Math.sin(aeg / 900 + o.d) * dt * 0.4;
				if (o.z < 1.2 || o.h < 0) { o.z = 6 + Math.random() * 40; o.h = 1 + Math.random() * 3.5; o.X = -9 + Math.random() * 16; }
				const L = Math.min(1, valgus(o.z, o.X, Math.min(o.h, 0.6)) * 2.2 + 0.04);
				const [x, y] = ekraan(o.z, o.X, o.h, nyok);
				if (lumine) {
					const r = Math.max(0.6, (f * 0.025) / o.z);
					ctx.fillStyle = `rgba(240,245,255,${0.15 + 0.85 * L})`;
					ctx.beginPath(); ctx.arc(x, y, r, 0, 6.29); ctx.fill();
				} else {
					const [x2, y2] = ekraan(o.z + 0.35, o.X, o.h + 0.16, nyok);
					ctx.strokeStyle = `rgba(210,220,235,${0.03 + 0.42 * L})`;
					ctx.lineWidth = Math.max(0.5, (f * 0.008) / o.z);
					ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x2, y2); ctx.stroke();
				}
			}
		}

		/* kapott */
		const kh = korgus * (mob ? 0.13 : 0.11);
		const kap = ctx.createLinearGradient(0, korgus - kh, 0, korgus);
		kap.addColorStop(0, '#0d0f12');
		kap.addColorStop(1, '#030405');
		ctx.fillStyle = kap;
		ctx.beginPath();
		ctx.moveTo(0, korgus);
		ctx.lineTo(0, korgus - kh * 0.55);
		ctx.quadraticCurveTo(laius * 0.5, korgus - kh * 1.25, laius, korgus - kh * 0.55);
		ctx.lineTo(laius, korgus);
		ctx.fill();
		ctx.strokeStyle = 'rgba(255,240,205,.10)';
		ctx.lineWidth = 1.2;
		ctx.beginPath();
		ctx.moveTo(laius * 0.12, korgus - kh * 0.62);
		ctx.quadraticCurveTo(laius * 0.5, korgus - kh * 1.18, laius * 0.88, korgus - kh * 0.62);
		ctx.stroke();

		/* tuuleklaasil vihmapiisad + kojamees */
		if (tilgad.length) {
			const kp = ((aeg / 1000) % 1.1) / 1.1;
			const nurk = Math.PI * (kp < 0.5 ? kp * 2 : 2 - kp * 2);
			for (const p of tilgad) {
				p.tekk += dt;
				const px = p.x * laius, py = p.y * korgus;
				const a = Math.min(0.55, p.tekk * 0.5);
				ctx.fillStyle = `rgba(200,215,235,${a * 0.35})`;
				ctx.beginPath(); ctx.arc(px, py, p.r * (laius / 800), 0, 6.29); ctx.fill();
			}
			/* kojamees pühib piisad ära */
			const ox = laius * 0.32, oy = korgus * 1.02, len = korgus * 1.0;
			const ex = ox - Math.cos(nurk) * len, ey = oy - Math.sin(nurk) * len;
			for (const p of tilgad) {
				const ang = Math.atan2(oy - p.y * korgus, ox - p.x * laius);
				if (Math.abs(ang - nurk) < 0.06) p.tekk = 0;
			}
			ctx.lineCap = 'round';
			ctx.strokeStyle = 'rgba(4,5,6,.95)';
			ctx.lineWidth = Math.max(5, laius / 110);
			ctx.beginPath(); ctx.moveTo(ox + (ex - ox) * 0.42, oy + (ey - oy) * 0.42); ctx.lineTo(ex, ey); ctx.stroke();
			ctx.strokeStyle = 'rgba(4,5,6,.92)';
			ctx.lineWidth = Math.max(2, laius / 400);
			ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(ox + (ex - ox) * 0.55, oy + (ey - oy) * 0.55 - korgus * 0.02); ctx.stroke();
		}

		/* löök */
		if (loodud) {
			if (paugAeg === null) { paugAeg = aeg; raputus = 1; }
			const k = Math.max(0, 1 - (aeg - paugAeg) / 900);
			ctx.fillStyle = `rgba(220,30,30,${0.12 + k * 0.35})`;
			ctx.fillRect(0, 0, laius, korgus);
		} else paugAeg = null;

		/* vinjett */
		const vin = ctx.createRadialGradient(laius / 2, korgus * 0.55, korgus * 0.35, laius / 2, korgus * 0.55, laius * 0.75);
		vin.addColorStop(0, 'rgba(0,0,0,0)');
		vin.addColorStop(1, 'rgba(0,0,0,.45)');
		ctx.fillStyle = vin;
		ctx.fillRect(0, 0, laius, korgus);
	}

	/* ---------- mängimine ---------- */
	let raf = 0, eelmine = 0;
	function samm(nyyd) {
		const dtR = Math.min(0.1, (nyyd - eelmine) / 1000);
		eelmine = nyyd;
		if (mangib) {
			tSim += dtR * kordaja;
			if (tSim >= tL) { tSim = tL; mangib = false; }
		}
		joonista(nyyd);
		/* lõpus joonistame veel veidi (vihm, kojamees, löögi välgatus) */
		if (mangib || nahtav) raf = requestAnimationFrame(samm);
		else raf = 0;
	}
	function kaivita() { if (!raf) { eelmine = performance.now(); raf = requestAnimationFrame(samm); } }
	function mangi() {
		if (!stseen) return;
		if (vaikne) { tSim = tL; requestAnimationFrame((a) => joonista(a)); return; }
		tSim = t0;
		mangib = true;
		looOsad();
		looTilgad();
		kaivita();
	}
	function uuendaMoot() {
		if (!figEl) return;
		laius = figEl.clientWidth || 800;
		const ar = laius < 560 ? 1.25 : 1.6;
		let h = laius / ar;
		const mh = canvas ? parseFloat(getComputedStyle(canvas).maxHeight) : NaN;
		if (mh > 0 && h > mh) h = mh;
		korgus = Math.round(h);
		f = (laius / 2) / Math.tan((mob ? 34 : 31) * Math.PI / 180);
		yH = korgus * 0.44;
		joonistaTaust();
		if (!raf) requestAnimationFrame((a) => joonista(a));
	}
	let ootel = 0;
	$effect(() => {
		stseen; D; naeb;
		untrack(() => {
			joonistaTaust();
			clearTimeout(ootel);
			if (!nahtav || vaikne) { tSim = 1e9; requestAnimationFrame((a) => joonista(a)); return; }
			ootel = setTimeout(mangi, 180);
		});
	});
	$effect(() => { naitaKoht; untrack(() => { if (!raf) requestAnimationFrame((a) => joonista(a)); }); });
	onMount(() => {
		vaikne = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
		uuendaMoot();
		const ro = new ResizeObserver(() => uuendaMoot());
		ro.observe(figEl);
		const io = new IntersectionObserver((e) => {
			const enne = nahtav;
			nahtav = e[0].isIntersecting;
			if (nahtav && !enne) { if (!vaikne) mangi(); else kaivita(); }
		}, { threshold: 0.3 });
		io.observe(figEl);
		return () => { io.disconnect(); ro.disconnect(); cancelAnimationFrame(raf); clearTimeout(ootel); };
	});
</script>

<figure class="jv" bind:this={figEl}>
	<div class="jv-scene">
		<canvas bind:this={canvas} style="height:{korgus}px" role="img" aria-label={t('Juhi vaade pimedas: kas ja millal jalakäija paistab')}></canvas>
		<div class="jv-hud" aria-hidden="true">
			<b class="jv-kmh">{nf(Math.max(0, q[3] === 3 ? 0 : q[2]))} <small>{t('km/h')}</small></b>
			<span class="jv-faas" class:jv-halb={olek[1]}>{olek[0]}</span>
			{#if kaugus != null && !loodud}<span class="jv-aeg">{t('Jalakäijani')} {nf(Math.max(0, kaugus))} {t('m')}</span>{/if}
		</div>
		<div class="jv-nupud">
			<button type="button" class="jv-btn" onclick={mangi}>
				<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M15.5 10a5.5 5.5 0 1 1-1.8-4.1M15.5 3.5v3h-3" /></svg>
				{t('Mängi uuesti')}
			</button>
			<div class="jv-kord" role="group" aria-label={t('Kiirus')}>
				{#each [[0.5, '½×'], [1, '1×'], [2, '2×']] as [k, n] (k)}
					<button type="button" aria-pressed={kordaja === k} onclick={() => (kordaja = k)}>{n}</button>
				{/each}
			</div>
		</div>
		<button type="button" class="jv-koht" aria-pressed={naitaKoht} onclick={() => (naitaKoht = !naitaKoht)}>{t('Näita, kus jalakäija on')}</button>
	</div>
	<figcaption>
		{t('Juhi silmade kõrguselt. Jalakäija muutub nähtavaks samal kaugusel, mida kasutab arvutus ({d} m).', { d: D })}
		{#if marg}{vihm ? t('Vihmas ja märjal teel neelab asfalt valgust — tee on tumedam.') : t('Märg tee neelab valgust — asfalt on tumedam.')}{:else if lumine}{t('Lumi peegeldab valgust — taust on heledam.')}{/if}
	</figcaption>
</figure>

<style>
	.jv {
		margin: var(--sp-4) 0 0;
	}
	.jv-scene {
		position: relative;
		border-radius: var(--r);
		overflow: hidden;
		background: #04060a;
	}
	.jv-scene > canvas {
		display: block;
		width: 100%;
	}
	.jv-hud {
		position: absolute;
		top: var(--sp-3);
		left: var(--sp-3);
		display: flex;
		flex-direction: column;
		gap: 2px;
		padding: var(--sp-2) var(--sp-3);
		background: rgba(10, 11, 13, 0.72);
		color: #fff;
		border-radius: var(--r-sm);
		font-variant-numeric: tabular-nums;
		pointer-events: none;
		min-width: 9.5em;
	}
	.jv-kmh {
		font-family: var(--display);
		font-size: 26px;
		line-height: 1.05;
	}
	.jv-kmh small {
		font-size: 14px;
		opacity: 0.75;
	}
	.jv-faas {
		font-size: 13px;
		font-weight: 600;
		color: var(--yellow-2);
		max-width: 16em;
	}
	.jv-faas.jv-halb {
		color: #ff8a80;
	}
	.jv-aeg {
		font-size: 12px;
		opacity: 0.75;
	}
	.jv-nupud {
		position: absolute;
		top: var(--sp-3);
		right: var(--sp-3);
		display: flex;
		gap: var(--sp-2);
		align-items: center;
	}
	.jv-btn,
	.jv-kord button,
	.jv-koht {
		border: 0;
		background: rgba(255, 255, 255, 0.92);
		color: #111;
		font-weight: 600;
		font-size: 13px;
		border-radius: var(--r-sm);
		padding: 6px 10px;
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		gap: 6px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}
	.jv-btn svg {
		width: 16px;
		height: 16px;
		fill: none;
		stroke: currentColor;
		stroke-width: 2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.jv-kord {
		display: flex;
		gap: 2px;
		background: rgba(255, 255, 255, 0.92);
		border-radius: var(--r-sm);
		padding: 2px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}
	.jv-kord button {
		box-shadow: none;
		background: transparent;
		padding: 4px 8px;
	}
	.jv-kord button[aria-pressed='true'] {
		background: var(--ink);
		color: #fff;
	}
	.jv-koht {
		position: absolute;
		right: var(--sp-3);
		bottom: calc(var(--sp-3) + 4%);
		background: rgba(10, 11, 13, 0.72);
		color: #fff;
		border: 1px solid rgba(255, 255, 255, 0.25);
	}
	.jv-koht[aria-pressed='true'] {
		background: var(--yellow);
		color: #111;
		border-color: var(--yellow);
	}
	figcaption {
		margin-top: var(--sp-2);
		font-size: 13px;
		color: var(--muted);
	}
	@media (max-width: 560px) {
		.jv-kmh {
			font-size: 21px;
		}
		.jv-hud {
			min-width: 0;
			padding: 6px 8px;
		}
		.jv-nupud {
			top: auto;
			bottom: var(--sp-3);
			left: var(--sp-3);
			right: auto;
		}
		.jv-koht {
			top: var(--sp-3);
			bottom: auto;
			font-size: 12px;
			padding: 5px 8px;
		}
	}
</style>
