<script>
	/* Vanad ja kulunud rehvid — kõik numbrid on arvutatud sama mudeliga mis
	   kalkulaator ja /rehvi-vanus/ (engine.js): VW Golf 8 1.5 TSI, 205/55 R16,
	   keskmine rehv (märghaardeklass C), autos juht, ilma reaktsiooniajata.
	   Märg asfalt: 1 mm vett, suvi +12 °C. Lumi: tallatud, −5 °C.
	   Uus suverehv 8 mm, uus talverehv 9 mm. Vanus mõjub üle 5 aasta
	   (CAL.ageFreeYears), kuni −13% haardest. Numbrid 2026-10-06. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const A = ARTIKLID.find((a) => a.slug === 'vanad-ja-kulunud-rehvid');
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Rehv ei muutu halvaks üleöö. Muster kulub millimeeter haaval ja kumm kõveneb aasta-aastalt. Sellepärast on raske märgata, millal rehv on oma aja ära elanud. Siin on numbrid, mis seda näitavad.</p>
<p>Pidurdusmaad on arvutatud sama mudeliga mis <a href="/">kalkulaator</a>: VW Golf 8, rehvimõõt 205/55 R16, keskmine rehv (märghaardeklass C). Arvestatud on ainult pidurdusteekonda, reaktsiooniaega mitte.</p>
<div class="note-box"><strong>Lühidalt.</strong> 3 mm mustriga suverehv peatub märjal teel 90 km/h pealt 4,2 m hiljem kui uus. Talverehv peatub 3 mm mustriga lumel veerandi võrra pikemalt. Vanus lisab vähem kui muster, aga 10 aasta vanune rehv peatub ka täie mustriga 2,4 m hiljem. Vanuse saad teada <a href="/rehvi-vanus/">DOT-koodist</a>.</div>

<h2>Kulunud muster märjal teel</h2>
<p>Märjal teel peab muster vee rehvi alt välja juhtima. Mida madalam muster, seda vähem vett ta mahutab ja seda varem hakkab rehv vee peal libisema. Suverehvi pidurdusmaa 90 km/h pealt märjal asfaldil:</p>
${tabel(
		['Mustri sügavus', 'Pidurdusmaa', 'Uuest rehvist rohkem', 'Kiirus, kus uus rehv juba seisab'],
		[
			['8 mm (uus)', '43,9 m', '—', '—'],
			['6 mm', '45,2 m', '+1,3 m', '17 km/h'],
			['4 mm', '46,9 m', '+3,1 m', '25 km/h'],
			['3 mm', '48,0 m', '+4,2 m', '29 km/h'],
			['2 mm', '49,3 m', '+5,5 m', '33 km/h'],
			['1,6 mm (seaduslik piir)', '49,9 m', '+6,1 m', '35 km/h']
		]
	)}
<p>Viimane veerg näitab kiirust kohas, kus uute rehvidega auto on juba seisma jäänud. Seaduslikul piiril 1,6 mm sõidad seal veel 35 km/h. Ees seisvale autole või jalakäijale on see suur vahe.</p>

<h2>Talverehv lumel</h2>
<p>Lumel haakub rehv lumega mustri soonte ja lamellide kaudu. Kui muster kulub, kaob just see haare. Põhjamaade lamellrehvi pidurdusmaa 50 km/h pealt tallatud lumel (−5 °C):</p>
${tabel(
		['Mustri sügavus', 'Pidurdusmaa', 'Uuest rehvist rohkem'],
		[
			['9 mm (uus)', '26,2 m', '—'],
			['7 mm', '28,1 m', '+2,0 m (+7%)'],
			['6 mm', '29,2 m', '+3,0 m (+12%)'],
			['5 mm', '30,4 m', '+4,2 m (+16%)'],
			['4 mm', '31,7 m', '+5,5 m (+21%)'],
			['3 mm (seaduslik piir)', '33,1 m', '+6,9 m (+26%)']
		]
	)}
<p>Seadus lubab talverehvi, mille muster on sügavam kui 3 mm. Aga 4 mm juures on pidurdusmaa lumel juba viiendiku võrra pikem kui uuel rehvil. Kui muster on hooaja alguses 4–5 mm, tasub uued rehvid osta enne lund.</p>

<h2>Vanus</h2>
<p>Kumm kõveneb ka siis, kui rehviga ei sõideta, näiteks garaažis või poe laos. Kõvem kumm haakub halvemini, eriti märjal ja külmal teel. Mudelis hakkab vanus haaret vähendama pärast 5. aastat. Täie mustriga suverehvi pidurdusmaa märjal asfaldil 90 km/h pealt:</p>
${tabel(
		['Rehvi vanus', 'Pidurdusmaa', 'Uuest rehvist rohkem'],
		[
			['kuni 5 aastat', '43,9 m', '—'],
			['8 aastat', '45,3 m', '+1,4 m'],
			['10 aastat', '46,2 m', '+2,4 m'],
			['12 aastat', '47,3 m', '+3,4 m'],
			['15 aastat', '48,9 m', '+5,0 m']
		]
	)}
<p>Vanus lisab vähem kui kulunud muster, aga need liituvad. 10 aastat vana suverehv 2 mm mustriga peatub märjal <strong>8,1 m</strong> hiljem kui uus. Uute rehvidega auto on seal juba seisnud, sina sõidad veel 39 km/h. Rehvitootjad soovitavad üle 5 aasta vanuseid rehve igal aastal kontrollida ja vahetada hiljemalt 10 aasta vanuselt.</p>

<h2>Kuidas rehvi vanust lugeda</h2>
<p>Rehvi küljel on DOT-kood. Selle lõpus on ovaalses raamis 4 numbrit: kaks esimest on tootmisnädal, kaks viimast aasta. <strong>2319</strong> tähendab 23. nädalat 2019 ehk juunit 2019. Kood on sageli ainult rehvi ühel küljel, nii et vaata vajadusel ka sisekülge.</p>
<p>Sisesta numbrid <a href="/rehvi-vanus/">rehvi vanuse kontrolli</a> ja näed vanust ning seda, kui palju sinu rehvi vanus ja muster pidurdusmaad pikendavad.</p>

<h2>Kuidas mustrit mõõta</h2>
<ul><li><strong>Mustrisügavuse mõõtja</strong> maksab paar eurot ja on kõige täpsem. Mõõda kõige kulunuma koha pealt, mitte rehvi keskelt.</li><li><strong>Kulumisnäidikud</strong> on mustrisoonte põhjas väikesed kühmud. Kui muster on nendega tasa, on suverehvi 1,6 mm piir käes. Talverehvidel on sageli eraldi näidik 4 mm juures.</li><li><strong>Ebaühtlane kulumine</strong> (üks serv rohkem kui teine) räägib valest rõhust või rattanurkadest. Siis kulub rehv kiiremini, kui ta peaks.</li></ul>

<h2>Proovi oma autoga</h2>
<ul><li><a href="/rehvi-vanus/">Rehvi vanuse kontroll</a>: DOT-kood, muster ja pidurdusmaa</li><li><a href="/">Pidurdusmaa kalkulaator</a>: sinu auto, sinu rehvid ja mustri sügavus</li><li><a href="/rehvi-valimine/">Rehvi valimine</a>: uued rehvid sinu auto mõõdus</li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>Шина не становится плохой за одну ночь. Протектор стирается миллиметр за миллиметром, а резина год за годом твердеет. Поэтому трудно заметить, когда шина отслужила своё. Вот цифры, которые это показывают.</p>
<p>Тормозной путь рассчитан той же моделью, что и <a href="/ru/">калькулятор</a>: VW Golf 8, размер шин 205/55 R16, средняя шина (класс сцепления на мокром C). Учтён только тормозной путь, без времени реакции.</p>
<div class="note-box"><strong>Коротко.</strong> Летняя шина с протектором 3 мм на мокрой дороге с 90 км/ч останавливается на 4,2 м дальше новой. Зимняя шина с протектором 3 мм на снегу тормозит на четверть дольше. Возраст добавляет меньше, чем износ протектора, но 10-летняя шина даже с полным протектором останавливается на 2,4 м дальше. Возраст шины можно узнать по <a href="/ru/rehvi-vanus/">коду DOT</a>.</div>

<h2>Изношенный протектор на мокрой дороге</h2>
<p>На мокрой дороге протектор должен отводить воду из-под шины. Чем он мельче, тем меньше воды вмещает и тем раньше шина начинает скользить по воде. Тормозной путь летней шины с 90 км/ч на мокром асфальте:</p>
${tabel(
		['Глубина протектора', 'Тормозной путь', 'Больше, чем у новой', 'Скорость там, где новая уже стоит'],
		[
			['8 мм (новая)', '43,9 м', '—', '—'],
			['6 мм', '45,2 м', '+1,3 м', '17 км/ч'],
			['4 мм', '46,9 м', '+3,1 м', '25 км/ч'],
			['3 мм', '48,0 м', '+4,2 м', '29 км/ч'],
			['2 мм', '49,3 м', '+5,5 м', '33 км/ч'],
			['1,6 мм (допустимый минимум)', '49,9 м', '+6,1 м', '35 км/ч']
		]
	)}
<p>Последний столбец показывает скорость в том месте, где машина с новыми шинами уже остановилась. На минимально допустимых 1,6 мм вы там всё ещё едете 35 км/ч.</p>

<h2>Зимняя шина на снегу</h2>
<p>На снегу шина цепляется за снег канавками протектора и ламелями. Когда протектор стирается, исчезает именно это сцепление. Тормозной путь северной фрикционной шины с 50 км/ч на укатанном снегу (−5 °C):</p>
${tabel(
		['Глубина протектора', 'Тормозной путь', 'Больше, чем у новой'],
		[
			['9 мм (новая)', '26,2 м', '—'],
			['7 мм', '28,1 м', '+2,0 м (+7%)'],
			['6 мм', '29,2 м', '+3,0 м (+12%)'],
			['5 мм', '30,4 м', '+4,2 м (+16%)'],
			['4 мм', '31,7 м', '+5,5 м (+21%)'],
			['3 мм (допустимый минимум)', '33,1 м', '+6,9 м (+26%)']
		]
	)}
<p>Закон Эстонии разрешает зимнюю шину с протектором глубже 3 мм. Но уже при 4 мм тормозной путь на снегу на пятую часть длиннее, чем у новой шины. Если в начале сезона протектор 4–5 мм, новые шины лучше купить до снега.</p>

<h2>Возраст</h2>
<p>Резина твердеет, даже если на шине не ездят, например в гараже или на складе магазина. Более твёрдая резина хуже держит дорогу, особенно мокрую и холодную. В модели возраст начинает снижать сцепление после 5 лет. Тормозной путь летней шины с полным протектором на мокром асфальте с 90 км/ч:</p>
${tabel(
		['Возраст шины', 'Тормозной путь', 'Больше, чем у новой'],
		[
			['до 5 лет', '43,9 м', '—'],
			['8 лет', '45,3 м', '+1,4 м'],
			['10 лет', '46,2 м', '+2,4 м'],
			['12 лет', '47,3 м', '+3,4 м'],
			['15 лет', '48,9 м', '+5,0 м']
		]
	)}
<p>Возраст добавляет меньше, чем износ протектора, но они складываются. 10-летняя летняя шина с протектором 2 мм на мокрой дороге останавливается на <strong>8,1 м</strong> дальше новой. Машина с новыми шинами там уже стоит, а вы всё ещё едете 39 км/ч. Производители рекомендуют ежегодно проверять шины старше 5 лет и менять их не позднее чем в 10 лет.</p>

<h2>Как узнать возраст шины</h2>
<p>На боковине шины есть код DOT. В его конце в овальной рамке 4 цифры: первые две — неделя производства, последние две — год. <strong>2319</strong> означает 23-ю неделю 2019 года, то есть июнь 2019. Код часто есть только на одной стороне шины, поэтому при необходимости посмотрите и внутреннюю сторону.</p>
<p>Введите цифры в <a href="/ru/rehvi-vanus/">проверку возраста шины</a> и увидите возраст и насколько возраст и протектор вашей шины удлиняют тормозной путь.</p>

<h2>Как измерить протектор</h2>
<ul><li><strong>Глубиномер</strong> стоит пару евро и точнее всего. Измеряйте в самом изношенном месте, а не по центру шины.</li><li><strong>Индикаторы износа</strong> — небольшие выступы на дне канавок. Если протектор сравнялся с ними, достигнут предел 1,6 мм для летней шины. У зимних шин часто есть отдельный индикатор на 4 мм.</li><li><strong>Неравномерный износ</strong> (один край сильнее другого) говорит о неправильном давлении или углах установки колёс. Тогда шина изнашивается быстрее, чем должна.</li></ul>

<h2>Проверьте на своём автомобиле</h2>
<ul><li><a href="/ru/rehvi-vanus/">Проверка возраста шины</a>: код DOT, протектор и тормозной путь</li><li><a href="/ru/">Калькулятор тормозного пути</a>: ваша машина, ваши шины и глубина протектора</li><li><a href="/ru/rehvi-valimine/">Выбор шин</a>: новые шины в размере вашего автомобиля</li></ul>
<p class="note">Расчётные результаты — это оценки, а не измерения. Точность модели и допущения: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a> (на эстонском).</p>`;

	const KKK = [
		['Kui palju pikeneb pidurdusmaa kulunud rehviga?', 'VW Golf 8 peatub märjal teel 90 km/h pealt uue suverehviga 43,9 m pealt. 3 mm mustriga on pidurdusmaa 48,0 m ehk 4,2 m pikem, seadusliku piiri 1,6 mm juures 49,9 m. Talverehv peatub lumel 3 mm mustriga veerandi võrra pikemalt kui uus.'],
		['Kui vana rehviga võib sõita?', 'Seadus rehvi vanust ei piira. Rehvitootjad soovitavad üle 5 aasta vanuseid rehve igal aastal kontrollida ja vahetada hiljemalt 10 aasta vanuselt, sest kumm kõveneb ja haare väheneb ka täie mustriga.'],
		['Kuidas teada saada rehvi vanust?', 'Rehvi küljel on DOT-kood, mille lõpus on ovaalses raamis 4 numbrit: kaks esimest on tootmisnädal ja kaks viimast aasta. Näiteks 2319 tähendab 23. nädalat 2019.'],
		['Kui sügav peab olema rehvi muster Eestis?', 'Suverehvil vähemalt 1,6 mm, talverehvil sügavam kui 3 mm. Pidurdusmaa hakkab pikenema palju varem: lumel on talverehvi pidurdusmaa 4 mm mustriga juba viiendiku võrra pikem kui uuel rehvil.']
	];
	const KKK_RU = [
		['Насколько удлиняется тормозной путь на изношенной шине?', 'VW Golf 8 на мокрой дороге с 90 км/ч останавливается на новой летней шине за 43,9 м. С протектором 3 мм тормозной путь 48,0 м, то есть на 4,2 м длиннее, при допустимом минимуме 1,6 мм — 49,9 м. Зимняя шина с протектором 3 мм на снегу тормозит на четверть дольше новой.'],
		['Сколько лет можно ездить на шинах?', 'Закон возраст шины не ограничивает. Производители рекомендуют ежегодно проверять шины старше 5 лет и менять их не позднее чем в 10 лет, потому что резина твердеет и сцепление снижается даже при полном протекторе.'],
		['Как узнать возраст шины?', 'На боковине шины есть код DOT, в конце которого в овальной рамке 4 цифры: первые две — неделя производства, последние две — год. Например, 2319 означает 23-ю неделю 2019 года.'],
		['Какой должна быть глубина протектора в Эстонии?', 'У летней шины не меньше 1,6 мм, у зимней — больше 3 мм. Тормозной путь начинает расти намного раньше: на снегу при протекторе 4 мм он уже на пятую часть длиннее, чем у новой шины.']
	];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	desc={T.desc}
	path="teadmine/artiklid/vanad-ja-kulunud-rehvid/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/vanad-ja-kulunud-rehvid/']]}
	lapsed={[]}
	uuendatud={A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/rehvi-vanus.png"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
