<?php
/**
 * Rehvipaarid, millel on oma võrdlusleht.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;

/**
 * "vs" paarid, millel on päris sisu: kaks rehvi SAMAS testis, naabrid
 * märja pidurduse järjestuses (mitte kõik 31×30 kombinatsiooni).
 */
function pm_vs_pairs(): array {
	static $pairs = null;
	if ( null !== $pairs ) {
		return $pairs;
	}
	$pairs = array();
	$by    = array();
	foreach ( pm_core()['tyres'] as $t ) {
		foreach ( $t['tests'] as $x ) {
			if ( 'ASPHALT' === $x['surf'] && $x['wet'] ) {
				$by[ $x['src'] ][] = array( $t['slug'], $x['m'] );
			}
		}
	}
	foreach ( $by as $list ) {
		usort(
			$list,
			static function ( $a, $b ) {
				return $a[1] <=> $b[1];
			}
		);
		for ( $i = 0; $i + 1 < count( $list ); $i++ ) {
			$a = $list[ $i ][0];
			$b = $list[ $i + 1 ][0];
			$k = $a < $b ? array( $a, $b ) : array( $b, $a );
			$pairs[ $k[0] . '|' . $k[1] ] = $k;
		}
	}
	$pairs = array_values( $pairs );
	return $pairs;
}

/** Rehvilehe "vs" lingid: naabrid samas testis. */
function pm_vs_links_for( string $slug ): array {
	$out = array();
	foreach ( pm_vs_pairs() as $p ) {
		if ( $p[0] === $slug || $p[1] === $slug ) {
			$out[] = $p;
		}
	}
	return $out;
}
