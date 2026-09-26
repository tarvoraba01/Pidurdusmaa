<script>
	import Meta from '$lib/Meta.svelte';
	import Autor from '$lib/Autor.svelte';
	import { num } from '$lib/util.js';
	import { AUTOR_NIMI, ETTEVOTE } from '$lib/seaded.js';
	import { BASE, ORG_ID, ORG, AUTOR, graph } from '$lib/skeem.js';
	let { data } = $props();
	const UUENDATUD = '2026-09-25';
	const TEGIJA = AUTOR_NIMI ? `${AUTOR_NIMI} (${ETTEVOTE})` : ETTEVOTE;
	const jsonld = graph(
		{
			'@type': 'AboutPage',
			'@id': BASE + '/meist/#leht',
			url: BASE + '/meist/',
			name: 'Meist',
			inLanguage: 'et',
			dateModified: UUENDATUD,
			about: { '@id': ORG_ID },
			...(AUTOR ? { mainEntity: { '@id': AUTOR['@id'] } } : {})
		},
		ORG,
		...(AUTOR ? [AUTOR] : [])
	);
</script>

<Meta
	title="Meist — kes teeb Pidurdusmaa.ee-d"
	desc="Kes teeb Pidurdusmaa.ee-d, kust tulevad andmed (EL-i rehvimärgis, sõltumatud rehvitestid) ja miks leht on sõltumatu."
	path="meist/"
	crumbs={[['Avaleht', '/'], ['Meist', '/meist/']]}
	{jsonld}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span>Meist</div>
		<h1>Meist</h1>
		<p>Tasuta tööriist, mis näitab, mitu meetrit rehvide vahe sinu autoga päriselt tähendab.</p>
	</div>
</section>

<div class="body-sec">
	<div class="wrap">
		<article class="entry prose entry-content">
			<Autor uuendatud={UUENDATUD} />

			<h2>Miks see leht on olemas</h2>
			<p>
				Rehvimärgis ütleb märghaardumise klassi A–E, aga mitte seda, mitu meetrit varem sinu auto
				nende rehvidega seisma jääb. Rehvitestid mõõdavad pidurdusmaad, aga ühe auto, ühe mõõdu ja ühe
				päeva kohta. Pidurdusmaa.ee paneb need kaks kokku: valid oma auto, rehvimõõdu ja teeolud ning
				näed arvutatud pidurdusmaad koos veapiiriga.
			</p>

			<h2>Kes teeb</h2>
			<p>
				Lehte teeb ja haldab {TEGIJA} Eestis. Mudel, andmete korje ja leht on tehtud nullist selle
				projekti jaoks. Küsimused, vead ja ettepanekud: <a href="/kontakt/">kontaktivorm</a>.
			</p>

			<h2>Kust andmed tulevad</h2>
			<ul>
				<li>
					<strong>EL-i rehvimärgis</strong> — ametlik tooteregister EPREL: praegu {num(data.mudeleid, 0)}
					rehvimudelit {num(data.mootusid, 0)} mõõdus.
				</li>
				<li>
					<strong>Sõltumatud rehvitestid</strong> — {data.testitud} rehvi mõõdetud pidurdusmaaga. Iga
					tulemuse juures on allikas ja aasta.
				</li>
				<li><strong>Autod</strong> — {data.autosid} automudelit koos tehase rehvimõõtudega.</li>
			</ul>
			<p>Testid, millele mudel toetub:</p>
			<ul>
				{#each data.allikad as a (a.kood)}
					<li><a href="/testid/{a.kood}/">{a.nimi}</a>{#if a.tegija} — {a.tegija}{/if}</li>
				{/each}
			</ul>
			<p>
				Kuidas neist andmetest pidurdusmaa arvutatakse ja kui täpne see on:
				<a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">kuidas pidurdusmaa arvutatakse</a>.
			</p>

			<h2>Sõltumatus</h2>
			<p>
				Leht ei müü rehve ja ükski tootja ega pood ei maksa järjestuse eest. Rehvid järjestatakse
				märgise ja mõõdetud testide järgi. Hind mõjutab järjestust ainult siis, kui valid ise „Soodne
				hind“ — ja sama märgiseklassi rehvidest, mis pidurdavad märjal ühtviisi, pakume esimesena
				soodsaimat.
			</p>

			<h2>Vead ja parandused</h2>
			<p>
				Kui leiad vale andmerea, puuduva auto või rehvimõõdu, kirjuta <a href="/kontakt/">kontaktivormi</a
				> kaudu.
			</p>
		</article>
	</div>
</div>
