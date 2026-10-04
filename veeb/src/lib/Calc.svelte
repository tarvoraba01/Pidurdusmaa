<script>
	import { useT } from '$lib/i18n.js';
	const t = useT();
	/* Kalkulaatori kaart: kaks režiimi (PIDURDUSMAA / VALI REHV) ühes kaardis.
	   Auto ja rehvimõõt on mõlemale ühised. Valikud täidab app.js failist
	   data/core.json — siin on ainult kest, täpselt samade konksudega
	   (data-*), mida app.js otsib. */
	import Icon from '$lib/Icon.svelte';
	import { CONDS } from '$lib/util.js';
</script>

<div class="calc-card" id="kalkulaator" data-calc>
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
							placeholder={t("Nt Hakkapeliitta R5")}
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
					<label class="own-mm-l" for="f-mm"
						title={t("Näitame, kui palju uued rehvid samades oludes varem peatuvad.")}
						>{t("Mustrisügavus")}
						<select class="sel own-mm" id="f-mm" data-f="muster">
							<option value="">{t("uus")}</option>
							{#each [7, 6, 5, 4, 3, 2] as mm (mm)}
								<option value={mm}>{mm} {t("mm")}</option>
							{/each}
						</select></label
					>
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

	<div class="cc" id="p-calc">
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

</div>
