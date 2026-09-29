<script>
	/* Liiklusohutuse kalkulaator (/liiklusohutus/).
	   Sama arvutusmootor mis põhilehel (engine.js), aga neutraalne:
	   ei poode, hindu, rehvisoovitusi ega kasutusloo jälgimist.
	   Kõik mudeli sisendid on nähtaval, et õpetaja ja õpilane saaksid
	   iga teguri mõju ise läbi mängida. Olukord salvestub aadressi
	   (#...), nii et lingi saab jagada või tunniks ette valmistada. */
	import { onMount } from 'svelte';
	import { version } from '$app/environment';

	let core = $state(null);
	let P = $state(null);
	let viga = $state('');

	const KAT = [
		['SUMMER_TOURING', 'Suverehv'],
		['SUMMER_UHP', 'Suverehv, sportlik'],
		['ALL_SEASON', 'Aastaringne rehv'],
		['WINTER_CENTRAL', 'Talverehv, Kesk-Euroopa'],
		['WINTER_NORDIC', 'Talverehv, Põhjamaade (lamell)'],
		['WINTER_STUDDED', 'Naastrehv']
	];
	const PIND = [
		['ASPHALT', 'Asfalt'],
		['CONCRETE', 'Betoon'],
		['GRAVEL', 'Kruus'],
		['SNOW_PACKED', 'Tallatud lumi'],
		['SNOW_LOOSE', 'Kohev lumi'],
		['ICE', 'Jää']
	];
	const VESI = [
		[0, 'Kuiv'],
		[0.2, 'Niiske'],
		[1, 'Märg'],
		[3, 'Väga märg'],
		[5, 'Lombid']
	];
	const TEKST = [
		['COARSE_NEW', 'Uus, kare'],
		['NORMAL', 'Tavaline'],
		['WORN_SMOOTH', 'Kulunud, roopad'],
		['POLISHED', 'Poleeritud']
	];
	const PIDUR = [
		[1, 'Korras'],
		[0.85, 'Nõrgenenud (~85 %)'],
		[0.65, 'Selgelt vigane (~65 %)'],
		[0.45, 'Kriitiline (~45 %)']
	];
	const REAKT = [
		[0.7, 'valmis pidurdama'],
		[1.0, 'tavaline arvestus'],
		[1.5, 'ootamatu oht'],
		[2.0, 'väsinud / hajevil']
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
		} catch (e) {
			viga = 'Andmed ei laadinud. Proovi lehte värskendada.';
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
			.map((v) => [v.key, v.yearLabel + (n[v.yearLabel] > 1 && v.variant && v.variant !== '—' ? ' · ' + v.variant : '')]);
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

	function arvuta(s) {
		if (!core || !P || !s) return null;
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
		try {
			const r = P.stoppingDistance(tyre, veh, cond);
			return { r, veh, v0: +s.kiirus, reakt: r.reactionM };
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

	/* ------------------------------------------------------ vormindus */
	const f1 = (x) => (Math.round(x * 10) / 10).toLocaleString('et-EE', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
	const f0 = (x) => Math.round(x).toLocaleString('et-EE');
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
</script>

<div class="lo" class:proj={esitlus} bind:this={juur}>
	{#if viga}<p class="lo-viga">{viga}</p>{/if}

	<div class="lo-top">
		<div class="lo-naited" aria-label="Näidisvõrdlused">
			<span class="lo-lbl">Valmis võrdlused:</span>
			<button type="button" onclick={() => naide('kiirus')}>50 vs 70 km/h</button>
			<button type="button" onclick={() => naide('telefon')}>Tähelepanelik vs hajevil</button>
			<button type="button" onclick={() => naide('muster')}>Uus vs kulunud rehv</button>
			<button type="button" onclick={() => naide('vesi')}>Märg vs lombid</button>
			<button type="button" onclick={() => naide('lumi')}>Suverehv lumel</button>
			<button type="button" onclick={() => naide('jaa')}>Jää −10 °C vs 0 °C</button>
		</div>
		<div class="lo-tools">
			<button type="button" class="lo-tool" onclick={kopeeri}>{kopeeritud ? 'Link kopeeritud' : 'Kopeeri link'}</button>
			<button type="button" class="lo-tool" aria-pressed={esitlus} onclick={esitlusrezim}>{esitlus ? 'Välju esitlusest' : 'Esitlusrežiim'}</button>
		</div>
	</div>

	<div class="lo-grid">
		<!-- ================= SISENDID ================= -->
		<section class="lo-in" aria-label="Olukord">
			<div class="lo-tabs" role="tablist" aria-label="Olukord">
				<button type="button" role="tab" aria-selected={muuda === 'A'} class="t-a" onclick={() => (muuda = 'A')}>Olukord A</button>
				{#if B}
					<button type="button" role="tab" aria-selected={muuda === 'B'} class="t-b" onclick={() => (muuda = 'B')}>Olukord B</button>
					<button type="button" class="lo-x" onclick={eemaldaB} aria-label="Eemalda olukord B">×</button>
				{:else}
					<button type="button" class="lo-add" onclick={lisaB}>+ Lisa võrdlus</button>
				{/if}
			</div>

			<fieldset>
				<legend>Kiirus ja juht</legend>
				<label class="lo-row" for="lo-kiirus">
					<span>Kiirus</span>
					<b class="lo-val">{S.kiirus} km/h</b>
				</label>
				<input id="lo-kiirus" class="slider" type="range" min="10" max="150" step="5" bind:value={S.kiirus} style="--p:{((S.kiirus - 10) / 140) * 100}%" />
				<label class="lo-row" for="lo-reakt">
					<span>Reaktsiooniaeg</span>
					<b class="lo-val">{f1(S.reakt)} s</b>
				</label>
				<input id="lo-reakt" class="slider" type="range" min="0" max="3" step="0.1" bind:value={S.reakt} style="--p:{(S.reakt / 3) * 100}%" />
				<div class="lo-chips">
					{#each REAKT as [t, n]}
						<button type="button" aria-pressed={Math.abs(S.reakt - t) < 0.05} onclick={() => (S.reakt = t)}>{f1(t)} s <small>{n}</small></button>
					{/each}
				</div>
			</fieldset>

			<fieldset>
				<legend>Tee</legend>
				<div class="lo-seg lo-seg6">
					{#each PIND as [k, n]}
						<button type="button" aria-pressed={S.pind === k} onclick={() => setPind(S, k)}>{n}</button>
					{/each}
				</div>
				{#if ASF[S.pind]}
					<span class="lo-sub">Vesi teel</span>
					<div class="lo-seg lo-seg5">
						{#each VESI as [w, n]}
							<button type="button" aria-pressed={Math.abs(S.vesi - w) < 0.01} onclick={() => setVesi(S, w)}>{n}<small>{String(w).replace('.', ',')} mm</small></button>
						{/each}
					</div>
					<label class="lo-row" for="lo-tekst"><span>Teekate</span></label>
					<select id="lo-tekst" class="lo-sel" bind:value={S.tekst}>
						{#each TEKST as [k, n]}<option value={k}>{n}</option>{/each}
					</select>
				{/if}
				{#if S.pind === 'ICE'}
					<label class="lo-row" for="lo-jaa"><span>Jää</span></label>
					<select id="lo-jaa" class="lo-sel" bind:value={S.jaa}>
						<option value="tee">Tavaline teejää (rööpad, liiv, karedus)</option>
						<option value="sile">Sile jää (kiilasjää, must jää)</option>
					</select>
				{/if}
				<label class="lo-row" for="lo-temp">
					<span>Teepinna temperatuur</span>
					<b class="lo-val">{S.temp > 0 ? '+' : ''}{S.temp} °C</b>
				</label>
				<input id="lo-temp" class="slider" type="range" min={tMin} max={tMax} step="1" bind:value={S.temp} style="--p:{((S.temp - tMin) / (tMax - tMin)) * 100}%" />
				<label class="lo-row" for="lo-kalle">
					<span>Tee kalle</span>
					<b class="lo-val">{S.kalle === 0 ? 'tasane' : (S.kalle < 0 ? 'allamäge ' : 'ülesmäge ') + Math.abs(S.kalle) + ' %'}</b>
				</label>
				<input id="lo-kalle" class="slider" type="range" min="-12" max="12" step="1" bind:value={S.kalle} style="--p:{((S.kalle + 12) / 24) * 100}%" />
			</fieldset>

			<fieldset>
				<legend>Rehvid</legend>
				<label class="lo-row" for="lo-kat"><span>Rehvi tüüp</span></label>
				<select id="lo-kat" class="lo-sel" bind:value={S.kat}>
					{#each KAT as [k, n]}<option value={k}>{n}</option>{/each}
				</select>
				{#if S.kat !== 'WINTER_STUDDED'}
					<span class="lo-sub">Märghaarde klass (EL-i rehvimärgis)</span>
					<div class="lo-seg lo-seg5">
						{#each ['A', 'B', 'C', 'D', 'E'] as k}
							<button type="button" aria-pressed={S.klass === k} onclick={() => (S.klass = k)}>{k}</button>
						{/each}
					</div>
				{/if}
				<span class="lo-sub">Rehvi seisukord</span>
				<div class="lo-seg lo-seg3">
					<button type="button" aria-pressed={S.muster === 8 && S.vanus === 1} onclick={() => seisund(S, 'uus')}>Uus</button>
					<button type="button" aria-pressed={S.muster === 4.5 && S.vanus === 6} onclick={() => seisund(S, 'kesk')}>Keskmiselt kulunud</button>
					<button type="button" aria-pressed={S.vanus === 10 && (S.muster === 1.6 || S.muster === 3)} onclick={() => seisund(S, 'piir')}>Seaduse piiril</button>
				</div>
				<label class="lo-row" for="lo-muster">
					<span>Mustrisügavus</span>
					<b class="lo-val" class:lo-halb={S.muster < (TALV[S.kat] ? 3 : 1.6)}>{f1(S.muster)} mm</b>
				</label>
				<input id="lo-muster" class="slider" type="range" min="0.5" max="8" step="0.5" bind:value={S.muster} style="--p:{((S.muster - 0.5) / 7.5) * 100}%" />
				<label class="lo-row" for="lo-vanus">
					<span>Rehvi vanus</span>
					<b class="lo-val">{S.vanus} {S.vanus === 1 ? 'aasta' : 'aastat'}</b>
				</label>
				<input id="lo-vanus" class="slider" type="range" min="0" max="15" step="1" bind:value={S.vanus} style="--p:{(S.vanus / 15) * 100}%" />
				<label class="lo-row" for="lo-rohk">
					<span>Rehvirõhk</span>
					<b class="lo-val">{S.rohk === 0 ? 'soovituslik' : (S.rohk > 0 ? '+' : '−') + f1(Math.abs(S.rohk)) + ' bar'}</b>
				</label>
				<input id="lo-rohk" class="slider" type="range" min="-1" max="0.6" step="0.1" bind:value={S.rohk} style="--p:{((S.rohk + 1) / 1.6) * 100}%" />
			</fieldset>

			<fieldset>
				<legend>Auto</legend>
				<label class="lo-row" for="lo-mk"><span>Mark</span></label>
				<select id="lo-mk" class="lo-sel" bind:value={S.mk} onchange={() => { S.md = mudelid[0] || ''; S.veh = polved[0]?.[0] || ''; S.abs = 'auto'; }}>
					<option value="">Tüüpauto (mark pole oluline)</option>
					{#each margid as mk}<option value={mk}>{mk}</option>{/each}
				</select>
				{#if !S.mk}
					<label class="lo-row" for="lo-tyyp"><span>Auto tüüp</span></label>
					<select id="lo-tyyp" class="lo-sel" bind:value={S.tyyp}>
						{#each tyybid as v}<option value={v.key}>{v.name}</option>{/each}
					</select>
				{:else}
					<div class="lo-two">
						<div>
							<label class="lo-row" for="lo-md"><span>Mudel</span></label>
							<select id="lo-md" class="lo-sel" bind:value={S.md} onchange={() => { S.veh = polved[0]?.[0] || ''; S.abs = 'auto'; }}>
								<option value="">Vali</option>
								{#each mudelid as md}<option value={md}>{md}</option>{/each}
							</select>
						</div>
						<div>
							<label class="lo-row" for="lo-veh"><span>Põlvkond</span></label>
							<select id="lo-veh" class="lo-sel" bind:value={S.veh} disabled={!S.md} onchange={() => (S.abs = 'auto')}>
								{#each polved as [k, n]}<option value={k}>{n}</option>{/each}
							</select>
						</div>
					</div>
				{/if}
				{#if auto(S)}
					{@const v = core.byKey[S.mk ? S.veh : S.tyyp]}
					<label class="lo-row" for="lo-abs"><span>ABS</span></label>
					<select id="lo-abs" class="lo-sel" bind:value={S.abs}>
						{#if v.absOpt}
							<option value="auto">ABS-ita (oli lisavarustus)</option>
							<option value="jah">ABS-iga</option>
						{:else if v.absClass === 'NONE'}
							<option value="auto">ABS-ita (autol ABS-i ei olnud)</option>
						{:else}
							<option value="auto">ABS-iga</option>
							<option value="ei">ABS-ita (rattad lukustuvad)</option>
						{/if}
					</select>
				{/if}
				<label class="lo-row" for="lo-laad">
					<span>Koormus (juht, reisijad, pagas)</span>
					<b class="lo-val">{S.laad} kg</b>
				</label>
				<input id="lo-laad" class="slider" type="range" min="75" max="600" step="25" bind:value={S.laad} style="--p:{((S.laad - 75) / 525) * 100}%" />
				<label class="lo-row" for="lo-pidur"><span>Pidurite seisukord</span></label>
				<select id="lo-pidur" class="lo-sel" bind:value={S.pidur}>
					{#each PIDUR as [k, n]}<option value={k}>{n}</option>{/each}
				</select>
			</fieldset>
		</section>

		<!-- ================= TULEMUS ================= -->
		<section class="lo-out" aria-live="polite" aria-label="Tulemus" bind:this={outEl}>
			{#if !core}
				<p class="lo-laeb">Laadin arvutusmudelit…</p>
			{:else}
				<div class="lo-resgrid" class:two={!!B}>
				{#each [['A', RA], ...(B ? [['B', RB]] : [])] as [n, x]}
					<div class="lo-res" class:lo-b={n === 'B'}>
						<div class="lo-res-h">
							<span class="lo-tag">{n}</span>
							{#if x && x.err}
								<span class="lo-err">Seda olukorda ei saa arvutada: {x.err}</span>
							{:else if x && x.r}
								<span class="lo-res-sub">{(n === 'A' ? A : B).kiirus} km/h · {PIND.find((p) => p[0] === (n === 'A' ? A : B).pind)[1].toLowerCase()} · {x.veh.name}</span>
							{/if}
						</div>
						{#if x && x.r}
							{#if !x.r.stopped}
								<p class="lo-big lo-nostop">Auto ei peatu</p>
								<p class="lo-note">Selle kalde ja haardega ei suuda rehvid autot peatada — auto libiseb edasi.</p>
							{:else}
								<p class="lo-big">{m(x.r.totalDistanceM)} <small>m</small></p>
								<p class="lo-kokku">peatumisteekond</p>
								<dl class="lo-split">
									<div><dt>Reageerimisteekond</dt><dd>{m(x.r.reactionM)} m</dd></div>
									<div><dt>Pidurdusteekond</dt><dd>{m(x.r.distanceM)} m</dd></div>
									<div><dt>Aeg seisuni</dt><dd>{f1(x.r.timeS)} s</dd></div>
									<div><dt>Tõenäoline vahemik</dt><dd>{m(x.r.lowM)}–{m(x.r.highM)} m</dd></div>
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
						<button type="button" class="lo-addb" onclick={lisaB}>+ Lisa võrdlus: olukord B</button>
					{:else}
						<span>Muudad:</span>
						<button type="button" class="lo-sw" aria-pressed={muuda === 'A'} onclick={() => (muuda = 'A')}>A</button>
						<button type="button" class="lo-sw lo-sw-b" aria-pressed={muuda === 'B'} onclick={() => (muuda = 'B')}>B</button>
						<button type="button" class="lo-rm" onclick={eemaldaB}>Eemalda B</button>
					{/if}
				</div>

				{#if stsenaariumid.length}
					<figure class="lo-fig" bind:clientWidth={figW}>
						<svg width={W} viewBox="0 0 {W} {60 + stsenaariumid.length * 70}" role="img" aria-label="Peatumisteekond teel meetrites">
							<defs>
								<pattern id="lo-hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
									<rect width="10" height="10" fill="#3a3f49" />
									<line x1="0" y1="0" x2="0" y2="10" stroke="#5c6370" stroke-width="4" />
								</pattern>
							</defs>
							{#each tikid as t}
								<line x1={X(t)} x2={X(t)} y1="18" y2={40 + stsenaariumid.length * 70} class="lo-grid-l" />
								<text x={X(t)} y="10" class="lo-tick">{t} m</text>
							{/each}
							{#each stsenaariumid as [n, x], i}
								{@const y = 30 + i * 70}
								{@const kokku = x.r.stopped ? x.r.totalDistanceM : maxD}
								<text x="4" y={y + 30} class="lo-rowlbl">{n}</text>
								<rect x={X(0)} y={y + 10} width={Math.max(0, X(x.r.reactionM) - X(0))} height="28" fill="url(#lo-hatch)" rx="3" />
								<rect x={X(x.r.reactionM)} y={y + 10} width={Math.max(0, X(kokku) - X(x.r.reactionM))} height="28" class={n === 'A' ? 'lo-bar-a' : 'lo-bar-b'} rx="3" />
								{#if x.r.stopped}
									<line x1={X(kokku)} x2={X(kokku)} y1={y + 4} y2={y + 44} class="lo-stop" />
									<text x={Math.min(X(kokku) + 6, W - 4)} y={y + 58} class="lo-endlbl" text-anchor={X(kokku) > W - 70 ? 'end' : 'start'}>{m(kokku)} m</text>
								{/if}
								{#if X(x.r.reactionM) - X(0) > 96}
									<text x={(X(0) + X(x.r.reactionM)) / 2} y={y + 30} class="lo-inlbl">reageerimine</text>
								{/if}
								{#if X(kokku) - X(x.r.reactionM) > 90}
									<text x={(X(x.r.reactionM) + X(kokku)) / 2} y={y + 30} class="lo-inlbl lo-dark">pidurdamine</text>
								{/if}
							{/each}
							{#if takistus > 0}
								<line x1={X(takistus)} x2={X(takistus)} y1="18" y2={40 + stsenaariumid.length * 70} class="lo-obst" />
								<text x={X(takistus) - 4} y={36 + stsenaariumid.length * 70} class="lo-obstlbl" text-anchor="end">takistus</text>
							{/if}
						</svg>
						<figcaption><span class="lo-key lo-key-r"></span> reageerimisteekond (auto sõidab täiskiirusel) <span class="lo-key lo-key-p"></span> pidurdusteekond</figcaption>
					</figure>
				{/if}

				<div class="lo-obst-in">
					<label for="lo-tak">Takistus tee peal (nt teele jooksev laps) kaugusel</label>
					<div class="lo-obst-row">
						<input id="lo-tak" type="number" min="0" max="500" step="1" bind:value={takistus} placeholder="0" />
						<span>m</span>
						{#if takistus > 0}<button type="button" class="lo-tool" onclick={() => (takistus = 0)}>Eemalda</button>{/if}
					</div>
					{#each tak as [n, v]}
						<p class="lo-impact" class:ok={v === 0}>
							<span class="lo-tag sm" class:lo-tag-b={n === 'B'}>{n}</span>
							{#if v === 0}
								Peatub enne takistust.
							{:else}
								Jõuab takistuseni kiirusega <b>{f0(v)} km/h</b> — löök nagu kukkudes {f1(kukkumine(v))} m kõrguselt.
							{/if}
						</p>
					{/each}
				</div>

				{#if vordlus}
					<div class="lo-cmp">
						<p>
							<b>{vordlus.Pk}</b> vajab peatumiseks <b>{m(vordlus.vahe)} m</b> rohkem.
							{#if vordlus.v > 0.5}
								Kohas, kus <b>{vordlus.L}</b> juba seisab ({m(vordlus.koht)} m), sõidab <b>{vordlus.Pk}</b> veel
								<b>{f0(vordlus.v)} km/h</b> — see on sama löök, nagu kukuks auto {f1(kukkumine(vordlus.v))} m kõrguselt.
							{/if}
						</p>
					</div>
				{/if}
			{/if}
		</section>
	</div>

	{#if core && !esitlus}
		<div class="lo-mini" class:peidus={tulemusNahtav}>
			<button type="button" class="lo-mini-res" onclick={naitaTulemust} aria-label="Näita tulemust">
				<span class="lo-tag sm">A</span><b>{RA?.r ? (RA.r.stopped ? m(RA.r.totalDistanceM) + ' m' : 'ei peatu') : '—'}</b>
				{#if B}<span class="lo-tag sm lo-tag-b">B</span><b>{RB?.r ? (RB.r.stopped ? m(RB.r.totalDistanceM) + ' m' : 'ei peatu') : '—'}</b>{/if}
				<span class="lo-mini-up">Tulemus ↑</span>
			</button>
			{#if B}
				<div class="lo-mini-sw" role="group" aria-label="Mida muudad">
					<button type="button" aria-pressed={muuda === 'A'} onclick={() => (muuda = 'A')}>A</button>
					<button type="button" class="b" aria-pressed={muuda === 'B'} onclick={() => (muuda = 'B')}>B</button>
				</div>
			{:else}
				<button type="button" class="lo-mini-add" onclick={lisaB}>+ Võrdle</button>
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
		grid-template-columns: repeat(3, 1fr);
	}
	.lo-seg5 {
		grid-template-columns: repeat(5, 1fr);
	}
	.lo-seg6 {
		grid-template-columns: repeat(3, 1fr);
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
</style>
