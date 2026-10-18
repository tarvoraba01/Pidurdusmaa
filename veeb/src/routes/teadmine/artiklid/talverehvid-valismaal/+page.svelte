<script>
	/* Talverehvid Soomes, Lätis ja Leedus 2026: tähtajad ja muster
	   Artiklite partii 18.10.2026 (mustandid: 2ND Brain, Pidurdusmaa.ee/01 Articles, „(C) 02 Talverehvid Soomes, Lätis ja Leedus - mis reeglid kehtivad 2026“).
	   Seadused ja testid: allikad lehe lõpus. Pidurdusmaad: sama mudel mis kalkulaator (engine.js),
	   VW Golf 8, 205/55 R16; numbrid kontrollitud mudeliga 18.10.2026. Lehe tekst on genereeritud
	   mustandist (scratchpad md2page.py), parandused tee siin otse. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'talverehvid-valismaal';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const SISU = `<p>Kui sõidad talvel Eestist välja, kehtivad sinu autole selle riigi reeglid, kus parasjagu sõidad. Soomes võivad talverehvid olla kohustuslikud juba 1. novembrist, Leedus 10. novembrist ja Lätis 1. detsembrist. Lätis peab talverehvi muster olema vähemalt 4 mm.</p>
<p>Eestis kehtivad kuupäevad on lehel <a href="/teadmine/rehvivahetus/">Rehvivahetus 2026</a>. Allpool on lühike võrdlus naaberriikidega.</p>
<h2>Kõik ühes tabelis</h2>
<div class="tbl-wrap"><table class="t" style="min-width:640px"><thead><tr><th style="white-space:normal">Riik</th><th style="white-space:normal">Talverehv kohustuslik</th><th style="white-space:normal">Naastrehvid</th><th class="n" style="white-space:normal">Mustri sügavus vähemalt</th></tr></thead><tbody><tr><td><strong>Eesti</strong></td><td>1. detsember kuni 1. märts</td><td>15. oktoober kuni 31. märts, talvistes oludes 1. oktoober kuni 30. aprill</td><td class="n" style="white-space:normal">3 mm</td></tr><tr><td><strong>Soome</strong></td><td>1. november kuni 31. märts, kui ilm või tee seda nõuab</td><td>1. november kuni 31. märts, muul ajal, kui olud seda nõuavad</td><td class="n" style="white-space:normal">3 mm (soovitus 5 mm)</td></tr><tr><td><strong>Läti</strong></td><td>1. detsember kuni 1. märts</td><td>lubatud 1. oktoobrist, maist septembri lõpuni trahv</td><td class="n" style="white-space:normal">4 mm</td></tr><tr><td><strong>Leedu</strong></td><td>10. november kuni 31. märts</td><td>tuleb ära võtta 10. aprilliks</td><td class="n" style="white-space:normal">3 mm</td></tr></tbody></table></div>
<p>Kontrolli enne sõitu ikka ametlikult lehelt, sest reeglid muutuvad.</p>
<h2>Kas Soomes peavad välismaa autol olema talverehvid?</h2>
<p>Jah. Soome transpordiamet Traficom ütleb otse, et ka välismaa numbriga autod peavad Soomes kasutama talverehve. Soome reegel on seotud ilmaga: 1. novembrist 31. märtsini on talverehv kohustuslik, kui ilm või teeolud seda nõuavad.</p>
<p>Naastrehvide reegel on sarnane. Neid võib Soomes kasutada 1. novembrist 31. märtsini ja ka muul ajal, kui olud seda nõuavad.</p>
<p>Alates 1. detsembrist 2024 peab Soomes naastudeta talverehvil olema 3PMSF märk, nagu Eestiski. Naastrehvidelt seda märki ei nõuta.</p>
<p>Mustri miinimum on 3 mm. Traficom soovitab lörtsis ja lumes vähemalt 5 mm. Kui sõidad sageli Tallinnast Helsingisse ja sealt edasi põhja, tasub sellest soovitusest kinni pidada.</p>
<h2>Mis on Lätis teisiti?</h2>
<p>Kaks asja. Esiteks on Lätis talverehvi mustri miinimum 4 mm, mitte 3 mm nagu Eestis. Eestis veel lubatud 3,5 mm rehv ei ole Lätis seaduslik.</p>
<p>Teiseks peab alates 2024. aasta sügisest talverehvil olema kolme mäetipu ja lumehelbe märk (3PMSF). Ainult M+S märgiga rehv ei sobi. Rikkumise eest on trahv 30 eurot. Sama trahv on ka naastrehvidega sõitmise eest 1. maist 30. septembrini.</p>
<p>Kuupäevad on samad mis Eestis: 1. detsembrist 1. märtsini.</p>
<h2>Mis on Leedus teisiti?</h2>
<p>Leedus algab talverehvi kohustus varem ja lõpeb hiljem: 10. novembrist 31. märtsini, kuni 3,5-tonnistel autodel. Naastrehvid tuleb ära võtta 10. aprilliks. Talverehvi mustri miinimum on 3 mm, suverehvil 1,6 mm.</p>
<p>Kohaliku meedia andmetel on sobimatute või kulunud rehvide eest trahv 50 kuni 100 eurot.</p>
<h2>Kas Eesti naastrehvidega võib Kesk-Euroopasse sõita?</h2>
<p>Ole ettevaatlik. Naastrehvid kulutavad teed ja paljudes riikides on need keelatud või piiratud. Kontrolli enne sõitu kõigi nende riikide reegleid, mida läbid. Ära eelda, et Eesti reegel kehtib ka Poolas või Saksamaal.</p>
<p>Kui sõidad talvel tihti välismaale, on Põhjamaade lamellrehv tavaliselt lihtsam valik. Jääl jääb see naastule alla, aga piiranguid on vähem. Võrdlus on artiklis <a href="/teadmine/artiklid/naastrehv-voi-lamell/">Naastrehv või lamell</a>.</p>
<h2>Mida enne sõitu kontrollida?</h2>
<ol><li>Mustri sügavus. Läti jaoks vähemalt 4 mm, Soome talveteede jaoks soovitavalt 5 mm.</li><li>3PMSF märk, kui sul on lamellrehvid.</li><li>Kuupäevad: Soome ja Leedu nõuavad talverehvi juba novembris.</li><li>Naastud: kas sihtriik ja teel olevad riigid neid lubavad.</li></ol>
<h2>Leia rehv, mis sobib igale poole</h2>
<p>Kui pead rehve vahetama, vali kohe selline, mis vastab ka Läti 4 mm nõudele veel mitu talve. <a href="/autod/">Kirjuta oma auto mark ja vaata talverehvide pidurdusmaid ja hindu</a> või vaata <a href="/talverehvid/">talverehve oma mõõdu järgi</a>.</p>
<p class="note">Allikad: <a href="https://www.traficom.fi/en/transport/road/winter-tyres" rel="noopener">Traficom</a>, <a href="https://moottori.fi/uutinen/talvirenkaiden-maaritelma-muuttui-autoliitto-vaarinymmarryksilta-ei-ole-valtytty/" rel="noopener">Moottori 06.12.2024</a>, <a href="https://lvportals.lv/skaidrojumi/368210-soziem-riepam-jabut-obligati-marketam-ar-apzimejumu-kalns-un-sniegparslina-2024" rel="noopener">LV portāls 01.10.2024</a>, <a href="https://www.lsm.lv/raksts/dzive--stils/motori/14.10.2023-kad-izveleties-un-automasinai-likt-riepas-ar-radzem-skaidro-specialists.a527341/" rel="noopener">LSM 14.10.2023</a>, <a href="https://www.lsm.lv/raksts/zinas/latvija/17.10.2024-sai-ziemas-sezona-speka-jaunie-noteikumi-par-ziemas-riepam.a572256/" rel="noopener">LSM 17.10.2024</a>, <a href="https://reidasofficial.lt/patarimai-ir-rekomendacijos/eksploatacija/padangu-keitimas-2026-datos-taisykles/" rel="noopener">Reidas 10.03.2026</a>, <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://liikluskool.ee/16-tehnoseisund-ja-muud-valdkonnad/" rel="noopener">Liikluskool</a>.</p>`;

	const SISU_RU = `<p>За границей на вашу машину действуют правила той страны, по которой вы едете. В Финляндии зимняя резина может понадобиться уже с 1 ноября, в Литве с 10 ноября, в Латвии с 1 декабря. В Латвии протектор зимней шины должен быть не меньше 4 мм.</p>
<p>Эстонские сроки собраны на странице <a href="/ru/teadmine/rehvivahetus/">Смена резины 2026</a>. Ниже короткое сравнение с соседями.</p>
<h2>Всё в одной таблице</h2>
<div class="tbl-wrap"><table class="t" style="min-width:640px"><thead><tr><th style="white-space:normal">Страна</th><th style="white-space:normal">Зимняя резина обязательна</th><th style="white-space:normal">Шипы</th><th class="n" style="white-space:normal">Протектор не меньше</th></tr></thead><tbody><tr><td><strong>Эстония</strong></td><td>с 1 декабря по 1 марта</td><td>с 15 октября по 31 марта, при зимних условиях с 1 октября по 30 апреля</td><td class="n" style="white-space:normal">3 мм</td></tr><tr><td><strong>Финляндия</strong></td><td>с 1 ноября по 31 марта, если этого требуют погода или дорога</td><td>с 1 ноября по 31 марта, в другое время, если требуют условия</td><td class="n" style="white-space:normal">3 мм (рекомендуется 5 мм)</td></tr><tr><td><strong>Латвия</strong></td><td>с 1 декабря по 1 марта</td><td>разрешены с 1 октября, с мая по конец сентября штраф</td><td class="n" style="white-space:normal">4 мм</td></tr><tr><td><strong>Литва</strong></td><td>с 10 ноября по 31 марта</td><td>снять до 10 апреля</td><td class="n" style="white-space:normal">3 мм</td></tr></tbody></table></div>
<p>Перед поездкой всё равно сверяйтесь с официальным источником, правила меняются.</p>
<h2>Нужна ли зимняя резина в Финляндии машине с эстонскими номерами?</h2>
<p>Да. Финское транспортное агентство Traficom прямо пишет, что машины с иностранными номерами в Финляндии тоже обязаны ездить на зимней резине. Финское правило привязано к погоде: с 1 ноября по 31 марта зимние шины обязательны, если этого требуют погода или состояние дороги.</p>
<p>С шипами правило похожее. В Финляндии их можно использовать с 1 ноября по 31 марта, а в другое время, если этого требуют условия.</p>
<p>С 1 декабря 2024 года в Финляндии на нешипованной зимней шине должен быть знак 3PMSF, как и в Эстонии. Для шипованной резины этот знак не требуется.</p>
<p>Протектор должен быть не меньше 3 мм. Traficom советует в слякоть и снег не меньше 5 мм. Если часто ездите на пароме в Хельсинки и дальше на север, лучше держаться этой рекомендации.</p>
<h2>Чем отличается Латвия?</h2>
<p>Двумя вещами. Во-первых, в Латвии протектор зимней шины должен быть не меньше 4 мм, а не 3 мм, как в Эстонии. Шина с протектором 3,5 мм у нас ещё законна, а в Латвии уже нет.</p>
<p>Во-вторых, с осени 2024 года на зимней шине должен быть знак горы со снежинкой. Шина только с M+S не подходит. За нарушение грозит штраф 30 евро. Такой же штраф грозит за езду на шипах с 1 мая по 30 сентября.</p>
<p>Сроки такие же, как в Эстонии: с 1 декабря по 1 марта.</p>
<h2>Чем отличается Литва?</h2>
<p>В Литве период обязательной зимней резины начинается раньше и заканчивается позже: с 10 ноября по 31 марта для машин до 3,5 тонны. Шипы нужно снять до 10 апреля. Протектор зимней шины должен быть не меньше 3 мм, летней не меньше 1,6 мм.</p>
<p>По данным местных СМИ, штраф за неподходящие или изношенные шины составляет от 50 до 100 евро.</p>
<h2>Можно ли на эстонских шипах ехать в Центральную Европу?</h2>
<p>Осторожно. Шипы изнашивают дорогу, и во многих странах они запрещены или ограничены. Перед поездкой проверьте правила каждой страны на маршруте. Не думайте, что эстонское правило действует и в Польше или Германии.</p>
<p>Если зимой часто ездите за границу, северная липучка обычно проще. На льду она уступает шипам, зато ограничений меньше. Сравнение в статье <a href="/ru/teadmine/artiklid/naastrehv-voi-lamell/">Шипы или липучка</a>.</p>
<h2>Что проверить перед поездкой?</h2>
<ol><li>Протектор. Для Латвии от 4 мм, для финских зимних дорог желательно от 5 мм.</li><li>Знак 3PMSF, если у вас липучка.</li><li>Сроки: Финляндия и Литва требуют зимнюю резину уже в ноябре.</li><li>Шипы: разрешены ли они в стране назначения и в странах по пути.</li></ol>
<h2>Подберите шины, которые подойдут везде</h2>
<p>Если меняете резину, берите такую, у которой и через пару зим протектор будет больше латвийских 4 мм. <a href="/ru/autod/">Введите марку своей машины и посмотрите тормозной путь и цены зимних шин</a> или откройте <a href="/ru/talverehvid/">зимние шины по размеру</a>.</p>
<p class="note">Источники: <a href="https://www.traficom.fi/en/transport/road/winter-tyres" rel="noopener">Traficom</a>, <a href="https://moottori.fi/uutinen/talvirenkaiden-maaritelma-muuttui-autoliitto-vaarinymmarryksilta-ei-ole-valtytty/" rel="noopener">Moottori 06.12.2024</a>, <a href="https://lvportals.lv/skaidrojumi/368210-soziem-riepam-jabut-obligati-marketam-ar-apzimejumu-kalns-un-sniegparslina-2024" rel="noopener">LV portāls 01.10.2024</a>, <a href="https://www.lsm.lv/raksts/dzive--stils/motori/14.10.2023-kad-izveleties-un-automasinai-likt-riepas-ar-radzem-skaidro-specialists.a527341/" rel="noopener">LSM 14.10.2023</a>, <a href="https://www.lsm.lv/raksts/zinas/latvija/17.10.2024-sai-ziemas-sezona-speka-jaunie-noteikumi-par-ziemas-riepam.a572256/" rel="noopener">LSM 17.10.2024</a>, <a href="https://reidasofficial.lt/patarimai-ir-rekomendacijos/eksploatacija/padangu-keitimas-2026-datos-taisykles/" rel="noopener">Reidas 10.03.2026</a>, <a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet 12.11.2025</a>, <a href="https://liikluskool.ee/16-tehnoseisund-ja-muud-valdkonnad/" rel="noopener">Liikluskool</a>.</p>`;

	const KKK = [
		[
		 "Kas Eesti numbriga auto peab Soomes 1. novembril talverehvidel olema?",
		 "Kui ilm või tee seda nõuab, siis jah. Soome nõue kehtib ka välismaa autodele."
		],
		[
		 "Kas 3,5 mm mustriga talverehviga võib Lätti sõita?",
		 "Ei. Lätis peab talverehvi muster olema vähemalt 4 mm."
		],
		[
		 "Millal tuleb Leedus naastrehvid ära võtta?",
		 "Hiljemalt 10. aprilliks."
		],
		[
		 "Kas M+S rehv sobib Lätis või Soomes talveks?",
		 "Lätis ei sobi: seal peab talverehvil olema kolme mäetipu ja lumehelbe märk (3PMSF). Soomes ei sobi see naastudeta rehvina, sest seal nõutakse seda märki naastudeta talverehvilt."
		]
];
	const KKK_RU = [
		[
		 "Нужно ли машине с эстонскими номерами быть на зимней резине в Финляндии 1 ноября?",
		 "Если этого требуют погода или дорога, да. Финское требование действует и для иностранных машин."
		],
		[
		 "Можно ли ехать в Латвию с протектором 3,5 мм?",
		 "Нет. В Латвии протектор зимней шины должен быть не меньше 4 мм."
		],
		[
		 "До какого числа нужно снять шипы в Литве?",
		 "До 10 апреля."
		],
		[
		 "Подойдёт ли шина M+S для зимы в Латвии или Финляндии?",
		 "В Латвии нет: там на зимней шине должен быть знак горы со снежинкой (3PMSF). В Финляндии такая шина не подойдёт как липучка, потому что там этот знак обязателен для нешипованной зимней резины."
		]
];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	h1={T.h1}
	desc={T.desc}
	path="teadmine/artiklid/talverehvid-valismaal/"
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/talverehvid-valismaal/']]}
	lapsed={[]}
	uuendatud={A.uuendatud || A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/talverehvid-valismaal.png"
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
