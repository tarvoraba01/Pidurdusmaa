<script>
	import Meta from '$lib/Meta.svelte';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const L = useLang().L;
	let { data } = $props();
	const m = $derived(data.mark);
	const path = $derived('/autod/' + m.slug + '/');
	const desc = $derived(
		t('{nimi}: {mudelid} mudelit, {n} põlvkonda — tehase rehvimõõdud, mootorid ja pidurdusmaa.', { nimi: m.nimi, mudelid: data.mudelid.length, n: data.n }) +
			' ' + data.mudelid.slice(0, 4).map((x) => x.model).join(', ') + '.'
	);
</script>

<Meta
	title={t('{nimi} rehvimõõdud ja pidurdusmaa mudeli järgi', { nimi: m.nimi })}
	{desc}
	path="autod/{m.slug}/"
	crumbs={[[t('Avaleht'), '/'], [t('Autod'), '/autod/'], [m.nimi, path]]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/autod/')}>{t('Autod')}</a><span>/</span>{m.nimi}</div>
		<h1>{m.nimi}</h1>
		<p>{t('Vali mudel ja põlvkond: näed tehase rehvimõõte, mootoreid, pidurdusmaad ja parimaid rehve.')}</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		{#each data.mudelid as x (x.model)}
			<div class="box">
				<h2>{m.nimi} {x.model}</h2>
				<div class="tbl-wrap">
					<table class="t">
						<thead><tr><th>{t('Põlvkond')}</th><th>{t('Tehase põhimõõt')}</th></tr></thead>
						<tbody>
							{#each x.polved as p (p.slug)}
								<tr><td><a href={L('/autod/' + m.slug + '/' + p.slug + '/')}>{p.nimi}</a></td><td>{p.moot}</td></tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/each}
	</div>
</div>
