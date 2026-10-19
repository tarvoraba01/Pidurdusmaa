/* Päeva etapi heli (WebAudio): mootor pööretega, kruusa krõbin kiiruse ja libisemisega. Faile pole. */
export function looHeli() {
	const AC = window.AudioContext || window.webkitAudioContext;
	if (!AC) return null;
	const ac = new AC();
	const pea = ac.createGain(); pea.gain.value = 0; pea.connect(ac.destination);
	/* mootor: kaks saehammast + madalpääs */
	const filt = ac.createBiquadFilter(); filt.type = 'lowpass'; filt.frequency.value = 900; filt.Q.value = 2;
	const mg = ac.createGain(); mg.gain.value = 0.22; filt.connect(mg); mg.connect(pea);
	const o1 = ac.createOscillator(), o2 = ac.createOscillator();
	o1.type = 'sawtooth'; o2.type = 'square';
	const g2 = ac.createGain(); g2.gain.value = 0.35;
	o1.connect(filt); o2.connect(g2); g2.connect(filt);
	o1.start(); o2.start();
	/* kruus: müra ribapääsuga */
	const buf = ac.createBuffer(1, ac.sampleRate * 2, ac.sampleRate), d = buf.getChannelData(0);
	for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
	const myra = ac.createBufferSource(); myra.buffer = buf; myra.loop = true;
	/* Tarvo 19.10: krõbin oli liiga vali ja terav: nüüd madal ja vaikne mürin, valjem ainult driftis */
	const bp = ac.createBiquadFilter(); bp.type = 'lowpass'; bp.frequency.value = 420; bp.Q.value = 0.5;
	const kg = ac.createGain(); kg.gain.value = 0;
	myra.connect(bp); bp.connect(kg); kg.connect(pea); myra.start();
	let vaigista = false;
	return {
		uuenda(o, kaib) {
			const t = ac.currentTime;
			const f = Math.max(25, o.prr / 30);
			o1.frequency.setTargetAtTime(f, t, 0.03);
			o2.frequency.setTargetAtTime(f / 2, t, 0.03);
			filt.frequency.setTargetAtTime(500 + o.prr * 0.35, t, 0.05);
			kg.gain.setTargetAtTime(Math.min(0.14, o.v / 400 + Math.max(0, Math.abs(Math.sin(o.libis)) - 0.08) * 0.35) * (o.maas ? 1.3 : 1), t, 0.08);
			pea.gain.setTargetAtTime(kaib && !vaigista ? 0.32 : 0, t, 0.1);
		},
		jatka() { if (ac.state !== 'running') ac.resume().catch(() => {}); },
		vaikne(v) { vaigista = v; },
		sulge() { try { ac.close(); } catch {} }
	};
}
