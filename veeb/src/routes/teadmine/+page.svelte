<script>
	/* Teadmine: kategooriad plokkidena, iga kaart üks rida selgitust. */
	import Meta from '$lib/Meta.svelte';
	import Icon from '$lib/Icon.svelte';
	import { ARTIKLID, artikliTee, kuup } from '$lib/artiklid.js';

	const POHI = [
		['/teadmine/rehvivahetus/', 'calendar', 'Rehvivahetus', 'Millal talverehvid ja suverehvid alla: kuupäevad ja nõuded.'],
		['/teadmine/pidurdusteekond-ja-peatumisteekond/', 'road', 'Pidurdus- ja peatumisteekond', 'Valem, reaktsiooniaeg ja näited eri kiirustel.'],
		['/teadmine/rehvimargis/', 'info', 'EL-i rehvimärgis', 'Mida tähendavad märghaarde, veeretakistuse ja müra klassid.']
	];
	const ANDMED = [
		['/autod/', 'road', 'Autod', 'Iga mudeli tehase rehvimõõdud, mootorid ja pidurdusmaa.'],
		['/rehvid/', 'tyre', 'Rehvid', 'Kõik rehvid märgise andmete ja testitulemustega.'],
		['/talverehvid/', 'snow', 'Talverehvid mõõdu järgi', 'Testitud naast- ja lamellrehvid sinu rehvimõõdus: pidurdusmaa lumel ja jääl.'],
		['/testid/', 'test', 'Sõltumatud testid', 'ADAC, Tekniikan Maailma jt — mõõdetud pidurdusmaad.'],
		['/margid/', 'scale', 'Rehvimargid', 'Tootjad ja nende rehvid ühest kohast.']
	];
	const MEETOD = [
		['/teadmine/kuidas-pidurdusmaa-arvutatakse/', 'gauge', 'Kuidas pidurdusmaa arvutatakse', 'Mudel, eeldused, täpsus ja piirangud.'],
		['/teadmine/partnerid/', 'shield', 'Partnerid ja poelingid', 'Kuidas leht tasuta püsib ja miks see järjestust ei mõjuta.']
	];
</script>

<Meta
	title="Teadmine"
	desc="Artiklid rehvi valimiseks ja kust iga Pidurdusmaa.ee number tuleb — mudel, EL-i rehvimärgis ja sõltumatud testid."
	path="teadmine/"
	crumbs={[['Avaleht', '/'], ['Teadmine', '/teadmine/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span>Teadmine</div>
		<h1>Teadmine</h1>
		<p>Kuidas pidurdamine töötab, kuidas rehvi valida ja kust iga number tuleb.</p>
	</div>
</section>

<div class="tm">
	<div class="wrap">
		<a class="tm-feat" href="/liiklusohutus/">
			<span class="tm-eyebrow">Tööriist</span>
			<span class="tm-feat-t">Peatumisteekonna kalkulaator</span>
			<span class="tm-feat-d">Kiirus, reaktsiooniaeg, teeolud ja rehvid — kaks olukorda kõrvuti.</span>
			<span class="tm-tags"><span>Jagatav link</span><span>Esitlusrežiim</span><span>Tasuta, ilma reklaamita</span></span>
			<span class="tm-go"><Icon name="arrow" /></span>
		</a>

		<section class="tm-sec" aria-labelledby="tm-art">
			<div class="tm-head">
				<h2 id="tm-art">Artiklid</h2>
				<a class="tm-all" href="/teadmine/artiklid/">Kõik artiklid <Icon name="arrow" /></a>
			</div>
			<div class="tm-grid">
				{#each ARTIKLID.slice(0, 4) as a (a.slug)}
					<a class="tm-card" href={artikliTee(a)}>
						<span class="tm-eyebrow dark">{a.silt}</span>
						<span class="tm-t">{a.title}</span>
						<span class="tm-d">{a.desc}</span>
						<span class="tm-date">{kuup(a.kuupaev)}</span>
					</a>
				{/each}
			</div>
		</section>

		<section class="tm-sec" aria-labelledby="tm-pohi">
			<h2 id="tm-pohi">Põhitõed</h2>
			<div class="tm-grid">
				{#each POHI as [href, ic, t, d] (href)}
					<a class="tm-card" {href}>
						<span class="tm-ic"><Icon name={ic} /></span>
						<span class="tm-t">{t}</span>
						<span class="tm-d">{d}</span>
					</a>
				{/each}
			</div>
		</section>

		<section class="tm-sec" aria-labelledby="tm-met">
			<h2 id="tm-met">Kust numbrid tulevad</h2>
			<div class="tm-grid">
				{#each MEETOD as [href, ic, t, d] (href)}
					<a class="tm-card" {href}>
						<span class="tm-ic"><Icon name={ic} /></span>
						<span class="tm-t">{t}</span>
						<span class="tm-d">{d}</span>
					</a>
				{/each}
			</div>
		</section>

		<section class="tm-sec" aria-labelledby="tm-and">
			<h2 id="tm-and">Autod, rehvid ja testid</h2>
			<div class="tm-grid">
				{#each ANDMED as [href, ic, t, d] (href)}
					<a class="tm-card" {href}>
						<span class="tm-ic"><Icon name={ic} /></span>
						<span class="tm-t">{t}</span>
						<span class="tm-d">{d}</span>
					</a>
				{/each}
			</div>
		</section>
	</div>
</div>

<style>
	.page-hero p {
		margin-top: var(--sp-2);
	}
	.tm {
		background: var(--paper-2);
		padding: var(--sp-10) 0 var(--sp-16);
	}
	.tm-sec {
		margin-top: var(--sp-10);
	}
	.tm-head {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: var(--sp-4);
	}
	h2 {
		font-family: var(--display);
		font-weight: 700;
		text-transform: uppercase;
		font-size: 28px;
		margin: 0 0 var(--sp-4);
	}
	.tm-all {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		font-weight: 600;
		text-decoration: none;
		white-space: nowrap;
	}
	.tm-all :global(svg) {
		width: 18px;
		height: 18px;
	}
	.tm-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: var(--sp-4);
	}
	.tm-grid3 {
		grid-template-columns: repeat(3, minmax(0, 1fr));
	}
	@media (max-width: 860px) {
		.tm-grid3 {
			grid-template-columns: 1fr;
		}
	}
	@media (max-width: 640px) {
		.tm-grid {
			grid-template-columns: 1fr;
		}
	}
	.tm-card {
		display: flex;
		flex-direction: column;
		gap: var(--sp-2);
		background: #fff;
		border: 1px solid var(--line);
		border-radius: var(--r-lg);
		padding: var(--sp-5);
		text-decoration: none;
		color: var(--text);
		transition:
			border-color 0.15s,
			box-shadow 0.15s,
			transform 0.15s;
	}
	.tm-card:hover {
		border-color: #c5cad3;
		box-shadow: var(--shadow);
		transform: translateY(-1px);
	}
	.tm-ic {
		width: 40px;
		height: 40px;
		border-radius: 10px;
		background: var(--yellow-soft);
		display: grid;
		place-items: center;
		color: var(--yellow-ink);
	}
	.tm-ic :global(svg) {
		width: 22px;
		height: 22px;
	}
	.tm-t {
		font-weight: 700;
		font-size: 18px;
		line-height: 1.3;
	}
	.tm-d {
		color: var(--muted);
		font-size: 15px;
	}
	.tm-date {
		margin-top: auto;
		font-size: 13px;
		color: var(--muted);
	}
	.tm-eyebrow {
		font-size: 12px;
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--yellow);
	}
	.tm-eyebrow.dark {
		color: var(--muted);
	}
	.tm-feat {
		position: relative;
		display: flex;
		flex-direction: column;
		gap: var(--sp-2);
		background: var(--ink);
		color: var(--on-d);
		border-radius: var(--r-lg);
		padding: var(--sp-6) var(--sp-16) var(--sp-6) var(--sp-6);
		text-decoration: none;
		box-shadow: var(--shadow);
	}
	.tm-feat-t {
		font-family: var(--display);
		font-weight: 700;
		font-size: clamp(26px, 3vw, 36px);
		line-height: 1;
		text-transform: uppercase;
	}
	.tm-feat-d {
		color: #cfd4db;
	}
	.tm-tags {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-2);
		margin-top: var(--sp-2);
	}
	.tm-tags span {
		border: 1px solid var(--line-d);
		border-radius: 999px;
		padding: 3px 12px;
		font-size: 13px;
		color: #dfe3e8;
	}
	.tm-go {
		position: absolute;
		right: var(--sp-6);
		top: 50%;
		transform: translateY(-50%);
		width: 44px;
		height: 44px;
		border-radius: 50%;
		background: var(--yellow);
		color: var(--yellow-ink);
		display: grid;
		place-items: center;
		transition: transform 0.15s;
	}
	.tm-go :global(svg) {
		width: 22px;
		height: 22px;
	}
	.tm-feat:hover .tm-go {
		transform: translateY(-50%) translateX(3px);
	}
	@media (max-width: 640px) {
		.tm-feat {
			padding: var(--sp-5);
		}
		.tm-go {
			position: static;
			transform: none;
			margin-top: var(--sp-2);
		}
		.tm-feat:hover .tm-go {
			transform: none;
		}
	}
</style>
