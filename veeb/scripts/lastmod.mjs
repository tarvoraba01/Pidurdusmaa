/* Saidikaardi lastmod = lehe PÄRIS viimane muutus (mitte ehituse kuupäev).
 *
 * Varem oli igal lehel lastmod = ehituse päev, st iga deploy ütles Google'ile,
 * et kõik ~6000 lehte muutusid. Google õpib sellist lastmod-i ignoreerima.
 *
 * Nüüd: iga saidikaardi lehe sisust arvutatakse räsi (ilma skriptide,
 * failiräside ja versioonita — need muutuvad iga ehitusega, sisu mitte).
 * scripts/lastmod.json hoiab iga aadressi kohta [räsi, kuupäev]. Kui räsi on
 * sama, jääb vana kuupäev; kui muutus (või leht on uus), saab tänase.
 * lastmod.json on repos — pärast ehitust commit'i see koos muu koodiga.
 *
 * Käivitub postbuild'is (package.json). */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';

const SITEMAP = 'build/prerendered/sitemap.xml';
const ANDMED = 'scripts/lastmod.json';
const TANA = new Date().toISOString().slice(0, 10);

/* ainult lehe oma sisu: <main> + pealkiri + kirjeldus. Päis, jalus ja
   alariba on kõigil lehtedel ühised — nende muutus ei ole lehe muutus. */
/* Plokid data-lm="0" (poodide pakkumised, „Kus osta“, ostutee) ei ole lehe sisu muutus:
   nende malli muutmine ei tohi kogu saidi lastmod-i tänaseks teha (audit 17.10). */
function ilmaLm0(html) {
	let out = html, i;
	while ((i = out.search(/<([a-z]+)\b[^>]*\bdata-lm="0"/i)) >= 0) {
		const tag = /^<([a-z]+)/i.exec(out.slice(i))[1].toLowerCase();
		const re = new RegExp('<(/?)' + tag + '\\b[^>]*>', 'gi');
		re.lastIndex = i;
		let sugavus = 0, lopp = -1, m;
		while ((m = re.exec(out))) {
			if (m[1]) sugavus--;
			else if (!/\/>$/.test(m[0])) sugavus++;
			if (sugavus === 0) { lopp = re.lastIndex; break; }
		}
		if (lopp < 0) break;
		out = out.slice(0, i) + out.slice(lopp);
	}
	return out;
}
/* viis: 'uus' = ilma data-lm="0" plokkide ja HTML-kommentaarideta (praegune);
   'eelmine' = ilma data-lm="0" plokkideta, kommentaarid sees (v86–v87 räsid lastmod.json-is);
   'vana' = data-lm plokid sees (enne v86). Üleminekul klapib vana kuupäev ükskõik millise viisiga. */
function sisu(html, viis = 'uus') {
	if (viis !== 'vana') html = ilmaLm0(html);
	/* Svelte'i hüdratsioonimärgid (<!--[-->, <!---->) ei ole sisu: nende arv muutub ka siis,
	   kui lehe tekst jääb samaks (nt tabel {@html}-iga), audit 18.10 */
	if (viis === 'uus') html = html.replace(/<!--[\s\S]*?-->/g, '');
	const m = /<main\b[\s\S]*<\/main>/i.exec(html);
	const pea = (/<title>[\s\S]*?<\/title>/i.exec(html) || [''])[0] + ((/<meta name="description"[^>]*>/i.exec(html) || [''])[0]);
	return (pea + (m ? m[0] : html))
		.replace(/<script\b[\s\S]*?<\/script>/gi, '')
		.replace(/<link\b[^>]*>/gi, '')
		.replace(/\/_app\/[^"'\s)]+/g, '')
		.replace(/<style\b[\s\S]*?<\/style>/gi, '')
		.replace(/\s?svelte-[a-z0-9]{4,}/g, '')
		.replace(/\s+/g, ' ');
}

const xml = readFileSync(SITEMAP, 'utf-8');
const vana = existsSync(ANDMED) ? JSON.parse(readFileSync(ANDMED, 'utf-8')) : {};
const uus = {};
let muutus = 0, uusi = 0, puudu = 0;

const valja = xml.replace(/<url><loc>https:\/\/[^/<]+(\/[^<]*)<\/loc><lastmod>[^<]*<\/lastmod>/g, (koik, tee) => {
	const fail = 'build/prerendered' + tee + (tee.endsWith('/') ? 'index.html' : '');
	let rasi = null, rasiEelm = null, rasiVana = null;
	const r = (x) => createHash('sha1').update(x).digest('hex').slice(0, 16);
	try {
		const html = readFileSync(fail, 'utf-8');
		rasi = r(sisu(html));
		/* üleminek: varasemad räsiviisid — kui mõni klapib, leht ei muutunud */
		rasiEelm = r(sisu(html, 'eelmine'));
		rasiVana = r(sisu(html.replace(/ data-lm="0"/g, ''), 'vana'));
	} catch {
		puudu++;
	}
	const v = vana[tee];
	let kp;
	/* LASTMOD_RASI_UUESTI=1: räsimise viis muutus, kuupäevad jäävad */
	if (v && rasi && (v[0] === rasi || v[0] === rasiEelm || v[0] === rasiVana || process.env.LASTMOD_RASI_UUESTI)) kp = v[1];
	else if (v && !rasi) kp = v[1];
	else {
		kp = TANA;
		if (v) muutus++;
		else uusi++;
	}
	uus[tee] = [rasi || (v && v[0]) || '', kp];
	return koik.replace(/<lastmod>[^<]*<\/lastmod>/, `<lastmod>${kp}</lastmod>`);
});

writeFileSync(SITEMAP, valja);
const sorditud = Object.fromEntries(Object.keys(uus).sort().map((k) => [k, uus[k]]));
writeFileSync(ANDMED, JSON.stringify(sorditud, null, 0).replace(/\],"/g, '],\n"') + '\n');
console.log(`Saidikaart: ${Object.keys(uus).length} lehte, muutunud ${muutus}, uued ${uusi}` + (puudu ? `, faili ei leitud ${puudu}` : '') + '.');
