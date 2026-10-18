import { core, sizeModelCount, SIZE_MIN_MODELS } from '$lib/server/andmed.js';
import { kaasMoodud } from '$lib/server/autod.js';

/** Mõõdud, millel on oma leht (/rehvid/<mõõt>/) — kalkulaator soovitab sama läbimõõduga mõõte.
 *  kaas: levinumad põhimõõdud ja mõõdud, mis on samadel autodel ka tehasemõõt (staatiline tabel,
 *  mida otsingumootor näeb ilma JavaScriptita). */
export function load() {
	return {
		moodud: core()
			.sizes.filter((s) => /^\d{5}R\d{2}$/.test(s.m) && sizeModelCount(s.m) >= SIZE_MIN_MODELS)
			.map((s) => ({ m: s.m, label: s.label, slug: s.slug, n: s.n })),
		kaas: kaasMoodud(10, 3)
	};
}
