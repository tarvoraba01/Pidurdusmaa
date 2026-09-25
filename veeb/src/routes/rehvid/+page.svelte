<script>
	import Meta from '$lib/Meta.svelte';
	import { KAT_NIMI, num } from '$lib/util.js';
	let { data } = $props();
</script>

<Meta
	title="Rehvid mõõdu ja mudeli järgi"
	desc="Rehvimudelid ja -mõõdud EL-i rehvimärgise (EPREL) andmetega ning sõltumatute testide mõõdetud pidurdusmaad."
	path="rehvid/"
	crumbs={[['Avaleht', '/'], ['Rehvid', '/rehvid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span>Rehvid</div>
		<h1>Rehvid</h1>
		<p>
			{num(data.mudeleid, 0)} rehvimudelit EL-i rehvimärgisega ja {data.tested.length} rehvi
			sõltumatutes testides. Vali mõõt, et näha kõiki selle mõõdu rehve.
		</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="box">
			<h2>Mõõdu järgi</h2>
			<p class="sub">Andmebaasis olevad mõõdud. Korje laieneb — kui sinu mõõtu pole, on andmed alles tulemas.</p>
			<div class="sizes-list">
				{#each data.sizes as s (s.slug)}
					<a href="/rehvid/{s.slug}/">{s.label} <span class="note">· {s.n}</span></a>
				{/each}
			</div>
		</div>
		<div class="box">
			<h2>Sõltumatult testitud</h2>
			<p class="sub">Neil rehvidel on mõõdetud pidurdusmaad — täpsemad kui märgise klass.</p>
			<div class="grid-cards">
				{#each data.tested as t, ti (t.slug + '#' + ti)}
					<a class="tcard" href="/rehvid/{t.slug}/">
						<span class="b">{KAT_NIMI[t.category] ?? ''}</span>
						<h3>{t.name}</h3>
						<span class="meta">{t.srcs}</span>
					</a>
				{/each}
			</div>
		</div>
		<div class="box">
			<h2>Margi järgi</h2>
			<p class="sub">Iga margi lehel on kõik selle mudelid kategooria kaupa. <a href="/margid/">Kõik margid →</a></p>
			<div class="sizes-list">
				{#each data.margid as m (m.slug)}
					<a href="/margid/{m.slug}/">{m.nimi} <span class="note">· {m.n}</span></a>
				{/each}
			</div>
		</div>
	</div>
</div>
