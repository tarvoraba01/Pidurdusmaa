<script>
	/* Kasutatud talverehvid: 7 asja, mida enne ostu kontrollida
	   Artiklite partii 18.10.2026 (mustandid: 2ND Brain, Pidurdusmaa.ee/01 Articles, „(C) 06 Kasutatud talverehvid - mida enne ostu kontrollida“).
	   Seadused ja testid: allikad lehe lõpus. Pidurdusmaad: sama mudel mis kalkulaator (engine.js),
	   VW Golf 8, 205/55 R16; numbrid kontrollitud mudeliga 18.10.2026. Lehe tekst on genereeritud
	   mustandist (scratchpad md2page.py), parandused tee siin otse. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'kasutatud-talverehvid';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const SISU = `<p><strong>Lühike vastus:</strong> kasutatud talverehvi juures kontrolli kõigepealt mustri sügavust (seadus nõuab vähemalt 3 mm), lamellrehvil lumehelbe märki ja tootmisaastat DOT-koodist. Kui üks neist kolmest ei klapi, ei ole rehv odav, vaid lihtsalt vale.</p>
<p>Kasutatud komplekt võib olla mõistlik ost. Aga talverehvil on „kaks kella“: muster kulub ja kumm vananeb. Müüja ütleb harva, et rehv on 9 aastat vana. Selle pead ise välja lugema.</p>
<h2>Kui palju mustrit peab kasutatud talverehvil olema?</h2>
<p>Transpordiamet tuletab igal sügisel meelde: kui ostad kasutatud talverehve, peab mustri jääksügavus olema vähemalt 3 mm. See on seaduse miinimum talveperioodil, mitte hea rehvi tunnus.</p>
<p>Mida vähem mustrit, seda pikem pidurdusmaa lumel. Pidurdusmaa.ee arvutus, Põhjamaade talverehv, 50 km/h lumel:</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th>Muster</th><th class="n">Pidurdusmaa</th></tr></thead><tbody><tr><td><strong>8 mm (uus)</strong></td><td class="n">26,2 m</td></tr><tr><td><strong>6 mm</strong></td><td class="n">28,4 m</td></tr><tr><td><strong>4 mm</strong></td><td class="n">31,1 m</td></tr><tr><td><strong>3 mm</strong></td><td class="n">32,7 m</td></tr></tbody></table></div>
<p>3 mm mustriga on pidurdusmaa lumel umbes veerandi võrra pikem kui uuel rehvil. Märjal asfaldil 90 km/h pealt kasvab see 47,5 meetrilt 54,0 meetrini.</p>
<p><strong>Praktiline mõte:</strong> kui rehvil on 4 kuni 5 mm, jõuab see 3 mm piirini palju varem kui uus rehv. Arvesta seda hinnas.</p>
<p><strong>Kuidas mõõta:</strong> kasuta mustrisügavuse mõõdikut või nihikut. Mõõda mitmest kohast ja mõlemast servast. Kui serv on palju rohkem kulunud kui keskosa, on autol tõenäoliselt olnud vale rõhk või reguleerimata rattad.</p>
<h2>Kuidas näha, kui vana rehv on?</h2>
<p>Otsi küljelt koodi, mis algab tähtedega DOT. Selle koodi lõpus on neljakohaline number. Esimesed kaks numbrit on nädal, viimased kaks aasta. Näiteks 3819 tähendab 2019. aasta 38. nädalat.</p>
<p>Continental soovitab kõik üle 10 aasta vanad rehvid kasutusest kõrvaldada, ka siis, kui need näevad korras välja. Pilk ei näita kõike, sest kumm kõvastub seest. Üle 5 aasta vanu rehve tasub igal aastal kontrollida. Kontrolli vanust kiiresti <a href="/rehvi-vanus/">rehvi vanuse kalkulaatoriga</a>.</p>
<p>Talverehvi puhul on vanus eriti tähtis. Kõvaks läinud kumm haarab külmas ja jääl kehvemini, isegi kui muster on veel sügav. Pikemalt loe artiklist <a href="/teadmine/artiklid/vanad-ja-kulunud-rehvid/">vanad ja kulunud rehvid</a>.</p>
<h2>Kas rehvil on lumehelbe märk?</h2>
<p>Kui ostad lamellrehve, otsi küljelt kolme mäetipu ja lumehelbe sümbolit. Transpordiameti järgi peab see talveperioodil olemas olema. Ainult M+S tähisest ei piisa.</p>
<p>Transpordiamet soovitab lisaks valida rehvi, millel on ka jäähaarduvuse märk. See näitab, et rehv on mõeldud Põhjamaade talveks.</p>
<h2>Mida kontrollida naastrehvi juures?</h2>
<ul><li><strong>Kas naastud on alles.</strong> Vaata üle kogu ringi. Kui paljudes aukudes naast puudub, on haarduvus jääl väiksem.</li><li><strong>Kas naastud ulatuvad välja.</strong> Kulunud rehvil võivad naastud olla kummiga tasa. Siis need enam jääd hästi ei hammusta.</li><li><strong>Kõik neli ühesugused.</strong> Ära pane autole segamini naastrehve ja lamellrehve.</li></ul>
<p>Naastrehvi ja lamellrehvi vahe on lahti kirjutatud artiklis <a href="/teadmine/artiklid/naastrehv-voi-lamell/">naastrehv või lamell</a>.</p>
<h2>Milliseid kahjustusi otsida?</h2>
<p>Vaata rehv üle nii väljast kui seest, mitte ainult mustri poolt.</p>
<ul><li><strong>Muhk või mull küljel.</strong> Tähendab tavaliselt, et rehv on seest kahjustatud. Sellist rehvi ära osta.</li><li><strong>Sügavad praod.</strong> Peened pinnalõhed on vanal rehvil tavalised, sügavad praod mustri soontes või küljel mitte.</li><li><strong>Lõiked ja paigad.</strong> Küsi, kas rehvi on parandatud ja millisest kohast.</li><li><strong>Ebaühtlane kulumine.</strong> Kui üks serv on rohkem kulunud, oli eelmisel autol tõenäoliselt vale rõhk või reguleerimata rattad.</li></ul>
<h2>Kas mõõt ja indeksid sobivad sinu autole?</h2>
<p>Kontrolli, et mõõt (näiteks 205/55 R16) on sama, mis su auto juhendis või juhiukse piilaril. Kui kaalud teist mõõtu, vaata enne <a href="/rehvi-kalkulaator/">rehvi kalkulaatorist</a>, kui palju see muudab ratta läbimõõtu. Vaata ka kandevõime indeksit (number mõõdu järel), see ei tohi olla väiksem kui autole ette nähtud.</p>
<h2>Kiire kontrollnimekiri</h2>
<ol><li>Muster vähemalt 3 mm, parem 5 mm või rohkem</li><li>DOT-kood: alla 10 aasta, ideaalis alla 6</li><li>Lumehelbe märk (lamellrehvil kohustuslik)</li><li>Naastud alles ja ulatuvad välja</li><li>Muhke, sügavaid pragusid ega lõikeid ei ole</li><li>Kulumine ühtlane, kõik neli sama mudel</li><li>Mõõt ja kandevõime sobivad autole</li></ol>
<h2>Proovi oma autoga</h2>
<p>Enne kui maksad kasutatud komplekti eest, võrdle uute rehvide hinda. <a href="/autod/">Kirjuta oma auto mark</a> ja vaata talverehvide pidurdusmaid ja hindu. Mõnikord on uus soodne rehv parem kui vana tippmudel.</p>
<p class="note">Allikad: <a href="https://www.transpordiamet.ee/uudised/homsest-lubatud-kasutada-naastrehve" rel="noopener">Transpordiamet 14.10.2024</a>, <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://www.continental-tires.com/in/en/b2c/tire-knowledge/replacing-tires" rel="noopener">Continental</a>.</p>`;

	const SISU_RU = `<p><strong>Коротко:</strong> у б/у зимней резины первым делом проверьте глубину протектора (по закону не менее 3 мм), у липучки знак снежинки на боковине и год выпуска по коду DOT. Если хоть один пункт не сходится, это не выгодная покупка, а просто неподходящая шина.</p>
<p>Купить зимнюю резину с рук бывает разумно. Но у зимней шины два «счётчика»: протектор стирается, а резина стареет. Продавец редко пишет в объявлении, что шине 9 лет. Это придётся выяснять самому.</p>
<h2>Сколько протектора должно быть у б/у зимней резины?</h2>
<p>Transpordiamet каждую осень напоминает: при покупке б/у зимних шин остаточная глубина протектора должна быть не менее 3 мм. Это законный минимум на зимний период, а не признак хорошей шины.</p>
<p>Чем меньше протектор, тем длиннее тормозной путь на снегу. Расчёт Pidurdusmaa.ee, северная зимняя шина, 50 км/ч по снегу:</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th>Протектор</th><th class="n">Тормозной путь</th></tr></thead><tbody><tr><td><strong>8 мм (новая)</strong></td><td class="n">26,2 м</td></tr><tr><td><strong>6 мм</strong></td><td class="n">28,4 м</td></tr><tr><td><strong>4 мм</strong></td><td class="n">31,1 м</td></tr><tr><td><strong>3 мм</strong></td><td class="n">32,7 м</td></tr></tbody></table></div>
<p>С протектором 3 мм тормозной путь на снегу примерно на четверть длиннее, чем у новой шины. На мокром асфальте с 90 км/ч он растёт с 47,5 до 54,0 м.</p>
<p><strong>На практике:</strong> если у шины 4 или 5 мм, до предела 3 мм она дойдёт намного раньше новой. Учитывайте это в цене.</p>
<p><strong>Как измерить:</strong> глубиномером или штангенциркулем, в нескольких местах и по обоим краям. Если край стёрт сильнее середины, у прошлого владельца, скорее всего, было неправильное давление или не отрегулирован развал.</p>
<h2>Как узнать возраст шины?</h2>
<p>Найдите на боковине код, который начинается с букв DOT. В конце этого кода стоит четырёхзначное число. Первые две цифры означают неделю, а последние две год. Например, 3819 означает: 38-я неделя 2019 года.</p>
<p>Continental советует снимать с эксплуатации все шины старше 10 лет, даже если на вид они в порядке. Внешний осмотр не всё показывает, резина дубеет изнутри. Шины старше 5 лет стоит проверять каждый год. Быстро посчитать возраст можно <a href="/ru/rehvi-vanus/">калькулятором возраста шин</a>.</p>
<p>Для зимней резины возраст особенно важен. Задубевшая резина хуже держит дорогу в мороз и на льду, даже если протектор ещё глубокий. Подробнее в статье <a href="/ru/teadmine/artiklid/vanad-ja-kulunud-rehvid/">старые и изношенные шины</a>.</p>
<h2>Есть ли на шине знак снежинки?</h2>
<p>Если покупаете липучку, ищите на боковине символ трёх горных вершин со снежинкой (3PMSF). По данным Transpordiamet, в зимний период он обязателен. Одной маркировки M+S недостаточно.</p>
<p>Transpordiamet также советует выбирать шины, у которых есть ещё и знак сцепления на льду. Он показывает, что шина рассчитана на северную зиму.</p>
<h2>Что проверить у б/у шипованной резины?</h2>
<ul><li><strong>Все ли шипы на месте.</strong> Осмотрите шину по всей окружности. Если много пустых гнёзд, сцепление на льду падает.</li><li><strong>Выступают ли шипы.</strong> На стёртой шине шипы бывают вровень с резиной и уже плохо цепляются за лёд.</li><li><strong>Все четыре одинаковые.</strong> Не ставьте на машину вперемешку шипованную резину и липучку.</li></ul>
<p>Разница между шипами и липучкой подробно разобрана в статье <a href="/ru/teadmine/artiklid/naastrehv-voi-lamell/">шипы или липучка</a>.</p>
<h2>Какие повреждения искать?</h2>
<p>Осмотрите шину снаружи и изнутри, а не только протектор.</p>
<ul><li><strong>Грыжа на боковине.</strong> Обычно значит, что повреждён корд. Такую шину не берите.</li><li><strong>Глубокие трещины.</strong> Мелкие трещинки на старой шине нормальны, а глубокие трещины в канавках или на боковине нет.</li><li><strong>Порезы и латки.</strong> Спросите, ремонтировали ли шину и в каком месте.</li><li><strong>Неравномерный износ.</strong> Если один край стёрт сильнее другого, на прошлой машине, скорее всего, было неправильное давление или не отрегулирован развал.</li></ul>
<h2>Подходят ли размер и индексы к вашей машине?</h2>
<p>Сверьте размер (например, 205/55 R16) с инструкцией или наклейкой на стойке водительской двери. Если думаете о другом размере, проверьте в <a href="/ru/rehvi-kalkulaator/">шинном калькуляторе</a>, насколько изменится диаметр колеса. Посмотрите и индекс нагрузки (число после размера), он не должен быть меньше положенного для вашей машины.</p>
<h2>Короткий чек-лист</h2>
<ol><li>Протектор не менее 3 мм, лучше 5 мм и больше</li><li>Код DOT: меньше 10 лет, в идеале меньше 6</li><li>Знак снежинки (для липучки обязателен)</li><li>Шипы на месте и выступают</li><li>Нет грыж, глубоких трещин и порезов</li><li>Износ ровный, все четыре одной модели</li><li>Размер и индекс нагрузки подходят машине</li></ol>
<h2>Проверьте на своей машине</h2>
<p>Прежде чем платить за б/у комплект, сравните с ценой новых. <a href="/ru/autod/">Введите марку своей машины</a> и посмотрите тормозной путь и цены зимней резины. Иногда новая недорогая шина лучше старой топовой.</p>
<p class="note">Источники: <a href="https://www.transpordiamet.ee/uudised/homsest-lubatud-kasutada-naastrehve" rel="noopener">Transpordiamet 14.10.2024</a>, <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://www.continental-tires.com/in/en/b2c/tire-knowledge/replacing-tires" rel="noopener">Continental</a>.</p>`;

	const KKK = [
		[
		 "Kui palju mustrit peab kasutatud talverehvil olema?",
		 "Talveperioodil seaduse järgi vähemalt 3 mm. Mõistlik on osta rehvi, millel on vähemalt 5 mm, sest muster kulub iga talvega."
		],
		[
		 "Kui vana talverehvi võib osta?",
		 "Continentali soovitus on, et üle 10 aasta vanad rehvid tuleks välja vahetada. Talverehvi puhul eelista nooremat, sest vana kumm kõvastub ja haarab külmas halvemini."
		],
		[
		 "Kuidas DOT-koodi lugeda?",
		 "DOT-koodi lõpus oleva neljakohalise numbri kaks esimest numbrit on tootmisnädal, kaks viimast aasta. 2219 tähendab 2019. aasta 22. nädalat."
		],
		[
		 "Kas kasutatud lamellrehvil peab olema lumehelbe märk?",
		 "Jah. 1. detsembrist 1. märtsini peab naastudeta talverehvil olema kolme mäetipu ja lumehelbe märk."
		]
];
	const KKK_RU = [
		[
		 "Сколько протектора должно быть у б/у зимней резины?",
		 "По закону в зимний период не менее 3 мм. Разумно брать шины хотя бы с 5 мм, протектор стирается каждую зиму."
		],
		[
		 "Зимнюю резину какого возраста можно покупать?",
		 "Continental советует менять шины старше 10 лет. Для зимы лучше брать шины помоложе: старая резина дубеет и хуже держит дорогу в мороз."
		],
		[
		 "Как читать код DOT?",
		 "Первые две цифры четырёхзначного числа означают неделю выпуска, а последние две год. 2219 означает: 22-я неделя 2019 года."
		],
		[
		 "Нужен ли знак снежинки на б/у липучке?",
		 "Да. С 1 декабря по 1 марта на нешипованной зимней шине должен быть знак трёх гор со снежинкой."
		]
];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	h1={T.h1}
	desc={T.desc}
	path="teadmine/artiklid/kasutatud-talverehvid/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/kasutatud-talverehvid/']]}
	lapsed={[]}
	uuendatud={A.uuendatud || A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/kasutatud-talverehvid.png"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
