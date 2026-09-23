<?php
/**
 * /vordle-rehve/ — valitud 2–4 rehvi kõrvuti. Valimise loogika on
 * /rehvi-valimine/ lehel; siin ainult võrdlus ja lihtne otsing lisamiseks.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;
get_header();
?>
<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">Avaleht</a><span>/</span><a href="<?php echo esc_url( pm_url( 'rehvi-valimine/' ) ); ?>">Rehvi valimine</a><span>/</span>Võrdle</div>
		<h1>Võrdle rehve kõrvuti</h1>
		<p>Iga omadus eraldi ja allikaga: EL-i rehvimärgis, sõltumatud testid ja arvutatud pidurdusmaa sinu autoga. Ühtegi „parima rehvi“ punktisummat ei ole.</p>
		<div class="pills"><span class="pill off">Ametlik märgis</span><span class="pill test">Sõltumatu test</span><span class="pill calc">Arvutus</span><span class="pill"><span class="est" style="margin:0">≈</span> Tuletatud</span></div>
	</div>
</section>

<div class="body-sec" data-cmp-page data-mode="vordle">
	<div class="wrap">
		<div data-cmp-table></div>

		<div class="box" style="margin-top:28px">
			<h2>Lisa rehve</h2>
			<div class="add-bar">
				<select class="lsel" data-f="make" aria-label="Mark"><option value="">Mark</option></select>
				<select class="lsel" data-f="model" aria-label="Mudel" disabled><option value="">Mudel</option></select>
				<select class="lsel" data-f="year" aria-label="Aasta" disabled><option value="">Aasta</option></select>
				<select class="lsel" data-f="variant" aria-label="Variant" disabled><option value="">Variant</option></select>
				<select class="lsel" data-f="size" aria-label="Rehvimõõt"><option value="20555R16">205/55 R16</option></select>
				<div class="lseg" role="group" aria-label="Hooaeg">
					<button type="button" data-season="summer">Suvi</button>
					<button type="button" data-season="all">Lamell</button>
					<button type="button" data-season="winter">Talv</button>
				</div>
				<select class="lsel" data-brand aria-label="Mark"><option value="">Kõik margid</option></select>
				<input class="lsel" type="search" data-q placeholder="Otsi marki või mudelit" aria-label="Otsi rehvi" style="background-image:none">
			</div>
			<p class="note" data-cmp-head style="margin:12px 0"></p>
			<div class="res-list" data-cmp-list><p class="note">Laen…</p></div>
		</div>
	</div>
</div>

<div class="cmp-tray" data-tray hidden>
	<div class="wrap">
		<div class="chips" data-tray-chips></div>
		<a class="btn yel sm" href="#vordlus" data-tray-go>Vaata võrdlust ↑</a>
	</div>
</div>
<?php
get_template_part( 'template-parts/how' );
get_footer();
