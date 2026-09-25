/* Integratsioonide seaded: KÕIK salajased väärtused tulevad serveri
 * keskkonnamuutujatest (Coolify → Environment Variables). Mitte kunagi
 * koodist, GitHubist ega brauserist.
 *
 * $env/dynamic/private on SvelteKit'i "ainult serveris" moodul: kui keegi
 * proovib seda kasutada brauseri koodis, katkeb ehitus veaga. Sama kehtib
 * kogu kausta src/lib/server kohta — see kood ei jõua brauserisse kunagi.
 */
import { env } from '$env/dynamic/private';

/** Loe muutuja; tühi = puudub. */
export function muutuja(nimi) {
	const v = env[nimi];
	return v && String(v).trim() ? String(v).trim() : null;
}

/** Kas kõik nõutud muutujad on olemas? */
export function koikOlemas(nimed) {
	return nimed.every((n) => muutuja(n));
}

/* Sisemised otspunktid (olek, statistika) — eraldi võti. */
export const adminVoti = () => muutuja('ADMIN_KEY');
