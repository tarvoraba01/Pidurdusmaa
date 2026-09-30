<script>
	/* Talverehvide testid hooajal 2025/26 ja 2026 sügisel — ainult avaldatud
	   absoluutsed pidurdusmaad (meie testide andmebaas):
	     Vi Bilägare 2025 lamell ja naast 235/60 R18 (Volvo XC60), 2026 naast 215/65 R17
	     (mudel/testid_ext/vi_bilagare_2025_2026.json, allikas motor.no / tyrereviews.com);
	     Tekniikan Maailma 2025 205/55 R16 ja ADAC 2025 (core.json TM25 / ADAC25).
	   Uusi teste lisame, kui nende mõõdetud meetrid on avalikud.
	   Vene tekst: SISU_RU (/ru/teadmine/artiklid/talverehvide-testid-2026/). */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const A = ARTIKLID.find((a) => a.slug === 'talverehvide-testid-2026');
	const ru = keel.lang === 'ru';
	const R = (s, n) => `<a href="/rehvid/${s}/">${n}</a>`;

	const SISU = `<p><strong>Talverehvide testid näitavad igal sügisel sama pilti:</strong> lumel on head ja keskmised rehvid peaaegu võrdsed, aga jääl ja märjal asfaldil võib vahe olla mitu autopikkust. Kogusime kokku viimaste testide <em>mõõdetud</em> pidurdusmaad — ainult meetrid, mitte punktid ega hinded.</p>

<h2>Jää: kõige suurem vahe</h2>
<p><strong>Vi Bilägare 2026, naastrehvid 215/65 R17</strong> (VW Tiguan): 25 km/h pealt 5 km/h-ni pidurdas parim ${R('bridgestone-blizzak-spike-3', 'Bridgestone Blizzak Spike 3')} <strong>8,3 meetriga</strong>, halvim ${R('kumho-wintercraft-ice-wi32', 'Kumho WinterCraft Ice Wi32')} <strong>17,6 meetriga</strong> — rohkem kui kaks korda pikemalt. Blizzak Spike 3 kõrvaldati küll pingereast, sest naelad ulatusid lubatust kaugemale.</p>
<p><strong>Vi Bilägare 2025, naastrehvid 235/60 R18</strong> (Volvo XC60): parim ${R('nokian-hakkapeliitta-10', 'Nokian Hakkapeliitta 10 SUV')} 11,5 m, odavaim Triangle IceLynk TI501 aga <strong>25,5 m</strong>. Sama Triangle oli märjal asfaldil hoopis parim — üks rehv võib ühes olus hiilata ja teises olla ohtlik.</p>
<p><strong>Tekniikan Maailma 2025</strong> (205/55 R16, VW Golf): 50 km/h pealt jääl peatus parim naastrehv 32,3 meetriga, halvim lamellrehv 53,5 meetriga. Vahe on <strong>21 meetrit</strong>.</p>

<h2>Lumi: vahed on väikesed</h2>
<p>Tallatud lumel olid parima ja halvima vahed kõigis kolmes Vi Bilägare testis alla meetri (35 km/h pealt 5 km/h-ni). Hea talverehv on lumel hea — aga see ei ütle midagi selle kohta, kuidas ta jääl või märjal asfaldil pidurdab.</p>

<h2>Märg asfalt: sama oluline kui jää</h2>
<p><strong>ADAC 2025</strong> (Kesk-Euroopa talverehvid): märjal asfaldil 80 km/h pealt peatus parim ${R('goodyear-ultragrip-performance-3', 'Goodyear UltraGrip Performance 3')} 31,7 meetriga, halvim ${R('syron-everest-2', 'Syron Everest 2')} 47,1 meetriga — <strong>15 meetrit vahet</strong>. Syron oli samas testis lumel ja jääl parim, jälle üks rehv, mis hiilgab ühes ja kukub läbi teises.</p>
<p>Põhjamaade testides oli märja asfaldi vahe 100 km/h pealt 7–9 meetrit. Eestis on talvel palju märga ja nullilähedast teed, nii et see number loeb.</p>

<h2>Mida sellest järeldada</h2>
<ul>
<li><strong>Vaata jää ja märja tulemust</strong>, mitte ainult lund ega kogupunkte.</li>
<li><strong>Odav naastrehv ei ole automaatselt jääl hea</strong> — halvimad naastrehvid pidurdasid jääl kehvemini kui head lamellrehvid.</li>
<li>Kui sõidad peamiselt linnas ja maanteel, on märja asfaldi tulemus sama tähtis kui jää.</li>
</ul>
<p>Iga testitud rehvi mõõdetud tulemused on rehvi lehel, näiteks ${R('continental-vikingcontact-8', 'Continental VikingContact 8')} või ${R('pirelli-ice-zero-2', 'Pirelli Ice Zero 2')}. Oma auto ja rehviga saad pidurdusmaa arvutada <a href="/">kalkulaatoris</a>.</p>

<h2>Mis on veel tulemas</h2>
<p>2026. aasta sügisel on ilmunud ka <strong>ADAC</strong> (185/65 R15 ja 225/50 R17) ja <strong>Tekniikan Maailma</strong> (205/55 R16) talvetestid. <strong>ADAC 2026, 225/50 R17</strong> (16 rehvi): märjal asfaldil 80 km/h pealt peatusid parimad, Continental WinterContact TS 870 ja Pirelli Cinturato Winter 3, umbes 35 meetriga; nõrgim, Sunwide Snowide, vajas ligi 12 meetrit rohkem. Rehvide kaupa mõõdetud meetreid ADAC avalikult ei näita (ainult hinded) ja Tekniikan Maailma test on tasuline — seepärast neid andmebaasis veel ei ole. Lisame need, kui mõõtmised avalikuks tulevad.</p>
<p class="note">Allikad: Vi Bilägare / Motor (NAF), Tekniikan Maailma, ADAC. Numbrid nii, nagu need on avaldatud; testid on tehtud eri autode, mõõtude ja tingimustega, nii et eri testide meetreid omavahel otse võrrelda ei saa.</p>`;

	const SISU_RU = `<p><strong>Тесты зимних шин каждую осень показывают одну и ту же картину:</strong> на снегу хорошие и средние шины почти равны, но на льду и мокром асфальте разница может составлять несколько длин автомобиля. Мы собрали <em>измеренный</em> тормозной путь из последних тестов — только метры, без баллов и оценок.</p>

<h2>Лёд: самая большая разница</h2>
<p><strong>Vi Bilägare 2026, шипованные шины 215/65 R17</strong> (VW Tiguan): при торможении с 25 до 5 км/ч лучшая ${R('bridgestone-blizzak-spike-3', 'Bridgestone Blizzak Spike 3')} остановилась за <strong>8,3 метра</strong>, худшая ${R('kumho-wintercraft-ice-wi32', 'Kumho WinterCraft Ice Wi32')} — за <strong>17,6 метра</strong>, более чем вдвое длиннее. Правда, Blizzak Spike 3 исключили из рейтинга, потому что шипы выступали больше допустимого.</p>
<p><strong>Vi Bilägare 2025, шипованные шины 235/60 R18</strong> (Volvo XC60): лучшая ${R('nokian-hakkapeliitta-10', 'Nokian Hakkapeliitta 10 SUV')} — 11,5 м, а самая дешёвая Triangle IceLynk TI501 — <strong>25,5 м</strong>. При этом та же Triangle на мокром асфальте оказалась лучшей — одна шина может блистать в одних условиях и быть опасной в других.</p>
<p><strong>Tekniikan Maailma 2025</strong> (205/55 R16, VW Golf): с 50 км/ч на льду лучшая шипованная шина остановилась за 32,3 метра, худшая нешипованная — за 53,5 метра. Разница — <strong>21 метр</strong>.</p>

<h2>Снег: разница небольшая</h2>
<p>На укатанном снегу разница между лучшей и худшей шиной во всех трёх тестах Vi Bilägare была меньше метра (с 35 до 5 км/ч). Хорошая зимняя шина на снегу хороша — но это ничего не говорит о том, как она тормозит на льду или мокром асфальте.</p>

<h2>Мокрый асфальт: так же важен, как лёд</h2>
<p><strong>ADAC 2025</strong> (европейские зимние шины): на мокром асфальте с 80 км/ч лучшая ${R('goodyear-ultragrip-performance-3', 'Goodyear UltraGrip Performance 3')} остановилась за 31,7 метра, худшая ${R('syron-everest-2', 'Syron Everest 2')} — за 47,1 метра, <strong>разница 15 метров</strong>. В том же тесте Syron была лучшей на снегу и льду — снова шина, которая блистает в одном и проваливается в другом.</p>
<p>В северных тестах разница на мокром асфальте с 100 км/ч составила 7–9 метров. В Эстонии зимой много мокрой дороги и дороги около нуля, так что эта цифра важна.</p>

<h2>Какие выводы сделать</h2>
<ul>
<li><strong>Смотрите на результаты на льду и мокром асфальте</strong>, а не только на снег или общий балл.</li>
<li><strong>Дешёвая шипованная шина не обязательно хороша на льду</strong> — худшие шипованные шины тормозили на льду хуже, чем хорошие нешипованные.</li>
<li>Если вы ездите в основном по городу и трассе, результат на мокром асфальте так же важен, как на льду.</li>
</ul>
<p>Измеренные результаты каждой протестированной шины есть на странице шины, например ${R('continental-vikingcontact-8', 'Continental VikingContact 8')} или ${R('pirelli-ice-zero-2', 'Pirelli Ice Zero 2')}. Рассчитать тормозной путь для своего автомобиля и шин можно в <a href="/">калькуляторе</a>.</p>

<h2>Что ещё впереди</h2>
<p>Осенью 2026 года вышли также зимние тесты <strong>ADAC</strong> (185/65 R15 и 225/50 R17) и <strong>Tekniikan Maailma</strong> (205/55 R16). <strong>ADAC 2026, 225/50 R17</strong> (16 шин): на мокром асфальте с 80 км/ч лучшие, Continental WinterContact TS 870 и Pirelli Cinturato Winter 3, остановились примерно за 35 метров; худшей, Sunwide Snowide, понадобилось почти на 12 метров больше. Измеренные метры по отдельным шинам ADAC публично не показывает (только оценки), а тест Tekniikan Maailma платный — поэтому в нашей базе данных их пока нет. Мы добавим их, когда измерения станут публичными.</p>
<p class="note">Источники: Vi Bilägare / Motor (NAF), Tekniikan Maailma, ADAC. Цифры приведены так, как они опубликованы; тесты проводились на разных автомобилях, в разных размерах и условиях, поэтому метры из разных тестов напрямую сравнивать нельзя.</p>`;

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	desc={T.desc}
	path="teadmine/artiklid/talverehvide-testid-2026/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/talverehvide-testid-2026/']]}
	uuendatud={A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/talverehvide-testid-2026.png"
	sisu={ru ? SISU_RU : SISU}
/>
