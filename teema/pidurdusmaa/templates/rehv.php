<?php
/**
 * /rehvid/<mudel>/ — ühe rehvimudeli leht.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
$ctx    = pm_ctx();
$t      = $ctx['tyre'];
$model  = $t['model'];
$tested = $t['tested'];
$sizes  = $model ? $model['sizes'] : array();
usort(
	$sizes,
	static function ( $a, $b ) {
		return strnatcmp( $a['m'], $b['m'] );
	}
);
$know = get_page_by_path( 'teadmine/rehvimargis' );

get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><span>/</span><a href="<?php echo esc_url( pm_url( 'rehvid/' ) ); ?>">Rehvid</a><span>/</span><?php echo esc_html( $t['name'] ); ?></div>
		<p class="eyebrow" style="color:var(--muted-d)"><?php echo esc_html( $t['brand'] ); ?></p>
		<h1><?php echo esc_html( $t['name'] ); ?></h1>
		<p><?php echo esc_html( PM_CAT_NAMES[ $t['cat'] ] ?? '' ); ?>
			<?php if ( $model && 0 === strpos( $model['katAlus'], 'OLETUS' ) ) : ?> · <span title="Märgisel on lumemärk, aga nimi ei ütle, kas talve- või lamellrehv">tüüp tuletatud</span><?php endif; ?>
		</p>
		<div class="pills">
			<?php if ( $model ) : ?><span class="pill off">EL-i märgis · <?php echo count( $sizes ); ?> mõõtu</span><?php endif; ?>
			<?php if ( $tested ) : ?><span class="pill test">Sõltumatult testitud</span><?php endif; ?>
		</div>
	</div>
</section>

<div class="body-sec">
	<div class="wrap cols">
		<div>
			<div class="box" data-tw data-slug="<?php echo esc_attr( $t['slug'] ); ?>" data-name="<?php echo esc_attr( $t['name'] ); ?>" data-cat="<?php echo esc_attr( $t['cat'] ); ?>"
				data-tested="<?php echo esc_attr( $tested['key'] ?? '' ); ?>"
				data-sizes="<?php echo esc_attr( wp_json_encode( array_map( static fn( $z ) => array( 'm' => $z['m'], 'g' => $z['g'] ), $sizes ) ) ); ?>">
				<h2>Pidurdusmaa sinu autoga</h2>
				<p class="sub">Auto: <span data-tw-veh>…</span></p>
				<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
					<div class="fld"><select class="lsel" data-tw-size aria-label="Rehvimõõt" style="min-width:220px"></select></div>
					<div class="lseg" role="group" aria-label="Teeolud">
						<?php foreach ( PM_CONDS as $k => $c ) : ?>
							<button type="button" data-tw-cond="<?php echo esc_attr( $k ); ?>" aria-pressed="<?php echo 'wet' === $k ? 'true' : 'false'; ?>"><?php echo esc_html( $c[0] ); ?></button>
						<?php endforeach; ?>
					</div>
				</div>
				<div data-tw-out><p class="note">Arvutan…</p></div>
			</div>

			<?php if ( $tested && $tested['tests'] ) : ?>
			<div class="box">
				<h2>Sõltumatud testid</h2>
				<p class="sub">Mõõdetud tulemused. Koht = järjekoht samas testis samal pinnal (1 = lühim pidurdusmaa).</p>
				<div class="tbl-wrap"><table class="t">
					<thead><tr><th>Test</th><th>Pind ja kiirus</th><th class="n">Tulemus</th><th class="n">Koht</th><th class="n">Parim</th></tr></thead>
					<tbody>
					<?php
					foreach ( $tested['tests'] as $x ) :
						$src = pm_source( $x['src'] );
						[ $pos, $n, $best ] = pm_rank_in_test( $x );
						?>
						<tr<?php echo 1 === $pos ? ' class="best"' : ''; ?>>
							<td><a href="<?php echo esc_url( pm_url( 'testid/' . pm_source_slug( $x['src'] ) . '/' ) ); ?>"><?php echo esc_html( $src['nimi'] ?? $x['src'] ); ?></a></td>
							<td><?php echo esc_html( pm_test_label( $x ) ); ?></td>
							<td class="n"><b><?php echo esc_html( pm_num( $x['m'] ) ); ?> m</b></td>
							<td class="n"><?php echo $pos ? esc_html( "$pos / $n" ) : '–'; ?></td>
							<td class="n"><?php echo null !== $best ? esc_html( pm_num( $best ) ) . ' m' : '–'; ?></td>
						</tr>
					<?php endforeach; ?>
					<?php if ( ! empty( $tested['aqua'] ) ) : ?>
						<tr><td><?php echo esc_html( pm_source( $tested['aqua']['src'] )['nimi'] ?? '' ); ?></td><td>akvaplaneerimise kiirus (suurem = parem)</td><td class="n"><b><?php echo esc_html( pm_num( $tested['aqua']['kmh'] ) ); ?> km/h</b></td><td class="n">–</td><td class="n">–</td></tr>
					<?php endif; ?>
					</tbody>
				</table></div>
				<p class="srcline">Test: <?php echo esc_html( $tested['size'] ); ?>. Sama rehv võib teises mõõdus olla veidi teistsugune.</p>
			</div>
			<?php endif; ?>

			<?php if ( $sizes ) : ?>
			<div class="box">
				<h2>EL-i rehvimärgis</h2>
				<p class="sub">Ametlikud andmed EL-i tooteregistrist EPREL, mõõdu kaupa. Klass on mõõdupõhine.<?php if ( $know ) : ?> <a href="<?php echo esc_url( get_permalink( $know ) ); ?>">Mida klassid tähendavad?</a><?php endif; ?></p>
				<div class="tbl-wrap"><table class="t">
					<thead><tr><th>Mõõt</th><th>Märghaardumine</th><th>Veeretakistus</th><th class="n">Müra</th><th>Talv</th><th>Koormus / kiirus</th></tr></thead>
					<tbody>
					<?php foreach ( $sizes as $z ) : ?>
						<tr>
							<td><?php $ss = pm_size_slug( $z['m'] ); echo $ss ? '<a href="' . esc_url( pm_url( 'rehvid/' . $ss . '/' ) ) . '">' . esc_html( pm_pretty_size( $z['m'] ) ) . '</a>' : esc_html( pm_pretty_size( $z['m'] ) ); ?></td>
							<td><?php echo pm_grade( $z['g'] ); // phpcs:ignore ?><?php if ( count( $z['gAll'] ) > 1 ) : ?> <span class="note" title="Eri koormus-/kiirusindeksiga variandid on eri klassiga; näidatud halvim">(variandid: <?php echo esc_html( implode( ', ', $z['gAll'] ) ); ?>)</span><?php endif; ?></td>
							<td><?php echo pm_grade( $z['f'] ); // phpcs:ignore ?></td>
							<td class="n"><?php echo $z['db'] ? esc_html( $z['db'] . ' dB' ) . ( $z['nk'] ? ' (' . esc_html( $z['nk'] ) . ')' : '' ) : '–'; ?></td>
							<td><?php echo esc_html( implode( ' + ', array_filter( array( $z['snow'] ? 'lumemärk' : '', $z['ice'] ? 'jäämärk' : '' ) ) ) ?: '–' ); ?></td>
							<td><?php echo esc_html( implode( '/', $z['li'] ) . ' ' . implode( '/', $z['si'] ) ); ?></td>
						</tr>
					<?php endforeach; ?>
					</tbody>
				</table></div>
			</div>
			<?php endif; ?>


			<?php
			$vs = pm_vs_links_for( $t['slug'] );
			if ( $vs ) :
				?>
				<div class="box">
					<h2>Võrdle samas testis</h2>
					<p class="sub">Rehvid, mis olid samas testis naabrid — sama auto, sama päev.</p>
					<div class="grid-cards">
					<?php
					foreach ( $vs as $p ) :
						$other = pm_tyre_page( $p[0] === $t['slug'] ? $p[1] : $p[0] );
						if ( ! $other ) {
							continue;
						}
						?>
						<a class="tcard" href="<?php echo esc_url( pm_url( 'rehvid/' . $p[0] . '-vs-' . $p[1] . '/' ) ); ?>"><span class="b">vs</span><h3><?php echo esc_html( $other['name'] ); ?></h3><span class="meta">Mõõdetud pidurdusmaad kõrvuti →</span></a>
					<?php endforeach; ?>
					</div>
				</div>
			<?php endif; ?>
		</div>

		<aside class="side">
			<div class="box">
				<div class="tyre-img" role="img" aria-label="Rehvi illustratsioon"><?php echo pm_tyre_art(); // phpcs:ignore ?></div>
				<p class="srcline" style="text-align:center">Illustratsioon. Tootja pilte ei kasutata.</p>
				<?php if ( $sizes ) : ?>
					<button type="button" class="btn yel" style="width:100%;margin-top:14px" data-tw-add>Võrdle seda rehvi →</button>
					<h3 style="font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:22px 0 8px">Mõõdud andmebaasis</h3>
					<div class="sizes-list">
						<?php foreach ( $sizes as $z ) : ?>
							<?php $ss = pm_size_slug( $z['m'] ); ?>
							<?php if ( $ss ) : ?><a href="<?php echo esc_url( pm_url( 'rehvid/' . $ss . '/' ) ); ?>"><?php echo esc_html( pm_pretty_size( $z['m'] ) ); ?></a><?php endif; ?>
						<?php endforeach; ?>
					</div>
					<p class="srcline">Andmebaasis on praegu ainult osa mõõtudest. Mudel võib olla müügil ka teistes.</p>
				<?php endif; ?>
			</div>
		</aside>
	</div>
</div>
<?php
get_template_part( 'template-parts/how' );
get_footer();
