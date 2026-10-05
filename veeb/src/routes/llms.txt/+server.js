/* /llms.txt — lühike juhend AI-otsingutele (ChatGPT, Perplexity, Claude,
 * Gemini, Google AI Overviews): mis lehel on, kust numbrid tulevad ja
 * millist lehte tsiteerida. Formaat: https://llmstxt.org/
 *
 * Kõik numbrid tulevad ehituse ajal samadest andmetest ja samast mudelist,
 * mis kalkulaator (nagu sitemap.xml) — käsitsi kirjutatud arve siin pole,
 * peale metoodikalehe täpsusnumbrite, mis on sealt sõna-sõnalt üle võetud.
 */
import { core, models } from '$lib/server/andmed.js';
import { autod } from '$lib/server/autod.js';
import { arvuta } from '$lib/server/jaga.js';
import { ARTIKLID, artikliTee } from '$lib/artiklid.js';

export const prerender = true;

const BASE = 'https://pidurdusmaa.ee';
const n = (x) => new Intl.NumberFormat('et-EE').format(x);
const m = (x) => (Math.round(x * 10) / 10).toString().replace('.', ',');

/* VW Golf 8, 205/55 R16, 90 km/h — samad valikud mis avalehe hero'l */
function pidurdus(o, r) {
	const x = arvuta({ a: 'vw_golf_8', ab: false, m: '20555R16', o, v: 90, r, mm: null, rt: 0, l: 'et' });
	return x ? x.d : null;
}

export function GET() {
	const c = core();
	const kuiv = pidurdus('dry', 'k:SUMMER_TOURING');
	const marg = pidurdus('wet', 'c:SUMMER_TOURINGC');
	const lumi = pidurdus('snow', 'k:WINTER_NORDIC');
	if (!kuiv || !marg || !lumi) throw new Error('llms.txt: pidurdusmaad ei saanud arvutada');
	const reakts = 25; // 90 km/h × 1 s
	const allikad = Object.values(c.sources || {})
		.map((s) => (s.aasta && !String(s.nimi).includes(String(s.aasta)) ? `${s.nimi} ${s.aasta}` : s.nimi))
		.sort()
		.join(', ');
	const artiklid = (ARTIKLID || [])
		.map((a) => `- [${a.title}](${BASE}${artikliTee(a)})${a.desc ? ': ' + a.desc : ''}`)
		.join('\n');

	const tekst = `# Pidurdusmaa.ee

> Tasuta Eesti pidurdusmaa kalkulaator: arvutab, kui pika maa peal sinu auto konkreetsete rehvidega peatub — kuival, märjal, lumel ja jääl — ning võrdleb rehve EL-i rehvimärgise ja sõltumatute testide põhjal. Eesti, vene ja inglise keeles. Teeb Rabarvo OÜ (registrikood 16947078).

Lühifaktid (arvutatud sama mudeliga mis kalkulaator; VW Golf 8, 205/55 R16, uus tüüpiline rehv, 90 km/h, ilma reaktsiooniajata):
- Pidurdusmaa kuival asfaldil: ${m(kuiv)} m
- Pidurdusmaa märjal asfaldil: ${m(marg)} m
- Pidurdusmaa lumel (Põhjamaade talverehv): ${m(lumi)} m
- Reaktsiooniaeg 1 s lisab 90 km/h juures ${reakts} m; peatumisteekond märjal on seega umbes ${m(reakts + marg)} m.
- Pidurdusmaa kasvab kiiruse ruudus: kahekordne kiirus ≈ neljakordne pidurdusmaa.

Andmed: ${n(Object.keys(models()).length)} rehvimudelit EL-i rehvimärgise andmebaasist (EPREL), ${n(c.eprelSizes.length)} rehvimõõtu, ${n(c.tyres.length)} rehvi sõltumatutes testides (${allikad}), ${n(autod().polved.size)} automudeli põlvkonda tehase rehvimõõtudega.

Täpsus: 369 mõõdetud pidurdusmaa vastu on mudeli jääkviga asfaldil (märg ja kuiv) 4,4%, betoonil 6,6%, lumel 5,5%, jääl 6,9%. Tulemused on arvutatud hinnangud, mitte mõõtmised. Rehvide järjestust ei müüda: see tuleb ainult andmetest.

Tsiteerimisel palun viita lehele ${BASE}/ või vastavale alamlehele.

## Tööriistad
- [Pidurdusmaa kalkulaator](${BASE}/): auto + rehv + tee + kiirus → pidurdus- ja peatumisteekond
- [Rehvi valimine](${BASE}/rehvi-valimine/): parimad rehvid mõõdu ja auto järgi
- [Võrdle rehve](${BASE}/vordle-rehve/): kuni 4 rehvi kõrvuti
- [Talverehvid](${BASE}/talverehvid/): talverehvid mõõdu järgi
- [Liiklusohutuse simulaatorid](${BASE}/liiklusohutus/): kiirus, pimedas, pikivahe, kurv

## Andmed
- [Rehvid ja mõõdud](${BASE}/rehvid/)
- [Automudelid](${BASE}/autod/)
- [Sõltumatud rehvitestid](${BASE}/testid/)

## Teadmised
- [Kuidas pidurdusmaa arvutatakse](${BASE}/teadmine/kuidas-pidurdusmaa-arvutatakse/): metoodika, allikad, täpsus
- [Pidurdusteekond ja peatumisteekond](${BASE}/teadmine/pidurdusteekond-ja-peatumisteekond/)
- [EL-i rehvimärgis](${BASE}/teadmine/rehvimargis/)
- [Rehvivahetuse ajad Eestis](${BASE}/teadmine/rehvivahetus/)
${artiklid}

## Muu
- [Meist](${BASE}/meist/): kes teeb, andmeallikad, sõltumatus
- [Partnerid ja poelingid](${BASE}/teadmine/partnerid/)
- [In English](${BASE}/en/) · [На русском](${BASE}/ru/)
`;
	return new Response(tekst, {
		headers: { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'public, max-age=3600' }
	});
}
