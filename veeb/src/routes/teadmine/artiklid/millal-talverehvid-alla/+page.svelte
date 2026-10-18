<script>
	import { lumi, jaa, ms } from '$lib/margid.js';
	/* Millal talverehvid alla — seaduse kuupäevad hooajal 2026/27 ja mida
	   pidurdusmaa ütleb vahetamise aja kohta.
	   Kuupäevad: Transpordiamet (14.10.2024), ERR (29.03.2024, 26.11.2019).
	   Pidurdusmaad: sama mudel mis kalkulaator, samad numbrid mis artiklis
	   „Talverehvi valimine“ (VW Golf 8, 205/55 R16, uued rehvid, ilma reaktsiooniajata).
	   Jää = tüüpiline jää (45 ajakirja jäätesti mediaan, model.py ice_road_factor),
	   −5 °C. Jää numbrid 13.10.2026.
	   Vene tekst: SISU_RU (/ru/teadmine/artiklid/millal-talverehvid-alla/). */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const A = ARTIKLID.find((a) => a.slug === 'millal-talverehvid-alla');
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const TA = 'https://www.transpordiamet.ee/uudised/homsest-lubatud-kasutada-naastrehve';

	const SISU = `<div class="note-box"><strong>Lühidalt, hooaeg 2026/2027.</strong> Naastrehvid on lubatud <strong>15. oktoobrist 2026 kuni 31. märtsini 2027</strong>. Talverehvid on kohustuslikud <strong>1. detsembrist 2026 kuni 1. märtsini 2027</strong>. Talverehvi muster peab olema sügavam kui <strong>3 mm</strong>. Talviste olude korral tohib naastrehve kasutada 1. oktoobrist 30. aprillini (<a href="${TA}" rel="noopener">Transpordiamet</a>). Kõik tähtajad ja tänane seis: <a href="/teadmine/rehvivahetus/">Rehvivahetus 2026</a>.</div>

<h2>Milline talverehv sobib</h2>
<ul>
<li><strong>Muster vähemalt 3 mm.</strong> See on seaduse miinimum talverehvile. Mõõda mustrisügavust enne hooaega.</li>
<li><strong>Kolme mäetipu ja lumehelbe märk.</strong> ${lumi()} Naastudeta talverehvil peab see märk olema. Transpordiamet soovitab valida ka <strong>jäämärgiga</strong> ${jaa()} rehvi — see on Põhjamaade rehv, mis on läbinud jääkatse. Lõuna- ja Kesk-Euroopa talverehvid (ainult M+S märgiga ${ms()}) Eestis ei sobi.</li>
<li><strong>Kõikidel ratastel sama tüüpi rehvid.</strong> Naast- ja lamellrehve ei tasu segamini panna: auto käitub pidurdades ja kurvis ettearvamatult.</li>
</ul>

<h2>Millal vahetada — mida numbrid ütlevad</h2>
<p>Seadus ütleb, millal <em>tohib</em> ja millal <em>peab</em>. Pidurdusmaa ütleb, millal on <em>mõistlik</em>. Märjal asfaldil 90 km/h pealt (VW Golf, Põhjamaade talverehv vs suverehv):</p>
${tabel(
		['Temperatuur', 'Suverehv', 'Talverehv'],
		[
			['+10 °C', '44,4 m', '47,5 m'],
			['+7 °C', '46,3 m', '47,2 m'],
			['+5 °C', '47,8 m', '47,1 m'],
			['0 °C', '53,7 m', '46,6 m']
		]
	)}
<p>Umbes <strong>+5 °C</strong> juures pidurdab talverehv märjal teel juba lühemalt, sest suverehvi kumm muutub külmaga kõvaks. Esimene lumi ja öökülm tulevad Eestis sageli ootamatult — vaheta, kui päevad jäävad alla +7 °C.</p>

<h2>Suverehv esimesel lumel</h2>
<p>Tallatud lumel 50 km/h pealt peatub auto suverehvidega <strong>60,9 meetriga</strong>, talverehvidega umbes <strong>26 meetriga</strong>. Jääl on vahe veel suurem: 165,0 m ja 58,9 m. Esimese lumega ootamine võib maksta üle 30 meetri pidurdusmaad.</p>

<h2>Vana talverehv: kas tuleb veel üks talv?</h2>
<p>Seaduse miinimum on 3 mm, aga haare kaob varem. Põhjamaade talverehv, pidurdusmaa 50 km/h pealt:</p>
${tabel(
		['Muster', 'Lumi', 'Jää'],
		[
			['8 mm (uus)', '26,2 m', '58,9 m'],
			['6 mm', '28,4 m', '61,2 m'],
			['4 mm', '31,1 m', '63,8 m'],
			['3 mm', '32,7 m', '65,2 m']
		]
	)}
<p>3 mm mustriga on pidurdusmaa lumel veerandi võrra pikem kui uuel rehvil. Kui muster on 4 mm või vähem, tasub uued rehvid osta enne hooaega, mitte keset talve.</p>

<h2>Kevadel tagasi</h2>
<p>Talverehv suvel pidurdab halvemini: kuival asfaldil +25 °C juures 90 km/h pealt suverehv 28,6 m, Põhjamaade talverehv 42,0 m. Naastrehvid tuleb ära vahetada hiljemalt 31. märtsiks (talveoludes 30. aprilliks).</p>

<h2>Kontrolli oma autoga</h2>
<ul>
<li><a href="/?olud=snow&kiirus=50#kalkulaator">Pidurdusmaa lumel sinu autoga</a></li>
<li><a href="/rehvi-valimine/?hooaeg=winter">Talverehvid sinu auto mõõdus</a> — järjestatud lume ja jää pidurduse järgi</li>
<li><a href="/teadmine/artiklid/talverehvi-valimine/">Talverehvi valimine: naast või lamell, Põhjamaade või Kesk-Euroopa</a></li>
</ul>
<p class="note">Kuupäevad: Transpordiamet. Pidurdusmaad on arvutatud hinnangud (VW Golf 8, 205/55 R16, uued rehvid, ilma reaktsiooniajata), mitte mõõtmised. <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<div class="note-box"><strong>Коротко, сезон 2026/2027.</strong> Шипованные шины разрешены <strong>с 15 октября 2026 по 31 марта 2027</strong>. Зимние шины обязательны <strong>с 1 декабря 2026 по 1 марта 2027</strong>. Глубина протектора зимней шины должна быть больше <strong>3 мм</strong>. При зимних условиях шипы можно использовать с 1 октября по 30 апреля (<a href="${TA}" rel="noopener">Транспортный департамент Эстонии</a>). Все сроки и что разрешено сегодня: <a href="/teadmine/rehvivahetus/">Смена резины в Эстонии 2026</a>.</div>

<h2>Какая зимняя шина подходит</h2>
<ul>
<li><strong>Протектор не меньше 3 мм.</strong> Это законный минимум для зимней шины. Измерьте глубину протектора до начала сезона.</li>
<li><strong>Знак «три горные вершины и снежинка» ${lumi('Знак «три горные вершины и снежинка» (3PMSF)')}.</strong> У нешипованной зимней шины этот знак обязателен. Транспортный департамент советует выбирать шину и со <strong>знаком льда</strong> — это шина северного типа, прошедшая испытание на льду. Южно- и центральноевропейские зимние шины (только с маркировкой M+S ${ms('Маркировка M+S')}) в Эстонии не подходят.</li>
<li><strong>Шины одного типа на всех колёсах.</strong> Не стоит смешивать шипованные и нешипованные шины: при торможении и в повороте автомобиль ведёт себя непредсказуемо.</li>
</ul>

<h2>Когда менять — что показывают цифры</h2>
<p>Закон говорит, когда <em>можно</em> и когда <em>нужно</em>. Тормозной путь показывает, когда это <em>разумно</em>. Мокрый асфальт, торможение с 90 км/ч (VW Golf, нешипованная зимняя шина северного типа и летняя шина):</p>
${tabel(
		['Температура', 'Летняя шина', 'Зимняя шина'],
		[
			['+10 °C', '44,4 м', '47,5 м'],
			['+7 °C', '46,3 м', '47,2 м'],
			['+5 °C', '47,8 м', '47,1 м'],
			['0 °C', '53,7 м', '46,6 м']
		]
	)}
<p>Примерно при <strong>+5 °C</strong> зимняя шина уже тормозит на мокрой дороге короче: резина летней шины на холоде твердеет. Первый снег и ночные заморозки в Эстонии часто приходят неожиданно — меняйте шины, когда днём держится ниже +7 °C.</p>

<h2>Летняя шина на первом снегу</h2>
<p>На укатанном снегу с 50 км/ч автомобиль на летних шинах останавливается примерно за <strong>60,9 метра</strong>, на зимних — примерно за <strong>26 метров</strong>. На льду разница ещё больше: 165,0 м и 58,9 м. Ожидание первого снега может стоить более 30 метров тормозного пути.</p>

<h2>Старая зимняя шина: переживёт ещё одну зиму?</h2>
<p>Минимум по закону 3 мм, но сцепление теряется раньше. Нешипованная зимняя шина северного типа, тормозной путь с 50 км/ч:</p>
${tabel(
		['Протектор', 'Снег', 'Лёд'],
		[
			['8 мм (новая)', '26,2 м', '58,9 м'],
			['6 мм', '28,4 м', '61,2 м'],
			['4 мм', '31,1 м', '63,8 м'],
			['3 мм', '32,7 м', '65,2 м']
		]
	)}
<p>С протектором 3 мм тормозной путь на снегу на четверть длиннее, чем у новой шины. Если протектор 4 мм или меньше, новые шины лучше купить до сезона, а не посреди зимы.</p>

<h2>Весной — обратно</h2>
<p>Летом зимняя шина тормозит хуже: на сухом асфальте при +25 °C с 90 км/ч летняя шина — 28,6 м, нешипованная зимняя северного типа — 42,0 м. Шипованные шины нужно снять не позднее 31 марта (при зимних условиях — до 30 апреля).</p>

<h2>Проверьте на своём автомобиле</h2>
<ul>
<li><a href="/?olud=snow&kiirus=50#kalkulaator">Тормозной путь на снегу для вашего автомобиля</a></li>
<li><a href="/rehvi-valimine/?hooaeg=winter">Зимние шины в размере вашего автомобиля</a> — по торможению на снегу и льду</li>
<li><a href="/teadmine/artiklid/talverehvi-valimine/">Как выбрать зимнюю шину: шипы или «липучка», северная или европейская</a></li>
</ul>
<p class="note">Сроки: Транспортный департамент Эстонии (Transpordiamet). Тормозной путь — расчётная оценка (VW Golf 8, 205/55 R16, новые шины, без времени реакции), а не измерение. <a href="/ru/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a>.</p>`;

	const KKK = ru
		? [
				['При какой температуре менять резину на зимнюю?', 'Когда днём держится ниже +7 °C и ночью подмораживает. На мокром асфальте зимняя шина тормозит короче летней уже примерно при +5 °C (с 90 км/ч 47,1 м против 47,8 м), а при 0 °C разница больше 7 метров.'],
				['Можно ли ждать на летней резине до первого снега?', 'Летняя резина разрешена до 30 ноября, но на укатанном снегу с 50 км/ч автомобиль на летних шинах останавливается примерно за 61 метр, на зимних примерно за 26 метров.'],
				['Выдержит ли зимняя шина с протектором 4 мм ещё одну зиму?', 'Минимум по закону 3 мм, но с протектором 4 мм тормозной путь на снегу примерно на 5 метров длиннее, чем у новой шины (31,1 м против 26,2 м с 50 км/ч). Новые шины лучше купить до сезона.']
			]
		: [
				['Mis temperatuuril talverehvid alla panna?', 'Kui päeval püsib alla +7 °C ja öösiti tuleb külma. Märjal asfaldil pidurdab talverehv suverehvist lühemalt juba umbes +5 °C juures (90 km/h pealt 47,1 m vs 47,8 m), 0 °C juures on vahe üle 7 meetri.'],
				['Kas suverehvidega võib esimese lumeni oodata?', 'Suverehvid on lubatud 30. novembrini, aga tallatud lumel 50 km/h pealt peatub auto suverehvidega umbes 61 meetriga, talverehvidega umbes 26 meetriga.'],
				['Kas 4 mm mustriga talverehv peab veel talve vastu?', 'Seaduse miinimum on 3 mm, aga 4 mm mustriga on pidurdusmaa lumel umbes 5 meetrit pikem kui uuel rehvil (31,1 m vs 26,2 m 50 km/h pealt). Uued rehvid tasub osta enne hooaega.']
			];
	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	desc={T.desc}
	path="teadmine/artiklid/millal-talverehvid-alla/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/millal-talverehvid-alla/']]}
	lapsed={[]}
	uuendatud={A.uuendatud || A.kuupaev}
	kkk={KKK}
	avaldatud={A.kuupaev}
	sisu={ru ? SISU_RU : SISU}
	image="/og/sait/millal-talverehvid-alla.png"
/>
