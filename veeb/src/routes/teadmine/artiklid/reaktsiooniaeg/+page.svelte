<script>
	/* Reaktsiooniaeg — numbrid sama mudeliga mis kalkulaator (engine.js):
	   VW Golf 8, 205/55 R16, suverehv märgise klass B, uus muster 8 mm.
	   Märg asfalt 1 mm vett +10 °C, kuiv +15 °C. Reaktsiooniteekond = kiirus × aeg.
	   Põdra näide: põder 80 m kaugusel, 90 km/h, märg tee; löögikiirus
	   v = 90·√(1 − ülejäänud maa / pidurdusmaa). Numbrid 2026-10-12
	   (tookoda/artikli-numbrid.mjs). Sama teema TikToki videos „Reaktsioon“. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'reaktsiooniaeg';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Kui ees juhtub midagi ootamatut, ei hakka auto kohe aeglustuma. Enne peab silm ohu märkama, aju otsustama ja jalg pidurile liikuma. Selle aja sõidab auto täiskiirusel edasi.</p>
<p>Pidurdusmaad on arvutatud sama mudeliga, mis <a href="/">kalkulaator</a>: VW Golf 8, rehvimõõt 205/55 R16, uus keskmine suverehv.</p>
<div class="note-box"><strong>Lühidalt.</strong> 90 km/h juures sõidab auto ühe sekundiga 25 meetrit. Märjal teel lisandub pidurdusmaa 44,4 m, kokku on peatumisteekond 69,4 m. Kui vaatasid sel hetkel kaks sekundit telefoni, tuleb otsa veel 50 meetrit.</div>

<h2>Mis on reaktsiooniaeg</h2>
<p>Reaktsiooniaeg on aeg ohu ilmumisest hetkeni, mil pidur hakkab tööle. Ärksal juhil, kes ohtu ootab, kulub selleks umbes üks sekund. Väsinult, hajameelselt või siis, kui oht tuleb täiesti ootamatult, on see sageli 1,5–2 sekundit.</p>
<p>Reaktsiooniteekond on lihtsalt kiirus korda aeg. Rehvid, teeolud ega auto seda ei muuda.</p>

<h2>Peatumisteekond eri kiirustel</h2>
<p>Reaktsiooniaeg 1 sekund, siis pidurdus:</p>
${tabel(
		['Kiirus', 'Reaktsioon (1 s)', 'Pidurdus märjal', 'Kokku märjal', 'Kokku kuival'],
		[
			['50 km/h', '13,9 m', '13,4 m', '27,3 m', '23,5 m'],
			['70 km/h', '19,4 m', '26,3 m', '45,8 m', '37,8 m'],
			['90 km/h', '25,0 m', '44,4 m', '69,4 m', '54,8 m'],
			['110 km/h', '30,6 m', '68,3 m', '98,8 m', '74,7 m']
		]
	)}
<p>Linnakiirusel on reaktsiooniteekond sama pikk kui pidurdusmaa ise. Maanteel on pidurdusmaa küll pikem, aga ka siis läheb esimese sekundiga 25–30 meetrit, enne kui midagi juhtuma hakkab.</p>

<h2>Näide: põder 80 meetri kaugusel</h2>
<p>Sõidad märjal maanteel 90 km/h ja 80 meetri kaugusel hüppab teele põder.</p>
<ul><li><strong>Ärkvel juht (1 s):</strong> 25 m reaktsiooni ja 44,4 m pidurdust. Auto seisab 69,4 m pärast, umbes 10 meetrit enne põtra.</li><li><strong>Väsinud juht (1,5 s):</strong> 37,5 m reaktsiooni, pidurdamiseks jääb 42,5 m. Põdrani jõuab auto veel umbes 19 km/h kiirusega.</li><li><strong>Telefoni vaatav juht (2 s pimesi + 1 s reaktsiooni):</strong> 75 m on läbitud enne, kui pidur tööle hakkab. Pidurdamiseks jääb 5 meetrit ja löök tuleb umbes 85 km/h kiirusega.</li></ul>
<p>Sama tee, sama auto ja samad rehvid. Vahe tuleb ainult sellest, millal juht ohtu märkab.</p>

<h2>Kuidas meetreid juurde võita</h2>
<ul><li><strong>Vaata kaugele.</strong> Mida varem ohtu märkad, seda rohkem on sul maad pidurdada. 90 km/h juures on iga sekund 25 meetrit.</li><li><strong>Telefon käest.</strong> Kahesekundiline pilk ekraanile on 90 km/h juures 50 meetrit pimesi sõitu.</li><li><strong>Hoia pikivahet.</strong> Vähemalt kaks sekundit eessõitjast, märjal ja pimedas rohkem. Vaata <a href="/liiklusohutus/pikivahe/">pikivahe simulaatorit</a>.</li><li><strong>Ära sõida väsinult.</strong> Väsimus pikendab reaktsiooniaega sama palju kui telefon.</li></ul>

<h2>Proovi ise</h2>
<ul><li><a href="/liiklusohutus/reaktsioon/">Reaktsioonimäng</a>: kui kiiresti sina reageerid?</li><li><a href="/">Pidurdusmaa kalkulaator</a>: muuda kiirust, reaktsiooniaega ja teeolusid</li><li><a href="/teadmine/artiklid/linnas-50-kmh/">Linnas 50 km/h: kui palju on vahet 40 ja 60 km/h vahel?</a></li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>Когда впереди происходит что-то неожиданное, машина не начинает замедляться сразу. Сначала глаз должен заметить опасность, мозг — принять решение, а нога — перейти на тормоз. Всё это время машина едет на полной скорости.</p>
<p>Тормозной путь рассчитан той же моделью, что и <a href="/ru/">калькулятор</a>: VW Golf 8, размер шин 205/55 R16, новая средняя летняя шина.</p>
<div class="note-box"><strong>Коротко.</strong> На скорости 90 км/ч машина за одну секунду проезжает 25 метров. На мокрой дороге к этому добавляется тормозной путь 44,4 м, всего остановочный путь 69,4 м. Если в этот момент вы две секунды смотрели в телефон, добавляется ещё 50 метров.</div>

<h2>Что такое время реакции</h2>
<p>Время реакции — это время от появления опасности до момента, когда начинает работать тормоз. У внимательного водителя, который ожидает опасность, на это уходит около секунды. Усталому, рассеянному водителю или при совсем неожиданной опасности часто нужно 1,5–2 секунды.</p>
<p>Путь за время реакции — это просто скорость, умноженная на время. Шины, дорога и машина на него не влияют.</p>

<h2>Остановочный путь на разных скоростях</h2>
<p>Время реакции 1 секунда, затем торможение:</p>
${tabel(
		['Скорость', 'Реакция (1 с)', 'Торможение на мокрой', 'Всего на мокрой', 'Всего на сухой'],
		[
			['50 км/ч', '13,9 м', '13,4 м', '27,3 м', '23,5 м'],
			['70 км/ч', '19,4 м', '26,3 м', '45,8 м', '37,8 м'],
			['90 км/ч', '25,0 м', '44,4 м', '69,4 м', '54,8 м'],
			['110 км/ч', '30,6 м', '68,3 м', '98,8 м', '74,7 м']
		]
	)}
<p>На городской скорости путь за время реакции такой же длинный, как сам тормозной путь. На трассе тормозной путь длиннее, но и там за первую секунду проходит 25–30 метров, прежде чем что-то начинает происходить.</p>

<h2>Пример: лось в 80 метрах</h2>
<p>Вы едете по мокрой трассе 90 км/ч, и в 80 метрах на дорогу выскакивает лось.</p>
<ul><li><strong>Внимательный водитель (1 с):</strong> 25 м реакции и 44,4 м торможения. Машина останавливается через 69,4 м, примерно в 10 метрах от лося.</li><li><strong>Усталый водитель (1,5 с):</strong> 37,5 м реакции, на торможение остаётся 42,5 м. До лося машина доезжает со скоростью около 19 км/ч.</li><li><strong>Водитель с телефоном (2 с вслепую + 1 с реакции):</strong> 75 м пройдено до того, как начинает работать тормоз. На торможение остаётся 5 метров, и удар происходит на скорости около 85 км/ч.</li></ul>
<p>Та же дорога, та же машина, те же шины. Разница только в том, когда водитель замечает опасность.</p>

<h2>Как выиграть метры</h2>
<ul><li><strong>Смотрите далеко вперёд.</strong> Чем раньше вы заметите опасность, тем больше у вас места для торможения. На 90 км/ч каждая секунда — это 25 метров.</li><li><strong>Отложите телефон.</strong> Двухсекундный взгляд на экран на 90 км/ч — это 50 метров езды вслепую.</li><li><strong>Держите дистанцию.</strong> Минимум две секунды до впереди идущей машины, на мокрой дороге и в темноте больше. Посмотрите <a href="/ru/liiklusohutus/pikivahe/">симулятор дистанции</a>.</li><li><strong>Не садитесь за руль уставшим.</strong> Усталость удлиняет время реакции так же, как телефон.</li></ul>

<h2>Попробуйте сами</h2>
<ul><li><a href="/ru/liiklusohutus/reaktsioon/">Игра на реакцию</a>: насколько быстро реагируете вы?</li><li><a href="/ru/">Калькулятор тормозного пути</a>: меняйте скорость, время реакции и дорожные условия</li><li><a href="/ru/teadmine/artiklid/linnas-50-kmh/">50 км/ч в городе: какая разница между 40 и 60 км/ч?</a></li></ul>
<p class="note">Расчётные результаты — это оценки, а не измерения. Точность модели и допущения: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a> (на эстонском).</p>`;

	const KKK = [
		['Kui pikk on reaktsiooniaeg?', 'Ärksal juhil, kes ohtu ootab, umbes 1 sekund. Väsinult, hajameelselt või täiesti ootamatu ohu korral sageli 1,5–2 sekundit.'],
		['Kui palju sõidab auto reaktsiooniaja jooksul?', 'Ühe sekundiga 50 km/h juures 13,9 m, 70 km/h juures 19,4 m, 90 km/h juures 25 m ja 110 km/h juures 30,6 m.'],
		['Kui pikk on peatumisteekond 90 km/h pealt?', 'Märjal asfaldil 1-sekundilise reaktsiooniga umbes 69,4 m (25 m reaktsiooni ja 44,4 m pidurdust), kuival umbes 54,8 m. VW Golf 8, uus keskmine suverehv.'],
		['Kui palju lisab telefoni vaatamine?', 'Kahesekundiline pilk telefoni on 90 km/h juures 50 meetrit, mille jooksul juht teed ei näe. See lisandub tavalisele reaktsiooniajale.']
	];
	const KKK_RU = [
		['Какое время реакции у водителя?', 'У внимательного водителя, который ожидает опасность, около 1 секунды. Усталому, рассеянному или при совсем неожиданной опасности часто 1,5–2 секунды.'],
		['Сколько проезжает машина за время реакции?', 'За одну секунду на 50 км/ч — 13,9 м, на 70 км/ч — 19,4 м, на 90 км/ч — 25 м и на 110 км/ч — 30,6 м.'],
		['Какой остановочный путь с 90 км/ч?', 'На мокром асфальте с реакцией 1 секунда около 69,4 м (25 м реакции и 44,4 м торможения), на сухом около 54,8 м. VW Golf 8, новая средняя летняя шина.'],
		['Сколько добавляет взгляд в телефон?', 'Двухсекундный взгляд в телефон на 90 км/ч — это 50 метров, в течение которых водитель не видит дорогу. Это добавляется к обычному времени реакции.']
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
