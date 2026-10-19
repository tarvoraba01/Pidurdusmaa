<script>
	/* Päeva etapp: võidusõit aja peale, õpetlik (vt $lib/Etapp.svelte). Ainult eesti keeles. */
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import Etapp from '$lib/Etapp.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = 'Tasuta kruusaralli brauseris: iga päev uus etapp, sõida aja peale, kaardilugeja näitab kurve. Füüsika ja haare on samast mudelist mis pidurdusmaa kalkulaatoris.';
	const jsonld = graph(tooriist('Päeva etapp: kruusaralli', '/liiklusohutus/etapp/', KIRJ, 'et'), ORG);
</script>

<Meta title="Päeva etapp: kruusaralli, iga päev uus rada" desc={KIRJ} path="liiklusohutus/etapp/" {jsonld} noindex image="/og/sait/liiklus-reaktsioon.png" />

<LiiklusLeht Tool={Etapp} kick="Mäng · ralli" h1="Päeva etapp" lead="Kruusaralli aja peale. Iga päev uus rada, kõigile sama. Kui kiiresti sina selle läbi sõidad?" vaade="reaktsioon">
	<div>
		<h2>Kuidas sõita</h2>
		<p>Pidurda enne kurvi, mitte kurvis: pidur ja pööramine jagavad sama haaret. Kaardilugeja number näitab kurvi järsust, 1 on juuksenõel ja 6 peaaegu sirge. Järsus kurvis aitab käsipidur: lühike tõmme toob tagaotsa ringi.</p>
	</div>
	<div>
		<h2>Füüsika</h2>
		<p>Auto käitub nagu päris: rehvid libisevad nurga all, koormus kandub pidurdades ette, ABS hoiab rattad veerevana. Kruusa haare tuleb samast mudelist mis pidurdusmaa kalkulaatoris, nii et kurvide piirkiirused on päris omad.</p>
	</div>
	<div>
		<h2>Veel mänge</h2>
		<ul>
			<li><a href="/liiklusohutus/reaktsioon/">Kui kiiresti sina pidurdad?</a></li>
			<li><a href="/liiklusohutus/kurv/">Pidurdamine kurvis</a></li>
		</ul>
	</div>
</LiiklusLeht>
