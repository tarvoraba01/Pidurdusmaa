<script>
	/* Tavaleht: pealkiri, teerada ja tekst. Sama kest, mis oli page.php.
	   Kui `uuendatud` on antud, on leht artikkel: autor + kuupäev nähtaval
	   ja Article-struktuurandmetes. */
	import Meta from '$lib/Meta.svelte';
	import Autor from '$lib/Autor.svelte';
	import { artikkel, graph } from '$lib/skeem.js';
	import { useT, useLang, lingid } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	let { title, desc, path, crumbs = [], sisu, lapsed = [], uuendatud = '', avaldatud = '', image = undefined } = $props();
	const jsonld = $derived(
		uuendatud ? graph(...artikkel({ path: L('/' + path), title, desc, uuendatud, avaldatud, lang: keel.lang })) : null
	);
</script>

<Meta {title} {desc} {path} crumbs={[[t('Avaleht'), '/'], ...crumbs]} ogType={uuendatud ? 'article' : undefined} {jsonld} {image} />

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href={L('/')}>{t('Avaleht')}</a>
			{#each crumbs.slice(0, -1) as c}<span>/</span><a href={L(c[1])}>{c[0]}</a>{/each}
			<span>/</span>{title}
		</div>
		<h1>{title}</h1>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<article class="entry prose entry-content">
			{#if uuendatud}<Autor {uuendatud} />{/if}
			{@html lingid(keel.lang, sisu)}
		</article>
		{#if lapsed.length}
			<div class="grid-cards" style="margin-top:var(--sp-8);max-width:760px">
				{#each lapsed as k (k[1])}
					<a class="tcard" href={L(k[1])}><span class="b">{t('Teadmine')}</span><h3>{k[0]}</h3></a>
				{/each}
			</div>
		{/if}
	</div>
</div>
