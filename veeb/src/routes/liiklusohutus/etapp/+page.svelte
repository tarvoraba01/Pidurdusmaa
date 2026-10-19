<script>
	/* Päeva etapp: võidusõit aja peale, õpetlik (vt $lib/Etapp.svelte). Ainult eesti keeles. */
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import Etapp from '$lib/Etapp.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = 'Tasuta sõidumäng: iga päev uus etapp, sõida aja peale finišisse. Teele tuleb ootamatult põder, jäälaik või lomp. Haare ja pidurdusmaa on samast mudelist mis kalkulaatoris.';
	const jsonld = graph(tooriist('Päeva etapp: sõidumäng', '/liiklusohutus/etapp/', KIRJ, 'et'), ORG);
</script>

<Meta title="Päeva etapp: sõidumäng, iga päev uus rada" desc={KIRJ} path="liiklusohutus/etapp/" {jsonld} image="/og/sait/liiklus-reaktsioon.png" />

<LiiklusLeht Tool={Etapp} kick="Liiklusohutus · mäng" h1="Päeva etapp" lead="Iga päev uus rada, ilm ja teekate. Vali rehvid, sõida finišisse ja vaata, mis juhtub, kui kiirus on teeoludele liiga suur." vaade="reaktsioon">
	<div>
		<h2>Kuidas see töötab</h2>
		<p>Haare tuleb samast mudelist mis pidurdusmaa kalkulaatoris: teekate, temperatuur ja rehvi tüüp. Kurvis jagub sama haare pidurdamise ja pööramise vahel, nii et kurvis pidurdades jääb pööramiseks vähem. Kurvi piirkiirus kasvab raadiusega: kaks korda laiemas kurvis on see umbes 1,4 korda suurem.</p>
	</div>
	<div>
		<h2>Takistused</h2>
		<p>Põder või metssiga astub teele päeval umbes 55 kuni 110 m ees, pimedas paistab ta lähitulede valgel alles 45 kuni 60 m pealt. Jäälaik ja sügav lomp on teel ootamatult. Avarii korral alustad eelmisest kontrollpunktist ja näed, mis kiirusega oleks jõudnud peatuda.</p>
	</div>
	<div>
		<h2>Teised mängud</h2>
		<ul>
			<li><a href="/liiklusohutus/reaktsioon/">Kui kiiresti sina pidurdad?</a></li>
			<li><a href="/liiklusohutus/kurv/">Pidurdamine kurvis</a></li>
			<li><a href="/liiklusohutus/pimedas/">Nähtavus pimedas</a></li>
		</ul>
	</div>
</LiiklusLeht>
