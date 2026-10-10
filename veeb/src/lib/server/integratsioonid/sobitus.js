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
	'goodyear dunlop': 'goodyear',
	'nokian tyres': 'nokian',
	'nokian renkaat': 'nokian'
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

/* autotootja sobivusmärgid (Mercedes MO1, Porsche N0–N5/NA0, Audi AO/RO1, BMW *, Volvo VOL, Jaguar J …):
   sama rehv, ainult heakskiidu märk — mõlemal poolel ära */
const OE = /^(mo|mo1|moe|ao|ao1|ro1|ro2|r01|n[0-5]|n[a-f][0-9]|j|lr|frv|vol|volfr|goe|tpc|ar)$/;

/* lühendid mudelinimes */
const SONA_ALIAS = { ug: 'ultragrip' };

/* mudelinimest ära: mõõt, indeksid ja lisamärgid, mis ei muuda mudelit */
/* NB: „winter“, „summer“, „all season“ EI ole müra — „Scorpion“ ja „Scorpion Winter“, „Scorpion Zero“ ja „Scorpion Zero All Season“ on eri rehvid */
const MYRA = new Set(
	'xl rf rft runflat ssr zp extra load reinf reinforced fr mfs tl tubeless 3pmsf pmsf fsl bsw studded naast naastrehv suverehv talverehv lamellrehv aastaringne'.split(
		' '
	)
);
export function mudeliSonad(mudel, mark) {
	let s = String(mudel || '').replace(/\([^)]*\)/g, ' '); // „Polaris North 6 (ContiVikingContact 6)“
	s = s.replace(/\d{3}\s*[/ ]?\s*\d{2}\s*Z?R\s*F?\s*\d{2}\s*C?/gi, ' '); // mõõt
	/* 92Y, 104/102T — aga ainult päris koormusindeksi vahemikus (60–130):
	   „WinterContact TS 860 S“ 860 ei ole indeks ja „860 S“ peab nimme jääma */
	s = s.replace(/\b(\d{2,3})(\/\d{2,3})?\s?[A-Z]\b/g, (k, n) => (+n >= 60 && +n <= 130 ? ' ' : k));
	s = s.replace(/\bM\s*[+&/]\s*S\b/gi, ' '); // M+S (mitte „S“ üksi — Pilot Sport 4 S on eri rehv)
	s = s.replace(/\+/g, ' plus '); // „UltraGrip Ice 2+“ ≠ „UltraGrip Ice 2“
	/* margi sõnad välja ("Nokian Tyres Hakkapeliitta R5" → "hakkapeliitta r5") */
	const markW = new Set(norm(mark).split(' '));
	let w = norm(s)
		.split(' ')
		.map((x) => SONA_ALIAS[x] || x)
		.filter((x) => x && !MYRA.has(x) && !markW.has(x) && !OE.test(x));
	/* Hankooki tehasekood (W429, K135, H750) — üks pood kirjutab, teine mitte */
	if (normMark(mark) === 'hankook') {
		const ilma = w.filter((x) => !/^[khwrz]\d{3}[a-z]?$/.test(x));
		if (ilma.length) w = ilma;
	}
	return w;
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
	/* kokkukirjutatult: „IceBlazer Arctic 2“ = „ICE BLAZER ARCTIC2“, „TS860 S“ = „TS 860 S“;
	   Continentali „Conti…“ eesliide („ContiWinterContact“ = „WinterContact“) */
	const kokku = (w, m) => {
		let j = w.join('');
		if (normMark(m) === 'continental') j = j.replace(/^conti(?=[a-z])/, '');
		return j;
	};
	const tapneK = kokku(sonad, toode.mark);
	let kokkuVaste = null;
	let parim = null;
	let parimSkoor = 0;
	for (const r of read) {
		if (normMark(r[1]) !== mk) continue;
		const meie = mudeliSonad(r[2], r[1]);
		if (meie.join(' ') === tapne) return r[0];
		if (!kokkuVaste && tapneK && kokku(meie, r[1]) === tapneK) kokkuVaste = r[0];
		const s = sarnasus(sonad, meie);
		if (s > parimSkoor) {
			parimSkoor = s;
			parim = r[0];
		}
	}
	if (kokkuVaste) return kokkuVaste;
	/* tehasekoodiga või ilma: „EffexSport TH202“ = „EffeXSport“, aga
	   „IcePlus S210“ ≠ „IcePlus S220“ (mõlemal kood ja need erinevad) */
	const kood = (x) => /^[a-z]{1,3}\d{2,4}[a-z]?$/.test(x);
	const [aK, aS] = [sonad.filter(kood), sonad.filter((x) => !kood(x))];
	if (aS.length) {
		for (const r of read) {
			if (normMark(r[1]) !== mk) continue;
			const meie = mudeliSonad(r[2], r[1]);
			const bK = meie.filter(kood), bS = meie.filter((x) => !kood(x));
			if (aK.length && bK.length && aK.join(' ') !== bK.join(' ')) continue;
			if (kokku(bS, r[1]) === kokku(aS, toode.mark)) return r[0];
		}
	}
	/* ainult tehasekood („V906“, „TS870P“, „W330A“): sobib, kui täpselt ühel sama margi
	   rehvil on see kood nimes (eraldi sõnana või nime lõpus kokkukirjutatult) */
	if (aK.length && !aS.length) {
		const vasted = new Set();
		for (const r of read) {
			if (normMark(r[1]) !== mk) continue;
			const w = norm(r[2]).split(' '), j = w.join('');
			if (aK.every((k) => w.includes(k) || j.endsWith(k))) vasted.add(r[0]);
		}
		if (vasted.size === 1) return [...vasted][0];
	}
	/* kood + sõnad ühel pool, ainult kood teisel („WinterCraft WS71“ ↔ „WS71“): koodid samad */
	if (aK.length) {
		const vasted = new Set();
		for (const r of read) {
			if (normMark(r[1]) !== mk) continue;
			const meie = mudeliSonad(r[2], r[1]);
			const bK = meie.filter(kood), bS = meie.filter((x) => !kood(x));
			/* „HA32+“ ≠ „HA32“: pluss on eri mudel */
			if (aS.includes('plus') !== bS.includes('plus')) continue;
			if (bK.length && bK.join(' ') === aK.join(' ') && (!bS.length || !aS.length)) vasted.add(r[0]);
		}
		if (vasted.size === 1) return [...vasted][0];
	}
	return parimSkoor >= 0.85 ? parim : null;
}
