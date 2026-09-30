<script>
	import Leht from '$lib/Leht.svelte';
	import { GA4_ID } from '$lib/seaded.js';

	/* Privaatsusteade. Kirjelda ainult seda, mida sait PÄRISELT teeb —
	   kui lisandub uus teenus (hinnad, uudiskiri, reklaam), tuleb see
	   leht enne avaldamist üle vaadata. */
	const SISU = `
<p><strong>Lühidalt:</strong> me ei küsi sinu nime ega e-posti, kui sa ise kontaktivormi ei täida. Statistikat kogume kolmel viisil: oma serveris ilma küpsisteta (lehe kasutus ja Plausible) ning — ainult sinu nõusolekul — Google Analyticsiga. Reklaami ei näita ja andmeid ei müü.</p>
<p><em>Viimati uuendatud 30.09.2026.</em></p>

<h2>Kes vastutab</h2>
<p>Pidurdusmaa.ee, Rabarvo OÜ. Küsimused ja taotlused: <a href="/kontakt/">kontaktivorm</a> või rabarvo@hotmail.com.</p>

<h2>1. Kasutusstatistika ilma küpsisteta (alati)</h2>
<p>Kui kasutad lehte, saadab brauser meie serverisse lühikesed teated selle kohta, <em>mida lehel tehti</em>: milline automudel ja rehvimõõt valiti, mis kiirusel arvutati, mida otsiti, millised rehvid võrdlusse lisati. Nii näeme, millised osad on kasulikud ja mis ei tööta.</p>
<ul>
<li>Nime, e-posti ega küpsist selle juures <strong>ei ole</strong>.</li>
<li>Sinu IP-aadressi ei salvestata. Sellest arvutatakse räsi (pöördumatu lühend) juhusliku soolaga, mis on olemas ainult ühe päeva ja siis kustutatakse. Nii näeme, millised sündmused kuulusid samale külastusele, ja hoiame ära, et üks masin serverit üle ei ujutaks. Pärast päeva lõppu ei saa ka meie ise ühtki rida kellegi IP-ga seostada ega eri päevade külastusi kokku viia.</li>
<li>Selle jaoks ei kirjutata sinu brauserisse midagi.</li>
<li>Alus: õigustatud huvi teenust parandada. Kuna read on anonüümsed, hoiame neid pikemat aega, et näha, kuidas lehe kasutus aastate jooksul muutub.</li>
</ul>
<p>Külastuste koondstatistika (mitu külastust, millistelt lehtedelt, mis riigist, millise seadmega) tuleb <strong>Plausible</strong>'ist, mis töötab meie enda serveris (track.pidurdusmaa.ee), mitte kolmanda osapoole juures. Plausible ei kasuta küpsiseid, ei salvesta IP-aadressi ega jälgi sind teistel lehtedel: külastaja eristamiseks kasutab ta räsi, mis vahetub iga päev. Lisaks loendab ta mõnda tegevust (näiteks arvutus, valitud automudel, otsingusõna, klikk poe lingile) koondnumbritena. Alus: õigustatud huvi.</p>

<h2>2. Google Analytics (ainult nõusolekul)</h2>
<p>Kui vajutad küpsiste ribal „Nõustun“, laetakse Google Analytics 4. Enne seda ei tehta Google'isse ühtegi päringut. Google Analytics paneb brauserisse küpsised <code>_ga</code> ja <code>_ga_…</code> (säilivad kuni 2 aastat) ning näitab meile koondstatistikat: mitu külastajat, millistelt lehtedelt, millise seadmega, mis riigist.</p>
<ul>
<li>Töötleja on Google Ireland Ltd. Andmed võivad liikuda USA-sse EL–USA andmeraamistiku alusel.</li>
<li>Google Analytics 4 ei salvesta IP-aadressi.</li>
<li>Reklaamiküpsiseid ja reklaami isikupärastamist ei kasutata.</li>
<li>Alus: sinu nõusolek. Saad selle igal ajal tagasi võtta jaluses „Küpsiste seaded“ — siis GA küpsised kustutatakse.</li>
</ul>

<h2>3. Kontaktivorm</h2>
<p>Kui kirjutad meile, saame sinu nime, e-posti, soovi korral ettevõtte nime ja sõnumi. Kasutame neid ainult sulle vastamiseks ega lisa sind ühelegi listile. Kiri jõuab meieni e-postiga (Google Gmail) ja koopia jääb meie serverisse, et ükski kiri kaotsi ei läheks. Kontaktivormi kaitseb rämpsposti eest Cloudflare Turnstile: see kontrollib vormi saatmisel, et tegu on inimese ja päris brauseriga, ning saab selleks sinu IP-aadressi ja brauseri tehnilised andmed. Turnstile ei kasuta reklaamiküpsiseid ega jälgi sind teistel lehtedel. Turnstile laetakse ainult kontaktilehel. Serveris olev koopia kustub automaatselt 12 kuu pärast; e-postkastist kustutame kirja hiljemalt 12 kuud pärast suhtluse lõppu. Alus: sinu pöördumine (vastamine sinu soovile).</p>

<h2>4. Poelingid</h2>
<p>Kui vajutad rehvi juures poe lingile, lahkud Pidurdusmaa.ee-lt. Osa linke käib läbi partnerivõrgustiku (näiteks Awin). Siis võivad partnerivõrgustik ja pood panna oma küpsise, et müük meile arvestataks — see on nende töötlus ja nende privaatsustingimuste järgi. Meie ei saa sinu kohta isikuandmeid: näeme ainult koondina, mitu klikki ja ostu partnerite kaudu tuli. Kuidas partnerid lehe tasuta hoiavad: <a href="/teadmine/partnerid/">Partnerid ja poelingid</a>.</p>

<h2>5. Mida su brauser meelde jätab</h2>
<ul>
<li><strong>Valitud auto, ABS-i valik, võrdluskorv ja peatumisteekonna seaded</strong> (reaktsiooniaeg) ning lehe kerimiskoht — ainult selle vahelehe ajaks (<code>sessionStorage</code>), et need lehtede vahel liikudes alles oleksid. Kaob vahelehe sulgemisel.</li>
<li><strong>Liiklusohutuse kalkulaatori valikud</strong> on ainult lehe aadressis (pärast #-märki), et linki saaks jagada. Seda osa brauser serverisse ei saada.</li>
<li><strong>Sinu küpsiste valik</strong> (<code>localStorage</code>), et riba ei küsiks iga kord uuesti.</li>
</ul>
<p>Need on lehe toimimiseks vajalikud ega saada midagi kellelegi.</p>

<h2>6. Sinu õigused</h2>
<p>Võid küsida, milliseid andmeid meil sinu kohta on, ja nõuda nende parandamist või kustutamist. Kasutusstatistika on anonüümne (nime, e-posti ega IP-d pole), seega seda ei saa inimese järgi välja otsida. Kui arvad, et oleme sinu andmeid valesti töödelnud, võid pöörduda <a href="https://www.aki.ee" rel="noopener">Andmekaitse Inspektsiooni</a>.</p>

<h2>7. Muudatused</h2>
<p>Kui lehele lisandub uus teenus, mis andmeid kasutab, uuendame seda teadet enne selle kasutuselevõttu.</p>
`;
</script>

<Leht
	title="Privaatsus ja küpsised"
	desc="Mida Pidurdusmaa.ee kogub: küpsisteta kasutusstatistika, Google Analytics ainult nõusolekul, kontaktivormi andmed. Reklaami ei näita ja andmeid ei müü."
	path="privaatsus/"
	crumbs={[['Privaatsus ja küpsised', '/privaatsus/']]}
	sisu={SISU}
/>

{#if GA4_ID}
	<div class="wrap" style="padding-bottom:var(--sp-12)">
		<button type="button" class="btn" onclick={() => window.PM_KUPSISED?.()}>Muuda küpsiste valikut</button>
	</div>
{/if}
