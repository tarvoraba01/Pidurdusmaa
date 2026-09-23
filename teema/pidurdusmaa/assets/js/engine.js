/* Pidurdusmaa füüsikamootor — port pidurdus/model.py-st.
   Peab andma Pythoni mootoriga identsed tulemused (vt web/verify.js).
   Sõltuvusteta, jookseb brauseris. */
(function (root) {
  'use strict';

  var G = 9.80665, RHO = 1.225;

  var CAL = {
    kG: 0.6727,
    muDry: { SUMMER_UHP: 1.314, SUMMER_TOURING: 1.208, ALL_SEASON: 1.039, WINTER_CENTRAL: 0.934, WINTER_NORDIC: 0.842, WINTER_STUDDED: 0.823 },
    muSnow: { SUMMER_UHP: 0.14, SUMMER_TOURING: 0.15, ALL_SEASON: 0.3925, WINTER_CENTRAL: 0.375, WINTER_NORDIC: 0.377, WINTER_STUDDED: 0.345 },
    muIce: { SUMMER_UHP: 0.06, SUMMER_TOURING: 0.06, ALL_SEASON: 0.107, WINTER_CENTRAL: 0.096, WINTER_NORDIC: 0.203, WINTER_STUDDED: 0.27 },
    muGravel: 0.694,
    treadLossGravel: 0.148, treadLossGravelLocked: 0.148, treadGravelSatFrac: 0.7,
    vRef: 22.222,
    kSpeedDry: 0.0022, kSpeedSnow: 0.0035, kSpeedIce: 0.001,
    wetLiftB: 1.154,
    tempCurves: {
      SUMMER_UHP: [[-10, 0.52], [0, 0.7], [5, 0.81], [10, 0.89], [15, 0.95], [20, 1.0], [30, 1.02], [45, 0.99]],
      SUMMER_TOURING: [[-10, 0.58], [0, 0.74], [5, 0.84], [10, 0.91], [15, 0.96], [20, 1.0], [30, 1.01], [45, 0.98]],
      ALL_SEASON: [[-10, 0.84], [0, 0.92], [5, 0.95], [10, 0.97], [15, 0.99], [20, 1.0], [30, 0.99], [45, 0.94]],
      WINTER_CENTRAL: [[-20, 1.025], [-10, 1.035], [0, 1.0325], [5, 1.025], [10, 1.0175], [20, 1.0], [30, 0.92], [45, 0.84]],
      WINTER_NORDIC: [[-20, 1.03], [-10, 1.04], [0, 1.0375], [5, 1.0275], [10, 1.0175], [20, 1.0], [30, 0.9], [45, 0.8]],
      WINTER_STUDDED: [[-20, 1.03], [-10, 1.04], [0, 1.0375], [5, 1.0275], [10, 1.0175], [20, 1.0], [30, 0.9], [45, 0.8]]
    },
    pressOptOffsetDry: -0.132, pressKDry: 0.0511,
    pressKWetUnder: 0.005, pressKWetOver: 0.0659,
    treadLossWetResidual: 0.03, treadLossDryFull: 0.055,
    ageFreeYears: 5.0, ageLossPerYear: 0.011, ageLossMax: 0.13,
    loadExp: -0.07, loadRefRatio: 0.55,
    textureMpdMm: { COARSE_NEW: 1.4, NORMAL: 0.7, WORN_SMOOTH: 0.45, POLISHED: 0.35 },
    textureMicro: { COARSE_NEW: 1.0, NORMAL: 1.0, WORN_SMOOTH: 1.0, POLISHED: 0.912 },
    ifiSpA: 14.2, ifiSpB: 89.7, ifiRefSpeedKmh: 60.0,
    concreteFactor: { SUMMER_UHP: 0.825, SUMMER_TOURING: 0.825, ALL_SEASON: 0.825, WINTER_CENTRAL: 0.825, WINTER_NORDIC: 0.825, WINTER_STUDDED: 0.825 },
    waterKDeep: 0.03, waterKShallow: 0.055,
    iceTempCurve: [[2.0, 0.42], [0.0, 0.55], [-2.0, 0.72], [-5.0, 1.0], [-10.0, 1.32], [-15.0, 1.58], [-20.0, 1.78], [-35.0, 1.92]],
    iceTempMin: 0.40, iceTempMax: 2.00,
    // Jää temperatuuritundlikkus ei ole kõigile üks. Nael lõikab jäässe
    // mehaaniliselt ja ei hooli temperatuurist nii palju kui kumm.
    // [VIB10D] Vi Bilägare 2010: sama 9 rehvi jääl kahel temperatuuril
    // samal päeval -> naastrehv 1,23, hõõrdrehv 1,69, vana mudel 1,45.
    // Aste mõjub AINULT kaopoolel (f < 1). Vt model.py ice_temp_exp.
    iceTempExp: {SUMMER_UHP: 1.0, SUMMER_TOURING: 1.0, ALL_SEASON: 1.0,
                 WINTER_CENTRAL: 1.0, WINTER_NORDIC: 1.0,
                 WINTER_STUDDED: 0.545},
    snowLooseFactor: 0.85,
    snowTempCurve: [[-30.0, 1.0], [-3.0, 1.0], [0.0, 0.9], [2.0, 0.84]],
    snowTempMin: 0.60, snowTempMax: 1.05,
    snowWarmFromC: -3.0, sigmaSnowWarm: 0.12,
    hpC: 63.5, hpTreadGain: 0.085, hpWaterRefMm: 1.15,
    hpWidthRefMm: 230.0, hpWidthExp: 1.0,
    muHydroplane: 0.08,
    hpCategoryFactor: { SUMMER_UHP: 1.062, SUMMER_TOURING: 1.062, ALL_SEASON: 1.015, WINTER_CENTRAL: 1.0, WINTER_NORDIC: 0.825, WINTER_STUDDED: 0.825 },
    pressAbsScale: { NONE: 9.16, EARLY: 1.0, MODERN: 1.0, LATEST: 1.0 },
    absEff: { NONE: 0.74, EARLY: 0.88, MODERN: 0.94, LATEST: 0.965 },
    absEffGravel: { NONE: 1.0, EARLY: 0.698, MODERN: 0.698, LATEST: 0.698 },
    brakeBuildup: { NONE: 0.35, EARLY: 0.28, MODERN: 0.22, LATEST: 0.17 },
    crr: 0.011,
    sigmaBase: { ASPHALT: 0.07, CONCRETE: 0.085, GRAVEL: 0.22, SNOW_PACKED: 0.13, SNOW_LOOSE: 0.18, ICE: 0.17 },
    speedRange: { ASPHALT: [40.0, 130.0], CONCRETE: [40.0, 120.0], SNOW_PACKED: [15.0, 80.0], SNOW_LOOSE: [15.0, 60.0], ICE: [15.0, 80.0], GRAVEL: [40.0, 80.0] },
    sigmaSpeedExtrap: 0.25, sigmaSpeedExtrapMax: 0.4,
    sigmaWetExtra: 0.02, sigmaLabelOnly: 0.045,
    sigmaSizeRimInch: 0.015, sigmaSizeMax: 0.08, sizeWarnInch: 2.0,
    sigmaExtrapolation: 0.06, sigmaSnowSingleSource: 0.06, sigmaTexture: 0.07
  };

  function clamp(x, lo, hi) { return Math.max(lo, Math.min(hi, x)); }

  // "225/40 R18" -> [225, 40, 18]; null kui ei parsi
  function parseSize(size) {
    if (!size) return null;
    var m = /\s*(\d{3})\s*\/\s*(\d{2})\s*R?\s*(\d{2})/.exec(size);
    return m ? [+m[1], +m[2], +m[3]] : null;
  }
  function sizeGapInch(tyreSize, oemSize) {
    var a = parseSize(tyreSize), b = parseSize(oemSize);
    return (a && b) ? Math.abs(a[2] - b[2]) : 0;
  }

  function interp(pts, x) {
    var p = pts.slice().sort(function (a, b) { return a[0] - b[0]; }), a, b, i;
    if (x <= p[0][0]) { a = p[0]; b = p[1]; }
    else if (x >= p[p.length - 1][0]) { a = p[p.length - 2]; b = p[p.length - 1]; }
    else {
      for (i = 0; i < p.length - 1; i++) {
        if (p[i][0] <= x && x <= p[i + 1][0]) { a = p[i]; b = p[i + 1]; break; }
      }
    }
    if (b[0] === a[0]) return a[1];
    return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]);
  }

  var ASPHALTISH = { ASPHALT: 1, CONCRETE: 1 };
  var SNOWISH = { SNOW_PACKED: 1, SNOW_LOOSE: 1 };

  function pressureOf(tyre, veh) {
    return (tyre.pressureBar === null || tyre.pressureBar === undefined)
      ? veh.recommendedPressureBar : tyre.pressureBar;
  }

  function hydroplaneSpeedKmh(tyre, veh, cond) {
    if (!ASPHALTISH[cond.surface]) return null;
    if (cond.waterMm <= 0.02) return null;
    var p = pressureOf(tyre, veh);
    var v = CAL.hpC * Math.sqrt(Math.max(0.5, p));
    v *= 1.0 + CAL.hpTreadGain * tyre.treadDepthMm;
    v *= CAL.hpCategoryFactor[tyre.category];
    if (tyre.hpFactor != null) v *= tyre.hpFactor;
    // lai rehv peab rohkem vett kõrvale lükkama -> ujub varem
    var szw = parseSize(tyre.size);
    if (szw) v *= Math.pow(CAL.hpWidthRefMm / szw[0], CAL.hpWidthExp);
    v *= Math.pow(CAL.hpWaterRefMm / Math.max(0.15, cond.waterMm), 0.42);
    return v;
  }

  function muAtSpeed(tyre, veh, cond, vMs) {
    var surf = cond.surface;
    var wet = !!ASPHALTISH[surf] && cond.waterMm > 0.02;
    var mu, k;

    if (ASPHALTISH[surf]) {
      mu = wet ? CAL.kG * tyre.wetGripIndex
               : (tyre.muDry != null ? tyre.muDry : CAL.muDry[tyre.category]);
      if (surf === 'CONCRETE') mu *= CAL.concreteFactor[tyre.category];
    } else if (SNOWISH[surf]) {
      mu = tyre.muSnow != null ? tyre.muSnow : CAL.muSnow[tyre.category];
      if (surf === 'SNOW_LOOSE') mu *= CAL.snowLooseFactor;
      mu *= clamp(interp(CAL.snowTempCurve, cond.tempC),
                  CAL.snowTempMin, CAL.snowTempMax);
    } else if (surf === 'ICE') {
      mu = tyre.muIce != null ? tyre.muIce : CAL.muIce[tyre.category];
      var fIce = interp(CAL.iceTempCurve, cond.tempC);
      var eIce = CAL.iceTempExp[tyre.category];
      if (eIce == null) eIce = 1.0;
      if (eIce !== 1.0 && fIce > 0.0 && fIce < 1.0) fIce = Math.pow(fIce, eIce);
      mu *= clamp(fIce, CAL.iceTempMin, CAL.iceTempMax);
    } else {
      mu = CAL.muGravel;
    }

    if (ASPHALTISH[surf]) {
      mu *= interp(CAL.tempCurves[tyre.category], cond.tempC);
      /* Tekstuur: KAKS mehhanismi, mitte üks kordaja.
         MAKRO (vee äravool) -> kiiruse gradient, ainult märjal, PIARC
         IFI kujul. MIKRO (poleeritus) -> tasemekadu, märjal ja kuival.
         NORMAL annab makroliikmeks täpselt 1,000 igal kiirusel.
         Vt model.py pikka selgitust. */
      mu *= CAL.textureMicro[cond.texture];
      if (wet) {
        var spT = CAL.ifiSpA + CAL.ifiSpB * CAL.textureMpdMm[cond.texture];
        var spR = CAL.ifiSpA + CAL.ifiSpB * CAL.textureMpdMm.NORMAL;
        var dd = CAL.ifiRefSpeedKmh - vMs * 3.6;
        mu *= Math.exp(dd / spT - dd / spR);
      }
    }

    if (wet) {
      var h = cond.waterMm;
      mu *= h >= 1.0 ? 1.0 / (1.0 + CAL.waterKDeep * (h - 1.0))
                     : 1.0 + CAL.waterKShallow * (1.0 - h);
    }

    if (wet) {
      var vhp = hydroplaneSpeedKmh(tyre, veh, cond) / 3.6;
      mu /= 1.0 + CAL.wetLiftB * Math.pow(vMs / vhp, 2);
      k = 0.0;
    } else if (ASPHALTISH[surf]) { k = CAL.kSpeedDry; }
    else if (surf === 'ICE') { k = CAL.kSpeedIce; }
    else if (SNOWISH[surf]) { k = CAL.kSpeedSnow; }
    else { k = CAL.kSpeedDry; }
    mu *= Math.exp(-k * (vMs - CAL.vRef));

    var tdNew = tyre.treadDepthNewMm != null ? tyre.treadDepthNewMm : 8.0;
    var worn = clamp((tdNew - tyre.treadDepthMm) / Math.max(0.1, tdNew - 1.0), 0, 1);
    if (wet) mu *= 1.0 - CAL.treadLossWetResidual * worn;
    else if (ASPHALTISH[surf]) mu *= 1.0 - CAL.treadLossDryFull * worn;
    else if (SNOWISH[surf]) mu *= 1.0 - 0.30 * worn;
    else if (surf === 'ICE') mu *= 1.0 - 0.15 * worn;
    else if (surf === 'GRAVEL') {
      /* Lukus ratas kaevub kruusa ja lükkab enda ette valli -- see jõud
         ei hooli mustrist, seega mustri mõju KÜLLASTUB. ABS hoiab ratta
         veerlemas, valli ei teki, muster loeb edasi. Vt model.py. */
      if (veh.absClass === 'NONE') {
        mu *= 1.0 - CAL.treadLossGravelLocked *
              Math.min(worn / CAL.treadGravelSatFrac, 1.0);
      } else {
        mu *= 1.0 - CAL.treadLossGravel * worn;
      }
    }

    var dp = pressureOf(tyre, veh) - veh.recommendedPressureBar;
    var pscale = CAL.pressAbsScale[veh.absClass] || 1.0;
    if (wet) {
      var kp = dp < 0 ? CAL.pressKWetUnder : CAL.pressKWetOver;
      mu *= clamp(1.0 - pscale * kp * dp * dp, 0.45, 1.02);
    } else {
      var d = dp - CAL.pressOptOffsetDry;
      mu *= clamp(1.0 - pscale * CAL.pressKDry * d * d, 0.45, 1.02);
    }

    var over = Math.max(0.0, (tyre.ageYears != null ? tyre.ageYears : 1.0) - CAL.ageFreeYears);
    mu *= 1.0 - Math.min(CAL.ageLossMax, CAL.ageLossPerYear * over);

    var mass = veh.kerbMassKg + cond.payloadKg;
    var cap = tyre.loadCapacityKg || (veh.kerbMassKg / 4.0 / CAL.loadRefRatio);
    var ratio = (mass / 4.0) / cap;
    mu *= Math.pow(ratio / CAL.loadRefRatio, CAL.loadExp);

    if (wet) {
      var vhpK = hydroplaneSpeedKmh(tyre, veh, cond), vk = vMs * 3.6;
      if (vhpK && vk > 0.72 * vhpK) {
        var t = clamp((vk - 0.72 * vhpK) / (0.28 * vhpK), 0, 1), blend = t * t;
        mu = mu * (1.0 - blend) + CAL.muHydroplane * blend;
      }
    }
    return Math.max(0.03, mu);
  }

  // Parim voimalik kiirendus 0 -> v0 samal pinnal: kogu haare veole,
  // ohutakistus arvestamata. Alahinnang, seega tugev argument.
  function accelToSpeed(tyre, veh, cond) {
    var vTarget = cond.speedKmh / 3.6;
    if (vTarget <= 0.05) return { t: 0, s: 0, ok: true };
    var dt = 0.004, v = 0, s = 0, t = 0;
    while (v < vTarget && t < 300) {
      var mu = muAtSpeed(tyre, veh, cond, Math.max(v, 1.0));
      var a = Math.max(0.02, mu * G);
      v += a * dt;
      s += v * dt;
      t += dt;
    }
    return { t: t, s: s, ok: v >= vTarget - 1e-6 };
  }

  function stoppingDistance(tyre, veh, cond) {
    var warnings = [];
    var v0 = cond.speedKmh / 3.6;
    var mass = veh.kerbMassKg + cond.payloadKg;
    var slopeA = G * Math.sin(Math.atan(cond.gradientPct / 100.0));
    // Kruusal on ABS-i mõju vastupidine, vt absEffGravel.
    var eta = (cond.surface === 'GRAVEL' ? CAL.absEffGravel : CAL.absEff)[veh.absClass];
    var tBuild = CAL.brakeBuildup[veh.absClass];
    var brakeCond = cond.brakeCondition != null ? cond.brakeCondition : 1.0;

    var dt = 0.004, v = v0, s = 0, t = 0, peakA = 0, muSum = 0, muN = 0, brakeLimited = 0;
    var trace = [];
    while (v > 0.05 && t < 60) {
      var mu = muAtSpeed(tyre, veh, cond, v);
      muSum += mu; muN++;
      var ramp = tBuild > 0 ? clamp(t / tBuild, 0, 1) : 1;
      var aTyre = mu * G * eta;
      var aBrakeMax = veh.brakeCapacityG * brakeCond * G;
      if (aBrakeMax < aTyre) brakeLimited++;
      aTyre = Math.min(aTyre, aBrakeMax);
      var a = aTyre * ramp + 0.5 * RHO * veh.cdaM2 * v * v / mass + CAL.crr * G + slopeA;
      a = Math.max(0.05, a);
      if (a > peakA) peakA = a;
      if (muN % 25 === 1) trace.push([s, v * 3.6]);
      v -= a * dt;
      s += Math.max(0, v) * dt;
      t += dt;
    }
    trace.push([s, 0]);

    var muEff = muSum / Math.max(1, muN);
    var sReact = v0 * cond.reactionTimeS;

    var sigma = CAL.sigmaBase[cond.surface];
    if (ASPHALTISH[cond.surface] && cond.waterMm > 0.02) sigma = Math.hypot(sigma, CAL.sigmaWetExtra);
    // Märgise ebamäärasus ainult siis, kui G tuleb klassi keskpunktist,
    // mitte päris testist. Vt model.py Tyre.g_source.
    if (tyre.gSource !== 'test') sigma = Math.hypot(sigma, CAL.sigmaLabelOnly);

    // Lumi, mille kategooria taga on ainult üks test: Põhjamaade naelutu
    // (UTAC 2025, 5 rehvi) ja naast (Za Rulem 2024, 4 rehvi). Vt
    // model.py sigma_snow_single_source ja anchors_snow_nordic.py.
    if (SNOWISH[cond.surface] &&
        (tyre.category === 'WINTER_NORDIC' || tyre.category === 'WINTER_STUDDED')) {
      sigma = Math.hypot(sigma, CAL.sigmaSnowSingleSource);
    }

    // Tekstuur: ükski ankur ei varieeri seda. Vt model.py sigma_texture.
    if (cond.texture !== 'NORMAL' && ASPHALTISH[cond.surface]) {
      sigma = Math.hypot(sigma, CAL.sigmaTexture);
    }

    // Sula lumi: mudeli kõige nõrgem koht (vt model.py snow_temp_curve)
    if (SNOWISH[cond.surface] && cond.tempC > CAL.snowWarmFromC) {
      var wramp = clamp((cond.tempC - CAL.snowWarmFromC) / 3.0, 0, 1);
      sigma = Math.hypot(sigma, CAL.sigmaSnowWarm * wramp);
      warnings.push('Lumi nulli lähedal on mudeli kõige ebakindlam koht. Haaret ei ' +
        'määra siin mitte termomeeter, vaid see, kas pinnakihis on vaba vett — ja ' +
        'seda kalkulaator ei küsi. Kuiv tallatud lumi -1 °C juures ja sama lumi ' +
        'päikese käes sulamas erinevad rohkem kui kogu see temperatuurikõver.');
    }

    var gap = sizeGapInch(tyre.size, veh.oemSize);
    if (gap > 0) {
      sigma = Math.hypot(sigma, Math.min(CAL.sigmaSizeRimInch * gap, CAL.sigmaSizeMax));
      if (gap >= CAL.sizeWarnInch) {
        warnings.push('Rehvi andmed on mõõdust ' + tyre.size + ', auto tehasemõõt on ' +
          veh.oemSize + ' — ' + gap.toFixed(0) + ' tolli vahet. Märghaardumise klass on ' +
          'mõõdupõhine, nii et see on ülekanne teiselt mõõdult, mitte selle mõõdu ' +
          'mõõtmine. Kontrolli ka, kas see rehv sellele autole üldse sobib.');
      }
    }

    if (cond.tempC < -25 || cond.tempC > 45 || cond.waterMm > 5.0) {
      sigma = Math.hypot(sigma, CAL.sigmaExtrapolation);
      warnings.push('Temperatuur või veekile on väljaspool valideeritud vahemikku — ' +
                    'tulemus on ekstrapolatsioon.');
    }
    var rng = CAL.speedRange[cond.surface], loV = rng[0], hiV = rng[1];
    if (hiV <= 0) {
      sigma = Math.hypot(sigma, CAL.sigmaExtrapolation);
    } else if (cond.speedKmh > hiV) {
      var f = cond.speedKmh / hiV;
      sigma = Math.hypot(sigma, Math.min(CAL.sigmaSpeedExtrap * (f - 1),
                                         CAL.sigmaSpeedExtrapMax));
      warnings.push(Math.round(cond.speedKmh) + ' km/h on sellel pinnal ekstrapolatsioon: ' +
        'mudeli mõõdetud ankrud ulatuvad ' + Math.round(hiV) + ' km/h-ni. ' +
        'Pidurdusmaa kasvab kiiruse RUUDUS, nii et viga kasvab kiiresti.');
    } else if (cond.speedKmh < loV) {
      sigma = Math.hypot(sigma, CAL.sigmaSpeedExtrap * (loV / Math.max(1, cond.speedKmh) - 1));
    }

    var vhp = hydroplaneSpeedKmh(tyre, veh, cond), hpRisk = 0;
    if (vhp) {
      hpRisk = clamp((cond.speedKmh - 0.72 * vhp) / (0.28 * vhp), 0, 1);
      if (hpRisk > 0.05) sigma = Math.hypot(sigma, 0.10 + 0.25 * hpRisk);
      if (hpRisk > 0.5) {
        warnings.push('Akvaplaneerimise oht: hinnanguline lävi ~' + Math.round(vhp) +
          ' km/h. Sellises olukorras pole pidurdusmaa enam usaldusväärselt ennustatav.');
      } else if (hpRisk > 0.05) {
        warnings.push('Lähened akvaplaneerimise lävele (~' + Math.round(vhp) + ' km/h).');
      }
    }

    var summerish = tyre.category === 'SUMMER_UHP' || tyre.category === 'SUMMER_TOURING';
    if (summerish && cond.tempC < 7) {
      warnings.push('Suverehv alla +7 °C: kummisegu on kõva, haare langeb kiiresti.');
    }
    if ((cond.surface === 'ICE' || SNOWISH[cond.surface]) && summerish) {
      warnings.push('Suverehv lumel/jääl — tulemus on orienteeruv ja reaalne käitumine on ettearvamatu.');
    }
    if (tyre.treadDepthMm < 1.6) warnings.push('Mustrisügavus alla seadusliku 1,6 mm.');
    var acc = accelToSpeed(tyre, veh, cond);
    var extreme = (s > 150.0) || (!acc.ok) || (acc.s > 400.0);
    if (s > 150.0) {
      warnings.push('Füüsika äärmus: ' + Math.round(s) + ' m on pikem kui nähtavus ' +
        'enamikul teedel. Number on matemaatiliselt õige — pidurdusmaa kasvab kiiruse ' +
        'ruudus — aga see kirjeldab pigem suletud ala või jäärada kui tavalist liiklust.');
    }
    if (!acc.ok) {
      warnings.push('Sellel pinnal ei jõuaks auto ' + Math.round(cond.speedKmh) +
        ' km/h-ni ka siis, kui kogu rehvi haare läheks veole: ratas kaotaks haarde enne. ' +
        'Sama haare, mis piirab pidurdamist, piirab ka kiirendamist.');
    } else if (acc.s > 400.0) {
      warnings.push('Hoovõtt: ' + Math.round(cond.speedKmh) + ' km/h-ni jõudmine võtaks ' +
        'sellel pinnal parimal juhul ' + Math.round(acc.t) + ' s ja ' + Math.round(acc.s) +
        ' m. Tavateel sellist hoovõtumaad ei ole, pikal jäärajasirgel on.');
    }

    var brakeFrac = brakeLimited / Math.max(1, muN), limiter;
    if (brakeFrac > 0.5) {
      limiter = 'pidurid';
      warnings.push('Pidurid ei suuda rehvi haaret ära kasutada — piirajaks on ' +
        'pidurisüsteem, mitte rehv. Parem rehv siin ei aitaks.');
    } else if (brakeFrac > 0.05) { limiter = 'rehv (osaliselt pidurid)'; }
    else { limiter = 'rehv'; }

    var conf = sigma <= 0.10 ? 'kõrge' : (sigma <= 0.16 ? 'keskmine' : 'madal');

    /* USALDUSE LAGI: ülekanne ei ole mõõtmine. Kui rehvi haardenumber
       tuleb teisest mõõdust kui auto tehasemõõt, ei tohi leht öelda
       "kõrge" -- see täht tuleks valideerimata liikme pealt. Number ise
       ei muutu, muutub ainult toon. Vt model.py pikemat selgitust. */
    if (gap >= CAL.sizeWarnInch && conf === 'kõrge') conf = 'keskmine';

    /* Sama lagi märgiselt tulnud G-le: see arv kirjeldab KLASSI, mitte
       seda rehvi. Vt model.py pikemat selgitust. */
    if (tyre.gSource !== 'test' && conf === 'kõrge') conf = 'keskmine';

    return {
      distanceM: s,
      totalDistanceM: s + sReact,
      reactionM: sReact,
      sigmaRel: sigma,
      lowM: (s + sReact) * (1 - sigma),
      highM: (s + sReact) * (1 + sigma),
      muEffective: muEff,
      peakDecelG: peakA / G,
      timeS: t + cond.reactionTimeS,
      hydroplaneSpeedKmh: vhp,
      hydroplaneRisk: hpRisk,
      limiter: limiter,
      confidence: conf,
      warnings: warnings,
      accelTimeS: acc.t,
      accelDistM: acc.s,
      accelReachable: acc.ok,
      extreme: extreme,
      trace: trace
    };
  }

  root.Pidurdus = {
    CAL: CAL,
    muAtSpeed: muAtSpeed,
    hydroplaneSpeedKmh: hydroplaneSpeedKmh,
    stoppingDistance: stoppingDistance
  };
})(typeof globalThis !== 'undefined' ? globalThis : this);
