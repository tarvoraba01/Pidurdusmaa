<script>
	import Leht from '$lib/Leht.svelte';
	const SISU = `<p>Igal Euroopas müüdaval sõiduauto rehvil on EL-i rehvimärgis (määrus 2020/740). Andmed tulevad EL-i tooteregistrist EPREL.</p>
<h2>Märghaardumine (A–E)</h2>
<p>Mõõdetakse märjal asfaldil 80 → 20 km/h, võrdluses standardse võrdlusrehviga. Klassi A ja E vahe on tavalisel sõiduautol 90 km/h juures umbes 18 meetrit (klasside keskpunktide järgi arvutatud). Klass on <strong>mõõdupõhine</strong>: sama rehvimudel võib olla ühes mõõdus A ja teises B.</p>
<h2>Veeretakistus (A–E)</h2>
<p>Mõjutab kütuse- või energiakulu. Pidurdusmaaga ei ole otsest seost — kontrollisime seda 41 testitud rehvi peal ja veeretakistuse klass ei seletanud märja pidurduse erinevusi.</p>
<h2>Müra (dB ja A–C)</h2>
<p>Rehvi veeremismüra ametliku katse järgi. Väiksem number = vaiksem rehv. Iga 3 dB on ligikaudu kahekordne heliväljund.</p>
<h2>Lume- ja jäämärk</h2>
<p>Kolme mäetipu ja lumehelbe märk (3PMSF) tähendab, et rehv läbis lumehaarde katse. Jäämärk tähendab Põhjamaade jääkatse läbimist (ainult sõiduauto rehvid).</p>`;
</script>

<Leht
	title="EL-i rehvimärgis: mida klassid tähendavad"
	desc="Märghaardumine, veeretakistus, müra, lume- ja jäämärk — mida EL-i rehvimärgise klassid päriselt tähendavad."
	path="teadmine/rehvimargis/"
	crumbs={[["Teadmine", "/teadmine/"], ["EL-i rehvimärgis: mida klassid tähendavad", "/teadmine/rehvimargis/"]]}
	lapsed={[]}
	uuendatud="2026-09-25"
	sisu={SISU}
	kkk={[
		['Mida tähendab märghaardumise klass A–E?', 'Klass näitab, kui hästi rehv pidurdab märjal asfaldil, võrreldes standardse võrdlusrehviga (katse 80 → 20 km/h). A on parim. Tavalisel sõiduautol on klasside A ja E vahe 90 km/h juures umbes 18 meetrit.'],
		['Kas veeretakistuse klass mõjutab pidurdust?', 'Otseselt mitte. Kontrollisime 41 testitud rehvi peal ja veeretakistuse klass ei seletanud märja pidurduse erinevusi. See klass mõjutab kütuse- või energiakulu.'],
		['Miks on samal rehvil eri mõõtudes erinev klass?', 'Märgis on mõõdupõhine: iga mõõt katsetatakse eraldi. Sama mudel võib olla ühes mõõdus A ja teises B.'],
		['Mida tähendab lumehelbe ja mäetippude märk?', 'Kolme mäetipu ja lumehelbe märk (3PMSF) tähendab, et rehv läbis lumehaarde katse. Eestis peab lamellrehvil talverehvide kohustuslikul ajal see märk olema. Jäämärk tähendab Põhjamaade jääkatse läbimist.'],
		['Kust saan oma rehvi märgise andmed?', 'Märgise andmed on EL-i tooteregistris EPREL. Pidurdusmaa.ee näitab neid iga rehvimudeli ja mõõdu juures ning arvutab märgise põhjal pidurdusmaa sinu autoga.']
	]}
/>
