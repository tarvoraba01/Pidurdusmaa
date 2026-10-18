<script>
	/* Rehvi märgistus: mida tähendavad numbrid ja talvemärgid
	   Artiklite partii 18.10.2026 (mustandid: 2ND Brain, Pidurdusmaa.ee/01 Articles, „(C) 07 Rehvi märgistus küljel - kuidas talverehvi lugeda“).
	   Seadused ja testid: allikad lehe lõpus. Pidurdusmaad: sama mudel mis kalkulaator (engine.js),
	   VW Golf 8, 205/55 R16; numbrid kontrollitud mudeliga 18.10.2026. Lehe tekst on genereeritud
	   mustandist (scratchpad md2page.py), parandused tee siin otse. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'rehvi-kulje-margistus';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const SISU = `<p><strong>Lühike vastus:</strong> rehvi küljel on mõõt (näiteks 205/55 R16), kandevõime indeks ja kiirusindeks (näiteks 91T), tootmisaeg (DOT-kood) ja talvemärgid. Eestis on talvel kõige tähtsam kolme mäetipu ja lumehelbe märk, sest ilma selleta ei tohi lamellrehviga 1. detsembrist 1. märtsini sõita.</p>
<p>Rehvi külg näeb välja nagu koodikeel. Tegelikult on vaja teada vaid mõnda asja. Võtame näiteks rehvi, mille küljel on <strong>205/55 R16 91T</strong>.</p>
<h2>Mida tähendab 205/55 R16?</h2>
<ul><li><strong>205</strong> on rehvi laius millimeetrites.</li><li><strong>55</strong> on külje kõrgus protsentides laiusest. Meie näites on see umbes 113 mm.</li><li><strong>R</strong> tähendab radiaalrehvi. Sõiduautodel on peaaegu kõik rehvid sellised.</li><li><strong>16</strong> on velje läbimõõt tollides.</li></ul>
<p>Talverehvi ostes peab mõõt olema sama, mis on sinu autole lubatud. Selle leiad auto juhendist või juhiukse piilarilt. Kui tahad teist mõõtu, kontrolli enne <a href="/rehvi-kalkulaator/">rehvi kalkulaatoriga</a>, kui palju ratta läbimõõt muutub.</p>
<h2>Mida tähendavad 91 ja T?</h2>
<p><strong>91 on kandevõime indeks.</strong> See näitab, kui palju üks rehv kannab. Mõned näited Hankooki tabelist:</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th>Indeks</th><th class="n">Kandevõime ühe rehvi kohta</th></tr></thead><tbody><tr><td><strong>88</strong></td><td class="n">560 kg</td></tr><tr><td><strong>91</strong></td><td class="n">615 kg</td></tr><tr><td><strong>94</strong></td><td class="n">670 kg</td></tr></tbody></table></div>
<p><strong>T on kiirusindeks</strong>, ehk suurim kiirus, mida rehv täiskoormusel ja õige rõhuga talub.</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th>Täht</th><th class="n">Suurim kiirus</th></tr></thead><tbody><tr><td><strong>Q</strong></td><td class="n">160 km/h</td></tr><tr><td><strong>R</strong></td><td class="n">170 km/h</td></tr><tr><td><strong>S</strong></td><td class="n">180 km/h</td></tr><tr><td><strong>T</strong></td><td class="n">190 km/h</td></tr><tr><td><strong>H</strong></td><td class="n">210 km/h</td></tr><tr><td><strong>V</strong></td><td class="n">240 km/h</td></tr></tbody></table></div>
<p>Michelin märgib, et talverehvi kiirusindeks võib olla madalam kui auto originaalsel suverehvil. See on talverehvide puhul tavaline. Kandevõime indeks ei tohi aga olla väiksem kui autole ette nähtud.</p>
<p><strong>XL</strong> tähendab tugevdatud rehvi (Extra Load). Selle kandevõime on samas mõõdus tavalisest suurem.</p>
<h2>Mis vahe on M+S tähisel ja lumehelbe märgil?</h2>
<p><strong>M+S</strong> on tootja enda tähis ja sellest Eestis talveperioodil lamellrehvil ei piisa. <strong>Kolme mäetipu ja lumehelbe märk</strong> (3PMSF) tähendab läbitud lumetesti ja on Transpordiameti järgi talveperioodil lamellrehvil kohustuslik. <strong>Jäämärk</strong> tähendab läbitud jäätesti ning Transpordiamet soovitab valida rehvi, millel on mõlemad märgid.</p>
<p>Need kolm märki on pikemalt lahti kirjutatud artiklis <a href="/teadmine/artiklid/talverehvi-margistus-3pmsf/">3PMSF, M+S ja jäämärk</a>. EL-i märgise klassid leiad lehelt <a href="/teadmine/rehvimargis/">EL-i rehvimärgis</a>.</p>
<h2>Kuidas lugeda DOT-koodi?</h2>
<p>DOT-koodi lõpus on neljakohaline number. Kaks esimest numbrit on tootmisnädal, kaks viimast aasta. <strong>4523</strong> tähendab 2023. aasta 45. nädalat. Kood on sageli ainult ühel küljel, nii et vaata vajadusel ka sisekülge. Vanuse saad kiiresti teada <a href="/rehvi-vanus/">rehvi vanuse kalkulaatoriga</a>.</p>
<h2>Mida tähendavad muud märgid?</h2>
<ul><li><strong>TWI</strong> näitab, kus on kulumisindikaatorid. Need on 1,6 mm kõrgused kühmud mustri soontes, suverehvi miinimum. Talverehvil on seaduse piir 3 mm, nii et indikaatorini ei tohi talvel jõuda.</li><li><strong>MAX PRESS</strong> on rehvi suurim lubatud rõhk, mitte sinu auto õige rõhk. Õige rõhk on kirjas juhiukse piilaril või kütusepaagi luugil.</li><li><strong>Nool ja ROTATION</strong> tähendavad suunamustriga rehvi. Nool peab näitama sõidu suunda.</li><li><strong>OUTSIDE ja INSIDE</strong> tähendavad asümmeetrilist rehvi. OUTSIDE peab jääma väljapoole.</li></ul>
<h2>Kiire kontroll talverehvil</h2>
<ol><li>Mõõt vastab autole</li><li>Kandevõime indeks ei ole väiksem kui autole ette nähtud</li><li>Lumehelbe märk on olemas (lamellrehvil kohustuslik)</li><li>Jäämärk, kui sõidad tihti jääl</li><li>Rehv ei ole liiga vana (vaata DOT-koodi)</li></ol>
<h2>Proovi oma autoga</h2>
<p>Kui tead nüüd oma rehvi mõõtu, vaata, mida see teel tähendab. <a href="/autod/">Kirjuta oma auto mark</a> või ava <a href="/talverehvid/">talverehvid sinu mõõdus</a> ja võrdle, kui pika maa pealt eri rehvid peatuvad ja mis need maksavad.</p>
<p class="note">Allikad: <a href="https://na.nokiantyres.com/customer-service/tire-maintenance-and-change/tire-regulations/what-do-different-numbers-and-letters-mean-on-the-sidewall-of-the-tire-for-example-tire-size-205-55-r-16-94-t-xl/" rel="noopener">Nokian Tyres</a>, <a href="https://na.nokiantyres.com/tips/tire-care-and-maintenance/sidewall-markings/" rel="noopener">Nokian Tyres</a>, <a href="https://africa.michelin.com/en/auto/advice/tyre-basics/tyre-markings-explained" rel="noopener">Michelin</a>, <a href="https://www.hankooktire.com/au/en/help-support/tire-guide/load-speed.html" rel="noopener">Hankook</a>, <a href="https://www.goodyear.eu/en_gb/consumer/learn/eu-tire-label-explained.html" rel="noopener">Goodyear</a>, <a href="https://www.err.ee/938636/minister-taavi-aas-kinnitas-auto-talverehvide-kasutamise-uued-nouded" rel="noopener">ERR</a>, <a href="https://www.transpordiamet.ee/uudised/homsest-lubatud-kasutada-naastrehve" rel="noopener">Transpordiamet</a>, <a href="https://treadmagazine.co.uk/?p=2110" rel="noopener">Tread</a>, <a href="https://www.rettum.ee/talverehvid/" rel="noopener">Rettum</a>.</p>`;

	const SISU_RU = `<p><strong>Коротко:</strong> на боковине шины указаны размер (например, 205/55 R16), индексы нагрузки и скорости (например, 91T), дата выпуска (код DOT) и зимние знаки. Зимой в Эстонии важнее всего знак трёх горных вершин со снежинкой: без него на липучке с 1 декабря по 1 марта ездить нельзя.</p>
<p>Боковина шины выглядит как шифр. На деле нужно знать всего несколько вещей. Разберём пример: <strong>205/55 R16 91T</strong>.</p>
<h2>Что означает 205/55 R16?</h2>
<ul><li><strong>205</strong>: ширина шины в миллиметрах.</li><li><strong>55</strong>: высота профиля в процентах от ширины. Здесь 55% от 205 мм, то есть около 113 мм.</li><li><strong>R</strong>: радиальная шина. На легковых машинах почти все шины такие.</li><li><strong>16</strong>: посадочный диаметр диска в дюймах.</li></ul>
<p>Размер зимней резины должен совпадать с допустимым для вашей машины. Его можно найти в инструкции или на стойке водительской двери. Если хотите другой размер, сначала проверьте в <a href="/ru/rehvi-kalkulaator/">шинном калькуляторе</a>, насколько изменится диаметр колеса.</p>
<h2>Что означают 91 и T?</h2>
<p><strong>Индекс нагрузки здесь 91.</strong> Он показывает, какой вес выдерживает одна шина. Несколько значений из таблицы Hankook:</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th>Индекс</th><th class="n">Нагрузка на одну шину</th></tr></thead><tbody><tr><td><strong>88</strong></td><td class="n">560 кг</td></tr><tr><td><strong>91</strong></td><td class="n">615 кг</td></tr><tr><td><strong>94</strong></td><td class="n">670 кг</td></tr></tbody></table></div>
<p><strong>Индекс скорости здесь T</strong>, то есть максимальная скорость при полной нагрузке и правильном давлении.</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th>Буква</th><th class="n">Макс. скорость</th></tr></thead><tbody><tr><td><strong>Q</strong></td><td class="n">160 км/ч</td></tr><tr><td><strong>R</strong></td><td class="n">170 км/ч</td></tr><tr><td><strong>S</strong></td><td class="n">180 км/ч</td></tr><tr><td><strong>T</strong></td><td class="n">190 км/ч</td></tr><tr><td><strong>H</strong></td><td class="n">210 км/ч</td></tr><tr><td><strong>V</strong></td><td class="n">240 км/ч</td></tr></tbody></table></div>
<p>Michelin отмечает, что у зимней шины индекс скорости может быть ниже, чем у штатной летней. Для зимней резины это обычное дело. А вот индекс нагрузки не должен быть ниже положенного для машины.</p>
<p><strong>XL</strong> означает усиленную шину (Extra Load). Её грузоподъёмность выше обычной для этого размера.</p>
<h2>Чем M+S отличается от снежинки?</h2>
<p><strong>M+S</strong> производитель ставит сам, и для липучки в зимний период в Эстонии этого недостаточно. <strong>Знак трёх гор со снежинкой</strong> (3PMSF) означает пройденный тест на снегу, и, по данным Transpordiamet, в зимний период на липучке он обязателен. <strong>Знак льда</strong> означает пройденный тест на льду, и Transpordiamet советует выбирать шины с обоими знаками.</p>
<p>Подробно эти три знака разобраны в статье <a href="/ru/teadmine/artiklid/talverehvi-margistus-3pmsf/">3PMSF, M+S и знак льда</a>. Классы этикетки ЕС описаны на странице <a href="/ru/teadmine/rehvimargis/">маркировка шин ЕС</a>.</p>
<h2>Как читать код DOT?</h2>
<p>В конце кода DOT стоит четырёхзначное число. Первые две цифры означают неделю выпуска, а последние две год. <strong>4523</strong> означает: 45-я неделя 2023 года. Код часто есть только с одной стороны, так что при необходимости посмотрите и внутреннюю боковину. Возраст быстро посчитает <a href="/ru/rehvi-vanus/">калькулятор возраста шин</a>.</p>
<h2>Что означают другие обозначения?</h2>
<ul><li><strong>TWI</strong> показывает, где находятся индикаторы износа. Это выступы высотой 1,6 мм в канавках протектора, предел для летней шины. У зимней шины по закону должно оставаться не меньше 3 мм, так что зимой до индикатора доходить нельзя.</li><li><strong>MAX PRESS</strong> означает максимально допустимое давление в шине, а не правильное давление для вашей машины. Нужное давление указано на стойке водительской двери или на лючке бензобака.</li><li><strong>Стрелка и ROTATION</strong> значат направленный рисунок. Стрелка должна смотреть по ходу движения.</li><li><strong>OUTSIDE и INSIDE</strong> значат асимметричную шину. Надпись OUTSIDE должна быть снаружи.</li></ul>
<h2>Быстрая проверка зимней шины</h2>
<ol><li>Размер подходит машине</li><li>Индекс нагрузки не ниже положенного</li><li>Есть знак снежинки (для липучки обязателен)</li><li>Знак льда, если часто ездите по льду</li><li>Шина не слишком старая (смотрите код DOT)</li></ol>
<h2>Проверьте на своей машине</h2>
<p>Теперь, когда вы знаете свой размер, посмотрите, что он значит на дороге. <a href="/ru/autod/">Введите марку своей машины</a> или откройте <a href="/ru/talverehvid/">зимние шины по размеру</a> и сравните тормозной путь и цены разных моделей.</p>
<p class="note">Источники: <a href="https://na.nokiantyres.com/customer-service/tire-maintenance-and-change/tire-regulations/what-do-different-numbers-and-letters-mean-on-the-sidewall-of-the-tire-for-example-tire-size-205-55-r-16-94-t-xl/" rel="noopener">Nokian Tyres</a>, <a href="https://na.nokiantyres.com/tips/tire-care-and-maintenance/sidewall-markings/" rel="noopener">Nokian Tyres</a>, <a href="https://africa.michelin.com/en/auto/advice/tyre-basics/tyre-markings-explained" rel="noopener">Michelin</a>, <a href="https://www.hankooktire.com/au/en/help-support/tire-guide/load-speed.html" rel="noopener">Hankook</a>, <a href="https://www.goodyear.eu/en_gb/consumer/learn/eu-tire-label-explained.html" rel="noopener">Goodyear</a>, <a href="https://www.err.ee/938636/minister-taavi-aas-kinnitas-auto-talverehvide-kasutamise-uued-nouded" rel="noopener">ERR</a>, <a href="https://www.transpordiamet.ee/uudised/homsest-lubatud-kasutada-naastrehve" rel="noopener">Transpordiamet</a>, <a href="https://treadmagazine.co.uk/?p=2110" rel="noopener">Tread</a>, <a href="https://www.rettum.ee/talverehvid/" rel="noopener">Rettum</a>.</p>`;

	const KKK = [
		[
		 "Kas M+S rehv on talverehv?",
		 "Naastudeta rehvina Eestis talveperioodil mitte, kui sel pole lisaks kolme mäetipu ja lumehelbe märki. M+S on tootja enda tähis, millele ei ole sama lumetesti nõuet."
		],
		[
		 "Mida tähendab lumehelbe märk rehvil?",
		 "Et rehv on läbinud pidurdustesti tihendatud lumel ÜRO eeskirja nr 117 järgi. Lamellrehvil on see Eestis talveperioodil kohustuslik."
		],
		[
		 "Kas talverehvi kiirusindeks võib olla madalam kui suverehvil?",
		 "Michelini järgi võib talverehvi kiirusindeks olla madalam. Kandevõime indeks peab aga vastama autole."
		],
		[
		 "Kus on rehvi tootmisaasta?",
		 "DOT-koodi neljas viimases numbris. Kaks esimest on nädal, kaks viimast aasta."
		]
];
	const KKK_RU = [
		[
		 "Считается ли шина M+S зимней?",
		 "Как липучка в Эстонии в зимний период нет, если на ней нет ещё и знака трёх гор со снежинкой. M+S производитель ставит сам, без такого же обязательного теста на снегу."
		],
		[
		 "Что означает снежинка на шине?",
		 "Что шина прошла тест торможения на укатанном снегу по правилам ООН № 117. На липучке в Эстонии в зимний период этот знак обязателен."
		],
		[
		 "Может ли индекс скорости зимней шины быть ниже, чем у летней?",
		 "По данным Michelin, может. А индекс нагрузки должен соответствовать машине."
		],
		[
		 "Где на шине год выпуска?",
		 "В последних четырёх цифрах кода DOT. Первые две означают неделю, а последние две год."
		]
];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	h1={T.h1}
	desc={T.desc}
	path="teadmine/artiklid/rehvi-kulje-margistus/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/rehvi-kulje-margistus/']]}
	lapsed={[]}
	uuendatud={A.uuendatud || A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/rehvi-kulje-margistus.png"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
