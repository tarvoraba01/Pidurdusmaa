/* Rehvi vanuse ja reaktsioonitesti vaikeauto (VW Golf 8) + märgiseklasside tabel.
   Need lehed vajavad core.json-ist (700 KB) ainult seda, kui kasutaja pole oma autot
   valinud — siis laetakse see väike fail (audit 17.10). */
import { json } from '@sveltejs/kit';
import { core } from '$lib/server/andmed.js';

export const prerender = true;

export function GET() {
	const c = core();
	return json({ vehicles: c.vehicles.filter((v) => v.key === 'vw_golf_8'), gClass: c.gClass });
}
