<script>
	import { lumi, jaa } from '$lib/margid.js';
	import Leht from '$lib/Leht.svelte';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const ru = keel.lang === 'ru';
	const SISU = `<p>Igal Euroopas müüdaval sõiduauto rehvil on EL-i rehvimärgis (määrus 2020/740). Andmed tulevad EL-i tooteregistrist EPREL.</p>
<h2>Märghaardumine (A–E)</h2>
<p>Mõõdetakse märjal asfaldil 80 → 20 km/h, võrdluses standardse võrdlusrehviga. Klassi A ja E vahe on tavalisel sõiduautol 90 km/h juures umbes 18 meetrit (klasside keskpunktide järgi arvutatud). Klass on <strong>mõõdupõhine</strong>: sama rehvimudel võib olla ühes mõõdus A ja teises B.</p>
<h2>Veeretakistus (A–E)</h2>
<p>Mõjutab kütuse- või energiakulu. Pidurdusmaaga ei ole otsest seost — kontrollisime seda 41 testitud rehvi peal ja veeretakistuse klass ei seletanud märja pidurduse erinevusi.</p>
<h2>Müra (dB ja A–C)</h2>
<p>Rehvi veeremismüra ametliku katse järgi. Väiksem number = vaiksem rehv. Iga 3 dB on ligikaudu kahekordne heliväljund.</p>
<h2>Lume- ja jäämärk</h2>
<p>Kolme mäetipu ja lumehelbe märk ${lumi()} (3PMSF) tähendab, et rehv läbis lumehaarde katse. Jäämärk ${jaa()} tähendab Põhjamaade jääkatse läbimist (ainult sõiduauto rehvid).</p>`;
	const SISU_RU = `<p>У каждой продаваемой в Европе шины для легкового автомобиля есть маркировка шин ЕС (регламент 2020/740). Данные берутся из реестра продукции ЕС EPREL.</p>
<h2>Сцепление на мокрой дороге (A–E)</h2>
<p>Измеряется на мокром асфальте при торможении с 80 до 20 км/ч в сравнении со стандартной эталонной шиной. Разница между классами A и E у обычного легкового автомобиля при 90 км/ч — около 18 метров (рассчитано по середине классов). Класс <strong>зависит от размера</strong>: одна и та же модель в одном размере может быть A, а в другом — B.</p>
<h2>Сопротивление качению (A–E)</h2>
<p>Влияет на расход топлива или энергии. Прямой связи с тормозным путём нет — мы проверили это на 41 протестированной шине, и класс сопротивления качению не объяснял разницу в торможении на мокрой дороге.</p>
<h2>Шум (дБ и A–C)</h2>
<p>Шум качения шины по официальному испытанию. Меньше число — тише шина. Каждые 3 дБ — это примерно вдвое больше звуковой энергии.</p>
<h2>Знак снега и льда</h2>
<p>Знак трёх горных вершин и снежинки ${lumi('Знак «три горные вершины и снежинка» (3PMSF)')} (3PMSF) означает, что шина прошла испытание на сцепление на снегу. Знак льда ${jaa('Знак льда (символ сцепления со льдом на этикетке ЕС)')} означает, что шина прошла северное испытание на льду (только шины для легковых автомобилей).</p>`;
	const KKK = [
		['Mida tähendab märghaardumise klass A–E?', 'Klass näitab, kui hästi rehv pidurdab märjal asfaldil, võrreldes standardse võrdlusrehviga (katse 80 → 20 km/h). A on parim. Tavalisel sõiduautol on klasside A ja E vahe 90 km/h juures umbes 18 meetrit.'],
		['Kas veeretakistuse klass mõjutab pidurdust?', 'Otseselt mitte. Kontrollisime 41 testitud rehvi peal ja veeretakistuse klass ei seletanud märja pidurduse erinevusi. See klass mõjutab kütuse- või energiakulu.'],
		['Miks on samal rehvil eri mõõtudes erinev klass?', 'Märgis on mõõdupõhine: iga mõõt katsetatakse eraldi. Sama mudel võib olla ühes mõõdus A ja teises B.'],
		['Mida tähendab lumehelbe ja mäetippude märk?', 'Kolme mäetipu ja lumehelbe märk (3PMSF) tähendab, et rehv läbis lumehaarde katse. Eestis peab lamellrehvil talverehvide kohustuslikul ajal see märk olema. Jäämärk tähendab Põhjamaade jääkatse läbimist.'],
		['Kust saan oma rehvi märgise andmed?', 'Märgise andmed on EL-i tooteregistris EPREL. Pidurdusmaa.ee näitab neid iga rehvimudeli ja mõõdu juures ning arvutab märgise põhjal pidurdusmaa sinu autoga.']
	];
	const KKK_RU = [
		['Что означает класс сцепления на мокрой дороге A–E?', 'Класс показывает, насколько хорошо шина тормозит на мокром асфальте по сравнению со стандартной эталонной шиной (испытание 80 → 20 км/ч). A — лучший. У обычного легкового автомобиля разница между классами A и E при 90 км/ч — около 18 метров.'],
		['Влияет ли класс сопротивления качению на торможение?', 'Напрямую нет. Мы проверили это на 41 протестированной шине, и класс сопротивления качению не объяснял разницу в торможении на мокрой дороге. Этот класс влияет на расход топлива или энергии.'],
		['Почему у одной шины в разных размерах разный класс?', 'Маркировка зависит от размера: каждый размер испытывают отдельно. Одна и та же модель может быть в одном размере A, а в другом — B.'],
		['Что означает знак снежинки и горных вершин?', 'Знак трёх горных вершин и снежинки (3PMSF) означает, что шина прошла испытание на сцепление на снегу. В Эстонии нешипованная шина в период обязательных зимних шин должна иметь этот знак. Знак льда означает, что шина прошла северное испытание на льду.'],
		['Где найти данные маркировки своей шины?', 'Данные маркировки есть в реестре продукции ЕС EPREL. Pidurdusmaa.ee показывает их для каждой модели и размера шины и по маркировке рассчитывает тормозной путь для вашего автомобиля.']
	];
	const TITLE = ru ? 'Маркировка шин ЕС: что означают классы' : 'EL-i rehvimärgis: mida klassid tähendavad';
</script>

<Leht
	title={TITLE}
	desc={ru ? 'Сцепление на мокрой дороге, сопротивление качению, шум, знак снега и льда — что на самом деле означают классы маркировки шин ЕС.' : 'Märghaardumine, veeretakistus, müra, lume- ja jäämärk — mida EL-i rehvimärgise klassid päriselt tähendavad.'}
	path="teadmine/rehvimargis/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [TITLE, '/teadmine/rehvimargis/']]}
	lapsed={[]}
	uuendatud="2026-09-25"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
