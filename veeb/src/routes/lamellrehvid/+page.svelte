<script>
	/* /lamellrehvid/: märksõna „lamellrehvid“ jaoturleht (andmed: $lib/server/jaoturid.js).
	   Põhjamaade naastudeta talverehvid: testide parimad mõõdus 205/55 R16, mõõdud ja kõik
	   lamellrehvid margi kaupa (testitud ja jäämärgiga märgitud). KKK = FAQPage. */
	import Meta from '$lib/Meta.svelte';
	import Autor from '$lib/Autor.svelte';
	import AutoTee from '$lib/AutoTee.svelte';
	import { BASE, graph, artikkel } from '$lib/skeem.js';
	import { ARTIKLID, artikliTee } from '$lib/artiklid.js';
	import { num } from '$lib/util.js';
	import { useT, useLang, autoNimi } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	let { data } = $props();
	const n = data.naide;
	const mm = (x) => (x == null ? '–' : num(x) + ' ' + t('m'));
	const jaa = (k) => mm(n?.tyybid.find((x) => x.kat === k)?.jaa);
	const auto = n ? autoNimi(keel.lang, n.auto) : '';
	const top = n ? n.top : [];
	const lyhi = (mark, nimi) => (nimi.toLowerCase().startsWith(mark.toLowerCase() + ' ') ? nimi.slice(mark.length + 1) : nimi);
	/* jäämärk (EL-i märgise jäähaarde piktogramm, sama mis $lib/margid.js jaa()) üks kord lehel,
	   iga mudeli juures ainult viide: 74 ikooni ei korda sama SVG-d */
	const jaaSilt = t('Jäämärk (EL-i rehvimärgise jäähaarde sümbol)');
	const lugeda = ['naastrehv-voi-lamell', 'pohjamaade-voi-kesk-euroopa-talverehv', 'talverehvi-margistus-3pmsf', 'talverehvide-testid-2026', 'talverehvi-valimine']
		.map((s) => ARTIKLID.find((a) => a.slug === s))
		.filter((a) => a && (keel.lang !== 'ru' || a.ru));

	const pealkiri = t('Lamellrehvid 2026/27: parimad lamellrehvid testide järgi');
	const desc = t('Parimad Põhjamaade lamellrehvid testide järgi: pidurdusmaa jääl ja märjal asfaldil, kõik {n} lamellrehvi margi kaupa ja millist märki Eestis vaja on.', { n: data.kokku });

	const vastus = n
		? t('Lamellrehv on naastudeta talverehv. Eesti talveks sobib Põhjamaade lamellrehv: 50 km/h pealt peatub auto jääl sellega umbes {lamell}, naastrehviga {naast} ja Kesk-Euroopa talverehviga {kesk}. Lumel on vahe naastrehviga väike. Lamellrehvil kuupäevapiirangut ei ole, aga 1. detsembrist 1. märtsini peab sellel olema kolme mäetipu ja lumehelbe märk (3PMSF).', {
				lamell: jaa('WINTER_NORDIC'),
				naast: jaa('WINTER_STUDDED'),
				kesk: jaa('WINTER_CENTRAL')
			})
		: '';

	const kkk = [
		[t('Mis on lamellrehv?'), t('Lamellrehv on naastudeta talverehv, mille mustris on palju peeneid lõikeid ehk lamelle. Põhjamaade lamellrehv on tehtud lume ja jää jaoks. Kesk-Euroopa talverehv on mõeldud märjale ja lörtsisele teele ning pidurdab jääl palju halvemini.')],
		[t('Milline märk peab lamellrehvil olema?'), t('Talverehvide kohustuslikul ajal, 1. detsembrist 1. märtsini, peab naastudeta talverehvil olema kolme mäetipu ja lumehelbe märk (3PMSF). Transpordiamet soovitab valida rehvi, millel on ka EL-i märgise jäämärk: selline rehv on läbinud jääkatse. Siin on {j} lamellrehvi {n}-st jäämärgiga.', { j: data.jaamargiga, n: data.kokku })],
		[t('Kumb on parem, naastrehv või lamellrehv?'), n ? t('Jääl peatub naastrehv lühemalt: 50 km/h pealt umbes {naast}, lamellrehviga {lamell}. Lumel ja kuival asfaldil on vahe väike. Kui sõidad palju maanteel või jäistel teedel, vali naast; linnas ja vaiksemaks sõiduks lamell.', { naast: jaa('WINTER_STUDDED'), lamell: jaa('WINTER_NORDIC') }) : ''],
		[t('Kas lamellrehviga tohib suvel sõita?'), data.soe ? t('Tohib, naastudeta talverehvil kuupäevapiirangut ei ole. Soojal asfaldil pidurdab talverehv aga halvemini: kuival asfaldil +25 °C juures peatub auto 90 km/h pealt suverehviga {s} ja Põhjamaade talverehviga {w}.', { s: mm(data.soe.suvi), w: mm(data.soe.talv) }) : ''],
		[t('Milline lamellrehv on testides parim?'), top.length >= 3 ? t('Testitud lamellrehvidest pidurdas jääl kõige lühemalt {a} ({am}), järgmised olid {b} ({bm}) ja {c} ({cm}). See on arvutus mõõdus {m} 50 km/h pealt jääl. Märjal asfaldil on järjestus teine: vaata tabelit.', {
				a: top[0].nimi, am: mm(top[0].jaa), b: top[1].nimi, bm: mm(top[1].jaa), c: top[2].nimi, cm: mm(top[2].jaa), m: n.moot
			}) : '']
	].filter((x) => x[1]);

	const jsonld = graph(
		...artikkel({ path: L('/lamellrehvid/'), title: pealkiri, desc, uuendatud: data.uuendatud, avaldatud: '2026-10-19', lang: keel.lang }),
		{ '@type': 'FAQPage', mainEntity: kkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) },
		...(top.length
			? [{
					'@type': 'ItemList',
					name: t('Testide parimad lamellrehvid jääl'),
					itemListElement: top.filter((x) => x.slug).map((x, i) => ({ '@type': 'ListItem', position: i + 1, name: x.nimi, url: BASE + L('/rehvid/' + x.slug + '/') }))
				}]
			: [])
	);
</script>

<Meta title={pealkiri} {desc} path="lamellrehvid/" crumbs={[[t('Avaleht'), '/'], [t('Talverehvid'), '/talverehvid/'], [t('Lamellrehvid'), '/lamellrehvid/']]} {jsonld} />

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/talverehvid/')}>{t('Talverehvid')}</a><span>/</span>{t('Lamellrehvid')}</div>
		<h1>{t('Parimad lamellrehvid 2026/2027')}</h1>
		{#if vastus}<p>{vastus}</p>{/if}
		<p style="margin-top:var(--sp-3)">{t('Allpool on testide parimad lamellrehvid, lamellrehvid sinu rehvimõõdus ja kõik {n} Põhjamaade lamellrehvi margi kaupa.', { n: data.kokku })}</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<Autor uuendatud={data.uuendatud} />
		{#if top.length}
			<div class="box">
				<h2>{t('Testide parimad lamellrehvid jääl')}</h2>
				<p class="sub">{t('Sõltumatute testide mõõdetud haarde järgi, arvutatud mõõdus {m} autole {auto}: pidurdusmaa 50 km/h pealt jääl ja 90 km/h pealt märjal asfaldil, ilma reaktsiooniajata. Rehvi nime all on testi enda mõõtmine testi autol ja mõõdus.', { m: n.moot, auto })}</p>
				<div class="tbl-wrap">
					<table class="t" style="min-width:0">
						<thead>
							<tr><th>{t('Rehv')}</th><th class="n">{t('Jää 50→0')}</th><th class="n">{t('Märg 90→0')}</th></tr>
						</thead>
						<tbody>
							{#each top as r, i (r.nimi + i)}
								<tr class:jt={r.jaaTest}>
									<td>{#if r.slug}<a href={L('/rehvid/' + r.slug + '/')}>{r.nimi}</a>{:else}{r.nimi}{/if}</td>
									<td class="n"><b>{mm(r.jaa)}</b></td>
									<td class="n">{mm(r.marg)}</td>
								</tr>
								{#if r.jaaTest}
									<tr class="mo-r"><td colspan="3"><small class="mo">{r.jaaTest.lyhi}: {num(r.jaaTest.m)} {t('m')} ({r.jaaTest.v0}→{r.jaaTest.v1} {t('km/h')}{r.jaaTest.moot && r.jaaTest.moot !== n.moot ? ', ' + r.jaaTest.moot : ''})</small></td></tr>
								{/if}
							{/each}
						</tbody>
					</table>
				</div>
				<p class="note"><a href={L('/talverehvid/' + n.slug + '/')}>{t('Kõik talverehvid mõõdus {m} →', { m: n.moot })}</a></p>
			</div>
		{/if}

		<div class="box">
			<h2>{t('Lamellrehvid mõõdu järgi')}</h2>
			<p class="sub">{t('Igal mõõdul on oma järjestus, sest kõiki rehve ei tehta igas mõõdus. Mõõt on rehvi küljel (nt 205/55 R16) ja juhiukse piirdel.')}</p>
			<div class="sizes-list">
				{#each data.moodud as m (m.slug)}
					<a href={L('/talverehvid/' + m.slug + '/')}>{m.label} <span class="note">· {m.autosid} {t('autot')}</span></a>
				{/each}
			</div>
			<p class="note"><a href={L('/talverehvid/')}>{t('Kõik mõõdud →')}</a></p>
		</div>

		<div class="box">
			<h2>{t('Kõik lamellrehvid margi kaupa')}</h2>
			<p class="sub">
				{t('{n} Põhjamaade lamellrehvi {k} margilt, neist {j} jäämärgiga.', { n: data.kokku, k: data.margid.length, j: data.jaamargiga })}
				<span class="ok">✓</span> {t('sõltumatult testitud')} · <svg class="ik" viewBox="0 0 30 26" aria-hidden="true"><use href="#jaa-ikoon" /></svg> {t('jäämärk')}
			</p>
			<svg width="0" height="0" style="position:absolute" aria-hidden="true">
				<defs>
					<clipPath id="jaa-loige"><path d="M2 24.5 15 2.5l13 22z" /></clipPath>
					<symbol id="jaa-ikoon" viewBox="0 0 30 26">
						<g fill="none" stroke="currentColor" stroke-linejoin="round"><path d="M2 24.5 15 2.5l13 22z" stroke-width="1.6" /><g clip-path="url(#jaa-loige)" stroke-width="1"><path d="M0 22 8 14M0 28l14-14M6 28l14-14M12 28l14-14M18 28l12-12M24 28l6-6" /></g></g>
					</symbol>
				</defs>
			</svg>
			<ul class="mk">
				{#each data.margid as m (m.mark)}
					<li>
						<b>{m.mark}</b>
						{#each m.rehvid as r, i (r.slug)}{i ? ' · ' : ''}<a href={L('/rehvid/' + r.slug + '/')}>{lyhi(m.mark, r.nimi)}</a>{#if r.testitud}<span class="ok" title={t('testitud')}>✓</span>{/if}{#if r.jaamark}<svg class="ik" viewBox="0 0 30 26" role="img" aria-label={jaaSilt}><use href="#jaa-ikoon" /></svg>{/if}{/each}
					</li>
				{/each}
			</ul>
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
			<a href={L('/naastrehvid/')}>{t('Naastrehvid')}</a> ·
			<a href={L('/talverehvid/')}>{t('Talverehvid')}</a> ·
			<a href={L('/suverehvid/')}>{t('Suverehvid')}</a> ·
			<a href={L('/rehvid/')}>{t('Autorehvid')}</a> ·
			<a href={L('/autod/')}>{t('Rehvid autole')}</a>
		</p>
	</div>
</div>
<AutoTee koht="lamellrehvid/" />

<style>
	.mk { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--sp-2); line-height: 1.6; }
	.mk b { margin-right: var(--sp-2); }
	.mo { color: var(--muted); font-size: 12.5px; }
	/* testi enda mõõtmine rehvi rea all, kogu tabeli laiuses (telefonis ei suru nime kitsaks) */
	tr.jt td { border-bottom: 0; padding-bottom: 0; }
	tr.mo-r td { padding-top: 2px; }
	.ok { margin-left: 3px; color: var(--tested); font-weight: 700; font-size: 13px; }
	.ik { width: 19px; height: 17px; vertical-align: -3px; margin-left: 3px; color: var(--muted); }
</style>
