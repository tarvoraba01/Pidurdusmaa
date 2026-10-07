<script>
	/* /kontakt/ — ettevõtetele: rehvimüüjate hinnad, koostöö, andmevead.
	   Vormi saadab app.js (initContact) serverisse; Turnstile kaitseb rämpsu eest.
	   Ettevõtte andmed (seaded.js) on seaduse järgi siin nähtaval. */
	import Meta from '$lib/Meta.svelte';
	import Turnstile from '$lib/Turnstile.svelte';
	import { useT, useLang } from '$lib/i18n.js';
	import { ETTEVOTE, ETTEVOTE_REGKOOD, ETTEVOTE_AADRESS, ETTEVOTE_EPOST } from '$lib/seaded.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	const TEEMAD = {
		hinnad: t('Rehvimüüja — hinnad lehele'),
		koostoo: t('Koostöö'),
		viga: t('Viga andmetes'),
		ettepanek: t('Ettepanek või küsimus'),
		muu: t('Muu')
	};
</script>

<Meta
	title={t('Kontakt')}
	desc={t('Võta Pidurdusmaa.ee-ga ühendust: rehvimüüjate hinnad ja koostöö, vead andmetes, ettepanekud.')}
	path="kontakt/"
	crumbs={[[t('Avaleht'), '/'], [t('Kontakt'), '/kontakt/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span>{t('Kontakt')}</div>
		<h1>{t('Kontakt')}</h1>
		<p>
			{t('Oled rehvimüüja ja soovid oma hinnad lehele? Leidsid andmetest vea? Või on lihtsalt mõte? Kirjuta — vastame e-postile.')}
		</p>
	</div>
</section>

<div class="body-sec">
	<div class="wrap contact-grid">
		<form class="box contact-form" data-contact novalidate>
			<div class="hp" aria-hidden="true">
				<label>Veebileht <input type="text" name="veeb" tabindex="-1" autocomplete="off" /></label>
			</div>

			<label class="fl" for="k-teema">{t('Teema')}</label>
			<select class="lsel" id="k-teema" name="teema">
				{#each Object.entries(TEEMAD) as [k, v] (k)}<option value={k}>{v}</option>{/each}
			</select>

			<div class="two">
				<div>
					<label class="fl" for="k-nimi">{t('Nimi')}</label>
					<input class="lin" id="k-nimi" name="nimi" type="text" autocomplete="name" required maxlength="120" />
				</div>
				<div>
					<label class="fl" for="k-email">{t('E-post')}</label>
					<input class="lin" id="k-email" name="email" type="email" autocomplete="email" required />
				</div>
			</div>

			<label class="fl" for="k-firma">{t('Ettevõte')} <span class="opt">{t('valikuline')}</span></label>
			<input class="lin" id="k-firma" name="firma" type="text" autocomplete="organization" maxlength="160" />

			<label class="fl" for="k-sonum">{t('Sõnum')}</label>
			<textarea class="lin" id="k-sonum" name="sonum" rows="7" required maxlength="5000"></textarea>

			<p class="note" style="margin:var(--sp-3) 0 0">
				{t('Kasutame sinu andmeid ainult sellele kirjale vastamiseks. Me ei lisa sind ühelegi listile.')}
			</p>
			<Turnstile />
			<div class="form-msg" data-contact-msg role="status" aria-live="polite" hidden></div>
			<button class="btn yel" type="submit" data-contact-go>{t('Saada kiri →')}</button>
		</form>

		<aside class="contact-side">
			<div class="box">
				<h3>{t('Ettevõtte andmed')}</h3>
				<dl class="firma">
					<dt>{t('Teenuse osutaja')}</dt>
					<dd>{ETTEVOTE}</dd>
					{#if ETTEVOTE_REGKOOD}<dt>{t('Registrikood')}</dt><dd>{ETTEVOTE_REGKOOD}</dd>{/if}
					{#if ETTEVOTE_AADRESS}<dt>{t('Aadress')}</dt><dd>{ETTEVOTE_AADRESS}</dd>{/if}
					{#if ETTEVOTE_EPOST}<dt>{t('E-post')}</dt><dd><a href="mailto:{ETTEVOTE_EPOST}">{ETTEVOTE_EPOST}</a></dd>{/if}
				</dl>
			</div>
			<div class="box">
				<h3>{t('Rehvimüüjale')}</h3>
				<p class="note">
					{t('Iga rehvi juures on koht müüjate hindadele — kalkulaatori tulemuses, rehvi valimisel ja võrdluses. Hinnad tulevad otse teie süsteemist (API või hinnafail) ja on alati koos lingiga teie poodi.')}
				</p>
				<p class="note" style="margin:0">
					{t('Järjestust ega pidurdusmaad hind ei mõjuta — see jääb andmepõhiseks.')}
				</p>
			</div>
			<div class="box">
				<h3>{t('Andmete kohta')}</h3>
				<p class="note" style="margin:0">
					{t('Kui mõni rehv, mõõt või testitulemus on vale, kirjuta rehvi nimi ja mõõt — parandame.')}
					{#if keel.lang === 'et'}<a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas arvutame</a>{/if}
				</p>
			</div>
		</aside>
	</div>
</div>

<style>
	.firma {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 4px var(--sp-3);
		margin: 0;
		font-size: 14px;
	}
	.firma dt {
		color: var(--muted);
	}
	.firma dd {
		margin: 0;
		font-weight: 600;
		overflow-wrap: anywhere;
	}
</style>
