<script>
	/* „Talvine pidurdusmaa“ (Tarvo 22.10): talvekampaania leht, pidurdusmaa.ee/talv,
	   /ru/talv, /en/talv. Kolm tööriista ühel lehel ja üks link kõigis kanalites:
	   pikivahe talvel, reaktsioonitest telefonisõnumiga, rehvi vanuse kontroll. LKF-i viited eemaldatud (Tarvo 29.10).
	   Numbrid tulevad sama mudeli järgi mis mujal saidil (sõltumatu metoodika). Mängu saab teistele
	   lehtedele anda iframe'ina: /talv/mang/.
	   PEIDETUD (Tarvo 22.10): noindex, pole saidikaardis ega menüüs, kuni kampaania on kokku lepitud. */
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import Liiklus from '$lib/Liiklus.svelte';
	import Reaktsioon from '$lib/Reaktsioon.svelte';
	import RehviVanus from '$lib/RehviVanus.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = t('Talvel peatub auto lumel ja jääl palju pikema maaga. Vaata, kui kiiresti pidurdad, kui telefon piiksub, kas su pikivahe on piisav ja kas su rehvid on talveks veel head.');
	const jsonld = graph(tooriist(t('Talvine pidurdusmaa'), '/talv/', KIRJ, keel.lang), ORG);
	const SAMMUD = [
		['reaktsioon', t('Reaktsioon ja telefon')],
		['pikivahe', t('Pikivahe talvel')],
		['jalakaija', t('Jalakäija pimedas')],
		['rehvid', t('Rehvide vanus')]
	];
</script>

<Meta title={t('Talvine pidurdusmaa: pikivahe, reaktsioon ja rehvid')} desc={KIRJ} path="talv/" {jsonld} image="/og/sait/liiklus-pikivahe.png" noindex />

<section class="tv-hero">
	<div class="wrap">
		<h1>{t('Talvine pidurdusmaa')}</h1>
		<p class="tv-lead">{KIRJ}</p>
		<nav class="tv-sammud" aria-label={t('Lehe osad')}>
			{#each SAMMUD as [id, nimi], i (id)}<a href={'#' + id}><b>{i + 1}</b>{nimi}</a>{/each}
		</nav>
	</div>
</section>

<section class="tv-osa" id="reaktsioon">
	<div class="wrap">
		<p class="tv-nr">1 / 4</p>
		<h2>{t('Kui kiiresti pidurdad, kui telefon piiksub?')}</h2>
		<p class="tv-sel">{t('Telefoni tuleb sõnum just siis, kui eesolev auto pidurdab. Vajuta kohe, kui pidurituled süttivad. Üks proov.')}</p>
	</div>
	<div class="wrap"><Reaktsioon algIlm="talv" algReziim="tuled" lukus telefon katseid={1} /></div>
</section>

<section class="tv-osa tv-tume" id="pikivahe">
	<div class="wrap">
		<p class="tv-nr">2 / 4</p>
		<h2>{t('Kas su pikivahe on talveks piisav?')}</h2>
		<p class="tv-sel">{t('Eesolev auto pidurdab järsult. Vaata, kas lumel jõuad peatuda, ja kui ei, siis millise kiirusega sõidad talle sisse.')}</p>
	</div>
	<div class="wrap"><Liiklus vaade="pikivahe" talv /></div>
</section>

<section class="tv-osa" id="jalakaija">
	<div class="wrap">
		<p class="tv-nr">3 / 4</p>
		<h2>{t('Kas märkad jalakäijat pimedas?')}</h2>
		<p class="tv-sel">{t('Talvel on pime vara ja jalakäija tuleb teele ootamatult. Vajuta kohe, kui teda näed.')}</p>
	</div>
	<div class="wrap"><Reaktsioon algIlm="talv" algReziim="pime" lukus telefon katseid={1} /></div>
</section>

<section class="tv-osa tv-tume" id="rehvid">
	<div class="wrap">
		<p class="tv-nr">4 / 4</p>
		<h2>{t('Kas su rehvid on talveks veel head?')}</h2>
		<p class="tv-sel">{t('Sisesta rehvi küljel oleva DOT-koodi 4 viimast numbrit ja mustri sügavus. Näed rehvi vanust ja seda, kui palju pikem on pidurdusmaa lumel.')}</p>
	</div>
	<div class="wrap"><RehviVanus talv /></div>
</section>


<section class="tv-info">
	<div class="wrap">
		<p>{t('Pidurdusmaad arvutab Pidurdusmaa.ee sama mudeliga, mis kõigis meie kalkulaatorites.')} <a href={keel.L('/teadmine/kuidas-pidurdusmaa-arvutatakse/')}>{t('Kuidas pidurdusmaa arvutatakse')}</a> · <a href={keel.L('/talverehvid/')}>{t('Talverehvid mõõdu järgi')}</a></p>
	</div>
</section>

<style>
	.tv-hero { background: var(--ink); color: var(--on-d); padding: var(--sp-10) 0 var(--sp-8); }
	.tv-kick { color: var(--yellow); font-weight: 700; font-size: 13px; letter-spacing: 0.14em; text-transform: uppercase; margin: 0 0 var(--sp-3); }
	.tv-hero h1 { font-family: var(--display); font-weight: 700; font-size: clamp(40px, 5.4vw, 68px); line-height: 0.95; text-transform: uppercase; margin: 0 0 var(--sp-3); text-wrap: balance; }
	:global(:lang(ru)) .tv-hero h1 { font-size: clamp(28px, 7.4vw, 60px); }
	.tv-lead { color: #cfd4db; font-size: 18px; max-width: 760px; margin: 0 0 var(--sp-6); }
	.tv-sammud { display: flex; flex-wrap: wrap; gap: var(--sp-2); }
	.tv-sammud a { display: inline-flex; align-items: center; gap: 10px; padding: 10px 16px 10px 10px; border-radius: 999px; border: 1px solid rgba(255, 255, 255, 0.16); color: #fff; text-decoration: none; font-weight: 600; font-size: 15px; }
	.tv-sammud a:hover { border-color: var(--yellow); }
	.tv-sammud b { display: grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: var(--yellow); color: #111; font-size: 14px; }
	/* pikivahe: ainult tööriist, ilma simulaatorite vahelehtede ja jagamisnuppudeta */
	#pikivahe :global(.lo-vaated), #pikivahe :global(.lo-tools) { display: none; }
	.tv-osa { background: var(--paper-2); padding: var(--sp-10) 0 var(--sp-6); scroll-margin-top: 60px; }
	.tv-osa + .tv-osa { border-top: 1px solid var(--line); }
	.tv-tume { background: #fff; }
	.tv-nr { color: var(--muted, #6b7280); font-weight: 700; font-size: 13px; letter-spacing: 0.12em; margin: 0 0 var(--sp-2); }
	.tv-osa h2 { font-family: var(--display); font-weight: 700; text-transform: uppercase; font-size: clamp(28px, 3.6vw, 42px); line-height: 1; margin: 0 0 var(--sp-2); text-wrap: balance; }
	.tv-sel { font-size: 17px; max-width: 720px; margin: 0 0 var(--sp-4); color: var(--ink-2, #333); }
	.tv-info { background: #fff; padding: var(--sp-6) 0 var(--sp-10); font-size: 15px; color: var(--muted, #6b7280); }
</style>
