<script>
	/* Kalkulaatori kaart: kaks režiimi (PIDURDUSMAA / VALI REHV) ühes kaardis.
	   Auto ja rehvimõõt on mõlemale ühised. Valikud täidab app.js failist
	   data/core.json — siin on ainult kest, täpselt samade konksudega
	   (data-*), mida app.js otsib. */
	import Icon from '$lib/Icon.svelte';
	import { VALIK_Q, CONDS } from '$lib/util.js';
</script>

<div class="calc-card" id="kalkulaator" data-calc>
	<div class="tabs" role="tablist" aria-label="Režiim">
		<button
			class="tab"
			role="tab"
			id="tab-calc"
			aria-controls="p-calc"
			aria-selected="true"
			data-tab="calc"><Icon name="target" />Pidurdusmaa</button
		>
		<button
			class="tab"
			role="tab"
			id="tab-valik"
			aria-controls="p-valik"
			aria-selected="false"
			tabindex="-1"
			data-tab="valik"><Icon name="check" />Vali rehv enda tingimustel</button
		>
	</div>

	<div class="cc" style="padding-bottom:0">
		<div class="cc-grid" style="margin-bottom:var(--sp-3)">
			<div>
				<p class="lbl">1. Sinu auto <span class="aside" data-veh-hint></span></p>
				<div class="car3">
					<select class="sel" data-f="make" aria-label="Mark"><option value="">Mark</option></select>
					<select class="sel" data-f="model" aria-label="Mudel" disabled
						><option value="">Mudel</option></select
					>
					<select class="sel" data-f="year" aria-label="Aasta / põlvkond" disabled
						><option value="">Aasta</option></select
					>
				</div>
				<div class="var-row">
					<select class="sel" data-f="variant" aria-label="Mootor / variant" disabled
						><option value="">Mootor / variant</option></select
					>
				</div>
			</div>
			<div>
				<p class="lbl"><label for="f-size">2. Rehvimõõt</label></p>
				<select class="sel" id="f-size" data-f="size"
					><option value="20555R16">205/55 R16</option></select
				>
				<p class="size-note" data-size-tag hidden></p>
				<p class="size-hint">Täpne mõõt on rehvi küljel ja juhiukse piirdel.</p>
			</div>
		</div>
	</div>

	<div class="cc" id="p-calc" role="tabpanel" aria-labelledby="tab-calc">
		<div class="cc-grid">
			<div>
				<p class="lbl"><label for="f-speed">3. Kiirus</label></p>
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
							aria-label="Kiirus km/h"
							data-f="speednum"
						/>km/h</span
					>
				</div>
				<p class="cap-note" data-cap-note hidden></p>
			</div>
			<div>
				<p class="lbl">4. Teeolud</p>
				<div class="conds" role="group" aria-label="Teeolud">
					{#each Object.entries(CONDS) as [k, c] (k)}
						<button
							type="button"
							class="cond"
							data-cond={k}
							aria-pressed={k === 'wet' ? 'true' : 'false'}
							title={c[1]}><Icon name={k} /><span>{c[0]}</span></button
						>
					{/each}
				</div>
			</div>
		</div>
		<button class="cta" type="button" data-go
			>Arvuta pidurdusmaa <span class="arr" aria-hidden="true">→</span></button
		>
		<p class="go-msg" data-go-msg hidden>
			Vali kõigepealt auto — siis arvutame just selle järgi.
			<button type="button" class="linkbtn" data-go-default
				>Pole oma autot? Arvuta tüüpilise kompaktauto järgi</button
			>
		</p>
	</div>

	<div class="cc" id="p-valik" role="tabpanel" aria-labelledby="tab-valik" hidden>
		<div class="vq">
			<div>
				<p class="lbl">3. Hooaeg</p>
				<div class="seg" role="group" aria-label="Hooaeg">
					<button type="button" data-season="summer" aria-pressed="true">Suvi</button>
					<button type="button" data-season="all" aria-pressed="false">Lamell</button>
					<button type="button" data-season="winter" aria-pressed="false">Talv</button>
				</div>
			</div>
			{#each Object.entries(VALIK_Q) as [g, item], i (g)}
				<div>
					<p class="lbl">{i + 4}. {item[0]}</p>
					<div class="qchips" role="group" aria-label={item[0]}>
						{#each Object.entries(item[1]) as [v, label] (v)}
							<button type="button" class="qchip" data-ct={g} data-v={v} aria-pressed="false"
								>{label}</button
							>
						{/each}
					</div>
				</div>
			{/each}
		</div>
		<div class="vq-out" data-ct-out></div>
		<button class="cta" type="button" data-go-valik
			>Näita sobivaid rehve <span class="arr" aria-hidden="true">→</span></button
		>
	</div>
</div>
