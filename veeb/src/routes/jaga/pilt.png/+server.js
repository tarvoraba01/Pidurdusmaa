/* Jagatud tulemuse pilt (og:image) — joonistatakse käigu pealt, number
   arvutatakse serveris (lib/server/jaga.js), mitte ei võeta lingist. */
import { error } from '@sveltejs/kit';
import { loeValik, arvuta, jagaPilt } from '$lib/server/jaga.js';
import { mootoridJson } from '$lib/server/andmed.js';
import { piirang } from '$lib/server/integratsioonid/kaitse.js';

export const prerender = false;
export const trailingSlash = 'never';

/* väike vahemälu: sama tulemus jagatakse tavaliselt mitu korda järjest */
const VAHE = new Map();
const MAX = 200;

export function GET(event) {
	const { url } = event;
	const val = loeValik(url.searchParams);
	if (!val) error(404, 'Tulemust ei leitud');
	const voti = JSON.stringify(val);
	let png = VAHE.get(voti);
	if (!png) {
		/* uue pildi joonistamine on CPU-kallis: piirang ainult vahemälust mööda minnes */
		if (!piirang('jagapilt', event, 30, 60)) error(429, 'Liiga palju päringuid');
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
