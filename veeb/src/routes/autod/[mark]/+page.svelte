<script>
	import Meta from '$lib/Meta.svelte';
	let { data } = $props();
	const m = $derived(data.mark);
	const path = $derived('/autod/' + m.slug + '/');
	const desc = $derived(
		`${m.nimi}: ${data.mudelid.length} mudelit, ${data.n} põlvkonda — tehase rehvimõõdud, mootorid ja pidurdusmaa. ` +
			data.mudelid.slice(0, 4).map((x) => x.model).join(', ') + '.'
	);
</script>

<Meta
	title="{m.nimi} rehvimõõdud ja pidurdusmaa mudeli järgi"
	{desc}
	path="autod/{m.slug}/"
	crumbs={[['Avaleht', '/'], ['Autod', '/autod/'], [m.nimi, path]]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span><a href="/autod/">Autod</a><span>/</span>{m.nimi}</div>
		<h1>{m.nimi}</h1>
		<p>Vali mudel ja põlvkond: näed tehase rehvimõõte, mootoreid, pidurdusmaad ja parimaid rehve.</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		{#each data.mudelid as x (x.model)}
			<div class="box">
				<h2>{m.nimi} {x.model}</h2>
				<div class="tbl-wrap">
					<table class="t">
						<thead><tr><th>Põlvkond</th><th>Tehase põhimõõt</th></tr></thead>
						<tbody>
							{#each x.polved as p (p.slug)}
								<tr><td><a href="/autod/{m.slug}/{p.slug}/">{p.nimi}</a></td><td>{p.moot}</td></tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/each}
	</div>
</div>
