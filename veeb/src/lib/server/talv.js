/* „Parimad talverehvid <mõõt>“ lehed (/talverehvid/<mõõt>/).
 *
 * Üks leht Eesti levinumate rehvimõõtude kohta. Kõik numbrid on samast
 * andmestikust ja samast mootorist kui kalkulaator:
 *   - testitud talverehvid (core.json tyres[].tests) — pidurdusmaa lumel ja
 *     jääl arvutatakse ehituse ajal selle mõõdu tüüpilise autoga;
 *   - Põhjamaade lamellrehvid EL-i märgise järgi (eprel/<mõõt>.json);
 *   - autod, mille tehase põhimõõt see on (autod.js).
 * Naastrehvidel ELi märgist ei ole — need tulevad ainult testidest ja
 * nende saadavust konkreetses mõõdus me ei tea (lehel on see öeldud).
 */
import '$lib/engine.js';
import { core, eprelSize, pretty, sizeSlug, titleCase, sizeModelCount, SIZE_MIN_MODELS, extTests, testidMoodus } from './andmed.js';
import { autodMoodus, autod as autodIdx, kaasMoot } from './autod.js';

const P = () => globalThis.Pidurdus;
/* talverehvide lehtede sisu viimati üle vaadatud (nähtav „uuendatud“ ja dateModified) */
export const TALV_UUENDATUD = '2026-10-18';
const FLAG = { SNOW: 4, ICE: 8 };
/* EPREL-i kategooria number (andmed.js eprelSize: katNr) */
const KAT = { SUVI: 0, AASTARING: 1, KESK: 2, POHJA: 3 };

/** Mõõdud, millele leht tehakse.
 *  1. järk: vähemalt 3 autot, mille PÕHImõõt see on, ja vähemalt 8 Põhjamaade talverehvi
 *     märgise andmetega; 40 levinumat. Enim autosid ees.
 *  2. järk (18.10): levinud lisamõõdud (225/45 R17, 225/40 R18, 205/50 R17 …), mis on vähemalt
 *     10 automudeli tehasemõõt, aga harva põhimõõt; vähemalt 20 Põhjamaade lamellrehvi ja oma
 *     mõõduleht. `lisa: true`, autosid = kõik autod, millel see on tehasemõõt. */
let _moodud = null;
/* Kõik kunagi avaldatud lehed. Aadress ei tohi kaduda, kui autode andmete muutudes mõõtude
   järjekord muutub (215/70 R16 oli korra avaldatud, kukkus välja ja andis Google'is 404). */
const AVALDATUD = new Set(('175-65-r14 175-65-r15 175-70-r13 175-70-r14 185-60-r15 185-65-r14 185-65-r15 185-70-r14 195-55-r16 ' +
	'195-60-r15 195-65-r15 205-55-r16 205-60-r16 205-70-r15 215-55-r16 215-55-r17 215-55-r18 215-60-r16 215-60-r17 215-65-r16 ' +
	'215-65-r17 225-50-r17 225-55-r16 225-55-r17 225-55-r18 225-55-r19 225-60-r17 225-60-r18 225-65-r17 235-50-r19 235-55-r17 ' +
	'235-55-r18 235-55-r19 235-60-r18 235-65-r17 235-65-r18 245-45-r18 255-55-r18 255-55-r19 265-60-r18 ' +
	'155-70-r13 165-70-r14 205-65-r15 215-70-r16').split(' '));
export function talveMoodud() {
	if (_moodud) return _moodud;
	const out = [], lisa = [];
	for (const s of core().sizes) {
		const koik = autodMoodus(s.m);
		const autod = koik.filter((c) => c.pohi);
		const pohja = eprelSize(s.m).filter((r) => r[3] === KAT.POHJA).length;
		const x = { m: s.m, slug: sizeSlug(s.m), label: pretty(s.m), autosid: autod.length, pohja };
		if (autod.length >= 3 && pohja >= 8) out.push(x);
		else if (koik.length >= 10 && pohja >= 20 && sizeModelCount(s.m) >= SIZE_MIN_MODELS) lisa.push({ ...x, autosid: koik.length, lisa: true });
		else if (AVALDATUD.has(x.slug) && koik.length && pohja >= 8) lisa.push({ ...x, autosid: koik.length, lisa: true });
	}
	out.sort((a, b) => b.autosid - a.autosid || b.pohja - a.pohja);
	const pohi = out.filter((x, i) => i < 40 || AVALDATUD.has(x.slug));
	const onPohi = new Set(pohi.map((x) => x.slug));
	/* 1. järgu mõõdud, mis jäid 40 hulgast välja, aga vastavad 2. järgu tingimustele, tulevad lisana */
	const valja = out.filter((x) => !onPohi.has(x.slug) && x.pohja >= 20 && autodMoodus(x.m).length >= 10 && sizeModelCount(x.m) >= SIZE_MIN_MODELS)
		.map((x) => ({ ...x, autosid: autodMoodus(x.m).length, lisa: true }));
	_moodud = [...pohi, ...[...lisa, ...valja].sort((a, b) => b.autosid - a.autosid || b.pohja - a.pohja)];
	return _moodud;
}

export function talveMoot(slug) {
	return talveMoodud().find((x) => x.slug === slug) || null;
}

/* Tüüpiline auto selle mõõduga: põhimõõduga põlvkondadest keskmise massiga
   (mediaan) — mitte kõige kergem ega raskem */
export function tyypAuto(m, lisa = false) {
	const massiga = (list) => list
		.map((c) => ({ c, p: autodIdx().polved.get(c.url.replace(/^\/autod\//, '').replace(/\/$/, '')) }))
		.filter((x) => x.p && x.p.rows[0].kerbMassKg)
		.sort((a, b) => a.p.rows[0].kerbMassKg - b.p.rows[0].kerbMassKg);
	/* lisamõõdul (2. järk) on põhimõõduga autosid vähe või pole: siis kõik autod, millel see on tehasemõõt */
	let polved = massiga(autodMoodus(m).filter((x) => x.pohi));
	if (!polved.length || (lisa && polved.length < 3)) polved = massiga(autodMoodus(m));
	if (!polved.length) return null;
	const x = polved[Math.floor(polved.length / 2)];
	return { veh: x.p.rows[0], nimi: x.c.nimi, url: x.c.url };
}

const OLUD = {
	lumi: { speedKmh: 50, surface: 'SNOW_PACKED', waterMm: 0, tempC: -5 },
	jaa: { speedKmh: 50, surface: 'ICE', waterMm: 0, tempC: -5 },
	marg: { speedKmh: 90, surface: 'ASPHALT', waterMm: 1, tempC: 5 }
};
function testKirje(x) {
	if (!x) return null;
	const src = core().sources[x.src] || {};
	return { nimi: src.nimi || x.src, lyhi: String(src.tegija || x.src).replace(/ \(.*\)/, '') + ' ' + (src.aasta || ''), moot: src.moot || '', m: x.m, v0: x.v0, v1: x.v1, t: x.t ?? null };
}
const r1 = (x) => (x == null ? null : Math.round(x * 10) / 10);

function pidurdus(tyre, veh, olu) {
	try {
		const x = P().stoppingDistance(tyre, veh, {
			texture: 'NORMAL', payloadKg: 75, gradientPct: 0, reactionTimeS: 1, brakeCondition: 1, ...OLUD[olu]
		});
		return x.stopped ? r1(x.distanceM) : null;
	} catch {
		return null;
	}
}

/** Andmed ühe mõõdu talverehvide lehe jaoks (meeles: autolehed küsivad sama mõõtu sadu kordi). */
const _lehed = new Map();
/* testitud-nimekirja kirje → mootori rehv (selles mõõdus), autolehe arvutuse jaoks; lehe andmetesse ei lähe */
const _toor = new WeakMap();
export function talveLeht(slug) {
	/* ainult olemasolevad mõõdud meelde (juhuslikud aadressid ei tohi mälu kasvatada) */
	if (!talveMoot(slug)) return null;
	if (!_lehed.has(slug)) _lehed.set(slug, talveLehtArvuta(slug));
	return _lehed.get(slug);
}

/** Autolehe KKK (18.10): selle mõõdu talvelehe jääl parim naast- ja lamellrehv, pidurdusmaa SELLE
 *  auto andmetega (50 km/h, −5 °C, uued rehvid, ilma reaktsioonita), nii et igal autol on oma number. */
export function talvParimadAutole(slug, veh) {
	const d = talveLeht(slug);
	if (!d || !veh) return null;
	const vali = (list) => {
		const x = list.find((r) => r.jaa != null && _toor.has(r));
		const jaa = x ? pidurdus(_toor.get(x), { ...veh }, 'jaa') : null;
		return jaa == null ? null : { slug: x.slug, nimi: x.nimi, jaa };
	};
	const naast = vali(d.naastud), lamell = vali(d.lamellid);
	return naast && lamell ? { naast, lamell } : null;
}

function talveLehtArvuta(slug) {
	const s = talveMoot(slug);
	if (!s) return null;
	const rows = eprelSize(s.m);
	const auto = tyypAuto(s.m, !!s.lisa);
	const veh = auto ? { ...auto.veh } : null;
	const label = s.label;

	/* testitud talverehvid: lamellid, mis on selles mõõdus EPREL-is olemas, + kõik testitud naastrehvid */
	const tyres = core().tyres;
	const bySlug = new Map(tyres.filter((t) => t.slug).map((t) => [t.slug, t]));
	const moodusSlug = new Set(rows.filter((r) => r[3] === KAT.POHJA || r[3] === KAT.KESK).map((r) => r[0]));
	const testitud = [];
	/* naastrehvi saadavus selles mõõdus: testitud selles mõõdus või poodides selles mõõdus müügil
	   (moodud on poolik: puudumine ei tähenda, et mõõtu pole — ainult positiivne tõend).
	   SUV-versioonid (testitud 235/60 R18 jne) ei käi väikese auto mõõdu esikohale (audit 18.10:
	   205/55 R16 lehe parim naastrehv oli Hakkapeliitta 10 SUV, mida selles mõõdus ei müüda). */
	const [, laius, profiil, velg] = /^(\d{3})(\d{2})R(\d{2})/.exec(s.m) || [];
	const suvMoot = +laius >= 215 && +profiil >= 50 && (+profiil >= 60 || +velg >= 17);
	const naastMoodus = (t) => t.size === label || (t.moodud || []).includes(s.m);
	for (const t of tyres) {
		const naast = t.category === 'WINTER_STUDDED';
		const lamell = t.category === 'WINTER_NORDIC' && t.slug && moodusSlug.has(t.slug);
		if (!naast && !lamell) continue;
		if (naast && !suvMoot && /\b(SUV|4x4)\b/i.test(t.name) && !naastMoodus(t)) continue;
		/* ajakirjatestidest tuletatud vanad mudelid (viimane test enne 2020) ei ole enam müügil */
		if (t.gSource === 'tuletatud' && ((t.tuletus || {}).viimane || 0) < 2020) continue;
		if (t.gSource === 'hinnang') continue; /* „testitud“ nimekiri: testimata naastrehvid siia ei käi */
		const onCar = { ...t, size: label, gSize: t.gSize || t.size };
		const kirje = {
			slug: t.slug || null,
			nimi: titleCase(t.name),
			kat: t.category,
			testMoot: t.size,
			lumi: veh ? pidurdus(onCar, veh, 'lumi') : null,
			jaa: veh ? pidurdus(onCar, veh, 'jaa') : null,
			marg: veh ? pidurdus(onCar, veh, 'marg') : null,
			/* mõõdetud jää: esimene jäätest (allikas, kiirus, meetrid) */
			jaaTest: testKirje((t.tests || []).find((x) => x.surf === 'ICE')),
			selMoodus: naast ? naastMoodus(t) : true
		};
		_toor.set(kirje, onCar);
		testitud.push(kirje);
	}
	/* selles mõõdus teadaolevalt olemas ees, siis jää pidurdusmaa järgi */
	testitud.sort((a, b) => (b.selMoodus ? 1 : 0) - (a.selMoodus ? 1 : 0) || (a.jaa ?? 999) - (b.jaa ?? 999));
	const naastud = testitud.filter((x) => x.kat === 'WINTER_STUDDED').slice(0, 15);
	const lamellid = testitud.filter((x) => x.kat !== 'WINTER_STUDDED').slice(0, 15);

	/* märgise järgi: Põhjamaade lamellid; jäämärgiga ees, siis märghaare, siis müra */
	const pohja = rows
		.filter((r) => r[3] === KAT.POHJA)
		.filter((r, i, a) => a.findIndex((x) => x[0] === r[0]) === i)
		.map((r) => ({ slug: r[0], nimi: titleCase(r[1] + ' ' + r[2]), g: r[4], db: r[6], jaa: !!(r[8] & FLAG.ICE), testitud: !!r[9] || extTests(r[0]).length > 0 }))
		.sort((a, b) => (b.jaa ? 1 : 0) - (a.jaa ? 1 : 0) || (b.testitud ? 1 : 0) - (a.testitud ? 1 : 0) || String(a.g || 'Z').localeCompare(String(b.g || 'Z')) || (a.db ?? 99) - (b.db ?? 99));
	const kesk = rows.filter((r) => r[3] === KAT.KESK).length;

	/* sama auto, rehvitüübi järgi (tüüpiline märgise klass), et näidata vahet */
	const gc = core().gClass || {};
	const tyyp = (kat) => {
		const g = ((gc.C || {})[kat] || (gc.C || {})._ || [1.3])[0];
		return { key: 'x', name: 'x', category: kat, wetGripIndex: g, treadDepthMm: 8, treadDepthNewMm: 8, ageYears: 1,
			pressureBar: null, loadCapacityKg: null, studded: kat === 'WINTER_STUDDED', size: label, gSource: 'label' };
	};
	const tyybid = veh
		? ['SUMMER_TOURING', 'ALL_SEASON', 'WINTER_CENTRAL', 'WINTER_NORDIC', 'WINTER_STUDDED'].map((k) => ({
				kat: k,
				lumi: pidurdus(tyyp(k), veh, 'lumi'),
				jaa: pidurdus(tyyp(k), veh, 'jaa')
			}))
		: [];

	/* lisamõõdul (2. järk) kõik autod, millel see on tehasemõõt (põhimõõduga ees) */
	const autod = s.lisa ? autodMoodus(s.m) : autodMoodus(s.m).filter((c) => c.pohi);
	return {
		uuendatud: TALV_UUENDATUD,
		moot: { m: s.m, slug: s.slug, label, sizeSlug: sizeModelCount(s.m) >= SIZE_MIN_MODELS ? s.slug : null },
		auto: auto ? { nimi: auto.nimi, url: auto.url, key: auto.veh.key } : null,
		autod: autod.slice(0, 16),
		autosid: autod.length,
		lisa: !!s.lisa,
		lamellid,
		naastud,
		pohja: pohja.slice(0, 15),
		pohjaKokku: pohja.length,
		pohjaJaa: pohja.filter((x) => x.jaa).length,
		kesk,
		tyybid,
		/* selles mõõdus tehtud talvetest (16 mõõdul 43-st): testi enda võitja, mitte arvutus */
		test: (testidMoodus(label) || {}).talv || null,
		/* samadel autodel ka tehasemõõt (sama läbimõõt ±3 %), millel on oma talverehvide leht */
		kaas: kaasMoot(s.m, 10).map((x) => ({ slug: sizeSlug(x.m), label: pretty(x.m), n: x.n })).filter((x) => x.slug && talveMoot(x.slug)).slice(0, 4),
		teised: talveMoodud().filter((x) => x.slug !== s.slug).slice(0, 24).map((x) => ({ slug: x.slug, label: x.label }))
	};
}
