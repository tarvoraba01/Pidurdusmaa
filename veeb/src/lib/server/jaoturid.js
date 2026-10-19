/* Märksõnade jaoturlehed (19.10): /naastrehvid/, /lamellrehvid/, /suverehvid/.
 *
 * Lühikesed päringud („naastrehvid“, „lamellrehvid“, „suverehvid“) on poodide päralt.
 * Meie leht annab samale päringule seda, mida poel ei ole: testide ja mootori numbrid
 * ning lingid kõigile selle tüübi rehvi- ja mõõdulehtedele. Numbrid tulevad samast
 * andmestikust ja mootorist kui kalkulaator ja talverehvide lehed (talv.js).
 */
import { core, models, tyrePage, rehviIndeks, extTests, sizeModelCount, SIZE_MIN_MODELS, suveTestideParimad } from './andmed.js';
import { talveLeht, talveMoodud } from './talv.js';

/* jaoturlehtede sisu viimati üle vaadatud (nähtav „uuendatud“ ja dateModified) */
export const JAOTUR_UUENDATUD = '2026-10-19';

/* näidismõõt: Eesti levinuim (sama mis /talverehvid/ lehel) */
const NAIDE = '205-55-r16';

/** Talverehvide näide mõõdus 205/55 R16: rehvitüüpide võrdlus ja jääl parimad testitud rehvid. */
function talveNaide(kat) {
	const d = talveLeht(NAIDE);
	if (!d) return null;
	const list = kat === 'WINTER_STUDDED' ? d.naastud : d.lamellid;
	return {
		moot: d.moot.label,
		slug: d.moot.slug,
		auto: d.auto ? d.auto.nimi : '',
		tyybid: d.tyybid,
		top: list
			.filter((x) => x.jaa != null)
			.slice(0, 10)
			.map((x) => ({ slug: x.slug, nimi: x.nimi, jaa: x.jaa, lumi: x.lumi, marg: x.marg, jaaTest: x.jaaTest }))
	};
}

/** Rehvid margi kaupa (ainult indekseeritavad lehed): [{ mark, rehvid: [...] }] */
function margiKaupa(read) {
	const by = new Map();
	for (const r of read) {
		if (!by.has(r.mark)) by.set(r.mark, []);
		by.get(r.mark).push(r);
	}
	return [...by.entries()]
		.map(([mark, rehvid]) => ({ mark, rehvid: rehvid.sort((a, b) => a.nimi.localeCompare(b.nimi, 'et', { numeric: true })) }))
		.sort((a, b) => a.mark.localeCompare(b.mark, 'et'));
}

/** Levinumad mõõdud, millel on talverehvide leht (/talverehvid/<mõõt>/). */
function talveMoodudLingid() {
	return talveMoodud()
		.filter((x) => !x.lisa)
		.slice(0, 30)
		.map((x) => ({ slug: x.slug, label: x.label, autosid: x.autosid }));
}

export function naastJaotur() {
	const read = [];
	for (const t of core().tyres) {
		if (t.category !== 'WINTER_STUDDED' || !t.slug || !rehviIndeks(t.slug).index) continue;
		const tp = tyrePage(t.slug);
		if (!tp) continue;
		read.push({
			slug: t.slug,
			nimi: tp.name,
			mark: tp.brand,
			hinnang: t.gSource === 'hinnang',
			viimane: (t.tuletus || {}).viimane || null
		});
	}
	return {
		uuendatud: JAOTUR_UUENDATUD,
		naide: talveNaide('WINTER_STUDDED'),
		margid: margiKaupa(read),
		kokku: read.length,
		testimata: read.filter((x) => x.hinnang).length,
		moodud: talveMoodudLingid()
	};
}

export function lamellJaotur() {
	const slugid = new Set();
	for (const t of core().tyres) if (t.category === 'WINTER_NORDIC' && t.slug) slugid.add(t.slug);
	for (const [slug, m] of Object.entries(models())) if (m.kat === 'WINTER_NORDIC') slugid.add(slug);
	const read = [];
	for (const slug of slugid) {
		if (!rehviIndeks(slug).index) continue;
		const tp = tyrePage(slug);
		if (!tp) continue;
		const tested = tp.tested && tp.tested.gSource !== 'hinnang' ? tp.tested : null;
		/* vanad tuletatud mudelid (viimane test enne 2016) ei ole enam müügil */
		if (!tp.model && tested && tested.gSource === 'tuletatud' && ((tested.tuletus || {}).viimane || 0) < 2016) continue;
		read.push({
			slug,
			nimi: tp.name,
			mark: tp.brand,
			testitud: !!tested || extTests(slug).length > 0,
			jaamark: !!(tp.model && (tp.model.sizes || []).some((s) => s.ice))
		});
	}
	return {
		uuendatud: JAOTUR_UUENDATUD,
		naide: talveNaide('WINTER_NORDIC'),
		/* soe asfalt: suverehv vs Põhjamaade talverehv (KKK „kas suvel tohib“) */
		soe: core().demo ? { suvi: core().demo.summerWarm, talv: core().demo.winterWarm } : null,
		margid: margiKaupa(read),
		kokku: read.length,
		testitud: read.filter((x) => x.testitud).length,
		jaamargiga: read.filter((x) => x.jaamark).length,
		moodud: talveMoodudLingid()
	};
}

export function suviJaotur() {
	const c = core();
	const testid = suveTestideParimad(2024);
	/* levinumad mõõdud (autode põhimõõdu järgi), millel on mõõdu leht /rehvid/<mõõt>/ */
	const moodud = talveMoodud()
		.filter((x) => !x.lisa && sizeModelCount(x.m) >= SIZE_MIN_MODELS)
		.slice(0, 30)
		.map((x) => ({ slug: x.slug, label: x.label, autosid: x.autosid, n: sizeModelCount(x.m) }));
	const suvemudeleid = Object.values(models()).filter((m) => m.kat === 'SUMMER_TOURING').length;
	/* kõige sagedamini testi 1. koht (viigi korral loevad kõik võitjad) */
	const voidud = (ala) => {
		const c = new Map();
		for (const t of testid)
			for (const r of (t.alad[ala] || {}).rehvid || []) {
				const x = c.get(r.slug) || { slug: r.slug, nimi: r.nimi, ix: r.ix, n: 0 };
				x.n++;
				c.set(r.slug, x);
			}
		return [...c.values()].sort((a, b) => b.n - a.n || a.nimi.localeCompare(b.nimi, 'et')).slice(0, 3);
	};
	const aastad = testid.map((t) => t.aasta);
	return {
		uuendatud: JAOTUR_UUENDATUD,
		demo: c.demo || null,
		testid,
		aasta0: aastad.length ? Math.min(...aastad) : null,
		aasta1: aastad.length ? Math.max(...aastad) : null,
		voidud: { marg: voidud('märg asfalt'), kuiv: voidud('kuiv asfalt') },
		moodud,
		suvemudeleid
	};
}
