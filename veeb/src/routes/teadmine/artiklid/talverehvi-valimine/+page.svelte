<script>
	/* Talverehvi valimine — kõik numbrid on arvutatud sama mudeliga, mis
	   kalkulaator (engine.js), v.a. „Mudelite vahe“ lõik, mis on otse
	   Tekniikan Maailma 2025 mõõtmistest (core.json → tyres[].tests, TM25).
	   Arvutuse eeldused: VW Golf 8 1.5 TSI, 205/55 R16, uus rehv 8 mm,
	   tüüpiline märgise klass (suvi B, talv/aastaringne B, põhjamaade D),
	   lumi ja jää −5 °C, märg asfalt +10 °C, kuiv +15 °C.
	   Jää = tüüpiline SÕIDUTEE jää (model.py ice_road_add), mitte testiväljak.
	   Numbrid uuendatud 2026-09-29 (ScratchPad artikkel.py).
	   Vene tekst: SISU_RU (/ru/teadmine/artiklid/talverehvi-valimine/). */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const A = ARTIKLID.find((a) => a.slug === 'talverehvi-valimine');
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Eesti talv ei ole ainult lumi. On tallatud lumi, jää, sulav jää nulli ümber ja väga palju märga asfalti. Iga rehvitüüp on mõnes neist hea ja mõnes halb. Siin on numbrid, mis aitavad valida.</p>
<p>Kui pole öeldud teisiti, on pidurdusmaad arvutatud sama mudeliga, mis <a href="/">kalkulaator</a>: VW Golf 8, rehvimõõt 205/55 R16, uued rehvid. Arvestatud on ainult pidurdusteekonda, reaktsiooniaega mitte.</p>
<div class="note-box"><strong>Lühidalt.</strong> Suverehviga pidurdab auto lumel üle kahe korra pikemalt. Jääl on suurim vahe talverehvide endi vahel: Kesk-Euroopa talverehv pidurdab jääl üle poole pikemalt kui Põhjamaade oma. Naastrehv on parim jääl, eriti nulli lähedal. Kulunud muster võtab lumel ära veerandi haardest.</div>

<h2>Suverehv talvel</h2>
<p>50 km/h pealt tallatud lumel (−5 °C) peatub auto suverehvidega <strong>60,9 meetriga</strong>, talverehvidega umbes <strong>26 meetriga</strong>. Jääl on vahe veel suurem: suverehviga 82,5 m, Põhjamaade talverehviga 38,9 m.</p>
<p class="note">Jää tähendab siin tavalist sõidutee jääd: rööbastatud, kare või liivatatud jääd ja kohati siledat kiilasjääd. Rehvitestide siledal jääväljakul on pidurdusmaad pikemad (suverehviga u 137 m).</p>
<p>Suverehvi kumm muutub külmaga kõvaks ja muster ei ole lume jaoks tehtud. Seda ei korva ettevaatlik sõit ega ABS.</p>

<h2>Millal vahetada</h2>
<p>Seadus: <strong>talverehvid on kohustuslikud 1. detsembrist 1. märtsini</strong>. Naastrehvid on lubatud 15. oktoobrist 31. märtsini, talveoludes ka 1. oktoobrist 30. aprillini (<a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet</a>).</p>
<p>Aga millal on talverehv päriselt parem? Pidurdusmaa 90 km/h pealt (talv = Põhjamaade talverehv):</p>
${tabel(
		['Temperatuur', 'Märg: suvi', 'Märg: talv', 'Kuiv: suvi', 'Kuiv: talv'],
		[
			['+10 °C', '44,4 m', '47,5 m', '31,3 m', '39,4 m'],
			['+7 °C', '46,3 m', '47,2 m', '32,7 m', '39,2 m'],
			['+5 °C', '47,8 m', '47,1 m', '33,7 m', '39,1 m'],
			['0 °C', '53,7 m', '46,6 m', '37,9 m', '38,7 m']
		]
	)}
<p><strong>Märjal teel</strong> on vahe +7 °C juures alla meetri ja <strong>umbes +5 °C</strong> juures on talverehv juba parem, sest suverehvi kumm hakkab kõvenema. Kuival asfaldil jääb suverehv paremaks peaaegu nullini. Eesti sügis on enamasti märg ja esimene öökülm tuleb ootamatult — vaheta, kui päevad jäävad alla +7 °C ja öösiti on külma.</p>

<h2>Põhjamaade või Kesk-Euroopa talverehv</h2>
<p>Talverehve on kaht liiki ja poes on need sageli kõrvuti. <strong>Kesk-Euroopa</strong> talverehv on tehtud märja ja lörtsise talve jaoks, <strong>Põhjamaade</strong> oma lume ja jää jaoks. Pidurdusmaa 50 km/h pealt (märg asfalt 90 km/h pealt):</p>
${tabel(
		['Rehv', 'Lumi', 'Jää', 'Märg asfalt'],
		[
			['Suverehv', '60,9 m', '82,5 m', '44,4 m'],
			['Aastaringne', '25,2 m', '60,1 m', '40,4 m'],
			['Kesk-Euroopa talverehv', '26,3 m', '64,2 m', '44,7 m'],
			['Põhjamaade talverehv (lamell)', '26,2 m', '38,9 m', '47,5 m'],
			['Naastrehv', '25,4 m', '31,4 m', '47,5 m']
		]
	)}
<p>Lumel on kõik talverehvid peaaegu võrdsed. <strong>Jääl</strong> pidurdab Kesk-Euroopa talverehv üle poole pikemalt kui Põhjamaade oma. Märjal asfaldil on Kesk-Euroopa rehv umbes 3 m parem. Eesti talvel, kus jää ja jäide on tavalised, on Põhjamaade rehv kindlam valik.</p>
<p><strong>Kuidas ära tunda:</strong> mõlemal on EL-i rehvimärgisel kolme mäetipu ja lumehelbe märk. Põhjamaade rehvil on lisaks <strong>jäämärk</strong> — see tähendab, et rehv läbis jääkatse. Transpordiamet soovitab valida jäämärgiga rehvi. Loe lähemalt: <a href="/teadmine/rehvimargis/">EL-i rehvimärgis</a>.</p>

<h2>Naastrehv või lamell</h2>
<p>Jää pidamine sõltub temperatuurist. Kõige libedam on sulav jää nulli lähedal. Pidurdusmaa jääl 50 km/h pealt:</p>
${tabel(
		['Jää temperatuur', 'Naastrehv', 'Põhjamaade lamell', 'Parem'],
		[
			['−15 °C', '36,5 m', '27,4 m', 'lamell, 9 m'],
			['−5 °C', '31,4 m', '38,9 m', 'naast, 7,5 m'],
			['0 °C', '40,1 m', '58,6 m', 'naast, 18,5 m']
		]
	)}
<p>Naast lõikab jäässe ja sulav jää ei mõjuta teda nii palju kui kummi. Seepärast on naastrehvi eelis suurim just nulli ümber, mis on Eesti talvel sage. Väga külmal kõval jääl naast enam hästi sisse ei lähe ja lamell pidurdab lühemalt — seda mõõtis Za Rulem samade rehvidega neljal temperatuuril.</p>
<p>Lumel on nad praktiliselt võrdsed (naast 25,4 m, lamell 26,2 m). Kuival asfaldil on lamell veidi parem (90 km/h pealt 39,7 m vs 40,6 m) ning vaiksem. <strong>Naastrehv</strong> sobib, kui sõidad palju maanteel ja kõrvalteedel, kus jää püsib. <strong>Lamell</strong> sobib, kui sõidad peamiselt linnas ja soolatud teedel.</p>
<p>Testides mõõdetud pidurdusmaad jääl, märjal ja kuival: <a href="/teadmine/artiklid/naastrehv-voi-lamell/">Naastrehv või lamell?</a></p>

<h2>Aastaringne rehv</h2>
<p>Lumel on aastaringne rehv hea (25,2 m), aga jääl pidurdab ta 60,1 meetriga — umbes sama halvasti kui Kesk-Euroopa talverehv ja üle poole pikemalt kui Põhjamaade oma. Eesti talveks, kus on jääd, see hea valik ei ole.</p>

<h2>Mustri sügavus</h2>
<p>Seadus lubab talverehvi, mille muster on sügavam kui 3 mm. Aga haare kaob varem. Põhjamaade talverehv, pidurdusmaa lumel ja jääl 50 km/h ning märjal 90 km/h pealt:</p>
${tabel(
		['Muster', 'Lumi', 'Jää', 'Märg asfalt'],
		[
			['8 mm (uus)', '26,2 m', '38,9 m', '47,5 m'],
			['6 mm', '28,4 m', '40,5 m', '49,5 m'],
			['4 mm', '31,1 m', '42,3 m', '52,2 m'],
			['3 mm', '32,7 m', '43,2 m', '54,0 m']
		]
	)}
<p>3 mm mustriga on pidurdusmaa lumel veerandi võrra pikem kui uuel rehvil. Mõõda mustrit enne hooaega mustrisügavuse mõõdikuga.</p>

<h2>Talverehv suvel</h2>
<p>Kevadel tasub rehvid tagasi vahetada. Kuival asfaldil +25 °C juures pidurdab suverehv 90 km/h pealt 28,6 meetriga, Põhjamaade talverehv 42,0 meetriga — 13 meetrit pikemalt.</p>

<h2>Mudelite vahe on suur</h2>
<p>Rehvitüüp ei ütle kõike. <a href="https://www.tyrereviews.com/Tyre-Tests/2025-Friction-and-Studded-Winter-Tyre-Test.htm" rel="noopener">Tekniikan Maailma 2025. aasta testis</a> (205/55 R16, sile jääväljak, 50 → 0 km/h, −5 °C) mõõdeti:</p>
<ul><li><strong>Põhjamaade lamellrehvid:</strong> 45,6–53,5 m. Parima ja nõrgima vahe 7,9 m.</li><li><strong>Naastrehvid:</strong> 32,3–42,5 m. Vahe 10,2 m.</li></ul>
<p>Selles testis ei jõudnud ükski lamellrehv jääl ühegi naastrehvini. Aga nõrgim naastrehv oli parimale lamellile lähemal kui parimale naastrehvile. Kõik testitud rehvid ja nende tulemused: <a href="/testid/">Sõltumatud testid</a>.</p>

<h2>Kontrolli oma autoga</h2>
<p>Numbrid siin on VW Golfi kohta. Sinu auto ja rehvimõõduga:</p>
<ul><li><a href="/?olud=snow&kiirus=50#kalkulaator">Pidurdusmaa lumel 50 km/h pealt</a></li><li><a href="/?olud=ice&kiirus=50#kalkulaator">Pidurdusmaa jääl 50 km/h pealt</a></li><li><a href="/rehvi-valimine/?hooaeg=winter">Talverehvid sinu auto mõõdus</a> — järjestatud lume ja jää pidurduse järgi</li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>Эстонская зима — это не только снег. Это укатанный снег, лёд, тающий лёд около нуля и очень много мокрого асфальта. Каждый тип шин хорош в одних из этих условий и плох в других. Здесь цифры, которые помогут выбрать.</p>
<p>Если не сказано иное, тормозной путь рассчитан по той же модели, что и <a href="/">калькулятор</a>: VW Golf 8, размер шин 205/55 R16, новые шины. Учитывается только тормозной путь, без времени реакции.</p>
<div class="note-box"><strong>Коротко.</strong> На летних шинах тормозной путь на снегу более чем вдвое длиннее. На льду самая большая разница — между самими зимними шинами: европейская зимняя шина тормозит на льду более чем в полтора раза длиннее, чем нешипованная северного типа. Шипованная шина лучше всех на льду, особенно около нуля. Изношенный протектор отнимает на снегу четверть сцепления.</div>

<h2>Летняя шина зимой</h2>
<p>С 50 км/ч на укатанном снегу (−5 °C) автомобиль на летних шинах останавливается за <strong>60,9 метра</strong>, на зимних — примерно за <strong>26 метров</strong>. На льду разница ещё больше: на летней шине 82,5 м, на нешипованной зимней шине северного типа 38,9 м.</p>
<p class="note">Лёд здесь — это обычный лёд на дороге: колейный, шероховатый или посыпанный песком, местами гладкий гололёд. На гладком ледовом полигоне шинных тестов тормозной путь длиннее (на летней шине около 137 м).</p>
<p>Резина летней шины на холоде твердеет, а рисунок протектора не рассчитан на снег. Этого не компенсируют ни осторожная езда, ни ABS.</p>

<h2>Когда менять</h2>
<p>Закон: <strong>зимние шины обязательны с 1 декабря по 1 марта</strong>. Шипованные шины разрешены с 15 октября по 31 марта, при зимних условиях — также с 1 октября по 30 апреля (<a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet</a>, Транспортный департамент).</p>
<p>Но когда зимняя шина действительно лучше? Тормозной путь с 90 км/ч (зимняя = нешипованная зимняя шина северного типа):</p>
${tabel(
		['Температура', 'Мокро: летняя', 'Мокро: зимняя', 'Сухо: летняя', 'Сухо: зимняя'],
		[
			['+10 °C', '44,4 м', '47,5 м', '31,3 м', '39,4 м'],
			['+7 °C', '46,3 м', '47,2 м', '32,7 м', '39,2 м'],
			['+5 °C', '47,8 м', '47,1 м', '33,7 м', '39,1 м'],
			['0 °C', '53,7 м', '46,6 м', '37,9 м', '38,7 м']
		]
	)}
<p><strong>На мокрой дороге</strong> при +7 °C разница меньше метра, а <strong>примерно при +5 °C</strong> зимняя шина уже лучше, потому что резина летней шины начинает твердеть. На сухом асфальте летняя шина остаётся лучше почти до нуля. Осень в Эстонии обычно мокрая, а первый ночной заморозок приходит неожиданно — меняйте шины, когда днём держится ниже +7 °C, а ночью подмораживает.</p>

<h2>Северная или европейская зимняя шина</h2>
<p>Зимние шины бывают двух видов, и в магазине они часто стоят рядом. <strong>Европейская</strong> зимняя шина сделана для мокрой зимы со слякотью, <strong>северная</strong> — для снега и льда. Тормозной путь с 50 км/ч (мокрый асфальт — с 90 км/ч):</p>
${tabel(
		['Шина', 'Снег', 'Лёд', 'Мокрый асфальт'],
		[
			['Летняя шина', '60,9 м', '82,5 м', '44,4 м'],
			['Всесезонная', '25,2 м', '60,1 м', '40,4 м'],
			['Европейская зимняя шина', '26,3 м', '64,2 м', '44,7 м'],
			['Нешипованная северного типа («липучка»)', '26,2 м', '38,9 м', '47,5 м'],
			['Шипованная шина', '25,4 м', '31,4 м', '47,5 м']
		]
	)}
<p>На снегу все зимние шины почти равны. <strong>На льду</strong> европейская зимняя шина тормозит более чем в полтора раза длиннее, чем северная. На мокром асфальте европейская шина примерно на 3 м лучше. Для эстонской зимы, где лёд и гололедица — обычное дело, северная шина — более надёжный выбор.</p>
<p><strong>Как отличить:</strong> у обеих на маркировке шин ЕС есть знак «три горные вершины и снежинка». У северной шины есть ещё и <strong>знак льда</strong> — он означает, что шина прошла испытание на льду. Transpordiamet советует выбирать шину со знаком льда. Подробнее: <a href="/teadmine/rehvimargis/">Маркировка шин ЕС</a> (на эстонском).</p>

<h2>Шипы или «липучка»</h2>
<p>Сцепление на льду зависит от температуры. Самый скользкий — тающий лёд около нуля. Тормозной путь на льду с 50 км/ч:</p>
${tabel(
		['Температура льда', 'Шипованная шина', 'Северная «липучка»', 'Лучше'],
		[
			['−15 °C', '36,5 м', '27,4 м', '«липучка», 9 м'],
			['−5 °C', '31,4 м', '38,9 м', 'шипы, 7,5 м'],
			['0 °C', '40,1 м', '58,6 м', 'шипы, 18,5 м']
		]
	)}
<p>Шип врезается в лёд, и тающий лёд влияет на него не так сильно, как на резину. Поэтому преимущество шипованной шины больше всего именно около нуля, а это в эстонскую зиму частое явление. На очень холодном твёрдом льду шип уже плохо входит в лёд, и «липучка» тормозит короче — это измерил Za Rulem на одних и тех же шинах при четырёх температурах.</p>
<p>На снегу они практически равны (шипы 25,4 м, «липучка» 26,2 м). На сухом асфальте «липучка» немного лучше (с 90 км/ч 39,7 м против 40,6 м) и тише. <strong>Шипованная шина</strong> подходит, если вы много ездите по трассе и второстепенным дорогам, где держится лёд. <strong>«Липучка»</strong> подходит, если вы ездите в основном по городу и по дорогам, посыпанным солью.</p>
<p>Измеренный в тестах тормозной путь на льду, мокром и сухом асфальте: <a href="/ru/teadmine/artiklid/naastrehv-voi-lamell/">Шипы или «липучка»?</a></p>

<h2>Всесезонная шина</h2>
<p>На снегу всесезонная шина хороша (25,2 м), но на льду тормозит за 60,1 метра — примерно так же плохо, как европейская зимняя шина, и более чем в полтора раза длиннее, чем северная. Для эстонской зимы со льдом это не лучший выбор.</p>

<h2>Глубина протектора</h2>
<p>Закон разрешает зимнюю шину с глубиной протектора больше 3 мм. Но сцепление теряется раньше. Нешипованная зимняя шина северного типа, тормозной путь на снегу и льду с 50 км/ч и на мокром асфальте с 90 км/ч:</p>
${tabel(
		['Протектор', 'Снег', 'Лёд', 'Мокрый асфальт'],
		[
			['8 мм (новая)', '26,2 м', '38,9 м', '47,5 м'],
			['6 мм', '28,4 м', '40,5 м', '49,5 м'],
			['4 мм', '31,1 м', '42,3 м', '52,2 м'],
			['3 мм', '32,7 м', '43,2 м', '54,0 м']
		]
	)}
<p>С протектором 3 мм тормозной путь на снегу на четверть длиннее, чем у новой шины. Измерьте глубину протектора до начала сезона глубиномером.</p>

<h2>Зимняя шина летом</h2>
<p>Весной шины стоит поменять обратно. На сухом асфальте при +25 °C летняя шина тормозит с 90 км/ч за 28,6 метра, нешипованная зимняя северного типа — за 42,0 метра, на 13 метров длиннее.</p>

<h2>Разница между моделями большая</h2>
<p>Тип шины говорит не всё. <a href="https://www.tyrereviews.com/Tyre-Tests/2025-Friction-and-Studded-Winter-Tyre-Test.htm" rel="noopener">В тесте Tekniikan Maailma 2025 года</a> (205/55 R16, гладкий ледовый полигон, 50 → 0 км/ч, −5 °C) намерили:</p>
<ul><li><strong>Нешипованные шины северного типа:</strong> 45,6–53,5 м. Разница между лучшей и худшей 7,9 м.</li><li><strong>Шипованные шины:</strong> 32,3–42,5 м. Разница 10,2 м.</li></ul>
<p>В этом тесте ни одна «липучка» на льду не догнала ни одну шипованную шину. Но худшая шипованная шина была ближе к лучшей «липучке», чем к лучшей шипованной. Все протестированные шины и их результаты: <a href="/testid/">Независимые тесты</a> (на эстонском).</p>

<h2>Проверьте на своём автомобиле</h2>
<p>Цифры здесь — для VW Golf. Для вашего автомобиля и размера шин:</p>
<ul><li><a href="/?olud=snow&kiirus=50#kalkulaator">Тормозной путь на снегу с 50 км/ч</a></li><li><a href="/?olud=ice&kiirus=50#kalkulaator">Тормозной путь на льду с 50 км/ч</a></li><li><a href="/rehvi-valimine/?hooaeg=winter">Зимние шины в размере вашего автомобиля</a> — по торможению на снегу и льду</li></ul>
<p class="note">Расчётные результаты — это оценки, а не измерения. Точность модели и допущения: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a> (на эстонском).</p>`;

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	desc={T.desc}
	path="teadmine/artiklid/talverehvi-valimine/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/talverehvi-valimine/']]}
	lapsed={[]}
	uuendatud={A.kuupaev}
	avaldatud={A.kuupaev}
	sisu={ru ? SISU_RU : SISU}
/>
