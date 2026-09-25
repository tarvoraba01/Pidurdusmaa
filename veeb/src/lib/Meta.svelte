<script>
	/* Lehe pealkiri, kirjeldus, canonical, OG ja JSON-LD ühest kohast —
	   sama roll, mis oli inc/seo.php-l. */
	const BASE = 'https://pidurdusmaa.ee';
	let {
		title,
		desc,
		path = '',
		canonical = null,
		noindex = false,
		crumbs = [],
		jsonld = null,
		/* jagamispilt 1200×630, vt routes/og */
		image = '/og/sait/avaleht.png',
		imageAlt = '',
		/* avalehel on pealkiri ilma „| Pidurdusmaa.ee“ lõputa */
		fullTitle = null
	} = $props();
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
	<title>{fullTitle ?? title + ' | Pidurdusmaa.ee'}</title>
	<meta name="description" content={desc} />
	<link rel="canonical" href={canon} />
	{#if noindex}<meta name="robots" content="noindex, follow" />{/if}
	<meta property="og:type" content="website" />
	<meta property="og:site_name" content="Pidurdusmaa.ee" />
	<meta property="og:title" content={title} />
	<meta property="og:description" content={desc} />
	<meta property="og:url" content={canon} />
	<meta property="og:locale" content="et_EE" />
	<meta property="og:image" content={BASE + image} />
	<meta property="og:image:width" content="1200" />
	<meta property="og:image:height" content="630" />
	<meta property="og:image:alt" content={imageAlt || title} />
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={title} />
	<meta name="twitter:description" content={desc} />
	<meta name="twitter:image" content={BASE + image} />
	{#if crumbLd}
		{@html '<script type="application/ld+json">' + JSON.stringify(crumbLd) + '<\/script>'}
	{/if}
	{#if jsonld}
		{@html '<script type="application/ld+json">' + JSON.stringify(jsonld) + '<\/script>'}
	{/if}
</svelte:head>
