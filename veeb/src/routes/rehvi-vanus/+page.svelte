<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import RehviVanus from '$lib/RehviVanus.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = t('Sisesta rehvi küljelt DOT-koodi 4 numbrit ja näed rehvi vanust. Vali mustri sügavus ja vaata, kui palju pikem on pidurdusmaa kui uue rehviga.');
	/* KKK (päring „rehvide vanus“): numbrid sama mudeliga mis tööriist (VW Golf 8, 205/55 R16, märg 90 km/h, keskmine C-klassi suverehv) */
	const KKK = [
		[t('Kui vana rehviga võib sõita?'), t('Seadus rehvi vanust ei piira, aga rehvitootjad soovitavad üle 5 aasta vanuseid rehve igal aastal kontrollida ja vahetada need hiljemalt 10 aasta vanuselt. Kumm kõveneb ka siis, kui rehviga ei sõideta.')],
		[t('Kuidas DOT-koodist rehvi vanust lugeda?'), t('Rehvi küljel on ovaalses raamis 4 numbrit: kaks esimest on tootmisnädal, kaks viimast aasta. Näiteks 0821 tähendab 2021. aasta 8. nädalat. Kui numbreid on ainult 3, on rehv tehtud enne 2000. aastat.')],
		[t('Kui palju pikendab rehvi vanus pidurdusmaad?'), t('Meie arvutuses pidurdab 10 aastat vana rehv märjal teel 90 km/h pealt ka täie mustriga umbes 2,3 m pikemalt kui uus (VW Golf 8, 205/55 R16). Kulunud muster mõjub veel rohkem: 3 mm mustriga rehv pidurdab umbes 4 m pikemalt kui uus.')]
	];
	const faq = { '@type': 'FAQPage', mainEntity: KKK.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) };
	const jsonld = graph(tooriist(t('Kui vanad on su rehvid? DOT-koodi kontroll'), '/rehvi-vanus/', KIRJ, keel.lang), ORG, faq);
</script>

<Meta title={t('Rehvide vanus ja DOT-kood: kui vana rehv on liiga vana?')} desc={KIRJ} path="rehvi-vanus/" crumbs={[[t('Avaleht'), '/'], [t('Rehvi vanus'), '/rehvi-vanus/']]} {jsonld} image="/og/sait/rehvi-vanus.png" />

<LiiklusLeht Tool={RehviVanus} kick={t('Rehvid · DOT-kood')} h1={t('Rehvide vanus: kui vanad on su rehvid?')} lead={t('Rehvi küljel on DOT-kood. Selle 4 viimast numbrit ütlevad, millal rehv tehti. Näitame vanust ja seda, kui palju vanus ja kulunud muster pidurdusmaad pikendavad.')} vaade="vanus">
	<div>
		<h2>{t('Kuidas DOT-koodi lugeda')}</h2>
		<p>{t('DOT-kood on rehvi küljel. Lõpus on ovaalses raamis 4 numbrit: kaks esimest on tootmisnädal, kaks viimast aasta. 0821 tähendab 2021. aasta 8. nädalat ehk veebruari 2021. Kui numbreid on ainult 3, on rehv tehtud enne 2000. aastat. Kood on tavaliselt ainult ühel küljel, nii et vaata vajadusel ka rehvi sisekülge.')}</p>
	</div>
	<div>
		<h2>{t('Miks vanus loeb')}</h2>
		<p>{t('Kumm kõveneb ka siis, kui rehviga ei sõideta. Kõvem kumm haakub märjal ja külmal teel halvemini. Rehvitootjad soovitavad üle 5 aasta vanuseid rehve igal aastal kontrollida ja vahetada need hiljemalt 10 aasta vanuselt. Mustri sügavus mõjutab pidurdust veel rohkem: kulunud muster ei juhi vett ega lund rehvi alt välja.')}</p>
	</div>
	<div>
		<h2>{t('Kuidas arvutame')}</h2>
		<p>{t('Sama arvutus, mis kalkulaatoris. Võrdleme keskmist uut rehvi (märghaardeklass C) sinu rehviga, millel on sinu sisestatud vanus ja muster. Auto on see, mille valisid kalkulaatoris, muidu VW Golf 8. Oma täpse rehvi tulemust näed kalkulaatoris.')}</p>
		<ul>
			<li><a href={keel.L('/')}>{t('Pidurdusmaa kalkulaator')}</a></li>
			<li><a href={keel.L('/rehvi-valimine/')}>{t('Rehvi valimine')}</a></li>
			{#if keel.lang !== 'en'}<li><a href={keel.L('/teadmine/artiklid/vanad-ja-kulunud-rehvid/')}>{t('Vanad ja kulunud rehvid: kui palju pikeneb pidurdusmaa?')}</a></li>{/if}
		</ul>
	</div>
	{#each KKK as [q, a] (q)}
		<div>
			<h2>{q}</h2>
			<p>{a}</p>
		</div>
	{/each}
</LiiklusLeht>
