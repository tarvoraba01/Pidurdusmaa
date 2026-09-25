<script>
	import Meta from '$lib/Meta.svelte';
	let { data } = $props();
	const populaarsed = $derived([...data.list].sort((a, b) => b.t - a.t || b.n - a.n).slice(0, 12));
</script>

<Meta
	title="Rehvitootjad — kõik margid"
	desc="Rehvimargid tähestiku järgi: iga tootja rehvimudelid EL-i rehvimärgise andmetega ja sõltumatute testide tulemustega."
	path="margid/"
	crumbs={[['Avaleht', '/'], ['Rehvid', '/rehvid/'], ['Margid', '/margid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span><a href="/rehvid/">Rehvid</a><span>/</span>Margid</div>
		<h1>Rehvimargid</h1>
		<p>{data.list.length} tootjat. Vali mark, et näha kõiki selle mudeleid, märgise klasse ja teste.</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="box">
			<h2>Enim testitud</h2>
			<div class="grid-cards">
				{#each populaarsed as m (m.slug)}
					<a class="tcard" href="/margid/{m.slug}/">
						<span class="b">{m.t ? m.t + ' testis' : 'EL-i märgis'}</span>
						<h3>{m.nimi}</h3>
						<span class="meta">{m.n} mudelit</span>
					</a>
				{/each}
			</div>
		</div>
		<div class="box">
			<h2>Kõik margid</h2>
			<div class="sizes-list">
				{#each data.list as m (m.slug)}
					<a href="/margid/{m.slug}/">{m.nimi} <span class="note">· {m.n}</span></a>
				{/each}
			</div>
		</div>
	</div>
</div>
