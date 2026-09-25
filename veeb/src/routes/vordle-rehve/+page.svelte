<script>
	/* /vordle-rehve/ — valitud 2–4 rehvi kõrvuti. Valimise loogika on
	   /rehvi-valimine/ lehel; siin ainult võrdlus ja otsing lisamiseks. */
	import Meta from '$lib/Meta.svelte';
	import { tooriist, graph } from '$lib/skeem.js';
	import How from '$lib/How.svelte';
</script>

<Meta
	title="Võrdle rehve — märghaare, müra, veeretakistus ja pidurdusmaa"
	desc="Võrdle rehvimudeleid sinu auto mõõdus päris andmete järgi: EL-i rehvimärgis, sõltumatud testid ja arvutatud pidurdusmaa. Ilma väljamõeldud koondhindeta."
	path="vordle-rehve/"
	crumbs={[['Avaleht', '/'], ['Rehvi valimine', '/rehvi-valimine/'], ['Võrdle', '/vordle-rehve/']]}
	jsonld={graph(tooriist('Rehvide võrdlus', '/vordle-rehve/', 'Võrdleb 2–4 rehvimudelit sinu auto mõõdus: märghaare, müra, veeretakistus ja arvutatud pidurdusmaa.'))}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href="/">Avaleht</a><span>/</span><a href="/rehvi-valimine/">Rehvi valimine</a><span>/</span>Võrdle
		</div>
		<h1>Võrdle rehve kõrvuti</h1>
		<p>
			Iga omadus eraldi ja allikaga: EL-i rehvimärgis, sõltumatud testid ja arvutatud pidurdusmaa sinu
			autoga. Ühtegi „parima rehvi“ punktisummat ei ole.
		</p>
		<div class="pills">
			<span class="pill off">Ametlik märgis</span><span class="pill test">Sõltumatu test</span><span
				class="pill calc">Arvutus</span
			><span class="pill"><span class="est" style="margin:0">≈</span> Tuletatud</span>
		</div>
	</div>
</section>

<div class="body-sec" data-cmp-page data-mode="vordle">
	<div class="wrap">
		<div id="vordlus" data-cmp-table></div>

		<div class="box" style="margin-top:var(--sp-8)">
			<h2>Lisa rehve</h2>
			<div class="add-bar">
				<select class="lsel" data-f="make" aria-label="Mark"><option value="">Mark</option></select>
				<select class="lsel" data-f="model" aria-label="Mudel" disabled><option value="">Mudel</option></select>
				<select class="lsel" data-f="year" aria-label="Aasta" disabled><option value="">Aasta</option></select>
				<select class="lsel" data-f="variant" aria-label="Variant" disabled><option value="">Variant</option></select>
				<select class="lsel" data-f="size" aria-label="Rehvimõõt"><option value="20555R16">205/55 R16</option></select>
				<div class="lseg" role="group" aria-label="Hooaeg">
					<button type="button" data-season="summer">Suvi</button>
					<button type="button" data-season="all">Aastaringne</button>
					<button type="button" data-season="winter">Talv</button>
				</div>
				<select class="lsel" data-brand aria-label="Mark"><option value="">Kõik margid</option></select>
				<input class="lsel" type="search" data-q placeholder="Otsi marki või mudelit" aria-label="Otsi rehvi" style="background-image:none" />
			</div>
			<p class="note" data-cmp-head style="margin:var(--sp-3) 0"></p>
			<div class="res-list" data-cmp-list><p class="note">Laen…</p></div>
		</div>
	</div>
</div>

<div class="cmp-tray" data-tray hidden>
	<div class="wrap">
		<div class="chips" data-tray-chips></div>
		<a class="btn yel sm" href="#vordlus" data-tray-go>Vaata võrdlust ↑</a>
	</div>
</div>
<How />
