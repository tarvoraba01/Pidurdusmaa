<script>
	/* „Talvine pidurdusmaa“ (Tarvo 22.10): talvekampaania leht koostöös LKF-iga, pidurdusmaa.ee/talv,
	   /ru/talv, /en/talv. Kolm tööriista ühel lehel ja üks link kõigis kanalites:
	   pikivahe talvel, reaktsioonitest telefonisõnumiga, rehvi vanuse kontroll; lõpus LKF-i sõnum.
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

	/* LKF-i juhend „Mis teha, kui juhtus“ (vene keeles LKF-il lehte pole, siis eestikeelne) */
	const LKF = keel.lang === 'en' ? 'https://www.lkf.ee/en' : 'https://www.lkf.ee/et/mistehakuijuhtus';
	const KIRJ = t('Talvel peatub auto lumel ja jääl palju pikema maaga. Vaata, kui kiiresti pidurdad, kui telefon piiksub, kas su pikivahe on piisav ja kas su rehvid on talveks veel head.');
	const jsonld = graph(tooriist(t('Talvine pidurdusmaa'), '/talv/', KIRJ, keel.lang), ORG);
	const SAMMUD = [
		['reaktsioon', t('Reaktsioon ja telefon')],
		['pikivahe', t('Pikivahe talvel')],
		['rehvid', t('Rehvide vanus')]
	];
</script>

<Meta title={t('Talvine pidurdusmaa: pikivahe, reaktsioon ja rehvid')} desc={KIRJ} path="talv/" {jsonld} image="/og/sait/liiklus-pikivahe.png" noindex />

<section class="tv-hero">
	<div class="wrap">
		<!-- partneri logo koht: tühi kast, päris logo ainult loaga (Tarvo 22.10) -->
		<p class="tv-kick tv-koos">{t('Koostöös')}: <span class="tv-logo">{t('teie logo')}</span></p>
		<h1>{t('Talvine pidurdusmaa')}</h1>
		<p class="tv-lead">{KIRJ}</p>
		<nav class="tv-sammud" aria-label={t('Lehe osad')}>
			{#each SAMMUD as [id, nimi], i (id)}<a href={'#' + id}><b>{i + 1}</b>{nimi}</a>{/each}
		</nav>
	</div>
</section>

<section class="tv-osa" id="reaktsioon">
	<div class="wrap">
		<p class="tv-nr">1 / 3</p>
		<h2>{t('Kui kiiresti pidurdad, kui telefon piiksub?')}</h2>
		<p class="tv-sel">{t('Telefoni tuleb sõnum just siis, kui eesolev auto pidurdab. Vajuta kohe, kui pidurituled süttivad. Üks proov.')}</p>
	</div>
	<div class="wrap"><Reaktsioon algIlm="talv" telefon katseid={1} /></div>
</section>

<section class="tv-osa tv-tume" id="pikivahe">
	<div class="wrap">
		<p class="tv-nr">2 / 3</p>
		<h2>{t('Kas su pikivahe on talveks piisav?')}</h2>
		<p class="tv-sel">{t('Eesolev auto pidurdab järsult. Vaata, kas lumel jõuad peatuda, ja kui ei, siis millise kiirusega sõidad talle sisse.')}</p>
	</div>
	<div class="wrap"><Liiklus vaade="pikivahe" talv /></div>
</section>

<section class="tv-osa" id="rehvid">
	<div class="wrap">
		<p class="tv-nr">3 / 3</p>
		<h2>{t('Kas su rehvid on talveks veel head?')}</h2>
		<p class="tv-sel">{t('Sisesta rehvi küljel oleva DOT-koodi 4 viimast numbrit ja mustri sügavus. Näed rehvi vanust ja seda, kui palju pikem on pidurdusmaa lumel.')}</p>
	</div>
	<div class="wrap"><RehviVanus talv /></div>
</section>

<section class="tv-lkf">
	<div class="wrap tv-lkf-sisu">
		<p class="tv-kick">LKF</p>
		<h2>{t('Mis teha, kui juhtus')}</h2>
		<p>{t('Pane ohutuled põlema ja tee ohukolmnurgaga teistele märku. Kui keegi sai viga, helista 112. Vaheta teise juhiga andmed ja pildista kahjustusi. Täpse juhendi ja avariiteate leiad Liikluskindlustuse Fondi lehelt.')}</p>
		<a class="btn yel" href={LKF} target="_blank" rel="noopener">{t('LKF-i juhend')} →</a>
	</div>
</section>

<section class="tv-info">
	<div class="wrap">
		<p>{t('Pidurdusmaad arvutab Pidurdusmaa.ee sama mudeliga, mis kõigis meie kalkulaatorites.')} <a href={keel.L('/teadmine/kuidas-pidurdusmaa-arvutatakse/')}>{t('Kuidas pidurdusmaa arvutatakse')}</a> · <a href={keel.L('/talverehvid/')}>{t('Talverehvid mõõdu järgi')}</a></p>
	</div>
</section>

<style>
	.tv-hero { background: var(--ink); color: var(--on-d); padding: var(--sp-10) 0 var(--sp-8); }
	.tv-kick { color: var(--yellow); font-weight: 700; font-size: 13px; letter-spacing: 0.14em; text-transform: uppercase; margin: 0 0 var(--sp-3); }
	.tv-koos { display: flex; align-items: center; gap: 12px; }
	.tv-logo { display: inline-grid; place-items: center; min-width: 140px; height: 44px; padding: 0 14px; border: 1.5px dashed rgba(255, 255, 255, 0.35); border-radius: 10px; color: rgba(255, 255, 255, 0.5); font-size: 11px; letter-spacing: 0.12em; }
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
	.tv-osa h2, .tv-lkf h2 { font-family: var(--display); font-weight: 700; text-transform: uppercase; font-size: clamp(28px, 3.6vw, 42px); line-height: 1; margin: 0 0 var(--sp-2); text-wrap: balance; }
	.tv-sel { font-size: 17px; max-width: 720px; margin: 0 0 var(--sp-4); color: var(--ink-2, #333); }
	.tv-lkf { background: var(--ink); color: var(--on-d); padding: var(--sp-10) 0; }
	.tv-lkf-sisu { max-width: 760px; }
	.tv-lkf p:not(.tv-kick) { color: #cfd4db; font-size: 17px; margin: 0 0 var(--sp-5); }
	.tv-info { background: #fff; padding: var(--sp-6) 0 var(--sp-10); font-size: 15px; color: var(--muted, #6b7280); }
</style>
