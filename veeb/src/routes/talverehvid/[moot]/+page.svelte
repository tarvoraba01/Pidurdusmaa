<script>
	import { jaa } from '$lib/margid.js';
	/* „Parimad talverehvid <mõõt>“ — andmed $lib/server/talv.js. Tekstid eesti keeles,
	   vene tõlge $lib/i18n/ru.js (/ru/talverehvid/<mõõt>/). */
	import Meta from '$lib/Meta.svelte';
	import Autor from '$lib/Autor.svelte';
	import { BASE, graph, artikkel } from '$lib/skeem.js';
	import { KAT_NIMI, num } from '$lib/util.js';
	import { useT, useLang, autoNimi } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	const an = (s) => autoNimi(keel.lang, s);
	let { data } = $props();
	const m = $derived(data.moot);
	const path = $derived('/talverehvid/' + m.slug + '/');
	const mm = (x) => (x == null ? '–' : num(x) + ' ' + t('m'));
	const q = $derived('?moot=' + m.m + '&hooaeg=winter');
	/* hooaeg pealkirjas (otsingud „talverehvid 2026“): mai–dets → see/järgmine aasta, jaan–apr → eelmine/see */
	const HOOAEG = (() => { const d = new Date(), y = d.getFullYear(); return d.getMonth() >= 4 ? y + '/' + String(y + 1).slice(2) : y - 1 + '/' + String(y).slice(2); })();
	const pealkiri = $derived(t('Talverehvid {m} {h} — parimad testides', { m: m.label, h: HOOAEG }));
	const desc = $derived(
		t('Talverehvid {m}: testitud naast- ja lamellrehvide pidurdusmaa lumel ja jääl ning {n} Põhjamaade talverehvi EL-i märgise järgi.', { m: m.label, n: data.pohjaKokku }) +
			(data.auto ? ' ' + t('Sobib nt autole {auto}.', { auto: an(data.auto.nimi) }) : '')
	);
	const tyybiRida = (x) => data.tyybid.find((y) => y.kat === x);
	/* esimene lause = vastus numbritega (AI ülevaated / ChatGPT tsiteerivad seda) */
	const parimN = $derived(data.naastud.find((x) => x.jaa != null));
	const parimL = $derived(data.lamellid.find((x) => x.jaa != null));
	const vastus = $derived(
		parimN && parimL && data.auto
			? t('Mõõdus {m} pidurdas jääl kõige paremini naastrehv {n} ({nm}) ja lamellrehvidest {l} ({lm}), arvutatud 50 km/h pealt autoga {auto}.', {
					m: m.label, n: parimN.nimi, nm: mm(parimN.jaa), l: parimL.nimi, lm: mm(parimL.jaa), auto: an(data.auto.nimi)
				})
			: ''
	);
	const kkk = $derived(
		[
			parimN && parimL ? [t('Milline on parim talverehv mõõdus {m}?', { m: m.label }), vastus + ' ' + t('Jääl pidurdab naastrehv tavaliselt lühemalt, lumel on vahe väike.')] : null,
			tyybiRida('WINTER_STUDDED') && tyybiRida('WINTER_NORDIC')
				? [t('Naast või lamell mõõdus {m}?', { m: m.label }), t('Tüüpilise naastrehviga peatub auto jääl 50 km/h pealt umbes {n}, Põhjamaade lamellrehviga {l}. Lumel {nl} vs {ll}.', { n: mm(tyybiRida('WINTER_STUDDED').jaa), l: mm(tyybiRida('WINTER_NORDIC').jaa), nl: mm(tyybiRida('WINTER_STUDDED').lumi), ll: mm(tyybiRida('WINTER_NORDIC').lumi) })]
				: null,
			[t('Mitu Põhjamaade talverehvi on mõõdus {m}?', { m: m.label }), t('EL-i rehviregistris on mõõdus {m} {n} Põhjamaade talverehvi, neist {j} jäämärgiga.', { m: m.label, n: data.pohjaKokku, j: data.pohjaJaa })]
		].filter(Boolean)
	);
	const ldTop = $derived([...data.naastud, ...data.lamellid].filter((x) => x.slug && x.jaa != null).sort((a, b) => a.jaa - b.jaa).slice(0, 10));
	/* kui testitud rehvide lumi on arvutuses kõigil sama (lumetesti pole), jäetakse veerg ära */
	const lumiErineb = (list) => new Set(list.map((r) => r.lumi)).size > 1;
</script>

<Meta
	title={pealkiri}
	{desc}
	path="talverehvid/{m.slug}/"
	crumbs={[[t('Avaleht'), '/'], [t('Talverehvid'), '/talverehvid/'], [m.label, path]]}
	jsonld={graph(
		...artikkel({ path: L(path), title: pealkiri, desc, uuendatud: data.uuendatud, avaldatud: data.lisa ? '2026-10-18' : '2026-09-30', lang: keel.lang }),
		{ '@type': 'FAQPage', mainEntity: kkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) },
		...(ldTop.length ? [{ '@type': 'ItemList', name: t('Parimad talverehvid {m}', { m: m.label }), itemListElement: ldTop.map((x, i) => ({ '@type': 'ListItem', position: i + 1, name: x.nimi, url: BASE + L('/rehvid/' + x.slug + '/') })) }] : [])
	)}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/talverehvid/')}>{t('Talverehvid')}</a><span>/</span>{m.label}
		</div>
		<p class="eyebrow" style="color:var(--muted-d)">{t('Talverehvid 2026/2027')}</p>
		<h1>{t('Parimad talverehvid {m}', { m: m.label })}</h1>
		{#if vastus}<p>{vastus}</p>{/if}
		<p>
			{t(data.lisa ? '{m} on tehasemõõt {n} automudelil.' : '{m} on tehase põhimõõt {n} automudelil.', { m: m.label, n: data.autosid })}
			{#if data.test}{t(data.test.ala === 'jää' ? 'Selles mõõdus tehtud testis {test} pidurdas jääl kõige lühemalt {r}: {mm} m.' : 'Selles mõõdus tehtud testis {test} pidurdas märjal asfaldil kõige lühemalt {r}: {mm} m.', { test: data.test.pub + ' ' + data.test.aasta + (data.test.v0 > 0 ? ' (' + Math.round(data.test.v0) + '→' + Math.round(data.test.v1 || 0) + ' ' + t('km/h') + ')' : ''), r: data.test.rehvid.map((x) => x.nimi).join(' / '), mm: num(data.test.m) })}{/if}
			{t('Siin on selle mõõdu talverehvid päris andmete järgi: testitud rehvide pidurdusmaa lumel ja jääl ning EL-i rehvimärgis.')}
		</p>
		<p class="ad-cta">
			<a class="btn yel" href={L('/rehvi-valimine/') + q}>{t('Vali talverehv oma autole')}</a>
			<a class="btn" href={L('/') + '?moot=' + m.m}>{t('Arvuta pidurdusmaa')}</a>
		</p>
	</div>
</section>

<div class="body-sec">
	<div class="wrap">
		<Autor uuendatud={data.uuendatud} />
		{#if data.tyybid.length}
			<div class="box">
				<h2>{t('Rehvitüüp loeb kõige rohkem')}</h2>
				<p class="sub">
					{t('Pidurdusmaa 50 km/h pealt, −5 °C, uued rehvid, ilma reaktsiooniajata. Auto: {auto}.', { auto: an(data.auto.nimi) })}
				</p>
				<div class="tbl-wrap">
					<table class="t" style="min-width:0">
						<thead><tr><th>{t('Rehv')}</th><th class="n">{t('Lumi')}</th><th class="n">{t('Jää')}</th></tr></thead>
						<tbody>
							{#each ['WINTER_STUDDED', 'WINTER_NORDIC', 'WINTER_CENTRAL', 'ALL_SEASON', 'SUMMER_TOURING'] as k (k)}
								{@const r = tyybiRida(k)}
								{#if r}
									<tr><td>{t(KAT_NIMI[k])}</td><td class="n">{mm(r.lumi)}</td><td class="n">{mm(r.jaa)}</td></tr>
								{/if}
							{/each}
						</tbody>
					</table>
				</div>
				<p class="note">
					{t('Jääl on vahe kõige suurem: Kesk-Euroopa talverehv ja aastaringne rehv pidurdavad jääl palju pikemalt kui Põhjamaade rehv. Eesti talveks vali naast- või Põhjamaade lamellrehv.')}
				</p>
			</div>
		{/if}

		{#each [['lamellid', data.lamellid], ['naastud', data.naastud]] as [k, list] (k)}
			<div class="box">
				<h2>{k === 'lamellid' ? t('Testitud lamellrehvid selles mõõdus') : t('Testitud naastrehvid')}</h2>
				<p class="sub">
					{k === 'lamellid'
						? t('Põhjamaade lamellrehvid, mis on sõltumatult testitud ja on EL-i registri järgi ka mõõdus {m} olemas. Järjestus jää pidurdusmaa järgi.', { m: m.label })
						: t('Naastrehvidel EL-i rehvimärgist ei ole. Ees on mudelid, mis on testitud või poodides müügil mõõdus {m}, edasi teistes mõõtudes testitud: nende saadavust kontrolli poest. Järjestus jää pidurdusmaa järgi.', { m: m.label })}
				</p>
				{#if list.length}
					<div class="tbl-wrap">
						<table class="t">
							<thead>
								<tr><th>{t('Rehv')}</th><th class="n">{t('Jää 50→0')}</th>{#if lumiErineb(list)}<th class="n">{t('Lumi 50→0')}</th>{/if}<th class="n">{t('Märg 90→0')}</th><th>{t('Mõõdetud jääl')}</th></tr>
							</thead>
							<tbody>
								{#each list as r, i (r.nimi + i)}
									<tr>
										<td>{#if r.slug}<a href={L('/rehvid/' + r.slug + '/')}>{r.nimi}</a>{:else}{r.nimi}{/if}</td>
										<td class="n"><b>{mm(r.jaa)}</b></td>
										{#if lumiErineb(list)}<td class="n">{mm(r.lumi)}</td>{/if}
										<td class="n">{mm(r.marg)}</td>
										<td class="note">{#if r.jaaTest}{r.jaaTest.lyhi}: {num(r.jaaTest.m)} {t('m')} ({r.jaaTest.v0}→{r.jaaTest.v1} {t('km/h')}, {r.jaaTest.moot}){:else}–{/if}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					<p class="note">
						{t('Pidurdusmaa on arvutatud selle mõõdu tüüpilise autoga ({auto}) testitud rehvi mõõdetud haarde järgi. Viimane veerg on testi enda mõõtmine testi autol ja mõõdus.', { auto: data.auto ? an(data.auto.nimi) : '–' })}
					</p>
				{:else}
					<p class="note">{t('Selles mõõdus ei ole praegu ühtegi sõltumatult testitud lamellrehvi. Vaata allpool rehve EL-i märgise järgi.')}</p>
				{/if}
			</div>
		{/each}

		<div class="box">
			<h2>{t('Põhjamaade talverehvid EL-i märgise järgi')}</h2>
			<p class="sub">
				{t('{n} mudelit, neist {j} jäämärgiga. Järjestus: jäämärk, testitud, siis märghaardumise klass ja müra.', { n: data.pohjaKokku, j: data.pohjaJaa })}
			</p>
			<div class="tbl-wrap">
				<table class="t">
					<thead><tr><th>{t('Rehv')}</th><th>{t('Jäämärk')}</th><th>{t('Märghaare')}</th><th class="n">{t('Müra')}</th></tr></thead>
					<tbody>
						{#each data.pohja as r (r.slug)}
							<tr>
								<td><a href={L('/rehvid/' + r.slug + '/')}>{r.nimi}</a>{#if r.testitud} <span class="pill test" style="margin-left:var(--sp-2)">{t('testitud')}</span>{/if}</td>
								<td>{#if r.jaa}{@html jaa(t('Jäämärk (EL-i rehvimärgise jäähaarde sümbol)'))}{:else}–{/if}</td>
								<td>{r.g || '–'}</td>
								<td class="n">{r.db ? r.db + ' ' + t('dB') : '–'}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
			<p class="note">
				{t('Jäämärk tähendab, et rehv läbis jääkatse — Transpordiamet soovitab Eestis valida jäämärgiga talverehvi.')}
				{#if m.sizeSlug}<a href={L('/rehvid/' + m.sizeSlug + '/')}>{t('Kõik rehvid mõõdus {m} →', { m: m.label })}</a>{/if}
			</p>
			{#if data.kesk}
				<p class="note">
					{t('Selles mõõdus on ka {n} Kesk-Euroopa talverehvi. Need on tehtud märja ja lörtsise talve jaoks ning pidurdavad jääl palju pikemalt — Eesti talveks neid ei soovita.', { n: data.kesk })}
				</p>
			{/if}
		</div>

		{#if data.autod.length}
			<div class="box">
				<h2>{t(data.lisa ? 'Autod, millel {m} on tehasemõõt' : 'Autod, mille tehase põhimõõt on {m}', { m: m.label })}</h2>
				<ul class="ad-muud">
					{#each data.autod as c (c.url)}<li><a href={L(c.url)}>{an(c.nimi)}</a></li>{/each}
				</ul>
				{#if data.autosid > data.autod.length}<p class="note">{t('…ja veel {n}.', { n: data.autosid - data.autod.length })}</p>{/if}
				{#if data.kaas.length}
					<p class="note">
						{t('Samadel autodel on tehasemõõduna ka')}
						{#each data.kaas as x, i (x.slug)}{i ? (i === data.kaas.length - 1 ? ' ' + t('ja') + ' ' : ', ') : ''}<a href={L('/talverehvid/' + x.slug + '/')}>{x.label}</a> ({x.n} {t('autot')}){/each}.
					</p>
				{/if}
			</div>
		{/if}

		{#if kkk.length}
			<div class="box">
				<h2>{t('Korduma kippuvad küsimused')}</h2>
				{#each kkk as [q, a] (q)}<h3 style="font-size:17px;margin:var(--sp-4) 0 var(--sp-1)">{q}</h3><p style="margin:0">{a}</p>{/each}
			</div>
		{/if}

		<div class="box">
			<h2>{t('Teised mõõdud')}</h2>
			<div class="sizes-list">
				{#each data.teised as x (x.slug)}<a href={L('/talverehvid/' + x.slug + '/')}>{x.label}</a>{/each}
			</div>
		</div>
		<p class="note">
			{t('Andmed: sõltumatud rehvitestid (Tekniikan Maailma, ADAC, Vi Bilägare jt), EL-i tooteregister EPREL, tootjate andmed. Pidurdusmaad on arvutatud hinnangud, mitte mõõtmised.')}
			<a href={L('/teadmine/rehvivahetus/')}>{t('Rehvivahetus {a}: millal talverehvid alla', { a: new Date().getFullYear() })}</a>
		</p>
	</div>
</div>

<style>
	.ad-cta {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-3);
		margin-top: var(--sp-4);
	}
	.ad-muud {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-2);
	}
	.ad-muud li a {
		display: inline-block;
		padding: 4px 12px;
		border: 1px solid var(--line);
		border-radius: 999px;
		background: #fff;
	}
</style>
