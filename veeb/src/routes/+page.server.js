import { core } from '$lib/server/andmed.js';

/** Avalehe numbrid (demo) tulevad ehituse ajal core.json-ist — samast
 *  mudelist, mis kalkulaator. Ei ühtki käsitsi kirjutatud arvu. */
export function load() {
	return { demo: core().demo || null };
}
