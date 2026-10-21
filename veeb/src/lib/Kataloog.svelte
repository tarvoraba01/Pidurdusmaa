<script>
	/* REHVIKATALOOG (Tarvo 21.10): vali mõõt ja tüüp, rehvid kohe kaartidena, sorteeri pidurdusmaa või
	   hinna järgi, osta ühe klikiga. Andmed: /api/kataloog ($lib/server/kataloog.js).
	   Ausus: meetrid ainult testitud rehvidel; märgise rehvil märghaarde klass ja müra.
	   Poed võrdselt: kaardil odavaim pakkumine (objektiivne), „Kõik poed“ viib rehvi lehe poodide kasti. */
	import { onMount } from 'svelte';
	import { useT, useLang } from '$lib/i18n.js';
	import { num } from '$lib/util.js';
	import TyreArt from '$lib/TyreArt.svelte';
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
	let sort = $state('pidurdus');
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
	const read = $derived.by(() => {
		if (!andmed) return [];
		let a = andmed.read.slice();
		if (poeFilter) a = a.filter((r) => r.hind);
		const pid = (r) => [r.m ?? 999, r.testitud ? 0 : 1, (andmed.tyyp !== 'naast' && andmed.tyyp !== 'suvi' && !r.jaa) ? 1 : 0, GJ[r.g] ?? 9, r.db ?? 99];
		const hind = (r) => [r.hind ? r.hind.min : 1e9, r.m ?? 999];
		const f = sort === 'hind' ? hind : pid;
		a.sort((x, y) => { const p = f(x), q = f(y); for (let i = 0; i < p.length; i++) if (p[i] !== q[i]) return p[i] - q[i]; return x.nimi.localeCompare(y.nimi, 'et'); });
		return a;
	});
	const eur = (x) => num(x, 2) + ' €';
	const KAT = { WINTER_NORDIC: 'Põhjamaade lamellrehv', WINTER_CENTRAL: 'Kesk-Euroopa talverehv', WINTER_STUDDED: 'Naastrehv', SUMMER: 'Suverehv' };
	const pretty = (m) => { const o = osad(m); return o.l + '/' + o.k + ' R' + o.v; };
	function yles() { ankur?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
	function track(e, v) { try { window.PM_TRACK && window.PM_TRACK(e, v); } catch {} }
</script>

<div class="kat" bind:this={ankur}>
	<div class="kat-pea" bind:this={pea}>
		<div class="kat-moot">
			<span class="kat-silt">{t('Rehvimõõt')}</span>
			<div class="kat-sel">
				<label><span>{t('Laius')}</span><select value={osad(moot).l} onchange={(e) => vali('l', e.currentTarget.value)}>{#each laiused as l (l)}<option value={l}>{l}</option>{/each}</select></label>
				<label><span>{t('Kõrgus')}</span><select value={osad(moot).k} onchange={(e) => vali('k', e.currentTarget.value)}>{#each korgused as k (k)}<option value={k}>{k}</option>{/each}</select></label>
				<label><span>{t('Velg')}</span><select value={osad(moot).v} onchange={(e) => vali('v', e.currentTarget.value)}>{#each velad as v (v)}<option value={v}>R{v}</option>{/each}</select></label>
			</div>
		</div>
		<div class="kat-tyyp" role="group" aria-label={t('Rehvi liik')}>
			<!-- vene keeles on täisnimed liiga pikad nupule: lühike silt -->
			{#each [['naast', 'Naastrehvid', 'Шипы'], ['lamell', 'Lamellrehvid', 'Липучки'], ['suvi', 'Suverehvid', 'Летние']] as [k, n, ru] (k)}
				<button type="button" class:on={tyyp === k} aria-pressed={tyyp === k} onclick={() => (tyyp = k)}>{keel.lang === 'ru' ? ru : t(n)}</button>
			{/each}
		</div>
		<div class="kat-rida">
			<label class="kat-sort"><span>{t('Sorteeri')}</span>
				<select bind:value={sort}>
					<option value="pidurdus">{t('Lühim pidurdusmaa')}</option>
					<option value="hind">{t('Odavamad eespool')}</option>
				</select>
			</label>
			{#if hinnaga >= 3}
				<label class="kat-chk"><input type="checkbox" bind:checked={ainultPoes} /> {t('Ainult poodides müügil')}</label>
			{/if}
			<span class="kat-arv">{#if andmed}{read.length} {t('rehvi')}{/if}</span>
		</div>
	</div>

	{#if andmed && andmed.read.length}
		<p class="kat-info">
			{#if andmed.auto}{t('Pidurdusmaa ({silt}, {auto}, ilma reaktsiooniajata) on testitud rehvidel. Teistel on EL-i märgise märghaarde klass, A on parim.', { silt: t(andmed.silt), auto: andmed.auto })}{/if}
		</p>
	{/if}

	<div class="kat-list" aria-busy={laeb}>
		{#if viga}
			<p class="kat-tyhi">{t('Rehve ei õnnestunud laadida. Proovi uuesti.')} <button type="button" class="btn" onclick={lae}>{t('Proovi uuesti')}</button></p>
		{:else if andmed && !read.length && !laeb}
			<p class="kat-tyhi">{t('Selles mõõdus ei ole seda tüüpi rehve andmebaasis.')}</p>
		{/if}
		{#each read.slice(0, naita) as r (r.slug)}
			<article class="kk">
				<a class="kk-pilt" href={r.url ? L(r.url) : undefined} tabindex="-1" aria-hidden="true">
					{#if r.pilt}<img src={'/api/pilt/' + r.slug} alt="" loading="lazy" decoding="async" onerror={(e) => (e.currentTarget.style.display = 'none')} />{:else}<span class="kk-art"><TyreArt /></span>{/if}
				</a>
				<div class="kk-info">
					<span class="kk-mark">{r.mark}</span>
					<h3>{#if r.url}<a href={L(r.url)}>{r.nimi.replace(new RegExp('^' + r.mark.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*', 'i'), '') || r.nimi}</a>{:else}{r.nimi}{/if}</h3>
					<span class="kk-moot">{pretty(andmed.moot)} · {t(KAT[r.kat] || '')}</span>
					<div class="kk-margid">
						{#if r.m != null}<span class="kk-pid" title={t(andmed.silt)}>{t(andmed.silt)} <b>{num(r.m)} m</b></span>{/if}
						{#if r.g}<span class="kk-g" title={t('EL-i märgise märghaarde klass')}>{t('Märghaare')} <b>{r.g}</b></span>{/if}
						{#if r.db}<span class="kk-g">{r.db} dB</span>{/if}
						{#if r.jaa}<span class="kk-g" title={t('Jäämärgis (Põhjamaade talverehv)')}>❄ {t('jää')}</span>{/if}
						{#if r.testitud}<span class="kk-test">✓ {t('testitud')}</span>{/if}
					</div>
				</div>
				<div class="kk-ost">
					{#if r.hind}
						<span class="kk-hind">{r.hind.umbes ? t('u') + ' ' : ''}{eur(r.hind.min)}</span>
						<span class="kk-4">{t('4 tk')} {eur(r.hind.min * 4)}</span>
						<span class="kk-poed">{r.hind.poode === 1 ? t('1 pood') : t('{n} poodi', { n: r.hind.poode })}{r.hind.laos ? ' · ' + t('laos') : ''}</span>
						<a class="btn yel kk-osta" href={r.hind.url} target="_blank" rel="nofollow sponsored noopener" data-pood={r.hind.pood} data-rehv={r.nimi}>{t('Osta')} · {r.hind.pood} →</a>
						{#if r.url && r.hind.poode > 1}<a class="kk-koik" href={L(r.url) + '#kus-osta'}>{t('Võrdle poode')}</a>{/if}
					{:else if r.url}
						<a class="btn kk-osta" href={L(r.url)}>{t('Vaata rehvi')} →</a>
					{/if}
				</div>
			</article>
		{/each}
		{#if read.length > naita}
			<button type="button" class="btn kat-veel" onclick={() => (naita += 24)}>{t('Näita veel')} ({read.length - naita})</button>
		{/if}
	</div>
</div>

{#if !ylal}
	<button type="button" class="kat-fab" onclick={yles}>⚙ {pretty(moot)} · {t('Muuda')}</button>
{/if}

<style>
	.kat { scroll-margin-top: 80px; }
	.kat-pea { background: var(--paper); border: 1px solid var(--line); border-radius: var(--r-lg); padding: var(--sp-4); display: grid; gap: var(--sp-3); box-shadow: var(--shadow); }
	.kat-silt { font-weight: 700; font-size: 14px; }
	.kat-moot { display: grid; gap: var(--sp-2); }
	.kat-sel { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--sp-2); }
	.kat-sel label, .kat-sort { display: grid; gap: 2px; font-size: 12px; color: var(--muted); }
	select { appearance: none; -webkit-appearance: none; width: 100%; border: 1px solid var(--line); border-radius: var(--r); padding: 10px 30px 10px 12px; font: 600 16px var(--body); color: var(--text); background: var(--paper) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%23565e6b' stroke-width='2'/%3E%3C/svg%3E") no-repeat right 12px center; }
	.kat-tyyp { display: grid; grid-template-columns: repeat(3, auto); justify-content: start; gap: var(--sp-2); }
	.kat-tyyp button { border: 1px solid var(--line); background: var(--paper); border-radius: 999px; padding: 8px 16px; font: 600 15px var(--body); color: var(--text); cursor: pointer; }
	.kat-tyyp button.on { background: var(--ink); border-color: var(--ink); color: #fff; }
	.kat-rida { display: flex; align-items: end; gap: var(--sp-3); flex-wrap: wrap; }
	.kat-sort { min-width: 210px; }
	.kat-chk { display: flex; align-items: center; gap: 6px; font-size: 14px; padding-bottom: 10px; cursor: pointer; }
	.kat-arv { margin-left: auto; color: var(--muted); font-size: 14px; padding-bottom: 10px; }
	.kat-info { color: var(--muted); font-size: 13px; margin: var(--sp-3) 2px; line-height: 1.45; }
	.kat-list { display: grid; gap: var(--sp-2); transition: opacity 0.15s; }
	.kat-list[aria-busy='true'] { opacity: 0.55; }
	.kat-tyhi { padding: var(--sp-6); text-align: center; color: var(--muted); background: var(--paper); border-radius: var(--r-lg); }
	.kk { display: grid; grid-template-columns: 76px 1fr auto; gap: var(--sp-4); align-items: center; background: var(--paper); border: 1px solid var(--line); border-radius: var(--r-lg); padding: var(--sp-3) var(--sp-4); }
	.kk-pilt { width: 76px; height: 76px; display: grid; place-items: center; }
	.kk-pilt img { max-width: 76px; max-height: 76px; object-fit: contain; }
	.kk-art { width: 62px; height: 62px; display: block; opacity: 0.85; }
	.kk-info { min-width: 0; display: grid; gap: 2px; }
	.kk-mark { font-size: 12px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
	.kk h3 { margin: 0; font: 700 18px/1.2 var(--body); }
	.kk h3 a { color: var(--text); text-decoration: none; }
	.kk h3 a:hover { text-decoration: underline; }
	.kk-moot { font-size: 13px; color: var(--muted); }
	.kk-margid { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
	.kk-pid { background: var(--yellow-soft); border: 1px solid #f3dc8f; color: var(--yellow-ink); border-radius: 999px; padding: 2px 10px; font-size: 13px; }
	.kk-g { background: var(--paper-2); border-radius: 999px; padding: 2px 10px; font-size: 13px; color: var(--text); }
	.kk-test { color: var(--tested); font-size: 13px; font-weight: 600; padding: 2px 4px; }
	.kk-ost { display: grid; justify-items: end; gap: 2px; min-width: 190px; text-align: right; }
	.kk-hind { font: 800 24px/1 var(--body); }
	.kk-4 { font-size: 13px; color: var(--muted); }
	.kk-poed { font-size: 13px; color: var(--tested); }
	.kk-osta { margin-top: 6px; white-space: nowrap; }
	.kk-koik { font-size: 13px; color: var(--muted); }
	.kat-veel { justify-self: center; margin-top: var(--sp-3); }
	.kat-fab { position: fixed; right: 16px; bottom: 84px; z-index: 40; border: 0; border-radius: 999px; padding: 12px 18px; background: var(--yellow); color: var(--yellow-ink); font: 700 15px var(--body); box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25); cursor: pointer; }
	@media (min-width: 900px) { .kat-pea { grid-template-columns: auto 1fr; align-items: end; } .kat-rida { grid-column: 1 / -1; } .kat-sel { grid-template-columns: repeat(3, 110px); } .kat-fab { bottom: 24px; } }
	@media (max-width: 640px) {
		.kat-tyyp { grid-template-columns: repeat(3, 1fr); }
		.kat-tyyp button { padding: 8px 4px; font-size: 14px; }
		.kk { grid-template-columns: 64px 1fr; gap: var(--sp-3); padding: var(--sp-3); }
		.kk-pilt { width: 64px; height: 64px; }
		.kk-ost { grid-column: 1 / -1; grid-template-columns: auto 1fr; justify-items: start; text-align: left; align-items: baseline; column-gap: var(--sp-2); min-width: 0; }
		.kk-hind { font-size: 22px; }
		.kk-poed { grid-column: 1 / -1; }
		.kk-osta { grid-column: 1 / -1; width: 100%; text-align: center; }
		.kk-koik { grid-column: 1 / -1; justify-self: center; }
		.kat-arv { margin-left: 0; }
	}
</style>
