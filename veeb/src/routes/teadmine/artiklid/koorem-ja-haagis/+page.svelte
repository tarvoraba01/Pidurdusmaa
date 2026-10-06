<script>
	/* Pidurdusmaa koormaga ja haagisega — numbrid sama mudeliga mis kalkulaator
	   (engine.js): VW Golf 8 1.5 TSI (1320 kg, 205/55 R16) ja Toyota RAV4 V
	   Hybrid (1660 kg, 225/60 R18), keskmine suverehv (märghaardeklass C), uus
	   muster, 80 km/h, ilma reaktsiooniajata. Märg asfalt 1 mm vett +10 °C,
	   kuiv +15 °C. Koorem = payloadKg (juht 75 kg + lisa). Haagis = trailerKg;
	   inertspidur = trailerBrakes (mudelis haagise pidur kuni 0,5 g, haagise
	   rehvide haare 0,85 auto omast). Numbrid 2026-10-07. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'koorem-ja-haagis';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Kui autos on terve pere koos pagasiga või taga on haagis, peab sama pidurisüsteem peatama palju suurema massi. Kas pidurdusmaa siis pikeneb ja kui palju? Vastus sõltub sellest, kas lisamass on autos või haagises ja kas haagisel on oma pidurid.</p>
<p>Pidurdusmaad on arvutatud sama mudeliga, mis <a href="/">kalkulaator</a>: VW Golf 8 (tühimass 1320 kg), keskmine suverehv, 80 km/h. Arvestatud on ainult pidurdusteekonda, reaktsiooniaega mitte.</p>
<div class="note-box"><strong>Lühidalt.</strong> Koorem autos pikendab pidurdusmaad vähe: täis autoga märjal alla meetri. Pidurita 750 kg haagis pikendab seda poole võrra: märjal 35,0 m asemel 52,4 m. Oma piduriga 1300 kg haagisega on pidurdusmaa 41,2 m, ehk raskem, aga piduriga haagis peatub lühemalt kui kergem pidurita haagis.</div>

<h2>Koorem autos</h2>
<p>Raskem auto ei pidurda tingimata kauem. Pidurdamisel aeglustab autot rehvi haare, ja haare kasvab koos massiga, sest rehv surutakse tugevamini vastu teed. Seepärast on kerge ja raske auto pidurdusmaa sama haardega peaaegu sama. Natuke mõjub koorem siiski: koormatud rehv haakub iga kilo kohta veidi halvemini.</p>
${tabel(
		['Koorem (koos juhiga)', 'Märg asfalt', 'Kuiv asfalt'],
		[
			['Ainult juht (75 kg)', '35,0 m', '23,7 m'],
			['4 inimest ja pagas (375 kg)', '35,5 m', '24,1 m'],
			['Täis auto (575 kg)', '35,8 m', '24,2 m']
		]
	)}
<p>Vahe on alla meetri. Koormaga auto juures loevad rohkem muud asjad: rehvirõhk (täis koormaga soovitab tootja enamasti suuremat rõhku), pidurite seisukord ja see, et raske auto on kurvis ja põiklemisel loiumalt juhitav.</p>

<h2>Pidurita haagis</h2>
<p>Kuni 750 kg täismassiga haagisel ei pea olema oma pidureid. Siis peatavad haagise auto pidurid ja rehvid: auto peab peale enda pidurdama ka haagist, mis lükkab tagant.</p>
${tabel(
		['', 'Märg asfalt', 'Kuiv asfalt'],
		[
			['Golf, ainult juht', '35,0 m', '23,7 m'],
			['Golf + 750 kg pidurita haagis', '52,4 m', '35,3 m'],
			['Toyota RAV4 (1660 kg)', '35,3 m', '23,7 m'],
			['RAV4 + 750 kg pidurita haagis', '49,5 m', '33,0 m']
		]
	)}
<p>Golfiga on pidurdusmaa poole pikem. RAV4 on raskem, nii et sama haagis on tema massist väiksem osa ja pidurdusmaa kasvab vähem. Samal põhjusel peatub koormatud auto pidurita haagisega mudeli järgi veidi lühemalt kui tühi: Golf nelja inimese ja pagasiga ning 750 kg haagisega 50,1 m, ainult juhiga 52,4 m. Raske haagis kerge tühja auto taga on kõige halvem kombinatsioon.</p>

<h2>Piduriga haagis</h2>
<p>Raskemal haagisel on inertspidur: kui auto pidurdab, surub haagis vastu haakekonksu ja see paneb haagise pidurid tööle. Haagis pidurdab siis ka ise, aga tavaliselt nõrgemalt kui auto.</p>
${tabel(
		['Golf + haagis', 'Märg asfalt', 'Kuiv asfalt'],
		[
			['Ilma haagiseta', '35,0 m', '23,7 m'],
			['1300 kg piduriga haagis', '41,2 m', '31,7 m'],
			['750 kg pidurita haagis', '52,4 m', '35,3 m'],
			['1300 kg haagis, pidurid ei tööta', '65,0 m', '43,7 m']
		]
	)}
<p>Piduriga 1300 kg haagisega on pidurdusmaa märjal 6 meetrit pikem kui ilma haagiseta, aga lühem kui 750 kg pidurita haagisega. Kui raske haagise pidurid ei tööta, on pidurdusmaa peaaegu kaks korda pikem. Seepärast tasub haagise pidurid ja haakeseadise enne pikemat sõitu üle vaadata.</p>

<h2>Mida see sõidul tähendab</h2>
<ul><li><strong>Hoia suuremat pikivahet.</strong> Pidurita haagisega on pidurdusmaa poole pikem, pikivahe peab olema samuti pikem. <a href="/liiklusohutus/pikivahe/">Pikivahe kalkulaator</a> näitab, kui suur vahe on piisav.</li><li><strong>Vaata registreerimistunnistusest</strong>, kui raske haagise (piduriga ja pidurita) võib sinu autoga vedada.</li><li><strong>Pane rehvidesse koormale sobiv rõhk.</strong> See on kirjas juhiukse piilaril või kütuseluugi sees. Vaata ka <a href="/teadmine/artiklid/rehvirohk-ja-pidurdus/">rehvirõhu ja pidurduse artiklit</a>.</li><li><strong>Märjal teel</strong> on vahe suurem kui kuival, sest haagise lisamassi peab peatama sama vähene haare.</li></ul>

<h2>Proovi oma autoga</h2>
<ul><li><a href="/liiklusohutus/">Peatumisteekonna kalkulaator</a>: saad lisada koorma ja haagise (piduriga või ilma)</li><li><a href="/">Pidurdusmaa kalkulaator</a>: sinu auto ja rehvid</li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Haagise pidurdus on mudelis lihtsustatud. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>Когда в машине вся семья с багажом или сзади прицеп, та же тормозная система должна остановить гораздо большую массу. Удлиняется ли тормозной путь и насколько? Ответ зависит от того, где дополнительная масса — в машине или в прицепе — и есть ли у прицепа свои тормоза.</p>
<p>Тормозной путь рассчитан той же моделью, что и <a href="/ru/">калькулятор</a>: VW Golf 8 (снаряжённая масса 1320 кг), средняя летняя шина, 80 км/ч. Учтён только тормозной путь, без времени реакции.</p>
<div class="note-box"><strong>Коротко.</strong> Груз в машине удлиняет тормозной путь мало: у полностью загруженной машины на мокрой дороге меньше чем на метр. Прицеп 750 кг без тормозов удлиняет его в полтора раза: на мокрой дороге 52,4 м вместо 35,0 м. С прицепом 1300 кг с собственными тормозами тормозной путь 41,2 м — прицеп тяжелее, но останавливается короче, чем более лёгкий прицеп без тормозов.</div>

<h2>Груз в машине</h2>
<p>Более тяжёлая машина не обязательно тормозит дольше. При торможении машину замедляет сцепление шин, а оно растёт вместе с массой, потому что шина сильнее прижимается к дороге. Поэтому тормозной путь лёгкой и тяжёлой машины при одинаковом сцеплении почти одинаков. Немного груз всё же влияет: нагруженная шина в расчёте на килограмм держит дорогу чуть хуже.</p>
${tabel(
		['Груз (вместе с водителем)', 'Мокрый асфальт', 'Сухой асфальт'],
		[
			['Только водитель (75 кг)', '35,0 м', '23,7 м'],
			['4 человека и багаж (375 кг)', '35,5 м', '24,1 м'],
			['Полная загрузка (575 кг)', '35,8 м', '24,2 м']
		]
	)}
<p>Разница меньше метра. С загруженной машиной важнее другое: давление в шинах (при полной загрузке производитель обычно рекомендует более высокое давление), состояние тормозов и то, что тяжёлая машина медленнее реагирует на руль в повороте и при объезде препятствия.</p>

<h2>Прицеп без тормозов</h2>
<p>У прицепа полной массой до 750 кг собственных тормозов может не быть. Тогда прицеп останавливают тормоза и шины автомобиля: машина должна затормозить не только себя, но и прицеп, который толкает её сзади.</p>
${tabel(
		['', 'Мокрый асфальт', 'Сухой асфальт'],
		[
			['Golf, только водитель', '35,0 м', '23,7 м'],
			['Golf + прицеп 750 кг без тормозов', '52,4 м', '35,3 м'],
			['Toyota RAV4 (1660 кг)', '35,3 м', '23,7 м'],
			['RAV4 + прицеп 750 кг без тормозов', '49,5 м', '33,0 м']
		]
	)}
<p>У Golf тормозной путь в полтора раза длиннее. RAV4 тяжелее, поэтому тот же прицеп составляет меньшую долю его массы и тормозной путь растёт меньше. По той же причине загруженная машина с прицепом без тормозов по модели останавливается чуть короче пустой: Golf с четырьмя людьми, багажом и прицепом 750 кг — 50,1 м, только с водителем — 52,4 м. Тяжёлый прицеп за лёгкой пустой машиной — худшее сочетание.</p>

<h2>Прицеп с тормозами</h2>
<p>У более тяжёлого прицепа есть инерционный тормоз: когда машина тормозит, прицеп давит на фаркоп, и это включает тормоза прицепа. Прицеп тогда тормозит и сам, но обычно слабее машины.</p>
${tabel(
		['Golf + прицеп', 'Мокрый асфальт', 'Сухой асфальт'],
		[
			['Без прицепа', '35,0 м', '23,7 м'],
			['Прицеп 1300 кг с тормозами', '41,2 м', '31,7 м'],
			['Прицеп 750 кг без тормозов', '52,4 м', '35,3 м'],
			['Прицеп 1300 кг, тормоза не работают', '65,0 м', '43,7 м']
		]
	)}
<p>С прицепом 1300 кг с тормозами тормозной путь на мокрой дороге на 6 метров длиннее, чем без прицепа, но короче, чем с прицепом 750 кг без тормозов. Если тормоза тяжёлого прицепа не работают, тормозной путь почти вдвое длиннее. Поэтому перед дальней поездкой стоит проверить тормоза прицепа и сцепное устройство.</p>

<h2>Что это значит в дороге</h2>
<ul><li><strong>Держите большую дистанцию.</strong> С прицепом без тормозов тормозной путь в полтора раза длиннее, дистанция тоже должна быть больше. <a href="/ru/liiklusohutus/pikivahe/">Калькулятор дистанции</a> покажет, какой дистанции достаточно.</li><li><strong>Посмотрите в техпаспорте</strong>, прицеп какой массы (с тормозами и без) можно буксировать вашей машиной.</li><li><strong>Накачайте шины под нагрузку.</strong> Давление указано на стойке водительской двери или в лючке бензобака. См. также <a href="/ru/teadmine/artiklid/rehvirohk-ja-pidurdus/">статью о давлении в шинах и торможении</a>.</li><li><strong>На мокрой дороге</strong> разница больше, чем на сухой: дополнительную массу прицепа должно остановить то же небольшое сцепление.</li></ul>

<h2>Проверьте на своём автомобиле</h2>
<ul><li><a href="/ru/liiklusohutus/">Калькулятор остановочного пути</a>: можно добавить груз и прицеп (с тормозами или без)</li><li><a href="/ru/">Калькулятор тормозного пути</a>: ваша машина и шины</li></ul>
<p class="note">Расчётные результаты — это оценки, а не измерения. Торможение прицепа в модели упрощено. Точность модели и допущения: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a> (на эстонском).</p>`;

	const KKK = [
		['Kas täis auto pidurdab kauem?', 'Natuke. VW Golf 8 pidurdusmaa märjal 80 km/h pealt on ainult juhiga 35,0 m ja täis autoga (575 kg) 35,8 m. Raskem auto surub rehvid tugevamini vastu teed, nii et haare kasvab peaaegu sama palju kui mass.'],
		['Kui palju pikendab pidurita haagis pidurdusmaad?', 'Golfiga 750 kg pidurita haagisega on pidurdusmaa märjal 80 km/h pealt 52,4 m, ilma haagiseta 35,0 m, ehk poole võrra pikem. Kuival 23,7 m asemel 35,3 m.'],
		['Kas piduriga haagisega peatub auto lühemalt?', 'Jah. 1300 kg piduriga haagisega on Golfi pidurdusmaa märjal 41,2 m, 750 kg pidurita haagisega 52,4 m. Kui raske haagise pidurid ei tööta, on see 65,0 m.'],
		['Kust näha, kui raske haagise võib autoga vedada?', 'Auto registreerimistunnistusest: seal on eraldi lubatud piduriga ja pidurita haagise mass.']
	];
	const KKK_RU = [
		['Загруженная машина тормозит дольше?', 'Немного. Тормозной путь VW Golf 8 на мокрой дороге с 80 км/ч только с водителем — 35,0 м, при полной загрузке (575 кг) — 35,8 м. Более тяжёлая машина сильнее прижимает шины к дороге, поэтому сцепление растёт почти так же, как масса.'],
		['Насколько прицеп без тормозов удлиняет тормозной путь?', 'Golf с прицепом 750 кг без тормозов на мокрой дороге с 80 км/ч тормозит 52,4 м, без прицепа — 35,0 м, то есть в полтора раза дольше. На сухой дороге — 35,3 м вместо 23,7 м.'],
		['С прицепом с тормозами машина останавливается короче?', 'Да. С прицепом 1300 кг с тормозами тормозной путь Golf на мокрой дороге 41,2 м, с прицепом 750 кг без тормозов — 52,4 м. Если тормоза тяжёлого прицепа не работают — 65,0 м.'],
		['Где посмотреть, прицеп какой массы можно буксировать?', 'В техпаспорте автомобиля: там отдельно указана допустимая масса прицепа с тормозами и без тормозов.']
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
