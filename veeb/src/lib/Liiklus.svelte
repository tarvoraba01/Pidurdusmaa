<script>
	import { useT, useLang, autoNimi } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const LOC = { et: 'et-EE', ru: 'ru-RU', en: 'en-GB' }[keel.lang] || 'et-EE';
	/* Neli eraldi tööriista, sama vasak paneel (olukord A/B). Vahekaart = eraldi leht;
	   olukord liigub aadressi #… kaudu ühest tööriistast teise kaasa. */
	let { vaade = 'peatumine' } = $props();
	const VAATED = [
		['peatumine', '/liiklusohutus/', t('Peatumisteekond')],
		['pimedas', '/liiklusohutus/pimedas/', t('Pimedas')],
		['pikivahe', '/liiklusohutus/pikivahe/', t('Pikivahe')],
		['kurv', '/liiklusohutus/kurv/', t('Kurv ja rehvid')]
	];
	const teeVaade = $derived(vaade === 'peatumine' || vaade === 'pimedas');
	/* Liiklusohutuse kalkulaator (/liiklusohutus/).
	   Sama arvutusmootor mis põhilehel (engine.js), aga neutraalne:
	   ei poode, hindu, rehvisoovitusi ega kasutusloo jälgimist.
	   Kõik mudeli sisendid on nähtaval, et õpetaja ja õpilane saaksid
	   iga teguri mõju ise läbi mängida. Olukord salvestub aadressi
	   (#...), nii et lingi saab jagada või tunniks ette valmistada. */
	import { onMount } from 'svelte';
	import { version } from '$app/environment';
	import { kaitumine } from '$lib/kaitumine.js';
	import { pikivahe } from '$lib/pikivahe.js';

	let core = $state(null);
	let P = $state(null);
	let viga = $state('');

	const KAT = [
		['SUMMER_TOURING', t('Suverehv')],
		['SUMMER_UHP', t('Suverehv, sportlik')],
		['ALL_SEASON', t('Aastaringne rehv')],
		['WINTER_CENTRAL', t('Talverehv, Kesk-Euroopa')],
		['WINTER_NORDIC', t('Talverehv, Põhjamaade (lamell)')],
		['WINTER_STUDDED', t('Naastrehv')]
	];
	const PIND = [
		['ASPHALT', t('Asfalt')],
		['CONCRETE', t('Betoon')],
		['GRAVEL', t('Kruus')],
		['SNOW_PACKED', t('Tallatud lumi')],
		['SNOW_LOOSE', t('Kohev lumi')],
		['ICE', t('Jää')]
	];
	const VESI = [
		[0, t('Kuiv')],
		[0.2, t('Niiske')],
		[1, t('Märg')],
		[3, t('Väga märg')],
		[5, t('Lombid')]
	];
	const TEKST = [
		['COARSE_NEW', t('Uus, kare')],
		['NORMAL', t('Tavaline')],
		['WORN_SMOOTH', t('Kulunud, roopad')],
		['POLISHED', t('Poleeritud')]
	];
	const PIDUR = [
		[1, t('Korras')],
		[0.85, t('Nõrgenenud (~85 %)')],
		[0.65, t('Selgelt vigane (~65 %)')],
		[0.45, t('Kriitiline (~45 %)')]
	];
	const REAKT = [
		[0.7, t('valmis pidurdama')],
		[1.0, t('tavaline arvestus')],
		[1.5, t('ootamatu oht')],
		[2.0, t('väsinud / hajevil')]
	];
	const ASF = { ASPHALT: 1, CONCRETE: 1 };
	const TALV = { ALL_SEASON: 1, WINTER_CENTRAL: 1, WINTER_NORDIC: 1, WINTER_STUDDED: 1 };

	const ALGNE = {
		tyyp: 'yld_kompakt', mk: '', md: '', veh: '', abs: 'auto', laad: 75, pidur: 1,
		kat: 'SUMMER_TOURING', klass: 'C', muster: 8, vanus: 1, rohk: 0,
		pind: 'ASPHALT', vesi: 1, tekst: 'NORMAL', temp: 10, jaa: 'tee', kalle: 0,
		kiirus: 50, reakt: 1.0
	};

	let A = $state({ ...ALGNE });
	let B = $state(null);
	let muuda = $state('A');
	let takistus = $state(0);
	/* Nähtavus pimedas: kaugus, kust juht jalakäijat märkab (Transpordiamet,
	   „Mida pead helkuri kohta teadma“, 2025): lähitulede valgel tumedas riietes
	   helkurita jalakäija kuni 30 m, heledas riietes 40–50 m, helkuriga 130–150 m;
	   kaugtulede valgel helkuriga 300–350 m. Kasutame vahemiku keskkohta. */
	const NAHT = [
		['tume', 30, t('Lähituled, tumedad riided, helkurita')],
		['hele', 45, t('Lähituled, heledad riided, helkurita')],
		['helkur', 140, t('Lähituled, helkuriga')],
		['kaug', 325, t('Kaugtuled, helkuriga')]
	];
	let naeb = $state('');
	const NAEB = $derived(NAHT.find((x) => x[0] === naeb) || null);
	function setNaeb(id) {
		const x = NAHT.find((n) => n[0] === id);
		if (!x || naeb === id) { naeb = ''; takistus = 0; return; }
		naeb = id;
		takistus = x[1];
		pl('Liiklusohutus: nähtavus', { naeb: id });
	}
	/* suurim kiirus, millega auto jõuab kaugusel d peatuda (sama olukord, ainult kiirus muutub) */
	function vMax(s, d) {
		if (!s || !(d > 0)) return null;
		let lo = 0, hi = 160;
		const ok = (v) => {
			const r = arvuta({ ...s, kiirus: v });
			return r && r.r && r.r.stopped && r.r.totalDistanceM <= d;
		};
		if (!ok(5)) return 0;
		if (ok(hi)) return hi;
		for (let i = 0; i < 16; i++) {
			const mid = (lo + hi) / 2;
			if (ok(mid)) lo = mid; else hi = mid;
		}
		return Math.floor(lo);
	}
	/* Auto käitumine pidurdamisel ($lib/kaitumine.js): kurv ja rehvid ees/taga */
	/* kurvid tavaliste sõnadega; raadius (m) ainult arvutuseks ja väikese vihjena */
	const KURV = [
		[0, t('Sirge tee'), ''],
		[300, t('Lauge kurv'), t('nagu maanteel, kus saab sõita 90 km/h')],
		[150, t('Tavaline kurv'), t('maantee kurv, enne mida kiirust veidi vähendad')],
		[75, t('Järsk kurv'), t('märk „Ohtlik kurv“, linnatänav')],
		[30, t('Väga järsk'), t('pööre ristmikul, ringtee')]
	];
	let kurv = $state(75);
	/* Kurvi tööriista oma sisendid (ei sõltu olukorrast A) */
	const KR_PIND = [
		['kuiv', t('Kuiv'), { surface: 'ASPHALT', waterMm: 0, tempC: 15 }],
		['marg', t('Märg'), { surface: 'ASPHALT', waterMm: 1, tempC: 10 }],
		['lumi', t('Lumi'), { surface: 'SNOW_PACKED', waterMm: 0, tempC: -5 }],
		['jaa', t('Jää'), { surface: 'ICE', waterMm: 0, tempC: -5 }]
	];
	const KR_KAT = [
		['SUMMER_TOURING', t('Suverehv')],
		['WINTER_NORDIC', t('Talverehv (lamell)')],
		['WINTER_STUDDED', t('Naastrehv')]
	];
	const KR_AUTO = [
		['yld_vaike', t('Väikeauto')],
		['yld_kompakt', t('Kompaktauto')],
		['yld_maastur', t('Maastur')],
		['yld_kaubik', t('Kaubik')]
	];
	let KR = $state({ kiirus: 75, pind: 'marg', kat: 'SUMMER_TOURING', esi: 8, taga: 2, auto: 'yld_kompakt' });
	/* Pikivahe ($lib/pikivahe.js): eesolev auto pidurdab järsult või peatub kohe */
	let ees = $state('pidurdab');
	let esitlus = $state(false);
	let kopeeritud = $state(false);
	let juur;
	let outEl = $state(null);
	let tulemusNahtav = $state(true);
	$effect(() => {
		if (!outEl || typeof IntersectionObserver === 'undefined') return;
		const io = new IntersectionObserver((e) => (tulemusNahtav = e[0].isIntersecting), { threshold: 0.15 });
		io.observe(outEl);
		return () => io.disconnect();
	});
	const naitaTulemust = () => outEl?.scrollIntoView({ behavior: 'smooth', block: 'start' });

	const S = $derived(muuda === 'B' && B ? B : A);

	/* Plausible (küpsisteta statistika): ainult tegevused, mitte iga liigutus */
	const pl = (nimi, props) => {
		try {
			if (typeof window !== 'undefined' && typeof window.plausible === 'function') window.plausible(nimi, props ? { props } : undefined);
		} catch {}
	};

	/* ------------------------------------------------------ andmed */
	onMount(async () => {
		try {
			await import('$lib/engine.js');
			P = globalThis.Pidurdus;
			const r = await fetch('/data/core.json?v=' + encodeURIComponent(version));
			const d = await r.json();
			d.byKey = {};
			d.vehicles.forEach((v) => (d.byKey[v.key] = v));
			core = d;
			loeAadressist();
			if (vaade === 'pimedas' && !naeb) setNaeb('tume');
		} catch (e) {
			viga = t('Andmed ei laadinud. Proovi lehte värskendada.');
		}
		document.addEventListener('fullscreenchange', () => {
			if (!document.fullscreenElement) esitlus = false;
		});
	});

	const tyybid = $derived(core ? core.vehicles.filter((v) => v.make === 'Ei leia oma autot') : []);
	const autod = $derived(core ? core.vehicles.filter((v) => v.make !== 'Ei leia oma autot') : []);
	const margid = $derived([...new Set(autod.map((v) => v.make))].sort((a, b) => a.localeCompare(b, 'et')));
	const mudelid = $derived(
		S.mk ? [...new Set(autod.filter((v) => v.make === S.mk).map((v) => v.model))].sort((a, b) => a.localeCompare(b, 'et', { numeric: true })) : []
	);
	const polved = $derived.by(() => {
		if (!S.mk || !S.md) return [];
		const rows = autod.filter((v) => v.make === S.mk && v.model === S.md);
		const alg = (v) => +((/(\d{4})/.exec(v.yearLabel) || [0, 0])[1]);
		const n = {};
		rows.forEach((v) => (n[v.yearLabel] = (n[v.yearLabel] || 0) + 1));
		return rows
			.sort((a, b) => alg(b) - alg(a))
			.map((v) => [v.key, v.yearLabel + (n[v.yearLabel] > 1 && v.variant && v.variant !== '—' ? ' · ' + v.variant.replace(' hj (', ' ' + t('hj') + ' (') : '')]);
	});

	function auto(s) {
		if (!core) return null;
		let v = core.byKey[s.mk ? s.veh : s.tyyp];
		if (!v) return null;
		if (v.absOpt && s.abs === 'jah') v = Object.assign({}, v, v.absOpt);
		if (s.abs === 'ei') v = Object.assign({}, v, { absClass: 'NONE' });
		return v;
	}

	function G(s) {
		const rida = core.gClass[s.klass] || core.gClass.C;
		const k = s.kat === 'WINTER_STUDDED' ? 'WINTER_NORDIC' : s.kat;
		return (rida[k] || rida._)[0];
	}

	/* olukorra sisend mootorile: auto, rehv ja tingimused */
	function sisend(s) {
		const veh = auto(s);
		if (!veh) return null;
		const asf = !!ASF[s.pind];
		const tyre = {
			key: 'x', name: 'x', category: s.kat, wetGripIndex: G(s),
			treadDepthMm: +s.muster, treadDepthNewMm: 8, ageYears: +s.vanus,
			pressureBar: +s.rohk ? Math.round((veh.recommendedPressureBar + +s.rohk) * 10) / 10 : null,
			loadCapacityKg: null, studded: s.kat === 'WINTER_STUDDED', size: veh.oemSize, gSource: 'label'
		};
		const cond = {
			speedKmh: +s.kiirus, surface: s.pind, texture: asf ? s.tekst : 'NORMAL',
			waterMm: asf ? +s.vesi : 0, tempC: +s.temp, payloadKg: +s.laad,
			gradientPct: +s.kalle, reactionTimeS: +s.reakt, brakeCondition: +s.pidur,
			iceRoad: s.jaa !== 'sile'
		};
		return { veh, tyre, cond };
	}

	function arvuta(s) {
		if (!core || !P || !s) return null;
		const x = sisend(s);
		if (!x) return null;
		try {
			const r = P.stoppingDistance(x.tyre, x.veh, x.cond);
			return { r, veh: x.veh, v0: +s.kiirus, reakt: r.reactionM };
		} catch (e) {
			return { err: String(e.message || e) };
		}
	}

	const RA = $derived(arvuta(A));
	const RB = $derived(B ? arvuta(B) : null);

	/* kiirus teel kaugusel d stardist: reaktsiooni ajal täis, siis pidurdusjälg */
	function kiirusKohal(res, d) {
		if (!res || !res.r) return null;
		if (d <= res.reakt) return res.v0;
		const x = d - res.reakt, tr = res.r.trace;
		if (!res.r.stopped) return null;
		for (let i = 1; i < tr.length; i++) {
			if (tr[i][0] >= x) {
				const [s0, v0] = tr[i - 1], [s1, v1] = tr[i];
				return s1 > s0 ? v0 + ((v1 - v0) * (x - s0)) / (s1 - s0) : v1;
			}
		}
		return 0;
	}
	const kukkumine = (kmh) => (kmh / 3.6) ** 2 / (2 * 9.81);
	/* Löögi võrdlus inimese kukkumisega (sama kiirus maandudes): h = v²/2g.
	   Korrus: 1. korrus maapinnal, iga korrus ~3 m. */
	function look(kmh) {
		const h = kukkumine(kmh);
		const hs = h >= 10 ? f0(h) : f1(h);
		return h >= 3
			? t('Löök on sama, nagu kukuks inimene {h} m kõrguselt — umbes {k}. korruse aknast.', { h: hs, k: Math.round(h / 3) + 1 })
			: t('Löök on sama, nagu kukuks inimene {h} m kõrguselt.', { h: hs });
	}

	/* ------------------------------------------------------ vormindus */
	const f1 = (x) => (Math.round(x * 10) / 10).toLocaleString(LOC, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
	const f0 = (x) => Math.round(x).toLocaleString(LOC);
	const m = (x) => (x >= 100 ? f0(x) : f1(x));

	/* ------------------------------------------------------ muutmine */
	function setPind(s, p) {
		s.pind = p;
		if (p === 'ICE' || p === 'SNOW_PACKED' || p === 'SNOW_LOOSE') s.temp = -5;
		else if (p === 'GRAVEL') s.temp = 12;
		else s.temp = s.vesi > 0 ? 10 : 15;
	}
	function setVesi(s, w) {
		s.vesi = w;
		if (w === 0 && s.temp === 10) s.temp = 15;
		if (w > 0 && s.temp === 15) s.temp = 10;
	}
	function seisund(s, k) {
		const piir = TALV[s.kat] ? 3.0 : 1.6;
		if (k === 'uus') { s.muster = 8; s.vanus = 1; }
		if (k === 'kesk') { s.muster = 4.5; s.vanus = 6; }
		if (k === 'piir') { s.muster = piir; s.vanus = 10; }
	}
	const tMin = $derived(S.pind === 'ICE' || S.pind.startsWith('SNOW') ? -30 : S.pind === 'GRAVEL' ? -10 : -20);
	const tMax = $derived(S.pind === 'ICE' ? 2 : S.pind.startsWith('SNOW') ? 3 : 40);
	$effect(() => {
		if (S.temp > tMax) S.temp = tMax;
		if (S.temp < tMin) S.temp = tMin;
	});

	function lisaB() {
		pl('Liiklusohutus: võrdlus lisatud');
		B = JSON.parse(JSON.stringify(A));
		muuda = 'B';
	}
	function eemaldaB() {
		B = null;
		muuda = 'A';
	}
	function naide(n) {
		pl('Liiklusohutus: valmis võrdlus', { naide: n });
		const a = { ...ALGNE, tyyp: A.tyyp, mk: A.mk, md: A.md, veh: A.veh };
		const b = { ...a };
		takistus = 0;
		naeb = '';
		if (n === 'kiirus') { a.kiirus = 50; b.kiirus = 70; takistus = 0; }
		if (n === 'muster') { Object.assign(a, { kiirus: 90, vesi: 1 }); Object.assign(b, { kiirus: 90, vesi: 1, muster: 1.6, vanus: 10 }); }
		if (n === 'lumi') {
			Object.assign(a, { kat: 'WINTER_NORDIC', pind: 'SNOW_PACKED', temp: -5, kiirus: 50 });
			Object.assign(b, { kat: 'SUMMER_TOURING', pind: 'SNOW_PACKED', temp: -5, kiirus: 50 });
		}
		if (n === 'telefon') { Object.assign(a, { reakt: 1.0, kiirus: 50, vesi: 0, temp: 15 }); Object.assign(b, { reakt: 2.0, kiirus: 50, vesi: 0, temp: 15 }); }
		if (n === 'jaa') {
			Object.assign(a, { kat: 'WINTER_NORDIC', pind: 'ICE', temp: -10, kiirus: 50 });
			Object.assign(b, { kat: 'WINTER_NORDIC', pind: 'ICE', temp: 0, kiirus: 50 });
		}
		if (n === 'vesi') { Object.assign(a, { kiirus: 90, vesi: 1 }); Object.assign(b, { kiirus: 90, vesi: 5, muster: 3, vanus: 6 }); }
		A = a;
		B = b;
		muuda = 'B';
		if (n === 'kiirus') takistus = Math.ceil(arvuta(a)?.r?.totalDistanceM || 0);
	}

	/* ------------------------------------------------------ aadress
	   Aadressi lõppu (#…) läheb AINULT see, mis erineb algseisust, loetava
	   nimega: #kiirus=70&pind=ICE&b.kiirus=90. Algseisus on aadress puhas.
	   Nii saab õpetaja lingi kopeerida ja olukord avaneb täpselt samana. */
	const VOTMED = Object.keys(ALGNE);
	function kirjuta(h, s, eel) {
		VOTMED.forEach((k) => {
			if (s[k] !== ALGNE[k]) h.set(eel + k, String(s[k]));
		});
	}
	function loe(h, eel) {
		const o = { ...ALGNE };
		VOTMED.forEach((k) => {
			const x = h.get(eel + k);
			if (x !== null && x !== '') o[k] = typeof ALGNE[k] === 'number' ? +x : x;
		});
		return o;
	}
	/* vana vorm (#a=***…) -- enne 2026-09-30 jagatud lingid töötavad edasi */
	function vanaVorm(t) {
		const o = { ...ALGNE };
		(t || '').split('*').forEach((x, i) => {
			const k = VOTMED[i];
			if (k && x !== '') o[k] = typeof ALGNE[k] === 'number' ? +x : x;
		});
		return o;
	}
	function loeAadressist() {
		try {
			const h = new URLSearchParams(location.hash.slice(1));
			if (h.get('a') && h.get('a').includes('*')) {
				A = vanaVorm(h.get('a'));
				if (h.get('b')) B = vanaVorm(h.get('b'));
			} else {
				A = loe(h, '');
				if (h.has('b') || [...h.keys()].some((k) => k.startsWith('b.'))) B = loe(h, 'b.');
			}
			if (h.get('t')) takistus = +h.get('t') || 0;
			if (h.get('takistus')) takistus = +h.get('takistus') || 0;
			if (NAHT.some((n) => n[0] === h.get('naeb'))) naeb = h.get('naeb');
			if (h.has('kurv') && KURV.some((k) => k[0] === +h.get('kurv'))) kurv = +h.get('kurv');
			if (h.get('kr')) {
				const [ki, pi, ka, es, ta, au] = h.get('kr').split('~');
				if (+ki >= 10 && +ki <= 150) KR.kiirus = +ki;
				if (KR_PIND.some((x) => x[0] === pi)) KR.pind = pi;
				if (KR_KAT.some((x) => x[0] === ka)) KR.kat = ka;
				if (+es >= 1 && +es <= 9) KR.esi = +es;
				if (+ta >= 1 && +ta <= 9) KR.taga = +ta;
				if (KR_AUTO.some((x) => x[0] === au)) KR.auto = au;
			}
			if (h.get('ees') === 'seisab') ees = 'seisab';
		} catch {}
	}
	$effect(() => {
		if (!core) return;
		const h = new URLSearchParams();
		kirjuta(h, A, '');
		if (B) {
			h.set('b', '1');
			kirjuta(h, B, 'b.');
		}
		if (takistus) h.set('takistus', String(takistus));
		if (naeb) h.set('naeb', naeb);
		if (vaade === 'kurv') {
			if (kurv !== 75) h.set('kurv', String(kurv));
			h.set('kr', [KR.kiirus, KR.pind, KR.kat, KR.esi, KR.taga, KR.auto].join('~'));
		}
		if (ees !== 'pidurdab') h.set('ees', ees);
		const q = h.toString();
		try {
			history.replaceState(history.state, '', location.pathname + location.search + (q ? '#' + q : ''));
		} catch {}
	});
	async function kopeeri() {
		try {
			await navigator.clipboard.writeText(location.href);
			pl('Liiklusohutus: link kopeeritud');
			kopeeritud = true;
			setTimeout(() => (kopeeritud = false), 2000);
		} catch {}
	}
	async function esitlusrezim() {
		esitlus = !esitlus;
		if (esitlus) pl('Liiklusohutus: esitlusrežiim');
		try {
			if (esitlus && juur.requestFullscreen) await juur.requestFullscreen();
			else if (!esitlus && document.fullscreenElement) await document.exitFullscreen();
		} catch {}
	}

	/* ------------------------------------------------------ joonis */
	const stsenaariumid = $derived([['A', RA], ...(B ? [['B', RB]] : [])].filter(([, x]) => x && x.r));
	const maxD = $derived(Math.max(10, takistus || 0, ...stsenaariumid.map(([, x]) => (x.r.stopped ? x.r.totalDistanceM : 0))));
	const samm = $derived([2, 5, 10, 20, 25, 50, 100, 200].find((s) => maxD / s <= 9) || 500);
	/* joonise laius = päris pikslid, et kiri oleks telefonis sama loetav kui arvutis */
	let figW = $state(700);
	const W = $derived(Math.max(300, Math.min(1000, Math.round(figW || 700))));
	const PADL = 26, PADR = 18;
	const X = (d) => PADL + (d / (Math.ceil(maxD / samm) * samm)) * (W - PADL - PADR);
	const tikid = $derived(Array.from({ length: Math.ceil(maxD / samm) + 1 }, (_, i) => i * samm));

	const vordlus = $derived.by(() => {
		if (!RB || !RA || !RA.r || !RB.r || !RA.r.stopped || !RB.r.stopped) return null;
		const a = RA.r.totalDistanceM, b = RB.r.totalDistanceM;
		const [lyh, pikk, L, Pk] = a <= b ? [RA, RB, 'A', 'B'] : [RB, RA, 'B', 'A'];
		const v = kiirusKohal(pikk, lyh.r.totalDistanceM);
		return { vahe: Math.abs(b - a), L, Pk, koht: lyh.r.totalDistanceM, v };
	});
	const tak = $derived(
		takistus > 0 ? stsenaariumid.map(([n, x]) => [n, x.r.stopped && x.r.totalDistanceM <= takistus ? 0 : kiirusKohal(x, takistus) ?? x.v0]) : []
	);
	const vmaxid = $derived(NAEB && core && P ? [['A', A], ...(B ? [['B', B]] : [])].map(([n, s]) => [n, vMax(s, takistus)]) : []);

	/* Pikivahe: A = sina; B (kui lisatud) = eesolev auto oma kiiruse, rehvide ja autoga */
	const pvRead = $derived.by(() => {
		if (!core || !P) return [];
		const x = arvuta({ ...A, reakt: 0 });
		if (!x || !x.r || !x.r.stopped || !x.r.trace || x.r.trace.length < 2) return [];
		let tL = null;
		if (B) {
			const y = arvuta({ ...B, reakt: 0 });
			if (y && y.r && y.r.stopped && y.r.trace && y.r.trace.length > 1) tL = y.r.trace;
		}
		return [1, 2, 3, 4].map((sek) => [sek, pikivahe(x.r.trace, +A.kiirus, sek, +A.reakt, ees, tL)]);
	});

	/* Kurvi tööriist: oma auto, tee, rehvid ja mustrisügavus ees/taga */
	const kr = $derived.by(() => {
		if (!core || !P) return null;
		const veh = core.byKey[KR.auto];
		if (!veh) return null;
		const pind = KR_PIND.find((x) => x[0] === KR.pind)[2];
		const tyre = (mm) => ({
			key: 'x', name: 'x', category: KR.kat, wetGripIndex: G({ klass: 'C', kat: KR.kat }),
			treadDepthMm: mm, treadDepthNewMm: 8, ageYears: 1, pressureBar: null, loadCapacityKg: null,
			studded: KR.kat === 'WINTER_STUDDED', size: veh.oemSize, gSource: 'label'
		});
		const cond = { speedKmh: +KR.kiirus, texture: 'NORMAL', payloadKg: 75, gradientPct: 0, reactionTimeS: 1, brakeCondition: 1, iceRoad: true, ...pind };
		const k = (f, r) => kaitumine(P, { veh, cond, tyreF: tyre(f), tyreR: tyre(r), R: kurv });
		try {
			return {
				sinu: k(KR.esi, KR.taga),
				vahetatud: KR.esi !== KR.taga ? k(KR.taga, KR.esi) : null,
				uued: KR.esi !== 8 || KR.taga !== 8 ? k(8, 8) : null
			};
		} catch {
			return null;
		}
	});
	const krPiir = $derived(TALV[KR.kat] ? 3 : 1.6);
	function krOtsus(r) {
		if (!kurv) return ['ok', t('Sirgel teel püsib auto otse ja peatub')];
		if (r.kaotus === 'taga') return ['halb', t('Tagaosa libiseb välja — auto pöörab ringi (ülejuhitavus)')];
		if (r.kaotus === 'esi') return ['halb', t('Esirattad libisevad — auto ei pööra ja sõidab kurvist välja (alajuhitavus)')];
		if (Math.min(r.varuTaga, r.varuEsi) < 0.15)
			return r.varuTaga <= r.varuEsi ? ['hoiatus', t('Peatub, aga tagaosa on libisemise piiril')] : ['hoiatus', t('Peatub, aga esirattad on haarde piiril')];
		return ['ok', t('Püsib kurvis ja peatub')];
	}
	/* skemaatiline pealtvaade: tee kaar, auto teekond, peatus või libisemine */
	const krJoon = $derived.by(() => {
		const r = kr?.sinu;
		if (!r) return null;
		const W = 420, H = 300, x0 = 90, y0 = 285;
		const Rpx = { 300: 520, 150: 330, 75: 210, 30: 120 }[kurv] || 0;
		const lopp = r.kaotus ? Math.max(r.kaotusM ?? 0, 0) : r.peatumineM;
		const pikkus = Math.max(40, (r.kaotus ? (r.kaotusM ?? 0) * 1.6 + 25 : r.peatumineM * 1.15));
		const skaala = 300 / pikkus; // px meetri kohta
		const P = (sPx) => {
			if (!Rpx) return [x0 + 110, y0 - sPx, -Math.PI / 2];
			const th = sPx / Rpx; // paremale pöörav kaar, keskpunkt (x0+Rpx, y0)
			return [x0 + Rpx - Rpx * Math.cos(th), y0 - Rpx * Math.sin(th), -Math.PI / 2 + th];
		};
		const tee = [], kulg = [];
		for (let i = 0; i <= 60; i++) tee.push(P((i / 60) * 340));
		const sL = lopp * skaala;
		for (let i = 0; i <= 40; i++) kulg.push(P((i / 40) * sL));
		const [lx, ly, la] = P(sL);
		let jatk = null;
		if (r.kaotus === 'esi') jatk = [[lx, ly], [lx + Math.cos(la) * 120, ly + Math.sin(la) * 120]];
		if (r.kaotus === 'taga') {
			jatk = [];
			let x = lx, y = ly; for (let i = 0; i <= 24; i++) { const a = la - (i / 24) * 1.1; x += Math.cos(a) * 4.2; y += Math.sin(a) * 4.2; jatk.push([x, y]); }
		}
		const pts = (a) => a.map((p) => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
		const auto = r.kaotus === 'taga' ? [jatk[jatk.length - 1][0], jatk[jatk.length - 1][1], la + 2.4] : r.kaotus === 'esi' ? [jatk[1][0], jatk[1][1], la] : [lx, ly, la];
		return { W, H, tee: pts(tee), kulg: pts(kulg), jatk: jatk ? pts(jatk) : null, auto: [auto[0], auto[1], (auto[2] * 180) / Math.PI + 90], kaotus: r.kaotus, stop: [lx, ly] };
	});
</script>

<div class="lo" class:proj={esitlus} bind:this={juur}>
	{#if viga}<p class="lo-viga">{viga}</p>{/if}

	<nav class="lo-vaated" aria-label={t('Kalkulaatorid')}>
		{#each VAATED as [id, tee, nimi] (id)}
			<a href={keel.L(tee)} aria-current={vaade === id ? 'page' : undefined} onclick={(e) => (e.currentTarget.href = keel.L(tee) + location.hash)}>{nimi}</a>
		{/each}
	</nav>

	<div class="lo-top">
		{#if vaade === 'pimedas'}
			<div class="lo-naited lo-naeb-top" role="group" aria-label={t('Jalakäija pimedas')}>
				<span class="lo-lbl">{t('Jalakäija pimedas — kust juht teda märkab:')}</span>
				{#each NAHT as [id, d, nimi] (id)}
					<button type="button" aria-pressed={naeb === id} onclick={() => setNaeb(id)}>{nimi} <small>~{d} {t('m')}</small></button>
				{/each}
			</div>
		{:else if vaade === 'peatumine'}
		<div class="lo-naited" aria-label={t("Näidisvõrdlused")}>
			<span class="lo-lbl">{t("Valmis võrdlused:")}</span>
			<button type="button" onclick={() => naide('kiirus')}>{t("50 vs 70 km/h")}</button>
			<button type="button" onclick={() => naide('telefon')}>{t("Tähelepanelik vs hajevil")}</button>
			<button type="button" onclick={() => naide('muster')}>{t("Uus vs kulunud rehv")}</button>
			<button type="button" onclick={() => naide('vesi')}>{t("Märg vs lombid")}</button>
			<button type="button" onclick={() => naide('lumi')}>{t("Suverehv lumel")}</button>
			<button type="button" onclick={() => naide('jaa')}>{t("Jää −10 °C vs 0 °C")}</button>
		</div>
		{:else}
			<div></div>
		{/if}
		<div class="lo-tools">
			<button type="button" class="lo-tool" onclick={kopeeri}>{kopeeritud ? t('Link kopeeritud') : t('Kopeeri link')}</button>
			<button type="button" class="lo-tool" aria-pressed={esitlus} onclick={esitlusrezim}>{esitlus ? t('Välju esitlusest') : t('Esitlusrežiim')}</button>
		</div>
	</div>

	<div class="lo-grid">
		<!-- ================= SISENDID ================= -->
		{#if vaade === 'kurv'}
		<section class="lo-in" aria-label={t('Olukord')}>
			<fieldset>
				<legend>{t('Kurv')}</legend>
				<div class="lo-kurvid">
					{#each KURV as [r, nimi, vihje] (r)}
						<button type="button" aria-pressed={kurv === r} onclick={() => (kurv = r)}>
							<svg viewBox="0 0 40 40" aria-hidden="true"><path d={r === 0 ? 'M20 38 L20 2' : r === 300 ? 'M12 38 Q14 10 34 4' : r === 150 ? 'M10 38 Q10 12 36 8' : r === 75 ? 'M8 38 Q8 16 36 14' : 'M8 38 Q8 24 36 24'} /></svg>
							<span><b>{nimi}</b>{#if vihje}<small>{vihje}</small>{/if}</span>
						</button>
					{/each}
				</div>
			</fieldset>
			<fieldset>
				<legend>{t('Kiirus ja tee')}</legend>
				<label class="lo-row" for="kr-kiirus"><span>{t('Kiirus')}</span><b class="lo-val">{KR.kiirus} {t('km/h')}</b></label>
				<input id="kr-kiirus" class="slider" type="range" min="20" max="130" step="5" bind:value={KR.kiirus} style="--p:{((KR.kiirus - 20) / 110) * 100}%" />
				<div class="lo-seg lo-seg4">
					{#each KR_PIND as [k, n] (k)}
						<button type="button" aria-pressed={KR.pind === k} onclick={() => (KR.pind = k)}>{n}</button>
					{/each}
				</div>
			</fieldset>
			<fieldset>
				<legend>{t('Rehvid')}</legend>
				<div class="lo-seg lo-seg3">
					{#each KR_KAT as [k, n] (k)}
						<button type="button" aria-pressed={KR.kat === k} onclick={() => (KR.kat = k)}>{n}</button>
					{/each}
				</div>
				<label class="lo-row" for="kr-esi"><span>{t('Esirehvide muster')}</span><b class="lo-val" class:lo-halb={KR.esi < krPiir}>{f1(KR.esi)} {t('mm')}</b></label>
				<input id="kr-esi" class="slider" type="range" min="1" max="8" step="0.5" bind:value={KR.esi} style="--p:{((KR.esi - 1) / 7) * 100}%" />
				<label class="lo-row" for="kr-taga"><span>{t('Tagarehvide muster')}</span><b class="lo-val" class:lo-halb={KR.taga < krPiir}>{f1(KR.taga)} {t('mm')}</b></label>
				<input id="kr-taga" class="slider" type="range" min="1" max="8" step="0.5" bind:value={KR.taga} style="--p:{((KR.taga - 1) / 7) * 100}%" />
				<p class="lo-kr-vihje">{t('Uus rehv 8 mm. Seaduse piir: suverehv 1,6 mm, talverehv 3 mm.')}</p>
			</fieldset>
			<fieldset>
				<legend>{t('Auto')}</legend>
				<div class="lo-seg lo-seg2">
					{#each KR_AUTO as [k, n] (k)}
						<button type="button" aria-pressed={KR.auto === k} onclick={() => (KR.auto = k)}>{n}</button>
					{/each}
				</div>
			</fieldset>
		</section>
		{:else}
		<section class="lo-in" aria-label={t("Olukord")}>
			<div class="lo-tabs">
				<div class="lo-tablist" role="tablist" aria-label={t("Olukord")}>
					<button type="button" role="tab" aria-selected={muuda === 'A'} class="t-a" onclick={() => (muuda = 'A')}>{vaade === 'pikivahe' ? t('Sina') : t("Olukord A")}</button>
					{#if B}
						<button type="button" role="tab" aria-selected={muuda === 'B'} class="t-b" onclick={() => (muuda = 'B')}>{vaade === 'pikivahe' ? t('Eesolev auto') : t("Olukord B")}</button>
					{/if}
				</div>
				{#if B}
					<button type="button" class="lo-x" onclick={eemaldaB} aria-label={t("Eemalda olukord B")}>×</button>
				{:else}
					<button type="button" class="lo-add" onclick={lisaB}>{vaade === 'pikivahe' ? t('+ Eesolev auto erineb') : t("+ Lisa võrdlus")}</button>
				{/if}
			</div>

			<fieldset>
				<legend>{t("Kiirus ja juht")}</legend>
				<label class="lo-row" for="lo-kiirus">
					<span>{t("Kiirus")}</span>
					<b class="lo-val">{S.kiirus} {t("km/h")}</b>
				</label>
				<input id="lo-kiirus" class="slider" type="range" min="10" max="150" step="5" bind:value={S.kiirus} style="--p:{((S.kiirus - 10) / 140) * 100}%" />
				<label class="lo-row" for="lo-reakt">
					<span>{t("Reaktsiooniaeg")}</span>
					<b class="lo-val">{f1(S.reakt)} {t("s")}</b>
				</label>
				<input id="lo-reakt" class="slider" type="range" min="0" max="3" step="0.1" bind:value={S.reakt} style="--p:{(S.reakt / 3) * 100}%" />
				<div class="lo-chips">
					{#each REAKT as [rt, n]}
						<button type="button" aria-pressed={Math.abs(S.reakt - rt) < 0.05} onclick={() => (S.reakt = rt)}>{f1(rt)} {t("s")} <small>{n}</small></button>
					{/each}
				</div>
			</fieldset>

			<fieldset>
				<legend>{t("Tee")}</legend>
				<div class="lo-seg lo-seg6">
					{#each PIND as [k, n]}
						<button type="button" aria-pressed={S.pind === k} onclick={() => setPind(S, k)}>{n}</button>
					{/each}
				</div>
				{#if ASF[S.pind]}
					<span class="lo-sub">{t("Vesi teel")}</span>
					<div class="lo-seg lo-seg5">
						{#each VESI as [w, n]}
							<button type="button" aria-pressed={Math.abs(S.vesi - w) < 0.01} onclick={() => setVesi(S, w)}>{n}<small>{String(w).replace('.', ',')} {t("mm")}</small></button>
						{/each}
					</div>
					<label class="lo-row" for="lo-tekst"><span>{t("Teekate")}</span></label>
					<select id="lo-tekst" class="lo-sel" bind:value={S.tekst}>
						{#each TEKST as [k, n]}<option value={k}>{autoNimi(keel.lang, n)}</option>{/each}
					</select>
				{/if}
				{#if S.pind === 'ICE'}
					<label class="lo-row" for="lo-jaa"><span>{t("Jää")}</span></label>
					<select id="lo-jaa" class="lo-sel" bind:value={S.jaa}>
						<option value="tee">{t("Tavaline teejää (rööpad, liiv, karedus)")}</option>
						<option value="sile">{t("Sile jää (kiilasjää, must jää)")}</option>
					</select>
				{/if}
				<label class="lo-row" for="lo-temp">
					<span>{t("Teepinna temperatuur")}</span>
					<b class="lo-val">{S.temp > 0 ? '+' : ''}{S.temp} °C</b>
				</label>
				<input id="lo-temp" class="slider" type="range" min={tMin} max={tMax} step="1" bind:value={S.temp} style="--p:{((S.temp - tMin) / (tMax - tMin)) * 100}%" />
				<label class="lo-row" for="lo-kalle">
					<span>{t("Tee kalle")}</span>
					<b class="lo-val">{S.kalle === 0 ? t('tasane') : (S.kalle < 0 ? t('allamäge ') : t('ülesmäge ')) + Math.abs(S.kalle) + ' %'}</b>
				</label>
				<input id="lo-kalle" class="slider" type="range" min="-12" max="12" step="1" bind:value={S.kalle} style="--p:{((S.kalle + 12) / 24) * 100}%" />
			</fieldset>

			<fieldset>
				<legend>{t("Rehvid")}</legend>
				<label class="lo-row" for="lo-kat"><span>{t("Rehvi tüüp")}</span></label>
				<select id="lo-kat" class="lo-sel" bind:value={S.kat}>
					{#each KAT as [k, n]}<option value={k}>{autoNimi(keel.lang, n)}</option>{/each}
				</select>
				{#if S.kat !== 'WINTER_STUDDED'}
					<span class="lo-sub">{t("Märghaarde klass (EL-i rehvimärgis)")}</span>
					<div class="lo-seg lo-seg5">
						{#each ['A', 'B', 'C', 'D', 'E'] as k}
							<button type="button" aria-pressed={S.klass === k} onclick={() => (S.klass = k)}>{k}</button>
						{/each}
					</div>
				{/if}
				<span class="lo-sub">{t("Rehvi seisukord")}</span>
				<div class="lo-seg lo-seg3">
					<button type="button" aria-pressed={S.muster === 8 && S.vanus === 1} onclick={() => seisund(S, 'uus')}>{t("Uus")}</button>
					<button type="button" aria-pressed={S.muster === 4.5 && S.vanus === 6} onclick={() => seisund(S, 'kesk')}>{t("Keskmiselt kulunud")}</button>
					<button type="button" aria-pressed={S.vanus === 10 && (S.muster === 1.6 || S.muster === 3)} onclick={() => seisund(S, 'piir')}>{t("Seaduse piiril")}</button>
				</div>
				<label class="lo-row" for="lo-muster">
					<span>{t("Mustrisügavus")}</span>
					<b class="lo-val" class:lo-halb={S.muster < (TALV[S.kat] ? 3 : 1.6)}>{f1(S.muster)} {t("mm")}</b>
				</label>
				<input id="lo-muster" class="slider" type="range" min="0.5" max="8" step="0.5" bind:value={S.muster} style="--p:{((S.muster - 0.5) / 7.5) * 100}%" />
				<label class="lo-row" for="lo-vanus">
					<span>{t("Rehvi vanus")}</span>
					<b class="lo-val">{S.vanus} {S.vanus === 1 ? t('aasta') : S.vanus < 5 && keel.lang === 'ru' ? 'года' : t('aastat')}</b>
				</label>
				<input id="lo-vanus" class="slider" type="range" min="0" max="15" step="1" bind:value={S.vanus} style="--p:{(S.vanus / 15) * 100}%" />
				<label class="lo-row" for="lo-rohk">
					<span>{t("Rehvirõhk")}</span>
					<b class="lo-val">{S.rohk === 0 ? t('soovituslik') : (S.rohk > 0 ? '+' : '−') + f1(Math.abs(S.rohk)) + ' bar'}</b>
				</label>
				<input id="lo-rohk" class="slider" type="range" min="-1" max="0.6" step="0.1" bind:value={S.rohk} style="--p:{((S.rohk + 1) / 1.6) * 100}%" />
			</fieldset>

			<fieldset>
				<legend>{t("Auto")}</legend>
				<label class="lo-row" for="lo-mk"><span>{t("Mark")}</span></label>
				<select id="lo-mk" class="lo-sel" bind:value={S.mk} onchange={() => { S.md = mudelid[0] || ''; S.veh = polved[0]?.[0] || ''; S.abs = 'auto'; }}>
					<option value="">{t("Tüüpauto (mark pole oluline)")}</option>
					{#each margid as mk}<option value={mk}>{mk}</option>{/each}
				</select>
				{#if !S.mk}
					<label class="lo-row" for="lo-tyyp"><span>{t("Auto tüüp")}</span></label>
					<select id="lo-tyyp" class="lo-sel" bind:value={S.tyyp}>
						{#each tyybid as v}<option value={v.key}>{t(v.name)}</option>{/each}
					</select>
				{:else}
					<div class="lo-two">
						<div>
							<label class="lo-row" for="lo-md"><span>{t("Mudel")}</span></label>
							<select id="lo-md" class="lo-sel" bind:value={S.md} onchange={() => { S.veh = polved[0]?.[0] || ''; S.abs = 'auto'; }}>
								<option value="">{t("Vali")}</option>
								{#each mudelid as md}<option value={md}>{autoNimi(keel.lang, md)}</option>{/each}
							</select>
						</div>
						<div>
							<label class="lo-row" for="lo-veh"><span>{t("Põlvkond")}</span></label>
							<select id="lo-veh" class="lo-sel" bind:value={S.veh} disabled={!S.md} onchange={() => (S.abs = 'auto')}>
								{#each polved as [k, n]}<option value={k}>{autoNimi(keel.lang, n)}</option>{/each}
							</select>
						</div>
					</div>
				{/if}
				{#if auto(S)}
					{@const v = core.byKey[S.mk ? S.veh : S.tyyp]}
					<label class="lo-row" for="lo-abs"><span>ABS</span></label>
					<select id="lo-abs" class="lo-sel" bind:value={S.abs}>
						{#if v.absOpt}
							<option value="auto">{t("ABS-ita (oli lisavarustus)")}</option>
							<option value="jah">{t("ABS-iga")}</option>
						{:else if v.absClass === 'NONE'}
							<option value="auto">{t("ABS-ita (autol ABS-i ei olnud)")}</option>
						{:else}
							<option value="auto">{t("ABS-iga")}</option>
							<option value="ei">{t("ABS-ita (rattad lukustuvad)")}</option>
						{/if}
					</select>
				{/if}
				<label class="lo-row" for="lo-laad">
					<span>{t("Koormus (juht, reisijad, pagas)")}</span>
					<b class="lo-val">{S.laad} {t("kg")}</b>
				</label>
				<input id="lo-laad" class="slider" type="range" min="75" max="600" step="25" bind:value={S.laad} style="--p:{((S.laad - 75) / 525) * 100}%" />
				<label class="lo-row" for="lo-pidur"><span>{t("Pidurite seisukord")}</span></label>
				<select id="lo-pidur" class="lo-sel" bind:value={S.pidur}>
					{#each PIDUR as [k, n]}<option value={k}>{autoNimi(keel.lang, n)}</option>{/each}
				</select>
			</fieldset>
		</section>
		{/if}

		<!-- ================= TULEMUS ================= -->
		{#if vaade === 'pikivahe'}
		{#if !core}<p class="lo-laeb">{t("Laadin arvutusmudelit…")}</p>{:else if pvRead.length}
		<section class="lo-kt lo-pv lo-side" aria-labelledby="lo-pv-h">
			<h2 id="lo-pv-h">{t('Pikivahe')}</h2>
			<p class="lo-kt-sub">
				{#if ees === 'seisab'}{t('Sõidad {v} km/h teise auto taga. Tema peatub hetkega (sõidab millelegi otsa), sina reageerid {r} s pärast ja pidurdad. Kas jõuad peatuda?', { v: A.kiirus, r: f1(A.reakt) })}{:else}{#if B}{t('Sõidad {v} km/h teise auto taga. Tema ({b} km/h) pidurdab järsult oma auto ja rehvidega (vasakul „Eesolev auto“), sina reageerid {r} s pärast. Kas jõuad peatuda?', { v: A.kiirus, b: B.kiirus, r: f1(A.reakt) })}{:else}{t('Sõidad {v} km/h teise auto taga. Tema pidurdab järsult, sina reageerid {r} s pärast ja pidurdad sama autoga samal teel. Kas jõuad peatuda?', { v: A.kiirus, r: f1(A.reakt) })}{/if}{/if}
			</p>
			<div class="lo-kt-ctl">
				<div class="lo-kt-seg" role="group" aria-label={t('Eesolev auto')}>
					<span>{t('Eesolev auto:')}</span>
					<button type="button" aria-pressed={ees === 'pidurdab'} onclick={() => (ees = 'pidurdab')}>{t('pidurdab järsult')}</button>
					<button type="button" aria-pressed={ees === 'seisab'} onclick={() => (ees = 'seisab')}>{t('peatub kohe (sõidab millelegi otsa)')}</button>
				</div>
			</div>
			<div class="tbl-wrap">
				<table class="lo-kt-t">
					<thead>
						<tr>
							<th>{t('Pikivahe')}</th>
							<th class="n">{t('Vahe meetrites')}</th>
							<th>{t('Mis juhtub')}</th>
						</tr>
					</thead>
					<tbody>
						{#each pvRead as [sek, x] (sek)}
							{@const napp = x.kokkuporge && x.loogKmh < 2}
							<tr>
								<td class="nw lo-kt-nimi"><b>{sek} {t('s')}</b></td>
								<td class="n nw" data-l={t('Vahe meetrites')}>{f0(x.vaheM)} {t('m')}</td>
								<td class="lo-kt-ots">
									{#if napp}
										<span class="lo-kt-o lo-kt-hoiatus">{t('Peatud vahetult tema taga — varu ei jää')}</span>
									{:else if x.kokkuporge}
										<span class="lo-kt-o lo-kt-halb">{t('Kokkupõrge {k} km/h', { k: f0(x.loogKmh) })}</span>
										<small class="lo-kt-varu">
											{#if x.temaKmh > 1}{t('Sinu kiirus {s} km/h, eesoleval autol veel {e} km/h.', { s: f0(x.sinuKmh), e: f0(x.temaKmh) })}{:else}{t('Eesolev auto juba seisab, sina sõidad veel {s} km/h.', { s: f0(x.sinuKmh) })}{/if}
										</small>
									{:else}
										<span class="lo-kt-o lo-kt-ok">{t('Peatud {m} m tema taga', { m: m(x.jaabM) })}</span>
									{/if}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
			<p class="lo-kt-note">
				{t('Levinud rusikareegel on vähemalt 2 sekundit, märjal ja libedal teel rohkem. Kui sinu reageerimisaeg on pikem kui pikivahe, sõidad eesolevale autole sisse ka siis, kui pidurdate täpselt ühtemoodi. Muuda vasakul kiirust, reageerimisaega ja teeolusid.')}
				{#if !B}{t('Eesoleva auto saad muuta vasakul („+ Eesolev auto erineb“): näiteks uute rehvidega auto pidurdab lühemalt ja kulunud rehvidega sina jõuad talle sisse ka 2 sekundi vahega.')}{/if}
			</p>
		</section>
		{/if}
		{:else if vaade === 'kurv'}
		{#if !core}<p class="lo-laeb">{t("Laadin arvutusmudelit…")}</p>{:else if kr}
		{@const ots = krOtsus(kr.sinu)}
		<section class="lo-kt lo-side" aria-labelledby="lo-kt-h">
			<h2 id="lo-kt-h">{t('Äkkpidurdus kurvis')}</h2>
			<p class="lo-kt-sub">{t('Sõidad {v} km/h, ees {e} mm ja taga {r} mm mustriga rehvid. Kurvis tuleb ootamatult takistus ja pidurdad täiest jõust (reageerimisaeg 1 s).', { v: KR.kiirus, e: f1(KR.esi), r: f1(KR.taga) })}</p>
			<div class="lo-kr-tulemus lo-kt-{ots[0]}">
				<p class="lo-kr-ots">{ots[1]}</p>
				<dl class="lo-kr-nr">
					{#if kurv}<div><dt>{t('Selle kurvi piirkiirus')}</dt><dd>{f0(kr.sinu.piirKmh)} {t('km/h')}</dd></div>{/if}
					<div><dt>{t('Peatumisteekond')}</dt><dd>{kr.sinu.peatumineM != null ? m(kr.sinu.peatumineM) + ' ' + t('m') : t('ei peatu kurvis')}</dd></div>
					{#if kr.sinu.kaotus}<div><dt>{t('Haare kaob')}</dt><dd>{kr.sinu.kaotusM ? t('{m} m pärast, kiirusel {k} km/h', { m: f0(kr.sinu.kaotusM), k: f0(kr.sinu.kaotusKmh) }) : t('kohe kurvi sisenedes')}</dd></div>{/if}
				</dl>
				{#if kurv && !kr.sinu.kaotus}<p class="lo-kt-varu">{t('Haardevaru kurvi hoidmiseks: ees {e} %, taga {r} %', { e: f0(kr.sinu.varuEsi * 100), r: f0(kr.sinu.varuTaga * 100) })}</p>{/if}
				{#if kurv && kr.sinu.kaotus && KR.kiirus > kr.sinu.piirKmh}<p class="lo-kt-varu">{t('Kiirus on selle kurvi jaoks liiga suur ka ilma pidurdamata.')}</p>{/if}
			</div>
			{#if krJoon}
				<figure class="lo-kr-fig">
					<svg viewBox="0 0 {krJoon.W} {krJoon.H}" role="img" aria-label={t('Auto teekond pealtvaates')}>
						<polyline points={krJoon.tee} class="kr-tee" />
						<polyline points={krJoon.tee} class="kr-joon" />
						<polyline points={krJoon.kulg} class="kr-kulg" />
						{#if krJoon.jatk}<polyline points={krJoon.jatk} class="kr-jatk" />{/if}
						{#if !krJoon.kaotus}<circle cx={krJoon.stop[0]} cy={krJoon.stop[1]} r="7" class="kr-stop" />{/if}
						<g transform="translate({krJoon.auto[0]} {krJoon.auto[1]}) rotate({krJoon.auto[2]})"><rect x="-9" y="-16" width="18" height="32" rx="5" class="kr-auto" class:halb={!!krJoon.kaotus} /><rect x="-6" y="-12" width="12" height="7" rx="2" class="kr-klaas" /></g>
					</svg>
					<figcaption>{t('Skeem pealtvaates, mitte mõõtkavas.')}</figcaption>
				</figure>
			{/if}
			{#if kr.vahetatud || kr.uued}
				<h3 class="lo-kr-h3">{t('Võrdle')}</h3>
				<div class="tbl-wrap">
					<table class="lo-kt-t">
						<thead><tr><th>{t('Rehvid')}</th><th class="n">{t('Peatumisteekond')}</th><th>{t('Mis juhtub')}</th></tr></thead>
						<tbody>
							{#each [[t('Sinu valik: ees {e} mm, taga {r} mm', { e: f1(KR.esi), r: f1(KR.taga) }), kr.sinu], ...(kr.vahetatud ? [[t('Rehvid vahetatud: ees {e} mm, taga {r} mm', { e: f1(KR.taga), r: f1(KR.esi) }), kr.vahetatud]] : []), ...(kr.uued ? [[t('Kõik neli uued (8 mm)'), kr.uued]] : [])] as [nimi, r], i (i)}
								{@const o = krOtsus(r)}
								<tr>
									<td class="lo-kt-nimi"><b>{nimi}</b></td>
									<td class="n nw" data-l={t('Peatumisteekond')}>{r.peatumineM != null ? m(r.peatumineM) + ' ' + t('m') : '—'}</td>
									<td class="lo-kt-ots"><span class="lo-kt-o lo-kt-{o[0]}">{o[1]}</span></td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}
			<p class="lo-kt-note">
				{t('Paremad rehvid pane tagasillale: kui tagarattad kaotavad haarde, pöörab auto ringi ja seda on palju raskem päästa kui otse sõitvat autot. Nii soovitavad ka ADAC, TCS ja ÖAMTC oma katsete põhjal.')}
				{t('Lihtsustatud füüsikamudel: rehvi haare tuleb samast mudelist mis kalkulaatoris, pidurdusjõud jaguneb umbes 72 % ette ja 28 % taha, kurv on ühtlane. ESP-d mudel ei arvesta — ESP aitab autot hoida, aga haaret juurde ei tee.')}
			</p>
		</section>
		{/if}
		{:else}
		<section class="lo-out" aria-live="polite" aria-label={t("Tulemus")} bind:this={outEl}>
			{#if !core}
				<p class="lo-laeb">{t("Laadin arvutusmudelit…")}</p>
			{:else}
				<div class="lo-resgrid" class:two={!!B}>
				{#each [['A', RA], ...(B ? [['B', RB]] : [])] as [n, x]}
					<div class="lo-res" class:lo-b={n === 'B'}>
						<div class="lo-res-h">
							<span class="lo-tag">{n}</span>
							{#if x && x.err}
								<span class="lo-err">{t("Seda olukorda ei saa arvutada:")} {x.err}</span>
							{:else if x && x.r}
								<span class="lo-res-sub">{(n === 'A' ? A : B).kiirus} {t("km/h ·")} {PIND.find((p) => p[0] === (n === 'A' ? A : B).pind)[1].toLowerCase()} · {autoNimi(keel.lang, t(x.veh.name))}</span>
							{/if}
						</div>
						{#if x && x.r}
							{#if !x.r.stopped}
								<p class="lo-big lo-nostop">{t("Auto ei peatu")}</p>
								<p class="lo-note">{t("Selle kalde ja haardega ei suuda rehvid autot peatada — auto libiseb edasi.")}</p>
							{:else}
								<p class="lo-big">{m(x.r.totalDistanceM)} <small>{t("m")}</small></p>
								<p class="lo-kokku">{t("peatumisteekond")}</p>
								<dl class="lo-split">
									<div><dt>{t("Reageerimisteekond")}</dt><dd>{m(x.r.reactionM)} {t("m")}</dd></div>
									<div><dt>{t("Pidurdusteekond")}</dt><dd>{m(x.r.distanceM)} {t("m")}</dd></div>
									<div><dt>{t("Aeg seisuni")}</dt><dd>{f1(x.r.timeS)} {t("s")}</dd></div>
									<div><dt>{t("Tõenäoline vahemik")}</dt><dd>{m(x.r.lowM)}–{m(x.r.highM)} {t("m")}</dd></div>
								</dl>
							{/if}
							{#if x.r.warnings.length}
								<ul class="lo-warn">
									{#each x.r.warnings as w}<li>{w}</li>{/each}
								</ul>
							{/if}
						{/if}
					</div>
				{/each}
				</div>

				<div class="lo-actions">
					{#if !B}
						<button type="button" class="lo-addb" onclick={lisaB}>{t("+ Lisa võrdlus: olukord B")}</button>
					{:else}
						<span>{t("Muudad:")}</span>
						<button type="button" class="lo-sw" aria-pressed={muuda === 'A'} onclick={() => (muuda = 'A')}>A</button>
						<button type="button" class="lo-sw lo-sw-b" aria-pressed={muuda === 'B'} onclick={() => (muuda = 'B')}>B</button>
						<button type="button" class="lo-rm" onclick={eemaldaB}>{t("Eemalda B")}</button>
					{/if}
				</div>

				{#if stsenaariumid.length}
					<figure class="lo-fig" bind:clientWidth={figW}>
						<svg width={W} viewBox="0 0 {W} {60 + stsenaariumid.length * 70}" role="img" aria-label={t("Peatumisteekond teel meetrites")}>
							<defs>
								<pattern id="lo-hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
									<rect width="10" height="10" fill="#3a3f49" />
									<line x1="0" y1="0" x2="0" y2="10" stroke="#5c6370" stroke-width="4" />
								</pattern>
							</defs>
							{#each tikid as tk}
								<line x1={X(tk)} x2={X(tk)} y1="18" y2={40 + stsenaariumid.length * 70} class="lo-grid-l" />
								<text x={X(tk)} y="10" class="lo-tick">{tk} {t("m")}</text>
							{/each}
							{#each stsenaariumid as [n, x], i}
								{@const y = 30 + i * 70}
								{@const kokku = x.r.stopped ? x.r.totalDistanceM : maxD}
								<text x="4" y={y + 30} class="lo-rowlbl">{n}</text>
								<rect x={X(0)} y={y + 10} width={Math.max(0, X(x.r.reactionM) - X(0))} height="28" fill="url(#lo-hatch)" rx="3" />
								<rect x={X(x.r.reactionM)} y={y + 10} width={Math.max(0, X(kokku) - X(x.r.reactionM))} height="28" class={n === 'A' ? 'lo-bar-a' : 'lo-bar-b'} rx="3" />
								{#if x.r.stopped}
									<line x1={X(kokku)} x2={X(kokku)} y1={y + 4} y2={y + 44} class="lo-stop" />
									<text x={Math.min(X(kokku) + 6, W - 4)} y={y + 58} class="lo-endlbl" text-anchor={X(kokku) > W - 70 ? 'end' : 'start'}>{m(kokku)} {t("m")}</text>
								{/if}
								{#if X(x.r.reactionM) - X(0) > 96}
									<text x={(X(0) + X(x.r.reactionM)) / 2} y={y + 30} class="lo-inlbl">{t("reageerimine")}</text>
								{/if}
								{#if X(kokku) - X(x.r.reactionM) > 90}
									<text x={(X(x.r.reactionM) + X(kokku)) / 2} y={y + 30} class="lo-inlbl lo-dark">{t("pidurdamine")}</text>
								{/if}
							{/each}
							{#if takistus > 0}
								<line x1={X(takistus)} x2={X(takistus)} y1="18" y2={40 + stsenaariumid.length * 70} class="lo-obst" />
								<text x={X(takistus) - 4} y={36 + stsenaariumid.length * 70} class="lo-obstlbl" text-anchor="end">{NAEB ? t('jalakäija') : t("takistus")}</text>
							{/if}
						</svg>
						<figcaption>{@html t("<span class=\"lo-key lo-key-r\"></span> reageerimisteekond (auto sõidab täiskiirusel) <span class=\"lo-key lo-key-p\"></span> pidurdusteekond")}</figcaption>
					</figure>
				{/if}

				<div class="lo-obst-in">
					<label for="lo-tak">{t("Takistus tee peal (nt teele jooksev laps) kaugusel")}</label>
					<div class="lo-obst-row">
						<input id="lo-tak" type="number" min="0" max="500" step="1" bind:value={takistus} oninput={() => (naeb = '')} placeholder="0" />
						<span>{t("m")}</span>
						{#if takistus > 0}<button type="button" class="lo-tool" onclick={() => { takistus = 0; naeb = ''; }}>{t("Eemalda")}</button>{/if}
					</div>
					{#if NAEB}
						<p class="lo-naeb-t">{t('Pimedas märkab juht jalakäijat alles umbes')} <b>{NAEB[1]} {t('m')}</b> {t('kauguselt (Transpordiamet). Takistus on pandud sinna.')}</p>
					{/if}
					{#each tak as [n, v]}
						<p class="lo-impact" class:ok={v === 0}>
							<span class="lo-tag sm" class:lo-tag-b={n === 'B'}>{n}</span>
							{#if v === 0}
								{t("Peatub enne takistust.")}
							{:else}
								{t("Jõuab takistuseni kiirusega")} <b>{f0(v)} {t("km/h")}</b>. {look(v)}
							{/if}
						</p>
					{/each}
					{#each vmaxid as [n, vm] (n)}
						<p class="lo-impact lo-vmax">
							<span class="lo-tag sm" class:lo-tag-b={n === 'B'}>{n}</span>
							{#if vm >= 160}{t('Jõuab peatuda igal mõistlikul kiirusel.')}{:else}{t('Et jõuda peatuda, tohib kiirus olla kuni')} <b>{vm} {t("km/h")}</b>.{/if}
						</p>
					{/each}
				</div>

				{#if vordlus}
					<div class="lo-cmp">
						<p>
							<b>{vordlus.Pk}</b> {t("vajab peatumiseks")} <b>{m(vordlus.vahe)} {t("m")}</b> {t("rohkem.")}
							{#if vordlus.v > 0.5 && !(takistus > 0)}
								{t("Kohas, kus")} <b>{vordlus.L}</b> {t("juba seisab (")}{m(vordlus.koht)} {t("m), sõidab")} <b>{vordlus.Pk}</b> {t("veel")}
								<b>{f0(vordlus.v)} {t("km/h")}</b>. {look(vordlus.v)}
							{/if}
						</p>
					</div>
				{/if}
			{/if}
		</section>
		{/if}
	</div>

	{#if core && !esitlus && teeVaade}
		<div class="lo-mini" class:peidus={tulemusNahtav}>
			<button type="button" class="lo-mini-res" onclick={naitaTulemust} aria-label={t("Näita tulemust")}>
				<span class="lo-tag sm">A</span><b>{RA?.r ? (RA.r.stopped ? m(RA.r.totalDistanceM) + ' m' : t('ei peatu')) : '—'}</b>
				{#if B}<span class="lo-tag sm lo-tag-b">B</span><b>{RB?.r ? (RB.r.stopped ? m(RB.r.totalDistanceM) + ' m' : t('ei peatu')) : '—'}</b>{/if}
				<span class="lo-mini-up">{t("Tulemus ↑")}</span>
			</button>
			{#if B}
				<div class="lo-mini-sw" role="group" aria-label={t("Mida muudad")}>
					<button type="button" aria-pressed={muuda === 'A'} onclick={() => (muuda = 'A')}>A</button>
					<button type="button" class="b" aria-pressed={muuda === 'B'} onclick={() => (muuda = 'B')}>B</button>
				</div>
			{:else}
				<button type="button" class="lo-mini-add" onclick={lisaB}>{t("+ Võrdle")}</button>
			{/if}
		</div>
	{/if}
</div>

<style>
	.lo {
		--lo-bg: var(--paper-2);
		--lo-card: #fff;
		--lo-b: #5aa9ff;
		padding: var(--sp-6) 0 var(--sp-10);
	}
	.lo.proj {
		background: var(--lo-bg);
		overflow: auto;
		padding: var(--sp-6);
		font-size: 19px;
	}
	.lo-viga {
		background: #fdecec;
		border: 1px solid #f3b4b4;
		padding: var(--sp-3) var(--sp-4);
		border-radius: var(--r-sm);
	}
	.lo-top {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-3);
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--sp-4);
	}
	.lo-naited {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-2);
		align-items: center;
	}
	.lo-lbl {
		font-size: 13px;
		font-weight: 700;
		color: var(--muted);
		text-transform: uppercase;
		letter-spacing: 0.06em;
	}
	.lo-naited button,
	.lo-tool {
		border: 1px solid var(--line);
		background: #fff;
		border-radius: 999px;
		padding: 6px 14px;
		font-size: 14px;
		font-weight: 600;
		cursor: pointer;
	}
	.lo-naited button:hover,
	.lo-tool:hover {
		border-color: #b9bfc9;
	}
	.lo-tools {
		display: flex;
		gap: var(--sp-2);
	}
	.lo-tool[aria-pressed='true'] {
		background: var(--ink);
		color: #fff;
		border-color: var(--ink);
	}
	.lo-grid {
		display: grid;
		grid-template-columns: minmax(300px, 420px) 1fr;
		gap: var(--sp-5);
		align-items: start;
	}
	@media (max-width: 900px) {
		.lo-grid {
			grid-template-columns: 1fr;
		}
		.lo-out {
			order: -1;
			position: static !important;
		}
		.lo {
			padding-bottom: 96px;
		}
	}
	/* tegevusrida tulemuse all */
	.lo-actions {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--sp-2);
		margin-top: var(--sp-4);
		color: var(--muted-d);
		font-size: 14px;
	}
	.lo-addb {
		border: 2px dashed #5aa9ff;
		background: rgba(90, 169, 255, 0.08);
		color: #cfe6ff;
		border-radius: 10px;
		padding: 10px 16px;
		font-weight: 700;
		cursor: pointer;
		width: 100%;
	}
	.lo-sw,
	.lo-rm {
		border: 1px solid #454b57;
		background: #1d2027;
		color: #fff;
		border-radius: 8px;
		padding: 6px 14px;
		font-weight: 800;
		cursor: pointer;
	}
	.lo-sw[aria-pressed='true'] {
		background: var(--yellow);
		color: var(--yellow-ink);
		border-color: var(--yellow);
	}
	.lo-sw-b[aria-pressed='true'] {
		background: #5aa9ff;
		border-color: #5aa9ff;
		color: #04121f;
	}
	.lo-rm {
		margin-left: auto;
		font-weight: 600;
		color: var(--muted-d);
	}
	/* telefoni alariba: tulemus nähtav ka siis, kui kerid sisendeid */
	.lo-mini {
		display: none;
	}
	@media (max-width: 900px) {
		.lo-mini {
			display: flex;
			position: fixed;
			left: 0;
			right: 0;
			bottom: 0;
			z-index: 40;
			gap: var(--sp-2);
			align-items: center;
			padding: 10px 12px calc(10px + env(safe-area-inset-bottom, 0px));
			background: var(--ink);
			color: #fff;
			box-shadow: 0 -8px 24px rgba(0, 0, 0, 0.35);
			transition: transform 0.2s;
		}
		.lo-mini.peidus {
			transform: translateY(110%);
		}
	}
	.lo-mini-res {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 6px;
		border: 0;
		background: transparent;
		color: #fff;
		font-size: 18px;
		cursor: pointer;
		padding: 0;
		min-width: 0;
	}
	.lo-mini-res b {
		font-variant-numeric: tabular-nums;
		margin-right: 8px;
	}
	.lo-mini-up {
		margin-left: auto;
		font-size: 13px;
		color: var(--muted-d);
		white-space: nowrap;
	}
	.lo-mini-sw {
		display: flex;
		gap: 4px;
	}
	.lo-mini-sw button,
	.lo-mini-add {
		border: 1px solid #454b57;
		background: #1d2027;
		color: #fff;
		border-radius: 8px;
		padding: 8px 12px;
		font-weight: 800;
		cursor: pointer;
	}
	.lo-mini-sw button[aria-pressed='true'] {
		background: var(--yellow);
		color: var(--yellow-ink);
		border-color: var(--yellow);
	}
	.lo-mini-sw button.b[aria-pressed='true'] {
		background: #5aa9ff;
		border-color: #5aa9ff;
		color: #04121f;
	}
	.lo-mini-add {
		border-color: #5aa9ff;
		color: #cfe6ff;
		white-space: nowrap;
	}
	.lo-in,
	.lo-out {
		min-width: 0;
	}
	.lo-in fieldset {
		min-width: 0;
	}
	.lo-seg button {
		min-width: 0;
		overflow-wrap: anywhere;
	}
	.lo-tabs [role='tab'],
	.lo-add {
		min-width: 0;
		overflow-wrap: anywhere;
	}
	.lo-in {
		background: var(--lo-card);
		border: 1px solid var(--line);
		border-radius: var(--r-lg);
		padding: var(--sp-4);
		box-shadow: var(--shadow);
	}
	.lo-tabs {
		display: flex;
		gap: var(--sp-2);
		margin-bottom: var(--sp-3);
		align-items: center;
	}
	.lo-tablist {
		flex: 1;
		display: flex;
		gap: var(--sp-2);
	}
	.lo-tabs [role='tab'] {
		flex: 1;
		border: 2px solid var(--line);
		background: #fff;
		border-radius: 10px;
		padding: 10px;
		font-weight: 700;
		cursor: pointer;
	}
	.lo-tabs .t-a[aria-selected='true'] {
		border-color: var(--yellow);
		background: var(--yellow-soft);
	}
	.lo-tabs .t-b[aria-selected='true'] {
		border-color: var(--lo-b);
		background: #e8f3ff;
	}
	.lo-add {
		flex: 1;
		border: 2px dashed #c5cad3;
		background: transparent;
		border-radius: 10px;
		padding: 10px;
		font-weight: 700;
		cursor: pointer;
		color: var(--muted);
	}
	.lo-add:hover {
		border-color: var(--lo-b);
		color: var(--text);
	}
	.lo-x {
		border: 0;
		background: transparent;
		font-size: 22px;
		cursor: pointer;
		color: var(--muted);
		width: 32px;
	}
	fieldset {
		border: 0;
		border-top: 1px solid var(--line);
		margin: 0;
		padding: var(--sp-3) 0 var(--sp-2);
	}
	legend {
		font-family: var(--display);
		font-weight: 700;
		font-size: 20px;
		text-transform: uppercase;
		letter-spacing: 0.02em;
		padding: 0;
	}
	.lo-row {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		gap: var(--sp-2);
		margin-top: var(--sp-3);
		font-size: 14px;
		font-weight: 600;
		color: var(--muted);
	}
	.lo-sub {
		display: block;
		margin: var(--sp-3) 0 var(--sp-1);
		font-size: 14px;
		font-weight: 600;
		color: var(--muted);
	}
	.lo-val {
		color: var(--text);
		font-variant-numeric: tabular-nums;
	}
	.lo-halb {
		color: var(--bad);
	}
	.lo .slider::-webkit-slider-runnable-track {
		background: linear-gradient(90deg, #111 var(--p), #d5d9e0 var(--p));
	}
	.lo .slider::-moz-range-track {
		background: #d5d9e0;
	}
	.lo .slider::-moz-range-progress {
		background: #111;
	}
	.lo .slider::-webkit-slider-thumb {
		background: var(--yellow);
		box-shadow: 0 0 0 2px #111;
	}
	.lo .slider::-moz-range-thumb {
		background: var(--yellow);
		box-shadow: 0 0 0 2px #111;
	}
	.lo-sel {
		width: 100%;
		height: 40px;
		border: 1px solid #cdd2da;
		border-radius: 8px;
		background: #fff;
		padding: 0 var(--sp-2);
		font-size: 15px;
	}
	.lo-two {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--sp-2);
	}
	.lo-seg {
		display: grid;
		gap: 4px;
		background: var(--paper-3);
		border-radius: 10px;
		padding: 4px;
	}
	.lo-seg3 {
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}
	.lo-seg5 {
		grid-template-columns: repeat(5, minmax(0, 1fr));
	}
	.lo-seg6 {
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}
	.lo-seg button {
		border: 0;
		background: transparent;
		border-radius: 7px;
		padding: 8px 4px;
		font-weight: 600;
		font-size: 14px;
		cursor: pointer;
		display: flex;
		flex-direction: column;
		align-items: center;
		line-height: 1.2;
	}
	.lo-seg button small {
		font-weight: 500;
		font-size: 11.5px;
		color: var(--muted);
	}
	.lo-seg button[aria-pressed='true'] {
		background: #fff;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15), inset 0 -3px 0 var(--yellow);
	}
	.lo-chips {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		margin-top: var(--sp-2);
	}
	.lo-chips button {
		border: 1px solid var(--line);
		background: #fff;
		border-radius: 999px;
		padding: 4px 10px;
		font-size: 13px;
		font-weight: 700;
		cursor: pointer;
	}
	.lo-chips small {
		font-weight: 500;
		color: var(--muted);
	}
	.lo-chips button[aria-pressed='true'] {
		border-color: #111;
		background: var(--yellow-soft);
	}
	/* ---- tulemus ---- */
	.lo-out {
		background: var(--ink);
		color: var(--on-d);
		border-radius: var(--r-lg);
		padding: var(--sp-5);
		position: sticky;
		top: 84px;
		box-shadow: var(--shadow);
	}
	.proj .lo-out {
		position: static;
	}
	.lo-laeb {
		color: var(--muted-d);
	}
	.lo-resgrid.two {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--sp-5);
	}
	.lo-resgrid.two .lo-res + .lo-res {
		border-left: 1px solid var(--line-d);
		padding-left: var(--sp-5);
	}
	.lo-resgrid.two .lo-big {
		font-size: clamp(48px, 5vw, 76px);
	}
	.lo-resgrid.two .lo-split {
		grid-template-columns: 1fr 1fr;
	}
	.lo-resgrid.two .lo-res-sub {
		font-size: 13px;
	}
	@media (max-width: 560px) {
		.lo-resgrid.two {
			grid-template-columns: 1fr;
		}
		.lo-resgrid.two .lo-res + .lo-res {
			border-left: 0;
			padding-left: 0;
			border-top: 1px solid var(--line-d);
			padding-top: var(--sp-4);
		}
	}
	.lo-res-h {
		display: flex;
		gap: var(--sp-2);
		align-items: center;
		flex-wrap: wrap;
	}
	.lo-tag {
		display: inline-grid;
		place-items: center;
		width: 28px;
		height: 28px;
		border-radius: 7px;
		background: var(--yellow);
		color: var(--yellow-ink);
		font-weight: 800;
	}
	.lo-b .lo-tag,
	.lo-tag-b {
		background: var(--lo-b);
		color: #04121f;
	}
	.lo-tag.sm {
		margin-right: 6px;
		vertical-align: middle;
		width: 22px;
		height: 22px;
		font-size: 13px;
	}
	.lo-res-sub {
		color: var(--muted-d);
		font-size: 14px;
	}
	.lo-err {
		color: #fca5a5;
	}
	.lo-big {
		font-family: var(--display);
		font-weight: 700;
		font-size: clamp(56px, 7vw, 96px);
		line-height: 0.9;
		margin: var(--sp-3) 0 0;
		color: var(--yellow);
		font-variant-numeric: tabular-nums;
	}
	.lo-b .lo-big {
		color: var(--lo-b);
	}
	.lo-big small {
		font-size: 0.45em;
		color: var(--on-d);
	}
	.lo-nostop {
		color: #fca5a5 !important;
		font-size: 48px;
	}
	.lo-kokku {
		margin: var(--sp-1) 0 var(--sp-3);
		text-transform: uppercase;
		letter-spacing: 0.08em;
		font-size: 13px;
		font-weight: 700;
		color: var(--muted-d);
	}
	.lo-split {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: var(--sp-3);
		margin: 0;
	}
	@media (max-width: 560px) {
		.lo-split {
			grid-template-columns: 1fr 1fr;
		}
	}
	.lo-split dt {
		font-size: 12.5px;
		color: var(--muted-d);
	}
	.lo-split dd {
		margin: 2px 0 0;
		font-weight: 700;
		font-size: 18px;
		font-variant-numeric: tabular-nums;
	}
	.lo-note {
		color: #e5e7eb;
	}
	.lo-warn {
		margin: var(--sp-3) 0 0;
		padding-left: 18px;
		color: #fcd34d;
		font-size: 14px;
	}
	.lo-fig {
		margin: var(--sp-5) 0 0;
	}
	.lo-fig svg {
		display: block;
		max-width: 100%;
		height: auto;
		overflow: visible;
	}
	.lo-grid-l {
		stroke: #2b3039;
		stroke-width: 1;
	}
	.lo-tick {
		fill: #9aa2ae;
		font-size: 12px;
		text-anchor: middle;
	}
	.lo-rowlbl {
		fill: #fff;
		font-weight: 800;
		font-size: 16px;
	}
	.lo-bar-a {
		fill: var(--yellow);
	}
	.lo-bar-b {
		fill: #5aa9ff;
	}
	.lo-stop {
		stroke: #fff;
		stroke-width: 3;
	}
	.lo-endlbl {
		fill: #fff;
		font-weight: 700;
		font-size: 14px;
	}
	.lo-inlbl {
		fill: #e5e7eb;
		font-size: 12px;
		text-anchor: middle;
		font-weight: 600;
	}
	.lo-inlbl.lo-dark {
		fill: #111;
	}
	.lo-obst {
		stroke: #f87171;
		stroke-width: 3;
		stroke-dasharray: 6 5;
	}
	.lo-obstlbl {
		fill: #f87171;
		font-size: 12px;
		font-weight: 700;
	}
	.lo-fig figcaption {
		font-size: 13px;
		color: var(--muted-d);
		margin-top: var(--sp-2);
		display: flex;
		align-items: center;
		gap: 6px;
		flex-wrap: wrap;
	}
	.lo-key {
		display: inline-block;
		width: 16px;
		height: 10px;
		border-radius: 2px;
	}
	.lo-key-r {
		background: repeating-linear-gradient(45deg, #3a3f49 0 4px, #5c6370 4px 8px);
	}
	.lo-key-p {
		background: var(--yellow);
		margin-left: var(--sp-2);
	}
	.lo-obst-in {
		margin-top: var(--sp-4);
		border-top: 1px solid var(--line-d);
		padding-top: var(--sp-3);
		font-size: 14px;
	}
	.lo-out .lo-tool {
		color: var(--text);
	}
	.lo-obst-in label {
		color: var(--muted-d);
	}
	.lo-obst-row {
		display: flex;
		align-items: center;
		gap: var(--sp-2);
		margin-top: var(--sp-1);
	}
	.lo-obst-row input {
		width: 90px;
		height: 38px;
		border-radius: 8px;
		border: 1px solid #3a3f49;
		background: #1b1e24;
		color: #fff;
		padding: 0 var(--sp-2);
		font-size: 16px;
	}
	.lo-impact {
		display: block;
		margin: var(--sp-2) 0 0;
		color: #fecaca;
	}
	.lo-impact.ok {
		color: #bbf7d0;
	}
	.lo-cmp {
		margin-top: var(--sp-4);
		background: var(--ink-3);
		border-radius: var(--r);
		padding: var(--sp-3) var(--sp-4);
		font-size: 16px;
	}
	.lo-cmp p {
		margin: 0;
	}
	.proj .lo-in {
		font-size: 17px;
	}
	.proj .lo-split dd {
		font-size: 24px;
	}
	.proj .lo-cmp {
		font-size: 21px;
	}
	button:focus-visible,
	select:focus-visible,
	input:focus-visible {
		outline: 3px solid #111;
		outline-offset: 2px;
	}
	.lo-out button:focus-visible,
	.lo-out input:focus-visible {
		outline-color: var(--yellow);
	}
	.lo-naeb {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-2);
		align-items: center;
		margin-top: var(--sp-3);
	}
	.lo-naeb-l {
		width: 100%;
		font-size: 13.5px;
		color: var(--muted-d);
		font-weight: 600;
	}
	.lo-naeb button {
		border: 1px solid var(--line-d);
		background: transparent;
		color: var(--on-d);
		border-radius: 999px;
		padding: 6px 12px;
		font: inherit;
		font-size: 13.5px;
		cursor: pointer;
	}
	.lo-naeb button small {
		color: var(--muted-d);
		margin-left: 4px;
	}
	.lo-naeb button[aria-pressed='true'] {
		background: var(--yellow);
		color: var(--yellow-ink);
		border-color: var(--yellow);
	}
	.lo-naeb button[aria-pressed='true'] small {
		color: var(--yellow-ink);
	}
	.lo-naeb-t {
		margin: var(--sp-3) 0 0;
		font-size: 14px;
		color: var(--muted-d);
	}
	.lo-naeb-t b {
		color: var(--on-d);
	}
	.lo-kt {
		margin-top: var(--sp-8);
		background: var(--lo-card);
		border: 1px solid var(--line);
		border-radius: var(--r-lg);
		padding: var(--sp-6);
	}
	.lo-kt h2 {
		margin: 0 0 var(--sp-2);
		font-family: var(--display);
		font-size: 30px;
		text-transform: uppercase;
	}
	.lo-kt-sub {
		margin: 0 0 var(--sp-4);
		color: var(--muted);
		max-width: 70ch;
	}
	.lo-kt-ctl {
		display: flex;
		flex-direction: column;
		gap: var(--sp-3);
		margin-bottom: var(--sp-4);
	}
	.lo-kt-seg {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-2);
		align-items: center;
	}
	.lo-kt-seg span {
		font-size: 14px;
		font-weight: 600;
		color: var(--muted);
	}
	.lo-kt-seg button {
		border: 1px solid var(--line);
		background: var(--paper-2);
		border-radius: 999px;
		padding: 7px 14px;
		font: inherit;
		font-size: 14px;
		font-weight: 600;
		cursor: pointer;
		color: var(--text);
	}
	.lo-kt-seg button[aria-pressed='true'] {
		background: var(--yellow-soft);
		border-color: var(--yellow);
	}
	.lo-kt-t {
		width: 100%;
		border-collapse: collapse;
		font-size: 15px;
	}
	.lo-kt-t th,
	.lo-kt-t td {
		text-align: left;
		padding: var(--sp-3) var(--sp-3);
		border-bottom: 1px solid var(--line);
		vertical-align: top;
	}
	.lo-kt-t th {
		font-size: 12.5px;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: var(--muted);
	}
	.lo-kt-t .n {
		text-align: right;
		font-variant-numeric: tabular-nums;
	}
	.lo-kt-t .nw {
		white-space: nowrap;
	}
	.lo-kt-o {
		display: inline-block;
		font-weight: 600;
		padding: 2px 10px;
		border-radius: 8px;
		border-left: 4px solid currentColor;
		background: var(--paper-2);
	}
	.lo-kt-ok {
		color: var(--good);
	}
	.lo-kt-hoiatus {
		color: var(--warn);
	}
	.lo-kt-halb {
		color: var(--bad);
	}
	.lo-kt-varu {
		display: block;
		margin-top: 4px;
		color: var(--muted);
		font-size: 13px;
	}
	.lo-kt.lo-side {
		margin-top: 0;
		align-self: start;
	}
	.lo-vaated {
		display: flex;
		gap: var(--sp-2);
		flex-wrap: wrap;
		margin-bottom: var(--sp-5);
		border-bottom: 1px solid var(--line);
	}
	.lo-vaated a {
		padding: var(--sp-3) var(--sp-4);
		font-weight: 700;
		font-size: 16px;
		color: var(--muted);
		text-decoration: none;
		border-bottom: 3px solid transparent;
		margin-bottom: -1px;
	}
	.lo-vaated a:hover {
		color: var(--text);
	}
	.lo-vaated a[aria-current='page'] {
		color: var(--text);
		border-bottom-color: var(--yellow);
	}
	.lo-naeb-top button small {
		color: var(--muted);
		margin-left: 4px;
		font-weight: 500;
	}
	.lo-naeb-top button[aria-pressed='true'] {
		background: var(--yellow);
		border-color: var(--yellow);
	}
	@media (max-width: 640px) {
		.lo-vaated {
			flex-wrap: nowrap;
			overflow-x: auto;
			gap: 0;
		}
		.lo-vaated a {
			white-space: nowrap;
			padding: var(--sp-3);
			font-size: 15px;
		}
	}
	.lo-kt-note {
		margin: var(--sp-4) 0 0;
		font-size: 14px;
		color: var(--muted);
		max-width: 80ch;
	}
	@media (max-width: 640px) {
		.lo-kt {
			padding: var(--sp-4);
		}
		/* telefonis iga rida kaardina: nimi, numbrid kõrvuti, siis tulemus */
		.lo-kt-t,
		.lo-kt-t tbody {
			display: block;
		}
		.lo-kt-t thead {
			display: none;
		}
		.lo-kt-t tr {
			display: flex;
			flex-wrap: wrap;
			gap: var(--sp-1) var(--sp-4);
			padding: var(--sp-3) 0;
			border-bottom: 1px solid var(--line);
		}
		.lo-kt-t td {
			border: 0;
			padding: 0;
			font-size: 14.5px;
		}
		.lo-kt-t td.lo-kt-nimi,
		.lo-kt-t td.lo-kt-ots {
			width: 100%;
		}
		.lo-kt-t td.n {
			text-align: left;
		}
		.lo-kt-t td[data-l]::before {
			content: attr(data-l) ': ';
			color: var(--muted);
			font-weight: 500;
		}
	}
	.lo-kurvid {
		display: grid;
		gap: var(--sp-2);
	}
	.lo-kurvid button {
		display: flex;
		align-items: center;
		gap: var(--sp-3);
		text-align: left;
		border: 1px solid var(--line);
		background: var(--paper-2);
		border-radius: 12px;
		padding: var(--sp-2) var(--sp-3);
		font: inherit;
		cursor: pointer;
		color: var(--text);
	}
	.lo-kurvid button[aria-pressed='true'] {
		background: var(--yellow-soft);
		border-color: var(--yellow);
	}
	.lo-kurvid svg {
		width: 34px;
		height: 34px;
		flex: none;
	}
	.lo-kurvid path {
		fill: none;
		stroke: #6b7280;
		stroke-width: 5;
		stroke-linecap: round;
	}
	.lo-kurvid button[aria-pressed='true'] path {
		stroke: var(--text);
	}
	.lo-kurvid span {
		display: flex;
		flex-direction: column;
	}
	.lo-kurvid small {
		color: var(--muted);
		font-size: 12.5px;
	}
	.lo-seg4 {
		grid-template-columns: repeat(4, 1fr) !important;
	}
	.lo-seg3 {
		grid-template-columns: repeat(3, 1fr) !important;
	}
	.lo-seg2 {
		grid-template-columns: repeat(2, 1fr) !important;
	}
	.lo-kr-vihje {
		font-size: 13px;
		color: var(--muted);
		margin: var(--sp-2) 0 0;
	}
	.lo-kr-tulemus {
		border-left: 6px solid currentColor;
		background: var(--paper-2);
		border-radius: 12px;
		padding: var(--sp-4) var(--sp-5);
		margin-bottom: var(--sp-4);
	}
	.lo-kr-ots {
		margin: 0 0 var(--sp-3);
		font-weight: 800;
		font-size: 20px;
	}
	.lo-kr-nr {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-3) var(--sp-8);
		margin: 0;
		color: var(--text);
	}
	.lo-kr-nr dt {
		font-size: 13px;
		color: var(--muted);
	}
	.lo-kr-nr dd {
		margin: 0;
		font-weight: 700;
		font-size: 22px;
		font-variant-numeric: tabular-nums;
	}
	.lo-kr-fig {
		margin: 0 0 var(--sp-4);
		background: #e9ecef;
		border-radius: 12px;
		padding: var(--sp-2);
	}
	.lo-kr-fig svg {
		width: 100%;
		max-height: 320px;
		display: block;
	}
	.lo-kr-fig figcaption {
		font-size: 12.5px;
		color: var(--muted);
		text-align: right;
		padding: 0 var(--sp-2);
	}
	.kr-tee {
		fill: none;
		stroke: #4b5563;
		stroke-width: 46;
		stroke-linecap: butt;
	}
	.kr-joon {
		fill: none;
		stroke: #f3f4f6;
		stroke-width: 2;
		stroke-dasharray: 10 10;
	}
	.kr-kulg {
		fill: none;
		stroke: var(--yellow);
		stroke-width: 5;
		stroke-linecap: round;
	}
	.kr-jatk {
		fill: none;
		stroke: var(--bad);
		stroke-width: 5;
		stroke-dasharray: 8 6;
		stroke-linecap: round;
	}
	.kr-stop {
		fill: var(--good);
		stroke: #fff;
		stroke-width: 2;
	}
	.kr-auto {
		fill: #1f2937;
		stroke: #fff;
		stroke-width: 1.5;
	}
	.kr-auto.halb {
		fill: var(--bad);
	}
	.kr-klaas {
		fill: #93c5fd;
	}
	.lo-kr-h3 {
		margin: var(--sp-4) 0 var(--sp-2);
		font-size: 16px;
	}
</style>
