<?php
/**
 * Sitemap: ainult indekseeritavad virtuaalsed lehed (vt pm_indexable).
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;

class PM_Sitemap_Provider extends WP_Sitemaps_Provider {
	public function __construct() {
		$this->name        = 'pidurdusmaa';
		$this->object_type = 'pidurdusmaa';
	}

	public function get_object_subtypes() {
		return array(
			'lehed'  => (object) array( 'name' => 'lehed' ),
			'rehvid' => (object) array( 'name' => 'rehvid' ),
		);
	}

	private function urls( string $sub ): array {
		$out = array();
		if ( 'lehed' === $sub ) {
			foreach ( array( 'rehvi-valimine/', 'vordle-rehve/', 'rehvid/', 'testid/', 'kontakt/' ) as $p ) {
				$out[] = pm_url( $p );
			}
			foreach ( pm_core()['sources'] as $code => $s ) {
				$out[] = pm_url( 'testid/' . pm_source_slug( $code ) . '/' );
			}
			foreach ( pm_core()['sizes'] as $s ) {
				if ( pm_size_model_count( $s['m'] ) >= PM_SIZE_MIN_MODELS ) {
					$out[] = pm_url( 'rehvid/' . $s['slug'] . '/' );
				}
			}
			foreach ( pm_vs_pairs() as $p ) {
				$out[] = pm_url( 'rehvid/' . $p[0] . '-vs-' . $p[1] . '/' );
			}
			return $out;
		}
		$seen = array();
		foreach ( pm_core()['tyres'] as $t ) {
			$seen[ $t['slug'] ] = true;
		}
		foreach ( pm_models() as $slug => $m ) {
			if ( ! empty( $m['tested'] ) || count( $m['sizes'] ) >= 3 ) {
				$seen[ $slug ] = true;
			}
		}
		foreach ( array_keys( $seen ) as $slug ) {
			$out[] = pm_tyre_url( $slug );
		}
		return $out;
	}

	public function get_url_list( $page_num, $object_subtype = '' ) {
		$all  = $this->urls( $object_subtype ?: 'lehed' );
		$size = wp_sitemaps_get_max_urls( $this->object_type );
		$page = array_slice( $all, ( $page_num - 1 ) * $size, $size );
		return array_map(
			static function ( $u ) {
				return array( 'loc' => $u );
			},
			$page
		);
	}

	public function get_max_num_pages( $object_subtype = '' ) {
		return (int) ceil( count( $this->urls( $object_subtype ?: 'lehed' ) ) / wp_sitemaps_get_max_urls( $this->object_type ) );
	}
}

