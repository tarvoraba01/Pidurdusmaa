/* Jagamispilt (og:image) 1200×630 — joonistatakse ehituse ajal SVG-na ja
 * tehakse PNG-ks (resvg). Välist teenust ega brauserit ei ole vaja.
 *
 * Fondid on samad, mis lehel (Inter, Barlow Condensed), aga TTF-kujul,
 * sest resvg ei loe woff2-te. Nõukogude ja Balti tähed (š, ž, õ) on
 * latin-ext failis; resvg otsib puuduva tähe ise teisest failist.
 * inter-latin-500/800.ttf on liidetud (latin + latin-ext + kirillitsa), et vene
 * teksti numbrid ja tähed tuleksid samast fondist. Pealkirja kirillitsa: Roboto Condensed.
 */
import { Resvg } from '@resvg/resvg-js';
import v8 from 'node:v8';
import vm from 'node:vm';

/* Iga Resvg hoiab ~3 MB fonte Rusti poolel mälus, kuni JS-i prügikoristus
   objekti vabastab — JS-i hunnik on väike, nii et koristus ei käivitu ise ja
   ~2000 pildi ehitusel sai mälu otsa. Käivitame koristuse ise iga 50 pildi järel
   (koos routes/og GET-i setImmediate'iga, mis laseb vabastamisel toimuda). */
let _gc = null;
try {
	v8.setFlagsFromString('--expose-gc');
	_gc = vm.runInNewContext('gc');
} catch {
	/* pole saadaval — jääb tavaline koristus */
}
let _loendur = 0;
function koristaVahel() {
	if (_gc && ++_loendur % 50 === 0) _gc();
}
import { readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

/* ehitusel src-kaustast; töötavas serveris (Docker: ainult build/) postbuild'i
   koopiast build/og-fondid (vt package.json) — jagamispildid tehakse seal käigu pealt */
const FONDID = [join(process.cwd(), 'src/lib/server/og-fondid'), join(process.cwd(), 'build/og-fondid')].find((d) => existsSync(d)) || join(process.cwd(), 'src/lib/server/og-fondid');
let _fondid = null;
function fondid() {
	if (!_fondid) _fondid = readdirSync(FONDID).filter((f) => f.endsWith('.ttf')).map((f) => join(FONDID, f));
	return _fondid;
}
/** Valmis SVG → PNG samade fontidega (jagamispilt /jaga/pilt.png). */
export function svgPng(svg, laius = 1200) {
	koristaVahel();
	return new Resvg(svg, { font: { fontFiles: fondid(), loadSystemFonts: false, defaultFontFamily: 'Inter' }, fitTo: { mode: 'width', value: laius } }).render().asPng();
}
export { esc as svgEsc };
/** Teksti tegelik laius pikslites (resvg mõõdab samade fontidega); vea korral hinnang. */
export function mootLaius(tekst, pere, paksus, px) {
	try {
		const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="${px * 2}"><text x="0" y="${px * 1.5}" font-family="${pere}" font-weight="${paksus}" font-size="${px}" fill="#000">${esc(tekst)}</text></svg>`;
		const bb = new Resvg(svg, { font: { fontFiles: fondid(), loadSystemFonts: false, defaultFontFamily: 'Inter' } }).getBBox();
		if (bb && bb.width > 0) return bb.x + bb.width;
	} catch {
		/* hinnang allpool */
	}
	return String(tekst).length * px * 0.42;
}

const W = 1200;

/* Sildi teksti tegelik laius (Inter 500, 26 px): resvg mõõdab, varuks hinnang */
const _laius = new Map();
function tekstiLaius(s) {
	if (_laius.has(s)) return _laius.get(s);
	let w = String(s).length * 15.2;
	try {
		const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="60"><text x="0" y="40" font-family="Inter" font-weight="500" font-size="26" fill="#000">${esc(s)}</text></svg>`;
		const bb = new Resvg(svg, { font: { fontFiles: fondid(), loadSystemFonts: false, defaultFontFamily: 'Inter' } }).getBBox();
		if (bb && bb.width > 0) w = bb.width;
	} catch {
		/* hinnang jääb */
	}
	_laius.set(s, w);
	return w;
}
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

/* Barlow Condensed 700 suurtähtedega: keskmine tähelaius ~0,42 em (mõõdetud);
   vene tekstil Roboto Condensed (Barlow'l kirillitsat pole), laiem ~0,55 em */
const KYR = /[\u0400-\u04FF]/;
function murra(tekst, px, laius, maxRidu) {
	const perRida = Math.max(8, Math.floor(laius / (px * (KYR.test(tekst) ? 0.55 : 0.42))));
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
/* Teemapildid paremale (lehe teema järgi), 1200×630 lõuendil */
const PILDID = {
	/* kurv: tee kaar, auto libiseb, punktiir näitab libisemist */
	kurv: `<g transform="translate(0 0)">
  <path d="M760 640 L760 470 A300 300 0 0 1 1060 170 L1220 170" fill="none" stroke="#2b3039" stroke-width="150"/>
  <path d="M760 640 L760 470 A300 300 0 0 1 1060 170 L1220 170" fill="none" stroke="#3a404b" stroke-width="140"/>
  <path d="M760 640 L760 470 A300 300 0 0 1 1060 170 L1220 170" fill="none" stroke="#f3f4f6" stroke-width="4" stroke-dasharray="26 30" opacity=".8"/>
  <path d="M735 600 L735 470 C735 400 760 350 805 318 C850 300 880 310 905 336" fill="none" stroke="#e5484d" stroke-width="8" stroke-linecap="round" stroke-dasharray="2 16"/>
  <path d="M735 600 L735 470 C735 400 760 350 805 318" fill="none" stroke="${KOLLANE}" stroke-width="8" stroke-linecap="round"/>
  <g transform="translate(930 360) rotate(120)">
    <rect x="-62" y="-27" width="124" height="54" rx="15" fill="#000" opacity=".35" transform="translate(6 8)"/>
    <rect x="-62" y="-27" width="124" height="54" rx="15" fill="${KOLLANE}" stroke="#171200" stroke-width="3"/>
    <path d="M16 -21 Q36 0 16 21 L2 18 Q12 0 2 -18Z" fill="#26303b"/>
    <path d="M-37 -19 Q-49 0 -37 19 L-27 16 Q-34 0 -27 -16Z" fill="#26303b"/>
  </g>
  <path d="M985 300 l18 -26 M1000 330 l30 -10 M960 290 l-2 -30" stroke="${KOLLANE}" stroke-width="6" stroke-linecap="round"/>
</g>`,
	/* pimedas: esituled, valgusvihk, jalakäija helkuriga */
	pimedas: `<defs><linearGradient id="vihk" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff3c4" stop-opacity=".55"/><stop offset="1" stop-color="#fff3c4" stop-opacity="0"/></linearGradient></defs>
<path d="M870 560 L740 150 L1180 150 L1030 560Z" fill="url(#vihk)"/>
<g transform="translate(950 560)">
  <rect x="-110" y="-10" width="220" height="90" rx="26" fill="#1f232b" stroke="#2b3039" stroke-width="3"/>
  <ellipse cx="-70" cy="10" rx="26" ry="14" fill="#fff8d6"/>
  <ellipse cx="70" cy="10" rx="26" ry="14" fill="#fff8d6"/>
</g>
<g transform="translate(960 250)" fill="#3a404b">
  <circle cx="0" cy="-58" r="20"/>
  <path d="M-22 -32 Q0 -40 22 -32 L30 40 L14 42 L10 100 L-10 100 L-14 42 L-30 40Z"/>
  <rect x="18" y="8" width="16" height="16" rx="3" fill="${KOLLANE}"/>
  <path d="M26 16 l26 -10 M26 16 l28 6 M26 16 l20 22" stroke="${KOLLANE}" stroke-width="4" stroke-linecap="round"/>
</g>`,
	/* pikivahe: kaks autot üksteise järel, vahe sekundites */
	pikivahe: `<rect x="840" y="-10" width="220" height="660" fill="#2b3039"/>
<rect x="848" y="-10" width="204" height="660" fill="#3a404b"/>
<path d="M950 -10 V640" stroke="#f3f4f6" stroke-width="4" stroke-dasharray="26 30" opacity=".6"/>
<g transform="translate(900 210)">
  <rect x="-27" y="-60" width="54" height="120" rx="15" fill="#c9ced6" stroke="#0a0b0d" stroke-width="3"/>
  <path d="M-21 26 Q0 40 21 26 L18 12 Q0 20 -18 12Z" fill="#26303b"/>
  <rect x="-23" y="52" width="14" height="7" rx="2" fill="#ff2d2d"/><rect x="9" y="52" width="14" height="7" rx="2" fill="#ff2d2d"/>
</g>
<g transform="translate(900 480)">
  <rect x="-27" y="-60" width="54" height="120" rx="15" fill="${KOLLANE}" stroke="#171200" stroke-width="3"/>
  <path d="M-21 -16 Q0 -36 21 -16 L18 -2 Q0 -12 -18 -2Z" fill="#26303b"/>
</g>
<path d="M1000 285 V405 M985 285 H1015 M985 405 H1015" stroke="${KOLLANE}" stroke-width="5"/>
<text x="1030" y="360" font-family="Barlow Condensed" font-weight="700" font-size="64" fill="${KOLLANE}">2 s?</text>`,
	/* peatumisteekond: auto, reageerimise (kollane) ja pidurdamise (punane) teekond, takistus */
	peatumine: `<rect x="840" y="-10" width="220" height="660" fill="#2b3039"/>
<rect x="848" y="-10" width="204" height="660" fill="#3a404b"/>
<path d="M950 -10 V640" stroke="#f3f4f6" stroke-width="4" stroke-dasharray="26 30" opacity=".6"/>
<path d="M900 470 V330" stroke="${KOLLANE}" stroke-width="14" stroke-linecap="round"/>
<path d="M900 330 V150" stroke="#e5484d" stroke-width="14" stroke-linecap="round"/>
<path d="M862 128 H938" stroke="#ffffff" stroke-width="8" stroke-linecap="round"/>
<g transform="translate(900 82)">
  <path d="M0 -34 L32 22 H-32Z" fill="${KOLLANE}" stroke="#171200" stroke-width="4" stroke-linejoin="round"/>
  <path d="M0 -14 V4" stroke="#171200" stroke-width="7" stroke-linecap="round"/><circle cx="0" cy="13" r="4" fill="#171200"/>
</g>
<g transform="translate(900 530)">
  <rect x="-27" y="-60" width="54" height="120" rx="15" fill="${KOLLANE}" stroke="#171200" stroke-width="3"/>
  <path d="M-21 -16 Q0 -36 21 -16 L18 -2 Q0 -12 -18 -2Z" fill="#26303b"/>
</g>
<path d="M1000 470 V150 M985 470 H1015 M985 150 H1015" stroke="#c9ced6" stroke-width="4"/>
<text x="1024" y="322" font-family="Barlow Condensed" font-weight="700" font-size="58" fill="#ffffff">? m</text>`,
	/* rehvivahetus: kalender lumehelbega */
	kalender: `<g transform="translate(830 170)">
  <rect x="0" y="20" width="300" height="290" rx="26" fill="#1a1d24" stroke="#2b3039" stroke-width="4"/>
  <rect x="0" y="20" width="300" height="78" rx="26" fill="${KOLLANE}"/>
  <rect x="0" y="70" width="300" height="28" fill="${KOLLANE}"/>
  <rect x="62" y="0" width="18" height="52" rx="9" fill="#c9ced6"/><rect x="220" y="0" width="18" height="52" rx="9" fill="#c9ced6"/>
  <text x="150" y="215" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="110" fill="#ffffff">1.12</text>
  <g transform="translate(150 266)" stroke="#8fc7ff" stroke-width="6" stroke-linecap="round">
    <path d="M0 -26 V26 M-22.5 -13 L22.5 13 M-22.5 13 L22.5 -13"/>
  </g>
</g>`,
	/* rehvi vanus: rehvi külg, DOT-kood ja tootmisnädal ovaalis */
	dot: `<circle cx="1020" cy="640" r="430" fill="#1a1d24" stroke="#2b3039" stroke-width="6"/>
<circle cx="1020" cy="660" r="200" fill="#0a0b0d" stroke="#2b3039" stroke-width="6"/>
<g transform="rotate(-14 1000 330)">
  <text x="840" y="300" font-family="Inter" font-weight="700" font-size="40" letter-spacing="6" fill="#8b93a0">DOT</text>
  <rect x="890" y="320" width="230" height="96" rx="48" fill="none" stroke="${KOLLANE}" stroke-width="7"/>
  <text x="1005" y="392" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="80" letter-spacing="4" fill="${KOLLANE}">2319</text>
</g>`
};

export function ogPilt({ kicker = '', pealkiri, alapealkiri = '', sildid = [], pilt = '' }) {
	const lai = PILDID[pilt] ? 680 : 1020;
	/* pealkiri: suurim font, mis mahub kahele reale */
	let px = 104;
	let read = null;
	while (px >= 56 && !(read = murra(pealkiri, px, lai, 2))) px -= 8;
	if (!read) read = murra(pealkiri, 56, lai, 3) || [String(pealkiri).toUpperCase().slice(0, 60)];

	const yPeal = 262;
	const reaKorgus = Math.round(px * 0.98);
	const pealSvg = read
		.map((r, i) => `<text x="80" y="${yPeal + i * reaKorgus}" font-family="${KYR.test(pealkiri) ? 'Roboto Condensed' : 'Barlow Condensed'}" font-weight="700" font-size="${px}" fill="#ffffff">${esc(r)}</text>`)
		.join('');
	const yAla = yPeal + (read.length - 1) * reaKorgus + 64;

	let x = 80;
	const siltSvg = sildid
		.filter(Boolean)
		.slice(0, 3)
		.map((s) => {
			const w = Math.round(tekstiLaius(s) + 40);
			const g = `<rect x="${x}" y="470" width="${w}" height="56" rx="12" fill="#1a1d24" stroke="#2b3039"/>` +
				`<text x="${x + 20}" y="507" font-family="Inter" font-weight="500" font-size="26" fill="#f3f4f6">${esc(s)}</text>`;
			x += w + 14;
			return g;
		})
		.join('');

	const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<rect width="${W}" height="${H}" fill="${INK}"/>
${PILDID[pilt] || `<g opacity="0.10" fill="none" stroke="#ffffff">
  <circle cx="1080" cy="150" r="200" stroke-width="44"/>
  <circle cx="1080" cy="150" r="78" stroke-width="30"/>
</g>`}
<g transform="translate(80 104) skewX(-10)">
  <text x="0" y="0" font-family="Inter" font-weight="800" font-size="40" fill="#ffffff">PIDURDUSMAA<tspan fill="${KOLLANE}">.ee</tspan></text>
</g>
${kicker ? `<text x="80" y="164" font-family="Inter" font-weight="500" font-size="26" letter-spacing="3" fill="${KOLLANE}">${esc(String(kicker).toUpperCase())}</text>` : ''}
${pealSvg}
${alapealkiri ? `<text x="80" y="${yAla}" font-family="Inter" font-weight="500" font-size="34" fill="#c9ced6">${esc(alapealkiri)}</text>` : ''}
${siltSvg}
<rect x="0" y="${H - 14}" width="${W}" height="14" fill="${KOLLANE}"/>
</svg>`;

	koristaVahel();
	const r = new Resvg(svg, {
		font: { fontFiles: fondid(), loadSystemFonts: false, defaultFontFamily: 'Inter' },
		fitTo: { mode: 'width', value: W }
	});
	return r.render().asPng();
}
