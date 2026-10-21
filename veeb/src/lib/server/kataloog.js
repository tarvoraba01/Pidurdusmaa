/* Rehvikataloog (Tarvo 21.10: „nagu rehvid.ai kataloog, mugav valida ja osta“).
 *
 * Ühe mõõdu ja tüübi rehvid ühe nimekirjana, mida /rehvid/ ja mõõdulehtede kataloog näitab:
 *   - suvi:   EL-i märgise suverehvid (eprel kat 0)
 *   - lamell: Põhjamaade (kat 3) ja Kesk-Euroopa (kat 2) lamellrehvid
 *   - naast:  naastrehvid (märgist pole): testitud ja hinnangulised, kui need on selles mõõdus
 *             testitud või poodides müügil
 * AUSUS (sama mis app.js): pidurdusmaa meetrites ainult rehvil, millel on päris testid. Märgise rehv
 * on teada ainult klassi järgi, seal näidatakse märghaarde klassi ja müra, mitte meetreid.
 * Hinnad tulevad samast koondist mis kalkulaatoris (hinnadMoodus), kõik poed võrdselt.
 */
import '$lib/engine.js';
import { core, eprelSize, pretty, titleCase, testedByKey, tyrePage, rehviIndeks, extTests } from './andmed.js';
import { tyypAuto } from './talv.js';
import { hinnadMoodus } from './integratsioonid/koond.js';

const P = () => globalThis.Pidurdus;
const KAT = { SUVI: 0, AASTARING: 1, KESK: 2, POHJA: 3 };
const FLAG = { SNOW: 4, ICE: 8 };
export const TYYBID = ['suvi', 'lamell', 'naast'];
/* pidurdusmaa tingimused tüübi järgi (ilma reaktsioonita, uued rehvid) */
const OLU = {
	suvi: { pind: 'marg', silt: 'Märg 80→0', speedKmh: 80, surface: 'ASPHALT', waterMm: 1, tempC: 15 },
	lamell: { pind: 'jaa', silt: 'Jää 50→0', speedKmh: 50, surface: 'ICE', waterMm: 0, tempC: -5 },
	naast: { pind: 'jaa', silt: 'Jää 50→0', speedKmh: 50, surface: 'ICE', waterMm: 0, tempC: -5 }
};
const r1 = (x) => (x == null ? null : Math.round(x * 10) / 10);

function pidurdus(t, veh, olu) {
	try {
		const x = P().stoppingDistance(t, veh, { texture: 'NORMAL', payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1, ...olu });
		return x.stopped ? r1(x.distanceM) : null;
	} catch {
		return null;
	}
}

/* mõõdu auto: tüüpiline selle mõõduga auto; kui pole, siis kalkulaatori vaikeauto mõõduga */
function autoMoodule(m) {
	const a = tyypAuto(m);
	if (a) return { veh: { ...a.veh }, nimi: a.nimi };
	const v = core().vehicles.find((x) => x.key === 'vw_golf_8') || core().vehicles[0];
	return v ? { veh: { ...v }, nimi: v.name } : null;
}

function leht(slug) {
	if (!slug) return null;
	try { return rehviIndeks(slug).index ? '/rehvid/' + slug + '/' : null; } catch { return null; }
}

/* hinnadeta põhinimekiri, mõõdu ja tüübi kaupa meeles (ainult olemasolevad mõõdud) */
const _alus = new Map();
function alus(m, tyyp) {
	const k = m + '|' + tyyp;
	if (_alus.has(k)) return _alus.get(k);
	const label = pretty(m);
	const rows = eprelSize(m);
	const auto = autoMoodule(m);
	const olu = OLU[tyyp];
	const read = [];
	const nahtud = new Set();
	const testitud = (t) => {
		if (!t || !auto) return null;
		return pidurdus({ ...t, size: label, gSize: t.gSize || t.size }, auto.veh, olu);
	};
	if (tyyp === 'naast') {
		for (const t of core().tyres) {
			if (t.category !== 'WINTER_STUDDED' || !t.slug || nahtud.has(t.slug)) continue;
			if (t.gSource === 'tuletatud' && ((t.tuletus || {}).viimane || 0) < 2020) continue;
			nahtud.add(t.slug);
			const onTest = t.gSource !== 'hinnang';
			const nimi = titleCase(t.name);
			read.push({
				slug: t.slug, nimi, mark: nimi.split(' ')[0], kat: 'WINTER_STUDDED', testitud: onTest,
				m: onTest ? testitud(t) : null, g: null, db: null, jaa: false, lumi: false,
				selMoodus: t.size === label || (t.moodud || []).includes(m), url: leht(t.slug)
			});
		}
	} else {
		const katid = tyyp === 'suvi' ? [KAT.SUVI] : [KAT.POHJA, KAT.KESK];
		for (const r of rows) {
			if (!katid.includes(r[3]) || nahtud.has(r[0])) continue;
			nahtud.add(r[0]);
			const t = r[9] ? testedByKey(r[9]) : null;
			read.push({
				slug: r[0], nimi: titleCase(r[1] + ' ' + r[2]), mark: titleCase(r[1]),
				kat: r[3] === KAT.SUVI ? 'SUMMER' : r[3] === KAT.POHJA ? 'WINTER_NORDIC' : 'WINTER_CENTRAL',
				testitud: !!t || extTests(r[0]).length > 0, m: t ? testitud(t) : null,
				g: r[4] || null, db: r[6] ?? null, jaa: !!(r[8] & FLAG.ICE), lumi: !!(r[8] & FLAG.SNOW),
				selMoodus: true, url: leht(r[0])
			});
		}
	}
	const val = { label, auto: auto ? auto.nimi : null, silt: olu.silt, read };
	if (_alus.size > 600) _alus.clear();
	_alus.set(k, val);
	return val;
}

/** Kataloog: { moot, tyyp, auto, silt, hinnadOlemas, read: [...] } */
export async function kataloog(m, tyyp) {
	if (!core().eprelSizes.includes(m)) return null;
	const a = alus(m, tyyp);
	let hinnad = {}, olemas = false;
	try {
		const h = await hinnadMoodus(m);
		olemas = !!h.available;
		hinnad = h.hinnad || {};
	} catch { /* hinnad pole kohustuslikud */ }
	const read = a.read
		.map((r) => {
			const list = (hinnad[r.slug + '@' + m] || []).filter((x) => x.hind > 0 && x.url);
			list.sort((x, y) => x.hind - y.hind);
			const parim = list[0];
			return {
				...r,
				hind: parim ? { min: parim.hind, umbes: !!parim.umbes, poode: new Set(list.map((x) => x.myyja)).size, laos: list.some((x) => x.laos),
					pood: parim.myyja, url: parim.url } : null,
				pilt: list.some((x) => x.pilt)
			};
		})
		/* naastrehv: ainult kui selles mõõdus teada (testitud selles mõõdus või poes müügil) */
		.filter((r) => tyyp !== 'naast' || r.selMoodus || r.hind);
	return { moot: m, label: a.label, tyyp, auto: a.auto, silt: a.silt, hinnadOlemas: olemas, read };
}
