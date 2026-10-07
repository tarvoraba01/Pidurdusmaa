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
import { core, eprelSize, pretty, sizeSlug, titleCase, sizeModelCount, SIZE_MIN_MODELS, extTests } from './andmed.js';
import { autodMoodus, autod as autodIdx } from './autod.js';

const P = () => globalThis.Pidurdus;
/* talverehvide lehtede sisu viimati üle vaadatud (nähtav „uuendatud“ ja dateModified) */
export const TALV_UUENDATUD = '2026-10-07';
const FLAG = { SNOW: 4, ICE: 8 };
/* EPREL-i kategooria number (andmed.js eprelSize: katNr) */
const KAT = { SUVI: 0, AASTARING: 1, KESK: 2, POHJA: 3 };

/** Mõõdud, millele leht tehakse: vähemalt 3 autot, mille PÕHImõõt see on,
 *  ja vähemalt 8 Põhjamaade talverehvi märgise andmetega. Enim autosid ees. */
let _moodud = null;
/* 2026-09-30 avaldatud esimesed 40 lehte */
const AVALDATUD = new Set(('175-65-r14 175-65-r15 175-70-r13 175-70-r14 185-60-r15 185-65-r14 185-65-r15 185-70-r14 195-55-r16 ' +
	'195-60-r15 195-65-r15 205-55-r16 205-60-r16 205-70-r15 215-55-r16 215-55-r17 215-55-r18 215-60-r16 215-60-r17 215-65-r16 ' +
	'215-65-r17 225-50-r17 225-55-r16 225-55-r17 225-55-r18 225-55-r19 225-60-r17 225-60-r18 225-65-r17 235-50-r19 235-55-r17 ' +
	'235-55-r18 235-55-r19 235-60-r18 235-65-r17 235-65-r18 245-45-r18 255-55-r18 255-55-r19 265-60-r18').split(' '));
export function talveMoodud() {
	if (_moodud) return _moodud;
	const out = [];
	for (const s of core().sizes) {
		const autod = autodMoodus(s.m).filter((c) => c.pohi);
		if (autod.length < 3) continue;
		const rows = eprelSize(s.m);
		const pohja = rows.filter((r) => r[3] === KAT.POHJA).length;
		if (pohja < 8) continue;
		out.push({ m: s.m, slug: sizeSlug(s.m), label: pretty(s.m), autosid: autod.length, pohja });
	}
	out.sort((a, b) => b.autosid - a.autosid || b.pohja - a.pohja);
	/* 40 levinumat + kõik juba avaldatud lehed (aadress ei tohi kaduda,
	   kui uute autode lisamisel mõõtude järjekord muutub) */
	_moodud = out.filter((x, i) => i < 40 || AVALDATUD.has(x.slug));
	return _moodud;
}

export function talveMoot(slug) {
	return talveMoodud().find((x) => x.slug === slug) || null;
}

/* Tüüpiline auto selle mõõduga: põhimõõduga põlvkondadest keskmise massiga
   (mediaan) — mitte kõige kergem ega raskem */
function tyypAuto(m) {
	const polved = autodMoodus(m)
		.filter((x) => x.pohi)
		.map((c) => ({ c, p: autodIdx().polved.get(c.url.replace(/^\/autod\//, '').replace(/\/$/, '')) }))
		.filter((x) => x.p && x.p.rows[0].kerbMassKg)
		.sort((a, b) => a.p.rows[0].kerbMassKg - b.p.rows[0].kerbMassKg);
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

/** Andmed ühe mõõdu talverehvide lehe jaoks. */
export function talveLeht(slug) {
	const s = talveMoot(slug);
	if (!s) return null;
	const rows = eprelSize(s.m);
	const auto = tyypAuto(s.m);
	const veh = auto ? { ...auto.veh } : null;
	const label = s.label;

	/* testitud talverehvid: lamellid, mis on selles mõõdus EPREL-is olemas, + kõik testitud naastrehvid */
	const tyres = core().tyres;
	const bySlug = new Map(tyres.filter((t) => t.slug).map((t) => [t.slug, t]));
	const moodusSlug = new Set(rows.filter((r) => r[3] === KAT.POHJA || r[3] === KAT.KESK).map((r) => r[0]));
	const testitud = [];
	for (const t of tyres) {
		const naast = t.category === 'WINTER_STUDDED';
		const lamell = t.category === 'WINTER_NORDIC' && t.slug && moodusSlug.has(t.slug);
		if (!naast && !lamell) continue;
		const onCar = { ...t, size: label, gSize: t.gSize || t.size };
		testitud.push({
			slug: t.slug || null,
			nimi: titleCase(t.name),
			kat: t.category,
			testMoot: t.size,
			lumi: veh ? pidurdus(onCar, veh, 'lumi') : null,
			jaa: veh ? pidurdus(onCar, veh, 'jaa') : null,
			marg: veh ? pidurdus(onCar, veh, 'marg') : null,
			/* mõõdetud jää: esimene jäätest (allikas, kiirus, meetrid) */
			jaaTest: testKirje((t.tests || []).find((x) => x.surf === 'ICE')),
			selMoodus: !naast
		});
	}
	testitud.sort((a, b) => (a.jaa ?? 999) - (b.jaa ?? 999));
	const naastud = testitud.filter((x) => x.kat === 'WINTER_STUDDED');
	const lamellid = testitud.filter((x) => x.kat !== 'WINTER_STUDDED');

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

	const autod = autodMoodus(s.m).filter((c) => c.pohi);
	return {
		uuendatud: TALV_UUENDATUD,
		moot: { m: s.m, slug: s.slug, label, sizeSlug: sizeModelCount(s.m) >= SIZE_MIN_MODELS ? s.slug : null },
		auto: auto ? { nimi: auto.nimi, url: auto.url, key: auto.veh.key } : null,
		autod: autod.slice(0, 16),
		autosid: autod.length,
		lamellid,
		naastud,
		pohja: pohja.slice(0, 15),
		pohjaKokku: pohja.length,
		pohjaJaa: pohja.filter((x) => x.jaa).length,
		kesk,
		tyybid,
		teised: talveMoodud().filter((x) => x.slug !== s.slug).slice(0, 24).map((x) => ({ slug: x.slug, label: x.label }))
	};
}
