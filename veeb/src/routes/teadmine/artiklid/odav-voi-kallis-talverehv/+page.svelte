<script>
	/* Odav või kallis talverehv? Mida testid tegelikult näitavad
	   Artiklite partii 18.10.2026 (mustandid: 2ND Brain, Pidurdusmaa.ee/01 Articles, „(C) 08 Odav või kallis talverehv - mida testid tegelikult näitavad“).
	   Seadused ja testid: allikad lehe lõpus. Pidurdusmaad: sama mudel mis kalkulaator (engine.js),
	   VW Golf 8, 205/55 R16; numbrid kontrollitud mudeliga 18.10.2026. Lehe tekst on genereeritud
	   mustandist (scratchpad md2page.py), parandused tee siin otse. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'odav-voi-kallis-talverehv';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const SISU = `<p><strong>Lühike vastus:</strong> odav talverehv ei ole automaatselt halb, aga sageli on sellel üks suur nõrkus: jää või märg asfalt. Testides on parima ja halvima vahe jääl üle kahe korra ja märjal teel umbes poolteist korda, lumel aga alla meetri. Vali rehv nende teede järgi, kus sa päriselt sõidad.</p>
<p>Hinnavahe on tuntav. Seepärast tasub teada, mille eest sa maksad.</p>
<h2>Kas odav talverehv on ohtlik?</h2>
<p>Vahel on, aga mitte igal pool. Vaata Rootsi ajakirja Vi Bilägare 2025. aasta naastrehvide testi (235/60 R18, Volvo XC60):</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th></th><th>Jää, 25 kuni 5 km/h</th><th>Märg asfalt</th></tr></thead><tbody><tr><td><strong>Nokian Hakkapeliitta 10 SUV</strong></td><td>11,5 m (parim)</td><td>49,7 m</td></tr><tr><td><strong>Triangle IceLynx TI501 (odavaim)</strong></td><td>25,5 m (halvim)</td><td>43,3 m (parim)</td></tr></tbody></table></div>
<p>Odavaim rehv vajas jääl üle kahe korra pikemat maad. Märjal asfaldil oli sama rehv aga testi parim. Kui sõidad peamiselt soolatud linnateedel, on pilt hoopis teine kui maal jäistel teedel.</p>
<p>Sama pilt kordub Kesk-Euroopa talverehvidel. ADAC ja ÖAMTC 2026. aasta testis (185/65 R15, Škoda Fabia) oli Rockblade Rock 868S talvisel teel kõige parem, aga märjal asfaldil väga nõrk. Pidurdusmaa 80 km/h pealt oli 51,4 m, parimal (Bridgestone Blizzak LM005) 33,5 m. Lõpphinne oli Rockblade'il ÖAMTC skaalal „nicht genügend“ ehk mitterahuldav, just märja tee pärast.</p>
<p>ADAC 2025. aasta testis oli märjal asfaldil vahe 15 meetrit: Goodyear UltraGrip Performance 3 peatus 31,7 meetriga, Syron Everest 2 aga 47,1 meetriga.</p>
<h2>Kus on vahed suured ja kus väikesed?</h2>
<ul><li><strong>Lumel väike.</strong> Kolmes Vi Bilägare testis oli parima ja halvima vahe tihendatud lumel alla meetri. Lumega saavad hakkama peaaegu kõik.</li><li><strong>Jääl suur.</strong> Soome ajakirja Tekniikan Maailma 2025. aasta testis (205/55 R16, 50 km/h) pidurdas parim naastrehv 32,3 m ja halvim lamellrehv 53,5 m. Vahe on 21 meetrit, kuigi osa sellest tuleb naastudest.</li><li><strong>Märjal asfaldil suur.</strong> Vahed on 15 kuni 18 meetrit.</li></ul>
<p>Seega see, et lumel on kõik rehvid sarnased, ei aita sul valida. Vaata jää ja märja tee tulemusi.</p>
<h2>Kuidas talverehvi testi õigesti lugeda?</h2>
<ol><li><strong>Vaata nõrkust, mitte koondhinnet.</strong> Rehv võib olla üldiselt hea ja ühes asjas väga halb. Talvel otsustab just halvim olukord.</li><li><strong>Vaata õiget tüüpi testi.</strong> ADAC ja Auto Bild testivad Kesk-Euroopa rehve. Eesti jääle sobivad paremini Vi Bilägare, Tekniikan Maailma ja teised Põhjamaade testid.</li><li><strong>Mõõt peab olema lähedal.</strong> Sama mudel võib eri mõõdus käituda veidi teisiti.</li><li><strong>Eri testide meetreid ei saa otse võrrelda.</strong> Autod, kiirused ja ilm on erinevad. Võrdle rehve sama testi sees.</li><li><strong>Vaata aastat.</strong> Mudelid uuenevad. Viis aastat vana test võib käia juba eelmise põlvkonna kohta.</li></ol>
<p>Selle hooaja kõigi testide numbrid on koos artiklis <a href="/teadmine/artiklid/talverehvide-testid-2026/">talverehvide testid 2025 ja 2026</a>.</p>
<h2>Kas EL-i rehvimärgis aitab?</h2>
<p>Lamellrehvi puhul jah. Märghaarduvuse klass näitab pidurdust märjal asfaldil. Pidurdusmaa.ee arvutuse järgi on märjal asfaldil 90 km/h pealt klassi E suverehvi pidurdusmaa 17,7 meetrit ehk 43% pikem kui klassi A suverehvil. Kesk-Euroopa talverehvil on vahe 12,6 meetrit ehk 30%. Lisaks näitab jäämärk, et rehv on läbinud jäätesti. Selgitus on lehel <a href="/teadmine/rehvimargis/">EL-i rehvimärgis</a>.</p>
<p>Naastrehvidel EL-i märgist ei ole. Määrus (EL) 2020/740 jätab naastrehvid välja. Naastrehvi puhul on sõltumatu test ainus usaldusväärne võrdlus.</p>
<h2>Kuidas siis valida?</h2>
<p>See on meie soovitus, mitte reegel.</p>
<ul><li><strong>Sõidad palju maal või jäistel teedel:</strong> maksa jää eest. Vali rehv, mis on Põhjamaade testis jääl esimeste seas.</li><li><strong>Sõidad peamiselt linnas:</strong> märg ja lörtsine asfalt on su tavaline tee. Vaata märja tee tulemust ja märgise klassi.</li><li><strong>Piiratud eelarve:</strong> parem tuntud keskklassi rehv, millel ühtki suurt nõrkust ei ole, kui odavaim rehv, mis mõnes testis on viimane.</li><li><strong>Ära maksa ainult nime eest.</strong> Tippbrändi vanem mudel võib olla nõrgem kui uuem keskklassi rehv. Vaata numbreid.</li></ul>
<p>Naastrehvi ja lamellrehvi valik on eraldi teema, see on lahti kirjutatud artiklis <a href="/teadmine/artiklid/naastrehv-voi-lamell/">naastrehv või lamell</a>.</p>
<h2>Proovi oma autoga</h2>
<p>Odava ja kalli rehvi vahe on meetrites näha. <a href="/autod/">Kirjuta oma auto mark</a> ja vaata talverehvide pidurdusmaid ja hindu oma mõõdus. Kaks konkreetset rehvi saad kõrvuti panna lehel <a href="/vordle-rehve/">võrdle rehve</a>.</p>
<p class="note">Allikad: <a href="https://www.tyrereviews.com/Tyre-Tests/The-BEST-Studded-Tyres-for-2025.htm" rel="noopener">Tyre Reviews</a>, <a href="https://www.oeamtc.at/tests/reifentest/winterreifentest-2026/rockblade-rock-868s-89453774/print" rel="noopener">ÖAMTC</a>, <a href="https://www.oeamtc.at/tests/reifentest/winterreifentest-2026/bridgestone-blizzak-lm-005-89453645/print" rel="noopener">ÖAMTC</a>, <a href="https://legislation.gov.uk/eur/2020/740/body/data.htm?view=plain" rel="noopener">Määrus (EL) 2020/740</a>.</p>`;

	const SISU_RU = `<p><strong>Коротко:</strong> дешёвая зимняя резина не обязательно плохая, но часто у неё есть одна серьёзная слабость: лёд или мокрый асфальт. В тестах разница между лучшей и худшей шиной на льду больше чем в два раза, на мокрой дороге примерно в полтора раза, а на снегу меньше метра. Выбирайте резину под те дороги, по которым ездите на самом деле.</p>
<p>Разница в цене заметна. Поэтому стоит понимать, за что вы платите.</p>
<h2>Опасна ли дешёвая зимняя резина?</h2>
<p>Иногда да, но не везде. Посмотрите тест шипованных шин шведского журнала Vi Bilägare 2025 года (235/60 R18, Volvo XC60):</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th></th><th>Лёд, с 25 до 5 км/ч</th><th>Мокрый асфальт</th></tr></thead><tbody><tr><td><strong>Nokian Hakkapeliitta 10 SUV</strong></td><td>11,5 м (лучший)</td><td>49,7 м</td></tr><tr><td><strong>Triangle IceLynx TI501 (самая дешёвая)</strong></td><td>25,5 м (худший)</td><td>43,3 м (лучший)</td></tr></tbody></table></div>
<p>Самой дешёвой шине на льду понадобилось в два с лишним раза больше места. Зато на мокром асфальте она оказалась лучшей в тесте. Для того, кто ездит по городу с реагентами, и для того, кто ездит по ледяным загородным дорогам, это разные истории.</p>
<p>С европейскими зимними шинами то же самое. В тесте ADAC и ÖAMTC 2026 года (185/65 R15, Škoda Fabia) Rockblade Rock 868S была лучшей на зимней дороге, но очень слабой на мокром асфальте. Тормозной путь с 80 км/ч составил 51,4 м, а у лучшей (Bridgestone Blizzak LM005) 33,5 м. У ÖAMTC Rockblade получила итоговую оценку «nicht genügend», то есть «неудовлетворительно», именно из-за мокрой дороги.</p>
<p>В тесте ADAC 2025 года разница на мокром асфальте составила 15 метров: Goodyear UltraGrip Performance 3 остановилась за 31,7 м, а Syron Everest 2 только за 47,1 м.</p>
<h2>Где разница большая, а где маленькая?</h2>
<ul><li><strong>На снегу маленькая.</strong> В трёх тестах Vi Bilägare разница между лучшей и худшей шиной на укатанном снегу была меньше метра. Со снегом справляются почти все.</li><li><strong>На льду большая.</strong> В тесте финского журнала Tekniikan Maailma 2025 года (205/55 R16, 50 км/ч) лучшая шипованная шина остановилась за 32,3 м, а худшая липучка за 53,5 м. Разница составила 21 метр, хотя часть её дают сами шипы.</li><li><strong>На мокром асфальте большая.</strong> Разница составляет от 15 до 18 метров.</li></ul>
<p>Так что одинаковые результаты на снегу почти не помогают с выбором. Смотрите результаты на льду и мокрой дороге.</p>
<h2>Как правильно читать тест зимних шин?</h2>
<ol><li><strong>Смотрите на слабость, а не на итоговое место.</strong> Шина может быть в целом хорошей и очень плохой в чём-то одном. Зимой решает как раз худшая ситуация.</li><li><strong>Смотрите подходящий тест.</strong> ADAC и Auto Bild тестируют европейские шины. Для эстонского льда полезнее Vi Bilägare, Tekniikan Maailma и другие северные тесты.</li><li><strong>Размер должен быть близким.</strong> Одна и та же модель в другом размере может вести себя немного иначе.</li><li><strong>Метры из разных тестов напрямую не сравнить.</strong> Машины, скорости и погода разные. Сравнивайте шины внутри одного теста.</li><li><strong>Смотрите год.</strong> Модели обновляются. Тест пятилетней давности может касаться уже прошлого поколения.</li></ol>
<p>Все цифры тестов этого сезона собраны в статье <a href="/ru/teadmine/artiklid/talverehvide-testid-2026/">тесты зимних шин 2025 и 2026</a>.</p>
<h2>Помогает ли этикетка ЕС?</h2>
<p>Для липучки да. Класс сцепления на мокрой дороге показывает торможение на мокром асфальте. По расчёту Pidurdusmaa.ee на мокром асфальте с 90 км/ч тормозной путь летней шины класса E на 17,7 метра, то есть на 43%, длиннее, чем у летней шины класса A. У центральноевропейской зимней шины разница составляет 12,6 метра, или 30%. Кроме того, знак льда говорит, что шина прошла тест на льду. Подробнее на странице <a href="/ru/teadmine/rehvimargis/">маркировка шин ЕС</a>.</p>
<p>У шипованной резины этикетки ЕС нет. Регламент (ЕС) 2020/740 исключает шипованные шины. Шипованные шины надёжно сравнить можно только по независимым тестам.</p>
<h2>Так как же выбрать?</h2>
<p>Это наша рекомендация, а не правило.</p>
<ul><li><strong>Много ездите за городом или по льду:</strong> платите за лёд. Берите шину, которая в северном тесте на льду оказалась среди первых.</li><li><strong>Ездите в основном по городу:</strong> у вас обычно мокрый асфальт и снежная каша. Смотрите результат на мокром асфальте и класс сцепления на этикетке.</li><li><strong>Бюджет ограничен:</strong> лучше известная шина среднего класса без серьёзных слабостей, чем самая дешёвая, которая в каком-то тесте оказалась последней.</li><li><strong>Не платите только за имя.</strong> Старая модель топового бренда может уступать новой шине среднего класса. Смотрите на цифры.</li></ul>
<p>Выбор между шипами и липучкой разобран в отдельной статье <a href="/ru/teadmine/artiklid/naastrehv-voi-lamell/">шипы или липучка</a>.</p>
<h2>Проверьте на своей машине</h2>
<p>Разницу между дешёвой и дорогой резиной видно в метрах. <a href="/ru/autod/">Введите марку своей машины</a> и посмотрите тормозной путь и цены зимней резины в вашем размере. Две конкретные шины можно сравнить на странице <a href="/ru/vordle-rehve/">сравнение шин</a>.</p>
<p class="note">Источники: <a href="https://www.tyrereviews.com/Tyre-Tests/The-BEST-Studded-Tyres-for-2025.htm" rel="noopener">Tyre Reviews</a>, <a href="https://www.oeamtc.at/tests/reifentest/winterreifentest-2026/rockblade-rock-868s-89453774/print" rel="noopener">ÖAMTC</a>, <a href="https://www.oeamtc.at/tests/reifentest/winterreifentest-2026/bridgestone-blizzak-lm-005-89453645/print" rel="noopener">ÖAMTC</a>, <a href="https://legislation.gov.uk/eur/2020/740/body/data.htm?view=plain" rel="noopener">Регламент (ЕС) 2020/740</a>.</p>`;

	const KKK = [
		[
		 "Kas odavad talverehvid on ohtlikud?",
		 "Mitte alati, aga neil on sageli üks suur nõrkus. Vi Bilägare 2025. aasta testis vajas odavaim naastrehv jääl üle kahe korra pikemat maad kui parim, aga märjal asfaldil oli parim."
		],
		[
		 "Kas kallis talverehv on alati parem?",
		 "Ei. Testides on näha, et ka tuntud rehv võib ühes olukorras jääda alla odavamale. Vaata konkreetse mudeli tulemusi."
		],
		[
		 "Millist talverehvi testi usaldada?",
		 "Eesti oludes Põhjamaade teste, näiteks Vi Bilägare ja Tekniikan Maailma, sest need testivad jääl ja Põhjamaade rehve. ADAC testib Kesk-Euroopa rehve."
		],
		[
		 "Kas naastrehvil on EL-i rehvimärgis?",
		 "Ei ole. Määrus (EL) 2020/740 jätab naastrehvid märgise nõudest välja."
		]
];
	const KKK_RU = [
		[
		 "Опасна ли дешёвая зимняя резина?",
		 "Не всегда, но часто у неё есть одна большая слабость. В тесте Vi Bilägare 2025 года у самой дешёвой шипованной шины тормозной путь на льду был в два с лишним раза длиннее, чем у лучшей, но на мокром асфальте она была первой."
		],
		[
		 "Дорогая зимняя резина всегда лучше?",
		 "Нет. Тесты показывают, что и известная шина в какой-то ситуации может уступить более дешёвой. Смотрите результаты конкретной модели."
		],
		[
		 "Каким тестам зимних шин доверять?",
		 "В условиях Эстонии северным, например Vi Bilägare и Tekniikan Maailma: там тестируют на льду и северные шины. ADAC тестирует европейские."
		],
		[
		 "Есть ли у шипованной резины этикетка ЕС?",
		 "Нет. Регламент (ЕС) 2020/740 исключает шипованные шины из требований к этикетке."
		]
];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	h1={T.h1}
	desc={T.desc}
	path="teadmine/artiklid/odav-voi-kallis-talverehv/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/odav-voi-kallis-talverehv/']]}
	lapsed={[]}
	uuendatud={A.uuendatud || A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/odav-voi-kallis-talverehv.png"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
