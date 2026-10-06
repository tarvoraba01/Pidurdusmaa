<script>
	/* MÄNG „Kui kiiresti SINA pidurdad?“ (6.10.2026, suur plaan faas 2).
	   Eesoleva auto pidurituled süttivad juhuslikul hetkel → vajuta.
	   3 katset, tulemus = mediaan. Peatumisteekond tuleb SAMAST mootorist
	   (engine.js) sinu autoga (kui kalkulaatoris valitud) või Golf 8-ga.
	   Ausus: test mõõdab lihtsat reaktsiooni ekraanil. Liikluses lisandub
	   jala viimine pidurile (~0,2 s) ja ootamatus — näitame ka 1 s ja 2 s.
	   Isikuandmeid ei koguta; jagatav link sisaldab ainult aega (?r=ms). */
	import { onMount } from 'svelte';
	import { version } from '$app/environment';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();

	const KATSEID = 3;
	const JALG = 0.2; /* jala viimine gaasilt pidurile, s */
	const PIKK = 2.5; /* üle selle = ei vajutanud */

	let P = null, core = null;
	let veh = $state(null);
	let kiirus = $state(90);
	let olek = $state('algus'); /* algus | oota | nyyd | vara | vahe | tulemus */
	let ajad = $state([]);
	let viimane = $state(0);
	let sobra = $state(0); /* sõbra tulemus lingist, ms */
	let jagatud = $state('');
	let taimer = 0, t0 = 0;

	onMount(async () => {
		try {
			const r = +new URLSearchParams(location.search).get('r');
			if (r >= 100 && r <= 2500) sobra = Math.round(r);
		} catch {}
		await import('$lib/engine.js');
		P = globalThis.Pidurdus;
		const d = await (await fetch('/data/core.json?v=' + encodeURIComponent(version))).json();
		core = d;
		let key = null;
		try { key = JSON.parse(sessionStorage.getItem('pm_veh') || 'null'); } catch {}
		const byKey = (k) => d.vehicles.find((v) => v.key === k);
		veh = (key && byKey(String(key).split('~')[0])) || byKey('vw_golf_8');
	});

	function alusta() {
		clearTimeout(taimer);
		olek = 'oota';
		taimer = setTimeout(() => { olek = 'nyyd'; t0 = performance.now(); taimer = setTimeout(() => vajuta(true), PIKK * 1000); }, 1200 + Math.random() * 2800);
	}
	function vajuta(aegus) {
		if (olek === 'algus' || olek === 'vahe') { if (olek === 'algus') { ajad = []; track('algus'); } alusta(); return; }
		if (olek === 'vara') { alusta(); return; }
		if (olek === 'oota') { clearTimeout(taimer); olek = 'vara'; return; }
		if (olek === 'nyyd') {
			clearTimeout(taimer);
			viimane = aegus === true ? PIKK * 1000 : Math.round(performance.now() - t0);
			ajad = [...ajad, viimane];
			if (ajad.length >= KATSEID) { olek = 'tulemus'; track('tulemus', Math.round(mediaan(ajad) / 50) * 50 + ' ms'); }
			else olek = 'vahe';
			return;
		}
		if (olek === 'tulemus') { ajad = []; jagatud = ''; alusta(); }
	}
	function klahv(e) {
		if ((e.code === 'Space' || e.key === 'Enter') && olek !== 'tulemus' && document.activeElement?.closest?.('.rk-ala')) { e.preventDefault(); vajuta(); }
	}
	const mediaan = (a) => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };
	const tulemusMs = $derived(ajad.length >= KATSEID ? mediaan(ajad) : 0);

	function track(e, v) { try { window.PM_TRACK && window.PM_TRACK('mang', e + (v ? ' · ' + v : '')); } catch {} }

	/* peatumisteekond: märg asfalt, uus C-klassi suverehv (sama mis kalkulaatori keskmine) */
	function teekond(reaktS) {
		if (!P || !veh) return null;
		const tyre = { key: 'x', name: 'x', category: 'SUMMER_TOURING', wetGripIndex: (core.gClass && core.gClass.C && core.gClass.C.SUMMER_TOURING ? core.gClass.C.SUMMER_TOURING[0] : 1.32), treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: false, size: veh.oemSize, gSource: 'label' };
		const cond = { speedKmh: kiirus, surface: 'ASPHALT', texture: 'NORMAL', waterMm: 1, tempC: 10, payloadKg: 75, gradientPct: 0, reactionTimeS: Math.min(5, reaktS), brakeCondition: 1 };
		try { const r = P.stoppingDistance(tyre, veh, cond); return { kokku: r.distanceM + r.reactionM, reakt: r.reactionM, pidur: r.distanceM }; } catch { return null; }
	}
	const read = $derived.by(() => {
		if (!tulemusMs || !veh) return [];
		const sina = tulemusMs / 1000 + JALG;
		return [
			[t('Sina, kui oled valmis'), sina, teekond(sina), true],
			[t('Tavaline juht liikluses (1 s)'), 1, teekond(1), false],
			[t('Tähelepanu mujal, nt telefon (2 s)'), 2, teekond(2), false]
		].filter((x) => x[2]);
	});
	const maxM = $derived(read.length ? Math.max(...read.map((x) => x[2].kokku)) : 1);
	const f1 = (x) => x.toLocaleString(keel.lang === 'en' ? 'en-GB' : keel.lang === 'ru' ? 'ru-RU' : 'et-EE', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
	const f2 = (ms) => (ms / 1000).toLocaleString(keel.lang === 'en' ? 'en-GB' : 'et-EE', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
	const hinnang = $derived(!tulemusMs ? '' : tulemusMs < 250 ? t('Väga kiire!') : tulemusMs < 330 ? t('Kiire.') : tulemusMs < 450 ? t('Tavaline.') : t('Aeglane — väsinud?'));

	/* ---------- jagamine: pilt (story 1080×1920) + link ilma isikuandmeteta ---------- */
	function link() { return location.origin + keel.L('/liiklusohutus/reaktsioon/') + '?r=' + tulemusMs; }
	function ring(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
	async function pilt() {
		try { await Promise.all([document.fonts.load('700 100px "Barlow Condensed"'), document.fonts.load('700 40px Inter')]); } catch {}
		const cv = document.createElement('canvas'); cv.width = 1080; cv.height = 1920;
		const g = cv.getContext('2d'), D = '"Barlow Condensed", "Arial Narrow", sans-serif', B = 'Inter, system-ui, sans-serif';
		g.fillStyle = '#0a0b0d'; g.fillRect(0, 0, 1080, 1920);
		g.fillStyle = '#fff'; g.font = 'italic 800 64px ' + B; g.fillText('PIDURDUSMAA', 90, 190); const w = g.measureText('PIDURDUSMAA').width; g.fillStyle = '#ffc20e'; g.fillText('.ee', 90 + w, 190);
		g.fillStyle = '#ffc20e'; g.font = '700 44px ' + B; g.fillText(t('MINU REAKTSIOON').toUpperCase(), 90, 360);
		g.fillStyle = '#ffc20e'; g.font = '700 300px ' + D; g.fillText(f2(tulemusMs), 80, 640); const w2 = g.measureText(f2(tulemusMs)).width; g.fillStyle = '#fff'; g.font = '700 120px ' + D; g.fillText(' s', 80 + w2, 640);
		g.fillStyle = '#fff'; g.font = '600 48px ' + B; g.fillText(t('Peatun') + ' ' + kiirus + ' ' + t('km/h pealt') + ' ' + f1(read[0][2].kokku) + ' m', 90, 760);
		g.fillStyle = '#aab1bc'; g.font = '500 36px ' + B; g.fillText(t('märg tee') + ' · ' + (veh.name.length > 34 ? veh.name.slice(0, 33) + '…' : veh.name), 90, 820);
		let y = 960;
		read.forEach(([n, , r, sina]) => {
			g.font = (sina ? '700 ' : '500 ') + '36px ' + B; g.fillStyle = sina ? '#fff' : '#aab1bc';
			g.fillText(n, 90, y); g.textAlign = 'right'; g.fillText(f1(r.kokku) + ' m', 990, y); g.textAlign = 'left';
			g.fillStyle = '#23262d'; ring(g, 90, y + 22, 900, 26, 13); g.fill();
			g.fillStyle = sina ? '#ffc20e' : '#5d636d'; ring(g, 90, y + 22, Math.max(30, (900 * r.kokku) / maxM), 26, 13); g.fill();
			y += 130;
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
	{#if sobra && olek === 'algus'}
		<p class="rk-sober">{t('Sõbra reaktsioon:')} <b>{f2(sobra)} s</b>. {t('Kas oled kiirem?')}</p>
	{/if}

	<button type="button" class="rk-ala" class:punane={olek === 'nyyd'} class:vara={olek === 'vara'} onpointerdown={(e) => { e.preventDefault(); vajuta(); }} aria-live="polite">
		<svg class="rk-auto" viewBox="0 0 200 120" aria-hidden="true">
			<rect x="30" y="20" width="140" height="70" rx="14" fill="#2b3039" />
			<rect x="48" y="30" width="104" height="30" rx="6" fill="#16181d" />
			<rect x="38" y="66" width="34" height="14" rx="4" class="tuli" />
			<rect x="128" y="66" width="34" height="14" rx="4" class="tuli" />
			<rect x="84" y="20" width="32" height="6" rx="3" class="tuli" />
			<rect x="40" y="90" width="28" height="18" rx="4" fill="#0a0b0d" />
			<rect x="132" y="90" width="28" height="18" rx="4" fill="#0a0b0d" />
		</svg>
		<span class="rk-tekst">
			{#if olek === 'algus'}<b>{t('Vajuta, et alustada')}</b><small>{t('Kui eesoleva auto pidurituled süttivad, vajuta kohe. Arvutis ka tühikuklahv.')}</small>
			{:else if olek === 'oota'}<b>{t('Oota…')}</b><small>{t('Vajuta alles siis, kui tuled süttivad')}</small>
			{:else if olek === 'nyyd'}<b>{t('PIDURDA!')}</b>
			{:else if olek === 'vara'}<b>{t('Liiga vara!')}</b><small>{t('Vajuta uuesti, et seda katset korrata')}</small>
			{:else if olek === 'vahe'}<b>{#if viimane >= PIKK * 1000}{t('Ei vajutanud')}{:else}{f2(viimane)}<span class="yh"> s</span>{/if}</b><small>{t('Katse')} {ajad.length} / {KATSEID} · {t('vajuta, et jätkata')}</small>
			{:else}<b>{f2(tulemusMs)}<span class="yh"> s</span></b><small>{hinnang + ' '}{#if sobra}{tulemusMs < sobra ? t('Sõbrast kiirem!') : tulemusMs > sobra ? t('Sõber oli kiirem') + ' (' + f2(sobra) + ' s).' : t('Täpselt sama kiire kui sõber!')}{/if}{' ' + t('Vajuta, et uuesti proovida')}</small>{/if}
		</span>
		<span class="rk-pallid" aria-hidden="true">{#each Array(KATSEID) as _, i}<i class:on={i < ajad.length}></i>{/each}</span>
	</button>

	{#if olek === 'tulemus' && read.length}
		<div class="rk-tul">
			<div class="rk-kiirus" role="group" aria-label={t('Kiirus')}>
				{#each [50, 90, 110] as k (k)}<button type="button" aria-pressed={kiirus === k} onclick={() => (kiirus = k)}>{k} {t('km/h')}</button>{/each}
			</div>
			<p class="rk-pea">{t('Peatumisteekond märjal teel')} · {veh.name}</p>
			<ol class="rk-read">
				{#each read as [nimi, s, r, sina] (nimi)}
					<li class:sina>
						<span class="n">{nimi} <small>{t('reaktsioon')} {f2(s * 1000)} s</small></span>
						<span class="v">{f1(r.kokku)} m</span>
						<span class="t"><span style="width:{(100 * r.kokku) / maxM}%"><i style="width:{(100 * r.reakt) / r.kokku}%"></i></span></span>
					</li>
				{/each}
			</ol>
			<p class="rk-sel">{t('Hele osa ribal = reageerimise ajal sõidad täiskiirusel edasi. Sinu ajale on lisatud 0,2 s jala viimiseks pidurile. Liikluses on oht ootamatu ja päris reaktsioon on tavaliselt pikem kui testis.')}</p>
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
	.rk-sober { background: #fff; border: 1px solid var(--line); border-radius: var(--r); padding: var(--sp-3) var(--sp-4); margin: 0 0 var(--sp-3); text-align: center; }
	.rk-ala { width: 100%; min-height: 360px; border: 0; border-radius: var(--r-lg, 16px); background: var(--ink); color: #fff; cursor: pointer; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--sp-4); padding: var(--sp-6); touch-action: manipulation; user-select: none; -webkit-user-select: none; position: relative; font: inherit; }
	.rk-ala:focus-visible { outline: 3px solid var(--yellow); outline-offset: 3px; }
	.rk-auto { width: min(260px, 70%); }
	.tuli { fill: #4a1d1d; transition: fill 0s; }
	.punane .tuli { fill: #ff2b2b; filter: drop-shadow(0 0 10px #ff2b2b); }
	.punane { background: #1a0707; }
	.vara { background: #2a2107; }
	.rk-tekst { display: flex; flex-direction: column; gap: 6px; text-align: center; }
	.rk-tekst b { font-family: var(--display); font-size: 44px; letter-spacing: 0.02em; text-transform: uppercase; line-height: 1; }
	.punane .rk-tekst b { color: #ff4d4d; }
	.rk-tekst .yh { text-transform: none; }
	.rk-tekst small { color: var(--muted-d); font-size: 15px; max-width: 420px; }
	.rk-pallid { display: flex; gap: 8px; }
	.rk-pallid i { width: 10px; height: 10px; border-radius: 50%; background: #2b3039; }
	.rk-pallid i.on { background: var(--yellow); }
	.rk-tul { background: #fff; border: 1px solid var(--line); border-radius: var(--r-lg, 16px); padding: var(--sp-5); margin-top: var(--sp-4); }
	.rk-kiirus { display: flex; gap: var(--sp-1); background: var(--paper-2); padding: var(--sp-1); border-radius: 10px; width: max-content; max-width: 100%; }
	.rk-kiirus button { border: 0; background: transparent; padding: var(--sp-2) var(--sp-3); border-radius: 7px; font-weight: 600; font-size: 14px; color: var(--muted); cursor: pointer; }
	.rk-kiirus button[aria-pressed='true'] { background: #fff; color: var(--text); box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
	.rk-pea { margin: var(--sp-4) 0 var(--sp-2); font-weight: 700; }
	.rk-read { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--sp-3); }
	.rk-read li { display: grid; grid-template-columns: 1fr auto; gap: 4px var(--sp-3); }
	.rk-read .n { font-size: 14.5px; color: var(--muted); }
	.rk-read .n small { display: block; font-size: 12.5px; }
	.rk-read .sina .n { color: var(--text); font-weight: 700; }
	.rk-read .v { font-weight: 800; font-variant-numeric: tabular-nums; font-size: 18px; }
	.rk-read .sina .v { color: var(--red); }
	.rk-read .t { grid-column: 1 / -1; height: 12px; background: var(--paper-2); border-radius: 6px; overflow: hidden; }
	.rk-read .t > span { display: block; height: 100%; background: #9aa2ae; border-radius: 6px; position: relative; }
	.rk-read .sina .t > span { background: var(--red); }
	.rk-read .t i { position: absolute; left: 0; top: 0; bottom: 0; background: rgba(255, 255, 255, 0.45); }
	.rk-sel { font-size: 13px; color: var(--muted); margin: var(--sp-3) 0 0; line-height: 1.45; }
	.rk-nupud { display: flex; flex-wrap: wrap; gap: var(--sp-2); margin-top: var(--sp-4); }
	@media (max-width: 640px) { .rk-ala { min-height: 300px; } .rk-tekst b { font-size: 36px; } .rk-nupud .btn { flex: 1 1 100%; text-align: center; } }
</style>
