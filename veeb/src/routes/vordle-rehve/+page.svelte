<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	/* /vordle-rehve/ — valitud 2–4 rehvi kõrvuti. Valimise loogika on
	   /rehvi-valimine/ lehel; siin ainult võrdlus ja otsing lisamiseks. */
	import Meta from '$lib/Meta.svelte';
	import { tooriist, graph } from '$lib/skeem.js';
	import How from '$lib/How.svelte';
</script>

<Meta
	title={t("Võrdle rehve — märghaare, müra, veeretakistus ja pidurdusmaa")}
	desc={t("Võrdle rehvimudeleid sinu auto mõõdus päris andmete järgi: EL-i rehvimärgis, sõltumatud testid ja arvutatud pidurdusmaa. Ilma väljamõeldud koondhindeta.")}
	path="vordle-rehve/"
	crumbs={[[t('Avaleht'), '/'], [t('Rehvi valimine'), '/rehvi-valimine/'], [t('Võrdle'), '/vordle-rehve/']]}
	jsonld={graph(tooriist(t('Rehvide võrdlus'), '/vordle-rehve/', t('Võrdleb 2–4 rehvimudelit sinu auto mõõdus: märghaare, müra, veeretakistus ja arvutatud pidurdusmaa.'), keel.lang))}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			{@html t("<a href=\"/\">Avaleht</a><span>/</span><a href=\"/rehvi-valimine/\">Rehvi valimine</a><span>/</span>Võrdle")}
		</div>
		<h1>{t("Võrdle rehve kõrvuti")}</h1>
		<p>
			{t("Iga omadus eraldi ja allikaga: EL-i rehvimärgis, sõltumatud testid ja arvutatud pidurdusmaa sinu autoga. Ühtegi „parima rehvi“ punktisummat ei ole.")}
		</p>
		<div class="pills">
			{@html t("<span class=\"pill off\">Ametlik märgis</span><span class=\"pill test\">Sõltumatu test</span><span class=\"pill calc\">Arvutus</span ><span class=\"pill\"><span class=\"est\" style=\"margin:0\">≈</span> Tuletatud</span>")}
		</div>
	</div>
</section>

<div class="body-sec" data-cmp-page data-mode="vordle">
	<div class="wrap">
		<div id="vordlus" data-cmp-table></div>

		<div class="box" style="margin-top:var(--sp-8)">
			<h2>{t("Lisa rehve")}</h2>
			<div class="add-bar">
				<select class="lsel" data-f="make" aria-label={t("Mark")}><option value="">{t("Mark")}</option></select>
				<select class="lsel" data-f="model" aria-label={t("Mudel")} disabled><option value="">{t("Mudel")}</option></select>
				<select class="lsel" data-f="year" aria-label={t("Aasta")} disabled><option value="">{t("Aasta")}</option></select>
				<select class="lsel" data-f="variant" aria-label={t("Mootor")} disabled><option value="">{t("Mootor")}</option></select>
				<select class="lsel" data-f="size" aria-label={t("Rehvimõõt")}><option value="20555R16">205/55 R16</option></select>
				<div class="lseg" role="group" aria-label={t("Rehvi liik")}>
					<button type="button" data-season="summer">{t("Suverehv")}</button>
					<button type="button" data-season="winter">{t("Lamellrehv")}</button>
					<button type="button" data-season="naast">{t("Naastrehv")}</button>
					<button type="button" data-season="all">{t("Aastaringne")}</button>
				</div>
				<select class="lsel" data-rft aria-label="Run-flat">
					<option value="">{t("Run-flat: kõik")}</option>
					<option value="only">{t("Ainult run-flat")}</option>
					<option value="no">{t("Ilma run-flatita")}</option>
				</select>
				<select class="lsel" data-brand aria-label={t("Mark")}><option value="">{t("Kõik margid")}</option></select>
				<input class="lsel" type="search" data-q placeholder={t("Otsi marki või mudelit")} aria-label={t("Otsi rehvi")} style="background-image:none" />
			</div>
			<p class="note" data-cmp-head style="margin:var(--sp-3) 0"></p>
			<div class="res-list" data-cmp-list><p class="note">{t("Laen…")}</p></div>
		</div>
	</div>
</div>

<div class="cmp-tray" data-tray hidden>
	<div class="wrap">
		<div class="chips" data-tray-chips></div>
		<a class="btn yel sm" href="#vordlus" data-tray-go>{t("Vaata võrdlust ↑")}</a>
	</div>
</div>
<How />
