<script>
	/* Sirge tee animatsioon pealtvaates (pimedas, pikivahe). Sama loogika mis
	   KurvAnimatsioon.svelte: meetrites joonis, kaamera sõidab autode järel ja näitab
	   lõpus kogu olukorda; tee välimus sõltub teeoludest, pimedas on öö ja esitulede valgus.

	   stseen = {
	     pind: 'kuiv' | 'marg' | 'lumi' | 'jaa' | 'kruus',
	     oo: true → öö (esituled, jalakäija paistab alles valguses),
	     teed: [{ silt, autod: [{ nimi, rada: [[t, x (esiots), km/h, faas 0 sõidab | 1 reageerib | 2 pidurdab | 3 seisab]], varv, peamine }],
	              jk: { x, riided: 'tume'|'hele', helkur, tNae } | null, valgus: m | 0,
	              loog: { t, x, kmh } | null }],
	     faasid: [tekst faasile 0..3], loogTekst: (kmh) => tekst
	   } */
	import { onMount, untrack } from 'svelte';

	let { stseen, t, LOC = 'et-EE' } = $props();

	const VARV = {
		kuiv: { maa: '#9dbf78', serv: '#bdb4a2', tee: '#565b63', joon: '#ffffff', puu: '#3d6b35', puu2: '#4f8044' },
		marg: { maa: '#7c9f5a', serv: '#8d8678', tee: '#363b43', joon: '#e9eef3', puu: '#2e5a2a', puu2: '#3c6e35' },
		lumi: { maa: '#f4f7fa', serv: '#e6ebf0', tee: '#d3d9e0', joon: 'rgba(255,255,255,.55)', puu: '#355a45', puu2: '#46705a' },
		jaa: { maa: '#eef3f7', serv: '#dde5ed', tee: '#93afc4', joon: 'rgba(255,255,255,.6)', puu: '#355a45', puu2: '#46705a' },
		kruus: { maa: '#9dbf78', serv: '#a39a86', tee: '#b3a68c', joon: 'rgba(255,255,255,0)', puu: '#3d6b35', puu2: '#4f8044' }
	};
	const OO = {
		kuiv: { maa: '#0b0f14', serv: '#151a20', tee: '#1b2028', joon: '#4b525d', puu: '#0f1a12', puu2: '#13221a' },
		marg: { maa: '#0a0e13', serv: '#13181e', tee: '#151a21', joon: '#4b525d', puu: '#0f1a12', puu2: '#13221a' },
		lumi: { maa: '#2a3240', serv: '#323b4a', tee: '#3a4352', joon: 'rgba(255,255,255,.18)', puu: '#121c18', puu2: '#17241f' },
		jaa: { maa: '#28303d', serv: '#303947', tee: '#2c3a4a', joon: 'rgba(255,255,255,.2)', puu: '#121c18', puu2: '#17241f' },
		kruus: { maa: '#0b0f14', serv: '#171a1d', tee: '#2a2722', joon: 'rgba(0,0,0,0)', puu: '#0f1a12', puu2: '#13221a' }
	};
	const oo = $derived(!!stseen?.oo);
	const V = $derived((oo ? OO : VARV)[stseen?.pind] || (oo ? OO.kuiv : VARV.kuiv));
	const talv = $derived(stseen?.pind === 'lumi' || stseen?.pind === 'jaa');

	const VAHE = 17; // teede vahe (m), kui A ja B on kõrvuti
	const LAI = 7; // tee laius (kaks rada)
	const yTee = (i) => i * VAHE;
	const yRada = (i) => yTee(i) + LAI / 4; // sinu rada (paremal = all)

	let figW = $state(800);
	const AR = $derived(figW < 560 ? 1.25 : 1.6);
	const CAMW = $derived(AR < 1.5 ? 48 : 66);

	/* ---------- ülevaade ja kaunistused ---------- */
	const rnd = (i) => {
		const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
		return x - Math.floor(x);
	};
	const geo = $derived.by(() => {
		if (!stseen) return null;
		let x0 = Infinity, x1 = -Infinity;
		for (const tee of stseen.teed) {
			for (const a of tee.autod) for (const q of a.rada) { if (q[1] - 5 < x0) x0 = q[1] - 5; if (q[1] > x1) x1 = q[1]; }
			if (tee.jk) x1 = Math.max(x1, tee.jk.x);
		}
		x0 = Math.max(x0, x1 - 400);
		/* varu servades, et sildid („märkad jalakäijat“, „jalakäija“) mahuksid ära */
		const varu = 6 + (x1 - x0) * 0.09;
		x0 -= varu;
		x1 += varu;
		const n = stseen.teed.length;
		const y0 = -LAI / 2 - 6, y1 = yTee(n - 1) + LAI / 2 + 6;
		let w = x1 - x0, h = y1 - y0;
		if (w / h < AR) w = h * AR; else h = w / AR;
		/* HUD on üleval vasakul: tee veidi allapoole */
		const yld = { x: (x0 + x1) / 2, y: (y0 + y1) / 2, w };
		/* puud ja postid tee ääres */
		const puud = [], postid = [];
		const A0 = x0 - 200, A1 = x1 + 200;
		for (let i = 0, x = A0; x < A1; i++, x += 6 + rnd(i) * 9) {
			puud.push([x, -LAI / 2 - 5 - rnd(i + 3) * 10, 1.5 + rnd(i + 7) * 1.5]);
			puud.push([x + 3, yTee(n - 1) + LAI / 2 + 5 + rnd(i + 5) * 10, 1.4 + rnd(i + 9) * 1.6]);
		}
		for (let x = Math.ceil(A0 / 25) * 25; x < A1; x += 25) for (let i = 0; i < n; i++) postid.push([x, yTee(i) - LAI / 2 - 0.9], [x, yTee(i) + LAI / 2 + 0.9]);
		return { yld, puud, postid, x0: A0, x1: A1, n };
	});

	/* ---------- taasesitus ---------- */
	const tAlg = $derived(stseen ? Math.min(...stseen.teed.flatMap((tt) => tt.autod.map((a) => a.rada[0][0]))) : 0);
	const tLopp = $derived(stseen ? Math.max(...stseen.teed.flatMap((tt) => tt.autod.map((a) => a.rada[a.rada.length - 1][0]))) : 0);
	let tSim = $state(1e9);
	let mangib = $state(false);
	let kordaja = $state(1);
	let cam = $state({ x: 0, y: 0, w: 66 });
	let lopuAeg = $state(null);
	let camAlgus = null;
	let vaikne = false, nahtav = false, figEl;
	const tNyyd = $derived(Math.min(Math.max(tSim, tAlg), tLopp));

	function asend(rada, tt) {
		if (tt <= rada[0][0]) return rada[0];
		const L = rada.length - 1;
		if (tt >= rada[L][0]) return rada[L];
		let lo = 0, hi = L;
		while (hi - lo > 1) { const m = (lo + hi) >> 1; if (rada[m][0] <= tt) lo = m; else hi = m; }
		const a = rada[lo], b = rada[hi];
		const k = b[0] > a[0] ? (tt - a[0]) / (b[0] - a[0]) : 0;
		return [tt, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k, a[3]];
	}
	const autod = $derived.by(() => {
		if (!stseen) return [];
		const out = [];
		stseen.teed.forEach((tee, i) => tee.autod.forEach((a) => {
			const q = asend(a.rada, tNyyd);
			out.push({ ...a, tee: i, x: q[1], kmh: q[2], faas: q[3] });
		}));
		return out;
	});
	const lopp = $derived(tSim >= tLopp);

	function seaKaamera(dtR, kohe) {
		if (!geo) return;
		const Y = geo.yld;
		if (!mangib && lopuAeg === null) { cam = { x: Y.x, y: Y.y, w: Y.w }; return; }
		if (Y.w <= CAMW * 1.05) { cam = { x: Y.x, y: Y.y, w: Y.w }; return; }
		if (lopuAeg !== null) {
			const k = Math.min(1, (performance.now() - lopuAeg) / 1400);
			const e = k < 0.5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2;
			const a = camAlgus || cam;
			cam = { x: a.x + (Y.x - a.x) * e, y: a.y + (Y.y - a.y) * e, w: a.w + (Y.w - a.w) * e };
			return;
		}
		const xs = autod.map((a) => a.x);
		const lo = Math.min(...xs) - 6, hi = Math.max(...xs);
		const w = Math.max(CAMW, hi - lo + 24);
		const tx = (lo + hi) / 2 + w * 0.14;
		const k = kohe ? 1 : Math.min(1, dtR * 3);
		cam = { x: cam.x + (tx - cam.x) * k, y: Y.y, w: cam.w + (w - cam.w) * k };
	}
	let raf = 0, eelmine = 0;
	function samm(nyyd) {
		const dtR = Math.min(0.1, (nyyd - eelmine) / 1000);
		eelmine = nyyd;
		if (mangib) {
			tSim += dtR * kordaja;
			if (tSim >= tLopp) { tSim = tLopp; mangib = false; lopuAeg = nyyd; camAlgus = { ...cam }; }
		}
		seaKaamera(dtR, false);
		if (mangib || (lopuAeg !== null && nyyd - lopuAeg < 1500)) raf = requestAnimationFrame(samm);
		else raf = 0;
	}
	function mangi() {
		if (!stseen) return;
		if (vaikne) { tSim = tLopp; lopuAeg = null; seaKaamera(0, true); return; }
		tSim = tAlg;
		lopuAeg = null;
		camAlgus = null;
		mangib = true;
		seaKaamera(0, true);
		if (!raf) { eelmine = performance.now(); raf = requestAnimationFrame(samm); }
	}
	let ootel = 0;
	$effect(() => {
		stseen;
		AR;
		untrack(() => {
			clearTimeout(ootel);
			if (!nahtav || vaikne) { tSim = 1e9; lopuAeg = null; mangib = false; seaKaamera(0, true); return; }
			ootel = setTimeout(mangi, 180);
		});
	});
	onMount(() => {
		vaikne = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
		seaKaamera(0, true);
		const io = new IntersectionObserver((e) => {
			const enne = nahtav;
			nahtav = e[0].isIntersecting;
			if (nahtav && !enne && !vaikne) mangi();
		}, { threshold: 0.35 });
		io.observe(figEl);
		return () => { io.disconnect(); cancelAnimationFrame(raf); clearTimeout(ootel); };
	});

	/* ---------- joonistamine ---------- */
	const H = $derived(cam.w / AR);
	/* HUD on üleval vasakul: tee veidi allapoole (nihe sõltub praegusest vaatest) */
	const camY = $derived(cam.y - H * 0.1);
	const vb = $derived(`${(cam.x - cam.w / 2).toFixed(2)} ${(camY - H / 2).toFixed(2)} ${cam.w.toFixed(2)} ${H.toFixed(2)}`);
	const fs = $derived(cam.w / (AR < 1.5 ? 32 : 42));
	const autoSuur = $derived(Math.max(1, cam.w / 120));
	const pts = (a) => a.map((p) => p[0].toFixed(2) + ',' + p[1].toFixed(2)).join(' ');
	/* läbitud teekond faaside kaupa */
	const jaljed = $derived.by(() => {
		if (!stseen) return [];
		const out = [];
		stseen.teed.forEach((tee, i) => tee.autod.forEach((a) => {
			if (!a.peamine) return;
			const y = yRada(i);
			const seg = [[], [], []];
			for (const q of a.rada) {
				if (q[0] > tNyyd) break;
				const f = Math.min(2, q[3]);
				if (seg[f].length === 0 && f > 0 && seg[f - 1].length) seg[f].push(seg[f - 1][seg[f - 1].length - 1]);
				seg[f].push([q[1] - 2.2, y]);
			}
			out.push(...seg.map((s, f) => ({ f, p: pts(s) })));
		}));
		return out;
	});
	const markid = $derived.by(() => {
		if (!stseen) return [];
		const out = [];
		stseen.teed.forEach((tee, i) => tee.autod.forEach((a) => {
			if (!a.peamine) return;
			for (const [f, tekst] of [[1, stseen.markNae], [2, t('pidurdad')]]) {
				const q = a.rada.find((r) => r[3] === f);
				if (q && q[0] <= tNyyd && tekst) out.push({ x: q[1] - 2.2, y: yRada(i), f, tekst, k: i + '-' + f });
			}
		}));
		return out;
	});
	const peamine = $derived(autod.find((a) => a.peamine) || autod[0]);
	const loogid = $derived(stseen ? stseen.teed.map((tee, i) => (tee.loog && tee.loog.t <= tNyyd ? { ...tee.loog, i } : null)).filter(Boolean) : []);
	const olek = $derived.by(() => {
		if (!stseen || !peamine) return ['', false];
		const L = stseen.teed.find((tee) => tee.loog && tee.loog.t <= tNyyd);
		if (L && stseen.teed.length === 1) return [stseen.loogTekst(L.loog.kmh), true];
		if (lopp) return [stseen.teed.some((tee) => tee.loog) ? stseen.loogTekst(Math.max(...stseen.teed.filter((x) => x.loog).map((x) => x.loog.kmh))) : stseen.faasid[3], stseen.teed.some((tee) => tee.loog)];
		return [stseen.faasid[peamine.faas] || '', false];
	});
	const nf = (x, d = 0) => x.toLocaleString(LOC, { minimumFractionDigits: d, maximumFractionDigits: d });
	const mootkava = $derived(cam.w > 160 ? 50 : cam.w > 70 ? 20 : 10);
	const aegNull = $derived(Math.max(0, tNyyd));
</script>

<figure class="sa" class:oo bind:this={figEl} bind:clientWidth={figW}>
	{#if stseen && geo}
		<div class="sa-scene">
			<svg viewBox={vb} role="img" aria-label={t('Auto teekond pealtvaates')} preserveAspectRatio="xMidYMid slice">
				<defs>
					<pattern id="sa-lumi" width="3" height="3" patternUnits="userSpaceOnUse"><circle cx=".6" cy=".8" r=".18" fill="#dfe6ee" opacity={oo ? 0.25 : 1} /><circle cx="2.1" cy="2.2" r=".14" fill="#e7edf3" opacity={oo ? 0.25 : 1} /></pattern>
					<linearGradient id="sa-kiir" x1="0" x2="1"><stop offset="0" stop-color="#fff4c8" stop-opacity=".62" /><stop offset=".7" stop-color="#fff4c8" stop-opacity=".22" /><stop offset="1" stop-color="#fff4c8" stop-opacity="0" /></linearGradient>
					<radialGradient id="sa-helk"><stop offset="0" stop-color="#fff7c2" /><stop offset=".35" stop-color="#ffd84a" stop-opacity=".9" /><stop offset="1" stop-color="#ffd84a" stop-opacity="0" /></radialGradient>
				</defs>
				<rect x={cam.x - 3000} y={cam.y - 1000} width="6000" height="2000" fill={V.maa} />
				{#if talv}<rect x={cam.x - 3000} y={cam.y - 1000} width="6000" height="2000" fill="url(#sa-lumi)" />{/if}
				{#each Array(geo.n) as _, i (i)}
					{@const y = yTee(i)}
					<rect x={geo.x0} y={y - LAI / 2 - (talv ? 1.6 : 0.9)} width={geo.x1 - geo.x0} height={LAI + (talv ? 3.2 : 1.8)} fill={V.serv} />
					<rect x={geo.x0} y={y - LAI / 2} width={geo.x1 - geo.x0} height={LAI} fill={V.tee} />
					{#if stseen.pind === 'marg'}
						{#each [y - 1, y + 2.4] as yy, k (k)}<line x1={geo.x0} x2={geo.x1} y1={yy} y2={yy} stroke="#c9dcec" stroke-opacity={oo ? 0.1 : 0.25} stroke-width=".35" stroke-dasharray="9 5 2 7" />{/each}
						{#each [-2.55, -0.95, 0.95, 2.55] as d, k (k)}<line x1={geo.x0} x2={geo.x1} y1={y + d} y2={y + d} stroke="#000" stroke-opacity=".35" stroke-width=".5" />{/each}
					{:else if stseen.pind === 'lumi'}
						{#each [-2.55, -0.95, 0.95, 2.55] as d, k (k)}<line x1={geo.x0} x2={geo.x1} y1={y + d} y2={y + d} stroke="#9aa5b1" stroke-opacity={oo ? 0.35 : 0.8} stroke-width=".5" />{/each}
					{:else if stseen.pind === 'jaa'}
						{#each [y - 1.4, y + 1.6] as yy, k (k)}<line x1={geo.x0} x2={geo.x1} y1={yy} y2={yy} stroke="#eaf5ff" stroke-opacity={oo ? 0.15 : 0.45} stroke-width="2.4" stroke-dasharray="18 7 6 12" stroke-linecap="round" />{/each}
					{/if}
					<line x1={geo.x0} x2={geo.x1} y1={y} y2={y} stroke={V.joon} stroke-width=".15" stroke-dasharray="3 9" />
					{#if !talv && stseen.pind !== 'kruus'}
						<line x1={geo.x0} x2={geo.x1} y1={y - LAI / 2 + 0.25} y2={y - LAI / 2 + 0.25} stroke={V.joon} stroke-width=".15" />
						<line x1={geo.x0} x2={geo.x1} y1={y + LAI / 2 - 0.25} y2={y + LAI / 2 - 0.25} stroke={V.joon} stroke-width=".15" />
					{/if}
					{#if stseen.teed[i].silt}
						<text x={cam.x - cam.w / 2 + fs * 0.6} y={y - LAI / 2 - fs * 0.45} font-size={fs} class="sa-silt" class:sa-silt-b={stseen.teed[i].silt === 'B'}>{stseen.teed[i].silt}</text>
					{/if}
				{/each}
				{#each geo.postid as p, i (i)}<rect x={p[0] - 0.14} y={p[1] - 0.14} width=".28" height=".28" fill={oo ? '#cfd5dd' : '#fff'} stroke="#22262c" stroke-width=".07" />{/each}
				{#each geo.puud as p, i (i)}
					<circle cx={p[0] + 0.4} cy={p[1] + 0.5} r={p[2]} fill="#000" opacity=".12" />
					<circle cx={p[0]} cy={p[1]} r={p[2]} fill={V.puu} />
					<circle cx={p[0] - p[2] * 0.25} cy={p[1] - p[2] * 0.25} r={p[2] * 0.55} fill={V.puu2} />
					{#if talv}<circle cx={p[0] - p[2] * 0.3} cy={p[1] - p[2] * 0.35} r={p[2] * 0.3} fill="#fff" opacity={oo ? 0.25 : 0.75} />{/if}
				{/each}

				<!-- esitulede valgus (öösel) -->
				{#if oo}
					{#each autod as a, i (i)}
						{#if a.peamine && stseen.teed[a.tee].valgus}
							{@const L = Math.min(stseen.teed[a.tee].valgus * 1.15, 400)}
							{@const y = yRada(a.tee)}
							<path d="M{a.x} {y - 0.7} L{a.x + L} {y - 0.7 - Math.min(9, L * 0.09)} L{a.x + L} {y + 0.7 + Math.min(6, L * 0.05)} L{a.x} {y + 0.7}Z" fill="url(#sa-kiir)" />
						{/if}
					{/each}
				{/if}

				<!-- jäljed ja märgid -->
				{#each jaljed as j, i (i)}<polyline points={j.p} class="sa-kulg sa-k{j.f}" stroke-width={fs * (j.f ? 0.16 : 0.12)} />{/each}
				{#each markid as mk (mk.k)}
					<circle cx={mk.x} cy={mk.y} r={fs * 0.32} class="sa-m sa-m{mk.f}" stroke-width={fs * 0.08} />
					<text x={mk.x} y={mk.f === 1 ? mk.y - fs * 0.75 : mk.y + fs * 1.45} font-size={fs * 0.9} text-anchor="middle" class="sa-tx" stroke-width={fs * 0.22}>{mk.tekst}</text>
				{/each}

				<!-- jalakäija -->
				{#each stseen.teed as tee, i (i)}
					{#if tee.jk && !(tee.loog && tee.loog.t <= tNyyd)}
						{@const nae = tNyyd >= tee.jk.tNae}
						{@const y = yRada(i) + 0.2}
						{@const hele = tee.jk.riided === 'hele'}
						<g transform="translate({tee.jk.x + 0.4} {y}) scale({1.4 * autoSuur})" opacity={oo && !nae ? 0.13 : 1}>
							<ellipse cx="0" cy="0" rx=".32" ry=".55" fill={hele ? '#f0ead8' : oo ? '#6b6f76' : '#2a2f37'} stroke={oo ? 'rgba(255,244,200,.5)' : '#111'} stroke-width=".05" />
							<circle cx="0" cy="0" r=".22" fill={hele ? '#c9b79a' : oo ? '#8a8d92' : '#3b3f45'} />
							{#if tee.jk.helkur && nae}<circle cx="-.05" cy=".55" r={oo ? 1.2 : 0.4} fill="url(#sa-helk)" /><circle cx="-.05" cy=".55" r=".13" fill="#fff7c2" />{/if}
						</g>
						{#if nae}<text x={tee.jk.x + 0.4} y={y - fs * 0.9} font-size={fs * 0.85} text-anchor="middle" class="sa-tx">{t('jalakäija')}</text>{/if}
					{/if}
				{/each}

				<!-- autod -->
				{#each autod as a, i (i)}
					{@const y = yRada(a.tee)}
					{@const L = a.pikkus || 4.4}
					<g transform="translate({(a.x - L / 2).toFixed(3)} {y}) scale({autoSuur})">
						<rect x={-L / 2} y="-1.05" width={L} height="2.1" rx=".5" fill="#000" opacity=".22" transform="translate(.15 .2)" />
						<rect x={-L / 2 + 0.6} y="-1.0" width=".72" height=".24" rx=".08" fill="#15171b" /><rect x={-L / 2 + 0.6} y=".76" width=".72" height=".24" rx=".08" fill="#15171b" />
						<rect x={L / 2 - 1.4} y="-1.0" width=".72" height=".24" rx=".08" fill="#15171b" /><rect x={L / 2 - 1.4} y=".76" width=".72" height=".24" rx=".08" fill="#15171b" />
						<rect x={-L / 2} y="-0.9" width={L} height="1.8" rx=".55" fill={a.varv} stroke="#171200" stroke-width=".09" />
						<path d="M{L / 2 - 1.65} -.72 Q{L / 2 - 0.95} 0 {L / 2 - 1.65} .72 L{L / 2 - 2.15} .62 Q{L / 2 - 1.8} 0 {L / 2 - 2.15} -.62Z" fill="#26303b" />
						<path d="M{-L / 2 + 0.85} -.66 Q{-L / 2 + 0.45} 0 {-L / 2 + 0.85} .66 L{-L / 2 + 1.2} .56 Q{-L / 2 + 0.95} 0 {-L / 2 + 1.2} -.56Z" fill="#26303b" />
						{#if a.faas === 2}
							<rect x={-L / 2 - 0.08} y="-0.8" width=".16" height=".42" rx=".05" class="sa-pidur" />
							<rect x={-L / 2 - 0.08} y="0.38" width=".16" height=".42" rx=".05" class="sa-pidur" />
						{/if}
						<rect x={L / 2 - 0.12} y="-0.78" width=".12" height=".34" rx=".05" fill="#fffbe6" />
						<rect x={L / 2 - 0.12} y="0.44" width=".12" height=".34" rx=".05" fill="#fffbe6" />
					</g>
				{/each}
				{#each loogid as l (l.i)}
					<g transform="translate({l.x} {yRada(l.i)}) scale({fs / 2})">
						<path d="M0-2.6 .7-1 2.4-1.8 1.4-.3 2.8.6 1 .8 1.3 2.6 0 1.3-1.3 2.6-1 .8-2.8.6-1.4-.3-2.4-1.8-.7-1Z" class="sa-paug" />
					</g>
				{/each}
				<!-- mõõtkava -->
				<g transform="translate({cam.x - cam.w / 2 + fs * 0.9} {camY + H / 2 - fs * 0.9})">
					<rect x={-fs * 0.4} y={-fs * 1.5} width={mootkava + fs * 0.8} height={fs * 2.1} rx={fs * 0.3} fill="#fff" opacity=".82" />
					<path d="M0 0H{mootkava}M0 {-fs * 0.3}V0M{mootkava} {-fs * 0.3}V0" stroke="#111" stroke-width={fs * 0.09} fill="none" />
					<text x={mootkava / 2} y={-fs * 0.45} font-size={fs * 0.8} text-anchor="middle" fill="#111">{mootkava} {t('m')}</text>
				</g>
			</svg>
			<div class="sa-hud" aria-hidden="true">
				{#each autod.filter((a) => a.nimi || a.peamine) as a, i (i)}
					<b class="sa-kmh">{#if a.nimi}<span class="sa-n" style="--c:{a.varv}">{a.nimi}</span>{/if} {nf(Math.max(0, a.faas === 3 ? 0 : a.kmh))} <small>{t('km/h')}</small></b>
				{/each}
				<span class="sa-faas" class:sa-halb={olek[1]}>{olek[0]}</span>
				<span class="sa-aeg">{nf(aegNull, 1)} {t('s')}</span>
			</div>
			<div class="sa-nupud">
				<button type="button" class="sa-btn" onclick={mangi}>
					<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M15.5 10a5.5 5.5 0 1 1-1.8-4.1M15.5 3.5v3h-3" /></svg>
					{t('Mängi uuesti')}
				</button>
				<div class="sa-kord" role="group" aria-label={t('Kiirus')}>
					{#each [[0.5, '½×'], [1, '1×'], [2, '2×']] as [k, n] (k)}
						<button type="button" aria-pressed={kordaja === k} onclick={() => (kordaja = k)}>{n}</button>
					{/each}
				</div>
			</div>
		</div>
	{/if}
	<figcaption>
		<span class="sa-l"><i class="sa-l0"></i>{t('sõidad')}</span>
		<span class="sa-l"><i class="sa-l1"></i>{t('reageerid')}</span>
		<span class="sa-l"><i class="sa-l2"></i>{t('pidurdad')}</span>
	</figcaption>
</figure>

<style>
	.sa {
		margin: var(--sp-4) 0 0;
	}
	.sa-scene {
		position: relative;
	}
	.sa-scene > svg {
		width: 100%;
		height: auto;
		aspect-ratio: 1.6;
		border-radius: var(--r);
		background: #9dbf78;
		display: block;
	}
	.sa.oo .sa-scene > svg {
		background: #0b0f14;
	}
	.sa-kulg {
		fill: none;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.sa-k0 {
		stroke: #fff;
		stroke-opacity: 0.5;
		stroke-dasharray: 0.6 0.9;
	}
	.sa-k1 {
		stroke: var(--yellow);
	}
	.sa-k2 {
		stroke: #e5484d;
	}
	.sa-m {
		fill: #fff;
	}
	.sa-m1 {
		stroke: #b98900;
	}
	.sa-m2 {
		stroke: #c53030;
	}
	.sa-tx {
		fill: #111;
		stroke: #fff;
		paint-order: stroke;
		font-weight: 700;
		font-family: var(--body);
	}
	.sa-silt {
		font-family: var(--display);
		font-weight: 700;
		fill: var(--yellow);
		stroke: #111;
		stroke-width: 0.12;
		paint-order: stroke;
	}
	.sa-silt-b {
		fill: #7cc4ff;
	}
	.sa-pidur {
		fill: #ff2d2d;
		filter: drop-shadow(0 0 0.35px #ff2d2d);
	}
	.sa-paug {
		fill: #ffdf3d;
		stroke: #c53030;
		stroke-width: 0.28;
		stroke-linejoin: round;
	}
	.sa-hud {
		position: absolute;
		top: var(--sp-3);
		left: var(--sp-3);
		display: flex;
		flex-direction: column;
		gap: 2px;
		padding: var(--sp-2) var(--sp-3);
		background: rgba(10, 11, 13, 0.8);
		color: #fff;
		border-radius: var(--r-sm);
		font-variant-numeric: tabular-nums;
		pointer-events: none;
		min-width: 9.5em;
	}
	.sa-kmh {
		font-family: var(--display);
		font-size: 26px;
		line-height: 1.05;
		display: flex;
		align-items: baseline;
		gap: 6px;
	}
	.sa-kmh small {
		font-size: 14px;
		opacity: 0.75;
	}
	.sa-n {
		font-family: var(--body);
		font-size: 12px;
		font-weight: 700;
		color: #111;
		background: var(--c);
		border-radius: 4px;
		padding: 1px 6px;
		align-self: center;
	}
	.sa-faas {
		font-size: 13px;
		font-weight: 600;
		color: var(--yellow-2);
		max-width: 16em;
	}
	.sa-faas.sa-halb {
		color: #ff8a80;
	}
	.sa-aeg {
		font-size: 12px;
		opacity: 0.7;
	}
	.sa-nupud {
		position: absolute;
		top: var(--sp-3);
		right: var(--sp-3);
		display: flex;
		gap: var(--sp-2);
		align-items: center;
	}
	.sa-btn,
	.sa-kord button {
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
	.sa-btn svg {
		width: 16px;
		height: 16px;
		fill: none;
		stroke: currentColor;
		stroke-width: 2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.sa-kord {
		display: flex;
		gap: 2px;
		background: rgba(255, 255, 255, 0.92);
		border-radius: var(--r-sm);
		padding: 2px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}
	.sa-kord button {
		box-shadow: none;
		background: transparent;
		padding: 4px 8px;
	}
	.sa-kord button[aria-pressed='true'] {
		background: var(--ink);
		color: #fff;
	}
	figcaption {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-1) var(--sp-4);
		margin-top: var(--sp-2);
		font-size: 13px;
		color: var(--muted);
	}
	.sa-l {
		display: inline-flex;
		align-items: center;
		gap: 6px;
	}
	.sa-l i {
		display: inline-block;
		width: 18px;
		height: 4px;
		border-radius: 2px;
	}
	.sa-l0 {
		background: repeating-linear-gradient(90deg, #8a929c 0 4px, transparent 4px 7px);
	}
	.sa-l1 {
		background: var(--yellow);
	}
	.sa-l2 {
		background: #e5484d;
	}
	@media (max-width: 560px) {
		.sa-scene > svg {
			aspect-ratio: 1.25;
		}
		.sa-kmh {
			font-size: 21px;
		}
		.sa-hud {
			min-width: 0;
			padding: 6px 8px;
		}
		.sa-nupud {
			top: auto;
			bottom: var(--sp-3);
		}
	}
</style>
