<script>
	/* Linnas 50 km/h — numbrid sama mudeliga mis kalkulaator (engine.js):
	   VW Golf 8 1.5 TSI, 205/55 R16, keskmine suverehv (märghaardeklass C),
	   uus muster, autos juht. Reaktsiooniaeg 1,0 s (kalkulaatori vaikeväärtus;
	   ootamatu oht 1,5 s). Kuiv asfalt +15 °C, märg 1 mm vett +10 °C.
	   "Kiirus seal, kus aeglasem auto peatub": kiirema auto pidurdusjälg
	   (stoppingDistance().trace) samal kaugusel. Numbrid 2026-10-07. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'linnas-50-kmh';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Linnas tundub 10 km/h vahe väike: 50 asemel 60 km/h on vaid viiendiku võrra kiirem. Peatumisteekond kasvab aga rohkem, sest pidurdusteekond kasvab kiiruse ruudus. Ja kui midagi juhtub, siis loeb ka see, mis kiirusega auto selles kohas veel sõidab.</p>
<p>Numbrid on arvutatud sama mudeliga, mis <a href="/liiklusohutus/">peatumisteekonna kalkulaator</a>: VW Golf 8, keskmine suverehv, reaktsiooniaeg 1 sekund.</p>
<div class="note-box"><strong>Lühidalt.</strong> 50 km/h pealt peatub auto kuival teel 23,5 m ja märjal 27,4 m pärast ohu märkamist. 60 km/h pealt on see 30,3 m ja 36,1 m. Kohas, kus 50 km/h auto seisab, sõidab 60 km/h auto veel umbes 45 km/h. 40 km/h pealt peatub auto 17,4 m pärast, ehk 6 meetrit varem kui 50 km/h pealt.</div>

<h2>Peatumisteekond linnakiirustel</h2>
<p>Peatumisteekond koosneb kahest osast. Reaktsiooniteekonna sõidab auto täiskiirusel, kuni juht ohtu märkab ja jala pidurile viib. Pidurdusteekond algab siis, kui pidurid tööle hakkavad.</p>
${tabel(
		['Kiirus', 'Reaktsioon (1 s)', 'Pidurdus', 'Kokku, kuiv', 'Kokku, märg'],
		[
			['30 km/h', '8,3 m', '3,7 m', '12,1 m', '13,4 m'],
			['40 km/h', '11,1 m', '6,3 m', '17,4 m', '19,9 m'],
			['50 km/h', '13,9 m', '9,6 m', '23,5 m', '27,4 m'],
			['60 km/h', '16,7 m', '13,6 m', '30,3 m', '36,1 m'],
			['70 km/h', '19,4 m', '18,3 m', '37,8 m', '46,0 m']
		]
	)}
<p>Pidurdusteekond on tabelis kuival teel. Linnakiirusel on reaktsiooniteekond pikem kui pidurdusteekond: 50 km/h pealt läbib auto enne pidurdamist 13,9 m. Seepärast mõjutab linnas tähelepanu peaaegu sama palju kui kiirus. Kui oht tuleb ootamatult ja reaktsiooniaeg on 1,5 sekundit, on märjal peatumisteekond 50 km/h pealt 34,4 m ja 60 km/h pealt 44,5 m.</p>

<h2>Mis kiirusel kiirem auto seal sõidab</h2>
<p>Kaks autot sõidavad kõrvuti ja juht näeb sama ohtu samal ajal. Üks sõidab aeglasemalt ja jõuab enne ohtu peatuda. Mis kiirusega sõidab teine auto samas kohas?</p>
${tabel(
		['Aeglasem auto peatub', 'Kiirem auto samas kohas', 'Kuiv', 'Märg'],
		[
			['30 km/h pealt', '40 km/h pealt', '39 km/h', '36 km/h'],
			['40 km/h pealt', '50 km/h pealt', '42 km/h', '39 km/h'],
			['50 km/h pealt', '60 km/h pealt', '45 km/h', '42 km/h'],
			['50 km/h pealt', '70 km/h pealt', '65 km/h', '61 km/h']
		]
	)}
<p>See on kiiruse kõige olulisem mõju. Seal, kus 50 km/h auto seisab, sõidab 60 km/h auto alles umbes 45 km/h. Pidurdusmaa esimesel poolel langeb kiirus vähe, suurem osa kiirusest kaob alles viimastel meetritel.</p>
<p>30 km/h auto peatub 12,1 m pärast. 50 km/h autol kulub sama vahemaa veel reaktsioonile, ehk see sõidab seal ikka täiskiirusel. 30 km/h pealt on peatumisteekond umbes poole lühem kui 50 km/h pealt.</p>

<h2>Mida see sõidul tähendab</h2>
<ul><li><strong>Ülekäigurajal ja ristmikul</strong> loeb iga meeter: 40 ja 50 km/h vahe on kuival 6 meetrit, 50 ja 60 km/h vahe ligi 7 meetrit.</li><li><strong>Märjal teel</strong> kasvab vahe veel. 60 km/h pealt on peatumisteekond märjal 36,1 m, kuival 30,3 m.</li><li><strong>Telefon või hajameelsus</strong> pikendab reaktsiooniaega. Ainult 0,5 sekundit lisab 50 km/h pealt 7 meetrit.</li></ul>

<h2>Proovi ise</h2>
<ul><li><a href="/liiklusohutus/">Peatumisteekonna kalkulaator</a>: sinu kiirus, reaktsiooniaeg ja teeolud</li><li><a href="/liiklusohutus/reaktsioon/">Reaktsioonimäng</a>: kui kiiresti sina pidurdad?</li><li><a href="/teadmine/pidurdusteekond-ja-peatumisteekond/">Pidurdusteekond ja peatumisteekond</a>: mis on nende vahe</li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>В городе разница в 10 км/ч кажется небольшой: 60 вместо 50 км/ч — всего на пятую часть быстрее. Но остановочный путь растёт сильнее, потому что тормозной путь растёт пропорционально квадрату скорости. А если что-то случится, важно ещё и то, с какой скоростью машина проезжает это место.</p>
<p>Цифры рассчитаны той же моделью, что и <a href="/ru/liiklusohutus/">калькулятор остановочного пути</a>: VW Golf 8, средняя летняя шина, время реакции 1 секунда.</p>
<div class="note-box"><strong>Коротко.</strong> С 50 км/ч машина останавливается на сухой дороге через 23,5 м, на мокрой — через 27,4 м после того, как водитель заметил опасность. С 60 км/ч — 30,3 м и 36,1 м. Там, где машина, ехавшая 50 км/ч, уже стоит, машина, ехавшая 60 км/ч, движется ещё примерно с 45 км/ч. С 40 км/ч машина останавливается через 17,4 м, то есть на 6 метров раньше, чем с 50 км/ч.</div>

<h2>Остановочный путь на городских скоростях</h2>
<p>Остановочный путь состоит из двух частей. Путь реакции машина проезжает на полной скорости, пока водитель замечает опасность и переносит ногу на тормоз. Тормозной путь начинается, когда начинают работать тормоза.</p>
${tabel(
		['Скорость', 'Реакция (1 с)', 'Торможение', 'Всего, сухо', 'Всего, мокро'],
		[
			['30 км/ч', '8,3 м', '3,7 м', '12,1 м', '13,4 м'],
			['40 км/ч', '11,1 м', '6,3 м', '17,4 м', '19,9 м'],
			['50 км/ч', '13,9 м', '9,6 м', '23,5 м', '27,4 м'],
			['60 км/ч', '16,7 м', '13,6 м', '30,3 м', '36,1 м'],
			['70 км/ч', '19,4 м', '18,3 м', '37,8 м', '46,0 м']
		]
	)}
<p>Тормозной путь в таблице — на сухой дороге. На городской скорости путь реакции длиннее тормозного: с 50 км/ч машина до начала торможения проезжает 13,9 м. Поэтому в городе внимание влияет почти так же сильно, как скорость. Если опасность возникает неожиданно и время реакции 1,5 секунды, остановочный путь на мокрой дороге с 50 км/ч — 34,4 м, с 60 км/ч — 44,5 м.</p>

<h2>С какой скоростью там едет более быстрая машина</h2>
<p>Две машины едут рядом, и водители видят одну и ту же опасность одновременно. Одна едет медленнее и успевает остановиться. С какой скоростью другая машина проезжает то же место?</p>
${tabel(
		['Медленная машина останавливается', 'Быстрая машина в том же месте', 'Сухо', 'Мокро'],
		[
			['с 30 км/ч', 'с 40 км/ч', '39 км/ч', '36 км/ч'],
			['с 40 км/ч', 'с 50 км/ч', '42 км/ч', '39 км/ч'],
			['с 50 км/ч', 'с 60 км/ч', '45 км/ч', '42 км/ч'],
			['с 50 км/ч', 'с 70 км/ч', '65 км/ч', '61 км/ч']
		]
	)}
<p>Это самое важное следствие скорости. Там, где машина с 50 км/ч уже стоит, машина с 60 км/ч едет ещё примерно 45 км/ч. На первой половине тормозного пути скорость падает мало, большая её часть теряется только на последних метрах.</p>
<p>Машина с 30 км/ч останавливается через 12,1 м. Машине с 50 км/ч это расстояние ещё уходит на реакцию, то есть там она едет на полной скорости. С 30 км/ч остановочный путь примерно вдвое короче, чем с 50 км/ч.</p>

<h2>Что это значит в дороге</h2>
<ul><li><strong>У пешеходного перехода и на перекрёстке</strong> важен каждый метр: разница между 40 и 50 км/ч на сухой дороге — 6 метров, между 50 и 60 км/ч — почти 7 метров.</li><li><strong>На мокрой дороге</strong> разница ещё больше. С 60 км/ч остановочный путь на мокрой дороге 36,1 м, на сухой — 30,3 м.</li><li><strong>Телефон или рассеянность</strong> удлиняют время реакции. Всего 0,5 секунды добавляют с 50 км/ч 7 метров.</li></ul>

<h2>Проверьте сами</h2>
<ul><li><a href="/ru/liiklusohutus/">Калькулятор остановочного пути</a>: ваша скорость, время реакции и дорожные условия</li><li><a href="/ru/liiklusohutus/reaktsioon/">Игра на реакцию</a>: как быстро тормозите вы?</li><li><a href="/ru/teadmine/pidurdusteekond-ja-peatumisteekond/">Тормозной и остановочный путь</a>: в чём разница</li></ul>
<p class="note">Расчётные результаты — это оценки, а не измерения. Точность модели и допущения: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a> (на эстонском).</p>`;

	const KKK = [
		['Kui pikk on peatumisteekond 50 km/h pealt?', 'Reaktsiooniajaga 1 sekund peatub keskmise suverehviga VW Golf 8 kuival teel 23,5 m ja märjal 27,4 m pärast ohu märkamist. Sellest 13,9 m sõidab auto enne pidurdamist täiskiirusel.'],
		['Kui palju pikem on peatumisteekond 60 km/h pealt?', 'Kuival 30,3 m, ehk 6,8 m rohkem kui 50 km/h pealt. Märjal 36,1 m, ehk 8,7 m rohkem.'],
		['Mis kiirusel sõidab 60 km/h auto seal, kus 50 km/h auto peatub?', 'Kuival umbes 45 km/h ja märjal umbes 42 km/h. Pidurdusmaa esimesel poolel langeb kiirus vähe.'],
		['Kui palju lühem on peatumisteekond 40 km/h pealt?', 'Kuival 17,4 m, ehk 6,1 m lühem kui 50 km/h pealt. Märjal 19,9 m, ehk 7,5 m lühem.']
	];
	const KKK_RU = [
		['Какой остановочный путь с 50 км/ч?', 'При времени реакции 1 секунда VW Golf 8 со средней летней шиной останавливается на сухой дороге через 23,5 м, на мокрой — через 27,4 м после того, как водитель заметил опасность. Из них 13,9 м машина проезжает до начала торможения на полной скорости.'],
		['Насколько длиннее остановочный путь с 60 км/ч?', 'На сухой дороге 30,3 м, то есть на 6,8 м больше, чем с 50 км/ч. На мокрой — 36,1 м, то есть на 8,7 м больше.'],
		['С какой скоростью едет машина с 60 км/ч там, где машина с 50 км/ч останавливается?', 'На сухой дороге примерно 45 км/ч, на мокрой — примерно 42 км/ч. На первой половине тормозного пути скорость падает мало.'],
		['Насколько короче остановочный путь с 40 км/ч?', 'На сухой дороге 17,4 м, то есть на 6,1 м короче, чем с 50 км/ч. На мокрой — 19,9 м, то есть на 7,5 м короче.']
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
