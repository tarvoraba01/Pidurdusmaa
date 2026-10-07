<script>
	/* Koolitus autokoolidele ja kõigile: eeltest → selgitused + simulaator → järeltest. */
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';

	const KIRJ = t('Tasuta liiklusohutuse test: pidurdusteekond, rehvid, libe tee ja pimedas sõitmine. Eeltest, selgitused simulaatoriga ja järeltest. Autokoolid saavad luua oma grupi testi.');
	const jsonld = graph(tooriist(t('Liiklusohutuse koolitus: kui hästi sa tunned pidurdamist?'), '/liiklusohutus/koolitus/', KIRJ, keel.lang), ORG);
</script>

<Meta title={t("Koolitus: kui hästi sa tunned pidurdamist?")} desc={KIRJ} path="liiklusohutus/koolitus/" {jsonld} />

<LiiklusLeht kick={t('Liiklusohutus · koolitus')} h1={t('Kui hästi sa tunned pidurdamist?')} lead={t('Vasta, nagu arvad. Siis näed, kuidas päriselt on.')} vaade="koolitus">
	<div>
		<h2>{t('Kuidas see töötab')}</h2>
		<p>{t('Eeltestis vastad ilma vihjeteta. Siis näed iga küsimuse juures õiget vastust, selgitust ja linki simulaatorisse, kus saad sama olukorda ise proovida. Järeltest küsib samu teadmisi teises olukorras, nii et näed, kas asi sai selgeks.')}</p>
	</div>
	<div>
		<h2>{t('Kust arvud tulevad')}</h2>
		<p>{t('Kõik arvud on arvutatud sama mudeliga, mis lehe kalkulaator: VW Golf 8, keskmine rehv, reaktsioon 1 sekund. Nähtavuse kaugused pimedas on Transpordiameti andmed.')}</p>
	</div>
	<div>
		<h2>{t('Autokoolidele')}</h2>
		<p>{t('Õpetaja loob grupile oma testi umbes 2 minutiga: vali teemad ja küsimuste arv, jaga õpilastele linki või QR-koodi. Tulemuste lehelt näeb iga õpilase tulemust enne ja pärast ning teemasid, mis jäid segaseks. Tulemused saab printida või PDF-ina salvestada. Kõik on tasuta.')}</p>
	</div>
</LiiklusLeht>
