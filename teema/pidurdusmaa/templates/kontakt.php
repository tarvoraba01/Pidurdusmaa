<?php
/**
 * /kontakt/ — kontaktivorm. Kiri läheb inc/contact.php kaudu.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><span>/</span>Kontakt</div>
		<h1>Kontakt</h1>
		<p>Oled rehvimüüja ja soovid oma hinnad lehele? Leidsid andmetest vea? Või on lihtsalt mõte? Kirjuta — vastame e-postile.</p>
	</div>
</section>

<div class="body-sec">
	<div class="wrap contact-grid">
		<form class="box contact-form" data-contact novalidate>
			<input type="hidden" name="_pm" value="<?php echo esc_attr( wp_create_nonce( 'pm_kontakt' ) ); ?>">
			<input type="hidden" name="_t" value="<?php echo esc_attr( time() ); ?>">
			<div class="hp" aria-hidden="true"><label>Veebileht <input type="text" name="veeb" tabindex="-1" autocomplete="off"></label></div>

			<label class="fl" for="k-teema">Teema</label>
			<select class="lsel" id="k-teema" name="teema">
				<?php foreach ( pm_contact_topics() as $k => $v ) : ?>
					<option value="<?php echo esc_attr( $k ); ?>"><?php echo esc_html( $v ); ?></option>
				<?php endforeach; ?>
			</select>

			<div class="two">
				<div>
					<label class="fl" for="k-nimi">Nimi</label>
					<input class="lin" id="k-nimi" name="nimi" type="text" autocomplete="name" required maxlength="120">
				</div>
				<div>
					<label class="fl" for="k-email">E-post</label>
					<input class="lin" id="k-email" name="email" type="email" autocomplete="email" required>
				</div>
			</div>

			<label class="fl" for="k-firma">Ettevõte <span class="opt">valikuline</span></label>
			<input class="lin" id="k-firma" name="firma" type="text" autocomplete="organization" maxlength="160">

			<label class="fl" for="k-sonum">Sõnum</label>
			<textarea class="lin" id="k-sonum" name="sonum" rows="7" required maxlength="5000"></textarea>

			<p class="note" style="margin:12px 0 0">Kasutame sinu andmeid ainult sellele kirjale vastamiseks. Me ei lisa sind ühelegi listile.</p>
			<div class="form-msg" data-contact-msg role="status" aria-live="polite" hidden></div>
			<button class="btn yel" type="submit" data-contact-go>Saada kiri →</button>
		</form>

		<aside class="contact-side">
			<div class="box">
				<h3>Rehvimüüjale</h3>
				<p class="note">Iga rehvi juures on koht müüjate hindadele — kalkulaatori tulemuses, rehvi valimisel ja võrdluses. Hinnad tulevad otse teie süsteemist (API või hinnafail) ja on alati koos lingiga teie poodi.</p>
				<p class="note" style="margin:0">Järjestust ega pidurdusmaad hind ei mõjuta — see jääb andmepõhiseks.</p>
			</div>
			<div class="box">
				<h3>Andmete kohta</h3>
				<p class="note" style="margin:0">Kui mõni rehv, mõõt või testitulemus on vale, kirjuta rehvi nimi ja mõõt — parandame. <a href="<?php echo esc_url( pm_url( 'teadmine/kuidas-pidurdusmaa-arvutatakse/' ) ); ?>">Kuidas arvutame</a></p>
			</div>
		</aside>
	</div>
</div>
<?php
get_footer();
