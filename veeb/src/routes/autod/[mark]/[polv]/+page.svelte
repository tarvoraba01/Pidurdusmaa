<script>
	import Meta from '$lib/Meta.svelte';
	import { BASE } from '$lib/skeem.js';
	import { useT, useLang } from '$lib/i18n.js';
	/* Tekstid: eesti keel on lähtetekst, vene tõlge $lib/i18n/ru.js (/ru/autod/…) */
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	let { data } = $props();
	const a = $derived(data.auto);
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
</script>

<Meta
	title={pealkiri}
	{desc}
	path="autod/{a.mk}/{a.slug}/"
	image="/og/auto/{a.mk}--{a.slug}.png"
	imageAlt={t('{nimi} — rehvimõõt ja pidurdusmaa', { nimi: a.nimi })}
	crumbs={[[t('Avaleht'), '/'], [t('Autod'), '/autod/'], [a.make, '/autod/' + a.mk + '/'], [a.model + ' ' + a.yearLabel, path]]}
	jsonld={{
		'@context': 'https://schema.org',
		'@type': 'WebPage',
		name: pealkiri,
		description: desc,
		url: BASE + L(path),
		inLanguage: keel.lang
		/* NB: mitte 'Car' / 'Vehicle' / 'Product' — Google peab neid tooteks ja
		   nõuab hinda või arvustusi; ilma nendeta on see Search Console'is viga */
	}}
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
						{#if z.slug}<a href="/rehvid/{z.slug}/">{z.label}</a>{:else}{z.label}{/if}
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
											><a href="/rehvid/{r.slug}/">{r.nimi}</a>{#if r.testitud}
												<span class="pill test" style="margin-left:var(--sp-2)">{t('testitud')}</span>{/if}</td
										>
										<td>{r.g || '–'}</td>
										<td class="n">{r.db ? r.db + ' dB' : '–'}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					{#if data.pohimootSlug}<p class="note"><a href="/rehvid/{data.pohimootSlug}/">{t('Kõik rehvid mõõdus {moot} →', { moot: data.pohimoot })}</a></p>{/if}
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
								<td><a href={L('/') + '?auto=' + encodeURIComponent(m.key)}>{hj(m.silt) || a.model}</a></td>
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

		{#if data.muudPolved.length}
			<div class="box">
				<h2>{t('Teised põlvkonnad')}</h2>
				<ul class="ad-muud">
					{#each data.muudPolved as p (p.slug)}<li><a href={L('/autod/' + a.mk + '/' + p.slug + '/')}>{p.nimi}</a></li>{/each}
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
