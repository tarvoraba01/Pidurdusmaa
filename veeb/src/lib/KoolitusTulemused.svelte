<script>
	/* Õpetaja vaade: grupi tulemused enne/pärast. Kood ja võti tulevad aadressi räsist
	   (#kood=…&voti=…), räsi serverisse ei jõua; võti läheb päringu päises. */
	import { onMount } from 'svelte';
	import { TEEMAD, leiaKysimus } from '$lib/koolitus/kysimused.js';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	let TOLGE = $state({});

	let kood = $state('');
	let voti = '';
	let andmed = $state(null);
	let viga = $state('');
	let laeb = $state(false);
	let minu = $state([]);
	const teemaNimi = (id) => t((TEEMAD.find((x) => x[0] === id) || [, id])[1]);
	const kysimus = (id) => {
		const q = leiaKysimus(id);
		const x = q && TOLGE[id];
		return x ? { ...q, k: x[0], v: x[1] } : q;
	};

	async function lae() {
		if (!kood || !voti) return;
		laeb = true;
		viga = '';
		try {
			const r = await fetch('/api/koolitus?tulemused=1&kood=' + encodeURIComponent(kood), { headers: { Authorization: 'Bearer ' + voti } });
			const j = await r.json().catch(() => null);
			if (!j?.ok) viga = r.status === 401 ? t('See link ei kehti. Kontrolli, et kopeerisid kogu lingi.') : j?.viga ? t(j.viga) : t('Tulemusi ei saanud laadida.');
			else andmed = j;
		} catch {
			viga = t('Ühendus katkes. Proovi uuesti.');
		} finally {
			laeb = false;
		}
	}
	onMount(() => {
		if (keel.lang === 'ru') import('$lib/koolitus/ru.js').then((m) => (TOLGE = m.default)).catch(() => {});
		try {
			const h = new URLSearchParams(location.hash.slice(1));
			kood = String(h.get('kood') || '').toUpperCase();
			voti = String(h.get('voti') || '');
			minu = JSON.parse(localStorage.getItem('pm-koolitus-minu') || '[]');
		} catch {}
		lae();
	});
	const mine = (m) => { location.hash = 'kood=' + m.kood + '&voti=' + m.voti; kood = m.kood; voti = m.voti; andmed = null; lae(); };
</script>

<div class="kt">
	{#if !kood}
		<div class="kt-kaart">
			<p>{t('Ava see leht lingiga, mille said testi loomisel.')}</p>
			{#if minu.length}
				<p><b>{t('Selles brauseris loodud testid:')}</b></p>
				<ul class="kt-minu">{#each minu as m (m.kood)}<li><button type="button" class="linkbtn" onclick={() => mine(m)}>{m.nimi} · {m.kood}</button></li>{/each}</ul>
			{/if}
			<a class="btn yel" href={keel.L('/liiklusohutus/koolitus/')}>{t('Loo uus test →')}</a>
		</div>
	{:else if viga}
		<div class="kt-kaart"><p class="kt-viga">{viga}</p></div>
	{:else if !andmed}
		<div class="kt-kaart"><p>{t('Laen tulemusi…')}</p></div>
	{:else}
		<div class="kt-kaart">
			<p class="kt-etapp">{t('Grupp')} · {andmed.kood}</p>
			<h2>{andmed.nimi}</h2>
			{#if !andmed.osalejaid.eel}
				<p>{t('Keegi pole veel testi teinud. Õpilaste link:')} <b>pidurdusmaa.ee{keel.L('/liiklusohutus/koolitus/')}?kood={andmed.kood}</b></p>
			{:else}
				<div class="kt-ep">
					<div><span>{t('Enne')}</span><b>{andmed.oigeid.eel ?? '–'}%</b><small>{t('{n} õpilast', { n: andmed.osalejaid.eel })}</small></div>
					<i aria-hidden="true">→</i>
					<div class:hea={andmed.oigeid.jarel > andmed.oigeid.eel}><span>{t('Pärast')}</span><b>{andmed.oigeid.jarel ?? '–'}%</b><small>{t('{n} õpilast', { n: andmed.osalejaid.jarel })}</small></div>
				</div>
				<p class="kt-vaike">{t('Õigete vastuste osa. Järeltest küsib samu teadmisi teises olukorras.')}</p>
			{/if}
			<div class="kt-nupud">
				<button type="button" class="btn" disabled={laeb} onclick={lae}>{laeb ? t('Laen…') : t('Värskenda')}</button>
				<button type="button" class="btn" onclick={() => window.print()}>{t('Prindi või salvesta PDF')}</button>
			</div>
			<p class="kt-vaike kt-printaeg">{t('Seisuga')} {new Date().toLocaleString(keel.lang === 'ru' ? 'ru-RU' : 'et-EE', { dateStyle: 'short', timeStyle: 'short' })}</p>
		</div>

		{#if andmed.opilased?.length}
			<div class="kt-kaart">
				<h3>{t('Õpilased')}</h3>
				<p class="kt-vaike">{t('Iga läbimine eraldi. Vajuta reale, et näha, milles õpilane eksis.')}</p>
				<div class="kt-op kt-op-pea" aria-hidden="true"><span>{t('Õpilane')}</span><span>{t('Enne')}</span><span>{t('Pärast')}</span><span>{t('Muutus')}</span></div>
				{#each andmed.opilased as o, nr (nr)}
					{@const e = o.eel[1] ? Math.round((o.eel[0] / o.eel[1]) * 100) : null}
					{@const j = o.jarel[1] ? Math.round((o.jarel[0] / o.jarel[1]) * 100) : null}
					<details class="kt-opd">
						<summary class="kt-op">
							<span class="kt-opn">{o.nimi || t('Õpilane') + ' ' + (nr + 1)}</span>
							<span>{o.eel[1] ? o.eel[0] + '/' + o.eel[1] : '–'}</span>
							<span>{o.jarel[1] ? o.jarel[0] + '/' + o.jarel[1] : t('pooleli')}</span>
							<span class:kt-plus={e !== null && j !== null && j > e} class:kt-miinus={e !== null && j !== null && j < e}>{e !== null && j !== null ? (j - e > 0 ? '+' : '') + (j - e) + ' ' + t('p.p.') : ''}</span>
						</summary>
						<div class="kt-valed">
							{#each [['eel', t('Eeltestis eksis')], ['jarel', t('Järeltestis eksis')]] as [et, pealk] (et)}
								{#if o.valed[et].length}
									<p class="kt-vaike"><b>{pealk}:</b></p>
									<ul>{#each o.valed[et] as id (id)}{@const q = kysimus(id)}{#if q}<li>{q.k} <span class="kt-vaike">{t('Õige:')} {q.v[q.o]}</span></li>{/if}{/each}</ul>
								{/if}
							{/each}
							{#if !o.valed.eel.length && !o.valed.jarel.length}<p class="kt-vaike">{t('Kõik vastused õiged.')}</p>{/if}
						</div>
					</details>
				{/each}
			</div>
		{/if}

		{#if andmed.teemad.length}
			<div class="kt-kaart">
				<h3>{t('Teemade kaupa')}</h3>
				<div class="kt-legend"><span class="e"></span>{t('enne')} <span class="j"></span>{t('pärast')}</div>
				{#each andmed.teemad as tm (tm.id)}
					<div class="kt-teema">
						<p>{teemaNimi(tm.id)}</p>
						<div class="kt-riba"><i class="e" style="width:{tm.eel ?? 0}%"></i><b>{tm.eel ?? '–'}%</b></div>
						<div class="kt-riba"><i class="j" style="width:{tm.jarel ?? 0}%"></i><b>{tm.jarel ?? '–'}%</b></div>
					</div>
				{/each}
			</div>
		{/if}

		{#if andmed.kysimused.length}
			<div class="kt-kaart">
				<h3>{t('Mis jäi segaseks')}</h3>
				<p class="kt-vaike">{t('Iga rida on üks teadmine: eeltestis üks küsimus, järeltestis sama asi teisiti küsitud. Ülal need, mis jäid ka pärast selgitust segaseks. Nendest tasub tunnis rääkida.')}</p>
				<ol class="kt-ras">
					{#each andmed.kysimused as k (k.id)}
						{@const q = kysimus(k.id)}
						{#if q}<li><p><b>{t('enne')} {k.eel ?? '–'}% → {t('pärast')} {k.jarel ?? '–'}%</b> <span class="kt-vaike">{t('õigeid')} · {t('{n} õpilast', { n: k.vastajaid })}</span></p><p>{q.k}</p><p class="kt-vaike">{t('Õige:')} {q.v[q.o]}</p></li>{/if}
					{/each}
				</ol>
			</div>
		{/if}
	{/if}
</div>

<style>
	.kt { max-width: 760px; margin: 0 auto; }
	.kt-kaart { background: #fff; border: 1px solid var(--line); border-radius: 16px; padding: var(--sp-6); margin-bottom: var(--sp-4); }
	.kt-kaart h2 { font-family: var(--display); font-size: 30px; line-height: 1.05; margin: 0 0 var(--sp-3); }
	.kt-kaart h3 { margin: 0 0 var(--sp-3); }
	.kt-etapp { font-size: 13px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; margin: 0 0 var(--sp-2); }
	.kt-ep { display: flex; align-items: center; gap: var(--sp-6); margin: var(--sp-4) 0 var(--sp-2); }
	.kt-ep div { display: grid; }
	.kt-ep span { font-size: 13px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
	.kt-ep b { font-family: var(--display); font-size: 56px; line-height: 1; }
	.kt-ep small { color: var(--muted); }
	.kt-ep .hea b { color: #1f9d55; }
	.kt-ep i { font-style: normal; font-size: 30px; color: var(--muted); }
	.kt-vaike { color: var(--muted); font-size: 14px; }
	.kt-viga { color: #b4471a; font-weight: 600; }
	.kt-legend { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--muted); margin-bottom: var(--sp-3); }
	.kt-legend span { width: 12px; height: 12px; border-radius: 3px; display: inline-block; margin-left: 8px; }
	.kt-legend .e, .kt-riba .e { background: #c4c9d1; }
	.kt-legend .j, .kt-riba .j { background: var(--yellow); }
	.kt-teema { margin-bottom: var(--sp-3); }
	.kt-teema p { margin: 0 0 4px; font-weight: 600; font-size: 15px; }
	.kt-riba { display: flex; align-items: center; gap: 8px; height: 14px; margin-bottom: 3px; }
	.kt-riba i { display: block; height: 100%; border-radius: 3px; min-width: 2px; }
	.kt-riba b { font-size: 12px; color: var(--muted); }
	.kt-ras { padding-left: 20px; display: grid; gap: var(--sp-3); }
	.kt-ras p { margin: 0 0 2px; }
	.kt-minu { padding-left: 18px; }
	.kt-op { display: grid; grid-template-columns: minmax(0, 1fr) 70px 70px 90px; gap: var(--sp-2); align-items: center; padding: 10px 4px; font-variant-numeric: tabular-nums; }
	.kt-op-pea { font-size: 12px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--line); }
	.kt-opd { border-bottom: 1px solid var(--line); }
	.kt-opd summary { cursor: pointer; list-style: none; }
	.kt-opd summary::-webkit-details-marker { display: none; }
	.kt-opd summary:hover { background: #f7f8fa; }
	.kt-opn { font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.kt-plus { color: #1f9d55; font-weight: 700; }
	.kt-miinus { color: #b4471a; font-weight: 700; }
	.kt-valed { padding: 0 4px var(--sp-3); }
	.kt-valed ul { margin: 4px 0 var(--sp-2); padding-left: 18px; font-size: 14px; }
	.kt-valed li { margin-bottom: 4px; }
	@media (max-width: 600px) { .kt-op { grid-template-columns: minmax(0, 1fr) 52px 60px 70px; font-size: 14px; } }
	.kt-nupud { display: flex; gap: var(--sp-2); flex-wrap: wrap; }
	.kt-printaeg { display: none; }
	/* print / PDF: ainult tulemused */
	@media print {
		:global(.site-header), :global(.site-footer), :global(.kps), :global(.skip) { display: none !important; }
		.kt-nupud { display: none; }
		.kt-printaeg { display: block; }
		.kt-kaart { border: 1px solid #ccc; break-inside: avoid; }
		.kt-opd summary { break-inside: avoid; }
		.kt-riba i { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
	}
</style>
