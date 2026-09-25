import { core } from '$lib/server/andmed.js';

/* Näidete numbrid tulevad samast mudelist, mis kalkulaator (core.json → demo). */
export function load() {
	return { demo: core().demo || null };
}
