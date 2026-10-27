/* MINURATTAD (minurattad.ee) — Google Merchant Center XML (Kaspar Karm 27.10.2026).
 *   https://minurattad.ee/feeds/GoogleMerchantCenter.xml   (avalik, võtit pole)
 *   Coolifys võib aadressi üle kirjutada: PAKKUJA_MINURATTAD_URL
 *
 * Kaspari kokkulepe (e-kirjad 26.–27.10):
 *   g:price  = MINIMAALSE ostukoguse koguhind (nt 2 × 30 € = 60 €)
 *   unit_price = 1 rehvi hind  → meie `hind` (alati 1 tk)
 *   quantity = laoseis tk, minimum_order_quantity = müük alates N tk, pieces_in_lot = komplekti suurus
 *   g:condition used/new; kasutatud rehvil g:product_detail: „Mustri sügavus“ (nt „5 mm“, „5–6 mm“), „DOT“
 *   link võib lõppeda #offer-123 → koond/app lisab UTM enne #-märki
 * Silte loetakse nii g:-eesliitega kui ilma (Kaspari lisaväljad võivad olla mõlemat moodi).
 */
import { normMoot } from '../sobitus.js';
import { looVoopakkuja, silt, sildid, arv, ilusMark } from '../voopakkuja.js';

const g = (s, ...n) => silt(s, ...n.flatMap((x) => ['g:' + x, x]));
const MOOT_RE = /(\d{3})\s*\/\s*(\d{2})\s*Z?R\s*F?\s*(\d{2})(\s*C\b)?/i;

/** product_detail plokid → { 'mustri sügavus': '5 mm', dot: '2421', … } */
function detailid(s) {
	const out = {};
	for (const p of sildid(s, 'g:product_detail').concat(sildid(s, 'product_detail'))) {
		const n = g(p, 'attribute_name').toLowerCase();
		if (n) out[n] = g(p, 'attribute_value');
	}
	return out;
}

/** Mudel pealkirjast: mark ette, mõõt ja kõik pärast seda ära, müra (kasutatud, talverehv, 4 tk) ära. */
export function mudelPealkirjast(pealkiri, mark) {
	let t = String(pealkiri || '');
	const m = MOOT_RE.exec(t);
	if (m) t = t.slice(0, m.index);
	if (mark) t = t.replace(new RegExp('(^|\\s)' + mark.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i'), ' ');
	t = t.replace(/\b(kasutatud|used|uus|new|komplekt|set|\d+\s*tk|suverehv(?:ad|id)?|talverehv(?:ad|id)?|lamellrehv(?:ad|id)?|naastrehv(?:ad|id)?|rehv(?:id)?|tyres?|tires?)\b/gi, ' ');
	return t.replace(/[,;|]+/g, ' ').replace(/\s+/g, ' ').trim();
}

export function teisenda(s, meieMoodud) {
	const pealkiri = g(s, 'title');
	const det = detailid(s);
	const mootTekst = g(s, 'size') || det['mõõt'] || det['size'] || det['rehvi mõõt'] || pealkiri;
	const mm = MOOT_RE.exec(mootTekst) || MOOT_RE.exec(pealkiri);
	if (!mm) return null;
	const moot = normMoot(mm[0]);
	if (!moot || (meieMoodud && !meieMoodud.has(moot))) return null;
	const mark = ilusMark(g(s, 'brand'));
	if (!mark) return null;
	const mudel = g(s, 'model', 'mpn_model') || det['mudel'] || det['model'] || mudelPealkirjast(pealkiri, g(s, 'brand'));
	if (!mudel) return null;

	const min = Math.floor(arv(g(s, 'minimum_order_quantity', 'min_order_quantity')));
	const komplekt = Math.floor(arv(g(s, 'pieces_in_lot')));
	const kogusRaw = arv(g(s, 'quantity'));
	let hind = arv(g(s, 'unit_price'));
	if (!(hind > 0)) {
		/* ühe rehvi hinda pole: g:price on min koguse koguhind → jagame */
		const kokku = arv(g(s, 'sale_price') || g(s, 'price'));
		const jaga = komplekt > 1 ? komplekt : min > 1 ? min : 1;
		hind = kokku / jaga;
	}
	hind = Math.round(hind * 100) / 100;
	if (!(hind > 5 && hind < 5000)) return null;

	const saad = g(s, 'availability');
	const laos = Number.isFinite(kogusRaw) ? kogusRaw > 0 : /in.?stock|laos/i.test(saad);
	const kasutatud = /used|kasutatud/i.test(g(s, 'condition')) || /\bkasutatud\b/i.test(pealkiri);
	const musterTekst = det['mustri sügavus'] || det['mustrisügavus'] || det['muster'] || det['tread depth'] || det['mustri sugavus'] || '';
	const muster = arv(musterTekst); /* „5–6 mm“ → 5 (väiksem, aus) */
	const url = g(s, 'link');
	const pilt = g(s, 'image_link');
	const gtin = g(s, 'gtin');
	return {
		mark,
		mudel,
		moot,
		hind,
		laos,
		...(Number.isFinite(kogusRaw) && kogusRaw >= 0 ? { kogus: Math.floor(kogusRaw) } : {}),
		...(min > 1 ? { min } : {}),
		...(komplekt > 1 ? { komplekt } : {}),
		...(kasutatud ? { kasutatud: true, ...(muster > 0 && muster < 15 ? { muster } : {}) } : {}),
		ean: /^\d{8,14}$/.test(gtin) ? gtin : undefined,
		pilt: !kasutatud && /^https:\/\//.test(pilt) ? pilt : undefined,
		url: /^https:\/\//.test(url) ? url : undefined,
		...(/naast|stud/i.test(pealkiri + ' ' + mudel) ? { naast: true } : {}),
		myyja: 'minurattad.ee'
	};
}

export default looVoopakkuja({
	id: 'minurattad',
	nimi: 'minurattad.ee',
	aadress: 'https://minurattad.ee/feeds/GoogleMerchantCenter.xml',
	env: ['PAKKUJA_MINURATTAD_URL'],
	hostid: ['minurattad.ee', 'www.minurattad.ee'],
	poeHostid: ['minurattad.ee', 'www.minurattad.ee'],
	element: 'item',
	teisenda
});
