<script>
	/* Talverehvi valimine — kõik numbrid on arvutatud sama mudeliga, mis
	   kalkulaator (engine.js), v.a. „Mudelite vahe“ lõik, mis on otse
	   Tekniikan Maailma 2025 mõõtmistest (core.json → tyres[].tests, TM25).
	   Arvutuse eeldused: VW Golf 8 1.5 TSI, 205/55 R16, uus rehv 8 mm,
	   tüüpiline märgise klass (suvi B, talv/aastaringne B, põhjamaade D),
	   lumi ja jää −5 °C, märg asfalt +10 °C, kuiv +15 °C. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	const A = ARTIKLID.find((a) => a.slug === 'talverehvi-valimine');

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Eesti talv ei ole ainult lumi. On tallatud lumi, jää, sulav jää nulli ümber ja väga palju märga asfalti. Iga rehvitüüp on mõnes neist hea ja mõnes halb. Siin on numbrid, mis aitavad valida.</p>
<p>Kui pole öeldud teisiti, on pidurdusmaad arvutatud sama mudeliga, mis <a href="/">kalkulaator</a>: VW Golf 8, rehvimõõt 205/55 R16, uued rehvid. Arvestatud on ainult pidurdusteekonda, reaktsiooniaega mitte.</p>
<div class="note-box"><strong>Lühidalt.</strong> Suverehviga pidurdab auto lumel üle kahe korra pikemalt. Jääl on suurim vahe talverehvide endi vahel: Kesk-Euroopa talverehv pidurdab jääl ligi kaks korda pikemalt kui Põhjamaade oma. Naastrehv on parim jääl, eriti nulli lähedal. Kulunud muster võtab lumel ära veerandi haardest.</div>

<h2>Suverehv talvel</h2>
<p>50 km/h pealt tallatud lumel (−5 °C) peatub auto suverehvidega <strong>60,9 meetriga</strong>, talverehvidega umbes <strong>26 meetriga</strong>. Jääl on vahe veel suurem: suverehviga 137 m, Põhjamaade talverehviga 48 m.</p>
<p>Suverehvi kumm muutub külmaga kõvaks ja muster ei ole lume jaoks tehtud. Seda ei korva ettevaatlik sõit ega ABS.</p>

<h2>Millal vahetada</h2>
<p>Seadus: <strong>talverehvid on kohustuslikud 1. detsembrist 1. märtsini</strong>. Naastrehvid on lubatud 15. oktoobrist 31. märtsini, talveoludes ka 1. oktoobrist 30. aprillini (<a href="https://www.transpordiamet.ee/uudised/transpordiamet-soovitab-ara-oota-kulmakraadide-saabumist-vaheta-rehvid-juba-tana" rel="noopener">Transpordiamet</a>).</p>
<p>Aga millal on talverehv päriselt parem? Pidurdusmaa 90 km/h pealt (talv = Põhjamaade talverehv):</p>
${tabel(
		['Temperatuur', 'Märg: suvi', 'Märg: talv', 'Kuiv: suvi', 'Kuiv: talv'],
		[
			['+10 °C', '45,6 m', '47,5 m', '31,3 m', '39,4 m'],
			['+7 °C', '47,6 m', '47,2 m', '32,7 m', '39,2 m'],
			['+5 °C', '49,1 m', '47,1 m', '33,7 m', '39,1 m'],
			['0 °C', '55,2 m', '46,6 m', '37,9 m', '38,7 m']
		]
	)}
<p><strong>Märjal teel</strong> on talverehv parem juba <strong>umbes +7 °C</strong> juures, sest suverehvi kumm hakkab kõvenema. Kuival asfaldil jääb suverehv paremaks peaaegu nullini. Eesti sügis on enamasti märg ja esimene öökülm tuleb ootamatult — vaheta, kui päevad jäävad alla +7 °C ja öösiti on külma.</p>

<h2>Põhjamaade või Kesk-Euroopa talverehv</h2>
<p>Talverehve on kaht liiki ja poes on need sageli kõrvuti. <strong>Kesk-Euroopa</strong> talverehv on tehtud märja ja lörtsise talve jaoks, <strong>Põhjamaade</strong> oma lume ja jää jaoks. Pidurdusmaa 50 km/h pealt (märg asfalt 90 km/h pealt):</p>
${tabel(
		['Rehv', 'Lumi', 'Jää', 'Märg asfalt'],
		[
			['Suverehv', '60,9 m', '137,4 m', '45,6 m'],
			['Aastaringne', '25,2 m', '84,5 m', '42,1 m'],
			['Kesk-Euroopa talverehv', '26,3 m', '92,8 m', '41,6 m'],
			['Põhjamaade talverehv (lamell)', '26,2 m', '47,6 m', '47,5 m'],
			['Naastrehv', '28,4 m', '36,7 m', '47,5 m']
		]
	)}
<p>Lumel on kõik talverehvid peaaegu võrdsed. <strong>Jääl</strong> pidurdab Kesk-Euroopa talverehv ligi kaks korda pikemalt kui Põhjamaade oma. Märjal asfaldil on Kesk-Euroopa rehv ligi 6 m parem. Eesti talvel, kus jää ja jäide on tavalised, on Põhjamaade rehv kindlam valik.</p>
<p><strong>Kuidas ära tunda:</strong> mõlemal on EL-i rehvimärgisel kolme mäetipu ja lumehelbe märk. Põhjamaade rehvil on lisaks <strong>jäämärk</strong> — see tähendab, et rehv läbis jääkatse. Transpordiamet soovitab valida jäämärgiga rehvi. Loe lähemalt: <a href="/teadmine/rehvimargis/">EL-i rehvimärgis</a>.</p>

<h2>Naastrehv või lamell</h2>
<p>Jää pidamine sõltub temperatuurist. Kõige libedam on sulav jää nulli lähedal. Pidurdusmaa jääl 50 km/h pealt:</p>
${tabel(
		['Jää temperatuur', 'Naastrehv', 'Põhjamaade lamell', 'Vahe'],
		[
			['−15 °C', '24,1 m', '31,3 m', '7 m'],
			['−5 °C', '36,7 m', '47,6 m', '11 m'],
			['0 °C', '49,4 m', '81,4 m', '32 m']
		]
	)}
<p>Naast lõikab jäässe ja ei hooli temperatuurist nii palju kui kumm. Seepärast on naastrehvi eelis suurim just nulli ümber, mis on Eesti talvel sage.</p>
<p>Lumel ja kuival asfaldil on lamell veidi parem (lumel 26,2 m vs 28,4 m) ning vaiksem. <strong>Naastrehv</strong> sobib, kui sõidad palju maanteel ja kõrvalteedel, kus jää püsib. <strong>Lamell</strong> sobib, kui sõidad peamiselt linnas ja soolatud teedel.</p>

<h2>Aastaringne rehv</h2>
<p>Lumel on aastaringne rehv hea (25,2 m), aga jääl pidurdab ta 84,5 meetriga — peaaegu sama halvasti kui Kesk-Euroopa talverehv. Eesti talveks, kus on jääd, see hea valik ei ole.</p>

<h2>Mustri sügavus</h2>
<p>Seadus lubab talverehvi, mille muster on sügavam kui 3 mm. Aga haare kaob varem. Põhjamaade talverehv, pidurdusmaa lumel ja jääl 50 km/h ning märjal 90 km/h pealt:</p>
${tabel(
		['Muster', 'Lumi', 'Jää', 'Märg asfalt'],
		[
			['8 mm (uus)', '26,2 m', '47,6 m', '47,5 m'],
			['6 mm', '28,4 m', '49,6 m', '49,5 m'],
			['4 mm', '31,1 m', '51,7 m', '52,2 m'],
			['3 mm', '32,7 m', '52,8 m', '54,0 m']
		]
	)}
<p>3 mm mustriga on pidurdusmaa lumel veerandi võrra pikem kui uuel rehvil. Mõõda mustrit enne hooaega mustrisügavuse mõõdikuga.</p>

<h2>Talverehv suvel</h2>
<p>Kevadel tasub rehvid tagasi vahetada. Kuival asfaldil +25 °C juures pidurdab suverehv 90 km/h pealt 28,6 meetriga, Põhjamaade talverehv 42,0 meetriga — 13 meetrit pikemalt.</p>

<h2>Mudelite vahe on suur</h2>
<p>Rehvitüüp ei ütle kõike. <a href="https://www.tyrereviews.com/Tyre-Tests/2025-Friction-and-Studded-Winter-Tyre-Test.htm" rel="noopener">Tekniikan Maailma 2025. aasta testis</a> (205/55 R16, jää, 50 → 0 km/h, −5 °C) mõõdeti:</p>
<ul><li><strong>Põhjamaade lamellrehvid:</strong> 45,6–53,5 m. Parima ja nõrgima vahe 7,9 m.</li><li><strong>Naastrehvid:</strong> 32,3–42,5 m. Vahe 10,2 m.</li></ul>
<p>Selles testis ei jõudnud ükski lamellrehv jääl ühegi naastrehvini. Aga nõrgim naastrehv oli parimale lamellile lähemal kui parimale naastrehvile. Kõik testitud rehvid ja nende tulemused: <a href="/testid/">Sõltumatud testid</a>.</p>

<h2>Kontrolli oma autoga</h2>
<p>Numbrid siin on VW Golfi kohta. Sinu auto ja rehvimõõduga:</p>
<ul><li><a href="/?olud=snow&kiirus=50#kalkulaator">Pidurdusmaa lumel 50 km/h pealt</a></li><li><a href="/?olud=ice&kiirus=50#kalkulaator">Pidurdusmaa jääl 50 km/h pealt</a></li><li><a href="/rehvi-valimine/?hooaeg=winter">Talverehvid sinu auto mõõdus</a> — järjestatud lume ja jää pidurduse järgi</li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;
</script>

<Leht
	title={A.title}
	desc={A.desc}
	path="teadmine/artiklid/talverehvi-valimine/"
	crumbs={[["Teadmine", "/teadmine/"], ["Artiklid", "/teadmine/artiklid/"], [A.title, "/teadmine/artiklid/talverehvi-valimine/"]]}
	lapsed={[]}
	uuendatud={A.kuupaev}
	avaldatud={A.kuupaev}
	sisu={SISU}
/>
