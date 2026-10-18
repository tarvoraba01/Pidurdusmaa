<script>
	/* Nelja aastaaja rehvid Eestis: kas tohib ja kas tasub?
	   Artiklite partii 18.10.2026 (mustandid: 2ND Brain, Pidurdusmaa.ee/01 Articles, „(C) 05 Nelja aastaaja rehvid Eestis - kas tohib ja kas tasub“).
	   Seadused ja testid: allikad lehe lõpus. Pidurdusmaad: sama mudel mis kalkulaator (engine.js),
	   VW Golf 8, 205/55 R16; numbrid kontrollitud mudeliga 18.10.2026. Lehe tekst on genereeritud
	   mustandist (scratchpad md2page.py), parandused tee siin otse. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'nelja-aastaaja-rehvid';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const SISU = `<p><strong>Lühike vastus:</strong> nelja aastaaja rehviga tohib Eestis talvel sõita, kui rehvil on kolme mäetipu ja lumehelbe märk ning mustrit on vähemalt 3 mm. Lumel on see peaaegu sama hea kui talverehv, aga jääl on pidurdusmaa selgelt pikem kui Põhjamaade talverehvil.</p>
<p>Nelja aastaaja rehvi kutsutakse ka universaalrehviks või aastaringseks rehviks. Mõte on lihtne: üks komplekt aastaringselt, rehvivahetust pole. Kevadel ja sügisel on see mugav. Küsimus on, millega sa selle eest talvel maksad.</p>
<h2>Kas nelja aastaaja rehvid on Eestis lubatud?</h2>
<p>Jah, aga tingimusega. Transpordiameti järgi on talverehvid kohustuslikud 1. detsembrist 1. märtsini. Sel ajal peab naastudeta rehvil olema kolme mäetipu ja lumehelbe tähis (rahvusvaheliselt 3PMSF) ning mustri jääksügavus peab olema vähemalt 3 mm.</p>
<p>Seega otsustab märk, mitte rehvi nimi. Paljudel uuematel nelja aastaaja rehvidel on lumehelbe märk küljel olemas. Osal odavamatel ja vanematel mudelitel on ainult M+S tähis ja sellest talveperioodil ei piisa. ERR-i andmetel leiab M+S tähist ka rehvidelt, mis polegi talveks mõeldud.</p>
<p>Euroopa tarbijakeskuste võrgustik kirjutab samuti, et Eestis võib nelja aastaaja rehve kasutada aastaringselt ja et alates 2022. aastast peab neil talvel olema lumehelbe märk.</p>
<p><strong>Kontrolli enne ostu:</strong> vaata rehvi küljelt, kas seal on mäetippude ja lumehelbega sümbol. Kui ei ole, ei sobi rehv Eestis 1. detsembrist 1. märtsini.</p>
<h2>Kui hästi nelja aastaaja rehv talvel pidurdab?</h2>
<p>Siin tulevad erinevused välja. Rootsi ajakiri Vi Bilägare võrdles 2020. aastal mõõdus 205/60 R16 nelja aastaaja rehvi (Continental AllSeasonContact) Kesk-Euroopa talverehvi, Põhjamaade lamellrehvi ja naastrehviga.</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th>Tee</th><th class="n">Nelja aastaaja</th><th class="n">Põhjamaade lamell</th><th class="n">Naastrehv</th></tr></thead><tbody><tr><td><strong>Jää (25 kuni 5 km/h)</strong></td><td class="n">15,1 m</td><td class="n">11,1 m</td><td class="n">9,9 m</td></tr><tr><td><strong>Lumi (40 kuni 5 km/h)</strong></td><td class="n">20,8 m</td><td class="n">17,6 m</td><td class="n">17,7 m</td></tr><tr><td><strong>Märg asfalt (80 kuni 0 km/h)</strong></td><td class="n">25,9 m</td><td class="n">31,6 m</td><td class="n">30,1 m</td></tr><tr><td><strong>Kuiv asfalt (100 kuni 0 km/h)</strong></td><td class="n">40,1 m</td><td class="n">45,1 m</td><td class="n">46,5 m</td></tr></tbody></table></div>
<p>Allikas: Vi Bilägare 2020, tyrereviews.com kokkuvõte.</p>
<p>Jääl vajas nelja aastaaja rehv umbes 36% pikemat maad kui Põhjamaade lamellrehv. Märjal ja kuival asfaldil oli see aga parem. See ongi kompromiss, mille sa ostad.</p>
<p>Pidurdusmaa.ee arvutus näitab tavalisel kiirusel sarnast pilti. VW Golf 8, 205/55 R16, 50 km/h, lumi ja jää −5 °C:</p>
<ul><li><strong>lumel:</strong> nelja aastaaja rehv 25,2 m, Põhjamaade talverehv 26,2 m</li><li><strong>jääl:</strong> nelja aastaaja rehv 103,3 m, Põhjamaade talverehv 58,9 m</li><li><strong>märjal asfaldil 90 km/h:</strong> nelja aastaaja rehv 40,4 m, Põhjamaade talverehv 47,5 m</li></ul>
<p>Jääl on vahe üle 44 meetri. See on umbes kümne auto pikkus ristmiku ees.</p>
<h2>Kellele nelja aastaaja rehv Eestis sobib?</h2>
<p>See on meie hinnang, mitte reegel.</p>
<p><strong>Sobib pigem siis, kui:</strong></p>
<ul><li>sõidad peamiselt linnas, kus teed hooldatakse ja soolatakse</li><li>saad halva ilmaga sõidu edasi lükata</li><li>sõidad aastas vähe ja kaks komplekti tundub üleliigne</li></ul>
<p><strong>Pigem ei sobi, kui:</strong></p>
<ul><li>sõidad tihti maal või kõrvalteedel, kus on jää ja lumi</li><li>pead sõitma igal hommikul, ilmast sõltumata</li><li>sinu kandis on talvel sageli nulli ümber külmumist ja sulamist, mil jää on kõige libedam</li></ul>
<p>Kui sõidad tihti jääl, on Põhjamaade talverehv (lamell või naast) ohutum valik. Pikemalt loe artiklist <a href="/teadmine/artiklid/pohjamaade-voi-kesk-euroopa-talverehv/">Põhjamaade või Kesk-Euroopa talverehv</a>.</p>
<h2>Mida jälgida, kui ostad nelja aastaaja rehvi?</h2>
<ol><li><strong>Lumehelbe märk küljel.</strong> Ilma selleta ei tohi talveperioodil sõita.</li><li><strong>Mustri sügavus.</strong> Talvel peab olema vähemalt 3 mm. Aastaringselt sõites kulub rehv kiiremini, sest suvi on samuti kilomeetreid täis. Mõõda mustrit igal sügisel.</li><li><strong>Märghaarduvuse klass.</strong> Vaata EL-i rehvimärgist. Selgitus on lehel <a href="/teadmine/rehvimargis/">EL-i rehvimärgis</a>.</li><li><strong>Jäämärk.</strong> Nelja aastaaja rehvidel seda tavaliselt ei ole. Kui jääl pidurdamine on sulle tähtis, vali päris talverehv.</li></ol>
<h2>Proovi oma autoga</h2>
<p>Numbrid sõltuvad autost ja rehvi mõõdust. <a href="/autod/">Kirjuta oma auto mark</a> ja vaata, kui pika maa pealt sinu auto talverehvidega peatub ning mis need maksavad. Kui tahad võrrelda konkreetseid mudeleid, ava <a href="/talverehvid/">talverehvid sinu mõõdus</a>.</p>
<p class="note">Allikad: <a href="https://www.transpordiamet.ee/uudised/homsest-lubatud-kasutada-naastrehve" rel="noopener">Transpordiamet 14.10.2024</a>, <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://transpordiamet.ee/uudised/alates-2022-aasta-detsembrist-voib-kasutada-ainult-pohjamaade-kliimasse-moeldud-talverehve" rel="noopener">Transpordiamet</a>, <a href="https://www.err.ee/938636/minister-taavi-aas-kinnitas-auto-talverehvide-kasutamise-uued-nouded" rel="noopener">ERR</a>, <a href="https://www.europe-consommateurs.eu/en/driving/winter-tyres/" rel="noopener">Euroopa tarbijakeskused</a>, <a href="https://www.tyrereviews.com/Article/All-Season-vs-Winter-vs-Nordic-vs-Studded-Tyres.htm" rel="noopener">Tyre Reviews</a>.</p>`;

	const SISU_RU = `<p><strong>Коротко:</strong> ездить зимой на всесезонной резине в Эстонии можно, если на боковине есть знак «три горные вершины и снежинка» (3PMSF), а глубина протектора не менее 3 мм. На снегу такая шина почти не уступает зимней, но на льду тормозит заметно хуже северной зимней резины.</p>
<p>Всесезонку выбирают ради удобства: один комплект на весь год, никакой смены резины весной и осенью. Вопрос в том, чем за это удобство придётся заплатить зимой.</p>
<h2>Разрешена ли всесезонная резина зимой в Эстонии?</h2>
<p>Да, но с условием. По данным Transpordiamet, зимние шины обязательны с 1 декабря по 1 марта. В этот период на нешипованной шине должен быть знак трёх горных вершин и снежинки, а остаточная глубина протектора должна быть не менее 3 мм.</p>
<p>То есть решает маркировка, а не название «всесезонная». У многих современных всесезонных шин знак 3PMSF есть. У части дешёвых и старых моделей только M+S. Одной маркировки M+S в зимний период недостаточно. Как писал ERR, M+S встречается даже на шинах, которые вообще не рассчитаны на зиму.</p>
<p>Европейская сеть центров защиты потребителей тоже указывает, что в Эстонии всесезонные шины можно использовать круглый год, а с 2022 года знак снежинки на них обязателен в зимний период.</p>
<p><strong>Перед покупкой:</strong> посмотрите на боковину. Нет знака с горами и снежинкой, значит, с 1 декабря по 1 марта такая шина в Эстонии не подходит.</p>
<h2>Как всесезонная шина тормозит зимой?</h2>
<p>Шведский журнал Vi Bilägare в 2020 году сравнил в размере 205/60 R16 всесезонную шину (Continental AllSeasonContact), европейскую зимнюю, северную «липучку» и шипованную.</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th>Покрытие</th><th class="n">Всесезонная</th><th class="n">Северная липучка</th><th class="n">Шипованная</th></tr></thead><tbody><tr><td><strong>Лёд (с 25 до 5 км/ч)</strong></td><td class="n">15,1 м</td><td class="n">11,1 м</td><td class="n">9,9 м</td></tr><tr><td><strong>Снег (с 40 до 5 км/ч)</strong></td><td class="n">20,8 м</td><td class="n">17,6 м</td><td class="n">17,7 м</td></tr><tr><td><strong>Мокрый асфальт (с 80 км/ч)</strong></td><td class="n">25,9 м</td><td class="n">31,6 м</td><td class="n">30,1 м</td></tr><tr><td><strong>Сухой асфальт (со 100 км/ч)</strong></td><td class="n">40,1 м</td><td class="n">45,1 м</td><td class="n">46,5 м</td></tr></tbody></table></div>
<p>Источник: Vi Bilägare 2020, сводка tyrereviews.com.</p>
<p>На льду всесезонке понадобилось примерно на 36% больше места, чем северной липучке. Зато на мокром и сухом асфальте она была лучше. Это и есть компромисс.</p>
<p>Расчёт Pidurdusmaa.ee даёт похожую картину на обычной скорости. VW Golf 8, 205/55 R16, 50 км/ч, снег и лёд −5 °C:</p>
<ul><li><strong>снег:</strong> всесезонная 25,2 м, северная зимняя 26,2 м</li><li><strong>лёд:</strong> всесезонная 103,3 м, северная зимняя 58,9 м</li><li><strong>мокрый асфальт, 90 км/ч:</strong> всесезонная 40,4 м, северная зимняя 47,5 м</li></ul>
<p>На льду разница больше 44 метров. Это примерно десять корпусов машины перед перекрёстком.</p>
<h2>Кому подходит всесезонка в Эстонии?</h2>
<p>Это наша оценка, а не правило.</p>
<p><strong>Скорее подходит, если вы:</strong></p>
<ul><li>ездите в основном по городу, где дороги чистят и посыпают солью</li><li>можете отложить поездку в плохую погоду</li><li>проезжаете мало и второй комплект кажется лишним</li></ul>
<p><strong>Скорее не подходит, если вы:</strong></p>
<ul><li>часто ездите за городом и по второстепенным дорогам, где лёд и снег</li><li>должны выезжать каждое утро в любую погоду</li><li>часто попадаете в оттепель с заморозками около 0 °C, когда лёд самый скользкий</li></ul>
<p>Если лёд для вас обычное дело, безопаснее северная зимняя резина, липучка или шипованная. Подробнее в статье <a href="/ru/teadmine/artiklid/pohjamaade-voi-kesk-euroopa-talverehv/">Северная или европейская зимняя шина</a>.</p>
<h2>На что смотреть при покупке всесезонной резины?</h2>
<ol><li><strong>Знак снежинки на боковине.</strong> Без него ездить в зимний период нельзя.</li><li><strong>Глубина протектора.</strong> Зимой не менее 3 мм. Всесезонка изнашивается быстрее, ведь летом она тоже катается. Проверяйте протектор каждую осень.</li><li><strong>Класс сцепления на мокрой дороге.</strong> Смотрите на этикетку ЕС, разбор здесь: <a href="/ru/teadmine/rehvimargis/">маркировка шин ЕС</a>.</li><li><strong>Знак льда.</strong> У всесезонных шин его обычно нет. Если торможение на льду для вас важно, это сигнал, что нужна настоящая зимняя резина.</li></ol>
<h2>Проверьте на своей машине</h2>
<p>Цифры зависят от автомобиля и размера шин. <a href="/ru/autod/">Введите марку своей машины</a> и посмотрите тормозной путь и цены зимней резины именно для неё. Конкретные модели можно сравнить на странице <a href="/ru/talverehvid/">зимние шины по размеру</a>.</p>
<p class="note">Источники: <a href="https://www.transpordiamet.ee/uudised/homsest-lubatud-kasutada-naastrehve" rel="noopener">Transpordiamet 14.10.2024</a>, <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://transpordiamet.ee/uudised/alates-2022-aasta-detsembrist-voib-kasutada-ainult-pohjamaade-kliimasse-moeldud-talverehve" rel="noopener">Transpordiamet</a>, <a href="https://www.err.ee/938636/minister-taavi-aas-kinnitas-auto-talverehvide-kasutamise-uued-nouded" rel="noopener">ERR</a>, <a href="https://www.europe-consommateurs.eu/en/driving/winter-tyres/" rel="noopener">Европейские центры потребителей</a>, <a href="https://www.tyrereviews.com/Article/All-Season-vs-Winter-vs-Nordic-vs-Studded-Tyres.htm" rel="noopener">Tyre Reviews</a>.</p>`;

	const KKK = [
		[
		 "Kas nelja aastaaja rehviga võib Eestis talvel sõita?",
		 "Jah, kui rehvil on kolme mäetipu ja lumehelbe märk ja mustrit on vähemalt 3 mm. Ainult M+S tähisega rehv 1. detsembrist 1. märtsini ei sobi."
		],
		[
		 "Kas nelja aastaaja rehv on sama hea kui talverehv?",
		 "Lumel peaaegu jah. Jääl ei ole. Vi Bilägare testis vajas see jääl umbes 36% pikemat pidurdusmaad kui Põhjamaade lamellrehv."
		],
		[
		 "Kas nelja aastaaja rehv on suvel parem kui talverehv?",
		 "Märjal ja kuival asfaldil pidurdas see Vi Bilägare testis lühemalt kui Põhjamaade talverehvid. Päris suverehvi tasemele see tavaliselt ei jõua."
		],
		[
		 "Kas nelja aastaaja rehvi peab sügisel vahetama?",
		 "Ei pea. Aga kontrolli igal sügisel mustri sügavust ja lumehelbe märki, sest talvel kehtib 3 mm piir."
		]
];
	const KKK_RU = [
		[
		 "Можно ли ездить на всесезонной резине зимой в Эстонии?",
		 "Да, если на шине есть знак 3PMSF (горы и снежинка) и протектор не менее 3 мм. Шина только с M+S с 1 декабря по 1 марта не подходит."
		],
		[
		 "Всесезонка так же хороша, как зимняя резина?",
		 "На снегу почти да. На льду нет. В тесте Vi Bilägare её тормозной путь на льду был примерно на 36% длиннее, чем у северной липучки."
		],
		[
		 "Летом всесезонка лучше зимней резины?",
		 "На мокром и сухом асфальте в тесте Vi Bilägare её тормозной путь был короче, чем у северных зимних шин. До уровня хорошей летней шины обычно не дотягивает."
		],
		[
		 "Нужно ли менять всесезонку осенью?",
		 "Нет. Но каждую осень проверяйте глубину протектора и маркировку, зимой действует порог 3 мм."
		]
];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	h1={T.h1}
	desc={T.desc}
	path="teadmine/artiklid/nelja-aastaaja-rehvid/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/nelja-aastaaja-rehvid/']]}
	lapsed={[]}
	uuendatud={A.uuendatud || A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/nelja-aastaaja-rehvid.png"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
