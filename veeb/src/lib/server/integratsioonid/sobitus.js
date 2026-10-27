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
	'nokian renkaat': 'nokian',
	general: 'generaltire' /* „General GRABBER A/T3“ = General Tire */
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
const SONA_ALIAS = { ug: 'ultragrip', hkpl: 'hakkapeliitta', iceiynx: 'icelynx', nor1: 'noranza001' }; /* Bridgestone „NOR1“ = Noranza 001 */ /* EPREL: „HKPL R3“ = Hakkapeliitta R3 */

/* mudelinimest ära: mõõt, indeksid ja lisamärgid, mis ei muuda mudelit */
/* NB: „winter“, „summer“, „all season“ EI ole müra — „Scorpion“ ja „Scorpion Winter“, „Scorpion Zero“ ja „Scorpion Zero All Season“ on eri rehvid */
const MYRA = new Set(
	'xl rf rft runflat ssr zp extra load reinf reinforced fr mfs tl tubeless 3pmsf pmsf fsl bsw studded naast naastrehv suverehv talverehv lamellrehv aastaringne sealtech contisilent contiseal acoustic ext demo 4x4'.split(
		' '
	)
);
export function mudeliSonad(mudel, mark, poe = false) {
	let s = String(mudel || '').replace(/\([^)]*\)/g, ' '); // „Polaris North 6 (ContiVikingContact 6)“
	s = s.replace(/\d{3}\s*[/ ]?\s*\d{2}\s*Z?R\s*F?\s*\d{2}\s*C?/gi, ' '); // mõõt
	/* 92Y, 104/102T — aga ainult päris koormusindeksi vahemikus (60–130):
	   „WinterContact TS 860 S“ 860 ei ole indeks ja „860 S“ peab nimme jääma */
	s = s.replace(/\b(\d{2,3})(\/\d{2,3})?\s?[A-Z]\b/g, (k, n) => (+n >= 60 && +n <= 130 ? ' ' : k));
	s = s.replace(/\bM\s*[+&/]\s*S\b/gi, ' '); // M+S (mitte „S“ üksi — Pilot Sport 4 S on eri rehv)
	s = s.replace(/\+/g, ' plus '); // „UltraGrip Ice 2+“ ≠ „UltraGrip Ice 2“
	s = s.replace(/\b([A-Za-z]{1,3})-(\d{1,4}[A-Za-z]?)\b/g, '$1$2'); // „AT-771“ = „AT771“, „SP-02“ = „SP02“
	/* margi sõnad välja ("Nokian Tyres Hakkapeliitta R5" → "hakkapeliitta r5") */
	const markW = new Set(norm(mark).split(' '));
	let w = norm(s)
		.split(' ')
		.map((x) => SONA_ALIAS[x] || x)
		.filter((x) => x && !MYRA.has(x) && !markW.has(x) && !OE.test(x));
	/* sarjanimi, mida pood vahel kirjutab, vahel mitte: Kumho „WINTERCRAFT WP52+“ = „WP52+“,
	   „SOLUS 4S HA32“ = „HA32“; Dunlop „SP SPORT MAXX RT 2“ = „SPORT MAXX RT2“ */
	/* „Ecsta“ ei ole siin: „Ecsta PS71“ (test) ja „PS71“ (EPREL) jääks muidu kaheks võrdseks kandidaadiks */
	const SARI = { kumho: ['wintercraft', 'solus', '4s'], dunlop: ['sp'] }[normMark(mark)];
	if (SARI && w.some((x) => /\d/.test(x))) {
		const ilma = w.filter((x) => !SARI.includes(x));
		if (ilma.length) w = [...new Set(ilma)];
	}
	/* Pirelli „WINTER ICE ZERO ASIMMETRICO“ = „ICE ZERO ASIMMETRICO“ */
	if (normMark(mark) === 'pirelli' && w[0] === 'winter' && w[1] === 'ice' && w[2] === 'zero' && w[3] === 'asimmetrico') w = w.slice(1);
	/* Pirelli „P ZERO SPORT“, „P-ZERO S.C“, „P ZERO LUXURY“, „P-ZERO L.S.“, „P-ZERO PZ4/PZ5“: EPREL-is kõik
	   üks „PZERO“ (PZ4/PZ5 Sports Car / Luxury Saloon). Corsa, E, Winter, All Season jäävad eraldi. */
	if (normMark(mark) === 'pirelli' && w[0] === 'p' && w[1] === 'zero' && w.slice(2).every((x) => /^(sport|luxury|s|c|l|pz4|pz5)$/.test(x)))
		w = ['pzero'];
	if (normMark(mark) === 'pirelli' && w.length === 1 && w[0] === 'pzero') w = ['pzero'];
	/* Yokohama „iceGUARD Stud iG65“ = meie „iceGUARD iG65“ (naastrehvi nimes „Stud“ ei erista) */
	if (normMark(mark) === 'yokohama' && w.includes('guard')) w = w.filter((x) => x !== 'stud');
	/* Maxxis naastrehv: pood „NS5 PREMITRA ICE“ = „Premitra Ice Nord 5 SUV“, „NP5 PREMITRA ICE“ = „Premitra Ice Nord NP5“ */
	if (normMark(mark) === 'maxxis' && w.includes('premitra')) {
		if (w.includes('ns5')) w = ['premitra', 'ice', 'nord', '5', 'suv'];
		else if (w.includes('np5')) w = ['premitra', 'ice', 'nord', 'np5'];
	}
	/* Hankooki tehasekood (W429, K135, H750) — üks pood kirjutab, teine mitte */
	/* „Winter i*cept X RW10“ = „i-Cept X“: Hankooki talvesarjal (i*cept, i*pike) ei erista
	   sõna „winter“ midagi ja RW/RA-kood (RW10, RW15) on tehasekood nagu W429 */
	if (normMark(mark) === 'hankook') {
		/* RW/RA-kood on tehasekood (RA33 = Dynapro HP2, RW10 = i*cept X), AGA i*Pike'il on kood
		   mudeli nimi (RW11 ≠ RS2) — seal jääb alles */
		const pike = w.includes('pike');
		const ilma = w.filter((x) => !(/^[khwrz]\d{3}[a-z]?$/.test(x) || (!pike && /^r[wa]\d{2}$/.test(x))));
		if (ilma.length) w = ilma;
		if (w.some((x) => /^i?(cept|pike)$/.test(x))) w = w.filter((x) => x !== 'winter');
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
	const v = leiaRehv0(toode, read);
	if (v) return v;
	/* „CINTURATO P7 (P7C2)“ meil vs „CINTURATO P7 P7C2“ poes: sulgude sisu loeb siis kaasa */
	if (read.some((r) => /\(/.test(r[2]) && normMark(r[1]) === normMark(toode.mark))) {
		const sulgudega = read.filter((r) => /\(/.test(r[2])).map((r) => [r[0], r[1], String(r[2]).replace(/[()]/g, ' ')].concat(r.slice(3)));
		const w = leiaRehv0(toode, sulgudega);
		if (w) return w;
	}
	return null;
}
function leiaRehv0(toode, read) {
	const mk = normMark(toode.mark);
	const sonad = mudeliSonad(toode.mudel, toode.mark, true);
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
	/* tehasekood: „TS870“, „W330A“, ka lühike „WP6“, „AP3“, „SP5“ (aga mitte „R5“, „P7“) */
	const kood = (x) => /^[a-z]{1,3}\d{2,4}[a-z]?$/.test(x) || /^(?!pz)[a-z]{2,3}\d$/.test(x); /* PZ4/PZ5 = P Zero põlvkond, mitte kood */
	const [aK, aS] = [sonad.filter(kood), sonad.filter((x) => !kood(x))];
	if (aS.length) {
		for (const r of read) {
			if (normMark(r[1]) !== mk) continue;
			const meie = mudeliSonad(r[2], r[1]);
			const bK = meie.filter(kood), bS = meie.filter((x) => !kood(x));
			if (aK.length && bK.length && aK.join(' ') !== bK.join(' ')) continue;
			if (kokku(bS, r[1]) !== kokku(aS, toode.mark)) continue;
			/* poel koodi pole, meil on: sobib ainult siis, kui sama nimega mudeleid on üks.
			   „Sailun Ice Blazer“ (kasutatud, Minurattad 27.10) läks WST3 alla, aga samas mõõdus
			   on ka Ice Blazer Alpine EVO2 ja Spike → kahtlane, ei sobita. */
			if (!aK.length && bK.length) {
				const pere = new Set();
				for (const q of read) {
					if (normMark(q[1]) !== mk) continue;
					const qw = mudeliSonad(q[2], q[1]);
					if (aS.every((x) => qw.includes(x))) pere.add(qw.join(' '));
				}
				if (pere.size > 1) continue;
			}
			return r[0];
		}
	}
	/* ainult tehasekood („V906“, „TS870P“, „W330A“): sobib, kui täpselt ühel sama margi
	   rehvil on see kood nimes (eraldi sõnana või nime lõpus kokkukirjutatult) */
	if (aK.length && !aS.length) {
		const vasted = new Set();
		for (const r of read) {
			if (normMark(r[1]) !== mk) continue;
			/* „WP52“ ≠ „WP52+“: pluss on eri mudel ka ainult-koodi puhul */
			if (/\+|\bplus\b/i.test(r[2]) !== /\+|\bplus\b/i.test(toode.mudel)) continue;
			const w = norm(r[2]).split(' '), j = w.join('');
			if (aK.every((k) => w.includes(k) || j.endsWith(k))) vasted.add(r[0]);
		}
		if (vasted.size === 1) return [...vasted][0];
	}
	/* kood + sõnad ühel pool, ainult kood teisel („WinterCraft WS71“ ↔ „WS71“): koodid samad */
	if (aK.length) {
		const vasted = new Set(), nimed = new Set();
		for (const r of read) {
			if (normMark(r[1]) !== mk) continue;
			const meie = mudeliSonad(r[2], r[1]);
			const bK = meie.filter(kood), bS = meie.filter((x) => !kood(x));
			/* „HA32+“ ≠ „HA32“: pluss on eri mudel */
			if (aS.includes('plus') !== bS.includes('plus')) continue;
			/* „WI31+“ ↔ „WinterCraft Ice WI31+“: pluss on osa koodist, mitte nimesõna */
			const aS2 = aS.filter((x) => x !== 'plus'), bS2 = bS.filter((x) => x !== 'plus');
			if (bK.length && bK.join(' ') === aK.join(' ') && (!bS2.length || !aS2.length)) { vasted.add(r[0]); nimed.add(meie.join(' ')); }
		}
		if (vasted.size === 1) return [...vasted][0];
		/* sama rehv kahe slugiga (EPREL „WS51“ ja test „WinterCraft WS51“ pärast sarjanime eemaldust):
		   nimed on identsed -> esimene (EPREL-i rida on read-is ees) */
		if (vasted.size > 1 && nimed.size === 1) return [...vasted][0];
	}
	/* „SOTTOZERO 3“ = „WINTER SOTTOZERO 3“: ainus vahe on sõna „winter“ ja nimes on number
	   (ilma numbrita mitte: „Scorpion“ ≠ „Scorpion Winter“) */
	if (sonad.some((x) => /\d/.test(x))) {
		const vasted = new Set();
		const ilmaW = (w) => w.filter((x) => x !== 'winter').join(' ');
		for (const r of read) {
			if (normMark(r[1]) !== mk) continue;
			const meie = mudeliSonad(r[2], r[1]);
			/* „SOTTO ZERO 3“ = „WINTER SOTTOZERO 3“: ka kokkukirjutatult */
			if (meie.includes('winter') !== sonad.includes('winter') && (ilmaW(meie) === ilmaW(sonad) || ilmaW(meie).replace(/ /g, '') === ilmaW(sonad).replace(/ /g, ''))) vasted.add(r[0]);
		}
		if (vasted.size === 1) return [...vasted][0];
	}
	return parimSkoor >= 0.85 ? parim : null;
}
