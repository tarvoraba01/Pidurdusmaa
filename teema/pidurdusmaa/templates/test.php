<?php
/**
 * /testid/<kood>/ — ühe testi tulemused.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
$ctx  = pm_ctx();
$code = $ctx['code'];
$src  = $ctx['source'];
$core = pm_core();

/* Veerud: kõik selles testis mõõdetud pind+kiirus kombinatsioonid */
$cols = array();
$rows = array();
foreach ( $core['tyres'] as $t ) {
	foreach ( $t['tests'] as $x ) {
		if ( $x['src'] !== $code ) {
			continue;
		}
		$k          = $x['surf'] . '|' . ( $x['wet'] ? 1 : 0 ) . '|' . $x['v0'] . '|' . $x['v1'];
		$cols[ $k ] = pm_test_label( $x );
		$rows[ $t['key'] ]['t']       = $t;
		$rows[ $t['key'] ]['v'][ $k ] = $x['m'];
	}
}
$vib = $core['vib'][ $code ] ?? null;
$wetk = null;
foreach ( array_keys( $cols ) as $k ) {
	if ( 0 === strpos( $k, 'ASPHALT|1' ) ) {
		$wetk = $k;
	}
}
if ( $wetk ) {
	uasort( $rows, static fn( $a, $b ) => ( $a['v'][ $wetk ] ?? 999 ) <=> ( $b['v'][ $wetk ] ?? 999 ) );
}
$best = array();
foreach ( array_keys( $cols ) as $k ) {
	$vals       = array_filter( array_map( static fn( $r ) => $r['v'][ $k ] ?? null, $rows ) );
	$best[ $k ] = $vals ? min( $vals ) : null;
}
get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><span>/</span><a href="<?php echo esc_url( pm_url( 'testid/' ) ); ?>">Testid</a><span>/</span><?php echo esc_html( $src['nimi'] ); ?></div>
		<p class="eyebrow" style="color:var(--muted-d)"><?php echo esc_html( $src['tegija'] ); ?> · <?php echo (int) $src['aasta']; ?></p>
		<h1><?php echo esc_html( $src['nimi'] ); ?></h1>
		<p><?php echo (int) $src['rehve']; ?> rehvi · <?php echo esc_html( $src['moot'] ); ?> · <?php echo esc_html( $src['auto'] ); ?></p>
		<div class="pills"><span class="pill test">Sõltumatu test</span><span class="pill"><?php echo esc_html( $src['protokoll'] ); ?></span></div>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<?php if ( $rows ) : ?>
			<div class="box">
				<h2>Tulemused</h2>
				<p class="sub">Pidurdusmaa meetrites (lühem = parem)<?php echo $wetk ? ', järjestatud märja asfaldi järgi' : ''; ?>. Kollane = parim veerus.</p>
				<div class="tbl-wrap"><table class="t">
					<thead><tr><th>#</th><th>Rehv</th><?php foreach ( $cols as $c ) : ?><th class="n"><?php echo esc_html( $c ); ?></th><?php endforeach; ?></tr></thead>
					<tbody>
					<?php
					$i = 0;
					foreach ( $rows as $r ) :
						?>
						<tr><td><?php echo ++$i; ?></td><td><a href="<?php echo esc_url( pm_tyre_url( $r['t']['slug'] ) ); ?>"><?php echo esc_html( $r['t']['name'] ); ?></a></td>
						<?php foreach ( array_keys( $cols ) as $k ) : ?>
							<?php $v = $r['v'][ $k ] ?? null; ?>
							<td class="n"<?php echo ( null !== $v && $v === $best[ $k ] ) ? ' style="font-weight:700;box-shadow:inset 0 -3px 0 var(--yellow)"' : ''; ?>><?php echo null !== $v ? esc_html( pm_num( $v ) ) : '–'; ?></td>
						<?php endforeach; ?></tr>
					<?php endforeach; ?>
					</tbody>
				</table></div>
			</div>
		<?php elseif ( $vib ) : ?>
			<div class="box">
				<h2>Tulemused</h2>
				<p class="sub">Pidurdusmaa meetrites. Neid rehve mudeli rehvinimekirjas ei ole — test on kasutusel mudeli kontrollina.</p>
				<div class="tbl-wrap"><table class="t">
					<thead><tr><th>Rehv</th><?php foreach ( $vib['cols'] as $c ) : ?><th class="n"><?php echo esc_html( $c ); ?></th><?php endforeach; ?></tr></thead>
					<tbody><?php foreach ( $vib['rows'] as $r ) : ?><tr><td><?php echo esc_html( $r[0] ); ?></td><?php foreach ( array_slice( $r, 1 ) as $v ) : ?><td class="n"><?php echo esc_html( pm_num( $v ) ); ?></td><?php endforeach; ?></tr><?php endforeach; ?></tbody>
				</table></div>
			</div>
		<?php endif; ?>
		<div class="box">
			<h2>Allikas</h2>
			<dl class="dl">
				<dt>Tegija</dt><dd><?php echo esc_html( $src['tegija'] ); ?></dd>
				<dt>Aasta</dt><dd><?php echo (int) $src['aasta']; ?></dd>
				<dt>Rehvimõõt</dt><dd><?php echo esc_html( $src['moot'] ); ?></dd>
				<dt>Testiauto</dt><dd><?php echo esc_html( $src['auto'] ); ?></dd>
				<dt>Protokoll</dt><dd style="text-align:right;font-weight:500"><?php echo esc_html( $src['protokoll'] ); ?></dd>
			</dl>
			<?php if ( ! empty( $src['markus'] ) ) : ?><p class="note-box"><?php echo esc_html( $src['markus'] ); ?></p><?php endif; ?>
			<p class="srcline">Kajastus: <a href="<?php echo esc_url( $src['kajastus'] ); ?>" rel="nofollow noopener"><?php echo esc_html( wp_parse_url( $src['kajastus'], PHP_URL_HOST ) ); ?></a></p>
		</div>
	</div>
</div>
<?php
get_footer();
