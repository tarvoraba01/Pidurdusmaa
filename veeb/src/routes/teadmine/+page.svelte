<script>
	import Leht from '$lib/Leht.svelte';
	const SISU = `<p>Pidurdusmaa.ee näitab arvutatud pidurdusmaad ja rehvide päris omadusi. Siin on kirjas, kust iga number tuleb ja mida me <strong>ei</strong> tea.</p>
<ul><li><a href="/teadmine/pidurdusteekond-ja-peatumisteekond/">Pidurdusteekond ja peatumisteekond</a> — valem, näited eri kiirustel ja reaktsiooniaja mõju</li><li><a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a> — mudel, eeldused, täpsus ja piirangud</li><li><a href="/teadmine/rehvimargis/">EL-i rehvimärgis</a> — mida märghaardumise, veeretakistuse ja müra klass tähendavad</li><li><a href="/testid/">Sõltumatud testid</a> — millised testid on andmestikus ja kuidas neid kasutatakse</li></ul>`;
</script>

<Leht
	title="Teadmine"
	desc="Kust iga number Pidurdusmaa.ee lehel tuleb — mudel, EL-i rehvimärgis ja sõltumatud testid."
	path="teadmine/"
	crumbs={[["Teadmine", "/teadmine/"]]}
	lapsed={[["Pidurdusteekond ja peatumisteekond", "/teadmine/pidurdusteekond-ja-peatumisteekond/"], ["Kuidas pidurdusmaa arvutatakse", "/teadmine/kuidas-pidurdusmaa-arvutatakse/"], ["EL-i rehvimärgis: mida klassid tähendavad", "/teadmine/rehvimargis/"]]}
	sisu={SISU}
/>
