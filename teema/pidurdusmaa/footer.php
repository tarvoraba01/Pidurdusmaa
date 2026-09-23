<?php
/**
 * Jalus.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
?>
</main>
<footer class="site-footer">
	<div class="wrap">
		<div class="ft">
			<div>
				<a class="logo" href="<?php echo esc_url( home_url( '/' ) ); ?>"><b>PIDURDUSMAA</b><em>.ee</em></a>
				<p>Sa ei pea teadma, milline rehv on hea. Näitame, kuidas need erinevad — päris andmete järgi, ja ütleme otse, kui andmeid ei ole.</p>
			</div>
			<div>
				<h4>Tööriistad</h4>
				<ul>
					<li><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Pidurdusmaa kalkulaator</a></li>
					<li><a href="<?php echo esc_url( pm_url( 'rehvi-valimine/' ) ); ?>">Rehvi valimine</a></li>
					<li><a href="<?php echo esc_url( pm_url( 'vordle-rehve/' ) ); ?>">Võrdle rehve</a></li>
									</ul>
			</div>
			<div>
				<h4>Andmed</h4>
				<ul>
					<li><a href="<?php echo esc_url( pm_url( 'rehvid/' ) ); ?>">Rehvid</a></li>
						<li><a href="<?php echo esc_url( pm_url( 'testid/' ) ); ?>">Sõltumatud testid</a></li>
					<li><a href="<?php echo esc_url( pm_url( 'teadmine/kuidas-pidurdusmaa-arvutatakse/' ) ); ?>">Kuidas arvutatakse</a></li>
					<li><a href="<?php echo esc_url( pm_teadmine_url() ); ?>">Teadmine</a></li>
						<li><a href="<?php echo esc_url( pm_url( 'kontakt/' ) ); ?>">Kontakt</a></li>
				</ul>
			</div>
			<div>
				<h4>Allikad</h4>
				<ul>
					<li>EL-i tooteregister EPREL</li>
					<li>ADAC, Tekniikan Maailma, UTAC, Vi Bilägare</li>
					<li>UNECE R117</li>
				</ul>
			</div>
		</div>
		<div class="ft-b">
			<span>© <?php echo esc_html( gmdate( 'Y' ) ); ?> Rabarvo OÜ · Pidurdusmaa.ee</span>
			<span>Tulemused on arvutatud hinnangud — mitte mõõtmised ega garantii. <a href="<?php echo esc_url( pm_url( 'kasutustingimused/' ) ); ?>">Kasutustingimused ja vastutus</a></span>
		</div>
	</div>
</footer>
<?php wp_footer(); ?>
</body>
</html>
