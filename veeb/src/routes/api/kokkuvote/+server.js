import { json, error } from '@sveltejs/kit';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

import { votiOnOige, piirang } from '$lib/server/integratsioonid/kaitse.js';

export const prerender = false;
/* API aadressid töötavad nii kaldkriipsuga kui ilma (lehtedel on alati kaldkriips) */
export const trailingSlash = 'ignore';

const DIR = process.env.LOG_DIR || join(process.cwd(), 'data');

/* Koondstatistika: mida lehel kõige rohkem tehti.
 *
 * Kaitstud võtmega (STATS_KEY, vähemalt 16 märki). Kui võtit seatud ei
 * ole, on otspunkt välja lülitatud — muidu näeks iga möödakäija, mida
 * külastajad teevad. Võti käib PÄISES, mitte aadressis (aadressid
 * satuvad logidesse ja brauseri ajalukku):
 *
 *   curl -H "Authorization: Bearer $STATS_KEY" "https://pidurdusmaa.ee/api/kokkuvote?paevi=7"
 */
export function GET(event) {
	const { url, request } = event;
	const key = process.env.STATS_KEY;
	if (!key) error(404, 'Statistika ei ole sisse lülitatud');
	if (!piirang('kokkuvote', event, 30, 60)) error(429, 'Liiga palju päringuid');
	if (!votiOnOige(request, key)) error(401, 'Vale võti');

	const paevi = Math.min(90, Math.max(1, +(url.searchParams.get('paevi') || 7)));
	const alates = Date.now() - paevi * 864e5;

	let read = [];
	try {
		read = readFileSync(join(DIR, 'logi.jsonl'), 'utf-8').trim().split('\n');
	} catch {
		return json({ ridu: 0, sessioone: 0, sundmused: {}, top: {} });
	}

	const sess = new Set();
	const sundmused = {};
	const vaartused = {};
	let ridu = 0;

	for (const rida of read) {
		let r;
		try {
			r = JSON.parse(rida);
		} catch {
			continue;
		}
		if (new Date(r.t).getTime() < alates) continue;
		ridu++;
		sess.add(r.k);
		sundmused[r.e] = (sundmused[r.e] || 0) + 1;
		if (r.v) {
			const m = (vaartused[r.e] = vaartused[r.e] || {});
			m[r.v] = (m[r.v] || 0) + 1;
		}
	}

	/* iga sündmuse 15 sagedasemat väärtust */
	const top = {};
	for (const [e, m] of Object.entries(vaartused)) {
		top[e] = Object.entries(m)
			.sort((a, b) => b[1] - a[1])
			.slice(0, 15);
	}

	return json({ paevi, ridu, sessioone: sess.size, sundmused, top });
}
