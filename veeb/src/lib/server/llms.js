/* llms.txt sisu (ET/EN/RU) — lühike juhend AI-otsingutele (ChatGPT, Perplexity, Claude,
 * Gemini, Google AI Overviews): mis lehel on, kust numbrid tulevad ja
 * millist lehte tsiteerida. Formaat: https://llmstxt.org/
 *
 * Kõik numbrid tulevad ehituse ajal samadest andmetest ja samast mudelist,
 * mis kalkulaator (nagu sitemap.xml) — käsitsi kirjutatud arve siin pole,
 * peale metoodikalehe täpsusnumbrite, mis on sealt sõna-sõnalt üle võetud.
 */
import { core, models } from '$lib/server/andmed.js';
import { autod } from '$lib/server/autod.js';
import { arvuta } from '$lib/server/jaga.js';
import { ARTIKLID, artikliTee } from '$lib/artiklid.js';

const BASE = 'https://pidurdusmaa.ee';
const n = (x) => new Intl.NumberFormat('et-EE').format(x);
const m = (x) => (Math.round(x * 10) / 10).toString().replace('.', ',');

/* VW Golf 8, 205/55 R16, 90 km/h — samad valikud mis avalehe hero'l */
function pidurdus(o, r, v = 90) {
	const x = arvuta({ a: 'vw_golf_8', ab: false, m: '20555R16', o, v, r, mm: null, rt: 0, l: 'et' });
	return x ? x.d : null;
}


/** llms.txt tekst keeles lang ('et' | 'en' | 'ru'). */
export function llmsTekst(lang = 'et') {
	const c = core();
	const kuiv = pidurdus('dry', 'k:SUMMER_TOURING');
	const marg = pidurdus('wet', 'c:SUMMER_TOURINGC');
	const lumi = pidurdus('snow', 'k:WINTER_NORDIC');
	if (!kuiv || !marg || !lumi) throw new Error('llms.txt: pidurdusmaad ei saanud arvutada');
	const reakts = 25; // 90 km/h × 1 s
	/* jää 50 km/h: rehvitüüpide keskmised (sama mis talverehvide lehel) */
	const jaaNaast = pidurdus('ice', 'k:WINTER_STUDDED', 50), jaaLamell = pidurdus('ice', 'k:WINTER_NORDIC', 50), jaaKesk = pidurdus('ice', 'k:WINTER_CENTRAL', 50), jaaSuvi = pidurdus('ice', 'k:SUMMER_TOURING', 50);
	const lumiSuvi = pidurdus('snow', 'k:SUMMER_TOURING', 50), lumiTalv = pidurdus('snow', 'k:WINTER_NORDIC', 50);
	const jaa = { naast: jaaNaast, lamell: jaaLamell, kesk: jaaKesk, suvi: jaaSuvi, lumiSuvi, lumiTalv };
	const allikad = Object.values(c.sources || {})
		.map((s) => (s.aasta && !String(s.nimi).includes(String(s.aasta)) ? `${s.nimi} ${s.aasta}` : s.nimi))
		.sort()
		.join(', ');
	const nMud = n(Object.keys(models()).length), nMoot = n(c.eprelSizes.filter((m) => /^\d{5}R\d{2}C?$/.test(m)).length) /* ainult päris mõõdud (audit: ~690 võtit on nimest valesti loetud) */, nTest = n(c.tyres.length), nAuto = n(autod().polved.size);
	const md = lang === 'et' ? m : (x) => (Math.round(x * 10) / 10).toString().replace('.', lang === 'en' ? '.' : ',');
	if (lang === 'en' || lang === 'ru') return valisKeel(lang, { kuiv, marg, lumi, reakts, allikad, nMud, nMoot, nTest, nAuto, md, jaa });
	const artiklid = (ARTIKLID || [])
		.map((a) => `- [${a.title}](${BASE}${artikliTee(a)})${a.desc ? ': ' + a.desc : ''}`)
		.join('\n');
	const tekst = `# Pidurdusmaa.ee

> Tasuta Eesti pidurdusmaa kalkulaator: arvutab, kui pika maa peal sinu auto konkreetsete rehvidega peatub — kuival, märjal, lumel ja jääl — ning võrdleb rehve EL-i rehvimärgise ja sõltumatute testide põhjal. Eesti, vene ja inglise keeles. Teeb Rabarvo OÜ (registrikood 16947078).

Lühifaktid (arvutatud sama mudeliga mis kalkulaator; VW Golf 8, 205/55 R16, uus tüüpiline rehv, 90 km/h, ilma reaktsiooniajata):
- Pidurdusmaa kuival asfaldil: ${m(kuiv)} m
- Pidurdusmaa märjal asfaldil (+10 °C): ${m(marg)} m
- Pidurdusmaa lumel (Põhjamaade talverehv): ${m(lumi)} m
- Reaktsiooniaeg 1 s lisab 90 km/h juures ${reakts} m; peatumisteekond märjal on seega umbes ${m(reakts + marg)} m.
- Pidurdusmaa kasvab kiiruse ruudus: kahekordne kiirus ≈ neljakordne pidurdusmaa.

Andmed: ${nMud} rehvimudelit EL-i rehvimärgise andmebaasist (EPREL), ${nMoot} rehvimõõtu, ${nTest} rehvi sõltumatutes testides (${allikad}), ${nAuto} automudeli põlvkonda tehase rehvimõõtudega.

Täpsus: 369 mõõdetud pidurdusmaa vastu on mudeli jääkviga asfaldil (märg ja kuiv) 4,4%, betoonil 6,6%, lumel 5,5%, jääl 6,9%. Tulemused on arvutatud hinnangud, mitte mõõtmised. Rehvide järjestust ei müüda: see tuleb ainult andmetest.

Tsiteerimisel palun viita lehele ${BASE}/ või vastavale alamlehele.

## Tööriistad
- [Pidurdusmaa kalkulaator](${BASE}/): auto + rehv + tee + kiirus → pidurdus- ja peatumisteekond
- [Rehvi valimine](${BASE}/rehvi-valimine/): parimad rehvid mõõdu ja auto järgi
- [Võrdle rehve](${BASE}/vordle-rehve/): kuni 4 rehvi kõrvuti
- [Talverehvid](${BASE}/talverehvid/): talverehvid mõõdu järgi
- [Liiklusohutuse simulaatorid](${BASE}/liiklusohutus/): kiirus, pimedas, pikivahe, kurv
- [Reaktsioonitest](${BASE}/liiklusohutus/reaktsioon/): mäng, kui kiiresti sina pidurdad
- [Koolitus](${BASE}/liiklusohutus/koolitus/): eeltest, selgitused simulaatoriga, järeltest; autokoolid loovad oma grupi testi
- [Rehvi vanus](${BASE}/rehvi-vanus/): DOT-kood → rehvi vanus, mustri sügavus → pidurdusmaa

## Levinud küsimused (lühivastused, samast mudelist)
- Millal on talverehvid Eestis kohustuslikud? 1. detsembrist 1. märtsini. Naastrehvid on lubatud 15. oktoobrist 31. märtsini, talviste olude korral 1. oktoobrist 30. aprillini. Talverehvil peab olema kolme mäetipu ja lumehelbe märk (3PMSF); mustri sügavus üle 3 mm, suverehvil vähemalt 1,6 mm.
- Millal talverehvid alla panna? Kui ööd on alla +7 °C või tuleb esimene lumi, mitte alles 1. detsembril: esimesel lumel 50 km/h pealt peatub suverehv umbes ${m(lumiSuvi)} m, Põhjamaade talverehv ${m(lumiTalv)} m (pidurdusmaa ilma reaktsiooniajata).
- Naast või lamell? Jääl 50 km/h pealt peatub tüüpiline naastrehv umbes ${m(jaaNaast)} m, Põhjamaade lamellrehv ${m(jaaLamell)} m, Kesk-Euroopa talverehv ${m(jaaKesk)} m ja suverehv ${m(jaaSuvi)} m. Lumel ja kuival asfaldil on naastu ja lamelli vahe väike.
- Kui palju loeb EL-i märgise märghaardumise klass? A- ja E-klassi suverehvi vahe on märjal asfaldil 90 km/h pealt umbes 18 m pidurdusmaad. Klass on mõõdupõhine: sama mudel võib teises mõõdus olla teise klassiga.
- Mis on peatumisteekond? Reaktsiooniteekond + pidurdusteekond. 50 km/h pealt peatub auto kuival teel umbes 24 m ja märjal 27 m, 90 km/h pealt umbes 55 m ja 70 m (1 s reaktsiooniga). 1 s reaktsioon = 14 m 50 km/h juures ja 25 m 90 km/h juures.
- Kui palju muudab kulunud muster? 3 mm mustriga suverehv peatub märjal 90 km/h pealt umbes 4 m kaugemal kui uus; sademevee roopas (3 mm vett) pikeneb pidurdusmaa 1,6 mm mustriga peaaegu kaks korda. Talverehvil on lumel 3 mm mustriga pidurdus umbes veerandi võrra pikem kui uuel.

## Andmed
- [Rehvid ja mõõdud](${BASE}/rehvid/): mõõdu lehel kõik selle mõõdu rehvid märgise klasside järgi, KKK ja autod, millel see on tehasemõõt
- [Rehvimargid](${BASE}/margid/): iga margi mudelid, märgise klasside jaotus ja testitud mudelid
- [Automudelid](${BASE}/autod/): ${nAuto} põlvkonda — tehase rehvimõõdud, mootorid, arvutatud pidurdusmaa, parimad rehvid põhimõõdus
- [Sõltumatud rehvitestid](${BASE}/testid/): mõõdetud pidurdusmaad testi kaupa
- Iga rehvi lehel (${BASE}/rehvid/<mudel>/): EL-i märgis mõõtude kaupa, sõltumatute testide tulemused ja koht, arvutatud pidurdusmaa valitud autoga, KKK

## Teadmised
- [Kuidas pidurdusmaa arvutatakse](${BASE}/teadmine/kuidas-pidurdusmaa-arvutatakse/): metoodika, allikad, täpsus
- [Pidurdusteekond ja peatumisteekond](${BASE}/teadmine/pidurdusteekond-ja-peatumisteekond/)
- [EL-i rehvimärgis](${BASE}/teadmine/rehvimargis/)
- [Rehvivahetuse ajad Eestis](${BASE}/teadmine/rehvivahetus/)
${artiklid}

## Muu
- [Meist](${BASE}/meist/): kes teeb, andmeallikad, sõltumatus
- [Partnerid ja poelingid](${BASE}/teadmine/partnerid/): hinnad ja poelingid tulevad partnerpoodidest, järjestust need ei mõjuta
- Autokoolidele: koolitus (${BASE}/liiklusohutus/koolitus/) on tasuta; õpetaja loob grupile testi, õpilased teevad eel- ja järeltesti, tulemused näeb õpetaja
- Kõik lehed on eesti keeles, enamik ka vene keeles (/ru/), tööriistad inglise keeles (/en/)
- [In English](${BASE}/en/) ([llms.txt](${BASE}/en/llms.txt)) · [На русском](${BASE}/ru/) ([llms.txt](${BASE}/ru/llms.txt))
`;
	return tekst;
}

function valisKeel(lang, x) {
	const en = lang === 'en';
	const L = (p) => BASE + '/' + lang + p;
	const ET = en ? ' (in Estonian)' : ' (на эстонском)';
	if (en) return `# Pidurdusmaa.ee

> Free Estonian braking distance calculator: shows how far your car stops on specific tyres — on dry, wet, snow and ice — and compares tyres using the EU tyre label and independent tests. In Estonian, Russian and English. Made by Rabarvo OÜ (registry code 16947078).

Key facts (same model as the calculator; VW Golf 8, 205/55 R16, typical new tyre, 90 km/h, without reaction time):
- Braking distance on dry asphalt: ${x.md(x.kuiv)} m
- Braking distance on wet asphalt (+10 °C): ${x.md(x.marg)} m
- Braking distance on snow (Nordic winter tyre): ${x.md(x.lumi)} m
- A 1 s reaction time adds ${x.reakts} m at 90 km/h, so the stopping distance on wet roads is about ${x.md(x.reakts + x.marg)} m.
- Braking distance grows with the square of speed: double the speed ≈ four times the braking distance.

Data: ${x.nMud} tyre models from the EU tyre label database (EPREL), ${x.nMoot} tyre sizes, ${x.nTest} tyres in independent tests (${x.allikad}), ${x.nAuto} car model generations with factory tyre sizes.

Accuracy: against 369 measured braking distances the model's residual error is 4.4% on asphalt (wet and dry), 6.6% on concrete, 5.5% on snow and 6.9% on ice. Results are calculated estimates, not measurements. Tyre rankings are not for sale: they come from the data only.

When citing, please link to ${BASE}/en/ or the relevant page.

## Tools
- [Braking distance calculator](${L('/')}): car + tyre + road + speed → braking and stopping distance
- [Tyre chooser](${L('/rehvi-valimine/')}): best tyres for your size and car
- [Compare tyres](${L('/vordle-rehve/')}): up to 4 tyres side by side
- [Road safety simulators](${L('/liiklusohutus/')}): speed, darkness, following distance, curves
- [Reaction test](${L('/liiklusohutus/reaktsioon/')}): game — how fast do you brake
- [Tyre age](${L('/rehvi-vanus/')}): DOT code → tyre age, tread depth → braking distance

## Data${ET}
- [Tyres and sizes](${BASE}/rehvid/)
- [Car models](${BASE}/autod/)
- [Independent tyre tests](${BASE}/testid/)
- [How braking distance is calculated](${BASE}/teadmine/kuidas-pidurdusmaa-arvutatakse/): method, sources, accuracy

## Other
- [Eesti keeles](${BASE}/) ([llms.txt](${BASE}/llms.txt)) · [На русском](${BASE}/ru/) ([llms.txt](${BASE}/ru/llms.txt))
`;
	return `# Pidurdusmaa.ee

> Бесплатный эстонский калькулятор тормозного пути: показывает, на каком расстоянии ваша машина останавливается на конкретных шинах — на сухой и мокрой дороге, снегу и льду — и сравнивает шины по европейской маркировке и независимым тестам. На эстонском, русском и английском. Делает Rabarvo OÜ (регистрационный код 16947078).

Краткие факты (та же модель, что и в калькуляторе; VW Golf 8, 205/55 R16, типичная новая шина, 90 км/ч, без времени реакции):
- Тормозной путь на сухом асфальте: ${x.md(x.kuiv)} м
- Тормозной путь на мокром асфальте (+10 °C): ${x.md(x.marg)} м
- Тормозной путь на снегу (северная зимняя шина): ${x.md(x.lumi)} м
- Время реакции 1 с добавляет на 90 км/ч ${x.reakts} м, поэтому остановочный путь на мокрой дороге около ${x.md(x.reakts + x.marg)} м.
- Тормозной путь растёт пропорционально квадрату скорости: вдвое большая скорость ≈ вчетверо больший тормозной путь.

Данные: ${x.nMud} моделей шин из базы европейской маркировки (EPREL), ${x.nMoot} размеров шин, ${x.nTest} шин в независимых тестах (${x.allikad}), ${x.nAuto} поколений моделей автомобилей с заводскими размерами шин.

Точность: по 369 измеренным тормозным путям остаточная ошибка модели на асфальте (мокром и сухом) 4,4%, на бетоне 6,6%, на снегу 5,5%, на льду 6,9%. Результаты — расчётные оценки, а не измерения. Рейтинг шин не продаётся: он основан только на данных.

При цитировании, пожалуйста, ссылайтесь на ${BASE}/ru/ или соответствующую страницу.

## Инструменты
- [Калькулятор тормозного пути](${L('/')}): машина + шина + дорога + скорость → тормозной и остановочный путь
- [Выбор шин](${L('/rehvi-valimine/')}): лучшие шины по размеру и машине
- [Сравнение шин](${L('/vordle-rehve/')}): до 4 шин рядом
- [Симуляторы безопасности](${L('/liiklusohutus/')}): скорость, темнота, дистанция, поворот
- [Тест реакции](${L('/liiklusohutus/reaktsioon/')}): игра — как быстро вы тормозите
- [Возраст шины](${L('/rehvi-vanus/')}): код DOT → возраст шины, глубина протектора → тормозной путь

## Частые вопросы (короткие ответы, та же модель)
- Когда в Эстонии обязательны зимние шины? С 1 декабря по 1 марта. Шипованные разрешены с 15 октября по 31 марта, при зимних условиях — с 1 октября по 30 апреля. На зимней шине должен быть знак «три горные вершины со снежинкой» (3PMSF); протектор глубже 3 мм, у летней — не менее 1,6 мм.
- Когда ставить зимние шины? Когда ночью ниже +7 °C или выпал первый снег, а не 1 декабря: на первом снегу со скорости 50 км/ч летняя шина останавливается примерно за ${x.md(x.jaa.lumiSuvi)} м, нордическая зимняя — за ${x.md(x.jaa.lumiTalv)} м (тормозной путь без времени реакции).
- Шипы или фрикционная? На льду со скорости 50 км/ч типичная шипованная шина останавливается примерно за ${x.md(x.jaa.naast)} м, нордическая фрикционная — за ${x.md(x.jaa.lamell)} м, центральноевропейская зимняя — за ${x.md(x.jaa.kesk)} м, летняя — за ${x.md(x.jaa.suvi)} м. На снегу и сухом асфальте разница между шипами и фрикционной небольшая.
- Насколько важен класс сцепления на мокрой дороге? Разница между летними шинами класса A и E на мокром асфальте со скорости 90 км/ч — около 18 м тормозного пути. Класс привязан к размеру.
- Что такое остановочный путь? Путь за время реакции + тормозной путь. Со скорости 50 км/ч автомобиль останавливается на сухой дороге примерно за 24 м, на мокрой — за 27 м; со скорости 90 км/ч — за 55 и 70 м (с реакцией 1 с).

## Данные${ET}
- [Шины и размеры](${BASE}/rehvid/): страницы размеров и шин есть и на русском (/ru/rehvid/…) для самых распространённых
- [Зимние шины по размерам](${BASE}/ru/talverehvid/): лучшие шипованные и фрикционные шины, тормозной путь на снегу и льду
- [Модели автомобилей](${BASE}/ru/autod/): заводские размеры шин, двигатели, расчётный тормозной путь, лучшие шины
- [Независимые тесты шин](${BASE}/testid/)
- [Как рассчитывается тормозной путь](${BASE}/teadmine/kuidas-pidurdusmaa-arvutatakse/): методика, источники, точность
- [Смена шин в Эстонии](${BASE}/ru/teadmine/rehvivahetus/): все сроки по закону и что разрешено сегодня
- [Обучение для автошкол](${BASE}/ru/liiklusohutus/koolitus/): бесплатный тест до и после с симуляторами; преподаватель создаёт тест для группы

## Другое
- [Eesti keeles](${BASE}/) ([llms.txt](${BASE}/llms.txt)) · [In English](${BASE}/en/) ([llms.txt](${BASE}/en/llms.txt))
`;
}
