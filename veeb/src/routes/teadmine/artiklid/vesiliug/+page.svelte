<script>
	/* Vesiliug (akvaplaneerimine) — numbrid sama mudeliga mis kalkulaator (engine.js):
	   VW Golf 8, 205/55 R16, tehase rõhk 2,3 bar. Suverehv märgise klass B,
	   Põhjamaade talverehv klass D (nagu talverehvi-valimine). Ujumiskiirus:
	   Pidurdus.hydroplaneSpeedKmh, veekiht 1 / 3 / 5 mm. Märg pidurdus 90 km/h,
	   1 mm vett, +10 °C, ilma reaktsiooniajata. Numbrid 2026-10-12
	   (tookoda/artikli-numbrid.mjs). Sama teema TikToki videos „Vesiliug“. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'vesiliug';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Vesiliug ehk akvaplaneerimine tekib siis, kui rehv ei jõua vett enda alt välja suruda. Vesi kuhjub rehvi ette kiiluks, tõstab rehvi teelt üles ja auto libiseb vee peal. Sel hetkel ei tööta rool ega pidur.</p>
<p>Numbrid on arvutatud sama mudeliga, mis <a href="/">kalkulaator</a>: VW Golf 8, rehvimõõt 205/55 R16, õige rõhk 2,3 bar.</p>
<div class="note-box"><strong>Lühidalt.</strong> Sügavas lombis (5 mm vett) hakkab uus suverehv vee peal libisema umbes 104 km/h juures, 3 mm mustriga juba 78 km/h ja seadusliku miinimumiga (1,6 mm) 70 km/h juures. Kui rool läheb äkki kergeks, ära pidurda järsult ega keera rooli: võta gaas ära ja hoia otse, kuni rehv uuesti haarab.</div>

<h2>Miks rehv vee peale tõuseb</h2>
<p>Rehvi mustrisooned töötavad nagu pumbad: nad suruvad vee rehvi alt külgedele ja taha. Mida kiiremini sõidad, seda vähem on neil selleks aega. Kui vett tuleb rohkem peale, kui sooned jõuavad ära viia, tekib rehvi ette veekiil. Kiil kasvab kiirusega ja lõpuks kannab ta rehvi.</p>
<p>Seepärast loevad kolm asja: <strong>vee sügavus</strong>, <strong>mustri sügavus</strong> ja <strong>kiirus</strong>. Neljas on rehvirõhk: pehme rehv ujub varem (vt <a href="/teadmine/artiklid/rehvirohk-ja-pidurdus/">Rehvirõhk ja pidurdus</a>).</p>

<h2>Millise kiirusega rehv ujuma hakkab</h2>
<p>Suverehv, õige rõhk. Kiirus, millest alates rehv kaotab teega kontakti:</p>
${tabel(
		['Mustri sügavus', '3 mm vett', '5 mm vett (sügav lomp)'],
		[
			['8 mm (uus)', 'u 129 km/h', 'u 104 km/h'],
			['5 mm', 'u 109 km/h', 'u 88 km/h'],
			['3 mm', 'u 96 km/h', 'u 78 km/h'],
			['1,6 mm (seaduse piir)', 'u 87 km/h', 'u 70 km/h']
		]
	)}
<p>Õhukese veekihiga (1 mm, tavaline märg tee) ei ujuks uus rehv mõistlikul kiirusel üldse. Probleem on rööbastes ja lompides, kus vett on mitu millimeetrit. Rööbastes seisab vesi kõige kauem ja just sealt sõidab enamik autosid.</p>

<h2>Talverehv ujub varem</h2>
<p>Talverehvi muster on tehtud lume ja jää jaoks, mitte vee kiireks ärajuhtimiseks. Uus Põhjamaade talverehv hakkab 3 mm vees ujuma umbes 100 km/h juures, 5 mm vees juba umbes 81 km/h juures. Kulunud talverehviga (4 mm) on need piirid umbes 80 ja 64 km/h. Sügisel ja kevadel, kui teel on vett ja lörtsi, tasub see meeles pidada.</p>

<h2>Kulunud muster pikendab ka tavalist pidurdust</h2>
<p>Ka siis, kui auto vee peale ei tõuse, pidurdab kulunud rehv märjal pikemalt. Pidurdusmaa 90 km/h pealt märjal asfaldil (1 mm vett):</p>
${tabel(
		['Mustri sügavus', 'Pidurdusmaa', 'Uuest rohkem'],
		[
			['8 mm (uus)', '44,4 m', '—'],
			['3 mm', '48,6 m', '+4,2 m'],
			['1,6 mm', '50,5 m', '+6,1 m']
		]
	)}

<h2>Mida teha, kui auto ujuma hakkab</h2>
<p>Vesiliugu tunned ära selle järgi, et rool läheb äkki kergeks, mootori pöörded võivad hüpata ja auto ei reageeri roolile.</p>
<ul><li><strong>Ära pidurda järsult.</strong> Rehvil pole teega kontakti, pidur ei aeglusta, aga lukustab rattad ja auto võib pöörama hakata.</li><li><strong>Ära keera rooli.</strong> Kui esirattad on pööratud siis, kui nad uuesti haarduvad, sööstab auto järsult sinna, kuhu rattad näitavad.</li><li><strong>Võta gaas ära ja hoia otse.</strong> Auto aeglustub ise, veekiil kahaneb ja rehv saab teega uuesti kontakti.</li><li><strong>Kui pead pidurdama</strong>, pidurda sujuvalt. ABS aitab alles siis, kui rehv on taas teel.</li></ul>

<h2>Kuidas vesiliugu vältida</h2>
<ul><li><strong>Vähenda vihmaga kiirust</strong>, eriti maanteel ja seal, kus näed rööbastes vett.</li><li><strong>Sõida rööbastest veidi kõrvale</strong>, kui see on ohutu: seal on vett vähem.</li><li><strong>Kontrolli mustri sügavust.</strong> Alla 3 mm on vihmaga riskantne, ka kui seadus lubab 1,6 mm.</li><li><strong>Hoia rehvirõhk õige.</strong> Rõhk langeb sügisel jahenemisega umbes 0,1 bar iga 10 kraadi kohta.</li></ul>

<h2>Proovi oma autoga</h2>
<ul><li><a href="/">Pidurdusmaa kalkulaator</a>: sinu auto, rehvid ja teeolud</li><li><a href="/rehvi-vanus/">Rehvi vanuse kontroll</a>: DOT-kood ja muster</li><li><a href="/teadmine/artiklid/vanad-ja-kulunud-rehvid/">Vanad ja kulunud rehvid: kui palju pikeneb pidurdusmaa?</a></li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Tegelik ujumiskiirus sõltub ka rehvi mudelist, laiusest ja tee pinnast. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>Аквапланирование возникает, когда шина не успевает вытеснить воду из-под себя. Вода собирается перед шиной клином, поднимает её над дорогой, и машина скользит по воде. В этот момент не работают ни руль, ни тормоза.</p>
<p>Цифры рассчитаны той же моделью, что и <a href="/ru/">калькулятор</a>: VW Golf 8, размер шин 205/55 R16, правильное давление 2,3 бар.</p>
<div class="note-box"><strong>Коротко.</strong> В глубокой луже (5 мм воды) новая летняя шина начинает скользить по воде примерно с 104 км/ч, с протектором 3 мм — уже с 78 км/ч, а с законным минимумом (1,6 мм) — с 70 км/ч. Если руль вдруг стал лёгким, не тормозите резко и не поворачивайте руль: отпустите газ и держите прямо, пока шина снова не сцепится с дорогой.</div>

<h2>Почему шина поднимается на воду</h2>
<p>Канавки протектора работают как насосы: они выдавливают воду из-под шины в стороны и назад. Чем выше скорость, тем меньше у них на это времени. Если воды поступает больше, чем канавки успевают отвести, перед шиной образуется водяной клин. Клин растёт со скоростью и в конце концов несёт шину.</p>
<p>Поэтому важны три вещи: <strong>глубина воды</strong>, <strong>глубина протектора</strong> и <strong>скорость</strong>. Четвёртая — давление: мягкая шина всплывает раньше (см. <a href="/ru/teadmine/artiklid/rehvirohk-ja-pidurdus/">Давление в шинах и торможение</a>).</p>

<h2>С какой скорости шина всплывает</h2>
<p>Летняя шина, правильное давление. Скорость, с которой шина теряет контакт с дорогой:</p>
${tabel(
		['Глубина протектора', '3 мм воды', '5 мм воды (глубокая лужа)'],
		[
			['8 мм (новая)', 'ок. 129 км/ч', 'ок. 104 км/ч'],
			['5 мм', 'ок. 109 км/ч', 'ок. 88 км/ч'],
			['3 мм', 'ок. 96 км/ч', 'ок. 78 км/ч'],
			['1,6 мм (предел по закону)', 'ок. 87 км/ч', 'ок. 70 км/ч']
		]
	)}
<p>При тонком слое воды (1 мм, обычная мокрая дорога) новая шина на разумной скорости не всплыла бы вообще. Проблема — колеи и лужи, где воды несколько миллиметров. В колеях вода стоит дольше всего, а именно по ним едет большинство машин.</p>

<h2>Зимняя шина всплывает раньше</h2>
<p>Рисунок зимней шины сделан для снега и льда, а не для быстрого отвода воды. Новая северная зимняя шина начинает всплывать в 3 мм воды примерно со 100 км/ч, в 5 мм — уже примерно с 81 км/ч. С изношенной зимней шиной (4 мм) эти пороги примерно 80 и 64 км/ч. Осенью и весной, когда на дороге вода и слякоть, об этом стоит помнить.</p>

<h2>Изношенный протектор удлиняет и обычное торможение</h2>
<p>Даже если машина не всплывает, изношенная шина на мокрой дороге тормозит дольше. Тормозной путь с 90 км/ч на мокром асфальте (1 мм воды):</p>
${tabel(
		['Глубина протектора', 'Тормозной путь', 'Больше, чем у новой'],
		[
			['8 мм (новая)', '44,4 м', '—'],
			['3 мм', '48,6 м', '+4,2 м'],
			['1,6 мм', '50,5 м', '+6,1 м']
		]
	)}

<h2>Что делать, если машина всплыла</h2>
<p>Аквапланирование узнаётся по тому, что руль вдруг становится лёгким, обороты двигателя могут подскочить, а машина не реагирует на руль.</p>
<ul><li><strong>Не тормозите резко.</strong> У шины нет контакта с дорогой: тормоз не замедляет, но блокирует колёса, и машину может развернуть.</li><li><strong>Не поворачивайте руль.</strong> Если передние колёса повёрнуты в момент, когда они снова сцепятся, машина резко рванёт туда, куда смотрят колёса.</li><li><strong>Отпустите газ и держите прямо.</strong> Машина замедлится сама, водяной клин уменьшится, и шина снова коснётся дороги.</li><li><strong>Если нужно тормозить</strong>, тормозите плавно. ABS помогает только тогда, когда шина снова на дороге.</li></ul>

<h2>Как избежать аквапланирования</h2>
<ul><li><strong>Снижайте скорость в дождь</strong>, особенно на трассе и там, где в колеях видна вода.</li><li><strong>Держитесь чуть в стороне от колеи</strong>, если это безопасно: там меньше воды.</li><li><strong>Проверяйте глубину протектора.</strong> Меньше 3 мм в дождь рискованно, даже если закон допускает 1,6 мм.</li><li><strong>Следите за давлением.</strong> Осенью с похолоданием оно падает примерно на 0,1 бар на каждые 10 градусов.</li></ul>

<h2>Проверьте на своём автомобиле</h2>
<ul><li><a href="/ru/">Калькулятор тормозного пути</a>: ваша машина, шины и дорожные условия</li><li><a href="/ru/rehvi-vanus/">Проверка возраста шины</a>: код DOT и протектор</li><li><a href="/ru/teadmine/artiklid/vanad-ja-kulunud-rehvid/">Старые и изношенные шины: насколько удлиняется тормозной путь?</a></li></ul>
<p class="note">Расчётные результаты — это оценки, а не измерения. Реальная скорость аквапланирования зависит также от модели шины, её ширины и покрытия дороги. Точность модели и допущения: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a> (на эстонском).</p>`;

	const KKK = [
		['Mis kiirusel tekib vesiliug?', 'Sügavas lombis (5 mm vett) uue suverehviga umbes 104 km/h, 3 mm mustriga umbes 78 km/h ja 1,6 mm mustriga umbes 70 km/h juures. 3 mm veekihis on need piirid umbes 129, 96 ja 87 km/h (VW Golf 8, 205/55 R16, õige rõhk).'],
		['Mida teha, kui auto hakkab vee peal libisema?', 'Ära pidurda järsult ega keera rooli. Võta gaas ära ja hoia rool otse, kuni rehv uuesti teega haarab. Kui pead pidurdama, pidurda sujuvalt.'],
		['Kas talverehv ujub varem kui suverehv?', 'Jah. Uus Põhjamaade talverehv hakkab 3 mm vees ujuma umbes 100 km/h juures, uus suverehv umbes 129 km/h juures. 4 mm mustriga talverehvil on piir umbes 80 km/h.'],
		['Kui palju mõjutab kulunud muster märga pidurdust?', '90 km/h pealt märjal asfaldil on pidurdusmaa uue rehviga 44,4 m, 3 mm mustriga 48,6 m ja 1,6 mm mustriga 50,5 m.']
	];
	const KKK_RU = [
		['С какой скорости начинается аквапланирование?', 'В глубокой луже (5 мм воды) у новой летней шины примерно с 104 км/ч, с протектором 3 мм — примерно с 78 км/ч, с протектором 1,6 мм — примерно с 70 км/ч. В слое воды 3 мм эти пороги около 129, 96 и 87 км/ч (VW Golf 8, 205/55 R16, правильное давление).'],
		['Что делать, если машина заскользила по воде?', 'Не тормозите резко и не поворачивайте руль. Отпустите газ и держите руль прямо, пока шина снова не сцепится с дорогой. Если нужно тормозить, тормозите плавно.'],
		['Всплывает ли зимняя шина раньше летней?', 'Да. Новая северная зимняя шина начинает всплывать в 3 мм воды примерно со 100 км/ч, новая летняя — примерно со 129 км/ч. У зимней шины с протектором 4 мм порог около 80 км/ч.'],
		['Насколько изношенный протектор влияет на торможение на мокрой дороге?', 'С 90 км/ч на мокром асфальте тормозной путь с новой шиной 44,4 м, с протектором 3 мм — 48,6 м, с протектором 1,6 мм — 50,5 м.']
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
