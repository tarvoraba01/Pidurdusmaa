<script>
	/* Tavaleht: pealkiri, teerada ja tekst. Sama kest, mis oli page.php. */
	import Meta from '$lib/Meta.svelte';
	let { title, desc, path, crumbs = [], sisu, lapsed = [] } = $props();
</script>

<Meta {title} {desc} {path} crumbs={[['Avaleht', '/'], ...crumbs]} />

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href="/">Avaleht</a>
			{#each crumbs.slice(0, -1) as c}<span>/</span><a href={c[1]}>{c[0]}</a>{/each}
			<span>/</span>{title}
		</div>
		<h1>{title}</h1>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<article class="entry prose entry-content">{@html sisu}</article>
		{#if lapsed.length}
			<div class="grid-cards" style="margin-top:var(--sp-8);max-width:760px">
				{#each lapsed as k (k[1])}
					<a class="tcard" href={k[1]}><span class="b">Teadmine</span><h3>{k[0]}</h3></a>
				{/each}
			</div>
		{/if}
	</div>
</div>
