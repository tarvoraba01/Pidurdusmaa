/* Rehvimärgid väikeste piltidena teksti sees. Kui tekst räägib märgist,
   näidatakse ka märki ennast — inimene tunneb selle poes rehvi küljel
   või EL-i rehvimärgisel ära.
   3PMSF: kolm mäetippu ja lumehelves (UNECE R117 lumehaarde märk).
   Jää: EL-i rehvimärgise jäähaarde piktogramm (mägi kaldjoontega, EL 2020/740).
   M+S: ainult tekst rehvi küljel, talvehaaret ei tõenda. */

const svg = (silt, sisu, w = 30) =>
	`<svg class="mrk" viewBox="0 0 ${w} 26" width="${Math.round(w * 1.05)}" height="27" role="img" aria-label="${silt}"><title>${silt}</title>${sisu}</svg>`;

const MAGI = 'M1.5 24.5 8.5 10l3.2 5.2L15.5 3l4 10.5 2.8-4.2 6.2 15.2z';
const HELVES =
	'<g stroke-width="1.3"><path d="M15 13.2v9.6M10.8 15.6l8.4 4.8M19.2 15.6l-8.4 4.8"/><path d="m13.6 13.9 1.4 1 1.4-1M13.6 22.1l1.4-1 1.4 1" stroke-width="1"/></g>';

export function lumi(silt = 'Kolme mäetipu ja lumehelbe märk (3PMSF)') {
	return svg(silt, `<g fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="1.6"><path d="${MAGI}"/>${HELVES}</g>`);
}

export function jaa(silt = 'Jäämärk (EL-i rehvimärgise jäähaarde sümbol)') {
	return svg(
		silt,
		'<defs><clipPath id="mrk-j"><path d="M2 24.5 15 2.5l13 22z"/></clipPath></defs>' +
			'<g fill="none" stroke="currentColor" stroke-linejoin="round"><path d="M2 24.5 15 2.5l13 22z" stroke-width="1.6"/>' +
			'<g clip-path="url(#mrk-j)" stroke-width="1"><path d="M0 22 8 14M0 28l14-14M6 28l14-14M12 28l14-14M18 28l12-12M24 28l6-6"/></g></g>'
	);
}

export function ms(silt = 'M+S märk (ainult muster, mitte talverehvi tõend)') {
	return svg(
		silt,
		'<rect x="1" y="5" width="36" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="1.4"/>' +
			'<text x="19" y="17.2" text-anchor="middle" font-size="11" font-weight="700" font-family="system-ui,sans-serif" fill="currentColor">M+S</text>',
		38
	);
}
