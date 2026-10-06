<script>
	/* MÄNG „Kui kiiresti SINA pidurdad?“ (suur plaan faas 2).
	   Kaks olukorda, sama füüsika mis kalkulaatoris (engine.js pidurdusjälg):
	    - PIDURITULED: eesolev auto pidurdab (süttivad tagatuled), sina sõidad
	      sama autoga valitud pikivahega järel. Hiline vajutus = kokkupõrge.
	    - PIMEDAS: jalakäija tuleb nähtavale riietusest sõltuval kaugusel
	      (Transpordiamet 2025: tumedad 30 m, heledad 45 m, helkur 140 m).
	   Reaktsioon = täpselt mõõdetud aeg (midagi juurde ei lisata). Märkus:
	   testis tead, et takistus tuleb. Isikuandmeid ei koguta; link ?r=ms. */
	import { onMount, onDestroy } from 'svelte';
	import { version } from '$app/environment';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();

	const KATSEID = 3;
	const NAHT = [
		['tume', 30, t('Tumedad riided')],
		['hele', 45, t('Heledad riided')],
		['helkur', 140, t('Helkuriga')]
	];

	let P = null, core = null;
	let veh = $state(null);
	let reziim = $state('tuled'); /* tuled | pime */
	let kiirus = $state(90);
	let vahe = $state(0.5); /* pikivahe, s */
	let riie = $state('tume');
	let olek = $state('algus'); /* algus | oota | nyyd | soit | vara | vahe | tulemus */
	let ajad = $state([]);
	let tulemused = $state([]); /* iga katse: { r, crash, kmh | m } */
	let sobra = $state(0);
	let jagatud = $state('');
	/* stseen */
	let gap = $state(0); /* m eesoleva autoni / jalakäijani */
	let tuled = $state(false);
	let nahtav = $state(false);
	let crash = $state(false);
	let teeNihe = $state(0);
	let taimer = 0, raf = 0, t0 = 0, tVajutus = null;

	onMount(async () => {
		try {
			const r = +new URLSearchParams(location.search).get('r');
			if (r >= 100 && r <= 3000) sobra = Math.round(r);
		} catch {}
		await import('$lib/engine.js');
		P = globalThis.Pidurdus;
		core = await (await fetch('/data/core.json?v=' + encodeURIComponent(version))).json();
		let key = null;
		try { key = JSON.parse(sessionStorage.getItem('pm_veh') || 'null'); } catch {}
		const byKey = (k) => core.vehicles.find((v) => v.key === k);
		veh = (key && byKey(String(key).split('~')[0])) || byKey('vw_golf_8');
	});
	onDestroy(() => { clearTimeout(taimer); if (typeof cancelAnimationFrame === 'function') cancelAnimationFrame(raf); });

	/* ---------- füüsika: pidurdus ajas samast mootorist ---------- */
	function jalg(kmh) {
		const tyre = { key: 'x', name: 'x', category: 'SUMMER_TOURING', wetGripIndex: core.gClass?.C?.SUMMER_TOURING?.[0] || 1.32, treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: false, size: veh.oemSize, gSource: 'label' };
		const r = P.stoppingDistance(tyre, veh, { speedKmh: kmh, surface: 'ASPHALT', texture: 'NORMAL', waterMm: 1, tempC: 10, payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1 });
		/* jälg [s, km/h] → aeg-tabel [t, s, v] sammuga 0,01 s */
		const tr = r.trace;
		const vAt = (s) => {
			for (let i = 1; i < tr.length; i++) if (tr[i][0] >= s) { const a = tr[i - 1], b = tr[i], k = (s - a[0]) / Math.max(1e-9, b[0] - a[0]); return (a[1] + k * (b[1] - a[1])) / 3.6; }
			return 0;
		};
		const T = [], dt = 0.01;
		let s = 0, v = kmh / 3.6, tt = 0;
		while (v > 0.05 && tt < 20) { T.push([tt, s, v]); s += v * dt; tt += dt; v = vAt(s); }
		T.push([tt, r.distanceM, 0]);
		return { T, d: r.distanceM };
	}
	function pidurdusAjal(J, tau) { /* [s, v] tau sekundit pärast pidurdama hakkamist */
		if (tau <= 0) return [0, J.T[0][2]];
		const i = Math.min(J.T.length - 1, Math.floor(tau / 0.01));
		return [J.T[i][1], J.T[i][2]];
	}
	let J = null;
	/* sinu asukoht ja kiirus ajal t (t=0: tuled süttivad / jalakäija tuleb nähtavale) */
	function sina(tt, r, v0) {
		if (r == null || tt < r) return [v0 * tt, v0];
		const x = pidurdusAjal(J, tt - r);
		return [v0 * r + x[0], x[1]];
	}
	const kaugus = () => NAHT.find((x) => x[0] === riie)[1];
	/* lõpptulemus reaktsiooniga r: { crash, kmh } või { crash: false, m } */
	function lopp(r) {
		const v0 = kiirus / 3.6;
		if (reziim === 'pime') {
			const D = kaugus(), vaja = v0 * r + J.d;
			if (vaja <= D) return { crash: false, m: D - vaja };
			let kmh = v0 * 3.6;
			if (v0 * r < D) { const rest = D - v0 * r; const p = J.T.find((x) => x[1] >= rest); kmh = p ? p[2] * 3.6 : 0; }
			return { crash: true, kmh };
		}
		const g0 = v0 * vahe;
		for (let tt = 0; tt < 25; tt += 0.005) {
			const pe = pidurdusAjal(J, tt), ees = g0 + pe[0], vE = pe[1];
			const [s, v] = sina(tt, r, v0);
			if (ees - s <= 0) return { crash: true, kmh: Math.max(0, v - vE) * 3.6 };
			if (v <= 0.05 && vE <= 0.05) return { crash: false, m: ees - s };
		}
		return { crash: false, m: 0 };
	}

	/* ---------- mänguvoog ---------- */
	function alusta() {
		clearTimeout(taimer); cancelAnimationFrame(raf);
		J = jalg(kiirus);
		crash = false; tuled = false; nahtav = false; tVajutus = null;
		gap = reziim === 'tuled' ? (kiirus / 3.6) * vahe : 200;
		olek = 'oota';
		const viide = 1500 + Math.random() * 3000, start = performance.now();
		const ooteKaader = () => { teeNihe = (((performance.now() - start) / 1000) * kiirus / 3.6) % 12; raf = requestAnimationFrame(ooteKaader); };
		raf = requestAnimationFrame(ooteKaader);
		taimer = setTimeout(() => {
			cancelAnimationFrame(raf);
			olek = 'nyyd'; t0 = performance.now(); tVajutus = null;
			tuled = reziim === 'tuled'; nahtav = reziim === 'pime';
			kaader();
		}, viide);
	}
	/* reaalajas: kokkupõrge võib tulla enne vajutust */
	function kaader() {
		const tt = (performance.now() - t0) / 1000, v0 = kiirus / 3.6, r = tVajutus;
		const [s, v] = sina(tt, r, v0);
		teeNihe = s % 12;
		let ees, vE = 0;
		if (reziim === 'tuled') { const p = pidurdusAjal(J, tt); ees = v0 * vahe + p[0]; vE = p[1]; } else ees = kaugus();
		gap = Math.max(0, ees - s);
		if (gap <= 0.01) { crash = true; lopeta(r == null ? tt : r, { crash: true, kmh: Math.max(0, v - vE) * 3.6 }); return; }
		if (r != null && v <= 0.05 && vE <= 0.05) { lopeta(r, { crash: false, m: gap }); return; }
		if (tt > 25) { lopeta(r ?? tt, lopp(r ?? tt)); return; }
		raf = requestAnimationFrame(kaader);
	}
	function lopeta(r, res) {
		cancelAnimationFrame(raf);
		const rec = { r, ...res, vajutamata: tVajutus == null };
		tulemused = [...tulemused, rec];
		if (!rec.vajutamata) ajad = [...ajad, Math.round(r * 1000)];
		track(reziim, (res.crash ? 'kokkupõrge ' + Math.round(res.kmh) + ' km/h' : 'peatus ' + Math.round(res.m) + ' m') + ' · ' + Math.round(r * 1000) + ' ms');
		olek = reziim === 'pime' || tulemused.length >= KATSEID ? 'tulemus' : 'vahe';
	}
	function vajuta() {
		if (!veh || !P) return;
		if (olek === 'algus' || olek === 'vahe' || olek === 'vara') { if (olek === 'algus') { tulemused = []; ajad = []; track('algus', reziim); } alusta(); return; }
		if (olek === 'oota') { clearTimeout(taimer); cancelAnimationFrame(raf); olek = 'vara'; return; }
		if (olek === 'nyyd') { if (tVajutus == null) { tVajutus = (performance.now() - t0) / 1000; olek = 'soit'; } return; }
		if (olek === 'tulemus') { tulemused = []; ajad = []; jagatud = ''; alusta(); }
	}
	const kaib = $derived(olek === 'oota' || olek === 'nyyd' || olek === 'soit');
	function vaheta(r) { if (kaib) return; reziim = r; olek = 'algus'; tulemused = []; ajad = []; kiirus = r === 'pime' ? 50 : 90; }
	function seadista(f) { if (kaib) return; f(); if (olek === 'tulemus' || olek === 'vahe' || olek === 'vara') { olek = 'algus'; tulemused = []; ajad = []; } }
	function klahv(e) {
		if ((e.code === 'Space' || e.key === 'Enter') && document.activeElement?.closest?.('.rk-ala')) { e.preventDefault(); vajuta(); }
	}
	const mediaan = (a) => { const s = [...a].sort((x, y) => x - y), m = Math.floor(s.length / 2); return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2); };
	const tulemusMs = $derived(ajad.length ? mediaan(ajad) : 0);
	const viimane = $derived(tulemused.length ? tulemused[tulemused.length - 1] : null);
	function track(e, v) { try { window.PM_TRACK && window.PM_TRACK('mang', e + (v ? ' · ' + v : '')); } catch {} }

	/* võrdlus: sinu aeg vs 1 s vs 2 s samas olukorras */
	const read = $derived.by(() => {
		if (olek !== 'tulemus' || !veh || !P) return [];
		void [kiirus, vahe, riie, reziim];
		J = jalg(kiirus);
		const sinu = tulemusMs ? tulemusMs / 1000 : null;
		return [
			...(sinu ? [[t('Sina'), sinu, lopp(sinu), true]] : []),
			[t('Tavaline juht liikluses'), 1, lopp(1), false],
			[t('Tähelepanu mujal, nt telefon'), 2, lopp(2), false]
		];
	});

	const LOC = keel.lang === 'en' ? 'en-GB' : keel.lang === 'ru' ? 'ru-RU' : 'et-EE';
	const f1 = (x) => x.toLocaleString(LOC, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
	const f2 = (ms) => (ms / 1000).toLocaleString(LOC, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
	const lause = (x) => (x.crash ? t('Kokkupõrge') + ' ' + Math.round(x.kmh) + ' ' + t('km/h') : t('Peatud') + ' ' + f1(x.m) + ' ' + t('m enne'));

	/* ---------- perspektiiv (viewBox 400×360) ---------- */
	const HOR = 110, ALL = 340;
	const yZ = (z) => HOR + (ALL - HOR) * Math.min(1, 6 / (z + 6));
	const kZ = (z) => Math.min(3.2, 14 / (z + 4));
	const kriipsud = $derived(Array.from({ length: 9 }, (_, i) => i * 12 + 12 - teeNihe).filter((z) => z > 0.5));

	/* ---------- jagamine ---------- */
	function link() { return location.origin + keel.L('/liiklusohutus/reaktsioon/') + (tulemusMs ? '?r=' + tulemusMs : ''); }
	function ring(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
	async function pilt() {
		try { await Promise.all([document.fonts.load('700 100px "Barlow Condensed"'), document.fonts.load('700 40px Inter')]); } catch {}
		const cv = document.createElement('canvas'); cv.width = 1080; cv.height = 1920;
		const g = cv.getContext('2d'), D = '"Barlow Condensed", "Arial Narrow", sans-serif', B = 'Inter, system-ui, sans-serif';
		g.fillStyle = '#0a0b0d'; g.fillRect(0, 0, 1080, 1920);
		g.fillStyle = '#fff'; g.font = 'italic 800 64px ' + B; g.fillText('PIDURDUSMAA', 90, 190); const w = g.measureText('PIDURDUSMAA').width; g.fillStyle = '#ffc20e'; g.fillText('.ee', 90 + w, 190);
		g.fillStyle = '#ffc20e'; g.font = '700 44px ' + B; g.fillText((reziim === 'pime' ? t('Pimedas') + ' · ' + NAHT.find((x) => x[0] === riie)[2] : t('Minu reaktsioon')).toUpperCase(), 90, 360);
		const tx = tulemusMs ? f2(tulemusMs) : '—';
		g.fillStyle = '#ffc20e'; g.font = '700 300px ' + D; g.fillText(tx, 80, 640); const w2 = g.measureText(tx).width; g.fillStyle = '#fff'; g.font = '700 120px ' + D; g.fillText(' s', 80 + w2, 640);
		const minu = viimane;
		g.fillStyle = minu && minu.crash ? '#ff5a5a' : '#4ade80'; g.font = '700 56px ' + B; g.fillText(minu ? lause(minu) : '', 90, 770);
		g.fillStyle = '#aab1bc'; g.font = '500 36px ' + B; g.fillText(kiirus + ' ' + t('km/h') + ' · ' + t('märg tee') + (reziim === 'tuled' ? ' · ' + t('vahe') + ' ' + f1(vahe) + ' s' : ''), 90, 830);
		let y = 960;
		read.forEach(([n, s, r, me]) => {
			g.font = (me ? '700 ' : '500 ') + '38px ' + B; g.fillStyle = me ? '#fff' : '#aab1bc'; g.fillText(n + ' (' + f2(s * 1000) + ' s)', 90, y);
			g.fillStyle = r.crash ? '#ff5a5a' : '#4ade80'; g.font = '700 40px ' + B; g.fillText(lause(r), 90, y + 56);
			y += 150;
		});
		y = 1500; g.fillStyle = '#16181d'; ring(g, 90, y, 900, 210, 28); g.fill(); g.strokeStyle = '#2b3039'; g.lineWidth = 2; g.stroke();
		g.fillStyle = '#fff'; g.font = '700 54px ' + B; g.fillText(t('Kas sina oled kiirem?'), 130, y + 88);
		g.fillStyle = '#ffc20e'; g.font = '700 64px ' + D; g.fillText('pidurdusmaa.ee', 130, y + 168);
		return new Promise((ok) => cv.toBlob(ok, 'image/png'));
	}
	async function jaga() {
		const l = link();
		try { navigator.clipboard.writeText(l); } catch {}
		const blob = await pilt();
		let fail = null;
		try { fail = new File([blob], 'pidurdusmaa-reaktsioon.png', { type: 'image/png' }); } catch {}
		if (fail && navigator.canShare && navigator.canShare({ files: [fail] })) {
			try { await navigator.share({ files: [fail] }); } catch {}
			jagatud = t('Link on kopeeritud. Storys lisa kleebis „Link“ ja kleebi — sõbrad saavad proovida.');
			track('jaga', 'story');
		} else {
			const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'pidurdusmaa-reaktsioon.png'; a.click();
			jagatud = t('Pilt laaditi alla ja link on kopeeritud. Lisa pilt storysse ja kleebi link kleebisega „Link“.');
			track('jaga', 'arvutis');
		}
	}
	function kopeeri() { try { navigator.clipboard.writeText(link()); jagatud = t('Link kopeeritud ✓'); track('jaga', 'link'); } catch {} }
</script>

<svelte:window onkeydown={klahv} />

<div class="rk">
	<div class="rk-rezh" role="tablist" aria-label={t('Olukord')}>
		<button type="button" role="tab" aria-selected={reziim === 'tuled'} disabled={kaib} onclick={() => vaheta('tuled')}>{t('Eesolev auto pidurdab')}</button>
		<button type="button" role="tab" aria-selected={reziim === 'pime'} disabled={kaib} onclick={() => vaheta('pime')}>{t('Jalakäija pimedas')}</button>
	</div>

	<div class="rk-seaded">
		<div class="rk-seg" role="group" aria-label={t('Kiirus')}>
			{#each reziim === 'pime' ? [30, 50, 70, 90] : [50, 90, 110] as k (k)}<button type="button" disabled={kaib} aria-pressed={kiirus === k} onclick={() => seadista(() => (kiirus = k))}>{k} {t('km/h')}</button>{/each}
		</div>
		{#if reziim === 'tuled'}
			<div class="rk-seg" role="group" aria-label={t('Pikivahe')}>
				{#each [0.5, 1, 2] as k (k)}<button type="button" disabled={kaib} aria-pressed={vahe === k} onclick={() => seadista(() => (vahe = k))}>{t('vahe')} {f1(k)} s</button>{/each}
			</div>
		{:else}
			<div class="rk-seg" role="group" aria-label={t('Jalakäija')}>
				{#each NAHT as [k, , n] (k)}<button type="button" disabled={kaib} aria-pressed={riie === k} onclick={() => seadista(() => (riie = k))}>{n}</button>{/each}
			</div>
		{/if}
	</div>

	{#if sobra && olek === 'algus'}
		<p class="rk-sober">{t('Sõbra reaktsioon:')} <b>{f2(sobra)} s</b>. {t('Kas oled kiirem?')}</p>
	{/if}

	<button type="button" class="rk-ala" class:crash onpointerdown={(e) => { e.preventDefault(); vajuta(); }} aria-live="polite">
		<svg class="rk-stseen" viewBox="0 0 400 360" aria-hidden="true">
			{#if reziim === 'pime'}
				<defs><linearGradient id="rk-tuli" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#3a3a2e" /><stop offset="0.55" stop-color="#15160f" /><stop offset="1" stop-color="#030405" /></linearGradient></defs>
				<rect width="400" height="360" fill="#030405" />
				<polygon points="40,360 360,360 215,{HOR} 185,{HOR}" fill="url(#rk-tuli)" />
			{:else}
				<rect width="400" height={HOR} fill="#1b1f27" />
				<rect y={HOR} width="400" height={360 - HOR} fill="#121419" />
				<polygon points="40,360 360,360 215,{HOR} 185,{HOR}" fill="#2a2e36" />
			{/if}
			{#each kriipsud as z (z)}
				<rect x={200 - 2 * kZ(z)} y={yZ(z)} width={4 * kZ(z)} height={Math.max(1, 10 * kZ(z))} fill={reziim === 'pime' ? '#55533f' : '#c9cdd4'} opacity={reziim === 'pime' ? Math.max(0, 1 - z / 40) : 1} />
			{/each}
			{#if reziim === 'tuled'}
				<g transform="translate(200 {yZ(gap)}) scale({kZ(gap)})">
					<rect x="-55" y="-62" width="110" height="52" rx="10" fill="#3a404b" />
					<rect x="-40" y="-56" width="80" height="20" rx="5" fill="#16181d" />
					<rect x="-50" y="-30" width="22" height="9" rx="3" class="tl" class:on={tuled} />
					<rect x="28" y="-30" width="22" height="9" rx="3" class="tl" class:on={tuled} />
					<rect x="-10" y="-62" width="20" height="4" rx="2" class="tl" class:on={tuled} />
					<rect x="-48" y="-10" width="20" height="12" rx="3" fill="#0a0b0d" />
					<rect x="28" y="-10" width="20" height="12" rx="3" fill="#0a0b0d" />
				</g>
			{:else if nahtav}
				<g transform="translate(200 {yZ(gap)}) scale({kZ(gap)})" opacity={Math.min(1, (riie === 'tume' ? 0.32 : riie === 'hele' ? 0.75 : 0.45) + (gap < 20 ? (20 - gap) / 40 : 0))}>
					<circle cx="0" cy="-58" r="7" fill={riie === 'hele' ? '#d9d6c8' : '#5a5850'} />
					<rect x="-8" y="-50" width="16" height="28" rx="5" fill={riie === 'hele' ? '#d9d6c8' : '#5a5850'} />
					<rect x="-7" y="-22" width="5" height="22" rx="2" fill={riie === 'hele' ? '#cfccbe' : '#4d4b44'} />
					<rect x="2" y="-22" width="5" height="22" rx="2" fill={riie === 'hele' ? '#cfccbe' : '#4d4b44'} />
				</g>
				{#if riie === 'helkur'}
					<circle cx={200 + 7 * kZ(gap)} cy={yZ(gap) - 20 * kZ(gap)} r={Math.max(2, 3 * kZ(gap))} fill="#fffbe0" class="helk" />
				{/if}
			{/if}
			{#if crash}<text x="200" y="70" text-anchor="middle" class="bang">{t('KOKKUPÕRGE')}</text>{/if}
		</svg>
		<span class="rk-tekst">
			{#if olek === 'algus'}<b>{t('Vajuta, et alustada')}</b><small>{reziim === 'pime' ? t('Sõidad pimedas. Kui näed teel jalakäijat, vajuta kohe.') : t('Kui eesoleva auto pidurituled süttivad, vajuta kohe.')} {t('Arvutis ka tühikuklahv.')}</small>
			{:else if olek === 'oota'}<b>{t('Sõidad…')}</b><small>{reziim === 'pime' ? t('Vaata teed') : t('Jälgi eesolevat autot')}</small>
			{:else if olek === 'nyyd' || olek === 'soit'}<b>&nbsp;</b><small>&nbsp;</small>
			{:else if olek === 'vara'}<b>{t('Liiga vara!')}</b><small>{t('Vajuta uuesti, et seda katset korrata')}</small>
			{:else if viimane}<b class:punane={viimane.crash} class:roheline={!viimane.crash}>{lause(viimane)}</b><small>{viimane.vajutamata ? t('Ei vajutanud') : t('Reaktsioon') + ' ' + f2(viimane.r * 1000) + ' s'}{olek === 'vahe' ? ' · ' + t('Katse') + ' ' + tulemused.length + ' / ' + KATSEID + ' · ' + t('vajuta, et jätkata') : ' · ' + t('Vajuta, et uuesti proovida')}</small>{/if}
		</span>
		{#if reziim === 'tuled'}<span class="rk-pallid" aria-hidden="true">{#each Array(KATSEID) as _, i}<i class:on={i < tulemused.length} class:cr={tulemused[i]?.crash}></i>{/each}</span>{/if}
	</button>

	{#if olek === 'tulemus' && read.length}
		<div class="rk-tul">
			{#if tulemusMs}<p class="rk-suur">{reziim === 'tuled' ? t('Sinu reaktsioon (3 katse mediaan)') : t('Sinu reaktsioon')}: <b>{f2(tulemusMs)} s</b>{#if sobra}{' · ' + (tulemusMs < sobra ? t('Sõbrast kiirem!') : tulemusMs > sobra ? t('Sõber oli kiirem') + ' (' + f2(sobra) + ' s)' : t('Täpselt sama kiire kui sõber!'))}{/if}</p>{/if}
			<p class="rk-pea">{t('Sama olukord, erinev reaktsioon')} · {veh.name}</p>
			<ol class="rk-read">
				{#each read as [nimi, s, r, me] (nimi)}
					<li class:me><span class="n">{nimi} <small>{f2(s * 1000)} s</small></span><span class="o" class:punane={r.crash}>{lause(r)}</span></li>
				{/each}
			</ol>
			<p class="rk-sel">{t('Testis sa tead, et takistus tuleb. Liikluses mitte — seal on reaktsioon tavaliselt pikem.')} {t('Märg asfalt, uued keskmised suverehvid, sama arvutus mis kalkulaatoris.')}</p>
			<div class="rk-nupud">
				<button type="button" class="btn yel" onclick={jaga}>{t('Jaga storysse')}</button>
				<button type="button" class="btn" onclick={kopeeri}>{t('Kopeeri link')}</button>
				<a class="btn" href={keel.L('/')}>{t('Arvuta oma auto ja rehvidega')}</a>
			</div>
			{#if jagatud}<p class="rk-sel" role="status">{jagatud}</p>{/if}
		</div>
	{/if}
</div>

<style>
	.rk { max-width: 760px; margin: 0 auto; padding: var(--sp-6) 0 var(--sp-10); }
	.rk-rezh { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-1); background: #fff; border: 1px solid var(--line); padding: var(--sp-1); border-radius: 12px; }
	.rk-rezh button { border: 0; background: transparent; padding: var(--sp-3); border-radius: 9px; font-weight: 700; font-size: 15px; color: var(--muted); cursor: pointer; }
	.rk-rezh button[aria-selected='true'] { background: var(--ink); color: #fff; box-shadow: inset 0 -3px 0 var(--yellow); }
	.rk-seaded { display: flex; flex-wrap: wrap; gap: var(--sp-2); margin: var(--sp-3) 0; }
	.rk-seg { display: flex; flex-wrap: wrap; gap: var(--sp-1); background: #fff; border: 1px solid var(--line); padding: var(--sp-1); border-radius: 10px; }
	.rk-seg button { border: 0; background: transparent; padding: 6px 10px; border-radius: 7px; font-weight: 600; font-size: 13.5px; color: var(--muted); cursor: pointer; }
	.rk-seg button[aria-pressed='true'] { background: var(--paper-2); color: var(--text); box-shadow: inset 0 -2px 0 var(--yellow); }
	.rk-rezh button:disabled, .rk-seg button:disabled { cursor: default; opacity: 0.6; }
	.rk-sober { background: #fff; border: 1px solid var(--line); border-radius: var(--r); padding: var(--sp-3) var(--sp-4); margin: 0 0 var(--sp-3); text-align: center; }
	.rk-ala { width: 100%; border: 0; border-radius: var(--r-lg, 16px); background: var(--ink); color: #fff; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: var(--sp-2); padding: 0 0 var(--sp-5); overflow: hidden; touch-action: manipulation; user-select: none; -webkit-user-select: none; font: inherit; }
	.rk-ala:focus-visible { outline: 3px solid var(--yellow); outline-offset: 3px; }
	.rk-ala.crash { animation: raputa 0.4s; }
	@keyframes raputa { 20% { transform: translate(-6px, 3px); } 40% { transform: translate(6px, -3px); } 60% { transform: translate(-4px, 2px); } 80% { transform: translate(3px, 0); } }
	.rk-stseen { width: 100%; display: block; }
	.tl { fill: #5a1f1f; }
	.tl.on { fill: #ff2b2b; filter: drop-shadow(0 0 6px #ff2b2b); }
	.helk { filter: drop-shadow(0 0 6px #fffbe0); }
	.bang { font-family: var(--display); font-weight: 700; font-size: 44px; fill: #ff4d4d; }
	.rk-tekst { display: flex; flex-direction: column; gap: 6px; text-align: center; padding: 0 var(--sp-4); min-height: 74px; }
	.rk-tekst b { font-family: var(--display); font-size: 36px; letter-spacing: 0.02em; text-transform: uppercase; line-height: 1; }
	.rk-tekst b.punane, .rk-tekst b.roheline { text-transform: none; font-size: 32px; }
	.rk-tekst b.punane { color: #ff5a5a; }
	.rk-tekst b.roheline { color: #4ade80; }
	.rk-tekst small { color: var(--muted-d); font-size: 14.5px; max-width: 460px; }
	.rk-pallid { display: flex; gap: 8px; }
	.rk-pallid i { width: 10px; height: 10px; border-radius: 50%; background: #2b3039; }
	.rk-pallid i.on { background: #4ade80; }
	.rk-pallid i.cr { background: #ff5a5a; }
	.rk-tul { background: #fff; border: 1px solid var(--line); border-radius: var(--r-lg, 16px); padding: var(--sp-5); margin-top: var(--sp-4); }
	.rk-suur { margin: 0 0 var(--sp-2); font-size: 17px; }
	.rk-pea { margin: var(--sp-3) 0 var(--sp-2); font-weight: 700; }
	.rk-read { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--sp-2); }
	.rk-read li { display: flex; justify-content: space-between; gap: var(--sp-3); padding: var(--sp-2) var(--sp-3); background: var(--paper-2); border-radius: 8px; align-items: baseline; }
	.rk-read .n { font-size: 14.5px; color: var(--muted); }
	.rk-read .n small { font-size: 12.5px; margin-left: 4px; }
	.rk-read .me .n { color: var(--text); font-weight: 700; }
	.rk-read .o { font-weight: 800; color: #15803d; text-align: right; }
	.rk-read .o.punane { color: var(--red); }
	.rk-sel { font-size: 13px; color: var(--muted); margin: var(--sp-3) 0 0; line-height: 1.45; }
	.rk-nupud { display: flex; flex-wrap: wrap; gap: var(--sp-2); margin-top: var(--sp-4); }
	@media (max-width: 640px) { .rk-tekst b { font-size: 30px; } .rk-nupud .btn { flex: 1 1 100%; text-align: center; } }
</style>
