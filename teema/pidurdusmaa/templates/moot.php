<?php
/**
 * /rehvid/205-55-r16/ — kõik ühe mõõdu rehvid märgise järgi.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
$ctx  = pm_ctx();
$size = $ctx['size'];
$rows = pm_eprel_size( $size['m'] );
$cats = array( 0 => 'Suverehvid', 1 => 'Lamellrehvid', 2 => 'Talverehvid (Kesk-Euroopa)', 3 => 'Talverehvid (Põhjamaade)' );
$by   = array();
foreach ( $rows as $r ) {
	$by[ $r[3] ][] = $r;
}
ksort( $by );
$cls = array_count_values( array_column( $rows, 4 ) );
ksort( $cls );
$cars = array_filter( pm_core()['vehicles'], static fn( $v ) => str_replace( array( '/', ' ' ), '', strtoupper( $v['oemSize'] ) ) === $size['m'] );
get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><span>/</span><a href="<?php echo esc_url( pm_url( 'rehvid/' ) ); ?>">Rehvid</a><span>/</span><?php echo esc_html( $size['label'] ); ?></div>
		<h1>Rehvid <?php echo esc_html( $size['label'] ); ?></h1>
		<p><?php echo count( $rows ); ?> rehvimudelit EL-i rehvimärgise andmetega. Märghaardumise klass ütleb, kui lühikeseks jääb pidurdusmaa märjal teel — ja klass on selle mõõdu oma, mitte mudeli üldine.</p>
		<div class="pills">
			<?php foreach ( $cls as $g => $n ) : ?>
				<span class="pill"><?php echo pm_grade( $g ); // phpcs:ignore ?> <?php echo (int) $n; ?> rehvi</span>
			<?php endforeach; ?>
		</div>
	</div>
</section>
<div class="body-sec">
	<div class="wrap cols">
		<div>
			<?php foreach ( $by as $ci => $list ) : ?>
				<div class="box">
					<h2><?php echo esc_html( $cats[ $ci ] ?? '' ); ?></h2>
					<p class="sub"><?php echo count( $list ); ?> mudelit · järjestatud märghaardumise klassi, siis müra järgi</p>
					<div class="tbl-wrap"><table class="t">
						<thead><tr><th>Rehv</th><th>Märghaare</th><th>Veeretakistus</th><th class="n">Müra</th><th>Test</th></tr></thead>
						<tbody>
						<?php
						usort(
							$list,
							static function ( $a, $b ) {
								return strcmp( $a[4], $b[4] ) ?: ( ( $a[6] ?? 99 ) <=> ( $b[6] ?? 99 ) );
							}
						);
						foreach ( $list as $r ) :
							?>
							<tr>
								<td><a href="<?php echo esc_url( pm_tyre_url( $r[0] ) ); ?>"><?php echo esc_html( pm_title_case( $r[1] . ' ' . $r[2] ) ); ?></a></td>
								<td><?php echo pm_grade( $r[4] ); // phpcs:ignore ?></td>
								<td><?php echo pm_grade( $r[5] ); // phpcs:ignore ?></td>
								<td class="n"><?php echo $r[6] ? esc_html( $r[6] . ' dB' ) : '–'; ?></td>
								<td><?php echo $r[9] ? '<span class="pill test">Testitud</span>' : '<span class="note">–</span>'; ?></td>
							</tr>
						<?php endforeach; ?>
						</tbody>
					</table></div>
				</div>
			<?php endforeach; ?>
		</div>
		<aside class="side">
			<div class="box">
				<h2 style="font-size:22px">Pidurdusmaa selles mõõdus</h2>
				<p class="note">Arvuta, kui palju muudab märghaardumise klass sinu auto pidurdusmaad.</p>
				<a class="btn yel" style="width:100%" href="<?php echo esc_url( add_query_arg( 'moot', $size['m'], home_url( '/' ) ) ); ?>">Arvuta selle mõõduga →</a>
				<a class="btn" style="width:100%;margin-top:8px" href="<?php echo esc_url( pm_url( 'vordle-rehve/?moot=' . $size['m'] ) ); ?>">Võrdle selle mõõdu rehve</a>
				<?php if ( $cars ) : ?>
					<h3 style="font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:22px 0 8px">Tehase mõõt näiteks</h3>
					<ul class="note" style="margin:0;padding-left:18px">
						<?php foreach ( array_slice( $cars, 0, 12 ) as $v ) : ?><li><?php echo esc_html( $v['name'] ); ?></li><?php endforeach; ?>
					</ul>
				<?php endif; ?>
			</div>
		</aside>
	</div>
</div>
<?php
get_footer();
