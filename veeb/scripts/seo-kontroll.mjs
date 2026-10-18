/* SEO kontroll pärast ehitust (npm run build → postbuild).
 *
 * Käib läbi KÕIK ehitatud HTML-lehed ja kontrollib, et otsingumootor ja
 * sotsiaalvõrgud saavad kõik vajaliku juba serveri HTML-ist, ilma
 * JavaScriptita (Facebook, Messenger, Slack ja LinkedIn JS-i ei käivita):
 *   - üks <title>, description, canonical, og:title/description/url/image
 *   - canonical, og:url ja og:image on TÄIS-URL-id (https://pidurdusmaa.ee/…)
 *   - og:image fail on ehituses päriselt olemas
 *   - JSON-LD on korrektne JSON
 *   - lehel on täpselt üks <h1>
 * Kui midagi on valesti, katkeb ehitus — vigane versioon ei jõua lehele.
 */
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const BASE = 'https://pidurdusmaa.ee';
const ROOT = 'build/prerendered';
const STATIC = ['build/prerendered', 'build/client'];

function* html(dir) {
	for (const n of readdirSync(dir)) {
		const p = join(dir, n);
		if (statSync(p).isDirectory()) yield* html(p);
		else if (n.endsWith('.html')) yield p;
	}
}
const count = (s, re) => (s.match(re) || []).length;
const val = (s, re) => (s.match(re) || [])[1];

const vead = [];
let n = 0;
/* vene lehelt eestikeelsele lehele, millel on vene versioon olemas (audit 18.10: 16 953 sellist linki).
   Ainult hoiatus (ei katkesta ehitust): loend + näited, et uus kõvakodeeritud link silma jääks. */
const ruOlemas = (p) => existsSync(join(ROOT, 'ru' + p.replace(/\/$/, '') + '.html')) || existsSync(join(ROOT, 'ru' + p, 'index.html'));
const ruLekked = new Map();
for (const f of html(ROOT)) {
	n++;
	const h = readFileSync(f, 'utf-8');
	const head = h.split('</head>')[0];
	const body = h.slice(head.length);
	const v = (m) => vead.push(f.replace(ROOT, '') + ': ' + m);

	if (count(head, /<title>/g) !== 1) v('<title> puudub või on mitu');
	for (const [nimi, re] of [
		['description', /<meta name="description" content="[^"]+"/g],
		['canonical', /<link rel="canonical" href="[^"]+"/g],
		['og:title', /<meta property="og:title" content="[^"]+"/g],
		['og:description', /<meta property="og:description" content="[^"]+"/g],
		['og:url', /<meta property="og:url" content="[^"]+"/g],
		['og:image', /<meta property="og:image" content="[^"]+"/g],
		['twitter:card', /<meta name="twitter:card" content="[^"]+"/g]
	]) {
		const c = count(head, re);
		if (c !== 1) v(`${nimi}: ${c} tk (peab olema 1)`);
	}
	for (const [nimi, re] of [
		['canonical', /<link rel="canonical" href="([^"]+)"/],
		['og:url', /<meta property="og:url" content="([^"]+)"/],
		['og:image', /<meta property="og:image" content="([^"]+)"/],
		['twitter:image', /<meta name="twitter:image" content="([^"]+)"/]
	]) {
		const u = val(head, re);
		if (u && !u.startsWith(BASE + '/')) v(`${nimi} ei ole täis-URL: ${u}`);
	}
	const img = val(head, /<meta property="og:image" content="([^"]+)"/);
	if (img && img.startsWith(BASE + '/')) {
		const rel = img.slice(BASE.length);
		if (!STATIC.some((d) => existsSync(join(d, rel)))) v('og:image faili ei ole: ' + rel);
	}
	for (const m of head.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
		try {
			JSON.parse(m[1]);
		} catch {
			v('JSON-LD ei ole korrektne JSON');
		}
	}
	if (/<meta (property|name)="(og:|twitter:|description)/.test(body)) v('meta-silt on <body> sees');
	if (f.startsWith(join(ROOT, 'ru') + '/') || f === join(ROOT, 'ru.html')) {
		/* ainult nähtav osa: SvelteKit'i andmeskriptides olevad aadressid ei ole lingid */
		/* keelevahetuse lingid (hreflang="et") peavadki eestikeelsele lehele viima */
		const nahtav = body.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<a\b[^>]*\bhreflang="[^"]*"[^>]*>/g, '');
		for (const m of nahtav.matchAll(/href="(\/(?!ru\/|en\/|_app\/|data\/|api\/|og\/|fonts\/)[^"?#]*)/g)) {
			if (ruOlemas(m[1])) ruLekked.set(m[1], (ruLekked.get(m[1]) || 0) + 1);
		}
	}
	const h1 = count(body, /<h1[\s>]/g);
	if (h1 !== 1) v(`<h1>: ${h1} tk (peab olema 1)`);
}

if (ruLekked.size) {
	const kokku = [...ruLekked.values()].reduce((a, b) => a + b, 0);
	console.warn(`SEO hoiatus: vene lehtedel ${kokku} linki eestikeelsele lehele, millel on vene versioon (sagedasemad: ` +
		[...ruLekked.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([p, c]) => p + ' ×' + c).join(', ') + ')');
}
if (vead.length) {
	console.error(`\nSEO kontroll: ${vead.length} viga ${n} lehel\n` + vead.slice(0, 30).join('\n'));
	process.exit(1);
}
console.log(`SEO kontroll: ${n} lehte korras (title, description, canonical, OG, Twitter, JSON-LD, H1).`);
