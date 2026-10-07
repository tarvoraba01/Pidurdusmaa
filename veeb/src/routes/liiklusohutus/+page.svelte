<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ =
		t('Tasuta peatumisteekonna kalkulaator: vaata, kuidas kiirus, reaktsiooniaeg, teeolud ja rehvid muudavad peatumismaad. Kaks olukorda kõrvuti, ilma reklaamita.');
	const jsonld = graph(tooriist(t('Peatumisteekonna kalkulaator'), '/liiklusohutus/', KIRJ, keel.lang), ORG);
</script>

<Meta title={t("Peatumisteekonna kalkulaator")} desc={KIRJ} path="liiklusohutus/" {jsonld} image="/og/sait/liiklusohutus.png" />

<LiiklusLeht
	kick={t("Liiklusohutus · tasuta, ilma reklaamita")}
	h1={t("Kui pika maa pealt auto peatub?")}
	lead={t("50 km/h pealt peatub auto kuival teel umbes 24 meetriga, märjal 27 meetriga; 90 km/h pealt 55 ja 70 meetriga. Muuda kiirust, reaktsiooniaega, teeolusid ja rehve ning vaata kohe, kuidas peatumisteekond muutub.")}
	vaade="peatumine"
>

		<div>
			<h2>{t("Mida proovida")}</h2>
			<ul>
				<li>
					{@html t("<b>Kiirus.</b> Vali „50 vs 70 km/h“. Takistus on pandud kohta, kus 50 km/h auto peatub — vaata, millise kiirusega 70 km/h auto sinna jõuab.")}
				</li>
				<li>
					{@html t("<b>Tähelepanu.</b> Reaktsiooniaja ajal sõidab auto täiskiirusel edasi. 50 km/h juures on iga lisasekund umbes 14 meetrit.")}
				</li>
				<li>
					{@html t("<b>Rehvid ja ilm.</b> Mustrisügavus loeb eriti märjal teel; suverehv lumel ja sulav jää nulli lähedal on kõige ohtlikumad olukorrad.")}
				</li>
				<li>
					{@html t("<b>Pimedas.</b> Vali „Jalakäija pimedas“: tumedates riietes helkurita jalakäijat märkab juht lähitulede valgel alles umbes 30 m kauguselt. Vaata, millise kiirusega jõuad veel peatuda.")}
				</li>
				<li>
					{@html t("<b>Pikivahe.</b> Kui eesolev auto pidurdab järsult, kas 1, 2 või 3 sekundit vahet on piisav? Kui reageerimisaeg on pikivahest pikem, tuleb kokkupõrge.")}
				</li>
				<li>
					{@html t("<b>Kurv ja rehvid.</b> „Auto käitumine pidurdamisel“ näitab, mis juhtub kurvis, kui paremad rehvid on ees või taga.")}
				</li>
				<li>
					{@html t("<b>Esitlus.</b> „Esitlusrežiim“ avab kalkulaatori täisekraanil. „Kopeeri link“ salvestab kõik valikud aadressi sisse — saad olukorra kellelegi saata või esitluseks ette valmistada.")}
				</li>
			</ul>
		</div>
		<div>
			<h2>{t("Mida arvutus arvestab")}</h2>
			<p>
				{t("Pidurdus arvutatakse väikeste ajasammudega: rehvi ja tee haare antud kiirusel ja temperatuuril, ABS, pidurite võimekus, koormus, õhutakistus ja tee kalle. Mudel on kalibreeritud 369 mõõdetud pidurdusmaa järgi sõltumatutest rehvitestidest ja kontrollitud veel umbes 1300 ajakirjade testitulemusega.")}
			</p>
			<p>
				{@html t("<b>Tulemus on hinnang, mitte mõõtmine.</b> Iga tulemuse juures on tõenäoline vahemik. Päris pidurdusmaa sõltub ka konkreetsest rehvist, teekattest ja juhist. Jää tähendab tavalist sõidutee jääd; siledal kiilasjääl on pidurdusmaa pikem (vali „Sile jää“).")}
			</p>
		</div>
		<div>
			<h2>{t("Allikad")}</h2>
			<ul class="lo-src">
				<li>{t("ADAC, Tekniikan Maailma, UTAC, Vi Bilägare, Auto Bild, Za Rulem jt — sõltumatud rehvitestid")}</li>
				<li>{t("EL-i tooteregister EPREL ja rehvimärgise katsemeetod UNECE R117")}</li>
				<li>{t("DEKRA — mustrisügavuse mõju märjal teel")}</li>
				<li>
					{t("Green, M. (2000). „How long does it take to stop?“ Transportation Human Factors 2(3) — reaktsiooniaeg: valmis juht u 0,7 s, ootamatu oht u 1,25–1,5 s")}
				</li>
				<li>{t("VTI (Rootsi), Statens vegvesen (Norra), Maanteeamet — haardetegur sõiduteede jääl")}</li>
				<li>{t("Transpordiamet (2025) — jalakäija nähtavus pimedas helkuriga ja ilma")}</li>
				<li>{t("ADAC, TCS, ÖAMTC — paremad rehvid tagasillale (katsed märjal teel)")}</li>
			</ul>
			<p class="lo-small">
				{t("Tööriist on tasuta kõigile — juhtidele, lapsevanematele, koolidele ja autokoolidele. Lehel ei ole reklaami, hindu ega poode.")}
			</p>
		</div>
</LiiklusLeht>
