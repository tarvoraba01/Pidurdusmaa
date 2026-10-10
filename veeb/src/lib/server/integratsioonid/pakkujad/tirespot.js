/* TIRESPOT.EE (Pärnu) — lao XML-voog: hind, laoseis ja pilt rehvi kaardile.
 *
 * Coolify:
 *   PAKKUJA_TIRESPOT_URL = (Tirespoti saadetud XML-i aadress, tirespot.ee/module/shopExport/…)
 *
 * Voog on üks ~45 MB XML-fail (~80 000 rida: rehvid, veljed, moto jm). Loeme selle
 * voona tükkhaaval (kogu fail ei ole korraga mälus), hoiame alles ainult meie
 * mõõtudes sõiduauto/maasturi/kaubiku rehvid, millel on laoseis, ja vastame
 * hinnapäringutele mälust. Värskendus iga 6 h; kui see ebaõnnestub, kehtib
 * eelmine (kuni 48 h).
 *
 * VÄLJAD (kontrollitud 10.10.2026 e-poe vastu):
 *   soovituslik_jaehind = e-poe müügihind ILMA käibemaksuta → ×1,24 = poe hind
 *     (nt 257,0865 → 318,79 €, täpselt nagu tirespot.ee lehel)
 *   jaehind = läbikriipsutatud „tavahind“ ilma km-ta — ei kasuta
 *   hulgihind = HULGIHIND — mitte kunagi lehele ega mällu (ei loeta üldse)
 *   laos = Tirespoti oma ladu (tk), tootjalaos = tarnija ladu (tellimisel)
 *   tootelinki voos ei ole → „Osta“ viib e-poe sama mõõdu nimekirja
 *
 * TURVA: ainult GET sellele ühele aadressile (http.js hostide kontroll).
 */
import { normMoot } from '../sobitus.js';
import { core } from '$lib/server/andmed.js';

const KM = 1.24; /* Eesti käibemaks 24 % (alates 1.07.2025) */
const VARSKE_MS = 6 * 3600 * 1000;
const MAX_VANUS_MS = 48 * 3600 * 1000;
const OOTA_VEA_JAREL_MS = 10 * 60 * 1000;
const POOD = 'https://www.tirespot.ee/';
/* e-poe kategooria → aadressi osa; muud (veljed, moto, veoauto, agro) jäetakse välja */
const KAT = { 'Sõiduauto/Maastur': 'soiduauto-maastur', Kaubik: 'kaubik' };

let indeks = null; // Map moot -> [toode]
let laetud = 0;
let laadib = null;
let viimaneViga = null;
const info = { ridu: 0, hoitud: 0, laetud: null, kestusMs: 0 };

const valja = (s, t) => {
	const m = new RegExp('<' + t + '>([^<]*)</' + t + '>').exec(s);
	/* voos on täpitähed koodina: „S&#xF5;iduauto“, „L&#xE4;&#xE4;ne“ */
	return m
		? m[1]
				.replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
				.replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(+d))
				.replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
				.trim()
		: '';
};
const arv = (v) => {
	const n = Number(String(v ?? '').replace(',', '.'));
	return Number.isFinite(n) ? n : NaN;
};

/* Tirespoti nimes on mudeli järel tehnilised märgid ja autotootja sobivus:
   „ULTRAGRIP PERFORMANCE 3   XL FP Elect Lääne-euroopa lamell“,
   „SCORPION WINTER 2 NC0 PORSCHE CAYENNE (PO536) 2017 >, Front XL FSL …“.
   Mudel = osa enne topelttühikut, ilma nende märkideta ja autotootja tekstita. */
const MYRA_SONAD = new Set(
	('XL RP RPB FP FR FSL NCS HL KS VOL POR OWL WL ELECT ENLITEN ECOPOINT3 W-SILENT B-SILENT SOUNDCOMFORT SOUND ABSORBER SEAL INSIDE ' +
		'MOEXTENDED MOE MO MO1 AO A0 RO1 R0 N0 N1 N2 NA0 NC0 NE0 ND0 MGT HN J LR RG RFT RUNFLAT SSR ZP DOT22 DOT23 DOT24 3PMSF M+S IGS VELJEKAITSEGA').split(' ')
);
const AUTOD = /\b(PORSCHE|AUDI|BMW|MERCEDES|VOLKSWAGEN|VW|SKODA|LAND ROVER|ASTON MARTIN|VOLVO|TESLA|JAGUAR|BENTLEY|FERRARI|LAMBORGHINI|MASERATI|TOYOTA|LEXUS)\b/i;
const HOOAEG = /\b(Suverehvid|Naastutatud|Naastrehvid|Aastaringsed rehvid|Pehme lamell|Lääne-euroopa lamell|Lääne-euroopa|Põhjamaade lamellrehvid|lamellrehvid)\b.*$/i;
/* Hankooki nimes on tihti ainult tehasekood (W330, K127A) — meie andmetes on mudeli nimi */
const HANKOOK = {
	W330: 'Winter i*cept evo3', W330A: 'Winter i*cept evo3 X', W320: 'Winter i*cept evo2', W320A: 'Winter i*cept evo2 SUV', W340: 'Winter i*cept evo 4',
	W462: 'Winter i*cept RS3', W452: 'Winter i*cept RS2', W442: 'Winter i*cept RS', W429: 'Winter i*Pike RS2', W429A: 'Winter i*Pike X', W419: 'Winter i*Pike RS',
	W636: 'Winter i*cept iZ3', W636A: 'Winter i*cept iZ3 X', W626: 'Winter i*cept iZ2', RW10: 'Winter i*cept X', RW12: 'Winter i*cept LV',
	K127: 'Ventus S1 evo3', K127A: 'Ventus S1 evo3 SUV', K127B: 'Ventus S1 evo3', K127E: 'Ventus S1 evo3 EV', K137: 'Ventus evo', K137A: 'Ventus evo SUV',
	K117: 'Ventus S1 evo2', K117A: 'Ventus S1 evo2 SUV', K125: 'Ventus Prime3', K135: 'Ventus Prime4', K115: 'Ventus Prime2', K435: 'Kinergy eco2',
	H750: 'Kinergy 4S 2', H750A: 'Kinergy 4S 2 X', H740: 'Kinergy 4S', RA43: 'Dynapro HPX', RF11: 'Dynapro AT2'
};
export function puhastaNimi(nimi, mark = '') {
	let s = String(nimi || '').split(/\s{2,}/)[0];
	s = s.replace(/\bEV\s+ready\b/gi, ' ');
	s = s.replace(HOOAEG, ' ');
	const a = AUTOD.exec(s);
	if (a) s = s.slice(0, a.index);
	s = s.replace(/\((\*|I\*|\+)\)|\s\*(\s|$)/g, ' ');
	/* sulgudes tehasekood jääb nimesse: „ICE GUARD (IG60A)“ ≠ „iceGUARD G075“ */
	s = s.replace(/\(([A-Z0-9-]{2,8})\)/gi, ' $1 ');
	s = s
		.split(/\s+/)
		.filter((w) => w && !MYRA_SONAD.has(w.toUpperCase()))
		.join(' ')
		.trim();
	const mk = String(mark).toLowerCase();
	if (mk === 'hankook') {
		const k = s.replace(/[()]/g, ' ').trim().toUpperCase();
		if (HANKOOK[k]) return HANKOOK[k];
	}
	if (mk === 'continental') {
		/* „CONTI ECO CONTACT 6“ → „EcoContact 6“, „ALLSEASON CONTACT“ → „AllSeasonContact“ */
		s = s.replace(/^CONTI\s+/i, '').replace(/\b([A-Za-z]+)\s+CONTACT\b/gi, '$1Contact');
	}
	if (mk === 'goodyear') s = s.replace(/\b4\s+SEASONS\b/gi, '4SEASONS').replace(/\bG(\d)\b/g, 'GEN-$1');
	return s;
}

/** E-poe sama mõõdu nimekiri (filter laius/kõrgus/diameeter). */
export function poeLinkMoodule(moot, kat = 'soiduauto-maastur') {
	const m = /^(\d{3})(\d{2})R(\d{2})/.exec(moot || '');
	if (!m) return POOD;
	return `${POOD}pood/kategooria/${kat}/filter/laius:${+m[1]};korgus:${+m[2]};diameeter:${+m[3]};/`;
}

/** Üks <product> sisu → meie kuju või null. hulgihinda ei loeta. */
export function teisenda(s, meieMoodud) {
	const kat = KAT[valja(s, 'kategooria')];
	if (!kat) return null;
	/* kaubiku C-rehv: voos C-tähist pole, aga topeltkoormusindeks (109/107) on C-rehvi tunnus */
	const c = kat === 'kaubik' && /^\d{2,3}\/\d{2,3}/.test(valja(s, 'koormusindeks'));
	const moot = normMoot(`${valja(s, 'laius')}/${valja(s, 'korgus')} R${valja(s, 'diameeter')}${c ? ' C' : ''}`);
	if (!moot || (meieMoodud && !meieMoodud.has(moot))) return null;
	const laos = Math.max(0, Math.round(arv(valja(s, 'laos')) || 0));
	const tootja = Math.max(0, Math.round(arv(valja(s, 'tootjalaos')) || 0));
	if (!laos && !tootja) return null; /* pole saadaval */
	const ilmaKm = arv(valja(s, 'soovituslik_jaehind'));
	const hind = Math.round(ilmaKm * KM * 100) / 100;
	if (!(hind > 5 && hind < 5000)) return null;
	const mark = valja(s, 'tootja');
	/* „TURANZA T005  AO  B-Silent“, „W.DRIVE (WY01)    Lääne-euroopa lamell“: mudel on osa enne topelttühikut;
	   autotootja märgised (AO, MO, *) ei muuda mudelit */
	const mudel = puhastaNimi(valja(s, 'nimi'), mark);
	if (!mark || !mudel) return null;
	const li = valja(s, 'koormusindeks'), si = valja(s, 'kiirusindeks');
	const pilt = valja(s, 'pilt');
	const ean = valja(s, 'ean');
	const kood = valja(s, 'kood');
	return {
		mark,
		mudel,
		moot,
		hind,
		laos: laos > 0,
		kogus: laos > 0 ? laos : undefined,
		lisi: [li, si].filter(Boolean).join(' ').slice(0, 30) || undefined,
		ean: /^\d{8,14}$/.test(ean) ? ean : undefined,
		pilt: /^https:\/\//.test(pilt) ? pilt : undefined,
		/* tootekoodiga otsing annab poes täpselt selle toote; täpne link ja hind tulevad taustal (tapsusta) */
		kood: /^[\w.-]{1,30}$/.test(kood) ? kood : undefined,
		url: /^[\w.-]{1,30}$/.test(kood) ? `${POOD}pood/shopsearch/${encodeURIComponent(kood)}` : poeLinkMoodule(moot, kat),
		/* voo soovitushind võib poe hinnast ±5% erineda, kuni täpne hind on poest kontrollitud */
		umbes: true,
		myyja: 'tirespot.ee'
	};
}

/* ---------------------------------------------------------------- täpsustus
 * Voos pole tootelinki ja poe hind võib soovitushinnast veidi erineda.
 * Poe otsing tootekoodiga (/pood/shopsearch/<kood>) annab täpselt selle toote
 * kaardi: lingi tootelehele, tegeliku hinna ja pildi. Seda tehakse ainult
 * mõõtudele, mida keegi vaatab, taustal, 2 korraga, tulemus 12 h meeles. */
const TAPNE_MS = 12 * 3600 * 1000;
const tapne = new Map(); // kood -> { url, hind, pilt, aeg } | { puudub: true, aeg }
const jarjekord = new Set();
let toolisi = 0;

/** Poe otsingutulemuse HTML → toote kaardid. */
export function loeOtsing(html) {
	const kaardid = [];
	for (const osa of String(html).split(/class="item\s/).slice(1)) {
		const href = /href="\/?(pood\/toode\/[^"#?]+)"/.exec(osa);
		const hind = /class="price[^"]*">\s*([\d.]+)\s*€/.exec(osa);
		if (!href || !hind) continue;
		const pealkiri = (/title="([^"]*)"/.exec(osa) || [])[1] || '';
		const pilt = (/data-bg="(https:\/\/[^"]+)"/.exec(osa) || [])[1];
		kaardid.push({ url: POOD + href[1], hind: +hind[1], pealkiri, pilt });
	}
	return kaardid;
}

/** Mitme vaste korral õige mõõduga kaart; muidu ainus. */
export function valiKaart(kaardid, moot) {
	if (kaardid.length === 1) return kaardid[0];
	const m = /^(\d{3})(\d{2})R(\d{2})/.exec(moot || '');
	const silt = m ? `${m[1]}/${m[2]}R${m[3]}` : null;
	const oiged = silt ? kaardid.filter((k) => k.pealkiri.includes(silt)) : [];
	return oiged.length === 1 ? oiged[0] : null;
}

function tapsusta(pakkuja, ctx, read) {
	for (const r of read) {
		if (!r.kood) continue;
		const t = tapne.get(r.kood);
		if (t && Date.now() - t.aeg < TAPNE_MS) continue;
		jarjekord.add(r.kood + '|' + r.moot);
	}
	while (toolisi < 2 && jarjekord.size) {
		toolisi++;
		(async () => {
			try {
				while (jarjekord.size) {
					const v = jarjekord.values().next().value;
					jarjekord.delete(v);
					const [kood, moot] = v.split('|');
					try {
						const r = await ctx.paring(pakkuja, `${POOD}pood/shopsearch/${encodeURIComponent(kood)}`, { maxBaite: 3_000_000, aegMs: 10_000 });
						if (r.status !== 200) throw new Error('HTTP ' + r.status);
						const k = valiKaart(loeOtsing(r.andmed.toString('utf-8')), moot);
						tapne.set(kood, k && k.hind > 5 && k.hind < 5000 ? { url: k.url, hind: k.hind, pilt: k.pilt, aeg: Date.now() } : { puudub: true, aeg: Date.now() });
					} catch {
						/* ajutine viga: proovib järgmisel vaatamisel uuesti */
					}
					while (tapne.size > 30000) tapne.delete(tapne.keys().next().value);
				}
			} finally {
				toolisi--;
			}
		})();
	}
}

function koosTapsusega(r) {
	const t = r.kood && tapne.get(r.kood);
	if (!t || t.puudub || Date.now() - t.aeg > TAPNE_MS) return r;
	return { ...r, url: t.url, hind: t.hind, umbes: false, pilt: r.pilt || t.pilt };
}

async function laeKoik(pakkuja, { muutuja, voog }) {
	const aadress = muutuja('PAKKUJA_TIRESPOT_URL');
	const algus = Date.now();
	const meieMoodud = new Set((core().eprelSizes || []).filter((m) => /^\d{5}R\d{2}C?$/.test(m)));
	const r = await voog(pakkuja, aadress, { maxBaite: 150_000_000, aegMs: 180_000 });
	const uus = new Map();
	let ridu = 0, hoitud = 0;
	let jaak = '';
	const dek = new TextDecoder('utf-8');
	const tootle = (tekst) => {
		let i = 0;
		for (;;) {
			const a = tekst.indexOf('<product>', i);
			if (a < 0) return tekst.slice(i);
			const b = tekst.indexOf('</product>', a);
			if (b < 0) return tekst.slice(a);
			ridu++;
			const t = teisenda(tekst.slice(a + 9, b), meieMoodud);
			if (t) {
				hoitud++;
				const l = uus.get(t.moot);
				if (l) l.push(t);
				else uus.set(t.moot, [t]);
			}
			i = b + 10;
		}
	};
	for await (const tykk of r.keha) jaak = tootle(jaak + dek.decode(tykk, { stream: true }));
	tootle(jaak + dek.decode());
	if (!ridu) throw new Error('tirespot: voos ei olnud ühtegi toodet');
	if (!hoitud) throw new Error(`tirespot: ${ridu} rida, aga ükski ei sobinud meie mõõtudega`);
	if (indeks && info.hoitud > 200 && hoitud < info.hoitud * 0.2)
		throw new Error(`tirespot: ainult ${hoitud} sobivat toodet (enne ${info.hoitud}) — jätsin vana`);
	indeks = uus;
	laetud = Date.now();
	Object.assign(info, { ridu, hoitud, laetud: new Date(laetud).toISOString(), kestusMs: Date.now() - algus });
	viimaneViga = null;
}

function lae(pakkuja, ctx) {
	if (laadib) return laadib;
	if (viimaneViga && Date.now() - viimaneViga.aeg < OOTA_VEA_JAREL_MS) return Promise.reject(new Error(viimaneViga.teade));
	laadib = laeKoik(pakkuja, ctx)
		.catch((e) => {
			viimaneViga = { aeg: Date.now(), teade: String(e.message || e).slice(0, 200) };
			throw new Error(viimaneViga.teade);
		})
		.finally(() => {
			laadib = null;
		});
	return laadib;
}

export default {
	id: 'tirespot',
	nimi: 'tirespot.ee',
	/* voog + tootepildid (Erply CDN) */
	hostid: ['www.tirespot.ee', 'tirespot.ee', 'eu.erply.com', 'cdn-old.erply.com'],
	poeHostid: ['www.tirespot.ee', 'tirespot.ee'],
	env: ['PAKKUJA_TIRESPOT_URL'],
	ttlHinnad: 120, /* täpsustatud link ja hind jõuavad lehele kiiresti */

	async soojenda(ctx) {
		await lae(this, ctx);
	},

	async hinnadMoodus(moot, ctx) {
		if (!indeks) await lae(this, ctx);
		else if (Date.now() - laetud > VARSKE_MS) lae(this, ctx).catch(() => {});
		if (Date.now() - laetud > MAX_VANUS_MS) throw new Error('tirespot: andmed üle 48 h vanad ja värskendus ei õnnestu');
		const read = indeks.get(moot) || [];
		if (ctx.paring) tapsusta(this, ctx, read);
		return read.map(koosTapsusega);
	},

	lisaOlek() {
		let tapseid = 0;
		for (const t of tapne.values()) if (!t.puudub) tapseid++;
		return { ...info, viga: viimaneViga ? viimaneViga.teade : null, laadib: !!laadib, tapseid, jarjekorras: jarjekord.size };
	}
};
