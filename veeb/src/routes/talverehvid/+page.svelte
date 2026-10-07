<script>
	/* /talverehvid/ — „Parimad talverehvid <mõõt>“ lehtede nimekiri (vt $lib/server/talv.js).
	   Esimene lõik vastab kohe küsimusele numbritega (AI ülevaated, ChatGPT), KKK = FAQPage. */
	import Meta from '$lib/Meta.svelte';
	import Autor from '$lib/Autor.svelte';
	import { BASE, graph, artikkel } from '$lib/skeem.js';
	import { KAT_NIMI, num } from '$lib/util.js';
	import { useT, useLang, autoNimi } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	let { data } = $props();
	const n = data.naide;
	const mm = (x) => (x == null ? '–' : num(x) + ' ' + t('m'));
	const ty = (k) => (n ? n.tyybid.find((x) => x.kat === k) : null);
	const jaa = (k) => mm(ty(k)?.jaa);
	const auto = n ? autoNimi(keel.lang, n.auto) : '';

	const pealkiri = t('Parimad talverehvid 2026/2027 mõõdu järgi');
	const desc = t('Talverehvid Eesti levinumates mõõtudes: testitud naast- ja lamellrehvid, pidurdusmaa lumel ja jääl ning Põhjamaade rehvid EL-i märgise järgi.');

	const vastus = n
		? t('Eesti talveks sobib naastrehv või Põhjamaade lamellrehv. 50 km/h pealt peatub {m} rehvidega auto jääl naastrehviga umbes {naast}, Põhjamaade lamellrehviga {lamell}, Kesk-Euroopa talverehviga {kesk} ja suverehviga {suvi}. Talverehvid on kohustuslikud 1. detsembrist 1. märtsini.', {
				m: n.moot,
				naast: jaa('WINTER_STUDDED'),
				lamell: jaa('WINTER_NORDIC'),
				kesk: jaa('WINTER_CENTRAL'),
				suvi: jaa('SUMMER_TOURING')
			})
		: '';

	const kkk = [
		[t('Millal tuleb talverehvid alla panna?'), t('Talverehvid on Eestis kohustuslikud 1. detsembrist 1. märtsini. Naastrehvid on lubatud 15. oktoobrist 31. märtsini, talviste olude korral 1. oktoobrist 30. aprillini. Vaheta varem, kui ööd on alla +7 °C või tuleb esimene lumi: suverehv kõvastub külmaga.')],
		[t('Kumb on parem, naastrehv või lamellrehv?'), n ? t('Jääl peatub naastrehv lühemalt: 50 km/h pealt umbes {naast} vs {lamell} lamellrehviga. Lumel ja kuival asfaldil on vahe väike. Kui sõidad palju maanteel või jäistel teedel, vali naast; linnas ja vaiksemaks sõiduks lamell.', { naast: jaa('WINTER_STUDDED'), lamell: jaa('WINTER_NORDIC') }) : ''],
		[t('Kas aastaringne või Kesk-Euroopa talverehv sobib Eesti talveks?'), n ? t('Jääl mitte hästi: Kesk-Euroopa talverehv peatub 50 km/h pealt umbes {kesk}, Põhjamaade lamellrehv {lamell}. Need rehvid on tehtud lörtsi ja märja tee jaoks. Eestis peab talverehvil olema kolme mäetipu ja lumehelbe märk.', { kesk: jaa('WINTER_CENTRAL'), lamell: jaa('WINTER_NORDIC') }) : ''],
		[t('Kui sügav peab olema talverehvi muster?'), t('Seaduse järgi üle 3 mm. Lumel on pidurdusteekond 4 mm mustriga umbes viiendiku ja 3 mm mustriga veerandi võrra pikem kui uuel rehvil, nii et 4 mm juures tasub vahetamisele mõelda.')]
	].filter((x) => x[1]);

	const top = n ? [...n.naastud, ...n.lamellid] : [];
	const jsonld = graph(
		...artikkel({ path: L('/talverehvid/'), title: pealkiri, desc, uuendatud: data.uuendatud, avaldatud: '2026-09-30', lang: keel.lang }),
		{ '@type': 'FAQPage', mainEntity: kkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) },
		...(top.length
			? [{
					'@type': 'ItemList',
					name: t('Jääl kõige paremini pidurdanud testitud talverehvid'),
					itemListElement: top.filter((x) => x.slug).map((x, i) => ({ '@type': 'ListItem', position: i + 1, name: x.nimi, url: BASE + L('/rehvid/' + x.slug + '/') }))
				}]
			: [])
	);
</script>

<Meta title={pealkiri} {desc} path="talverehvid/" crumbs={[[t('Avaleht'), '/'], [t('Talverehvid'), '/talverehvid/']]} {jsonld} />

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span>{t('Talverehvid')}</div>
		<h1>{t('Parimad talverehvid mõõdu järgi')}</h1>
		{#if vastus}<p>{vastus}</p>{/if}
		<p>{t('Vali oma rehvimõõt: näed testitud naast- ja lamellrehve, nende pidurdusmaad lumel ja jääl ning kõiki Põhjamaade talverehve selles mõõdus.')}</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<Autor uuendatud={data.uuendatud} />
		<div class="box">
			<h2>{t('Eesti levinumad mõõdud')}</h2>
			<p class="sub">{t('Järjestatud selle järgi, mitmel automudelil on see tehase põhimõõt.')}</p>
			<div class="sizes-list">
				{#each data.moodud as m (m.slug)}
					<a href={L('/talverehvid/' + m.slug + '/')}>{m.label} <span class="note">· {m.autosid} {t('autot')}</span></a>
				{/each}
			</div>
		</div>

		{#if n}
			<div class="box">
				<h2>{t('Rehvitüüp loeb kõige rohkem')}</h2>
				<p class="sub">{t('Pidurdusmaa 50 km/h pealt, −5 °C, uued rehvid, ilma reaktsiooniajata. Auto: {auto}.', { auto })}</p>
				<div class="tbl-wrap">
					<table class="t" style="min-width:0">
						<thead><tr><th>{t('Rehv')}</th><th class="n">{t('Lumi')}</th><th class="n">{t('Jää')}</th></tr></thead>
						<tbody>
							{#each ['WINTER_STUDDED', 'WINTER_NORDIC', 'WINTER_CENTRAL', 'ALL_SEASON', 'SUMMER_TOURING'] as k (k)}
								{@const r = ty(k)}
								{#if r}<tr><td>{t(KAT_NIMI[k])}</td><td class="n">{mm(r.lumi)}</td><td class="n">{mm(r.jaa)}</td></tr>{/if}
							{/each}
						</tbody>
					</table>
				</div>
			</div>

			{#if top.length}
				<div class="box">
					<h2>{t('Jääl kõige paremini pidurdanud testitud talverehvid')}</h2>
					<p class="sub">{t('Sõltumatute testide järgi, arvutatud mõõdus {m} ({auto}), 50 km/h pealt jääl. Teiste mõõtude järjestus on mõõdu lehel.', { m: n.moot, auto })}</p>
					<div class="tbl-wrap">
						<table class="t" style="min-width:0">
							<thead><tr><th>{t('Rehv')}</th><th>{t('Tüüp')}</th><th class="n">{t('Jää 50→0')}</th></tr></thead>
							<tbody>
								{#each [[n.naastud, 'WINTER_STUDDED'], [n.lamellid, 'WINTER_NORDIC']] as [list, k] (k)}
									{#each list as r (r.nimi)}
										<tr><td>{#if r.slug}<a href={L('/rehvid/' + r.slug + '/')}>{r.nimi}</a>{:else}{r.nimi}{/if}</td><td>{k === 'WINTER_STUDDED' ? t('Naastrehv') : t('Lamell')}</td><td class="n">{mm(r.jaa)}</td></tr>
									{/each}
								{/each}
							</tbody>
						</table>
					</div>
					<p class="note"><a href={L('/talverehvid/' + n.slug + '/')}>{t('Kõik talverehvid mõõdus {m} →', { m: n.moot })}</a></p>
				</div>
			{/if}
		{/if}

		<div class="box">
			<h2>{t('Korduma kippuvad küsimused')}</h2>
			{#each kkk as [q, a] (q)}<h3 style="font-size:17px;margin:var(--sp-4) 0 var(--sp-1)">{q}</h3><p style="margin:0">{a}</p>{/each}
		</div>
		<p class="note">
			{t('Mõõt on rehvi küljel (nt 205/55 R16) ja juhiukse piirdel.')}
			<a href={L('/teadmine/rehvivahetus/')}>{t('Rehvivahetus: kõik kuupäevad')}</a> ·
			<a href={L('/teadmine/artiklid/millal-talverehvid-alla/')}>{t('Millal talverehvid alla?')}</a>
		</p>
	</div>
</div>
