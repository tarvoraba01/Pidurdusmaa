<script>
	import Meta from '$lib/Meta.svelte';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const L = useLang().L;
	let { data } = $props();
	const desc = $derived(
		t('{n} automudeli põlvkonda: tehase rehvimõõdud, mootorid ja pidurdusmaa. Vali mark ja vaata, millised rehvid sinu autole sobivad.', { n: data.kokku })
	);
</script>

<Meta title={t('Autod — rehvimõõdud ja pidurdusmaa mudeli järgi')} {desc} path="autod/" crumbs={[[t('Avaleht'), '/'], [t('Autod'), '/autod/']]} />

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span>{t('Autod')}</div>
		<h1>{t('Autod')}</h1>
		<p>{t('Vali mark: iga mudeli põlvkonna kohta näed tehase rehvimõõte, mootoreid, pidurdusmaad ja parimaid rehve selles mõõdus.')}</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="ad-margid">
			{#each data.margid as m (m.slug)}
				<a class="ad-mark" href={L('/autod/' + m.slug + '/')}><span class="n">{m.nimi}</span><span class="c">{t('{mudelid} mudelit · {n} põlvkonda', { mudelid: m.mudelid, n: m.n })}</span></a>
			{/each}
		</div>
	</div>
</div>

<style>
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
