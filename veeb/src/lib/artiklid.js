/* Artiklid (/teadmine/artiklid/) — uusim esimesena.
 * Uue artikli lisamine: tee kaust src/routes/teadmine/artiklid/<slug>/
 * (vt talverehvi-valimine) ja lisa siia üks rida. Sitemap, artiklite
 * leht ja Teadmine leht loevad nimekirja siit. */
export const ARTIKLID = [
	{
		slug: 'talverehvide-nouded',
		title: 'Talverehvide nõuded 2026: muster, märk, naastud ja trahv',
		h1: 'Talverehvide nõuded 2026: mis on kohustuslik ja mis ähvardab',
		desc: '1. detsembrist peab autol olema talverehv, muster vähemalt 3 mm ja lamellil 3PMSF märk. Vaata kõiki nõudeid ja seda, mis juhtub, kui politsei sind peatab.',
		kuupaev: '2026-10-18',
		silt: 'Talverehvid',
		ru: {
			title: 'Зимняя резина в Эстонии 2026: протектор, 3PMSF и штраф',
			h1: 'Требования к зимней резине в Эстонии 2026: что обязательно и чем грозит нарушение',
			desc: 'С 1 декабря зимняя резина обязательна: протектор от 3 мм, на липучке знак 3PMSF, шипы на все колёса. Все требования и что будет при проверке.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'naastrehvid-liiga-vara-voi-hilja',
		title: 'Naastrehvid liiga vara või hilja? Soe asfalt ja aprill',
		h1: 'Naastrehvid liiga vara või liiga hilja: soe asfalt, aprill ja reeglid',
		desc: 'Naastrehvid on lubatud 15. oktoobrist, varem ainult talvistes oludes. Vaata, mida soe asfalt pidurdusele teeb ja millal on õige aeg naastud alla panna.',
		kuupaev: '2026-10-18',
		silt: 'Talverehvid',
		ru: {
			title: 'Шипы слишком рано или поздно? Тёплый асфальт и апрель',
			h1: 'Шипы слишком рано или слишком поздно: тёплый асфальт, апрель и правила',
			desc: 'Шипы разрешены с 15 октября, раньше только при зимних условиях. Что тёплый асфальт делает с торможением и когда лучше ставить шипованную резину.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'nelja-aastaaja-rehvid',
		title: 'Nelja aastaaja rehvid Eestis: kas tohib ja kas tasub?',
		h1: 'Nelja aastaaja rehvid Eestis: kas tohib ja kas tasub',
		desc: 'Universaalrehv on Eestis talvel lubatud, kui sel on lumehelbe märk. Jääl on pidurdusmaa aga märgatavalt pikem. Vaata numbreid ja kellele see sobib.',
		kuupaev: '2026-10-18',
		silt: 'Talverehvid',
		ru: {
			title: 'Всесезонная резина в Эстонии: можно ли зимой?',
			h1: 'Всесезонная резина в Эстонии: можно ли ездить зимой и стоит ли',
			desc: 'Всесезонка в Эстонии разрешена зимой, если на ней есть знак снежинки. Но на льду тормозной путь заметно длиннее. Цифры тестов и кому она подходит.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'kasutatud-talverehvid',
		title: 'Kasutatud talverehvid: 7 asja, mida enne ostu kontrollida',
		h1: 'Kasutatud talverehvid: mida enne ostu kontrollida',
		desc: 'Kasutatud talverehvil peab olema vähemalt 3 mm mustrit, lamellil ka lumehelbe märk. Vaata ka vanust, naaste ja kahjustusi. Lihtne nimekiri enne ostu.',
		kuupaev: '2026-10-18',
		silt: 'Talverehvid',
		ru: {
			title: 'Б/у зимняя резина: 7 вещей, которые нужно проверить',
			h1: 'Б/у зимняя резина: что проверить перед покупкой',
			desc: 'У б/у зимней резины протектор должен быть не менее 3 мм, у липучки нужен знак снежинки. Проверьте возраст по DOT, шипы и повреждения. Чек-лист покупателя.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'talverehvid-valismaal',
		title: 'Talverehvid Soomes, Lätis ja Leedus 2026: tähtajad ja muster',
		h1: 'Talverehvid Soomes, Lätis ja Leedus: mis reeglid kehtivad 2026. aastal',
		desc: 'Talverehv on nõutud Leedus 10. novembrist ja Lätis 1. detsembrist, Soomes vajadusel 1. novembrist. Lätis on mustri miinimum 4 mm. Kas su rehvid sobivad?',
		kuupaev: '2026-10-18',
		silt: 'Talverehvid',
		ru: {
			title: 'Зимняя резина в Финляндии, Латвии и Литве 2026: сроки',
			h1: 'Зимняя резина в Финляндии, Латвии и Литве: правила 2026 года',
			desc: 'Зимняя резина обязательна в Литве с 10 ноября и в Латвии с 1 декабря, в Финляндии по погоде с 1 ноября. В Латвии протектор от 4 мм. Подходят ли ваши шины?',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'talverehvi-margistus-3pmsf',
		title: '3PMSF, M+S ja jäämärk: kuidas tunda ära õige talverehv',
		h1: '3PMSF, M+S ja jäämärk: kuidas ära tunda õiget talverehvi',
		desc: 'M+S märki paneb tootja ise, 3PMSF tähendab läbitud lumetesti ja jäämärk jäätesti. Vaata, mis peab Eestis talverehvil olema ja mida poes jälgida.',
		kuupaev: '2026-10-18',
		silt: 'Talverehvid',
		ru: {
			title: '3PMSF, M+S и знак льда: как отличить настоящую зимнюю шину',
			h1: '3PMSF, M+S и знак льда: как отличить настоящую зимнюю шину',
			desc: 'M+S ставит сам производитель, 3PMSF значит пройденный тест на снегу, а знак льда тест на льду. Что обязательно в Эстонии и на что смотреть при покупке.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'rehvi-kulje-margistus',
		title: 'Rehvi märgistus: mida tähendavad numbrid ja talvemärgid',
		h1: 'Rehvi märgistus küljel: kuidas talverehvi lugeda',
		desc: '205/55 R16 91T, M+S, lumehelves, jäämärk, DOT. Mida rehvi küljel olevad tähised tähendavad ja millised neist on Eestis talvel kohustuslikud.',
		kuupaev: '2026-10-18',
		silt: 'Talverehvid',
		ru: {
			title: 'Маркировка шин: расшифровка цифр и зимних значков',
			h1: 'Маркировка на боковине шины: как её расшифровать',
			desc: '205/55 R16 91T, M+S, снежинка, значок льда, DOT. Что означает маркировка на боковине и какие знаки обязательны зимой в Эстонии.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'odav-voi-kallis-talverehv',
		title: 'Odav või kallis talverehv? Mida testid tegelikult näitavad',
		h1: 'Odav või kallis talverehv: mida testid tegelikult näitavad',
		desc: 'Odavaim naastrehv vajas jääl üle kahe korra pikemat maad kui parim, aga märjal asfaldil oli parim. Kuidas teste lugeda ja oma teedele rehv valida.',
		kuupaev: '2026-10-18',
		silt: 'Talverehvid',
		ru: {
			title: 'Дешёвая или дорогая зимняя резина: что говорят тесты',
			h1: 'Дешёвая или дорогая зимняя резина: что на самом деле показывают тесты',
			desc: 'У самой дешёвой шипованной шины тормозной путь на льду был вдвое с лишним длиннее, чем у лучшей, зато на мокром асфальте она была первой. Как читать тесты.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'pohjamaade-voi-kesk-euroopa-talverehv',
		title: 'Põhjamaade või Kesk-Euroopa talverehv: jääl üle 50 meetri vahet',
		desc: 'Jääl peatub Põhjamaade talverehv 50 km/h pealt 59,9 m, Kesk-Euroopa oma 114,9 m pealt. Lumel on nad võrdsed, märjal asfaldil on Kesk-Euroopa rehv 3 m parem. Kuidas poes vahet teha.',
		kuupaev: '2026-10-12',
		silt: 'Talverehvid',
		ru: {
			title: 'Северная или европейская зимняя шина: на льду больше 50 метров разницы',
			desc: 'На льду северная зимняя шина останавливается с 50 км/ч за 59,9 м, европейская — за 114,9 м. На снегу они равны, на мокром асфальте европейская на 3 м лучше. Как отличить в магазине.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'reaktsiooniaeg',
		title: 'Reaktsiooniaeg: üks sekund on 90 km/h juures 25 meetrit',
		desc: '90 km/h pealt sõidab auto enne pidurdamist 25 m. Märjal teel tuleb pidurdusmaa 44,4 m, kokku 69,4 m. Kaks sekundit telefonis lisab 50 m. Peatumisteekond eri kiirustel.',
		kuupaev: '2026-10-12',
		silt: 'Liiklusohutus',
		ru: {
			title: 'Время реакции: на 90 км/ч одна секунда — это 25 метров',
			desc: 'С 90 км/ч машина до начала торможения проезжает 25 м. На мокрой дороге тормозной путь 44,4 м, всего 69,4 м. Две секунды в телефоне добавляют 50 м. Остановочный путь на разных скоростях.',
			silt: 'Безопасность'
		}
	},
	{
		slug: 'vesiliug',
		title: 'Vesiliug: millal auto lombis ujuma hakkab ja mida siis teha',
		desc: 'Sügavas lombis hakkab uus suverehv vee peal libisema umbes 104 km/h, 3 mm mustriga 78 km/h ja 1,6 mm mustriga 70 km/h juures. Miks see juhtub ja mida vesiliu ajal teha.',
		kuupaev: '2026-10-12',
		silt: 'Liiklusohutus',
		ru: {
			title: 'Аквапланирование: когда машина всплывает в луже и что делать',
			desc: 'В глубокой луже новая летняя шина начинает скользить по воде примерно с 104 км/ч, с протектором 3 мм — с 78 км/ч, с 1,6 мм — с 70 км/ч. Почему так происходит и что делать.',
			silt: 'Безопасность'
		}
	},
	{
		slug: 'abs-pidurdus',
		title: 'ABS: mida see tegelikult teeb ja kuidas hädaolukorras pidurdada',
		desc: 'ABS hoiab rattad veeremas, et saaksid pidurdades pöörata. Märjal 80 km/h pealt peatub auto ABS-iga 34,7 m, keskmise juhiga ilma ABS-ita 46,2 m. Kruusal võib ABS pidurdust pikendada.',
		kuupaev: '2026-10-12',
		silt: 'Liiklusohutus',
		ru: {
			title: 'ABS: что он делает на самом деле и как тормозить в опасной ситуации',
			desc: 'ABS не даёт колёсам заблокироваться, чтобы при торможении можно было поворачивать. На мокрой дороге с 80 км/ч машина с ABS останавливается за 34,7 м, без ABS — за 46,2 м.',
			silt: 'Безопасность'
		}
	},
	{
		slug: 'pimedas-helkur',
		title: 'Pidurdusmaa pimedas: miks helkur päästab elu',
		desc: 'Tumedas riietuses jalakäijat näeb lähitulede valgel 30 m, helkuriga 130–150 m kauguselt. Märjal teel jõuab 30 m peale peatuda vaid kuni 53 km/h pealt.',
		kuupaev: '2026-10-07',
		silt: 'Liiklusohutus',
		ru: {
			title: 'Тормозной путь в темноте: зачем нужен световозвращатель',
			desc: 'Пешехода в тёмной одежде при ближнем свете видно с 30 м, со световозвращателем — со 130–150 м. На мокрой дороге на 30 м можно остановиться только с 53 км/ч.',
			silt: 'Безопасность'
		}
	},
	{
		slug: 'naastrehv-voi-lamell',
		title: 'Naastrehv või lamell? Pidurdusmaad jääl, lumel ja asfaldil',
		desc: 'Jääl peatus naastrehv testis 50 km/h pealt keskmiselt 36,9 m, lamell 49,4 m. Märjal ja kuival on vahe alla 2 m. Kõige suurem on naastu eelis jääl nulli lähedal.',
		kuupaev: '2026-10-07',
		silt: 'Talverehvid',
		ru: {
			title: 'Шипы или «липучка»: тормозной путь на льду, снегу и асфальте',
			desc: 'На льду шипованная шина в тесте остановилась с 50 км/ч в среднем за 36,9 м, «липучка» — за 49,4 м. На мокром и сухом асфальте разница меньше 2 м.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'linnas-50-kmh',
		title: 'Linnas 50 km/h: kui palju on vahet 40 ja 60 km/h vahel?',
		desc: 'Peatumisteekond 50 km/h pealt on kuival 23,5 m, 60 km/h pealt 30,3 m. Seal, kus 50 km/h auto seisab, sõidab 60 km/h auto veel 45 km/h.',
		kuupaev: '2026-10-07',
		silt: 'Liiklusohutus',
		ru: {
			title: '50 км/ч в городе: какая разница между 40 и 60 км/ч?',
			desc: 'Остановочный путь с 50 км/ч на сухой дороге 23,5 м, с 60 км/ч — 30,3 м. Там, где машина с 50 км/ч уже стоит, машина с 60 км/ч едет ещё 45 км/ч.',
			silt: 'Безопасность'
		}
	},
	{
		slug: 'koorem-ja-haagis',
		title: 'Pidurdusmaa koormaga ja haagisega: kui palju see pikeneb?',
		desc: 'Täis auto pidurdab märjal alla meetri kauem. 750 kg pidurita haagisega on pidurdusmaa poole pikem: 35,0 m asemel 52,4 m. Piduriga haagis peatub lühemalt.',
		kuupaev: '2026-10-07',
		silt: 'Liiklusohutus',
		ru: {
			title: 'Тормозной путь с грузом и прицепом: насколько он удлиняется?',
			desc: 'Груз в машине удлиняет тормозной путь меньше чем на метр. С прицепом 750 кг без тормозов он в полтора раза длиннее: 52,4 м вместо 35,0 м.',
			silt: 'Безопасность'
		}
	},
	{
		slug: 'rehvirohk-ja-pidurdus',
		title: 'Rehvirõhk ja pidurdus: mida teeb liiga madal rõhk?',
		desc: 'Tavaliselt lisab liiga madal rõhk märjal mõne meetri. Sügavas vees langeb akvaplaneerimise kiirus 129 km/h pealt 101 km/h peale. Numbrid, sügisene rõhulangus ja kuidas kontrollida.',
		kuupaev: '2026-10-06',
		silt: 'Rehvid',
		ru: {
			title: 'Давление в шинах и торможение: чем опасно низкое давление?',
			desc: 'Обычно низкое давление добавляет на мокрой дороге пару метров. В глубокой воде скорость аквапланирования падает со 129 до 101 км/ч. Цифры, осеннее падение давления и как проверить.',
			silt: 'Шины'
		}
	},
	{
		slug: 'vanad-ja-kulunud-rehvid',
		title: 'Vanad ja kulunud rehvid: kui palju pikeneb pidurdusmaa?',
		desc: '3 mm mustriga suverehvi pidurdusmaa on märjal 4 m pikem kui uuel, talverehvil lumel veerandi võrra pikem. Arvutatud pidurdusmaad, DOT-koodi lugemine ja millal vahetada.',
		kuupaev: '2026-10-06',
		silt: 'Rehvid',
		ru: {
			title: 'Старые и изношенные шины: насколько удлиняется тормозной путь?',
			desc: 'Летняя шина с протектором 3 мм на мокрой дороге останавливается на 4 м дальше новой, зимняя на снегу — на четверть дальше. Расчёты, как читать код DOT и когда менять.',
			silt: 'Шины'
		}
	},
	{
		slug: 'millal-talverehvid-alla',
		title: 'Mis temperatuuril talverehvid alla panna? +7 °C reegel numbrites',
		desc: 'Ära oota 1. detsembrit: esimesel lumel peatub suverehv 50 km/h pealt 61 m, talverehv 26 m. Mis temperatuuril vahetada, milline talverehv valida ja kas vana rehv peab veel talve vastu.',
		kuupaev: '2026-09-30',
		uuendatud: '2026-10-18',
		silt: 'Talverehvid',
		ru: {
			title: 'При какой температуре менять резину на зимнюю: правило +7 °C',
			desc: 'Не ждите 1 декабря: на первом снегу с 50 км/ч летняя шина останавливается за 61 м, зимняя — за 26 м. При какой температуре менять, какую зимнюю шину выбрать и выдержит ли старая ещё зиму.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'talverehvide-testid-2026',
		title: 'Talverehvide test 2026: parimad naast- ja lamellrehvid',
		desc: 'Kes pidurdas 2025. ja 2026. aasta talvetestides jääl, lumel ja märjal kõige lühemalt: Vi Bilägare, ADAC, Auto Bild, Tekniikan Maailma. Mõõdetud meetrid ühes tabelis, mitte punktid.',
		kuupaev: '2026-09-30',
		uuendatud: '2026-10-18',
		silt: 'Testid',
		ru: {
			title: 'Тест зимних шин 2026: лучшие шипованные и нешипованные',
			desc: 'Кто тормозил короче всех на льду, снегу и мокром в зимних тестах 2025 и 2026 годов: Vi Bilägare, ADAC, Auto Bild, Tekniikan Maailma. Измеренные метры в одной таблице, а не баллы.',
			silt: 'Тесты'
		}
	},
	{
		slug: 'peatumisteekonna-kalkulaator',
		title: 'Uus tasuta kalkulaator: kui pika maa pealt auto peatub?',
		desc: 'Muuda kiirust, reaktsiooniaega, teeolusid ja rehve ning vaata kohe, kuidas peatumisteekond muutub. Kaks olukorda kõrvuti — tasuta ja ilma reklaamita.',
		kuupaev: '2026-09-29',
		silt: 'Tööriist'
	},
	{
		slug: 'talverehvi-valimine',
		title: 'Talverehvi valimine: mida numbrid ütlevad',
		desc: 'Suverehv lumel, Põhjamaade vs Kesk-Euroopa talverehv, naast vs lamell, mustri sügavus ja millal vahetada — pidurdusmaad meetrites.',
		kuupaev: '2026-09-26',
		silt: 'Talverehvid',
		ru: {
			title: 'Как выбрать зимнюю шину: что говорят цифры',
			desc: 'Летняя шина на снегу, северная и европейская зимняя шина, шипы или «липучка», глубина протектора и когда менять — тормозной путь в метрах.',
			silt: 'Зимние шины'
		}
	}
];

export const artikliTee = (a) => '/teadmine/artiklid/' + a.slug + '/';

/** 2026-09-26 → 26.09.2026 */
export const kuup = (iso) => iso.split('-').reverse().join('.');
