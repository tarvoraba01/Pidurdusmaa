/* Cloudflare Turnstile — kontaktivormi kaitse robotite eest.
 *
 * Brauseris lahendab Turnstile väikese kontrolli (enamasti nähtamatult)
 * ja annab vormile ühekordse loa (token). Siin küsime Cloudflare'ilt, kas
 * luba on ehtne. Salajane võti on AINULT serveri keskkonnamuutujas:
 *
 *   TURNSTILE_SECRET   Cloudflare → Turnstile → sinu vidin → Secret key
 *
 * Avalik võti (site key) on failis src/lib/seaded.js. Mõlemad peavad
 * olema seatud korraga — kui salajane võti puudub, kontrolli ei tehta.
 */
const VERIFY = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';

/** @returns {Promise<{ok: boolean, why?: string}>} */
export async function kontrolliTurnstile(token, ip) {
	const secret = process.env.TURNSTILE_SECRET;
	if (!secret) return { ok: true };
	if (!token || typeof token !== 'string' || token.length > 2048) return { ok: false, why: 'puudub' };
	try {
		const body = new URLSearchParams({ secret, response: token });
		if (ip) body.set('remoteip', ip);
		// TURNSTILE_VERIFY_URL ainult automaattestide jaoks (Cloudflare'i asendus)
		const r = await fetch(process.env.TURNSTILE_VERIFY_URL || VERIFY, {
			method: 'POST',
			body,
			signal: AbortSignal.timeout(8000)
		});
		const d = await r.json();
		return d && d.success ? { ok: true } : { ok: false, why: (d && d['error-codes'] || []).join(',') || 'tagasi lükatud' };
	} catch (e) {
		/* Cloudflare ei vasta: ei kaota päris inimese kirja, aga logime.
		   Sagedusepiir (5 kirja tunnis ühelt IP-lt) kehtib ikka. */
		console.error('Turnstile:', e.message);
		return { ok: true, why: 'kontroll ei vastanud' };
	}
}
