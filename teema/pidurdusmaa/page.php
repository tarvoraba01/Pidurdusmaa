<?php
/**
 * Tavaleht (Teadmine jms).
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
get_header();
while ( have_posts() ) :
	the_post();
	$anc = array_reverse( get_post_ancestors( get_the_ID() ) );
	?>
	<section class="page-hero">
		<div class="wrap">
			<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><?php foreach ( $anc as $a ) : ?><span>/</span><a href="<?php echo esc_url( get_permalink( $a ) ); ?>"><?php echo esc_html( get_the_title( $a ) ); ?></a><?php endforeach; ?><span>/</span><?php the_title(); ?></div>
			<h1><?php the_title(); ?></h1>
		</div>
	</section>
	<div class="body-sec">
		<div class="wrap">
			<article class="entry prose entry-content"><?php the_content(); ?></article>
			<?php
			$kids = get_pages( array( 'parent' => get_the_ID(), 'sort_column' => 'menu_order,post_title' ) );
			if ( $kids ) :
				?>
				<div class="grid-cards" style="margin-top:32px;max-width:760px">
					<?php foreach ( $kids as $k ) : ?>
						<a class="tcard" href="<?php echo esc_url( get_permalink( $k ) ); ?>"><span class="b">Teadmine</span><h3><?php echo esc_html( $k->post_title ); ?></h3></a>
					<?php endforeach; ?>
				</div>
			<?php endif; ?>
		</div>
	</div>
	<?php
endwhile;
get_footer();
