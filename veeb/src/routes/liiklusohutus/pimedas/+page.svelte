<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = t('Pimedas märkab juht helkurita jalakäijat lähitulede valgel alles umbes 30 m kauguselt. Vaata oma kiiruse, auto ja teeoludega, kas jõuad peatuda ja kui kiiresti tohiks sõita.');
	const jsonld = graph(tooriist(t('Nähtavuse kalkulaator pimedas'), '/liiklusohutus/pimedas/', KIRJ, keel.lang), ORG);
</script>

<Meta title={t('Nähtavus pimedas: kas jõuad jalakäija ees peatuda?')} desc={KIRJ} path="liiklusohutus/pimedas/" {jsonld} image="/og/sait/liiklus-pimedas.png" />

<LiiklusLeht kick={t('Liiklusohutus · pimedas')} h1={t('Kas jõuad pimedas peatuda?')} lead={t('Vali, kuidas jalakäija on riietatud ja mis tuled põlevad. Näed, kas auto jõuab enne teda peatuda, ja suurimat kiirust, millega see veel õnnestub.')} vaade="pimedas">
	<div>
		<h2>{t('Kuidas see töötab')}</h2>
		<p>{t('Takistus pannakse kohta, kust juht jalakäijat märkab. Edasi on sama arvutus mis peatumisteekonna kalkulaatoris: reageerimisaja jooksul sõidab auto täiskiirusel, siis pidurdab. Pimedas tuleb oht sageli ootamatult — proovi ka reageerimisaega 1,5 sekundit.')}</p>
	</div>
	<div>
		<h2>{t('Allikad')}</h2>
		<ul class="lo-src">
				<li>{t("Transpordiamet (2025), „Mida pead helkuri kohta teadma“: lähitulede valgel tumedas riietes helkurita jalakäija kuni 30 m, heledas riietes 40–50 m, helkuriga 130–150 m; kaugtulede valgel helkuriga 300–350 m")}</li>
		</ul>
	</div>
	<div>
		<h2>{t('Teised tööriistad')}</h2>
		<ul>
			<li><a href={keel.L('/liiklusohutus/')}>{t('Peatumisteekonna kalkulaator')}</a></li>
			<li><a href={keel.L('/liiklusohutus/pimedas/')}>{t('Nähtavus pimedas')}</a></li>
			<li><a href={keel.L('/liiklusohutus/pikivahe/')}>{t('Pikivahe kalkulaator')}</a></li>
			<li><a href={keel.L('/liiklusohutus/kurv/')}>{t('Pidurdamine kurvis')}</a></li>
		</ul>
	</div>
</LiiklusLeht>
