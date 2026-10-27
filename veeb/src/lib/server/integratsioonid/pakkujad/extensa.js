/* EXTENSA (extensa.ee, Tartu) — oma tootevoog pidurdusmaa jaoks (Margus Meos 27.10.2026).
 *   https://www.extensa.ee/rehvid/feeds/pidurdusmaa.xml   (avalik, võtit pole)
 *   Coolifys võib aadressi üle kirjutada: PAKKUJA_EXTENSA_URL
 *
 * Kuju: <products generated_at="…"><product>
 *   <id>4871</id><brand>HANKOOK</brand><model>KINERGY ECO2 (K435)</model><size>155/80 R13</size>
 *   <price>54.51</price> (KOOS käibemaksuga, 1 tk) <currency>EUR</currency><stock>5</stock>
 *   <availability>…</availability><url>…</url><ean>…</ean><load_index>79</load_index>
 *   <speed_index>T</speed_index><delivery>1–2 tööpäeva</delivery>
 * Sulgudes tehasekood („(K435)“) eemaldab sobitus ise (mudeliSonad).
 */
import { normMoot } from '../sobitus.js';
import { looVoopakkuja, silt, arv, ilusMark } from '../voopakkuja.js';

export function teisenda(s, meieMoodud) {
	const moot = normMoot(silt(s, 'size'));
	if (!moot || (meieMoodud && !meieMoodud.has(moot))) return null;
	const valuuta = silt(s, 'currency');
	if (valuuta && valuuta.toUpperCase() !== 'EUR') return null;
	const hind = Math.round(arv(silt(s, 'price')) * 100) / 100;
	if (!(hind > 5 && hind < 5000)) return null;
	const mark = ilusMark(silt(s, 'brand'));
	const mudel = silt(s, 'model');
	if (!mark || !mudel) return null;
	const stock = arv(silt(s, 'stock'));
	const saad = silt(s, 'availability');
	const laos = Number.isFinite(stock) ? stock > 0 : /in.?stock|laos|olemas/i.test(saad);
	const url = silt(s, 'url');
	const ean = silt(s, 'ean');
	const li = silt(s, 'load_index'), si = silt(s, 'speed_index');
	return {
		mark,
		mudel,
		moot,
		hind,
		laos,
		...(Number.isFinite(stock) && stock >= 0 ? { kogus: Math.floor(stock) } : {}),
		lisi: li && si ? `${li}${si}` : undefined,
		ean: /^\d{8,14}$/.test(ean) ? ean : undefined,
		url: /^https:\/\//.test(url) ? url : undefined,
		...(/naast|stud/i.test(mudel) ? { naast: true } : {}),
		myyja: 'extensa.ee'
	};
}

export default looVoopakkuja({
	id: 'extensa',
	nimi: 'extensa.ee',
	aadress: 'https://www.extensa.ee/rehvid/feeds/pidurdusmaa.xml',
	env: ['PAKKUJA_EXTENSA_URL'],
	hostid: ['www.extensa.ee', 'extensa.ee'],
	poeHostid: ['www.extensa.ee', 'extensa.ee'],
	element: 'product',
	teisenda
});
