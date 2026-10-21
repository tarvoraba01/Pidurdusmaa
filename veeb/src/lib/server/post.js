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
import { LOGO_PNG } from './meililogo.js';

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
			body: JSON.stringify({ content: tekst, text: tekst, subject, replyTo, allowed_mentions: { parse: [] } }), /* @everyone kirjas ei pingi kõiki */
			signal: AbortSignal.timeout(8000)
		});
		return r.ok;
	} catch (e) {
		console.error('Teade:', e.message);
		return false;
	}
}

/* ---- Automaatne kinnitus kirja saatjale ----
 * „Täname teid kirja eest! Pidurdusmaa.ee vastab teile 24 h jooksul.“
 * Spämmikaitse (vorm ei tohi muutuda tasuta meilisaatjaks):
 *  - tekst on FIKSEERITUD: kasutaja nime, sõnumit ega linke kirja ei panda;
 *  - saadetakse ainult siis, kui Turnstile on päriselt sees ja läbitud
 *    (kutsuja kontrollib) ning sama aadress saab kuni 1 kinnituse ööpäevas;
 *  - Reply-To = meie postkast, nii et vastus jõuab Tarvoni. */
const KINNITUS = {
	et: {
		subject: 'Täname teid kirja eest | Pidurdusmaa.ee',
		tere: 'Tere!', p1: 'Täname teid kirja eest! Vastame teile 24 tunni jooksul.', p2: 'See on automaatne kinnitus. Kui soovite midagi lisada, vastake lihtsalt sellele kirjale.', url: 'https://pidurdusmaa.ee/'
	},
	en: {
		subject: 'Thank you for your message | Pidurdusmaa.ee',
		tere: 'Hello!', p1: 'Thank you for your message. We will reply within 24 hours.', p2: 'This is an automatic confirmation. If you want to add something, simply reply to this e-mail.', url: 'https://pidurdusmaa.ee/en/'
	},
	ru: {
		subject: 'Спасибо за письмо | Pidurdusmaa.ee',
		tere: 'Здравствуйте!', p1: 'Спасибо за ваше письмо. Мы ответим вам в течение 24 часов.', p2: 'Это автоматическое подтверждение. Если хотите что-то добавить, просто ответьте на это письмо.', url: 'https://pidurdusmaa.ee/ru/'
	}
};

/* Tekstiversioon: allkirjas ainult üks link (enne oli „Pidurdusmaa.ee“ + URL eraldi reana, mis
   meiliprogrammis tegi kaks linki järjest. Tarvo 21.10). */
function kinnitusTekst(k) {
	return `${k.tere}\n\n${k.p1}\n\n${k.p2}\n\nPidurdusmaa.ee\n`;
}
/* HTML-versioon: logo (P + Pidurdusmaa.ee) üleval, rahulik tekst, allkirjas üks link. Tabelid ja
   inline-stiilid, sest meiliprogrammid ei toeta muud. Värvideta taust töötab ka tumedas režiimis. */
function kinnitusHtml(k) {
	return `<!doctype html><html><body style="margin:0;padding:0">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding:24px 16px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="max-width:520px;width:100%;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;font-size:16px;line-height:1.55">
<tr><td style="padding:0 0 24px"><a href="${k.url}" style="text-decoration:none;color:inherit"><img src="cid:logo@pidurdusmaa.ee" width="40" height="40" alt="" style="vertical-align:middle;border:0;border-radius:9px"> <span style="vertical-align:middle;font-size:20px;font-weight:800;letter-spacing:-0.01em;padding-left:8px">Pidurdusmaa<span style="font-weight:400">.ee</span></span></a></td></tr>
<tr><td style="padding:0 0 12px">${k.tere}</td></tr>
<tr><td style="padding:0 0 12px">${k.p1}</td></tr>
<tr><td style="padding:0 0 24px">${k.p2}</td></tr>
<tr><td style="padding:16px 0 0;border-top:1px solid #d9d9d9;font-size:14px;opacity:0.75"><a href="${k.url}" style="color:inherit">Pidurdusmaa.ee</a></td></tr>
</table></td></tr></table></body></html>`;
}

/** Saada kinnitus aadressile `to`. lang = 'et' | 'en' | 'ru'. true = saadetud. */
export async function saadaKinnitus(to, lang = 'et') {
	const t = smtp();
	if (!t) return false;
	const k = KINNITUS[lang] || KINNITUS.et;
	const from = process.env.MAIL_FROM || process.env.SMTP_USER;
	try {
		await t.sendMail({
			from: `"Pidurdusmaa.ee" <${from}>`,
			to,
			replyTo: process.env.MAIL_TO || from,
			subject: k.subject,
			text: kinnitusTekst(k),
			html: kinnitusHtml(k),
			attachments: [{ filename: 'pidurdusmaa.png', content: LOGO_PNG, cid: 'logo@pidurdusmaa.ee', contentDisposition: 'inline' }],
			headers: { 'Auto-Submitted': 'auto-replied', 'X-Auto-Response-Suppress': 'All' }
		});
		return true;
	} catch (e) {
		console.error('Kinnitus:', e.code || '', e.message);
		return false;
	}
}

/** Saadab kirja kõigisse seadistatud kanalitesse. true = vähemalt üks õnnestus. */
export async function saadaKiri(kiri) {
	const [a, b] = await Promise.all([saadaEpost(kiri), saadaTeade(kiri)]);
	return a || b;
}
