<script>
	import Meta from '$lib/Meta.svelte';
	let { data } = $props();
</script>

<Meta
	title="Sõltumatud rehvitestid — mõõdetud pidurdusmaad"
	desc="Rehvitestid, mille mõõdetud tulemusi Pidurdusmaa.ee kasutab: ADAC, Tekniikan Maailma, UTAC, Vi Bilägare. Allikas, kuupäev, protokoll ja iga rehvi tulemus."
	path="testid/"
	crumbs={[['Avaleht', '/'], ['Testid', '/testid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span>Testid</div>
		<h1>Sõltumatud testid</h1>
		<p>
			Testid, mille mõõdetud tulemusi Pidurdusmaa.ee kasutab. Igal testil on allikas, aasta, auto,
			rehvimõõt ja protokoll. Me ei korralda teste ise.
		</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="grid-cards" style="grid-template-columns:repeat(auto-fill,minmax(340px,1fr))">
			{#each data.sources as s (s.slug)}
				<a class="tcard" href="/testid/{s.slug}/" style="padding:20px">
					<span class="b">{s.tegija} · {s.aasta}</span>
					<h3 style="font-size:20px">{s.nimi}</h3>
					<span class="meta">{s.rehve} rehvi · {s.moot} · {s.auto}</span>
					<p class="note" style="margin:10px 0 0">{s.protokoll}</p>
				</a>
			{/each}
		</div>
		<div class="box" style="margin-top:24px">
			<h2>Kuidas teste kasutatakse</h2>
			<ul>
				<li>Testi mõõdetud märja pidurduse järgi tuletatakse rehvi märghaardumise indeks — see on täpsem kui märgise klass.</li>
				<li>Kuiva, lume ja jää tulemused kalibreerivad mudeli rehvikategooriate kaupa.</li>
				<li>Vi Bilägare 2010 testid on mudeli kontrolliks: mudel ei näinud neid kalibreerimisel.</li>
				<li>Testi tulemus kehtib testi mõõdus ja autol. Teises mõõdus võib sama rehv olla veidi teistsugune.</li>
			</ul>
		</div>
	</div>
</div>
