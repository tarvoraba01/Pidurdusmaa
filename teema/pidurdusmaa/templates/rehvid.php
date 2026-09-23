<?php
/**
 * /rehvid/ — mõõdud, testitud rehvid, margid.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
$core   = pm_core();
$sizes  = array_filter( $core['sizes'], static fn( $s ) => pm_size_model_count( $s['m'] ) >= PM_SIZE_MIN_MODELS );
usort( $sizes, static fn( $a, $b ) => strnatcmp( $a['label'], $b['label'] ) );
$tested = $core['tyres'];
usort( $tested, static fn( $a, $b ) => strcmp( $a['category'], $b['category'] ) ?: strcmp( $a['name'], $b['name'] ) );
$brands = array();
foreach ( pm_models() as $slug => $m ) {
	$brands[ pm_title_case( $m['mark'] ) ][] = array( $slug, pm_title_case( $m['nimi'] ), count( $m['sizes'] ) );
}
ksort( $brands, SORT_NATURAL | SORT_FLAG_CASE );
get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><span>/</span>Rehvid</div>
		<h1>Rehvid</h1>
		<p><?php echo esc_html( number_format( count( pm_models() ), 0, ',', ' ' ) ); ?> rehvimudelit EL-i rehvimärgisega ja <?php echo count( $tested ); ?> rehvi sõltumatutes testides. Vali mõõt, et näha kõiki selle mõõdu rehve.</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="box">
			<h2>Mõõdu järgi</h2>
			<p class="sub">Andmebaasis olevad mõõdud. Korje laieneb — kui sinu mõõtu pole, on andmed alles tulemas.</p>
			<div class="sizes-list">
				<?php foreach ( $sizes as $s ) : ?>
					<a href="<?php echo esc_url( pm_url( 'rehvid/' . $s['slug'] . '/' ) ); ?>"><?php echo esc_html( $s['label'] ); ?> <span class="note">· <?php echo (int) pm_size_model_count( $s['m'] ); ?></span></a>
				<?php endforeach; ?>
			</div>
		</div>
		<div class="box">
			<h2>Sõltumatult testitud</h2>
			<p class="sub">Neil rehvidel on mõõdetud pidurdusmaad — täpsemad kui märgise klass.</p>
			<div class="grid-cards">
				<?php foreach ( $tested as $t ) : ?>
					<a class="tcard" href="<?php echo esc_url( pm_tyre_url( $t['slug'] ) ); ?>">
						<span class="b"><?php echo esc_html( PM_CAT_NAMES[ $t['category'] ] ?? '' ); ?></span>
						<h3><?php echo esc_html( $t['name'] ); ?></h3>
						<span class="meta"><?php echo esc_html( implode( ', ', array_unique( array_map( static fn( $x ) => pm_source( $x['src'] )['nimi'] ?? $x['src'], $t['tests'] ) ) ) ); ?></span>
					</a>
				<?php endforeach; ?>
			</div>
		</div>
		<div class="box">
			<h2>Margi järgi</h2>
			<?php foreach ( $brands as $b => $list ) : ?>
				<details style="border-top:1px solid var(--paper-3);padding:10px 0">
					<summary style="cursor:pointer;font-weight:600"><?php echo esc_html( $b ); ?> <span class="note">· <?php echo count( $list ); ?> mudelit</span></summary>
					<div class="sizes-list" style="margin-top:10px">
						<?php
						usort( $list, static fn( $x, $y ) => strnatcasecmp( $x[1], $y[1] ) );
						foreach ( $list as $m ) :
							?>
							<a href="<?php echo esc_url( pm_tyre_url( $m[0] ) ); ?>"><?php echo esc_html( $m[1] ); ?></a>
						<?php endforeach; ?>
					</div>
				</details>
			<?php endforeach; ?>
		</div>
	</div>
</div>
<?php
get_footer();
