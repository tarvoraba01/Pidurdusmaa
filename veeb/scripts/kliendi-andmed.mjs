/* Brauserisse minev core.json ilma väljadeta, mida brauser ei kasuta.
 *
 * static/data/core.json on täisfail (ehitus, testid, serveri lehed).
 * Brauser laeb build/client/data/core.json-i — sealt eemaldatakse:
 *   vehicles[].oemSrc, vehicles[].note, vehicles[].oemConf  (allikad ja
 *   märkmed: kasutab ainult serveri autoleht), vib (testilehe tabel).
 * Täisfail jääb serverile alles: build/andmed/core.json (ei ole veebis
 * nähtav; andmed.js loeb seda töötavas serveris).
 *
 * Kui app.js hakkab mõnda neist väljadest kasutama, eemalda see siit.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';

const KLIENT = 'build/client/data/core.json';
if (!existsSync(KLIENT)) { console.error('kliendi-andmed: ' + KLIENT + ' puudub'); process.exit(1); }
const algne = readFileSync(KLIENT, 'utf8');
mkdirSync('build/andmed', { recursive: true });
writeFileSync('build/andmed/core.json', algne);

const c = JSON.parse(algne);
delete c.vib;
for (const v of c.vehicles) { delete v.oemSrc; delete v.note; delete v.oemConf; }
const uus = JSON.stringify(c);
writeFileSync(KLIENT, uus);
console.log(`kliendi-andmed: core.json ${(algne.length / 1024) | 0} KB -> ${(uus.length / 1024) | 0} KB (täisfail: build/andmed/core.json)`);
