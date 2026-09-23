<?php
/**
 * Pealkirjad, kirjeldused, canonical, robots, struktureeritud andmed,
 * sitemap.
 *
 * INDEKSEERIMISE REEGEL: leht läheb otsingusse ainult siis, kui tal on
 * midagi, mida mujal ei ole. 1157 EPREL-i mudelist on enamikul ainult
 * märgise read ühes-kahes mõõdus — need lehed on kasutajale olemas
 * (võrdlusest lingitud), aga "noindex, follow". Vt pm_indexable().
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;

const PM_SIZE_MIN_MODELS = 10;

function pm_indexable( array $ctx ): bool {
	switch ( $ctx['view'] ?? '' ) {
		case 'rehv':
			$t = $ctx['tyre'];
			if ( ! empty( $t['tested'] ) ) {
				return true;
			}
			return $t['model'] && count( $t['model']['sizes'] ) >= 3;
		case 'moot':
			return pm_size_model_count( $ctx['size']['m'] ) >= PM_SIZE_MIN_MODELS;
		default:
			return true;
	}
}

function pm_size_model_count( string $m ): int {
	return count( pm_eprel_size( $m ) );
}

function pm_meta(): array {
	$ctx = pm_ctx();
	if ( ! empty( $ctx['404'] ) ) {
		return array();
	}
	$v   = $ctx['view'] ?? '';
	switch ( $v ) {
		case 'vordle':
			return array(
				'title' => 'Võrdle rehve — märghaare, müra, veeretakistus ja pidurdusmaa',
				'desc'  => 'Võrdle rehvimudeleid sinu auto mõõdus päris andmete järgi: EL-i rehvimärgis, sõltumatud testid ja arvutatud pidurdusmaa. Ilma väljamõeldud koondhindeta.',
				'path'  => 'vordle-rehve/',
			);
		case 'kontakt':
			return array(
				'title' => 'Kontakt',
				'desc'  => 'Võta Pidurdusmaa.ee-ga ühendust: rehvimüüjate hinnad ja koostöö, vead andmetes, ettepanekud.',
				'path'  => 'kontakt/',
			);
		case 'valik':
			return array(
				'title' => 'Rehvi valimine — vali rehv selle järgi, mis sulle oluline on',
				'desc'  => 'Ütle, kus ja kui palju sõidad ning mis sulle rehvi juures oluline on. Näitame sinu auto mõõdus sobivaid rehve ja põhjuse, miks — päris andmete järgi.',
				'path'  => 'rehvi-valimine/',
			);
		case 'rehvid':
			return array(
				'title' => 'Rehvid mõõdu ja mudeli järgi',
				'desc'  => 'Rehvimudelid ja -mõõdud EL-i rehvimärgise (EPREL) andmetega ning sõltumatute testide mõõdetud pidurdusmaad.',
				'path'  => 'rehvid/',
			);
		case 'moot':
			$s = $ctx['size'];
			$n = pm_size_model_count( $s['m'] );
			return array(
				'title' => "Rehvid {$s['label']} — {$n} rehvimudelit märgise andmetega",
				'desc'  => "Kõik {$s['label']} mõõdus rehvid EL-i rehvimärgise järgi: märghaardumise klass, veeretakistus ja müra. Võrdle ja vaata, kui palju muutub pidurdusmaa.",
				'path'  => "rehvid/{$s['slug']}/",
			);
		case 'rehv':
			$t   = $ctx['tyre'];
			$bit = array();
			if ( $t['tested'] ) {
				$bit[] = 'sõltumatu testi pidurdusmaad';
			}
			if ( $t['model'] ) {
				$bit[] = 'EL-i rehvimärgis ' . count( $t['model']['sizes'] ) . ' mõõdus';
			}
			return array(
				'title' => $t['name'] . ' — pidurdusmaa, märgis ja testid',
				'desc'  => $t['name'] . ' (' . ( PM_CAT_NAMES[ $t['cat'] ] ?? '' ) . '): ' . implode( ', ', $bit ) . '. Võrdle teiste rehvidega.',
				'path'  => "rehvid/{$t['slug']}/",
			);
		case 'vs':
			return array(
				'title' => $ctx['a']['name'] . ' vs ' . $ctx['b']['name'] . ' — mõõdetud pidurdusmaad',
				'desc'  => 'Kaks rehvi samas sõltumatus testis, sama auto ja sama päev: ' . $ctx['a']['name'] . ' ja ' . $ctx['b']['name'] . '. Pidurdusmaad märjal, kuival ja muudel pindadel.',
				'path'  => 'rehvid/' . get_query_var( 'pm_a' ) . '-vs-' . get_query_var( 'pm_b' ) . '/',
			);
		case 'testid':
			return array(
				'title' => 'Sõltumatud rehvitestid — mõõdetud pidurdusmaad',
				'desc'  => 'Rehvitestid, mille mõõdetud tulemusi Pidurdusmaa.ee kasutab: ADAC, Tekniikan Maailma, UTAC, Vi Bilägare. Allikas, kuupäev, protokoll ja iga rehvi tulemus.',
				'path'  => 'testid/',
			);
		case 'test':
			$s = $ctx['source'];
			return array(
				'title' => $s['nimi'] . ' — tulemused',
				'desc'  => "{$s['nimi']}: {$s['rehve']} rehvi, {$s['moot']}, {$s['auto']}. Mõõdetud pidurdusmaad ({$s['protokoll']}).",
				'path'  => 'testid/' . pm_source_slug( $ctx['code'] ) . '/',
			);
	}
	return array();
}

add_filter(
	'pre_get_document_title',
	static function ( $t ) {
		$m = pm_meta();
		if ( $m ) {
			return $m['title'] . ' | Pidurdusmaa.ee';
		}
		if ( is_front_page() ) {
			return 'Pidurdusmaa.ee — kui kiiresti sinu auto peatub?';
		}
		return $t;
	}
);

add_action(
	'wp_head',
	static function () {
		$ctx = pm_ctx();
		$m   = pm_meta();
		if ( is_front_page() ) {
			$m = array(
				'title' => 'Pidurdusmaa.ee — kui kiiresti sinu auto peatub?',
				'desc'  => 'Arvuta oma auto pidurdusmaa erinevatel kiirustel ja teeoludel ning vaata, kui palju muudab tulemust rehv. Võrdle rehve päris omaduste järgi.',
				'path'  => '',
			);
		}
		if ( ! $m ) {
			return;
		}
		$url = pm_url( $m['path'] );
		echo '<meta name="description" content="' . esc_attr( $m['desc'] ) . "\">\n";
		if ( ! empty( $ctx['view'] ) && empty( $ctx['404'] ) ) {
			echo '<link rel="canonical" href="' . esc_url( $url ) . "\">\n";
		}
		echo '<meta property="og:type" content="website">' . "\n";
		echo '<meta property="og:site_name" content="Pidurdusmaa.ee">' . "\n";
		echo '<meta property="og:title" content="' . esc_attr( $m['title'] ) . "\">\n";
		echo '<meta property="og:description" content="' . esc_attr( $m['desc'] ) . "\">\n";
		echo '<meta property="og:url" content="' . esc_url( $url ) . "\">\n";
		echo '<meta property="og:locale" content="et_EE">' . "\n";
		pm_jsonld( $ctx, $url );
	},
	2
);

add_filter(
	'wp_robots',
	static function ( $r ) {
		$ctx = pm_ctx();
		if ( ! empty( $ctx['view'] ) && empty( $ctx['404'] ) && ! pm_indexable( $ctx ) ) {
			$r['noindex'] = true;
			$r['follow']  = true;
			unset( $r['max-image-preview'] );
		}
		return $r;
	}
);

/** WordPressi enda canonical ei tohi virtuaalsel lehel avalehele osutada. */
add_action(
	'wp',
	static function () {
		if ( get_query_var( 'pm_view' ) ) {
			remove_action( 'wp_head', 'rel_canonical' );
		}
	}
);

function pm_jsonld( array $ctx, string $url ) {
	if ( ! empty( $ctx['404'] ) ) {
		return;
	}
	$crumbs = array( array( 'Avaleht', pm_url() ) );
	$extra  = null;
	switch ( $ctx['view'] ?? '' ) {
		case 'rehv':
			$t        = $ctx['tyre'];
			$crumbs[] = array( 'Rehvid', pm_url( 'rehvid/' ) );
			$crumbs[] = array( $t['name'], $url );
			$props    = array();
			if ( $t['model'] ) {
				foreach ( $t['model']['sizes'] as $z ) {
					$props[] = array(
						'@type' => 'PropertyValue',
						'name'  => 'EL rehvimärgis ' . pm_pretty_size( $z['m'] ),
						'value' => 'märghaardumine ' . $z['g'] . ', veeretakistus ' . $z['f'] . ', müra ' . $z['db'] . ' dB',
					);
				}
			}
			$extra = array(
				'@context'           => 'https://schema.org',
				'@type'              => 'Product',
				'name'               => $t['name'],
				'brand'              => array( '@type' => 'Brand', 'name' => $t['brand'] ),
				'category'           => PM_CAT_NAMES[ $t['cat'] ] ?? 'Rehv',
				'url'                => $url,
				'additionalProperty' => array_slice( $props, 0, 20 ),
			);
			break;
		case 'moot':
			$crumbs[] = array( 'Rehvid', pm_url( 'rehvid/' ) );
			$crumbs[] = array( $ctx['size']['label'], $url );
			break;
		case 'test':
			$crumbs[] = array( 'Testid', pm_url( 'testid/' ) );
			$crumbs[] = array( $ctx['source']['nimi'], $url );
			break;
		case 'vs':
			$crumbs[] = array( 'Rehvid', pm_url( 'rehvid/' ) );
			$crumbs[] = array( $ctx['a']['name'] . ' vs ' . $ctx['b']['name'], $url );
			break;
	}
	if ( count( $crumbs ) > 1 ) {
		$items = array();
		foreach ( $crumbs as $i => $c ) {
			$items[] = array( '@type' => 'ListItem', 'position' => $i + 1, 'name' => $c[0], 'item' => $c[1] );
		}
		echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $items ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}
	if ( $extra ) {
		echo '<script type="application/ld+json">' . wp_json_encode( $extra, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}
}

/* ---------------------------------------------------------------- sitemap */
add_action(
	'init',
	static function () {
		if ( ! class_exists( 'WP_Sitemaps_Provider' ) ) {
			return;
		}
		require_once __DIR__ . '/sitemap.php';
		wp_register_sitemap_provider( 'pidurdusmaa', new PM_Sitemap_Provider() );
	}
);
