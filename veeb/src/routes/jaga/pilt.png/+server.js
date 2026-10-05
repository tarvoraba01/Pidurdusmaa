/* Jagatud tulemuse pilt (og:image) — joonistatakse käigu pealt, number
   arvutatakse serveris (lib/server/jaga.js), mitte ei võeta lingist. */
import { error } from '@sveltejs/kit';
import { loeValik, arvuta, jagaPilt } from '$lib/server/jaga.js';
import { mootoridJson } from '$lib/server/andmed.js';

export const prerender = false;
export const trailingSlash = 'never';

/* väike vahemälu: sama tulemus jagatakse tavaliselt mitu korda järjest */
const VAHE = new Map();
const MAX = 200;

export function GET({ url }) {
	const val = loeValik(url.searchParams);
	if (!val) error(404, 'Tulemust ei leitud');
	const voti = JSON.stringify(val);
	let png = VAHE.get(voti);
	if (!png) {
		const res = arvuta(val, val.a.includes('~') ? mootoridJson() : null);
		if (!res) error(404, 'Tulemust ei leitud');
		png = jagaPilt(res);
		if (VAHE.size >= MAX) VAHE.delete(VAHE.keys().next().value);
		VAHE.set(voti, png);
	}
	return new Response(png, {
		headers: { 'Content-Type': 'image/png', 'Cache-Control': 'public, max-age=86400' }
	});
}
