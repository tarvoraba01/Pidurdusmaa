/* Testide parimad alade kaupa (jää, lumi, märg asfalt) — testid_ext.json + core.json.
   Uus test (nt Tekniikan Maailma 2026), mille meetrid on avalikud, tuleb tabelisse ise. */
import { talveTestideParimad } from '$lib/server/andmed.js';

export function load() {
	return { testid: talveTestideParimad(2025) };
}
