/* Jagamispildid (og:image), tehakse ehituse ajal valmis:
 *   /og/sait/avaleht.png        üldine pilt (avaleht ja muud lehed)
 *   /og/m/205-55-r16.png        mõõdu leht
 *   /og/r/<rehv>.png            testitud rehvi leht
 *   /og/vs/<a>-vs-<b>.png       kahe rehvi võrdlus samas testis
 * Pilte tehakse ainult saidikaardis olevatele lehtedele — ülejäänud
 * kasutavad üldist pilti.
 */
import { error } from '@sveltejs/kit';
import { ogPilt } from '$lib/server/ogpilt.js';
import { autoNimi } from '$lib/i18n.js';
import { autod, polveLeht } from '$lib/server/autod.js';
import {
	core,
	models,
	sizeBySlug,
	sizeModelCount,
	SIZE_MIN_MODELS,
	eprelSize,
	tyrePage,
	rehviIndeks,
	vsPairs,
	sharedSources,
	source,
	num,
	KAT_NIMI
} from '$lib/server/andmed.js';

export const prerender = true;

export function entries() {
	const out = [{ liik: 'sait', slug: 'avaleht' }, { liik: 'sait', slug: 'liiklusohutus' }, { liik: 'sait', slug: 'peatumisteekonna-kalkulaator' }, { liik: 'sait', slug: 'talverehvide-testid-2026' }, { liik: 'sait', slug: 'millal-talverehvid-alla' }];
	for (const s of core().sizes) if (sizeModelCount(s.m) >= SIZE_MIN_MODELS) out.push({ liik: 'm', slug: s.slug });
	const rehvid = new Set([...Object.keys(models()), ...core().tyres.map((t) => t.slug).filter(Boolean)]);
	for (const slug of rehvid) if (rehviIndeks(slug).sitemap) out.push({ liik: 'r', slug });
	for (const [a, b] of vsPairs()) out.push({ liik: 'vs', slug: a + '-vs-' + b });
	for (const p of autod().polved.values()) out.push({ liik: 'auto', slug: p.mk + '--' + p.slug });
	/* vene/inglise lehtede pildid (vt ogLang $lib/i18n.js-is) */
	for (const x of ['liiklus-kurv', 'liiklus-pimedas', 'liiklus-pikivahe', 'liiklus-reaktsioon', 'rehvivahetus']) out.push({ liik: 'sait', slug: x });
	for (const k of ['ru', 'en']) for (const x of ['avaleht', 'liiklusohutus', 'liiklus-kurv', 'liiklus-pimedas', 'liiklus-pikivahe', 'liiklus-reaktsioon']) out.push({ liik: 'sait', slug: x + '.' + k });
	out.push({ liik: 'sait', slug: 'rehvivahetus.ru' });
	out.push({ liik: 'sait', slug: 'millal-talverehvid-alla.ru' });
	for (const p of autod().polved.values()) out.push({ liik: 'auto', slug: p.mk + '--' + p.slug + '.ru' });
	return out;
}

function lyhenda(s, n) {
	s = String(s);
	return s.length <= n ? s : s.slice(0, n - 1).trimEnd() + '…';
}
function vahemik(arr) {
	const u = [...new Set(arr.filter((x) => x !== null && x !== undefined && x !== ''))].sort((a, b) =>
		typeof a === 'number' ? a - b : String(a).localeCompare(String(b))
	);
	return !u.length ? '' : u.length === 1 ? String(u[0]) : u[0] + '–' + u[u.length - 1];
}
/* esimene mõõdetud märja asfaldi tulemus, muidu esimene üldse */
function mootmine(tested) {
	const x = tested.tests.find((t) => t.surf === 'ASPHALT' && t.wet) || tested.tests[0];
	if (!x) return '';
	const pind = x.surf === 'ASPHALT' ? (x.wet ? 'Märg' : 'Kuiv') : x.surf === 'CONCRETE' ? 'Märg betoon' : x.surf === 'ICE' ? 'Jää' : 'Lumi';
	const src = source(x.src) || {};
	const kes = src.tegija ? String(src.tegija).split(' (')[0] + ' ' + (src.aasta || '') : '';
	/* noolt → fondis ei ole — kirjutame sõnadega */
	const kiirus = x.v1 ? `${x.v0}–${x.v1} km/h` : `${x.v0} km/h pealt`;
	return `${pind}: ${kiirus} ${num(x.m)} m` + (kes ? ' · ' + kes.trim() : '');
}

function andmed(liik, slug) {
	if (liik === 'auto') {
		const p = autod().polved.get(String(slug).replace('--', '/'));
		if (!p) return null;
		const d = polveLeht(p);
		const m90 = d.pidurdus.find((x) => x.id === 'marg')?.r?.[90]?.peatumine;
		return {
			kicker: p.make,
			pealkiri: p.model + ' ' + p.yearLabel,
			alapealkiri: 'Rehvimõõt ' + d.pohimoot + (m90 ? ' · märjal 90 km/h pealt ~' + Math.round(m90) + ' m' : ''),
			sildid: [d.mootorid.length + (d.mootorid.length === 1 ? ' mootor' : ' mootorit'), 'Parimad rehvid', 'Pidurdusmaa']
		};
	}
	if (liik === 'sait' && slug === 'avaleht') {
		return {
			kicker: 'Pidurdusmaa kalkulaator',
			pealkiri: 'Kui kiiresti sinu auto peatub?',
			alapealkiri: 'Päris rehviandmed: EL-i märgis ja sõltumatud testid',
			sildid: [
				num(Object.keys(models()).length, 0) + ' rehvimudelit',
				num(core().vehicles.length, 0) + ' autot',
				'Tasuta'
			]
		};
	}
	if (liik === 'sait' && slug === 'millal-talverehvid-alla') {
		return {
			kicker: 'Talverehvid 2026/2027',
			pealkiri: 'Millal talverehvid alla?',
			alapealkiri: 'Naastrehvid 15.10, talverehvid kohustuslikud 1.12',
			sildid: ['Kuupäevad', '3 mm reegel', 'Pidurdusmaad']
		};
	}
	if (liik === 'sait' && slug === 'talverehvide-testid-2026') {
		return {
			kicker: 'Testid',
			pealkiri: 'Talverehvide testid 2025–2026',
			alapealkiri: 'Jääl üle kahe korra pikem pidurdusmaa',
			sildid: ['Mõõdetud meetrid', 'Jää, lumi, märg']
		};
	}
	if (liik === 'sait' && (slug === 'liiklusohutus' || slug === 'peatumisteekonna-kalkulaator')) {
		return {
			pilt: 'peatumine',
			kicker: slug === 'liiklusohutus' ? 'Liiklusohutus · peatumisteekond' : 'Uus tasuta kalkulaator',
			pealkiri: 'Kui pika maa pealt auto peatub?',
			alapealkiri: 'Kiirus, reaktsioon, tee ja rehvid',
			sildid: ['Kaks olukorda kõrvuti', 'Tasuta']
		};
	}
	if (liik === 'sait' && TEEMA[slug]) return TEEMA[slug].et;
	if (liik === 'm') {
		const s = sizeBySlug(slug);
		if (!s) return null;
		const rows = eprelSize(s.m);
		const a = rows.filter((r) => r[4] === 'A').length;
		return {
			kicker: 'Rehvimõõt',
			pealkiri: 'Rehvid ' + s.label,
			alapealkiri: rows.length + ' rehvimudelit EL-i märgise andmetega',
			sildid: [a ? a + ' A-klassi märjal' : '', 'Võrdle pidurdusmaad']
		};
	}
	if (liik === 'r') {
		const t = tyrePage(slug);
		if (!t || !rehviIndeks(slug).sitemap) return null;
		const sizes = t.model ? t.model.sizes : [];
		const g = vahemik(sizes.map((z) => z.g));
		const db = vahemik(sizes.map((z) => z.db));
		return {
			kicker: (KAT_NIMI[t.cat] || 'Rehv') + (t.tested ? ' · sõltumatult testitud' : ''),
			pealkiri: t.name,
			alapealkiri: lyhenda(t.tested ? mootmine(t.tested) : '', 54),
			sildid: [g ? 'Märghaare ' + g : '', db ? 'Müra ' + db + ' dB' : '', sizes.length ? sizes.length + ' mõõtu' : '']
		};
	}
	if (liik === 'vs') {
		const m = /^(.+)-vs-(.+)$/.exec(slug);
		if (!m) return null;
		const a = tyrePage(m[1]);
		const b = tyrePage(m[2]);
		const shared = a && b ? sharedSources(a, b) : [];
		if (!shared.length) return null;
		const src = source(shared[0]) || {};
		return {
			kicker: 'Mõõdetud samas testis',
			pealkiri: a.name + ' vs ' + b.name,
			alapealkiri: lyhenda(src.nimi || '', 54),
			sildid: ['Sama auto, sama päev']
		};
	}
	return null;
}

/* Tööriistade ja teemalehtede pildid: oma pealkiri ja teemajoonis paremal */
const AASTA = (() => { const d = new Date(); return d.getMonth() + 1 >= 5 ? d.getFullYear() : d.getFullYear() - 1; })();
const TEEMA = {
	'liiklus-kurv': {
		et: { pilt: 'kurv', kicker: 'Liiklusohutus · kurv', pealkiri: 'Pidurdamine kurvis', alapealkiri: 'Paremad rehvid ees või taga?', sildid: ['Animatsioon', '92 olukorda'] },
		ru: { pilt: 'kurv', kicker: 'Безопасность · поворот', pealkiri: 'Торможение в повороте', alapealkiri: 'Лучшие шины спереди или сзади?', sildid: ['Анимация', '92 ситуации'] },
		en: { pilt: 'kurv', kicker: 'Road safety · bends', pealkiri: 'Braking in a bend', alapealkiri: 'Better tyres on the front or rear?', sildid: ['Animation', '92 scenarios'] }
	},
	'liiklus-pimedas': {
		et: { pilt: 'pimedas', kicker: 'Liiklusohutus · pimedas', pealkiri: 'Kas jõuad jalakäija ees peatuda?', alapealkiri: 'Helkur, tumedad riided, kaugtuled', sildid: ['Ohutu kiirus', 'Tasuta'] },
		ru: { pilt: 'pimedas', kicker: 'Безопасность · темнота', pealkiri: 'Успеете остановиться перед пешеходом?', alapealkiri: 'Световозвращатель, тёмная одежда', sildid: ['Безопасная скорость', 'Бесплатно'] },
		en: { pilt: 'pimedas', kicker: 'Road safety · darkness', pealkiri: 'Can you stop for the pedestrian?', alapealkiri: 'Reflector, dark clothes, high beam', sildid: ['Safe speed', 'Free'] }
	},
	'liiklus-pikivahe': {
		et: { pilt: 'pikivahe', kicker: 'Liiklusohutus · pikivahe', pealkiri: 'Kas 2 sekundit on piisav?', alapealkiri: 'Kui eesolev auto järsult pidurdab', sildid: ['1–4 sekundit', 'Tasuta'] },
		ru: { pilt: 'pikivahe', kicker: 'Безопасность · дистанция', pealkiri: 'Хватит ли 2 секунд?', alapealkiri: 'Если машина впереди резко тормозит', sildid: ['1–4 секунды', 'Бесплатно'] },
		en: { pilt: 'pikivahe', kicker: 'Road safety · following distance', pealkiri: 'Is 2 seconds enough?', alapealkiri: 'When the car ahead brakes hard', sildid: ['1–4 seconds', 'Free'] }
	},
	'liiklus-reaktsioon': {
		et: { pilt: 'pikivahe', kicker: 'Liiklusohutus · mäng', pealkiri: 'Kui kiiresti SINA pidurdad?', alapealkiri: 'Testi oma reaktsiooni', sildid: ['3 katset', 'Jaga sõpradega'] },
		ru: { pilt: 'pikivahe', kicker: 'Безопасность · игра', pealkiri: 'Как быстро ВЫ тормозите?', alapealkiri: 'Проверьте свою реакцию', sildid: ['3 попытки', 'Поделитесь'] },
		en: { pilt: 'pikivahe', kicker: 'Road safety · game', pealkiri: 'How fast do YOU brake?', alapealkiri: 'Test your reaction', sildid: ['3 tries', 'Share'] }
	},
	rehvivahetus: {
		et: { pilt: 'kalender', kicker: 'Rehvivahetus ' + AASTA, pealkiri: 'Millal talverehvid alla?', alapealkiri: 'Talverehvid kohustuslikud 1.12–1.03', sildid: ['Naast 15.10–31.03', 'Seadus'] },
		ru: { pilt: 'kalender', kicker: 'Смена резины ' + AASTA, pealkiri: 'Когда ставить зимние шины?', alapealkiri: 'Зимние шины обязательны 1.12–1.03', sildid: ['Шипы 15.10–31.03', 'Закон'] }
	}
};

/* Vene/inglise tekstid (ainult pildid, mida vene/inglise lehed kasutavad) */
function andmedKeel(liik, slug, lang) {
	const ru = lang === 'ru';
	if (liik === 'sait' && TEEMA[slug]) return TEEMA[slug][lang] || null;
	if (liik === 'auto') {
		const p = autod().polved.get(String(slug).replace('--', '/'));
		if (!p) return null;
		const d = polveLeht(p);
		const m90 = d.pidurdus.find((x) => x.id === 'marg')?.r?.[90]?.peatumine;
		const n = d.mootorid.length;
		return ru
			? { kicker: p.make, pealkiri: autoNimi('ru', p.model + ' ' + p.yearLabel),
				alapealkiri: 'Размер шин ' + d.pohimoot + (m90 ? ' · на мокрой дороге с 90 км/ч ~' + Math.round(m90) + ' м' : ''),
				sildid: ['Двигателей: ' + n, 'Лучшие шины', 'Тормозной путь'] }
			: null;
	}
	if (liik === 'sait' && slug === 'avaleht') {
		const nR = num(Object.keys(models()).length, 0), nA = num(core().vehicles.length, 0);
		return ru
			? { kicker: 'Калькулятор тормозного пути', pealkiri: 'Как быстро остановится ваш автомобиль?',
				alapealkiri: 'Реальные данные шин: маркировка ЕС и независимые тесты', sildid: [nR + ' моделей шин', nA + ' авто', 'Бесплатно'] }
			: { kicker: 'Braking distance calculator', pealkiri: 'How quickly does your car stop?',
				alapealkiri: 'Real tyre data: EU label and independent tests', sildid: [nR.replace(/\s/g, ',') + ' tyre models', nA.replace(/\s/g, ',') + ' cars', 'Free'] };
	}
	if (liik === 'sait' && slug === 'millal-talverehvid-alla' && ru) {
		return { kicker: 'Зимние шины 2026/2027', pealkiri: 'Когда менять шины на зимние?',
			alapealkiri: 'Шипы с 15.10, зимние шины обязательны с 1.12', sildid: ['Сроки', 'Правило 3 мм', 'Тормозной путь'] };
	}
	if (liik === 'sait' && slug === 'liiklusohutus') {
		return ru
			? { pilt: 'peatumine', kicker: 'Безопасность · остановочный путь', pealkiri: 'С какого расстояния остановится автомобиль?',
				alapealkiri: 'Скорость, реакция, дорога и шины', sildid: ['Две ситуации рядом', 'Бесплатно'] }
			: { pilt: 'peatumine', kicker: 'Road safety · stopping distance', pealkiri: 'How far does it take a car to stop?',
				alapealkiri: 'Speed, reaction, road and tyres', sildid: ['Two scenarios side by side', 'Free'] };
	}
	return null;
}

export async function GET({ params }) {
	/* Anna sündmuste tsüklile hetk: resvg vabastab eelmiste piltide mälu (≈3 MB
	   pildi kohta) alles siis — muidu jookseb ~2000 pildiga ehitus mälust välja */
	await new Promise((r) => setImmediate(r));
	const k = /\.(ru|en)$/.exec(params.slug);
	const d = k ? andmedKeel(params.liik, params.slug.slice(0, -3), k[1]) : andmed(params.liik, params.slug);
	if (!d) error(404, 'Pilti ei ole');
	return new Response(ogPilt(d), {
		headers: { 'Content-Type': 'image/png', 'Cache-Control': 'public, max-age=86400' }
	});
}
