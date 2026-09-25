/* Jagamispilt (og:image) 1200×630 — joonistatakse ehituse ajal SVG-na ja
 * tehakse PNG-ks (resvg). Välist teenust ega brauserit ei ole vaja.
 *
 * Fondid on samad, mis lehel (Inter, Barlow Condensed), aga TTF-kujul,
 * sest resvg ei loe woff2-te. Nõukogude ja Balti tähed (š, ž, õ) on
 * latin-ext failis; resvg otsib puuduva tähe ise teisest failist.
 */
import { Resvg } from '@resvg/resvg-js';
import { readdirSync } from 'node:fs';
import { join } from 'node:path';

const FONDID = join(process.cwd(), 'src/lib/server/og-fondid');
let _fondid = null;
function fondid() {
	if (!_fondid) _fondid = readdirSync(FONDID).filter((f) => f.endsWith('.ttf')).map((f) => join(FONDID, f));
	return _fondid;
}

const W = 1200;
const H = 630;
const INK = '#0a0b0d';
const KOLLANE = '#ffc20e';

function esc(s) {
	return String(s ?? '')
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;');
}

/* Barlow Condensed 700 suurtähtedega: keskmine tähelaius ~0,42 em (mõõdetud) */
function murra(tekst, px, laius, maxRidu) {
	const perRida = Math.max(8, Math.floor(laius / (px * 0.42)));
	const sonad = String(tekst).toUpperCase().split(/\s+/);
	const read = [];
	let rida = '';
	for (const s of sonad) {
		if (!rida) rida = s;
		else if ((rida + ' ' + s).length <= perRida) rida += ' ' + s;
		else {
			read.push(rida);
			rida = s;
		}
	}
	if (rida) read.push(rida);
	/* üksik lühike sõna viimasel real („5“) näeb kehv välja — proovi väiksemat fonti */
	if (read.length > 1 && read[read.length - 1].length <= 3) return null;
	return read.length <= maxRidu ? read : null;
}

/**
 * @param {{ kicker?: string, pealkiri: string, alapealkiri?: string, sildid?: string[] }} o
 * @returns {Buffer} PNG
 */
export function ogPilt({ kicker = '', pealkiri, alapealkiri = '', sildid = [] }) {
	/* pealkiri: suurim font, mis mahub kahele reale */
	let px = 104;
	let read = null;
	while (px >= 56 && !(read = murra(pealkiri, px, 1020, 2))) px -= 8;
	if (!read) read = murra(pealkiri, 56, 1020, 3) || [String(pealkiri).toUpperCase().slice(0, 60)];

	const yPeal = 262;
	const reaKorgus = Math.round(px * 0.98);
	const pealSvg = read
		.map((r, i) => `<text x="80" y="${yPeal + i * reaKorgus}" font-family="Barlow Condensed" font-weight="700" font-size="${px}" fill="#ffffff">${esc(r)}</text>`)
		.join('');
	const yAla = yPeal + (read.length - 1) * reaKorgus + 64;

	let x = 80;
	const siltSvg = sildid
		.filter(Boolean)
		.slice(0, 3)
		.map((s) => {
			const w = Math.round(String(s).length * 15.2 + 40);
			const g = `<rect x="${x}" y="470" width="${w}" height="56" rx="12" fill="#1a1d24" stroke="#2b3039"/>` +
				`<text x="${x + 20}" y="507" font-family="Inter" font-weight="500" font-size="26" fill="#f3f4f6">${esc(s)}</text>`;
			x += w + 14;
			return g;
		})
		.join('');

	const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<rect width="${W}" height="${H}" fill="${INK}"/>
<g opacity="0.10" fill="none" stroke="#ffffff">
  <circle cx="1080" cy="150" r="200" stroke-width="44"/>
  <circle cx="1080" cy="150" r="78" stroke-width="30"/>
</g>
<g transform="translate(80 104) skewX(-10)">
  <text x="0" y="0" font-family="Inter" font-weight="800" font-size="40" fill="#ffffff">PIDURDUSMAA<tspan fill="${KOLLANE}">.ee</tspan></text>
</g>
${kicker ? `<text x="80" y="164" font-family="Inter" font-weight="500" font-size="26" letter-spacing="3" fill="${KOLLANE}">${esc(String(kicker).toUpperCase())}</text>` : ''}
${pealSvg}
${alapealkiri ? `<text x="80" y="${yAla}" font-family="Inter" font-weight="500" font-size="34" fill="#c9ced6">${esc(alapealkiri)}</text>` : ''}
${siltSvg}
<rect x="0" y="${H - 14}" width="${W}" height="14" fill="${KOLLANE}"/>
</svg>`;

	const r = new Resvg(svg, {
		font: { fontFiles: fondid(), loadSystemFonts: false, defaultFontFamily: 'Inter' },
		fitTo: { mode: 'width', value: W }
	});
	return r.render().asPng();
}
