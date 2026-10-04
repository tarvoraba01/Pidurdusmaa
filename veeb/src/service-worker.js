/* Pidurdusmaa.ee — service worker (PWA).
 *
 * Eesmärk: leht avaneb avaekraanilt kiiresti ja põhiasjad (kalkulaator,
 * simulaatorid) töötavad ka nõrga levi või ühenduseta. Mudel arvutab niikuinii
 * brauseris, seega piisab, kui failid on telefonis olemas.
 *
 * Reeglid:
 *   - lehed (HTML): ALATI enne võrgust (värske sisu ja hinnad); kui võrku pole,
 *     siis viimati nähtud koopia telefonist;
 *   - _app/immutable (JS/CSS, nimes räsi): ette laetud, ei muutu kunagi;
 *   - /data/*.json?v=<versioon>: esimesel kasutamisel telefoni, sama versiooni
 *     ei laeta enam uuesti;
 *   - /api/pilt/: rehvipildid telefoni (piiratud arv);
 *   - /api/hinnad ja muu /api/: MITTE KUNAGI vahemällu — hinnad peavad olema värsked;
 *   - teised domeenid (statistika jne): ei puututa.
 * Uue versiooni (deploy) korral kustutatakse vanad koopiad ära. */
import { build, files, version } from '$service-worker';

const APP = 'app-' + version;
const LEHED = 'lehed-' + version;
const ANDMED = 'andmed';
const PILDID = 'pildid';
const STAATILINE = 'staatiline';
const KOIK = [APP, LEHED, ANDMED, PILDID, STAATILINE];

/* ette: rakenduse failid, fondid, ikoonid + avaleht ja simulaatorid */
const ETTE = build
	.concat(files.filter((f) => /^\/(fonts\/.*\.woff2|favicon\.(svg|ico)|icon-[\w-]+\.png|apple-touch-icon\.png|manifest\.webmanifest|img\/hero-car\.jpg)$/.test(f)));
const ETTE_LEHED = ['/', '/liiklusohutus/', '/liiklusohutus/pimedas/', '/liiklusohutus/pikivahe/', '/liiklusohutus/kurv/'];

self.addEventListener('install', (e) => {
	e.waitUntil(
		(async () => {
			const c = await caches.open(APP);
			await c.addAll(ETTE);
			/* lehed eraldi: üks ebaõnnestunud leht ei tohi paigaldust katki teha */
			const l = await caches.open(LEHED);
			await Promise.all(ETTE_LEHED.map((u) => l.add(u).catch(() => {})));
			await self.skipWaiting();
		})()
	);
});

self.addEventListener('activate', (e) => {
	e.waitUntil(
		(async () => {
			for (const k of await caches.keys()) if (!KOIK.includes(k)) await caches.delete(k);
			await self.clients.claim();
		})()
	);
});

/* vahemälu piir: vanimad kirjed välja */
async function piira(nimi, max) {
	const c = await caches.open(nimi);
	const v = await c.keys();
	for (let i = 0; i < v.length - max; i++) await c.delete(v[i]);
}
function sobib(r) {
	return r && r.ok && r.type === 'basic';
}
async function pane(nimi, req, res, max) {
	if (!sobib(res)) return;
	const c = await caches.open(nimi);
	await c.put(req, res);
	if (max) piira(nimi, max);
}

const VALJAS = `<!doctype html><html lang="et"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ühendus puudub · Pidurdusmaa.ee</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0a0b0d;color:#fff;font:16px/1.5 system-ui,sans-serif;padding:24px;box-sizing:border-box;text-align:center}b{display:block;font-size:22px;margin-bottom:8px}a{display:inline-block;margin-top:20px;background:#ffc20e;color:#0a0b0d;font-weight:700;text-decoration:none;padding:12px 22px;border-radius:8px}</style></head><body><div><b>Võrguühendus puudub</b>Seda lehte pole veel telefoni salvestatud. Varem avatud lehed, kalkulaator ja simulaatorid töötavad ka ilma võrguta.<br><a href="/">Ava kalkulaator</a></div></body></html>`;

/* leht: enne võrk (kuni 6 s, kui telefonis on koopia), siis koopia */
async function leht(req) {
	const c = await caches.open(LEHED);
	const koopia = await c.match(req, { ignoreSearch: true });
	const vork = fetch(req).then((res) => {
		if (sobib(res)) c.put(req, res.clone()).then(() => piira(LEHED, 60));
		return res;
	});
	try {
		if (!koopia) return await vork;
		return await Promise.race([vork, new Promise((_, rej) => setTimeout(() => rej(new Error('aeglane')), 6000))]);
	} catch {
		if (koopia) return koopia;
		if (req.mode !== 'navigate') return Response.error();
		return new Response(VALJAS, { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } });
	}
}

/* esmalt telefonist, puudumisel võrgust ja telefoni */
async function enneKoopia(nimi, req, max) {
	const k = await caches.match(req);
	if (k) return k;
	const res = await fetch(req);
	pane(nimi, req, res.clone(), max);
	return res;
}

/* telefonist kohe, taustal uuendus */
async function koopiaJaUuendus(nimi, req, max) {
	const k = await caches.match(req);
	const v = fetch(req).then((res) => { pane(nimi, req, res.clone(), max); return res; }).catch(() => k);
	return k || v;
}

self.addEventListener('fetch', (e) => {
	const req = e.request;
	if (req.method !== 'GET') return;
	const url = new URL(req.url);
	if (url.origin !== self.location.origin) return;
	const p = url.pathname;

	if (p.startsWith('/api/')) {
		if (p.startsWith('/api/pilt/')) e.respondWith(enneKoopia(PILDID, req, 200));
		return; /* hinnad jm: alati võrgust, brauser ise */
	}
	if (req.mode === 'navigate' || p.endsWith('/__data.json')) {
		e.respondWith(leht(req));
		return;
	}
	if (p.startsWith('/_app/immutable/')) {
		e.respondWith(enneKoopia(APP, req));
		return;
	}
	if (p.startsWith('/data/')) {
		/* versiooniga (?v=) fail ei muutu; ilma versioonita värskendame taustal */
		e.respondWith(url.searchParams.has('v') ? enneKoopia(ANDMED, req, 80) : koopiaJaUuendus(ANDMED, req, 80));
		return;
	}
	if (ETTE.includes(p)) {
		e.respondWith(enneKoopia(APP, req));
		return;
	}
	if (/\.(png|jpe?g|webp|svg|woff2)$/.test(p)) e.respondWith(koopiaJaUuendus(STAATILINE, req, 120));
});
