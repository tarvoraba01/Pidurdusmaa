<script>
	/* /teadmine/artiklid/ — kõik artiklid, uusim esimesena (nimekiri: $lib/artiklid.js).
	   Vene lehel (/ru/teadmine/artiklid/) ainult artiklid, millel on vene versioon (`ru`). */
	import Meta from '$lib/Meta.svelte';
	import { ARTIKLID, artikliTee, kuup } from '$lib/artiklid.js';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	const ru = keel.lang === 'ru';
	const list = ru ? ARTIKLID.filter((a) => a.ru).map((a) => ({ ...a, ...a.ru })) : ARTIKLID;
</script>

<Meta
	title={t('Artiklid — rehvi valimine numbritega')}
	desc={t('Praktilised juhendid rehvi valimiseks: talverehvid, naast vs lamell, mustri sügavus. Iga väide on pidurdusmaa meetrites.')}
	path="teadmine/artiklid/"
	crumbs={[[t('Avaleht'), '/'], [t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href="/teadmine/">{t('Teadmine')}</a><span>/</span>{t('Artiklid')}</div>
		<h1>{t('Artiklid')}</h1>
		<p>{t('Praktilised juhendid rehvi valimiseks. Iga väide on pidurdusmaa meetrites.')}</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="grid-cards art-list">
			{#each list as a (a.slug)}
				<a class="tcard" href={L(artikliTee(a))}>
					<span class="b">{a.silt} · <time datetime={a.kuupaev}>{kuup(a.kuupaev)}</time></span>
					<h3>{a.title}</h3>
					<p class="art-d">{a.desc}</p>
				</a>
			{/each}
		</div>
	</div>
</div>
