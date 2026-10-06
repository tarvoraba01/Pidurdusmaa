<script>
	/* Rehvimõõdu kalkulaator: kaks mõõtu kõrvuti — läbimõõt, külje kõrgus,
	   ümbermõõt, spidomeetri viga ja sama läbimõõduga mõõdud (lingid mõõdulehtedele).
	   Arvutus: külg = laius × profiil / 100; läbimõõt = velg × 25,4 + 2 × külg. */
	import { onMount } from 'svelte';
	import { useT, useLang, onTolgitud } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	let { moodud = [] } = $props();

	const LAIUSED = [125, 135, 145, 155, 165, 175, 185, 195, 205, 215, 225, 235, 245, 255, 265, 275, 285, 295, 305, 315, 325, 335, 345, 355];
	const PROFIILID = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85];
	const VELJED = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];

	let a = $state({ w: 205, p: 55, r: 16 });
	let b = $state({ w: 225, p: 45, r: 17 });
	/* mõõdulehelt tulles (?a=205-55-r16) on praegune mõõt ette valitud */
	onMount(() => {
		try {
			const q = new URLSearchParams(location.search);
			for (const [k, x] of [['a', a], ['b', b]]) {
				const m = /^(\d{3})-(\d{2})-r(\d{2})c?$/i.exec(q.get(k) || '');
				if (m && LAIUSED.includes(+m[1]) && PROFIILID.includes(+m[2]) && VELJED.includes(+m[3])) { x.w = +m[1]; x.p = +m[2]; x.r = +m[3]; }
			}
		} catch {}
	});
	let kiirus = $state(90);

	const LOC = keel.lang === 'en' ? 'en-GB' : keel.lang === 'ru' ? 'ru-RU' : 'et-EE';
	const f = (x, d = 1) => x.toLocaleString(LOC, { minimumFractionDigits: d, maximumFractionDigits: d });
	const mm = t('mm');

	const arvuta = (x) => {
		const kylg = (x.w * x.p) / 100;
		const d = x.r * 25.4 + 2 * kylg;
		return { kylg, d, umber: Math.PI * d, poordeid: 1e6 / (Math.PI * d) };
	};
	const A = $derived(arvuta(a));
	const B = $derived(arvuta(b));
	/* ümardub nulliks -> 0, mitte „−0,0“ */
	const vahe = $derived(((x) => (Math.abs(x) < 0.05 ? 0 : x))((B.d / A.d - 1) * 100));
	const tegelik = $derived(kiirus * (B.d / A.d));
	const hinne = $derived(
		Math.abs(vahe) <= 1.5
			? ['hea', t('Sobib hästi: läbimõõdu vahe on väike.')]
			: Math.abs(vahe) <= 3
				? ['jalgi', t('Üldjuhul sobib, aga kontrolli auto tootja lubatud mõõte.')]
				: ['halb', t('Vahe on üle 3%: spidomeeter, ABS ja ESP ei pruugi õigesti töötada. Kontrolli auto lubatud mõõte.')]
	);

	/* sama läbimõõduga (±1,5%) mõõdud, millel on oma leht */
	const sarnased = $derived.by(() => {
		const out = [];
		for (const s of moodud) {
			const x = /^(\d{3})(\d{2})R(\d{2})$/.exec(s.m);
			if (!x) continue;
			const d = arvuta({ w: +x[1], p: +x[2], r: +x[3] }).d;
			const v = (d / A.d - 1) * 100;
			if (Math.abs(v) <= 1.5 && !(+x[1] === a.w && +x[2] === a.p && +x[3] === a.r)) out.push({ ...s, v, n: s.n });
		}
		return out.sort((p, q) => Math.abs(p.v) - Math.abs(q.v)).slice(0, 12);
	});
	const link = (slug) => {
		const p = '/rehvid/' + slug + '/';
		return onTolgitud(keel.lang, p) ? keel.L(p) : p;
	};
	const silt = (x) => x.w + '/' + x.p + ' R' + x.r;
	function track(v) { try { window.PM_TRACK && window.PM_TRACK('rehvimoot', v); } catch {} }
	let viimane = '';
	$effect(() => { const s = silt(a) + ' → ' + silt(b); if (s !== viimane) { const esimene = !viimane; viimane = s; if (!esimene) track(s); } });
</script>

<div class="rm">
	<div class="rm-kaart">
		{#each [[a, t('Praegune mõõt')], [b, t('Uus mõõt')]] as [x, nimi], i (i)}
			<div class="rm-moot">
				<p class="rm-lab"><span>{i + 1}</span>{nimi}</p>
				<div class="rm-valik">
					<label><small>{t('Laius')}</small><select bind:value={x.w} aria-label={nimi + ' ' + t('Laius')}>{#each LAIUSED as v (v)}<option value={v}>{v}</option>{/each}</select></label>
					<span class="rm-k">/</span>
					<label><small>{t('Profiil')}</small><select bind:value={x.p} aria-label={nimi + ' ' + t('Profiil')}>{#each PROFIILID as v (v)}<option value={v}>{v}</option>{/each}</select></label>
					<span class="rm-k">R</span>
					<label><small>{t('Velg')}</small><select bind:value={x.r} aria-label={nimi + ' ' + t('Velg')}>{#each VELJED as v (v)}<option value={v}>{v}</option>{/each}</select></label>
				</div>
			</div>
		{/each}
	</div>

	<div class="rm-tul">
		<div class="rm-tabel">
			<div class="rm-rida rm-pea"><span></span><b>{silt(a)}</b><b>{silt(b)}</b><b>{t('Vahe')}</b></div>
			<div class="rm-rida"><span>{t('Läbimõõt')}</span><b>{f(A.d)} {mm}</b><b>{f(B.d)} {mm}</b><b class:pl={vahe > 0}>{vahe > 0 ? '+' : ''}{f(vahe)} %</b></div>
			<div class="rm-rida"><span>{t('Külje kõrgus')}</span><b>{f(A.kylg)} {mm}</b><b>{f(B.kylg)} {mm}</b><b>{B.kylg - A.kylg > 0 ? '+' : ''}{f(B.kylg - A.kylg)} {mm}</b></div>
			<div class="rm-rida"><span>{t('Ümbermõõt')}</span><b>{f(A.umber, 0)} {mm}</b><b>{f(B.umber, 0)} {mm}</b><b>{B.umber - A.umber > 0 ? '+' : ''}{f(B.umber - A.umber, 0)} {mm}</b></div>
			<div class="rm-rida"><span>{t('Pöördeid kilomeetril')}</span><b>{f(A.poordeid, 0)}</b><b>{f(B.poordeid, 0)}</b><b>{f(B.poordeid - A.poordeid, 0)}</b></div>
		</div>
		<p class="rm-hinne {hinne[0]}"><b>{vahe > 0 ? '+' : ''}{f(vahe)} %.</b> {hinne[1]}</p>
		<div class="rm-spido">
			<p>{t('Kui spidomeeter näitab')}
				<select bind:value={kiirus} aria-label={t('Spidomeetri näit')}>{#each [50, 90, 110, 130] as v (v)}<option value={v}>{v}</option>{/each}</select>
				{t('km/h')}, {t('sõidad uue mõõduga tegelikult')} <b>{f(tegelik)} {t('km/h')}</b>.</p>
		</div>
	</div>

	{#if sarnased.length}
		<div class="rm-sarn">
			<h2>{t('Sama läbimõõduga mõõdud')} <small>(±1,5 %)</small></h2>
			<p class="rm-sel">{t('Vali, millise mõõdu rehve vaadata — igal lehel on rehvid märghaarde ja testide järgi.')}</p>
			<div class="rm-chips">
				{#each sarnased as s (s.slug)}<a href={link(s.slug)}><b>{s.label}</b> <small>{s.v >= 0.05 ? '+' : ''}{f(Math.abs(s.v) < 0.05 ? 0 : s.v)} %</small></a>{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	.rm { max-width: 980px; margin: 0 auto; padding: var(--sp-6) 0 var(--sp-10); display: grid; gap: var(--sp-4); }
	.rm-kaart { background: #fff; border: 1px solid var(--line); border-radius: var(--r-lg, 16px); padding: var(--sp-5); display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-6); }
	@media (max-width: 720px) { .rm-kaart { grid-template-columns: 1fr; gap: var(--sp-4); } }
	.rm-lab { display: flex; gap: 10px; align-items: center; font-weight: 800; font-size: 16px; margin: 0 0 var(--sp-3); }
	.rm-lab span { display: inline-grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: var(--ink); color: var(--yellow); font-size: 14px; flex: none; }
	.rm-valik { display: flex; align-items: flex-end; gap: 6px; }
	.rm-valik label { display: grid; gap: 4px; flex: 1; }
	.rm-valik small { font-size: 12px; color: var(--muted); font-weight: 600; }
	.rm-valik select { font: inherit; font-family: var(--display); font-weight: 700; font-size: 26px; padding: 6px 8px; border: 2px solid var(--line); border-radius: 10px; background: var(--paper-2); color: var(--text); width: 100%; }
	.rm-valik select:focus { outline: none; border-color: var(--yellow); }
	.rm-k { font-family: var(--display); font-weight: 700; font-size: 26px; padding-bottom: 10px; color: var(--muted); }
	.rm-tul { background: var(--ink); color: #fff; border-radius: var(--r-lg, 16px); padding: var(--sp-5); }
	.rm-tabel { display: grid; gap: 2px; }
	.rm-rida { display: grid; grid-template-columns: 1.3fr 1fr 1fr 0.8fr; gap: var(--sp-2); padding: 8px 0; border-bottom: 1px solid #23262d; align-items: baseline; }
	.rm-rida span { color: #cfd4db; font-size: 14px; }
	.rm-rida b { text-align: right; font-weight: 700; }
	.rm-rida b.pl { color: var(--yellow); }
	.rm-pea b { color: var(--yellow); font-size: 13px; text-transform: uppercase; letter-spacing: 0.04em; }
	@media (max-width: 560px) { .rm-rida { grid-template-columns: 1.2fr 1fr 1fr 0.8fr; font-size: 13.5px; } .rm-rida span { font-size: 12.5px; } }
	.rm-hinne { margin: var(--sp-4) 0 0; padding: var(--sp-3) var(--sp-4); border-radius: 10px; font-size: 14.5px; line-height: 1.45; background: #16181d; border-left: 4px solid #4ade80; }
	.rm-hinne.jalgi { border-color: #eab308; }
	.rm-hinne.halb { border-color: #ff5a5a; }
	.rm-spido { margin-top: var(--sp-3); color: #e5e7eb; }
	.rm-spido p { margin: 0; }
	.rm-spido select { font: inherit; font-weight: 700; background: #23262d; color: #fff; border: 1px solid #343944; border-radius: 7px; padding: 2px 6px; }
	.rm-spido b { color: var(--yellow); }
	.rm-sarn { background: #fff; border: 1px solid var(--line); border-radius: var(--r-lg, 16px); padding: var(--sp-5); }
	.rm-sarn h2 { font-family: var(--display); text-transform: uppercase; font-size: 24px; margin: 0 0 var(--sp-2); }
	.rm-sarn h2 small { font-size: 15px; color: var(--muted); }
	.rm-sel { margin: 0 0 var(--sp-3); color: var(--muted); font-size: 14px; }
	.rm-chips { display: flex; flex-wrap: wrap; gap: var(--sp-2); }
	.rm-chips a { display: inline-flex; gap: 6px; align-items: baseline; padding: 8px 12px; border: 1px solid var(--line); border-radius: 10px; text-decoration: none; color: var(--text); background: var(--paper-2); }
	.rm-chips a:hover { border-color: var(--yellow); }
	.rm-chips small { color: var(--muted); }
</style>
