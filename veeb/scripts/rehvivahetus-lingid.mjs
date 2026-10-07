/* Rehvivahetus.ee e-poe tootelingid → src/lib/server/integratsioonid/pakkujad/rehvivahetus-lingid.json
 *
 * Sisend: JSON-massiiv e-poe nimekirja kaartidest [ct, id, tootja, mudel, meta, info],
 * kogutud kogu e-poe läbikäimisel (?s=tires&carType=1|2, kõik leheküljed).
 *   node scripts/rehvivahetus-lingid.mjs kaardid.json [kasutatud.json]
 * kasutatud.json = e-poe toote nr-id, mille märkus on „USED: …“ (lehe peidetud tooteandmetest).
 *
 * Võti on sama, mis serveris (epoeVoti): tootja | mudel | mõõt | koormus+kiirus.
 * Varuvõti ilma indeksita („|*“) ainult siis, kui see mudel on selles mõõdus üks.
 * Kasutatud rehvid (info „USED: …“) jäetakse välja. Nimekiri on hinna järgi kasvavas
 * järjekorras, nii et kahe sama uue rehvi puhul jääb odavam.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { normMoot, normMark, norm } from '../src/lib/server/integratsioonid/sobitus.js';

const lisiTuum = (s) => {
	const m = /(\d{2,3}(?:\/\d{2,3})?)\s*([A-Z])\b/.exec(String(s || '').toUpperCase());
	return m ? m[1] + m[2] : '';
};
const voti = (mark, mudel, moot, lisi) => `${normMark(mark)}|${norm(mudel).replace(/ /g, '')}|${moot}|${lisiTuum(lisi)}`;
const ilmaIndeksita = (v) => v.slice(0, v.lastIndexOf('|')) + '|*';

const read = JSON.parse(readFileSync(process.argv[2], 'utf-8'));
const KAS = new Set(process.argv[3] ? JSON.parse(readFileSync(process.argv[3], 'utf-8')) : []);
const v = {};
let kasutatud = 0, vigane = 0;
for (const [, id, mark, mudel, meta, info] of read) {
	if (KAS.has(id) || /USED\s*:/i.test(info || '')) { kasutatud++; continue; }
	const moot = normMoot(meta);
	if (!moot) { vigane++; continue; }
	const k = voti(mark, mudel, moot, meta.slice(meta.indexOf(' ')));
	if (!(k in v)) v[k] = id;
}
/* varuvõti ainult siis, kui mudel on mõõdus üks (eri indeksid = eri tooted) */
const mudeleid = new Map();
for (const k of Object.keys(v)) { const k2 = ilmaIndeksita(k); mudeleid.set(k2, [...(mudeleid.get(k2) || []), k]); }
for (const [k2, kk] of mudeleid) if (kk.length === 1) v[k2] = v[kk[0]];

const valja = { aeg: new Date().toISOString().slice(0, 10), v: Object.fromEntries(Object.entries(v).sort()) };
writeFileSync(new URL('../src/lib/server/integratsioonid/pakkujad/rehvivahetus-lingid.json', import.meta.url), JSON.stringify(valja) + '\n');
console.log(`kaarte ${read.length}, kasutatud välja ${kasutatud}, mõõduta ${vigane}, võtmeid ${Object.keys(v).length}`);
