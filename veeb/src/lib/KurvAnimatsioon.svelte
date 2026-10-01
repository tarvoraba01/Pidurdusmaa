<script>
	/* Äkkpidurdus kurvis — animatsioon pealtvaates ($lib/kurvisoit.js tulemuse põhjal).
	   Kõik joonised meetrites (viewBox = meetrid), kaamera sõidab auto järel ja näitab
	   lõpus kogu teekonda. Tee välimus sõltub teeoludest (kuiv, märg, lumi, jää). */
	import { onMount, untrack } from 'svelte';
	import { RADA } from '$lib/kurvisoit.js';

	let { sim, pind = 'kuiv', t, LOC = 'et-EE' } = $props();

	const VARV = {
		kuiv: { maa: '#9dbf78', serv: '#bdb4a2', tee: '#565b63', joon: '#ffffff', puu: '#3d6b35', puu2: '#4f8044', jalg: 'rgba(25,25,25,.55)' },
		marg: { maa: '#7c9f5a', serv: '#8d8678', tee: '#363b43', joon: '#e9eef3', puu: '#2e5a2a', puu2: '#3c6e35', jalg: 'rgba(15,15,15,.6)' },
		lumi: { maa: '#f4f7fa', serv: '#e6ebf0', tee: '#d3d9e0', joon: 'rgba(255,255,255,.55)', puu: '#355a45', puu2: '#46705a', jalg: 'rgba(90,100,112,.7)' },
		jaa: { maa: '#eef3f7', serv: '#dde5ed', tee: '#93afc4', joon: 'rgba(255,255,255,.6)', puu: '#355a45', puu2: '#46705a', jalg: 'rgba(255,255,255,.85)' }
	};
	const V = $derived(VARV[pind] || VARV.kuiv);
	const talv = $derived(pind === 'lumi' || pind === 'jaa');

	/* ---------- tee geomeetria ---------- */
	const nihe = (p, d) => [p[0] + Math.sin(p[2]) * d, p[1] - Math.cos(p[2]) * d];
	function teeJoon(T, d) {
		const f = (x) => x.toFixed(2);
		if (T.sirge) {
			const a = nihe(T.punkt(-300), d), b = nihe(T.punkt(1200), d);
			return `M${f(a[0])} ${f(a[1])}L${f(b[0])} ${f(b[1])}`;
		}
		const a = nihe(T.punkt(-300), d), b = nihe(T.punkt(0), d), c = nihe(T.punkt(T.L), d), e = nihe(T.punkt(T.L + 1200), d);
		const r = T.R + d;
		return `M${f(a[0])} ${f(a[1])}L${f(b[0])} ${f(b[1])}A${f(r)} ${f(r)} 0 0 1 ${f(c[0])} ${f(c[1])}L${f(e[0])} ${f(e[1])}`;
	}
	/* deterministlik „juhuslik“ */
	const rnd = (i) => {
		const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
		return x - Math.floor(x);
	};

	let figW = $state(800);
	const AR = $derived(figW < 560 ? 1.25 : 1.6);
	const geo = $derived.by(() => {
		if (!sim) return null;
		const T = sim.tee;
		const kesk = RADA / 2; // keskjoon (sinu raja keskelt vasakule)
		const r = sim.rada;
		/* ülevaate piirid: kogu teekond + natuke teed ümber */
		let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
		const lisa = (x, y) => { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; };
		const sNae = sim.sNae;
		let sMax = sNae;
		for (const q of r) {
			if (q[7] >= 1) lisa(q[1], q[2]);
			const [s] = T.asend(q[1], q[2]);
			if (q[7] >= 1 && s > sMax) sMax = s;
		}
		for (let s = sNae - 15; s <= sMax + 15; s += 4) for (const d of [-2.5, RADA * 1.5 + 1]) { const p = nihe(T.punkt(s), d); lisa(p[0], p[1]); }
		const pad = 6;
		x0 -= pad; x1 += pad; y0 -= pad; y1 += pad;
		let w = x1 - x0, h = y1 - y0;
		if (w / h < AR) { const nw = h * AR; x0 -= (nw - w) / 2; w = nw; } else { const nh = w / AR; y0 -= (nh - h) / 2; h = nh; }
		const yld = { x: x0 + w / 2, y: y0 + h / 2, w };

		/* teepostid ja puud */
		const postid = [], puud = [];
		const sA = Math.min(-40, sNae - 60), sB = sMax + 260;
		for (let s = Math.ceil(sA / 25) * 25; s <= sB; s += 25) {
			postid.push(nihe(T.punkt(s), -RADA / 2 - 0.9), nihe(T.punkt(s), RADA * 1.5 + 0.9));
		}
		for (let i = 0, s = sA; s < sB; i++, s += 5 + rnd(i) * 7) {
			const dV = RADA * 1.5 + 7 + rnd(i + 99) * 14;
			const p = nihe(T.punkt(s), dV);
			puud.push([p[0], p[1], 1.6 + rnd(i + 7) * 1.6]);
			if (rnd(i + 3) > 0.45) {
				const dS = -RADA / 2 - 6 - rnd(i + 5) * 14;
				if (T.sirge || T.R + dS > 8) { const q = nihe(T.punkt(s + 2), dS); puud.push([q[0], q[1], 1.4 + rnd(i + 11) * 1.5]); }
			}
		}
		return {
			yld,
			tee: teeJoon(T, kesk),
			kesk: teeJoon(T, kesk),
			serv1: teeJoon(T, -RADA / 2 + 0.25),
			serv2: teeJoon(T, RADA * 1.5 - 0.25),
			rajad: [-0.8, 0.8, RADA - 0.8, RADA + 0.8].map((d) => teeJoon(T, d)),
			laigud: [0.2, RADA + 0.6].map((d) => teeJoon(T, d)),
			postid,
			puud
		};
	});

	/* ---------- libisemisjäljed (iga ratas eraldi), jälgjoon ---------- */
	const RATAS = [[1.25, -0.78], [1.25, 0.78], [-1.4, -0.78], [-1.4, 0.78]];
	const jaljed = $derived.by(() => {
		if (!sim) return [];
		const r = sim.rada;
		const out = [];
		for (let w = 0; w < 4; w++) {
			const esi = w < 2;
			let cur = null;
			for (let i = 0; i < r.length; i++) {
				const q = r[i];
				const lib = (esi ? q[5] : q[6]) > 0.96 && q[4] > 4;
				if (lib) {
					const [lx, ly] = RATAS[w];
					const c = Math.cos(q[3]), s = Math.sin(q[3]);
					const p = [q[1] + c * lx - s * ly, q[2] + s * lx + c * ly];
					if (!cur) { cur = { i0: i, p: [] }; out.push(cur); }
					cur.p.push(p);
				} else cur = null;
			}
		}
		return out;
	});

	/* ---------- taasesitus ---------- */
	let tSim = $state(1e9); // algul: lõppseis
	let mangib = $state(false);
	let kordaja = $state(1);
	let cam = $state({ x: 0, y: 0, w: 80 });
	let lopuAeg = $state(null); // millal animatsioon lõppes (ülevaatesse liikumiseks)
	let vaikne = false;
	let nahtav = false;
	let figEl;

	const tLopp = $derived(sim ? sim.rada[sim.rada.length - 1][0] : 0);
	function idx(tt) {
		const r = sim.rada;
		let lo = 0, hi = r.length - 1;
		if (tt >= r[hi][0]) return hi;
		while (hi - lo > 1) { const m = (lo + hi) >> 1; if (r[m][0] <= tt) lo = m; else hi = m; }
		return lo;
	}
	const hetk = $derived.by(() => {
		if (!sim) return null;
		const r = sim.rada;
		const i = idx(Math.min(tSim, tLopp));
		const q = r[i], n = r[Math.min(i + 1, r.length - 1)];
		const k = n[0] > q[0] ? Math.max(0, Math.min(1, (Math.min(tSim, tLopp) - q[0]) / (n[0] - q[0]))) : 0;
		let dp = n[3] - q[3];
		dp = Math.atan2(Math.sin(dp), Math.cos(dp));
		return { i, x: q[1] + (n[1] - q[1]) * k, y: q[2] + (n[2] - q[2]) * k, psi: q[3] + dp * k, kmh: q[4] + (n[4] - q[4]) * k, faas: q[7], useF: q[5], useR: q[6], t: Math.min(tSim, tLopp) };
	});
	const libiseb = $derived(hetk && hetk.faas < 3 && hetk.kmh > 4 && Math.max(hetk.useF, hetk.useR) > 0.97);

	const jarel = $derived(geo && geo.yld.w > 95);
	const CAMW = $derived(AR < 1.5 ? 52 : 70);

	/* kaamera: järgib autot, lõpus liigub ülevaatesse */
	function seaKaamera(dtR, kohe) {
		if (!geo || !hetk) return;
		const Y = geo.yld;
		if (!jarel || !mangib && lopuAeg === null) { cam = { x: Y.x, y: Y.y, w: Y.w }; return; }
		if (lopuAeg !== null) {
			const k = Math.min(1, (performance.now() - lopuAeg) / 1400);
			const e = k < 0.5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2;
			const a = camAlgus || cam;
			cam = { x: a.x + (Y.x - a.x) * e, y: a.y + (Y.y - a.y) * e, w: a.w + (Y.w - a.w) * e };
			return;
		}
		const tx = hetk.x + Math.cos(hetk.psi) * CAMW * 0.16, ty = hetk.y + Math.sin(hetk.psi) * CAMW * 0.16;
		const a = kohe ? 1 : Math.min(1, dtR * 3);
		cam = { x: cam.x + (tx - cam.x) * a, y: cam.y + (ty - cam.y) * a, w: CAMW };
	}
	let camAlgus = null;

	let raf = 0, eelmine = 0;
	function samm(nyyd) {
		const dtR = Math.min(0.1, (nyyd - eelmine) / 1000);
		eelmine = nyyd;
		if (mangib) {
			tSim += dtR * kordaja;
			if (tSim >= tLopp) {
				tSim = tLopp;
				mangib = false;
				lopuAeg = nyyd;
				camAlgus = { ...cam };
			}
		}
		seaKaamera(dtR, false);
		if (mangib || (lopuAeg !== null && nyyd - lopuAeg < 1500)) raf = requestAnimationFrame(samm);
		else raf = 0;
	}
	function mangi() {
		if (!sim) return;
		if (vaikne) { tSim = tLopp; lopuAeg = null; seaKaamera(0, true); return; }
		tSim = 0;
		lopuAeg = null;
		camAlgus = null;
		mangib = true;
		seaKaamera(0, true);
		if (!raf) { eelmine = performance.now(); raf = requestAnimationFrame(samm); }
	}
	/* uus arvutus → mängi uuesti (kui joonis on nähtav) */
	let ootel = 0;
	$effect(() => {
		sim;
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
	const vb = $derived(`${(cam.x - cam.w / 2).toFixed(2)} ${(cam.y - H / 2).toFixed(2)} ${cam.w.toFixed(2)} ${H.toFixed(2)}`);
	const pts = (a) => a.map((p) => p[0].toFixed(2) + ',' + p[1].toFixed(2)).join(' ');
	const jalgNahtav = $derived.by(() => {
		if (!hetk) return [];
		return jaljed.filter((j) => j.i0 <= hetk.i).map((j) => pts(j.p.slice(0, hetk.i - j.i0 + 1)));
	});
	const kulg = $derived.by(() => {
		if (!sim || !hetk) return { a: '', b: '', c: '' };
		const r = sim.rada;
		const a = [], b = [], c = [];
		for (let i = 0; i <= hetk.i; i++) {
			const q = r[i];
			(q[7] === 0 ? a : q[7] === 1 ? b : c).push([q[1], q[2]]);
		}
		if (b.length && a.length) b.unshift(a[a.length - 1]);
		if (c.length && b.length) c.unshift(b[b.length - 1]);
		c.push([hetk.x, hetk.y]);
		return { a: pts(a), b: pts(b), c: pts(c) };
	});
	const markid = $derived.by(() => {
		if (!sim) return [];
		const r = sim.rada;
		const out = [];
		const i1 = r.findIndex((q) => q[7] === 1), i2 = r.findIndex((q) => q[7] === 2);
		if (i1 >= 0) out.push({ x: r[i1][1], y: r[i1][2], k: 'nae', i: i1, tekst: t('märkad ohtu') });
		if (i2 >= 0) out.push({ x: r[i2][1], y: r[i2][2], k: 'pidur', i: i2, tekst: t('pidurdad') });
		return out;
	});
	const fs = $derived(cam.w / (AR < 1.5 ? 32 : 42));
	const autoSuur = $derived(Math.max(1, cam.w / 110));
	const faasTekst = $derived.by(() => {
		if (!hetk || !sim) return '';
		if (hetk.faas >= 3 || hetk.t >= tLopp) {
			if (sim.teelt) return t('Teelt väljas');
			return sim.ringi ? t('Seisab, auto pöördus ringi') : t('Seisab');
		}
		if (libiseb) return hetk.faas === 2 && hetk.useR > 0.97 && hetk.useR >= hetk.useF ? t('Tagaosa libiseb!') : t('Libiseb!');
		if (hetk.faas === 2) return t('Pidurdad (ABS)');
		if (hetk.faas === 1) return t('Märkad ohtu, reageerid…');
		return sim.tee.sirge ? t('Sõidad') : t('Sõidad kurvi');
	});
	const lopp = $derived(sim && hetk && hetk.t >= tLopp);
	const nf = (x, d = 0) => x.toLocaleString(LOC, { minimumFractionDigits: d, maximumFractionDigits: d });
	const mootkava = $derived(cam.w > 160 ? 50 : cam.w > 70 ? 20 : 10);
</script>

<figure class="ka" class:talv bind:this={figEl} bind:clientWidth={figW}>
	{#if sim && geo && hetk}
		<div class="ka-scene">
		<svg viewBox={vb} role="img" aria-label={t('Auto teekond pealtvaates')} preserveAspectRatio="xMidYMid slice">
			<defs>
				<pattern id="ka-lumi" width="3" height="3" patternUnits="userSpaceOnUse"><circle cx=".6" cy=".8" r=".18" fill="#dfe6ee" /><circle cx="2.1" cy="2.2" r=".14" fill="#e7edf3" /></pattern>
				<linearGradient id="ka-laik" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0" /><stop offset=".5" stop-color="#fff" stop-opacity=".9" /><stop offset="1" stop-color="#fff" stop-opacity="0" /></linearGradient>
			</defs>
			<rect x={cam.x - 2000} y={cam.y - 2000} width="4000" height="4000" fill={V.maa} />
			{#if talv}<rect x={cam.x - 2000} y={cam.y - 2000} width="4000" height="4000" fill="url(#ka-lumi)" />{/if}
			<!-- teepeenar / lumevall -->
			<path d={geo.tee} class="ka-t" stroke={V.serv} stroke-width={RADA * 2 + (talv ? 3.2 : 1.8)} />
			{#if talv}<path d={geo.tee} class="ka-t" stroke="#fff" stroke-opacity=".7" stroke-width={RADA * 2 + 1.2} />{/if}
			<path d={geo.tee} class="ka-t" stroke={V.tee} stroke-width={RADA * 2} />
			<!-- teeolud -->
			{#if pind === 'marg'}
				{#each geo.laigud as d, i (i)}
					<path {d} class="ka-t ka-r" stroke="#c9dcec" stroke-opacity=".3" stroke-width=".35" stroke-dasharray="9 5 2 7" />
					<path {d} class="ka-t ka-r" stroke="#c9dcec" stroke-opacity=".18" stroke-width="1.4" stroke-dasharray="3 17 6 11" stroke-dashoffset="5" />
				{/each}
				{#each geo.rajad as d, i (i)}<path {d} class="ka-t" stroke="#15191e" stroke-opacity=".45" stroke-width=".5" />{/each}
			{:else if pind === 'lumi'}
				{#each geo.rajad as d, i (i)}<path {d} class="ka-t" stroke="#9aa5b1" stroke-opacity=".8" stroke-width=".5" />{/each}
				{#each geo.laigud as d, i (i)}<path {d} class="ka-t ka-r" stroke="#fff" stroke-opacity=".8" stroke-width=".9" stroke-dasharray="1.5 4 .8 7" />{/each}
			{:else if pind === 'jaa'}
				{#each geo.laigud as d, i (i)}<path {d} class="ka-t ka-r" stroke="#eaf5ff" stroke-opacity=".45" stroke-width="2.4" stroke-dasharray="18 7 6 12" />{/each}
				{#each geo.rajad as d, i (i)}<path {d} class="ka-t" stroke="#6f8ea6" stroke-opacity=".75" stroke-width=".5" />{/each}
				{#each geo.laigud as d, i (i)}<path {d} class="ka-t ka-r" stroke="#fff" stroke-opacity=".7" stroke-width=".25" stroke-dasharray="10 9 3 14" stroke-dashoffset="4" />{/each}
			{/if}
			<!-- teekattemärgised -->
			<path d={geo.kesk} class="ka-t" stroke={V.joon} stroke-width=".15" stroke-dasharray="3 9" />
			{#if !talv}
				<path d={geo.serv1} class="ka-t" stroke={V.joon} stroke-width=".15" />
				<path d={geo.serv2} class="ka-t" stroke={V.joon} stroke-width=".15" />
			{/if}
			<!-- teepostid ja puud -->
			{#each geo.postid as p, i (i)}<rect x={p[0] - 0.14} y={p[1] - 0.14} width=".28" height=".28" fill="#fff" stroke="#22262c" stroke-width=".07" />{/each}
			{#each geo.puud as p, i (i)}
				<circle cx={p[0] + 0.4} cy={p[1] + 0.5} r={p[2]} fill="#000" opacity=".12" />
				<circle cx={p[0]} cy={p[1]} r={p[2]} fill={V.puu} />
				<circle cx={p[0] - p[2] * 0.25} cy={p[1] - p[2] * 0.25} r={p[2] * 0.55} fill={V.puu2} />
				{#if talv}<circle cx={p[0] - p[2] * 0.3} cy={p[1] - p[2] * 0.35} r={p[2] * 0.3} fill="#fff" opacity=".75" />{/if}
			{/each}
			<!-- jäljed -->
			{#each jalgNahtav as p, i (i)}<polyline points={p} class="ka-jalg" stroke={V.jalg} />{/each}
			<polyline points={kulg.a} class="ka-kulg ka-k0" stroke-width={fs * 0.12} />
			<polyline points={kulg.b} class="ka-kulg ka-k1" stroke-width={fs * 0.16} />
			<polyline points={kulg.c} class="ka-kulg ka-k2" stroke-width={fs * 0.16} />
			{#each markid as mk (mk.k)}
				{#if mk.i <= hetk.i}
					<circle cx={mk.x} cy={mk.y} r={fs * 0.32} class="ka-m ka-m-{mk.k}" stroke-width={fs * 0.08} />
					<text x={mk.x - fs * 0.7} y={mk.y + fs * 0.35} font-size={fs} text-anchor="end" class="ka-tx" stroke-width={fs * 0.22}>{mk.tekst}</text>
				{/if}
			{/each}
			{#if lopp && sim.teelt}
				<g transform="translate({hetk.x} {hetk.y}) scale({fs / 2})">
					<path d="M0-2.6 .7-1 2.4-1.8 1.4-.3 2.8.6 1 .8 1.3 2.6 0 1.3-1.3 2.6-1 .8-2.8.6-1.4-.3-2.4-1.8-.7-1Z" class="ka-paug" />
				</g>
			{/if}
			<!-- auto -->
			<g transform="translate({hetk.x.toFixed(3)} {hetk.y.toFixed(3)}) rotate({((hetk.psi * 180) / Math.PI).toFixed(2)}) scale({autoSuur})">
				<rect x="-2.3" y="-1.05" width="4.6" height="2.1" rx=".5" fill="#000" opacity=".18" transform="translate(.15 .2)" />
				{#each RATAS as [lx, ly], i (i)}<rect x={lx - 0.36} y={ly < 0 ? -1.0 : 0.76} width=".72" height=".24" rx=".08" fill="#15171b" />{/each}
				<rect x="-2.2" y="-0.9" width="4.4" height="1.8" rx=".55" class="ka-keha" class:libiseb />
				<path d="M.55 -.72 Q1.25 0 .55 .72 L.05 .62 Q.4 0 .05 -.62Z" fill="#26303b" />
				<path d="M-1.35 -.66 Q-1.75 0 -1.35 .66 L-1.0 .56 Q-1.25 0 -1.0 -.56Z" fill="#26303b" />
				<rect x="-0.95" y="-0.66" width="0.95" height="1.32" rx=".2" fill="#000" opacity=".08" />
				{#if hetk.faas === 2 && !lopp}
					<rect x="-2.28" y="-0.8" width=".16" height=".42" rx=".05" class="ka-pidur" />
					<rect x="-2.28" y="0.38" width=".16" height=".42" rx=".05" class="ka-pidur" />
				{/if}
				<rect x="2.08" y="-0.78" width=".12" height=".34" rx=".05" fill="#fffbe6" />
				<rect x="2.08" y="0.44" width=".12" height=".34" rx=".05" fill="#fffbe6" />
			</g>
			<!-- mootkavakava -->
			<g transform="translate({cam.x - cam.w / 2 + fs * 0.9} {cam.y + H / 2 - fs * 0.9})">
				<rect x={-fs * 0.4} y={-fs * 1.5} width={mootkava + fs * 0.8} height={fs * 2.1} rx={fs * 0.3} fill="#fff" opacity=".82" />
				<path d="M0 0H{mootkava}M0 {-fs * 0.3}V0M{mootkava} {-fs * 0.3}V0" stroke="#111" stroke-width={fs * 0.09} fill="none" />
				<text x={mootkava / 2} y={-fs * 0.45} font-size={fs * 0.8} text-anchor="middle" fill="#111">{mootkava} {t('m')}</text>
			</g>
		</svg>
		<div class="ka-hud" aria-hidden="true">
			<b class="ka-kmh">{nf(lopp && sim.peatus ? 0 : Math.max(0, hetk.kmh))} <small>{t('km/h')}</small></b>
			<span class="ka-faas" class:ka-halb={libiseb || (lopp && (sim.teelt || sim.ringi))}>{faasTekst}</span>
			<span class="ka-aeg">{nf(hetk.t, 1)} {t('s')}</span>
		</div>
		<div class="ka-nupud">
			<button type="button" class="ka-btn" onclick={mangi}>
				<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M15.5 10a5.5 5.5 0 1 1-1.8-4.1M15.5 3.5v3h-3" /></svg>
				{t('Mängi uuesti')}
			</button>
			<div class="ka-kord" role="group" aria-label={t('Kiirus')}>
				{#each [[0.5, '½×'], [1, '1×'], [2, '2×']] as [k, n] (k)}
					<button type="button" aria-pressed={kordaja === k} onclick={() => (kordaja = k)}>{n}</button>
				{/each}
			</div>
		</div>
		</div>
	{/if}
	<figcaption>
		<span class="ka-l"><i class="ka-l0"></i>{t('sõidad')}</span>
		<span class="ka-l"><i class="ka-l1"></i>{t('reageerid (1 s)')}</span>
		<span class="ka-l"><i class="ka-l2"></i>{t('pidurdad')}</span>
		<span class="ka-l"><i class="ka-l3"></i>{t('rehvid libisevad')}</span>
	</figcaption>
</figure>

<style>
	.ka {
		position: relative;
		margin: var(--sp-4) 0 0;
	}
	.ka-scene {
		position: relative;
	}
	.ka-scene > svg {
		width: 100%;
		height: auto;
		aspect-ratio: 1.6;
		border-radius: var(--r);
		background: #9dbf78;
		display: block;
	}
	.ka-t {
		fill: none;
		stroke-linecap: butt;
	}
	.ka-r {
		stroke-linecap: round;
	}
	.ka-jalg {
		fill: none;
		stroke-width: 0.26;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.ka-kulg {
		fill: none;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.ka-k0 {
		stroke: #fff;
		stroke-opacity: 0.55;
		stroke-dasharray: 0.6 0.9;
	}
	.ka-k1 {
		stroke: var(--yellow);
	}
	.ka-k2 {
		stroke: #e5484d;
	}
	.ka-m {
		fill: #fff;
	}
	.ka-m-nae {
		stroke: #b98900;
	}
	.ka-m-pidur {
		stroke: #c53030;
	}
	.ka-tx {
		fill: #111;
		stroke: #fff;
		paint-order: stroke;
		font-weight: 700;
		font-family: var(--body);
	}
	.ka-keha {
		fill: var(--yellow);
		stroke: #171200;
		stroke-width: 0.09;
	}
	.ka-keha.libiseb {
		fill: #ffb020;
	}
	.ka-pidur {
		fill: #ff2d2d;
		filter: drop-shadow(0 0 0.35px #ff2d2d);
	}
	.ka-paug {
		fill: #ffdf3d;
		stroke: #c53030;
		stroke-width: 0.28;
		stroke-linejoin: round;
	}
	.ka-hud {
		position: absolute;
		top: var(--sp-3);
		left: var(--sp-3);
		display: flex;
		flex-direction: column;
		gap: 2px;
		padding: var(--sp-2) var(--sp-3);
		background: rgba(10, 11, 13, 0.78);
		color: #fff;
		border-radius: var(--r-sm);
		font-variant-numeric: tabular-nums;
		pointer-events: none;
		min-width: 9.5em;
	}
	.ka-kmh {
		font-family: var(--display);
		font-size: 30px;
		line-height: 1;
	}
	.ka-kmh small {
		font-size: 15px;
		opacity: 0.75;
	}
	.ka-faas {
		font-size: 13px;
		font-weight: 600;
		color: var(--yellow-2);
	}
	.ka-faas.ka-halb {
		color: #ff8a80;
	}
	.ka-aeg {
		font-size: 12px;
		opacity: 0.7;
	}
	.ka-nupud {
		position: absolute;
		top: var(--sp-3);
		right: var(--sp-3);
		display: flex;
		gap: var(--sp-2);
		align-items: center;
	}
	.ka-btn,
	.ka-kord button {
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
	.ka-btn svg {
		width: 16px;
		height: 16px;
		fill: none;
		stroke: currentColor;
		stroke-width: 2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.ka-kord {
		display: flex;
		gap: 2px;
		background: rgba(255, 255, 255, 0.92);
		border-radius: var(--r-sm);
		padding: 2px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
	}
	.ka-kord button {
		box-shadow: none;
		background: transparent;
		padding: 4px 8px;
	}
	.ka-kord button[aria-pressed='true'] {
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
	.ka-l {
		display: inline-flex;
		align-items: center;
		gap: 6px;
	}
	.ka-l i {
		display: inline-block;
		width: 18px;
		height: 4px;
		border-radius: 2px;
	}
	.ka-l0 {
		background: repeating-linear-gradient(90deg, #8a929c 0 4px, transparent 4px 7px);
	}
	.ka-l1 {
		background: var(--yellow);
	}
	.ka-l2 {
		background: #e5484d;
	}
	.ka-l3 {
		background: #2b2f36;
		height: 3px !important;
		box-shadow: 0 4px 0 #2b2f36;
	}
	@media (max-width: 560px) {
		.ka-scene > svg {
			aspect-ratio: 1.25;
		}
		.ka-kmh {
			font-size: 24px;
		}
		.ka-hud {
			min-width: 0;
			padding: 6px 8px;
		}
		.ka-nupud {
			top: auto;
			bottom: var(--sp-3);
		}
	}
</style>
