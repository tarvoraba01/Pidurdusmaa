<script>
	import Leht from '$lib/Leht.svelte';
	const SISU = `<p>Kalkulaator <strong>arvutab</strong> pidurdusmaa. See ei ole laborimõõtmine ega lubadus, et sinu auto peatub täpselt selle meetri pealt. Tulemus on hinnang, millel on alati veapiir, ja leht näitab seda veapiiri iga tulemuse juures.</p>
<h2>Mida mudel teeb</h2>
<p>Pidurdus simuleeritakse väikeste ajasammudega: iga hetk arvutatakse rehvi ja tee vaheline haare antud kiirusel, ABS-i tõhusus, õhutakistus, veeretakistus, kalle ja pidurite võimekus. Haare sõltub kiirusest (märjal kukub ta kiiruse kasvades rohkem kui kuival), temperatuurist ja rehvi kategooriast.</p>
<h2>Kust tuleb rehvi haare</h2>
<ul><li><strong>Märjal</strong> tuleb haare EL-i rehvimärgise märghaardumise indeksist. Indeks on ametliku UNECE R117 katse tulemus (märg asfalt, 80 → 20 km/h, võrdlusrehvi suhtes). Mudel teisendab selle haardeks ühe kordajaga, mis on sobitatud 85 mõõdetud märja pidurdusmaa vastu.</li><li><strong>Sõltumatult testitud rehvidel</strong> on indeks tuletatud testi enda mõõdetud märjast pidurdusmaast — see on täpsem kui märgise klass.</li><li><strong>Ainult märgisega rehvidel</strong> on teada ainult klass (A–E), mitte täpne number. Mudel kasutab klassi keskpunkti ja lisab veapiirile ±4,5%. Mõõtsime järele: mõõdetud rehvide hajuvus ühe klassi sees oli 2,4–3,9%.</li><li><strong>Kuival, lumel ja jääl</strong> ei ütle märgis midagi. Testitud rehvidel kasutatakse testi tulemust, teistel rehvi kategooria keskmist. Seetõttu ei järjesta leht ainult märgisega rehve kuival, lumel ega jääl — nad oleksid kõik võrdsed ja see näeks välja nagu teadmine, mida meil ei ole.</li></ul>
<h2>Teeolud kalkulaatoris</h2>
<p>Kalkulaatoris valid ühe neljast teeolust. Iga valiku taga on kindel teepind ja temperatuur:</p>
<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr><th>Teeolu</th><th>Teepind</th><th class="n">Temperatuur</th></tr></thead><tbody><tr><td><strong>Märg</strong></td><td>Asfalt, 1 mm veekiht</td><td class="n">+10 °C</td></tr><tr><td><strong>Kuiv</strong></td><td>Asfalt</td><td class="n">+15 °C</td></tr><tr><td><strong>Lumi</strong></td><td>Tallatud lumi</td><td class="n">−5 °C</td></tr><tr><td><strong>Jää</strong></td><td>Jääkate</td><td class="n">−5 °C</td></tr></tbody></table></div>
<p>Rehv on uus (mustrisügavus 8 mm), rõhk tehase soovituse järgi, autos juht (75 kg). Pidurdusmaa algab hetkest, kui pidur on põhjas — reaktsiooniaega ei arvestata, sest see tuleb inimesest, mitte rehvist.</p>
<h2>Kui täpne see on</h2>
<ul><li>369 mõõdetud pidurdusmaa vastu (ADAC, Tekniikan Maailma, UTAC) on mudeli jääkviga asfaldil (märg ja kuiv) 4,4%, betoonil 6,6%, lumel 5,5%, jääl 6,9%.</li><li>Kontroll testidega, mida mudel kunagi ei näinud (Vi Bilägare 2010, teine mõõt ja teised kiirused): kuival 3,2–5,7%.</li><li>Iga tulemuse juures on vahemik. Vaikimisi näidatakse keskmist hinnangut.</li></ul>
<h2>Piirangud</h2>
<ul><li>Kummisegu. Parimate rehvide vahe märjal on umbes 17%, ja see tuleb peamiselt segust, mida tootjad ei avalda.</li><li>Lörtsi, märga või külmunud kruusa ja kurvis pidurdamist.</li><li>Rehvide järjestust lumel ja jääl, kui rehv ei ole testitud.</li></ul>
<h2>Andmete liigid</h2>
<ul><li><strong>Ametlik</strong> — EL-i tooteregister EPREL (rehvimärgis).</li><li><strong>Sõltumatu test</strong> — ajakirja või autoklubi mõõdetud tulemus, allika ja aastaga.</li><li><strong>Arvutatud hinnang</strong> — selle lehe mudel.</li><li><strong>Sinu sisend</strong> — auto, kiirus, teeolud.</li></ul>`;
</script>

<Leht
	title="Kuidas pidurdusmaa arvutatakse"
	desc="Mudel, eeldused, täpsus ja piirangud: kuidas Pidurdusmaa.ee pidurdusmaa arvutab ja kui täpne see on."
	path="teadmine/kuidas-pidurdusmaa-arvutatakse/"
	crumbs={[["Teadmine", "/teadmine/"], ["Kuidas pidurdusmaa arvutatakse", "/teadmine/kuidas-pidurdusmaa-arvutatakse/"]]}
	lapsed={[]}
	uuendatud="2026-09-25"
	sisu={SISU}
/>
