<script>
	/* Rehvirõhk ja pidurdus — numbrid sama mudeliga mis kalkulaator (engine.js):
	   VW Golf 8 1.5 TSI, 205/55 R16, tehase rõhk 2,3 bar, keskmine suverehv
	   (märghaardeklass C), uus muster 8 mm, autos juht, ilma reaktsiooniajata.
	   Märg asfalt 1 mm vett +12 °C; sügav vesi 3 mm; kuiv +15 °C; 90 km/h.
	   Akvaplaneerimise kiirus: Pidurdus.hydroplaneSpeedKmh. Numbrid 2026-10-06. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'rehvirohk-ja-pidurdus';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Rehvirõhk on asi, mida enamik juhte kontrollib harva. Tavalisel märjal teel mõjutab vale rõhk pidurdust vähem, kui arvatakse. Sügavas vees on vahe aga suur, sest pehme rehv hakkab vee peal ujuma palju väiksema kiirusega.</p>
<p>Pidurdusmaad on arvutatud sama mudeliga, mis <a href="/">kalkulaator</a>: VW Golf 8, rehvimõõt 205/55 R16, tehase soovitatud rõhk 2,3 bar, keskmine suverehv, 90 km/h. Arvestatud on ainult pidurdusteekonda, reaktsiooniaega mitte.</p>
<div class="note-box"><strong>Lühidalt.</strong> Märjal teel lisab 0,7 bar liiga madal rõhk pidurdusmaale umbes 2 meetrit. Sügavas vees (3 mm veekiht) on pidurdusmaa 1,4 bar rõhuga 10 meetrit pikem ja auto hakkab vee peal ujuma juba 101 km/h juures, õige rõhuga alles 129 km/h juures. Sügisel langeb rõhk iga 10 kraadi jahenemisega umbes 0,1 bar.</div>

<h2>Märg tee</h2>
<p>Õhuke veekiht (1 mm) märjal asfaldil. Pidurdusmaa 90 km/h pealt:</p>
${tabel(
		['Rõhk', 'Pidurdusmaa', 'Õigest rõhust rohkem'],
		[
			['2,3 bar (tehase soovitus)', '43,9 m', '—'],
			['2,0 bar', '44,5 m', '+0,6 m'],
			['1,8 bar', '45,1 m', '+1,2 m'],
			['1,6 bar', '45,8 m', '+1,9 m'],
			['1,4 bar', '46,7 m', '+2,8 m']
		]
	)}
<p>Liiga madal rõhk teeb rehvi kontaktpinna laiemaks, aga muster ei suuda nii laialt pinnalt vett välja juhtida. Liiga kõrge rõhk ei aita ka: 3,0 bar juures on märjal pidurdusmaa 44,3 m, natuke pikem kui õige rõhuga. Kuival teel on vahe väike, kuni umbes meeter mõlemas suunas.</p>

<h2>Sügav vesi ja akvaplaneerimine</h2>
<p>Pärast tugevat vihma on teel rööbastes sageli 3 mm või rohkem vett. Siis loeb rõhk palju rohkem, sest pehme rehv surub vett vähem eest ära ja tõuseb vee peale varem:</p>
${tabel(
		['Rõhk', 'Pidurdusmaa 90 km/h pealt', 'Akvaplaneerimise kiirus'],
		[
			['2,3 bar', '52,8 m', 'u 129 km/h'],
			['2,0 bar', '54,4 m', 'u 120 km/h'],
			['1,8 bar', '56,0 m', 'u 114 km/h'],
			['1,6 bar', '58,4 m', 'u 107 km/h'],
			['1,4 bar', '63,0 m', 'u 101 km/h']
		]
	)}
<p>Akvaplaneerimise kiirusel kaotab rehv teega kontakti: rool ja pidur ei tööta enam. Kui rõhk on madal ja muster ka kulunud, tuleb see piir veel lähemale. 3 mm mustriga suverehvil on see õige rõhuga umbes 96 km/h, 1,6 bar rõhuga umbes 80 km/h. Siis on maanteekiirusel sügavas vees auto vee peal ja pidurdusmaad ei saa enam usaldusväärselt arvutada.</p>

<h2>Miks rõhk sügisel langeb</h2>
<p>Õhk rehvis tõmbub külmaga kokku. Rõhk langeb umbes 0,1 bar iga 10 kraadi kohta. Kui rehvid pumbati suvel +20 °C juures õigeks, on need öökülmaga juba 0,2 bar pehmemad. Lisaks lekib igast rehvist aeglaselt õhku, tavaliselt 0,1 bar kuus.</p>
<p>Seepärast tasub rõhku kontrollida rehvivahetuse ajal ja siis, kui ilm järsult jaheneb.</p>

<h2>Kuidas rõhku kontrollida</h2>
<ul><li><strong>Õige rõhk</strong> on kirjas juhiukse piilaril, kütuseluugi sees või auto käsiraamatus. Rehvi küljel olev number on rehvi maksimaalne rõhk, mitte soovitus.</li><li><strong>Mõõda külmalt</strong>, enne sõitu või pärast paari kilomeetrit. Soojad rehvid näitavad 0,2–0,3 bar rohkem.</li><li><strong>Täis koormaga</strong> (pere ja pagas, haagis) soovitab tootja enamasti suuremat rõhku. See on kirjas samal sildil.</li><li><strong>Rõhuandur</strong> annab märku alles siis, kui rõhk on langenud umbes 20–25%. 2,3 bar puhul on see 1,8 bar, ja see on juba tabelis näha.</li></ul>

<h2>Proovi oma autoga</h2>
<ul><li><a href="/">Pidurdusmaa kalkulaator</a>: sinu auto, rehvid ja teeolud</li><li><a href="/teadmine/artiklid/vanad-ja-kulunud-rehvid/">Vanad ja kulunud rehvid: kui palju pikeneb pidurdusmaa?</a></li><li><a href="/rehvi-vanus/">Rehvi vanuse kontroll</a>: DOT-kood ja muster</li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>Давление в шинах большинство водителей проверяет редко. На обычной мокрой дороге неправильное давление влияет на торможение меньше, чем кажется. Но в глубокой воде разница большая: мягкая шина начинает всплывать на воде при гораздо меньшей скорости.</p>
<p>Тормозной путь рассчитан той же моделью, что и <a href="/ru/">калькулятор</a>: VW Golf 8, размер шин 205/55 R16, рекомендованное заводом давление 2,3 бар, средняя летняя шина, 90 км/ч. Учтён только тормозной путь, без времени реакции.</p>
<div class="note-box"><strong>Коротко.</strong> На мокрой дороге давление на 0,7 бар ниже нормы добавляет к тормозному пути около 2 метров. В глубокой воде (слой 3 мм) при давлении 1,4 бар тормозной путь на 10 метров длиннее, а аквапланирование начинается уже с 101 км/ч, при правильном давлении — только со 129 км/ч. Осенью давление падает примерно на 0,1 бар на каждые 10 градусов похолодания.</div>

<h2>Мокрая дорога</h2>
<p>Тонкий слой воды (1 мм) на мокром асфальте. Тормозной путь с 90 км/ч:</p>
${tabel(
		['Давление', 'Тормозной путь', 'Больше, чем при норме'],
		[
			['2,3 бар (рекомендация завода)', '43,9 м', '—'],
			['2,0 бар', '44,5 м', '+0,6 м'],
			['1,8 бар', '45,1 м', '+1,2 м'],
			['1,6 бар', '45,8 м', '+1,9 м'],
			['1,4 бар', '46,7 м', '+2,8 м']
		]
	)}
<p>При низком давлении пятно контакта шины шире, но протектор не успевает отводить воду с такой площади. Слишком высокое давление тоже не помогает: при 3,0 бар тормозной путь на мокрой дороге 44,3 м, чуть длиннее, чем при норме. На сухой дороге разница мала, до метра в обе стороны.</p>

<h2>Глубокая вода и аквапланирование</h2>
<p>После сильного дождя в колеях часто стоит 3 мм воды и больше. Тогда давление значит гораздо больше: мягкая шина хуже вытесняет воду и раньше поднимается на неё:</p>
${tabel(
		['Давление', 'Тормозной путь с 90 км/ч', 'Скорость аквапланирования'],
		[
			['2,3 бар', '52,8 м', 'ок. 129 км/ч'],
			['2,0 бар', '54,4 м', 'ок. 120 км/ч'],
			['1,8 бар', '56,0 м', 'ок. 114 км/ч'],
			['1,6 бар', '58,4 м', 'ок. 107 км/ч'],
			['1,4 бар', '63,0 м', 'ок. 101 км/ч']
		]
	)}
<p>На скорости аквапланирования шина теряет контакт с дорогой: руль и тормоза больше не работают. Если давление низкое, а протектор ещё и изношен, этот порог ещё ближе. У летней шины с протектором 3 мм он при правильном давлении около 96 км/ч, при 1,6 бар — около 80 км/ч. На трассовой скорости в глубокой воде машина тогда уже на воде, и тормозной путь надёжно рассчитать нельзя.</p>

<h2>Почему осенью давление падает</h2>
<p>Воздух в шине сжимается от холода. Давление падает примерно на 0,1 бар на каждые 10 градусов. Если шины накачали летом при +20 °C, то в ночной заморозок они уже на 0,2 бар мягче. Кроме того, из любой шины медленно уходит воздух, обычно 0,1 бар в месяц.</p>
<p>Поэтому давление стоит проверять при смене шин и когда резко холодает.</p>

<h2>Как проверить давление</h2>
<ul><li><strong>Правильное давление</strong> указано на стойке водительской двери, внутри лючка бензобака или в руководстве по эксплуатации. Число на боковине шины — это её максимальное давление, а не рекомендация.</li><li><strong>Измеряйте на холодных шинах</strong>, до поездки или после пары километров. Тёплые шины показывают на 0,2–0,3 бар больше.</li><li><strong>При полной загрузке</strong> (семья и багаж, прицеп) производитель обычно рекомендует более высокое давление. Это указано на той же табличке.</li><li><strong>Датчик давления</strong> предупреждает, только когда давление упало примерно на 20–25%. При норме 2,3 бар это 1,8 бар, и разница уже видна в таблице.</li></ul>

<h2>Проверьте на своём автомобиле</h2>
<ul><li><a href="/ru/">Калькулятор тормозного пути</a>: ваша машина, шины и дорожные условия</li><li><a href="/ru/teadmine/artiklid/vanad-ja-kulunud-rehvid/">Старые и изношенные шины: насколько удлиняется тормозной путь?</a></li><li><a href="/ru/rehvi-vanus/">Проверка возраста шины</a>: код DOT и протектор</li></ul>
<p class="note">Расчётные результаты — это оценки, а не измерения. Точность модели и допущения: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a> (на эстонском).</p>`;

	const KKK = [
		['Kui palju mõjutab madal rehvirõhk pidurdusmaad?', 'Märjal teel 90 km/h pealt on VW Golf 8 pidurdusmaa õige rõhuga (2,3 bar) 43,9 m ja 1,4 bar rõhuga 46,7 m, ehk 2,8 m pikem. Sügavas vees (3 mm) on vahe 10 m: 52,8 m ja 63,0 m.'],
		['Mis kiirusel tekib akvaplaneerimine?', 'Uue suverehvi ja õige rõhuga 3 mm veekihis umbes 129 km/h juures. 1,4 bar rõhuga juba umbes 101 km/h juures. 3 mm mustri ja 1,6 bar rõhuga umbes 80 km/h juures.'],
		['Kui palju langeb rehvirõhk külmaga?', 'Umbes 0,1 bar iga 10 kraadi jahenemise kohta. Suvel +20 °C juures õigeks pumbatud rehv on öökülmaga umbes 0,2 bar pehmem.'],
		['Kust leida auto õige rehvirõhk?', 'Juhiukse piilarilt, kütuseluugi seest või auto käsiraamatust. Rehvi küljel olev number on rehvi maksimaalne lubatud rõhk, mitte soovitus.']
	];
	const KKK_RU = [
		['Насколько низкое давление в шинах влияет на тормозной путь?', 'На мокрой дороге с 90 км/ч тормозной путь VW Golf 8 при правильном давлении (2,3 бар) 43,9 м, а при 1,4 бар — 46,7 м, то есть на 2,8 м длиннее. В глубокой воде (3 мм) разница 10 м: 52,8 м и 63,0 м.'],
		['На какой скорости начинается аквапланирование?', 'У новой летней шины при правильном давлении в слое воды 3 мм примерно со 129 км/ч. При 1,4 бар — уже примерно со 101 км/ч. С протектором 3 мм и давлением 1,6 бар — примерно с 80 км/ч.'],
		['Насколько падает давление в шинах на холоде?', 'Примерно на 0,1 бар на каждые 10 градусов похолодания. Шина, накачанная летом при +20 °C, в ночной заморозок мягче примерно на 0,2 бар.'],
		['Где найти правильное давление для автомобиля?', 'На стойке водительской двери, внутри лючка бензобака или в руководстве по эксплуатации. Число на боковине шины — её максимально допустимое давление, а не рекомендация.']
	];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	desc={T.desc}
	path={'teadmine/artiklid/' + SLUG + '/'}
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/' + SLUG + '/']]}
	lapsed={[]}
	uuendatud={A.kuupaev}
	avaldatud={A.kuupaev}
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
