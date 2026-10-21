<script>
	/* REHVIKATALOOG (Tarvo 21.10): vali mõõt ja tüüp, rehvid kohe kaartidena, sorteeri pidurdusmaa või
	   hinna järgi, osta ühe klikiga. Andmed: /api/kataloog ($lib/server/kataloog.js).
	   Ausus: meetrid ainult testitud rehvidel; märgise rehvil märghaarde klass ja müra.
	   Poed võrdselt: kaardil odavaim pakkumine (objektiivne), „Kõik poed“ viib rehvi lehe poodide kasti. */
	import { onMount } from 'svelte';
	import { useT, useLang } from '$lib/i18n.js';
	import { num } from '$lib/util.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;

	/** moodud: EPREL-i mõõdukoodid (['20555R16', …]); moot/tyyp: algväärtus; kinni: mõõt URL-ist (mõõduleht) */
	let { moodud = [], moot: algMoot = '20555R16', tyyp: algTyyp = null, kinni = false } = $props();

	const RE = /^(\d{3})(\d{2})R(\d{2})$/;
	const koodid = moodud.filter((m) => RE.test(m));
	const osad = (m) => { const x = RE.exec(m) || []; return { l: x[1], k: x[2], v: x[3] }; };
	const talv = () => { const k = new Date().getMonth(); return k >= 9 || k <= 2; };

	let moot = $state(RE.test(algMoot) ? algMoot : '20555R16');
	let tyyp = $state(algTyyp || (talv() ? 'naast' : 'suvi'));
	let sort = $state('parim');
	let ainultPoes = $state(true);
	let andmed = $state(null);
	let laeb = $state(false);
	let viga = $state(false);
	let naita = $state(24);
	let ylal = $state(true);
	let ankur, pea;

	const laiused = [...new Set(koodid.map((m) => osad(m).l))].sort();
	const korgused = $derived([...new Set(koodid.filter((m) => osad(m).l === osad(moot).l).map((m) => osad(m).k))].sort());
	const velad = $derived([...new Set(koodid.filter((m) => osad(m).l === osad(moot).l && osad(m).k === osad(moot).k).map((m) => osad(m).v))].sort());

	/* osa vahetus: jää samale mõõdule kui võimalik, muidu lähim olemasolev */
	function vali(osa, val) {
		const o = { ...osad(moot), [osa]: val };
		let m = o.l + o.k + 'R' + o.v;
		if (!koodid.includes(m)) {
			const sobivad = koodid.filter((x) => osad(x).l === o.l && (osa === 'l' || osad(x).k === o.k));
			m = sobivad.find((x) => osad(x).v === o.v) || sobivad[0] || koodid.find((x) => osad(x).l === o.l) || moot;
		}
		moot = m;
	}

	let pariNr = 0;
	async function lae() {
		const nr = ++pariNr;
		laeb = true; viga = false;
		try {
			const r = await fetch('/api/kataloog?moot=' + moot + '&tyyp=' + tyyp, { credentials: 'omit' });
			const d = r.ok ? await r.json() : null;
			if (nr !== pariNr) return;
			andmed = d; viga = !d;
		} catch {
			if (nr === pariNr) viga = true;
		}
		if (nr === pariNr) laeb = false;
	}

	onMount(() => {
		if (!kinni) {
			try {
				const q = new URLSearchParams(location.search);
				const qm = (q.get('moot') || '').toUpperCase().replace(/[^0-9R]/g, '');
				const s = JSON.parse(localStorage.getItem('pm_kataloog') || '{}');
				if (RE.test(qm) && koodid.includes(qm)) moot = qm;
				else if (s.moot && koodid.includes(s.moot)) moot = s.moot;
				if (['suvi', 'lamell', 'naast'].includes(q.get('tyyp'))) tyyp = q.get('tyyp');
				else if (s.tyyp && !algTyyp) tyyp = s.tyyp;
			} catch {}
		}
		/* „Muuda“ nupp ilmub, kui mõõduvalik on ekraanilt üles kadunud */
		const kerimine = () => { if (pea) ylal = pea.getBoundingClientRect().bottom > 0; };
		window.addEventListener('scroll', kerimine, { passive: true });
		kerimine();
		return () => window.removeEventListener('scroll', kerimine);
	});

	$effect(() => {
		moot; tyyp;
		naita = 24;
		lae();
		try { localStorage.setItem('pm_kataloog', JSON.stringify({ moot, tyyp })); } catch {}
	});

	const GJ = { A: 1, B: 2, C: 3, D: 4, E: 5 };
	const hinnaga = $derived(andmed ? andmed.read.filter((r) => r.hind).length : 0);
	const poeFilter = $derived(ainultPoes && hinnaga >= 3);
	/* PARIM VALIK (Tarvo 21.10): hinna ja pidurdusmaa tasakaal. Ainult rehvidel, millel on mõlemad
	   (testitud pidurdusmaa ja hind poes). Mõlemad skaleeritakse selle nimekirja piires 0..1 (parim 0)
	   ja võetakse pooleks kokku: väiksem skoor = parem. */
	const skoor = $derived.by(() => {
		const out = new Map();
		if (!andmed) return out;
		const c = andmed.read.filter((r) => r.m != null && r.hind);
		if (c.length < 3) return out;
		const mm = c.map((r) => r.m), hh = c.map((r) => r.hind.min);
		const [m0, m1, h0, h1] = [Math.min(...mm), Math.max(...mm), Math.min(...hh), Math.max(...hh)];
		for (const r of c) out.set(r.slug, 0.5 * ((r.m - m0) / Math.max(0.1, m1 - m0)) + 0.5 * ((r.hind.min - h0) / Math.max(1, h1 - h0)));
		return out;
	});
	const parimSlug = $derived.by(() => { let b = null, v = 9; for (const [k, x] of skoor) if (x < v) { v = x; b = k; } return b; });
	$effect(() => { if (andmed && !laeb && skoor.size < 3 && sort === 'parim') sort = 'pidurdus'; });
	const read = $derived.by(() => {
		if (!andmed) return [];
		let a = andmed.read.slice();
		if (poeFilter) a = a.filter((r) => r.hind);
		const pid = (r) => [r.m ?? 999, r.testitud ? 0 : 1, (andmed.tyyp !== 'naast' && andmed.tyyp !== 'suvi' && !r.jaa) ? 1 : 0, GJ[r.g] ?? 9, r.db ?? 99];
		const hind = (r) => [r.hind ? r.hind.min : 1e9, r.m ?? 999];
		const parim = (r) => [skoor.has(r.slug) ? skoor.get(r.slug) : 9, ...pid(r)];
		const f = sort === 'hind' ? hind : sort === 'parim' ? parim : pid;
		a.sort((x, y) => { const p = f(x), q = f(y); for (let i = 0; i < p.length; i++) if (p[i] !== q[i]) return p[i] - q[i]; return x.nimi.localeCompare(y.nimi, 'et'); });
		return a;
	});
	const eur = (x) => num(x, 2) + ' €';
	const KAT = { WINTER_NORDIC: 'Põhjamaade lamellrehv', WINTER_CENTRAL: 'Kesk-Euroopa talverehv', WINTER_STUDDED: 'Naastrehv', SUMMER: 'Suverehv' };
	const pretty = (m) => { const o = osad(m); return o.l + '/' + o.k + ' R' + o.v; };
	function yles() { ankur?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
	const pind = (silt) => (String(silt).startsWith('Jää') ? 'jääl' : 'märjal');
</script>

<div class="kat" bind:this={ankur}>
	<div class="kat-pea" bind:this={pea}>
		<div class="kat-r1">
			<div class="kat-moot" role="group" aria-label={t('Rehvimõõt')}>
				<label><span class="sr">{t('Laius')}</span><select value={osad(moot).l} onchange={(e) => vali('l', e.currentTarget.value)}>{#each laiused as l (l)}<option value={l}>{l}</option>{/each}</select></label>
				<span class="kat-sep">/</span>
				<label><span class="sr">{t('Kõrgus')}</span><select value={osad(moot).k} onchange={(e) => vali('k', e.currentTarget.value)}>{#each korgused as k (k)}<option value={k}>{k}</option>{/each}</select></label>
				<label><span class="sr">{t('Velg')}</span><select value={osad(moot).v} onchange={(e) => vali('v', e.currentTarget.value)}>{#each velad as v (v)}<option value={v}>R{v}</option>{/each}</select></label>
			</div>
			<div class="kseg" role="group" aria-label={t('Rehvi liik')}>
				<!-- vene keeles on täisnimed liiga pikad nupule: lühike silt -->
				{#each [['naast', 'Naastrehvid', 'Шипы'], ['lamell', 'Lamellrehvid', 'Липучки'], ['suvi', 'Suverehvid', 'Летние']] as [k, n, ru] (k)}
					<button type="button" class:on={tyyp === k} aria-pressed={tyyp === k} onclick={() => (tyyp = k)}>{keel.lang === 'ru' ? ru : t(n)}</button>
				{/each}
			</div>
		</div>
		<div class="kat-r2">
			<div class="kseg" role="group" aria-label={t('Sorteeri')}>
				{#if skoor.size >= 3}<button type="button" class:on={sort === 'parim'} aria-pressed={sort === 'parim'} onclick={() => (sort = 'parim')} title={t('Pool kaalu pidurdusmaal, pool hinnal')}>{t('Parim valik')}</button>{/if}
				<button type="button" class:on={sort === 'pidurdus'} aria-pressed={sort === 'pidurdus'} onclick={() => (sort = 'pidurdus')}>{t('Lühim pidurdus')}</button>
				<button type="button" class:on={sort === 'hind'} aria-pressed={sort === 'hind'} onclick={() => (sort = 'hind')}>{t('Odavaim')}</button>
			</div>
			<div class="kat-paremal">
				{#if hinnaga >= 3}
					<label class="lyliti"><input type="checkbox" bind:checked={ainultPoes} /><span aria-hidden="true"></span>{t('Ainult müügil')}</label>
				{/if}
				<span class="kat-arv">{#if andmed}{read.length} {t('rehvi')}{/if}</span>
			</div>
		</div>
	</div>

	<div class="kat-list" aria-busy={laeb}>
		{#if viga}
			<p class="kat-tyhi">{t('Rehve ei õnnestunud laadida. Proovi uuesti.')} <button type="button" class="btn" onclick={lae}>{t('Proovi uuesti')}</button></p>
		{:else if andmed && !read.length && !laeb}
			<p class="kat-tyhi">{t('Selles mõõdus ei ole seda tüüpi rehve andmebaasis.')}</p>
		{/if}
		{#each read.slice(0, naita) as r (r.slug)}
			<article class="kk" class:parim={r.slug === parimSlug}>
				{#if r.slug === parimSlug}<span class="kk-silt">★ {t('Parim valik')}</span>{/if}
				<a class="kk-pilt" href={r.url ? L(r.url) : undefined} tabindex="-1" aria-hidden="true">
					{#if r.pilt}<img src={'/api/pilt/' + r.slug} alt="" loading="lazy" decoding="async" onerror={(e) => (e.currentTarget.parentElement.classList.add('tyhi'))} />{/if}
				</a>
				<div class="kk-info">
					<span class="kk-mark">{r.mark}</span>
					<h3>{#if r.url}<a href={L(r.url)}>{r.nimi.replace(new RegExp('^' + r.mark.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*', 'i'), '') || r.nimi}</a>{:else}{r.nimi}{/if}</h3>
					<span class="kk-meta">{pretty(andmed.moot)} · {t(KAT[r.kat] || '')}{#if r.testitud}{' · '}<span class="kk-test">✓&nbsp;{t('testitud')}</span>{/if}</span>
				</div>
				<div class="kk-num" title={andmed.auto ? t('Pidurdusmaa {silt}, {auto}, ilma reaktsiooniajata', { silt: t(andmed.silt), auto: andmed.auto }) : ''}>
					{#if r.m != null}
						<b>{num(r.m)} m</b>
						<span>{t('pidurdus ' + pind(andmed.silt))} {t(andmed.silt).replace(/^\S+\s/, '')}</span>
					{:else if r.g}
						<b class="kk-g">{r.g}</b>
						<span>{t('märghaare')}{r.db ? ' · ' + r.db + ' dB' : ''}{r.jaa ? ' · ❄' : ''}</span>
					{/if}
				</div>
				<div class="kk-ost">
					{#if r.hind}
						<span class="kk-hind">{r.hind.umbes ? t('u') + ' ' : ''}{eur(r.hind.min)}</span>
						<span class="kk-4">{t('4 tk')} {eur(r.hind.min * 4)}</span>
						<a class="kk-osta" href={r.hind.url} target="_blank" rel="nofollow sponsored noopener" data-pood={r.hind.pood} data-rehv={r.nimi}>{t('Osta')} · {r.hind.pood}</a>
						<span class="kk-poed">{#if r.hind.laos}<i></i>{t('laos')}{' · '}{/if}{#if r.url && r.hind.poode > 1}<a href={L(r.url) + '#kus-osta'}>{t('{n} poodi', { n: r.hind.poode })}</a>{:else}{r.hind.poode === 1 ? t('1 pood') : t('{n} poodi', { n: r.hind.poode })}{/if}</span>
					{:else if r.url}
						<a class="kk-osta kk-vaata" href={L(r.url)}>{t('Vaata rehvi')}</a>
					{/if}
				</div>
			</article>
		{/each}
		{#if read.length > naita}
			<button type="button" class="kat-veel" onclick={() => (naita += 24)}>{t('Näita veel')} ({read.length - naita})</button>
		{/if}
	</div>
</div>

{#if !ylal}
	<button type="button" class="kat-fab" onclick={yles}>⚙ {pretty(moot)} · {t('Muuda')}</button>
{/if}

<style>
	.kat { scroll-margin-top: 80px; }
	.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
	/* juhtpaneel: rahulik valge kast, segmentnupud (iOS-i stiilis) */
	.kat-pea { background: var(--paper); border: 1px solid var(--line); border-radius: 20px; padding: 14px; display: grid; gap: 12px; }
	.kat-r1, .kat-r2 { display: flex; flex-wrap: wrap; gap: 10px 14px; align-items: center; justify-content: space-between; }
	.kat-moot { display: flex; align-items: center; background: var(--paper-2); border-radius: 12px; padding: 4px; }
	.kat-moot select { appearance: none; -webkit-appearance: none; border: 0; background: transparent; font: 700 18px var(--body); color: var(--text); padding: 8px 10px; border-radius: 9px; cursor: pointer; }
	.kat-moot select:hover, .kat-moot select:focus-visible { background: var(--paper); }
	.kat-sep { color: var(--muted); font-weight: 600; }
	.kseg { display: inline-grid; grid-auto-flow: column; grid-auto-columns: 1fr; background: var(--paper-2); border-radius: 12px; padding: 4px; gap: 2px; }
	.kseg button { border: 0; background: transparent; border-radius: 9px; padding: 9px 14px; font: 600 14.5px var(--body); color: var(--muted); cursor: pointer; white-space: nowrap; }
	.kseg button.on { background: var(--paper); color: var(--text); box-shadow: 0 1px 3px rgba(10, 11, 13, 0.12); }
	.kat-paremal { display: flex; align-items: center; gap: 16px; margin-left: auto; }
	.lyliti { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; cursor: pointer; color: var(--text); }
	.lyliti input { position: absolute; opacity: 0; }
	.lyliti span { width: 36px; height: 22px; border-radius: 11px; background: var(--line); position: relative; transition: background 0.15s; }
	.lyliti span::after { content: ''; position: absolute; top: 2px; left: 2px; width: 18px; height: 18px; border-radius: 50%; background: #fff; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.25); transition: transform 0.15s; }
	.lyliti input:checked + span { background: var(--good); }
	.lyliti input:checked + span::after { transform: translateX(14px); }
	.lyliti input:focus-visible + span { outline: 2px solid var(--yellow); outline-offset: 2px; }
	.kat-arv { color: var(--muted); font-size: 14px; }

	.kat-list { display: grid; gap: 10px; margin-top: 14px; transition: opacity 0.15s; }
	.kat-list[aria-busy='true'] { opacity: 0.5; }
	.kat-tyhi { padding: var(--sp-6); text-align: center; color: var(--muted); background: var(--paper); border-radius: 20px; }

	/* rehvikaart */
	.kk { position: relative; display: grid; grid-template-columns: 92px 1fr 150px 210px; gap: 20px; align-items: center; background: var(--paper); border: 1px solid var(--line); border-radius: 20px; padding: 16px 20px; transition: box-shadow 0.15s, border-color 0.15s; }
	.kk:hover { border-color: #d3d7de; box-shadow: 0 6px 24px rgba(10, 11, 13, 0.06); }
	.kk.parim { border-color: var(--yellow); box-shadow: 0 0 0 1px var(--yellow) inset; }
	.kk-silt { position: absolute; top: -10px; left: 18px; background: var(--yellow); color: var(--yellow-ink); font: 700 12px var(--body); letter-spacing: 0.02em; padding: 3px 10px; border-radius: 999px; }
	.kk-pilt { width: 92px; height: 92px; border-radius: 14px; background: var(--paper-2); display: grid; place-items: center; overflow: hidden; }
	.kk-pilt img { width: 84%; height: 84%; object-fit: contain; mix-blend-mode: multiply; }
	.kk-pilt:empty, .kk-pilt.tyhi { background: var(--paper-2) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Ccircle cx='20' cy='20' r='15' fill='none' stroke='%23c4c9d1' stroke-width='5'/%3E%3Ccircle cx='20' cy='20' r='5' fill='%23c4c9d1'/%3E%3C/svg%3E") no-repeat center / 38px; }
	.kk-pilt.tyhi img { display: none; }
	.kk-info { min-width: 0; display: grid; gap: 3px; }
	.kk-mark { font-size: 11.5px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
	.kk h3 { margin: 0; font: 650 19px/1.2 var(--body); letter-spacing: -0.01em; }
	.kk h3 a { color: var(--text); text-decoration: none; }
	.kk h3 a:hover { text-decoration: underline; text-underline-offset: 3px; }
	.kk-meta { font-size: 13.5px; color: var(--muted); }
	.kk-test { color: var(--tested); font-weight: 600; }
	.kk-num { display: grid; gap: 2px; }
	.kk-num b { font: 800 24px/1 var(--body); letter-spacing: -0.02em; }
	.kk-num b.kk-g { display: inline-grid; place-items: center; width: 30px; height: 30px; border-radius: 8px; background: var(--paper-2); font-size: 17px; }
	.kk-num span { font-size: 12.5px; color: var(--muted); }
	.kk-ost { display: grid; justify-items: end; gap: 3px; text-align: right; }
	.kk-hind { font: 800 24px/1 var(--body); letter-spacing: -0.02em; }
	.kk-4 { font-size: 12.5px; color: var(--muted); }
	.kk-osta { margin-top: 8px; display: inline-flex; align-items: center; justify-content: center; gap: 6px; background: var(--ink); color: #fff; text-decoration: none; font: 600 14.5px var(--body); padding: 11px 18px; border-radius: 12px; white-space: nowrap; max-width: 100%; overflow: hidden; text-overflow: ellipsis; }
	.kk-osta::after { content: '→'; }
	.kk-osta:hover { background: #2a2e36; }
	.kk.parim .kk-osta { background: var(--yellow); color: var(--yellow-ink); }
	.kk-vaata { background: var(--paper-2); color: var(--text); }
	.kk-vaata:hover { background: var(--paper-3); }
	.kk-poed { font-size: 12.5px; color: var(--muted); }
	.kk-poed i { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: var(--good); margin-right: 5px; vertical-align: 1px; }
	.kk-poed a { color: var(--muted); }
	.kat-veel { justify-self: center; margin-top: 10px; border: 1px solid var(--line); background: var(--paper); border-radius: 12px; padding: 12px 22px; font: 600 15px var(--body); cursor: pointer; }
	.kat-fab { position: fixed; right: 16px; bottom: 84px; z-index: 40; border: 0; border-radius: 999px; padding: 12px 18px; background: var(--ink); color: #fff; font: 600 15px var(--body); box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25); cursor: pointer; }
	@media (min-width: 900px) { .kat-fab { bottom: 24px; } }
	@media (max-width: 860px) {
		.kk { grid-template-columns: 76px 1fr; gap: 10px 14px; padding: 16px; }
		.kk-pilt { width: 76px; height: 76px; grid-row: 1 / span 2; align-self: start; }
		.kk-num { grid-column: 2; grid-row: 2; grid-template-columns: auto 1fr; align-items: baseline; column-gap: 8px; }
		.kk-ost { grid-column: 1 / -1; grid-template-columns: auto 1fr; justify-items: start; text-align: left; align-items: baseline; column-gap: 10px; padding-top: 12px; border-top: 1px solid var(--line); }
		.kk-4 { justify-self: start; }
		.kk-osta { grid-column: 1 / -1; width: 100%; }
		.kk-poed { grid-column: 1 / -1; }
	}
	@media (max-width: 640px) {
		.kat-r1, .kat-r2 { flex-direction: column; align-items: stretch; }
		.kat-moot { justify-content: center; }
		.kseg { display: grid; }
		.kseg button { padding: 9px 4px; font-size: 14px; }
		.kat-paremal { margin-left: 0; justify-content: space-between; }
		.kk h3 { font-size: 17px; }
		.kk-num b { font-size: 20px; }
	}
</style>
