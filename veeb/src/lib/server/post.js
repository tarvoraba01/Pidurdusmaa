/* Teavitus uuest kirjast.
 *
 * Kiri kirjutatakse alati faili (vt api/kontakt) — see on ainus koht,
 * kus ta kindlasti alles on. Lisaks saab seadistada ühe teavituskanali:
 *
 *   TEADE_URL  — aadress, kuhu POSTitatakse JSON {tekst, kiri}.
 *                Töötab Discordi ja Slacki webhook'iga, n8n-i,
 *                Make'i või oma väikese releega.
 *
 * SMTP-d siin teadlikult ei ole: käsitsi kirjutatud SMTP-klient on
 * õrn (STARTTLS, autentimine, serverite erisused) ja seda ei saa
 * ilma päris postiserverita ausalt läbi testida. Kui kirjad on vaja
 * otse e-postile, lisa nodemailer ja üks funktsioon siia asemele —
 * ülejäänud kood ei muutu.
 */

export async function saadaKiri({ subject, text, replyTo }) {
	const url = process.env.TEADE_URL;
	if (!url) return false;

	const tekst = subject + '\n\n' + text + (replyTo ? '\n\nVasta: ' + replyTo : '');
	try {
		const r = await fetch(url, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			/* "content" on Discordi väljanimi, "text" Slacki oma — saadame
			   mõlemad, siis töötab ilma seadistamiseta mõlemas. */
			body: JSON.stringify({ content: tekst, text: tekst, subject, replyTo }),
			signal: AbortSignal.timeout(8000)
		});
		return r.ok;
	} catch (e) {
		console.error('Teade:', e.message);
		return false;
	}
}
