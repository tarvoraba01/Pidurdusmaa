<script>
	import { lumi, jaa } from '$lib/margid.js';
	/* Põhjamaade vs Kesk-Euroopa talverehv — numbrid sama mudeliga mis
	   kalkulaator (engine.js): VW Golf 8, 205/55 R16, uus muster 8 mm.
	   Märgise klassid nagu talverehvi-valimine: Kesk-Euroopa B, Põhjamaade D,
	   naastrehv D. Lumi ja jää −5 °C (jää = tüüpiline jää: 45 ajakirja
	   jäätesti mediaan, model.py ice_road_factor), märg asfalt +10 °C,
	   kuiv +15 °C. Ilma reaktsiooniajata. Talverehvidel treadDepthNewMm 9
	   (muster 8 mm), seepärast erinevad numbrid talverehvi-valimine
	   artiklist (seal 8/8) 1–3%. Numbrid 13.10.2026.
	   Sama teema TikToki videos „Põhjamaade vs Kesk-Euroopa“. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'pohjamaade-voi-kesk-euroopa-talverehv';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Poes on talverehvid tihti kõrvuti ja mõlema küljel on lumehelbega mäe märk ${lumi()}. Ometi on need tehtud väga erineva talve jaoks: Kesk-Euroopa talverehv märja ja lörtsise talve jaoks, Põhjamaade talverehv lume ja jää jaoks.</p>
<p>Pidurdusmaad on arvutatud sama mudeliga, mis <a href="/">kalkulaator</a>: VW Golf 8, rehvimõõt 205/55 R16, uued rehvid (8 mm).</p>
<div class="note-box"><strong>Lühidalt.</strong> Jääl peatub Põhjamaade talverehv 50 km/h pealt 59,9 m, Kesk-Euroopa oma alles 114,9 m pealt, üle 50 meetri hiljem. Lumel on nad peaaegu võrdsed. Märjal asfaldil on Kesk-Euroopa rehv umbes 3 m parem. Eesti talvel, kus jää ja jäide on tavalised, on Põhjamaade rehv kindlam valik.</div>

<h2>Pidurdusmaad kõrvuti</h2>
${tabel(
		['Olud', 'Kesk-Euroopa', 'Põhjamaade (lamell)', 'Naastrehv'],
		[
			['Jää, 50 km/h', '114,9 m', '59,9 m', '46,2 m'],
			['Tallatud lumi, 50 km/h', '27,2 m', '27,1 m', '26,3 m'],
			['Märg asfalt, 90 km/h', '44,9 m', '47,7 m', '52,1 m'],
			['Kuiv asfalt, 90 km/h', '36,3 m', '40,0 m', '40,8 m']
		]
	)}
<p>Suurim vahe on jääl. Lumel haaravad kõik talverehvid sarnaselt, sest lumi jääb mustrisse kinni ja haarab lume vastu. Asfaldil on Kesk-Euroopa rehv parem, aga vahe on mõni meeter, mitte kümneid.</p>

<h2>Miks vahe nii suur on</h2>
<p>Vahe on kummis ja mustris. <strong>Kesk-Euroopa talverehv</strong> on kõvema seguga ja suuremate mustriplokkidega. See hoiab plokid asfaldil stabiilsena ja juhib vett hästi ära, aga jääl libiseb.</p>
<p><strong>Põhjamaade talverehv</strong> on pehmem ja täis peeneid lõikeid ehk lamelle. Iga lõige on serv, mis haarab jääst kinni. Pehme kumm jääb ka kõva külmaga elastseks. Asfaldil teeb sama pehmus plokid liikuvaks, seepärast on märg ja kuiv pidurdus veidi pikem.</p>

<h2>Jää temperatuur muudab palju</h2>
<p>Nulli lähedal on jää märg ja kõige libedam. Pidurdusmaa jääl 50 km/h pealt:</p>
${tabel(
		['Temperatuur', 'Kesk-Euroopa', 'Põhjamaade', 'Vahe'],
		[
			['0 °C', '184,3 m', '101,2 m', '83,1 m'],
			['−5 °C', '114,9 m', '59,9 m', '55,0 m'],
			['−15 °C', '77,6 m', '39,5 m', '38,1 m']
		]
	)}
<p>Just nulli lähedal, sügisel ja kevadel, kui jäide tekib ootamatult, on vahe kõige suurem.</p>

<h2>Kuidas poes vahet teha</h2>
<ul><li><strong>Lumehelbega mäe märk</strong> ${lumi()} (3PMSF) on mõlemal. See näitab ainult, et rehv läbis lumekatse, mitte seda, kuidas ta jääl pidurdab.</li><li><strong>Jää sümbol ELi rehvimärgisel</strong> ${jaa()} näitab, et rehv on läbinud jäähaarde katse. Kesk-Euroopa talverehvidel seda ei ole.</li><li><strong>Küsi Põhjamaade (Nordic) talverehvi.</strong> Tootjad nimetavad neid sageli Nordic, Arctic või Ice. Kesk-Euroopa rehvid kannavad sageli nimes Alpin, Winter või Snow, aga nimi üksi ei ole kindel tunnus.</li><li><strong>Naastrehv</strong> on jääl veel parem, aga asfaldil kõige halvem. Naastrehvid on Eestis lubatud 15. oktoobrist.</li></ul>

<h2>Kellele sobib Kesk-Euroopa talverehv?</h2>
<p>Kui sõidad peamiselt linnas, kus tänavad on hooldatud ja soolatud, ning talvel jääl harva, võib Kesk-Euroopa rehv olla mõistlik. Kui sõidad maanteel, maal või öösel, kui jäide tekib, on Põhjamaade rehv või naastrehv ohutum.</p>

<h2>Vaata ise</h2>
<ul><li><a href="/talverehvid/">Talverehvid</a>: võrdle talverehve oma auto jaoks</li><li><a href="/teadmine/artiklid/naastrehv-voi-lamell/">Naastrehv või lamell? Pidurdusmaad jääl, lumel ja asfaldil</a></li><li><a href="/teadmine/artiklid/talverehvi-valimine/">Talverehvi valimine: mida numbrid ütlevad</a></li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Tegelik pidurdusmaa sõltub rehvi mudelist: parima ja nõrgima rehvi vahe võib testides olla sama suur kui rehvitüüpide vahe. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>В магазине зимние шины часто стоят рядом, и на боковине у обеих — знак горы со снежинкой ${lumi('Знак «три горные вершины и снежинка» (3PMSF)')}. Но сделаны они для совсем разных зим: европейская зимняя шина — для мокрой зимы со слякотью, северная — для снега и льда.</p>
<p>Тормозной путь рассчитан той же моделью, что и <a href="/ru/">калькулятор</a>: VW Golf 8, размер шин 205/55 R16, новые шины (8 мм).</p>
<div class="note-box"><strong>Коротко.</strong> На льду с 50 км/ч северная зимняя шина останавливается за 59,9 м, европейская — только за 114,9 м, больше чем на 50 метров позже. На снегу они почти равны. На мокром асфальте европейская шина примерно на 3 м лучше. Для эстонской зимы, где лёд и гололедица обычное дело, северная шина — более надёжный выбор.</div>

<h2>Тормозной путь рядом</h2>
${tabel(
		['Условия', 'Европейская', 'Северная («липучка»)', 'Шипованная'],
		[
			['Лёд, 50 км/ч', '114,9 м', '59,9 м', '46,2 м'],
			['Укатанный снег, 50 км/ч', '27,2 м', '27,1 м', '26,3 м'],
			['Мокрый асфальт, 90 км/ч', '44,9 м', '47,7 м', '52,1 м'],
			['Сухой асфальт, 90 км/ч', '36,3 м', '40,0 м', '40,8 м']
		]
	)}
<p>Самая большая разница — на льду. На снегу все зимние шины держат похоже: снег забивается в протектор и цепляется за снег. На асфальте европейская шина лучше, но разница — несколько метров, а не десятки.</p>

<h2>Почему разница такая большая</h2>
<p>Разница — в резине и рисунке протектора. <strong>Европейская зимняя шина</strong> сделана из более жёсткой смеси с крупными блоками. Это делает блоки устойчивыми на асфальте и хорошо отводит воду, но на льду шина скользит.</p>
<p><strong>Северная зимняя шина</strong> мягче и покрыта множеством тонких прорезей — ламелей. Каждая прорезь — это кромка, которая цепляется за лёд. Мягкая резина остаётся эластичной и в сильный мороз. На асфальте та же мягкость делает блоки подвижными, поэтому торможение на мокрой и сухой дороге немного длиннее.</p>

<h2>Температура льда меняет многое</h2>
<p>Около нуля лёд мокрый и самый скользкий. Тормозной путь на льду с 50 км/ч:</p>
${tabel(
		['Температура', 'Европейская', 'Северная', 'Разница'],
		[
			['0 °C', '184,3 м', '101,2 м', '83,1 м'],
			['−5 °C', '114,9 м', '59,9 м', '55,0 м'],
			['−15 °C', '77,6 м', '39,5 м', '38,1 м']
		]
	)}
<p>Именно около нуля, осенью и весной, когда гололедица появляется неожиданно, разница самая большая.</p>

<h2>Как отличить в магазине</h2>
<ul><li><strong>Знак горы со снежинкой</strong> ${lumi('Знак «три горные вершины и снежинка» (3PMSF)')} (3PMSF) есть у обеих. Он показывает только, что шина прошла испытание на снегу, а не то, как она тормозит на льду.</li><li><strong>Символ льда на этикетке ЕС</strong> ${jaa('Знак льда (символ сцепления со льдом на этикетке ЕС)')} показывает, что шина прошла испытание на сцепление со льдом. У европейских зимних шин его нет.</li><li><strong>Спрашивайте северную (Nordic) зимнюю шину.</strong> Производители часто называют их Nordic, Arctic или Ice. Европейские шины часто носят в названии Alpin, Winter или Snow, но одно название не надёжный признак.</li><li><strong>Шипованная шина</strong> на льду ещё лучше, но на асфальте хуже всех. Шипованные шины в Эстонии разрешены с 15 октября.</li></ul>

<h2>Кому подходит европейская зимняя шина?</h2>
<p>Если вы ездите в основном по городу, где улицы чистят и посыпают солью, а на лёд попадаете редко, европейская шина может быть разумной. Если вы ездите по трассе, в сельской местности или ночью, когда появляется гололедица, северная или шипованная шина безопаснее.</p>

<h2>Посмотрите сами</h2>
<ul><li><a href="/ru/talverehvid/">Зимние шины</a>: сравните зимние шины для своего автомобиля</li><li><a href="/ru/teadmine/artiklid/naastrehv-voi-lamell/">Шипы или «липучка»: тормозной путь на льду, снегу и асфальте</a></li><li><a href="/ru/teadmine/artiklid/talverehvi-valimine/">Как выбрать зимнюю шину: что говорят цифры</a></li></ul>
<p class="note">Расчётные результаты — это оценки, а не измерения. Реальный тормозной путь зависит от модели шины: в тестах разница между лучшей и худшей шиной бывает такой же большой, как между типами шин. Точность модели и допущения: <a href="/ru/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a>.</p>`;

	const KKK = [
		['Mis vahe on Põhjamaade ja Kesk-Euroopa talverehvil?', 'Põhjamaade talverehv on pehmem ja täis peeneid lõikeid, mis haaravad jääst. Kesk-Euroopa oma on kõvem ja tehtud märjale ja lörtsisele asfaldile. Jääl peatub Põhjamaade rehv 50 km/h pealt 59,9 m, Kesk-Euroopa oma 114,9 m pealt.'],
		['Kas Kesk-Euroopa talverehv sobib Eestisse?', 'Linnas, kus tänavad on hooldatud, võib see sobida. Maanteel ja seal, kus tekib jäide, on Põhjamaade talverehv või naastrehv ohutum, sest jääl on vahe üle 50 meetri.'],
		['Kuidas poes Põhjamaade talverehvi ära tunda?', 'ELi rehvimärgisel on lisaks lumehelbele jää sümbol. Lumehelbega mäe märk on ka Kesk-Euroopa rehvil, seega sellest üksi ei piisa. Küsi müüjalt Põhjamaade ehk Nordic talverehvi.'],
		['Kas Põhjamaade talverehv on asfaldil halvem?', 'Veidi. Märjal asfaldil 90 km/h pealt on pidurdusmaa 47,7 m, Kesk-Euroopa rehviga 44,9 m. Kuival 40,0 m ja 36,3 m.']
	];
	const KKK_RU = [
		['Чем отличаются северная и европейская зимние шины?', 'Северная зимняя шина мягче и покрыта тонкими прорезями, которые цепляются за лёд. Европейская жёстче и сделана для мокрого асфальта и слякоти. На льду с 50 км/ч северная шина останавливается за 59,9 м, европейская — за 114,9 м.'],
		['Подходит ли европейская зимняя шина для Эстонии?', 'В городе, где улицы обслуживаются, может подойти. На трассе и там, где бывает гололедица, северная или шипованная шина безопаснее: на льду разница больше 50 метров.'],
		['Как узнать северную зимнюю шину в магазине?', 'На этикетке ЕС кроме снежинки есть символ льда. Знак горы со снежинкой есть и у европейской шины, поэтому одного его мало. Спросите у продавца северную (Nordic) зимнюю шину.'],
		['Хуже ли северная зимняя шина на асфальте?', 'Немного. На мокром асфальте с 90 км/ч тормозной путь 47,7 м, с европейской шиной 44,9 м. На сухом 40,0 м и 36,3 м.']
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
