<script>
	import Meta from '$lib/Meta.svelte';
	import AutoPilt from '$lib/AutoPilt.svelte';
	import { BASE } from '$lib/skeem.js';
	import { useT, useLang, autoNimi } from '$lib/i18n.js';
	/* Tekstid: eesti keel on lähtetekst, vene tõlge $lib/i18n/ru.js (/ru/autod/…) */
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	let { data } = $props();
	const an = (s) => autoNimi(keel.lang, s);
	/* vene keeles E-klass → E-Класс jne (ainult nähtav nimi; mk/slug jäävad) */
	const a = $derived({ ...data.auto, nimi: an(data.auto.nimi), model: an(data.auto.model), yearLabel: an(data.auto.yearLabel) });
	const path = $derived('/autod/' + a.mk + '/' + a.slug + '/');
	const DEC = keel.lang === 'en' ? '.' : ',';
	const f1 = (x) => (x == null ? '–' : (Math.round(x * 10) / 10).toFixed(1).replace('.', DEC));
	const marg90 = $derived(data.pidurdus.find((x) => x.id === 'marg')?.r?.[90]?.peatumine);
	const lumi50 = $derived(data.pidurdus.find((x) => x.id === 'lumiT')?.r?.[50]?.peatumine);
	/* heros pidurdusmaa (pidur põhja kuni seisuni, ilma reaktsioonita) — sama mõiste mis kalkulaatori suur number */
	const margP = $derived(data.pidurdus.find((x) => x.id === 'marg')?.r?.[90]?.pidurdus);
	const lumiP = $derived(data.pidurdus.find((x) => x.id === 'lumiT')?.r?.[50]?.pidurdus);
	const nMootoreid = $derived(data.mootorid.length);
	const desc = $derived(
		t(nMootoreid === 1 ? '{nimi}: rehvimõõt {moot}, {n} mootor.' : '{nimi}: rehvimõõt {moot}, {n} mootorit.', { nimi: a.nimi, moot: data.pohimoot, n: nMootoreid }) +
			(marg90 ? ' ' + t('Märjal 90 km/h pealt peatub ~{m} m.', { m: Math.round(marg90) }) : '') +
			' ' + t('Parimad rehvid selles mõõdus.')
	);
	const PEALKIRI = { suvi: 'Suverehvid mõõdus {moot}', talv: 'Talverehvid (Põhjamaade, naastudeta) mõõdus {moot}', aastaring: 'Aastaringsed rehvid mõõdus {moot}' };
	const autoQ = $derived('?auto=' + encodeURIComponent(a.key));
	/* mootori silt „1.6 TDI · 105 hj (77 kW)“ */
	const hj = (s) => (s ? String(s).replace(/ hj \(/, ' ' + t('hj') + ' (') : s);
	const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
	const pealkiri = $derived(t('{nimi} rehvimõõt ja pidurdusmaa', { nimi: a.nimi }));

	/* KKK (AI-otsing / FAQPage): vastused ainult lehe andmetest */
	const kuiv90 = $derived(data.pidurdus.find((x) => x.id === 'kuiv')?.r?.[90]?.peatumine);
	const ja = (arr) => (arr.length < 2 ? arr.join('') : arr.slice(0, -1).join(', ') + ' ' + t('ja') + ' ' + arr[arr.length - 1]);
	const kkk = $derived(
		[
			[
				t('Mis rehvimõõt on autol {nimi}?', { nimi: a.nimi }),
				t('Tehase põhimõõt on {moot}.', { moot: data.pohimoot }) +
					(data.moodud.length > 1 ? ' ' + t('Tehase mõõte on kokku {n}: {list}.', { n: data.moodud.length, list: data.moodud.map((z) => z.label).join(', ') }) : '') +
					' ' + t('Täpne mõõt on rehvi küljel ja juhiukse piirdel.')
			],
			marg90 && kuiv90
				? [
						t('Kui pikk on {nimi} pidurdusmaa?', { nimi: a.nimi }),
						t('Keskmise suverehviga peatub {nimi} 90 km/h pealt kuival asfaldil umbes {k} meetriga ja märjal umbes {m} meetriga (koos 1 s reaktsiooniga).', { nimi: a.nimi, k: Math.round(kuiv90), m: Math.round(marg90) }) +
							(lumi50 ? ' ' + t('Tallatud lumel 50 km/h pealt talverehviga umbes {l} m.', { l: Math.round(lumi50) }) : '') +
							' ' + t('See on arvutatud hinnang, mitte mõõtmine; täpne tulemus sõltub rehvist.')
					]
				: null,
			data.talv.length
				? [
						t('Millised talverehvid sobivad autole {nimi}?', { nimi: a.nimi }),
						t('Põhimõõdus {moot} on EL-i rehvimärgise järgi head Põhjamaade talverehvid näiteks {list}.', { moot: data.pohimoot, list: ja(data.talv.slice(0, 3).map((r) => r.nimi)) }) +
							' ' + t('Eesti talveks sobib naast- või Põhjamaade lamellrehv; talverehvid on kohustuslikud 1. detsembrist 1. märtsini.')
					]
				: null,
			data.suvi.length
				? [
						t('Millised suverehvid sobivad autole {nimi}?', { nimi: a.nimi }),
						t('Põhimõõdus {moot} on märghaardumise klassi järgi parimad suverehvid näiteks {list}.', { moot: data.pohimoot, list: ja(data.suvi.slice(0, 3).map((r) => r.nimi)) }) +
							' ' + t('Sõltumatult testitud mudelid on nimekirjas eespool.')
					]
				: null,
			[t('Kas autol {nimi} on ABS?', { nimi: a.nimi }), t(data.absTekst)]
		].filter(Boolean)
	);
	const nimekiri = (nimi, list) =>
		list.length ? [{ '@type': 'ItemList', name: nimi, itemListElement: list.map((r, i) => ({ '@type': 'ListItem', position: i + 1, name: r.nimi, url: BASE + L('/rehvid/' + r.slug + '/') })) }] : [];
	const jsonld = $derived({
		'@context': 'https://schema.org',
		'@graph': [
			{
				'@type': 'WebPage',
				name: pealkiri,
				description: desc,
				url: BASE + L(path),
				inLanguage: keel.lang
				/* NB: mitte 'Car' / 'Vehicle' / 'Product' — Google peab neid tooteks ja
				   nõuab hinda või arvustusi; ilma nendeta on see Search Console'is viga */
			},
			{ '@type': 'FAQPage', mainEntity: kkk.map(([q, an]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: an } })) },
			...nimekiri(t('Parimad suverehvid mõõdus {moot}', { moot: data.pohimoot }), data.suvi),
			...nimekiri(t('Parimad talverehvid mõõdus {moot}', { moot: data.pohimoot }), data.talv)
		]
	});
</script>

<Meta
	title={pealkiri}
	{desc}
	path="autod/{a.mk}/{a.slug}/"
	image="/og/auto/{a.mk}--{a.slug}.png"
	imageAlt={t('{nimi} — rehvimõõt ja pidurdusmaa', { nimi: a.nimi })}
	crumbs={[[t('Avaleht'), '/'], [t('Autod'), '/autod/'], [a.make, '/autod/' + a.mk + '/'], [a.model + ' ' + a.yearLabel, path]]}
	{jsonld}
/>

<section class="page-hero ad-hero">
	<div class="wrap ad-hero-in">
		<div class="ad-hero-txt">
			<div class="crumbs">
				<a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/autod/')}>{t('Autod')}</a><span>/</span><a href={L('/autod/' + a.mk + '/')}>{a.make}</a><span
					>/</span
				>{a.model}
				{a.yearLabel}
			</div>
			<p class="ad-mark">{a.make}</p>
			<h1>{a.model} <span class="ad-aastad">{a.yearLabel}</span></h1>
			<p class="ad-lyhi">{t('Rehvid ja pidurdusmaa')}</p>
			<ul class="ad-faktid">
				<li><small>{t('Rehvimõõt')}</small><b>{data.pohimoot}</b></li>
				{#if margP}<li><small>{t('Märjal 90→0')}</small><b>~{Math.round(margP)} {t('m')}</b></li>{/if}
				{#if lumiP}<li><small>{t('Lumel 50→0')}</small><b>~{Math.round(lumiP)} {t('m')}</b></li>{/if}
			</ul>
		</div>
		<div class="ad-pilt"><AutoPilt keha={a.keha} moot={data.pohimoot} /></div>
	</div>
</section>

<!-- rehvivalik selle auto jaoks: sama nimekiri mis /rehvi-valimine/, lihtsustatud (app.js initTyres, data-auto) -->
<div class="body-sec ad-valik" data-cmp-page data-mode="valik" data-auto={a.key} data-lihtne>
	<div class="wrap">
		<div class="box ad-samm">
			<h2 class="ad-sh"><span>1</span>{t('Vali oma mootor')}</h2>
			<p class="sub">{t('Mootoril võib olla oma rehvimõõt ja mass — nii on rehvid ja pidurdusmaa täpselt sinu autole.')}</p>
			<div class="ad-mootorid" role="group" aria-label={t('Mootor')}>
				{#each data.mootorid as m (m.key)}
					<button type="button" class="ad-mootor" data-mootor={m.key} aria-pressed={m.key === a.key ? 'true' : 'false'}>
						<b>{an(hj(m.silt)) || a.model}</b>
						<span>{[m.kytus ? t(m.kytus) : '', m.aastad].filter(Boolean).join(' · ')}</span>
						<span class="ad-m-moot">{m.moot || data.pohimoot}</span>
					</button>
				{/each}
			</div>
		</div>

		<div class="box ad-samm">
			<h2 class="ad-sh"><span>2</span>{t('Sinu autole sobivad rehvid')}</h2>
			<div class="ad-seaded">
				<div class="lseg ad-hooaeg" role="group" aria-label={t('Rehvi liik')}>
					<button type="button" data-season="summer">{t('Suverehv')}</button>
					<button type="button" data-season="winter">{t('Lamell')}</button>
					<button type="button" data-season="naast">{t('Naast')}</button>
				</div>
				<label class="ad-moot">
					<span>{t('Rehvimõõt')}</span>
					<select class="lsel" data-f="size"><option value={data.moodud.find((z) => z.pohi)?.m || ''}>{data.pohimoot}</option></select>
				</label>
			</div>
			<div class="list-filter">
				<select class="lsel" data-brand aria-label={t('Mark')}><option value="">{t('Kõik margid')}</option></select>
				<input class="lsel" type="search" data-q placeholder={t('Otsi marki või mudelit')} aria-label={t('Otsi rehvi')} style="background-image:none" />
			</div>
			<p class="note" data-cmp-head style="margin:0 0 var(--sp-3);font-size:15px"></p>
			<div class="res-list" data-cmp-list>
				<!-- enne JS-i (ja otsingumootoritele): parimad märgise järgi põhimõõdus -->
				{#each [['suvi', data.suvi], ['talv', data.talv]] as [k, list] (k)}
					{#if list.length}
						<p class="note"><b>{t(PEALKIRI[k], { moot: data.pohimoot })}</b></p>
						<ul class="ad-ssr">
							{#each list as r (r.slug)}<li><a href={L('/rehvid/' + r.slug + '/')}>{r.nimi}</a> · {r.g || '–'}{#if r.testitud} · {t('testitud')}{/if}</li>{/each}
						</ul>
					{/if}
				{/each}
			</div>
		</div>
	</div>
</div>

<div class="cmp-tray" data-tray hidden>
	<div class="wrap">
		<div class="chips" data-tray-chips></div>
		<a class="btn yel sm" href={L('/vordle-rehve/')} data-tray-go>{t('Võrdle kõrvuti →')}</a>
	</div>
</div>

<div class="body-sec" style="padding-top:0">
	<div class="wrap">
		<div class="box">
			<h2>{t('Pidurdusmaa')}</h2>
			<p class="sub">
				{t('Peatumisteekond (reaktsioon 1 s + pidurdus) uute, keskmise märgiseklassiga (C) rehvidega, põhimõõdus {moot}. Muuda tingimusi', { moot: data.pohimoot })}
				<a href={L('/') + autoQ}>{t('kalkulaatoris')}</a>.
			</p>
			<div class="tbl-wrap">
				<table class="t ad-kompakt">
					<thead><tr><th>{t('Tingimused')}</th><th class="n">50 {t('km/h')}</th><th class="n">90 {t('km/h')}</th></tr></thead>
					<tbody>
						{#each data.pidurdus as x (x.id)}
							<tr>
								<td>{t(x.nimi)}</td>
								<td class="n">{x.r[50]?.peatumine != null ? f1(x.r[50].peatumine) + ' ' + t('m') : t('ei peatu')}</td>
								<td class="n">{x.r[90]?.peatumine != null ? f1(x.r[90].peatumine) + ' ' + t('m') : t('ei peatu')}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
			<p class="note">{t(data.absTekst)} {t('Hinnang, mitte mõõtmine — päris pidurdusmaa sõltub konkreetsest rehvist, teest ja juhist.')}</p>
		</div>

		<div class="box">
			<h2>{t('Korduma kippuvad küsimused')}</h2>
			{#each kkk as [q, v] (q)}<h3 class="ad-kkk-k">{q}</h3><p class="ad-kkk-v">{v}</p>{/each}
			{#if data.talvSlug}<p class="note"><a href={L('/talverehvid/' + data.talvSlug + '/')}>{t('Parimad talverehvid {m} — testid, naast ja lamell →', { m: data.pohimoot })}</a></p>{/if}
		</div>

		{#if data.muudPolved.length}
			<div class="box">
				<h2>{t('Teised põlvkonnad')}</h2>
				<ul class="ad-muud">
					{#each data.muudPolved as p (p.slug)}<li><a href={L('/autod/' + a.mk + '/' + p.slug + '/')}>{an(p.nimi)}</a></li>{/each}
				</ul>
			</div>
		{/if}
		<p class="note">
			{t('Andmed: tootjate andmed ja auto-data.net (mõõdud, mootorid, mass), EL-i tooteregister EPREL (rehvimärgis), sõltumatud rehvitestid.')}
			<a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">{t('Kuidas pidurdusmaa arvutatakse')}</a>.
		</p>
	</div>
</div>

<style>
	/* ---- hero: auto pilt + põhifaktid */
	.ad-hero { padding-bottom: var(--sp-8); }
	.ad-hero-in { display: grid; grid-template-columns: 1.05fr 1fr; gap: var(--sp-8); align-items: center; }
	.ad-mark { color: var(--yellow) !important; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; font-size: 14px !important; margin: var(--sp-4) 0 var(--sp-1) !important; }
	.ad-aastad { color: #9aa2ae; font-size: 0.5em; letter-spacing: 0.02em; white-space: nowrap; }
	.ad-lyhi { font-size: 18px; margin: 0 0 var(--sp-5) !important; }
	.ad-faktid { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: var(--sp-3); }
	.ad-faktid li { background: var(--ink-3); border: 1px solid var(--line-d, #2a2f39); border-radius: 14px; padding: 10px 16px; display: grid; gap: 2px; min-width: 128px; }
	.ad-faktid small { color: #9aa2ae; font-size: 12.5px; }
	.ad-faktid b { color: #fff; font-size: 22px; font-family: var(--display); letter-spacing: 0.01em; }
	.ad-pilt { max-width: 520px; justify-self: center; width: 100%; }
	@media (max-width: 820px) {
		.ad-hero-in { grid-template-columns: 1fr; gap: var(--sp-4); }
		.ad-pilt { order: 2; max-width: 420px; }
		.ad-faktid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--sp-2); }
		.ad-faktid li { min-width: 0; padding: 8px 10px; border-radius: 12px; }
		.ad-faktid small { font-size: 11.5px; }
		.ad-faktid b { font-size: 18px; white-space: nowrap; }
		.ad-sh { font-size: 26px; }
	}
	/* ---- 1. mootor, 2. rehvid */
	.ad-valik { padding-bottom: var(--sp-6); }
	.ad-samm { margin-bottom: var(--sp-6); }
	.ad-sh { display: flex; align-items: center; gap: var(--sp-3); margin: 0 0 var(--sp-2); }
	.ad-sh span { display: inline-grid; place-items: center; width: 34px; height: 34px; border-radius: 50%; background: var(--yellow); color: var(--yellow-ink); font-size: 18px; flex: none; }
	.ad-mootorid { display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: var(--sp-3); max-height: 340px; overflow-y: auto; padding: 2px; }
	.ad-mootor { text-align: left; display: grid; gap: 3px; padding: 12px 14px; border: 1.5px solid var(--line); border-radius: 14px; background: #fff; cursor: pointer; font: inherit; color: inherit; transition: border-color 0.15s, background 0.15s; }
	.ad-mootor:hover { border-color: #c5cad3; }
	.ad-mootor b { font-size: 15px; line-height: 1.3; }
	.ad-mootor span { color: var(--muted); font-size: 13px; }
	.ad-mootor .ad-m-moot { justify-self: start; margin-top: 4px; padding: 2px 9px; border-radius: 999px; background: var(--bg-2, #f3f4f6); color: var(--text); font-weight: 600; font-size: 12.5px; }
	.ad-mootor[aria-pressed='true'] { border-color: var(--yellow); background: var(--yellow-soft); box-shadow: 0 0 0 2px var(--yellow) inset; }
	.ad-mootor[aria-pressed='true'] .ad-m-moot { background: var(--yellow); color: var(--yellow-ink); }
	@media (max-width: 640px) {
		/* telefonis üks rida, keritav külgsuunas */
		.ad-mootorid { display: flex; overflow-x: auto; max-height: none; scroll-snap-type: x mandatory; padding-bottom: var(--sp-2); }
		.ad-mootor { flex: 0 0 78%; scroll-snap-align: start; }
	}
	.ad-seaded { display: flex; flex-wrap: wrap; gap: var(--sp-3) var(--sp-5); align-items: end; margin: var(--sp-3) 0 var(--sp-4); }
	.ad-hooaeg button { min-width: 96px; }
	.ad-moot { display: grid; gap: 4px; font-size: 13px; color: var(--muted); font-weight: 600; }
	.ad-moot select { min-width: 210px; }
	.ad-ssr { margin: 0 0 var(--sp-4); padding-left: var(--sp-5); }
	.ad-kkk-k { font-size: 17px; margin: var(--sp-4) 0 var(--sp-1); }
	.ad-kkk-v { margin: 0; }
	:global(table.t.ad-kompakt) {
		min-width: 0;
	}
	.ad-cta {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-3);
		margin-top: var(--sp-4);
	}
	.ad-moodud,
	.ad-muud {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-2);
	}
	.ad-moodud li {
		border: 1px solid var(--line);
		border-radius: 999px;
		padding: 4px 12px;
		background: #fff;
		display: flex;
		gap: var(--sp-2);
		align-items: center;
	}
	.ad-moodud li.pohi {
		border-color: var(--yellow);
		background: var(--yellow-soft);
	}
	.ad-muud li a {
		display: inline-block;
		padding: 4px 12px;
		border: 1px solid var(--line);
		border-radius: 999px;
		background: #fff;
	}
</style>
