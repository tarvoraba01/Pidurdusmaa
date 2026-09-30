<script>
	/* Talverehvide testid hooajal 2025/26 ja 2026 sügisel — ainult avaldatud
	   absoluutsed pidurdusmaad (meie testide andmebaas):
	     Vi Bilägare 2025 lamell ja naast 235/60 R18 (Volvo XC60), 2026 naast 215/65 R17
	     (mudel/testid_ext/vi_bilagare_2025_2026.json, allikas motor.no / tyrereviews.com);
	     Tekniikan Maailma 2025 205/55 R16 ja ADAC 2025 (core.json TM25 / ADAC25).
	   Uusi teste lisame, kui nende mõõdetud meetrid on avalikud. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	const A = ARTIKLID.find((a) => a.slug === 'talverehvide-testid-2026');
	const R = (s, n) => `<a href="/rehvid/${s}/">${n}</a>`;

	const SISU = `<p><strong>Talverehvide testid näitavad igal sügisel sama pilti:</strong> lumel on head ja keskmised rehvid peaaegu võrdsed, aga jääl ja märjal asfaldil võib vahe olla mitu autopikkust. Kogusime kokku viimaste testide <em>mõõdetud</em> pidurdusmaad — ainult meetrid, mitte punktid ega hinded.</p>

<h2>Jää: kõige suurem vahe</h2>
<p><strong>Vi Bilägare 2026, naastrehvid 215/65 R17</strong> (VW Tiguan): 25 km/h pealt 5 km/h-ni pidurdas parim ${R('bridgestone-blizzak-spike-3', 'Bridgestone Blizzak Spike 3')} <strong>8,3 meetriga</strong>, halvim ${R('kumho-wintercraft-ice-wi32', 'Kumho WinterCraft Ice Wi32')} <strong>17,6 meetriga</strong> — rohkem kui kaks korda pikemalt. Blizzak Spike 3 kõrvaldati küll pingereast, sest naelad ulatusid lubatust kaugemale.</p>
<p><strong>Vi Bilägare 2025, naastrehvid 235/60 R18</strong> (Volvo XC60): parim ${R('nokian-hakkapeliitta-10', 'Nokian Hakkapeliitta 10 SUV')} 11,5 m, odavaim Triangle IceLynk TI501 aga <strong>25,5 m</strong>. Sama Triangle oli märjal asfaldil hoopis parim — üks rehv võib ühes olus hiilata ja teises olla ohtlik.</p>
<p><strong>Tekniikan Maailma 2025</strong> (205/55 R16, VW Golf): 50 km/h pealt jääl peatus parim naastrehv 32,3 meetriga, halvim lamellrehv 53,5 meetriga. Vahe on <strong>21 meetrit</strong>.</p>

<h2>Lumi: vahed on väikesed</h2>
<p>Tallatud lumel olid parima ja halvima vahed kõigis kolmes Vi Bilägare testis alla meetri (35 km/h pealt 5 km/h-ni). Hea talverehv on lumel hea — aga see ei ütle midagi selle kohta, kuidas ta jääl või märjal asfaldil pidurdab.</p>

<h2>Märg asfalt: sama oluline kui jää</h2>
<p><strong>ADAC 2025</strong> (Kesk-Euroopa talverehvid): märjal asfaldil 80 km/h pealt peatus parim ${R('goodyear-ultragrip-performance-3', 'Goodyear UltraGrip Performance 3')} 31,7 meetriga, halvim ${R('syron-everest-2', 'Syron Everest 2')} 47,1 meetriga — <strong>15 meetrit vahet</strong>. Syron oli samas testis lumel ja jääl parim, jälle üks rehv, mis hiilgab ühes ja kukub läbi teises.</p>
<p>Põhjamaade testides oli märja asfaldi vahe 100 km/h pealt 7–9 meetrit. Eestis on talvel palju märga ja nullilähedast teed, nii et see number loeb.</p>

<h2>Mida sellest järeldada</h2>
<ul>
<li><strong>Vaata jää ja märja tulemust</strong>, mitte ainult lund ega kogupunkte.</li>
<li><strong>Odav naastrehv ei ole automaatselt jääl hea</strong> — halvimad naastrehvid pidurdasid jääl kehvemini kui head lamellrehvid.</li>
<li>Kui sõidad peamiselt linnas ja maanteel, on märja asfaldi tulemus sama tähtis kui jää.</li>
</ul>
<p>Iga testitud rehvi mõõdetud tulemused on rehvi lehel, näiteks ${R('continental-vikingcontact-8', 'Continental VikingContact 8')} või ${R('pirelli-ice-zero-2', 'Pirelli Ice Zero 2')}. Oma auto ja rehviga saad pidurdusmaa arvutada <a href="/">kalkulaatoris</a>.</p>

<h2>Mis on veel tulemas</h2>
<p>2026. aasta sügisel on ilmunud ka <strong>ADAC</strong> (185/65 R15 ja 225/50 R17) ja <strong>Tekniikan Maailma</strong> (205/55 R16) talvetestid. Lisame nende pidurdusmaad andmebaasi ja siia artiklisse, kui mõõdetud meetrid on avalikud.</p>
<p class="note">Allikad: Vi Bilägare / Motor (NAF), Tekniikan Maailma, ADAC. Numbrid nii, nagu need on avaldatud; testid on tehtud eri autode, mõõtude ja tingimustega, nii et eri testide meetreid omavahel otse võrrelda ei saa.</p>`;
</script>

<Leht
	title={A.title}
	desc={A.desc}
	path="teadmine/artiklid/talverehvide-testid-2026/"
	crumbs={[['Teadmine', '/teadmine/'], ['Artiklid', '/teadmine/artiklid/'], [A.title, '/teadmine/artiklid/talverehvide-testid-2026/']]}
	uuendatud={A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/talverehvide-testid-2026.png"
	sisu={SISU}
/>
