<script>
	import Meta from '$lib/Meta.svelte';
	import { KAT_NIMI } from '$lib/util.js';
	import { BASE } from '$lib/skeem.js';
	import { MARGI_INFO } from '$lib/margiInfo.js';
	let { data } = $props();
	const m = $derived(data.mark);
	const info = $derived(MARGI_INFO[m.slug] || '');
	const path = $derived('/margid/' + m.slug + '/');
	/* KKK: vastused ainult lehe andmetest (märgise jaotus, testitud mudelid, kategooriad, mõõdud) */
	const ja = (a) => (a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' ja ' + a[a.length - 1]);
	const kat = (...k) => data.kategooriad.filter((x) => k.includes(x.kat)).flatMap((x) => x.list);
	const kkk = $derived.by(() => {
		const out = [];
		const n = m.nimi;
		if (data.jaotus.length || data.testitud.length) {
			out.push([
				`Kas ${n} rehvid on head?`,
				(data.jaotus.length ? `EL-i rehvimärgise järgi on ${n} rehvide märghaardumise klassid kõigis mõõtudes: ${data.jaotus.map(([g, p]) => g + ' ' + p + '%').join(', ')}. ` : '') +
					(data.testitud.length
						? `Sõltumatutes testides on olnud ${data.testitud.length === 1 ? '1 mudel' : data.testitud.length + ' mudelit'}, näiteks ${ja(data.testitud.slice(0, 3).map((x) => x.name))}. `
						: `Ükski ${n} mudel ei ole meie andmetes olnud sõltumatus pidurdustestis, seega põhineb hinnang ainult märgisel. `) +
					'Sama mudel võib eri mõõdus olla eri klassiga, nii et vaata oma mõõdu andmeid mudeli lehelt.'
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
				`Millised ${n} talverehvid sobivad Eesti talveks?`,
				`Eesti talveks sobivad naast- ja Põhjamaade lamellrehvid. ` +
					(talv.length === 1 ? `${n} valikus on selline ${talv[0]}.` : `${n} valikus on neid vähemalt ${talv.length}, näiteks ${ja(talv.slice(0, 4))}.`) +
					(kat('WINTER_CENTRAL').length ? ` Kesk-Euroopa talverehvid (${kat('WINTER_CENTRAL').length} mudelit) on mõeldud märjale ja lörtsisele talvele ning pidurdavad jääl pikemalt.` : '')
			]);
		}
		if (data.topMoodud.length) {
			out.push([`Millistes mõõtudes on ${n} rehve kõige rohkem?`, `Kõige rohkem ${n} mudeleid on mõõtudes ${ja(data.topMoodud.map((z) => z.label + ' (' + z.k + ')'))}. Kokku on ${n} rehve EL-i registris ${data.mootudKokku} mõõdus.`]);
		}
		return out;
	});
	const desc = $derived(
		(info ? `${m.nimi} on ${info} ` : '') +
		`${m.nimi} rehvid: ${data.mudeleid} mudelit EL-i rehvimärgise andmetega` +
			(data.testitud.length ? `, neist ${data.testitud.length} sõltumatult testitud` : '') +
			'. Vaata märghaardumise klasse ja pidurdusmaad oma autoga.'
	);
</script>

<Meta
	title="{m.nimi} rehvid — {data.mudeleid} mudelit, testid ja märgised"
	{desc}
	path="margid/{m.slug}/"
	noindex={data.noindex}
	crumbs={[['Avaleht', '/'], ['Rehvid', '/rehvid/'], ['Margid', '/margid/'], [m.nimi, path]]}
	jsonld={{
		'@context': 'https://schema.org',
		'@graph': [
			{
				'@type': 'CollectionPage',
				name: m.nimi + ' rehvid',
				description: desc,
				url: BASE + path,
				inLanguage: 'et',
				about: { '@type': 'Brand', name: m.nimi }
			},
			...(kkk.length ? [{ '@type': 'FAQPage', mainEntity: kkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) }] : [])
		]
	}}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href="/">Avaleht</a><span>/</span><a href="/rehvid/">Rehvid</a><span>/</span><a href="/margid/"
				>Margid</a
			><span>/</span>{m.nimi}
		</div>
		<h1>{m.nimi} rehvid</h1>
		{#if info}<p>{m.nimi} on {info}</p>{/if}
		<p>
			{data.mudeleid} mudelit ja {data.mootudKokku} mõõtu EL-i rehvimärgise andmebaasis{#if data.testitud.length},
				{data.testitud.length} mudelit sõltumatutes testides{/if}.
			{#if data.jaotus.length}Märghaardumise klassid kõigis mõõtudes: {data.jaotus.map(([g, p]) => g + ' ' + p + '%').join(', ')}.{/if}
			{#if data.topMoodud.length}Kõige rohkem mudeleid mõõtudes
				{#each data.topMoodud as z, i (z.label)}{#if z.slug}<a href="/rehvid/{z.slug}/">{z.label}</a>{:else}{z.label}{/if} ({z.k}){i < data.topMoodud.length - 1 ? ', ' : '.'}{/each}{/if}
		</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		{#if data.testitud.length}
			<div class="box">
				<h2>Sõltumatult testitud</h2>
				<p class="sub">Nende rehvide pidurdusmaa on päriselt mõõdetud — täpsem kui märgise klass.</p>
				<div class="grid-cards">
					{#each data.testitud as t, ti (t.slug + '#' + ti)}
						<a class="tcard" href="/rehvid/{t.slug}/">
							<span class="b">{KAT_NIMI[t.category] ?? ''}</span>
							<h3>{t.name}</h3>
							<span class="meta">{t.srcs}</span>
						</a>
					{/each}
				</div>
			</div>
		{/if}
		{#each data.kategooriad as k (k.kat)}
			<div class="box">
				<h2>{k.nimi} <span class="note">· {k.list.length}</span></h2>
				<div class="tbl-wrap">
					<table class="t">
						<thead><tr><th>Mudel</th><th class="n">Mõõte</th><th>Märghaardumine</th></tr></thead>
						<tbody>
							{#each k.list as r (r.slug)}
								<tr>
									<td
										><a href="/rehvid/{r.slug}/">{r.nimi}</a>{#if r.testitud}
											<span class="pill test" style="margin-left:var(--sp-2)">testitud</span>{/if}</td
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
				<h2>Korduma kippuvad küsimused</h2>
				{#each kkk as [q, a] (q)}<h3 style="font-size:17px;margin:var(--sp-4) 0 var(--sp-1)">{q}</h3><p style="margin:0">{a}</p>{/each}
			</div>
		{/if}
		<p class="srcline">
			Märghaardumise klass on mõõdupõhine: vahemik „A–C“ tähendab, et mudeli eri mõõdud on eri klassis.
			<a href="/teadmine/rehvimargis/">Mida klassid tähendavad?</a>
		</p>
	</div>
</div>
