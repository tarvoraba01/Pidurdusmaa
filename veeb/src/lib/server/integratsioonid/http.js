/* Turvaline väljaminev päring pakkuja API-sse.
 *
 * Kaitsed:
 *  - ainult pakkuja enda lubatud aadressid (provider.hostid). Kui keegi
 *    sokutab pakkuja vastusesse võõra pildi-URL-i (nt sisevõrgu aadressi),
 *    siis sinna meie server ei lähe (SSRF-kaitse).
 *  - ainult https (välja arvatud näidispakkuja kohalikus testis)
 *  - ajapiirang ja vastuse suuruse piir — aeglane või hiiglaslik vastus ei
 *    saa serverit kinni panna
 *  - ümbersuunamist järgitakse ainult lubatud aadressile
 *  - logidesse ei kirjutata kunagi päiseid ega URL-i päringuosa (seal
 *    võib olla võti)
 */

function lubatud(pakkuja, url) {
	let u;
	try {
		u = new URL(url);
	} catch {
		return false;
	}
	if (u.protocol !== 'https:' && !(pakkuja.lubaHttp && u.protocol === 'http:')) return false;
	if (u.username || u.password) return false;
	const host = u.host.toLowerCase();
	return (pakkuja.hostid || []).some((h) =>
		h.startsWith('*.') ? host.endsWith(h.slice(1)) : host === h.toLowerCase()
	);
}

const puhas = (url) => {
	try {
		const u = new URL(url);
		return u.origin + u.pathname;
	} catch {
		return '(vigane URL)';
	}
};

/**
 * @param {object} pakkuja
 * @param {string} url
 * @param {{ headers?: object, method?: string, body?: any, maxBaite?: number, aegMs?: number }} [o]
 * @returns {Promise<{ status: number, tyyp: string, andmed: Buffer }>}
 */
export async function paring(pakkuja, url, o = {}) {
	const maxBaite = o.maxBaite ?? 2_000_000;
	let siht = url;
	for (let hyppe = 0; hyppe < 3; hyppe++) {
		if (!lubatud(pakkuja, siht)) throw new Error(`${pakkuja.id}: aadress pole lubatud (${puhas(siht)})`);
		const r = await fetch(siht, {
			method: o.method || 'GET',
			headers: { 'User-Agent': 'Pidurdusmaa.ee/1.0 (+https://pidurdusmaa.ee/kontakt/)', ...(o.headers || {}) },
			body: o.body,
			redirect: 'manual',
			signal: AbortSignal.timeout(o.aegMs ?? 6000)
		});
		if (r.status >= 300 && r.status < 400 && r.headers.get('location')) {
			siht = new URL(r.headers.get('location'), siht).toString();
			continue;
		}
		const pikkus = +(r.headers.get('content-length') || 0);
		if (pikkus > maxBaite) throw new Error(`${pakkuja.id}: vastus liiga suur`);
		/* loeme tükkhaaval ja katkestame, kui piir ületatakse */
		const tykid = [];
		let kokku = 0;
		if (r.body) {
			for await (const t of r.body) {
				kokku += t.length;
				if (kokku > maxBaite) throw new Error(`${pakkuja.id}: vastus liiga suur`);
				tykid.push(t);
			}
		}
		return { status: r.status, tyyp: r.headers.get('content-type') || '', andmed: Buffer.concat(tykid) };
	}
	throw new Error(`${pakkuja.id}: liiga palju ümbersuunamisi`);
}

/** JSON-päring; viskab vea, kui vastus pole 2xx või pole JSON. */
export async function jsonParing(pakkuja, url, o = {}) {
	const r = await paring(pakkuja, url, o);
	if (r.status < 200 || r.status >= 300) throw new Error(`${pakkuja.id}: HTTP ${r.status} (${puhas(url)})`);
	try {
		return JSON.parse(r.andmed.toString('utf-8'));
	} catch {
		throw new Error(`${pakkuja.id}: vastus ei ole JSON`);
	}
}

export { lubatud };
