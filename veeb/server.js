/* Pidurdusmaa.ee — käivitusfail (tavalise `node build` asemel).
 *
 * Miks eraldi fail: lehed on eelrenderdatud ja SvelteKit annab need välja
 * otse failidena, ilma hooks.server.js-ist läbi käimata. Turvapäised ja
 * suunamised peavad seega olema siin, enne SvelteKiti — siis kehtivad need
 * KÕIGILE vastustele (lehed, pildid, API).
 *
 * Ehitus kopeerib selle faili kausta build/ (vt package.json → postbuild),
 * Dockerfile käivitab `node build/server.js`.
 *
 * Suunamised — alati ÜKS samm ja alati 301:
 *   www.pidurdusmaa.ee/rehvid   → https://pidurdusmaa.ee/rehvid/
 *   pidurdusmaa.ee/rehvid       → https://pidurdusmaa.ee/rehvid/
 * (Varem: www → 302 → pidurdusmaa.ee/rehvid → 308 → /rehvid/ = kaks sammu.)
 */
import http from 'node:http';
import { handler } from './handler.js';

const HOST = process.env.KANOONILINE_HOST || 'pidurdusmaa.ee';
const PORT = Number(process.env.PORT || 3000);
const LISTEN = process.env.HOST || '0.0.0.0';

/* Välised aadressid, mida leht tohib kasutada:
 *   Google Analytics (ainult pärast küpsiste nõusolekut)
 *   Cloudflare Turnstile (kontaktivormi robotikaitse)
 * Uue välise teenuse lisamisel tuleb see siia lisada, muidu brauser
 * blokeerib selle (konsoolis on siis „Content Security Policy“ viga). */
const GA = 'https://www.googletagmanager.com';
const GTM_KOIK = 'https://*.googletagmanager.com';
const GA_KOGU = 'https://*.google-analytics.com https://*.analytics.google.com';
const CF = 'https://challenges.cloudflare.com';

const CSP = [
	"default-src 'self'",
	/* 'unsafe-inline': SvelteKiti käivitusskript on lehe sees. Välist
	   skripti ei saa laadida mujalt kui allolevatelt aadressidelt. */
	`script-src 'self' 'unsafe-inline' ${GA} ${CF}`,
	"style-src 'self' 'unsafe-inline'",
	`img-src 'self' data: blob: ${GTM_KOIK} ${GA_KOGU}`,
	"font-src 'self'",
	`connect-src 'self' ${GTM_KOIK} ${GA_KOGU} ${CF}`,
	`frame-src ${CF}`,
	"frame-ancestors 'self'",
	"base-uri 'self'",
	"form-action 'self'",
	"object-src 'none'",
	'upgrade-insecure-requests'
].join('; ');

const PAISED = {
	/* brauser kasutab 1 aasta jooksul ainult https-i */
	'Strict-Transport-Security': 'max-age=31536000',
	'Content-Security-Policy': CSP,
	'X-Content-Type-Options': 'nosniff',
	'X-Frame-Options': 'SAMEORIGIN',
	'Referrer-Policy': 'strict-origin-when-cross-origin',
	'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()',
	'Cross-Origin-Opener-Policy': 'same-origin-allow-popups'
};

/** Kas aadress on leht, mis peab lõppema kaldkriipsuga? */
function vajabKaldkriipsu(tee) {
	if (tee.endsWith('/')) return false;
	if (tee.startsWith('/api/') || tee.startsWith('/_app/')) return false;
	const viimane = tee.slice(tee.lastIndexOf('/') + 1);
	return !viimane.includes('.'); // failid (.png, .xml, .txt) jäävad nagu on
}

function suunamine(req) {
	if (req.method !== 'GET' && req.method !== 'HEAD') return null;
	const host = String(req.headers.host || '').toLowerCase().replace(/:\d+$/, '');
	const proto = String(req.headers['x-forwarded-proto'] || '').split(',')[0].trim();
	const url = req.url || '/';
	const q = url.indexOf('?');
	let tee = q < 0 ? url : url.slice(0, q);
	const paring = q < 0 ? '' : url.slice(q);

	/* ainult meie enda domeenid; localhost, 127.0.0.1 ja tervisekontroll jäävad puutumata */
	const meie = host === HOST || host === 'www.' + HOST;
	if (!meie) return null;

	let muutus = false;
	if (host !== HOST) muutus = true; // www → ilma www-ta
	if (proto === 'http') muutus = true; // http → https (kui proksi selle meile saadab)
	if (/\/\/+/.test(tee)) {
		tee = tee.replace(/\/\/+/g, '/');
		muutus = true;
	}
	if (vajabKaldkriipsu(tee)) {
		tee += '/';
		muutus = true;
	}
	return muutus ? `https://${HOST}${tee}${paring}` : null;
}

const server = http.createServer((req, res) => {
	for (const [k, v] of Object.entries(PAISED)) res.setHeader(k, v);

	const kuhu = suunamine(req);
	if (kuhu) {
		res.writeHead(301, { Location: kuhu, 'Cache-Control': 'public, max-age=86400' });
		return res.end();
	}
	handler(req, res, () => {
		res.statusCode = 404;
		res.end('Not found');
	});
});

server.listen(PORT, LISTEN, () => console.log(`Listening on http://${LISTEN}:${PORT}`));

/* Coolify peatab vana konteineri SIGTERM-iga: lõpeta pooleli päringud ära */
function sulge() {
	server.close(() => process.exit(0));
	setTimeout(() => process.exit(0), 10_000).unref();
}
process.on('SIGTERM', sulge);
process.on('SIGINT', sulge);
