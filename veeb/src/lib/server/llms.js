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
function pidurdus(o, r) {
	const x = arvuta({ a: 'vw_golf_8', ab: false, m: '20555R16', o, v: 90, r, mm: null, rt: 0, l: 'et' });
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
	const allikad = Object.values(c.sources || {})
		.map((s) => (s.aasta && !String(s.nimi).includes(String(s.aasta)) ? `${s.nimi} ${s.aasta}` : s.nimi))
		.sort()
		.join(', ');
	const nMud = n(Object.keys(models()).length), nMoot = n(c.eprelSizes.filter((m) => /^\d{5}R\d{2}C?$/.test(m)).length) /* ainult päris mõõdud (audit: ~690 võtit on nimest valesti loetud) */, nTest = n(c.tyres.length), nAuto = n(autod().polved.size);
	const md = lang === 'et' ? m : (x) => (Math.round(x * 10) / 10).toString().replace('.', lang === 'en' ? '.' : ',');
	if (lang === 'en' || lang === 'ru') return valisKeel(lang, { kuiv, marg, lumi, reakts, allikad, nMud, nMoot, nTest, nAuto, md });
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
- [Rehvi vanus](${BASE}/rehvi-vanus/): DOT-kood → rehvi vanus, mustri sügavus → pidurdusmaa

## Andmed
- [Rehvid ja mõõdud](${BASE}/rehvid/)
- [Automudelid](${BASE}/autod/)
- [Sõltumatud rehvitestid](${BASE}/testid/)

## Teadmised
- [Kuidas pidurdusmaa arvutatakse](${BASE}/teadmine/kuidas-pidurdusmaa-arvutatakse/): metoodika, allikad, täpsus
- [Pidurdusteekond ja peatumisteekond](${BASE}/teadmine/pidurdusteekond-ja-peatumisteekond/)
- [EL-i rehvimärgis](${BASE}/teadmine/rehvimargis/)
- [Rehvivahetuse ajad Eestis](${BASE}/teadmine/rehvivahetus/)
${artiklid}

## Muu
- [Meist](${BASE}/meist/): kes teeb, andmeallikad, sõltumatus
- [Partnerid ja poelingid](${BASE}/teadmine/partnerid/)
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

## Данные${ET}
- [Шины и размеры](${BASE}/rehvid/)
- [Модели автомобилей](${BASE}/ru/autod/)
- [Независимые тесты шин](${BASE}/testid/)
- [Как рассчитывается тормозной путь](${BASE}/teadmine/kuidas-pidurdusmaa-arvutatakse/): методика, источники, точность
- [Смена шин в Эстонии](${BASE}/ru/teadmine/rehvivahetus/)

## Другое
- [Eesti keeles](${BASE}/) ([llms.txt](${BASE}/llms.txt)) · [In English](${BASE}/en/) ([llms.txt](${BASE}/en/llms.txt))
`;
}
