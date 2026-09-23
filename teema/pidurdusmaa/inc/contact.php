<?php
/**
 * Kontaktivorm: /kontakt/ → POST /wp-json/pm/v1/kontakt → wp_mail().
 *
 * Saaja aadress on AINULT siin serveris (mitte lehe HTML-is), et
 * rämpsposti robotid seda lehelt ei korjaks. Muuda PM_CONTACT_TO või
 * lisa wp-config.php-sse define( 'PM_CONTACT_TO', '…' ).
 *
 * Kaitse: nonce, peidetud „mesipott“ väli, minimaalne täitmisaeg ja
 * piirang 5 kirja tunnis ühelt IP-lt. Kirja „Vasta“ läheb saatjale.
 *
 * NB: paljud hostingud ei saada wp_mail() kirju usaldusväärselt (eriti
 * Hotmaili/Outlooki postkasti). Siis paigalda SMTP-plugin (nt WP Mail SMTP)
 * — teema koodi muuta pole vaja.
 *
 * @package pidurdusmaa
 */

defined( 'ABSPATH' ) || exit;

if ( ! defined( 'PM_CONTACT_TO' ) ) {
	define( 'PM_CONTACT_TO', 'rabarvo@hotmail.com' );
}

/** Kontaktivormi teemad (võti => silt). */
function pm_contact_topics(): array {
	return array(
		'myyja'  => 'Olen rehvimüüja — hinnad / koostöö',
		'andmed' => 'Andmetes on viga',
		'ettepanek' => 'Ettepanek või tagasiside',
		'muu'    => 'Muu',
	);
}

add_action(
	'rest_api_init',
	static function () {
		register_rest_route(
			'pm/v1',
			'/kontakt',
			array(
				'methods'             => 'POST',
				'permission_callback' => '__return_true',
				'callback'            => 'pm_rest_kontakt',
			)
		);
	}
);

/**
 * @param WP_REST_Request $req Päring.
 */
function pm_rest_kontakt( $req ) {
	$err = static fn( $msg, $code = 400 ) => new WP_REST_Response( array( 'ok' => false, 'msg' => $msg ), $code );

	if ( ! wp_verify_nonce( (string) $req->get_param( '_pm' ), 'pm_kontakt' ) ) {
		return $err( 'Leht on liiga kaua lahti olnud. Värskenda lehte ja proovi uuesti.', 403 );
	}
	// Robotid täidavad peidetud välja ja saadavad vormi kohe.
	if ( '' !== trim( (string) $req->get_param( 'veeb' ) ) ) {
		return new WP_REST_Response( array( 'ok' => true ), 200 );
	}
	$t0 = (int) $req->get_param( '_t' );
	if ( $t0 && time() - $t0 < 3 ) {
		return new WP_REST_Response( array( 'ok' => true ), 200 );
	}

	$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
	$key = 'pm_k_' . md5( $ip );
	$n   = (int) get_transient( $key );
	if ( $n >= 5 ) {
		return $err( 'Liiga palju kirju lühikese ajaga. Proovi tunni aja pärast uuesti.', 429 );
	}

	$nimi   = sanitize_text_field( (string) $req->get_param( 'nimi' ) );
	$email  = sanitize_email( (string) $req->get_param( 'email' ) );
	$firma  = sanitize_text_field( (string) $req->get_param( 'firma' ) );
	$teema  = (string) $req->get_param( 'teema' );
	$sonum  = sanitize_textarea_field( (string) $req->get_param( 'sonum' ) );
	$topics = pm_contact_topics();

	if ( '' === $nimi || mb_strlen( $nimi ) > 120 ) {
		return $err( 'Palun kirjuta oma nimi.' );
	}
	if ( ! is_email( $email ) ) {
		return $err( 'Palun kontrolli e-posti aadressi — sellele vastame.' );
	}
	if ( mb_strlen( $sonum ) < 5 || mb_strlen( $sonum ) > 5000 ) {
		return $err( 'Palun kirjuta sõnum (5–5000 märki).' );
	}
	$teema_silt = $topics[ $teema ] ?? $topics['muu'];

	$subject = '[Pidurdusmaa.ee] ' . $teema_silt . ' — ' . $nimi;
	$body    = "Teema: {$teema_silt}\nNimi: {$nimi}\nE-post: {$email}\n" .
		( $firma ? "Ettevõte: {$firma}\n" : '' ) .
		"\n{$sonum}\n\n—\nSaadetud lehe " . home_url( '/kontakt/' ) . ' kontaktivormist ' . wp_date( 'd.m.Y H:i' ) . '.';
	$headers = array(
		'Content-Type: text/plain; charset=UTF-8',
		'Reply-To: ' . str_replace( array( "\r", "\n" ), '', $nimi ) . ' <' . $email . '>',
	);

	$sent = wp_mail( PM_CONTACT_TO, $subject, $body, $headers );
	if ( ! $sent ) {
		return $err( 'Kirja saatmine ebaõnnestus serveri poolel. Proovi hiljem uuesti.', 500 );
	}
	set_transient( $key, $n + 1, HOUR_IN_SECONDS );
	return new WP_REST_Response( array( 'ok' => true ), 200 );
}
