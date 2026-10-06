/* Jagatud tulemus (/jaga/?…): pidurdusmaa arvutatakse SERVERIS uuesti sama
 * mootoriga (engine.js) ja samade reeglitega kui kalkulaatori tulemus
 * (app.js rowsFor). Lingis on ainult valikud (auto, mõõt, kiirus, olud,
 * rehv, muster, reaktsioon) — mitte number. Nii ei saa keegi jagada
 * võltsitud tulemust Pidurdusmaa nime all: number on alati mudeli oma.
 *
 * Rehvi kirjeldus `r`:
 *   t:<testvõti>        sõltumatult testitud rehv
 *   c:<KAT><G>          EL-i märgise klass (märjal), nt c:SUMMER_TOURINGB
 *   k:<KAT>             kategooria keskmine (kuiv/lumi/jää)
 *   e:<eprelSlug>       klassist valitud konkreetne rehv
 *   o:e:<slug> | o:t:<võti>   sinu rehv (koos mustriga mm)
 *   g:<KAT><G>          „sinu rehvid praegu“ — tüüpiline, ainult mustriga
 * Tundmatu või vigane valik → null (leht ütleb, et tulemust ei saa näidata).
 */
import '$lib/engine.js';
import { core, eprelSize, pretty, titleCase } from './andmed.js';
import RU from '$lib/i18n/ru.js';
import EN from '$lib/i18n/en.js';

const P = () => globalThis.Pidurdus;
const SONAD = { ru: RU, en: EN };
export const tJ = (l, s) => (l !== 'et' && SONAD[l] && SONAD[l][s]) || s;

const GNOM = { A: 1.6, B: 1.47, C: 1.32, D: 1.17, E: 1.05 };
const KATID = ['SUMMER_UHP', 'SUMMER_TOURING', 'ALL_SEASON', 'WINTER_CENTRAL', 'WINTER_NORDIC', 'WINTER_STUDDED'];
const EKAT = ['SUMMER_TOURING', 'ALL_SEASON', 'WINTER_CENTRAL', 'WINTER_NORDIC'];
const CATNAME = {
	SUMMER_UHP: 'Suverehv (sportlik)', SUMMER_TOURING: 'Suverehv', ALL_SEASON: 'Aastaringne rehv',
	WINTER_CENTRAL: 'Talverehv (Kesk-Euroopa)', WINTER_NORDIC: 'Talverehv (Põhjamaade)', WINTER_STUDDED: 'Naastrehv'
};
/* sama tabel mis app.js COND */
const COND = {
	wet: { surface: 'ASPHALT', waterMm: 1.0, tempC: 10, label: 'märg asfalt', lyh: 'Märg asfalt' },
	dry: { surface: 'ASPHALT', waterMm: 0.0, tempC: 15, label: 'kuiv asfalt', lyh: 'Kuiv asfalt' },
	snow: { surface: 'SNOW_PACKED', waterMm: 0.0, tempC: -5, label: 'tallatud lumi', lyh: 'Tallatud lumi' },
	ice: { surface: 'ICE', waterMm: 0.0, tempC: -5, label: 'jää', lyh: 'Jää' }
};
const DEFAULT_VEH = 'vw_golf_8';

function gmid(g, cat) {
	const t = (core().gClass || {})[g];
	if (t) {
		if (cat && t[cat]) return t[cat][0];
		if (t._ && t._[1]) return t._[0];
	}
	return GNOM[g];
}
const baasRehv = (o) => ({ treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: false, gSource: 'label', ...o });
const classTyre = (g, cat, m) => baasRehv({ key: 'c:' + g + cat, name: 'Klass ' + g, category: cat, wetGripIndex: gmid(g, cat), size: pretty(m) });
const eprelTyre = (r) => baasRehv({ key: 'e:' + r.slug + '@' + r.m, name: r.mark + ' ' + r.name, category: r.cat, wetGripIndex: gmid(r.g, r.cat) || gmid('C', r.cat), size: pretty(r.m) });
const onCar = (t, m) => ({ ...t, size: pretty(m), gSize: t.gSize || t.size });
function kulunud(t, mm) {
	if (!mm) return t;
	const uus = t.treadDepthNewMm || 8;
	return { ...t, treadDepthNewMm: uus, treadDepthMm: Math.min(mm, uus) };
}
const moodetud = (t, ck) => ck === 'wet' || (ck === 'dry' ? t.muDry != null : ck === 'snow' ? t.muSnow != null : t.muIce != null);

let _idx = null;
function idx() {
	if (_idx) return _idx;
	const c = core();
	const veh = new Map(c.vehicles.map((v) => [v.key, v]));
	for (const [a, b] of Object.entries(c.vehAlias || {})) if (veh.has(b)) veh.set(a, veh.get(b));
	_idx = { veh, tyre: new Map(c.tyres.map((t) => [t.key, t])) };
	return _idx;
}

/* mootori variant (<rida>~<mootor>): sama loogika mis app.js laeMootorid */
function autoLeia(key, mootorid) {
	const { veh } = idx();
	if (!key) return null;
	if (veh.has(key)) return veh.get(key);
	const [rida, moot] = String(key).split('~');
	const v = veh.get(rida);
	if (!v || !moot || !mootorid) return null;
	const e = (mootorid[rida] || []).find((x) => x[3] === moot);
	if (!e) return null;
	const x = { ...v, key: v.key + '~' + e[3], variant: e[0], name: [v.make.split(' /')[0], v.model, v.gen, e[0].split(' · ')[0]].filter(Boolean).join(' ') + ' (' + (e[2] || v.years) + ')' };
	const o = e[5];
	if (o) {
		if (o.m) x.kerbMassKg = o.m;
		if (o.s) { x.oemSizes = o.s; x.oemSize = o.o || o.s[0]; }
	}
	return x;
}

function eprelRead(m) {
	return eprelSize(m).map((r) => ({ slug: r[0], mark: titleCase(r[1]), name: titleCase(r[2]), cat: EKAT[r[3]], catNr: r[3], g: r[4], tested: r[9], m }));
}

/** URL-i parameetrid → puhastatud valik (või null). */
export function loeValik(q) {
	const s = (k) => String(q.get(k) || '').slice(0, 120);
	const m = s('m').toUpperCase();
	if (!/^\d{3}\d{2}R\d{2}C?$/.test(m)) return null;
	const o = s('o');
	if (!COND[o]) return null;
	const v = Math.round(+s('v'));
	if (!(v >= 20 && v <= 130)) return null;
	const r = s('r');
	if (!/^(t:[\w.-]+|c:[A-Z_]+[A-E]|k:[A-Z_]+|e:[\w.-]+|o:[et]:[\w.-]+|g:[A-Z_]+[A-E])$/.test(r)) return null;
	let mm = s('mm') ? Math.round(+s('mm') * 10) / 10 : null;
	if (mm != null && !(mm >= 1.6 && mm <= 8)) mm = null;
	if (mm === 8) mm = null;
	let rt = s('rt') ? +s('rt') : 0;
	if (!(rt >= 0 && rt <= 3)) rt = 0;
	rt = Math.round(rt * 10) / 10; /* piiratud arv variante → piltide vahemälu toimib */
	const a = s('a');
	const l = ['et', 'ru', 'en'].includes(s('l')) ? s('l') : 'et';
	return { a: /^[\w~.-]+$/.test(a) ? a : '', ab: s('ab') === '1', m, o, v, r, mm, rt, l };
}

/** Valik → tulemus. mootorid = mootoridJson() (ainult kui auto võtmes on ~). */
export function arvuta(val, mootorid) {
	if (!val) return null;
	const { tyre: TY } = idx();
	const l = val.l;
	let veh = autoLeia(val.a, mootorid);
	const vaikimisi = !veh;
	if (!veh) veh = idx().veh.get(DEFAULT_VEH);
	if (!veh) return null;
	if (val.ab && veh.absOpt) veh = { ...veh, ...veh.absOpt };
	const ck = val.o, C = COND[ck];
	const cond = { speedKmh: val.v, surface: C.surface, texture: 'NORMAL', waterMm: C.waterMm, tempC: C.tempC, payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1 };
	const m = val.m, mm = val.mm;
	const [liik, ...jupp] = val.r.split(':');
	const id = jupp.join(':');
	let tyre = null, nimi = '', alla = '', oma = false;
	if (liik === 't') {
		const t = TY.get(id);
		if (!t || !moodetud(t, ck)) return null;
		tyre = onCar(t, m);
		nimi = t.name;
		alla = tJ(l, 'Sõltumatu test');
	} else if (liik === 'c' || liik === 'g') {
		const g = id.slice(-1), cat = id.slice(0, -1); /* sama kuju mis kalkulaatori rea id: c:<KAT><G> */
		if (!GNOM[g] || !EKAT.includes(cat)) return null;
		if (liik === 'c' && ck !== 'wet') return null;
		tyre = classTyre(g, cat, m);
		if (liik === 'g') {
			if (!mm) return null;
			tyre = kulunud(tyre, mm);
			nimi = tJ(l, 'Sinu rehvid praegu');
			alla = tJ(l, CATNAME[cat]) + (ck === 'wet' ? ' · ' + tJ(l, 'märgise klass ') + g : '');
			oma = true;
		} else {
			nimi = tJ(l, 'Märgise klass ') + g;
			alla = tJ(l, CATNAME[cat]);
		}
	} else if (liik === 'k') {
		if (!KATID.includes(id) || ck === 'wet') return null;
		tyre = classTyre('C', id, m);
		nimi = tJ(l, CATNAME[id]);
		alla = tJ(l, 'kategooria keskmine');
	} else if (liik === 'e') {
		const r = eprelRead(m).find((x) => x.slug === id);
		if (!r) return null;
		const t = r.tested ? TY.get(r.tested) : null;
		if (t && moodetud(t, ck)) {
			tyre = onCar(t, m);
			alla = tJ(l, 'Sõltumatu test');
		} else {
			if (ck !== 'wet') return null; /* märgis ei ütle kuiva/lume/jää kohta midagi */
			tyre = classTyre(r.g, r.cat, m);
			alla = tJ(l, 'märgise klass ') + r.g;
		}
		nimi = r.mark + ' ' + r.name;
	} else if (liik === 'o') {
		const [ol, ov] = [jupp[0], jupp.slice(1).join(':')];
		let r = null, t = null;
		if (ol === 'e') {
			r = eprelRead(m).find((x) => x.slug === ov);
			if (!r) return null;
			t = r.tested ? TY.get(r.tested) : null;
		} else {
			t = TY.get(ov);
			if (!t) return null;
			r = eprelRead(m).find((x) => x.tested === t.key) || null;
		}
		const mt = t && moodetud(t, ck);
		/* märgisega rehv kuival/lumel/jääl: muDry/muSnow/muIce puudub → rehvitüübi keskmine (nagu kalkulaatoris) */
		const base = mt ? onCar(t, m) : r ? eprelTyre(r) : { ...t, muDry: null, muSnow: null, muIce: null };
		tyre = kulunud(base, mm);
		nimi = r ? r.mark + ' ' + r.name : t.name;
		alla = tJ(l, 'Sinu rehv') + (mt ? ' · ' + tJ(l, 'Sõltumatu test') : '');
		oma = true;
	}
	if (!tyre) return null;
	let x;
	try {
		x = P().stoppingDistance(tyre, veh, cond);
	} catch {
		return null;
	}
	if (!x || !(x.distanceM > 0) || !isFinite(x.distanceM)) return null;
	const react = val.rt ? (val.v / 3.6) * val.rt : 0;
	return {
		d: x.distanceM + react, pidur: x.distanceM, react, lo: x.lowM + react, hi: x.highM + react,
		stop: !!val.rt, rt: val.rt, v: val.v, ck, olu: tJ(l, C.lyh),
		auto: vaikimisi ? 'VW Golf 8' : veh.name, autoVaikimisi: vaikimisi,
		moot: pretty(m), rehv: nimi, alla, mm: oma ? mm : null, oma, l
	};
}

/** Kalkulaatori link samade valikutega (CTA „Arvuta oma auto“). */
/* „Arvuta oma auto ja rehvidega“: PUHAS avaleht. Jagaja auto ja mõõt ei
   tohi järgmisele inimesele ette tulla — ta tahab oma autot (Tarvo 6.10). */
export function kalkLink(val) {
	return val.l === 'et' ? '/' : '/' + val.l + '/';
}

/* ---------------------------------------------------------------- pilt */
import { svgPng, svgEsc as esc, mootLaius } from './ogpilt.js';

const nf = (l, x) => x.toLocaleString(l === 'en' ? 'en-GB' : l === 'ru' ? 'ru-RU' : 'et-EE', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
/* lühenda pikk tekst ~n märgini */
const lyh = (s, n) => (String(s).length > n ? String(s).slice(0, n - 1).trimEnd() + '…' : String(s));

/** 1200×630 PNG: suur number, rehv, auto; paremal tee, kus pidurdusjälg on number meetrites skaalas. */
export function jagaPilt(res) {
	const l = res.l, K = '#ffc20e';
	const pealkiri = (res.stop ? tJ(l, 'Peatumisteekond') : tJ(l, 'Pidurdusteekond')) + ' ' + res.v + '–0 ' + (l === 'ru' ? 'км/ч' : 'km/h'); /* noolt (→) pildi fontides pole */
	const kick = pealkiri + ' · ' + res.olu;
	const kickPx = kick.length > 44 ? 20 : kick.length > 38 ? 23 : 26;
	const num = nf(l, res.d);
	const numPx = num.length > 5 ? 190 : 210;
	/* ühik eraldi tekstina, et kirillitsa „м“ ei vahetaks numbri fonti */
	const numW = mootLaius(num, 'Barlow Condensed', 700, numPx) + 22;
	/* tee paremal: 0…max m, jälg skaalas (lumi/jää võivad olla pikad) */
	const maxM = Math.max(60, Math.ceil(res.d / 20) * 20);
	const y0 = 560, y1 = 70, k = (y0 - y1) / maxM;
	const yAuto = y0 - res.d * k;
	const yReact = y0 - res.react * k;
	const marke = [];
	for (let m = 0; m <= maxM; m += maxM > 120 ? 40 : 20) marke.push(`<path d="M1062 ${y0 - m * k} H1074" stroke="#5d6672" stroke-width="2"/><text x="1084" y="${y0 - m * k + 8}" font-family="Inter" font-weight="500" font-size="22" fill="#8b929e">${m}</text>`);
	const pinnaVarv = res.ck === 'snow' ? '#aab3bf' : res.ck === 'ice' ? '#bcd4e6' : res.ck === 'wet' ? '#1c222b' : '#30353e';
	const read = [
		[lyh(res.rehv, 34), '#ffffff', 34, 800],
		[lyh(res.alla + (res.mm ? ' · ' + tJ(l, 'muster') + ' ' + String(res.mm).replace('.', l === 'en' ? '.' : ',') + ' mm' : ''), 52), '#c9ced6', 24, 500],
		[lyh(res.auto, 44) + ' · ' + res.moot, '#c9ced6', 24, 500]
	];
	const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="#0a0b0d"/>
<rect x="890" y="0" width="150" height="630" fill="${pinnaVarv}"/>
<path d="M965 0 V630" stroke="${res.ck === 'snow' || res.ck === 'ice' ? '#ffffff' : '#f3f4f6'}" stroke-width="4" stroke-dasharray="26 30" opacity="${res.ck === 'snow' ? 0.25 : 0.5}"/>
${marke.join('')}
<path d="M900 ${y0} H1030" stroke="${K}" stroke-width="4" stroke-dasharray="10 6"/>
${res.react > 0 ? `<path d="M965 ${y0} V${yReact}" stroke="${K}" stroke-width="8" stroke-linecap="round" opacity=".9"/>` : ''}
<path d="M944 ${yReact} V${yAuto + 70}" stroke="#e5484d" stroke-width="8" stroke-linecap="round"/>
<path d="M986 ${yReact} V${yAuto + 70}" stroke="#e5484d" stroke-width="8" stroke-linecap="round"/>
<g transform="translate(965 ${yAuto})">
  <rect x="-25" y="0" width="50" height="92" rx="13" fill="${K}" stroke="#171200" stroke-width="3"/>
  <path d="M-18 24 Q0 10 18 24 L16 36 Q0 28 -16 36Z" fill="#26303b"/>
  <rect x="-19" y="84" width="12" height="5" rx="2" fill="#ff2d2d"/><rect x="7" y="84" width="12" height="5" rx="2" fill="#ff2d2d"/>
</g>
<g transform="translate(70 96) skewX(-10)"><text x="0" y="0" font-family="Inter" font-weight="800" font-size="38" fill="#ffffff">PIDURDUSMAA<tspan fill="${K}">.ee</tspan></text></g>
<text x="70" y="168" font-family="Inter" font-weight="500" font-size="${kickPx}" letter-spacing="${kickPx > 22 ? 2 : 1}" fill="${K}">${esc((pealkiri + ' · ' + res.olu).toUpperCase())}</text>
<text x="62" y="${168 + numPx * 0.88}" font-family="Barlow Condensed" font-weight="700" font-size="${numPx}" fill="#ffffff">${esc(num)}</text>
<text x="${62 + numW}" y="${168 + numPx * 0.88}" font-family="${l === 'ru' ? 'Roboto Condensed' : 'Barlow Condensed'}" font-weight="700" font-size="${Math.round(numPx * 0.42)}" fill="#c9ced6">${l === 'ru' ? 'м' : 'm'}</text>
${read.map(([t, c, px, w], i) => `<text x="70" y="${448 + i * 44 + (i ? 4 : 0)}" font-family="Inter" font-weight="${w}" font-size="${px}" fill="${c}">${esc(t)}</text>`).join('')}
<text x="70" y="590" font-family="Inter" font-weight="500" font-size="22" fill="#8b929e">${esc(tJ(l, 'Arvuta oma auto ja rehvidega → pidurdusmaa.ee').replace(' → ', ' — '))}</text>
<rect x="0" y="616" width="1200" height="14" fill="${K}"/>
</svg>`;
	return svgPng(svg, 1200);
}

/** Mõõdulehe KKK: sama auto pidurdusmaa märjal 80 km/h pealt selle mõõdu
 *  parima ja halvima märgise klassiga (samas rehvitüübis). Sama mootor ja
 *  samad klassi väärtused mis kalkulaatoris. null, kui klasse on alla kahe. */
export function klassiVahe(m, autoKey) {
	const read = eprelRead(m).filter((r) => GNOM[r.g]);
	if (!read.length) return null;
	const kat = Object.entries(read.reduce((o, r) => ((o[r.cat] = (o[r.cat] || 0) + 1), o), {})).sort((a, b) => b[1] - a[1])[0][0];
	const kl = [...new Set(read.filter((r) => r.cat === kat).map((r) => r.g))].sort();
	if (kl.length < 2) return null;
	const { veh } = idx();
	const v = (autoKey && veh.get(autoKey)) || veh.get(DEFAULT_VEH);
	if (!v) return null;
	const C = COND.wet;
	const cond = { speedKmh: 80, surface: C.surface, texture: 'NORMAL', waterMm: C.waterMm, tempC: C.tempC, payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1 };
	const d = (g) => Math.round(P().stoppingDistance(classTyre(g, kat, m), v, cond).distanceM * 10) / 10;
	const g1 = kl[0], g2 = kl[kl.length - 1], d1 = d(g1), d2 = d(g2);
	return { kat, g1, g2, d1, d2, vahe: Math.round((d2 - d1) * 10) / 10, auto: v.name.replace(/\s*\(.*\)$/, ''), autoKey: v.key };
}

/** Autolehtede sissejuhatus: pidurdusmaa märjal asfaldil 80 km/h pealt
 *  keskmise suverehviga (märgise klass C) auto enda tehase põhimõõdus. */
export function marg80(autoKey) {
	const v = idx().veh.get(autoKey);
	if (!v || !v.oemSize) return null;
	const m = String(v.oemSize).replace(/[/ ]/g, '').toUpperCase();
	const C = COND.wet;
	const cond = { speedKmh: 80, surface: C.surface, texture: 'NORMAL', waterMm: C.waterMm, tempC: C.tempC, payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1 };
	try {
		const d = P().stoppingDistance(classTyre('C', 'SUMMER_TOURING', m), v, cond).distanceM;
		return Number.isFinite(d) ? Math.round(d * 10) / 10 : null;
	} catch {
		return null;
	}
}
