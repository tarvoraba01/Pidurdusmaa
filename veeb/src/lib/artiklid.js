/* Artiklid (/teadmine/artiklid/) — uusim esimesena.
 * Uue artikli lisamine: tee kaust src/routes/teadmine/artiklid/<slug>/
 * (vt talverehvi-valimine) ja lisa siia üks rida. Sitemap, artiklite
 * leht ja Teadmine leht loevad nimekirja siit. */
export const ARTIKLID = [
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
		title: 'Millal talverehvid alla? Kuupäevad 2026/2027 ja reeglid',
		desc: 'Naastrehvid on lubatud 15. oktoobrist, talverehvid kohustuslikud 1. detsembrist. Kõik kuupäevad, 3 mm reegel ja pidurdusmaa numbrid: millal vahetada.',
		kuupaev: '2026-09-30',
		silt: 'Talverehvid',
		ru: {
			title: 'Когда менять шины на зимние в Эстонии? Сроки 2026/2027 и правила',
			desc: 'Шипованные шины разрешены с 15 октября, зимние обязательны с 1 декабря. Все сроки, правило 3 мм и тормозной путь: когда пора менять.',
			silt: 'Зимние шины'
		}
	},
	{
		slug: 'talverehvide-testid-2026',
		title: 'Talverehvide testid 2025–2026: mida mõõtmised näitavad',
		desc: 'Jääl üle kahe korra pikem pidurdusmaa, märjal 15 meetrit vahet, lumel alla meetri. Viimaste talverehvitestide mõõdetud pidurdusmaad ühest kohast.',
		kuupaev: '2026-09-30',
		silt: 'Testid',
		ru: {
			title: 'Тесты зимних шин 2025–2026: что показывают измерения',
			desc: 'На льду тормозной путь более чем вдвое длиннее, на мокром — 15 метров разницы, на снегу меньше метра. Измеренный тормозной путь из последних тестов зимних шин.',
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
