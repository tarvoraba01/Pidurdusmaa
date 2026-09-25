<script>
	/* /rehvi-valimine/ — kõik ühel ekraanil, iga klõps muudab järjestust
	   kohe ja lehel on kirjas, MIDA ta arvestas. Nimekirja täidab app.js. */
	import Meta from '$lib/Meta.svelte';
	import { tooriist, graph } from '$lib/skeem.js';
	import How from '$lib/How.svelte';
	import { VALIK_Q } from '$lib/util.js';
</script>

<Meta
	title="Rehvi valimine — vali rehv selle järgi, mis sulle oluline on"
	desc="Ütle, kus ja kui palju sõidad ning mis sulle rehvi juures oluline on. Näitame sinu auto mõõdus sobivaid rehve ja põhjuse, miks — päris andmete järgi."
	path="rehvi-valimine/"
	crumbs={[['Avaleht', '/'], ['Rehvi valimine', '/rehvi-valimine/']]}
	jsonld={graph(tooriist('Rehvi valimine', '/rehvi-valimine/', 'Näitab sinu auto mõõdus sobivaid rehve selle järgi, kus ja kui palju sõidad ning mis on rehvi juures tähtis.'))}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span>Rehvi valimine</div>
		<h1>Rehvi valimine</h1>
		<p>
			Ütle, kus ja kui palju sõidad ning mis sulle rehvi juures oluline on. Näitame sinu auto mõõdus
			sobivaid rehve — ja miks just neid.
		</p>
	</div>
</section>

<div class="body-sec" data-cmp-page data-mode="valik">
	<div class="wrap">
		<div class="qcard">
			<div class="qcol">
				<h2 class="qh"><span>1</span>Sinu auto ja rehv</h2>
				<div class="qsel">
					<select class="lsel" data-f="make" aria-label="Mark"><option value="">Mark</option></select>
					<select class="lsel" data-f="model" aria-label="Mudel" disabled><option value="">Mudel</option></select>
					<select class="lsel" data-f="year" aria-label="Aasta" disabled><option value="">Aasta</option></select>
					<select class="lsel" data-f="variant" aria-label="Mootor / variant" disabled><option value="">Variant</option></select>
				</div>
				<label class="qlab" for="v-size">Rehvimõõt</label>
				<select class="lsel" id="v-size" data-f="size"><option value="20555R16">205/55 R16</option></select>
				<p class="qlab">Hooaeg</p>
				<div class="lseg" role="group" aria-label="Hooaeg">
					<button type="button" data-season="summer">Suverehv</button>
					<button type="button" data-season="all">Aastaringne</button>
					<button type="button" data-season="winter">Talverehv</button>
				</div>
			</div>
			<div class="qcol">
				<h2 class="qh"><span>2</span>Mis sulle oluline on</h2>
				{#each Object.entries(VALIK_Q) as [g, item] (g)}
					<p class="qlab">{item[0]}</p>
					<div class="qchips" role="group" aria-label={item[0]}>
						{#each Object.entries(item[1]) as [v, label] (v)}
							<button type="button" class="qchip" data-ct={g} data-v={v} aria-pressed="false">{label}</button>
						{/each}
					</div>
				{/each}
				<div class="qout" data-ct-out></div>
			</div>
		</div>

		<div class="cmp-layout" style="margin-top:var(--sp-8)">
			<aside class="filters" aria-label="Täpsemad seaded">
				<div class="box">
					<div style="display:flex;align-items:center;justify-content:space-between">
						<h3 style="margin:0">Täpsusta kaalusid</h3>
						<button type="button" class="btn sm" data-prio-reset hidden>Tühjenda</button>
					</div>
					<p class="note" style="margin:var(--sp-2) 0 var(--sp-3)">
						Valikuline. Sinu vastused täidavad selle ise — siin näed ja muudad, kui palju iga omadus
						loeb (1–3).
					</p>
					<div class="prio" data-prio></div>
				</div>
				<div class="box">
					<h3 style="margin:0 0 var(--sp-2)">Kuidas järjestatakse</h3>
					<p class="note" style="margin:0">
						„Sobivus“ on ainult selle nimekirja sisene võrdlus sinu valitud omaduste järgi — mitte
						rehvi üldhinne. Omadus, mille kohta andmeid pole, jäetakse välja ja see öeldakse kaardil.
					</p>
					<p class="note" style="margin:var(--sp-3) 0 0">
						See on andmete kõrvutus, mitte ostunõuanne. <a href="/kasutustingimused/">Tingimused</a>
					</p>
				</div>
			</aside>
			<div>
				<div class="list-filter">
					<select class="lsel" data-brand aria-label="Mark"><option value="">Kõik margid</option></select>
					<input class="lsel" type="search" data-q placeholder="Otsi marki või mudelit" aria-label="Otsi rehvi" style="background-image:none" />
				</div>
				<p class="note" data-cmp-head style="margin:0 0 var(--sp-3);font-size:15px"></p>
				<div class="res-list" data-cmp-list><p class="note">Laen…</p></div>
			</div>
		</div>
	</div>
</div>

<div class="cmp-tray" data-tray hidden>
	<div class="wrap">
		<div class="chips" data-tray-chips></div>
		<a class="btn yel sm" href="/vordle-rehve/" data-tray-go>Võrdle kõrvuti →</a>
	</div>
</div>
<How />
