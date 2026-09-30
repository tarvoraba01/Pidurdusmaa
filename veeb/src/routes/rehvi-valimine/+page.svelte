<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	/* /rehvi-valimine/ — kõik ühel ekraanil, iga klõps muudab järjestust
	   kohe ja lehel on kirjas, MIDA ta arvestas. Nimekirja täidab app.js. */
	import Meta from '$lib/Meta.svelte';
	import { tooriist, graph } from '$lib/skeem.js';
	import How from '$lib/How.svelte';
	import { VALIK_Q } from '$lib/util.js';
</script>

<Meta
	title={t("Rehvi valimine — vali rehv selle järgi, mis sulle oluline on")}
	desc={t("Ütle, kus ja kui palju sõidad ning mis sulle rehvi juures oluline on. Näitame sinu auto mõõdus sobivaid rehve ja põhjuse, miks — päris andmete järgi.")}
	path="rehvi-valimine/"
	crumbs={[[t('Avaleht'), '/'], [t('Rehvi valimine'), '/rehvi-valimine/']]}
	jsonld={graph(tooriist(t('Rehvi valimine'), '/rehvi-valimine/', t('Näitab sinu auto mõõdus sobivaid rehve selle järgi, kus ja kui palju sõidad ning mis on rehvi juures tähtis.'), keel.lang))}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">{@html t("<a href=\"/\">Avaleht</a><span>/</span>Rehvi valimine")}</div>
		<h1>{t("Rehvi valimine")}</h1>
		<p>{t("Ütle, kus ja kui palju sõidad ning mis sulle rehvi juures oluline on.")}</p>
		<p class="hero-lisa">{t("Näitame rehve sinu tingimustel.")}</p>
	</div>
</section>

<div class="body-sec" data-cmp-page data-mode="valik">
	<div class="wrap">
		<div class="qcard">
			<div class="qcol">
				<h2 class="qh">{@html t("<span>1</span>Sinu auto ja rehv")}</h2>
				<div class="qsel">
					<select class="lsel" data-f="make" aria-label={t("Mark")}><option value="">{t("Mark")}</option></select>
					<select class="lsel" data-f="model" aria-label={t("Mudel")} disabled><option value="">{t("Mudel")}</option></select>
					<select class="lsel" data-f="year" aria-label={t("Aasta")} disabled><option value="">{t("Aasta")}</option></select>
					<select class="lsel" data-f="variant" aria-label={t("Mootor")} disabled><option value="">{t("Mootor")}</option></select>
				</div>
				<label class="qlab" for="v-size">{t("Rehvimõõt")}</label>
				<select class="lsel" id="v-size" data-f="size"><option value="20555R16">205/55 R16</option></select>
				<p class="qlab">{t("Hooaeg")}</p>
				<div class="lseg" role="group" aria-label={t("Hooaeg")}>
					<button type="button" data-season="summer">{t("Suverehv")}</button>
					<button type="button" data-season="all">{t("Aastaringne")}</button>
					<button type="button" data-season="winter">{t("Talverehv")}</button>
				</div>
			</div>
			<div class="qcol">
				<h2 class="qh">{@html t("<span>2</span>Mis sulle oluline on")}</h2>
				{#each Object.entries(VALIK_Q) as [g, item] (g)}
					<p class="qlab">{t(item[0])} {#if item[2]}<span class="tip" tabindex="0" data-tip={t(item[2])} aria-label={t(item[2])}>i</span>{/if}</p>
					<div class="qchips" role="group" aria-label={t(item[0])}>
						{#each Object.entries(item[1]) as [v, label] (v)}
							<button type="button" class="qchip" data-ct={g} data-v={v} aria-pressed="false">{t(label)}</button>
						{/each}
					</div>
				{/each}
				<div class="qout" data-ct-out></div>
			</div>
		</div>

		<div class="cmp-layout" style="margin-top:var(--sp-8)">
			<aside class="filters" aria-label={t("Täpsemad seaded")}>
				<div class="box">
					<div style="display:flex;align-items:center;justify-content:space-between">
						<h3 style="margin:0">{t("Täpsusta soove")}</h3>
						<button type="button" class="btn sm" data-prio-reset hidden>{t("Tühjenda")}</button>
					</div>
					<p class="note" style="margin:var(--sp-2) 0 var(--sp-3)">
						{t("Valikuline. Sinu vastused täidavad selle ise — siin näed ja muudad, kui palju iga omadus loeb (1–3).")}
					</p>
					<div class="prio" data-prio></div>
				</div>
				<div class="box">
					<h3 style="margin:0 0 var(--sp-2)">{t("Kuidas järjestatakse")}</h3>
					<p class="note" style="margin:0">
						{t("„Sobivus“ on ainult selle nimekirja sisene võrdlus sinu valitud omaduste järgi — mitte rehvi üldhinne. Omadus, mille kohta andmeid pole, jäetakse välja ja see öeldakse kaardil.")}
					</p>
					<p class="note" style="margin:var(--sp-3) 0 0">
						{@html t("See on andmete kõrvutus, mitte ostunõuanne. <a href=\"/kasutustingimused/\">Tingimused</a>")}
					</p>
				</div>
			</aside>
			<div>
				<div class="list-filter">
					<select class="lsel" data-brand aria-label={t("Mark")}><option value="">{t("Kõik margid")}</option></select>
					<input class="lsel" type="search" data-q placeholder={t("Otsi marki või mudelit")} aria-label={t("Otsi rehvi")} style="background-image:none" />
				</div>
				<p class="note" data-cmp-head style="margin:0 0 var(--sp-3);font-size:15px"></p>
				<div class="res-list" data-cmp-list><p class="note">{t("Laen…")}</p></div>
			</div>
		</div>
	</div>
</div>

<div class="cmp-tray" data-tray hidden>
	<div class="wrap">
		<div class="chips" data-tray-chips></div>
		<a class="btn yel sm" href={keel.L('/vordle-rehve/')} data-tray-go>{t("Võrdle kõrvuti →")}</a>
	</div>
</div>
<How />
