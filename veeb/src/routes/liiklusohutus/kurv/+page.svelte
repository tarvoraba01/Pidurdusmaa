<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = t('Mis juhtub, kui pidurdad kurvis ja kulunud rehvid on ees või taga? Kurvi piirkiirus, peatumisteekond ja kas auto pöörab ringi või sõidab kurvist otse välja.');
	const jsonld = graph(tooriist(t('Kurvis pidurdamise kalkulaator'), '/liiklusohutus/kurv/', KIRJ, keel.lang), ORG);
</script>

<Meta title={t('Pidurdamine kurvis: paremad rehvid ees või taga?')} desc={KIRJ} path="liiklusohutus/kurv/" {jsonld} image="/og/sait/liiklus-kurv.png" />

<LiiklusLeht kick={t('Liiklusohutus · kurv ja rehvid')} h1={t('Pidurdamine kurvis')} lead={t('Vali kurv, kiirus, teeolud ja rehvid ning vaata animatsioonist, mis juhtub äkkpidurdusel: kas auto peatub oma rajal, kandub vastassuunavööndisse, pöörab ringi või sõidab teelt välja.')} vaade="kurv">
	<div>
		<h2>{t('Kuidas see töötab')}</h2>
		<p>{t('Kurvis kulub osa rehvi haardest auto pööramisele. Pidurdades kandub koormus esisillale ja tagarattad jäävad kergemaks — kui taga on kulunud rehvid, kaotab tagaosa haarde esimesena ja auto pöörab ringi. Kui kulunud on esirehvid, auto ei pööra ja sõidab kurvist otse välja.')}</p>
		<p>{t('Auto liikumine arvutatakse iga 2 millisekundi järel: rehvide haare, koormuse ülekanne, ABS ja juhi roolimine. Tabelis „Kõik kiirused ja teeolud“ on sama kurv läbi arvutatud 23 kiirusel ja neljal teel — kokku 92 olukorda.')}</p>
	</div>
	<div>
		<h2>{t('Allikad')}</h2>
		<ul class="lo-src">
				<li>{t("ADAC, TCS, ÖAMTC — paremad rehvid tagasillale (katsed märjal teel)")}</li>
				<li>{t("Pidurdusmaa arvutusmudel: rehvi haare mustrisügavuse, vee, temperatuuri ja kiiruse järgi")}</li>
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
