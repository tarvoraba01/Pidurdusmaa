<script>
	/* PÄEVA ETAPP: kruusaralli aja peale. Üks mäng: kuiv kruus, päevavalgus, kaamera auto taga.
	   Rada on päeva järgi kõigile sama ($lib/etapp.js), füüsika ühe roopa mudel (rehvi libisemine,
	   koormuse ülekanne, käsipidur), haare samast mootorist mis kalkulaatoris.
	   Teelt välja: tagasi eelmisesse kontrollpunkti, kell käib edasi. Õpetlik osa on kõrval:
	   avarii korral üks lause kurvi piirkiirusega, finišis üks „kas teadsid“. */
	import { onMount, onDestroy } from 'svelte';
	import { version } from '$app/environment';
	import { joonista, TEE } from '$lib/tee3d.js';
	import { looEtapp, paevaNr, rehv, haardeTabel, piirkiirus, koverus, samm, uusAuto, ALGUS_Z, PIKKUS, KP_VAHE } from '$lib/etapp.js';

	const nr = paevaNr();
	const E = looEtapp(nr);
	const KAT = 'SUMMER_TOURING';
	let olek = $state('laeb'); /* laeb | algus | soit | avarii | finis */
	let teade = $state(null);
	let tulemus = $state(null);
	let taisekraan = $state(false);
	let mang = $state({});

	let P = null, veh = null, gClass = null, H = null, Hasf = null;
	let cv, ctx, W = 800, H2 = 500, raf = 0, eelm = 0, aeg0 = 0, ekraan;
	const o = uusAuto(ALGUS_Z - 14, TEE.KAAM_X);
	const sis = { gaas: false, pidur: false, kasi: false, vasak: false, parem: false };
	let kell = 0, kp = 0, sohiAeg = 0, avariid = 0, tipp = 0, ajalugu = [], risti = 0, vaheajad = [];
	let camX = TEE.KAAM_X, camPsi = 0, loendus = 0;

	const aegTekst = (s) => Math.floor(s / 60) + ':' + (s % 60).toFixed(1).padStart(4, '0').replace('.', ',');

	onMount(async () => {
		try { mang = JSON.parse(localStorage.getItem('pm_etapp') || '{}') || {}; } catch {}
		ctx = cv.getContext('2d');
		suurus();
		window.addEventListener('resize', suurus);
		await import('$lib/engine.js');
		P = globalThis.Pidurdus;
		const d = await (await fetch('/data/vaikeauto.json?v=' + encodeURIComponent(version))).json();
		veh = d.vehicles[0]; gClass = d.gClass;
		H = haardeTabel(P, rehv(KAT, veh, gClass), veh, E.olud.cond);
		Hasf = haardeTabel(P, rehv(KAT, veh, gClass), veh, { surface: 'ASPHALT', waterMm: 0, tempC: 14 });
		olek = 'algus';
		raf = requestAnimationFrame(kaader);
	});
	onDestroy(() => {
		if (typeof window === 'undefined') return;
		cancelAnimationFrame(raf); window.removeEventListener('resize', suurus);
		try { document.documentElement.style.overflow = ''; } catch {}
	});
	function suurus() {
		if (!cv) return;
		const dpr = Math.min(2, window.devicePixelRatio || 1), w = cv.clientWidth || 800;
		const h = taisekraan ? cv.clientHeight || w * 0.6 : w * 0.6;
		W = Math.round(w * dpr); H2 = Math.round(h * dpr);
		cv.width = W; cv.height = H2;
	}

	/* ---------- mänguvoog ---------- */
	function alusta() {
		if (!H) return;
		Object.assign(o, uusAuto(ALGUS_Z - 6, TEE.KAAM_X));
		kp = 0; kell = 0; avariid = 0; tipp = 0; ajalugu = []; vaheajad = []; risti = 0;
		camX = o.x; camPsi = 0;
		teade = null; tulemus = null; olek = 'soit'; loendus = 3;
		try { if (!taisekraan && matchMedia('(pointer: coarse)').matches) taisEkraan(); } catch {}
		track('algus');
		setTimeout(() => ekraan?.querySelector('.et-ala')?.focus(), 30);
	}
	function avarii() {
		avariid++;
		const v = Math.max(o.v, ...ajalugu.map((x) => x[1])) * 3.6;
		const n = Math.floor(o.z / TEE.SEG);
		const kurv = E.kurvid.find((k) => n >= k.n0 - 2 && n <= k.n1 + 8);
		teade = kurv
			? `Liiga kiire. Selle kurvi piirkiirus kruusal on umbes ${Math.round(piirkiirus(H, kurv.R))} km/h, sina tulid ${Math.round(v)} km/h.`
			: `Teelt välja ${Math.round(v)} km/h pealt.`;
		track('avarii', Math.round(v) + ' km/h');
		olek = 'avarii';
		sohiAeg = 0;
	}
	function taasta() {
		Object.assign(o, uusAuto(ALGUS_Z + kp * KP_VAHE + 2, TEE.KAAM_X));
		camX = o.x; camPsi = 0; ajalugu = []; risti = 0;
		teade = null; olek = 'soit';
	}
	function finis() {
		olek = 'finis';
		const p = mang[nr] || { parim: null, katseid: 0 };
		p.katseid = (p.katseid || 0) + 1;
		const uus = !p.parim || kell < p.parim;
		if (uus) p.parim = Math.round(kell * 10) / 10;
		mang = { ...mang, [nr]: p };
		try { localStorage.setItem('pm_etapp', JSON.stringify(mang)); } catch {}
		const k = E.kurvid.reduce((a, b) => (b.R < a.R ? b : a));
		tulemus = { aeg: kell, uus, parim: p.parim, avariid, tipp: Math.round(tipp * 3.6), R: k.R, kruus: Math.round(piirkiirus(H, k.R)), asfalt: Math.round(piirkiirus(Hasf, k.R)) };
		track('finis', aegTekst(kell) + ' · avariid ' + avariid);
	}

	/* ---------- kaader ---------- */
	function kaader(now) {
		raf = requestAnimationFrame(kaader);
		if (!ctx) return;
		const dt = eelm ? Math.min(0.05, (now - eelm) / 1000) : 0.016;
		eelm = now;
		if (!aeg0) aeg0 = now;
		if (olek === 'soit' && H) {
			if (loendus > 0) loendus = Math.max(0, loendus - dt); else fyysika(dt);
		} else if (olek === 'avarii') { sohiAeg += dt; kell += dt; o.vx = o.v = Math.max(0, o.v - 14 * dt); o.vy = 0; o.r = 0; o.z += o.v * dt; if (sohiAeg > 2.4) taasta(); }
		else if (olek === 'finis') { o.vx = o.v = Math.max(0, o.v - 7 * dt); o.vy = 0; o.r = 0; o.z += o.v * Math.cos(o.psi) * dt; }
		/* kaamera järgib autot pehmelt: libisedes paistab auto nurga all */
		/* kaamera vaatab sõidusuunas (mitte auto nina suunas): libisedes paistab auto külgsi;
		   kaamera on auto taga sama joone peal, nii et auto jääb pildi keskele */
		const suund = o.psi + (o.v > 2 ? Math.atan2(o.vy, Math.max(1, o.vx)) : 0);
		camPsi += (suund - camPsi) * Math.min(1, dt * 4);
		camX = o.x - camPsi * 9.4;
		joonista(ctx, W, H2, E.tee, {
			taga: true, z: o.z, kmh: o.v * 3.6, oo: false, ilm: 'kuiv', kate: 'kruus', px: camX, psi: camPsi, cx: o.x, cpsi: o.psi,
			pidur: sis.pidur && olek === 'soit', libisemine: o.libiseb ? 1 : Math.min(1, Math.abs(o.vy) / 3), crash: false, aeg: (now - aeg0) / 1000
		});
		hud();
	}
	function fyysika(dt) {
		const tSisend = { gaas: sis.gaas, pidur: sis.pidur, kasi: sis.kasi, roolSiht: (sis.parem ? 1 : 0) - (sis.vasak ? 1 : 0) };
		const maas = Math.abs(o.x) > TEE.TEE_L + 0.3;
		let syndmus = null;
		for (let i = 0; i < 8 && !syndmus; i++) if (samm(o, tSisend, dt / 8, koverus(E.tee, o.z), H.a, maas) === 'teelt') syndmus = 'teelt';
		if (o.z >= ALGUS_Z) kell += dt;
		tipp = Math.max(tipp, o.v);
		ajalugu.push([kell, o.v]); if (ajalugu.length > 90) ajalugu.shift();
		while (kp < 4 && o.z >= ALGUS_Z + (kp + 1) * KP_VAHE) { kp++; vaheajad = [...vaheajad, kell]; }
		risti = o.v < 1 && Math.abs(o.psi) > 0.9 ? risti + dt : 0;
		if (syndmus || risti > 1.5) { risti = 0; avarii(); return; }
		if (o.z >= ALGUS_Z + PIKKUS) finis();
	}
	/* kaardilugeja: järgmine kurv ees */
	function noot() {
		const n = Math.floor(o.z / TEE.SEG);
		const k = E.kurvid.find((x) => x.n1 > n + 1);
		if (!k) return null;
		const d = k.n0 * TEE.SEG - o.z;
		if (d > 160) return null;
		return { suund: k.suund, aste: k.aste, d: Math.max(0, Math.round(d / 10) * 10) };
	}
	function hud() {
		const s = Math.max(W / 900, Math.min(2, window.devicePixelRatio || 1) * 0.8);
		ctx.save();
		const DF = '"Barlow Condensed", "Arial Narrow", sans-serif';
		/* aeg */
		ctx.fillStyle = 'rgba(10,11,13,0.6)'; ctx.fillRect(12 * s, 12 * s, 150 * s, 50 * s);
		ctx.fillStyle = '#ffc20e'; ctx.font = `700 ${34 * s}px ${DF}`; ctx.fillText(aegTekst(kell), 22 * s, 48 * s);
		/* kiirus */
		ctx.textAlign = 'right';
		ctx.fillStyle = 'rgba(10,11,13,0.6)'; ctx.fillRect(W - 122 * s, H2 - 70 * s, 110 * s, 58 * s);
		ctx.fillStyle = '#fff'; ctx.font = `700 ${40 * s}px ${DF}`; ctx.fillText(String(Math.round(o.v * 3.6)), W - 40 * s, H2 - 26 * s);
		ctx.fillStyle = '#aab1bc'; ctx.font = `600 ${13 * s}px Inter, system-ui, sans-serif`; ctx.fillText('km/h', W - 18 * s, H2 - 26 * s);
		ctx.textAlign = 'left';
		/* edenemine ja kontrollpunktid */
		const x0 = 180 * s, w = W - 300 * s, p = Math.max(0, Math.min(1, (o.z - ALGUS_Z) / PIKKUS));
		ctx.fillStyle = 'rgba(255,255,255,0.22)'; ctx.fillRect(x0, 20 * s, w, 6 * s);
		ctx.fillStyle = '#ffc20e'; ctx.fillRect(x0, 20 * s, w * p, 6 * s);
		for (let k = 1; k <= 4; k++) { ctx.fillStyle = k <= kp ? '#ffc20e' : 'rgba(255,255,255,0.5)'; ctx.fillRect(x0 + (w * k * KP_VAHE) / PIKKUS - 1, 15 * s, 3 * s, 16 * s); }
		if (vaheajad.length) { ctx.fillStyle = '#fff'; ctx.font = `600 ${14 * s}px Inter, system-ui, sans-serif`; ctx.fillText(`KP${vaheajad.length} ${aegTekst(vaheajad[vaheajad.length - 1])}`, x0, 48 * s); }
		/* kaardilugeja märge */
		const nt = olek === 'soit' ? noot() : null;
		if (nt) {
			const cx = W / 2, cy = 92 * s;
			ctx.fillStyle = nt.aste <= 2 ? 'rgba(200,30,30,0.85)' : 'rgba(10,11,13,0.7)';
			ctx.beginPath(); ctx.roundRect(cx - 95 * s, cy - 36 * s, 190 * s, 62 * s, 12 * s); ctx.fill();
			ctx.strokeStyle = '#fff'; ctx.lineWidth = 6 * s; ctx.lineCap = 'round';
			const ax = cx - 60 * s, dir = nt.suund;
			ctx.beginPath(); ctx.moveTo(ax - dir * 12 * s, cy + 16 * s); ctx.lineTo(ax - dir * 12 * s, cy - 6 * s); ctx.quadraticCurveTo(ax - dir * 12 * s, cy - 18 * s, ax + dir * 10 * s, cy - 18 * s); ctx.stroke();
			ctx.beginPath(); ctx.moveTo(ax + dir * 4 * s, cy - 27 * s); ctx.lineTo(ax + dir * 14 * s, cy - 18 * s); ctx.lineTo(ax + dir * 4 * s, cy - 9 * s); ctx.stroke();
			ctx.fillStyle = '#fff'; ctx.font = `700 ${40 * s}px ${DF}`; ctx.fillText(String(nt.aste), cx - 22 * s, cy + 12 * s);
			ctx.font = `700 ${22 * s}px ${DF}`; ctx.fillText((dir > 0 ? 'PAREM' : 'VASAK'), cx + 6 * s, cy - 6 * s);
			ctx.fillStyle = '#ffc20e'; ctx.fillText(nt.d + ' m', cx + 6 * s, cy + 18 * s);
		}
		/* stardi loendus */
		if (olek === 'soit' && loendus > 0) {
			ctx.textAlign = 'center'; ctx.fillStyle = '#fff'; ctx.font = `700 ${120 * s}px ${DF}`;
			ctx.fillText(loendus > 0.5 ? String(Math.ceil(loendus - 0.5)) : 'START', W / 2, H2 * 0.48); ctx.textAlign = 'left';
		}
		ctx.restore();
	}

	/* ---------- juhtimine ---------- */
	const KLAHV = { ArrowUp: 'gaas', KeyW: 'gaas', ArrowDown: 'pidur', KeyS: 'pidur', Space: 'kasi', ArrowLeft: 'vasak', KeyA: 'vasak', ArrowRight: 'parem', KeyD: 'parem' };
	function klahv(e, alla) {
		const k = KLAHV[e.code];
		if (!k || (!ekraan?.contains(document.activeElement) && olek !== 'soit')) return;
		e.preventDefault();
		sis[k] = alla;
		if (alla && k === 'gaas' && (olek === 'algus' || olek === 'finis')) alusta();
	}
	function nupp(k, alla) { return (e) => { e.preventDefault(); sis[k] = alla; if (alla && k === 'gaas' && olek === 'algus') alusta(); }; }
	function taisEkraan() {
		taisekraan = !taisekraan;
		try { document.documentElement.style.overflow = taisekraan ? 'hidden' : ''; } catch {}
		setTimeout(suurus, 60);
	}
	function track(e, v) { try { window.PM_TRACK && window.PM_TRACK('etapp', e + (v ? ' · ' + v : '')); } catch {} }
	const parim = $derived((mang[nr] || {}).parim || null);
	const seeria = $derived.by(() => { let n = 0; while (mang[nr - n] && mang[nr - n].parim) n++; return n; });
</script>

<svelte:window onkeydown={(e) => klahv(e, true)} onkeyup={(e) => klahv(e, false)} />

<div class="et">
	<div class="et-info">
		<div>
			<p class="et-nr">Etapp nr {nr} · {new Date().toLocaleDateString('et-EE', { day: 'numeric', month: 'long' })}</p>
			<p class="et-olud">Kuiv kruus · 1,85 km · {E.kurvid.length} kurvi · uus rada iga päev</p>
		</div>
		<div class="et-paremal">
			{#if parim}<p class="et-parim">Sinu tänane parim <b>{aegTekst(parim)}</b></p>{/if}
			{#if seeria > 1}<p class="et-seeria">🔥 {seeria} päeva järjest</p>{/if}
		</div>
	</div>

	<div class="et-ekraan" class:tais={taisekraan} bind:this={ekraan}>
		<div class="et-ala" tabindex="0" role="application" aria-label="Päeva etapp: nooleklahvid juhivad">
			<canvas bind:this={cv} class="et-cv" aria-hidden="true"></canvas>
			{#if olek === 'algus' || olek === 'laeb'}
				<div class="et-kiht">
					<b>Päeva etapp</b>
					<span>Kruusaralli aja peale. Kaardilugeja näitab ees tulevat kurvi: 1 on kõige järsem, 6 peaaegu sirge. Teelt välja minnes alustad eelmisest kontrollpunktist.</span>
					<button type="button" class="btn yel" disabled={olek === 'laeb'} onclick={alusta}>{olek === 'laeb' ? 'Laen…' : 'Stardi'}</button>
					<small>Nooleklahvid: ↑ gaas, ↓ pidur, ← → rool, tühik käsipidur. Telefonis nupud ekraanil.</small>
				</div>
			{/if}
			{#if olek === 'avarii' && teade}
				<div class="et-teade" role="status"><b>Teelt välja</b><span>{teade}</span></div>
			{/if}
			{#if olek === 'finis' && tulemus}
				<div class="et-kiht et-tul" role="dialog" aria-label="Tulemus">
					<p class="et-k-pea">Finiš · etapp nr {nr}</p>
					<p class="et-k-aeg">{aegTekst(tulemus.aeg)}</p>
					<p class="et-k-s">{tulemus.uus ? 'Sinu tänane parim!' : 'Tänane parim ' + aegTekst(tulemus.parim)} · tipp {tulemus.tipp} km/h · teelt välja {tulemus.avariid} korda</p>
					<p class="et-k-tead"><b>Kas teadsid?</b> Etapi järseima kurvi (raadius {tulemus.R} m) saab kruusal läbida umbes {tulemus.kruus} km/h, kuival asfaldil {tulemus.asfalt} km/h. Kruusal on haaret ligi kolmandiku võrra vähem.</p>
					<div class="et-nupud">
						<button type="button" class="btn yel" onclick={alusta}>Sõida uuesti</button>
					</div>
					<small>Homme on uus rada.</small>
				</div>
			{/if}
			<div class="et-juht" aria-hidden="true">
				<div class="et-pool">
					<button type="button" tabindex="-1" onpointerdown={nupp('vasak', true)} onpointerup={nupp('vasak', false)} onpointerleave={nupp('vasak', false)} onpointercancel={nupp('vasak', false)}>◀</button>
					<button type="button" tabindex="-1" onpointerdown={nupp('parem', true)} onpointerup={nupp('parem', false)} onpointerleave={nupp('parem', false)} onpointercancel={nupp('parem', false)}>▶</button>
				</div>
				<div class="et-pool">
					<button type="button" tabindex="-1" class="kasi" onpointerdown={nupp('kasi', true)} onpointerup={nupp('kasi', false)} onpointerleave={nupp('kasi', false)} onpointercancel={nupp('kasi', false)}>Käsi&shy;pidur</button>
					<button type="button" tabindex="-1" class="pidur" onpointerdown={nupp('pidur', true)} onpointerup={nupp('pidur', false)} onpointerleave={nupp('pidur', false)} onpointercancel={nupp('pidur', false)}>Pidur</button>
					<button type="button" tabindex="-1" class="gaas" onpointerdown={nupp('gaas', true)} onpointerup={nupp('gaas', false)} onpointerleave={nupp('gaas', false)} onpointercancel={nupp('gaas', false)}>Gaas</button>
				</div>
			</div>
		</div>
		<button type="button" class="et-fs" onclick={taisEkraan} aria-label={taisekraan ? 'Välju täisekraanist' : 'Täisekraan'}>
			<svg viewBox="0 0 24 24" aria-hidden="true">{#if taisekraan}<path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" />{:else}<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />{/if}</svg>
		</button>
	</div>
</div>

<style>
	.et { max-width: 960px; margin: 0 auto; padding: var(--sp-6) 0 var(--sp-10); }
	.et-info { display: flex; justify-content: space-between; align-items: flex-end; gap: var(--sp-3); flex-wrap: wrap; margin-bottom: var(--sp-3); }
	.et-nr { margin: 0; font-family: var(--display); font-size: 26px; font-weight: 700; text-transform: uppercase; }
	.et-olud { margin: 2px 0 0; color: var(--muted); font-size: 15px; }
	.et-paremal { text-align: right; }
	.et-parim, .et-seeria { margin: 0; font-size: 14.5px; }
	.et-parim b { font-family: var(--display); font-size: 20px; }
	.et-ekraan { position: relative; }
	.et-ala { position: relative; border-radius: var(--r-lg, 16px); overflow: hidden; background: #0a0b0d; outline: none; user-select: none; -webkit-user-select: none; touch-action: none; }
	.et-ala:focus-visible { box-shadow: 0 0 0 3px var(--yellow); }
	.et-cv { width: 100%; aspect-ratio: 1 / 0.6; display: block; }
	.et-kiht { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--sp-3); padding: var(--sp-5); text-align: center; color: #fff; background: linear-gradient(rgba(5, 6, 8, 0.35), rgba(5, 6, 8, 0.75)); }
	.et-kiht b { font-family: var(--display); font-size: 56px; text-transform: uppercase; line-height: 0.95; letter-spacing: 0.01em; }
	.et-kiht span { max-width: 30em; color: #e3e6ea; font-size: 15.5px; line-height: 1.45; }
	.et-kiht small { color: #aab1bc; font-size: 13px; }
	.et-teade { position: absolute; left: 50%; top: 30%; transform: translateX(-50%); width: min(92%, 520px); background: rgba(16, 18, 22, 0.9); border-left: 4px solid #ff5a5a; color: #fff; border-radius: 12px; padding: 12px 16px; display: grid; gap: 4px; font-size: 15px; line-height: 1.45; }
	.et-teade b { color: #ff5a5a; font-family: var(--display); font-size: 24px; text-transform: uppercase; }
	.et-tul { overflow: auto; }
	.et-k-pea { margin: 0; color: #ffc20e; font-weight: 700; font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase; }
	.et-k-aeg { margin: 0; font-family: var(--display); font-size: 80px; font-weight: 700; color: #ffc20e; line-height: 1; }
	.et-k-s { margin: 0; color: #e3e6ea; font-size: 15px; }
	.et-k-tead { margin: 0; max-width: 32em; color: #cfd4db; font-size: 14px; line-height: 1.45; background: rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 10px 14px; }
	.et-k-tead b { color: #fff; }
	.et-nupud { display: flex; gap: var(--sp-2); }
	.et-juht { position: absolute; left: 0; right: 0; bottom: 0; display: flex; justify-content: space-between; padding: 10px; pointer-events: none; }
	.et-pool { display: flex; gap: 10px; }
	.et-juht button { pointer-events: auto; width: 64px; height: 64px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.25); background: rgba(10, 11, 13, 0.45); color: #fff; font-size: 22px; font-weight: 800; cursor: pointer; touch-action: none; }
	.et-juht button.gaas { background: rgba(22, 101, 52, 0.6); font-size: 15px; }
	.et-juht button.pidur { background: rgba(153, 27, 27, 0.6); font-size: 15px; }
	.et-juht button.kasi { background: rgba(120, 80, 10, 0.6); font-size: 12px; line-height: 1.1; }
	@media (hover: hover) and (pointer: fine) { .et-juht { display: none; } }
	.et-fs { position: absolute; top: 10px; right: 10px; width: 40px; height: 40px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.18); background: rgba(10, 11, 13, 0.55); color: #fff; display: grid; place-items: center; cursor: pointer; padding: 0; z-index: 2; }
	.et-fs svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
	.et-ekraan.tais { position: fixed; inset: 0; z-index: 1000; background: #0a0b0d; display: flex; }
	.et-ekraan.tais .et-ala { flex: 1; border-radius: 0; display: flex; }
	.et-ekraan.tais .et-cv { aspect-ratio: auto; height: 100%; }
</style>
