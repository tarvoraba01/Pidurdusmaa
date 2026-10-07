<script>
	/* MÄNG „Kui kiiresti SINA pidurdad?“ (suur plaan faas 2).
	   Pseudo-3D tee ($lib/tee3d.js): mets või küla, kurvid, päev/öö, kuiv/vihm/talv.
	   Kaks olukorda, sama füüsika mis kalkulaatoris (engine.js pidurdusjälg):
	    - EESOLEV AUTO: pidurdab (süttivad pidurituled), sina sõidad sama autoga
	      valitud pikivahega järel. Hiline vajutus = kokkupõrge.
	    - JALAKÄIJA PIMEDAS: astub puu / pargitud auto tagant teele riietusest
	      sõltuval kaugusel (Transpordiamet 2025: tumedad 30 m, heledad 45 m,
	      helkur 140 m).
	   Iga katse on juhuslik: tee, kurvid, maastik, öö/päev (eesoleva auto puhul).
	   Reaktsioon = täpselt mõõdetud aeg (midagi juurde ei lisata).
	   Isikuandmeid ei koguta; link ?r=ms. */
	import { onMount, onDestroy } from 'svelte';
	import { version } from '$app/environment';
	import { useT, useLang } from '$lib/i18n.js';
	import { looTee, lisaVarjaja, joonista, TEE } from '$lib/tee3d.js';
	const t = useT();
	const keel = useLang();

	const KATSEID = 3;
	const NAHT = [
		['tume', 30, t('Tumedad riided')],
		['hele', 45, t('Heledad riided')],
		['helkur', 140, t('Helkuriga')]
	];
	const ILM = [
		['kuiv', t('Kuiv'), { surface: 'ASPHALT', waterMm: 0, tempC: 15 }, 'SUMMER_TOURING'],
		['vihm', t('Vihm'), { surface: 'ASPHALT', waterMm: 1, tempC: 10 }, 'SUMMER_TOURING'],
		['talv', t('Talv'), { surface: 'SNOW_PACKED', waterMm: 0, tempC: -5 }, 'WINTER_NORDIC']
	];

	let P = null, core = null;
	let veh = $state(null);
	let reziim = $state('tuled'); /* tuled | pime */
	let kiirus = $state(90);
	let vahe = $state(1);
	let riie = $state('tume');
	let ilm = $state('vihm');
	let muster = $state(8); /* sinu rehvide muster tulemuse võrdluses; eesoleval autol jäävad uued */
	let olek = $state('algus'); /* algus | oota | nyyd | soit | vara | vahe | tulemus */
	let ajad = $state([]);
	let tulemused = $state([]);
	let sobra = $state(0);
	let jagatud = $state('');
	let crash = $state(false);
	let taisekraan = $state(false); /* mäng üle kogu ekraani */
	let kaart = $state(false); /* tulemuse + jagamise kaart mänguekraanil */
	let ekraan;

	/* stseen (ei ole $state: joonistatakse igal kaadril canvas'ele) */
	let cv, ctx, W = 800, H = 500, raf = 0, taimer = 0;
	let tee = looTee({ maastik: 'mets', seed: 7 });
	let oo = false, z = 0, kmhNaha = 0, ees = null, jk = null, aeg0 = performance?.now?.() || 0;
	let zOoteAlgus = 0, tOoteAlgus = 0, zBase = 0, t0 = 0, tVajutus = null, D = 0, jkPool = 1, zOht = 0, tOht = 0;

	onMount(async () => {
		try {
			const q = new URLSearchParams(location.search);
			const r = +q.get('r');
			if (r >= 100 && r <= 3000) sobra = Math.round(r);
			/* simulaatorilt tulles (?m=pime | ?m=tuled) õige režiim */
			if (q.get('m') === 'pime' || q.get('m') === 'tuled') { reziim = q.get('m'); kiirus = reziim === 'pime' ? 50 : 90; }
		} catch {}
		ctx = cv.getContext('2d');
		suurus();
		window.addEventListener('resize', suurus);
		document.addEventListener('fullscreenchange', fsMuutus); document.addEventListener('webkitfullscreenchange', fsMuutus);
		raf = requestAnimationFrame(kaader);
		await import('$lib/engine.js');
		P = globalThis.Pidurdus;
		core = await (await fetch('/data/core.json?v=' + encodeURIComponent(version))).json();
		let key = null;
		try { key = JSON.parse(sessionStorage.getItem('pm_veh') || 'null'); } catch {}
		const byKey = (k) => core.vehicles.find((v) => v.key === k);
		veh = (key && byKey(String(key).split('~')[0])) || byKey('vw_golf_8');
		uusStseen();
	});
	onDestroy(() => {
		if (typeof window === 'undefined') return;
		clearTimeout(taimer); cancelAnimationFrame(raf); window.removeEventListener('resize', suurus);
		document.removeEventListener('fullscreenchange', fsMuutus); document.removeEventListener('webkitfullscreenchange', fsMuutus);
		try { document.documentElement.style.overflow = ''; } catch {}
	});
	let viimaneLaius = 0, viimaneKorgus = 0;
	function suurus() {
		if (!cv) return;
		const dpr = Math.min(2, window.devicePixelRatio || 1), w = cv.clientWidth || 800;
		const h = taisekraan ? cv.clientHeight || w * 0.62 : w * 0.62;
		/* telefonis kerimine muudab akna kõrgust (aadressiriba): siis ei joonista ümber */
		if (Math.abs(w - viimaneLaius) < 2 && Math.abs(h - viimaneKorgus) < 2) return;
		viimaneLaius = w; viimaneKorgus = h;
		W = Math.round(w * dpr); H = Math.round(h * dpr);
		cv.width = W; cv.height = H;
	}

	/* ---------- füüsika: pidurdus ajas samast mootorist ---------- */
	const ilmRida = () => ILM.find((x) => x[0] === ilm);
	function jalg(kmh, mm = 8) {
		const [, , c, kat] = ilmRida();
		const tyre = { key: 'x', name: 'x', category: kat, wetGripIndex: core.gClass?.C?.[kat]?.[0] || 1.32, treadDepthMm: mm, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: false, size: veh.oemSize, gSource: 'label' };
		const r = P.stoppingDistance(tyre, veh, { speedKmh: kmh, texture: 'NORMAL', payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1, ...c });
		const tr = r.trace;
		const vAt = (s) => {
			for (let i = 1; i < tr.length; i++) if (tr[i][0] >= s) { const a = tr[i - 1], b = tr[i], k = (s - a[0]) / Math.max(1e-9, b[0] - a[0]); return (a[1] + k * (b[1] - a[1])) / 3.6; }
			return 0;
		};
		const T = [], dt = 0.01;
		let s = 0, v = kmh / 3.6, tt = 0;
		while (v > 0.05 && tt < 30) { T.push([tt, s, v]); s += v * dt; tt += dt; v = vAt(s); }
		T.push([tt, r.distanceM, 0]);
		return { T, d: r.distanceM };
	}
	const pidurdusAjal = (J, tau) => { if (tau <= 0) return [0, J.T[0][2]]; const i = Math.min(J.T.length - 1, Math.floor(tau / 0.01)); return [J.T[i][1], J.T[i][2]]; };
	let J = null, M = null; /* J = uued rehvid (eesolev auto), M = sinu auto valitud mustriga */
	function sina(tt, r, v0, Jx = M) { if (r == null || tt < r) return [v0 * tt, v0]; const x = pidurdusAjal(Jx, tt - r); return [v0 * r + x[0], x[1]]; }
	const kaugus = () => NAHT.find((x) => x[0] === riie)[1];
	/* Jx = sinu auto pidurdus (vaikimisi valitud mustriga); eesolev auto pidurdab alati uute rehvidega (J) */
	function lopp(r, Jx = M) {
		const v0 = kiirus / 3.6;
		if (reziim === 'pime') {
			const Dk = D || kaugus(), vaja = v0 * r + Jx.d; /* sama nähtavuskaugus mis katses */
			if (vaja <= Dk) return { crash: false, m: Dk - vaja };
			let kmh = v0 * 3.6;
			if (v0 * r < Dk) { const rest = Dk - v0 * r; const p = Jx.T.find((x) => x[1] >= rest); kmh = p ? p[2] * 3.6 : 0; }
			return { crash: true, kmh };
		}
		const g0 = v0 * vahe;
		for (let tt = 0; tt < 40; tt += 0.005) {
			const pe = pidurdusAjal(J, tt), ee = g0 + pe[0], vE = pe[1];
			const [s, v] = sina(tt, r, v0, Jx);
			if (ee - s <= 0) return { crash: true, kmh: Math.max(0, v - vE) * 3.6 };
			if (v <= 0.05 && vE <= 0.05) return { crash: false, m: ee - s };
		}
		return { crash: false, m: 0 };
	}

	/* ---------- stseen: iga katse uus juhuslik tee ---------- */
	function uusStseen() {
		const seed = Math.floor(Math.random() * 1e9);
		const maastik = Math.random() < 0.5 ? 'mets' : 'kula';
		tee = looTee({ maastik, seed });
		oo = reziim === 'pime' ? true : Math.random() < 0.4;
		z = 0; kmhNaha = kiirus; crash = false; jk = null; zOht = 0;
		ees = reziim === 'tuled' ? { gap: (kiirus / 3.6) * vahe, pidur: false } : null;
	}
	function kaader(now) {
		raf = requestAnimationFrame(kaader);
		if (!ctx) return;
		const v0 = kiirus / 3.6;
		if (olek === 'oota') {
			z = zOoteAlgus + v0 * Math.max(0, (now - tOoteAlgus) / 1000); kmhNaha = kiirus;
			if (ees) ees = { gap: v0 * vahe, pidur: false };
			/* enne ohuhetke jalakäijat ei joonistata: ta on varjaja taga (muidu paistsid jalad ja „Liiga vara!“) */
			if (reziim === 'pime') jk = null;
		} else if (olek === 'nyyd' || olek === 'soit') {
			samm(now);
		} else if (olek === 'algus') {
			z += v0 * 0.016 * 0.5; kmhNaha = kiirus; /* aeglane eelvaade */
		}
		joonista(ctx, W, H, tee, { z, kmh: kmhNaha, oo, ilm, ees, jk, crash, aeg: (now - aeg0) / 1000 });
	}
	/* reaalajas pärast ohtu: kokkupõrge võib tulla enne vajutust */
	function samm(now) {
		const tt = Math.max(0, (now - t0) / 1000), v0 = kiirus / 3.6, r = tVajutus;
		const [s, v] = sina(tt, r, v0);
		z = zBase + s; kmhNaha = v * 3.6;
		let gap, vE = 0;
		if (reziim === 'tuled') { const p = pidurdusAjal(J, tt); vE = p[1]; gap = v0 * vahe + p[0] - s; ees = { gap: Math.max(0, gap), pidur: true }; }
		else {
			gap = D - s;
			jk = { z: zBase + D, x: jkX(tt), riie, kond: jkX(tt) === jkX(tt + 0.05) ? 0 : tt * 7 };
		}
		if (gap <= 0.01) { crash = true; lopeta(r == null ? tt : r, { crash: true, kmh: Math.max(0, v - vE) * 3.6 }); return; }
		if (r != null && v <= 0.05 && vE <= 0.05) { lopeta(r, { crash: false, m: gap }); return; }
		if (tt > 40) lopeta(r ?? tt, lopp(r ?? tt));
	}

	/* JALAKÄIJA: seisab varjaja (puu / pargitud auto) taga, astub t0 hetkel tee
	   servale (nähtavale) ja kõnnib sinu rajale nii, et jõuab sinna hiljemalt siis,
	   kui sina täiskiirusel tema juurde jõuaksid; seal ehmatab ja jääb seisma.
	   Vasakult tulles ületab ta vastassuuna raja. */
	const RAJA_X = TEE.KAAM_X, KOND = 1.4;
	/* Ohuhetkel (t0) astub jalakäija varjaja (pargitud auto / kuusk) tee poolse
	   serva tagant välja: tema algkoht arvutatakse nii, et kaamerast vaadates on
	   ta täpselt varjaja serva kõrval — enne t0 teda ei joonistata, pärast t0 on
	   ta kohe nähtav (reaktsiooniaeg ei sisalda „varjatud“ aega). */
	let jkAlg = 0, jkDz = 3;
	function varjajaServ() {
		const kula = tee.maastik === 'kula';
		const X = kula ? TEE.TEE_L + 1.3 : TEE.TEE_L + 2.6, pool = kula ? 0.9 : 11 * 0.38 / 2;
		return jkPool * (X - pool - 0.25);
	}
	function arvutaAlg(Dn) {
		const e = varjajaServ();
		return RAJA_X + (e - RAJA_X) * (Dn / Math.max(1, Dn - jkDz));
	}
	function jkX(tt, Dn = D) {
		const Tk = Math.max(0.3, Dn / (kiirus / 3.6));
		const vahe = RAJA_X - jkAlg;
		const vk = Math.min(4.5, Math.max(KOND, Math.abs(vahe) / Tk));
		return jkAlg + Math.sign(vahe) * Math.min(Math.abs(vahe), vk * Math.max(0, tt));
	}

	/* ---------- täisekraan: päris täisekraan, kus brauser lubab (iPhone'is mitte) — muidu kogu akna peale ---------- */
	function taisEkraan() {
		if (taisekraan) { valjuTais(); return; }
		taisekraan = true; track('taisekraan');
		try { document.documentElement.style.overflow = 'hidden'; } catch {}
		try { const r = ekraan.requestFullscreen || ekraan.webkitRequestFullscreen; r && r.call(ekraan)?.catch?.(() => {}); } catch {}
		setTimeout(() => { viimaneLaius = 0; suurus(); ekraan?.querySelector('.rk-ala')?.focus(); }, 60);
	}
	function valjuTais() {
		taisekraan = false;
		try { document.documentElement.style.overflow = ''; } catch {}
		try { const fe = document.fullscreenElement || document.webkitFullscreenElement; if (fe) (document.exitFullscreen || document.webkitExitFullscreen).call(document); } catch {}
		setTimeout(() => { viimaneLaius = 0; suurus(); }, 60);
	}
	function fsMuutus() { if (taisekraan && !(document.fullscreenElement || document.webkitFullscreenElement) && natiivne) valjuTais(); natiivne = !!(document.fullscreenElement || document.webkitFullscreenElement); }
	let natiivne = false;

	/* ---------- mänguvoog ---------- */
	function alusta() {
		clearTimeout(taimer);
		uusStseen();
		J = jalg(kiirus);
		M = muster < 8 ? jalg(kiirus, muster) : J;
		tVajutus = null;
		const viide = 2000 + Math.random() * 3500, v0 = kiirus / 3.6;
		zOoteAlgus = z; tOoteAlgus = performance.now();
		if (reziim === 'pime') {
			/* jalakäija ja tema varjaja (puu / pargitud auto) ette */
			/* nähtavus kõigub: tee kõverus, valgus, riiete toon — ±20% (Transpordiameti keskmise ümber) */
			D = Math.round(kaugus() * (0.85 + Math.random() * 0.4));
			/* vasakult ainult siis, kui ta jõuab terve raja ületada (≤ 4,5 m/s) */
			zOht = zOoteAlgus + v0 * (viide / 1000) + D; tOht = tOoteAlgus + viide;
			const nV = Math.floor((zOht - 1.5) / TEE.SEG);
			jkDz = zOht - nV * TEE.SEG;
			/* vasakult ainult siis, kui ta jõuab terve tee ületada (≤ 4,5 m/s) */
			jkPool = -1; const vasak = Math.abs(RAJA_X - arvutaAlg(D)) / (D / v0) <= 4.5;
			jkPool = Math.random() < 0.5 && vasak ? -1 : 1;
			jkAlg = arvutaAlg(D);
			lisaVarjaja(tee, nV, jkPool);
		} else zOht = 0;
		olek = 'oota';
		taimer = setTimeout(() => {
			t0 = performance.now(); zBase = z; tVajutus = null;
			if (reziim === 'pime') { D = zOht - zBase; jkAlg = arvutaAlg(D); } /* täpselt seal, kus ta varjaja taga on */
			if (reziim === 'tuled') ees = { gap: v0 * vahe, pidur: true };
			olek = 'nyyd';
		}, viide);
	}
	function lopeta(r, res) {
		const rec = { r, ...res, vajutamata: tVajutus == null };
		tulemused = [...tulemused, rec];
		if (!rec.vajutamata) ajad = [...ajad, Math.round(r * 1000)];
		track(reziim, ilm + ' · ' + (res.crash ? 'kokkupõrge ' + Math.round(res.kmh) + ' km/h' : 'peatus ' + Math.round(res.m) + ' m') + ' · ' + Math.round(r * 1000) + ' ms');
		olek = reziim === 'pime' || tulemused.length >= KATSEID ? 'tulemus' : 'vahe';
		/* kokkupõrke raputus jõuab enne lõpuni, siis tuleb kaart */
		if (olek === 'tulemus') tulemusAeg = performance.now();
		if (olek === 'tulemus') setTimeout(() => { if (olek === 'tulemus') { kaart = true; jagatud = ''; } }, res.crash ? 900 : 500);
	}
	function vajuta() {
		if (!veh || !P) return;
		if (olek === 'algus' || olek === 'vahe' || olek === 'vara') { if (olek === 'algus') { tulemused = []; ajad = []; track('algus', reziim); } alusta(); return; }
		if (olek === 'oota') { clearTimeout(taimer); olek = 'vara'; return; }
		if (olek === 'nyyd') { if (tVajutus == null) { tVajutus = (performance.now() - t0) / 1000; olek = 'soit'; } return; }
		/* kohe pärast viimast katset ei alusta uut (kiire topeltpuudutus kustutaks tulemused) */
		if (olek === 'tulemus') { if (kaart || performance.now() - tulemusAeg < 1200) return; tulemused = []; ajad = []; jagatud = ''; alusta(); }
	}
	const kaib = $derived(olek === 'oota' || olek === 'nyyd' || olek === 'soit');
	function lahtesta() { kaart = false; olek = 'algus'; tulemused = []; ajad = []; if (core) uusStseen(); }
	function vaheta(r) { if (kaib) return; reziim = r; kiirus = r === 'pime' ? 50 : 90; lahtesta(); }
	function seadista(f) { if (kaib) return; f(); lahtesta(); }
	function juhuslik() {
		if (kaib) return;
		const vali = (a) => a[Math.floor(Math.random() * a.length)];
		ilm = vali(['kuiv', 'vihm', 'talv']);
		if (reziim === 'pime') { kiirus = vali([30, 50, 50, 70, 90, 110]); riie = vali(['tume', 'tume', 'hele', 'helkur']); }
		else { kiirus = vali([50, 70, 90, 90, 110, 130]); vahe = vali([0.5, 1, 1, 2]); }
		lahtesta();
	}
	function klahv(e) {
		if (e.key === 'Escape') { if (kaart) { kaart = false; return; } if (taisekraan && !natiivne) valjuTais(); return; }
		if ((e.code === 'Space' || e.key === 'Enter') && document.activeElement?.closest?.('.rk-ala')) { e.preventDefault(); vajuta(); }
	}
	const mediaan = (a) => { const s = [...a].sort((x, y) => x - y), m = Math.floor(s.length / 2); return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2); };
	const tulemusMs = $derived(ajad.length ? mediaan(ajad) : 0);
	const viimane = $derived(tulemused.length ? tulemused[tulemused.length - 1] : null);
	function track(e, v) { try { window.PM_TRACK && window.PM_TRACK('mang', e + (v ? ' · ' + v : '')); } catch {} }

	const read = $derived.by(() => {
		if (!tulemused.length || kaib || !veh || !P) return [];
		void [kiirus, vahe, riie, reziim, ilm, muster];
		J = jalg(kiirus);
		M = muster < 8 ? jalg(kiirus, muster) : J;
		const sinu = tulemusMs ? tulemusMs / 1000 : null;
		return [
			...(sinu ? [[t('Sina'), sinu, lopp(sinu), true]] : []),
			...(sinu && M !== J ? [[t('Sina, uute rehvidega'), sinu, lopp(sinu, J), false]] : []),
			[t('Tavaline juht liikluses'), 1, lopp(1), false],
			[t('Tähelepanu mujal, nt telefon'), 2, lopp(2), false]
		];
	});

	/* kaardil ja pildil: mediaanreaktsiooni tulemus (mitte viimane katse), sama mis tabelis „Sina“ */
	const kaardiTul = $derived(read.length && read[0][3] ? read[0][2] : viimane);
	const LOC = keel.lang === 'en' ? 'en-GB' : keel.lang === 'ru' ? 'ru-RU' : 'et-EE';
	const f1 = (x) => x.toLocaleString(LOC, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
	const f2 = (ms) => (ms / 1000).toLocaleString(LOC, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
	let tulemusAeg = 0;
	const lause = (x) => (x.crash ? t('Kokkupõrge') + ' ' + Math.round(x.kmh) + ' ' + t('km/h') : (x.m < 0.1 ? t('Peatud viimasel hetkel, vahet alla 10 cm') : t('Peatud {m} m enne takistust', { m: f1(x.m) })));
	const ilmNimi = $derived(ILM.find((x) => x[0] === ilm)[1]);

	/* ---------- jagamine ---------- */
	function link() { return location.origin + keel.L('/liiklusohutus/reaktsioon/') + (tulemusMs ? '?r=' + tulemusMs : ''); }
	function ring(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
	async function pilt() {
		try { await Promise.all([document.fonts.load('700 100px "Barlow Condensed"'), document.fonts.load('700 40px Inter')]); } catch {}
		const c = document.createElement('canvas'); c.width = 1080; c.height = 1920;
		const g = c.getContext('2d'), DF = '"Barlow Condensed", "Arial Narrow", sans-serif', B = 'Inter, system-ui, sans-serif';
		g.fillStyle = '#0a0b0d'; g.fillRect(0, 0, 1080, 1920);
		/* mängu kaader pildi ülaossa */
		const kh = Math.min(700, Math.round(1080 * (cv.height / cv.width))), sh = Math.round(cv.width * kh / 1080);
		try { g.drawImage(cv, 0, Math.max(0, (cv.height - sh) / 2), cv.width, Math.min(sh, cv.height), 0, 230, 1080, kh); } catch {}
		const yy = 230 + kh + 90;
		g.fillStyle = '#fff'; g.font = 'italic 800 64px ' + B; g.fillText('PIDURDUSMAA', 90, 150); const w = g.measureText('PIDURDUSMAA').width; g.fillStyle = '#ffc20e'; g.fillText('.ee', 90 + w, 150);
		g.fillStyle = '#ffc20e'; g.font = '700 40px ' + B; g.fillText((t('Minu reaktsioon') + ' · ' + ilmNimi + ' · ' + kiirus + ' ' + t('km/h')).toUpperCase(), 90, yy);
		const tx = tulemusMs ? f2(tulemusMs) : '—';
		g.fillStyle = '#ffc20e'; g.font = '700 220px ' + DF; g.fillText(tx, 80, yy + 210); const w2 = g.measureText(tx).width; g.fillStyle = '#fff'; g.font = '700 90px ' + DF; g.fillText(' s', 80 + w2, yy + 210);
		if (kaardiTul) { g.fillStyle = kaardiTul.crash ? '#ff5a5a' : '#4ade80'; g.font = '700 54px ' + B; g.fillText(lause(kaardiTul), 90, yy + 300); }
		let y = yy + 400;
		read.slice(1).forEach(([n, s, r]) => {
			g.font = '500 34px ' + B; g.fillStyle = '#aab1bc'; g.fillText(n + ' (' + f2(s * 1000) + ' s): ', 90, y);
			const wn = g.measureText(n + ' (' + f2(s * 1000) + ' s): ').width;
			g.fillStyle = r.crash ? '#ff5a5a' : '#4ade80'; g.font = '700 34px ' + B; g.fillText(lause(r), 90 + wn, y);
			y += 60;
		});
		y = 1640; g.fillStyle = '#16181d'; ring(g, 90, y, 900, 200, 28); g.fill(); g.strokeStyle = '#2b3039'; g.lineWidth = 2; g.stroke();
		g.fillStyle = '#fff'; g.font = '700 54px ' + B; g.fillText(t('Kas sina oled kiirem?'), 130, y + 85);
		g.fillStyle = '#ffc20e'; g.font = '700 64px ' + DF; g.fillText('pidurdusmaa.ee', 130, y + 160);
		return new Promise((ok) => c.toBlob(ok, 'image/png'));
	}
	async function jaga() {
		const l = link();
		try { navigator.clipboard.writeText(l); } catch {}
		const blob = await pilt();
		let fail = null;
		try { fail = new File([blob], 'pidurdusmaa-reaktsioon.png', { type: 'image/png' }); } catch {}
		if (fail && navigator.canShare && navigator.canShare({ files: [fail] })) {
			try { await navigator.share({ files: [fail] }); } catch {}
			jagatud = t('Link on kopeeritud. Storys lisa kleebis „Link“ ja kleebi — sõbrad saavad proovida.');
			track('jaga', 'story');
		} else {
			const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'pidurdusmaa-reaktsioon.png'; a.click();
			jagatud = t('Pilt laaditi alla ja link on kopeeritud. Lisa pilt storysse ja kleebi link kleebisega „Link“.');
			track('jaga', 'arvutis');
		}
	}
	/* saada sõbrale: telefonis jagamismenüü (Messenger, WhatsApp…), muidu link lõikelauale */
	/* saada sõbrale: telefonis süsteemi jagamismenüü (Messenger, WhatsApp…);
	   arvutis on see menüü (AirDrop, Mail…) kasutu — näitame otse Facebooki ja WhatsAppi */
	let valikud = $state(false);
	const puutekas = () => { try { return matchMedia('(pointer: coarse)').matches; } catch { return false; } };
	const jagaTekst = () => (tulemusMs ? t('Minu reaktsioon') + ' ' + f2(tulemusMs) + ' s. ' : '') + t('Kas sina oled kiirem?');
	async function saada() {
		const l = link();
		if (navigator.share && puutekas()) { try { await navigator.share({ title: t('Kui kiiresti SINA pidurdad?'), text: jagaTekst(), url: l }); track('jaga', 'sobrale'); return; } catch (e) { if (e && e.name === 'AbortError') return; } }
		valikud = !valikud;
	}

	function kopeeri() { try { navigator.clipboard.writeText(link()); jagatud = t('Link kopeeritud ✓'); track('jaga', 'link'); } catch {} }
</script>

<svelte:window onkeydown={klahv} />

<div class="rk">
	<div class="rk-rezh" role="tablist" aria-label={t('Olukord')}>
		<button type="button" role="tab" aria-selected={reziim === 'tuled'} disabled={kaib} onclick={() => vaheta('tuled')}>{t('Eesolev auto pidurdab')}</button>
		<button type="button" role="tab" aria-selected={reziim === 'pime'} disabled={kaib} onclick={() => vaheta('pime')}>{t('Jalakäija pimedas')}</button>
	</div>

	<div class="rk-seaded">
		<label class="rk-kiirus">
			<span>{t('Kiirus')} <b>{kiirus} {t('km/h')}</b></span>
			<input type="range" min="30" max="150" step="10" bind:value={kiirus} disabled={kaib} onchange={() => lahtesta()} aria-label={t('Kiirus')} />
		</label>
		{#if reziim === 'tuled'}
			<div class="rk-seg" role="group" aria-label={t('Pikivahe')}>
				{#each [0.5, 1, 2] as k (k)}<button type="button" disabled={kaib} aria-pressed={vahe === k} onclick={() => seadista(() => (vahe = k))}>{t('vahe')} {f1(k)} s</button>{/each}
			</div>
		{:else}
			<div class="rk-seg" role="group" aria-label={t('Jalakäija')}>
				{#each NAHT as [k, , n] (k)}<button type="button" disabled={kaib} aria-pressed={riie === k} onclick={() => seadista(() => (riie = k))}>{n}</button>{/each}
			</div>
		{/if}
		<div class="rk-seg" role="group" aria-label={t('Ilm')}>
			{#each ILM as [k, n] (k)}<button type="button" disabled={kaib} aria-pressed={ilm === k} onclick={() => seadista(() => (ilm = k))}>{n}</button>{/each}
		</div>
		<label class="rk-kiirus rk-mliug">
			<span>{t('Rehvi muster')} <b>{muster >= 8 ? t('uus') + ' 8' : (+muster).toFixed(1).replace('.', ',')} {t('mm')}</b></span>
			<input type="range" min="0.5" max="8" step="0.1" bind:value={muster} disabled={kaib} onchange={() => track('muster', String(muster))} aria-label={t('Sinu rehvide muster')} />
		</label>
		<button type="button" class="rk-juh" disabled={kaib} onclick={juhuslik}>{t('Juhuslik olukord')}</button>
	</div>

	{#if sobra && olek === 'algus'}
		<p class="rk-sober">{t('Sõbra reaktsioon:')} <b>{f2(sobra)} s</b>. {t('Kas oled kiirem?')}</p>
	{/if}

	<div class="rk-ekraan" class:tais={taisekraan} bind:this={ekraan}>
	<button type="button" class="rk-ala" class:crash onpointerdown={(e) => { e.preventDefault(); vajuta(); }} aria-live="polite">
		<canvas bind:this={cv} class="rk-cv" aria-hidden="true"></canvas>
		<span class="rk-tekst">
			{#if olek === 'algus'}<b>{t('Vajuta, et alustada')}</b><small>{reziim === 'pime' ? t('Sõidad pimedas. Kui näed teel jalakäijat, vajuta kohe.') : t('Kui eesoleva auto pidurituled süttivad, vajuta kohe.')} {t('Arvutis ka tühikuklahv.')}</small>
			{:else if olek === 'oota' || olek === 'nyyd'}<b>{t('Sõidad…')}</b><small>{reziim === 'pime' ? t('Vaata teed') : t('Jälgi eesolevat autot')}</small><!-- sama tekst ka ohuhetkel: muutuv tekst reedaks hetke -->
			{:else if olek === 'soit'}<b>&nbsp;</b><small>&nbsp;</small>
			{:else if olek === 'vara'}<b>{t('Liiga vara!')}</b><small>{t('Vajuta uuesti, et seda katset korrata')}</small>
			{:else if viimane}<b class:punane={viimane.crash} class:roheline={!viimane.crash}>{lause(viimane)}</b><small>{viimane.vajutamata ? t('Ei vajutanud') : t('Reaktsioon') + ' ' + f2(viimane.r * 1000) + ' s'}{olek === 'vahe' ? ' · ' + t('Katse nr') + ' ' + tulemused.length + ' / ' + KATSEID + ' · ' + t('vajuta, et jätkata') : ' · ' + t('Vajuta, et uuesti proovida')}</small>{/if}
		</span>
		{#if reziim === 'tuled'}<span class="rk-pallid" aria-hidden="true">{#each Array(KATSEID) as _, i}<i class:on={i < tulemused.length} class:cr={tulemused[i]?.crash}></i>{/each}</span>{/if}
	</button>
	<button type="button" class="rk-fs" onclick={taisEkraan} aria-label={taisekraan ? t('Välju täisekraanist') : t('Täisekraan')} title={taisekraan ? t('Välju täisekraanist') : t('Täisekraan')}>
		{#if taisekraan}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5"/></svg>
		{:else}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>{/if}
	</button>

	{#if kaart && olek === 'tulemus' && viimane}
		<div class="rk-kaart" role="dialog" aria-modal="false" aria-label={t('Jaga tulemust')}>
			<div class="rk-kaart-sisu">
				<button type="button" class="rk-x" onclick={() => (kaart = false)} aria-label={t('Sulge')}>×</button>
				{#if tulemusMs}<p class="rk-k-pea">{reziim === 'tuled' ? t('Sinu reaktsioon (3 katse mediaan)') : t('Sinu reaktsioon')}</p><p class="rk-k-aeg">{f2(tulemusMs)} <small>s</small></p>{/if}
				<p class="rk-k-lause" class:punane={kaardiTul.crash}>{lause(kaardiTul)}</p>
				{#if sobra && tulemusMs}<p class="rk-k-sober">{tulemusMs < sobra ? t('Sõbrast kiirem!') : tulemusMs > sobra ? t('Sõber oli kiirem') + ' (' + f2(sobra) + ' s)' : t('Täpselt sama kiire kui sõber!')}</p>{/if}
				<div class="rk-jaga">
					<button type="button" class="btn yel" onclick={jaga}>{t('Jaga storysse')}</button>
					<button type="button" class="btn" onclick={saada}>{t('Saada sõbrale')}</button>
					<button type="button" class="btn" onclick={kopeeri}>{t('Kopeeri link')}</button>
				</div>
				{#if valikud}
					<div class="rk-valik">
						<a href={'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(link())} target="_blank" rel="noopener" onclick={() => track('jaga', 'facebook')}>Facebook</a>
						<a href={'https://wa.me/?text=' + encodeURIComponent(jagaTekst() + ' ' + link())} target="_blank" rel="noopener" onclick={() => track('jaga', 'whatsapp')}>WhatsApp</a>
					</div>
				{/if}
				{#if jagatud}<p class="rk-k-s" role="status">{jagatud}</p>{/if}
				<button type="button" class="rk-uuesti" onclick={() => { kaart = false; vajuta(); }}>{t('Proovi uuesti')}</button>
			</div>
		</div>
	{/if}
	</div>

	{#if olek === 'tulemus' && read.length}
		<div class="rk-tul">
			{#if tulemusMs}<p class="rk-suur">{reziim === 'tuled' ? t('Sinu reaktsioon (3 katse mediaan)') : t('Sinu reaktsioon')}: <b>{f2(tulemusMs)} s</b>{#if sobra}{' · ' + (tulemusMs < sobra ? t('Sõbrast kiirem!') : tulemusMs > sobra ? t('Sõber oli kiirem') + ' (' + f2(sobra) + ' s)' : t('Täpselt sama kiire kui sõber!'))}{/if}</p>{/if}
			<p class="rk-pea">{t('Sama olukord, erinev reaktsioon')} · {ilmNimi} · {kiirus} {t('km/h')}{reziim === 'pime' && D ? ' · ' + t('jalakäija nähtav') + ' ' + Math.round(D) + ' ' + t('m') : ''}{muster < 8 ? ' · ' + t('Rehvi muster {mm} mm', { mm: (+muster).toFixed(1).replace('.', ',') }).toLowerCase() : ''} · {veh.name}</p>
			<ol class="rk-read">
				{#each read as [nimi, s, r, me] (nimi)}
					<li class:me><span class="n">{nimi} <small>{f2(s * 1000)} s</small></span><span class="o" class:punane={r.crash}>{lause(r)}</span></li>
				{/each}
			</ol>
			<label class="rk-kiirus rk-mliug">
				<span>{t('Rehvi muster')} <b>{muster >= 8 ? t('uus') + ' 8' : (+muster).toFixed(1).replace('.', ',')} {t('mm')}</b></span>
				<input type="range" min="0.5" max="8" step="0.1" bind:value={muster} onchange={() => track('muster', String(muster))} aria-label={t('Sinu rehvide muster')} />
			</label>
			<p class="rk-sel">{t('Testis sa tead, et takistus tuleb. Liikluses mitte — seal on reaktsioon tavaliselt pikem.')}<br />{ilm === 'talv' ? t('Talvel lamellrehvid, tallatud lumi.') : (muster < 8 ? t('Keskmised suverehvid.') : t('Uued keskmised suverehvid.'))} {reziim === 'tuled' ? t('Eesoleval autol on alati uued rehvid.') + ' ' : ''}{t('Sama arvutus, mis kalkulaatoris.')}{#if reziim === 'tuled'}<br />{t('Kui eesolev auto pidurdab sama hästi kui sina, ei muuda ilm tulemust: otsustavad pikivahe ja reaktsioon. Kui tal on paremad rehvid või ta sõidab millelegi otsa, peatub ta kiiremini kui sina, ja libedal teel on see vahe suurem.')}{/if}</p>
			<div class="rk-nupud">
				<button type="button" class="btn yel" onclick={() => { kaart = true; jagatud = ''; ekraan?.scrollIntoView({ block: 'center', behavior: 'smooth' }); }}>{t('Jaga tulemust')}</button>
				<a class="btn" href={keel.L('/')}>{t('Arvuta oma auto ja rehvidega')}</a>
				<a class="btn" href={keel.L(reziim === 'pime' ? '/liiklusohutus/pimedas/' : '/liiklusohutus/pikivahe/')}>{reziim === 'pime' ? t('Nähtavus pimedas: simulaator') : t('Pikivahe: simulaator')} →</a>
			</div>
		</div>
	{/if}
</div>

<style>
	.rk { max-width: 860px; margin: 0 auto; padding: var(--sp-6) 0 var(--sp-10); }
	.rk-rezh { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-1); background: #fff; border: 1px solid var(--line); padding: var(--sp-1); border-radius: 12px; }
	.rk-rezh button { border: 0; background: transparent; padding: var(--sp-3); border-radius: 9px; font-weight: 700; font-size: 15px; color: var(--muted); cursor: pointer; }
	.rk-rezh button[aria-selected='true'] { background: var(--ink); color: #fff; box-shadow: inset 0 -3px 0 var(--yellow); }
	.rk-seaded { display: flex; flex-wrap: wrap; gap: var(--sp-2); margin: var(--sp-3) 0; align-items: center; }
	.rk-seg { display: flex; flex-wrap: wrap; gap: var(--sp-1); background: #fff; border: 1px solid var(--line); padding: var(--sp-1); border-radius: 10px; }
	.rk-seg button { border: 0; background: transparent; padding: 6px 10px; border-radius: 7px; font-weight: 600; font-size: 13.5px; color: var(--muted); cursor: pointer; }
	.rk-seg button[aria-pressed='true'] { background: var(--paper-2); color: var(--text); box-shadow: inset 0 -2px 0 var(--yellow); }
	.rk-tul .rk-mliug { margin-top: var(--sp-3); }
	.rk-kiirus { display: flex; align-items: center; gap: var(--sp-3); background: #fff; border: 1px solid var(--line); padding: 6px 12px; border-radius: 10px; font-size: 13.5px; color: var(--muted); font-weight: 600; flex: 1 1 260px; }
	.rk-kiirus b { color: var(--text); font-family: var(--display); font-size: 18px; min-width: 76px; display: inline-block; }
	.rk-kiirus input { flex: 1; accent-color: var(--ink); min-width: 120px; }
	.rk-juh { border: 1px dashed var(--line); background: #fff; border-radius: 10px; padding: 9px 12px; font-weight: 700; font-size: 13.5px; cursor: pointer; color: var(--text); }
	.rk-juh:hover { border-color: var(--yellow); }
	.rk-rezh button:disabled, .rk-seg button:disabled, .rk-juh:disabled { cursor: default; opacity: 0.6; }
	.rk-sober { background: #fff; border: 1px solid var(--line); border-radius: var(--r); padding: var(--sp-3) var(--sp-4); margin: 0 0 var(--sp-3); text-align: center; }
	.rk-ala { width: 100%; border: 0; border-radius: var(--r-lg, 16px); background: var(--ink); color: #fff; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: var(--sp-2); padding: 0 0 var(--sp-5); overflow: hidden; touch-action: manipulation; user-select: none; -webkit-user-select: none; font: inherit; }
	.rk-ala:focus-visible { outline: 3px solid var(--yellow); outline-offset: 3px; }
	.rk-ala.crash { animation: raputa 0.45s; }
	@keyframes raputa { 15% { transform: translate(-8px, 4px); } 35% { transform: translate(7px, -4px); } 55% { transform: translate(-5px, 2px); } 75% { transform: translate(3px, 0); } }
	.rk-cv { width: 100%; aspect-ratio: 1 / 0.62; display: block; background: #0a0b0d; }
	.rk-tekst { display: flex; flex-direction: column; justify-content: center; gap: 6px; text-align: center; padding: 0 var(--sp-4); height: 96px; overflow: hidden; }
	.rk-tekst b { font-family: var(--display); font-size: 34px; letter-spacing: 0.02em; text-transform: uppercase; line-height: 1; }
	.rk-tekst b.punane, .rk-tekst b.roheline { text-transform: none; font-size: 32px; }
	.rk-tekst b.punane { color: #ff5a5a; }
	.rk-tekst b.roheline { color: #4ade80; }
	.rk-tekst small { color: var(--muted-d); font-size: 14.5px; max-width: 520px; }
	.rk-pallid { display: flex; gap: 8px; }
	.rk-pallid i { width: 10px; height: 10px; border-radius: 50%; background: #2b3039; }
	.rk-pallid i.on { background: #4ade80; }
	.rk-pallid i.cr { background: #ff5a5a; }
	.rk-tul { background: #fff; border: 1px solid var(--line); border-radius: var(--r-lg, 16px); padding: var(--sp-5); margin-top: var(--sp-4); }
	.rk-suur { margin: 0 0 var(--sp-2); font-size: 17px; }
	.rk-pea { margin: var(--sp-3) 0 var(--sp-2); font-weight: 700; }
	.rk-read { list-style: none; margin: 0; padding: 0; display: grid; gap: var(--sp-2); }
	.rk-read li { display: flex; justify-content: space-between; gap: var(--sp-3); padding: var(--sp-2) var(--sp-3); background: var(--paper-2); border-radius: 8px; align-items: baseline; }
	.rk-read .n { font-size: 14.5px; color: var(--muted); }
	.rk-read .n small { font-size: 12.5px; margin-left: 4px; }
	.rk-read .me .n { color: var(--text); font-weight: 700; }
	.rk-read .o { font-weight: 800; color: #15803d; text-align: right; }
	.rk-read .o.punane { color: var(--red); }
	.rk-sel { font-size: 13px; color: var(--muted); margin: var(--sp-3) 0 0; line-height: 1.45; }
	.rk-ekraan { position: relative; }
	.rk-fs { position: absolute; top: 10px; right: 10px; width: 40px; height: 40px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.18); background: rgba(10,11,13,0.55); color: #fff; display: grid; place-items: center; cursor: pointer; padding: 0; z-index: 2; }
	.rk-fs:hover { background: rgba(10,11,13,0.8); }
	.rk-fs svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
	.rk-ekraan.tais { position: fixed; inset: 0; z-index: 1000; background: #0a0b0d; display: flex; flex-direction: column; padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left); }
	.rk-ekraan.tais .rk-ala { flex: 1 1 auto; min-height: 0; border-radius: 0; padding-bottom: var(--sp-3); }
	.rk-ekraan.tais .rk-cv { flex: 1 1 auto; min-height: 0; aspect-ratio: auto; height: 100%; }
	.rk-ekraan.tais .rk-fs { top: calc(10px + env(safe-area-inset-top)); right: calc(10px + env(safe-area-inset-right)); }
	.rk-kaart { position: absolute; inset: 0; z-index: 3; display: grid; place-items: center; padding: var(--sp-3); background: rgba(5,6,8,0.55); border-radius: var(--r-lg, 16px); animation: kaartSisse 0.25s ease-out; }
	.rk-ekraan.tais .rk-kaart { border-radius: 0; }
	/* täisekraanil tekst pildi peale (üles, taeva kohale), et pilt saaks kogu kõrguse */
	.rk-ekraan.tais .rk-ala { position: relative; padding-bottom: 0; }
	.rk-ekraan.tais .rk-tekst { position: absolute; left: 0; right: 0; top: 0; height: auto; padding: calc(14px + env(safe-area-inset-top)) 70px 34px; background: linear-gradient(rgba(0, 0, 0, 0.62), rgba(0, 0, 0, 0)); pointer-events: none; }
	.rk-ekraan.tais .rk-tekst b { font-size: 28px; }
	.rk-ekraan.tais .rk-tekst small { color: #e3e6ea; }
	.rk-ekraan.tais .rk-pallid { position: absolute; left: calc(16px + env(safe-area-inset-left)); top: calc(18px + env(safe-area-inset-top)); pointer-events: none; }
	@keyframes kaartSisse { from { opacity: 0; transform: translateY(8px); } }
	.rk-kaart-sisu { position: relative; width: 100%; max-width: 440px; max-height: 100%; overflow: auto; background: #16181d; color: #fff; border: 1px solid #2b3039; border-radius: 16px; padding: var(--sp-5) var(--sp-4) var(--sp-4); text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
	.rk-x { position: absolute; top: 6px; right: 6px; width: 40px; height: 40px; border: 0; background: transparent; color: #aab1bc; font-size: 28px; line-height: 1; cursor: pointer; border-radius: 10px; }
	.rk-x:hover { color: #fff; background: #23262d; }
	.rk-k-pea { margin: 0; padding: 0 36px; color: #ffc20e; font-weight: 700; font-size: 13px; letter-spacing: 0.04em; text-transform: uppercase; }
	.rk-k-aeg { margin: 2px 0 0; font-family: var(--display); font-size: 64px; font-weight: 700; line-height: 1; color: #ffc20e; }
	.rk-k-aeg small { font-size: 28px; color: #fff; }
	.rk-k-lause { margin: var(--sp-2) 0 0; font-weight: 800; font-size: 18px; color: #4ade80; }
	.rk-k-lause.punane { color: #ff5a5a; }
	.rk-k-sober { margin: 4px 0 0; color: #d6dae1; font-size: 14.5px; }
	.rk-k-s { font-size: 13px; color: #aab1bc; margin: var(--sp-2) 0 0; line-height: 1.4; }
	.rk-jaga { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-2); margin-top: var(--sp-4); }
	.rk-jaga .btn { text-align: center; justify-content: center; }
	.rk-jaga .yel { grid-column: 1 / -1; }
	.rk-kaart .rk-jaga .btn:not(.yel) { background: #23262d; color: #fff; border-color: #343944; }
	.rk-valik { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-2); margin-top: var(--sp-2); }
	.rk-valik a { text-align: center; padding: 10px 6px; border-radius: 10px; background: #23262d; border: 1px solid #343944; color: #fff; text-decoration: none; font-weight: 700; font-size: 14px; }
	.rk-valik a:hover { border-color: #ffc20e; }
	.rk-uuesti { margin-top: var(--sp-3); border: 0; background: transparent; color: #aab1bc; font-weight: 700; font-size: 14px; cursor: pointer; text-decoration: underline; text-underline-offset: 3px; padding: 8px; }
	.rk-uuesti:hover { color: #fff; }
	.rk-nupud { display: flex; flex-wrap: wrap; gap: var(--sp-2); margin-top: var(--sp-4); }
	@media (max-width: 640px) { .rk-tekst b { font-size: 28px; } .rk-nupud .btn { flex: 1 1 100%; text-align: center; } }
</style>
