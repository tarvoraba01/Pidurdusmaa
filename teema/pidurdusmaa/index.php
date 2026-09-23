<?php
/**
 * Varumall (arhiivid, otsing). Blogi saidil ei ole.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<h1><?php echo esc_html( is_search() ? 'Otsing' : wp_strip_all_tags( get_the_archive_title() ) ); ?></h1>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<?php if ( have_posts() ) : ?>
			<div class="posts">
				<?php
				while ( have_posts() ) :
					the_post();
					?>
					<article class="post-card">
						<span class="d"><?php echo esc_html( get_the_date() ); ?></span>
						<h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
						<p class="note"><?php echo esc_html( get_the_excerpt() ); ?></p>
					</article>
				<?php endwhile; ?>
			</div>
			<div style="margin-top:28px"><?php the_posts_pagination(); ?></div>
		<?php else : ?>
			<p>Postitusi veel ei ole.</p>
		<?php endif; ?>
	</div>
</div>
<?php
get_footer();
