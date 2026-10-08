<script>
	import Meta from '$lib/Meta.svelte';
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

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/autod/')}>{t('Autod')}</a><span>/</span><a href={L('/autod/' + a.mk + '/')}>{a.make}</a><span
				>/</span
			>{a.model}
			{a.yearLabel}
		</div>
		<h1>{t('{nimi} rehvid ja pidurdusmaa', { nimi: a.nimi })}</h1>
		<p>
			{@html t('Tehase põhimõõt on <b>{moot}</b>.', { moot: esc(data.pohimoot) })}{#if marg90}{' '}{@html t('Märjal asfaldil 90 km/h pealt peatub see auto keskmise (C-klassi) suverehviga umbes <b>{m} meetriga</b>', { m: Math.round(marg90) })}{#if lumi50}{@html t(', tallatud lumel 50 km/h pealt talverehviga umbes <b>{m} meetriga</b>', { m: Math.round(lumi50) })}{/if}.{/if}
		</p>
		<p class="ad-cta">
			<a class="btn yel" href={L('/') + autoQ}>{t('Arvuta oma rehviga')}</a>
			<a class="btn" href={L('/rehvi-valimine/') + autoQ}>{t('Leia sobiv rehv')}</a>
		</p>
	</div>
</section>

<div class="body-sec">
	<div class="wrap">
		<div class="box">
			<h2>{t('Tehase rehvimõõdud')}</h2>
			<p class="sub">{t('Mõõdud, millega see põlvkond tehasest tuli. Täpne mõõt on rehvi küljel ja juhiukse piirdel.')}</p>
			<ul class="ad-moodud">
				{#each data.moodud as z (z.m)}
					<li class:pohi={z.pohi}>
						{#if z.slug}<a href={L("/rehvid/" + z.slug + "/")}>{z.label}</a>{:else}{z.label}{/if}
						{#if z.pohi}<span class="pill">{t('põhimõõt')}</span>{/if}
					</li>
				{/each}
			</ul>
		</div>

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

		{#each [['suvi', data.suvi], ['talv', data.talv], ['aastaring', data.aastaring]] as [k, list] (k)}
			{#if list.length}
				<div class="box">
					<h2>{t(PEALKIRI[k], { moot: data.pohimoot })}</h2>
					<p class="sub">{t('Sõltumatult testitud mudelid eespool, seejärel EL-i märgise märghaardumise klassi järgi.')}</p>
					<div class="tbl-wrap">
						<table class="t">
							<thead><tr><th>{t('Rehv')}</th><th>{t('Märghaardumine')}</th><th class="n">{t('Müra')}</th></tr></thead>
							<tbody>
								{#each list as r (r.slug)}
									<tr>
										<td
											><a href={L("/rehvid/" + r.slug + "/")}>{r.nimi}</a>{#if r.testitud}
												<span class="pill test" style="margin-left:var(--sp-2)">{t('testitud')}</span>{/if}</td
										>
										<td>{r.g || '–'}</td>
										<td class="n">{r.db ? r.db + ' dB' : '–'}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					{#if k === 'talv' && data.talvSlug}<p class="note"><a href={L('/talverehvid/' + data.talvSlug + '/')}>{t('Parimad talverehvid {m} — testid, naast ja lamell →', { m: data.pohimoot })}</a></p>{/if}
					{#if data.pohimootSlug}<p class="note"><a href={L("/rehvid/" + data.pohimootSlug + "/")}>{t('Kõik rehvid mõõdus {moot} →', { moot: data.pohimoot })}</a></p>{/if}
				</div>
			{/if}
		{/each}

		<div class="box">
			<h2>{t('Mootorid')}</h2>
			<p class="sub">{t('Tehase mootorid. Kui mootoril on oma rehvimõõt või mass, arvestab kalkulaator seda.')}</p>
			<div class="tbl-wrap">
				<table class="t">
					<thead><tr><th>{t('Mootor')}</th><th>{t('Kütus')}</th><th>{t('Aastad')}</th><th>{t('Rehvimõõt')}</th><th class="n">{t('Tühimass')}</th></tr></thead>
					<tbody>
						{#each data.mootorid as m (m.key)}
							<tr>
								<td><a href={L('/') + '?auto=' + encodeURIComponent(m.key)}>{an(hj(m.silt)) || a.model}</a></td>
								<td>{m.kytus ? t(m.kytus) : '–'}</td>
								<td>{m.aastad || '–'}</td>
								<td>{m.moot || '–'}</td>
								<td class="n">{m.mass ? m.mass + ' ' + t('kg') : '–'}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
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
