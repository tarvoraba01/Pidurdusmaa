<script>
	/* /kontakt/ — ettevõtetele: rehvimüüjate hinnad, koostöö, andmevead.
	   Staatilisel saidil ei ole serverit, kes kirja saadaks — vorm avab
	   valmis kirja kasutaja e-posti programmis (app.js, CFG.contact tühi). */
	import Meta from '$lib/Meta.svelte';
	const TEEMAD = {
		hinnad: 'Rehvimüüja — hinnad lehele',
		koostoo: 'Koostöö või reklaam',
		viga: 'Viga andmetes',
		ettepanek: 'Ettepanek või küsimus',
		muu: 'Muu'
	};
</script>

<Meta
	title="Kontakt"
	desc="Võta Pidurdusmaa.ee-ga ühendust: rehvimüüjate hinnad ja koostöö, vead andmetes, ettepanekud."
	path="kontakt/"
	crumbs={[['Avaleht', '/'], ['Kontakt', '/kontakt/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="/">Avaleht</a><span>/</span>Kontakt</div>
		<h1>Kontakt</h1>
		<p>
			Oled rehvimüüja ja soovid oma hinnad lehele? Leidsid andmetest vea? Või on lihtsalt mõte?
			Kirjuta — vastame e-postile.
		</p>
	</div>
</section>

<div class="body-sec">
	<div class="wrap contact-grid">
		<form class="box contact-form" data-contact novalidate>
			<div class="hp" aria-hidden="true">
				<label>Veebileht <input type="text" name="veeb" tabindex="-1" autocomplete="off" /></label>
			</div>

			<label class="fl" for="k-teema">Teema</label>
			<select class="lsel" id="k-teema" name="teema">
				{#each Object.entries(TEEMAD) as [k, v] (k)}<option value={k}>{v}</option>{/each}
			</select>

			<div class="two">
				<div>
					<label class="fl" for="k-nimi">Nimi</label>
					<input class="lin" id="k-nimi" name="nimi" type="text" autocomplete="name" required maxlength="120" />
				</div>
				<div>
					<label class="fl" for="k-email">E-post</label>
					<input class="lin" id="k-email" name="email" type="email" autocomplete="email" required />
				</div>
			</div>

			<label class="fl" for="k-firma">Ettevõte <span class="opt">valikuline</span></label>
			<input class="lin" id="k-firma" name="firma" type="text" autocomplete="organization" maxlength="160" />

			<label class="fl" for="k-sonum">Sõnum</label>
			<textarea class="lin" id="k-sonum" name="sonum" rows="7" required maxlength="5000"></textarea>

			<p class="note" style="margin:var(--sp-3) 0 0">
				Kasutame sinu andmeid ainult sellele kirjale vastamiseks. Me ei lisa sind ühelegi listile.
			</p>
			<div class="form-msg" data-contact-msg role="status" aria-live="polite" hidden></div>
			<button class="btn yel" type="submit" data-contact-go>Saada kiri →</button>
		</form>

		<aside class="contact-side">
			<div class="box">
				<h3>Rehvimüüjale</h3>
				<p class="note">
					Iga rehvi juures on koht müüjate hindadele — kalkulaatori tulemuses, rehvi valimisel ja
					võrdluses. Hinnad tulevad otse teie süsteemist (API või hinnafail) ja on alati koos lingiga
					teie poodi.
				</p>
				<p class="note" style="margin:0">
					Järjestust ega pidurdusmaad hind ei mõjuta — see jääb andmepõhiseks.
				</p>
			</div>
			<div class="box">
				<h3>Andmete kohta</h3>
				<p class="note" style="margin:0">
					Kui mõni rehv, mõõt või testitulemus on vale, kirjuta rehvi nimi ja mõõt — parandame.
					<a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas arvutame</a>
				</p>
			</div>
		</aside>
	</div>
</div>
