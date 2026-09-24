import { json } from '@sveltejs/kit';
import { lisaRida, ipHash, kasLubatud } from '$lib/server/logi.js';
import { saadaKiri } from '$lib/server/post.js';
import { kontrolliTurnstile } from '$lib/server/turnstile.js';

export const prerender = false;

const TEEMAD = {
	hinnad: 'Rehvimüüja — hinnad lehele',
	koostoo: 'Koostöö või reklaam',
	viga: 'Viga andmetes',
	ettepanek: 'Ettepanek või küsimus',
	muu: 'Muu'
};

/* Kontaktivorm. Kiri saadetakse SMTP kaudu, kui see on seadistatud;
   igal juhul kirjutatakse kiri ka faili, et ükski sõnum ei kaoks, kui
   postiserver parajasti ei tööta. */
export async function POST({ request, getClientAddress }) {
	const paljasIp = getClientAddress();
	const ip = ipHash(paljasIp);
	if (!kasLubatud('kontakt:' + ip, 5, 3600)) {
		return json({ ok: false, msg: 'Liiga palju kirju ühest kohast. Proovi tunni pärast.' }, { status: 429 });
	}

	let f;
	try {
		const ct = request.headers.get('content-type') || '';
		f = ct.includes('json')
			? await request.json()
			: Object.fromEntries(await request.formData());
	} catch {
		return json({ ok: false, msg: 'Vigane päring.' }, { status: 400 });
	}

	const v = (k) => String(f[k] ?? '').trim();

	/* Peidetud väli: inimene seda ei näe, robot täidab ära. */
	if (v('veeb')) return json({ ok: true });

	if (!v('nimi')) return json({ ok: false, msg: 'Palun kirjuta oma nimi.' }, { status: 400 });
	if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('email')))
		return json({ ok: false, msg: 'Palun kontrolli e-posti aadressi.' }, { status: 400 });
	if (v('sonum').length < 5)
		return json({ ok: false, msg: 'Palun kirjuta sõnum.' }, { status: 400 });

	/* Robotikontroll (Cloudflare Turnstile), kui see on sisse lülitatud */
	const tk = await kontrolliTurnstile(v('cf-turnstile-response'), paljasIp);
	if (!tk.ok) {
		return json(
			{ ok: false, msg: 'Robotikontroll ei läinud läbi. Oota, kuni vormi all on linnuke, ja proovi uuesti.' },
			{ status: 400 }
		);
	}

	const teema = TEEMAD[v('teema')] || TEEMAD.muu;
	const kiri = {
		aeg: new Date().toISOString(),
		teema,
		nimi: v('nimi').slice(0, 120),
		email: v('email').slice(0, 160),
		firma: v('firma').slice(0, 160),
		sonum: v('sonum').slice(0, 5000)
	};

	lisaRida('kontakt.jsonl', kiri);

	const saadetud = await saadaKiri({
		subject: `[Pidurdusmaa.ee] ${teema} — ${kiri.nimi}`,
		replyTo: kiri.email,
		text:
			`Teema: ${teema}\nNimi: ${kiri.nimi}\nE-post: ${kiri.email}` +
			(kiri.firma ? `\nEttevõte: ${kiri.firma}` : '') +
			`\n\n${kiri.sonum}\n`
	});

	/* Kiri on igal juhul failis, nii et kasutajale vastame ausalt „kohal“. */
	return json({ ok: true, mail: saadetud });
}
