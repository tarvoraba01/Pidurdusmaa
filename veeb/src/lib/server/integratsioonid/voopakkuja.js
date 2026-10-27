/* Ühine XML-tootevoo pakkuja: laeb voo (voona, mitte korraga mällu), hoiab ainult
 * meie mõõtudes rehvid, värskendab iga 6 h, vea korral kehtib eelmine kuni 48 h.
 * Sama loogika mis intercars.js-is, aga korduvkasutatav (Minurattad, Extensa, …).
 *
 *   looVoopakkuja({ id, nimi, aadress, env, hostid, poeHostid, element, teisenda })
 *     aadress  = vaikimisi voo URL (avalik, ilma võtmeta); `env` muutuja kirjutab üle
 *     element  = kordumise silt: 'item' (Google Merchant RSS) või 'product'
 *     teisenda = (tooteXml, meieMoodud) => toode | toode[] | null
 * TURVA: päringud ainult `hostid` aadressidele (http.js), lingid ainult `poeHostid` peale (koond.js).
 */
import { core } from '$lib/server/andmed.js';

const VARSKE_MS = 6 * 3600 * 1000;
const MAX_VANUS_MS = 48 * 3600 * 1000;
const OOTA_VEA_JAREL_MS = 10 * 60 * 1000;

/** Sildi sisu (ka nimeruumiga, nt g:price, ja CDATA-ga), dekodeeritud. Esimene vaste. */
export function silt(s, ...nimed) {
	for (const t of nimed) {
		const m = new RegExp('<' + t + '(?:\\s[^>]*)?>(?:\\s*<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>\\s*)?</' + t + '>').exec(s);
		if (m) return dekodeeri(m[1]);
	}
	return '';
}
/** Kõik sama sildi esinemised (nt mitu g:product_detail plokki). */
export function sildid(s, t) {
	const out = [];
	const re = new RegExp('<' + t + '(?:\\s[^>]*)?>([\\s\\S]*?)</' + t + '>', 'g');
	let m;
	while ((m = re.exec(s))) out.push(m[1]);
	return out;
}
export function dekodeeri(v) {
	return String(v)
		.replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
		.replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(+d))
		.replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
		.trim();
}
/** „54.51“, „54,51“, „60.00 EUR“ → number */
export function arv(v) {
	const m = /-?\d+(?:[.,]\d+)?/.exec(String(v ?? '').replace(/\s/g, ''));
	return m ? Number(m[0].replace(',', '.')) : NaN;
}
/** „HANKOOK“ → „Hankook“ (sobitus võrdleb nagunii normaliseeritult) */
export const ilusMark = (m) => {
	const s = String(m || '').trim();
	return s && s === s.toUpperCase() ? s.charAt(0) + s.slice(1).toLowerCase() : s;
};

export function looVoopakkuja(o) {
	let indeks = null; // Map moot -> [toode]
	let laetud = 0;
	let laadib = null;
	let viimaneViga = null;
	const info = { ridu: 0, hoitud: 0, laetud: null, kestusMs: 0 };
	const algusSilt = '<' + o.element;
	const loppSilt = '</' + o.element + '>';

	async function laeKoik(pakkuja, { muutuja, voog }) {
		const aadress = (o.env && o.env[0] && muutuja(o.env[0])) || o.aadress;
		const algus = Date.now();
		const meieMoodud = new Set((core().eprelSizes || []).filter((m) => /^\d{5}R\d{2}C?$/.test(m)));
		const r = await voog(pakkuja, aadress, { maxBaite: 200_000_000, aegMs: 180_000 });
		const uus = new Map();
		let ridu = 0, hoitud = 0, jaak = '';
		const dek = new TextDecoder('utf-8');
		const lisa = (t) => {
			if (!t) return;
			hoitud++;
			const l = uus.get(t.moot);
			if (l) l.push(t);
			else uus.set(t.moot, [t]);
		};
		const tootle = (tekst) => {
			let i = 0;
			for (;;) {
				/* <item> või <item attr…>, aga mitte <items> */
				let a = tekst.indexOf(algusSilt, i);
				while (a >= 0 && !/[\s>]/.test(tekst.charAt(a + algusSilt.length))) a = tekst.indexOf(algusSilt, a + 1);
				if (a < 0) return tekst.slice(Math.max(i, tekst.length - 200));
				const b = tekst.indexOf(loppSilt, a);
				if (b < 0) return tekst.slice(a);
				ridu++;
				const t = o.teisenda(tekst.slice(tekst.indexOf('>', a) + 1, b), meieMoodud);
				if (Array.isArray(t)) t.forEach(lisa);
				else lisa(t);
				i = b + loppSilt.length;
			}
		};
		for await (const tykk of r.keha) jaak = tootle(jaak + dek.decode(tykk, { stream: true }));
		tootle(jaak + dek.decode());
		if (!ridu) throw new Error(`${o.id}: voos ei olnud ühtegi toodet`);
		if (!hoitud) throw new Error(`${o.id}: ${ridu} rida, aga ükski ei sobinud meie mõõtudega`);
		if (indeks && info.hoitud > 50 && hoitud < info.hoitud * 0.2)
			throw new Error(`${o.id}: ainult ${hoitud} sobivat toodet (enne ${info.hoitud}) — jätsin vana`);
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

	return {
		id: o.id,
		nimi: o.nimi,
		hostid: o.hostid,
		poeHostid: o.poeHostid,
		/* avalik voog vaikeaadressiga: sees ka ilma muutujata (env ainult üle kirjutamiseks) */
		env: [],
		ttlHinnad: 600,
		async soojenda(ctx) {
			await lae(this, ctx);
		},
		async hinnadMoodus(moot, ctx) {
			if (!indeks) await lae(this, ctx);
			else if (Date.now() - laetud > VARSKE_MS) lae(this, ctx).catch(() => {});
			if (Date.now() - laetud > MAX_VANUS_MS) throw new Error(`${o.id}: andmed üle 48 h vanad ja värskendus ei õnnestu`);
			return indeks.get(moot) || [];
		},
		/* kõik mõõdud mälust (pildikataloog: sama rehvi pilt teisest mõõdust) */
		koikMoodud() {
			return indeks ? [...indeks.entries()] : [];
		},
		lisaOlek() {
			return { ...info, viga: viimaneViga ? viimaneViga.teade : null, laadib: !!laadib };
		}
	};
}
