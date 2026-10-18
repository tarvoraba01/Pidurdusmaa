/* Enne ehitust (npm prebuild): millistel rehvilehtedel on vene versioon
 * (/ru/rehvid/…). Samad lehed, mis saidikaardis — mõõdud (vähemalt
 * SIZE_MIN_MODELS mudelit), saidikaardi rehvid ja vs-lehed. Ülejäänud
 * (noindex) rehvilehtedel vene versiooni ei tehta, vene lehtede lingid
 * viivad neil eestikeelsele lehele. Kirjutab src/lib/i18n/ru_rehvid.js. */
import { readFileSync, writeFileSync } from 'node:fs';
import { core, models, sizeModelCount, SIZE_MIN_MODELS, rehviIndeks, vsPairs } from '../src/lib/server/andmed.js';

const s = new Set();
for (const z of core().sizes) if (sizeModelCount(z.m) >= SIZE_MIN_MODELS) s.add(z.slug);
for (const slug of new Set([...Object.keys(models()), ...core().tyres.map((t) => t.slug).filter(Boolean)]))
	if (rehviIndeks(slug).sitemap) s.add(slug);
for (const [a, b] of vsPairs()) s.add(a + '-vs-' + b);

const list = [...s].sort();

/* avaldatud võrdluslehtede nimekiri: kord tehtud leht jääb alles (vt andmed.js vsPairs) */
const vsFail = 'static/data/vs_paarid.json';
let vanad = [];
try {
	vanad = JSON.parse(readFileSync(vsFail, 'utf8'));
} catch (e) {
	/* puuduv fail = alles algus; katkine fail ei tohi nimekirja vaikselt tühjendada */
	if (e.code !== 'ENOENT') throw e;
}
const koik = new Map(vanad.map(([a, b]) => [a + '|' + b, [a, b]]));
for (const [a, b] of vsPairs()) koik.set(a + '|' + b, [a, b]);
const vs = [...koik.values()].sort((x, y) => (x[0] + '|' + x[1]).localeCompare(y[0] + '|' + y[1]));
writeFileSync(vsFail, JSON.stringify(vs));
console.log('vs_paarid:', vs.length, 'paari (' + (vs.length - vanad.length) + ' uut)');
writeFileSync(
	'src/lib/i18n/ru_rehvid.js',
	'/* GENEREERITUD: scripts/ru-rehvid.mjs (npm prebuild). Käsitsi ei muuda. */\nexport default ' + JSON.stringify(list) + ';\n'
);
console.log('ru_rehvid:', list.length, 'rehvilehte');
