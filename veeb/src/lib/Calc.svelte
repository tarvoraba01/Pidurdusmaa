<script>
	import { useT } from '$lib/i18n.js';
	const t = useT();
	/* Kalkulaatori kaart: kaks režiimi (PIDURDUSMAA / VALI REHV) ühes kaardis.
	   Auto ja rehvimõõt on mõlemale ühised. Valikud täidab app.js failist
	   data/core.json — siin on ainult kest, täpselt samade konksudega
	   (data-*), mida app.js otsib. */
	import Icon from '$lib/Icon.svelte';
	import { VALIK_Q, CONDS } from '$lib/util.js';
</script>

<div class="calc-card" id="kalkulaator" data-calc>
	<div class="tabs" role="tablist" aria-label={t("Režiim")}>
		<button
			class="tab"
			role="tab"
			id="tab-calc"
			aria-controls="p-calc"
			aria-selected="true"
			data-tab="calc"><Icon name="target" />{t("Arvuta pidurdusmaa")}</button
		>
		<button
			class="tab"
			role="tab"
			id="tab-valik"
			aria-controls="p-valik"
			aria-selected="false"
			tabindex="-1"
			data-tab="valik"><Icon name="check" />{t("Leia sobiv rehv")}</button
		>
	</div>

	<div class="cc" style="padding-bottom:0">
		<div class="cc-grid" style="margin-bottom:var(--sp-3)">
			<div>
				<p class="lbl">{@html t("1. Sinu auto <span class=\"aside\" data-veh-hint></span>")}</p>
				<div class="car3">
					<select class="sel" data-f="make" aria-label={t("Mark")}><option value="">{t("Mark")}</option></select>
					<select class="sel" data-f="model" aria-label={t("Mudel")} disabled
						><option value="">{t("Mudel")}</option></select
					>
					<select class="sel" data-f="year" aria-label={t("Aasta / põlvkond")} disabled
						><option value="">{t("Aasta")}</option></select
					>
				</div>
				<div class="var-row">
					<select class="sel" data-f="variant" aria-label={t("Mootor")} disabled
						><option value="">{t("Mootor")}</option></select
					>
					<button type="button" class="abs-lamp" data-abs hidden aria-pressed="false" aria-disabled="true"
						><svg viewBox="0 0 44 28" aria-hidden="true"
							><path d="M9 4.5a14 14 0 0 0 0 19M35 4.5a14 14 0 0 1 0 19" /><circle cx="22" cy="14" r="10" /><text
								x="22"
								y="17.3">ABS</text
							></svg
						><span data-abs-t>{t("Kas on ABS?")}</span></button
					>
				</div>
			</div>
			<div>
				<div class="own" data-calc-only>
					<p class="lbl">
						<label for="f-own">{t("Sinu rehv")}</label> <span class="opt">{t("valikuline")}</span>
					</p>
					<div class="vs vs-dark own-vs">
						<input
							id="f-own"
							class="sel vs-in"
							type="search"
							placeholder={t("Nt Hakkapeliitta R5 — pole kohustuslik")}
							autocomplete="off"
							spellcheck="false"
							role="combobox"
							aria-expanded="false"
							aria-autocomplete="list"
							aria-controls="own-list"
							aria-describedby="own-hint"
							data-own-in
						/>
						<ul class="vs-list" id="own-list" role="listbox" hidden data-own-list></ul>
					</div>
					<p class="size-hint" id="own-hint" data-own-hint hidden></p>
				</div>
				<p class="lbl"><label for="f-size">{t("2. Rehvimõõt")}</label></p>
				<select class="sel" id="f-size" data-f="size"
					><option value="20555R16">205/55 R16</option></select
				>
				<p class="size-note" data-size-tag hidden></p>
				<p class="size-hint">{t("Täpne mõõt on rehvi küljel ja juhiukse piirdel.")}</p>
			</div>
		</div>
	</div>

	<div class="cc" id="p-calc" role="tabpanel" aria-labelledby="tab-calc">
		<div class="cc-grid">
			<div>
				<p class="lbl"><label for="f-speed">{t("3. Kiirus")}</label></p>
				<div class="spd">
					<input
						class="slider"
						type="range"
						id="f-speed"
						min="40"
						max="130"
						step="5"
						value="90"
						data-f="speed"
					/>
					<span class="spd-num"
						><input
							type="number"
							inputmode="numeric"
							min="20"
							max="130"
							step="5"
							value="90"
							aria-label={t("Kiirus km/h")}
							data-f="speednum"
						/>{t("km/h")}</span
					>
				</div>
				<p class="cap-note" data-cap-note hidden></p>
			</div>
			<div>
				<p class="lbl">{t("4. Teeolud")}</p>
				<div class="conds" role="group" aria-label={t("Teeolud")}>
					{#each Object.entries(CONDS) as [k, c] (k)}
						<button
							type="button"
							class="cond"
							data-cond={k}
							aria-pressed={k === 'wet' ? 'true' : 'false'}
							title={t(c[1])}><Icon name={k} /><span>{t(c[0])}</span></button
						>
					{/each}
				</div>
			</div>
		</div>
		<button class="cta" type="button" data-go
			>{@html t("Arvuta pidurdusmaa <span class=\"arr\" aria-hidden=\"true\">→</span>")}</button
		>
		<p class="go-msg" data-go-msg hidden>
			{t("Vali kõigepealt auto — siis arvutame just selle järgi.")}
			<button type="button" class="linkbtn" data-go-default
				>{t("Pole oma autot? Arvuta tüüpilise kompaktauto järgi")}</button
			>
		</p>
	</div>

	<div class="cc" id="p-valik" role="tabpanel" aria-labelledby="tab-valik" hidden>
		<div class="vq">
			<div>
				<p class="lbl">{t("3. Hooaeg")}</p>
				<div class="seg" role="group" aria-label={t("Hooaeg")}>
					<button type="button" data-season="summer" aria-pressed="true">{t("Suvi")}</button>
					<button type="button" data-season="all" aria-pressed="false">{t("Aastaringne")}</button>
					<button type="button" data-season="winter" aria-pressed="false">{t("Talv")}</button>
				</div>
			</div>
			{#each Object.entries(VALIK_Q) as [g, item], i (g)}
				<div>
					<p class="lbl">{i + 4}. {t(item[0])} {#if item[2]}<span class="tip" tabindex="0" data-tip={t(item[2])} aria-label={t(item[2])}>i</span>{/if}</p>
					<div class="qchips" role="group" aria-label={t(item[0])}>
						{#each Object.entries(item[1]) as [v, label] (v)}
							<button type="button" class="qchip" data-ct={g} data-v={v} aria-pressed="false"
								>{t(label)}</button
							>
						{/each}
					</div>
				</div>
			{/each}
		</div>
		<div class="vq-out" data-ct-out></div>
		<button class="cta" type="button" data-go-valik
			>{@html t("Näita sobivaid rehve <span class=\"arr\" aria-hidden=\"true\">→</span>")}</button
		>
	</div>
</div>
