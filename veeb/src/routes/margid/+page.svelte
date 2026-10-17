<script>
	import Meta from '$lib/Meta.svelte';
	import { useT, useLang } from '$lib/i18n.js';
	let { data } = $props();
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	const populaarsed = $derived([...data.list].sort((a, b) => b.t - a.t || b.n - a.n).slice(0, 12));
</script>

<Meta
	title={t('Rehvimargid — kõik rehvitootjad ja mudelid')}
	desc={t('Rehvimargid tähestiku järgi: iga tootja rehvimudelid EL-i rehvimärgise andmetega ja sõltumatute testide tulemustega.')}
	path="margid/"
	crumbs={[[t('Avaleht'), '/'], [t('Rehvid'), '/rehvid/'], [t('Margid'), '/margid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/rehvid/')}>{t('Rehvid')}</a><span>/</span>{t('Margid')}</div>
		<h1>{t('Rehvimargid')}</h1>
		<p>{t('{n} tootjat. Vali mark, et näha kõiki selle mudeleid, märgise klasse ja teste.', { n: data.list.length })}</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="box">
			<h2>{t('Enim testitud')}</h2>
			<div class="grid-cards">
				{#each populaarsed as m (m.slug)}
					<a class="tcard" href={L('/margid/' + m.slug + '/')}>
						<span class="b">{m.t ? t('{n} testis', { n: m.t }) : t('EL-i märgis')}</span>
						<h3>{m.nimi}</h3>
						<span class="meta">{t('{n} mudelit', { n: m.n })}</span>
					</a>
				{/each}
			</div>
		</div>
		<div class="box">
			<h2>{t('Kõik margid')}</h2>
			<div class="sizes-list">
				{#each data.list as m (m.slug)}
					<a href={L('/margid/' + m.slug + '/')}>{m.nimi} <span class="note">· {m.n}</span></a>
				{/each}
			</div>
		</div>
	</div>
</div>
