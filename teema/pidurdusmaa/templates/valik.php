<?php
/**
 * /rehvi-valimine/ — vali rehv enda tingimuste järgi.
 *
 * Mitte küsimustik, mis tuleb läbida: kõik on ühel ekraanil, iga klõps
 * muudab järjestust kohe ja lehel on kirjas, MIDA ta arvestas. Omadused,
 * mille kohta andmeid ei ole, on nähtavad, aga ei mõjuta midagi.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
get_header();
$q  = pm_valik_q();
$na = array();
?>
<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><span>/</span>Rehvi valimine</div>
		<h1>Rehvi valimine</h1>
		<p>Ütle, kus ja kui palju sõidad ning mis sulle rehvi juures oluline on. Näitame sinu auto mõõdus sobivaid rehve — ja miks just neid.</p>
	</div>
</section>

<div class="body-sec" data-cmp-page data-mode="valik">
	<div class="wrap">
		<div class="qcard">
			<div class="qcol">
				<h2 class="qh"><span>1</span>Sinu auto ja rehv</h2>
				<div class="qsel">
					<select class="lsel" data-f="make" aria-label="Mark"><option value="">Mark</option></select>
					<select class="lsel" data-f="model" aria-label="Mudel" disabled><option value="">Mudel</option></select>
					<select class="lsel" data-f="year" aria-label="Aasta" disabled><option value="">Aasta</option></select>
					<select class="lsel" data-f="variant" aria-label="Mootor / variant" disabled><option value="">Variant</option></select>
				</div>
				<label class="qlab" for="v-size">Rehvimõõt</label>
				<select class="lsel" id="v-size" data-f="size"><option value="20555R16">205/55 R16</option></select>
				<p class="qlab">Hooaeg</p>
				<div class="lseg" role="group" aria-label="Hooaeg">
					<button type="button" data-season="summer">Suverehv</button>
					<button type="button" data-season="all">Lamellrehv</button>
					<button type="button" data-season="winter">Talverehv</button>
				</div>
			</div>
			<div class="qcol">
				<h2 class="qh"><span>2</span>Mis sulle oluline on</h2>
				<?php foreach ( $q as $g => $item ) : ?>
					<p class="qlab"><?php echo esc_html( $item[0] ); ?></p>
					<div class="qchips" role="group" aria-label="<?php echo esc_attr( $item[0] ); ?>">
						<?php foreach ( $item[1] as $v => $label ) : ?>
							<button type="button" class="qchip<?php echo in_array( $v, $na, true ) ? ' na' : ''; ?>" data-ct="<?php echo esc_attr( $g ); ?>" data-v="<?php echo esc_attr( $v ); ?>" aria-pressed="false"<?php echo in_array( $v, $na, true ) ? ' title="Andmed puuduvad — valik ei mõjuta järjestust"' : ''; ?>><?php echo esc_html( $label ); ?><?php echo in_array( $v, $na, true ) ? ' <small>andmed puuduvad</small>' : ''; ?></button>
						<?php endforeach; ?>
					</div>
				<?php endforeach; ?>
				<div class="qout" data-ct-out></div>
			</div>
		</div>

		<div class="cmp-layout" style="margin-top:28px">
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
					<p class="note" style="margin:0">„Sobivus“ on ainult selle nimekirja sisene võrdlus sinu valitud omaduste järgi — mitte rehvi üldhinne. Omadus, mille kohta andmeid pole, jäetakse välja ja see öeldakse kaardil.</p>
					<p class="note" style="margin:10px 0 0">See on andmete kõrvutus, mitte ostunõuanne. <a href="<?php echo esc_url( pm_url( 'kasutustingimused/' ) ); ?>">Tingimused</a></p>
				</div>
			</aside>
			<div>
				<div class="list-filter">
					<select class="lsel" data-brand aria-label="Mark"><option value="">Kõik margid</option></select>
					<input class="lsel" type="search" data-q placeholder="Otsi marki või mudelit" aria-label="Otsi rehvi" style="background-image:none">
				</div>
				<p class="note" data-cmp-head style="margin:0 0 12px;font-size:15px"></p>
				<div class="res-list" data-cmp-list><p class="note">Laen…</p></div>
			</div>
		</div>
	</div>
</div>

<div class="cmp-tray" data-tray hidden>
	<div class="wrap">
		<div class="chips" data-tray-chips></div>
		<a class="btn yel sm" href="<?php echo esc_url( pm_url( 'vordle-rehve/' ) ); ?>" data-tray-go>Võrdle kõrvuti →</a>
	</div>
</div>
<?php
get_template_part( 'template-parts/how' );
get_footer();
