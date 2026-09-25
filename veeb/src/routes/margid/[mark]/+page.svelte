<script>
	import Meta from '$lib/Meta.svelte';
	import { KAT_NIMI } from '$lib/util.js';
	import { BASE } from '$lib/skeem.js';
	let { data } = $props();
	const m = $derived(data.mark);
	const path = $derived('/margid/' + m.slug + '/');
	const desc = $derived(
		`${m.nimi} rehvid: ${data.mudeleid} mudelit EL-i rehvimärgise andmetega` +
			(data.testitud.length ? `, neist ${data.testitud.length} sõltumatult testitud` : '') +
			'. Vaata märghaardumise klasse ja pidurdusmaad oma autoga.'
	);
</script>

<Meta
	title="{m.nimi} rehvid — mudelid, märgised ja testid"
	{desc}
	path="margid/{m.slug}/"
	noindex={data.noindex}
	crumbs={[['Avaleht', '/'], ['Rehvid', '/rehvid/'], ['Margid', '/margid/'], [m.nimi, path]]}
	jsonld={{
		'@context': 'https://schema.org',
		'@type': 'CollectionPage',
		name: m.nimi + ' rehvid',
		description: desc,
		url: BASE + path,
		inLanguage: 'et',
		about: { '@type': 'Brand', name: m.nimi }
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
		<p>
			{data.mudeleid} mudelit ja {data.mootudKokku} mõõtu EL-i rehvimärgise andmebaasis{#if data.testitud.length},
				{data.testitud.length} mudelit sõltumatutes testides{/if}.
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
		<p class="srcline">
			Märghaardumise klass on mõõdupõhine: vahemik „A–C“ tähendab, et mudeli eri mõõdud on eri klassis.
			<a href="/teadmine/rehvimargis/">Mida klassid tähendavad?</a>
		</p>
	</div>
</div>
