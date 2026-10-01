<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = t('Kui eesolev auto pidurdab järsult, kas jõuad peatuda? Vaata 1, 2, 3 ja 4 sekundi pikivahet oma kiiruse, reageerimisaja ja teeoludega — ja kokkupõrke kiirust, kui ei jõua.');
	const jsonld = graph(tooriist(t('Pikivahe kalkulaator'), '/liiklusohutus/pikivahe/', KIRJ, keel.lang), ORG);
</script>

<Meta title={t('Pikivahe kalkulaator: kas 2 sekundit on piisav?')} desc={KIRJ} path="liiklusohutus/pikivahe/" {jsonld} image="/og/sait/liiklusohutus.png" />

<LiiklusLeht kick={t('Liiklusohutus · pikivahe')} h1={t('Kas pikivahe on piisav?')} lead={t('Eesolev auto pidurdab järsult või peatub hetkega. Vaata, kas jõuad peatuda, ja kui ei, siis millise kiirusega sõidad talle sisse.')} vaade="pikivahe">
	<div>
		<h2>{t('Kuidas see töötab')}</h2>
		<p>{t('Mõlemad autod pidurdavad sama arvutusega: sama auto, rehvid ja tee. Sina hakkad pidurdama alles pärast reageerimisaega, seega tuleb kokkupõrge siis, kui reageerimisaeg on pikivahest pikem. Kui eesolev auto peatub hetkega (sõidab millelegi otsa), on vaja palju suuremat vahet.')}</p>
	</div>
	<div>
		<h2>{t('Allikad')}</h2>
		<ul class="lo-src">
				<li>{t("Pidurdusmaa arvutusmudel (sama mis peatumisteekonna kalkulaatoris)")}</li>
				<li>{t("Green, M. (2000). „How long does it take to stop?“ Transportation Human Factors 2(3) — reaktsiooniaeg: valmis juht u 0,7 s, ootamatu oht u 1,25–1,5 s")}</li>
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
