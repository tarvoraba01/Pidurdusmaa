<?php
/**
 * Andmekiht. Teema EI OMA andmeid — kõik tuleb failidest data/*.json,
 * mille kirjutab pidurdus/export_wp.py samast allikast, kust tuleb
 * kalkulaatori mootor. Siin ainult loetakse.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;

const PM_CAT_NAMES = array(
	'SUMMER_UHP'     => 'Suverehv (sportlik)',
	'SUMMER_TOURING' => 'Suverehv',
	'ALL_SEASON'     => 'Lamellrehv (aastaringne)',
	'WINTER_CENTRAL' => 'Talverehv (Kesk-Euroopa)',
	'WINTER_NORDIC'  => 'Talverehv (Põhjamaade, naelutu)',
	'WINTER_STUDDED' => 'Naastrehv',
);
const PM_CAT_SHORT = array(
	'SUMMER_UHP'     => 'Suvi',
	'SUMMER_TOURING' => 'Suvi',
	'ALL_SEASON'     => 'Lamell',
	'WINTER_CENTRAL' => 'Talv',
	'WINTER_NORDIC'  => 'Talv (Põhjamaa)',
	'WINTER_STUDDED' => 'Naast',
);
const PM_EPREL_CAT = array( 'SUMMER_TOURING', 'ALL_SEASON', 'WINTER_CENTRAL', 'WINTER_NORDIC' );

/**
 * Loe JSON-fail teema data/ kaustast. Staatiline puhver + objektipuhver,
 * sest models.json on ~0,5 MB ja rehvilehel loetakse teda igal päringul.
 */
function pm_json( string $rel ) {
	static $mem = array();
	if ( isset( $mem[ $rel ] ) ) {
		return $mem[ $rel ];
	}
	$path = get_template_directory() . '/data/' . $rel;
	if ( ! is_readable( $path ) ) {
		return $mem[ $rel ] = null;
	}
	$key    = 'pm_' . md5( $rel . filemtime( $path ) );
	$cached = wp_cache_get( $key, 'pidurdusmaa' );
	if ( false !== $cached ) {
		return $mem[ $rel ] = $cached;
	}
	$data = json_decode( file_get_contents( $path ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions
	wp_cache_set( $key, $data, 'pidurdusmaa', HOUR_IN_SECONDS );
	return $mem[ $rel ] = $data;
}

function pm_core(): array {
	return pm_json( 'core.json' ) ?: array( 'vehicles' => array(), 'tyres' => array(), 'sources' => array(), 'sizes' => array() );
}
function pm_models(): array {
	return pm_json( 'models.json' ) ?: array();
}
function pm_model( string $slug ): ?array {
	$m = pm_models();
	return $m[ $slug ] ?? null;
}
/** EPREL-i read ühes mõõdus: [slug, mark, nimi, katNr, märg, kütus, dB, müraKl, lipud, testKey] */
function pm_eprel_size( string $mootN ): array {
	if ( ! preg_match( '/^[0-9A-Za-z]+$/', $mootN ) ) {
		return array();
	}
	return pm_json( 'eprel/' . $mootN . '.json' ) ?: array();
}
function pm_size_by_slug( string $slug ): ?array {
	foreach ( pm_core()['sizes'] as $s ) {
		if ( $s['slug'] === $slug ) {
			return $s;
		}
	}
	return null;
}
function pm_tested_by_key( string $key ): ?array {
	foreach ( pm_core()['tyres'] as $t ) {
		if ( $t['key'] === $key ) {
			return $t;
		}
	}
	return null;
}
function pm_tested_by_slug( string $slug ): ?array {
	foreach ( pm_core()['tyres'] as $t ) {
		if ( ( $t['slug'] ?? '' ) === $slug ) {
			return $t;
		}
	}
	return null;
}
function pm_source( string $code ): ?array {
	return pm_core()['sources'][ $code ] ?? null;
}
function pm_source_slug( string $code ): string {
	return strtolower( $code );
}

/**
 * Rehvileht on olemas, kui slug on kas EPREL-i mudel või mõõdetud rehv.
 * Tagastab ühtse kirjelduse, mida mall kasutab.
 */
function pm_tyre_page( string $slug ): ?array {
	$model  = pm_model( $slug );
	$tested = null;
	if ( $model && ! empty( $model['tested'] ) ) {
		$tested = pm_tested_by_key( $model['tested'] );
	}
	if ( ! $tested ) {
		$tested = pm_tested_by_slug( $slug );
	}
	if ( ! $model && ! $tested ) {
		return null;
	}
	$name  = $model ? trim( $model['mark'] . ' ' . $model['nimi'] ) : $tested['name'];
	$brand = $model ? $model['mark'] : strtok( $tested['name'], ' ' );
	$cat   = $tested['category'] ?? ( $model['kat'] ?? '' );
	return array(
		'slug'   => $slug,
		'name'   => pm_title_case( $name ),
		'brand'  => pm_title_case( $brand ),
		'cat'    => $cat,
		'model'  => $model,
		'tested' => $tested,
	);
}

/** EPREL-i nimed on sageli SUURTÄHTEDES. Ilusamaks, aga mudelikoodid jäävad. */
function pm_title_case( string $s ): string {
	// Kõik suurtähtedes -> iga vähemalt 3-täheline sõna; muidu ainult 4+ tähega
	// suurtähesõnad. Mudelikoodid (ZR, XL, EVO3, PS71) jäävad puutumata.
	$min = preg_match( '/\p{Ll}/u', $s ) ? 4 : 3;
	return preg_replace_callback(
		'/(?<![\p{L}\d])(\p{Lu})(\p{Lu}{' . ( $min - 1 ) . ',})(?![\p{L}\d])/u',
		static function ( $m ) {
			return $m[1] . mb_strtolower( $m[2] );
		},
		$s
	);
}

/** Mõõdu kuvavorm: 20555R16 -> 205/55 R16 */
function pm_pretty_size( string $m ): string {
	if ( preg_match( '/^(\d{3})(\d{2})R(\d{2})(C?)$/', $m, $x ) ) {
		return "{$x[1]}/{$x[2]} R{$x[3]}{$x[4]}";
	}
	return $m;
}
function pm_size_slug( string $m ): ?string {
	if ( preg_match( '/^(\d{3})(\d{2})R(\d{2})(C?)$/', $m, $x ) ) {
		return "{$x[1]}-{$x[2]}-r{$x[3]}" . ( $x[4] ? 'c' : '' );
	}
	return null;
}

/** Eesti arvuvorming: koma, mitte punkt. */
function pm_num( $v, int $dec = 1 ): string {
	return number_format( (float) $v, $dec, ',', ' ' );
}

/** Protsentuaalne vahe: +48 % või +5,8 % (alla 10 % ühe komakohaga). */
function pm_pct( float $val, float $base ): string {
	$v = 100 * ( $val - $base ) / $base;
	return ( $v >= 0 ? '+' : '' ) . pm_num( $v, abs( $v ) < 10 ? 1 : 0 ) . ' %';
}

function pm_grade( ?string $g ): string {
	if ( ! $g || ! preg_match( '/^[A-E]$/', $g ) ) {
		return '<span class="gr x">–</span>';
	}
	return '<span class="gr ' . esc_attr( $g ) . '" aria-label="klass ' . esc_attr( $g ) . '">' . esc_html( $g ) . '</span>';
}

/** Mõõdetud testitulemuse inimloetav kirjeldus. */
function pm_test_label( array $t ): string {
	$s = array(
		'ASPHALT'     => $t['wet'] ? 'märg asfalt' : 'kuiv asfalt',
		'CONCRETE'    => 'märg betoon',
		'ICE'         => 'jää',
		'SNOW_PACKED' => 'lumi',
	)[ $t['surf'] ] ?? strtolower( $t['surf'] );
	return $s . ', ' . (int) $t['v0'] . '→' . (int) $t['v1'] . ' km/h';
}

function pm_url( string $path = '' ): string {
	return home_url( '/' . ltrim( $path, '/' ) );
}
function pm_tyre_url( string $slug ): string {
	return pm_url( 'rehvid/' . $slug . '/' );
}

/** Koht selles testis samal pinnal (1 = parim). */
function pm_rank_in_test( array $x ): array {
	$all = array();
	foreach ( pm_core()['tyres'] as $o ) {
		foreach ( $o['tests'] as $y ) {
			if ( $y['src'] === $x['src'] && $y['surf'] === $x['surf'] && $y['wet'] === $x['wet'] && $y['v0'] === $x['v0'] ) {
				$all[] = $y['m'];
			}
		}
	}
	sort( $all );
	$pos = array_search( $x['m'], $all, true );
	return array( false === $pos ? null : $pos + 1, count( $all ), $all ? $all[0] : null );
}


/** Rehvi valimise küsimused — sama nii /rehvi-valimine/ lehel kui avalehe kaardis. */
function pm_valik_q(): array {
	return array(
		'drive' => array(
			'Kus sõidad kõige rohkem?',
			array( 'city' => 'Linnas', 'road' => 'Maanteel', 'hwy' => 'Kiirteel', 'mix' => 'Linn + maantee' ),
		),
		'km'    => array(
			'Kui palju sõidad aastas?',
			array( 'lo' => 'alla 10 000 km', 'mid' => '10–20 000 km', 'hi' => '20–30 000 km', 'vhi' => 'üle 30 000 km' ),
		),
		'main'  => array(
			'Mis on sulle kõige tähtsam? (kuni 3)',
			array(
				'safe'   => 'Ohutus märjal',
				'brake'  => 'Lühike pidurdusmaa',
				'quiet'  => 'Vaikne sõit',
				'fuel'   => 'Väike kütusekulu',
				'winter' => 'Talvised omadused',
			),
		),
	);
}
