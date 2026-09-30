<script>
	import Meta from '$lib/Meta.svelte';
	import { BASE } from '$lib/skeem.js';
	let { data } = $props();
	const a = $derived(data.auto);
	const path = $derived('/autod/' + a.mk + '/' + a.slug + '/');
	const f1 = (x) => (x == null ? '–' : (Math.round(x * 10) / 10).toFixed(1).replace('.', ','));
	const marg90 = $derived(data.pidurdus.find((x) => x.id === 'marg')?.r?.[90]?.peatumine);
	const lumi50 = $derived(data.pidurdus.find((x) => x.id === 'lumiT')?.r?.[50]?.peatumine);
	const nMootoreid = $derived(data.mootorid.length);
	const desc = $derived(
		`${a.nimi}: rehvimõõt ${data.pohimoot}, ${nMootoreid} ${nMootoreid === 1 ? 'mootor' : 'mootorit'}.` +
			(marg90 ? ` Märjal 90 km/h pealt peatub ~${Math.round(marg90)} m.` : '') +
			' Parimad rehvid selles mõõdus.'
	);
	const PEALKIRI = { suvi: 'Suverehvid', talv: 'Talverehvid (Põhjamaade, naastudeta)', aastaring: 'Aastaringsed rehvid' };
	const autoQ = $derived('?auto=' + encodeURIComponent(a.key));
</script>

<Meta
	title="{a.nimi} rehvimõõt ja pidurdusmaa"
	{desc}
	path="autod/{a.mk}/{a.slug}/"
	image="/og/auto/{a.mk}--{a.slug}.png"
	imageAlt="{a.nimi} — rehvimõõt ja pidurdusmaa"
	crumbs={[['Avaleht', '/'], ['Autod', '/autod/'], [a.make, '/autod/' + a.mk + '/'], [a.model + ' ' + a.yearLabel, path]]}
	jsonld={{
		'@context': 'https://schema.org',
		'@type': 'WebPage',
		name: a.nimi + ' rehvimõõt ja pidurdusmaa',
		description: desc,
		url: BASE + path,
		inLanguage: 'et'
		/* NB: mitte 'Car' / 'Vehicle' / 'Product' — Google peab neid tooteks ja
		   nõuab hinda või arvustusi; ilma nendeta on see Search Console'is viga */
	}}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href="/">Avaleht</a><span>/</span><a href="/autod/">Autod</a><span>/</span><a href="/autod/{a.mk}/">{a.make}</a><span
				>/</span
			>{a.model}
			{a.yearLabel}
		</div>
		<h1>{a.nimi} rehvid ja pidurdusmaa</h1>
		<p>
			Tehase põhimõõt on <b>{data.pohimoot}</b>.{#if marg90}{' '}Märjal asfaldil 90 km/h pealt peatub see auto keskmise (C-klassi) suverehviga umbes <b>{Math.round(marg90)} meetriga</b>{#if lumi50}, tallatud
					lumel 50 km/h pealt talverehviga umbes <b>{Math.round(lumi50)} meetriga</b>{/if}.{/if}
		</p>
		<p class="ad-cta">
			<a class="btn yel" href="/{autoQ}">Arvuta oma rehviga</a>
			<a class="btn" href="/rehvi-valimine/{autoQ}">Leia sobiv rehv</a>
		</p>
	</div>
</section>

<div class="body-sec">
	<div class="wrap">
		<div class="box">
			<h2>Tehase rehvimõõdud</h2>
			<p class="sub">Mõõdud, millega see põlvkond tehasest tuli. Täpne mõõt on rehvi küljel ja juhiukse piirdel.</p>
			<ul class="ad-moodud">
				{#each data.moodud as z (z.m)}
					<li class:pohi={z.pohi}>
						{#if z.slug}<a href="/rehvid/{z.slug}/">{z.label}</a>{:else}{z.label}{/if}
						{#if z.pohi}<span class="pill">põhimõõt</span>{/if}
					</li>
				{/each}
			</ul>
		</div>

		<div class="box">
			<h2>Pidurdusmaa</h2>
			<p class="sub">
				Peatumisteekond (reaktsioon 1 s + pidurdus) uute, keskmise märgiseklassiga (C) rehvidega, põhimõõdus {data.pohimoot}. Muuda tingimusi
				<a href="/{autoQ}">kalkulaatoris</a>.
			</p>
			<div class="tbl-wrap">
				<table class="t ad-kompakt">
					<thead><tr><th>Tingimused</th><th class="n">50 km/h</th><th class="n">90 km/h</th></tr></thead>
					<tbody>
						{#each data.pidurdus as x (x.id)}
							<tr>
								<td>{x.nimi}</td>
								<td class="n">{x.r[50]?.peatumine != null ? f1(x.r[50].peatumine) + ' m' : 'ei peatu'}</td>
								<td class="n">{x.r[90]?.peatumine != null ? f1(x.r[90].peatumine) + ' m' : 'ei peatu'}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
			<p class="note">{data.absTekst} Hinnang, mitte mõõtmine — päris pidurdusmaa sõltub konkreetsest rehvist, teest ja juhist.</p>
		</div>

		{#each [['suvi', data.suvi], ['talv', data.talv], ['aastaring', data.aastaring]] as [k, list] (k)}
			{#if list.length}
				<div class="box">
					<h2>{PEALKIRI[k]} mõõdus {data.pohimoot}</h2>
					<p class="sub">Sõltumatult testitud mudelid eespool, seejärel EL-i märgise märghaardumise klassi järgi.</p>
					<div class="tbl-wrap">
						<table class="t">
							<thead><tr><th>Rehv</th><th>Märghaardumine</th><th class="n">Müra</th></tr></thead>
							<tbody>
								{#each list as r (r.slug)}
									<tr>
										<td
											><a href="/rehvid/{r.slug}/">{r.nimi}</a>{#if r.testitud}
												<span class="pill test" style="margin-left:var(--sp-2)">testitud</span>{/if}</td
										>
										<td>{r.g || '–'}</td>
										<td class="n">{r.db ? r.db + ' dB' : '–'}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					{#if data.pohimootSlug}<p class="note"><a href="/rehvid/{data.pohimootSlug}/">Kõik rehvid mõõdus {data.pohimoot} →</a></p>{/if}
				</div>
			{/if}
		{/each}

		<div class="box">
			<h2>Mootorid</h2>
			<p class="sub">Tehase mootorid. Kui mootoril on oma rehvimõõt või mass, arvestab kalkulaator seda.</p>
			<div class="tbl-wrap">
				<table class="t">
					<thead><tr><th>Mootor</th><th>Kütus</th><th>Aastad</th><th>Rehvimõõt</th><th class="n">Tühimass</th></tr></thead>
					<tbody>
						{#each data.mootorid as m (m.key)}
							<tr>
								<td><a href="/?auto={encodeURIComponent(m.key)}">{m.silt || a.model}</a></td>
								<td>{m.kytus || '–'}</td>
								<td>{m.aastad || '–'}</td>
								<td>{m.moot || '–'}</td>
								<td class="n">{m.mass ? m.mass + ' kg' : '–'}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>

		{#if data.muudPolved.length}
			<div class="box">
				<h2>Teised põlvkonnad</h2>
				<ul class="ad-muud">
					{#each data.muudPolved as p (p.slug)}<li><a href="/autod/{a.mk}/{p.slug}/">{p.nimi}</a></li>{/each}
				</ul>
			</div>
		{/if}
		<p class="note">
			Andmed: tootjate andmed ja auto-data.net (mõõdud, mootorid, mass), EL-i tooteregister EPREL (rehvimärgis), sõltumatud rehvitestid.
			<a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.
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
