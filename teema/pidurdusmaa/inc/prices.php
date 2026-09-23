<?php
/**
 * Rehvide hinnad müüjatelt.
 *
 * Teema ise hindu EI tea. Siin on ainult ühenduskoht: REST-otspunkt
 * /wp-json/pm/v1/hinnad?ids=slug@MOOT,slug@MOOT (rehvikaardid, võrdlus) või
 * /wp-json/pm/v1/hinnad?moot=20555R16 (kalkulaatori tulemus: kõik ühe mõõdu
 * rehvid korraga), mida leht küsib, ja filter
 * `pm_hinnad`, mille kaudu müüjate API-ühendus (eraldi plugin või
 * mu-plugin) hinnad annab. API võtmed hoitakse serveris — mitte kunagi
 * teemas ega brauseris.
 *
 * Filtri kuju:
 *   add_filter( 'pm_hinnad', function ( array $out, array $ids, string $moot ) {
 *       // $ids  = [ 'michelin-primacy-5@20555R16', ... ]  (või tühi)
 *       // $moot = '20555R16' (või tühi) — siis anna kõik selle mõõdu rehvid
 *       $out['michelin-primacy-5@20555R16'] = [
 *           [ 'myyja' => 'Rehvipood OÜ', 'hind' => 89.90, 'url' => 'https://…', 'laos' => true ],
 *       ];
 *       return $out;
 *   }, 10, 3 );
 *
 * Kui ükski ühendus filtrit ei kasuta, vastab otspunkt `available: false`
 * ja leht näitab „Hinnad pole hetkel saadaval“.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;

add_action(
	'rest_api_init',
	static function () {
		register_rest_route(
			'pm/v1',
			'/hinnad',
			array(
				'methods'             => 'GET',
				'permission_callback' => '__return_true',
				'args'                => array(
					'ids'  => array(
						'type'    => 'string',
						'default' => '',
					),
					'moot' => array(
						'type'    => 'string',
						'default' => '',
					),
				),
				'callback'            => 'pm_rest_hinnad',
			)
		);
	}
);

/**
 * @param WP_REST_Request $req Päring.
 */
function pm_rest_hinnad( $req ) {
	$ids = array_slice( array_filter( array_map( 'trim', explode( ',', (string) $req['ids'] ) ) ), 0, 40 );
	$ids  = array_values( array_filter( $ids, static fn( $x ) => (bool) preg_match( '/^[a-z0-9-]{1,120}@[0-9A-Z]{5,12}$/', $x ) ) );
	$moot = preg_match( '/^[0-9A-Z]{5,12}$/', (string) $req['moot'] ) ? (string) $req['moot'] : '';
	$available = has_filter( 'pm_hinnad' );
	$out       = array();
	if ( $available && ( $ids || $moot ) ) {
		$key = 'pm_h_' . md5( $moot . '|' . implode( ',', $ids ) );
		$out = get_transient( $key );
		if ( ! is_array( $out ) ) {
			$raw = (array) apply_filters( 'pm_hinnad', array(), $ids, $moot );
			$out = array();
			$keys = $ids ? $ids : array_slice( array_filter( array_keys( $raw ), static fn( $x ) => is_string( $x ) && (bool) preg_match( '/^[a-z0-9-]{1,120}@' . $moot . '$/', $x ) ), 0, 600 );
			foreach ( $keys as $id ) {
				foreach ( (array) ( $raw[ $id ] ?? array() ) as $row ) {
					if ( empty( $row['myyja'] ) || ! isset( $row['hind'] ) || ! is_numeric( $row['hind'] ) ) {
						continue;
					}
					$out[ $id ][] = array(
						'myyja' => sanitize_text_field( $row['myyja'] ),
						'hind'  => round( (float) $row['hind'], 2 ),
						'url'   => isset( $row['url'] ) ? esc_url_raw( $row['url'] ) : '',
						'laos'  => isset( $row['laos'] ) ? (bool) $row['laos'] : null,
					);
				}
				if ( ! empty( $out[ $id ] ) ) {
					usort( $out[ $id ], static fn( $a, $b ) => $a['hind'] <=> $b['hind'] );
				}
			}
			set_transient( $key, $out, 15 * MINUTE_IN_SECONDS );
		}
	}
	$res = rest_ensure_response(
		array(
			'available' => (bool) $available,
			'hinnad'    => (object) $out,
		)
	);
	$res->header( 'Cache-Control', 'public, max-age=300' );
	return $res;
}
