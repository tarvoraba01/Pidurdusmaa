<script>
	/* „Kui vanad on su rehvid?“ — DOT-koodi 4 numbrit → tootmisnädal ja vanus,
	   mustri sügavus → kui palju pikem on pidurdusmaa kui uue rehviga.
	   Sama mootor mis kalkulaatoris (engine.js): vanus vähendab haaret üle 5 aasta,
	   kulunud muster eriti märjal ja lumel. */
	import { onMount } from 'svelte';
	import { version } from '$app/environment';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();

	let P = null, core = null;
	let veh = $state(null);
	let dot = $state('');
	let liik = $state('suvi'); /* suvi | talv */
	let muster = $state(5);
	let tee = $state('marg'); /* marg | lumi */
	let kiirus = $state(90);
	let valmis = $state(false);
	let puudutatud = false;

	const UUS = { suvi: 8, talv: 9 };
	const KAT = { suvi: 'SUMMER_TOURING', talv: 'WINTER_NORDIC' };

	onMount(async () => {
		try {
			const q = new URLSearchParams(location.search).get('dot');
			if (q && /^\d{3,4}$/.test(q)) dot = q;
		} catch {}
		await import('$lib/engine.js');
		P = globalThis.Pidurdus;
		core = await (await fetch('/data/core.json?v=' + encodeURIComponent(version))).json();
		let key = null;
		try { key = JSON.parse(sessionStorage.getItem('pm_veh') || 'null'); } catch {}
		const byKey = (k) => core.vehicles.find((v) => v.key === k);
		veh = (key && byKey(String(key).split('~')[0])) || byKey('vw_golf_8');
		valmis = true;
	});

	/* ISO nädala esmaspäev */
	function nadalaAlgus(a, n) {
		const j4 = new Date(Date.UTC(a, 0, 4)), p = (j4.getUTCDay() + 6) % 7;
		return new Date(Date.UTC(a, 0, 4 - p + (n - 1) * 7));
	}
	const kood = $derived.by(() => {
		const s = String(dot).replace(/\D/g, '');
		if (!s) return null;
		if (s.length === 3) return { vana: true };
		if (s.length !== 4) return { viga: t('Sisesta 4 numbrit, nt 2319.') };
		const n = +s.slice(0, 2), a = 2000 + +s.slice(2);
		if (n < 1 || n > 53) return { viga: t('Kahe esimese numbri (nädal) peab olema 01–53.') };
		const algus = nadalaAlgus(a, n), nyyd = new Date();
		if (algus > nyyd) return { viga: t('See kuupäev on tulevikus. Kontrolli numbreid: esimesed kaks on nädal, viimased kaks aasta.') };
		const kuud = Math.max(0, Math.floor((nyyd - algus) / (30.44 * 864e5)));
		return { n, a, algus, kuud, aastad: (nyyd - algus) / (365.25 * 864e5) };
	});
	const LOC = keel.lang === 'en' ? 'en-GB' : keel.lang === 'ru' ? 'ru-RU' : 'et-EE';
	const kuuNimi = (d) => d.toLocaleDateString(LOC, { month: 'long', year: 'numeric', timeZone: 'UTC' });
	const f1 = (x) => x.toLocaleString(LOC, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
	/* käänded: vene keeles 1 год / 2 года / 5 лет */
	const VORMID = {
		et: { a: { one: 'aasta', other: 'aastat' }, k: { one: 'kuu', other: 'kuud' } },
		en: { a: { one: 'year', other: 'years' }, k: { one: 'month', other: 'months' } },
		ru: { a: { one: 'год', few: 'года', many: 'лет', other: 'года' }, k: { one: 'месяц', few: 'месяца', many: 'месяцев', other: 'месяца' } }
	};
	const PR = new Intl.PluralRules(LOC);
	const sona = (n, liik) => { const v = (VORMID[keel.lang] || VORMID.et)[liik]; return n + ' ' + (v[PR.select(n)] || v.other); };
	const vanusTekst = (k) => {
		const a = Math.floor(k / 12), m = k % 12;
		return [a ? sona(a, 'a') : '', m || !a ? sona(m, 'k') : ''].filter(Boolean).join(' ');
	};

	/* vanuse hinnang: tootjad soovitavad üle 5 a kontrollida igal aastal, vahetada hiljemalt 10 a */
	const vanusHinne = $derived.by(() => {
		const k = kood;
		if (!k || k.viga) return null;
		const a = k.vana ? 99 : k.aastad;
		if (a < 5) return ['hea', t('Vanus on korras'), t('Alla 5 aasta vanune rehv ei ole vanuse tõttu veel kõvenenud. Jälgi mustrit.')];
		if (a < 8) return ['jalgi', t('Kontrolli igal aastal'), t('Üle 5 aasta vanune kumm hakkab kõvenema ja haare väheneb vähehaaval. Lase rehvid igal hooajal üle vaadata: praod küljel ja mustrisoontes on märk, et aeg on vahetada.')];
		if (a < 10) return ['moelda', t('Mõtle vahetusele'), t('Kumm on juba märgatavalt kõvem kui uuel rehvil, eriti külmaga. Isegi kui mustrit on veel küllalt, pidurdab rehv halvemini.')];
		return ['vaheta', t('Aeg vahetada'), t('Rehvitootjad soovitavad vahetada hiljemalt 10 aasta vanuselt, ka siis, kui mustrit on veel.')];
	});
	const piir = $derived(liik === 'talv' ? 3 : 1.6);
	const musterHinne = $derived.by(() => {
		if (muster < piir) return ['vaheta', liik === 'talv' ? t('Alla seadusliku 3 mm (talverehv)') : t('Alla seadusliku 1,6 mm')];
		if (muster <= (liik === 'talv' ? 4 : 3)) return ['moelda', t('Muster on peaaegu läbi')];
		if (muster < (liik === 'talv' ? 6 : 5)) return ['jalgi', t('Muster on poole peal')];
		return ['hea', t('Mustrit on küllalt')];
	});
	$effect(() => { if (liik === 'suvi' && tee === 'lumi') tee = 'marg'; });
	$effect(() => { muster = Math.min(muster, UUS[liik]); });

	function tyre(td, age) {
		const kat = KAT[liik];
		return { key: 'x', name: 'x', category: kat, wetGripIndex: core.gClass?.C?.[kat]?.[0] || 1.3, treadDepthMm: td, treadDepthNewMm: UUS[liik], pressureBar: null, loadCapacityKg: null, ageYears: age, studded: false, size: veh.oemSize, gSource: 'label' };
	}
	const tulemus = $derived.by(() => {
		if (!valmis || !veh || !P || !kood || kood.viga) return null;
		const vanus = kood.vana ? 26 : kood.aastad;
		const c = tee === 'lumi' ? { surface: 'SNOW_PACKED', waterMm: 0, tempC: -5 } : { surface: 'ASPHALT', waterMm: 1, tempC: liik === 'talv' ? 3 : 12 };
		const cond = { speedKmh: kiirus, texture: 'NORMAL', payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1, ...c };
		try {
			const uus = P.stoppingDistance(tyre(UUS[liik], 1), veh, cond);
			const sinu = P.stoppingDistance(tyre(muster, vanus), veh, cond);
			/* sinu kiirus kohas, kus uus rehv on juba seisma jäänud */
			const tr = sinu.trace || [];
			let jaak = 0;
			for (let i = 1; i < tr.length; i++) if (tr[i][0] >= uus.distanceM) { const a = tr[i - 1], b = tr[i], k = (uus.distanceM - a[0]) / Math.max(1e-9, b[0] - a[0]); jaak = a[1] + k * (b[1] - a[1]); break; }
			const ainultVanus = P.stoppingDistance(tyre(UUS[liik], vanus), veh, cond).distanceM - uus.distanceM;
			return { uus: uus.distanceM, sinu: sinu.distanceM, lisa: sinu.distanceM - uus.distanceM, jaak, ainultVanus };
		} catch {
			return null;
		}
	});
	const halb = $derived((vanusHinne && (vanusHinne[0] === 'moelda' || vanusHinne[0] === 'vaheta')) || musterHinne[0] === 'moelda' || musterHinne[0] === 'vaheta');

	function track(e, v) { try { window.PM_TRACK && window.PM_TRACK('vanus', e + (v ? ' · ' + v : '')); } catch {} }
	let viimane = '';
	$effect(() => {
		const k = kood;
		if (!k || k.viga) return;
		const s = k.vana ? 'vana' : Math.floor(k.aastad) + ' a';
		if (s !== viimane) { viimane = s; track('dot', s); }
	});
	const vanusSilt = $derived(kood && !kood.viga ? (kood.vana ? t('üle 25 aasta') : vanusTekst(kood.kuud)) : '');
	const ribaMax = $derived(tulemus ? Math.max(tulemus.sinu, tulemus.uus) : 1);
</script>

<div class="rv">
	<div class="rv-kaart">
		<div class="rv-sisend">
			<label class="rv-lab" for="rv-dot"><span>1</span>{t('Rehvi küljel oleva DOT-koodi 4 viimast numbrit')}</label>
			<div class="rv-rida">
				<input
					id="rv-dot"
					class="rv-dot"
					type="text"
					inputmode="numeric"
					autocomplete="off"
					maxlength="4"
					placeholder="2319"
					bind:value={dot}
					oninput={() => { if (!puudutatud) { puudutatud = true; track('sisestus'); } }}
				/>
				<p class="rv-abi">{t('Numbrid on ovaalses raamis DOT-tähtede järel. Esimesed kaks on nädal, viimased kaks aasta: 2319 = 23. nädal 2019.')}</p>
			</div>
			<svg class="rv-pilt" viewBox="0 0 360 120" role="img" aria-label={t('Kus DOT-kood rehvil asub')}>
				<path d="M0 120 A 420 420 0 0 1 360 120" fill="#2b3039" />
				<path d="M0 120 A 420 420 0 0 1 360 120" fill="none" stroke="#3a404b" stroke-width="44" transform="translate(0 40)" opacity=".6" />
				<text x="58" y="74" fill="#9aa3af" font-size="17" font-weight="700" font-family="Inter, system-ui, sans-serif" letter-spacing="2" transform="rotate(-8 58 74)">DOT 4B YC 9RX</text>
				<g transform="rotate(5 262 68)">
					<rect x="222" y="50" width="82" height="34" rx="17" fill="none" stroke="#ffc20e" stroke-width="3" />
					<text x="263" y="74" text-anchor="middle" fill="#ffc20e" font-size="20" font-weight="800" font-family="Inter, system-ui, sans-serif" letter-spacing="1">{String(dot).replace(/\D/g, '').padEnd(4, '·').slice(0, 4)}</text>
				</g>
			</svg>
		</div>

		<div class="rv-vastus" aria-live="polite">
			{#if !kood}
				<p class="rv-tyhi">{t('Sisesta numbrid ja näed kohe rehvi vanust.')}</p>
			{:else if kood.viga}
				<p class="rv-viga">{kood.viga}</p>
			{:else}
				{#if kood.vana}
					<p class="rv-pea">{t('Toodetud enne 2000. aastat')}</p>
				{:else}
					<p class="rv-pea">{t('Toodetud')} {kuuNimi(kood.algus)} · {t('nädal')} {kood.n}</p>
				{/if}
				<p class="rv-vanus">{vanusSilt}</p>
				{#if vanusHinne}<p class="rv-hinne {vanusHinne[0]}"><b>{vanusHinne[1]}.</b> {vanusHinne[2]}</p>{/if}
			{/if}
		</div>
	</div>

	{#if kood && !kood.viga}
		<div class="rv-kaart rv-teine">
			<div>
				<p class="rv-lab"><span>2</span>{t('Rehv ja muster')}</p>
				<div class="rv-seg" role="group" aria-label={t('Rehvi liik')}>
					<button type="button" aria-pressed={liik === 'suvi'} onclick={() => (liik = 'suvi')}>{t('Suverehv')}</button>
					<button type="button" aria-pressed={liik === 'talv'} onclick={() => { liik = 'talv'; muster = Math.min(muster, UUS.talv); }}>{t('Talverehv')}</button>
				</div>
				<label class="rv-sl" for="rv-muster">
					<span>{t('Mustri sügavus')}</span><b>{f1(muster)} {t('mm')}</b>
				</label>
				<input id="rv-muster" type="range" min="1" max={UUS[liik]} step="0.5" bind:value={muster} onchange={() => track('muster', liik + ' ' + muster)} />
				<div class="rv-sk"><span>1 {t('mm')}</span><span>{t('uus')} {UUS[liik]} {t('mm')}</span></div>
				<p class="rv-hinne {musterHinne[0]} rv-v"><b>{musterHinne[1]}.</b> {t('Mõõda kõige kulunuma koha pealt: mündi või mustrisügavuse mõõtjaga. Seadus: suverehv vähemalt 1,6 mm, talverehv üle 3 mm.')}</p>
				<p class="rv-lab rv-lab2">{t('Tee ja kiirus')}</p>
				<div class="rv-seg" role="group" aria-label={t('Tee')}>
					<button type="button" aria-pressed={tee === 'marg'} onclick={() => { tee = 'marg'; kiirus = 90; }}>{t('Märg asfalt')}</button>
					<button type="button" aria-pressed={tee === 'lumi'} disabled={liik !== 'talv'} title={liik !== 'talv' ? t('Lumel ainult talverehviga') : ''} onclick={() => { tee = 'lumi'; kiirus = 50; }}>{t('Lumi')}</button>
				</div>
				<div class="rv-seg" role="group" aria-label={t('Kiirus')}>
					{#each [50, 70, 90, 110] as k (k)}<button type="button" aria-pressed={kiirus === k} onclick={() => (kiirus = k)}>{k} {t('km/h')}</button>{/each}
				</div>
			</div>

			<div class="rv-tul">
				{#if tulemus}
					<p class="rv-tpea">{t('Pidurdusmaa')} · {tee === 'lumi' ? t('lumi') : t('märg asfalt')} · {kiirus} {t('km/h')}</p>
					<div class="rv-ribad">
						<div class="rv-r"><span class="n">{t('Uus rehv')} <small>{UUS[liik]} {t('mm')}</small></span><span class="b"><i style="width:{(tulemus.uus / ribaMax) * 100}%"></i></span><b>{f1(tulemus.uus)} {t('m')}</b></div>
						<div class="rv-r me"><span class="n">{t('Sinu rehv')} <small>{f1(muster)} {t('mm')} · {vanusSilt}</small></span><span class="b"><i style="width:{(tulemus.sinu / ribaMax) * 100}%"></i></span><b>{f1(tulemus.sinu)} {t('m')}</b></div>
					</div>
					{#if tulemus.lisa >= 0.3}
						<p class="rv-suur">+{f1(tulemus.lisa)} {t('m')} <small>({Math.round((tulemus.lisa / tulemus.uus) * 100)}% {t('pikem')})</small></p>
						{#if tulemus.jaak >= 3}<p class="rv-jaak">{t('Kohas, kus uute rehvidega auto juba seisab, sõidad sina veel')} <b>{Math.round(tulemus.jaak)} {t('km/h')}</b>.</p>{/if}
						{#if tulemus.ainultVanus >= 0.3}<p class="rv-sel">{t('Sellest vanuse arvelt')} {f1(tulemus.ainultVanus)} {t('m')}, {t('ülejäänu kulunud mustri tõttu.')}</p>{/if}
					{:else}
						<p class="rv-suur ok">{t('Peaaegu sama nagu uuel rehvil')}</p>
					{/if}
					<p class="rv-sel">{veh?.name} · {t('keskmine rehv (märghaardeklass C)')} · {t('ainult pidurdus, reaktsiooniaeg on lisaks.')}</p>
					<div class="rv-nupud">
						{#if halb}<a class="btn yel" href={keel.L('/rehvi-valimine/')} onclick={() => track('cta', 'valimine')}>{t('Vali uued rehvid')} →</a>{/if}
						<a class="btn" href={keel.L('/')} onclick={() => track('cta', 'kalkulaator')}>{t('Arvuta oma auto ja rehviga')}</a>
					</div>
				{:else}
					<p class="rv-tyhi">{t('Laen…')}</p>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.rv { max-width: 980px; margin: 0 auto; padding: var(--sp-6) 0 var(--sp-10); display: grid; gap: var(--sp-4); }
	.rv-kaart { background: #fff; border: 1px solid var(--line); border-radius: var(--r-lg, 16px); padding: var(--sp-5); display: grid; grid-template-columns: 1.1fr 1fr; gap: var(--sp-6); align-items: start; }
	@media (max-width: 820px) { .rv-kaart { grid-template-columns: 1fr; gap: var(--sp-4); } }
	.rv-lab { display: flex; gap: 10px; align-items: center; font-weight: 800; font-size: 16px; margin: 0 0 var(--sp-3); }
	.rv-lab span { display: inline-grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: var(--ink); color: var(--yellow); font-size: 14px; flex: none; }
	.rv-lab2 { margin-top: var(--sp-4); font-size: 14.5px; }
	.rv-rida { display: flex; gap: var(--sp-3); align-items: center; }
	.rv-dot { width: 150px; flex: none; font-family: var(--display); font-weight: 700; font-size: 44px; letter-spacing: 0.12em; text-align: center; padding: 6px 10px; border: 2px solid var(--line); border-radius: 12px; background: var(--paper-2); color: var(--text); }
	.rv-dot:focus { outline: none; border-color: var(--yellow); background: #fff; }
	.rv-abi { margin: 0; font-size: 13.5px; color: var(--muted); line-height: 1.45; }
	.rv-pilt { width: 100%; max-width: 420px; margin-top: var(--sp-3); display: block; border-radius: 12px; background: #16181d; }
	.rv-vastus { min-height: 120px; }
	.rv-tyhi { color: var(--muted); margin: 0; }
	.rv-viga { color: var(--red); font-weight: 700; margin: 0; }
	.rv-pea { margin: 0; color: var(--muted); font-weight: 700; font-size: 14px; text-transform: uppercase; letter-spacing: 0.04em; }
	.rv-vanus { margin: 4px 0 var(--sp-3); font-family: var(--display); font-weight: 700; font-size: clamp(40px, 6vw, 56px); line-height: 1; text-transform: uppercase; }
	.rv-hinne { margin: 0; padding: var(--sp-3) var(--sp-4); border-radius: 10px; font-size: 14.5px; line-height: 1.45; background: var(--paper-2); border-left: 4px solid var(--line); }
	.rv-hinne.hea { border-color: #16a34a; background: #f0fdf4; }
	.rv-hinne.jalgi { border-color: #eab308; background: #fefce8; }
	.rv-hinne.moelda { border-color: #f97316; background: #fff7ed; }
	.rv-hinne.vaheta { border-color: var(--red); background: #fef2f2; }
	.rv-v { margin-top: var(--sp-3); font-size: 13.5px; }
	.rv-seg { display: flex; flex-wrap: wrap; gap: var(--sp-1); background: var(--paper-2); border: 1px solid var(--line); padding: var(--sp-1); border-radius: 10px; margin-bottom: var(--sp-2); width: fit-content; }
	.rv-seg button { border: 0; background: transparent; padding: 7px 12px; border-radius: 7px; font-weight: 600; font-size: 14px; color: var(--muted); cursor: pointer; }
	.rv-seg button[aria-pressed='true'] { background: #fff; color: var(--text); box-shadow: inset 0 -2px 0 var(--yellow); }
	.rv-seg button:disabled { opacity: 0.45; cursor: default; }
	.rv-sl { display: flex; justify-content: space-between; align-items: baseline; margin: var(--sp-3) 0 4px; font-weight: 600; font-size: 14.5px; }
	.rv-sl b { font-family: var(--display); font-size: 26px; }
	.rv-teine input[type='range'] { width: 100%; accent-color: var(--ink); }
	.rv-sk { display: flex; justify-content: space-between; font-size: 12.5px; color: var(--muted); }
	.rv-tul { background: var(--ink); color: #fff; border-radius: 14px; padding: var(--sp-5); }
	.rv-tpea { margin: 0 0 var(--sp-3); color: var(--yellow); font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; }
	.rv-ribad { display: grid; gap: var(--sp-3); }
	.rv-r { display: grid; grid-template-columns: 1fr auto; gap: 4px 10px; align-items: center; }
	.rv-r .n { font-size: 14px; color: #cfd4db; grid-column: 1 / -1; }
	.rv-r .n small { color: #8b93a0; margin-left: 4px; }
	.rv-r .b { height: 12px; background: #23262d; border-radius: 6px; overflow: hidden; }
	.rv-r .b i { display: block; height: 100%; background: #4ade80; border-radius: 6px; transition: width 0.25s; }
	.rv-r.me .b i { background: var(--yellow); }
	.rv-r b { font-weight: 800; min-width: 64px; text-align: right; }
	.rv-suur { margin: var(--sp-4) 0 0; font-family: var(--display); font-weight: 700; font-size: 44px; line-height: 1; color: #ff7a7a; }
	.rv-suur small { font-family: var(--body, Inter), system-ui, sans-serif; font-size: 16px; color: #cfd4db; font-weight: 600; }
	.rv-suur.ok { color: #4ade80; font-size: 30px; }
	.rv-jaak { margin: var(--sp-2) 0 0; color: #e5e7eb; }
	.rv-jaak b { color: #ff7a7a; }
	.rv-sel { margin: var(--sp-2) 0 0; color: #8b93a0; font-size: 13px; line-height: 1.45; }
	.rv-nupud { display: flex; flex-wrap: wrap; gap: var(--sp-2); margin-top: var(--sp-4); }
	.rv-tul .btn:not(.yel) { background: #23262d; color: #fff; border-color: #343944; }
	@media (max-width: 640px) { .rv-dot { width: 120px; font-size: 36px; } .rv-rida { align-items: flex-start; } .rv-nupud .btn { flex: 1 1 100%; text-align: center; justify-content: center; } }
</style>
