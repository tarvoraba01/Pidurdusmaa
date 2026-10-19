import { lamellJaotur } from '$lib/server/jaoturid.js';

/* /lamellrehvid/: testide parimad, mõõdud ja kõik Põhjamaade lamellrehvid margi kaupa (vt jaoturid.js) */
export function load() {
	return lamellJaotur();
}
