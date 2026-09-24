import { json, error } from '@sveltejs/kit';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

export const prerender = false;

const DIR = process.env.LOG_DIR || join(process.cwd(), 'data');

/* Koondstatistika: mida lehel kõige rohkem tehti.
 *
 * Kaitstud võtmega (STATS_KEY). Kui võtit seatud ei ole, on otspunkt
 * välja lülitatud — muidu näeks iga möödakäija, mida külastajad teevad.
 *
 *   GET /api/kokkuvote?key=…&paevi=7
 */
export function GET({ url }) {
	const key = process.env.STATS_KEY;
	if (!key) error(404, 'Statistika ei ole sisse lülitatud');
	if (url.searchParams.get('key') !== key) error(401, 'Vale võti');

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
