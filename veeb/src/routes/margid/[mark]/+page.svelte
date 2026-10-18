<script>
	import Meta from '$lib/Meta.svelte';
	import { KAT_NIMI } from '$lib/util.js';
	import { BASE } from '$lib/skeem.js';
	import { MARGI_INFO, MARGI_INFO_RU } from '$lib/margiInfo.js';
	import { useT, useLang } from '$lib/i18n.js';
	let { data } = $props();
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	const ru = keel.lang === 'ru';
	const m = $derived(data.mark);
	const info = $derived((ru ? MARGI_INFO_RU : MARGI_INFO)[m.slug] || '');
	const path = $derived('/margid/' + m.slug + '/');
	/* KKK: vastused ainult lehe andmetest (märgise jaotus, testitud mudelid, kategooriad, mõõdud) */
	const ja = (a) => (a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' ' + t('ja') + ' ' + a[a.length - 1]);
	const kat = (...k) => data.kategooriad.filter((x) => k.includes(x.kat)).flatMap((x) => x.list);
	const jaotusTxt = $derived(data.jaotus.map(([g, p]) => g + ' ' + p + '%').join(', '));
	const kkk = $derived.by(() => {
		const out = [];
		const n = m.nimi;
		if (data.jaotus.length || data.testitud.length) {
			out.push([
				t('Kas {n} rehvid on head?', { n }),
				(data.jaotus.length ? t('EL-i rehvimärgise järgi on {n} rehvide märghaardumise klassid kõigis mõõtudes: {j}.', { n, j: jaotusTxt }) + ' ' : '') +
					(data.testitud.length
						? (data.testitud.length === 1
								? t('Sõltumatutes testides on olnud 1 mudel: {x}.', { x: data.testitud[0].name })
								: t('Sõltumatutes testides on olnud {k} mudelit, näiteks {x}.', { k: data.testitud.length, x: ja(data.testitud.slice(0, 3).map((x) => x.name)) })) + ' '
						: t('Ükski {n} mudel ei ole meie andmetes olnud sõltumatus pidurdustestis, seega põhineb hinnang ainult märgisel.', { n }) + ' ') +
					(data.kohad.length
						? t('Uusimad kohad testides: {list}.', {
								list: data.kohad
									.map((k) => k.name + ' (' + k.test + '): ' + t('{ala} {pos}./{n}', { ala: t(k.parim.ala), pos: k.parim.pos, n: k.parim.n }) + (k.kehvim ? ', ' + t('{ala} {pos}./{n}', { ala: t(k.kehvim.ala), pos: k.kehvim.pos, n: k.kehvim.n }) : ''))
									.join('; ')
							}) + ' '
						: '') +
					t('Sama mudel võib eri mõõdus olla eri klassiga, nii et vaata oma mõõdu andmeid mudeli lehelt.')
			]);
		}
		/* naastrehvidel EL-i märgist ei ole — need tulevad testitud rehvide hulgast */
		const nimi = (x) => (x.toLowerCase().startsWith(n.toLowerCase()) ? x : n + ' ' + x);
		const talv = [...new Set([
			...data.testitud.filter((x) => /^WINTER_(STUDDED|NORDIC)$/i.test(x.category)).map((x) => x.name),
			...kat('WINTER_STUDDED', 'WINTER_NORDIC').map((x) => nimi(x.nimi))
		])];
		if (talv.length) {
			out.push([
				t('Millised {n} talverehvid sobivad Eesti talveks?', { n }),
				t('Eesti talveks sobivad naast- ja Põhjamaade lamellrehvid.') + ' ' +
					(talv.length === 1 ? t('{n} valikus on selline {x}.', { n, x: talv[0] }) : t('{n} valikus on neid vähemalt {k}, näiteks {x}.', { n, k: talv.length, x: ja(talv.slice(0, 4)) })) +
					(kat('WINTER_CENTRAL').length ? ' ' + t('Kesk-Euroopa talverehvid ({k} mudelit) on mõeldud märjale ja lörtsisele talvele ning pidurdavad jääl pikemalt.', { k: kat('WINTER_CENTRAL').length }) : '')
			]);
		}
		if (data.topMoodud.length) {
			out.push([
				t('Millistes mõõtudes on {n} rehve kõige rohkem?', { n }),
				t('Kõige rohkem {n} mudeleid on mõõtudes {x}. Kokku on {n} rehve EL-i registris {k} mõõdus.', { n, x: ja(data.topMoodud.map((z) => z.label + ' (' + z.k + ')')), k: data.mootudKokku })
			]);
		}
		return out;
	});
	const desc = $derived(
		(info ? (ru ? `${m.nimi} — ${info} ` : `${m.nimi} on ${info} `) : '') +
			(data.testitud.length
				? t('{n} rehvid: {k} mudelit EL-i rehvimärgise andmetega, neist {x} sõltumatult testitud.', { n: m.nimi, k: data.mudeleid, x: data.testitud.length })
				: t('{n} rehvid: {k} mudelit EL-i rehvimärgise andmetega.', { n: m.nimi, k: data.mudeleid })) +
			' ' + t('Vaata märghaardumise klasse ja pidurdusmaad oma autoga.')
	);
</script>

<Meta
	title={t('{n} rehvid — {k} mudelit, testid ja märgised', { n: m.nimi, k: data.mudeleid })}
	{desc}
	path="margid/{m.slug}/"
	noindex={data.noindex}
	crumbs={[[t('Avaleht'), '/'], [t('Rehvid'), '/rehvid/'], [t('Margid'), '/margid/'], [m.nimi, path]]}
	jsonld={{
		'@context': 'https://schema.org',
		'@graph': [
			{
				'@type': 'CollectionPage',
				name: t('{n} rehvid', { n: m.nimi }),
				description: desc,
				url: BASE + L(path),
				inLanguage: keel.lang,
				about: { '@type': 'Brand', name: m.nimi }
			},
			...(kkk.length ? [{ '@type': 'FAQPage', mainEntity: kkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) }] : [])
		]
	}}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/rehvid/')}>{t('Rehvid')}</a><span>/</span><a href={L('/margid/')}
				>{t('Margid')}</a
			><span>/</span>{m.nimi}
		</div>
		<h1>{t('{n} rehvid', { n: m.nimi })}</h1>
		{#if info}<p>{ru ? `${m.nimi} — ${info}` : `${m.nimi} on ${info}`}</p>{/if}
		<p>
			{data.testitud.length ? t('{k} mudelit ja {z} mõõtu EL-i rehvimärgise andmebaasis, {x} mudelit sõltumatutes testides.', { k: data.mudeleid, z: data.mootudKokku, x: data.testitud.length }) : t('{k} mudelit ja {z} mõõtu EL-i rehvimärgise andmebaasis.', { k: data.mudeleid, z: data.mootudKokku })}
			{#if data.jaotus.length}{t('Märghaardumise klassid kõigis mõõtudes: {j}.', { j: jaotusTxt })}{/if}
			{#if data.topMoodud.length}{t('Kõige rohkem mudeleid mõõtudes')}
				{#each data.topMoodud as z, i (z.label)}{#if z.slug}<a href={L('/rehvid/' + z.slug + '/')}>{z.label}</a>{:else}{z.label}{/if} ({z.k}){i < data.topMoodud.length - 1 ? ', ' : '.'}{/each}{/if}
		</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		{#if data.testitud.length}
			<div class="box">
				<h2>{t('Sõltumatult testitud rehvid')}</h2>
				<p class="sub">{t('Nende rehvide pidurdusmaa on päriselt mõõdetud — täpsem kui märgise klass.')}</p>
				<div class="grid-cards">
					{#each data.testitud as tt, ti (tt.slug + '#' + ti)}
						<a class="tcard" href={L('/rehvid/' + tt.slug + '/')}>
							<span class="b">{t(KAT_NIMI[tt.category] ?? '')}</span>
							<h3>{tt.name}</h3>
							<span class="meta">{tt.srcs.map((x) => t(x)).join(', ')}</span>
						</a>
					{/each}
				</div>
			</div>
		{/if}
		{#if data.hinnang.length}
			<div class="box">
				<h2>{t('Naastrehvid, mida pole testitud')} <span class="note">· {data.hinnang.length}</span></h2>
				<p class="sub">{t('Pidurdusmaa on hinnang sarnaste testitud naastrehvide põhjal.')}</p>
				<ul class="mk-hin">
					{#each data.hinnang as h (h.slug)}<li><a href={L('/rehvid/' + h.slug + '/')}>{h.name}</a>{#if h.n} <span class="note">· {t('{k} mõõtu poodides', { k: h.n })}</span>{/if}</li>{/each}
				</ul>
			</div>
		{/if}
		{#each data.kategooriad as k (k.kat)}
			<div class="box">
				<h2>{t(k.nimi)} <span class="note">· {k.list.length}</span></h2>
				<div class="tbl-wrap">
					<table class="t">
						<thead><tr><th>{t('Mudel')}</th><th class="n">{t('Mõõte')}</th><th>{t('Märghaardumine')}</th></tr></thead>
						<tbody>
							{#each k.list as r (r.slug)}
								<tr>
									<td
										>{#if r.index}<a href={L('/rehvid/' + r.slug + '/')}>{r.nimi}</a>{:else}{r.nimi}{/if}{#if r.testitud}
											<span class="pill test" style="margin-left:var(--sp-2)">{t('testitud')}</span>{/if}</td
									>
									<td class="n">{r.n}</td>
									<td>{r.g || '–'}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/each}
		{#if kkk.length}
			<div class="box">
				<h2>{t('Korduma kippuvad küsimused')}</h2>
				{#each kkk as [q, a] (q)}<h3 style="font-size:17px;margin:var(--sp-4) 0 var(--sp-1)">{q}</h3><p style="margin:0">{a}</p>{/each}
			</div>
		{/if}
		<p class="srcline">
			{t('Märghaardumise klass on mõõdupõhine: vahemik „A–C“ tähendab, et mudeli eri mõõdud on eri klassis.')}
			<a href={L('/teadmine/rehvimargis/')}>{t('Mida klassid tähendavad?')}</a>
		</p>
	</div>
</div>
