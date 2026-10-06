<script>
	/* Naastrehv või lamell — mõõdetud tulemused: Tekniikan Maailma 2025
	   (core.json sources.TM25: 205/55 R16, VW Golf, 7 naastrehvi + 7 Põhjamaade
	   lamelli; kuiv 80→0, märg 80→0, jää 50→0) ja Vi Bilägare 2010
	   (sources.VIB10D: jää 30→5 −2,5 °C ja +0,75 °C, lumi 45→5; lamell =
	   Continental VikingContact 5). Temperatuuri tabel ja lumi: mudel
	   (engine.js), VW Golf 8, kategooria keskmine (klass C), sõidutee jää.
	   Numbrid 2026-10-07. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'naastrehv-voi-lamell';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Igal sügisel tuleb valida, kas panna alla naastrehvid või naastudeta Põhjamaade talverehvid (lamellrehvid). Siin on vastus mõõtmistest: kus naast on parem, kus ei ole ja kui suur vahe on.</p>
<div class="note-box"><strong>Lühidalt.</strong> Jääl peatub naastrehv selgelt varem: Tekniikan Maailma 2025 testis 50 km/h pealt keskmiselt 36,9 m, lamell 49,4 m. Isegi halvim naastrehv oli jääl parem kui parim lamell. Kõige suurem on naastu eelis jääl nulli lähedal. Kuival ja märjal asfaldil on vahe väike ning sõltub rohkem rehvimudelist kui sellest, kas rehvil on naastud.</div>

<h2>Mõõdetud: Tekniikan Maailma 2025</h2>
<p>Soome ajakiri testis 2025. aastal samas mõõdus (205/55 R16) ja samal autol 7 naastrehvi ja 7 Põhjamaade lamelli. Pidurdusmaa meetrites, keskmine ja vahemik:</p>
${tabel(
		['Pind', 'Naastrehv', 'Lamell'],
		[
			['Jää, 50→0 km/h', '36,9 m (32,3–42,5)', '49,4 m (45,6–53,5)'],
			['Märg asfalt, 80→0 km/h', '36,9 m (34,3–40,8)', '38,7 m (37,5–41,1)'],
			['Kuiv asfalt, 80→0 km/h', '32,2 m (31,5–33,4)', '31,5 m (30,8–32,6)']
		]
	)}
<p><strong>Jääl</strong> on vahe keskmiselt 12,5 meetrit ehk kolmandik. Parim lamell (Michelin X-Ice Snow, 45,6 m) peatus 3 meetrit hiljem kui halvim naastrehv (Continental IceContact 3, 42,5 m).</p>
<p><strong>Märjal asfaldil</strong> olid naastrehvid keskmiselt 1,8 m paremad, aga vahemikud kattuvad: testi parim rehv (34,3 m) oli naastrehv, kuid ka üks halvemaid (40,8 m) oli naastrehv. Siin loeb rohkem konkreetne mudel.</p>
<p><strong>Kuival asfaldil</strong> olid lamellid keskmiselt 0,7 m paremad. See vahe on väike.</p>

<h2>Jää nulli lähedal: naastu suurim eelis</h2>
<p>Kumm haakub jääga seda halvemini, mida lähemal on temperatuur nullile, sest jää pinnal on siis õhuke veekiht. Nael lõikab jäässe ja ei sõltu sellest nii palju. Rootsi ajakiri Vi Bilägare mõõtis 2010. aastal jääl samal päeval kahel temperatuuril (pidurdus 30→5 km/h):</p>
${tabel(
		['Jää temperatuur', 'Naastrehvid (7)', 'Lamell (VikingContact 5)'],
		[
			['−2,5 °C', '23,0–28,2 m', '28,1 m'],
			['+0,75 °C (sulav)', '26,3–35,5 m', '47,4 m']
		]
	)}
<p>Sulaval jääl pikenes lamelli pidurdusmaa üle poole, naastrehvidel vähem. Sama näitab mudel, mida kasutab ka <a href="/">kalkulaator</a> (VW Golf 8, keskmine rehv, sõidutee jää, 50→0 km/h):</p>
${tabel(
		['Temperatuur', 'Naastrehv', 'Lamell'],
		[
			['0 °C', '40,1 m', '58,6 m'],
			['−2 °C', '36,0 m', '49,2 m'],
			['−5 °C', '31,4 m', '38,9 m']
		]
	)}
<p>Väga külmal kõval jääl (−10 °C ja külmem) pidurdab mudeli järgi lamell isegi lühemalt, sest naast ei lähe kõvasse jäässe hästi sisse. See põhineb ühel testil (Za Rulem 2008, samad rehvid neljal temperatuuril), nii et see osa on ebakindlam. Eesti talvel on jää aga sageli just nulli lähedal: hommikune kiilasjää, sulailm ja öökülm.</p>

<h2>Lumi</h2>
<p>Lumel on vahe väike. Vi Bilägare testis oli pidurdusmaa tallatud lumel 45→5 km/h pealt naastrehvidel 36,3–43,0 m ja lamellil 42,3 m. Mudeli järgi on vahe 50 km/h pealt −5 °C juures alla meetri: naastrehv 25,4 m, lamell 26,2 m.</p>

<h2>Kumb valida</h2>
<ul><li><strong>Naastrehv</strong> on parem, kui sõidad sageli jäistel teedel, näiteks maal ja maanteel, eriti sulailmaga.</li><li><strong>Lamell</strong> sobib, kui sõidad peamiselt linnas puhastatud teedel. Kuival ja märjal asfaldil pidurdab hea lamell sama hästi kui naastrehv.</li><li><strong>Mudelite vahe on suur.</strong> Hea lamell on märjal parem kui halb naastrehv. Vaata konkreetsete rehvide tulemusi <a href="/talverehvid/">talverehvide lehelt</a>.</li></ul>
<p>Naastrehvid on Eestis lubatud 15. oktoobrist 31. märtsini. Kõik kuupäevad: <a href="/teadmine/artiklid/millal-talverehvid-alla/">Millal talverehvid alla?</a></p>

<h2>Proovi oma autoga</h2>
<ul><li><a href="/">Pidurdusmaa kalkulaator</a>: vali olud "jää" ja võrdle naastrehvi ning lamelli oma autoga</li><li><a href="/teadmine/artiklid/talverehvide-testid-2026/">Talverehvide testid 2025–2026</a>: kõik mõõdetud pidurdusmaad</li><li><a href="/teadmine/artiklid/talverehvi-valimine/">Talverehvi valimine: mida numbrid ütlevad</a></li></ul>
<p class="note">Testitulemused on mõõdetud testiväljakul. Mudeli tulemused on hinnangud. Allikad: <a href="/testid/tm25/">Tekniikan Maailma 2025</a>, <a href="/testid/vib10d/">Vi Bilägare 2010</a>.</p>`;

	const SISU_RU = `<p>Каждую осень приходится выбирать: шипованные шины или нешипованные зимние шины северного типа («липучка»). Здесь ответ по измерениям: где шипы лучше, где нет и насколько велика разница.</p>
<div class="note-box"><strong>Коротко.</strong> На льду шипованная шина останавливается заметно раньше: в тесте Tekniikan Maailma 2025 с 50 км/ч в среднем за 36,9 м, «липучка» — за 49,4 м. Даже худшая шипованная шина на льду была лучше лучшей «липучки». Больше всего преимущество шипов на льду около нуля. На сухом и мокром асфальте разница небольшая и зависит больше от модели шины, чем от наличия шипов.</div>

<h2>Измерено: Tekniikan Maailma 2025</h2>
<p>Финский журнал в 2025 году испытал в одном размере (205/55 R16) на одной машине 7 шипованных шин и 7 «липучек» северного типа. Тормозной путь в метрах, среднее и разброс:</p>
${tabel(
		['Покрытие', 'Шипованная', '«Липучка»'],
		[
			['Лёд, 50→0 км/ч', '36,9 м (32,3–42,5)', '49,4 м (45,6–53,5)'],
			['Мокрый асфальт, 80→0 км/ч', '36,9 м (34,3–40,8)', '38,7 м (37,5–41,1)'],
			['Сухой асфальт, 80→0 км/ч', '32,2 м (31,5–33,4)', '31,5 м (30,8–32,6)']
		]
	)}
<p><strong>На льду</strong> разница в среднем 12,5 метра, то есть треть. Лучшая «липучка» (Michelin X-Ice Snow, 45,6 м) остановилась на 3 метра дальше худшей шипованной шины (Continental IceContact 3, 42,5 м).</p>
<p><strong>На мокром асфальте</strong> шипованные шины были в среднем на 1,8 м лучше, но разброс перекрывается: лучшая шина теста (34,3 м) была шипованной, но и одна из худших (40,8 м) тоже. Здесь важнее конкретная модель.</p>
<p><strong>На сухом асфальте</strong> «липучки» были в среднем на 0,7 м лучше. Это небольшая разница.</p>

<h2>Лёд около нуля: главное преимущество шипов</h2>
<p>Резина держит лёд тем хуже, чем ближе температура к нулю, потому что на поверхности льда появляется тонкий слой воды. Шип врезается в лёд и зависит от этого меньше. Шведский журнал Vi Bilägare в 2010 году измерил торможение на льду в один день при двух температурах (торможение 30→5 км/ч):</p>
${tabel(
		['Температура льда', 'Шипованные (7)', '«Липучка» (VikingContact 5)'],
		[
			['−2,5 °C', '23,0–28,2 м', '28,1 м'],
			['+0,75 °C (тающий)', '26,3–35,5 м', '47,4 м']
		]
	)}
<p>На тающем льду тормозной путь «липучки» вырос больше чем в полтора раза, у шипованных шин — меньше. То же показывает модель, которую использует и <a href="/ru/">калькулятор</a> (VW Golf 8, средняя шина, лёд на дороге, 50→0 км/ч):</p>
${tabel(
		['Температура', 'Шипованная', '«Липучка»'],
		[
			['0 °C', '40,1 м', '58,6 м'],
			['−2 °C', '36,0 м', '49,2 м'],
			['−5 °C', '31,4 м', '38,9 м']
		]
	)}
<p>На очень холодном твёрдом льду (−10 °C и холоднее) «липучка» по модели тормозит даже короче, потому что шип плохо входит в твёрдый лёд. Это основано на одном тесте (Za Rulem 2008, одни и те же шины при четырёх температурах), поэтому эта часть менее надёжна. Но эстонской зимой лёд часто именно около нуля: утренний гололёд, оттепель и ночные заморозки.</p>

<h2>Снег</h2>
<p>На снегу разница небольшая. В тесте Vi Bilägare тормозной путь на укатанном снегу с 45 до 5 км/ч у шипованных шин составил 36,3–43,0 м, у «липучки» — 42,3 м. По модели с 50 км/ч при −5 °C разница меньше метра: шипованная шина 25,4 м, «липучка» 26,2 м.</p>

<h2>Что выбрать</h2>
<ul><li><strong>Шипованная шина</strong> лучше, если вы часто ездите по обледенелым дорогам, например за городом и по трассе, особенно в оттепель.</li><li><strong>«Липучка»</strong> подходит, если вы ездите в основном по очищенным городским дорогам. На сухом и мокром асфальте хорошая «липучка» тормозит так же, как шипованная шина.</li><li><strong>Разница между моделями большая.</strong> Хорошая «липучка» на мокрой дороге лучше плохой шипованной шины. Результаты конкретных шин — на <a href="/ru/talverehvid/">странице зимних шин</a>.</li></ul>
<p>Шипованные шины в Эстонии разрешены с 15 октября по 31 марта. Все сроки: <a href="/ru/teadmine/artiklid/millal-talverehvid-alla/">Когда менять шины на зимние?</a></p>

<h2>Проверьте на своём автомобиле</h2>
<ul><li><a href="/ru/">Калькулятор тормозного пути</a>: выберите условия «лёд» и сравните шипованную шину и «липучку» на своей машине</li><li><a href="/ru/teadmine/artiklid/talverehvide-testid-2026/">Тесты зимних шин 2025–2026</a>: весь измеренный тормозной путь</li><li><a href="/ru/teadmine/artiklid/talverehvi-valimine/">Как выбрать зимнюю шину: что говорят цифры</a></li></ul>
<p class="note">Результаты тестов измерены на испытательном полигоне. Результаты модели — оценки. Источники: <a href="/testid/tm25/">Tekniikan Maailma 2025</a>, <a href="/testid/vib10d/">Vi Bilägare 2010</a> (на эстонском).</p>`;

	const KKK = [
		['Kas naastrehv pidurdab jääl paremini kui lamell?', 'Jah. Tekniikan Maailma 2025 testis peatusid naastrehvid jääl 50 km/h pealt keskmiselt 36,9 m ja Põhjamaade lamellid 49,4 m pärast. Halvim naastrehv (42,5 m) oli parem kui parim lamell (45,6 m).'],
		['Kas lamell on märjal või kuival asfaldil parem?', 'Vahe on väike. Samas testis olid märjal keskmiselt paremad naastrehvid (36,9 m vs 38,7 m), kuival lamellid (31,5 m vs 32,2 m). Rehvimudelite vahe on suurem kui naastu ja lamelli vahe.'],
		['Millal on naastrehvi eelis kõige suurem?', 'Jääl nulli lähedal. Vi Bilägare testis oli lamelli pidurdusmaa +0,75 °C jääl 47,4 m, naastrehvidel 26,3–35,5 m. −2,5 °C juures oli vahe palju väiksem.'],
		['Kas lumel on naastrehvi ja lamelli vahel vahe?', 'Väike. Mudeli järgi on vahe 50 km/h pealt −5 °C juures alla meetri (25,4 m ja 26,2 m).']
	];
	const KKK_RU = [
		['Шипованная шина тормозит на льду лучше «липучки»?', 'Да. В тесте Tekniikan Maailma 2025 шипованные шины на льду с 50 км/ч останавливались в среднем через 36,9 м, а нешипованные шины северного типа — через 49,4 м. Худшая шипованная шина (42,5 м) была лучше лучшей «липучки» (45,6 м).'],
		['«Липучка» лучше на мокром или сухом асфальте?', 'Разница небольшая. В том же тесте на мокром асфальте в среднем были лучше шипованные (36,9 м против 38,7 м), на сухом — «липучки» (31,5 м против 32,2 м). Разница между моделями больше, чем между шипами и «липучкой».'],
		['Когда преимущество шипов больше всего?', 'На льду около нуля. В тесте Vi Bilägare тормозной путь «липучки» на льду при +0,75 °C составил 47,4 м, у шипованных шин — 26,3–35,5 м. При −2,5 °C разница была намного меньше.'],
		['Есть ли разница между шипами и «липучкой» на снегу?', 'Небольшая. По модели с 50 км/ч при −5 °C разница меньше метра (25,4 м и 26,2 м).']
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
