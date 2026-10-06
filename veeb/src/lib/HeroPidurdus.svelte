<script>
	/* Avalehe hero: kolm autot pidurdavad samal hetkel 90 km/h pealt —
	   kuival, märjal ja lumel. Näitab ühe pilguga, mida leht teeb.
	   Numbrid arvutab server ehitusel sama mudeliga (routes/+page.server.js
	   heroNumbrid): VW Golf 8, 205/55 R16, uus tüüpiline rehv — kuival ja
	   märjal suverehv, lumel Põhjamaade talverehv. Käsitsi numbreid ei ole. Arvutis jookseb tee alt üles, telefonis vasakult paremale. */
	import { onMount } from 'svelte';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const LOC = { et: 'et-EE', ru: 'ru-RU', en: 'en-GB' }[keel.lang] || 'et-EE';

	let { suund = 'ules', d } = $props(); // suund: 'ules' (arvuti) | 'paremale' (telefon); d = { kuiv, marg, lumi } m

	const V = 90 / 3.6;
	const rajad = [
		{ k: 'kuiv', nimi: t('Kuiv'), d: d.kuiv },
		{ k: 'marg', nimi: t('Märg'), d: d.marg },
		{ k: 'lumi', nimi: t('Lumi'), d: d.lumi }
	];
	const EEL = 0.7; // s enne pidurdust (auto sõidab 90 km/h)
	const KORD = 1.35; // kiirendus, et lumi ei veniks
	const PAUS = 2.2;
	const tStop = (d) => (2 * d) / V;
	const tKokku = $derived(EEL + tStop(Math.max(...rajad.map((r) => r.d))) + PAUS);

	let w = $state(360), h = $state(440);
	let tt = $state(99);
	let el;
	const ules = $derived(suund === 'ules');

	/* geomeetria: piki teed = "a" (meetrid), risti = rada */
	const PIKK = $derived(ules ? h : w);
	const RISTI = $derived(ules ? w : h);
	const M_ALGUS = $derived(suund === 'ules' ? 6 : 16), M_LOPP = 90; // nähtav lõik meetrites
	const marg = $derived(ules ? 30 : 6);
	const pxm = $derived((PIKK - marg * 2) / (M_LOPP + M_ALGUS));
	/* risti-suunas: telefonis jääb alla ruumi allkirjale */
	const RISTI_K = $derived(ules ? RISTI : RISTI - 18);
	const raLai = $derived(Math.min(ules ? 74 : 50, (RISTI_K - 16) / 3 - 8));
	const raVahe = $derived((RISTI_K - raLai * 3) / 4);

	function asend(d, aeg) {
		const s = aeg - EEL;
		if (s <= 0) return { m: V * s, kmh: 90, pidur: false, seis: false };
		const a = (V * V) / (2 * d), ts = V / a;
		if (s >= ts) return { m: d, kmh: 0, pidur: false, seis: true };
		return { m: V * s - (a * s * s) / 2, kmh: (V - a * s) * 3.6, pidur: true, seis: false };
	}
	/* meetrid → ekraan */
	const P = (m, i, nihe = 0) => {
		const a = marg + (m + M_ALGUS) * pxm;
		const r = raVahe + i * (raLai + raVahe) + raLai / 2 + nihe;
		return ules ? [r, PIKK - a] : [a, r];
	};
	const nf = (x) => x.toLocaleString(LOC, { minimumFractionDigits: 1, maximumFractionDigits: 1 });

	onMount(() => {
		const ro = new ResizeObserver(() => { w = el.clientWidth; h = el.clientHeight; });
		ro.observe(el);
		w = el.clientWidth; h = el.clientHeight;
		const vaikne = matchMedia('(prefers-reduced-motion: reduce)').matches;
		if (vaikne) { tt = 99; return () => ro.disconnect(); }
		let raf = 0, t0 = performance.now(), nahtav = true;
		const io = new IntersectionObserver((e) => { nahtav = e[0].isIntersecting; if (nahtav && !raf) { t0 = performance.now() - tt * 1000 / KORD; raf = requestAnimationFrame(samm); } }, { threshold: 0.05 });
		io.observe(el);
		function samm(n) {
			tt = (((n - t0) / 1000) * KORD) % tKokku;
			raf = nahtav ? requestAnimationFrame(samm) : 0;
		}
		raf = requestAnimationFrame(samm);
		return () => { cancelAnimationFrame(raf); io.disconnect(); ro.disconnect(); };
	});

	const autod = $derived(rajad.map((r) => ({ ...r, ...asend(r.d, tt) })));
	const marke = $derived(Array.from({ length: 10 }, (_, i) => i * 10));
	const PINNAD = {
		kuiv: { tee: '#24272d', joon: 'rgba(255,255,255,.35)' },
		marg: { tee: '#14181e', joon: 'rgba(200,220,240,.3)' },
		lumi: { tee: '#9aa4b1', joon: 'rgba(255,255,255,.0)' }
	};
	const AUTO_L = 4.3 * 1.35, AUTO_W = 1.8 * 1.35;
</script>

<div class="hpa" class:hp-p={!ules} bind:this={el} aria-hidden="true">
	<svg width={w} height={h} viewBox="0 0 {w} {h}">
		<defs>
			<linearGradient id="hp-marg" x1="0" x2={ules ? 0 : 1} y1={ules ? 1 : 0} y2="0">
				<stop offset="0" stop-color="#9fb8d6" stop-opacity=".0" />
				<stop offset=".5" stop-color="#9fb8d6" stop-opacity=".12" />
				<stop offset="1" stop-color="#9fb8d6" stop-opacity=".0" />
			</linearGradient>
			<radialGradient id="hp-tuli"><stop offset="0" stop-color="#fff6d0" stop-opacity=".55" /><stop offset="1" stop-color="#fff6d0" stop-opacity="0" /></radialGradient>
		</defs>
		<!-- rajad -->
		{#each autod as r, i (r.k)}
			{@const [x0, y0] = P(-M_ALGUS, i, -raLai / 2)}
			{@const [x1, y1] = P(M_LOPP, i, raLai / 2)}
			<rect x={Math.min(x0, x1)} y={Math.min(y0, y1)} width={Math.abs(x1 - x0)} height={Math.abs(y1 - y0)} rx="6" fill={PINNAD[r.k].tee} />
			{#if r.k === 'marg'}<rect x={Math.min(x0, x1)} y={Math.min(y0, y1)} width={Math.abs(x1 - x0)} height={Math.abs(y1 - y0)} rx="6" fill="url(#hp-marg)" />{/if}
			{#if r.k === 'lumi'}
				{#each [-0.28, 0.28] as n (n)}
					{@const [a0, b0] = P(-M_ALGUS + 2, i, n * raLai)}
					{@const [a1, b1] = P(M_LOPP - 2, i, n * raLai)}
					<line x1={a0} y1={b0} x2={a1} y2={b1} stroke="#a9b3bf" stroke-width={raLai * 0.16} stroke-linecap="round" opacity=".55" />
				{/each}
			{/if}
			<!-- algusjoon: siit pidur põhja -->
			{@const [s0, t0] = P(0, i, -raLai / 2)}
			{@const [s1, t1] = P(0, i, raLai / 2)}
			<line x1={s0} y1={t0} x2={s1} y2={t1} stroke="#ffc20e" stroke-width="2" stroke-dasharray="4 3" />
			<!-- pidurdusjälg -->
			{#if r.m > 0}
				{#each [-0.22, 0.22] as n (n)}
					{@const [j0, k0] = P(0, i, n * raLai)}
					{@const [j1, k1] = P(r.m - AUTO_L * 0.75, i, n * raLai)}
					{#if r.m - AUTO_L * 0.75 > 0}<line x1={j0} y1={k0} x2={j1} y2={k1} stroke={r.k === 'lumi' ? '#5d6875' : '#e5484d'} stroke-width={Math.max(1.5, raLai * 0.05)} stroke-linecap="round" opacity=".6" />{/if}
				{/each}
			{/if}
			<!-- auto -->
			{@const [cx, cy] = P(r.m - AUTO_L / 2, i)}
			{@const L = Math.max(0, AUTO_L * pxm)}
			{@const W = Math.max(0, Math.min(AUTO_W * pxm * 1.25, raLai * 0.62))}
			<g transform="translate({cx} {cy}) rotate({ules ? -90 : 0})">
				{#if !r.seis}<ellipse cx={L / 2 + L * 0.9} cy="0" rx={L * 0.95} ry={W * 0.7} fill="url(#hp-tuli)" />{/if}
				<rect x={-L / 2} y={-W / 2} width={L} height={W} rx={W * 0.32} fill="#ffc20e" stroke="#171200" stroke-width="1" />
				<rect x={L * 0.08} y={-W * 0.38} width={L * 0.2} height={W * 0.76} rx="2" fill="#26303b" />
				<rect x={-L * 0.36} y={-W * 0.34} width={L * 0.14} height={W * 0.68} rx="2" fill="#26303b" />
				{#if r.pidur}<rect x={-L / 2 - 1.5} y={-W * 0.42} width="3" height={W * 0.84} rx="1.5" fill="#ff2d2d" />{/if}
			</g>
			<!-- silt: raja nimi alguses, number auto ees -->
			{#if ules}
				{@const [lx, ly] = P(-M_ALGUS, i)}
				<text x={lx} y={ly + 18} class="hp-n" text-anchor="middle">{r.nimi}</text>
			{:else}
				{@const [lx, ly] = P(-M_ALGUS, i)}
				<text x={lx + 6} y={ly + 4} class="hp-n" class:hp-tume={r.k === 'lumi'}>{r.nimi}</text>
			{/if}
			{#if r.seis || r.m > 1}
				{@const lopus = !ules && r.m > M_LOPP - 22}
				{@const [nx, ny] = ules ? P(Math.max(r.m, 4) + 4.2, i) : P(lopus ? r.m - AUTO_L - 1.5 : Math.max(r.m, 4) + 1.5, i)}
				<text x={nx} y={ules ? ny : ny + 4.5} class="hp-m" class:hp-seis={r.seis} class:hp-tume={r.k === 'lumi'} text-anchor={ules ? 'middle' : lopus ? 'end' : 'start'}>{r.seis ? nf(r.d) + ' m' : Math.round(r.kmh) + ' km/h'}</text>
			{/if}
		{/each}
	</svg>
	<p class="hp-cap">{t('Pidurdusteekond 90 → 0 km/h, uued rehvid')}</p>
</div>

<style>
	.hpa {
		position: relative;
		width: 100%;
		height: 100%;
	}
	.hpa svg {
		display: block;
		overflow: visible;
	}
	.hp-n {
		fill: #c9ced6;
		font: 600 12px/1 Inter, system-ui, sans-serif;
		letter-spacing: 0.04em;
		text-transform: uppercase;
	}
	.hp-m {
		fill: #fff;
		font: 700 13px/1 Inter, system-ui, sans-serif;
		font-variant-numeric: tabular-nums;
		paint-order: stroke;
		stroke: #050506;
		stroke-width: 4px;
	}
	.hp-m.hp-seis {
		fill: var(--yellow);
		font-size: 15px;
	}
	.hp-n.hp-tume {
		fill: #1d232b;
	}
	.hp-m.hp-tume {
		fill: #10151b;
		stroke: #b8c0cb;
	}
	.hp-m.hp-seis.hp-tume {
		fill: #10151b;
	}
	.hp-cap {
		position: absolute;
		left: 0;
		right: 0;
		top: 0;
		margin: 0;
		text-align: center;
		font-size: 11.5px;
		color: #8b929e;
	}
	.hp-p .hp-cap {
		top: auto;
		bottom: -2px;
	}
</style>
