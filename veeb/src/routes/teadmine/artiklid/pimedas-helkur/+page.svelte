<script>
	/* Pidurdusmaa pimedas — nähtavuskaugused: Transpordiamet (2025), „Mida pead
	   helkuri kohta teadma“ (sama mis /liiklusohutus/pimedas/: tume riietus
	   30 m, hele 40–50 m, helkur 130–150 m, kaugtuled + helkur 300–350 m).
	   Pidurdus sama mudeliga mis kalkulaator (engine.js): VW Golf 8, 205/55 R16,
	   keskmine rehv (klass C), märg asfalt 1 mm vett +10 °C; lumi −5 °C
	   Põhjamaade talverehviga. Reaktsiooniaeg 1,0 s ja 1,5 s. "Kiirus kohas":
	   stoppingDistance().trace. Suurim kiirus: 1 km/h sammuga. Numbrid 2026-10-07. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'pimedas-helkur';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Pimedas ei sõltu peatumine ainult rehvidest ja pidurdusmaast, vaid sellest, kui kaugelt juht jalakäijat üldse näeb. Lähitulede valgel on see tumedas riietuses inimese puhul nii lühike vahemaa, et linnakiirusest suuremalt ei jõua auto peatuda. Helkur muudab selle vahemaa mitu korda pikemaks.</p>
<div class="note-box"><strong>Lühidalt.</strong> Lähitulede valgel märkab juht tumedas riietuses helkurita jalakäijat umbes 30 m kauguselt, helkuriga 130–150 m kauguselt (Transpordiamet). Märjal teel jõuab auto 30 m peale peatuda kuni umbes 53 km/h kiiruselt, kui juht reageerib 1 sekundiga. 70 km/h pealt jõuab auto jalakäijani veel 57 km/h kiirusega. Helkuriga jõuab auto peatuda ka 120–130 km/h pealt.</div>

<h2>Kui kaugelt jalakäijat näeb</h2>
<p>Transpordiameti andmetel märkab juht jalakäijat pimedas lähitulede valgel:</p>
${tabel(
		['Jalakäija', 'Märkamise kaugus'],
		[
			['Tume riietus, helkurita', 'kuni 30 m'],
			['Hele riietus, helkurita', '40–50 m'],
			['Helkuriga', '130–150 m'],
			['Helkuriga, auto kaugtuledega', '300–350 m']
		]
	)}

<h2>Mis kiiruselt jõuab peatuda</h2>
<p>Suurim kiirus, millelt auto jõuab peatuda enne jalakäijat, kui juht märkab teda alles tabelis toodud kauguselt. Märg asfalt, keskmine suverehv, VW Golf 8:</p>
${tabel(
		['Märkamise kaugus', 'Reaktsioon 1 s', 'Reaktsioon 1,5 s'],
		[
			['30 m (tume riietus)', '53 km/h', '45 km/h'],
			['45 m (hele riietus)', '69 km/h', '60 km/h'],
			['140 m (helkur)', '132 km/h', '123 km/h']
		]
	)}
<p>Pimedas tuleb oht sageli ootamatult, siis on reaktsiooniaeg pigem 1,5 sekundit. Tumedas riietuses jalakäija ees jõuab auto siis märjal teel peatuda ainult kuni 45 km/h kiiruselt. Lumel Põhjamaade talverehviga on piir veel madalam: 30 m peale jõuab peatuda kuni 41 km/h pealt (reaktsioon 1 s).</p>

<h2>Mis kiirusega auto jalakäijani jõuab</h2>
<p>Kui auto ei jõua peatuda, loeb kiirus, millega see jalakäijani jõuab. Jalakäija märgatakse 30 m kauguselt (tume riietus), märg asfalt:</p>
${tabel(
		['Auto kiirus', 'Reaktsioon 1 s', 'Reaktsioon 1,5 s'],
		[
			['50 km/h', 'peatub', '30 km/h'],
			['70 km/h', '57 km/h', '70 km/h'],
			['90 km/h', '87 km/h', '90 km/h']
		]
	)}
<p>70 km/h pealt läbib auto 1,5 sekundiga 29 meetrit. Kui jalakäija paistab alles 30 m kauguselt, jõuab juht enne kokkupõrget vaevalt pidurit vajutada. Helkuriga jalakäija märgatakse 140 m kauguselt ja kõigil neil kiirustel jõuab auto peatuda.</p>

<h2>Mida see tähendab</h2>
<ul><li><strong>Jalakäijale:</strong> kanna helkurit pimedal ajal alati, ka linnas. Eesti liiklusseaduse järgi peab jalakäija pimedal ajal teel liikudes kandma helkurit või kasutama valgustit. Helkur peaks rippuma põlve kõrgusel, et auto lähituled seda valgustaksid.</li><li><strong>Juhile:</strong> lähitulede valgel paistab tumedas riietuses jalakäija lähemalt, kui on märjal teel peatumisteekond juba 60 km/h pealt (36 m). Kasuta kaugtulesid, kui see on lubatud, ja vähenda kiirust, kui nähtavus on halb.</li><li><strong>Märg tee ja lumi</strong> pikendavad peatumisteekonda, nähtavus ei pikene. Sügisel ja talvel on vahe kõige suurem.</li></ul>

<h2>Proovi ise</h2>
<ul><li><a href="/liiklusohutus/pimedas/">Nähtavus pimedas</a>: vali riietus, tuled ja kiirus ning vaata, kas auto jõuab peatuda</li><li><a href="/liiklusohutus/reaktsioon/">Reaktsioonimäng</a>: jalakäija pimedal teel, kas jõuad pidurdada?</li><li><a href="/teadmine/artiklid/linnas-50-kmh/">Linnas 50 km/h: kui palju on vahet 40 ja 60 km/h vahel?</a></li></ul>
<p class="note">Märkamise kaugused: Transpordiamet (2025), „Mida pead helkuri kohta teadma“. Pidurdus on arvutatud mudeliga ja on hinnang, mitte mõõtmine: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>В темноте остановка зависит не только от шин и тормозного пути, но и от того, с какого расстояния водитель вообще видит пешехода. При ближнем свете это расстояние для человека в тёмной одежде настолько короткое, что с большей, чем городская, скорости машина не успевает остановиться. Световозвращатель увеличивает это расстояние в несколько раз.</p>
<div class="note-box"><strong>Коротко.</strong> При ближнем свете водитель замечает пешехода в тёмной одежде без световозвращателя примерно с 30 м, со световозвращателем — со 130–150 м (Департамент транспорта). На мокрой дороге машина успевает остановиться на 30 м примерно с 53 км/ч, если водитель реагирует за 1 секунду. С 70 км/ч машина доезжает до пешехода ещё со скоростью 57 км/ч. Со световозвращателем машина успевает остановиться даже со 120–130 км/ч.</div>

<h2>С какого расстояния видно пешехода</h2>
<p>По данным Департамента транспорта, при ближнем свете водитель замечает пешехода в темноте:</p>
${tabel(
		['Пешеход', 'Расстояние, с которого видно'],
		[
			['Тёмная одежда, без световозвращателя', 'до 30 м'],
			['Светлая одежда, без световозвращателя', '40–50 м'],
			['Со световозвращателем', '130–150 м'],
			['Со световозвращателем, у машины дальний свет', '300–350 м']
		]
	)}

<h2>С какой скорости можно успеть остановиться</h2>
<p>Наибольшая скорость, с которой машина успевает остановиться перед пешеходом, если водитель замечает его только с расстояния из таблицы. Мокрый асфальт, средняя летняя шина, VW Golf 8:</p>
${tabel(
		['Расстояние, с которого видно', 'Реакция 1 с', 'Реакция 1,5 с'],
		[
			['30 м (тёмная одежда)', '53 км/ч', '45 км/ч'],
			['45 м (светлая одежда)', '69 км/ч', '60 км/ч'],
			['140 м (световозвращатель)', '132 км/ч', '123 км/ч']
		]
	)}
<p>В темноте опасность часто возникает неожиданно, тогда время реакции скорее 1,5 секунды. Перед пешеходом в тёмной одежде машина на мокрой дороге успевает остановиться только со скорости до 45 км/ч. На снегу с нешипованной зимней шиной северного типа предел ещё ниже: на 30 м можно остановиться со скорости до 41 км/ч (реакция 1 с).</p>

<h2>С какой скоростью машина доезжает до пешехода</h2>
<p>Если машина не успевает остановиться, важна скорость, с которой она доезжает до пешехода. Пешехода замечают с 30 м (тёмная одежда), мокрый асфальт:</p>
${tabel(
		['Скорость машины', 'Реакция 1 с', 'Реакция 1,5 с'],
		[
			['50 км/ч', 'останавливается', '30 км/ч'],
			['70 км/ч', '57 км/ч', '70 км/ч'],
			['90 км/ч', '87 км/ч', '90 км/ч']
		]
	)}
<p>С 70 км/ч машина за 1,5 секунды проезжает 29 метров. Если пешеход виден только с 30 м, водитель едва успевает нажать на тормоз до столкновения. Пешехода со световозвращателем замечают со 140 м, и на всех этих скоростях машина успевает остановиться.</p>

<h2>Что это значит</h2>
<ul><li><strong>Пешеходу:</strong> в тёмное время всегда носите световозвращатель, в том числе в городе. По эстонскому закону о дорожном движении пешеход в тёмное время на дороге должен носить световозвращатель или пользоваться фонарём. Световозвращатель лучше вешать на уровне колена, чтобы его освещал ближний свет фар.</li><li><strong>Водителю:</strong> при ближнем свете пешеход в тёмной одежде виден ближе, чем остановочный путь на мокрой дороге уже с 60 км/ч (36 м). Пользуйтесь дальним светом, когда это разрешено, и снижайте скорость при плохой видимости.</li><li><strong>Мокрая дорога и снег</strong> удлиняют остановочный путь, а видимость не увеличивается. Осенью и зимой разница больше всего.</li></ul>

<h2>Проверьте сами</h2>
<ul><li><a href="/ru/liiklusohutus/pimedas/">Видимость в темноте</a>: выберите одежду, свет фар и скорость и посмотрите, успеет ли машина остановиться</li><li><a href="/ru/liiklusohutus/reaktsioon/">Игра на реакцию</a>: пешеход на тёмной дороге — успеете затормозить?</li><li><a href="/ru/teadmine/artiklid/linnas-50-kmh/">50 км/ч в городе: какая разница между 40 и 60 км/ч?</a></li></ul>
<p class="note">Расстояния видимости: Департамент транспорта Эстонии (2025), «Что нужно знать о световозвращателе». Торможение рассчитано моделью и является оценкой, а не измерением: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a> (на эстонском).</p>`;

	const KKK = [
		['Kui kaugelt näeb juht pimedas jalakäijat?', 'Transpordiameti andmetel lähitulede valgel tumedas riietuses helkurita jalakäijat kuni 30 m, heledas riietuses 40–50 m ja helkuriga 130–150 m kauguselt. Kaugtulede valgel helkuriga 300–350 m kauguselt.'],
		['Mis kiiruselt jõuab auto peatuda, kui jalakäija paistab alles 30 m kauguselt?', 'Märjal asfaldil keskmise suverehviga kuni umbes 53 km/h pealt, kui juht reageerib 1 sekundiga. Kui reaktsioon võtab 1,5 sekundit, kuni umbes 45 km/h pealt.'],
		['Kui palju aitab helkur?', 'Helkuriga märkab juht jalakäijat 130–150 m kauguselt. Märjal teel jõuab auto 140 m peale peatuda kuni umbes 132 km/h pealt (reaktsioon 1 s), tumedas riietuses helkurita jalakäija ees ainult kuni 53 km/h pealt.'],
		['Kuhu helkur kinnitada?', 'Põlve kõrgusele, nii et see ripub vabalt ja liigub. Siis valgustavad seda auto lähituled ja juht märkab seda varem.']
	];
	const KKK_RU = [
		['С какого расстояния водитель видит пешехода в темноте?', 'По данным Департамента транспорта, при ближнем свете пешехода в тёмной одежде без световозвращателя — до 30 м, в светлой одежде — с 40–50 м, со световозвращателем — со 130–150 м. При дальнем свете со световозвращателем — с 300–350 м.'],
		['С какой скорости машина успевает остановиться, если пешеход виден только с 30 м?', 'На мокром асфальте со средней летней шиной — примерно с 53 км/ч, если водитель реагирует за 1 секунду. Если реакция занимает 1,5 секунды — примерно с 45 км/ч.'],
		['Насколько помогает световозвращатель?', 'Со световозвращателем водитель замечает пешехода со 130–150 м. На мокрой дороге машина успевает остановиться на 140 м со скорости примерно до 132 км/ч (реакция 1 с), а перед пешеходом в тёмной одежде без световозвращателя — только до 53 км/ч.'],
		['Куда крепить световозвращатель?', 'На уровне колена, чтобы он свободно висел и двигался. Тогда его освещает ближний свет фар, и водитель замечает его раньше.']
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
