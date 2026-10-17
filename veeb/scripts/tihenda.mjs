/* Eeltihendus (.br; brauserid, mis br-i ei oska, saavad tihendamata faili) pärast ehitust — server annab need failid otse kettalt.
 *
 * Miks (audit 17.10): server tihendas iga vastuse käigu pealt (compression()),
 * see võttis ~80% protsessorist (346 vs 1665 päringut/s) ja mälu kasvas
 * koormuse all 1,5 GB-ni. adapter-node'i enda precompress avab kõik ~35 000
 * faili korraga ja kukub „EMFILE: too many open files“ veaga, seepärast teeme
 * selle siin piiratud paralleelsusega.
 *
 * Lõpuks lülitab build/handler.js-is sirv'i .br/.gz failide kasutamise sisse.
 * compression() server.js-is jääb alles ainult dünaamiliste vastuste jaoks
 * (API) — eeltihendatud vastusel on Content-Encoding juba olemas ja see jätab
 * selle vahele. */
import { readdirSync, statSync, readFileSync, writeFileSync } from 'node:fs';
import { join, extname } from 'node:path';
import { brotliCompressSync, constants } from 'node:zlib';

const KAUSTAD = ['build/client', 'build/prerendered'];
const LAIENDID = new Set(['.html', '.js', '.mjs', '.css', '.json', '.svg', '.xml', '.txt', '.webmanifest']);
const MIN = 1024;

let n = 0, enne = 0, parast = 0;
function kaivi(dir) {
	for (const nimi of readdirSync(dir)) {
		const p = join(dir, nimi);
		const st = statSync(p);
		if (st.isDirectory()) {
			kaivi(p);
			continue;
		}
		if (!LAIENDID.has(extname(nimi)) || st.size < MIN) continue;
		const sisu = readFileSync(p);
		const br = brotliCompressSync(sisu, {
			params: { [constants.BROTLI_PARAM_QUALITY]: 8, [constants.BROTLI_PARAM_SIZE_HINT]: sisu.length }
		});
		writeFileSync(p + '.br', br);
		n++;
		enne += sisu.length;
		parast += br.length;
	}
}
const t0 = Date.now();
for (const k of KAUSTAD) kaivi(k);

/* sirv: kasuta .br/.gz faile (adapter-node paneb siia oma precompress-seade;
   kood on build/handler.js-is või build/server/chunks/handler-*.js-is) */
const kandidaadid = ['build/handler.js', ...readdirSync('build/server/chunks').filter((f) => /^handler-.*\.js$/.test(f)).map((f) => 'build/server/chunks/' + f)];
let parandatud = 0;
for (const H of kandidaadid) {
	const h = readFileSync(H, 'utf-8');
	const uus = h.replace(/gzip:\s*(false|PRECOMPRESS),(\s*)brotli:\s*(false|PRECOMPRESS)/, 'gzip: true,$2brotli: true');
	if (uus !== h) {
		writeFileSync(H, uus);
		parandatud++;
	} else if (/gzip:\s*true,\s*brotli:\s*true/.test(h)) parandatud++;
}
if (!parandatud) {
	console.error('tihenda: sirv-i gzip/brotli seadet ei leitud (build/handler.js, build/server/chunks/handler-*.js) — adapter-node muutus?');
	process.exit(1);
}
console.log(`Eeltihendus: ${n} faili, ${(enne / 1e6).toFixed(1)} MB → br ${(parast / 1e6).toFixed(1)} MB, ${Math.round((Date.now() - t0) / 1000)} s.`);
