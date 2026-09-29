<script>
	import Meta from '$lib/Meta.svelte';
	import Liiklus from '$lib/Liiklus.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ =
		'Tasuta peatumisteekonna kalkulaator autokoolidele ja liiklusohutuse õppeks: kiirus, reaktsiooniaeg, teeolud ja rehvid, kaks olukorda kõrvuti. Ilma reklaamita.';
	const jsonld = graph(tooriist('Pidurdusmaa kalkulaator liiklusohutuse õppeks', '/liiklusohutus/', KIRJ), ORG);
</script>

<Meta title="Peatumisteekonna kalkulaator liiklusohutuse õppeks" desc={KIRJ} path="liiklusohutus/" {jsonld} image="/og/sait/liiklusohutus.png" />

<section class="lo-hero">
	<div class="wrap">
		<p class="lo-kick">Tasuta õppevahend · autokoolidele ja liiklusohutuse tööks</p>
		<h1>Kui pika maa pealt auto peatub?</h1>
		<p>
			Muuda kiirust, reaktsiooniaega, teeolusid ja rehvide seisukorda ning vaata kohe, kuidas
			peatumisteekond muutub. Pane kaks olukorda kõrvuti ja näe, millise kiirusega jõuab auto sinna, kus
			teine juba seisab.
		</p>
	</div>
</section>

<section class="lo-bg">
	<div class="wrap">
		<Liiklus />
	</div>
</section>

<section class="lo-info">
	<div class="wrap lo-cols">
		<div>
			<h2>Kuidas tunnis kasutada</h2>
			<ul>
				<li>
					<b>Kiirus.</b> Vali „50 vs 70 km/h“. Takistus on pandud kohta, kus 50 km/h auto peatub — vaata,
					millise kiirusega 70 km/h auto sinna jõuab.
				</li>
				<li>
					<b>Tähelepanu.</b> Reaktsiooniaja ajal sõidab auto täiskiirusel edasi. 50 km/h juures on iga
					lisasekund umbes 14 meetrit.
				</li>
				<li>
					<b>Rehvid ja ilm.</b> Mustrisügavus loeb eriti märjal teel; suverehv lumel ja sulav jää nulli
					lähedal on kõige ohtlikumad olukorrad.
				</li>
				<li>
					<b>Esitlus.</b> „Esitlusrežiim“ avab kalkulaatori täisekraanil. „Kopeeri link“ salvestab kõik
					valikud aadressi sisse — saad tunni jaoks olukorrad ette valmistada.
				</li>
			</ul>
		</div>
		<div>
			<h2>Mida arvutus arvestab</h2>
			<p>
				Pidurdus arvutatakse väikeste ajasammudega: rehvi ja tee haare antud kiirusel ja temperatuuril,
				ABS, pidurite võimekus, koormus, õhutakistus ja tee kalle. Mudel on kalibreeritud 369 mõõdetud
				pidurdusmaa järgi sõltumatutest rehvitestidest ja kontrollitud veel umbes 1300 ajakirjade
				testitulemusega.
			</p>
			<p>
				<b>Tulemus on hinnang, mitte mõõtmine.</b> Iga tulemuse juures on tõenäoline vahemik. Päris
				pidurdusmaa sõltub ka konkreetsest rehvist, teekattest ja juhist. Jää tähendab tavalist
				sõidutee jääd; siledal kiilasjääl on pidurdusmaa pikem (vali „Sile jää“).
			</p>
		</div>
		<div>
			<h2>Allikad</h2>
			<ul class="lo-src">
				<li>ADAC, Tekniikan Maailma, UTAC, Vi Bilägare, Auto Bild, Za Rulem jt — sõltumatud rehvitestid</li>
				<li>EL-i tooteregister EPREL ja rehvimärgise katsemeetod UNECE R117</li>
				<li>DEKRA — mustrisügavuse mõju märjal teel</li>
				<li>
					Green, M. (2000). „How long does it take to stop?“ Transportation Human Factors 2(3) —
					reaktsiooniaeg: valmis juht u 0,7 s, ootamatu oht u 1,25–1,5 s
				</li>
				<li>VTI (Rootsi), Statens vegvesen (Norra), Maanteeamet — haardetegur sõiduteede jääl</li>
			</ul>
			<p class="lo-small">
				Tööriist on tasuta kasutamiseks koolides, autokoolides ja liiklusohutuse töös. Lehel ei ole
				reklaami, hindu ega poode.
			</p>
		</div>
	</div>
</section>

<style>
	.lo-hero {
		background: var(--ink);
		color: var(--on-d);
		padding: var(--sp-10) 0 var(--sp-8);
	}
	.lo-kick {
		color: var(--yellow);
		font-weight: 700;
		font-size: 13px;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		margin: 0 0 var(--sp-3);
	}
	.lo-hero h1 {
		font-family: var(--display);
		font-weight: 700;
		font-size: clamp(40px, 5.4vw, 68px);
		line-height: 0.95;
		text-transform: uppercase;
		margin: 0 0 var(--sp-3);
		text-wrap: balance;
	}
	.lo-hero p:last-child {
		color: #cfd4db;
		font-size: 18px;
		max-width: 760px;
		margin: 0;
	}
	.lo-bg {
		background: var(--paper-2);
	}
	.lo-info {
		background: #fff;
		padding: var(--sp-10) 0 var(--sp-12);
		border-top: 1px solid var(--line);
	}
	.lo-cols {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: var(--sp-8);
	}
	@media (max-width: 900px) {
		.lo-cols {
			grid-template-columns: 1fr;
		}
	}
	.lo-info h2 {
		font-family: var(--display);
		font-weight: 700;
		text-transform: uppercase;
		font-size: 26px;
		margin: 0 0 var(--sp-3);
	}
	.lo-info ul {
		padding-left: 18px;
		margin: 0;
		display: grid;
		gap: var(--sp-2);
	}
	.lo-info p {
		max-width: 65ch;
	}
	.lo-src {
		font-size: 14.5px;
	}
	.lo-small {
		font-size: 14px;
		color: var(--muted);
	}
</style>
