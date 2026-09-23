<?php
/**
 * Pidurdusmaa teema.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;

define( 'PM_VER', '1.0.0' );

require_once __DIR__ . '/inc/data.php';
require_once __DIR__ . '/inc/icons.php';
require_once __DIR__ . '/inc/routes.php';
require_once __DIR__ . '/inc/vs.php';
require_once __DIR__ . '/inc/prices.php';
require_once __DIR__ . '/inc/contact.php';
require_once __DIR__ . '/inc/seo.php';
require_once __DIR__ . '/inc/setup-content.php';

/* Teeolude tingimused avalehel. NB: sama tabel on assets/js/app.js-is
   (COND) ja "Kuidas arvutatakse" tekstis — muuda kõiki kolme koos. */
const PM_CONDS = array(
	'wet'  => array( 'Märg', 'märg asfalt, veekiht 1 mm, +10 °C' ),
	'dry'  => array( 'Kuiv', 'kuiv asfalt, +15 °C' ),
	'snow' => array( 'Lumi', 'tallatud lumi, −5 °C' ),
	'ice'  => array( 'Jää', 'jää, −5 °C' ),
);

add_action(
	'after_setup_theme',
	static function () {
		add_theme_support( 'title-tag' );
		add_theme_support( 'post-thumbnails' );
		add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
		add_theme_support( 'responsive-embeds' );
	}
);

/** Versioon faili muutmisaja järgi, et vahemälu ei näitaks vana mootorit. */
function pm_asset_ver( string $rel ): string {
	$p = get_template_directory() . '/' . $rel;
	return is_readable( $p ) ? PM_VER . '.' . filemtime( $p ) : PM_VER;
}

add_action(
	'wp_enqueue_scripts',
	static function () {
		$uri = get_template_directory_uri();
		wp_enqueue_style( 'pm-main', $uri . '/assets/css/main.css', array(), pm_asset_ver( 'assets/css/main.css' ) );
		wp_enqueue_script( 'pm-engine', $uri . '/assets/js/engine.js', array(), pm_asset_ver( 'assets/js/engine.js' ), array( 'strategy' => 'defer', 'in_footer' => true ) );
		wp_enqueue_script( 'pm-app', $uri . '/assets/js/app.js', array( 'pm-engine' ), pm_asset_ver( 'assets/js/app.js' ), array( 'strategy' => 'defer', 'in_footer' => true ) );
		$ctx = pm_ctx();
		wp_add_inline_script(
			'pm-app',
			'window.PM_CFG=' . wp_json_encode(
				array(
					'data'  => $uri . '/data/',
					'ver'   => pm_asset_ver( 'data/core.json' ),
					'home'  => home_url( '/' ),
					'page'  => $ctx['view'] ?? ( is_front_page() ? 'home' : '' ),
					'tyre'  => isset( $ctx['tyre'] ) ? $ctx['tyre']['slug'] : null,
					'size'  => isset( $ctx['size'] ) ? $ctx['size']['m'] : null,
					'prices' => rest_url( 'pm/v1/hinnad' ),
					'contact' => rest_url( 'pm/v1/kontakt' ),
				),
				JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
			) . ';',
			'before'
		);
		// Kalkulaatori lehed ei vaja plokiredaktori stiile.
		if ( get_query_var( 'pm_view' ) || is_front_page() ) {
			wp_dequeue_style( 'wp-block-library' );
			wp_dequeue_style( 'global-styles' );
			wp_dequeue_style( 'classic-theme-styles' );
		}
	},
	20
);

add_action(
	'wp_head',
	static function () {
		$uri = get_template_directory_uri();
		echo '<link rel="preload" href="' . esc_url( $uri . '/assets/fonts/barlow-condensed-latin-700-normal.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
		echo '<link rel="preload" href="' . esc_url( $uri . '/assets/fonts/inter-latin-wght-normal.woff2' ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
		$v = get_query_var( 'pm_view' );
		if ( is_front_page() || in_array( $v, array( 'vordle', 'valik', 'rehv', 'moot' ), true ) ) {
			echo '<link rel="preload" href="' . esc_url( $uri . '/data/core.json?v=' . pm_asset_ver( 'data/core.json' ) ) . '" as="fetch" type="application/json" crossorigin>' . "\n";
		}
		echo '<meta name="theme-color" content="#0a0b0d">' . "\n";
		echo '<link rel="icon" href="' . esc_url( $uri . '/assets/img/favicon.svg' ) . '" type="image/svg+xml">' . "\n";
	},
	1
);

/* ---------------------------------------------------------------- menüü */
function pm_teadmine_url(): string {
	$know = get_page_by_path( 'teadmine' );
	return $know ? get_permalink( $know ) : pm_url( 'teadmine/' );
}

function pm_nav_current(): string {
	if ( is_front_page() ) {
		return 'home';
	}
	$v = get_query_var( 'pm_view' );
	if ( in_array( $v, array( 'rehv', 'moot', 'vs', 'rehvid' ), true ) ) {
		return 'rehvid';
	}
	if ( in_array( $v, array( 'test', 'testid' ), true ) ) {
		return 'testid';
	}
	if ( $v ) {
		return $v;
	}
	if ( is_page( 'teadmine' ) || ( is_page() && in_array( 'teadmine', array_map( static fn( $p ) => get_post_field( 'post_name', $p ), get_post_ancestors( get_the_ID() ) ), true ) ) ) {
		return 'teadmine';
	}
	return '';
}

/* ---------------------------------------------------------------- kohandaja */
add_action(
	'customize_register',
	static function ( $wp ) {
		$wp->add_section( 'pm_hero', array( 'title' => 'Avalehe hero', 'priority' => 30 ) );
		$wp->add_setting( 'pm_hero_image', array( 'sanitize_callback' => 'absint' ) );
		$wp->add_control(
			new WP_Customize_Media_Control(
				$wp,
				'pm_hero_image',
				array(
					'label'       => 'Taustapilt',
					'description' => 'Auto märjal teel, tume taust. Soovitus: vähemalt 1200 × 1200 px, auto keskel-vasakul. Tühi = ajutine pilt.',
					'section'     => 'pm_hero',
					'mime_type'   => 'image',
				)
			)
		);
	}
);

function pm_hero_bg( bool $mobile = false ) {
	$id  = (int) get_theme_mod( 'pm_hero_image' );
	$pri = $mobile ? 'low' : 'high';
	if ( $id ) {
		echo wp_get_attachment_image( $id, 'large', false, array( 'alt' => '', 'fetchpriority' => $pri, 'decoding' => 'async' ) );
		return;
	}
	// Ajutine pilt (kärbitud kasutaja kujunduskavandist, madal resolutsioon).
	// Asenda: Välimus → Kohanda → Avalehe hero.
	echo '<img src="' . esc_url( get_template_directory_uri() . '/assets/img/hero-car.jpg' ) . '" alt="" fetchpriority="' . $pri . '" decoding="async" width="624" height="588">';
}

