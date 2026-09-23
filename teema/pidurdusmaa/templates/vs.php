<?php
/**
 * /rehvid/a-vs-b/ — kaks rehvi SAMAS testis. Ainult mõõdetud arvud.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
$ctx = pm_ctx();
$a   = $ctx['a'];
$b   = $ctx['b'];
get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><span>/</span><a href="<?php echo esc_url( pm_url( 'rehvid/' ) ); ?>">Rehvid</a><span>/</span>Võrdlus</div>
		<h1><?php echo esc_html( $a['name'] ); ?> <span style="color:var(--yellow)">vs</span> <?php echo esc_html( $b['name'] ); ?></h1>
		<p>Mõlemad rehvid olid samas sõltumatus testis — sama auto, sama rada, sama päev. Siin on ainult mõõdetud tulemused.</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<?php
		foreach ( $ctx['shared'] as $code ) :
			$src = pm_source( $code );
			$ta  = array_values( array_filter( $a['tested']['tests'], static fn( $x ) => $x['src'] === $code ) );
			?>
			<div class="box">
				<h2><?php echo esc_html( $src['nimi'] ); ?></h2>
				<p class="sub"><?php echo esc_html( $src['moot'] . ' · ' . $src['auto'] . ' · ' . $src['tegija'] ); ?></p>
				<div class="tbl-wrap"><table class="t">
					<thead><tr><th>Pind ja kiirus</th><th class="n"><?php echo esc_html( $a['name'] ); ?></th><th class="n"><?php echo esc_html( $b['name'] ); ?></th><th class="n">Vahe</th></tr></thead>
					<tbody>
					<?php
					foreach ( $ta as $x ) :
						$y = null;
						foreach ( $b['tested']['tests'] as $z ) {
							if ( $z['src'] === $code && $z['surf'] === $x['surf'] && $z['wet'] === $x['wet'] && $z['v0'] === $x['v0'] ) {
								$y = $z;
							}
						}
						if ( ! $y ) {
							continue;
						}
						$d = $y['m'] - $x['m'];
						?>
						<tr>
							<td><?php echo esc_html( pm_test_label( $x ) ); ?></td>
							<td class="n"<?php echo $x['m'] < $y['m'] ? ' style="font-weight:700;box-shadow:inset 0 -3px 0 var(--yellow)"' : ''; ?>><?php echo esc_html( pm_num( $x['m'] ) ); ?> m</td>
							<td class="n"<?php echo $y['m'] < $x['m'] ? ' style="font-weight:700;box-shadow:inset 0 -3px 0 var(--yellow)"' : ''; ?>><?php echo esc_html( pm_num( $y['m'] ) ); ?> m</td>
							<td class="n"><?php echo esc_html( ( $d > 0 ? '+' : '' ) . pm_num( $d ) ); ?> m <span class="note">(<?php echo esc_html( ( $d > 0 ? '+' : '' ) . pm_num( 100 * $d / min( $x['m'], $y['m'] ), abs( 100 * $d / min( $x['m'], $y['m'] ) ) < 10 ? 1 : 0 ) ); ?> %)</span></td>
						</tr>
					<?php endforeach; ?>
					</tbody>
				</table></div>
				<p class="srcline">Allikas: <a href="<?php echo esc_url( $src['kajastus'] ); ?>" rel="nofollow noopener"><?php echo esc_html( $src['nimi'] ); ?></a>. Vahe = teine miinus esimene, protsent lühemast; lühem on parem.</p>
			</div>
		<?php endforeach; ?>
		<div class="box">
			<h2>Rehvide lehed</h2>
			<p>Märgise andmed kõigis mõõtudes ja arvutatud pidurdusmaa sinu autoga.</p>
			<p><a class="btn" href="<?php echo esc_url( pm_tyre_url( $a['slug'] ) ); ?>"><?php echo esc_html( $a['name'] ); ?> →</a> <a class="btn" href="<?php echo esc_url( pm_tyre_url( $b['slug'] ) ); ?>"><?php echo esc_html( $b['name'] ); ?> →</a></p>
		</div>
	</div>
</div>
<?php
get_footer();
