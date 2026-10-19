<script>
	/* PÄEVA ETAPP: võidusõit aja peale ($lib/etapp.js füüsika ja rada, $lib/tee3d.js pilt).
	   Rada on päeva järgi kõigile sama. Takistused tulevad juhuslikul hetkel.
	   Avarii või teelt välja: tagasi eelmisesse kontrollpunkti, kell käib edasi,
	   ja ekraanil on lühike selgitus numbritega (sama mootor mis kalkulaatoris). */
	import { onMount, onDestroy } from 'svelte';
	import { version } from '$app/environment';
	import { joonista, TEE } from '$lib/tee3d.js';
	import { looEtapp, paevaNr, REHVID, rehv, haardeTabel, piirkiirus, ohutuKiirus, koverus, samm, uusAuto, ALGUS_Z, PIKKUS, KP_VAHE } from '$lib/etapp.js';

	const nr = paevaNr();
	const E = looEtapp(nr);
	const kuu = new Date().getMonth() + 1;
	let kat = $state(kuu >= 11 || kuu <= 3 || E.olud.cond.tempC < 3 ? 'WINTER_NORDIC' : 'SUMMER_TOURING');
	let olek = $state('laeb'); /* laeb | algus | soit | avarii | finis */
	let teade = $state(null); /* avarii selgitus */
	let tulemus = $state(null);
	let kell = $state(0), kpNahtav = $state(0), libiseb = $state(false);
	let taisekraan = $state(false);
	let mang = $state({}); /* localStorage: parimad ajad */

	let P = null, veh = null, gClass = null, H = null, Hjaa = null, Hlomp = null;
	let cv, ctx, W = 800, H2 = 500, raf = 0, eelm = 0, aeg0 = 0, ekraan;
	const o = uusAuto(ALGUS_Z - 14, TEE.KAAM_X);
	const sis = { gaas: false, pidur: false, kasi: false, vasak: false, parem: false };
	let risti = 0, kp = 0, loomad = [], laigud = [], jargmine = 8, sohiAeg = 0, avariid = 0, opp = [], tipp = 0, ajalugu = [];

	const f1 = (x) => x.toLocaleString('et-EE', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
	const aegTekst = (s) => Math.floor(s / 60) + ':' + (s % 60).toFixed(1).padStart(4, '0').replace('.', ',');
	const rehviNimi = (k) => REHVID.find((x) => x[0] === k)[1];
	const rehviga = (n) => n.toLowerCase() + 'iga'; /* suverehviga, lamellrehviga, naastrehviga */

	onMount(async () => {
		try { mang = JSON.parse(localStorage.getItem('pm_etapp') || '{}') || {}; } catch {}
		ctx = cv.getContext('2d');
		suurus();
		window.addEventListener('resize', suurus);
		await import('$lib/engine.js');
		P = globalThis.Pidurdus;
		const d = await (await fetch('/data/vaikeauto.json?v=' + encodeURIComponent(version))).json();
		veh = d.vehicles[0]; gClass = d.gClass;
		arvuta();
		olek = 'algus';
		raf = requestAnimationFrame(kaader);
	});
	onDestroy(() => {
		if (typeof window === 'undefined') return;
		cancelAnimationFrame(raf); window.removeEventListener('resize', suurus);
		try { document.documentElement.style.overflow = ''; } catch {}
	});
	function arvuta() {
		const ty = rehv(kat, veh, gClass), c = E.olud.cond;
		H = haardeTabel(P, ty, veh, c);
		Hjaa = haardeTabel(P, ty, veh, { surface: 'ICE', waterMm: 0, tempC: Math.min(0, c.tempC) });
		Hlomp = haardeTabel(P, ty, veh, { surface: 'ASPHALT', waterMm: 8, tempC: c.tempC });
	}
	function suurus() {
		if (!cv) return;
		const dpr = Math.min(2, window.devicePixelRatio || 1), w = cv.clientWidth || 800;
		const h = taisekraan ? cv.clientHeight || w * 0.62 : w * 0.62;
		W = Math.round(w * dpr); H2 = Math.round(h * dpr);
		cv.width = W; cv.height = H2;
	}

	/* ---------- mänguvoog ---------- */
	function alusta() {
		if (!P) return;
		arvuta();
		Object.assign(o, uusAuto(ALGUS_Z - 14, TEE.KAAM_X));
		kp = 0; kpNahtav = 0; kell = 0; loomad = []; laigud = []; avariid = 0; opp = []; tipp = 0; ajalugu = [];
		jargmine = 6 + Math.random() * 8; sohiAeg = 0;
		teade = null; tulemus = null; olek = 'soit';
		/* telefonis on kitsas pilt liiga väike: mäng läheb kohe üle kogu ekraani */
		try { if (!taisekraan && matchMedia('(pointer: coarse)').matches) taisEkraan(); } catch {}
		track('algus', E.olud.id + ' · ' + kat);
		setTimeout(() => ekraan?.querySelector('.et-ala')?.focus(), 30);
	}
	function avarii(liik, lisa = {}) {
		avariid++;
		const v = Math.max(o.v, ...ajalugu.map((x) => x[1])) * 3.6;
		let tekst = '';
		if (liik === 'loom') {
			const d = lisa.d, vs = lisa.v * 3.6, vaja = lisa.v + H.pidurdusmaa(vs), ohutu = ohutuKiirus(H, d);
			tekst = `${lisa.t === 'poder' ? 'Põder' : 'Metssiga'} tuli teele ${Math.round(d)} m ees. ${Math.round(vs)} km/h pealt on peatumisteekond 1 s reaktsiooniga umbes ${Math.round(vaja)} m. Selle nähtavusega jõuad peatuda kuni ${Math.round(ohutu)} km/h.`;
		} else {
			const laik = laigud.find((l) => o.z >= l.z0 - 5 && o.z <= l.z1 + 25);
			const n = Math.floor(o.z / TEE.SEG);
			const kurv = E.kurvid.find((k) => n >= k.n0 - 2 && n <= k.n1 + 8);
			if (laik && laik.t === 'jaa') {
				const pr = Math.round((1 - Hjaa.a(15) / H.a(15)) * 100);
				tekst = `Jäälaik: jääl on haaret umbes ${pr}% vähem kui ülejäänud teel. Pidurda ja pööra enne laiku, laigu peal hoia rool otse.`;
			} else if (laik) {
				tekst = `Sügav lomp: ${Math.round(v)} km/h juures hakkab rehv vee peal ujuma (vesiliug) ja rool ei pööra. Aeglusta enne lompi.`;
			} else if (kurv) {
				const lim = piirkiirus(H, kurv.R);
				const teised = REHVID.filter((r) => r[0] !== kat).map((r) => `${rehviga(r[1])} ${Math.round(piirkiirus(haardeTabel(P, rehv(r[0], veh, gClass), veh, E.olud.cond), kurv.R))}`).join(', ');
				tekst = `Kurv raadiusega ${kurv.R} m: selle tee ja ${rehviga(rehviNimi(kat))} oli piirkiirus ${Math.round(lim)} km/h, sina sõitsid ${Math.round(v)} km/h. Sama kurvi piirkiirus ${teised} km/h.`;
			} else tekst = `Sõitsid teelt välja ${Math.round(v)} km/h pealt. Järsk rooli keeramine suurel kiirusel viib auto libisema.`;
		}
		opp.push(tekst);
		teade = tekst;
		track('avarii', liik + ' · ' + Math.round(v) + ' km/h');
		olek = 'avarii';
		sohiAeg = 0;
	}
	function taasta() {
		Object.assign(o, uusAuto(ALGUS_Z + kp * KP_VAHE + 2, TEE.KAAM_X));
		loomad = []; laigud = []; ajalugu = [];
		jargmine = 5 + Math.random() * 8; sohiAeg = 0;
		teade = null; olek = 'soit';
	}
	function finis() {
		olek = 'finis';
		const p = mang[nr] || { parim: {}, katseid: 0 };
		p.katseid = (p.katseid || 0) + 1;
		const uus = !p.parim[kat] || kell < p.parim[kat];
		if (uus) p.parim[kat] = Math.round(kell * 10) / 10;
		mang = { ...mang, [nr]: p };
		try { localStorage.setItem('pm_etapp', JSON.stringify(mang)); } catch {}
		/* etapi järseim kurv kõigi rehvidega: see on mängu õppetund numbrites */
		const R = Math.min(...E.kurvid.map((k) => k.R));
		const kurviTabel = REHVID.map((r) => [r[1], Math.round(piirkiirus(haardeTabel(P, rehv(r[0], veh, gClass), veh, E.olud.cond), R))]);
		tulemus = { aeg: kell, uus, avariid, opp: [...new Set(opp)], R, kurviTabel, tipp: Math.round(tipp * 3.6), kesk: Math.round((PIKKUS / kell) * 3.6) };
		track('finis', aegTekst(kell) + ' · ' + kat + ' · avariid ' + avariid);
	}

	/* ---------- takistused juhuslikul hetkel ---------- */
	function uusTakistus() {
		const tyyp = E.olud.takistused[Math.floor(Math.random() * E.olud.takistused.length)];
		if (tyyp === 'poder' || tyyp === 'siga') {
			/* nähtavus: päeval 55–110 m (tuleb metsast), öösel lähitulede ulatus ~45–60 m */
			const d = E.oo ? 45 + Math.random() * 15 : 55 + Math.random() * 55;
			const pool = Math.random() < 0.5 ? -1 : 1;
			loomad.push({ t: tyyp, z: o.z + d, x: pool * (TEE.TEE_L + 2.5), siht: -pool * (0.5 + Math.random() * 2.2), suund: -pool, kiir: tyyp === 'poder' ? 1.6 : 3.2, kond: 0, d, v: o.v, seisab: 0 });
		} else {
			const d = 40 + Math.random() * 50, pikk = 22 + Math.random() * 25;
			laigud.push({ t: tyyp, z0: o.z + d, z1: o.z + d + pikk });
		}
	}

	/* ---------- kaader ---------- */
	function kaader(now) {
		raf = requestAnimationFrame(kaader);
		if (!ctx) return;
		const dt = eelm ? Math.min(0.05, (now - eelm) / 1000) : 0.016;
		eelm = now;
		if (!aeg0) aeg0 = now;
		if (olek === 'soit' && H) fyysika(dt);
		else if (olek === 'avarii') { sohiAeg += dt; kell += dt; o.vx = o.v = Math.max(0, o.v - 12 * dt); o.vy = 0; o.r = 0; o.z += o.v * dt; if (sohiAeg > 3.2) taasta(); }
		else if (olek === 'finis') { o.vx = o.v = Math.max(0, o.v - 6 * dt); o.vy = 0; o.r = 0; o.z += o.v * Math.cos(o.psi) * dt; }
		else if (olek === 'algus') { o.psi = 0; }
		joonista(ctx, W, H2, E.tee, {
			z: o.z, kmh: o.v * 3.6, oo: E.oo, ilm: E.olud.ilm, kate: E.olud.kate, px: o.x, psi: o.psi,
			loomad, laigud, crash: olek === 'avarii', aeg: (now - aeg0) / 1000
		});
		hud();
	}
	function fyysika(dt) {
		const tSisend = { gaas: sis.gaas, pidur: sis.pidur, kasi: sis.kasi, roolSiht: (sis.parem ? 1 : 0) - (sis.vasak ? 1 : 0) };
		const laik = laigud.find((l) => o.z >= l.z0 && o.z <= l.z1);
		const aKate = laik ? (laik.t === 'jaa' ? Hjaa.a : Hlomp.a) : H.a;
		const maas = Math.abs(o.x) > TEE.TEE_L + 0.3;
		const n = 8;
		let syndmus = null;
		for (let i = 0; i < n && !syndmus; i++) {
			const r = samm(o, tSisend, dt / n, koverus(E.tee, o.z), aKate, maas);
			if (r === 'teelt') syndmus = 'teelt';
		}
		libiseb = o.libiseb;
		if (o.z >= ALGUS_Z) kell += dt;
		tipp = Math.max(tipp, o.v);
		ajalugu.push([kell, o.v]); if (ajalugu.length > 90) ajalugu.shift();
		while (kp < 4 && o.z >= ALGUS_Z + (kp + 1) * KP_VAHE) { kp++; kpNahtav = kp; }
		/* keeras ringi ja jäi risti seisma: tagasi kontrollpunkti */
		risti = o.v < 1 && Math.abs(o.psi) > 0.9 ? risti + dt : 0;
		if (syndmus || risti > 1.5) { risti = 0; avarii('teelt'); return; }
		/* loomad liiguvad üle tee; kokkupõrge, kui auto esiots jõuab looma kohale */
		for (const l of loomad) {
			if (l.seisab > 0) l.seisab -= dt;
			else {
				const suund = Math.sign(l.siht - l.x);
				if (Math.abs(l.siht - l.x) < 0.1) { l.seisab = 1.5 + Math.random() * 2; l.siht = -Math.sign(l.x || 1) * (TEE.TEE_L + 4); }
				else { l.x += suund * Math.min(Math.abs(l.siht - l.x), l.kiir * dt); l.kond += dt * 7; l.suund = suund || l.suund; }
			}
			const pool = l.t === 'poder' ? 1.3 : 0.7;
			if (o.z >= l.z - 0.4 && o.z <= l.z + 2 && Math.abs(o.x - l.x) < 0.9 + pool && o.v > 1) { avarii('loom', l); return; }
		}
		loomad = loomad.filter((l) => o.z < l.z + 30 && Math.abs(l.x) < TEE.TEE_L + 6);
		laigud = laigud.filter((l) => o.z < l.z1 + 40);
		/* uus takistus juhuslikul hetkel (ainult sõites, mitte stardis ega finiši lähedal) */
		if (o.v > 8 && o.z > ALGUS_Z + 40 && o.z < ALGUS_Z + PIKKUS - 140) {
			jargmine -= dt;
			if (jargmine <= 0 && !loomad.length) { uusTakistus(); jargmine = 7 + Math.random() * 12; }
		}
		if (o.z >= ALGUS_Z + PIKKUS) finis();
	}
	function hud() {
		const s = Math.max(W / 800, Math.min(2, window.devicePixelRatio || 1) * 0.85); /* telefonis loetav */
		ctx.save();
		ctx.fillStyle = 'rgba(10,11,13,0.62)';
		ctx.fillRect(10 * s, 10 * s, 168 * s, 52 * s);
		ctx.fillStyle = '#ffc20e'; ctx.font = `700 ${30 * s}px "Barlow Condensed", "Arial Narrow", sans-serif`;
		ctx.fillText(aegTekst(kell), 20 * s, 44 * s);
		ctx.fillStyle = '#cfd4db'; ctx.font = `600 ${13 * s}px Inter, system-ui, sans-serif`;
		ctx.fillText(`KP ${kpNahtav}/4`, 112 * s, 32 * s);
		ctx.fillText(avariid ? `✕ ${avariid}` : '', 112 * s, 50 * s);
		/* edenemine */
		const p = Math.max(0, Math.min(1, (o.z - ALGUS_Z) / PIKKUS));
		ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fillRect(190 * s, 18 * s, W - 290 * s, 6 * s);
		ctx.fillStyle = '#ffc20e'; ctx.fillRect(190 * s, 18 * s, (W - 290 * s) * p, 6 * s);
		for (let k = 1; k <= 4; k++) { ctx.fillStyle = k <= kpNahtav ? '#ffc20e' : 'rgba(255,255,255,0.45)'; ctx.fillRect(190 * s + ((W - 290 * s) * k * KP_VAHE) / PIKKUS - 1, 14 * s, 3 * s, 14 * s); }
		if (libiseb && olek === 'soit') {
			ctx.fillStyle = '#ff5a5a'; ctx.font = `700 ${26 * s}px "Barlow Condensed", "Arial Narrow", sans-serif`; ctx.textAlign = 'center';
			ctx.fillText('LIBISEB', W / 2, 70 * s); ctx.textAlign = 'left';
		}
		ctx.restore();
	}

	/* ---------- juhtimine ---------- */
	const KLAHV = { ArrowUp: 'gaas', KeyW: 'gaas', ArrowDown: 'pidur', KeyS: 'pidur', Space: 'kasi', ArrowLeft: 'vasak', KeyA: 'vasak', ArrowRight: 'parem', KeyD: 'parem' };
	function klahv(e, alla) {
		const k = KLAHV[e.code];
		if (!k || !ekraan?.contains(document.activeElement) && olek !== 'soit') return;
		e.preventDefault();
		sis[k] = alla;
		if (alla && (olek === 'algus' || olek === 'finis') && (k === 'gaas')) alusta();
	}
	function nupp(k, alla) { return (e) => { e.preventDefault(); sis[k] = alla; if (alla && k === 'gaas' && (olek === 'algus')) alusta(); }; }
	function taisEkraan() {
		taisekraan = !taisekraan;
		try { document.documentElement.style.overflow = taisekraan ? 'hidden' : ''; } catch {}
		setTimeout(suurus, 60);
	}
	function vahetaRehv(k) { if (olek === 'soit' || olek === 'avarii') return; kat = k; if (P) arvuta(); olek = 'algus'; tulemus = null; }
	function track(e, v) { try { window.PM_TRACK && window.PM_TRACK('etapp', e + (v ? ' · ' + v : '')); } catch {} }
	const parim = $derived((mang[nr] || {}).parim || {});
	const seeria = $derived.by(() => { let n = 0; while (mang[nr - n] && Object.keys(mang[nr - n].parim || {}).length) n++; return n; });
</script>

<svelte:window onkeydown={(e) => klahv(e, true)} onkeyup={(e) => klahv(e, false)} />

<div class="et">
	<div class="et-info">
		<div>
			<p class="et-nr">Etapp nr {nr} · {new Date().toLocaleDateString('et-EE', { day: 'numeric', month: 'long' })}</p>
			<p class="et-olud">{E.olud.nimi} · {E.oo ? 'öö' : 'päev'} · {f1(PIKKUS / 1000)} km · {E.kurvid.length} kurvi</p>
		</div>
		{#if seeria > 1}<p class="et-seeria">🔥 {seeria} päeva järjest</p>{/if}
	</div>
	<div class="et-rehvid" role="group" aria-label="Rehvid">
		{#each REHVID as [k, n] (k)}
			<button type="button" aria-pressed={kat === k} disabled={olek === 'soit' || olek === 'avarii'} onclick={() => vahetaRehv(k)}>
				{n}{#if parim[k]}<small>{aegTekst(parim[k])}</small>{/if}
			</button>
		{/each}
	</div>

	<div class="et-ekraan" class:tais={taisekraan} bind:this={ekraan}>
		<div class="et-ala" tabindex="0" role="application" aria-label="Päeva etapp: nooleklahvid juhivad">
			<canvas bind:this={cv} class="et-cv" aria-hidden="true"></canvas>
			{#if olek === 'algus' || olek === 'laeb'}
				<div class="et-kiht">
					<b>Päeva etapp</b>
					<span>Sõida finišisse nii kiiresti kui suudad. Teele võib igal hetkel tulla põder, jäälaik või lomp. Avarii korral alustad eelmisest kontrollpunktist ja kell käib edasi.</span>
					<button type="button" class="btn yel" disabled={olek === 'laeb'} onclick={alusta}>{olek === 'laeb' ? 'Laen…' : 'Start'}</button>
					<small>Arvutis nooleklahvid: ↑ gaas, ↓ pidur, ← → rool, tühik käsipidur. Telefonis nupud ekraanil.</small>
				</div>
			{/if}
			{#if olek === 'avarii' && teade}
				<div class="et-teade" role="status"><b>Avarii</b><span>{teade}</span></div>
			{/if}
			{#if olek === 'finis' && tulemus}
				<div class="et-kiht et-tul" role="dialog" aria-label="Tulemus">
					<p class="et-k-pea">Finiš · {rehviNimi(kat)}</p>
					<p class="et-k-aeg">{aegTekst(tulemus.aeg)}</p>
					<p class="et-k-s">{tulemus.uus ? 'Sinu tänane parim! ' : ''}Keskmine {tulemus.kesk} km/h, tipp {tulemus.tipp} km/h, avariisid {tulemus.avariid}.</p>
					<p class="et-k-s"><b>Etapi järseim kurv (R = {tulemus.R} m), piirkiirus täna:</b> {#each tulemus.kurviTabel as [n, v], i (n)}{i ? ', ' : ''}{n.toLowerCase()} {v} km/h{/each}.</p>
					{#if tulemus.opp.length}<ul class="et-opp">{#each tulemus.opp as x (x)}<li>{x}</li>{/each}</ul>{/if}
					<div class="et-nupud">
						<button type="button" class="btn yel" onclick={alusta}>Sõida uuesti</button>
						<button type="button" class="btn" onclick={() => { olek = 'algus'; tulemus = null; }}>Vaheta rehve</button>
					</div>
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
	.et { max-width: 900px; margin: 0 auto; padding: var(--sp-6) 0 var(--sp-10); }
	.et-info { display: flex; justify-content: space-between; align-items: flex-end; gap: var(--sp-3); flex-wrap: wrap; margin-bottom: var(--sp-3); }
	.et-nr { margin: 0; font-family: var(--display); font-size: 26px; font-weight: 700; text-transform: uppercase; }
	.et-olud { margin: 2px 0 0; color: var(--muted); font-size: 15px; }
	.et-seeria { margin: 0; font-weight: 700; }
	.et-rehvid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--sp-1); background: #fff; border: 1px solid var(--line); padding: var(--sp-1); border-radius: 12px; margin-bottom: var(--sp-3); }
	.et-rehvid button { border: 0; background: transparent; padding: 10px 6px; border-radius: 9px; font-weight: 700; font-size: 15px; color: var(--muted); cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 2px; }
	.et-rehvid button small { font-weight: 600; font-size: 12px; }
	.et-rehvid button[aria-pressed='true'] { background: var(--ink); color: #fff; box-shadow: inset 0 -3px 0 var(--yellow); }
	.et-rehvid button:disabled { cursor: default; opacity: 0.7; }
	.et-ekraan { position: relative; }
	.et-ala { position: relative; border-radius: var(--r-lg, 16px); overflow: hidden; background: #0a0b0d; outline: none; user-select: none; -webkit-user-select: none; touch-action: none; }
	.et-ala:focus-visible { box-shadow: 0 0 0 3px var(--yellow); }
	.et-cv { width: 100%; aspect-ratio: 1 / 0.62; display: block; }
	.et-kiht { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--sp-3); padding: var(--sp-5); text-align: center; color: #fff; background: rgba(5, 6, 8, 0.6); }
	.et-kiht b { font-family: var(--display); font-size: 40px; text-transform: uppercase; line-height: 1; }
	.et-kiht span { max-width: 32em; color: #dfe3ea; font-size: 15.5px; line-height: 1.45; }
	.et-kiht small { color: #aab1bc; font-size: 13px; }
	.et-teade { position: absolute; left: 50%; top: 22%; transform: translateX(-50%); width: min(92%, 560px); background: rgba(16, 18, 22, 0.92); border: 1px solid #3a2a2a; border-left: 4px solid #ff5a5a; color: #fff; border-radius: 12px; padding: 12px 16px; display: grid; gap: 4px; font-size: 15px; line-height: 1.45; }
	.et-teade b { color: #ff5a5a; font-family: var(--display); font-size: 22px; text-transform: uppercase; }
	.et-tul { overflow: auto; justify-content: flex-start; padding-top: var(--sp-6); }
	.et-k-pea { margin: 0; color: #ffc20e; font-weight: 700; font-size: 13px; letter-spacing: 0.06em; text-transform: uppercase; }
	.et-k-aeg { margin: 0; font-family: var(--display); font-size: 64px; font-weight: 700; color: #ffc20e; line-height: 1; }
	.et-k-s { margin: 0; color: #dfe3ea; font-size: 15px; max-width: 36em; line-height: 1.45; }
	.et-opp { text-align: left; margin: 0; padding-left: 1.2em; color: #cfd4db; font-size: 14px; line-height: 1.45; max-width: 36em; display: grid; gap: 4px; }
	.et-nupud { display: flex; gap: var(--sp-2); flex-wrap: wrap; justify-content: center; }
	.et-tul .btn:not(.yel) { background: #23262d; color: #fff; border-color: #343944; }
	.et-juht { position: absolute; left: 0; right: 0; bottom: 0; display: flex; justify-content: space-between; padding: 10px; pointer-events: none; }
	.et-pool { display: flex; gap: 10px; }
	.et-juht button { pointer-events: auto; width: 64px; height: 64px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.25); background: rgba(10, 11, 13, 0.45); color: #fff; font-size: 22px; font-weight: 800; cursor: pointer; touch-action: none; }
	.et-juht button.gaas { background: rgba(22, 101, 52, 0.6); font-size: 15px; }
	.et-juht button.pidur { background: rgba(153, 27, 27, 0.6); font-size: 15px; }
	.et-juht button.kasi { background: rgba(120, 80, 10, 0.6); font-size: 12px; line-height: 1.1; }
	@media (hover: hover) and (pointer: fine) { .et-juht { opacity: 0.55; } }
	.et-fs { position: absolute; top: 10px; right: 10px; width: 40px; height: 40px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.18); background: rgba(10, 11, 13, 0.55); color: #fff; display: grid; place-items: center; cursor: pointer; padding: 0; z-index: 2; }
	.et-fs svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
	.et-ekraan.tais { position: fixed; inset: 0; z-index: 1000; background: #0a0b0d; display: flex; }
	.et-ekraan.tais .et-ala { flex: 1; border-radius: 0; display: flex; }
	.et-ekraan.tais .et-cv { aspect-ratio: auto; height: 100%; }
</style>
