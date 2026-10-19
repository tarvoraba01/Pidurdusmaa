import { naastJaotur } from '$lib/server/jaoturid.js';

/* /naastrehvid/: testide parimad, mõõdud ja kõik naastrehvid margi kaupa (vt jaoturid.js) */
export function load() {
	return naastJaotur();
}
