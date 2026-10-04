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
function sisu(html) {
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
	let rasi = null;
	try {
		rasi = createHash('sha1').update(sisu(readFileSync(fail, 'utf-8'))).digest('hex').slice(0, 16);
	} catch {
		puudu++;
	}
	const v = vana[tee];
	let kp;
	/* LASTMOD_RASI_UUESTI=1: räsimise viis muutus, kuupäevad jäävad */
	if (v && rasi && (v[0] === rasi || process.env.LASTMOD_RASI_UUESTI)) kp = v[1];
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
