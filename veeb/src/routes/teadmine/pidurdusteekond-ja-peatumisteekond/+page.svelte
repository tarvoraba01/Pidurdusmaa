<script>
	/* Artikkel: pidurdusteekond, reageerimisteekond ja peatumisteekond.
	   Otsingusõnad, mida kasutavad autokoolid, õpikud ja liikluseeskiri.
	   Kõik näidete arvud tulevad mudelist (demo), käsitsi kirjutatud on
	   ainult reageerimisteekond, mis on lihtne korrutis. */
	import Meta from '$lib/Meta.svelte';
	import { num } from '$lib/util.js';
	import { BASE, ORG_ID, AUTOR, autorRef, graph } from '$lib/skeem.js';
	import Autor from '$lib/Autor.svelte';

	let { data } = $props();
	const d = data.demo;
	const UUENDATUD = '2026-09-25';
	const PATH = '/teadmine/pidurdusteekond-ja-peatumisteekond/';
	const TITLE = 'Pidurdusteekond ja peatumisteekond: valem, näited ja kalkulaator';
	const react = (v, t = 1) => (v / 3.6) * t;
	const i90 = d ? d.speeds.indexOf(90) : -1;

	const KKK = [
		[
			'Mis vahe on pidurdusteekonnal ja peatumisteekonnal?',
			'Pidurdusteekond on vahemaa hetkest, kui pidur hakkab tööle, kuni auto seisab. Peatumisteekond on pikem: sellele lisandub reageerimisteekond, mille auto läbib täiskiirusel ajal, kui juht ohtu märkab ja jalga pidurile viib.'
		],
		[
			'Kuidas peatumisteekonda arvutada?',
			'Peatumisteekond = reageerimisteekond + pidurdusteekond. Reageerimisteekond on kiirus meetrites sekundis korda reaktsiooniaeg (km/h jagatud 3,6-ga). Pidurdusteekond on ligikaudu v² / (2 · μ · g), kus μ on rehvi ja tee haardetegur ning g = 9,81 m/s².'
		],
		[
			'Kui pikk on juhi reaktsiooniaeg?',
			'Arvutustes kasutatakse tavaliselt umbes 1 sekundit. Kui juht on pidurdamiseks valmis, võib see olla alla 1 sekundi; väsinud või telefoni vaatava juhi reaktsiooniaeg on sageli 1,5–2 sekundit või rohkem.'
		],
		[
			'Mitu korda pikeneb pidurdusteekond, kui kiirus kahekordistub?',
			'Pidurdusteekond kasvab kiiruse ruudus: kaks korda suurem kiirus tähendab umbes neli korda pikemat pidurdusteekonda. Reageerimisteekond kasvab kiirusega võrdeliselt, ehk kaks korda.'
		]
	];
	if (d && i90 >= 0) {
		KKK.push([
			'Kui pikk on peatumisteekond 90 km/h juures?',
			`Tüüpilise kompaktauto (${d.car}) peatumisteekond 1-sekundilise reaktsiooniajaga on kuival asfaldil umbes ${num(react(90) + d.dry[i90])} m ja märjal umbes ${num(react(90) + d.wet[i90])} m. Sellest 25 m on reageerimisteekond.`
		]);
	}

	const jsonld = graph(
		{
			'@type': 'Article',
			'@id': BASE + PATH + '#artikkel',
			headline: TITLE,
			inLanguage: 'et',
			datePublished: UUENDATUD,
			dateModified: UUENDATUD,
			author: autorRef(),
			publisher: { '@id': ORG_ID },
			mainEntityOfPage: BASE + PATH,
			image: BASE + '/og/sait/avaleht.png'
		},
		...(AUTOR ? [AUTOR] : []),
		{
			'@type': 'FAQPage',
			mainEntity: KKK.map(([q, a]) => ({
				'@type': 'Question',
				name: q,
				acceptedAnswer: { '@type': 'Answer', text: a }
			}))
		}
	);
</script>

<Meta
	title="Pidurdusteekond ja peatumisteekond — valem ja näited"
	desc="Mis on reageerimisteekond, pidurdusteekond ja peatumisteekond, kuidas neid arvutada ja kui pikad need on eri kiirustel kuival ja märjal teel. Koos kalkulaatoriga."
	path="teadmine/pidurdusteekond-ja-peatumisteekond/"
	ogType="article"
	crumbs={[
		['Avaleht', '/'],
		['Teadmine', '/teadmine/'],
		['Pidurdusteekond ja peatumisteekond', PATH]
	]}
	{jsonld}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href="/">Avaleht</a><span>/</span><a href="/teadmine/">Teadmine</a><span>/</span>Pidurdusteekond ja
			peatumisteekond
		</div>
		<h1>Pidurdusteekond ja peatumisteekond</h1>
		<p>Valem, näited ja kalkulaator: kui kaugel auto tegelikult peatub.</p>
	</div>
</section>

<div class="body-sec">
	<div class="wrap">
		<article class="entry prose entry-content">
			<Autor uuendatud={UUENDATUD} />

			<p>
				<strong>Peatumisteekond = reageerimisteekond + pidurdusteekond.</strong> Pidurdusteekond (ehk
				pidurdusmaa) algab hetkest, kui pidur hakkab tööle. Peatumisteekond algab juba hetkest, kui
				juht ohtu märkab, ja see on alati pikem.
			</p>

			<h2>Kolm mõistet</h2>
			<ul>
				<li>
					<strong>Reageerimisteekond</strong>: vahemaa, mille auto läbib täiskiirusel ajal, kui juht
					ohtu märkab, otsustab ja jala pidurile viib.
				</li>
				<li>
					<strong>Pidurdusteekond</strong> (pidurdusmaa): vahemaa pidurdamise algusest seismajäämiseni.
					Selle määravad kiirus, rehv, tee ja auto.
				</li>
				<li>
					<strong>Peatumisteekond</strong>: need kaks kokku ehk vahemaa ohu märkamisest kuni auto
					seisab.
				</li>
			</ul>

			<h2>Valemid</h2>
			<p><strong>Reageerimisteekond</strong> = kiirus (m/s) × reaktsiooniaeg (s)</p>
			<p>
				Kiiruse saad meetriteks sekundis, kui jagad km/h 3,6-ga. 90 km/h on 25 m/s, seega 1-sekundilise
				reaktsiooniajaga sõidab auto enne pidurdamist <strong>25 meetrit</strong>.
			</p>
			<p><strong>Pidurdusteekond</strong> ≈ v² / (2 · μ · g)</p>
			<p>
				Siin on v kiirus meetrites sekundis, μ rehvi ja tee haardetegur ning g = 9,81 m/s². Haardetegur
				on kuival asfaldil heal rehvil umbes 0,8–1,0, märjal asfaldil sageli 0,5–0,7, lumel ja jääl
				palju väiksem. Kuna kiirus on ruudus, tähendab <strong>kaks korda suurem kiirus umbes neli
				korda pikemat pidurdusteekonda</strong>.
			</p>
			<p>
				Lihtne valem annab suurusjärgu. Päris pidurdusteekond sõltub ka sellest, kui kiiresti pidurid
				täisjõu saavutavad, ABS-ist, rehvi mustrisügavusest, veekihist ja temperatuurist.
				Pidurdusmaa.ee kalkulaator arvestab neid ja kasutab rehvi kohta päris andmeid: EL-i rehvimärgist
				ja sõltumatuid teste. Täpsemalt loe
				<a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">kuidas pidurdusmaa arvutatakse</a>.
			</p>

			{#if d}
				<h2>Näited eri kiirustel</h2>
				<p>
					Arvutatud kalkulaatori sama mudeliga: {d.car}. Reaktsiooniaeg 1 s. Märg asfalt: veekiht
					1 mm, +10 °C. Kuiv asfalt: +15 °C.
				</p>
				<p>
					Tabelis on peatumisteekond (suur number) ja selle sees olev pidurdusteekond (väike number).
				</p>
				<div class="tbl-wrap">
					<table class="t peat">
						<thead>
							<tr>
								<th>Kiirus</th>
								<th class="n">Reagee&shy;rimine</th>
								<th class="n">Kuival</th>
								<th class="n">Märjal</th>
							</tr>
						</thead>
						<tbody>
							{#each d.speeds as v, i (v)}
								<tr>
									<td class="nw"><b>{v}</b> km/h</td>
									<td class="n">{num(react(v))} m</td>
									<td class="n">
										<b>{num(react(v) + d.dry[i])} m</b><small>sh pidurdus {num(d.dry[i])}</small>
									</td>
									<td class="n">
										<b>{num(react(v) + d.wet[i])} m</b><small>sh pidurdus {num(d.wet[i])}</small>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
				<p>
					Madalal kiirusel on suurem osa peatumisteekonnast reageerimine: 50 km/h juures on see
					{num(react(50))} m, pidurdus kuival {num(d.dry[0])} m. Suurel kiirusel on vastupidi, sest
					pidurdusteekond kasvab ruudus.
				</p>
			{/if}

			<h2>Reaktsiooniaeg</h2>
			<p>
				Arvutustes võetakse tavaliselt umbes <strong>1 sekund</strong>. Kui juht on pidurdamiseks
				valmis (jalg juba pedaali kohal), võib see olla alla 1 sekundi. Väsimus, telefon, alkohol või
				ootamatu olukord venitavad selle kergesti 1,5–2 sekundini ja enamgi. 90 km/h juures tähendab iga
				lisasekund veel <strong>25 meetrit</strong> enne, kui auto üldse pidurdama hakkab.
			</p>

			<h2>Mis veel pidurdusteekonda muudab</h2>
			{#if d}
				<ul>
					<li>
						<strong>Rehv.</strong> Sama auto, sama märg tee, 90 km/h: EL-i märgise märghaardumise klass A
						{num(d.classA)} m, klass E {num(d.classE)} m.
					</li>
					<li>
						<strong>Mustrisügavus.</strong> Märjal 90 km/h: uus rehv (8 mm) {num(d.tread8)} m, kulunud (3
						mm) {num(d.tread3)} m.
					</li>
					<li>
						<strong>Hooaeg.</strong> Lumel 50 km/h: suverehviga {num(d.snowSummer)} m, talverehviga
						{num(d.snowWinter)} m.
					</li>
					<li>
						<strong>Koormus.</strong> Märjal 90 km/h: tühi auto {num(d.tread8)} m, 450 kg lisakoormaga
						{num(d.loaded)} m.
					</li>
				</ul>
			{/if}

			<h2>Arvuta oma auto peatumisteekond</h2>
			<p>
				<a href="/">Pidurdusmaa kalkulaatoris</a> vali oma auto, rehvimõõt, kiirus ja teeolud. Tulemuses
				vali <strong>„Peatumisteekond“</strong> ja reaktsiooniaeg: näed eraldi reageerimisteekonda ja
				pidurdusteekonda ning seda, kui palju muudaks teine rehv.
			</p>

			<h2>Korduma kippuvad küsimused</h2>
			{#each KKK as [q, a] (q)}
				<h3>{q}</h3>
				<p>{a}</p>
			{/each}

			<p class="note">
				Arvud on arvutatud hinnang, mitte garantii. Ära kasuta neid liikluses otsustamiseks: hoia alati
				piisavat pikivahet ja vali kiirus teeolude järgi.
			</p>
		</article>
	</div>
</div>

<style>
	table.peat {
		min-width: 0;
	}
	table.peat small {
		white-space: normal;
		display: block;
		font-size: 12px;
		color: var(--muted);
		font-weight: 500;
	}
	table.peat .nw {
		white-space: nowrap;
	}
	@media (max-width: 480px) {
		table.peat th,
		table.peat td {
			padding: var(--sp-2) var(--sp-1);
			font-size: 13.5px;
		}
		table.peat th {
			letter-spacing: 0;
			white-space: normal;
		}
	}
</style>
