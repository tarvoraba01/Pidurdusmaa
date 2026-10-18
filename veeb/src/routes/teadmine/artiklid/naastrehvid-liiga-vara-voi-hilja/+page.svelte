<script>
	/* Naastrehvid liiga vara või hilja? Soe asfalt ja aprill
	   Artiklite partii 18.10.2026 (mustandid: 2ND Brain, Pidurdusmaa.ee/01 Articles, „(C) 03 Naastrehvid liiga vara või liiga hilja - soe asfalt, aprill ja reeglid“).
	   Seadused ja testid: allikad lehe lõpus. Pidurdusmaad: sama mudel mis kalkulaator (engine.js),
	   VW Golf 8, 205/55 R16; numbrid kontrollitud mudeliga 18.10.2026. Lehe tekst on genereeritud
	   mustandist (scratchpad md2page.py), parandused tee siin otse. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'naastrehvid-liiga-vara-voi-hilja';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const SISU = `<p>Naastrehve võib Eestis kasutada 15. oktoobrist 31. märtsini. Kui teel on talvised olud, võib neid kasutada ka 1. oktoobrist 30. aprillini. Liiga vara alla pandud naastrehv ei ole ohtlik naastude pärast, vaid seetõttu, et talverehvi pehme kumm pidurdab soojal kuival asfaldil kehvemini kui suverehv.</p>
<p>Allpool on numbrid ja lihtne reegel, kuidas õige hetk valida.</p>
<h2>Kas 1. oktoobril võib naastrehvidega sõita?</h2>
<p>Ainult siis, kui on talvised tee- või ilmaolud. Ilma nendeta algab naastrehvide aeg 15. oktoobril.</p>
<p>Talviseid olusid keegi eraldi välja ei kuuluta. Transpordiamet on öelnud, et iga juht otsustab oma sõiduvajaduse ja ilma järgi. Kui politsei peatab, vaatab ta juhtumit eraldi. Kui oktoobri alguses on öösel jää ja sa sõidad varahommikul maanteel, on naastud ilmselt põhjendatud. Kui on +12 °C ja päike, ei ole.</p>
<h2>Mis juhtub, kui naastrehvid on soojal asfaldil?</h2>
<p>Kaks asja: pidurdusmaa pikeneb ja rehv kulub.</p>
<p><strong>Pidurdus.</strong> Probleem on pigem kummis kui naastudes. Talverehvi kumm on mõeldud külma jaoks ja muutub soojas liiga pehmeks. Pidurdusmaa.ee arvutuse järgi peatub VW Golf kuival asfaldil +25 °C juures 90 km/h pealt suverehviga 28,6 m ja Põhjamaade talverehviga 42,0 m. See on ligi poole võrra pikem.</p>
<p>Oktoobris on asfalt jahedam ja vahe väiksem. Soome ajakirja Tekniikan Maailma 2025. aasta testis pidurdasid naastrehvid kuival asfaldil 80 km/h pealt keskmiselt 32,2 m ja Põhjamaade lamellid 31,5 m. Märjal asfaldil olid naastrehvid isegi veidi paremad, 36,9 m ja 38,7 m. Seega naast ise pidurdust asfaldil palju ei halvenda. Suurem vahe on talverehvi ja suverehvi vahel.</p>
<p><strong>Kulumine.</strong> Paljal asfaldil kulub nii rehv kui tee. Tallinna linn on öelnud, et lumeta teedel rebivad naastrehvid asfalti lahti ja kõige hullem on see sulanud teedel. Helsingi uuringu järgi, millele Tallinn viitas, tuleb umbes 75% Helsingi piirkonna tänavatolmust naastrehvidest.</p>
<h2>Kas naastrehvid tasub siis panna alla võimalikult hilja?</h2>
<p>Ei. Naastu suurim eelis on just esimesel jääl, kui temperatuur on nulli lähedal. Pidurdusmaa.ee arvutuse järgi pidurdab VW Golf 0 °C jääl 50 km/h pealt naastrehviga umbes 61 m, Põhjamaade lamelliga umbes 100 m ja Kesk-Euroopa talverehviga umbes 182 m.</p>
<p>Esimene öökülm tuleb Eestis tihti oktoobris. Sild või metsavahe võib olla jääs ka siis, kui linnas on asfalt kuiv.</p>
<p>Transpordiamet soovitab rehvid vahetada enne esimesi miinuskraade. Ameti andmetel kaotab suverehvi kumm elastsuse juba +5 kuni +8 kraadi juures.</p>
<h2>Kuidas valida õige hetk?</h2>
<p>Lihtne rusikareegel:</p>
<ul><li><strong>Pane naastud alla</strong>, kui päeval on alla +7 °C ja öösel on külm, või kui ilmateade lubab öökülma. Eriti siis, kui sõidad maanteel, varahommikul või üle sildade.</li><li><strong>Võid veel oodata</strong>, kui sõidad ainult linnas puhastatud tänavatel ja ööd on soojad. Siis võib olla mõistlik kaaluda Põhjamaade lamellrehvi.</li><li><strong>Ära pane alla</strong>, kui on 1. kuni 14. oktoober ja teel ei ole talviseid olusid.</li></ul>
<p>Pikemalt temperatuuridest loe artiklist <a href="/teadmine/artiklid/millal-talverehvid-alla/">Millal talverehvid alla</a>.</p>
<h2>Mis saab kevadel? Kas aprillis tohib naastudega sõita?</h2>
<p>Tavaliselt lõpeb naastude aeg 31. märtsiga. Kui aprillis on talvised olud, võib nendega sõita kuni 30. aprillini. Ka siin otsustab juht ise ilma järgi.</p>
<p>Alates 1. maist on naastrehvid keelatud igal juhul. Politsei on varem öelnud, et vaatab iga rikkumist eraldi ja kohe pärast tähtaega pigem soovitab rehvid ära vahetada, kui trahvib. Ära sellele siiski looda.</p>
<p>Kevadel on soe asfalt sama probleem mis sügisel. Kui öökülmad on läbi, vaheta. Ülejäänud kevadised kuupäevad on lehel <a href="/teadmine/rehvivahetus/">Rehvivahetus 2026</a>.</p>
<h2>Kas lamellrehv lahendab ajastuse mure?</h2>
<p>Osaliselt. Lamellrehvil kuupäevapiirangut ei ole, nii et sa ei pea oktoobris kalendrit jälgima. Jääl jääb lamell naastule alla, eriti nulli lähedal. Lumel ja kuival asfaldil on vahe alla meetri. Täpsed numbrid on artiklis <a href="/teadmine/artiklid/naastrehv-voi-lamell/">Naastrehv või lamell</a>.</p>
<h2>Vaata, kuidas sinu auto pidurdab</h2>
<p>Õige aeg sõltub sinu teedest ja sinu rehvist. <a href="/autod/">Kirjuta oma auto mark ja vaata talverehvide pidurdusmaid ja hindu</a> või proovi <a href="/">pidurdusmaa kalkulaatorit</a> eri tingimustes.</p>
<p class="note">Allikad: <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://www.err.ee/1609133201/puhapaevast-alates-voib-soita-naastrehvidega" rel="noopener">ERR 15.10.2023</a>, <a href="https://www.err.ee/1609297662/naastrehvidega-tohib-soita-kuni-aprilli-lopuni" rel="noopener">ERR 29.03.2024</a>, <a href="https://www.err.ee/1082518/maist-naastrehvidega-enam-soita-ei-tohi" rel="noopener">ERR 26.04.2020</a>, <a href="https://www.err.ee/870174/tallinna-linnavoim-kutsub-eelistama-naastrehvidele-lamellrehve" rel="noopener">ERR 18.10.2018</a>, <a href="https://www.err.ee/1065555/soe-talv-tanavatel-on-lume-asemel-naastrehvide-rebitud-asfalditolm" rel="noopener">ERR 18.03.2020</a>.</p>`;

	const SISU_RU = `<p>В Эстонии шипованную резину можно использовать с 15 октября по 31 марта, а при зимних условиях на дороге также с 1 октября по 30 апреля. Слишком ранние шипы плохи не из-за самих шипов, а из-за того, что мягкая зимняя резина на тёплом сухом асфальте тормозит хуже летней.</p>
<p>Ниже цифры и простое правило, как выбрать момент.</p>
<h2>Можно ли ездить на шипах 1 октября?</h2>
<p>Только при зимних дорожных или погодных условиях. Без них шипы разрешены с 15 октября.</p>
<p>Никто официально «зимние условия» не объявляет. В Transpordiamet говорили, что каждый водитель решает сам, глядя на погоду и свои поездки. Если остановит полиция, случай рассмотрят отдельно. Если в начале октября ночью был гололёд, а вы рано утром едете по трассе, шипы, скорее всего, обоснованы. Если плюс 12 и солнце, нет.</p>
<h2>Что происходит с шипами на тёплом асфальте?</h2>
<p>Две вещи: тормозной путь растёт и шина изнашивается.</p>
<p><strong>Торможение.</strong> Дело скорее в резине, чем в шипах. Зимняя резиновая смесь рассчитана на холод и в тепле становится слишком мягкой. По расчёту Pidurdusmaa.ee VW Golf на сухом асфальте при +25 °C с 90 км/ч останавливается на летней резине за 28,6 м, а на северной липучке за 42,0 м. Это почти в полтора раза длиннее.</p>
<p>В октябре асфальт прохладнее, и разница меньше. В тесте финского журнала Tekniikan Maailma 2025 года шипованные шины тормозили на сухом асфальте с 80 км/ч в среднем за 32,2 м, а северные липучки за 31,5 м. На мокром асфальте шипы были даже чуть лучше: 36,9 м против 38,7 м. То есть на торможение по асфальту сами шипы почти не влияют. Гораздо больше разница между зимней и летней резиной.</p>
<p><strong>Износ.</strong> На голом асфальте изнашиваются и шина, и дорога. Таллиннские власти говорили, что на дорогах без снега шипы рвут асфальт, хуже всего на оттаявших дорогах. По данным исследования из Хельсинки, на которое ссылался Таллинн, около 75% уличной пыли в районе Хельсинки дают шипованные шины.</p>
<h2>Значит, шипы лучше ставить как можно позже?</h2>
<p>Нет. Сильнее всего шипы выигрывают именно на первом льду, когда около нуля. По расчёту Pidurdusmaa.ee VW Golf на льду при 0 °C с 50 км/ч останавливается на шипах примерно за 61 м, на северной липучке примерно за 100 м, а на центральноевропейской зимней шине примерно за 182 м.</p>
<p>Первые ночные заморозки в Эстонии часто бывают в октябре. Мост или участок у леса может обледенеть, даже если в городе асфальт сухой.</p>
<p>Transpordiamet советует менять резину до первых минусовых температур. По данным ведомства, летняя резина теряет эластичность уже при температуре от +5 до +8 градусов.</p>
<h2>Как выбрать момент?</h2>
<p>Простое правило:</p>
<ul><li><strong>Ставьте шипы</strong>, если днём ниже +7 °C и ночью холодно, или обещают заморозки. Особенно если ездите по трассе, рано утром или через мосты.</li><li><strong>Можно подождать</strong>, если ездите только по расчищенным городским улицам и ночи тёплые. Тогда стоит подумать о северной липучке.</li><li><strong>Не ставьте</strong>, если на календаре с 1 по 14 октября и на дороге нет зимних условий.</li></ul>
<p>Подробнее о температурах в статье <a href="/ru/teadmine/artiklid/millal-talverehvid-alla/">Когда ставить зимние шины</a>.</p>
<h2>А весной? Можно ли ездить на шипах в апреле?</h2>
<p>Обычно ездить на шипах можно по 31 марта включительно. Если в апреле зимние условия, на них можно ездить по 30 апреля. Решает здесь тоже сам водитель, глядя на погоду.</p>
<p>С 1 мая шипы запрещены в любом случае. Полиция раньше говорила, что рассматривает каждый случай и сразу после срока скорее советует сменить резину, чем штрафует. Но рассчитывать на это не стоит.</p>
<p>Весной с тёплым асфальтом та же проблема, что и осенью. Как только закончатся ночные заморозки, меняйте резину. Остальные весенние сроки на странице <a href="/ru/teadmine/rehvivahetus/">Смена резины 2026</a>.</p>
<h2>Решает ли липучка проблему со сроками?</h2>
<p>Частично. Для липучки нет ограничений по датам, за календарём следить не нужно. На льду она уступает шипам, особенно около нуля. На снегу и сухом асфальте разница меньше метра. Цифры в статье <a href="/ru/teadmine/artiklid/naastrehv-voi-lamell/">Шипы или липучка</a>.</p>
<h2>Посмотрите, как тормозит ваша машина</h2>
<p>Правильный момент зависит от ваших дорог и ваших шин. <a href="/ru/autod/">Введите марку своей машины и посмотрите тормозной путь и цены зимних шин</a> или попробуйте <a href="/ru/">калькулятор тормозного пути</a> в разных условиях.</p>
<p class="note">Источники: <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://www.err.ee/1609133201/puhapaevast-alates-voib-soita-naastrehvidega" rel="noopener">ERR 15.10.2023</a>, <a href="https://www.err.ee/1609297662/naastrehvidega-tohib-soita-kuni-aprilli-lopuni" rel="noopener">ERR 29.03.2024</a>, <a href="https://www.err.ee/1082518/maist-naastrehvidega-enam-soita-ei-tohi" rel="noopener">ERR 26.04.2020</a>, <a href="https://www.err.ee/870174/tallinna-linnavoim-kutsub-eelistama-naastrehvidele-lamellrehve" rel="noopener">ERR 18.10.2018</a>, <a href="https://www.err.ee/1065555/soe-talv-tanavatel-on-lume-asemel-naastrehvide-rebitud-asfalditolm" rel="noopener">ERR 18.03.2020</a>.</p>`;

	const KKK = [
		[
		 "Kas 10. oktoobril võib naastrehvidega sõita?",
		 "Ainult talvistes tee- või ilmaoludes. Muidu algab naastrehvide aeg 15. oktoobril."
		],
		[
		 "Kas naastrehvid kuluvad soojal asfaldil kiiremini?",
		 "Paljal asfaldil kuluvad nii rehv kui teepind kiiremini. Pidurdusele mõjub soojus aga rohkem kummi kui naastude kaudu."
		],
		[
		 "Kas 15. aprillil võib naastrehvidega sõita?",
		 "Kui on talvised olud, siis jah, kuni 30. aprillini. Kui teed on kuivad ja soojad, siis mitte."
		],
		[
		 "Kas naastrehvid tasub juba oktoobri keskel alla panna?",
		 "Kui sõidad maanteel või varahommikul ja ööd on külmad, siis jah. Linnasõiduks soojal sügisel võib oodata."
		]
];
	const KKK_RU = [
		[
		 "Можно ли ездить на шипах 10 октября?",
		 "Только при зимних дорожных или погодных условиях. Иначе шипы разрешены с 15 октября."
		],
		[
		 "Быстрее ли изнашиваются шипованные шины на тёплом асфальте?",
		 "На голом асфальте быстрее изнашиваются и шина, и покрытие. А на торможение тепло влияет больше через резину, чем через шипы."
		],
		[
		 "Можно ли ездить на шипах 15 апреля?",
		 "Если зимние условия, да, по 30 апреля. Если дороги сухие и тепло, нет."
		],
		[
		 "Стоит ли ставить шипы уже в середине октября?",
		 "Если ездите по трассе или рано утром и ночи холодные, да. Для города в тёплую осень можно подождать."
		]
];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	h1={T.h1}
	desc={T.desc}
	path="teadmine/artiklid/naastrehvid-liiga-vara-voi-hilja/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/naastrehvid-liiga-vara-voi-hilja/']]}
	lapsed={[]}
	uuendatud={A.uuendatud || A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/naastrehvid-liiga-vara-voi-hilja.png"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
