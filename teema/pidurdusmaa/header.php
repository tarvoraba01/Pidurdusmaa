<?php
/**
 * Päis.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
$cur = pm_nav_current();
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip" href="#sisu">Liigu sisu juurde</a>
<header class="site-header">
	<div class="wrap">
		<a class="logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="Pidurdusmaa.ee avaleht"><b>PIDURDUSMAA</b><em>.ee</em></a>
		<nav class="nav" aria-label="Peamenüü">
			<a href="<?php echo esc_url( home_url( '/' ) ); ?>"<?php echo in_array( $cur, array( 'home', 'kalkulaator' ), true ) ? ' aria-current="page"' : ''; ?>>Pidurdusmaa</a>
			<div class="dd" data-dd>
				<button type="button" class="dd-btn" aria-expanded="false" aria-haspopup="true"<?php echo in_array( $cur, array( 'valik', 'vordle' ), true ) ? ' aria-current="page"' : ''; ?>>Rehvi valimine <?php echo pm_icon( 'chev' ); // phpcs:ignore ?></button>
				<div class="dd-menu" role="menu">
					<a role="menuitem" href="<?php echo esc_url( pm_url( 'rehvi-valimine/' ) ); ?>"><b>Vali rehv enda tingimustele</b><span>Mis on sulle oluline — näitame sobivaid</span></a>
					<a role="menuitem" href="<?php echo esc_url( pm_url( 'vordle-rehve/' ) ); ?>"><b>Võrdle rehve kõrvuti</b><span>2–4 rehvi ühes tabelis</span></a>
				</div>
			</div>
			<a href="<?php echo esc_url( pm_url( 'testid/' ) ); ?>"<?php echo 'testid' === $cur ? ' aria-current="page"' : ''; ?>>Testid</a>
			<a href="<?php echo esc_url( pm_url( 'rehvid/' ) ); ?>"<?php echo 'rehvid' === $cur ? ' aria-current="page"' : ''; ?>>Rehvid</a>
			<a href="<?php echo esc_url( pm_teadmine_url() ); ?>"<?php echo 'teadmine' === $cur ? ' aria-current="page"' : ''; ?>>Teadmine</a>
		</nav>
		<div class="hdr-right">
			<a class="cmp-link" href="<?php echo esc_url( pm_url( 'vordle-rehve/' ) ); ?>" data-cmp-pill>
				<?php echo pm_icon( 'heart' ); // phpcs:ignore ?><span>Võrdlus (<span data-cmp-n>0</span>)</span>
			</a>
			<button class="burger" type="button" aria-controls="pm-panel" aria-expanded="false" aria-label="Menüü" data-burger>
				<?php echo pm_icon( 'menu' ); // phpcs:ignore ?>
			</button>
		</div>
	</div>
	<div class="panel-menu" id="pm-panel" hidden>
		<div class="wrap">
			<div class="pm-cols">
				<div>
					<h4>Pidurdusmaa</h4>
					<a href="<?php echo esc_url( home_url( '/' ) ); ?>">Pidurdusmaa kalkulaator</a>
					<a href="<?php echo esc_url( pm_url( 'teadmine/kuidas-pidurdusmaa-arvutatakse/' ) ); ?>">Kuidas arvutatakse</a>
				</div>
				<div>
					<h4>Rehvi valimine</h4>
					<a href="<?php echo esc_url( pm_url( 'rehvi-valimine/' ) ); ?>">Vali rehv enda tingimustele</a>
					<a href="<?php echo esc_url( pm_url( 'vordle-rehve/' ) ); ?>">Võrdle rehve kõrvuti</a>
				</div>
				<div>
					<h4>Andmed</h4>
					<a href="<?php echo esc_url( pm_url( 'rehvid/' ) ); ?>">Rehvid</a>
					<a href="<?php echo esc_url( pm_url( 'testid/' ) ); ?>">Sõltumatud testid</a>
					<a href="<?php echo esc_url( pm_teadmine_url() ); ?>">Teadmine</a>
					<a href="<?php echo esc_url( pm_url( 'teadmine/rehvimargis/' ) ); ?>">EL-i rehvimärgis</a>
					<a href="<?php echo esc_url( pm_url( 'kontakt/' ) ); ?>">Kontakt</a>
				</div>
			</div>
		</div>
	</div>
</header>
<main id="sisu">
