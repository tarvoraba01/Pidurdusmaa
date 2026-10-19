<script>
	/* PÄEVA ETAPP: kruusaralli 3D-s, aja peale. Iga päev uus rada, kõigile sama.
	   Rada ja sõidumudel: $lib/ralli.js (arkaadlik drift), pilt: $lib/ralli3d.js (three.js), heli: $lib/ralliHeli.js.
	   Pidurdus tuleb samast mootorist mis kalkulaatoris (kruus, ABS). Teelt välja või puusse:
	   tagasi eelmisesse kontrollpunkti, kell käib edasi. Õpetlik osa on kõrval (avarii teade, finiši „kas teadsid“). */
	import { onMount, onDestroy } from 'svelte';
	import { version } from '$app/environment';
	import { looRada, paevaNr, uusAuto, samm, noot, piirkiirus, peatumine, rehv, haardeTabel, ALGUS, PIKKUS, KP_VAHE, POOL, DS } from '$lib/ralli.js';

	const nr = paevaNr();
	const rada = looRada(nr);
	const KAT = 'SUMMER_TOURING';
	let olek = $state('laeb'); /* laeb | algus | soit | avarii | finis */
	let viga = $state('');
	let teade = $state(null);
	let tulemus = $state(null);
	let taisekraan = $state(false);
	let mang = $state({});
	let vaikne = $state(false);
	let h = $state({ kell: 0, kmh: 0, kaik: 1, noot: null, kp: 0, vahe: '', loendus: 0, vale: false, abi: false, mx: 0, my: 0 });

	let cv, ala, ekraan, maailm = null, heli = null, H = null, Hasf = null, raf = 0, eelm = 0;
	let o = uusAuto(rada, ALGUS - 8);
	const sis = { gaas: false, pidur: false, kasi: false, vasak: false, parem: false };
	let kell = 0, kp = 0, sohiAeg = 0, avariid = 0, tipp = 0, loendus = 0, seisab = 0, vaheajad = [], ajalugu = [];
	/* põdrad: märgiga kohtades (rada.podrad); igal sõidul juhuslikult 1 kuni 2 kohta, põder seisab metsaservas
	   ja hakkab üle tee kõndima, kui auto läheneb (Tarvo 19.10: ei tohi tulla tühjast õhust) */
	let podrad = [];
	function seaPodrad(alates = -1) {
		const vanad = podrad;
		podrad = rada.podrad.map((p, j) => {
			if (p.s < alates && vanad[j]) return vanad[j];
			const aktiivne = Math.random() < 0.55;
			const pool = Math.random() < 0.5 ? -1 : 1;
			return { s: p.s + (Math.random() - 0.5) * 30, d: pool * (POOL + 12), suund: -pool, olek: aktiivne ? 'oota' : 'ei', faas: 0, paus: 0, kaib: false };
		});
		if (alates < 0 && !podrad.some((p) => p.olek === 'oota') && podrad.length) podrad[Math.floor(Math.random() * podrad.length)].olek = 'oota';
	}
	function podradSamm(dt) {
		let k = 0, tabas = false;
		for (const p of podrad) {
			if (p.olek === 'ei' || p.olek === 'lainud') continue;
			const kaugus = p.s - o.s;
			if (p.olek === 'oota' && kaugus < Math.max(85, o.v * 4.3) && kaugus > 10) p.olek = 'kaib';
			if (p.olek === 'kaib') {
				p.kaib = true; p.faas += dt;
				if (Math.abs(p.d) < 1 && p.paus < 1.1) { p.paus += dt; p.kaib = false; } /* jääb hetkeks tee keskele seisma */
				else p.d += p.suund * 3.0 * dt;
				if (p.d * p.suund > POOL + 12) p.olek = 'lainud';
			}
			if (k < 3 && kaugus > -30 && kaugus < 260) {
				const w = maailm.poder(k++, p);
				if (w && Math.hypot(w.x - o.x, w.z - o.z) < 2.1) tabas = true;
			}
		}
		for (; k < 3; k++) maailm.poder(k, null);
		return tabas;
	}

	const aegTekst = (s) => Math.floor(s / 60) + ':' + (s % 60).toFixed(1).padStart(4, '0').replace('.', ',');

	/* minikaart */
	const kaart = (() => {
		let a = Infinity, b = -Infinity, c = Infinity, d = -Infinity;
		for (let i = 0; i < rada.n; i++) { a = Math.min(a, rada.x[i]); b = Math.max(b, rada.x[i]); c = Math.min(c, rada.z[i]); d = Math.max(d, rada.z[i]); }
		const k = 100 / Math.max(b - a, d - c), ox = (110 - (b - a) * k) / 2, oz = (110 - (d - c) * k) / 2;
		const P = (x, z) => [ox + (b - x) * k, oz + (d - z) * k];
		const lopp = Math.round((ALGUS + PIKKUS) / DS);
		let tee = '';
		for (let i = Math.round(ALGUS / DS); i <= lopp; i += 4) { const [x, y] = P(rada.x[i], rada.z[i]); tee += (tee ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); }
		const kpd = [];
		for (let j = 1; j * KP_VAHE < PIKKUS; j++) { const i = Math.round((ALGUS + j * KP_VAHE) / DS); kpd.push(P(rada.x[i], rada.z[i])); }
		const fin = P(rada.x[lopp], rada.z[lopp]);
		return { tee, P, kpd, fin };
	})();

	onMount(async () => {
		try { mang = JSON.parse(localStorage.getItem('pm_etapp') || '{}') || {}; } catch {}
		try { vaikne = localStorage.getItem('pm_etapp_vaikne') === '1'; } catch {}
		try {
			const madal = matchMedia('(pointer: coarse)').matches || window.innerWidth < 700;
			const [{ looMaailm }] = await Promise.all([import('$lib/ralli3d.js'), import('$lib/engine.js')]);
			const P = globalThis.Pidurdus;
			const d = await (await fetch('/data/vaikeauto.json?v=' + encodeURIComponent(version))).json();
			const veh = d.vehicles[0];
			H = haardeTabel(P, rehv(KAT, veh, d.gClass), veh, { surface: 'GRAVEL', waterMm: 0, tempC: 10 });
			Hasf = haardeTabel(P, rehv(KAT, veh, d.gClass), veh, { surface: 'ASPHALT', waterMm: 0, tempC: 14 });
			maailm = looMaailm(cv, rada, { madal });
			suurus();
			window.addEventListener('resize', suurus);
			olek = 'algus';
			raf = requestAnimationFrame(kaader);
			/* arenduses: kaader-kaadrilt juhtimine testide ja video jaoks */
			if (import.meta.env.DEV) window.__etapp = { peata: () => { peatus = true; cancelAnimationFrame(raf); }, tikk: (dt, s, pilt = true) => { Object.assign(sis, s || {}); tikk(dt, pilt); }, start: () => alusta(), podrad: () => podrad, auto: () => o, maailm: () => maailm, rada, olek: () => olek };
		} catch (e) {
			viga = 'Mängu ei õnnestunud käivitada. Proovi teise brauseriga (vaja on WebGL-i).';
			olek = 'algus';
		}
	});
	onDestroy(() => {
		if (typeof window === 'undefined') return;
		cancelAnimationFrame(raf); window.removeEventListener('resize', suurus);
		try { document.documentElement.style.overflow = ''; } catch {}
		maailm?.havita(); heli?.sulge();
	});
	function suurus() {
		if (!cv || !maailm) return;
		const w = cv.clientWidth || 800, hh = cv.clientHeight || w * 0.5625;
		maailm.suurus(w, hh);
	}

	/* ---------- mänguvoog ---------- */
	function alusta() {
		if (!H || !maailm) return;
		o = uusAuto(rada, ALGUS - 8);
		seaPodrad();
		kp = 0; kell = 0; avariid = 0; tipp = 0; vaheajad = []; ajalugu = []; seisab = 0;
		teade = null; tulemus = null; olek = 'soit'; loendus = 3;
		maailm.kaamUus();
		heli?.jatka(); heli?.vaikne(vaikne);
		try { if (!taisekraan && matchMedia('(pointer: coarse)').matches) taisEkraan(); } catch {}
		track('algus');
		setTimeout(() => ala?.focus(), 30);
	}
	async function laeHeli() {
		if (heli) return;
		try { const { looHeli } = await import('$lib/ralliHeli.js'); heli = looHeli(); heli?.jatka(); heli?.vaikne(vaikne); } catch {}
	}
	function avarii(miks) {
		avariid++;
		const v = Math.max(o.v, ...ajalugu) * 3.6;
		const n = o.s / 5;
		const kurv = rada.kurvid.find((k) => n >= k.n0 - 3 && n <= k.n1 + 6);
		const kurvis = kurv ? ` Sina tulid ${Math.round(v)} km/h. Tavalise autoga on selle kurvi piirkiirus kruusal umbes ${Math.round(piirkiirus(H.a, kurv.R))} km/h.` : '';
		teade = miks === 'poder'
			? `Põder! Sina tulid ${Math.round(v)} km/h. Sellelt kiiruselt peatub auto kruusal umbes ${Math.round(peatumine(H.a, v / 3.6))} meetriga (1 s reaktsioon + pidurdus). Põdramärgi juures võta hoog maha.`
			: (miks === 'puu' ? 'Puusse.' : 'Teelt välja.') + kurvis;
		track('avarii', Math.round(v) + ' km/h');
		olek = 'avarii';
		sohiAeg = 0;
	}
	function taasta() {
		o = uusAuto(rada, kp ? ALGUS + kp * KP_VAHE + 4 : ALGUS - 8);
		seaPodrad(o.s);
		maailm.kaamUus();
		ajalugu = []; seisab = 0;
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
		const k = rada.kurvid.reduce((a, b) => (b.R < a.R ? b : a));
		tulemus = { aeg: kell, uus, parim: p.parim, avariid, tipp: Math.round(tipp * 3.6), R: k.R, kruus: Math.round(piirkiirus(H.a, k.R)), asfalt: Math.round(piirkiirus(Hasf.a, k.R)) };
		track('finis', aegTekst(kell) + ' · avariid ' + avariid);
	}

	/* ---------- kaader ---------- */
	let peatus = false, mangAeg = 0;
	function kaader(now) {
		if (peatus) return;
		raf = requestAnimationFrame(kaader);
		const dt = eelm ? Math.min(0.05, (now - eelm) / 1000) : 0.016;
		eelm = now;
		tikk(dt);
	}
	function tikk(dt, pilt = true) {
		mangAeg += dt;
		const tyhi = { gaas: false, pidur: false, kasi: false, rool: 0 };
		if (olek === 'soit') {
			if (loendus > 0) { loendus = Math.max(0, loendus - dt); fyysika(dt, tyhi, true); }
			else fyysika(dt, { gaas: sis.gaas, pidur: sis.pidur, kasi: sis.kasi, rool: (sis.parem ? 1 : 0) - (sis.vasak ? 1 : 0) });
		} else if (olek === 'avarii') {
			sohiAeg += dt; kell += dt;
			fyysika(dt, { ...tyhi, pidur: true, kasi: true }, true);
			if (sohiAeg > 2.2) taasta();
		} else if (olek === 'finis' || olek === 'algus') {
			fyysika(dt, olek === 'finis' ? { ...tyhi, pidur: o.v > 1 } : tyhi, true);
		}
		maailm.uuenda(o, dt, { aeg: mangAeg });
		if (pilt) maailm.joonista();
		heli?.uuenda(o, olek === 'soit' || olek === 'finis' || olek === 'avarii');
		hud();
	}
	function fyysika(dt, s, vaba = false) {
		const N = Math.max(1, Math.ceil(dt / (1 / 120))), sd = dt / N;
		let syndmus = null;
		for (let i = 0; i < N && (!syndmus || syndmus === 'pall'); i++) syndmus = samm(o, s, sd, H.a, rada, maailm.takistus) || syndmus;
		if (syndmus === 'pall') syndmus = null; /* heinapall pehmendab, ralli.js lükkab auto välja */
		if (vaba) return;
		if (o.s >= ALGUS) kell += dt;
		tipp = Math.max(tipp, o.v);
		ajalugu.push(o.v); if (ajalugu.length > 90) ajalugu.shift();
		while (kp < 4 && o.s >= ALGUS + (kp + 1) * KP_VAHE) { kp++; vaheajad = [...vaheajad, kell]; }
		seisab = o.v < 1.5 && Math.abs(o.d) > POOL + 1.5 ? seisab + dt : 0;
		if (podradSamm(dt)) syndmus = 'poder';
		if (syndmus || seisab > 3) { avarii(syndmus || 'teelt'); return; }
		if (o.s >= ALGUS + PIKKUS) finis();
	}
	function hud() {
		const nt = olek === 'soit' ? noot(rada, o.s) : null;
		let vale = false;
		if (olek === 'soit' && o.v > 3) { const dh = Math.cos(o.h - rada.h[o.i]); vale = dh < -0.2; }
		const [mx, my] = kaart.P(o.x, o.z);
		h = {
			kell, kmh: Math.round(o.v * 3.6), kaik: o.kaik, noot: nt && nt.d < 190 ? { suund: nt.suund, aste: nt.aste, d: Math.round(nt.d / 10) * 10, sees: nt.sees } : null,
			kp, vahe: vaheajad.length ? `KP${vaheajad.length}  ${aegTekst(vaheajad[vaheajad.length - 1])}` : '',
			loendus, vale, abi: olek === 'soit' && seisab > 1.2, mx, my, prog: Math.max(0, Math.min(1, (o.s - ALGUS) / PIKKUS))
		};
	}

	/* ---------- juhtimine ---------- */
	const KLAHV = { ArrowUp: 'gaas', KeyW: 'gaas', ArrowDown: 'pidur', KeyS: 'pidur', Space: 'kasi', ArrowLeft: 'vasak', KeyA: 'vasak', ArrowRight: 'parem', KeyD: 'parem' };
	function klahv(e, alla) {
		const sees = ekraan?.contains(document.activeElement) || olek === 'soit';
		if (alla && e.code === 'KeyR' && olek === 'soit' && sees) { e.preventDefault(); taasta(); return; }
		if (alla && e.code === 'KeyM' && sees) { muudaHeli(); return; }
		const k = KLAHV[e.code];
		if (!k || !sees) return;
		e.preventDefault();
		sis[k] = alla;
		if (alla && k === 'gaas' && (olek === 'algus' || olek === 'finis')) start();
	}
	function nupp(k, alla) { return (e) => { e.preventDefault(); sis[k] = alla; if (alla && k === 'gaas' && olek === 'algus') start(); }; }
	function start() { laeHeli(); alusta(); }
	function muudaHeli() {
		vaikne = !vaikne;
		heli?.vaikne(vaikne);
		try { localStorage.setItem('pm_etapp_vaikne', vaikne ? '1' : '0'); } catch {}
	}
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
			<p class="et-olud">Kruusatee metsas · 1,85 km · {rada.kurvid.length} kurvi · uus rada iga päev</p>
		</div>
		<div class="et-paremal">
			{#if parim}<p class="et-parim">Sinu tänane parim <b>{aegTekst(parim)}</b></p>{/if}
			{#if seeria > 1}<p class="et-seeria">🔥 {seeria} päeva järjest</p>{/if}
		</div>
	</div>

	<div class="et-ekraan" class:tais={taisekraan} bind:this={ekraan}>
		<div class="et-ala" tabindex="0" role="application" aria-label="Päeva etapp: nooleklahvid juhivad" bind:this={ala}>
			<canvas bind:this={cv} class="et-cv" aria-hidden="true"></canvas>

			{#if olek === 'soit' || olek === 'avarii'}
				<div class="hud-aeg"><b>{aegTekst(h.kell)}</b>{#if h.vahe}<span>{h.vahe}</span>{/if}</div>
				<div class="hud-prog"><i style="width:{h.prog * 100}%"></i>{#each [1, 2, 3, 4] as k (k)}<em class:ok={k <= h.kp} style="left:{(k * KP_VAHE * 100) / PIKKUS}%"></em>{/each}</div>
				<div class="hud-kiirus"><b>{h.kmh}</b><span>km/h</span><small>{h.kaik < 0 ? 'R' : h.kaik}</small></div>
				<svg class="hud-kaart" viewBox="0 0 110 110" aria-hidden="true">
					<path d={kaart.tee} />
					{#each kaart.kpd as [x, y], j (j)}<circle cx={x} cy={y} r="2.6" class:ok={j < h.kp} />{/each}
					<rect x={kaart.fin[0] - 3} y={kaart.fin[1] - 3} width="6" height="6" />
					<circle class="auto" cx={h.mx} cy={h.my} r="4" />
				</svg>
				{#if h.noot}
					<div class="hud-noot" class:ohtlik={h.noot.aste <= 2}>
						<svg viewBox="0 0 40 40" aria-hidden="true" style="transform:scaleX({h.noot.suund})"><path d="M12 34V20a8 8 0 0 1 8-8h10" /><path d="m25 6 6 6-6 6" /></svg>
						<b>{h.noot.aste}</b>
						<span>{h.noot.suund > 0 ? 'PAREM' : 'VASAK'}{#if !h.noot.sees}<em>{h.noot.d} m</em>{/if}</span>
					</div>
				{/if}
				{#if h.loendus > 0}<div class="hud-loendus">{h.loendus > 0.5 ? Math.ceil(h.loendus - 0.5) : 'MINE!'}</div>{/if}
				{#if h.vale}<div class="hud-vale">Vale suund</div>{/if}
				{#if h.abi}<div class="hud-vale abi">Kinni? Vajuta R</div>{/if}
			{/if}

			{#if olek === 'algus' || olek === 'laeb'}
				<div class="et-kiht">
					<b>Päeva etapp</b>
					<span>Kruusaralli aja peale. Auto läheb sinna, kuhu rooli keerad. Järsu kurvi ees pidurda, driftimiseks tõmba kurvis käsipidurit. Kaardilugeja näitab ees tulevat kurvi, 1 on kõige järsem.</span>
					{#if viga}<span class="viga">{viga}</span>{:else}<button type="button" class="btn yel" disabled={olek === 'laeb'} onclick={start}>{olek === 'laeb' ? 'Laen rada…' : 'Stardi'}</button>{/if}
					<small>↑ gaas · ↓ pidur · ← → rool · tühik käsipidur · R tagasi kontrollpunkti · M heli</small>
				</div>
			{/if}
			{#if olek === 'avarii' && teade}
				<div class="et-teade" role="status"><b>Avarii</b><span>{teade} Alustad eelmisest kontrollpunktist.</span></div>
			{/if}
			{#if olek === 'finis' && tulemus}
				<div class="et-kiht et-tul" role="dialog" aria-label="Tulemus">
					<p class="et-k-pea">Finiš · etapp nr {nr}</p>
					<p class="et-k-aeg">{aegTekst(tulemus.aeg)}</p>
					<p class="et-k-s">{tulemus.uus ? 'Sinu tänane parim!' : 'Tänane parim ' + aegTekst(tulemus.parim)} · tipp {tulemus.tipp} km/h · avariisid {tulemus.avariid}</p>
					<p class="et-k-tead"><b>Kas teadsid?</b> Etapi järseima kurvi (raadius {tulemus.R} m) saab kruusal läbida umbes {tulemus.kruus} km/h, kuival asfaldil {tulemus.asfalt} km/h. Kruusal on haaret ligi kolmandiku võrra vähem, seega ka pidurdusmaa on pikem.</p>
					<div class="et-nupud"><button type="button" class="btn yel" onclick={start}>Sõida uuesti</button></div>
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
		<div class="et-nupurida">
			<button type="button" class="et-fs" onclick={muudaHeli} aria-label={vaikne ? 'Heli sisse' : 'Heli välja'}>
				<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z" />{#if vaikne}<path d="m17 9 5 6M22 9l-5 6" />{:else}<path d="M17 8a5 5 0 0 1 0 8M19.5 5a9 9 0 0 1 0 14" />{/if}</svg>
			</button>
			<button type="button" class="et-fs" onclick={taisEkraan} aria-label={taisekraan ? 'Välju täisekraanist' : 'Täisekraan'}>
				<svg viewBox="0 0 24 24" aria-hidden="true">{#if taisekraan}<path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" />{:else}<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />{/if}</svg>
			</button>
		</div>
	</div>
</div>

<style>
	.et { max-width: 1080px; margin: 0 auto; padding: var(--sp-6) 0 var(--sp-10); }
	.et-info { display: flex; justify-content: space-between; align-items: flex-end; gap: var(--sp-3); flex-wrap: wrap; margin-bottom: var(--sp-3); }
	.et-nr { margin: 0; font-family: var(--display); font-size: 26px; font-weight: 700; text-transform: uppercase; }
	.et-olud { margin: 2px 0 0; color: var(--muted); font-size: 15px; }
	.et-paremal { text-align: right; }
	.et-parim, .et-seeria { margin: 0; font-size: 14.5px; }
	.et-parim b { font-family: var(--display); font-size: 20px; }
	.et-ekraan { position: relative; }
	.et-ala { position: relative; border-radius: var(--r-lg, 16px); overflow: hidden; background: #c9d6de; outline: none; user-select: none; -webkit-user-select: none; touch-action: none; }
	.et-ala:focus-visible { box-shadow: 0 0 0 3px var(--yellow); }
	.et-cv { width: 100%; aspect-ratio: 16 / 9; display: block; }
	.et-ala > div:not(.et-kiht):not(.et-juht):not(.et-teade), .et-ala > svg { pointer-events: none; }
	.hud-aeg { position: absolute; left: 14px; top: 12px; display: grid; color: #fff; text-shadow: 0 1px 3px rgba(0, 0, 0, 0.55); }
	.hud-aeg b { font-family: var(--display); font-size: clamp(28px, 4.4vw, 44px); line-height: 1; letter-spacing: 0.01em; }
	.hud-aeg span { font-size: 13px; font-weight: 700; color: #ffe08a; }
	.hud-prog { position: absolute; left: 50%; transform: translateX(-50%); top: 16px; width: min(46%, 420px); height: 6px; border-radius: 3px; background: rgba(0, 0, 0, 0.3); }
	.hud-prog i { position: absolute; inset: 0 auto 0 0; border-radius: 3px; background: #ffc20e; }
	.hud-prog em { position: absolute; top: -4px; width: 3px; height: 14px; margin-left: -1px; background: rgba(255, 255, 255, 0.75); border-radius: 1px; }
	.hud-prog em.ok { background: #ffc20e; }
	.hud-kiirus { position: absolute; right: 16px; bottom: 14px; display: grid; grid-template-columns: auto auto; align-items: end; column-gap: 6px; color: #fff; text-shadow: 0 1px 4px rgba(0, 0, 0, 0.6); }
	.hud-kiirus b { font-family: var(--display); font-size: clamp(40px, 6vw, 64px); line-height: 0.9; grid-row: span 2; }
	.hud-kiirus span { font-size: 12px; font-weight: 700; opacity: 0.85; }
	.hud-kiirus small { font-family: var(--display); font-size: 22px; font-weight: 700; color: #ffc20e; line-height: 1; }
	.hud-kaart { position: absolute; left: 12px; bottom: 12px; width: clamp(84px, 13vw, 130px); height: auto; background: rgba(10, 12, 16, 0.38); border-radius: 12px; }
	.hud-kaart path { fill: none; stroke: rgba(255, 255, 255, 0.85); stroke-width: 2.4; stroke-linejoin: round; stroke-linecap: round; }
	.hud-kaart circle { fill: rgba(255, 255, 255, 0.7); }
	.hud-kaart circle.ok { fill: #ffc20e; }
	.hud-kaart rect { fill: #ffc20e; }
	.hud-kaart circle.auto { fill: #ff3b30; stroke: #fff; stroke-width: 1.5; }
	.hud-noot { position: absolute; left: 50%; top: 38px; transform: translateX(-50%); display: flex; align-items: center; gap: 10px; padding: 8px 16px 8px 12px; border-radius: 14px; background: rgba(12, 14, 18, 0.72); color: #fff; }
	.hud-noot.ohtlik { background: rgba(196, 28, 28, 0.88); }
	.hud-noot svg { width: 34px; height: 34px; fill: none; stroke: #fff; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }
	.hud-noot b { font-family: var(--display); font-size: 44px; line-height: 1; }
	.hud-noot span { display: grid; font-family: var(--display); font-size: 20px; font-weight: 700; line-height: 1.05; }
	.hud-noot em { font-style: normal; color: #ffc20e; }
	.hud-loendus { position: absolute; inset: 0; display: grid; place-items: center; font-family: var(--display); font-size: clamp(80px, 16vw, 160px); font-weight: 700; color: #fff; text-shadow: 0 4px 18px rgba(0, 0, 0, 0.45); }
	.hud-vale { position: absolute; left: 50%; top: 44%; transform: translateX(-50%); padding: 8px 16px; border-radius: 10px; background: rgba(196, 28, 28, 0.88); color: #fff; font-family: var(--display); font-size: 26px; font-weight: 700; text-transform: uppercase; }
	.hud-vale.abi { top: 56%; background: rgba(12, 14, 18, 0.75); }
	.et-kiht { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--sp-3); padding: var(--sp-5); text-align: center; color: #fff; background: linear-gradient(rgba(5, 6, 8, 0.25), rgba(5, 6, 8, 0.72)); }
	.et-kiht b { font-family: var(--display); font-size: 56px; text-transform: uppercase; line-height: 0.95; letter-spacing: 0.01em; }
	.et-kiht span { max-width: 32em; color: #e9ecef; font-size: 15.5px; line-height: 1.45; }
	.et-kiht span.viga { color: #ffd2d2; }
	.et-kiht small { color: #c3c9d1; font-size: 13px; }
	.et-teade { position: absolute; left: 50%; top: 30%; transform: translateX(-50%); width: min(92%, 520px); background: rgba(16, 18, 22, 0.9); border-left: 4px solid #ff5a5a; color: #fff; border-radius: 12px; padding: 12px 16px; display: grid; gap: 4px; font-size: 15px; line-height: 1.45; }
	.et-teade b { color: #ff5a5a; font-family: var(--display); font-size: 24px; text-transform: uppercase; }
	.et-tul { overflow: auto; }
	.et-k-pea { margin: 0; color: #ffc20e; font-weight: 700; font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase; }
	.et-k-aeg { margin: 0; font-family: var(--display); font-size: 80px; font-weight: 700; color: #ffc20e; line-height: 1; }
	.et-k-s { margin: 0; color: #e3e6ea; font-size: 15px; }
	.et-k-tead { margin: 0; max-width: 32em; color: #d5dae0; font-size: 14px; line-height: 1.45; background: rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 10px 14px; }
	.et-k-tead b { color: #fff; font-family: inherit; font-size: inherit; text-transform: none; }
	.et-nupud { display: flex; gap: var(--sp-2); }
	.et-juht { position: absolute; left: 0; right: 0; bottom: 0; display: flex; justify-content: space-between; padding: 10px; pointer-events: none; }
	.et-pool { display: flex; gap: 10px; }
	.et-juht button { pointer-events: auto; width: 68px; height: 68px; border-radius: 18px; border: 1px solid rgba(255, 255, 255, 0.3); background: rgba(10, 11, 13, 0.4); color: #fff; font-size: 24px; font-weight: 800; cursor: pointer; touch-action: none; }
	.et-juht button.gaas { background: rgba(22, 101, 52, 0.62); font-size: 15px; }
	.et-juht button.pidur { background: rgba(153, 27, 27, 0.62); font-size: 15px; }
	.et-juht button.kasi { background: rgba(120, 80, 10, 0.62); font-size: 12px; line-height: 1.1; }
	@media (hover: hover) and (pointer: fine) { .et-juht { display: none; } }
	@media (pointer: coarse) { .hud-kaart { display: none; } .hud-kiirus { bottom: auto; top: 10px; right: 112px; } }
	.et-nupurida { position: absolute; top: 10px; right: 10px; display: flex; gap: 8px; z-index: 2; }
	.et-fs { width: 40px; height: 40px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.25); background: rgba(10, 11, 13, 0.45); color: #fff; display: grid; place-items: center; cursor: pointer; padding: 0; }
	.et-fs svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
	.et-ekraan.tais { position: fixed; inset: 0; z-index: 1000; background: #0a0b0d; display: flex; }
	.et-ekraan.tais .et-ala { flex: 1; border-radius: 0; display: flex; }
	.et-ekraan.tais .et-cv { aspect-ratio: auto; height: 100%; }
</style>
