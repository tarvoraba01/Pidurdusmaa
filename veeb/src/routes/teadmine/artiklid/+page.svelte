<script>
	/* /teadmine/artiklid/ — kõik artiklid, uusim esimesena (nimekiri: $lib/artiklid.js) */
	import Meta from '$lib/Meta.svelte';
	import { ARTIKLID, artikliTee, kuup } from '$lib/artiklid.js';
</script>

<Meta
	title="Artiklid — rehvi valimine numbritega"
	desc="Praktilised juhendid rehvi valimiseks: talverehvid, naast vs lamell, mustri sügavus. Iga väide on pidurdusmaa meetrites."
	path="teadmine/artiklid/"
	crumbs={[['Avaleht', '/'], ['Teadmine', '/teadmine/'], ['Artiklid', '/teadmine/artiklid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span><a href="/teadmine/">Teadmine</a><span>/</span>Artiklid</div>
		<h1>Artiklid</h1>
		<p>Praktilised juhendid rehvi valimiseks. Iga väide on pidurdusmaa meetrites.</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="grid-cards art-list">
			{#each ARTIKLID as a (a.slug)}
				<a class="tcard" href={artikliTee(a)}>
					<span class="b">{a.silt} · <time datetime={a.kuupaev}>{kuup(a.kuupaev)}</time></span>
					<h3>{a.title}</h3>
					<p class="art-d">{a.desc}</p>
				</a>
			{/each}
		</div>
	</div>
</div>
