/* Pakkuja toode → meie rehv.
 *
 * Pakkujal on rehv kirjas näiteks "MICHELIN Pilot Sport 5 225/40 R18 92Y XL",
 * meil on sama rehv "michelin-pilot-sport-5" mõõdus 22540R18. Sobitame nii:
 *   1. mõõt peab olema TÄPSELT sama
 *   2. mark peab olema sama (aliaste kaudu: "Conti" = "Continental")
 *   3. mudelinimi: mõõt, koormus/kiirusindeks ja XL/RunFlat jms eemaldatakse,
 *      seejärel peab ülejäänu olema sama (või vähemalt 85% samadest sõnadest)
 * Kui EAN on mõlemal olemas, võidab EAN. Kahtluse korral EI sobitata —
 * vale hind vale rehvi all on hullem kui hinnata jätmine.
 */
const MARK_ALIAS = {
	conti: 'continental',
	'bf goodrich': 'bfgoodrich',
	'b f goodrich': 'bfgoodrich',
	vredestein: 'vredestein',
	'goodyear dunlop': 'goodyear'
};

export function norm(s) {
	return String(s || '')
		.normalize('NFKD')
		.replace(/[̀-ͯ]/g, '')
		.toLowerCase()
		.replace(/[^a-z0-9]+/g, ' ')
		.trim();
}
export const normMark = (m) => {
	const n = norm(m);
	return MARK_ALIAS[n] || n.replace(/\s+/g, '');
};

/* "225/40 R18", "225/40R18", "22540R18", "225 40 ZR18" → 22540R18 */
export function normMoot(s) {
	const m = String(s || '')
		.toUpperCase()
		.match(/(\d{3})\s*[/ ]?\s*(\d{2})\s*Z?R\s*F?\s*(\d{2})(\s*C\b)?/);
	return m ? `${m[1]}${m[2]}R${m[3]}${m[4] ? 'C' : ''}` : null;
}

/* mudelinimest ära: mõõt, indeksid ja lisamärgid, mis ei muuda mudelit */
const MYRA = new Set(
	'xl rf rft runflat ssr zp extra load reinf reinforced fr mfs tl tubeless 3pmsf pmsf studded naast naastrehv suverehv talverehv lamellrehv aastaringne summer winter allseason all season'.split(
		' '
	)
);
export function mudeliSonad(mudel, mark) {
	let s = String(mudel || '');
	s = s.replace(/\d{3}\s*[/ ]?\s*\d{2}\s*Z?R\s*F?\s*\d{2}\s*C?/gi, ' '); // mõõt
	s = s.replace(/\b\d{2,3}(\/\d{2,3})?\s?[A-Z]\b/g, ' '); // 92Y, 104/102T
	s = s.replace(/\bM\s*[+&/]\s*S\b/gi, ' '); // M+S (mitte „S“ üksi — Pilot Sport 4 S on eri rehv)
	const markN = norm(mark);
	return norm(s)
		.split(' ')
		.filter((w) => w && !MYRA.has(w) && w !== markN);
}

function sarnasus(a, b) {
	const A = new Set(a), B = new Set(b);
	if (!A.size || !B.size) return 0;
	let yhine = 0;
	for (const x of A) if (B.has(x)) yhine++;
	return yhine / Math.max(A.size, B.size);
}

/**
 * Leia toote jaoks meie rehv samas mõõdus.
 * @param {{ mark: string, mudel: string, ean?: string }} toode
 * @param {Array} read  eprelSize(moot) read: [slug, mark, nimi, ...]
 * @returns {string|null} slug
 */
export function leiaRehv(toode, read) {
	const mk = normMark(toode.mark);
	const sonad = mudeliSonad(toode.mudel, toode.mark);
	const tapne = sonad.join(' ');
	let parim = null;
	let parimSkoor = 0;
	for (const r of read) {
		if (normMark(r[1]) !== mk) continue;
		const meie = mudeliSonad(r[2], r[1]);
		if (meie.join(' ') === tapne) return r[0];
		const s = sarnasus(sonad, meie);
		if (s > parimSkoor) {
			parimSkoor = s;
			parim = r[0];
		}
	}
	return parimSkoor >= 0.85 ? parim : null;
}
