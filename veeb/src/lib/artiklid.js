/* Artiklid (/teadmine/artiklid/) — uusim esimesena.
 * Uue artikli lisamine: tee kaust src/routes/teadmine/artiklid/<slug>/
 * (vt talverehvi-valimine) ja lisa siia üks rida. Sitemap, artiklite
 * leht ja Teadmine leht loevad nimekirja siit. */
export const ARTIKLID = [
	{
		slug: 'pohjamaade-voi-kesk-euroopa-talverehv',
		title: 'Põhjamaade või Kesk-Euroopa talverehv: jääl üle 25 meetri vahet',
		desc: 'Jääl peatub Põhjamaade talverehv 50 km/h pealt 39,6 m, Kesk-Euroopa oma 65,3 m pealt. Lumel on nad võrdsed, märjal asfaldil on Kesk-Euroopa rehv 3 m parem. Kuidas poes vahet teha.',
		kuupaev: '2026-10-12',
		silt: 'Talverehvid',
		ru: {
			title: 'Северная или европейская зимняя шина: на льду больше 25 метров разницы',
			desc: 'На льду северная зимняя шина останавливается с 50 км/ч за 39,6 м, европейская — за 65,3 м. На снегу они равны, на мокром асфальте европейская на 3 м лучше. Как отличить в магазине.',
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
		title: 'Millal talverehvid alla panna: +7 °C reegel ja esimene lumi numbrites',
		desc: 'Ära oota 1. detsembrit: esimesel lumel peatub suverehv 50 km/h pealt 61 m, talverehv 26 m. Millal vahetada, milline talverehv valida ja kas vana rehv peab veel talve vastu.',
		kuupaev: '2026-09-30',
		silt: 'Talverehvid',
		ru: {
			title: 'Когда ставить зимние шины: правило +7 °C и первый снег в цифрах',
			desc: 'Не ждите 1 декабря: на первом снегу с 50 км/ч летняя шина останавливается за 61 м, зимняя — за 26 м. Когда менять, какую зимнюю шину выбрать и выдержит ли старая ещё зиму.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'talverehvide-testid-2026',
		title: 'Talverehvide testid 2025–2026: mida mõõtmised näitavad',
		desc: 'Jääl üle kahe korra pikem pidurdusmaa, märjal kuni 18 meetrit vahet, lumel alla meetri. ADAC, Auto Bild, Tekniikan Maailma ja Vi Bilägare talvetestide mõõdetud pidurdusmaad ühest kohast.',
		kuupaev: '2026-09-30',
		uuendatud: '2026-10-12',
		silt: 'Testid',
		ru: {
			title: 'Тесты зимних шин 2025–2026: что показывают измерения',
			desc: 'На льду тормозной путь более чем вдвое длиннее, на мокром — до 18 метров разницы, на снегу меньше метра. Измеренный тормозной путь из зимних тестов ADAC, Auto Bild, Tekniikan Maailma и Vi Bilägare.',
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
