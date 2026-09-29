<script>
	/* Uue kalkulaatori (/liiklusohutus/) tutvustus. Lühike, jagamiseks (FB).
	   Numbrid: sama mootor ja eeldused mis kalkulaatoris (tüüpiline kompaktauto,
	   C-klassi suverehv, uus muster, reaktsiooniaeg 1 s; märg asfalt 1 mm +10 °C,
	   kuiv +15 °C, tallatud lumi −5 °C). Arvutatud 2026-09-29. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	const A = ARTIKLID.find((a) => a.slug === 'peatumisteekonna-kalkulaator');

	const K = '/liiklusohutus/';
	const SISU = `<p><strong>Kui pika maa pealt auto peatub?</strong> Uue tasuta kalkulaatoriga saad seda ise järele proovida: muuda kiirust, reaktsiooniaega, teeolusid ja rehve ning vaata kohe, kuidas peatumisteekond muutub. Pane kaks olukorda kõrvuti ja näed, millise kiirusega jõuab auto sinna, kus teine juba seisab.</p>
<p><a class="btn yel" href="${K}">Ava kalkulaator →</a></p>

<h2>Mida sellega teha saab</h2>
<ul>
<li><strong>Kiirus ja reaktsiooniaeg</strong> — näed eraldi, kui palju sõidab auto enne pidurdamist ja kui palju pidurdades.</li>
<li><strong>Teeolud</strong> — kuiv, märg või lompidega asfalt, betoon, kruus, lumi ja jää, teepinna temperatuur ja tee kalle.</li>
<li><strong>Rehvid</strong> — suve-, aastaringne, talve- või naastrehv, EL-i märgise märghaarde klass, mustrisügavus, vanus ja rõhk.</li>
<li><strong>Auto</strong> — tüüpauto või sinu enda mark ja mudel, ABS, koormus ja pidurite seisukord.</li>
<li><strong>Kaks olukorda kõrvuti</strong> ja takistus tee peal: kas auto jõuab peatuda või millise kiirusega ta sinna jõuab.</li>
<li><strong>Jagatav link</strong> — kõik valikud salvestuvad aadressi. Esitlusrežiim näitab kalkulaatorit suurelt ekraanil.</li>
</ul>

<h2>Kolm näidet</h2>
<p><strong>50 või 70 km/h.</strong> Märjal teel peatub auto 50 km/h pealt umbes <strong>28 meetriga</strong>, 70 km/h pealt <strong>47 meetriga</strong>. Kohas, kus aeglasem auto juba seisab, sõidab kiirem veel <strong>61 km/h</strong>. <a href="${K}#b=1&amp;b.kiirus=70&amp;takistus=29">Vaata kalkulaatoris</a></p>
<p><strong>Tähelepanelik või hajevil juht.</strong> Kuival teel 50 km/h pealt peatub 1-sekundilise reaktsiooniajaga juht 24 meetriga. 2-sekundilise reaktsiooniajaga juht jõuab samasse kohta veel täiskiirusel — ta pole pidurit veel vajutanudki. <a href="${K}#vesi=0&amp;temp=15&amp;b=1&amp;b.vesi=0&amp;b.temp=15&amp;b.reakt=2">Vaata kalkulaatoris</a></p>
<p><strong>Suverehv lumel.</strong> Tallatud lumel 50 km/h pealt peatub auto talverehvidega umbes <strong>41 meetriga</strong>, suverehvidega <strong>77 meetriga</strong>. <a href="${K}#kat=WINTER_NORDIC&amp;pind=SNOW_PACKED&amp;temp=-5&amp;b=1&amp;b.pind=SNOW_PACKED&amp;b.temp=-5">Vaata kalkulaatoris</a></p>

<h2>Millal kasutada</h2>
<ul>
<li>Autokoolis ja liiklusohutuse tunnis — valmis võrdlused on ühe klikiga olemas.</li>
<li>Enne rehvivahetust — kui palju muudab kulunud muster või vale rehv.</li>
<li>Kui tahad lihtsalt aru saada, miks kiirusepiirang ja pikivahe on just sellised.</li>
</ul>

<h2>Kuidas see arvutab</h2>
<p>Arvutus on sama, mis Pidurdusmaa.ee kalkulaatoris: mudel on kalibreeritud sõltumatute rehvitestide mõõdetud pidurdusmaade järgi ja iga tulemuse juures on tõenäoline vahemik. Tulemus on hinnang, mitte mõõtmine. Lähemalt: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">kuidas pidurdusmaa arvutatakse</a>.</p>
<p>Kalkulaator on tasuta ja ilma reklaamita. Kasuta ja jaga vabalt.</p>`;
</script>

<Leht
	title={A.title}
	desc={A.desc}
	path="teadmine/artiklid/peatumisteekonna-kalkulaator/"
	crumbs={[['Teadmine', '/teadmine/'], ['Artiklid', '/teadmine/artiklid/'], [A.title, '/teadmine/artiklid/peatumisteekonna-kalkulaator/']]}
	uuendatud={A.kuupaev}
	avaldatud={A.kuupaev}
	image="/og/sait/peatumisteekonna-kalkulaator.png"
	sisu={SISU}
/>
