import { suviJaotur } from '$lib/server/jaoturid.js';

/* /suverehvid/: suvetestide parimad, märgise klassi mõju ja mõõdud (vt jaoturid.js) */
export function load() {
	return suviJaotur();
}
