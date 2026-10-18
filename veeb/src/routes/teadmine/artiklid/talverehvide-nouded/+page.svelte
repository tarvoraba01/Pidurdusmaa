<script>
	/* Talverehvide nõuded 2026: muster, märk, naastud ja trahv
	   Artiklite partii 18.10.2026 (mustandid: 2ND Brain, Pidurdusmaa.ee/01 Articles, „(C) 01 Talverehvide nõuded 2026 - mis on kohustuslik ja mis ähvardab“).
	   Seadused ja testid: allikad lehe lõpus. Pidurdusmaad: sama mudel mis kalkulaator (engine.js),
	   VW Golf 8, 205/55 R16; numbrid kontrollitud mudeliga 18.10.2026. Lehe tekst on genereeritud
	   mustandist (scratchpad md2page.py), parandused tee siin otse. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'talverehvide-nouded';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const SISU = `<p>Eestis peab sõiduautol 1. detsembrist 1. märtsini olema talverehv, mille mustri jääksügavus on vähemalt 3 mm. Naastudeta talverehvil peab olema kolme mäetipu ja lumehelbe märk (3PMSF) ning naastrehvid peavad olema kõigil ratastel.</p>
<p>Täpsed kuupäevad on lehel <a href="/teadmine/rehvivahetus/">Rehvivahetus 2026</a>. Siin on kõik muu, mida politsei või ülevaataja rehvi juures vaatab.</p>
<h2>Millistele sõidukitele talverehvi nõue kehtib?</h2>
<p>Nõue kehtib sõiduautole (M1), kuni 3,5-tonnisele kaubikule (N1) ja haagisele, mille registrimass on üle 0,75 ja kuni 3,5 tonni (O2). Kerge haagis kuni 750 kg ei ole selles loetelus.</p>
<p>Nõue on kalendri järgi. See tähendab, et 1. detsembril peab talverehv all olema ka siis, kui teed on kuivad ja väljas on plusskraadid.</p>
<h2>Kui sügav peab olema talverehvi muster?</h2>
<p>Talverehvi mustri jääksügavus peab olema vähemalt 3 mm. Suverehvil on miinimum 1,6 mm.</p>
<p>3 mm on seaduse alampiir, mitte ohutu piir. Pidurdusmaa.ee arvutuse järgi pidurdab 3 mm mustriga Põhjamaade lamellrehv lumel 50 km/h pealt umbes 33 m, uus rehv umbes 26 m. Vahe on veidi üle veerandi. Kui sinu rehvil on sügisel 4 mm või vähem, on mõistlik uued osta enne lund. Tabel on artiklis <a href="/teadmine/artiklid/vanad-ja-kulunud-rehvid/">Vanad ja kulunud rehvid</a>.</p>
<p>Mõõda mustrit mitmest kohast ja arvesta kõige kulunumat kohta. Paljudel rehvidel on soones ka kulumisnäidik.</p>
<h2>Milline märk peab rehvil olema?</h2>
<p>Alates 1. detsembrist 2022 peab naastudeta talverehvil olema 3PMSF märk, ehk kolm mäetippu ja lumehelves. See märk antakse rehvile, mis on lumel testi läbinud (UNECE eeskiri nr 117).</p>
<p>Ainult M+S märgiga lamellrehv talvisel perioodil enam ei sobi. Ministeerium on öelnud, et M+S rehv sobib nulli lähedasel temperatuuril, aga mitte lumele ega jääle. Erand on maastikurehvid märgiga POR.</p>
<p>Transpordiamet soovitab lisaks valida rehvi, millel on ka jäähaarduvuse märk. See näitab, et rehv on läbinud jäätesti. Märkide kohta loe lähemalt <a href="/teadmine/rehvimargis/">rehvimärgise lehelt</a>.</p>
<h2>Kas naastrehvid peavad olema kõigil ratastel?</h2>
<p>Jah. Kui kasutad naastrehve, peavad need olema kõigil neljal rattal. Naastrehvid ees ja lamellid taga, või vastupidi, ei ole lubatud.</p>
<p>Ka lamellrehvide puhul on mõistlik panna kõigile ratastele sama mudel. Sama telje rehvid peavad olema sama mustri ja kulumisega.</p>
<h2>Kas lamellrehviga tohib suvel sõita?</h2>
<p>Tohib. Naastudeta talverehvil kuupäevapiirangut ei ole. Naastrehvidega võib aga sõita ainult 31. märtsini, talviste olude korral 30. aprillini.</p>
<p>Lubatud ei tähenda, et see on hea. Pidurdusmaa.ee arvutuse järgi peatub VW Golf kuival asfaldil +25 °C juures 90 km/h pealt suverehviga 28,6 m ja Põhjamaade talverehviga 42,0 m. See on ligi poole võrra pikem.</p>
<h2>Mis juhtub, kui politsei peatab sind detsembris suverehvidega?</h2>
<p>Politsei kontrollib talverehve igal talvel alates 1. detsembrist. Eraldi „rehvitrahvi“ seaduses ei ole. Rikkumist menetletakse liiklusseaduse § 242 lõike 1 alusel, mis käsitleb seda, kui juht rikub liiklusnõudeid. Seda saab lahendada ka lühimenetluses. See tähendab, et trahvi võib saada kohe kohapeal.</p>
<p>Trahv on kuni 20 trahviühikut. Alates 2025. aastast on üks trahviühik 8 eurot, nii et trahv võib olla kuni 160 eurot. Politsei hindab iga juhtumit eraldi. Kui rikkumisega tekitati liiklusoht, on ülempiir palju kõrgem: kuni 100 trahviühikut ehk 800 eurot või juhtimisõiguse äravõtmine kuni kuueks kuuks.</p>
<p>Suurem oht kui trahv on see, et lumel võib suverehviga auto pidurdusmaa olla üle kahe korra pikem. Pidurdusmaa.ee arvutuse järgi on see 50 km/h pealt suverehviga 60,9 m ja talverehviga 26,2 m.</p>
<h2>Kes otsustab, kas on „talvised olud“?</h2>
<p>Sina ise. Naastrehve võib kasutada 1. oktoobrist 30. aprillini, kui on talvised tee- või ilmastikuolud. Keegi seda eraldi välja ei kuuluta. Transpordiamet on öelnud, et iga juht otsustab oma sõiduvajaduse ja ilma järgi. Politsei hindab iga juhtumit eraldi ja vaatab, kas naastud olid põhjendatud.</p>
<h2>Kokkuvõte: kontrolli need 4 asja</h2>
<ol><li>Talverehv all 1. detsembriks.</li><li>Muster vähemalt 3 mm, parem 5 mm või rohkem.</li><li>Lamellil 3PMSF märk, soovitavalt ka jäämärk.</li><li>Naastrehvid kõigil ratastel, mitte segamini.</li></ol>
<h2>Vaata oma auto talverehve</h2>
<p>Seadus paneb paika ainult miinimumi. Kui hästi sinu auto talvel pidurdab, sõltub rehvist. <a href="/autod/">Kirjuta oma auto mark ja vaata talverehvide pidurdusmaid ja hindu</a> või otsi <a href="/talverehvid/">talverehve oma mõõdu järgi</a>.</p>
<p class="note">Allikad: <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://liikluskool.ee/16-tehnoseisund-ja-muud-valdkonnad/" rel="noopener">Liikluskool</a>, <a href="https://www.transpordiamet.ee/media/636/download" rel="noopener">Transpordiamet</a>, <a href="https://www.err.ee/1007161/kolme-aasta-parast-on-eestis-louna-euroopa-lamellrehvid-keelatud" rel="noopener">ERR 26.11.2019</a>, <a href="https://www.tehnoulevaatus.ee/talverehvide-nouete-muudatus/" rel="noopener">Tehnoülevaatus</a>, <a href="https://www.err.ee/1609133201/puhapaevast-alates-voib-soita-naastrehvidega" rel="noopener">ERR 15.10.2023</a>, <a href="https://www.err.ee/1609297662/naastrehvidega-tohib-soita-kuni-aprilli-lopuni" rel="noopener">ERR 29.03.2024</a>, <a href="https://www.err.ee/1082518/maist-naastrehvidega-enam-soita-ei-tohi" rel="noopener">ERR 26.04.2020</a>, <a href="https://www.err.ee/1608419693/politsei-kontrollis-parnus-talverehvide-kasutamist" rel="noopener">ERR 29.11.2021</a>, <a href="https://cms.advokatuur.ee/app/uploads/2024/03/KarS-muutmine-jt-seaduste-muutmine-trahviuhiku-tostmine-2024-SELETUSKIRI.pdf" rel="noopener">Justiitsministeeriumi seletuskiri</a>, <a href="https://www.err.ee/1609369370/riigikogu-vottis-vastu-trahve-ja-riigiloive-tostvad-seadused" rel="noopener">ERR 12.06.2024</a>.</p>`;

	const SISU_RU = `<p>В Эстонии с 1 декабря по 1 марта на легковой машине должна стоять зимняя резина с остаточной глубиной протектора не меньше 3 мм. На нешипованной резине («липучке») должен быть знак с тремя горными вершинами и снежинкой (3PMSF), а шипованные шины ставятся только на все четыре колёса.</p>
<p>Точные даты смены резины собраны на странице <a href="/ru/teadmine/rehvivahetus/">Смена резины 2026</a>. Здесь всё остальное, на что смотрят полиция и техосмотр.</p>
<h2>На какие машины распространяется требование?</h2>
<p>Требование распространяется на легковые автомобили (M1), фургоны до 3,5 тонны (N1) и прицепы с регистрационной массой более 0,75 и до 3,5 тонны (O2). Лёгкого прицепа до 750 кг в этом списке нет.</p>
<p>Требование привязано к календарю. Даже если 1 декабря сухо и плюс, зимняя резина уже должна стоять.</p>
<h2>Какой минимальный протектор у зимней резины?</h2>
<p>Не меньше 3 мм. Для летней резины минимум 1,6 мм.</p>
<p>Закон требует минимум 3 мм, но это не безопасный запас. По расчёту Pidurdusmaa.ee северная липучка с протектором 3 мм останавливается на снегу с 50 км/ч примерно за 33 м, а новая примерно за 26 м. Разница больше четверти. Если осенью на шине 4 мм или меньше, лучше купить новый комплект до снега. Таблица есть в статье <a href="/ru/teadmine/artiklid/vanad-ja-kulunud-rehvid/">Старые и изношенные шины</a>.</p>
<p>Мерить протектор нужно в нескольких местах и ориентироваться на самое изношенное. На многих шинах в канавке есть и индикатор износа.</p>
<h2>Какая маркировка должна быть на шине?</h2>
<p>С 1 декабря 2022 года на нешипованной зимней шине обязателен знак 3PMSF. Его получает шина, которая прошла тест на снегу по правилам ООН (UNECE R117).</p>
<p>Липучка только с маркировкой M+S в зимний период больше не подходит. Министерство объясняло, что M+S годится для температуры около нуля, но не для снега и льда. Исключение только для внедорожных шин с маркировкой POR.</p>
<p>Transpordiamet советует дополнительно выбирать шину со знаком сцепления на льду. Он показывает, что шина прошла тест на льду. Подробнее на странице <a href="/ru/teadmine/rehvimargis/">маркировка шин ЕС</a>.</p>
<h2>Нужно ли ставить шипы на все колёса?</h2>
<p>Да. Если ездите на шипованной резине, она должна стоять на всех колёсах. Шипы спереди и липучка сзади, или наоборот, запрещены.</p>
<p>С липучкой тоже разумно ставить одну модель на все колёса. На одной оси шины должны быть с одинаковым рисунком и износом.</p>
<h2>Можно ли ездить летом на липучке?</h2>
<p>Можно, ограничений по датам для нешипованной резины нет. На шипах же можно ездить только по 31 марта, а при зимних условиях по 30 апреля.</p>
<p>Но «можно» не значит «хорошо». По расчёту Pidurdusmaa.ee VW Golf на сухом асфальте при +25 °C с 90 км/ч останавливается на летней резине за 28,6 м, а на северной липучке за 42,0 м. Это почти в полтора раза длиннее.</p>
<h2>Что будет, если в декабре остановят на летней резине?</h2>
<p>Полиция каждую зиму проверяет резину с 1 декабря. Отдельного «штрафа за резину» в законе нет. Нарушение рассматривается по части 1 § 242 закона о дорожном движении (нарушение водителем правил дорожного движения), его можно оформить в упрощённом порядке, то есть штраф могут выписать сразу на месте.</p>
<p>Штраф составляет до 20 штрафных единиц. С 2025 года одна единица равна 8 евро, то есть штраф может достигать 160 евро. Полиция рассматривает каждый случай отдельно. Если нарушение создало опасность на дороге, верхний предел намного выше: до 100 единиц, то есть 800 евро, или лишение прав на срок до шести месяцев.</p>
<p>Опаснее штрафа другое: на снегу тормозной путь на летней резине может быть больше чем вдвое длиннее. По расчёту Pidurdusmaa.ee с 50 км/ч это 60,9 м на летней резине против 26,2 м на зимней.</p>
<h2>Кто решает, что наступили «зимние условия»?</h2>
<p>Вы сами. Шипы разрешены с 1 октября по 30 апреля при зимних дорожных или погодных условиях. Никто это официально не объявляет. В Transpordiamet говорили, что каждый водитель решает сам, глядя на погоду и свои поездки. Полиция рассматривает каждый случай и проверяет, было ли это обоснованно.</p>
<h2>Коротко: проверьте 4 вещи</h2>
<ol><li>Зимняя резина стоит к 1 декабря.</li><li>Протектор от 3 мм, лучше 5 мм и больше.</li><li>На липучке знак 3PMSF, желательно и знак льда.</li><li>Шипы на всех колёсах, без смешивания.</li></ol>
<h2>Посмотрите зимнюю резину для своей машины</h2>
<p>Закон задаёт только минимум. Как ваша машина тормозит зимой, зависит от конкретной шины. <a href="/ru/autod/">Введите марку своей машины и посмотрите тормозной путь и цены зимних шин</a> или найдите <a href="/ru/talverehvid/">зимние шины по размеру</a>.</p>
<p class="note">Источники: <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://liikluskool.ee/16-tehnoseisund-ja-muud-valdkonnad/" rel="noopener">Liikluskool</a>, <a href="https://www.transpordiamet.ee/media/636/download" rel="noopener">Transpordiamet</a>, <a href="https://www.err.ee/1007161/kolme-aasta-parast-on-eestis-louna-euroopa-lamellrehvid-keelatud" rel="noopener">ERR 26.11.2019</a>, <a href="https://www.tehnoulevaatus.ee/talverehvide-nouete-muudatus/" rel="noopener">Tehnoülevaatus</a>, <a href="https://www.err.ee/1609133201/puhapaevast-alates-voib-soita-naastrehvidega" rel="noopener">ERR 15.10.2023</a>, <a href="https://www.err.ee/1609297662/naastrehvidega-tohib-soita-kuni-aprilli-lopuni" rel="noopener">ERR 29.03.2024</a>, <a href="https://www.err.ee/1082518/maist-naastrehvidega-enam-soita-ei-tohi" rel="noopener">ERR 26.04.2020</a>, <a href="https://www.err.ee/1608419693/politsei-kontrollis-parnus-talverehvide-kasutamist" rel="noopener">ERR 29.11.2021</a>, <a href="https://cms.advokatuur.ee/app/uploads/2024/03/KarS-muutmine-jt-seaduste-muutmine-trahviuhiku-tostmine-2024-SELETUSKIRI.pdf" rel="noopener">Пояснительная записка Минюста</a>, <a href="https://www.err.ee/1609369370/riigikogu-vottis-vastu-trahve-ja-riigiloive-tostvad-seadused" rel="noopener">ERR 12.06.2024</a>.</p>`;

	const KKK = [
		[
		 "Kas talverehvi minimaalne mustri sügavus on 3 mm või 4 mm?",
		 "Eestis on see 3 mm. Lätis on talverehvi miinimum 4 mm, sellest tekibki segadus. Ohutuse mõttes tasub rehv vahetada hiljemalt siis, kui mustrit on alles 4 mm."
		],
		[
		 "Kas M+S rehv on talverehv?",
		 "Talvisel perioodil mitte. Naastudeta talverehvil peab olema 3PMSF märk. Ainult M+S märgist ei piisa."
		],
		[
		 "Kas haagisel peavad olema talverehvid?",
		 "Haagisel registrimassiga üle 0,75 ja kuni 3,5 tonni peavad. Kerge haagise kohta (kuni 750 kg) see nõue ei kehti."
		],
		[
		 "Mis siis, kui varurattal on suverehv?",
		 "Varuratas on mõeldud ajutiseks sõiduks pärast rehvi purunemist, et jõuda töökotta. Kontrolli oma auto juhendist varuratta kiiruspiirangut ja vaheta rehv esimesel võimalusel."
		]
];
	const KKK_RU = [
		[
		 "Минимальный протектор зимней резины 3 мм или 4 мм?",
		 "В Эстонии 3 мм. В Латвии для зимних шин нужно минимум 4 мм, отсюда путаница. Для безопасности шину лучше менять, когда протектор дошёл до 4 мм."
		],
		[
		 "Считается ли M+S зимней резиной?",
		 "В зимний период нет. На нешипованной зимней шине должен быть знак 3PMSF, одного M+S недостаточно."
		],
		[
		 "Нужна ли прицепу зимняя резина?",
		 "Прицепу с регистрационной массой более 0,75 и до 3,5 тонны нужна. Лёгкому прицепу до 750 кг нет."
		],
		[
		 "Что, если на запаске летняя шина?",
		 "Запасное колесо рассчитано на временную езду после повреждения шины, чтобы доехать до мастерской. Ограничение скорости смотрите в инструкции к машине и меняйте шину при первой возможности."
		]
];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	h1={T.h1}
	desc={T.desc}
	path="teadmine/artiklid/talverehvide-nouded/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/talverehvide-nouded/']]}
	lapsed={[]}
	uuendatud={A.uuendatud || A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/talverehvide-nouded.png"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
