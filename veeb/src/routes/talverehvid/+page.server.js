import { talveMoodud } from '$lib/server/talv.js';

export function load() {
	return { moodud: talveMoodud() };
}
