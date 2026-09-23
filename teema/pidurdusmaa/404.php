<?php
/**
 * 404.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<h1>Lehte ei leitud</h1>
		<p>Seda lehte ei ole — või on see rehv või mõõt, mille andmeid meil veel ei ole.</p>
		<p style="margin-top:20px"><a class="btn yel" href="<?php echo esc_url( home_url( '/' ) ); ?>">Arvuta pidurdusmaa →</a> <a class="btn" style="background:transparent;color:#fff;border-color:#2b3039" href="<?php echo esc_url( pm_url( 'rehvid/' ) ); ?>">Sirvi rehve</a></p>
	</div>
</section>
<?php
get_footer();
