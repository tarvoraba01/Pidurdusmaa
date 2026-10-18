<script>
	/* 3PMSF, M+S ja jäämärk: kuidas tunda ära õige talverehv
	   Artiklite partii 18.10.2026 (mustandid: 2ND Brain, Pidurdusmaa.ee/01 Articles, „(C) 04 3PMSF, M+S ja jäämärk - kuidas ära tunda õiget talverehvi“).
	   Seadused ja testid: allikad lehe lõpus. Pidurdusmaad: sama mudel mis kalkulaator (engine.js),
	   VW Golf 8, 205/55 R16; numbrid kontrollitud mudeliga 18.10.2026. Lehe tekst on genereeritud
	   mustandist (scratchpad md2page.py), parandused tee siin otse. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'talverehvi-margistus-3pmsf';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const SISU = `<p>Eestis peab naastudeta talverehvil olema 3PMSF märk (kolm mäetippu ja lumehelves). See tähendab, et rehv on läbinud lumetesti. Ainult M+S märgist ei piisa ja Eesti jäiste teede jaoks tasub otsida ka jäähaarduvuse märki.</p>
<p>Allpool on iga märk lahti seletatud ja lühike nimekiri, mida poes või kuulutuses vaadata.</p>
<h2>Mida tähendab M+S?</h2>
<p>M+S tähendab „Mud and Snow“, muda ja lumi. Sama tähis võib olla kirjutatud ka kujul MS, M.S. või M&amp;S.</p>
<p>Oluline on see, et M+S märki paneb tootja ise rehvi mustri järgi. Selleks ei pea rehv läbima ühtegi testi lumel ega jääl. Ministeerium on öelnud, et M+S rehv sobib nulli lähedasel temperatuuril, aga mitte lumele ega jääle.</p>
<p>Seepärast ei piisa Eestis 1. detsembrist 1. märtsini naastudeta rehvil ainult M+S märgist.</p>
<h2>Mida tähendab 3PMSF?</h2>
<p>3PMSF (three peak mountain snowflake) on kolme mäetipu sees olev lumehelves. Selle saab rehv, mis on läbinud lumetesti ÜRO eeskirja nr 117 järgi.</p>
<p>Testis võrreldakse rehvi standardse võrdlusrehviga. Sõiduauto rehv peab lumel olema võrdlusrehvist vähemalt 7% parem pidurdustestis või vähemalt 10% parem veojõutestis.</p>
<p>Alates 1. detsembrist 2022 peab Eestis igal naastudeta talverehvil talvisel perioodil olema 3PMSF märk. Erand on ainult maastikurehvid märgiga POR.</p>
<p><strong>Mida 3PMSF ei ütle:</strong> see on ainult lumetest. Märk ei näita, kuidas rehv jääl pidurdab. Ka paljudel Kesk-Euroopa talverehvidel ja nelja aastaaja rehvidel on 3PMSF märk.</p>
<h2>Mida tähendab jäämärk?</h2>
<p>Jäämärk (ice grip) on mäe kujutis, mille sees on jäätükk. See näitab, et rehv on läbinud jäätesti standardi ISO 19447 järgi. Pidurdus jääl peab olema vähemalt 18% parem kui võrdlusrehvil.</p>
<p>Jäämärk on nii rehvi küljel kui EL-i rehvimärgisel. Seda antakse sõiduauto rehvidele. Rohkem märgise kohta loe <a href="/teadmine/rehvimargis/">rehvimärgise lehelt</a>.</p>
<p>Jäämärk ei ole Eestis kohustuslik, aga Transpordiamet soovitab lamellrehvi puhul valida just sellise. Põhjus on lihtne: Eesti talvel on suurim oht tavaliselt jää, mitte sügav lumi.</p>
<h2>Kui suur on vahe numbrites?</h2>
<p>Pidurdusmaa.ee arvutuse järgi pidurdab VW Golf −5 °C jääl 50 km/h pealt jäämärgiga Põhjamaade lamellrehviga 58,9 m ja Kesk-Euroopa talverehviga 113,1 m. Mõlemal võib olla 3PMSF märk. Lumel on vahe väike.</p>
<p>Täpsem võrdlus on artiklis <a href="/teadmine/artiklid/pohjamaade-voi-kesk-euroopa-talverehv/">Põhjamaade või Kesk-Euroopa talverehv</a>.</p>
<h2>Kas naastrehvil peab olema 3PMSF?</h2>
<p>Eestis kehtib 3PMSF nõue ainult naastudeta talverehvidele. Naastrehv haakub jääga naastude abil. Paljudel naastrehvidel on 3PMSF märk sellegipoolest olemas.</p>
<h2>Kuidas rehvi küljelt õiget märki leida?</h2>
<p>Vaata rehvi külge. Otsi:</p>
<ol><li><strong>3PMSF</strong>: kolm mäetippu, sees lumehelves. Lamellrehvil kohustuslik.</li><li><strong>Jäämärk</strong>: mägi, sees jäätükk. Soovitatav.</li><li><strong>M+S</strong>: on tavaliselt olemas, aga üksi ei piisa.</li><li><strong>DOT-kood</strong>: viimased neli numbrit näitavad tootmise nädalat ja aastat. Kontrolli vanust <a href="/rehvi-vanus/">DOT-kalkulaatoriga</a>.</li></ol>
<p>Kui ostad kasutatud rehve kuulutusest, palu müüjalt foto rehvi küljest. Kui 3PMSF märki ei ole, ei tohi sa naastudeta rehviga talvisel perioodil sõita.</p>
<h2>Millist talverehvi siis osta?</h2>
<p>Eesti oludes on hea valik kas naastrehv või Põhjamaade lamellrehv, millel on 3PMSF ja jäämärk. Kumb sobib sulle, sõltub sellest, kus sa sõidad. Võrdlus on artiklis <a href="/teadmine/artiklid/talverehvi-valimine/">Talverehvi valimine</a>.</p>
<h2>Vaata oma auto talverehve</h2>
<p>Märk ütleb, et rehv on testi läbinud. Kui hästi see pidurdab, näitavad numbrid. <a href="/autod/">Kirjuta oma auto mark ja vaata talverehvide pidurdusmaid ja hindu</a> või vaata <a href="/talverehvid/">talverehve oma mõõdu järgi</a>, kus on ka testitud rehvide pidurdusmaad jääl.</p>
<p class="note">Allikad: <a href="https://www.blackcircles.com/news/3pmsf-explained-best-tyres-for-winter" rel="noopener">Blackcircles</a>, <a href="https://www.tehnoulevaatus.ee/talverehvide-nouete-muudatus/" rel="noopener">Tehnoülevaatus</a>, <a href="https://www.err.ee/1007161/kolme-aasta-parast-on-eestis-louna-euroopa-lamellrehvid-keelatud" rel="noopener">ERR 26.11.2019</a>, <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://www.tirerack.com/winter/tech/techpage.jsp?techid=691" rel="noopener">Tire Rack</a>, <a href="https://ustires.org/sites/default/files/2024-08/TISB%2056%20No%201.pdf" rel="noopener">USTMA</a>, <a href="https://legislation.gov.uk/eur/2020/740/annex/I/data.xht" rel="noopener">Määrus (EL) 2020/740</a>, <a href="https://liikluskool.ee/16-tehnoseisund-ja-muud-valdkonnad/" rel="noopener">Liikluskool</a>.</p>`;

	const SISU_RU = `<p>В Эстонии на нешипованной зимней шине должен быть знак 3PMSF (три горные вершины со снежинкой). Этот знак означает, что шина прошла тест на снегу. Одной маркировки M+S недостаточно, а для эстонских дорог с гололёдом стоит искать ещё и знак сцепления на льду.</p>
<p>Ниже разбираем каждый знак и даём короткий список того, на что смотреть в магазине или в объявлении.</p>
<h2>Что означает M+S?</h2>
<p>M+S означает «Mud and Snow», то есть грязь и снег. Встречается и в виде MS, M.S. или M&amp;S.</p>
<p>Главное: M+S производитель ставит сам, по рисунку протектора. Никаких тестов на снегу или льду для этого проходить не нужно. Министерство объясняло, что M+S подходит для температуры около нуля, но не для снега и льда.</p>
<p>Поэтому в Эстонии с 1 декабря по 1 марта на липучке одной маркировки M+S мало.</p>
<h2>Что означает 3PMSF?</h2>
<p>Знак 3PMSF (three peak mountain snowflake) выглядит как снежинка внутри трёх горных вершин. Его получает шина, прошедшая тест на снегу по правилам ООН № 117.</p>
<p>В тесте шину сравнивают со стандартной эталонной шиной. Легковая шина должна быть на снегу минимум на 7% лучше эталона в тесте торможения или минимум на 10% лучше в тесте тяги.</p>
<p>С 1 декабря 2022 года в Эстонии на каждой нешипованной зимней шине в зимний период должен быть знак 3PMSF. Исключение только для внедорожных шин с маркировкой POR.</p>
<p><strong>Чего 3PMSF не показывает:</strong> это только тест на снегу. Знак ничего не говорит о торможении на льду. Знак 3PMSF есть и у многих центральноевропейских зимних, и у всесезонных шин.</p>
<h2>Что означает знак льда?</h2>
<p>Знак льда (ice grip) выглядит как гора с куском льда внутри. Он показывает, что шина прошла тест на льду по стандарту ISO 19447. Торможение на льду должно быть минимум на 18% лучше, чем у эталонной шины.</p>
<p>Знак есть и на боковине шины, и на этикетке шин ЕС. Его присваивают шинам для легковых машин. Подробнее на странице <a href="/ru/teadmine/rehvimargis/">маркировка шин ЕС</a>.</p>
<p>В Эстонии знак льда не обязателен, но Transpordiamet советует при выборе липучки брать именно такую. Причина простая: главная опасность эстонской зимы обычно в гололёде, а не в глубоком снеге.</p>
<h2>Какая разница в цифрах?</h2>
<p>По расчёту Pidurdusmaa.ee VW Golf на льду при −5 °C с 50 км/ч останавливается на северной липучке со знаком льда за 58,9 м, а на центральноевропейской зимней шине за 113,1 м. Знак 3PMSF может быть у обеих. На снегу разница небольшая.</p>
<p>Подробное сравнение в статье <a href="/ru/teadmine/artiklid/pohjamaade-voi-kesk-euroopa-talverehv/">Северная или европейская зимняя шина</a>.</p>
<h2>Нужен ли 3PMSF на шипованной резине?</h2>
<p>Эстонское требование о знаке 3PMSF касается нешипованных зимних шин. Шипованная шина держится на льду за счёт шипов. При этом на многих шипованных шинах знак 3PMSF всё равно есть.</p>
<h2>Как найти нужный знак на боковине?</h2>
<p>Посмотрите на боковину шины. Ищите:</p>
<ol><li><strong>3PMSF</strong>: три вершины, внутри снежинка. Для липучки обязателен.</li><li><strong>Знак льда</strong>: гора, внутри кусок льда. Желателен.</li><li><strong>M+S</strong>: обычно есть, но одного его мало.</li><li><strong>Код DOT</strong>: последние четыре цифры показывают неделю и год выпуска. Проверьте возраст <a href="/ru/rehvi-vanus/">калькулятором DOT</a>.</li></ol>
<p>Если покупаете б/у резину по объявлению, попросите фото боковины. Если знака 3PMSF нет, на такой липучке в зимний период ездить нельзя.</p>
<h2>Какую зимнюю резину тогда брать?</h2>
<p>Для эстонских условий хорошо подходят либо шипы, либо северная липучка со знаками 3PMSF и льда. Что подойдёт именно вам, зависит от того, где вы ездите. Сравнение в статье <a href="/ru/teadmine/artiklid/talverehvi-valimine/">Как выбрать зимнюю шину</a>.</p>
<h2>Посмотрите зимние шины для своей машины</h2>
<p>Знак говорит, что шина прошла тест. Насколько хорошо она тормозит, показывают цифры. <a href="/ru/autod/">Введите марку своей машины и посмотрите тормозной путь и цены зимних шин</a> или откройте <a href="/ru/talverehvid/">зимние шины по размеру</a>, там есть и тормозной путь протестированных шин на льду.</p>
<p class="note">Источники: <a href="https://www.blackcircles.com/news/3pmsf-explained-best-tyres-for-winter" rel="noopener">Blackcircles</a>, <a href="https://www.tehnoulevaatus.ee/talverehvide-nouete-muudatus/" rel="noopener">Tehnoülevaatus</a>, <a href="https://www.err.ee/1007161/kolme-aasta-parast-on-eestis-louna-euroopa-lamellrehvid-keelatud" rel="noopener">ERR 26.11.2019</a>, <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://www.tirerack.com/winter/tech/techpage.jsp?techid=691" rel="noopener">Tire Rack</a>, <a href="https://ustires.org/sites/default/files/2024-08/TISB%2056%20No%201.pdf" rel="noopener">USTMA</a>, <a href="https://legislation.gov.uk/eur/2020/740/annex/I/data.xht" rel="noopener">Регламент (ЕС) 2020/740</a>, <a href="https://liikluskool.ee/16-tehnoseisund-ja-muud-valdkonnad/" rel="noopener">Liikluskool</a>.</p>`;

	const KKK = [
		[
		 "Kas M+S rehv on talverehv?",
		 "Eestis talvisel perioodil mitte, kui see on naastudeta. Naastudeta talverehvil peab olema 3PMSF märk."
		],
		[
		 "Kas 3PMSF märgiga rehv sobib jääle?",
		 "Mitte tingimata. 3PMSF on lumetest. Jää kohta annab infot jäämärk."
		],
		[
		 "Kas nelja aastaaja rehviga tohib Eestis talvel sõita?",
		 "Kui sellel on 3PMSF märk ja muster on vähemalt 3 mm, siis seadus seda ei keela. Jääl on see aga tavaliselt nõrk. Loe lähemalt: [Nelja aastaaja rehvid Eestis](/teadmine/artiklid/nelja-aastaaja-rehvid/)."
		],
		[
		 "Kus jäämärki näha?",
		 "Rehvi küljel ja EL-i rehvimärgisel, märghaarduvuse ja mürataseme kõrval."
		]
];
	const KKK_RU = [
		[
		 "Считается ли M+S зимней резиной?",
		 "В Эстонии в зимний период нет, если шина без шипов. На нешипованной зимней шине должен быть знак 3PMSF."
		],
		[
		 "Подходит ли шина с 3PMSF для льда?",
		 "Не обязательно. 3PMSF означает только тест на снегу. О льде говорит знак льда."
		],
		[
		 "Можно ли зимой в Эстонии ездить на всесезонке?",
		 "Если на ней есть 3PMSF и протектор не меньше 3 мм, закон этого не запрещает. Но на льду она обычно слабая. Подробнее: [Всесезонная резина в Эстонии](/ru/teadmine/artiklid/nelja-aastaaja-rehvid/)."
		],
		[
		 "Где искать знак льда?",
		 "На боковине шины и на этикетке шин ЕС, рядом с классом сцепления на мокрой дороге и уровнем шума."
		]
];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	h1={T.h1}
	desc={T.desc}
	path="teadmine/artiklid/talverehvi-margistus-3pmsf/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/talverehvi-margistus-3pmsf/']]}
	lapsed={[]}
	uuendatud={A.uuendatud || A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/talverehvi-margistus-3pmsf.png"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
