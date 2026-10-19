<script>
	/* /suverehvid/: märksõna „suverehvid“ jaoturleht (andmed: $lib/server/jaoturid.js).
	   Suvetestide võitjad märjal ja kuival asfaldil (iga testi enda mõõtmine, andmed.js
	   suveTestideParimad), märgise klassi ja mustri mõju pidurdusmaale (core.json demo) ning
	   lingid mõõdulehtedele. Aastaarvu pealkirjas ei ole: uus test tuleb tabelisse ise. */
	import Meta from '$lib/Meta.svelte';
	import Autor from '$lib/Autor.svelte';
	import AutoTee from '$lib/AutoTee.svelte';
	import { graph, artikkel } from '$lib/skeem.js';
	import { ARTIKLID, artikliTee } from '$lib/artiklid.js';
	import { num } from '$lib/util.js';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	let { data } = $props();
	const d = data.demo;
	const mm = (x) => (x == null ? '–' : num(x) + ' ' + t('m'));
	const ALAD = ['märg asfalt', 'kuiv asfalt'];
	/* uusimad kaks aastat tabelis, vanemad avatava loendi all */
	const uued = data.testid.filter((x) => x.aasta >= data.aasta1 - 1);
	const vanad = data.testid.filter((x) => x.aasta < data.aasta1 - 1);
	const vM = data.voidud.marg[0] || null;
	const vK = data.voidud.kuiv[0] || null;
	const lugeda = ['vanad-ja-kulunud-rehvid', 'vesiliug', 'rehvirohk-ja-pidurdus', 'millal-talverehvid-alla']
		.map((s) => ARTIKLID.find((a) => a.slug === s))
		.filter((a) => a && (keel.lang !== 'ru' || a.ru));

	const pealkiri = t('Suverehvid: parimad suverehvid testide ja märgise järgi');
	const desc = t('Parimad suverehvid testide järgi: iga testi võitja märjal ja kuival asfaldil, märgise klassi mõju pidurdusmaale ja millal suverehvid alla panna.');

	const vastus = d
		? t('Suverehvi juures loeb kõige rohkem pidurdus märjal teel. EL-i rehvimärgise A-klassi suverehviga peatub auto märjal asfaldil 90 km/h pealt umbes {a}, E-klassiga {e}: vahe on {v}.', { a: mm(d.classA), e: mm(d.classE), v: mm(d.classE - d.classA) })
		: '';
	const voitja = vM
		? t('Meie andmebaasi {n} suverehvitestist aastatel {y0} kuni {y1} oli märjal asfaldil kõige sagedamini parim {r}: {k} korda.', { n: data.testid.length, y0: data.aasta0, y1: data.aasta1, r: vM.nimi, k: vM.n })
		: '';

	const kkk = [
		[t('Millal suverehvid alla panna?'), d ? t('Kui päevad püsivad üle +7 °C ja öökülmad on läbi. Naastrehvid tuleb ära vahetada hiljemalt 31. märtsiks, talviste olude korral 30. aprilliks. Lamellrehviga võib sõita kauem, aga soojal asfaldil pidurdab talverehv halvemini: kuival asfaldil +25 °C juures peatub auto 90 km/h pealt suverehviga {s} ja Põhjamaade talverehviga {w}.', { s: mm(d.summerWarm), w: mm(d.winterWarm) }) : ''],
		[t('Kui palju loeb suverehvi märgise klass?'), d ? t('Märjal teel palju: 90 km/h pealt peatub A-klassi suverehviga auto umbes {a}, B-klassiga {b} ja E-klassiga {e}. Klass kehtib ühe mõõdu kohta: sama mudel võib teises mõõdus olla teise klassiga, seepärast vaata klassi oma mõõdu lehelt.', { a: mm(d.classA), b: mm(d.tread8), e: mm(d.classE) }) : ''],
		[t('Kui sügav peab olema suverehvi muster?'), d ? t('Seaduse järgi vähemalt 1,6 mm. Pidurdusmaa pikeneb aga juba varem: märjal asfaldil 90 km/h pealt peatub auto uue rehviga umbes {k8}, 3 mm mustriga {k3}. Mida rohkem vett teel, seda suurem vahe.', { k8: mm(d.tread8), k3: mm(d.tread3) }) : ''],
		[t('Milline suverehv on testides parim?'), vM && vK
			? vM.slug === vK.slug
				? t('Meie andmebaasi {n} suverehvitestist aastatel {y0} kuni {y1} oli nii märjal kui ka kuival asfaldil kõige sagedamini parim {r}: märjal {km} ja kuival {kk} korda. Iga testi võitja on tabelis.', { n: data.testid.length, y0: data.aasta0, y1: data.aasta1, r: vM.nimi, km: vM.n, kk: vK.n })
				: t('Meie andmebaasi {n} suverehvitestist aastatel {y0} kuni {y1} oli märjal asfaldil kõige sagedamini parim {r} ({km} korda) ja kuival asfaldil {r2} ({kk} korda). Iga testi võitja on tabelis.', { n: data.testid.length, y0: data.aasta0, y1: data.aasta1, r: vM.nimi, km: vM.n, r2: vK.nimi, kk: vK.n })
			: '']
	].filter((x) => x[1]);

	const jsonld = graph(
		...artikkel({ path: L('/suverehvid/'), title: pealkiri, desc, uuendatud: data.uuendatud, avaldatud: '2026-10-19', lang: keel.lang }),
		{ '@type': 'FAQPage', mainEntity: kkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) }
	);
</script>

{#snippet lahter(o)}
	{#if o}
		{#each o.rehvid as r, i (r.slug)}{i ? ' / ' : ''}{#if r.ix}<a href={L('/rehvid/' + r.slug + '/')}>{r.nimi}</a>{:else}{r.nimi}{/if}{/each}<br /><b>{mm(o.m)}</b>
		{#if o.v0}<small class="kiirus">{o.v0}→{o.v1 || 0} {t('km/h')}</small>{/if}
	{:else}–{/if}
{/snippet}

{#snippet tabel(rows)}
	<div class="tbl-wrap">
		<!-- testi nimi oma real, võitjad kahes veerus: telefonis mahub ära ilma külgkerimiseta -->
		<table class="t" style="min-width:0">
			<thead><tr><th>{t('Märg asfalt')}</th><th>{t('Kuiv asfalt')}</th></tr></thead>
			<tbody>
				{#each rows as x (x.id)}
					<tr class="tt">
						<td colspan="2"><strong>{x.pub} {x.aasta}</strong> <small class="mo">{[x.moot, x.auto, x.n ? t('{n} rehvi', { n: x.n }) : ''].filter(Boolean).join(' · ')}</small></td>
					</tr>
					<tr>
						{#each ALAD as a (a)}<td>{@render lahter(x.alad[a])}</td>{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/snippet}

<Meta title={pealkiri} {desc} path="suverehvid/" crumbs={[[t('Avaleht'), '/'], [t('Rehvid'), '/rehvid/'], [t('Suverehvid'), '/suverehvid/']]} {jsonld} />

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/rehvid/')}>{t('Rehvid')}</a><span>/</span>{t('Suverehvid')}</div>
		<h1>{t('Parimad suverehvid testide järgi')}</h1>
		{#if vastus}<p>{vastus} {voitja}</p>{/if}
		<p style="margin-top:var(--sp-3)">{t('Allpool on iga testi võitja, märgise klassi ja mustri mõju pidurdusmaale ning suverehvid mõõdu järgi: {n} suverehvi mudelit EL-i rehvimärgisega.', { n: num(data.suvemudeleid, 0) })}</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<Autor uuendatud={data.uuendatud} />
		{#if data.testid.length}
			<div class="box">
				<h2>{t('Suverehvitestide võitjad')}</h2>
				<p class="sub">{t('Iga testi parim rehv märjal ja kuival asfaldil: testi enda mõõdetud pidurdusmaa. Eri testide meetreid otse võrrelda ei saa, sest autod ja kiirused on erinevad.')}</p>
				{@render tabel(uued)}
				{#if vanad.length}
					<details class="vanad">
						<summary>{t('Varasemad testid ({n})', { n: vanad.length })}</summary>
						{@render tabel(vanad)}
					</details>
				{/if}
				<p class="note"><a href={L('/testid/')}>{t('Kõik rehvitestid →')}</a></p>
			</div>
		{/if}

		{#if d}
			<div class="box">
				<h2>{t('Mis muudab suverehvi pidurdusmaad')}</h2>
				<p class="sub">{t('Pidurdusmaa märjal asfaldil 90 km/h pealt, ilma reaktsiooniajata. Auto VW Golf 8, mõõt 205/55 R16. Pidurdusmaa.ee arvutus.')}</p>
				<div class="tbl-wrap">
					<table class="t" style="min-width:0">
						<thead><tr><th>{t('Suverehv')}</th><th class="n">{t('Pidurdusmaa')}</th></tr></thead>
						<tbody>
							<tr><td>{t('Märgise klass A')}</td><td class="n"><b>{mm(d.classA)}</b></td></tr>
							<tr><td>{t('Märgise klass B, uus rehv')}</td><td class="n">{mm(d.tread8)}</td></tr>
							<tr><td>{t('Märgise klass B, muster 3 mm')}</td><td class="n">{mm(d.tread3)}</td></tr>
							<tr><td>{t('Märgise klass E')}</td><td class="n">{mm(d.classE)}</td></tr>
						</tbody>
					</table>
				</div>
				<p class="note">
					{t('Kuival asfaldil +25 °C juures peatub sama auto 90 km/h pealt suverehviga {s} ja Põhjamaade talverehviga {w}.', { s: mm(d.summerWarm), w: mm(d.winterWarm) })}
					<a href={L('/teadmine/rehvimargis/')}>{t('EL-i rehvimärgis')} →</a>
				</p>
			</div>
		{/if}

		<div class="box">
			<h2>{t('Suverehvid mõõdu järgi')}</h2>
			<p class="sub">{t('Mõõdu lehel on kõik selle mõõdu rehvid EL-i märgise klasside järgi ja testide tulemused. Mõõt on rehvi küljel (nt 205/55 R16) ja juhiukse piirdel.')}</p>
			<div class="sizes-list">
				{#each data.moodud as m (m.slug)}
					<a href={L('/rehvid/' + m.slug + '/')}>{m.label} <span class="note">· {m.autosid} {t('autot')}</span></a>
				{/each}
			</div>
			<p class="note"><a href={L('/rehvid/')}>{t('Kõik mõõdud →')}</a> · <a href={L('/rehvi-valimine/')}>{t('Vali rehv oma autole →')}</a></p>
		</div>

		<div class="box">
			<h2>{t('Korduma kippuvad küsimused')}</h2>
			{#each kkk as [q, a] (q)}<h3 style="font-size:17px;margin:var(--sp-4) 0 var(--sp-1)">{q}</h3><p style="margin:0">{a}</p>{/each}
		</div>
		<p class="note">
			{t('Loe ka:')}
			{#each lugeda as a, i (a.slug)}{i ? ' · ' : ''}<a href={L(artikliTee(a))}>{keel.lang === 'ru' ? a.ru.title : a.title}</a>{/each}
		</p>
		<p class="note">
			<a href={L('/talverehvid/')}>{t('Talverehvid')}</a> ·
			<a href={L('/naastrehvid/')}>{t('Naastrehvid')}</a> ·
			<a href={L('/lamellrehvid/')}>{t('Lamellrehvid')}</a> ·
			<a href={L('/rehvid/')}>{t('Autorehvid')}</a> ·
			<a href={L('/autod/')}>{t('Rehvid autole')}</a>
		</p>
	</div>
</div>
<AutoTee koht="suverehvid/" />

<style>
	.kiirus { white-space: nowrap; margin-left: 4px; color: var(--muted); }
	.mo { color: var(--muted); }
	tr.tt td { border-bottom: 0; padding-bottom: 0; padding-top: var(--sp-4); }
	tr:not(.tt) td { width: 50%; }
	.vanad { margin-top: var(--sp-4); }
	.vanad summary { cursor: pointer; font-weight: 600; margin-bottom: var(--sp-3); }
</style>
