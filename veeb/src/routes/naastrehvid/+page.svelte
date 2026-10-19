<script>
	/* /naastrehvid/: märksõna „naastrehvid“ jaoturleht (andmed: $lib/server/jaoturid.js).
	   Lühike päring on poodide päralt; see leht annab sellele vastuseks testide numbrid ja lingid
	   kõigile naastrehvide ja mõõtude lehtedele. Esimene lõik vastab kohe numbritega, KKK = FAQPage. */
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
	/* margi sees mudeli nimi ilma margita („Bridgestone Blizzak Spike 3“ → „Blizzak Spike 3“) */
	const lyhi = (mark, nimi) => (nimi.toLowerCase().startsWith(mark.toLowerCase() + ' ') ? nimi.slice(mark.length + 1) : nimi);
	const lugeda = ['naastrehv-voi-lamell', 'naastrehvid-liiga-vara-voi-hilja', 'talverehvide-testid-2026', 'talverehvide-nouded', 'talverehvid-valismaal']
		.map((s) => ARTIKLID.find((a) => a.slug === s))
		.filter((a) => a && (keel.lang !== 'ru' || a.ru));

	const pealkiri = t('Naastrehvid 2026/27: parimad naastrehvid testide järgi');
	const desc = t('Parimad naastrehvid testide järgi: pidurdusmaa jääl ja märjal asfaldil, kõik {n} naastrehvi margi kaupa ja naastude lubatud ajad Eestis.', { n: data.kokku });

	const vastus = n
		? t('Naastrehv pidurdab jääl kõige paremini: 50 km/h pealt peatub auto jääl naastrehviga umbes {naast}, Põhjamaade lamellrehviga {lamell} ja suverehviga {suvi}. Lumel ja asfaldil on naast- ja lamellrehvi vahe väike. Naastrehvid on Eestis lubatud 15. oktoobrist 31. märtsini, talviste olude korral 1. oktoobrist 30. aprillini.', {
				naast: jaa('WINTER_STUDDED'),
				lamell: jaa('WINTER_NORDIC'),
				suvi: jaa('SUMMER_TOURING')
			})
		: '';

	const kkk = [
		[t('Millal tohib naastrehvidega sõita?'), t('Naastrehvid on lubatud 15. oktoobrist 31. märtsini. Kui teel on talvised olud, võib nendega sõita ka 1. oktoobrist 30. aprillini: seda otsustab juht ise ilma järgi. Alates 1. maist on naastrehvid keelatud igal juhul.')],
		[t('Kas naastrehvid peavad olema kõigil ratastel?'), t('Jah. Kui kasutad naastrehve, peavad need olema kõigil neljal rattal. Naastrehvid ees ja lamellid taga, või vastupidi, ei ole lubatud.')],
		[t('Kumb on parem, naastrehv või lamellrehv?'), n ? t('Jääl peatub naastrehv lühemalt: 50 km/h pealt umbes {naast}, lamellrehviga {lamell}. Lumel ja kuival asfaldil on vahe väike. Kui sõidad palju maanteel või jäistel teedel, vali naast; linnas ja vaiksemaks sõiduks lamell.', { naast: jaa('WINTER_STUDDED'), lamell: jaa('WINTER_NORDIC') }) : ''],
		[t('Milline naastrehv on testides parim?'), top.length >= 3 ? t('Testitud naastrehvidest pidurdas jääl kõige lühemalt {a} ({am}), järgmised olid {b} ({bm}) ja {c} ({cm}). See on arvutus mõõdus {m} 50 km/h pealt jääl. Märjal asfaldil on järjestus teine: vaata tabelit.', {
				a: top[0].nimi, am: mm(top[0].jaa), b: top[1].nimi, bm: mm(top[1].jaa), c: top[2].nimi, cm: mm(top[2].jaa), m: n.moot
			}) : '']
	].filter((x) => x[1]);

	const jsonld = graph(
		...artikkel({ path: L('/naastrehvid/'), title: pealkiri, desc, uuendatud: data.uuendatud, avaldatud: '2026-10-19', lang: keel.lang }),
		{ '@type': 'FAQPage', mainEntity: kkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) },
		...(top.length
			? [{
					'@type': 'ItemList',
					name: t('Testide parimad naastrehvid jääl'),
					itemListElement: top.filter((x) => x.slug).map((x, i) => ({ '@type': 'ListItem', position: i + 1, name: x.nimi, url: BASE + L('/rehvid/' + x.slug + '/') }))
				}]
			: [])
	);
</script>

<Meta title={pealkiri} {desc} path="naastrehvid/" crumbs={[[t('Avaleht'), '/'], [t('Talverehvid'), '/talverehvid/'], [t('Naastrehvid'), '/naastrehvid/']]} {jsonld} />

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/talverehvid/')}>{t('Talverehvid')}</a><span>/</span>{t('Naastrehvid')}</div>
		<h1>{t('Parimad naastrehvid 2026/2027')}</h1>
		{#if vastus}<p>{vastus}</p>{/if}
		<p style="margin-top:var(--sp-3)">{t('Allpool on testide parimad naastrehvid, naastrehvid sinu rehvimõõdus ja kõik {n} naastrehvi margi kaupa.', { n: data.kokku })}</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<Autor uuendatud={data.uuendatud} />
		{#if top.length}
			<div class="box">
				<h2>{t('Testide parimad naastrehvid jääl')}</h2>
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
			<h2>{t('Naastrehvid mõõdu järgi')}</h2>
			<p class="sub">{t('Igal mõõdul on oma järjestus, sest kõiki rehve ei tehta igas mõõdus. Mõõt on rehvi küljel (nt 205/55 R16) ja juhiukse piirdel.')}</p>
			<div class="sizes-list">
				{#each data.moodud as m (m.slug)}
					<a href={L('/talverehvid/' + m.slug + '/')}>{m.label} <span class="note">· {m.autosid} {t('autot')}</span></a>
				{/each}
			</div>
			<p class="note"><a href={L('/talverehvid/')}>{t('Kõik mõõdud →')}</a></p>
		</div>

		<div class="box">
			<h2>{t('Kõik naastrehvid margi kaupa')}</h2>
			<p class="sub">{t('{n} naastrehvi {k} margilt. ✓ tähendab, et rehvi on sõltumatult testitud. Teiste pidurdusmaa on hinnang testitud naastrehvide põhjal.', { n: data.kokku, k: data.margid.length })}</p>
			<ul class="mk">
				{#each data.margid as m (m.mark)}
					<li>
						<b>{m.mark}</b>
						{#each m.rehvid as r, i (r.slug)}{i ? ' · ' : ''}<a href={L('/rehvid/' + r.slug + '/')}>{lyhi(m.mark, r.nimi)}</a>{#if !r.hinnang}<span class="ok" title={t('testitud')}>✓</span>{/if}{/each}
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
			<a href={L('/lamellrehvid/')}>{t('Lamellrehvid')}</a> ·
			<a href={L('/talverehvid/')}>{t('Talverehvid')}</a> ·
			<a href={L('/suverehvid/')}>{t('Suverehvid')}</a> ·
			<a href={L('/rehvid/')}>{t('Autorehvid')}</a> ·
			<a href={L('/autod/')}>{t('Rehvid autole')}</a>
		</p>
	</div>
</div>
<AutoTee koht="naastrehvid/" />

<style>
	.mk { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--sp-2); line-height: 1.6; }
	.mk b { margin-right: var(--sp-2); }
	.mo { color: var(--muted); font-size: 12.5px; }
	/* testi enda mõõtmine rehvi rea all, kogu tabeli laiuses (telefonis ei suru nime kitsaks) */
	tr.jt td { border-bottom: 0; padding-bottom: 0; }
	tr.mo-r td { padding-top: 2px; }
	.ok { margin-left: 3px; color: var(--tested); font-weight: 700; font-size: 13px; }
</style>
