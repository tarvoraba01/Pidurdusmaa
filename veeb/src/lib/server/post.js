/* Kontaktivormi kirja edastamine.
 *
 * Kiri kirjutatakse alati faili (vt api/kontakt): see on koht, kus ta
 * kindlasti alles on. Lisaks saadetakse see edasi:
 *
 *   E-post (SMTP). Keskkonnamuutujad, mis on seatud ainult serveris
 *   (Coolify → Environment Variables), mitte koodis:
 *     SMTP_HOST   smtp.gmail.com
 *     SMTP_PORT   465 (SSL), vaikimisi 465
 *     SMTP_USER   Gmaili aadress
 *     SMTP_PASS   Gmaili RAKENDUSE parool (app password), mitte põhiparool
 *     MAIL_TO     kuhu kiri saadetakse, vaikimisi tarvo.raba01@gmail.com
 *     MAIL_FROM   saatja, vaikimisi SMTP_USER
 *   Kirja Reply-To on vormi täitja aadress, nii et "Vasta" läheb otse
 *   talle.
 *
 *   TEADE_URL   valikuline lisateade: aadress, kuhu POSTitatakse JSON
 *               (Discordi/Slacki webhook, n8n vms).
 *
 * Kui SMTP pole seadistatud, jääb kiri ainult faili.
 */
import nodemailer from 'nodemailer';

let transport = null;
function smtp() {
	const { SMTP_HOST, SMTP_USER, SMTP_PASS } = process.env;
	if (!SMTP_HOST || !SMTP_USER || !SMTP_PASS) return null;
	if (!transport) {
		const port = Number(process.env.SMTP_PORT || 465);
		transport = nodemailer.createTransport({
			host: SMTP_HOST,
			port,
			secure: port === 465, // 465 = SSL kohe; 587 = STARTTLS
			auth: { user: SMTP_USER, pass: SMTP_PASS },
			connectionTimeout: 10000,
			greetingTimeout: 10000,
			socketTimeout: 15000
		});
	}
	return transport;
}

async function saadaEpost({ subject, text, replyTo }) {
	const t = smtp();
	if (!t) return false;
	const from = process.env.MAIL_FROM || process.env.SMTP_USER;
	try {
		await t.sendMail({
			from: `"Pidurdusmaa.ee" <${from}>`,
			to: process.env.MAIL_TO || 'tarvo.raba01@gmail.com',
			replyTo: replyTo || undefined,
			subject,
			text
		});
		return true;
	} catch (e) {
		// ainult veateade, mitte seaded ega parool
		console.error('E-post:', e.code || '', e.message);
		return false;
	}
}

async function saadaTeade({ subject, text, replyTo }) {
	const url = process.env.TEADE_URL;
	if (!url) return false;
	const tekst = subject + '\n\n' + text + (replyTo ? '\n\nVasta: ' + replyTo : '');
	try {
		const r = await fetch(url, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			/* "content" on Discordi väljanimi, "text" Slacki oma */
			body: JSON.stringify({ content: tekst, text: tekst, subject, replyTo }),
			signal: AbortSignal.timeout(8000)
		});
		return r.ok;
	} catch (e) {
		console.error('Teade:', e.message);
		return false;
	}
}

/** Saadab kirja kõigisse seadistatud kanalitesse. true = vähemalt üks õnnestus. */
export async function saadaKiri(kiri) {
	const [a, b] = await Promise.all([saadaEpost(kiri), saadaTeade(kiri)]);
	return a || b;
}
