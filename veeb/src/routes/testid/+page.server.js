import { core } from '$lib/server/andmed.js';

/** /testid/ — sõltumatud testid, mille tulemusi mudel kasutab. */
export function load() {
	return {
		sources: Object.entries(core().sources).map(([code, s]) => ({ ...s, slug: code.toLowerCase() }))
	};
}
