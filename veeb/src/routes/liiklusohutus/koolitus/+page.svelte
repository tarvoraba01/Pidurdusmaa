<script>
	/* Koolitus autokoolidele ja kõigile: eeltest → selgitused + simulaator → järeltest.
	   Esialgu noindex: küsimused on ülevaatamisel (dokument „Pidurdusmaa koolitus — küsimustik“). */
	import Meta from '$lib/Meta.svelte';
	import LiiklusLeht from '$lib/LiiklusLeht.svelte';

	const KIRJ = 'Kontrolli, mida tead pidurdusteekonnast, rehvidest ja libedast teest. Eeltest, selgitused, simulaatorid ja järeltest uute küsimustega.';
</script>

<Meta title="Koolitus: kui hästi sa tunned pidurdamist?" desc={KIRJ} path="liiklusohutus/koolitus/" noindex />

<LiiklusLeht kick="Liiklusohutus · koolitus" h1="Kui hästi sa tunned pidurdamist?" lead="Mis sa arvad, siis vaata, kuidas päriselt on. Iga vale vastuse olukorda saad simulaatoris ise proovida." vaade="koolitus">
	<div>
		<h2>Kuidas see töötab</h2>
		<p>Eeltestis vastad ilma vihjeteta. Siis näed iga küsimuse juures õiget vastust, selgitust ja linki simulaatorisse, kus saad sama olukorda ise proovida. Järeltestis on uued küsimused samadel teemadel, osa neist trikiga.</p>
	</div>
	<div>
		<h2>Kust arvud tulevad</h2>
		<p>Kõik arvud on arvutatud sama mudeliga, mis lehe kalkulaator: VW Golf 8, keskmine rehv, reaktsioon 1 sekund. Nähtavuse kaugused pimedas on Transpordiameti andmed.</p>
	</div>
	<div>
		<h2>Autokoolidele</h2>
		<p>Autokool saab oma koodi. Õpilased avavad lingi koodiga ja kool näeb grupi tulemusi enne ja pärast, ilma õpilaste nimedeta. Küsi koodi: <a href="/kontakt/">kontakt</a>.</p>
	</div>
</LiiklusLeht>
