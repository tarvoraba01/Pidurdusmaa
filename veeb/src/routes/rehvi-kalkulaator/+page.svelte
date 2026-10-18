<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import RehviMoot from '$lib/RehviMoot.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';
	let { data } = $props();

	const KIRJ = t('Rehvimõõdu kalkulaator: võrdle kahte rehvimõõtu. Näed läbimõõtu, külje kõrgust, spidomeetri viga ja sama läbimõõduga mõõte, mis sinu autole sobivad.');
	const KKK = [
		[t('Kui palju võib uus rehvimõõt erineda?'), t('Uue mõõdu läbimõõt võiks erineda tehase mõõdust kuni 1,5%, ja kindlasti mitte üle 3%. Suurema vahe korral näitab spidomeeter valesti ning ABS ja ESP võivad töötada halvemini. Lubatud mõõdud on auto registreerimistunnistusel või tootja andmetes.')],
		[t('Kuidas rehvi läbimõõtu arvutada?'), t('Külje kõrgus on laius korda profiil: 205/55 rehvil 205 × 0,55 = 112,75 mm. Läbimõõt on velje läbimõõt millimeetrites pluss kaks külge: 16 × 25,4 + 2 × 112,75 = 632 mm.')],
		[t('Kas suurem rehv muudab spidomeetri näitu?'), t('Jah. Kui uus rehv on 2% suurema läbimõõduga, sõidad spidomeetri 90 km/h juures tegelikult umbes 91,8 km/h. Väiksema rehviga sõidad aeglasemalt, kui spidomeeter näitab.')]
	];
	const protsent = (p) => (p > 0 ? '+' : p < 0 ? '−' : '') + String(Math.abs(p).toFixed(1)).replace('.', keel.lang === 'en' ? '.' : ',') + ' %';
	const faq = { '@type': 'FAQPage', mainEntity: KKK.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) };
	const jsonld = graph(tooriist(t('Rehvimõõdu kalkulaator'), '/rehvi-kalkulaator/', KIRJ, keel.lang), ORG, faq);
</script>

<Meta title={t('Rehvi kalkulaator — rehvimõõt, läbimõõt, külje kõrgus ja spidomeeter')} desc={KIRJ} path="rehvi-kalkulaator/" crumbs={[[t('Avaleht'), '/'], [t('Rehvimõõdu kalkulaator'), '/rehvi-kalkulaator/']]} {jsonld} image="/og/sait/rehvi-kalkulaator.png" />

<LiiklusLeht Tool={RehviMoot} kick={t('Rehvid · mõõt')} h1={t('Rehvimõõdu kalkulaator')} lead={t('Uue rehvimõõdu läbimõõt võiks erineda tehase mõõdust kuni 1,5%, mitte üle 3%. Vali praegune ja uus mõõt: näed läbimõõtu, külje kõrgust ja mida näitab spidomeeter.')} vaade="moot" andmed={data.moodud}>
	{#each KKK as [q, a] (q)}
		<div>
			<h2>{q}</h2>
			<p>{a}</p>
		</div>
	{/each}
	{#if data.kaas?.length}
		<!-- päris asendusmõõdud: samade automudelite tehasemõõdud (staatiline, näha ka ilma JavaScriptita) -->
		<div style="grid-column:1/-1">
			<h2>{t('Levinumad tehasemõõdud ja asendusmõõdud')}</h2>
			<p>{t('Mõõdud, mis on samadel automudelitel ka tehasemõõt. Sulgudes on läbimõõdu vahe; kõige sagedasem ees.')}</p>
			<div class="tbl-wrap">
				<table class="t" style="min-width:0">
					<thead><tr><th>{t('Mõõt')}</th><th class="n">{t('Läbimõõt')}</th><th class="n">{t('Põhimõõt autodel')}</th><th>{t('Samadel autodel ka')}</th></tr></thead>
					<tbody>
						{#each data.kaas as r (r.m)}
							<tr>
								<td>{#if r.slug}<a href={keel.L('/rehvid/' + r.slug + '/')}>{r.label}</a>{:else}{r.label}{/if}</td>
								<td class="n">{r.d} mm</td>
								<td class="n">{r.n}</td>
								<td>{#each r.alt as z, i (z.m)}{#if i}, {/if}{#if z.slug}<a href={keel.L('/rehvid/' + z.slug + '/')}>{z.label}</a>{:else}{z.label}{/if} ({protsent(z.pct)}){/each}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	{/if}
</LiiklusLeht>
