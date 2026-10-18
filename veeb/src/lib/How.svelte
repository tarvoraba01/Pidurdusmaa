<script>
	import { onMount, flushSync } from 'svelte';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const L = useLang().L;
	/* „Kuidas pidurdusmaa arvutatakse?“ — lühike selgitus dialoogis.
	   Pikk versioon on lehel /teadmine/kuidas-pidurdusmaa-arvutatakse/.
	   Avamise ja sulgemise teeb app.js (data-how / data-how-close).
	   lazy: sisu tehakse alles esimesel avamisel. Rehvilehtedel (4 600 URL-i) oli sama
	   313 sõna igal lehel serveri HTML-is (audit 18.10) — kasutaja näeb sama dialoogi. */
	import { CONDS } from '$lib/util.js';
	let { lazy = false } = $props();
	let avatud = $state(!lazy);
	onMount(() => {
		if (avatud) return;
		/* püüdmisfaasis enne app.js-i: sisu on DOM-is enne showModal()-i */
		const ava = (e) => {
			if (e.target && e.target.closest && e.target.closest('[data-how]')) {
				avatud = true;
				flushSync();
				window.removeEventListener('click', ava, true);
			}
		};
		window.addEventListener('click', ava, true);
		return () => window.removeEventListener('click', ava, true);
	});
</script>

<dialog class="how" id="how" aria-labelledby="how-t">
	<div class="how-h">
		<h2 id="how-t">{t("Kuidas arvutatakse")}</h2>
		<button type="button" class="how-x" data-how-close aria-label={t("Sulge")}>×</button>
	</div>
	<div class="how-b">
		{#if avatud}
		<p>
			{@html t("Tulemus on <strong>arvutatud hinnang</strong>, mitte laborimõõtmine. Mudel simuleerib pidurdust samm-sammult: rehvi haare antud kiirusel, ABS, õhutakistus, auto mass ja pidurid.")}
		</p>
		<h3>{t("Andmete liigid lehel")}</h3>
		<div class="legend">
			<div>
				{@html t("<span class=\"pill off\">Ametlik</span><span >EL-i rehvimärgis (EPREL): märghaardumine, veeretakistus, müra, lume- ja jäämärk.</span >")}
			</div>
			<div>
				{@html t("<span class=\"pill test\">Sõltumatu test</span><span >ADAC, Tekniikan Maailma, UTAC — mõõdetud pidurdusmaad, allika ja aastaga.</span >")}
			</div>
			<div>
				{@html t("<span class=\"pill calc\">Arvutatud</span><span >Selle lehe mudel sinu auto, kiiruse ja teeolude jaoks.</span >")}
			</div>
			<div>
				{@html t("<span class=\"pill\"><span class=\"est\" style=\"margin:0\">≈</span> Tuletatud</span><span >Meie mudeli hinnang omadusele, mida selle rehvi kohta mõõdetud ei ole (kuivpidurdus, pidurdus sügavas vees, lumi, jää) — rehvitüübi keskmise järgi.</span >")}
			</div>
			<div>{@html t("<span class=\"pill\">Sinu sisend</span><span>Auto, rehvimõõt, kiirus, teeolud.</span>")}</div>
		</div>
		<h3>{t("Eeldused")}</h3>
		<ul>
			{#each Object.values(CONDS) as c}
				<li><strong>{t(c[0])}:</strong> {t(c[1])}</li>
			{/each}
			<li>{t("Uus rehv (8 mm), rõhk tehase soovituse järgi, autos juht.")}</li>
			<li>
				{@html t("<strong>Vesiliug:</strong> sama uus rehv, aga teel on 3 mm vett (roopad, suur lomp). Tavaline märg tee on 1 mm.")}
			</li>
			<li>
				{@html t("<strong>Reaktsiooniaega ei arvestata.</strong> Pidurdusmaa algab hetkest, kui pidur on põhjas. Reaktsioonile kulub tavaliselt umbes 1 sekund — 90 km/h juures on see veel 25 meetrit enne, kui auto üldse aeglustama hakkab.")}
			</li>
			<li>
				{t("Auto tehasemõõdud on veebist üle kontrollitud (rehvisobivuse ja tootjate lehed) — enamasti on neid 2–4. Leht pakub neist levinuima, aga täpne mõõt on sinu rehvi küljel.")}
			</li>
			<li>{t("Kui auto on valimata, arvutatakse tüüpilise kompaktauto järgi (VW Golf 8).")}</li>
		</ul>
		<h3>{t("Täpsus")}</h3>
		<ul>
			<li>
				{t("Testitud rehvidel tuleb haare mõõdetud tulemusest. Mõõdetud pidurdusmaade vastu on mudeli viga asfaldil keskmiselt 4,4%.")}
			</li>
			<li>
				{@html t("Ainult märgisega rehvidel on teada ainult klass (A–E). Klassi haare ei ole vahemiku nominaalne keskpunkt, vaid <strong>sama klassi mõõdetud rehvide mediaan</strong> (nt A-klassi tavaline suverehv 1,47, A-klassi sportrehv 1,64). Sama klassi rehvid on mudelis võrdsed — päris elus erinevad nad ±3–4%.")}
			</li>
			<li>
				{t("Kuival, lumel ja jääl ei ütle märgis midagi. Neil pindadel järjestatakse ainult testitud rehve.")}
			</li>
		</ul>
		<h3>{t("Piirangud")}</h3>
		<p>{t("Lörtsi ja kurvis pidurdamist mudel ei arvesta. Vahemik tulemuse all näitab ebakindlust.")}</p>
		<h3>{t("Vastutus")}</h3>
		<p>
			{@html t("Lehe numbrid on üldiseks teadmiseks ja rehvide võrdlemiseks. Need ei ole garantii, ekspertarvamus ega alus liikluses otsustamiseks — sõida alati vastavalt oludele. <a href=\"/kasutustingimused/\">Kasutustingimused ja vastutus</a>")}
		</p>
		{/if}
		<p><a href={L('/teadmine/kuidas-pidurdusmaa-arvutatakse/')}>{t("Loe täielikku metoodikat →")}</a></p>
	</div>
</dialog>
