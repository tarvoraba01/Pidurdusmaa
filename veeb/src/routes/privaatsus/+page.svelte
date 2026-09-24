<script>
	import Leht from '$lib/Leht.svelte';
	import { GA4_ID } from '$lib/seaded.js';

	/* Privaatsusteade. Kirjelda ainult seda, mida sait PÄRISELT teeb —
	   kui lisandub uus teenus (hinnad, uudiskiri, reklaam), tuleb see
	   leht enne avaldamist üle vaadata. */
	const SISU = `
<p><strong>Lühidalt:</strong> me ei küsi sinu nime ega e-posti, kui sa ise kontaktivormi ei täida. Statistikat kogume kahel viisil: anonüümselt oma serveris ja — ainult sinu nõusolekul — Google Analyticsiga. Reklaami ei näita ja andmeid ei müü.</p>

<h2>Kes vastutab</h2>
<p>Pidurdusmaa.ee, Rabarvo OÜ. Küsimused ja taotlused: <a href="/kontakt/">kontaktivorm</a> või rabarvo@hotmail.com.</p>

<h2>1. Anonüümne kasutusstatistika (alati)</h2>
<p>Kui kasutad lehte, saadab brauser meie serverisse lühikesed teated selle kohta, <em>mida lehel tehti</em>: milline automudel ja rehvimõõt valiti, mis kiirusel arvutati, mida otsiti, millised rehvid võrdlusse lisati. Nii näeme, millised osad on kasulikud ja mis ei tööta.</p>
<ul>
<li>Nime, e-posti ega küpsist selle juures <strong>ei ole</strong>.</li>
<li>IP-aadressist hoitakse ainult soolatud räsi (pöördumatu lühend), et üks masin ei saaks serverit üle ujutada. Sinu IP-d ennast ei salvestata.</li>
<li>Midagi ei kirjutata sinu brauserisse.</li>
<li>Alus: õigustatud huvi teenust parandada. Andmeid hoitakse kuni 12 kuud.</li>
</ul>

<h2>2. Google Analytics (ainult nõusolekul)</h2>
<p>Kui vajutad küpsiste ribal „Nõustun“, laetakse Google Analytics 4. Enne seda ei tehta Google'isse ühtegi päringut. Google Analytics paneb brauserisse küpsised <code>_ga</code> ja <code>_ga_…</code> (säilivad kuni 2 aastat) ning näitab meile koondstatistikat: mitu külastajat, millistelt lehtedelt, millise seadmega, mis riigist.</p>
<ul>
<li>Töötleja on Google Ireland Ltd. Andmed võivad liikuda USA-sse EL–USA andmeraamistiku alusel.</li>
<li>Google Analytics 4 ei salvesta IP-aadressi.</li>
<li>Reklaamiküpsiseid ja reklaami isikupärastamist ei kasutata.</li>
<li>Alus: sinu nõusolek. Saad selle igal ajal tagasi võtta jaluses „Küpsiste seaded“ — siis GA küpsised kustutatakse.</li>
</ul>

<h2>3. Kontaktivorm</h2>
<p>Kui kirjutad meile, saame sinu nime, e-posti, soovi korral ettevõtte nime ja sõnumi. Kasutame neid ainult sulle vastamiseks ega lisa sind ühelegi listile. Kiri jõuab meieni e-postiga (Google Gmail). Kontaktivormi kaitseb rämpsposti eest Cloudflare Turnstile: see kontrollib vormi saatmisel, et tegu on inimese ja päris brauseriga, ning saab selleks sinu IP-aadressi ja brauseri tehnilised andmed. Turnstile ei kasuta reklaamiküpsiseid ega jälgi sind teistel lehtedel. Turnstile laetakse ainult kontaktilehel. Kiri hoitakse kuni 12 kuud pärast suhtluse lõppu.</p>

<h2>4. Mida su brauser meelde jätab</h2>
<ul>
<li><strong>Valitud auto ja võrdluskorv</strong> — ainult selle vahelehe ajaks (<code>sessionStorage</code>), et need lehtede vahel liikudes alles oleksid. Kaob vahelehe sulgemisel.</li>
<li><strong>Sinu küpsiste valik</strong> (<code>localStorage</code>), et riba ei küsiks iga kord uuesti.</li>
</ul>
<p>Need on lehe toimimiseks vajalikud ega saada midagi kellelegi.</p>

<h2>5. Sinu õigused</h2>
<p>Võid küsida, milliseid andmeid meil sinu kohta on, ja nõuda nende parandamist või kustutamist. Anonüümset statistikat ei saa inimese järgi eristada, seega seda ei saa ka kellegi kohta välja otsida. Kui arvad, et oleme sinu andmeid valesti töödelnud, võid pöörduda <a href="https://www.aki.ee" rel="noopener">Andmekaitse Inspektsiooni</a>.</p>

<h2>6. Muudatused</h2>
<p>Kui lehele lisandub uus teenus, mis andmeid kasutab, uuendame seda teadet enne selle kasutuselevõttu.</p>
`;
</script>

<Leht
	title="Privaatsus ja küpsised"
	desc="Mida Pidurdusmaa.ee kogub: anonüümne kasutusstatistika, Google Analytics ainult nõusolekul, kontaktivormi andmed. Reklaami ei näita ja andmeid ei müü."
	path="privaatsus/"
	crumbs={[['Privaatsus ja küpsised', '/privaatsus/']]}
	sisu={SISU}
/>

{#if GA4_ID}
	<div class="wrap" style="padding-bottom:var(--sp-12)">
		<button type="button" class="btn" onclick={() => window.PM_KUPSISED?.()}>Muuda küpsiste valikut</button>
	</div>
{/if}
