/* Pidurdusmaa mootori ja andmete testid (brauseri mootor engine.js).
 *
 *   cd veeb && node --test tests/
 *
 * Mida siin kontrollitakse ja miks:
 *  1. PAARSUS: engine.js annab samad tulemused mis Pythoni mootor
 *     (tõe allikas, kalibreeritud). Fikstuuri teeb
 *     `python3 -m mudel.parity_core` -- käivita see iga mudelimuudatuse järel.
 *  2. ANDMED: iga core.json-i auto ja rehv läbib sisendikontrolli; EPREL-i
 *     read on kehtivad (klass A-E, kategooria 0-3).
 *  3. KÕIK AUTOD x KÕIK LEHE OLUD: tulemus on lõplik, positiivne,
 *     kiirusega kasvav; pindade järjekord kuiv < märg < lumi < jää;
 *     parem märgise klass ei anna kunagi pikemat märga pidurdusmaad.
 *  4. ÄÄRMUSED: vigane sisend annab vea, mitte numbri; auto, mis ei saa
 *     peatuda, annab Infinity ja hoiatuse, mitte kärbitud numbri.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
// engine.js on IIFE, mis kirjutab globalThis.Pidurdus
new Function(fs.readFileSync(path.join(root, 'src/lib/engine.js'), 'utf8'))();
const P = globalThis.Pidurdus;
const core = JSON.parse(fs.readFileSync(path.join(root, 'static/data/core.json'), 'utf8'));
const vehByKey = Object.fromEntries(core.vehicles.map(v => [v.key, v]));

const GNOM = { A: 1.60, B: 1.47, C: 1.32, D: 1.17, E: 1.05 };
function gmid(g, cat) {
  const t = core.gClass[g];
  if (t) { if (t[cat]) return t[cat][0]; if (t._ && t._[1]) return t._[0]; }
  return GNOM[g];
}
// SAMA tabel mis app.js COND (lehe olud)
const COND = { wet: ['ASPHALT', 1.0, 10], dry: ['ASPHALT', 0, 15], snow: ['SNOW_PACKED', 0, -5], ice: ['ICE', 0, -5] };
const cond = (ck, v, extra = {}) => Object.assign({ speedKmh: v, surface: COND[ck][0], texture: 'NORMAL', waterMm: COND[ck][1], tempC: COND[ck][2], payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1 }, extra);
const classTyre = (g, cat, size) => ({ key: 'c', name: 'K', category: cat, wetGripIndex: gmid(g, cat), treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: false, size, gSource: 'label' });
const CATS = ['SUMMER_TOURING', 'ALL_SEASON', 'WINTER_CENTRAL', 'WINTER_NORDIC'];

test('paarsus Pythoni mootoriga (core.json andmed)', () => {
  const fx = JSON.parse(fs.readFileSync(path.join(here, 'parity_fixture.json'), 'utf8'));
  let bad = [];
  fx.cases.forEach((c, i) => {
    const v = vehByKey[c.veh];
    assert.ok(v, 'fikstuuri auto puudub core.json-ist: ' + c.veh + ' -- käivita python3 -m mudel.parity_core');
    const r = P.stoppingDistance(c.tyre, v, c.cond), py = fx.python[i];
    const js = { d: r.distanceM, tot: r.totalDistanceM, lo: r.lowM, hi: r.highM, sig: r.sigmaRel, mu: r.muEffective, g: r.peakDecelG, t: r.timeS, at: r.accelTimeS, ad: r.accelDistM };
    for (const k of Object.keys(js)) {
      const a = py[k] === null ? Infinity : py[k], b = js[k];
      if (!(a === b || Math.abs(a - b) <= 1e-6 * Math.max(1, Math.abs(a)))) bad.push(`#${i} ${k}: py=${a} js=${b}`);
    }
    for (const [k, jk] of [['lim', 'limiter'], ['conf', 'confidence'], ['ex', 'extreme']])
      if (py[k] !== r[jk]) bad.push(`#${i} ${k}: py=${py[k]} js=${r[jk]}`);
    if (py.w !== r.warnings.length) bad.push(`#${i} hoiatusi: py=${py.w} js=${r.warnings.length}`);
  });
  assert.deepEqual(bad.slice(0, 20), [], bad.length + ' erinevust');
});

test('iga auto ja testitud rehv läbib sisendikontrolli', () => {
  for (const v of core.vehicles) {
    assert.doesNotThrow(() => P.validate(classTyre('C', 'ALL_SEASON', v.oemSize), v, cond('dry', 50)), v.key);
  }
  const golf = vehByKey.vw_golf_8;
  for (const t of core.tyres) assert.doesNotThrow(() => P.validate(t, golf, cond('wet', 50)), t.key);
});

test('võtmed on unikaalsed ja valija kombinatsioonid ei kattu', () => {
  const k = new Set(), combo = new Set();
  for (const v of core.vehicles) {
    assert.ok(!k.has(v.key), 'topelt võti ' + v.key); k.add(v.key);
    const c = [v.make, v.model, v.yearLabel, v.variant].join('|');
    assert.ok(!combo.has(c), 'kaks autot sama valikuga: ' + c); combo.add(c);
    assert.match(v.oemSize, /^\d{3}\/\d{2} R\d{2}C?$/, v.key + ' tehasemõõt');
    if (v.oemSizes && v.oemSizes.length) assert.ok(v.oemSizes.includes(v.oemSize), v.key + ': baasmõõt puudub tehasemõõtude seast');
  }
  const tk = new Set(); for (const t of core.tyres) { assert.ok(!tk.has(t.key), 'topelt rehv ' + t.key); tk.add(t.key); }
});

test('EPREL-i read: klass A-E, kategooria 0-3, iga loetletud mõõdu fail olemas', () => {
  const dir = path.join(root, 'static/data/eprel');
  const files = new Set(fs.readdirSync(dir).map(f => f.replace(/\.json$/, '')));
  for (const m of core.eprelSizes) assert.ok(files.has(m), 'puudub fail ' + m);
  let n = 0;
  for (const m of core.eprelSizes) {
    for (const r of JSON.parse(fs.readFileSync(path.join(dir, m + '.json'), 'utf8'))) {
      n++;
      assert.ok('ABCDE'.includes(r[4]) && r[4].length === 1, `${m} ${r[0]}: märghaardumise klass ${r[4]}`);
      assert.ok([0, 1, 2, 3].includes(r[3]), `${m} ${r[0]}: kategooria ${r[3]}`);
    }
  }
  assert.ok(n > 1000);
});

test('märgise klassi väärtused on igas kategoorias järjestuses A >= B >= C >= D >= E', () => {
  for (const cat of CATS) {
    const g = 'ABCDE'.split('').map(x => gmid(x, cat));
    for (let i = 0; i < 4; i++) assert.ok(g[i] >= g[i + 1], `${cat}: ${'ABCDE'[i]}=${g[i]} < ${'ABCDE'[i + 1]}=${g[i + 1]}`);
  }
});

const wetOverSnow = [];
test('kõik autod x lehe olud: lõplik, kiirusega kasvav, pindade ja klasside järjestus', () => {
  const speeds = [20, 50, 80, 110, 130];
  const probs = [];
  for (const v of core.vehicles) {
    for (const cat of CATS) {
      const byClass = {};
      for (const g of ['A', 'C', 'E']) {
        const ty = classTyre(g, cat, v.oemSize), per = {};
        for (const ck of Object.keys(COND)) {
          let prev = 0; per[ck] = {};
          for (const s of speeds) {
            const r = P.stoppingDistance(ty, v, cond(ck, s)), d = r.distanceM;
            if (!Number.isFinite(d) || d <= 0) probs.push(`${v.key} ${cat} ${g} ${ck} ${s}: d=${d}`);
            if (!(r.lowM <= d && d <= r.highM)) probs.push(`${v.key} ${ck} ${s}: vahemik ei kata tulemust`);
            if (!(d > prev)) probs.push(`${v.key} ${cat} ${g} ${ck}: ${s} km/h ${d} <= eelmine ${prev}`);
            prev = d; per[ck][s] = d;
          }
        }
        for (const s of speeds) {
          // kuiv vs märg SAMAL temperatuuril (eelseaded: kuiv 15 °C, märg 10 °C;
          // talverehv haarab 10 °C juures paremini -> eelseadete otsevõrdlus
          // mõõdaks temperatuuri, mitte pinda)
          const dry10 = P.stoppingDistance(ty, v, cond('dry', s, { tempC: 10 })).distanceM;
          if (!(dry10 <= per.wet[s] + 1e-9)) probs.push(`${v.key} ${cat} ${g} ${s}: kuiv@10 ${dry10} >= märg ${per.wet[s]}`);
          // märg < lumi kuni 110 km/h. Üle selle ennustab mudel laiadel
          // Põhjala talverehvidel 1 mm vees osalist vesiliugu (vt QA_ARUANNE
          // "Jäänud riskid"); seda EI peideta, vaid loetakse eraldi testis.
          if (s <= 110 && !(per.wet[s] < per.snow[s])) probs.push(`${v.key} ${cat} ${g} ${s}: märg >= lumi`);
          if (s > 110 && !(per.wet[s] < per.snow[s])) wetOverSnow.push(`${v.key} ${cat} ${g} ${s}`);
          if (!(per.snow[s] < per.ice[s])) probs.push(`${v.key} ${cat} ${g} ${s}: lumi >= jää`);
        }
        byClass[g] = per.wet;
      }
      for (const s of speeds) {
        if (!(byClass.A[s] <= byClass.C[s] && byClass.C[s] <= byClass.E[s]))
          probs.push(`${v.key} ${cat} ${s}: märja klassi järjestus A ${byClass.A[s]} C ${byClass.C[s]} E ${byClass.E[s]}`);
      }
    }
  }
  assert.deepEqual(probs.slice(0, 15), [], probs.length + ' probleemi');
});

test('teadaolev kõrvalekalle: märg >= lumi üle 110 km/h ainult talverehvidel', () => {
  // Mudel: 1 mm vesi + lai talverehv + suur kiirus = osaline vesiliug.
  // Tugineb veesügavuse astendajale 0,42 (ankrud ~7,8 mm juures) ja laiuse
  // astendajale 1,0 (üks allikas). Füüsikaliselt võimalik, empiiriliselt
  // kinnitamata. Test lukustab ulatuse: kui see hakkab levima suve-
  // rehvidele või madalamale kiirusele, on midagi muutunud.
  if (wetOverSnow.length) console.log(`# märg >= lumi (>110 km/h): ${wetOverSnow.length} juhtu, nt ${wetOverSnow.slice(0, 3).join('; ')}`);
  const bad = wetOverSnow.filter(x => !/ WINTER_(NORDIC|CENTRAL) /.test(x));
  assert.deepEqual(bad.slice(0, 10), [], bad.length + ' juhtu väljaspool talverehve');
});

test('vigane sisend annab vea, mitte numbri', () => {
  const v = vehByKey.vw_golf_8, t = classTyre('B', 'SUMMER_TOURING', v.oemSize);
  const bad = [
    [t, v, cond('dry', NaN)], [t, v, cond('dry', -10)], [t, v, cond('dry', Infinity)], [t, v, cond('dry', 400)],
    [t, v, cond('dry', 80, { payloadKg: -500 })], [t, v, cond('dry', 80, { tempC: 90 })],
    [t, v, cond('dry', 80, { surface: 'LAVA' })], [t, v, cond('dry', 80, { waterMm: -1 })],
    [t, v, cond('dry', 80, { reactionTimeS: -1 })], [t, v, cond('dry', 80, { brakeCondition: 0 })],
    [t, Object.assign({}, v, { kerbMassKg: 0 }), cond('dry', 80)],
    [t, Object.assign({}, v, { recommendedPressureBar: 0 }), cond('dry', 80)],
    [Object.assign({}, t, { wetGripIndex: 0 }), v, cond('wet', 80)],
    [Object.assign({}, t, { category: 'SUMMER' }), v, cond('dry', 80)],
    [Object.assign({}, t, { size: '000/00 R00' }), v, cond('wet', 80)],
    [Object.assign({}, t, { size: '999/99 R99' }), v, cond('wet', 80)],
    [Object.assign({}, t, { pressureBar: 0 }), v, cond('wet', 80)],
    [t, v, Object.assign(cond('dry', 80), { payloadKg: undefined })],
  ];
  bad.forEach((b, i) => assert.throws(() => P.stoppingDistance(...b), undefined, 'juhtum ' + i));
});

test('null- ja väga väike kiirus', () => {
  const v = vehByKey.vw_golf_8, t = classTyre('B', 'SUMMER_TOURING', v.oemSize);
  assert.equal(P.stoppingDistance(t, v, cond('dry', 0)).distanceM, 0);
  const d1 = P.stoppingDistance(t, v, cond('dry', 1)).distanceM;
  assert.ok(d1 > 0 && d1 < 0.1, 'd(1 km/h) = ' + d1);
});

test('auto, mis ei saa peatuda, annab Infinity ja hoiatuse', () => {
  const v = vehByKey.vw_golf_8, t = classTyre('B', 'SUMMER_TOURING', v.oemSize);
  const r = P.stoppingDistance(t, v, cond('ice', 60, { gradientPct: -12 }));
  assert.equal(r.distanceM, Infinity);
  assert.equal(r.stopped, false);
  assert.equal(r.confidence, 'madal');
  assert.ok(r.warnings.some(w => /ei peatu/.test(w)));
});

test('pikk pidurdus ei kärbita (varem vaikne 60 s piir)', () => {
  const v = vehByKey.vw_golf_8, t = classTyre('B', 'SUMMER_TOURING', v.oemSize);
  // testiväljaku jää (sõidutee jääl on aeg u 40 s, alla vana 60 s piiri)
  const r = P.stoppingDistance(t, v, cond('ice', 200, { iceRoad: false }));
  assert.ok(r.stopped && r.timeS > 60, 'aeg ' + r.timeS);
  // kiirusega kasvav ka seal, kus vana piir lõikas
  const r180 = P.stoppingDistance(t, v, cond('ice', 180, { iceRoad: false }));
  assert.ok(Number.isFinite(r.distanceM) && r.distanceM > r180.distanceM);
});

test('kiirus: pidurdusmaa kasvab umbes ruudus (kuiv, konstantse haarde lähedal)', () => {
  const v = vehByKey.vw_golf_8, t = classTyre('B', 'SUMMER_TOURING', v.oemSize);
  const d50 = P.stoppingDistance(t, v, cond('dry', 50)).distanceM, d100 = P.stoppingDistance(t, v, cond('dry', 100)).distanceM;
  const k = d100 / d50;
  // puhas ruut = 4; pidurite ülesehitus lisab lineaarse osa (-> alla 4), kiirusega langev haare (-> üle 4)
  assert.ok(k > 3.6 && k < 4.4, 'd100/d50 = ' + k);
});

test('sama rehv = sama tulemus; mõõt autol mõjutab ainult märga (laius)', () => {
  const v = vehByKey.vw_golf_8, base = core.tyres[0];
  const a = P.stoppingDistance(base, v, cond('wet', 90)).distanceM, b = P.stoppingDistance(Object.assign({}, base), v, cond('wet', 90)).distanceM;
  assert.equal(a, b);
  const narrow = Object.assign({}, base, { size: '205/55 R16', gSize: base.size });
  const wide = Object.assign({}, base, { size: '245/40 R18', gSize: base.size });
  assert.ok(P.stoppingDistance(narrow, v, cond('wet', 110)).distanceM < P.stoppingDistance(wide, v, cond('wet', 110)).distanceM, 'lai rehv ujub varem');
  assert.equal(P.stoppingDistance(narrow, v, cond('dry', 90)).distanceM, P.stoppingDistance(wide, v, cond('dry', 90)).distanceM);
});

test('mass: auto mass muudab pidurdusmaad vähe (a = mu*g), suunaga raskem = pikem', () => {
  const v = vehByKey.vw_golf_8, t = classTyre('B', 'SUMMER_TOURING', v.oemSize);
  const light = P.stoppingDistance(t, Object.assign({}, v, { kerbMassKg: 900 }), cond('dry', 100)).distanceM;
  const heavy = P.stoppingDistance(t, Object.assign({}, v, { kerbMassKg: 2800 }), cond('dry', 100)).distanceM;
  const lightLoad = P.stoppingDistance(t, v, cond('dry', 100, { payloadKg: 0 })).distanceM;
  const fullLoad = P.stoppingDistance(t, v, cond('dry', 100, { payloadKg: 500 })).distanceM;
  assert.ok(Math.abs(heavy - light) / light < 0.03, `900 kg ${light} vs 2800 kg ${heavy}`);
  assert.ok(fullLoad > lightLoad, 'koorem pikendab (koormustundlikkus)');
});

test('kalle: ülesmäge lühem, allamäge pikem', () => {
  const v = vehByKey.vw_golf_8, t = classTyre('B', 'SUMMER_TOURING', v.oemSize);
  const flat = P.stoppingDistance(t, v, cond('wet', 80)).distanceM;
  assert.ok(P.stoppingDistance(t, v, cond('wet', 80, { gradientPct: 8 })).distanceM < flat);
  assert.ok(P.stoppingDistance(t, v, cond('wet', 80, { gradientPct: -8 })).distanceM > flat);
});

test('kiire tee: eelarvutatud haare = muAtSpeed bitt-bitilt (öövahetus 7.10)', () => {
  // stoppingDistance kasutab makeMu-d (kiirusest sõltumatud tegurid ühe korra).
  // See peab andma TÄPSELT sama arvu mis muAtSpeed, igal pinnal ja kiirusel.
  const SURF = ['ASPHALT', 'CONCRETE', 'GRAVEL', 'SNOW_PACKED', 'SNOW_LOOSE', 'ICE'];
  const TEX = ['COARSE_NEW', 'NORMAL', 'WORN_SMOOTH', 'POLISHED'];
  let seed = 7; const R = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const bad = [];
  for (let i = 0; i < 400; i++) {
    const v = core.vehicles[Math.floor(R() * core.vehicles.length)];
    const cat = [...CATS, 'SUMMER_UHP', 'WINTER_STUDDED'][Math.floor(R() * 6)];
    const t = Object.assign(classTyre('ABCDE'[Math.floor(R() * 5)], cat, v.oemSize), { treadDepthMm: R() * 8, ageYears: R() * 14, pressureBar: R() < 0.5 ? null : 1.5 + R() * 1.5 });
    const surf = SURF[Math.floor(R() * SURF.length)];
    const c = cond('dry', 80, { surface: surf, texture: TEX[Math.floor(R() * 4)], waterMm: /ASPHALT|CONCRETE/.test(surf) && R() < 0.6 ? R() * 6 : 0, tempC: -25 + R() * 60, payloadKg: Math.round(R() * 500) });
    const f = P._muKiire(t, v, c);
    for (const vMs of [0.06, 1, 5, 13.9, 25, 36.1, 45]) {
      const a = P.muAtSpeed(t, v, c, vMs), b = f(vMs);
      if (a !== b) bad.push(`${surf} ${cat} v=${vMs}: ${a} vs ${b}`);
    }
  }
  assert.deepEqual(bad.slice(0, 10), [], bad.length + ' erinevust');
});

test('EPREL-i mõõdufailid: sõiduauto mõõtudel õige võti (öövahetus 7.10)', () => {
  // Vigased võtmed ("20555R1691W", "17565R14C6PR") liideti õige mõõdu alla.
  // Alles võivad jääda ainult LT (light truck) ja veoauto veljed (17.5, 19.5).
  const files = fs.readdirSync(path.join(root, 'static/data/eprel')).map(f => f.replace(/\.json$/, ''));
  const muud = files.filter(f => !/^\d{5}R\d{2}C?$/.test(f) && !/LT|^\d{5}R1[79]5/.test(f));
  assert.deepEqual(muud, []);
  const sizes = new Set(core.sizes.map(s => s.m));
  for (const s of core.sizes) assert.ok(files.includes(s.m), 'mõõdulehel pole faili ' + s.m);
  assert.ok(sizes.size === core.sizes.length);
});
