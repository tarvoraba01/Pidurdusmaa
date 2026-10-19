/* Päeva etapp: 3D-maailm (three.js). Kruusatee metsas, ralliauto, tolm, kaamera auto taga.
 * Laaditakse ainult mängulehel (dünaamiline import), teisi lehti ei koorma. */
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { POOL, DS, ALGUS, PIKKUS, KP_VAHE, profiil, rng, asukoht, korgus } from './ralli.js';

const V = (x, y, z) => new THREE.Vector3(x, y, z);

/* keskjoone ruudustik kauguse päringuteks */
function looRuudustik(rada, rakk) {
	const m = new Map();
	for (let i = 0; i < rada.n; i++) {
		const k = Math.floor(rada.x[i] / rakk) + ',' + Math.floor(rada.z[i] / rakk);
		(m.get(k) || m.set(k, []).get(k)).push(i);
	}
	return (x, z, ring = 1) => {
		const cx = Math.floor(x / rakk), cz = Math.floor(z / rakk);
		let parim = -1, pd = Infinity;
		for (let a = -ring; a <= ring; a++) for (let b = -ring; b <= ring; b++) {
			for (const i of m.get(cx + a + ',' + (cz + b)) || []) {
				const dd = (rada.x[i] - x) ** 2 + (rada.z[i] - z) ** 2;
				if (dd < pd) { pd = dd; parim = i; }
			}
		}
		if (parim < 0) return null;
		const h = rada.h[parim], fx = Math.sin(h), fz = Math.cos(h), ex = x - rada.x[parim], ez = z - rada.z[parim];
		return { i: parim, dist: Math.sqrt(pd), d: ex * -fz + ez * fx, s: parim * DS + ex * fx + ez * fz };
	};
}

function tekst(txt, w, h, bg, fg) {
	const c = document.createElement('canvas');
	c.width = w; c.height = h;
	const g = c.getContext('2d');
	g.fillStyle = bg; g.fillRect(0, 0, w, h);
	g.fillStyle = fg; g.font = `800 ${Math.round(h * 0.62)}px "Barlow Condensed", "Arial Narrow", Arial, sans-serif`;
	g.textAlign = 'center'; g.textBaseline = 'middle';
	g.fillText(txt, w / 2, h / 2 + h * 0.04);
	const t = new THREE.CanvasTexture(c);
	t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
	return t;
}

/* kruusatee tekstuur: helepruun kruus, rattajäljed tumedamad, keskel lahtine kruusavall */
function kruusTekstuur() {
	const W = 256, H = 512, c = document.createElement('canvas');
	c.width = W; c.height = H;
	const g = c.getContext('2d'), r = rng(77);
	g.fillStyle = '#a08d6d'; g.fillRect(0, 0, W, H);
	const rada = (u, laius, varv) => { const grd = g.createLinearGradient((u - laius) * W, 0, (u + laius) * W, 0); grd.addColorStop(0, 'rgba(0,0,0,0)'); grd.addColorStop(0.5, varv); grd.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = grd; g.fillRect((u - laius) * W, 0, laius * 2 * W, H); };
	/* u: 0 = vasak serv (-POOL-0.6), 1 = parem serv; rattajäljed ±1,6 m ja ±0,1 m keskelt */
	const U = (d) => (d + POOL + 0.6) / (2 * POOL + 1.2);
	for (const d of [-2.6, -0.95, 0.95, 2.6]) rada(U(d), 0.06, 'rgba(70,58,42,0.42)');
	rada(U(0), 0.05, 'rgba(200,185,150,0.35)');
	rada(U(-POOL - 0.3), 0.07, 'rgba(90,95,60,0.5)');
	rada(U(POOL + 0.3), 0.07, 'rgba(90,95,60,0.5)');
	for (let k = 0; k < 9000; k++) {
		const l = 50 + r() * 150;
		g.fillStyle = `rgba(${l + 30},${l + 18},${l},${0.15 + r() * 0.35})`;
		const s = 1 + r() * 2.2;
		g.fillRect(r() * W, r() * H, s, s);
	}
	const t = new THREE.CanvasTexture(c);
	t.wrapS = THREE.ClampToEdgeWrapping; t.wrapT = THREE.RepeatWrapping;
	t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
	return t;
}

/* muru tekstuur: heledal põhjal tumedad ja kollakad kõrred. Korrutub tipuvärviga; liikudes vilksub mööda
   ja annab kiiruse tunde (Tarvo 19.10: kiiruse tunnetus kadunud) */
function muruTekstuur() {
	const W = 256, c = document.createElement('canvas');
	c.width = c.height = W;
	const g = c.getContext('2d'), r = rng(91);
	g.fillStyle = 'rgb(222,228,210)'; g.fillRect(0, 0, W, W);
	for (let k = 0; k < 2600; k++) {
		const x = r() * W, y = r() * W, l = 2 + r() * 5, a = (r() - 0.5) * 0.9;
		g.strokeStyle = r() < 0.7 ? `rgba(${40 + r() * 40},${70 + r() * 50},${25 + r() * 20},${0.25 + r() * 0.35})` : `rgba(255,${235 + r() * 20},${170 + r() * 40},${0.2 + r() * 0.3})`;
		g.lineWidth = 1 + r() * 1.2;
		g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.sin(a) * l, y - Math.cos(a) * l); g.stroke();
	}
	for (let k = 0; k < 60; k++) { g.fillStyle = `rgba(110,90,60,${0.12 + r() * 0.15})`; g.beginPath(); g.arc(r() * W, r() * W, 2 + r() * 6, 0, 6.283); g.fill(); }
	const t = new THREE.CanvasTexture(c);
	t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
	return t;
}

/* ---------- auto ---------- */
function looAuto() {
	const auto = new THREE.Group();
	const kere = new THREE.Group();
	auto.add(kere);
	const M = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.45, metalness: 0.15, ...o });
	const kollane = M(0xf6b800, { roughness: 0.32, metalness: 0.25 });
	const must = M(0x15171b, { roughness: 0.6 });
	const klaas = M(0x1d2733, { roughness: 0.08, metalness: 0.6 });
	const valge = M(0xf2f2f0, { roughness: 0.35 });
	const kast = (w, h, l, mat, x, y, z, rx = 0) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, l), mat); m.position.set(x, y, z); m.rotation.x = rx; m.castShadow = true; kere.add(m); return m; };
	/* kere */
	kast(1.8, 0.42, 4.05, kollane, 0, 0.56, 0);
	kast(1.74, 0.16, 1.15, kollane, 0, 0.8, 1.35, 0.1); /* kapott */
	kast(1.74, 0.2, 0.75, kollane, 0, 0.82, -1.62); /* pagas */
	kast(1.86, 0.2, 4.1, must, 0, 0.4, 0); /* põll */
	/* salong: külgprofiil (z, y) välja pressitud üle laiuse; kaldu esi- ja tagaklaas */
	const prof = new THREE.Shape();
	prof.moveTo(-1.45, 0); prof.lineTo(0.95, 0); prof.lineTo(0.2, 0.52); prof.lineTo(-1.05, 0.52); prof.lineTo(-1.45, 0.08); prof.lineTo(-1.45, 0);
	const sg = new THREE.ExtrudeGeometry(prof, { depth: 1.52, bevelEnabled: false });
	sg.rotateY(-Math.PI / 2); sg.translate(0.76, 0.76, 0);
	const salong = new THREE.Mesh(sg, klaas); salong.castShadow = true; kere.add(salong);
	kast(1.4, 0.05, 1.22, kollane, 0, 1.3, -0.42); /* katus */
	kast(0.36, 0.012, 1.22, must, -0.3, 1.33, -0.42); /* triibud */
	kast(0.42, 0.012, 1.2, must, -0.32, 0.9, 1.35, 0.1);
	kast(1.82, 0.012, 0.42, valge, 0, 0.775, 0.55); /* esiklaasi riba */
	/* spoiler */
	kast(1.62, 0.05, 0.32, must, 0, 1.2, -1.86);
	kast(0.05, 0.3, 0.16, must, -0.6, 1.03, -1.84);
	kast(0.05, 0.3, 0.16, must, 0.6, 1.03, -1.84);
	/* tuled */
	const tuli = M(0xfff6dd, { emissive: 0xfff2cc, emissiveIntensity: 1.4 });
	kast(0.36, 0.12, 0.05, tuli, -0.6, 0.66, 2.03);
	kast(0.36, 0.12, 0.05, tuli, 0.6, 0.66, 2.03);
	for (const x of [-0.6, -0.2, 0.2, 0.6]) { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.07, 14), tuli); l.rotation.x = Math.PI / 2; l.position.set(x * 0.85, 0.5, 2.06); kere.add(l); }
	const tagatuli = M(0x5a0a0a, { emissive: 0xff1a1a, emissiveIntensity: 0.25 });
	kast(0.42, 0.12, 0.05, tagatuli, -0.62, 0.7, -2.03);
	kast(0.42, 0.12, 0.05, tagatuli, 0.62, 0.7, -2.03);
	/* number külgedel */
	const nr = new THREE.MeshBasicMaterial({ map: tekst('52', 128, 128, '#ffffff', '#111111') });
	for (const s of [-1, 1]) { const p = new THREE.Mesh(new THREE.PlaneGeometry(0.55, 0.55), nr); p.position.set(s * 0.905, 0.62, 0.15); p.rotation.y = s * Math.PI / 2; kere.add(p); }
	/* porilapid */
	for (const z of [1.05, -1.75]) for (const x of [-0.78, 0.78]) kast(0.3, 0.32, 0.03, must, x, 0.32, z - 0.3);
	/* rattad */
	const rehvM = M(0x1a1a1a, { roughness: 0.9 }), velg = M(0xd9dde2, { roughness: 0.3, metalness: 0.7 });
	const rG = new THREE.CylinderGeometry(0.34, 0.34, 0.27, 20); rG.rotateZ(Math.PI / 2);
	const vG = new THREE.CylinderGeometry(0.22, 0.22, 0.28, 10); vG.rotateZ(Math.PI / 2);
	const rattad = [];
	for (const [x, z, esi] of [[-0.8, 1.32, 1], [0.8, 1.32, 1], [-0.8, -1.38, 0], [0.8, -1.38, 0]]) {
		const pivot = new THREE.Group(); pivot.position.set(x, 0.34, z);
		const ratas = new THREE.Group();
		const t = new THREE.Mesh(rG, rehvM); t.castShadow = true;
		const v = new THREE.Mesh(vG, velg);
		const kodar = new THREE.Mesh(new THREE.BoxGeometry(0.29, 0.06, 0.4), velg);
		ratas.add(t, v, kodar); pivot.add(ratas); auto.add(pivot);
		rattad.push({ pivot, ratas, esi });
	}
	return { auto, kere, rattad, tagatuli };
}

/* ---------- tolm ---------- */
function looTolm(n) {
	const geo = new THREE.BufferGeometry();
	const pos = new Float32Array(n * 3), suur = new Float32Array(n), alfa = new Float32Array(n);
	geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
	geo.setAttribute('suur', new THREE.BufferAttribute(suur, 1));
	geo.setAttribute('alfa', new THREE.BufferAttribute(alfa, 1));
	const mat = new THREE.ShaderMaterial({
		transparent: true, depthWrite: false,
		uniforms: { varv: { value: new THREE.Color(0xe6dcc6) }, skaala: { value: 600 }, fogColor: { value: new THREE.Color() }, fogNear: { value: 1 }, fogFar: { value: 1000 } },
		vertexShader: `attribute float suur; attribute float alfa; varying float vA; varying float vF; uniform float skaala; uniform float fogNear; uniform float fogFar;
			void main(){ vec4 mv = modelViewMatrix * vec4(position,1.0); gl_Position = projectionMatrix * mv; gl_PointSize = suur * skaala / -mv.z; vA = alfa; vF = smoothstep(fogNear, fogFar, -mv.z); }`,
		fragmentShader: `uniform vec3 varv; uniform vec3 fogColor; varying float vA; varying float vF;
			void main(){ vec2 p = gl_PointCoord - 0.5; float r = dot(p,p)*4.0; if(r>1.0) discard; float a = (1.0-r)*vA; gl_FragColor = vec4(mix(varv, fogColor, vF), a*(1.0-vF)); }`
	});
	const pts = new THREE.Points(geo, mat);
	pts.frustumCulled = false;
	const osa = Array.from({ length: n }, () => ({ elu: 0, max: 1, x: 0, y: 0, z: 0, vx: 0, vy: 0, vz: 0, s0: 1, a0: 0.5 }));
	let jarg = 0;
	return {
		pts, mat,
		lisa(x, y, z, vx, vy, vz, s0, a0, max) { const p = osa[jarg]; jarg = (jarg + 1) % n; Object.assign(p, { elu: max, max, x, y, z, vx, vy, vz, s0, a0 }); },
		uuenda(dt) {
			for (let i = 0; i < n; i++) {
				const p = osa[i];
				if (p.elu <= 0) { alfa[i] = 0; continue; }
				p.elu -= dt;
				const k = 1 - p.elu / p.max;
				p.vx *= 1 - dt * 1.6; p.vz *= 1 - dt * 1.6; p.vy = p.vy * (1 - dt * 1.2) + dt * 0.25;
				p.x += p.vx * dt; p.y += p.vy * dt; p.z += p.vz * dt;
				pos[i * 3] = p.x; pos[i * 3 + 1] = p.y; pos[i * 3 + 2] = p.z;
				suur[i] = p.s0 * (1 + k * 3.2);
				alfa[i] = p.a0 * Math.min(1, k * 8) * Math.pow(1 - k, 1.3);
			}
			geo.attributes.position.needsUpdate = true; geo.attributes.suur.needsUpdate = true; geo.attributes.alfa.needsUpdate = true;
		}
	};
}

export function looMaailm(canvas, rada, { madal = false } = {}) {
	const renderer = new THREE.WebGLRenderer({ canvas, antialias: !madal, powerPreference: 'high-performance' });
	renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, madal ? 1.25 : 1.75));
	renderer.shadowMap.enabled = true;
	renderer.shadowMap.type = THREE.PCFShadowMap;
	renderer.outputColorSpace = THREE.SRGBColorSpace;
	renderer.toneMapping = THREE.ACESFilmicToneMapping;
	renderer.toneMappingExposure = 1.05;

	const scene = new THREE.Scene();
	const UDU = new THREE.Color(0xc9d6de);
	scene.fog = new THREE.Fog(UDU, 70, madal ? 330 : 430);
	scene.background = UDU;
	const camera = new THREE.PerspectiveCamera(64, 16 / 9, 0.1, 900);

	/* taevas: gradient kuppel */
	const taevas = new THREE.Mesh(new THREE.SphereGeometry(800, 24, 12), new THREE.ShaderMaterial({
		side: THREE.BackSide, depthWrite: false, fog: false,
		uniforms: { yla: { value: new THREE.Color(0x5d93cf) }, all: { value: UDU } },
		vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
		fragmentShader: 'uniform vec3 yla; uniform vec3 all; varying vec3 vP; void main(){ float t = clamp(vP.y*2.2, 0.0, 1.0); gl_FragColor = vec4(mix(all, yla, pow(t,0.7)), 1.0); }'
	}));
	scene.add(taevas);

	scene.add(new THREE.HemisphereLight(0xe4efff, 0x5a5236, 1.05));
	const paike = new THREE.DirectionalLight(0xfff0d6, 2.4);
	paike.castShadow = true;
	paike.shadow.mapSize.set(madal ? 1024 : 2048, madal ? 1024 : 2048);
	Object.assign(paike.shadow.camera, { left: -32, right: 32, top: 32, bottom: -32, near: 1, far: 160 });
	paike.shadow.bias = -0.0004; paike.shadow.normalBias = 0.03;
	scene.add(paike, paike.target);
	const PAIKE = V(-38, 62, 30);

	const r = rng(rada.seeme);
	const lahim = looRuudustik(rada, 14);
	const lahimKaugel = looRuudustik(rada, 40);

	const muru = muruTekstuur();
	/* ---------- maastik: laia ruudustikuga kõrgusväli ---------- */
	let minX = Infinity, maxX = -Infinity, minZ = Infinity, maxZ = -Infinity, keskY = 0;
	for (let i = 0; i < rada.n; i++) { minX = Math.min(minX, rada.x[i]); maxX = Math.max(maxX, rada.x[i]); minZ = Math.min(minZ, rada.z[i]); maxZ = Math.max(maxZ, rada.z[i]); keskY += rada.y[i]; }
	keskY /= rada.n;
	const AAR = 420, SAMM = madal ? 9 : 6;
	const x0 = minX - AAR, z0 = minZ - AAR, nx = Math.ceil((maxX - minX + 2 * AAR) / SAMM), nz = Math.ceil((maxZ - minZ + 2 * AAR) / SAMM);
	const mur = (x, z) => Math.sin(x * 0.013 + rada.seeme) * Math.cos(z * 0.011 - rada.seeme * 0.7) * 5 + Math.sin(x * 0.041 + z * 0.037) * 1.6;
	function maapind(x, z) {
		const q = lahim(x, z, 1) || lahimKaugel(x, z, 2);
		if (!q) return { y: keskY + mur(x, z) + 6, dist: 999 };
		const j = Math.max(0, Math.min(rada.n - 1, q.i));
		const base = rada.y[j];
		const a = q.dist;
		if (a < 17) return { y: base + profiil(a) - 0.7, dist: a };
		const kauge = Math.min(1, (a - 17) / 70);
		return { y: base + profiil(a) + mur(x, z) * kauge, dist: a };
	}
	{
		const pos = new Float32Array((nx + 1) * (nz + 1) * 3), col = new Float32Array((nx + 1) * (nz + 1) * 3);
		const c = new THREE.Color();
		for (let j = 0; j <= nz; j++) for (let i = 0; i <= nx; i++) {
			const x = x0 + i * SAMM, z = z0 + j * SAMM, k = (j * (nx + 1) + i) * 3;
			const m = maapind(x, z);
			pos[k] = x; pos[k + 1] = m.y; pos[k + 2] = z;
			const t = Math.sin(x * 0.07) * Math.cos(z * 0.05) * 0.5 + 0.5;
			c.setRGB(0.2 + t * 0.06, 0.29 + t * 0.07, 0.13 + t * 0.02);
			if (m.dist > 30) c.multiplyScalar(0.8);
			col[k] = c.r; col[k + 1] = c.g; col[k + 2] = c.b;
		}
		const idx = [];
		for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) { const a = j * (nx + 1) + i, b = a + 1, d = a + nx + 1, e = d + 1; idx.push(a, d, b, b, d, e); }
		const g = new THREE.BufferGeometry();
		g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
		g.setAttribute('color', new THREE.BufferAttribute(col, 3));
		const uv = new Float32Array((nx + 1) * (nz + 1) * 2);
		for (let k = 0; k < uv.length / 2; k++) { uv[k * 2] = pos[k * 3] / 5; uv[k * 2 + 1] = pos[k * 3 + 2] / 5; }
		g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
		g.setIndex(idx); g.computeVertexNormals();
		const m = new THREE.Mesh(g, new THREE.MeshLambertMaterial({ vertexColors: true, map: muru }));
		m.receiveShadow = true;
		scene.add(m);
	}

	/* ---------- tee ääred (muru, kraav) ja tee ---------- */
	function riba(nihked, varvid, uv, mat, lisaY) {
		const n = rada.n, w = nihked.length;
		const pos = new Float32Array(n * w * 3), col = varvid ? new Float32Array(n * w * 3) : null, uvs = uv ? new Float32Array(n * w * 2) : null;
		for (let i = 0; i < n; i++) {
			const h = rada.h[i], rx = -Math.cos(h), rz = Math.sin(h);
			const tumm = 0.92 + 0.08 * Math.sin(i * 0.37) * Math.sin(i * 0.11);
			for (let j = 0; j < w; j++) {
				const d = nihked[j], k = (i * w + j) * 3;
				pos[k] = rada.x[i] + rx * d; pos[k + 1] = rada.y[i] + profiil(d) + lisaY; pos[k + 2] = rada.z[i] + rz * d;
				if (col) { const c = varvid(d); col[k] = c[0] * tumm; col[k + 1] = c[1] * tumm; col[k + 2] = c[2] * tumm; }
				if (uvs) { uvs[(i * w + j) * 2] = (d - nihked[0]) / (nihked[w - 1] - nihked[0]); uvs[(i * w + j) * 2 + 1] = (i * DS) / 6; }
			}
		}
		const idx = [];
		for (let i = 0; i < n - 1; i++) for (let j = 0; j < w - 1; j++) { const a = i * w + j, b = a + 1, c = a + w, d = c + 1; idx.push(a, b, c, b, d, c); }
		const g = new THREE.BufferGeometry();
		g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
		if (col) g.setAttribute('color', new THREE.BufferAttribute(col, 3));
		if (uvs) g.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
		g.setIndex(idx); g.computeVertexNormals();
		const m = new THREE.Mesh(g, mat);
		m.receiveShadow = true;
		scene.add(m);
		return m;
	}
	const aareNihked = [-17, -13, -10, -8.4, -7.3, -6.5, -5.9, -5.3, -4.4, 4.4, 5.3, 5.9, 6.5, 7.3, 8.4, 10, 13, 17];
	riba(aareNihked, (d) => {
		const a = Math.abs(d);
		if (a < 5.6) return [0.36, 0.36, 0.22]; /* peenar */
		if (a < 7.6) return [0.17, 0.25, 0.11]; /* kraav, tumedam */
		return [0.24, 0.34, 0.15];
	}, true, new THREE.MeshLambertMaterial({ vertexColors: true, map: (() => { const t = muru.clone(); t.needsUpdate = true; t.repeat.set(7, 1.5); return t; })() }), 0);
	const teeNihked = [-POOL - 0.6, -POOL, -3, -1.6, -0.6, 0, 0.6, 1.6, 3, POOL, POOL + 0.6];
	riba(teeNihked, null, true, new THREE.MeshStandardMaterial({ map: kruusTekstuur(), roughness: 0.96, metalness: 0, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }), 0.03);

	/* ---------- puud ---------- */
	const kuuskG = (() => {
		const osad = [];
		const tyvi = new THREE.CylinderGeometry(0.12, 0.18, 1.6, 6); tyvi.translate(0, 0.8, 0);
		osad.push(varvi(tyvi, 0x4a3524));
		for (const [y, r0, h] of [[1.2, 1.9, 3.4], [2.9, 1.5, 3.0], [4.5, 1.05, 2.6], [5.9, 0.6, 2.0]]) { const k = new THREE.ConeGeometry(r0, h, 8); k.translate(0, y + h / 2, 0); osad.push(varvi(k, 0x1f3b24)); }
		return mergeGeometries(osad);
	})();
	const kaskG = (() => {
		const tyvi = new THREE.CylinderGeometry(0.1, 0.16, 5.2, 6); tyvi.translate(0, 2.6, 0);
		const vo = new THREE.IcosahedronGeometry(1.4, 1); vo.scale(1, 1.5, 1); vo.translate(0, 5.7, 0);
		const vo2 = new THREE.IcosahedronGeometry(0.9, 1); vo2.translate(0.6, 4.5, 0.3);
		return mergeGeometries([varvi(tyvi, 0xe8e4da), varvi(vo, 0xd7a92c), varvi(vo2, 0xc99a28)]);
	})();
	function varvi(g, hex) {
		const c = new THREE.Color(hex), n = g.attributes.position.count, a = new Float32Array(n * 3);
		for (let i = 0; i < n; i++) { a[i * 3] = c.r; a[i * 3 + 1] = c.g; a[i * 3 + 2] = c.b; }
		g.setAttribute('color', new THREE.BufferAttribute(a, 3));
		return g.index ? g.toNonIndexed() : g;
	}
	const kuused = [], kased = [], kaugKuused = [], kaugKased = [], kokku = new Map(), KR = 8;
	const lisaKokku = (x, z, raad, t) => { const k = Math.floor(x / KR) + ',' + Math.floor(z / KR); (kokku.get(k) || kokku.set(k, []).get(k)).push([x, z, raad, t]); };
	const vaba = (x, z, min) => { const q = lahim(x, z, 2); return !q || q.dist >= min; };
	for (let i = 0; i < rada.n; i += 2) {
		const h = rada.h[i], rx = -Math.cos(h), rz = Math.sin(h);
		for (const pool of [-1, 1]) {
			for (let t = 0; t < 3; t++) {
				const d = pool * (8.6 + Math.pow(r(), 1.6) * (t === 0 ? 10 : 55));
				if (r() < (t === 0 ? 0.32 : 0.7)) {
					const x = rada.x[i] + rx * d + (r() - 0.5) * 3, z = rada.z[i] + rz * d + (r() - 0.5) * 3;
					if (!vaba(x, z, 8.2)) continue;
					const kask = r() < 0.22, s = 0.75 + r() * 0.75;
					(kask ? kased : kuused).push([x, z, s, r() * 6.28]);
					lisaKokku(x, z, 0.35 * s + 0.15, 'puu');
				}
			}
		}
	}
	/* kaugem metsasein */
	for (let k = 0; k < (madal ? 2500 : 5000); k++) {
		const x = x0 + r() * nx * SAMM, z = z0 + r() * nz * SAMM;
		const q = lahimKaugel(x, z, 2);
		if (q && q.dist < 70) continue;
		(r() < 0.15 ? kaugKased : kaugKuused).push([x, z, 1 + r() * 0.8, r() * 6.28]);
	}
	const puuMat = new THREE.MeshLambertMaterial({ vertexColors: true });
	const m4 = new THREE.Matrix4(), q4 = new THREE.Quaternion(), s4 = new THREE.Vector3(), p4 = new THREE.Vector3(), yl = V(0, 1, 0);
	/* kaugel metsal varju ei arvutata (vari on niikuinii ainult auto ümber) */
	for (const [g, list, vari] of [[kuuskG, kuused, true], [kaskG, kased, true], [kuuskG, kaugKuused, false], [kaskG, kaugKased, false]]) {
		if (!list.length) continue;
		const im = new THREE.InstancedMesh(g, puuMat, list.length);
		const c = new THREE.Color();
		list.forEach(([x, z, s, rot], j) => {
			const y = maapind(x, z).y - 0.2;
			q4.setFromAxisAngle(yl, rot); s4.set(s, s * (0.9 + (j % 7) * 0.05), s); p4.set(x, y, z);
			im.setMatrixAt(j, m4.compose(p4, q4, s4));
			const t = 0.8 + ((j * 7919) % 100) / 300;
			im.setColorAt(j, c.setRGB(t, t, t));
		});
		im.castShadow = vari; im.receiveShadow = false;
		scene.add(im);
	}

	/* ---------- teeäärsed põõsad ja kivid: lähedal, vilksuvad mööda ---------- */
	{
		const poosad = [], kivid = [];
		for (let i = 0; i < rada.n; i += 1) {
			const h = rada.h[i], rx = -Math.cos(h), rz = Math.sin(h);
			for (const pool of [-1, 1]) {
				if (r() > 0.42) continue;
				const d = pool * (POOL + 2.3 + Math.pow(r(), 1.4) * 6.5);
				const x = rada.x[i] + rx * d + (r() - 0.5) * 2, z = rada.z[i] + rz * d + (r() - 0.5) * 2;
				if (!vaba(x, z, POOL + 2)) continue;
				(r() < 0.75 ? poosad : kivid).push([x, z, 0.35 + r() * 0.7, r() * 6.28]);
			}
		}
		const pG = new THREE.IcosahedronGeometry(1, 0); pG.scale(1.2, 0.75, 1.2); pG.translate(0, 0.45, 0);
		const kG = new THREE.DodecahedronGeometry(0.55, 0); kG.scale(1, 0.6, 1.2); kG.translate(0, 0.12, 0);
		for (const [g, list, varv] of [[pG, poosad, 0x3d5a2a], [kG, kivid, 0x8a8a84]]) {
			if (!list.length) continue;
			const im = new THREE.InstancedMesh(g, new THREE.MeshLambertMaterial({ color: varv, flatShading: true }), list.length);
			const c = new THREE.Color();
			list.forEach(([x, z, sk, rot], j) => {
				q4.setFromAxisAngle(yl, rot); p4.set(x, maapind(x, z).y - 0.05, z);
				im.setMatrixAt(j, m4.compose(p4, q4, s4.set(sk, sk, sk)));
				const t = 0.75 + ((j * 7919) % 100) / 220; im.setColorAt(j, c.setRGB(t, t * (varv === 0x3d5a2a ? 1.05 : 1), t));
			});
			scene.add(im);
		}
	}

	/* ---------- teeäärsed: postid, heinapallid, pealtvaatajad, väravad ---------- */
	const postid = [];
	for (let i = 0; i < rada.n; i += 10) for (const p of [-1, 1]) postid.push([i, p * (POOL + 1.1)]);
	{
		const g = mergeGeometries([varvi(new THREE.BoxGeometry(0.1, 1.1, 0.1).translate(0, 0.55, 0), 0xf2f2f2), varvi(new THREE.BoxGeometry(0.11, 0.18, 0.11).translate(0, 0.9, 0), 0xd42020)]);
		const im = new THREE.InstancedMesh(g, new THREE.MeshLambertMaterial({ vertexColors: true }), postid.length);
		postid.forEach(([i, d], j) => { const h = rada.h[i]; p4.set(rada.x[i] - Math.cos(h) * d, rada.y[i] + profiil(d), rada.z[i] + Math.sin(h) * d); im.setMatrixAt(j, m4.compose(p4, q4.identity(), s4.set(1, 1, 1))); });
		im.castShadow = true; scene.add(im);
	}
	const pallid = [], inimesed = [];
	for (const k of rada.kurvid) {
		if (k.R > 110) continue;
		const valis = -k.suund; /* d > 0 on paremal; parempööre (suund +1) → väliskülg vasakul */
		for (let n = k.n0 + 1; n < k.n1; n += 2) {
			const i = Math.min(rada.n - 1, Math.round((n * 5) / DS));
			const d = valis * (POOL + 1.9), h = rada.h[i];
			const x = rada.x[i] - Math.cos(h) * d, z = rada.z[i] + Math.sin(h) * d;
			if (!vaba(x, z, POOL + 1.5)) continue;
			pallid.push([x, z, h, rada.y[i] + profiil(d)]);
			lisaKokku(x, z, 0.7, 'pall');
		}
		const kesk = Math.min(rada.n - 1, Math.round(((k.n0 + k.n1) / 2) * 5 / DS));
		for (let g = 0; g < 2; g++) {
			const i0 = Math.min(rada.n - 1, kesk + (g ? 6 : -4));
			const hulk = 4 + Math.floor(r() * 6);
			for (let m = 0; m < hulk; m++) {
				const i = Math.min(rada.n - 1, i0 + Math.round((r() - 0.5) * 6));
				const d = valis * (POOL + 6.5 + r() * 3.5), h = rada.h[i];
				const x = rada.x[i] - Math.cos(h) * d, z = rada.z[i] + Math.sin(h) * d;
				if (!vaba(x, z, POOL + 5.5)) continue;
				inimesed.push([x, z, maapind(x, z).y, r()]);
			}
		}
	}
	{
		const g = new THREE.CylinderGeometry(0.62, 0.62, 1.25, 14); g.rotateZ(Math.PI / 2);
		const im = new THREE.InstancedMesh(g, new THREE.MeshLambertMaterial({ color: 0xd8bf6a }), Math.max(1, pallid.length));
		pallid.forEach(([x, z, h, y], j) => { q4.setFromAxisAngle(yl, h); p4.set(x, y + 0.55, z); im.setMatrixAt(j, m4.compose(p4, q4, s4.set(1, 1, 1))); });
		im.count = pallid.length; im.castShadow = true; scene.add(im);
	}
	const VARVID = [0xd7262e, 0x1f5fd1, 0xf2c200, 0x2b9a48, 0xf07a1a, 0x222222, 0xeeeeee, 0x7a3fb0];
	const inimKeha = new THREE.InstancedMesh(new THREE.CapsuleGeometry(0.24, 0.8, 3, 6).translate(0, 0.7, 0), new THREE.MeshLambertMaterial(), Math.max(1, inimesed.length));
	const inimPea = new THREE.InstancedMesh(new THREE.SphereGeometry(0.15, 8, 6).translate(0, 1.42, 0), new THREE.MeshLambertMaterial({ color: 0xe9c4a2 }), Math.max(1, inimesed.length));
	{
		const c = new THREE.Color();
		inimesed.forEach(([x, z, y, v], j) => { p4.set(x, y, z); m4.compose(p4, q4.identity(), s4.set(1, 0.9 + v * 0.25, 1)); inimKeha.setMatrixAt(j, m4); inimPea.setMatrixAt(j, m4); inimKeha.setColorAt(j, c.setHex(VARVID[Math.floor(v * VARVID.length)])); });
		inimKeha.count = inimPea.count = inimesed.length;
		inimKeha.castShadow = true; scene.add(inimKeha, inimPea);
	}
	/* väravad: start, kontrollpunktid, finiš */
	function varav(s, txt, bg) {
		const i = Math.min(rada.n - 1, Math.round(s / DS)), h = rada.h[i];
		const g = new THREE.Group();
		const post = new THREE.MeshLambertMaterial({ color: 0x222428 });
		for (const d of [-POOL - 1.2, POOL + 1.2]) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.35, 5.2, 0.35), post); p.position.set(-d, 2.6, 0); p.castShadow = true; g.add(p); }
		const silt = new THREE.Mesh(new THREE.BoxGeometry(2 * POOL + 2.8, 1.25, 0.25), [post, post, post, post, new THREE.MeshBasicMaterial({ map: tekst(txt, 1024, 128, bg, '#111') }), new THREE.MeshBasicMaterial({ map: tekst(txt, 1024, 128, bg, '#111') })]);
		silt.position.y = 5.0; silt.castShadow = true; g.add(silt);
		g.position.set(rada.x[i], rada.y[i], rada.z[i]); g.rotation.y = h;
		scene.add(g);
	}
	varav(ALGUS, 'START  ·  PÄEVA ETAPP', '#ffc20e');
	for (let k = 1; k * KP_VAHE < PIKKUS; k++) varav(ALGUS + k * KP_VAHE, 'KONTROLLPUNKT ' + k, '#ffffff');
	varav(ALGUS + PIKKUS, 'FINIŠ', '#ffc20e');

	/* ---------- põdraohu märgid ---------- */
	const margiTex = (() => {
		const c = document.createElement('canvas'); c.width = c.height = 256;
		const g = c.getContext('2d');
		g.beginPath(); g.moveTo(128, 14); g.lineTo(246, 230); g.lineTo(10, 230); g.closePath();
		g.fillStyle = '#d61f1f'; g.fill();
		g.beginPath(); g.moveTo(128, 50); g.lineTo(214, 210); g.lineTo(42, 210); g.closePath();
		g.fillStyle = '#ffffff'; g.fill();
		/* põdra siluett */
		g.fillStyle = '#111';
		g.fillRect(88, 140, 64, 26); g.fillRect(92, 166, 7, 30); g.fillRect(104, 166, 7, 30); g.fillRect(132, 166, 7, 30); g.fillRect(143, 166, 7, 30);
		g.fillRect(146, 118, 12, 30); g.fillRect(150, 112, 26, 14); g.fillRect(140, 100, 6, 16); g.fillRect(132, 98, 16, 5); g.fillRect(156, 100, 6, 14); g.fillRect(156, 98, 16, 5);
		const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
	})();
	for (const p of rada.podrad || []) {
		const i = Math.max(0, Math.round((p.s - 110) / DS)), h = rada.h[i], d = POOL + 1.7;
		const g = new THREE.Group();
		const post = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 2.2, 6), new THREE.MeshLambertMaterial({ color: 0x9aa0a6 }));
		post.position.y = 1.1; post.castShadow = true; g.add(post);
		const silt = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 1.0), new THREE.MeshBasicMaterial({ map: margiTex, transparent: true, side: THREE.DoubleSide }));
		silt.position.set(0, 2.2, 0.06); g.add(silt);
		g.position.set(rada.x[i] - Math.cos(h) * d, rada.y[i] + profiil(d), rada.z[i] + Math.sin(h) * d);
		g.rotation.y = h + Math.PI; /* näoga sõitja poole */
		scene.add(g);
	}

	/* ---------- põdrad (kuni 3 korraga) ---------- */
	function looPoder() {
		const g = new THREE.Group();
		const pr = new THREE.MeshLambertMaterial({ color: 0x3b2a1e }), hele = new THREE.MeshLambertMaterial({ color: 0xcbb68f }), jalaM = new THREE.MeshLambertMaterial({ color: 0x6b5a48 });
		const b = (w, h, l, m, x, y, z) => { const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, l), m); o.position.set(x, y, z); o.castShadow = true; g.add(o); return o; };
		b(0.9, 1.0, 2.3, pr, 0, 1.75, 0); /* keha */
		b(0.95, 0.5, 0.9, pr, 0, 2.15, 0.7); /* turi */
		const kael = b(0.4, 0.9, 0.45, pr, 0, 2.2, 1.25); kael.rotation.x = -0.6;
		b(0.38, 0.42, 0.95, pr, 0, 2.45, 1.75); /* pea */
		b(0.2, 0.3, 0.12, pr, 0, 2.1, 1.8); /* habe */
		b(1.25, 0.08, 0.5, hele, 0, 2.78, 1.5); /* sarved */
		b(0.08, 0.3, 0.08, hele, -0.45, 2.92, 1.5); b(0.08, 0.3, 0.08, hele, 0.45, 2.92, 1.5);
		const jalad = [];
		for (const [x, z] of [[-0.3, 0.85], [0.3, 0.85], [-0.3, -0.85], [0.3, -0.85]]) {
			const piv = new THREE.Group(); piv.position.set(x, 1.3, z);
			const j = new THREE.Mesh(new THREE.BoxGeometry(0.16, 1.3, 0.16), jalaM); j.position.y = -0.65; j.castShadow = true;
			piv.add(j); g.add(piv); jalad.push(piv);
		}
		g.visible = false;
		scene.add(g);
		return { g, jalad };
	}
	const podrad = [looPoder(), looPoder(), looPoder()];
	/* asend tee suhtes: s, d → maailm */
	function poder(k, p) {
		const P = podrad[k];
		if (!p) { P.g.visible = false; return; }
		const i = Math.max(0, Math.min(rada.n - 1, Math.round(p.s / DS))), h = rada.h[i];
		const x = rada.x[i] - Math.cos(h) * p.d, z = rada.z[i] + Math.sin(h) * p.d;
		P.g.visible = true;
		P.g.position.set(x, maapind(x, z).y + (Math.abs(p.d) < POOL + 0.5 ? rada.y[i] + profiil(p.d) - maapind(x, z).y : 0), z);
		/* kõnnib üle tee: nina risti teega */
		P.g.rotation.y = h + (p.suund > 0 ? -Math.PI / 2 : Math.PI / 2);
		P.jalad.forEach((j, n) => { j.rotation.x = p.kaib ? Math.sin(p.faas * 6 + (n % 2 ? Math.PI : 0) + (n > 1 ? Math.PI / 2 : 0)) * 0.45 : 0; });
		return { x, z };
	}

	/* ---------- auto, tolm ---------- */
	const A = looAuto();
	scene.add(A.auto);
	const tolm = looTolm(madal ? 320 : 600);
	scene.add(tolm.pts);
	let tolmJaak = 0;

	/* kokkupõrke päring auto jaoks: lähim puu / pall */
	function takistus(x, z) {
		const cx = Math.floor(x / KR), cz = Math.floor(z / KR);
		let parim = null, pd = Infinity;
		for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) for (const t of kokku.get(cx + a + ',' + (cz + b)) || []) {
			const dd = (t[0] - x) ** 2 + (t[1] - z) ** 2 - t[2] * t[2];
			if (dd < pd) { pd = dd; parim = t; }
		}
		return parim;
	}

	/* ---------- kaamera ---------- */
	const kaam = { yaw: rada.h[0], pos: V(0, 3, -8), init: false };
	const poos = { p: 0, r: 0, h: 0, vh: 0, kp: 0, vp: 0, kr: 0, vr: 0 };
	const ajut = V(0, 0, 0), siht = V(0, 0, 0);
	function lerpNurk(a, b, t) { let d = b - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return a + d * t; }

	function uuenda(o, dt, { aeg = 0 } = {}) {
		/* auto asend */
		/* AUTO JA MAAILM ERALDI (Tarvo 19.10): iga ratas loeb maapinda oma kohas, auto kallutatakse
		   rataste järgi (ei vaju maa sisse), kere istub vedrudel (pidurdus, kurv, maandumine), õhus
		   rattad ripuvad. */
		const sh = Math.sin(o.h), ch = Math.cos(o.h);
		const maaKoht = (lx, lz) => { const x = o.x + sh * lz + ch * lx, z = o.z + ch * lz - sh * lx; const q = asukoht(rada, x, z, o.i); return korgus(rada, q.i, q.d, q.s); };
		const gFL = maaKoht(0.8, 1.32), gFR = maaKoht(-0.8, 1.32), gRL = maaKoht(0.8, -1.38), gRR = maaKoht(-0.8, -1.38);
		const ees = (gFL + gFR) / 2, taga_ = (gRL + gRR) / 2, vas = (gFL + gRL) / 2, par = (gFR + gRR) / 2;
		let pSiht = -Math.atan2(ees - taga_, 2.7), rSiht = Math.atan2(vas - par, 1.6);
		const keskMaa = (ees + taga_) / 2;
		const ohus = o.ohus && o.y > keskMaa + 0.02;
		if (ohus) { pSiht = Math.max(-0.35, Math.min(0.35, -Math.atan2(o.vy, Math.max(5, o.v)) * 0.55)); rSiht = 0; }
		const kk = 1 - Math.exp(-dt * (ohus ? 3 : 14));
		poos.p += (pSiht - poos.p) * kk; poos.r += (rSiht - poos.r) * kk;
		A.auto.position.set(o.x, ohus ? o.y : Math.max(o.y, keskMaa), o.z);
		A.auto.rotation.set(poos.p, o.h, poos.r, 'YXZ');
		/* vedrud: kere vajub pidurdades ette, kurvis välja, maandudes alla */
		if (o.loog > 0.5) poos.vh -= Math.min(6, o.loog) * 0.32;
		o.loog = 0; /* löök on vedrudele üle antud */
		const hSiht = ohus ? 0.05 : 0, kpSiht = ohus ? 0 : Math.max(-0.06, Math.min(0.06, -o.along * 0.008)), krSiht = ohus ? 0 : Math.max(-0.08, Math.min(0.08, -o.alat * 0.0085));
		for (let n = 0, sd = dt / 2; n < 2; n++) {
			poos.vh += ((hSiht - poos.h) * 140 - poos.vh * 13) * sd; poos.h += poos.vh * sd;
			poos.vp += ((kpSiht - poos.kp) * 110 - poos.vp * 12) * sd; poos.kp += poos.vp * sd;
			poos.vr += ((krSiht - poos.kr) * 110 - poos.vr * 12) * sd; poos.kr += poos.vr * sd;
		}
		poos.h = Math.max(-0.16, Math.min(0.12, poos.h));
		const kruus = ohus ? 0 : Math.sin(aeg * 31) * Math.sin(aeg * 17.3) * 0.008 * Math.min(1, o.v / 20);
		A.kere.position.y = poos.h + kruus;
		A.kere.rotation.x = poos.kp; A.kere.rotation.z = poos.kr;
		/* rattad: maas kontaktis (väike jääk tasapinnast), õhus ripuvad */
		const tasand = [gFL, gFR, gRL, gRR].map((g, n) => g - (keskMaa + (n < 2 ? 1 : -1) * (ees - taga_) / 2 + (n % 2 === 0 ? 1 : -1) * (vas - par) / 2));
		for (const [n, w] of A.rattad.entries()) {
			w.ratas.rotation.x = o.ratas; if (w.esi) w.pivot.rotation.y = -o.rool * 0.42;
			const sihtY = ohus ? 0.34 - 0.13 : 0.34 + Math.max(-0.1, Math.min(0.1, tasand[[1, 0, 3, 2][n]] || 0));
			w.pivot.position.y += (sihtY - w.pivot.position.y) * (1 - Math.exp(-dt * 18));
		}
		A.tagatuli.emissiveIntensity = o.pidur ? 3.2 : 0.25;
		/* tolm tagaratastest */
		if (o.v > 3 && !o.ohus) {
			const mitu = (o.v * 1.6 + Math.abs(Math.sin(o.libis)) * 70) * dt * (madal ? 0.6 : 1) * (o.maas ? 0.5 : 1);
			tolmJaak += mitu;
			const fx = Math.sin(o.h), fz = Math.cos(o.h), rx = -fz, rz = fx;
			while (tolmJaak >= 1) {
				tolmJaak -= 1;
				const pool = Math.random() < 0.5 ? -0.8 : 0.8;
				const x = o.x - fx * 1.9 + rx * pool, z = o.z - fz * 1.9 + rz * pool;
				tolm.lisa(x, o.y + 0.3, z, o.vx * 0.2 + (Math.random() - 0.5) * 2.5, 0.5 + Math.random() * 0.9, o.vz * 0.2 + (Math.random() - 0.5) * 2.5, 1.4 + Math.random() * 1.2, 0.5 + Math.min(0.3, Math.abs(o.libis)), 2.4 + Math.random() * 2);
			}
		}
		tolm.uuenda(dt);
		tolm.mat.uniforms.fogColor.value.copy(UDU); tolm.mat.uniforms.fogNear.value = scene.fog.near; tolm.mat.uniforms.fogFar.value = scene.fog.far;
		tolm.mat.uniforms.skaala.value = renderer.domElement.height * 0.55;

		/* kaamera: auto taga, vaatab sõidusuuna ja nina vahele (driftis paistab auto külg) */
		const sSuund = o.v > 3 ? Math.atan2(o.vx, o.vz) : o.h;
		const sihtYaw = lerpNurk(o.h, sSuund, 0.55);
		if (!kaam.init) { kaam.yaw = sihtYaw; }
		kaam.yaw = lerpNurk(kaam.yaw, sihtYaw, 1 - Math.exp(-dt * 4.5));
		const taga = 5.7 + Math.min(1.3, o.v * 0.025), korge = 1.95 + Math.min(0.35, o.v * 0.007);
		siht.set(o.x - Math.sin(kaam.yaw) * taga, A.auto.position.y + korge, o.z - Math.cos(kaam.yaw) * taga);
		const maa = maapind(siht.x, siht.z).y + 1.2;
		if (siht.y < maa) siht.y = maa;
		/* asend jäik (auto ei jookse kaamerast eest ära), ainult kõrgus sujuv */
		if (!kaam.init) { kaam.pos.copy(siht); kaam.init = true; }
		kaam.pos.x = siht.x; kaam.pos.z = siht.z;
		kaam.pos.y += (siht.y - kaam.pos.y) * (1 - Math.exp(-dt * 9));
		camera.position.copy(kaam.pos);
		const raputus = o.maas || o.v > 20 ? Math.min(0.035, o.v * 0.0007) * (o.maas ? 2 : 1) : 0;
		camera.position.x += (Math.random() - 0.5) * raputus; camera.position.y += (Math.random() - 0.5) * raputus;
		ajut.set(o.x + Math.sin(kaam.yaw) * 6, A.auto.position.y + 0.95, o.z + Math.cos(kaam.yaw) * 6);
		camera.lookAt(ajut);
		const fov = 63 + Math.min(19, o.v * 0.36); /* kiirusega laiem vaade: kiiruse tunne */
		if (Math.abs(camera.fov - fov) > 0.05) { camera.fov += (fov - camera.fov) * Math.min(1, dt * 3); camera.updateProjectionMatrix(); }
		/* päike järgib autot (vari ainult auto ümber) */
		paike.position.set(o.x + PAIKE.x, o.y + PAIKE.y, o.z + PAIKE.z);
		paike.target.position.set(o.x, o.y, o.z);
		taevas.position.copy(camera.position);
	}
	function joonista() { renderer.render(scene, camera); }
	function suurus(w, h) { renderer.setSize(w, h, false); camera.aspect = w / Math.max(1, h); camera.updateProjectionMatrix(); }
	function kaamUus() { kaam.init = false; }
	function havita() {
		scene.traverse((x) => { x.geometry?.dispose?.(); const m = x.material; (Array.isArray(m) ? m : m ? [m] : []).forEach((mm) => { mm.map?.dispose?.(); mm.dispose?.(); }); });
		renderer.dispose();
	}
	return { uuenda, joonista, suurus, havita, takistus, kaamUus, poder, _dbg: { scene, tolm, renderer, camera } };
}
