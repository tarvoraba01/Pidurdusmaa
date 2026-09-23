<?php
/**
 * Teema aktiveerimisel: lehed "Avaleht", "Teadmine" (+ metoodika)
 * ja lugemisseaded. Blogi ei ole. Olemasolevaid lehti EI kirjutata üle —
 * kui slug on juba olemas, jäetakse ta rahule.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;

function pm_ensure_page( string $slug, string $title, string $content = '', int $parent = 0 ): int {
	$existing = get_page_by_path( $parent ? get_post_field( 'post_name', $parent ) . '/' . $slug : $slug );
	if ( $existing ) {
		return (int) $existing->ID;
	}
	return (int) wp_insert_post(
		array(
			'post_type'    => 'page',
			'post_status'  => 'publish',
			'post_name'    => $slug,
			'post_title'   => $title,
			'post_content' => $content,
			'post_parent'  => $parent,
		)
	);
}

function pm_setup_content() {
	$home = pm_ensure_page( 'avaleht', 'Avaleht' );
	$know = pm_ensure_page( 'teadmine', 'Teadmine', pm_content_teadmine() );
	pm_ensure_page( 'kuidas-pidurdusmaa-arvutatakse', 'Kuidas pidurdusmaa arvutatakse', pm_content_metoodika(), $know );
	pm_ensure_page( 'rehvimargis', 'EL-i rehvimärgis: mida klassid tähendavad', pm_content_margis(), $know );
	pm_ensure_page( 'kasutustingimused', 'Kasutustingimused ja vastutus', pm_content_tingimused() );

	if ( 'page' !== get_option( 'show_on_front' ) ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $home );
	}
	update_option( 'permalink_structure', get_option( 'permalink_structure' ) ?: '/%postname%/' );
	update_option( 'blogdescription', 'Kui kiiresti sinu auto peatub?' );
	pm_register_routes();
	flush_rewrite_rules();

	// Blogi ei ole. WordPressi enda näidispostitus ja -leht viiakse prügikasti
	// (taastatav), aga AINULT siis, kui neid pole muudetud.
	foreach ( array( array( 'hello-world', 'post' ), array( 'sample-page', 'page' ) ) as $d ) {
		$p = get_page_by_path( $d[0], OBJECT, $d[1] );
		if ( $p && $p->post_modified_gmt === $p->post_date_gmt ) {
			wp_trash_post( $p->ID );
		}
	}

}
add_action( 'after_switch_theme', 'pm_setup_content', 20 );

/* Teema uuendus ei käivita after_switch_theme'i. Uued lehed (nt
   kasutustingimused) luuakse seepärast ka versioonikontrolliga — ainult
   puuduvad, olemasolevaid ei puudutata. */
const PM_CONTENT_VER = '2';
add_action(
	'init',
	static function () {
		if ( get_option( 'pm_content_ver' ) === PM_CONTENT_VER ) {
			return;
		}
		pm_ensure_page( 'kasutustingimused', 'Kasutustingimused ja vastutus', pm_content_tingimused() );
		update_option( 'pm_content_ver', PM_CONTENT_VER );
	},
	20
);

function pm_content_tingimused(): string {
	return <<<'HTML'
<!-- wp:paragraph -->
<p><strong>Lühidalt:</strong> Pidurdusmaa.ee näitab arvutatud hinnanguid üldiseks teadmiseks ja rehvide võrdlemiseks. Need ei ole mõõtmised, garantii ega ekspertarvamus. Ära tugine neile liikluses ega otsustes, millest sõltub kellegi ohutus.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>1. Mis see leht on</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Pidurdusmaa.ee (edaspidi „leht“) on Rabarvo OÜ hallatav infoleht. Leht arvutab pidurdusmaa hinnangu mudeliga, mis põhineb avalikel andmetel: EL-i rehvimärgise registril (EPREL) ja sõltumatute väljaannete avaldatud rehvitestidel.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>2. Tulemused on hinnangud</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li>Iga number lehel on <strong>arvutatud hinnang</strong>, millel on veapiir. Päris pidurdusmaa sõltub paljust, mida leht ei tea ega küsi: juhi reaktsioonist, rehvide tegelikust seisukorrast ja rõhust, teekattest, veekihi paksusest, temperatuurist, pidurite ja ABS-i seisukorrast, koormast ja auto tehnilisest korrasolekust.</li><li>Päris elus võib pidurdusmaa olla lehel näidatust oluliselt pikem.</li><li>Rehvide võrdlus ja „sobivus sinu valikute põhjal“ on andmete kõrvutus, <strong>mitte ostunõuanne</strong> ega soovitus konkreetse toote kasuks.</li></ul>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>3. Milleks lehte kasutada ei tohi</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li>kiiruse, pikivahe või pidurdamise otsustamiseks liikluses — sõida alati vastavalt oludele ja liiklusseadusele;</li><li>liiklusõnnetuse asjaolude hindamiseks, ekspertarvamuseks, kindlustus- või kohtumenetluses tõendina;</li><li>sõiduki või rehvide tehnilise korrasoleku hindamiseks.</li></ul>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>4. Andmed ja allikad</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li>Rehvimärgise andmed pärinevad EL-i tooteregistrist EPREL, testitulemused kolmandate osapoolte avaldatud testidest. Iga allikas on lehel viidatud.</li><li>Andmetes võib olla vigu, lünki või aegunud infot. Me ei vastuta kolmandate osapoolte andmete õigsuse eest.</li><li>Tootjate ja toodete nimed ning kaubamärgid kuuluvad nende omanikele.</li><li>Leht näitab ainult omadusi, mille kohta on usaldusväärsed andmed, ega arva midagi juurde.</li></ul>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>5. Vastutuse piirang</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Leht ja selle sisu antakse kasutada „nagu on“, ilma otseste või kaudsete garantiideta. Seadusega lubatud ulatuses ei vastuta Rabarvo OÜ otsese ega kaudse kahju eest, mis tuleneb lehe kasutamisest, sellele tuginemisest või selle kättesaamatusest. Kasutaja vastutab ise otsuste eest, mida ta lehe teabe põhjal teeb.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>6. Muudatused</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Arvutusmudel, andmed ja need tingimused võivad muutuda. Kehtib lehel avaldatud versioon.</p>
<!-- /wp:paragraph -->
HTML;
}

function pm_content_teadmine(): string {
	return <<<'HTML'
<!-- wp:paragraph -->
<p>Pidurdusmaa.ee näitab arvutatud pidurdusmaad ja rehvide päris omadusi. Siin on kirjas, kust iga number tuleb ja mida me <strong>ei</strong> tea.</p>
<!-- /wp:paragraph -->
<!-- wp:list -->
<ul><li><a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a> — mudel, eeldused, täpsus ja piirangud</li><li><a href="/teadmine/rehvimargis/">EL-i rehvimärgis</a> — mida märghaardumise, veeretakistuse ja müra klass tähendavad</li><li><a href="/testid/">Sõltumatud testid</a> — millised testid on andmestikus ja kuidas neid kasutatakse</li></ul>
<!-- /wp:list -->
HTML;
}

function pm_content_metoodika(): string {
	return <<<'HTML'
<!-- wp:paragraph -->
<p>Kalkulaator <strong>arvutab</strong> pidurdusmaa. See ei ole laborimõõtmine ega lubadus, et sinu auto peatub täpselt selle meetri pealt. Tulemus on hinnang, millel on alati veapiir, ja leht näitab seda veapiiri iga tulemuse juures.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>Mida mudel teeb</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Pidurdus simuleeritakse väikeste ajasammudega: iga hetk arvutatakse rehvi ja tee vaheline haare antud kiirusel, ABS-i tõhusus, õhutakistus, veeretakistus, kalle ja pidurite võimekus. Haare sõltub kiirusest (märjal kukub ta kiiruse kasvades rohkem kui kuival), temperatuurist ja rehvi kategooriast.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>Kust tuleb rehvi haare</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li><strong>Märjal</strong> tuleb haare EL-i rehvimärgise märghaardumise indeksist. Indeks on ametliku UNECE R117 katse tulemus (märg asfalt, 80 → 20 km/h, võrdlusrehvi suhtes). Mudel teisendab selle haardeks ühe kordajaga, mis on sobitatud 85 mõõdetud märja pidurdusmaa vastu.</li><li><strong>Sõltumatult testitud rehvidel</strong> on indeks tuletatud testi enda mõõdetud märjast pidurdusmaast — see on täpsem kui märgise klass.</li><li><strong>Ainult märgisega rehvidel</strong> on teada ainult klass (A–E), mitte täpne number. Mudel kasutab klassi keskpunkti ja lisab veapiirile ±4,5 %. Mõõtsime järele: mõõdetud rehvide hajuvus ühe klassi sees oli 2,4–3,9 %.</li><li><strong>Kuival, lumel ja jääl</strong> ei ütle märgis midagi. Testitud rehvidel kasutatakse testi tulemust, teistel rehvi kategooria keskmist. Seetõttu ei järjesta leht ainult märgisega rehve kuival, lumel ega jääl — nad oleksid kõik võrdsed ja see näeks välja nagu teadmine, mida meil ei ole.</li></ul>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>Avalehe teeolud</h2>
<!-- /wp:heading -->
<!-- wp:table -->
<figure class="wp-block-table"><table><thead><tr><th>Valik</th><th>Mida arvutatakse</th></tr></thead><tbody><tr><td>Märg</td><td>märg asfalt, veekiht 1 mm, +10 °C</td></tr><tr><td>Kuiv</td><td>kuiv asfalt, +15 °C</td></tr><tr><td>Lumi</td><td>tallatud lumi, −5 °C</td></tr><tr><td>Jää</td><td>jää, −5 °C</td></tr></tbody></table></figure>
<!-- /wp:table -->
<!-- wp:paragraph -->
<p>Rehv on uus (mustrisügavus 8 mm), rõhk tehase soovituse järgi, autos juht (75 kg). Pidurdusmaa algab hetkest, kui pidur on põhjas — reaktsiooniaega ei arvestata, sest see tuleb inimesest, mitte rehvist.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>Kui täpne see on</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li>369 mõõdetud pidurdusmaa vastu (ADAC, Tekniikan Maailma, UTAC) on mudeli jääkviga asfaldil (märg ja kuiv) 4,4 %, betoonil 6,6 %, lumel 5,5 %, jääl 6,9 %.</li><li>Kontroll testidega, mida mudel kunagi ei näinud (Vi Bilägare 2010, teine mõõt ja teised kiirused): kuival 3,2–5,7 %.</li><li>Iga tulemuse juures on vahemik. Vaikimisi näidatakse keskmist hinnangut.</li></ul>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>Piirangud</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li>Kummisegu. Parimate rehvide vahe märjal on umbes 17 %, ja see tuleb peamiselt segust, mida tootjad ei avalda.</li><li>Lörtsi, märga või külmunud kruusa ja kurvis pidurdamist.</li><li>Rehvide järjestust lumel ja jääl, kui rehv ei ole testitud.</li></ul>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>Andmete liigid</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li><strong>Ametlik</strong> — EL-i tooteregister EPREL (rehvimärgis).</li><li><strong>Sõltumatu test</strong> — ajakirja või autoklubi mõõdetud tulemus, allika ja aastaga.</li><li><strong>Arvutatud hinnang</strong> — selle lehe mudel.</li><li><strong>Sinu sisend</strong> — auto, kiirus, teeolud.</li></ul>
<!-- /wp:list -->
HTML;
}

function pm_content_margis(): string {
	return <<<'HTML'
<!-- wp:paragraph -->
<p>Igal Euroopas müüdaval sõiduauto rehvil on EL-i rehvimärgis (määrus 2020/740). Andmed tulevad EL-i tooteregistrist EPREL.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>Märghaardumine (A–E)</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Mõõdetakse märjal asfaldil 80 → 20 km/h, võrdluses standardse võrdlusrehviga. Klassi A ja E vahe on tavalisel sõiduautol 90 km/h juures umbes 18 meetrit (klasside keskpunktide järgi arvutatud). Klass on <strong>mõõdupõhine</strong>: sama rehvimudel võib olla ühes mõõdus A ja teises B.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>Veeretakistus (A–E)</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Mõjutab kütuse- või energiakulu. Pidurdusmaaga ei ole otsest seost — kontrollisime seda 41 testitud rehvi peal ja veeretakistuse klass ei seletanud märja pidurduse erinevusi.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>Müra (dB ja A–C)</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Rehvi veeremismüra ametliku katse järgi. Väiksem number = vaiksem rehv. Iga 3 dB on ligikaudu kahekordne heliväljund.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>Lume- ja jäämärk</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Kolme mäetipu ja lumehelbe märk (3PMSF) tähendab, et rehv läbis lumehaarde katse. Jäämärk tähendab Põhjamaade jääkatse läbimist (ainult sõiduauto rehvid).</p>
<!-- /wp:paragraph -->
HTML;
}
