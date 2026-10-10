<script>
	import Meta from '$lib/Meta.svelte';
	import { BASE, ORG, ORG_ID, graph } from '$lib/skeem.js';
	import { num } from '$lib/util.js';
	let { data } = $props();
	const aastad = data.sources.map((s) => +s.aasta).filter(Boolean);
	const uusim = Math.max(...aastad);
	const RUHMAD = [
		['talv', 'Talverehvide testid ' + uusim, 'Lamell- ja naastrehvid: pidurdus märjal ja kuival asfaldil, lumel ja jääl.'],
		['suvi', 'Suve- ja aastaringsete rehvide testid ' + uusim, 'Pidurdus märjal ja kuival asfaldil, vesiliug; aastaringsetel ka lumi.'],
		['vana', 'Vanemad testid (mudeli kontroll)', 'Neid tulemusi mudel kalibreerimisel ei näinud — nendega kontrollitakse, kas arvutus peab paika.']
	];
	const ruhm = (h) => data.sources.filter((s) => s.hooaeg === h);
	const esimene = (h) => ruhm(h).filter((s) => s.top.length).map((s) => `${s.nimi}: ${s.top[0].name} (${num(s.top[0].m)} m)`);

	/* KKK: vastused tulevad andmetest, mitte käsitsi */
	const kkk = [
		['Mis on rehvitest?', 'Rehvitestis sõidetakse samade tingimuste, sama auto ja sama rehvimõõduga läbi kümmekond rehvi ning mõõdetakse pidurdusmaad märjal ja kuival asfaldil, talverehvidel ka lumel ja jääl. Suurimad Põhjamaade jaoks olulised testijad on ADAC (Saksamaa) ja Tekniikan Maailma (Soome).'],
		...(esimene('talv').length ? [['Milline talverehv pidurdas ' + uusim + '. aasta testides märjal kõige lühemalt?', 'Lühim pidurdusmaa märjal asfaldil: ' + esimene('talv').join('; ') + '. Testi üldvõitja arvestab ka lund, jääd, müra ja kulumist, seega vaata kogu tabelit.']] : []),
		...(esimene('suvi').length ? [['Milline suverehv pidurdas ' + uusim + '. aasta testides märjal kõige lühemalt?', 'Lühim pidurdusmaa märjal asfaldil: ' + esimene('suvi').join('; ') + '.']] : []),
		['Kas rehvitesti tulemus kehtib ka minu rehvimõõdus ja autol?', 'Ligikaudu. Test mõõdetakse ühes mõõdus ja ühel autol. Pidurdusmaa.ee arvutab testi järgi rehvi haarde ja sellega sinu auto ja mõõdu pidurdusmaa — vali kalkulaatoris oma auto.'],
		['Kui paljusid rehve testid katavad?', 'Testides on kokku ' + data.sources.reduce((a, s) => a + (s.rehve || 0), 0) + ' rehvitulemust. Testimata rehvidel kasutame ELi rehvimärgise märghaarde klassi, mis on vähem täpne.']
	];

	const jsonld = graph(ORG, {
		'@type': 'Dataset',
		'@id': BASE + '/testid/#andmed',
		name: 'Rehvitestide mõõdetud pidurdusmaad',
		description: 'Rehvitestide (ADAC, Tekniikan Maailma, UTAC, Vi Bilägare) mõõdetud pidurdusmaad märjal ja kuival asfaldil, lumel ja jääl, allika, aasta, auto, rehvimõõdu ja protokolliga. Pidurdusmaa.ee kalibreerib nende järgi oma pidurdusmudelit.',
		url: BASE + '/testid/',
		inLanguage: 'et',
		creator: { '@id': ORG_ID },
		publisher: { '@id': ORG_ID },
		keywords: ['rehvitest', 'rehvitestid', 'talverehvide test', 'suverehvide test', 'ADAC rehvitest', 'pidurdusmaa'],
		variableMeasured: ['pidurdusmaa märjal asfaldil', 'pidurdusmaa kuival asfaldil', 'pidurdusmaa lumel', 'pidurdusmaa jääl'],
		...(aastad.length ? { temporalCoverage: Math.min(...aastad) + '/' + Math.max(...aastad) } : {}),
		isBasedOn: data.sources.map((s) => ({ '@type': 'CreativeWork', name: s.nimi, author: { '@type': 'Organization', name: s.tegija }, datePublished: String(s.aasta), url: BASE + '/testid/' + s.slug + '/' }))
	}, { '@type': 'FAQPage', mainEntity: kkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) });
</script>

<Meta
	title="Rehvitestid {uusim} — talve- ja suverehvide testide tulemused"
	desc="Rehvitestid {uusim}: ADAC, Tekniikan Maailma ja UTAC talverehvide ja suverehvide testid. Iga rehvi mõõdetud pidurdusmaa märjal, kuival, lumel ja jääl ühes kohas."
	path="testid/"
	crumbs={[['Avaleht', '/'], ['Rehvitestid', '/testid/']]}
	{jsonld}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span>Rehvitestid</div>
		<h1>Rehvitestid {uusim}</h1>
		<p>
			Kõik suuremad talverehvide ja suverehvide testid ühes kohas: iga rehvi mõõdetud pidurdusmaa,
			testi auto, rehvimõõt ja protokoll. Testid teevad ADAC, Tekniikan Maailma jt — meie ei korralda
			teste ise, vaid arvutame nende järgi pidurdusmaa sinu autole.
		</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		{#each RUHMAD as [h, pealkiri, selgitus] (h)}
			{#if ruhm(h).length}
				<h2 style="margin:var(--sp-6) 0 var(--sp-1)">{pealkiri}</h2>
				<p class="sub" style="margin:0 0 var(--sp-4)">{selgitus}</p>
				<div class="grid-cards" style="grid-template-columns:repeat(auto-fill,minmax(min(340px,100%),1fr))">
					{#each ruhm(h) as s (s.slug)}
						<a class="tcard" href="/testid/{s.slug}/" style="padding:var(--sp-5)">
							<span class="b">{s.tegija} · {s.aasta}</span>
							<h3 style="font-size:20px">{s.nimi}</h3>
							<span class="meta">{s.rehve} rehvi · {s.moot} · {s.auto}</span>
							{#if s.top.length}
								<span class="note" style="display:block;margin:var(--sp-3) 0 var(--sp-1);font-weight:600">Lühim pidurdus märjal ({s.top[0].v0}→{s.top[0].v1} km/h):</span>
								<ol class="note" style="margin:0;padding-left:1.2em">
									{#each s.top as r (r.slug)}<li>{r.name} — {num(r.m)} m</li>{/each}
								</ol>
							{:else}
								<p class="note" style="margin:var(--sp-3) 0 0">{s.protokoll}</p>
							{/if}
						</a>
					{/each}
				</div>
			{/if}
		{/each}
		<div class="box" style="margin-top:var(--sp-6)">
			<h2>Kuidas rehvitestide tulemusi kasutatakse</h2>
			<ul>
				<li>Testi mõõdetud märja pidurduse järgi tuletatakse rehvi märghaardumise indeks — see on täpsem kui märgise klass.</li>
				<li>Kuiva, lume ja jää tulemused kalibreerivad mudeli rehvikategooriate kaupa.</li>
				<li>Vi Bilägare 2010 testid on mudeli kontrolliks: mudel ei näinud neid kalibreerimisel.</li>
				<li>Testi tulemus kehtib testi mõõdus ja autol. Teises mõõdus võib sama rehv olla veidi teistsugune.</li>
			</ul>
			<p style="margin:var(--sp-4) 0 0"><a class="btn yel" href="/#kalkulaator">Arvuta pidurdusmaa oma autoga →</a></p>
		</div>
		<div class="box">
			<h2>Korduma kippuvad küsimused</h2>
			{#each kkk as [q, a] (q)}<h3 style="font-size:17px;margin:var(--sp-4) 0 var(--sp-1)">{q}</h3><p style="margin:0">{a}</p>{/each}
		</div>
	</div>
</div>
