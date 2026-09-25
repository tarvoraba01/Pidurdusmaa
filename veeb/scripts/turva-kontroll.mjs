/* Turvakontroll pärast ehitust: kas midagi salajast on sattunud brauserisse
 * minevatesse failidesse (build/client)?
 *
 *  - serveri keskkonnamuutujate NIMED (SMTP_PASS, PAKKUJA_*_VOTI …) ei tohi
 *    brauseri koodis olla — kui on, loeb mingi brauseri kood saladust
 *  - tüüpilised võtmemustrid (sk_live_, AKIA…, "Bearer eyJ…")
 *  - kui muutujal on ehituse ajal väärtus, ei tohi see väärtus esineda
 * Leid → ehitus katkeb, lehele jääb vana versioon.
 *
 * NB: SvelteKit ise keelab juba $lib/server ja $env/dynamic/private importimise
 * brauseri koodis. See skript on teine lukk samale uksele.
 */
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const SALADUSED = [
	'SMTP_PASS', 'SMTP_USER', 'TURNSTILE_SECRET', 'STATS_KEY', 'ADMIN_KEY', 'TEADE_URL', 'IP_SALT'
];
const MUSTRID = [
	[/PAKKUJA_[A-Z0-9_]+_(VOTI|KEY|SECRET|PAROOL|TOKEN)/, 'pakkuja võtme muutuja nimi'],
	[/sk_live_[0-9a-zA-Z]{10,}/, 'Stripe live võti'],
	[/AKIA[0-9A-Z]{16}/, 'AWS võti'],
	[/Bearer\s+eyJ[0-9A-Za-z_-]{20,}/, 'JWT võti'],
	[/-----BEGIN [A-Z ]*PRIVATE KEY-----/, 'privaatvõti']
];

function* failid(dir) {
	for (const n of readdirSync(dir)) {
		const p = join(dir, n);
		if (statSync(p).isDirectory()) yield* failid(p);
		else if (/\.(js|mjs|html|json|css|map)$/.test(n)) yield p;
	}
}

const leiud = [];
const vaartused = SALADUSED.map((n) => [n, process.env[n]]).filter(([, v]) => v && v.length >= 8);
for (const f of failid('build/client')) {
	if (f.includes('/data/')) continue; // rehviandmed, suured ja ohutud
	const t = readFileSync(f, 'utf-8');
	for (const n of SALADUSED) if (new RegExp('\\b' + n + '\\b').test(t)) leiud.push(`${f}: muutuja nimi ${n}`);
	for (const [re, nimi] of MUSTRID) if (re.test(t)) leiud.push(`${f}: ${nimi}`);
	for (const [n, v] of vaartused) if (t.includes(v)) leiud.push(`${f}: muutuja ${n} VÄÄRTUS`);
}
if (leiud.length) {
	console.error('\nTURVAKONTROLL: brauseri failides on saladusi!\n' + leiud.slice(0, 20).join('\n'));
	process.exit(1);
}
console.log('Turvakontroll: brauseri failides saladusi ei ole.');
