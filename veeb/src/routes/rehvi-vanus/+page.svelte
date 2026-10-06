<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = t('Sisesta rehvi küljelt DOT-koodi 4 numbrit ja näed rehvi vanust. Vali mustri sügavus ja vaata, kui palju pikem on pidurdusmaa kui uue rehviga.');
	const jsonld = graph(tooriist(t('Kui vanad on su rehvid? DOT-koodi kontroll'), '/rehvi-vanus/', KIRJ, keel.lang), ORG);
</script>

<Meta title={t('Kui vanad on su rehvid? DOT-koodi kontroll ja pidurdusmaa')} desc={KIRJ} path="rehvi-vanus/" crumbs={[[t('Avaleht'), '/'], [t('Rehvi vanus'), '/rehvi-vanus/']]} {jsonld} image="/og/sait/rehvi-vanus.png" />

<LiiklusLeht kick={t('Rehvid · DOT-kood')} h1={t('Kui vanad on su rehvid?')} lead={t('Rehvi küljel on DOT-kood. Selle 4 viimast numbrit ütlevad, millal rehv tehti. Näitame vanust ja seda, kui palju vanus ja kulunud muster pidurdusmaad pikendavad.')} vaade="vanus">
	<div>
		<h2>{t('Kuidas DOT-koodi lugeda')}</h2>
		<p>{t('DOT-kood on rehvi küljel. Lõpus on ovaalses raamis 4 numbrit: kaks esimest on tootmisnädal, kaks viimast aasta. 0821 tähendab 8. nädalat 2021, ehk veebruari 2021. Kui numbreid on ainult 3, on rehv tehtud enne 2000. aastat. Kood on tavaliselt ainult ühel küljel, nii et vaata vajadusel ka rehvi sisekülge.')}</p>
	</div>
	<div>
		<h2>{t('Miks vanus loeb')}</h2>
		<p>{t('Kumm kõveneb ka siis, kui rehviga ei sõideta. Kõvem kumm haakub märjal ja külmal teel halvemini. Rehvitootjad soovitavad üle 5 aasta vanuseid rehve igal aastal kontrollida ja vahetada need hiljemalt 10 aasta vanuselt. Mustri sügavus mõjutab pidurdust veel rohkem: kulunud muster ei juhi vett ega lund rehvi alt välja.')}</p>
	</div>
	<div>
		<h2>{t('Kuidas arvutame')}</h2>
		<p>{t('Sama arvutus mis kalkulaatoris. Võrdleme keskmist uut rehvi (märghaardeklass C) sinu rehviga, millel on sinu sisestatud vanus ja muster. Auto on see, mille valisid kalkulaatoris, muidu VW Golf 8. Oma täpse rehvi tulemust näed kalkulaatoris.')}</p>
		<ul>
			<li><a href={keel.L('/')}>{t('Pidurdusmaa kalkulaator')}</a></li>
			<li><a href={keel.L('/rehvi-valimine/')}>{t('Rehvi valimine')}</a></li>
		</ul>
	</div>
</LiiklusLeht>
