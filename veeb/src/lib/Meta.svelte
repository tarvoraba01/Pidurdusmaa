<script>
	/* Lehe pealkiri, kirjeldus, canonical, OG ja JSON-LD ühest kohast —
	   sama roll, mis oli inc/seo.php-l. */
	const BASE = 'https://pidurdusmaa.ee';
	let { title, desc, path = '', canonical = null, noindex = false, crumbs = [], jsonld = null } = $props();
	const url = $derived(BASE + '/' + String(path).replace(/^\//, ''));
	/* tootjavariandi leht viitab emamudelile (vt andmed.js rehviIndeks) */
	const canon = $derived(canonical ? BASE + '/' + String(canonical).replace(/^\//, '') : url);
	const crumbLd = $derived(
		crumbs.length > 1
			? {
					'@context': 'https://schema.org',
					'@type': 'BreadcrumbList',
					itemListElement: crumbs.map((c, i) => ({
						'@type': 'ListItem',
						position: i + 1,
						name: c[0],
						item: c[1].startsWith('http') ? c[1] : BASE + c[1]
					}))
				}
			: null
	);
</script>

<svelte:head>
	<title>{title} | Pidurdusmaa.ee</title>
	<meta name="description" content={desc} />
	<link rel="canonical" href={canon} />
	{#if noindex}<meta name="robots" content="noindex, follow" />{/if}
	<meta property="og:type" content="website" />
	<meta property="og:site_name" content="Pidurdusmaa.ee" />
	<meta property="og:title" content={title} />
	<meta property="og:description" content={desc} />
	<meta property="og:url" content={canon} />
	<meta property="og:locale" content="et_EE" />
	{#if crumbLd}
		{@html '<script type="application/ld+json">' + JSON.stringify(crumbLd) + '<\/script>'}
	{/if}
	{#if jsonld}
		{@html '<script type="application/ld+json">' + JSON.stringify(jsonld) + '<\/script>'}
	{/if}
</svelte:head>
