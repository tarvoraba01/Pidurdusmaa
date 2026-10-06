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
 *   /rehvid/michelin-pilot-sport-4-ao → https://pidurdusmaa.ee/rehvid/michelin-pilot-sport-4/
 *   pidurdusmaa.com/testid, www.pidurdusmaa.eu → https://pidurdusmaa.ee/…
 * (Varem: www → 302 → pidurdusmaa.ee/rehvid → 308 → /rehvid/ = kaks sammu.)
 */
import http from 'node:http';
import { readFileSync } from 'node:fs';
import { handler } from './handler.js';

/* Koondatud rehvimudelid (SEO samm 5): vana aadress → uus.
 * Nt /rehvid/michelin-pilot-sport-4-ao/ → /rehvid/michelin-pilot-sport-4/
 *    /rehvid/nankang-145-65r15-72v-as-1/ → /rehvid/nankang-as-1/
 * Fail tehakse andmete ekspordiga (mudel/koondamine.py). */
let REHVID = {};
try {
	REHVID = JSON.parse(readFileSync(new URL('./client/data/suunamised.json', import.meta.url), 'utf-8'));
} catch {
	/* faili pole (nt arenduses) — suunamisi pole */
}

const HOST = process.env.KANOONILINE_HOST || 'pidurdusmaa.ee';
/* Lisadomeenid, mis suunatakse (301) põhidomeenile — koos www-ga.
 * Lisamiseks: DNS-is A-kirje sama IP peale + domeen Coolifys rakenduse
 * „Domains“ alla (siis tuleb ka SSL-sertifikaat). */
const LISAD = new Set(
	['pidurdusmaa.com', 'pidurdusmaa.eu']
		.concat(String(process.env.LISA_DOMEENID || '').split(',').map((d) => d.trim().toLowerCase()).filter(Boolean))
		.flatMap((d) => [d, 'www.' + d])
);
const PORT = Number(process.env.PORT || 3000);
const LISTEN = process.env.HOST || '0.0.0.0';

/* Välised aadressid, mida leht tohib kasutada:
 *   Google Analytics (ainult pärast küpsiste nõusolekut)
 *   Cloudflare Turnstile (kontaktivormi robotikaitse)
 *   Plausible (küpsisteta statistika, oma server track.pidurdusmaa.ee)
 * Uue välise teenuse lisamisel tuleb see siia lisada, muidu brauser
 * blokeerib selle (konsoolis on siis „Content Security Policy“ viga). */
const GA = 'https://www.googletagmanager.com';
const GTM_KOIK = 'https://*.googletagmanager.com';
const GA_KOGU = 'https://*.google-analytics.com https://*.analytics.google.com';
const CF = 'https://challenges.cloudflare.com';
const PLAUSIBLE = 'https://track.pidurdusmaa.ee';

const CSP = [
	"default-src 'self'",
	/* 'unsafe-inline': SvelteKiti käivitusskript on lehe sees. Välist
	   skripti ei saa laadida mujalt kui allolevatelt aadressidelt. */
	`script-src 'self' 'unsafe-inline' ${GA} ${CF} ${PLAUSIBLE}`,
	"style-src 'self' 'unsafe-inline'",
	`img-src 'self' data: blob: ${GTM_KOIK} ${GA_KOGU}`,
	"font-src 'self'",
	`connect-src 'self' ${GTM_KOIK} ${GA_KOGU} ${CF} ${PLAUSIBLE}`,
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
	const meie = host === HOST || host === 'www.' + HOST || LISAD.has(host);
	if (!meie) return null;

	let muutus = false;
	if (host !== HOST) muutus = true; // www → ilma www-ta
	if (proto === 'http') muutus = true; // http → https (kui proksi selle meile saadab)
	if (/\/\/+/.test(tee)) {
		tee = tee.replace(/\/\/+/g, '/');
		muutus = true;
	}
	const r = /^\/rehvid\/([a-z0-9-]+)\/?$/.exec(tee);
	if (r && Object.hasOwn(REHVID, r[1])) {
		tee = '/rehvid/' + REHVID[r[1]] + '/';
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
	/* PWA: service worker ja manifest peavad iga deploy järel kohe uuenema */
	const tee0 = (req.url || '').split('?')[0];
	if (tee0 === '/service-worker.js' || tee0 === '/manifest.webmanifest') res.setHeader('Cache-Control', 'no-cache');
	if (tee0 === '/manifest.webmanifest') res.setHeader('Content-Type', 'application/manifest+json; charset=utf-8');
	/* llms.txt on eesti tekst — ilma charset'ita loeks mõni AI-robot täpitähed valesti */
	if (tee0 === '/llms.txt') res.setHeader('Content-Type', 'text/plain; charset=utf-8');
	/* Vahemälu (audit 6.10): andmefailid küsitakse alati ?v=<versioon> parameetriga,
	   seega võivad need aasta brauseris olla; fondid 30 päeva; HTML iga kord
	   üle kontrollida (ETag on olemas — muutmata lehte uuesti ei laadita).
	   _app/immutable/* päised paneb adapter ise. */
	if (!tee0.startsWith('/_app/')) {
		if (tee0.startsWith('/data/')) res.setHeader('Cache-Control', /[?&]v=/.test(req.url || '') ? 'public, max-age=31536000, immutable' : 'public, max-age=300');
		else if (tee0.startsWith('/fonts/')) res.setHeader('Cache-Control', 'public, max-age=2592000');
		else if (tee0.endsWith('/') || tee0.endsWith('.html')) res.setHeader('Cache-Control', 'no-cache');
	}
	handler(req, res, () => {
		res.statusCode = 404;
		res.end('Not found');
	});
});

server.listen(PORT, LISTEN, () => console.log(`Listening on http://${LISTEN}:${PORT}`));

/* IndexNow: pärast deploy'd teatame Bingile, Yandexile jt (api.indexnow.org
 * jagab teadet kõigiga), millised lehed on uued või muutunud. Google seda ei
 * kasuta — Google loeb saidikaarti (lastmod = lehe päris muutus, vt
 * scripts/lastmod.mjs).
 * Võti EI OLE saladus: see peabki olema avalik failis /<võti>.txt, sellega
 * tõestame, et sait on meie oma.
 * Mis on juba teatatud, hoitakse Supabase'i tabelis seis (voti 'indexnow'),
 * kui SUPABASE_URL ja SUPABASE_SECRET_KEY on seatud; muidu failis
 * LOG_DIR/indexnow.json (Coolify püsikaust). Kui kumbagi pole, teatatakse
 * viimase 7 päeva muutused.
 * Välja lülitamiseks: keskkonnamuutuja INDEXNOW=0. */
const INDEXNOW_VOTI = '338c17d8674a0c635991930347fc5fbd';

/* Väike Supabase'i abiline ainult IndexNow oleku jaoks (vt src/lib/server/supabase.js) */
function sbSeis() {
	const url = String(process.env.SUPABASE_URL || '').trim().replace(/\/+$/, '');
	const voti = String(process.env.SUPABASE_SECRET_KEY || '').trim();
	if (!/^https:\/\//.test(url) || voti.length < 20) return null;
	const pais = { apikey: voti, 'Content-Type': 'application/json' };
	if (voti.startsWith('eyJ')) pais.Authorization = 'Bearer ' + voti;
	return {
		async loe(nimi) {
			const r = await fetch(`${url}/rest/v1/seis?voti=eq.${encodeURIComponent(nimi)}&select=vaartus`, { headers: pais, signal: AbortSignal.timeout(15000) });
			if (!r.ok) throw new Error('Supabase seis: HTTP ' + r.status);
			const rida = (await r.json())[0];
			return rida ? rida.vaartus : null;
		},
		async kirjuta(nimi, vaartus) {
			const r = await fetch(`${url}/rest/v1/seis`, {
				method: 'POST',
				headers: { ...pais, Prefer: 'resolution=merge-duplicates,return=minimal' },
				body: JSON.stringify({ voti: nimi, vaartus, uuendatud: new Date().toISOString() }),
				signal: AbortSignal.timeout(30000)
			});
			if (!r.ok) throw new Error('Supabase seis: HTTP ' + r.status);
		}
	};
}
async function indexNow() {
	const { readFile, writeFile } = await import('node:fs/promises');
	const { join } = await import('node:path');
	const xml = await readFile(new URL('./prerendered/sitemap.xml', import.meta.url), 'utf-8');
	const lehed = [...xml.matchAll(/<loc>([^<]+)<\/loc><lastmod>([^<]+)<\/lastmod>/g)].map((m) => [m[1], m[2]]);
	const olekFail = join(process.env.LOG_DIR || new URL('./', import.meta.url).pathname, 'indexnow.json');
	const sbs = sbSeis();
	let olek = null;
	if (sbs) {
		try {
			olek = await sbs.loe('indexnow');
		} catch (e) {
			console.log('IndexNow:', e.message);
		}
	}
	if (!olek) {
		try {
			olek = JSON.parse(await readFile(olekFail, 'utf-8'));
		} catch {
			/* esimene kord või püsikausta pole */
		}
	}
	const piir = new Date(Date.now() - 7 * 864e5).toISOString().slice(0, 10);
	const saata = lehed.filter(([u, kp]) => (olek ? olek[u] !== kp : kp >= piir)).map(([u]) => u);
	if (!saata.length) return console.log('IndexNow: muutusi pole');
	for (let i = 0; i < saata.length; i += 10000) {
		const r = await fetch('https://api.indexnow.org/indexnow', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json; charset=utf-8' },
			body: JSON.stringify({ host: HOST, key: INDEXNOW_VOTI, keyLocation: `https://${HOST}/${INDEXNOW_VOTI}.txt`, urlList: saata.slice(i, i + 10000) })
		});
		console.log(`IndexNow: ${Math.min(10000, saata.length - i)} aadressi → HTTP ${r.status}`);
		if (!r.ok) return;
	}
	const uusOlek = Object.fromEntries(lehed);
	if (sbs) {
		try {
			await sbs.kirjuta('indexnow', uusOlek);
			return;
		} catch (e) {
			console.log('IndexNow:', e.message, '— salvestan faili');
		}
	}
	try {
		await writeFile(olekFail, JSON.stringify(uusOlek));
	} catch {
		/* püsikausta pole — järgmine kord saadetakse uuesti viimase 7 päeva muutused */
	}
}
if (process.env.NODE_ENV === 'production' && process.env.INDEXNOW !== '0') {
	/* oota, kuni uus versioon on päriselt väljas (võtmefail peab olema kättesaadav) */
	setTimeout(() => indexNow().catch((e) => console.log('IndexNow viga:', e.message)), 90_000).unref();
}

/* Coolify peatab vana konteineri SIGTERM-iga: lõpeta pooleli päringud ära */
function sulge() {
	server.close(() => process.exit(0));
	setTimeout(() => process.exit(0), 10_000).unref();
}
process.on('SIGTERM', sulge);
process.on('SIGINT', sulge);
