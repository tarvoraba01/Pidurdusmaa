<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = t('Reaktsioonimäng: eesolev auto pidurdab või pimedas on teel jalakäija. Vajuta, kui näed ohtu, ja vaata, kas jõuad peatuda või sõidad otsa. Jaga tulemust sõpradega.');
	const jsonld = graph(tooriist(t('Reaktsioonitest: kui kiiresti sina pidurdad?'), '/liiklusohutus/reaktsioon/', KIRJ, keel.lang), ORG);
</script>

<Meta title={t('Reaktsioonitest: kui kiiresti sina pidurdad?')} desc={KIRJ} path="liiklusohutus/reaktsioon/" {jsonld} image="/og/sait/liiklus-reaktsioon.png" />

<LiiklusLeht kick={t('Liiklusohutus · mäng')} h1={t('Kui kiiresti SINA pidurdad?')} lead={t('Eesolev auto pidurdab järsult või pimedas on teel jalakäija. Vajuta, kui näed ohtu, ja vaata, kas jõuad peatuda.')} vaade="reaktsioon">
	<div>
		<h2>{t('Kuidas see töötab')}</h2>
		<p>{t('Mõõdame, kui kiiresti vajutad pärast seda, kui oht tuleb nähtavale. Edasi on sama arvutus mis kalkulaatoris valitud ilmaga: kuiv või märg asfalt suverehvidega, talvel tallatud lumi lamellrehvidega; sinu auto või VW Golf 8. Eesolev auto pidurdab sama tugevalt kui sina. Pimedas tuleb jalakäija nähtavale lähitulede valgel: tumedates riietes umbes 30 m, heledates 45 m ja helkuriga 140 m kauguselt (Transpordiamet).')}</p>
	</div>
	<div>
		<h2>{t('Miks liikluses on rohkem')}</h2>
		<p>{t('Testis ootad tulesid. Liikluses tuleb oht ootamatult ja juht vajab tavaliselt umbes 1 sekundi, väsinuna või telefoniga veel rohkem. Iga sekund 90 km/h juures on 25 meetrit sõitu täiskiirusel.')}</p>
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
