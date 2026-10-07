<script>
	/* Koolitus: eeltest → selgitused + „proovi simulaatoris“ → järeltest → tulemus enne/pärast.
	   Küsimused tulevad pangast (lib/koolitus/kysimused.js) juhuslikult; juba nähtud küsimused
	   jäävad tahaplaanile (meeles ainult selles brauseris). Autokooli kood tuleb aadressist
	   (?kood=VIIKING-7K3) ja läheb statistikasse koos vastustega — nime ei küsita. */
	import { onMount } from 'svelte';
	import { KYSIMUSED, TEEMAD } from '$lib/koolitus/kysimused.js';

	const NAHTUD_VOTI = 'pm-koolitus-nahtud';
	let olek = $state('algus'); /* algus | eel | selgitus | jarel | tulemus */
	let valitud = $state(TEEMAD.map((x) => x[0]));
	let kood = $state('');
	let eel = $state([]); /* [{ q, jarjestus, vastus }] */
	let jarel = $state([]);
	let i = $state(0);
	let ylal; /* kerime küsimuse vahetudes ploki algusse */

	onMount(() => {
		try {
			const k = new URLSearchParams(location.search).get('kood') || sessionStorage.getItem('pm-koolitus-kood') || '';
			kood = puhasKood(k);
			if (kood) sessionStorage.setItem('pm-koolitus-kood', kood);
			const t = new URLSearchParams(location.search).get('teemad');
			if (t) {
				const v = t.split(',').filter((x) => TEEMAD.some((y) => y[0] === x));
				if (v.length) valitud = v;
			}
		} catch {}
	});

	const puhasKood = (k) => String(k || '').toUpperCase().replace(/[^A-Z0-9-]/g, '').slice(0, 20);
	function track(e, v) {
		try { window.PM_TRACK && window.PM_TRACK(e, v); } catch {}
	}
	function nahtud() {
		try { return new Set(JSON.parse(localStorage.getItem(NAHTUD_VOTI) || '[]')); } catch { return new Set(); }
	}
	function margiNahtuks(ids) {
		try {
			const s = nahtud();
			ids.forEach((x) => s.add(x));
			localStorage.setItem(NAHTUD_VOTI, JSON.stringify([...s].slice(-400)));
		} catch {}
	}
	const sega = (a) => {
		const b = a.slice();
		for (let j = b.length - 1; j > 0; j--) { const r = Math.floor(Math.random() * (j + 1)); [b[j], b[r]] = [b[r], b[j]]; }
		return b;
	};

	/* Valik: teemad ringiratast (alustades `esimesed` teemadest), igast teemast eelistatud märgiga
	   ja nägemata küsimused ees. Vastused segatakse, et õige ei oleks alati samal kohal. */
	function vali(n, eelista, valja, esimesed = []) {
		const N = nahtud();
		const jarg = (q) => (eelista.some((m) => q.m.includes(m)) ? 0 : 2) + (N.has(q.id) ? 1 : 0);
		const pool = {};
		for (const t of valitud) {
			pool[t] = sega(KYSIMUSED.filter((q) => q.teema === t && !valja.has(q.id))).sort((a, b) => jarg(a) - jarg(b));
		}
		const jarjekord = [...esimesed.filter((t) => valitud.includes(t)), ...sega(valitud.filter((t) => !esimesed.includes(t)))];
		const out = [];
		while (out.length < n && jarjekord.some((t) => pool[t].length)) {
			for (const t of jarjekord) if (out.length < n && pool[t].length) out.push(pool[t].shift());
		}
		return out.map((q) => ({ q, jarjestus: sega([0, 1, 2, 3]), vastus: null }));
	}
	const mitu = () => Math.max(3, Math.min(10, Math.floor(KYSIMUSED.filter((q) => valitud.includes(q.teema)).length / 2)));

	function alusta() {
		eel = vali(mitu(), ['e'], new Set());
		i = 0;
		olek = 'eel';
		track('koolitus', 'algus · ' + valitud.length + ' teemat' + (kood ? ' · ' + kood : ''));
	}
	function vasta(rida, nr) {
		if (rida.vastus !== null) return;
		rida.vastus = nr;
		track('koolitus_vastus', [olek, rida.q.id, nr === rida.q.o ? 'õige' : 'vale', kood].filter(Boolean).join(' · '));
	}
	function edasi() {
		const list = olek === 'eel' ? eel : jarel;
		if (i < list.length - 1) { i++; kerI(); return; }
		margiNahtuks(list.map((r) => r.q.id));
		if (olek === 'eel') {
			track('koolitus', 'eel ' + skoor(eel) + '/' + eel.length + (kood ? ' · ' + kood : ''));
			olek = 'selgitus';
		} else {
			track('koolitus', 'jarel ' + skoor(jarel) + '/' + jarel.length + (kood ? ' · ' + kood : '') + ' · eel ' + skoor(eel));
			olek = 'tulemus';
		}
		kerI();
	}
	function jareltest() {
		/* järeltest: teised küsimused, kõigepealt teemad, kus eksisid */
		const valed = [...new Set(eel.filter((r) => r.vastus !== r.q.o).map((r) => r.q.teema))];
		jarel = vali(eel.length, ['j', 't'], new Set(eel.map((r) => r.q.id)), valed);
		i = 0;
		olek = 'jarel';
		kerI();
	}
	function uuesti() {
		olek = 'algus';
		eel = [];
		jarel = [];
		kerI();
	}
	function kerI() {
		requestAnimationFrame(() => ylal?.scrollIntoView({ block: 'start', behavior: 'smooth' }));
	}
	const skoor = (list) => list.filter((r) => r.vastus === r.q.o).length;
	const teemaNimi = (id) => (TEEMAD.find((x) => x[0] === id) || [, id])[1];
	const tahed = ['A', 'B', 'C', 'D'];
	function lulita(t) {
		valitud = valitud.includes(t) ? valitud.filter((x) => x !== t) : [...valitud, t];
	}

	let jagatud = $state('');
	async function jaga() {
		const tekst = `Pidurdusmaa koolitus: enne ${skoor(eel)}/${eel.length}, pärast ${skoor(jarel)}/${jarel.length}. Proovi ise:`;
		const url = location.origin + location.pathname + (kood ? '?kood=' + kood : '');
		try {
			if (navigator.share) { await navigator.share({ text: tekst, url }); track('koolitus', 'jaga'); return; }
			await navigator.clipboard.writeText(tekst + ' ' + url);
			jagatud = 'Link kopeeritud ✓';
			track('koolitus', 'jaga');
		} catch {}
	}

	/* simulaator hüpikaknas samal lehel (iframe, ?upotus=1 peidab päise ja jaluse) */
	let sim = $state(null); /* { nimi, url, k } */
	let simValmis = $state(false);
	function avaSim(q) {
		const [alus, rasi] = q.sim[1].split('#');
		sim = { nimi: q.sim[0], url: alus + (alus.includes('?') ? '&' : '?') + 'upotus=1' + (rasi ? '#' + rasi : ''), k: q.k };
		simValmis = false;
		setTimeout(() => (simValmis = true), 2500); /* varu, kui teadet ei tule */
		track('koolitus', 'simulaator · ' + q.id);
		try { document.documentElement.style.overflow = 'hidden'; } catch {}
	}
	function sulgeSim() {
		sim = null;
		try { document.documentElement.style.overflow = ''; } catch {}
	}
	onMount(() => {
		const teade = (e) => { if (e.origin === location.origin && e.data?.pm === 'upotus-valmis') simValmis = true; };
		const klahv = (e) => { if (e.key === 'Escape' && sim) sulgeSim(); };
		window.addEventListener('message', teade);
		window.addEventListener('keydown', klahv);
		return () => { window.removeEventListener('message', teade); window.removeEventListener('keydown', klahv); };
	});

	const rida = $derived(olek === 'eel' ? eel[i] : olek === 'jarel' ? jarel[i] : null);
	const list = $derived(olek === 'eel' ? eel : jarel);
</script>

<div class="kl" bind:this={ylal}>
	{#if kood}<p class="kl-kood">Grupp: <b>{kood}</b></p>{/if}

	{#if olek === 'algus'}
		<div class="kl-kaart">
			<h2>Test: arvamused ja tõed</h2>
			<ol class="kl-sammud">
				<li><b>Eeltest</b><span>{mitu()} küsimust. Vasta nii, nagu arvad.</span></li>
				<li><b>Vastused</b><span>Näed, mis oli õige ja miks. Proovi olukorda simulaatoris.</span></li>
				<li><b>Järeltest</b><span>{mitu()} uut küsimust. Vaata, kui palju juurde õppisid.</span></li>
			</ol>
			<fieldset class="kl-teemad">
				<legend>Teemad</legend>
				{#each TEEMAD as [id, nimi] (id)}
					<button type="button" aria-pressed={valitud.includes(id)} onclick={() => lulita(id)}>{nimi}</button>
				{/each}
			</fieldset>
			<button type="button" class="btn yel kl-suur" disabled={!valitud.length} onclick={alusta}>Alusta →</button>
			<p class="kl-vaike">Umbes 10 minutit. Nime ei küsita.</p>
		</div>
	{:else if (olek === 'eel' || olek === 'jarel') && rida}
		<div class="kl-kaart">
			<div class="kl-ylal">
				<span class="kl-etapp">{olek === 'eel' ? 'Eeltest' : 'Järeltest'} · {teemaNimi(rida.q.teema)}</span>
				<span class="kl-nr">{i + 1} / {list.length}</span>
			</div>
			<div class="kl-riba" aria-hidden="true"><i style="width:{((i + (rida.vastus !== null ? 1 : 0)) / list.length) * 100}%"></i></div>
			<h2 class="kl-k">{rida.q.k}</h2>
			<div class="kl-v" role="group" aria-label="Vastused">
				{#each rida.jarjestus as nr, j (nr)}
					<button type="button" aria-pressed={rida.vastus === nr} disabled={rida.vastus !== null && rida.vastus !== nr} onclick={() => vasta(rida, nr)}>
						<b>{tahed[j]}</b><span>{rida.q.v[nr]}</span>
					</button>
				{/each}
			</div>
			{#if olek === 'jarel' && rida.vastus !== null}
				<p class="kl-tagasi" class:hea={rida.vastus === rida.q.o}>
					<b>{rida.vastus === rida.q.o ? 'Õige.' : 'Õige oli: ' + rida.q.v[rida.q.o] + '.'}</b> {rida.q.s}
				</p>
			{/if}
			<div class="kl-nupud">
				<button type="button" class="btn yel" disabled={rida.vastus === null} onclick={edasi}>{i < list.length - 1 ? 'Edasi →' : olek === 'eel' ? 'Vaata vastuseid →' : 'Vaata tulemust →'}</button>
			</div>
		</div>
	{:else if olek === 'selgitus'}
		<div class="kl-kaart">
			<p class="kl-etapp">Eeltest</p>
			<h2>Õigesti {skoor(eel)} / {eel.length}</h2>
			<p class="kl-lead">{skoor(eel) === eel.length ? 'Kõik õiged. Järeltestis on küsimused trikkidega: loe täpselt.' : 'Vaata, kus eksisid, ja proovi seda olukorda simulaatoris. Siis järeltest uute küsimustega.'}</p>
		</div>
		<ol class="kl-selg">
			{#each eel as r (r.q.id)}
				<li class:vale={r.vastus !== r.q.o}>
					<p class="kl-sk">{r.q.k}</p>
					{#if r.vastus !== r.q.o}<p class="kl-sinu">Sinu vastus: {r.q.v[r.vastus]}</p>{/if}
					<p class="kl-oige"><b>{r.vastus === r.q.o ? '✓' : 'Õige:'}</b> {r.q.v[r.q.o]}</p>
					<p class="kl-ss">{r.q.s}</p>
					{#if r.q.sim}<button type="button" class="kl-sim" class:esile={r.vastus !== r.q.o} onclick={() => avaSim(r.q)}>Proovi simulaatoris: {r.q.sim[0]} →</button>{/if}
				</li>
			{/each}
		</ol>
		<div class="kl-kaart kl-keskel">
			<p class="kl-lead">Järeltestis on {eel.length} uut küsimust samadel teemadel. Kõigepealt need teemad, kus eksisid.</p>
			<button type="button" class="btn yel kl-suur" onclick={jareltest}>Järeltest →</button>
		</div>
	{:else if olek === 'tulemus'}
		<div class="kl-kaart kl-keskel">
			<p class="kl-etapp">Tulemus</p>
			<div class="kl-ep">
				<div><span>Enne</span><b>{skoor(eel)}/{eel.length}</b></div>
				<i aria-hidden="true">→</i>
				<div class:p={skoor(jarel) > skoor(eel)}><span>Pärast</span><b>{skoor(jarel)}/{jarel.length}</b></div>
			</div>
			<p class="kl-lead">{skoor(jarel) > skoor(eel) ? 'Teadmised kasvasid. Kõige rohkem jääb meelde see, mida simulaatoris ise proovisid.' : skoor(jarel) === jarel.length ? 'Kõik õiged, ka trikiküsimused.' : 'Järeltesti küsimused olid trikkidega. Proovi uuesti: tulevad teised küsimused.'}</p>
			<div class="kl-nupud kl-keskel">
				<button type="button" class="btn yel" onclick={jaga}>Jaga tulemust</button>
				<button type="button" class="btn" onclick={uuesti}>Proovi uuesti</button>
			</div>
			{#if jagatud}<p class="kl-vaike" role="status">{jagatud}</p>{/if}
		</div>
		{#if jarel.some((r) => r.vastus !== r.q.o)}
			<h3 class="kl-h3">Järeltestis eksisid</h3>
			<ol class="kl-selg">
				{#each jarel.filter((r) => r.vastus !== r.q.o) as r (r.q.id)}
					<li class="vale">
						<p class="kl-sk">{r.q.k}</p>
						<p class="kl-oige"><b>Õige:</b> {r.q.v[r.q.o]}</p>
						<p class="kl-ss">{r.q.s}</p>
						{#if r.q.sim}<button type="button" class="kl-sim esile" onclick={() => avaSim(r.q)}>Proovi simulaatoris: {r.q.sim[0]} →</button>{/if}
					</li>
				{/each}
			</ol>
		{/if}
	{/if}
</div>

{#if sim}
	<div class="kl-modal" role="dialog" aria-modal="true" aria-label={'Simulaator: ' + sim.nimi}>
		<button type="button" class="kl-modal-taust" aria-label="Sulge" onclick={sulgeSim}></button>
		<div class="kl-modal-aken">
			<div class="kl-modal-pea">
				<div><b>{sim.nimi}</b><span>{sim.k}</span></div>
				<button type="button" class="kl-x" onclick={sulgeSim} aria-label="Sulge">×</button>
			</div>
			<div class="kl-modal-sisu">
				{#if !simValmis}<p class="kl-laeb">Laen simulaatorit…</p>{/if}
				<iframe src={sim.url} title={'Simulaator: ' + sim.nimi} class:peidus={!simValmis} allow="fullscreen"></iframe>
			</div>
			<div class="kl-modal-jalus"><button type="button" class="btn yel" onclick={sulgeSim}>Tagasi testi juurde</button></div>
		</div>
	</div>
{/if}


<style>
	.kl { max-width: 760px; margin: 0 auto; scroll-margin-top: 90px; }
	.kl-kood { margin: 0 0 var(--sp-3); font-size: 14px; color: var(--muted); }
	.kl-kood b { color: var(--text); letter-spacing: 0.04em; }
	.kl-kaart { background: #fff; border: 1px solid var(--line); border-radius: 16px; padding: var(--sp-6); margin-bottom: var(--sp-4); }
	.kl-kaart h2 { font-family: var(--display); font-size: 30px; line-height: 1.05; margin: 0 0 var(--sp-3); }
	.kl-lead { font-size: 16px; color: var(--muted); margin: 0 0 var(--sp-4); }
	.kl-sammud { list-style: none; counter-reset: s; padding: 0; margin: 0 0 var(--sp-5); display: grid; gap: var(--sp-3); }
	.kl-sammud li { counter-increment: s; display: grid; grid-template-columns: 34px 1fr; column-gap: var(--sp-3); align-items: start; }
	.kl-sammud li::before { content: counter(s); grid-row: span 2; width: 34px; height: 34px; border-radius: 50%; background: var(--yellow); color: var(--ink); font-weight: 800; display: grid; place-items: center; }
	.kl-sammud b { font-size: 17px; line-height: 1.3; }
	.kl-sammud span { color: var(--muted); font-size: 15px; }
	.kl-vaike { font-size: 13px; color: var(--muted); margin: var(--sp-3) 0 0; }
	.kl-keskel { text-align: center; }
	.kl-keskel.kl-nupud { justify-content: center; }
	.kl-suur { font-size: 17px; padding: 14px 28px; }
	.kl-teemad { border: 0; padding: 0; margin: 0 0 var(--sp-5); display: flex; flex-wrap: wrap; gap: var(--sp-2); }
	.kl-teemad legend { font-weight: 700; margin-bottom: var(--sp-2); }
	.kl-teemad button { border: 1px solid var(--line); background: #fff; border-radius: 999px; padding: 7px 14px; font: inherit; font-size: 14px; font-weight: 600; cursor: pointer; }
	.kl-teemad button[aria-pressed='true'] { background: var(--ink); color: #fff; border-color: var(--ink); }
	.kl-ylal { display: flex; justify-content: space-between; gap: var(--sp-3); font-size: 13px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
	.kl-etapp { font-size: 13px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; margin: 0 0 var(--sp-2); }
	.kl-riba { height: 4px; background: #eef0f3; border-radius: 4px; margin: var(--sp-2) 0 var(--sp-5); overflow: hidden; }
	.kl-riba i { display: block; height: 100%; background: var(--yellow); transition: width 0.25s; }
	.kl-k { font-family: inherit !important; font-size: 21px !important; font-weight: 700; line-height: 1.3 !important; }
	.kl-v { display: grid; gap: var(--sp-2); margin: var(--sp-4) 0; }
	.kl-v button { display: flex; gap: var(--sp-3); align-items: flex-start; text-align: left; width: 100%; border: 1.5px solid var(--line); background: #fff; border-radius: 12px; padding: 13px 16px; font: inherit; font-size: 16px; cursor: pointer; color: var(--text); }
	.kl-v button b { flex: 0 0 auto; width: 26px; height: 26px; border-radius: 50%; background: #eef0f3; display: grid; place-items: center; font-size: 13px; }
	.kl-v button:hover:not(:disabled) { border-color: var(--ink); }
	.kl-v button[aria-pressed='true'] { border-color: var(--ink); background: #fffbea; }
	.kl-v button[aria-pressed='true'] b { background: var(--yellow); }
	.kl-v button:disabled { opacity: 0.5; cursor: default; }
	.kl-tagasi { border-left: 4px solid #d9661a; background: #fff6ef; padding: 12px 14px; border-radius: 8px; margin: 0 0 var(--sp-4); }
	.kl-tagasi.hea { border-color: #1f9d55; background: #f0faf4; }
	.kl-nupud { display: flex; gap: var(--sp-2); flex-wrap: wrap; }
	.kl-selg { list-style: none; padding: 0; margin: 0 0 var(--sp-4); display: grid; gap: var(--sp-3); counter-reset: s; }
	.kl-selg li { background: #fff; border: 1px solid var(--line); border-left: 4px solid #1f9d55; border-radius: 12px; padding: var(--sp-4) var(--sp-5); }
	.kl-selg li.vale { border-left-color: #d9661a; }
	.kl-selg p { margin: 0 0 6px; }
	.kl-sk { font-weight: 700; }
	.kl-sinu { color: #b4471a; font-size: 15px; }
	.kl-oige { font-size: 15px; }
	.kl-ss { color: var(--muted); font-size: 15px; }
	.kl-sim { display: inline-block; margin-top: 4px; font: inherit; font-weight: 700; font-size: 14px; background: none; border: 0; padding: 0; color: var(--link, #1a56db); text-decoration: underline; cursor: pointer; }
	.kl-sim.esile { text-decoration: none; }
	.kl-modal { position: fixed; inset: 0; z-index: 1000; display: grid; place-items: center; padding: 16px; }
	.kl-modal-taust { position: absolute; inset: 0; background: rgba(10, 11, 13, 0.6); border: 0; cursor: pointer; }
	.kl-modal-aken { position: relative; width: min(1100px, 100%); height: min(92vh, 980px); background: #f4f5f7; border-radius: 16px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 24px 60px rgba(0, 0, 0, 0.4); }
	.kl-modal-pea { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 16px; background: var(--ink); color: #fff; }
	.kl-modal-pea div { display: grid; min-width: 0; }
	.kl-modal-pea b { font-family: var(--display); font-size: 20px; text-transform: uppercase; letter-spacing: 0.02em; }
	.kl-modal-pea span { font-size: 13px; color: #cfd4db; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.kl-x { flex: 0 0 auto; width: 40px; height: 40px; border-radius: 50%; border: 0; background: rgba(255, 255, 255, 0.12); color: #fff; font-size: 26px; line-height: 1; cursor: pointer; }
	.kl-modal-sisu { position: relative; flex: 1 1 auto; min-height: 0; }
	.kl-modal-sisu iframe { width: 100%; height: 100%; border: 0; display: block; background: #f4f5f7; }
	.kl-modal-sisu iframe.peidus { visibility: hidden; }
	.kl-laeb { position: absolute; inset: 0; display: grid; place-items: center; margin: 0; color: var(--muted); }
	.kl-modal-jalus { padding: 10px 16px; background: #fff; border-top: 1px solid var(--line); display: flex; justify-content: flex-end; }
	@media (max-width: 600px) { .kl-modal { padding: 0; } .kl-modal-aken { height: 100%; border-radius: 0; } }
	.kl-sim.esile { background: var(--yellow); color: var(--ink); padding: 8px 14px; border-radius: 999px; text-decoration: none; }
	.kl-ep { display: flex; align-items: center; justify-content: center; gap: var(--sp-5); margin: var(--sp-3) 0 var(--sp-4); }
	.kl-ep div { display: grid; gap: 2px; }
	.kl-ep span { font-size: 13px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
	.kl-ep b { font-family: var(--display); font-size: 56px; line-height: 1; }
	.kl-ep .p b { color: #1f9d55; }
	.kl-ep i { font-style: normal; font-size: 30px; color: var(--muted); }
	.kl-h3 { margin: var(--sp-6) 0 var(--sp-3); }
	@media (max-width: 600px) {
		.kl-kaart { padding: var(--sp-5) var(--sp-4); }
		.kl-k { font-size: 19px !important; }
		.kl-ep b { font-size: 46px; }
	}
</style>
