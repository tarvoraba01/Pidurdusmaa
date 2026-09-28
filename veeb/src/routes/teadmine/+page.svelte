<script>
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID, artikliTee } from '$lib/artiklid.js';
	const esc = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;');
	const SISU =
		`<p>Pidurdusmaa.ee näitab arvutatud pidurdusmaad ja rehvide päris omadusi. Siin on kirjas, kust iga number tuleb ja mida me <strong>ei</strong> tea.</p>
<h2>Artiklid</h2>
<p>Praktilised juhendid rehvi valimiseks — numbritega.</p>
<ul>` +
		ARTIKLID.slice(0, 5).map((a) => `<li><a href="${artikliTee(a)}">${esc(a.title)}</a></li>`).join('') +
		`</ul>
<p><a href="/teadmine/artiklid/">Kõik artiklid →</a></p>
<h2>Kuidas leht töötab</h2>
<ul><li><a href="/teadmine/pidurdusteekond-ja-peatumisteekond/">Pidurdusteekond ja peatumisteekond</a> — valem, näited eri kiirustel ja reaktsiooniaja mõju</li><li><a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a> — mudel, eeldused, täpsus ja piirangud</li><li><a href="/teadmine/rehvimargis/">EL-i rehvimärgis</a> — mida märghaardumise, veeretakistuse ja müra klass tähendavad</li><li><a href="/testid/">Sõltumatud testid</a> — millised testid on andmestikus ja kuidas neid kasutatakse</li><li><a href="/teadmine/partnerid/">Partnerid ja poelingid</a> — kuidas leht tasuta püsib ja miks see järjestust ei mõjuta</li></ul>`;
</script>

<Leht
	title="Teadmine"
	desc="Artiklid rehvi valimiseks ja kust iga Pidurdusmaa.ee number tuleb — mudel, EL-i rehvimärgis ja sõltumatud testid."
	path="teadmine/"
	crumbs={[["Teadmine", "/teadmine/"]]}
	lapsed={[["Artiklid", "/teadmine/artiklid/"], ["Pidurdusteekond ja peatumisteekond", "/teadmine/pidurdusteekond-ja-peatumisteekond/"], ["Kuidas pidurdusmaa arvutatakse", "/teadmine/kuidas-pidurdusmaa-arvutatakse/"], ["EL-i rehvimärgis: mida klassid tähendavad", "/teadmine/rehvimargis/"]]}
	sisu={SISU}
/>
