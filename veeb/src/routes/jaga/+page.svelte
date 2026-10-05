<script>
	/* Jagatud tulemus: suur number + mis selle taga on + „Arvuta oma auto“.
	   og:image on selle tulemuse pilt (/jaga/pilt.png), nii et Facebooki,
	   WhatsAppi jm eelvaade näitab sama numbrit. Number arvutatakse serveris. */
	import Meta from '$lib/Meta.svelte';
	import { page } from '$app/state';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	let { data } = $props();
	const r = $derived(data.res);
	const LOC = $derived({ et: 'et-EE', ru: 'ru-RU', en: 'en-GB' }[keel.lang] || 'et-EE');
	const nf = (x) => x.toLocaleString(LOC, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
	const pealkiri = $derived(
		r ? (r.stop ? t('Peatumisteekond') : t('Pidurdusteekond')) + ' ' + nf(r.d) + ' m · ' + r.v + ' km/h, ' + r.olu.toLowerCase() : t('Jagatud tulemus')
	);
	const kirjeldus = $derived(
		r ? r.rehv + ' · ' + r.auto + ' · ' + r.moot + '. ' + t('Arvuta oma auto ja rehvidega — tasuta, ilma registreerimata.') : t('Arvuta oma auto pidurdusmaa.')
	);
	const canon = $derived(page.url.pathname + page.url.search);
</script>

<Meta
	title={pealkiri}
	desc={kirjeldus}
	path="jaga/"
	canonical={canon}
	noindex
	image={data.pilt || undefined}
	imageAlt={pealkiri}
/>

<section class="jg">
	<div class="wrap jg-in">
		{#if r}
			<p class="jg-k">{r.stop ? t('Peatumisteekond') : t('Pidurdusteekond')} {r.v} → 0 km/h · {r.olu}</p>
			<p class="jg-num"><b>{nf(r.d)}</b> m</p>
			{#if r.stop}<p class="jg-split">{t('Reageerimisteekond')} {nf(r.react)} m ({String(r.rt).replace('.', ',')} s) + {t('pidurdusteekond')} {nf(r.pidur)} m</p>{/if}
			<dl class="jg-dl">
				<dt>{t('Rehv')}</dt>
				<dd>{r.rehv}<small>{r.alla + (r.mm ? ' · ' + t('muster') + ' ' + String(r.mm).replace('.', ',') + ' mm' : '')}</small></dd>
				<dt>{t('Auto')}</dt>
				<dd>{r.auto}{#if r.autoVaikimisi}<small>{t('auto valimata — arvutatud VW Golf 8 järgi')}</small>{/if}</dd>
				<dt>{t('Rehvimõõt')}</dt>
				<dd>{r.moot}</dd>
			</dl>
			<p class="jg-vahemik">{t('Mudeli hinnang, vahemik')} {nf(r.lo)}–{nf(r.hi)} m. {t('Päris elus võib pidurdusmaa olla pikem.')}</p>
			<div class="jg-cta">
				<a class="btn yel" href={data.kalk}>{t('Arvuta oma auto ja rehvidega →')}</a>
				<a class="linkbtn" href={L('/teadmine/kuidas-pidurdusmaa-arvutatakse/')}>{t('Kuidas arvutame')}</a>
			</div>
		{:else}
			<h1 class="jg-h">{t('Seda tulemust ei saa näidata')}</h1>
			<p>{t('Link on vigane või andmed on vahepeal muutunud. Arvuta uuesti — see võtab mõne sekundi.')}</p>
			<div class="jg-cta"><a class="btn yel" href={L('/')}>{t('Arvuta pidurdusmaa →')}</a></div>
		{/if}
	</div>
</section>

<style>
	.jg {
		background: var(--ink, #0a0b0d);
		color: #fff;
		padding: var(--sp-10, 56px) 0 var(--sp-12, 72px);
	}
	.jg-in {
		max-width: 760px;
	}
	.jg-k {
		margin: 0;
		color: var(--yellow);
		font-size: 14px;
		font-weight: 600;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}
	.jg-num {
		margin: 6px 0 0;
		font: 700 clamp(84px, 18vw, 150px) / 0.95 'Barlow Condensed', Inter, system-ui, sans-serif;
		font-variant-numeric: tabular-nums;
		color: #c9ced6;
	}
	.jg-num b {
		color: #fff;
		font-weight: 700;
	}
	.jg-split {
		margin: 8px 0 0;
		color: #c9ced6;
		font-size: 15px;
	}
	.jg-dl {
		display: grid;
		grid-template-columns: auto minmax(0, 1fr);
		gap: 10px var(--sp-4, 16px);
		margin: var(--sp-6, 28px) 0 0;
		font-size: 17px;
	}
	.jg-dl dt {
		color: #8b929e;
		font-size: 14px;
		padding-top: 2px;
	}
	.jg-dl dd {
		margin: 0;
		font-weight: 700;
		overflow-wrap: break-word;
	}
	.jg-dl small {
		display: block;
		font-weight: 400;
		color: #aab0ba;
		font-size: 14px;
		margin-top: 2px;
	}
	.jg-vahemik {
		margin: var(--sp-5, 22px) 0 0;
		color: #8b929e;
		font-size: 14px;
	}
	.jg-cta {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--sp-4, 16px);
		margin-top: var(--sp-6, 28px);
	}
	.jg-cta .linkbtn {
		color: #fff;
	}
	.jg-h {
		color: #fff;
		margin: 0 0 8px;
	}
</style>
