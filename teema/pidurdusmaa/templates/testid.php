<?php
/**
 * /testid/ — sõltumatud testid.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
$core = pm_core();
get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><span>/</span>Testid</div>
		<h1>Sõltumatud testid</h1>
		<p>Testid, mille mõõdetud tulemusi Pidurdusmaa.ee kasutab. Igal testil on allikas, aasta, auto, rehvimõõt ja protokoll. Me ei korralda teste ise.</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="grid-cards" style="grid-template-columns:repeat(auto-fill,minmax(340px,1fr))">
			<?php foreach ( $core['sources'] as $code => $s ) : ?>
				<a class="tcard" href="<?php echo esc_url( pm_url( 'testid/' . pm_source_slug( $code ) . '/' ) ); ?>" style="padding:20px">
					<span class="b"><?php echo esc_html( $s['tegija'] ); ?> · <?php echo (int) $s['aasta']; ?></span>
					<h3 style="font-size:20px"><?php echo esc_html( $s['nimi'] ); ?></h3>
					<span class="meta"><?php echo (int) $s['rehve']; ?> rehvi · <?php echo esc_html( $s['moot'] ); ?> · <?php echo esc_html( $s['auto'] ); ?></span>
					<p class="note" style="margin:10px 0 0"><?php echo esc_html( $s['protokoll'] ); ?></p>
				</a>
			<?php endforeach; ?>
		</div>
		<div class="box" style="margin-top:24px">
			<h2>Kuidas teste kasutatakse</h2>
			<ul>
				<li>Testi mõõdetud märja pidurduse järgi tuletatakse rehvi märghaardumise indeks — see on täpsem kui märgise klass.</li>
				<li>Kuiva, lume ja jää tulemused kalibreerivad mudeli rehvikategooriate kaupa.</li>
				<li>Vi Bilägare 2010 testid on mudeli kontrolliks: mudel ei näinud neid kalibreerimisel.</li>
				<li>Testi tulemus kehtib testi mõõdus ja autol. Teises mõõdus võib sama rehv olla veidi teistsugune.</li>
			</ul>
		</div>
	</div>
</div>
<?php
get_footer();
