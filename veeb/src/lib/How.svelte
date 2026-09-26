<script>
	/* „Kuidas pidurdusmaa arvutatakse?“ — lühike selgitus dialoogis.
	   Pikk versioon on lehel /teadmine/kuidas-pidurdusmaa-arvutatakse/.
	   Avamise ja sulgemise teeb app.js (data-how / data-how-close). */
	import { CONDS } from '$lib/util.js';
</script>

<dialog class="how" id="how" aria-labelledby="how-t">
	<div class="how-h">
		<h2 id="how-t">Kuidas arvutatakse</h2>
		<button type="button" class="how-x" data-how-close aria-label="Sulge">×</button>
	</div>
	<div class="how-b">
		<p>
			Tulemus on <strong>arvutatud hinnang</strong>, mitte laborimõõtmine. Mudel simuleerib
			pidurdust samm-sammult: rehvi haare antud kiirusel, ABS, õhutakistus, auto mass ja pidurid.
		</p>
		<h3>Andmete liigid lehel</h3>
		<div class="legend">
			<div>
				<span class="pill off">Ametlik</span><span
					>EL-i rehvimärgis (EPREL): märghaardumine, veeretakistus, müra, lume- ja jäämärk.</span
				>
			</div>
			<div>
				<span class="pill test">Sõltumatu test</span><span
					>ADAC, Tekniikan Maailma, UTAC — mõõdetud pidurdusmaad, allika ja aastaga.</span
				>
			</div>
			<div>
				<span class="pill calc">Arvutatud</span><span
					>Selle lehe mudel sinu auto, kiiruse ja teeolude jaoks.</span
				>
			</div>
			<div>
				<span class="pill"><span class="est" style="margin:0">≈</span> Tuletatud</span><span
					>Meie mudeli hinnang omadusele, mida selle rehvi kohta mõõdetud ei ole (kuivpidurdus,
					pidurdus sügavas vees, lumi, jää) — rehvitüübi keskmise järgi.</span
				>
			</div>
			<div><span class="pill">Sinu sisend</span><span>Auto, rehvimõõt, kiirus, teeolud.</span></div>
		</div>
		<h3>Eeldused</h3>
		<ul>
			{#each Object.values(CONDS) as c}
				<li><strong>{c[0]}:</strong> {c[1]}</li>
			{/each}
			<li>Uus rehv (8 mm), rõhk tehase soovituse järgi, autos juht.</li>
			<li>
				<strong>Vesiliug:</strong> sama uus rehv, aga teel on 3 mm vett (roopad, suur lomp). Tavaline
				märg tee on 1 mm.
			</li>
			<li>
				<strong>Reaktsiooniaega ei arvestata.</strong> Pidurdusmaa algab hetkest, kui pidur on põhjas.
				Reaktsioonile kulub tavaliselt umbes 1 sekund — 90 km/h juures on see veel 25 meetrit enne, kui
				auto üldse aeglustama hakkab.
			</li>
			<li>
				Auto tehasemõõdud on veebist üle kontrollitud (rehvisobivuse ja tootjate lehed) — enamasti on
				neid 2–4. Leht pakub neist levinuima, aga täpne mõõt on sinu rehvi küljel.
			</li>
			<li>Kui auto on valimata, arvutatakse tüüpilise kompaktauto järgi (VW Golf 8).</li>
		</ul>
		<h3>Täpsus</h3>
		<ul>
			<li>
				Testitud rehvidel tuleb haare mõõdetud tulemusest. Mõõdetud pidurdusmaade vastu on mudeli
				viga asfaldil keskmiselt 4,4%.
			</li>
			<li>
				Ainult märgisega rehvidel on teada ainult klass (A–E). Klassi haare ei ole vahemiku
				nominaalne keskpunkt, vaid <strong>sama klassi mõõdetud rehvide mediaan</strong> (nt A-klassi
				tavaline suverehv 1,47, A-klassi sportrehv 1,64). Sama klassi rehvid on mudelis võrdsed —
				päris elus erinevad nad ±3–4%.
			</li>
			<li>
				Kuival, lumel ja jääl ei ütle märgis midagi. Neil pindadel järjestatakse ainult testitud
				rehve.
			</li>
		</ul>
		<h3>Piirangud</h3>
		<p>Lörtsi ja kurvis pidurdamist mudel ei arvesta. Vahemik tulemuse all näitab ebakindlust.</p>
		<h3>Vastutus</h3>
		<p>
			Lehe numbrid on üldiseks teadmiseks ja rehvide võrdlemiseks. Need ei ole garantii,
			ekspertarvamus ega alus liikluses otsustamiseks — sõida alati vastavalt oludele.
			<a href="/kasutustingimused/">Kasutustingimused ja vastutus</a>
		</p>
		<p><a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Loe täielikku metoodikat →</a></p>
	</div>
</dialog>
