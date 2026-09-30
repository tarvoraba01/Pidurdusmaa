<script>
	/* Millal talverehvid alla — seaduse kuupäevad hooajal 2026/27 ja mida
	   pidurdusmaa ütleb vahetamise aja kohta.
	   Kuupäevad: Transpordiamet (14.10.2024), ERR (29.03.2024, 26.11.2019).
	   Pidurdusmaad: sama mudel mis kalkulaator, samad numbrid mis artiklis
	   „Talverehvi valimine“ (VW Golf 8, 205/55 R16, uued rehvid, ilma reaktsiooniajata).
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

	const SISU = `<div class="note-box"><strong>Lühidalt, hooaeg 2026/2027.</strong> Naastrehvid on lubatud <strong>15. oktoobrist 2026 kuni 31. märtsini 2027</strong>. Talverehvid on kohustuslikud <strong>1. detsembrist 2026 kuni 1. märtsini 2027</strong>. Talverehvi muster peab olema sügavam kui <strong>3 mm</strong>.</div>

<h2>Kuupäevad</h2>
${tabel(
		['Mis', 'Millal'],
		[
			['Naastrehvid lubatud', '15.10.2026 – 31.03.2027'],
			['Naastrehvid talveoludes', 'juba 1.10.2026, kuni 30.04.2027'],
			['Talverehvid kohustuslikud', '1.12.2026 – 1.03.2027'],
			['Lamell-talverehvid (naastudeta)', 'lubatud aastaringselt']
		]
	)}
<p>Kui ilm on talvine juba septembri lõpus või veel aprillis, tohib naastrehve kasutada 1. oktoobrist 30. aprillini. Allikas: <a href="${TA}" rel="noopener">Transpordiamet</a>.</p>

<h2>Milline talverehv sobib</h2>
<ul>
<li><strong>Muster üle 3 mm.</strong> See on seaduse miinimum talverehvile. Mõõda mustrisügavust enne hooaega.</li>
<li><strong>Kolme mäetipu ja lumehelbe märk.</strong> Naastudeta talverehvil peab see märk olema. Transpordiamet soovitab valida ka <strong>jäämärgiga</strong> rehvi — see on Põhjamaade rehv, mis on läbinud jääkatse. Lõuna- ja Kesk-Euroopa talverehvid (ainult M+S märgiga) Eestis ei sobi.</li>
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
<p>Tallatud lumel 50 km/h pealt peatub auto suverehvidega <strong>60,9 meetriga</strong>, talverehvidega umbes <strong>26 meetriga</strong>. Jääl on vahe veel suurem: 82,5 m ja 38,9 m. Esimese lumega ootamine võib maksta üle 30 meetri pidurdusmaad.</p>

<h2>Vana talverehv: kas tuleb veel üks talv?</h2>
<p>Seadus lubab kuni 3 mm, aga haare kaob varem. Põhjamaade talverehv, pidurdusmaa 50 km/h pealt:</p>
${tabel(
		['Muster', 'Lumi', 'Jää'],
		[
			['8 mm (uus)', '26,2 m', '38,9 m'],
			['6 mm', '28,4 m', '40,5 m'],
			['4 mm', '31,1 m', '42,3 m'],
			['3 mm', '32,7 m', '43,2 m']
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

	const SISU_RU = `<div class="note-box"><strong>Коротко, сезон 2026/2027.</strong> Шипованные шины разрешены <strong>с 15 октября 2026 по 31 марта 2027</strong>. Зимние шины обязательны <strong>с 1 декабря 2026 по 1 марта 2027</strong>. Глубина протектора зимней шины должна быть больше <strong>3 мм</strong>.</div>

<h2>Сроки</h2>
${tabel(
		['Что', 'Когда'],
		[
			['Шипованные шины разрешены', '15.10.2026 – 31.03.2027'],
			['Шипованные шины при зимних условиях', 'уже с 1.10.2026, до 30.04.2027'],
			['Зимние шины обязательны', '1.12.2026 – 1.03.2027'],
			['Нешипованные зимние шины («липучки»)', 'разрешены круглый год']
		]
	)}
<p>Если зимняя погода наступила уже в конце сентября или держится в апреле, шипованные шины можно использовать с 1 октября по 30 апреля. Источник: <a href="${TA}" rel="noopener">Transpordiamet</a> (Транспортный департамент Эстонии).</p>

<h2>Какая зимняя шина подходит</h2>
<ul>
<li><strong>Протектор глубже 3 мм.</strong> Это законный минимум для зимней шины. Измерьте глубину протектора до начала сезона.</li>
<li><strong>Знак «три горные вершины и снежинка».</strong> У нешипованной зимней шины этот знак обязателен. Транспортный департамент советует выбирать шину и со <strong>знаком льда</strong> — это шина северного типа, прошедшая испытание на льду. Южно- и центральноевропейские зимние шины (только с маркировкой M+S) в Эстонии не подходят.</li>
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
<p>На укатанном снегу с 50 км/ч автомобиль на летних шинах останавливается примерно за <strong>60,9 метра</strong>, на зимних — примерно за <strong>26 метров</strong>. На льду разница ещё больше: 82,5 м и 38,9 м. Ожидание первого снега может стоить более 30 метров тормозного пути.</p>

<h2>Старая зимняя шина: переживёт ещё одну зиму?</h2>
<p>Закон допускает протектор до 3 мм, но сцепление теряется раньше. Нешипованная зимняя шина северного типа, тормозной путь с 50 км/ч:</p>
${tabel(
		['Протектор', 'Снег', 'Лёд'],
		[
			['8 мм (новая)', '26,2 м', '38,9 м'],
			['6 мм', '28,4 м', '40,5 м'],
			['4 мм', '31,1 м', '42,3 м'],
			['3 мм', '32,7 м', '43,2 м']
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
<p class="note">Сроки: Transpordiamet. Тормозной путь — расчётная оценка (VW Golf 8, 205/55 R16, новые шины, без времени реакции), а не измерение. <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a> (на эстонском).</p>`;

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	desc={T.desc}
	path="teadmine/artiklid/millal-talverehvid-alla/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/millal-talverehvid-alla/']]}
	lapsed={[]}
	uuendatud={A.kuupaev}
	avaldatud={A.kuupaev}
	sisu={ru ? SISU_RU : SISU}
	image="/og/sait/millal-talverehvid-alla.png"
/>
