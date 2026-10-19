<script>
	/* Päeva etapp: võidusõit aja peale, õpetlik (vt $lib/Etapp.svelte). Ainult eesti keeles. */
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';
	import Etapp from '$lib/Etapp.svelte';
	import { ORG, graph, tooriist } from '$lib/skeem.js';

	const KIRJ = 'Tasuta 3D kruusaralli brauseris: iga päev uus etapp metsateel, sõida aja peale ja drifti kurvides. Kaardilugeja näitab kurve, pidurdus tuleb pidurdusmaa kalkulaatori mudelist.';
	const jsonld = graph(tooriist('Päeva etapp: kruusaralli', '/liiklusohutus/etapp/', KIRJ, 'et'), ORG);
</script>

<Meta title="Päeva etapp: kruusaralli, iga päev uus rada" desc={KIRJ} path="liiklusohutus/etapp/" {jsonld} noindex image="/og/sait/liiklus-reaktsioon.png" />

<LiiklusLeht Tool={Etapp} kick="Mäng · ralli" h1="Päeva etapp" lead="Kruusaralli aja peale. Iga päev uus rada, kõigile sama. Kui kiiresti sina selle läbi sõidad?" vaade="reaktsioon">
	<div>
		<h2>Kuidas sõita</h2>
		<p>Auto läheb sinna, kuhu rooli keerad. Järsu kurvi ees pidurda enne kurvi, mitte kurvis. Driftimiseks tõmba kurvis käsipidurit (tühik): tagaots tuleb välja, gaas hoiab drifti ja vasturool toob auto sirgeks. Kaardilugeja number näitab kurvi järsust, 1 on kõige järsem ja 6 peaaegu sirge.</p>
	</div>
	<div>
		<h2>Mis on päris</h2>
		<p>Pidurdusjõud ja haare kruusal tulevad samast mudelist mis pidurdusmaa kalkulaatoris. Kui sõidad kurvi liiga kiiresti ja teelt välja lähed, näitab mäng, mis on selle kurvi piirkiirus kruusal.</p>
	</div>
	<div>
		<h2>Veel mänge</h2>
		<ul>
			<li><a href="/liiklusohutus/reaktsioon/">Kui kiiresti sina pidurdad?</a></li>
			<li><a href="/liiklusohutus/kurv/">Pidurdamine kurvis</a></li>
		</ul>
	</div>
</LiiklusLeht>
