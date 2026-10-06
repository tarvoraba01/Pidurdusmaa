<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';
	let { data } = $props();

	const KIRJ = t('Rehvimõõdu kalkulaator: võrdle kahte rehvimõõtu. Näed läbimõõtu, külje kõrgust, spidomeetri viga ja sama läbimõõduga mõõte, mis sinu autole sobivad.');
	const KKK = [
		[t('Kui palju võib uus rehvimõõt erineda?'), t('Uue mõõdu läbimõõt võiks erineda tehase mõõdust kuni 1,5%, ja kindlasti mitte üle 3%. Suurema vahe korral näitab spidomeeter valesti ning ABS ja ESP võivad töötada halvemini. Lubatud mõõdud on auto registreerimistunnistusel või tootja andmetes.')],
		[t('Kuidas rehvi läbimõõtu arvutada?'), t('Külje kõrgus on laius korda profiil: 205/55 rehvil 205 × 0,55 = 112,75 mm. Läbimõõt on velje läbimõõt millimeetrites pluss kaks külge: 16 × 25,4 + 2 × 112,75 = 632 mm.')],
		[t('Kas suurem rehv muudab spidomeetri näitu?'), t('Jah. Kui uus rehv on 2% suurema läbimõõduga, sõidad spidomeetri 90 km/h juures tegelikult umbes 91,8 km/h. Väiksema rehviga sõidad aeglasemalt, kui spidomeeter näitab.')]
	];
	const faq = { '@type': 'FAQPage', mainEntity: KKK.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) };
	const jsonld = graph(tooriist(t('Rehvimõõdu kalkulaator'), '/rehvi-kalkulaator/', KIRJ, keel.lang), ORG, faq);
</script>

<Meta title={t('Rehvimõõdu kalkulaator — läbimõõt, külje kõrgus ja spidomeeter')} desc={KIRJ} path="rehvi-kalkulaator/" crumbs={[[t('Avaleht'), '/'], [t('Rehvimõõdu kalkulaator'), '/rehvi-kalkulaator/']]} {jsonld} image="/og/sait/rehvi-kalkulaator.png" />

<LiiklusLeht kick={t('Rehvid · mõõt')} h1={t('Rehvimõõdu kalkulaator')} lead={t('Vali praegune ja uus rehvimõõt. Näed, kui palju muutuvad läbimõõt ja külje kõrgus ning mida näitab spidomeeter.')} vaade="moot" andmed={data.moodud}>
	{#each KKK as [q, a] (q)}
		<div>
			<h2>{q}</h2>
			<p>{a}</p>
		</div>
	{/each}
</LiiklusLeht>
