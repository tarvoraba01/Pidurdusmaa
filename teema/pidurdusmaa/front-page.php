<?php
/**
 * Avaleht = pidurdusmaa. Kaardi teine vaheleht „Vali rehv enda tingimustel“
 * peidab kalkulaatori tulemuse ja infoplokid ning näitab nende asemel
 * sobivate rehvide nimekirja (sama loogika mis /rehvi-valimine/ lehel).
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
get_header();
$demo = pm_core()['demo'] ?? array();
?>
<section class="hero" aria-labelledby="hero-h">
	<div class="wrap">
		<div class="hero-copy">
			<h1 id="hero-h">Kui kiiresti <span class="up">sinu auto</span><span class="up">peatub?</span></h1>
			<p class="lede">Arvuta pidurdusmaa erinevatel kiirustel ja teeoludel.</p>
			<p class="tagline">Lihtne. Kiire. Täpne.<svg viewBox="0 0 120 10" preserveAspectRatio="none" aria-hidden="true"><path d="M2 7 C 30 2, 70 2, 118 5" stroke="#ffc20e" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg></p>
			<div class="hero-visual-m" aria-hidden="true"><?php pm_hero_bg( true ); ?></div>
		</div>
		<div class="hero-photo" aria-hidden="true"><?php pm_hero_bg(); ?></div>
		<?php get_template_part( 'template-parts/calc' ); ?>
	</div>
</section>

<div data-home="calc">
<?php get_template_part( 'template-parts/result' ); ?>

<?php if ( $demo ) : ?>
<section class="sec" aria-labelledby="s1">
	<div class="wrap why">
		<div>
			<div class="sec-h">
				<span class="eyebrow" style="color:var(--muted)">Miks pidurdusmaa loeb</span>
				<h2 id="s1">Kiirus kasvab lineaarselt. Pidurdusmaa ei kasva.</h2>
				<p>Kahekordne kiirus tähendab rohkem kui kahekordset pidurdusmaad. Märjal teel on vahe veel suurem.</p>
			</div>
			<div class="bullets">
				<div><span class="ic"><?php echo pm_icon( 'speed' ); // phpcs:ignore ?></span><div><h3>90 → 110 km/h</h3><p>Märjal <?php echo esc_html( pm_num( $demo['wet'][1] ) ); ?> m asemel <?php echo esc_html( pm_num( $demo['wet'][2] ) ); ?> m — <?php echo esc_html( pm_num( $demo['wet'][2] - $demo['wet'][1] ) ); ?> meetrit ehk <?php echo esc_html( ltrim( pm_pct( $demo['wet'][2], $demo['wet'][1] ), '+' ) ); ?> rohkem.</p></div></div>
				<div><span class="ic"><?php echo pm_icon( 'wet' ); // phpcs:ignore ?></span><div><h3>Märg vs kuiv</h3><p>90 km/h juures kuival <?php echo esc_html( pm_num( $demo['dry'][1] ) ); ?> m, märjal <?php echo esc_html( pm_num( $demo['wet'][1] ) ); ?> m.</p></div></div>
				<div><span class="ic"><?php echo pm_icon( 'tyre' ); // phpcs:ignore ?></span><div><h3>Rehv</h3><p>Sama auto, sama märg tee: märgise klass A <?php echo esc_html( pm_num( $demo['classA'] ) ); ?> m, klass E <?php echo esc_html( pm_num( $demo['classE'] ) ); ?> m.</p></div></div>
			</div>
		</div>
		<div class="stopline" role="img" aria-label="Pidurdusmaa märjal eri kiirustel">
			<h3>Pidurdusmaa · <?php echo esc_html( $demo['car'] ); ?></h3>
			<?php
			$max = max( $demo['wet'] );
			foreach ( $demo['speeds'] as $i => $v ) :
				?>
				<div class="sl-row"><span class="k"><?php echo (int) $v; ?> km/h</span>
					<span class="t"><span style="width:<?php echo esc_attr( round( 100 * $demo['wet'][ $i ] / $max, 1 ) ); ?>%"></span></span>
					<span class="v"><?php echo esc_html( pm_num( $demo['wet'][ $i ] ) ); ?> m</span></div>
			<?php endforeach; ?>
			<p class="src">Märg asfalt, veekiht 1 mm, +10 °C. Ilma reaktsiooniajata. <span class="pill calc" style="margin-left:6px">Arvutatud</span></p>
		</div>
	</div>
</section>

<section class="sec alt" aria-labelledby="s2">
	<div class="wrap">
		<div class="sec-h">
			<span class="eyebrow" style="color:var(--muted)">Mis mõjutab pidurdusmaad</span>
			<h2 id="s2">Kuus asja, mida saad mõjutada</h2>
			<p>Kõik arvud on arvutatud sama mudeliga, mis kalkulaator — sama auto, üks asi korraga muudetud.</p>
		</div>
		<div class="factors">
			<div class="factor"><div class="ic"><?php echo pm_icon( 'speed' ); // phpcs:ignore ?></div><h3>Kiirus</h3><p>Kõige suurem üksik tegur. Energia kasvab kiiruse ruudus.</p><p class="fx">50 → 110 km/h märjal: <b><?php echo esc_html( pm_num( $demo['wet'][0] ) ); ?> → <?php echo esc_html( pm_num( $demo['wet'][2] ) ); ?> m</b></p></div>
			<div class="factor"><div class="ic"><?php echo pm_icon( 'road' ); // phpcs:ignore ?></div><h3>Teeolud</h3><p>Lumi ja jää muudavad kõike. Suverehv lumel on teine maailm.</p><p class="fx">Lumi 50 km/h, suvi vs talv: <b><?php echo esc_html( pm_num( $demo['snowSummer'] ) ); ?> / <?php echo esc_html( pm_num( $demo['snowWinter'] ) ); ?> m</b></p></div>
			<div class="factor"><div class="ic"><?php echo pm_icon( 'tyre' ); // phpcs:ignore ?></div><h3>Rehv</h3><p>Märghaardumise klass on ametlik ja võrreldav. Ainult sinu mõõdus.</p><p class="fx">Klass A vs E, 90 km/h: <b>+<?php echo esc_html( pm_num( $demo['classE'] - $demo['classA'] ) ); ?> m (<?php echo esc_html( pm_pct( $demo['classE'], $demo['classA'] ) ); ?>)</b></p></div>
			<div class="factor"><div class="ic"><?php echo pm_icon( 'temp' ); // phpcs:ignore ?></div><h3>Temperatuur</h3><p>Talverehv on soojal asfaldil pehme ja pidurdab halvemini.</p><p class="fx">Kuiv +25 °C, suvi vs talv: <b><?php echo esc_html( pm_num( $demo['summerWarm'] ) ); ?> / <?php echo esc_html( pm_num( $demo['winterWarm'] ) ); ?> m (<?php echo esc_html( pm_pct( $demo['winterWarm'], $demo['summerWarm'] ) ); ?>)</b></p></div>
			<div class="factor"><div class="ic"><?php echo pm_icon( 'car' ); // phpcs:ignore ?></div><h3>Auto</h3><p>Mass, ABS ja pidurid. Koorem mõjutab vähem, kui arvatakse.</p><p class="fx">+375 kg koormat märjal: <b><?php echo esc_html( pm_num( $demo['tread8'] ) ); ?> → <?php echo esc_html( pm_num( $demo['loaded'] ) ); ?> m (<?php echo esc_html( pm_pct( $demo['loaded'], $demo['tread8'] ) ); ?>)</b></p></div>
			<div class="factor"><div class="ic"><?php echo pm_icon( 'wear' ); // phpcs:ignore ?></div><h3>Rehvi seisukord</h3><p>Kulunud muster juhib vett halvemini. Sügavas vees kordades.</p><p class="fx">8 mm → 3 mm, märg 90 km/h: <b><?php echo esc_html( pm_num( $demo['tread8'] ) ); ?> → <?php echo esc_html( pm_num( $demo['tread3'] ) ); ?> m (<?php echo esc_html( pm_pct( $demo['tread3'], $demo['tread8'] ) ); ?>)</b></p></div>
		</div>
	</div>
</section>
<?php endif; ?>
</div>

<div data-home="valik" hidden>
	<section class="body-sec home-valik" id="sobivad" aria-labelledby="hv-h" data-valik-home>
		<div class="wrap">
			<div class="hv-head">
				<div>
					<span class="eyebrow" style="color:var(--muted)">Rehvi valimine</span>
					<h2 id="hv-h">Sinu tingimustele sobivad rehvid</h2>
				</div>
				<div class="list-filter">
					<select class="lsel" data-brand aria-label="Mark"><option value="">Kõik margid</option></select>
					<input class="lsel" type="search" data-q placeholder="Otsi marki või mudelit" aria-label="Otsi rehvi" style="background-image:none">
				</div>
				<p class="note" data-cmp-head style="margin:0;font-size:15px"></p>
			</div>
			<div class="cmp-layout">
				<aside class="filters" aria-label="Täpsemad seaded">
					<div class="box">
						<div style="display:flex;align-items:center;justify-content:space-between">
							<h3 style="margin:0">Täpsusta kaalusid</h3>
							<button type="button" class="btn sm" data-prio-reset hidden>Tühjenda</button>
						</div>
						<p class="note" style="margin:6px 0 12px">Valikuline. Sinu vastused täidavad selle ise — siin näed ja muudad, kui palju iga omadus loeb (1–3).</p>
						<div class="prio" data-prio></div>
					</div>
					<div class="box">
						<h3 style="margin:0 0 8px">Kuidas järjestatakse</h3>
						<p class="note" style="margin:0">„Sobivus“ on ainult selle nimekirja sisene võrdlus sinu valitud omaduste järgi — mitte rehvi üldhinne. Hinnad ei mõjuta järjestust.</p>
						<p class="note" style="margin:10px 0 0">See on andmete kõrvutus, mitte ostunõuanne. <a href="<?php echo esc_url( pm_url( 'kasutustingimused/' ) ); ?>">Tingimused</a></p>
					</div>
				</aside>
				<div class="res-list" data-cmp-list><p class="note">Laen…</p></div>
			</div>
		</div>
	</section>
	<div class="cmp-tray" data-tray hidden>
		<div class="wrap">
			<div class="chips" data-tray-chips></div>
			<a class="btn yel sm" href="<?php echo esc_url( pm_url( 'vordle-rehve/' ) ); ?>" data-tray-go>Võrdle kõrvuti →</a>
		</div>
	</div>
</div>

<?php
get_template_part( 'template-parts/how' );
get_footer();
