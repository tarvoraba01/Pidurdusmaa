<script>
	/* /talverehvid/ — „Parimad talverehvid <mõõt>“ lehtede nimekiri (vt $lib/server/talv.js) */
	import Meta from '$lib/Meta.svelte';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const L = useLang().L;
	let { data } = $props();
</script>

<Meta
	title={t('Parimad talverehvid 2026/2027 mõõdu järgi')}
	desc={t('Talverehvid Eesti levinumates mõõtudes: testitud naast- ja lamellrehvid, pidurdusmaa lumel ja jääl ning Põhjamaade rehvid EL-i märgise järgi.')}
	path="talverehvid/"
	crumbs={[[t('Avaleht'), '/'], [t('Talverehvid'), '/talverehvid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span>{t('Talverehvid')}</div>
		<h1>{t('Parimad talverehvid mõõdu järgi')}</h1>
		<p>{t('Vali oma rehvimõõt: näed testitud naast- ja lamellrehve, nende pidurdusmaad lumel ja jääl ning kõiki Põhjamaade talverehve selles mõõdus.')}</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="box">
			<h2>{t('Eesti levinumad mõõdud')}</h2>
			<p class="sub">{t('Järjestatud selle järgi, mitmel automudelil on see tehase põhimõõt.')}</p>
			<div class="sizes-list">
				{#each data.moodud as m (m.slug)}
					<a href={L('/talverehvid/' + m.slug + '/')}>{m.label} <span class="note">· {m.autosid} {t('autot')}</span></a>
				{/each}
			</div>
		</div>
		<p class="note">
			{t('Mõõt on rehvi küljel (nt 205/55 R16) ja juhiukse piirdel.')}
			<a href={L('/teadmine/artiklid/millal-talverehvid-alla/')}>{t('Millal talverehvid alla?')}</a>
		</p>
	</div>
</div>
