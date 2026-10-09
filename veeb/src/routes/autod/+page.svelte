<script>
	import Meta from '$lib/Meta.svelte';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	import { autoNimi } from '$lib/i18n.js';
	let { data } = $props();
	const an = (x) => autoNimi(keel.lang, x);
	/* otsing üle kõigi autode: mark, mudel, põlvkond või aasta (nt „golf 2015“, „passat b6“) */
	let q = $state('');
	const lihtne = (x) => String(x || '').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
	const tulemus = $derived.by(() => {
		const sonad = lihtne(q).split(' ').filter(Boolean);
		if (!sonad.length) return null;
		return data.koik
			.filter((p) => {
				const hay = ' ' + lihtne(p.n) + ' ';
				return sonad.every((w) => (/^\d{4}$/.test(w) ? p.a0 && +w >= p.a0 && +w <= (p.a1 || 9999) : hay.includes(' ' + w)));
			})
			.slice(0, 40);
	});
	const desc = $derived(
		t('{n} automudeli põlvkonda: tehase rehvimõõdud, mootorid ja pidurdusmaa. Vali mark ja vaata, millised rehvid sinu autole sobivad.', { n: data.kokku })
	);
</script>

<Meta title={t('Autod — rehvimõõdud ja pidurdusmaa mudeli järgi')} {desc} path="autod/" crumbs={[[t('Avaleht'), '/'], [t('Autod'), '/autod/']]} />

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span>{t('Autod')}</div>
		<h1>{t('Autod')}</h1>
		<p>{t('Leia oma auto: näed tehase rehvimõõte, pidurdusmaad ja sobivaid rehve.')}</p>
		<input class="lsel au-otsi" type="search" bind:value={q} placeholder={t('Otsi autot, nt Golf 2015 või Passat B6')} aria-label={t('Otsi autot')} />
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		{#if tulemus}
			{#if tulemus.length}
				<ul class="au-tul">
					{#each tulemus as p (p.u)}<li><a href={L(p.u)}><span class="n">{an(p.n)}</span><span class="m">{p.m}</span><span aria-hidden="true">→</span></a></li>{/each}
				</ul>
			{:else}
				<p class="note">{t('Sellist autot ei leidnud. Proovi ainult margi või mudeli nime.')}</p>
			{/if}
			<h2 class="au-h">{t('Või vali mark')}</h2>
		{/if}
		<div class="ad-margid">
			{#each data.margid as m (m.slug)}
				<a class="ad-mark" href={L('/autod/' + m.slug + '/')}><span class="n">{m.nimi}</span><span class="c">{t('{mudelid} mudelit · {n} põlvkonda', { mudelid: m.mudelid, n: m.n })}</span></a>
			{/each}
		</div>
	</div>
</div>

<style>
	.au-otsi { margin-top: var(--sp-5); max-width: 560px; width: 100%; height: 54px; font-size: 17px; background-image: none; }
	.au-tul { list-style: none; margin: 0 0 var(--sp-6); padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: var(--sp-2); }
	.au-tul a { display: flex; align-items: center; gap: var(--sp-3); padding: 12px 14px; border-radius: 12px; background: #fff; border: 1px solid var(--line); text-decoration: none; color: var(--text); }
	.au-tul a:hover { border-color: var(--yellow); background: var(--yellow-soft); }
	.au-tul .n { flex: 1; font-weight: 600; }
	.au-tul .m { color: var(--muted); font-size: 13.5px; white-space: nowrap; }
	.au-h { font-size: 22px; margin: 0 0 var(--sp-3); }
	.ad-margid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		gap: var(--sp-3);
	}
	.ad-mark {
		display: flex;
		flex-direction: column;
		gap: 2px;
		padding: var(--sp-3) var(--sp-4);
		background: #fff;
		border: 1px solid var(--line);
		border-radius: var(--r);
		text-decoration: none;
		color: var(--ink);
	}
	.ad-mark:hover {
		border-color: #c5cad3;
		box-shadow: var(--shadow);
	}
	.ad-mark .n {
		font-weight: 700;
	}
	.ad-mark .c {
		font-size: 13px;
		color: var(--muted);
	}
</style>
