<script>
	/* Talverehvide testid hooajal 2025/26 ja 2026 sügisel — ainult avaldatud
	   absoluutsed pidurdusmaad (meie testide andmebaas):
	     Vi Bilägare 2025 lamell ja naast 235/60 R18 (Volvo XC60), 2026 naast 215/65 R17
	     (mudel/testid_ext/vi_bilagare_2025_2026.json, allikas motor.no / tyrereviews.com);
	     Tekniikan Maailma 2025 205/55 R16 ja ADAC 2025 (core.json TM25 / ADAC25);
	     ADAC 2026 185/65 R15 ja 225/50 R17, Auto Bild 2026 225/55 R18 (testid_ext, adac.de / autobild.de).
	   Uusi teste lisame, kui nende mõõdetud meetrid on avalikud.
	   Vene tekst: SISU_RU (/ru/teadmine/artiklid/talverehvide-testid-2026/). */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	let { data } = $props();
	const keel = useLang();
	const t = useT();
	const A = ARTIKLID.find((a) => a.slug === 'talverehvide-testid-2026');
	const ru = keel.lang === 'ru';
	const R = (s, n) => `<a href="/rehvid/${s}/">${n}</a>`;

	/* Testide parimad alade kaupa (+page.server.js → talveTestideParimad): iga testi enda
	   1. koht jääl, lumel ja märjal asfaldil. Uus avalik test tuleb tabelisse ise. */
	const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
	const nr = (m) => (Math.round(m * 10) / 10).toFixed(1).replace('.', ',');
	const ALAD = ['jää', 'lumi', 'märg asfalt'];
	const PIND = ru ? { jää: 'Лёд', lumi: 'Снег', 'märg asfalt': 'Мокрый асфальт' } : { jää: 'Jää', lumi: 'Lumi', 'märg asfalt': 'Märg asfalt' };
	const KAT = ru
		? { naast: 'шипованные', lamell: 'северные нешипованные', kesk: 'европейские зимние', 'naast+lamell': 'шипованные и нешипованные', segu: 'разные зимние' }
		: { naast: 'naastrehvid', lamell: 'Põhjamaade lamellrehvid', kesk: 'Kesk-Euroopa talverehvid', 'naast+lamell': 'naast- ja lamellrehvid', segu: 'eri tüüpi talverehvid' };
	const lahter = (o) =>
		!o
			? '—'
			: o.rehvid.map((r) => (r.ix ? `<a href="/rehvid/${r.slug}/">${esc(r.nimi)}</a>` : esc(r.nimi))).join(' / ') +
				`<br><b>${nr(o.m)} m</b> <small style="white-space:nowrap">${o.v0}→${o.v1} km/h</small>`;
	const tabel = (rows) =>
		`<div class="tbl-wrap"><table class="t"><thead><tr><th>${ru ? 'Тест' : 'Test'}</th>${ALAD.map((a) => `<th>${PIND[a]}</th>`).join('')}</tr></thead><tbody>` +
		rows
			.map(
				(x) =>
					`<tr><td><strong>${esc(x.pub)} ${x.aasta}</strong><br><small>${[KAT[x.kat], x.moot, x.auto, x.n ? x.n + (ru ? ' шин' : ' rehvi') : ''].filter(Boolean).map(esc).join(' · ')}</small></td>` +
					ALAD.map((a) => `<td>${lahter(x.alad[a])}</td>`).join('') +
					'</tr>'
			)
			.join('') +
		'</tbody></table></div>';
	const testid = data.testid || [];
	const aastad = [...new Set(testid.map((x) => x.aasta))];
	const TABELID = aastad
		.map((y, i) => {
			const rows = testid.filter((x) => x.aasta === y);
			const h = ru
				? i === 0
					? `Лучшие в зимних тестах ${y} года`
					: `Тесты ${y} года (зима ${y}/${String(y + 1).slice(2)})`
				: i === 0
					? `${y}. aasta talvetestide parimad`
					: `${y}. aasta testid (talv ${y}/${String(y + 1).slice(2)})`;
			const selg =
				i > 0
					? ''
					: ru
						? '<p>Лучшая шина каждого теста на льду, снегу и мокром асфальте: тормозной путь, измеренный самим тестом. Прочерк: такой дисциплины в тесте не было или победителя нет в нашей базе. Метры из разных тестов напрямую сравнивать нельзя: разные автомобили и скорости.</p>'
						: '<p>Iga testi parim rehv jääl, lumel ja märjal asfaldil: testi enda mõõdetud pidurdusmaa. Kriips: seda ala testis polnud või võitjat pole meie andmebaasis. Eri testide meetreid otse võrrelda ei saa: autod ja kiirused on erinevad.</p>';
			return `<h2>${h}</h2>${selg}${tabel(rows)}`;
		})
		.join('');

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

<h2>2026. aasta sügise testid: ADAC ja Auto Bild</h2>
<p><strong>ADAC 2026, 185/65 R15</strong> (Škoda Fabia, 16 rehvi): märjal asfaldil 80 km/h pealt peatus parim ${R('bridgestone-blizzak-lm005', 'Bridgestone Blizzak LM005')} <strong>33,5 meetriga</strong>, halvim Rockblade Rock 868S <strong>51,4 meetriga</strong> — ligi 18 meetrit vahet. Sama Rockblade oli aga jääl (20 km/h pealt) parim, 19,4 m. Lumel 30 km/h pealt olid kõik 10,0 ja 11,0 meetri vahel.</p>
<p><strong>ADAC 2026, 225/50 R17</strong> (Audi A4 Avant, 16 rehvi): märjal parim ${R('continental-wintercontact-ts-870', 'Continental WinterContact TS 870')} <strong>34,7 m</strong>, halvim Sunwide Snowide <strong>46,3 m</strong>. Sunwide oli samas testis lumel ja jääl parim — jälle sama muster: lumel ja jääl hea odav rehv võib märjal asfaldil olla ohtlik.</p>
<p><strong>Auto Bild 2026, 225/55 R18</strong> (BMW X1, 10 rehvi): märjal 100 km/h pealt parim ${R('pirelli-cinturato-winter-3', 'Pirelli Cinturato Winter 3')} <strong>44,4 m</strong>, halvim ${R('zeetex-wh1000-suv', 'Zeetex WH1000 SUV')} <strong>57,5 m</strong>. Lumel 50 km/h pealt parim ${R('michelin-pilot-alpin-5', 'Michelin Pilot Alpin 5')} 27,7 m, halvim taas Zeetex 31,8 m.</p>
<p>Need on Kesk-Euroopa talverehvid (jääle mõeldud Põhjamaade rehve ADAC ja Auto Bild ei testi). <strong>Tekniikan Maailma 2026</strong> (205/55 R16) test on tasuline — lisame selle, kui mõõdetud meetrid on avalikud.</p>
<p class="note">Allikad: Vi Bilägare / Motor (NAF), Tekniikan Maailma, ADAC, Auto Bild. Numbrid nii, nagu need on avaldatud; testid on tehtud eri autode, mõõtude ja tingimustega, nii et eri testide meetreid omavahel otse võrrelda ei saa.</p>`;

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

<h2>Тесты осени 2026 года: ADAC и Auto Bild</h2>
<p><strong>ADAC 2026, 185/65 R15</strong> (Škoda Fabia, 16 шин): на мокром асфальте с 80 км/ч лучшая ${R('bridgestone-blizzak-lm005', 'Bridgestone Blizzak LM005')} остановилась за <strong>33,5 метра</strong>, худшая Rockblade Rock 868S — за <strong>51,4 метра</strong>, разница почти 18 метров. При этом та же Rockblade оказалась лучшей на льду (с 20 км/ч) — 19,4 м. На снегу с 30 км/ч все шины уложились в 10,0–11,0 метра.</p>
<p><strong>ADAC 2026, 225/50 R17</strong> (Audi A4 Avant, 16 шин): на мокром лучшая ${R('continental-wintercontact-ts-870', 'Continental WinterContact TS 870')} — <strong>34,7 м</strong>, худшая Sunwide Snowide — <strong>46,3 м</strong>. В том же тесте Sunwide была лучшей на снегу и льду — снова та же картина: дешёвая шина, хорошая на снегу и льду, может быть опасной на мокром асфальте.</p>
<p><strong>Auto Bild 2026, 225/55 R18</strong> (BMW X1, 10 шин): на мокром с 100 км/ч лучшая ${R('pirelli-cinturato-winter-3', 'Pirelli Cinturato Winter 3')} — <strong>44,4 м</strong>, худшая ${R('zeetex-wh1000-suv', 'Zeetex WH1000 SUV')} — <strong>57,5 м</strong>. На снегу с 50 км/ч лучшая ${R('michelin-pilot-alpin-5', 'Michelin Pilot Alpin 5')} — 27,7 м, худшая снова Zeetex — 31,8 м.</p>
<p>Это европейские зимние шины (северные шины для льда ADAC и Auto Bild не тестируют). Тест <strong>Tekniikan Maailma 2026</strong> (205/55 R16) платный — добавим его, когда измеренные метры станут публичными.</p>
<p class="note">Источники: Vi Bilägare / Motor (NAF), Tekniikan Maailma, ADAC, Auto Bild. Цифры приведены так, как они опубликованы; тесты проводились на разных автомобилях, в разных размерах и условиях, поэтому метры из разных тестов напрямую сравнивать нельзя.</p>`;

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	desc={T.desc}
	path="teadmine/artiklid/talverehvide-testid-2026/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/talverehvide-testid-2026/']]}
	uuendatud={A.uuendatud || A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/talverehvide-testid-2026.png"
	sisu={(ru ? SISU_RU : SISU).replace('</p>', '</p>' + TABELID)}
/>
