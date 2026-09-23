<?php
/**
 * Virtuaalsed lehed: /pidurdusmaa/, /vordle-rehve/, /rehvid/…, /testid/…
 *
 * Miks mitte custom post type: siis oleks rehvide andmed kahes kohas
 * (andmebaasis ja data/*.json-is) ja nad triiviksid lahku. Nii on üks
 * allikas ja iga leht renderdatakse sellest serveris — otsingumootor
 * näeb päris sisu, mitte tühja JS-kesta.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;

function pm_register_routes() {
	add_rewrite_rule( '^pidurdusmaa/?$', 'index.php?pm_view=kalkulaator', 'top' );
	add_rewrite_rule( '^vordle-rehve/?$', 'index.php?pm_view=vordle', 'top' );
	add_rewrite_rule( '^rehvi-valimine/?$', 'index.php?pm_view=valik', 'top' );
	add_rewrite_rule( '^rehvid/?$', 'index.php?pm_view=rehvid', 'top' );
	add_rewrite_rule( '^rehvid/([a-z0-9-]+)-vs-([a-z0-9-]+)/?$', 'index.php?pm_view=vs&pm_a=$matches[1]&pm_b=$matches[2]', 'top' );
	add_rewrite_rule( '^rehvid/([a-z0-9-]+)/?$', 'index.php?pm_view=rehv&pm_slug=$matches[1]', 'top' );
	add_rewrite_rule( '^testid/?$', 'index.php?pm_view=testid', 'top' );
	add_rewrite_rule( '^testid/([a-z0-9-]+)/?$', 'index.php?pm_view=test&pm_slug=$matches[1]', 'top' );
	add_rewrite_rule( '^kontakt/?$', 'index.php?pm_view=kontakt', 'top' );
}
add_action( 'init', 'pm_register_routes' );

/* Kui teema uuendusega lisandub URL, värskendatakse reeglid ise — muidu
   jääks uus leht 404-ks, kuni keegi käsitsi püsiviited salvestab. */
const PM_RULES_VER = '3';
add_action(
	'init',
	static function () {
		if ( get_option( 'pm_rules_ver' ) !== PM_RULES_VER ) {
			flush_rewrite_rules( false );
			update_option( 'pm_rules_ver', PM_RULES_VER );
		}
	},
	99
);

add_filter(
	'query_vars',
	static function ( $v ) {
		return array_merge( $v, array( 'pm_view', 'pm_slug', 'pm_a', 'pm_b' ) );
	}
);

/** Aktiivse virtuaalse lehe kontekst (arvutatakse üks kord). */
function pm_ctx(): array {
	static $ctx = null;
	if ( null !== $ctx ) {
		return $ctx;
	}
	$view = get_query_var( 'pm_view' );
	$ctx  = array( 'view' => $view );
	if ( ! $view ) {
		return $ctx;
	}
	$slug = (string) get_query_var( 'pm_slug' );
	switch ( $view ) {
		case 'rehv':
			$size = pm_size_by_slug( $slug );
			if ( $size ) {
				$ctx['view'] = 'moot';
				$ctx['size'] = $size;
			} else {
				$ctx['tyre'] = pm_tyre_page( $slug );
				if ( ! $ctx['tyre'] ) {
					$ctx['404'] = true;
				}
			}
			break;
		case 'vs':
			// Mõne rehvi nimes endas on „vs“ (nt Maxxis VS-EV → maxxis-vs-ev).
			// Kui selline rehvileht on olemas, on see rehvileht, mitte võrdlus.
			$whole = pm_tyre_page( get_query_var( 'pm_a' ) . '-vs-' . get_query_var( 'pm_b' ) );
			if ( $whole ) {
				$ctx['view'] = 'rehv';
				$ctx['tyre'] = $whole;
				break;
			}
			$a = pm_tyre_page( (string) get_query_var( 'pm_a' ) );
			$b = pm_tyre_page( (string) get_query_var( 'pm_b' ) );
			$shared = ( $a && $b ) ? pm_shared_sources( $a, $b ) : array();
			if ( ! $shared ) {
				// Ainult sama testi rehvid saavad oma "vs" lehe — muidu oleks
				// see kahe märgise kõrvutus, mida võrdlustööriist teeb paremini.
				$ctx['404'] = true;
			} else {
				$ctx += array( 'a' => $a, 'b' => $b, 'shared' => $shared );
			}
			break;
		case 'test':
			$code = strtoupper( $slug );
			$src  = pm_source( $code );
			if ( ! $src ) {
				$ctx['404'] = true;
			} else {
				$ctx['code']   = $code;
				$ctx['source'] = $src;
			}
			break;
	}
	return $ctx;
}

/** Mõõdetud testid, kus mõlemad rehvid olid KOOS (sama auto, sama päev). */
function pm_shared_sources( array $a, array $b ): array {
	if ( empty( $a['tested'] ) || empty( $b['tested'] ) || $a['slug'] === $b['slug'] ) {
		return array();
	}
	$sa = array_unique( array_column( $a['tested']['tests'], 'src' ) );
	$sb = array_unique( array_column( $b['tested']['tests'], 'src' ) );
	return array_values( array_intersect( $sa, $sb ) );
}

add_action(
	'template_redirect',
	static function () {
		$ctx = pm_ctx();
		if ( empty( $ctx['view'] ) ) {
			return;
		}
		if ( 'kalkulaator' === $ctx['view'] ) {
			// Kalkulaator ON avaleht — vana aadress suunatakse sinna.
			wp_safe_redirect( home_url( '/' ), 301 );
			exit;
		}
		if ( ! empty( $ctx['404'] ) ) {
			global $wp_query;
			$wp_query->set_404();
			status_header( 404 );
			nocache_headers();
			return;
		}
		status_header( 200 );
		global $wp_query;
		// NB: EI märgi is_page/is_singular — virtuaalsel lehel ei ole postitust
		// ja WordPress hakkaks body_class'is olematut postitust lugema.
		$wp_query->is_home = false;
		$wp_query->is_404  = false;
	},
	1
);

// /rehvid/x/ ei tohi WordPress "parandada" mõneks postituseks.
add_filter(
	'redirect_canonical',
	static function ( $url ) {
		return get_query_var( 'pm_view' ) ? false : $url;
	}
);

add_filter(
	'template_include',
	static function ( $tpl ) {
		$ctx = pm_ctx();
		if ( empty( $ctx['view'] ) || ! empty( $ctx['404'] ) ) {
			return $tpl;
		}
		$map  = array(
			'vordle'      => 'vordle',
			'valik'       => 'valik',
			'rehvid'      => 'rehvid',
			'rehv'        => 'rehv',
			'moot'        => 'moot',
			'vs'          => 'vs',
			'testid'      => 'testid',
			'test'        => 'test',
			'kontakt'     => 'kontakt',
		);
		$file = get_template_directory() . '/templates/' . ( $map[ $ctx['view'] ] ?? '' ) . '.php';
		return is_readable( $file ) ? $file : $tpl;
	},
	99
);

add_action(
	'after_switch_theme',
	static function () {
		pm_register_routes();
		flush_rewrite_rules();
	}
);

add_filter(
	'body_class',
	static function ( $c ) {
		$v = get_query_var( 'pm_view' );
		if ( ! $v ) {
			return $c;
		}
		$c = array_filter( $c, static fn( $x ) => ! preg_match( '/^(page-id-|page-template|post-template|wp-singular|page|blog|home)$|^(page-id-|page-template)/', $x ) );
		$c[] = 'pm-view-' . sanitize_html_class( pm_ctx()['view'] ?? $v );
		return $c;
	}
);
