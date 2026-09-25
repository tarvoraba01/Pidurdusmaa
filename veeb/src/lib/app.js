/* Pidurdusmaa.ee — kasutajaliides.
 *
 * Arvutus: window.Pidurdus (assets/js/engine.js), SAMA mootor, mis on
 * pidurdus/model.py port ja mille paarsust kontrollib pidurdus/parity.py.
 * Siin ei ole ühtegi füüsikakonstanti — ainult andmete sidumine ja kuvamine.
 *
 * Andmed: data/core.json (autod, testitud rehvid, allikad) ja
 * data/eprel/<MÕÕT>.json (EL-i rehvimärgis ühes mõõdus, laetakse vajadusel).
 *
 * AUSUSE REEGLID, mida see fail järgib:
 *  - Märgisega rehvid on mudelis teada ainult KLASSI järgi. Sama klassi
 *    rehve ei näidata eraldi ribadena (nad oleksid identsed) — neid
 *    näidatakse klassi reana, arvuga.
 *  - Kuival, lumel ja jääl ei ütle märgis midagi. Seal on eraldi read
 *    ainult testitud rehvidel, kellel see pind on päriselt mõõdetud.
 *  - Omadusi, mille kohta usaldusväärseid andmeid ei ole (juhitavus,
 *    kulumine, hind), lehel ei näidata — ei arvata ega pakuta valikuks.
 */
(function () {
  'use strict';

  var CFG = window.PM_CFG || {};
  /* Märgise klassi esindusväärtus. Nominaalne keskpunkt on varuvariant;
     kui sellest klassist ja rehvitüübist on mõõdetud rehve (core.gClass,
     vt pidurdus/kalibreeri_gklass.py), kasutame nende MEDIAANI. Ilma
     selleta paistaks rida "märgise klass A" parem kui päris testitud
     A-klassi rehvid, sest nominaalne 1,60 on nende mõõdetud tasemest üle. */
  var GNOM = { A: 1.60, B: 1.47, C: 1.32, D: 1.17, E: 1.05 };
  function gmid(g, cat) {
    var t = (core && core.gClass && core.gClass[g]) || null;
    if (t) {
      if (cat && t[cat]) return t[cat][0];
      if (t._ && t._[1]) return t._[0];
    }
    return GNOM[g];
  }
  /* mitu mõõdetud rehvi selle klassi väärtuse taga on (0 = nominaalne) */
  function gmidN(g, cat) {
    var t = (core && core.gClass && core.gClass[g]) || null;
    if (!t) return 0;
    if (cat && t[cat]) return t[cat][1];
    return t._ ? t._[1] : 0;
  }
  var GMID = GNOM;
  var EKAT = ['SUMMER_TOURING', 'ALL_SEASON', 'WINTER_CENTRAL', 'WINTER_NORDIC'];
  var CATNAME = {
    SUMMER_UHP: 'Suverehv (sportlik)', SUMMER_TOURING: 'Suverehv', ALL_SEASON: 'Aastaringne rehv',
    WINTER_CENTRAL: 'Talverehv (Kesk-Euroopa)', WINTER_NORDIC: 'Talverehv (Põhjamaade)', WINTER_STUDDED: 'Naastrehv'
  };
  /* NB: sama tabel on functions.php-s (PM_CONDS) ja metoodika tekstis. */
  var COND = {
    wet:  { surface: 'ASPHALT', waterMm: 1.0, tempC: 10, label: 'märg asfalt', short: 'Märg' },
    dry:  { surface: 'ASPHALT', waterMm: 0.0, tempC: 15, label: 'kuiv asfalt', short: 'Kuiv' },
    snow: { surface: 'SNOW_PACKED', waterMm: 0.0, tempC: -5, label: 'tallatud lumi', short: 'Lumi' },
    ice:  { surface: 'ICE', waterMm: 0.0, tempC: -5, label: 'jää', short: 'Jää' }
  };
  var SEASON = {
    summer: { label: 'Suvi', long: 'suverehvid', yks: 'suverehv', osa: 'suverehvi', tested: ['SUMMER_TOURING', 'SUMMER_UHP'], eprel: [0] },
    all:    { label: 'Aastaringne', long: 'aastaringsed rehvid', yks: 'aastaringne rehv', osa: 'aastaringset rehvi', tested: ['ALL_SEASON'], eprel: [1] },
    winter: { label: 'Talv', long: 'talverehvid', yks: 'talverehv', osa: 'talverehvi', tested: ['WINTER_CENTRAL', 'WINTER_NORDIC', 'WINTER_STUDDED'], eprel: [2, 3] }
  };
  var DEFAULT_VEH = 'vw_golf_8';
  var FLAG = { GUESS: 1, CONFLICT: 2, SNOW: 4, ICE: 8 };

  /* ------------------------------------------------------------ abivahendid */
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function fmt(n, d) { return (d == null ? n.toFixed(1) : n.toFixed(d)).replace('.', ','); }
  /* vahe protsendina parimast: alla 10 % ühe komakohaga, muidu täisarv */
  function pct(diff, base) {
    var v = 100 * diff / base;
    return '+' + (v < 10 ? fmt(v, 1) : String(Math.round(v))) + ' %';
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pretty(m) {
    var x = /^(\d{3})(\d{2})R(\d{2})(C?)$/.exec(m || '');
    return x ? x[1] + '/' + x[2] + ' R' + x[3] + x[4] : m;
  }
  function norm(s) { return String(s || '').toUpperCase().replace(/[^0-9A-Z]/g, ''); }
  function titleCase(s) {
    /* sama reegel mis PHP pm_title_case: kõik suurtähtedes -> 3+ tähega sõnad,
       muidu ainult 4+ tähega suurtähesõnad; mudelikoodid jäävad */
    var min = /[a-zõäöüšž]/.test(s) ? 4 : 3;
    return s.replace(new RegExp('(^|[^A-Za-zÕÄÖÜŠŽõäöüšž0-9])([A-ZÕÄÖÜŠŽ])([A-ZÕÄÖÜŠŽ]{' + (min - 1) + ',})(?![A-Za-zÕÄÖÜŠŽõäöüšž0-9])', 'g'),
      function (_, pre, a, b) { return pre + a + b.toLowerCase(); });
  }
  function grade(g) {
    return /^[A-E]$/.test(g || '') ? '<span class="gr ' + g + '">' + g + '</span>' : '<span class="gr x">–</span>';
  }
  /* Brauserisse jäetakse ainult kaks asja ja ainult selle vahelehe ajaks
     (sessionStorage — kaob, kui vaheleht suletakse): valitud auto ja
     võrdluskorv, et need lehtede vahel liikudes alles oleksid. Kiirust,
     teeolusid, küsimuste vastuseid jms ei salvestata üldse. */
  var store = {
    get: function (k, d) { try { var v = sessionStorage.getItem('pm_' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { sessionStorage.setItem('pm_' + k, JSON.stringify(v)); } catch (e) { /* privaatrežiim */ } }
  };
  /* vanad püsivad kirjed (varasemast versioonist) ära */
  try { ['calc', 'valik', 'pick', 'cmp'].forEach(function (k) { localStorage.removeItem('pm_' + k); }); } catch (e) { /* ei loe */ }

  /* ------------------------------------------------------------ kasutuslugu
     Salvestab ANONÜÜMSELT, MIDA lehel tehti: milline auto ja mõõt valiti,
     mitu korda arvutati, millised rehvid avati, mida otsiti. Nime, e-posti,
     IP-d ega küpsist siin ei ole ja midagi ei saadeta automaatselt kuhugi.
       - eelvaates (serverit pole): logi jääb ainult sellesse brauserisse ja
         kasutaja saab selle ise tagasisidega kaasa saata;
       - päris saidil: kui PM_CFG.track on seatud, saadetakse sündmused
         sellele aadressile kogumiks (sendBeacon), muidu mitte. */
  var Track = (function () {
    /* Logi on AINULT mälus. Brauserisse (localStorage) seda ei kirjutata:
       see oleks seadmesse salvestamine, mis EL-i reeglite järgi vajaks
       nõusolekut, ja siin ei ole selleks vajadust — serverisse läheb
       sündmus niikuinii kohe. Vana eelvaate-versiooni kirje koristatakse. */
    var MAX = 400, log = [], t0 = Date.now(), jarjekord = [], ajastus = null;
    try { localStorage.removeItem('pm_log'); } catch (e) { /* ei loe */ }
    function salvesta() { /* ainult mälus, vt ülal */ }
    function saada() {
      ajastus = null;
      if (!CFG.track || !jarjekord.length) { jarjekord = []; return; }
      var pakk = jarjekord; jarjekord = [];
      try {
        var b = new Blob([JSON.stringify({ e: pakk })], { type: 'application/json' });
        if (navigator.sendBeacon) navigator.sendBeacon(CFG.track, b);
        else fetch(CFG.track, { method: 'POST', body: b, keepalive: true });
      } catch (e) { /* statistika ei tohi kunagi lehte katki teha */ }
    }
    function t(nimi, vaartus) {
      var rida = { s: Math.round((Date.now() - t0) / 1000), e: nimi };
      if (vaartus != null && vaartus !== '') rida.v = String(vaartus).slice(0, 120);
      var v = log[log.length - 1];
      if (v && v.e === rida.e && v.v === rida.v && rida.s - v.s < 3) { v.s = rida.s; return; }
      log.push(rida);
      if (log.length > MAX) log.splice(0, log.length - MAX);
      salvesta();
      jarjekord.push(rida);
      if (CFG.track && !ajastus) ajastus = setTimeout(saada, 4000);
      ga4(rida);
    }
    /* Sama sündmus ka Google Analyticsisse — AINULT siis, kui külastaja on
       küpsistega nõustunud (window.PM_GA on olemas ainult pärast nõusolekut,
       vt Nousolek.svelte). Otsing läheb GA4 soovitatud nimega "search", siis
       ilmub ta GA4 aruannetesse ise; ülejäänud on oma nimedega.
       "leht" jäetakse välja — lehevaatamise saadab GA ise (page_view). */
    /* Iga sündmuse väärtus läheb GA-sse ka OMA NIMEGA parameetrina (auto,
       moot, kiirus, teeolu …), et GA-s saaks igaühe jaoks eraldi
       dimensiooni teha. `vaartus` jääb lisaks kõigile alles.
       GA4 piirang: parameetri väärtus kuni 100 märki. */
    var GA_SILDID = {
      drive: { city: 'Linnas', road: 'Maanteel', hwy: 'Kiirteel', mix: 'Linn + maantee' },
      km: { lo: 'alla 10 000 km', mid: '10–20 000 km', hi: '20–30 000 km', vhi: 'üle 30 000 km' },
      main: { safe: 'Ohutus märjal', brake: 'Lühike pidurdusmaa', quiet: 'Vaikne sõit', fuel: 'Väike kütusekulu', winter: 'Talvised omadused' }
    };
    var GA_KRIT = { drive: 'soidukoht', km: 'labisoit', main: 'tahtsaim' };
    function gaParam(r) {
      var v = String(r.v || ''), p = {};
      switch (r.e) {
        case 'auto': p.auto = v; break;
        case 'moot':
          p.moot = v.replace(/ \(.*\)$/, '');
          if (/\(tehase\)/.test(v)) p.tehasemoot = 'jah';
          else if (/\(EI OLE tehase\)/.test(v)) p.tehasemoot = 'ei';
          break;
        case 'arvuta': {
          var o = v.split(' · ');            // auto · mõõt · 90 km/h · teeolu
          p.auto = o[0] || ''; p.moot = o[1] || '';
          p.kiirus = String(parseInt(o[2], 10) || ''); p.teeolu = o[3] || '';
          break;
        }
        case 'pind': p.teeolu = v; break;
        case 'hooaeg': p.hooaeg = v; break;
        case 'kriteerium': {
          var g = v.split('=')[0], val = v.slice(g.length + 1);
          var sildid = GA_SILDID[g] || {};
          var tekst = val ? val.split('+').map(function (x) { return sildid[x] || x; }).join(' + ') : '(tühi)';
          if (GA_KRIT[g]) p[GA_KRIT[g]] = tekst;
          break;
        }
        case 'margifilter': p.mark = v; break;
        case 'vordlusse': case 'vordlusest_ara': p.rehv = v; break;
        case 'vaheleht': p.vaheleht = v; break;
      }
      if (v) p.vaartus = v;
      for (var k in p) p[k] = String(p[k]).slice(0, 100);
      return p;
    }
    function ga4(r) {
      if (typeof window.PM_GA !== 'function' || r.e === 'leht') return;
      try {
        if (r.e === 'otsing') window.PM_GA('search', { search_term: String(r.v || '').split(' → ')[0].slice(0, 100) });
        else window.PM_GA(r.e.slice(0, 40), gaParam(r));
      } catch (e) { /* statistika ei tohi lehte katki teha */ }
    }
    t.log = function () { return log.slice(); };
    t.t0 = function () { return t0; };
    t.clear = function () { log = []; t0 = Date.now(); salvesta(); };
    return t;
  })();
  window.PM_TRACK = Track;

  /* ------------------------------------------------------------ andmed */
  var core = null, sizeCache = {};
  function loadCore() {
    if (core) return Promise.resolve(core);
    return fetch(CFG.data + 'core.json?v=' + encodeURIComponent(CFG.ver || ''), { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        core = d;
        core.vehByKey = {};
        d.vehicles.forEach(function (v) { core.vehByKey[v.key] = v; });
        core.tyreByKey = {};
        d.tyres.forEach(function (t) { core.tyreByKey[t.key] = t; });
        return core;
      });
  }
  function loadSize(m) {
    if (!m) return Promise.resolve([]);
    if (sizeCache[m]) return Promise.resolve(sizeCache[m]);
    if (core && core.eprelSizes.indexOf(m) < 0) return Promise.resolve(sizeCache[m] = []);
    return fetch(CFG.data + 'eprel/' + m + '.json?v=' + encodeURIComponent(CFG.ver || ''))
      .then(function (r) { return r.ok ? r.json() : []; })
      .catch(function () { return []; })
      .then(function (rows) {
        /* [slug, mark, nimi, katNr, märg, kütus, dB, müraKl, lipud, testKey] */
        sizeCache[m] = rows.map(function (r) {
          return { slug: r[0], mark: titleCase(r[1]), name: titleCase(r[2]), cat: EKAT[r[3]], catNr: r[3],
                   g: r[4], f: r[5], db: r[6], nk: r[7], flags: r[8], tested: r[9], m: m };
        });
        return sizeCache[m];
      });
  }

  /* Mootori rehviobjekt EPREL-i reast: G = klassi esindusväärtus, gSource 'label'. */
  function eprelTyre(r) {
    return { key: 'e:' + r.slug + '@' + r.m, name: r.mark + ' ' + r.name, category: r.cat,
             wetGripIndex: gmid(r.g, r.cat) || gmid('C', r.cat), treadDepthMm: 8, treadDepthNewMm: 8,
             pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: false,
             size: pretty(r.m), gSource: 'label' };
  }
  function classTyre(g, cat, m) {
    return { key: 'c:' + g + cat, name: 'Klass ' + g, category: cat, wetGripIndex: gmid(g, cat),
             treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null,
             ageYears: 1, studded: false, size: pretty(m), gSource: 'label' };
  }
  function condObj(ck, speed) {
    var c = COND[ck];
    return { speedKmh: speed, surface: c.surface, texture: 'NORMAL', waterMm: c.waterMm, tempC: c.tempC,
             payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1 };
  }
  function calc(tyre, veh, cond) { return window.Pidurdus.stoppingDistance(tyre, veh, cond); }

  /* ------------------------------------------------------------ võrdluskorv */
  var cmp = {
    list: function () { return store.get('cmp', []); },
    has: function (id) { return cmp.list().some(function (x) { return x.id === id; }); },
    toggle: function (item) {
      var l = cmp.list(), i = l.findIndex(function (x) { return x.id === item.id; });
      if (i >= 0) l.splice(i, 1);
      else { if (l.length >= 4) l.shift(); l.push(item); }
      store.set('cmp', l); cmp.paint(); return i < 0;
    },
    set: function (l) { store.set('cmp', l.slice(0, 4)); cmp.paint(); },
    paint: function () {
      var n = cmp.list().length;
      $$('[data-cmp-n]').forEach(function (e) { e.textContent = n; });
      $$('[data-cmp-pill]').forEach(function (e) { e.classList.toggle('has', n > 0); });
      document.dispatchEvent(new CustomEvent('pm:cmp'));
    }
  };

  /* ------------------------------------------------------------ päis */
  function initHeader() {
    var b = $('[data-burger]'), panel = $('#pm-panel');
    if (b && panel) b.addEventListener('click', function () {
      panel.hidden = !panel.hidden;
      b.setAttribute('aria-expanded', panel.hidden ? 'false' : 'true');
    });
    $$('[data-dd]').forEach(function (dd) {
      var btn = $('.dd-btn', dd);
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = dd.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      /* klaviatuur: kui fookus lahkub menüüst, sulgeme selle */
      dd.addEventListener('focusout', function (e) {
        if (!dd.contains(e.relatedTarget)) { dd.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
      });
    });
    document.addEventListener('click', function (e) {
      $$('[data-dd].open').forEach(function (dd) { if (!dd.contains(e.target)) { dd.classList.remove('open'); $('.dd-btn', dd).setAttribute('aria-expanded', 'false'); } });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      $$('[data-dd].open').forEach(function (dd) { dd.classList.remove('open'); $('.dd-btn', dd).focus(); });
      if (panel && !panel.hidden) { panel.hidden = true; b.setAttribute('aria-expanded', 'false'); }
    });
    cmp.paint();
    $$('[data-cmp-pill]').forEach(function (a) {
      a.addEventListener('click', function () {
        var l = cmp.list();
        if (!l.length) return;
        a.href = cmpUrl(l);
      });
    });
  }
  /* navigeerimine; eelvaates (ühe faili sait) annab ruuter oma PM_NAV-i */
  function nav(u) { if (window.PM_NAV) window.PM_NAV(u); else location.href = u; }
  function cmpUrl(l, extra) {
    var q = [];
    if (l && l.length) q.push('rehvid=' + l.map(function (x) { return x.id; }).join(','));
    if (extra) Object.keys(extra).forEach(function (k) { if (extra[k]) q.push(k + '=' + encodeURIComponent(extra[k])); });
    return CFG.home + 'vordle-rehve/' + (q.length ? '?' + q.join('&') : '');
  }

  /* ------------------------------------------------------------ auto valija
     Mark → mudel → aasta/põlvkond → mootor/variant. Andmebaasis on üks rida
     põlvkonna kohta; kui valikuid on üks, valitakse ta ise. */
  function VehPicker(root, onChange) {
    var sel = {
      make: $('[data-f=make]', root), model: $('[data-f=model]', root),
      year: $('[data-f=year]', root), variant: $('[data-f=variant]', root)
    };
    var V = core.vehicles;
    function opts(el, list, ph) {
      el.innerHTML = '<option value="">' + esc(ph) + '</option>' + list.map(function (o) {
        return '<option value="' + esc(o[0]) + '">' + esc(o[1]) + '</option>';
      }).join('');
      el.disabled = !list.length;
      if (list.length === 1) el.value = list[0][0];
    }
    function uniq(arr) { var s = {}; return arr.filter(function (x) { return s[x[0]] ? false : (s[x[0]] = 1); }); }
    var GEN = 'Ei leia oma autot';
    var makes = uniq(V.map(function (v) { return [v.make, v.make]; })).filter(function (m) { return m[0] !== GEN; })
      .sort(function (a, b) { return a[1].localeCompare(b[1], 'et'); });
    /* üldised tüüpautod nimekirja lõppu, selge sildiga */
    if (V.some(function (v) { return v.make === GEN; })) makes.push([GEN, '— Ei leia oma autot? Vali tüüp —']);
    opts(sel.make, makes, 'Vali mark');
    sel.make.value = '';
    function fill(from) {
      var mk = sel.make.value, md = sel.model.value, yr = sel.year.value;
      if (from === 'make') {
        var models = uniq(V.filter(function (v) { return v.make === mk; }).map(function (v) { return [v.model, v.model]; }))
          .sort(function (a, b) { return a[1].localeCompare(b[1], 'et', { numeric: true }); });
        opts(sel.model, mk ? models : [], mk ? 'Vali mudel' : '—');
        md = sel.model.value; from = 'model';
      }
      if (from === 'model') {
        var yrs = uniq(V.filter(function (v) { return v.make === mk && v.model === md; }).map(function (v) { return [v.yearLabel, v.yearLabel]; }));
        opts(sel.year, md ? yrs : [], md ? 'Vali aasta' : '—');
        yr = sel.year.value; from = 'year';
      }
      if (from === 'year') {
        var vars = V.filter(function (v) { return v.make === mk && v.model === md && v.yearLabel === yr; })
          .map(function (v) { return [v.key, v.variant === '—' ? 'Standard' : v.variant]; });
        opts(sel.variant, yr ? vars : [], yr ? 'Vali variant' : '—');
      }
      onChange(sel.variant.value || null);
    }
    sel.make.addEventListener('change', function () { fill('make'); });
    sel.model.addEventListener('change', function () { fill('model'); });
    sel.year.addEventListener('change', function () { fill('year'); });
    sel.variant.addEventListener('change', function () { onChange(sel.variant.value || null); });
    return {
      set: function (key) {
        var v = core.vehByKey[key]; if (!v) return;
        sel.make.value = v.make; fill('make');
        sel.model.value = v.model; fill('model');
        sel.year.value = v.yearLabel; fill('year');
        sel.variant.value = v.key; onChange(v.key);
      }
    };
  }

  function sizeOptions(el, veh, current) {
    var oem = veh ? norm(veh.oemSize) : null;
    var fab = veh && veh.oemSizes && veh.oemSizes.length ? veh.oemSizes.map(norm) : (oem ? [oem] : []);
    var list = core.sizes.filter(function (s) { return s.n >= 5; }).slice()
      .sort(function (a, b) { return a.label.localeCompare(b.label, 'et', { numeric: true }); });
    var h = '';
    if (fab.length) {
      /* KÕIK selle põlvkonna tehasemõõdud, mitte ainult üks: enamikul
         autodel on neid 2-4 ja kasutaja teab oma oma rehvi küljelt. */
      h += '<optgroup label="' + esc(veh.model + ' tehasemõõdud') + '">' + fab.map(function (m) {
        var known = core.eprelSizes.indexOf(m) >= 0;
        return '<option value="' + esc(m) + '">' + esc(pretty(m)) + (m === oem ? ' · levinuim' : '') +
          (known ? '' : ' (märgise andmed puuduvad)') + '</option>';
      }).join('') + '</optgroup>';
    }
    h += '<optgroup label="' + (fab.length ? 'Muu mõõt' : 'Rehvimõõt') + '">' + list.filter(function (s) { return fab.indexOf(s.m) < 0; }).map(function (s) {
      return '<option value="' + esc(s.m) + '">' + esc(s.label) + ' · ' + s.n + ' rehvi</option>';
    }).join('') + '</optgroup>';
    el.innerHTML = h;
    el.value = current && $('option[value="' + current + '"]', el) ? current : (oem || '20555R16');
    return el.value;
  }

  /* ------------------------------------------------------------ kalkulaator */
  function initCalc(root) {
    var S = { veh: store.get('veh', null), size: '20555R16', speed: 90, cond: 'wet', season: 'summer' };
    S.tab = 'calc';
    var qsc = new URLSearchParams(location.search);
    if (qsc.get('moot')) S.size = qsc.get('moot');
    var sizeSel = $('[data-f=size]', root), sizeTag = $('[data-size-tag]', root);
    var speedIn = $('[data-f=speed]', root), speedNum = $('[data-f=speednum]', root), capNote = $('[data-cap-note]', root);
    /* auto ja mõõt on kaardi mõlemal vahelehel ühised — avalehe rehvide
       nimekiri (initTyres välises režiimis) kuulab neid siit */
    var bus = [];
    function emit() { bus.forEach(function (f) { f({ veh: S.veh, size: S.size }); }); }
    root.pmBus = { get: function () { return { veh: S.veh, size: S.size }; }, on: function (f) { bus.push(f); } };
    /* Tulemus tekib ALLES nupuvajutusega („Arvuta pidurdusmaa“) ja muutub
       nähtavalt ainult uue vajutusega. Valikute muutmisel laetakse andmed
       taustal ette ja nupp ütleb „Arvuta uuesti“ — ekraanil olev tulemus
       vastab alati sellele, mille eest nuppu vajutati. */
    var shown = false, goBtn = $('[data-go]', root), goMsg = $('[data-go-msg]', root);
    function goLabel(t) { goBtn.innerHTML = t + ' <span class="arr" aria-hidden="true">→</span>'; }
    function recalc() {
      loadSize(S.size);
      if (goMsg && S.veh) goMsg.hidden = true;
      if (shown) { goLabel('Arvuta uuesti'); goBtn.classList.add('stale'); }
    }

    var picker = VehPicker(root, function (key) {
      S.veh = key;
      var veh = key ? core.vehByKey[key] : null;
      if (veh) Track('auto', veh.make + ' ' + veh.model + ' ' + veh.yearLabel);
      S.size = sizeOptions(sizeSel, veh, veh && !qsc.get('moot') ? norm(veh.oemSize) : S.size);
      qsc.delete('moot');
      paintSize(); save(); recalc(); emit();
      $('[data-veh-hint]', root).textContent = veh ? 'levinuim tehasemõõt ' + veh.oemSize : '';
    });
    S.size = sizeOptions(sizeSel, null, S.size);

    function paintSize() {
      var veh = S.veh ? core.vehByKey[S.veh] : null;
      sizeTag.hidden = !veh;
      if (veh) {
        var fab = (veh.oemSizes && veh.oemSizes.length ? veh.oemSizes.map(norm) : [norm(veh.oemSize)]);
        var on = fab.indexOf(S.size) >= 0;
        sizeTag.textContent = on ? '✓ Tehasemõõt' : 'Ei ole selle auto tehasemõõt (tehases: ' + fab.map(pretty).join(', ') + ')';
        sizeTag.className = 'size-note' + (on ? '' : ' warn');
      }
    }
    sizeSel.addEventListener('change', function () {
      S.size = sizeSel.value;
      var vv = S.veh ? core.vehByKey[S.veh] : null;
      var fb = vv ? (vv.oemSizes && vv.oemSizes.length ? vv.oemSizes.map(norm) : [norm(vv.oemSize)]) : [];
      Track('moot', pretty(S.size) + (vv ? (fb.indexOf(S.size) >= 0 ? ' (tehase)' : ' (EI OLE tehase)') : ''));
      paintSize(); save(); recalc(); emit();
    });

    function range() {
      var rng = window.Pidurdus.CAL.speedRange[COND[S.cond].surface] || [20, 130];
      return [Math.max(20, Math.ceil(rng[0] / 5) * 5), Math.floor(rng[1] / 5) * 5];
    }
    function paintSpeed() {
      var r = range(), lo = r[0], hi = r[1];
      var capped = S.speed > hi || S.speed < lo;
      S.speed = Math.min(hi, Math.max(lo, S.speed));
      speedIn.min = lo; speedIn.max = hi; speedNum.min = lo; speedNum.max = hi;
      speedIn.value = S.speed; speedNum.value = S.speed;
      speedIn.style.setProperty('--p', (100 * (S.speed - lo) / (hi - lo)) + '%');
      capNote.hidden = !capped && !(S.cond === 'snow' || S.cond === 'ice');
      if (!capNote.hidden) capNote.textContent = (S.cond === 'snow' || S.cond === 'ice')
        ? 'Lumel ja jääl arvutame ' + lo + '–' + hi + ' km/h — kiiremini ei ole mõõdetud andmeid.'
        : 'Sellel pinnal arvutame ' + lo + '–' + hi + ' km/h.';
    }
    speedIn.addEventListener('input', function () { S.speed = +speedIn.value; paintSpeed(); save(); recalc(); });
    speedNum.addEventListener('change', function () {
      var v = Math.round((+speedNum.value || S.speed) / 5) * 5;
      S.speed = v; paintSpeed(); save(); recalc();
    });
    $$('[data-cond]', root).forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.cond === S.cond ? 'true' : 'false');
      b.addEventListener('click', function () {
        S.cond = b.dataset.cond;
        Track('pind', COND[S.cond].label);
        $$('[data-cond]', root).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        paintSpeed(); save(); recalc();
      });
    });
    paintSpeed();

    /* režiimid */
    $$('[data-tab]', root).forEach(function (t) {
      t.addEventListener('click', function () { setTab(t.dataset.tab); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { var o = t.dataset.tab === 'calc' ? 'valik' : 'calc'; setTab(o); $('[data-tab=' + o + ']', root).focus(); }
      });
    });
    function setTab(tab) {
      S.tab = tab;
      Track('vaheleht', tab === 'valik' ? 'rehvi valimine' : 'kalkulaator');
      $$('[data-tab]', root).forEach(function (x) { x.setAttribute('aria-selected', x.dataset.tab === tab ? 'true' : 'false'); x.tabIndex = x.dataset.tab === tab ? 0 : -1; });
      $('#p-calc', root).hidden = tab !== 'calc';
      $('#p-valik', root).hidden = tab !== 'valik';
      /* avalehe alumine osa: kalkulaatori tulemus + info VÕI sobivad rehvid */
      $$('[data-home]').forEach(function (x) { x.hidden = x.dataset.home !== tab; });
    }
    function smooth() { return matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'; }
    var goV = $('[data-go-valik]', root);
    if (goV) goV.addEventListener('click', function () {
      var t = $('#sobivad'); if (t) t.scrollIntoView({ behavior: smooth(), block: 'start' });
    });
    /* tulemuse riba nupp „Rehvi valimine“ avab avalehel sama vahelehe */
    var rv = $('[data-r-valik]');
    if (rv) rv.addEventListener('click', function (e) {
      e.preventDefault(); setTab('valik');
      root.scrollIntoView({ behavior: smooth(), block: 'start' });
    });

    function save() { store.set('veh', S.veh); }

    function compute(force) {
      if (!S.veh && !force) {
        Track('arvuta_ilma_autota');
        if (goMsg) goMsg.hidden = false;
        var mk = $('[data-f=make]', root); if (mk) mk.focus();
        return;
      }
      if (goMsg) goMsg.hidden = true;
      var av = S.veh ? core.vehByKey[S.veh] : null;
      Track('arvuta', (av ? av.make + ' ' + av.model : 'tüüpauto') + ' · ' + pretty(S.size) + ' · ' + S.speed + ' km/h · ' + COND[S.cond].label);
      loadSize(S.size).then(function (rows) {
        Result.show(Object.assign({}, S), rows);
        shown = true; goLabel('Arvuta pidurdusmaa'); goBtn.classList.remove('stale');
        var res = $('#tulemus');
        if (!res) return;
        res.hidden = false;
        var top = res.getBoundingClientRect().top;
        if (top > window.innerHeight - 160 || top < 0) {
          res.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
        }
        var big = $('[data-r-big]'); if (big) { big.parentNode.classList.remove('flash'); void big.offsetWidth; big.parentNode.classList.add('flash'); }
      });
    }
    var useDefault = false; /* kasutaja valis „arvuta tüüpilise auto järgi“ */
    goBtn.addEventListener('click', function () { compute(useDefault); });
    var goDef = $('[data-go-default]', root);
    if (goDef) goDef.addEventListener('click', function () { useDefault = true; compute(true); });

    if (S.veh && core.vehByKey[S.veh]) picker.set(S.veh); else recalc();
  }

  /* ------------------------------------------------------------ tulemus */
  var Result = (function () {
    var el, state, rowsAll, sel, showAll = false;
    function rowsFor(S, eprelRows, season) {
      var veh = core.vehByKey[S.veh] || core.vehByKey[DEFAULT_VEH];
      var cond = condObj(S.cond, S.speed), ck = S.cond, rows = [];
      var sea = SEASON[season];
      /* testitud rehvid */
      var eprelByTest = {};
      eprelRows.forEach(function (r) { if (r.tested) eprelByTest[r.tested] = r; });
      var collapsed = {};
      var hiddenOther = 0;
      core.tyres.forEach(function (t) {
        if (sea.tested.indexOf(t.category) < 0) return;
        /* Testitud rehv on SINU autole asjakohane ainult siis, kui seda mudelit
           müüakse sinu mõõdus (EPREL-is on rida) või test oligi selles mõõdus.
           18-tolline sportrehv 15-tollise auto tulemuste seas oleks eksitav. */
        var avail = !!eprelByTest[t.key] || norm(t.size) === S.size;
        if (!avail && !S.showOther) { hiddenOther++; return; }
        var measured = ck === 'wet' ? true : ck === 'dry' ? t.muDry != null : ck === 'snow' ? t.muSnow != null : t.muIce != null;
        if (!measured) { collapsed[t.category] = t; return; }
        var r = calc(t, veh, cond);
        var srcs = uniqSrc(t.tests), er = eprelByTest[t.key];
        rows.push({ id: 't:' + t.key, kind: 'test', name: t.name, d: r.distanceM, r: r, t: t, pids: er ? [er.slug + '@' + S.size] : [],
          sub: 'Sõltumatu test' + (srcs.length ? ' · ' + srcs.map(srcName).join(', ') : ''),
          sizeNote: norm(t.size) !== S.size ? t.size : null, label: er ? er.g : null, slug: t.slug, other: !avail });
      });
      /* märgis sinu mõõdus */
      var inSeason = eprelRows.filter(function (r) { return sea.eprel.indexOf(r.catNr) >= 0; });
      if (ck === 'wet') {
        var byCls = {};
        inSeason.forEach(function (r) { (byCls[r.cat + r.g] = byCls[r.cat + r.g] || []).push(r); });
        Object.keys(byCls).forEach(function (k) {
          var list = byCls[k], g = list[0].g, cat = list[0].cat;
          if (!GNOM[g]) return;
          var r = calc(classTyre(g, cat, S.size), veh, cond);
          rows.push({ id: 'c:' + k, kind: 'class', g: g, cat: cat, n: list.length, d: r.distanceM, r: r, members: list,
            pids: list.map(function (x) { return x.slug + '@' + S.size; }),
            name: 'Märgise klass ' + g + (sea.eprel.length > 1 ? ' · ' + (cat === 'WINTER_NORDIC' ? 'Põhjamaade' : 'Kesk-Euroopa') : ''),
            sub: list.length + ' rehvimudelit sinu mõõdus, nt ' + list.slice(0, 2).map(function (x) { return x.mark + ' ' + x.name; }).join(', ') });
        });
      } else {
        /* märgis ei ütle kuiva/lume/jää kohta midagi: üks kategooria keskmise rida */
        var cats = {};
        inSeason.forEach(function (r) { cats[r.cat] = (cats[r.cat] || 0) + 1; });
        Object.keys(collapsed).forEach(function (c) { if (!cats[c]) cats[c] = 0; });
        Object.keys(cats).forEach(function (c) {
          var r = calc(classTyre('C', c, S.size), veh, cond);
          rows.push({ id: 'k:' + c, kind: 'cat', cat: c, n: cats[c], d: r.distanceM, r: r, pids: [],
            name: CATNAME[c] + ' — kategooria keskmine',
            sub: (cats[c] ? cats[c] + ' märgisega rehvimudelit sinu mõõdus · ' : '') + 'märgis ei ütle ' + COND[ck].label + ' kohta midagi' });
        });
      }
      rows.sort(function (a, b) { return a.d - b.d; });
      return { rows: rows, veh: veh, cond: cond, vehDefault: !core.vehByKey[S.veh], nSeason: inSeason.length, hiddenOther: hiddenOther };
    }
    function uniqSrc(tests) { var s = []; (tests || []).forEach(function (x) { if (s.indexOf(x.src) < 0) s.push(x.src); }); return s; }
    function srcName(c) { var s = core.sources[c]; return s ? s.tegija.replace(/ \(.*\)/, '') + ' ' + s.aasta : c; }
    function defaultSel(rows) {
      var cls = rows.filter(function (r) { return r.kind === 'class'; });
      if (cls.length) return cls.slice().sort(function (a, b) { return b.n - a.n; })[0].id;
      var cat = rows.filter(function (r) { return r.kind === 'cat'; });
      if (cat.length) return cat[0].id;
      return rows.length ? rows[Math.floor(rows.length / 2)].id : null;
    }
    function show(S, eprelRows) {
      el = $('[data-result]');
      if (!el) return;
      /* hooaeg järgib teeolusid (lumi/jää -> talv), kuni kasutaja pole ise valinud */
      if (!S._userSeason) S.resSeason = (S.cond === 'snow' || S.cond === 'ice') ? 'winter' : 'summer';
      state = S; state._eprel = eprelRows;
      sel = null; showAll = false;
      render();
    }
    /* HINNAD tulemuses: iga rea juures odavaim hind (klassi real „alates“),
       valitud rea all müüjad linkidega. Andmed tulevad Prices.size()
       kaudu serverist; kui ühendust pole, öeldakse see üks kord. */
    function cheapest(pids, h) {
      var best = null;
      pids.forEach(function (id) { var r = h[id]; if (r && r.length && (!best || r[0].hind < best.hind)) best = { id: id, hind: r[0].hind, row: r[0] }; });
      return best;
    }
    function paintPrices(size, cur) {
      var box = $('[data-r-price]', el);
      Prices.size(size).then(function (d) {
        if (state.size !== size) return;
        var h = (d && d.hinnad) || {}, avail = !!(d && d.available);
        $$('[data-rp]').forEach(function (e) {
          var x = rowsAll.filter(function (r) { return r.id === e.dataset.rp; })[0], c = x && cheapest(x.pids || [], h);
          e.textContent = c ? (x.kind === 'class' ? 'al ' : '') + Math.round(c.hind) + ' €' : '';
          e.title = c ? (x.kind === 'class' ? 'Soodsaim selle klassi rehv: ' : 'Soodsaim hind: ') + eur(c.hind) : '';
        });
        var mb = $('[data-r-mbars]', el);
        if (mb) mb.classList.toggle('has-prices', !!$('.mbar .p:not(:empty)', mb));
        if (!box) return;
        if (!avail) { box.innerHTML = '<span class="pl">Hinnad müüjatelt</span> <span class="none">pole hetkel saadaval</span> ' + tip(PRICE_T); return; }
        if (cur.kind === 'test') {
          var id = (cur.pids || [])[0];
          box.innerHTML = '<span class="pl">' + esc(cur.name) + ' — hinnad</span>' + (id ? priceHtml(h[id], true) : '<span class="none">Seda rehvi sinu mõõdus müüjatelt ei leitud</span>');
        } else if (cur.kind === 'class') {
          var top = cur.members.map(function (m) { var id = m.slug + '@' + size; return h[id] && h[id].length ? { m: m, r: h[id][0] } : null; })
            .filter(Boolean).sort(function (a, b) { return a.r.hind - b.r.hind; }).slice(0, 3);
          box.innerHTML = '<span class="pl">Soodsaimad klassi ' + cur.g + ' rehvid</span>' + (top.length ? '<ul class="sellers">' + top.map(function (t) {
            return '<li><span><a href="' + CFG.home + 'rehvid/' + esc(t.m.slug) + '/">' + esc(t.m.mark + ' ' + t.m.name) + '</a> <small>' + esc(t.r.myyja) + '</small></span>' +
              (t.r.url ? '<a class="buy" href="' + esc(t.r.url) + '" target="_blank" rel="nofollow sponsored noopener">' + eur(t.r.hind) + '</a>' : '<b>' + eur(t.r.hind) + '</b>') + '</li>';
          }).join('') + '</ul>' : '<span class="none">Hindu selles klassis veel pole</span>');
        } else box.innerHTML = '<span class="pl">Hinnad</span> <span class="none">vali rehv, et näha müüjaid</span>';
      });
    }
    function row(x, best, max, compact) {
      var dd = x.d - best;
      if (compact) {
        var nm = x.kind === 'class' ? 'Märgise klass ' + x.g + ' (' + x.n + ' rehvi)' : x.kind === 'cat' ? (CATNAME[x.cat] + ', keskmine') : x.name;
        return '<li><button type="button" class="mbar" data-row="' + esc(x.id) + '" aria-pressed="' + (x.id === sel) + '" title="' + esc(x.sub || '') + '">' +
          '<span class="n">' + esc(nm) + '</span>' +
          '<span class="t" aria-hidden="true"><span style="width:' + (100 * x.d / max).toFixed(1) + '%"></span></span>' +
          '<span class="v">' + fmt(x.d) + ' m</span>' +
          '<span class="d">' + (dd < 0.05 ? '' : '+' + fmt(dd) + ' m <i>' + pct(dd, best) + '</i>') + '</span>' +
          '<span class="p" data-rp="' + esc(x.id) + '"></span></button></li>';
      }
      var sub = '<small>' + esc(x.sub) + (x.kind === 'test' && x.sizeNote ? ' · mõõt ' + esc(x.sizeNote) : '') + '</small>';
      var badge = x.kind === 'class' ? grade(x.g) : (x.label ? grade(x.label) : '');
      return '<li><button type="button" class="bar" data-row="' + esc(x.id) + '" aria-pressed="' + (x.id === sel) + '">' +
        '<span class="bn">' + badge + '<span>' + esc(x.name) + (x.other ? ' <small style="color:#92400e">· pole sinu mõõdus</small>' : '') + '<br>' + sub + '</span></span>' +
        '<span class="bd">' + fmt(x.d) + ' m<small class="bp" data-rp="' + esc(x.id) + '"></small></span>' +
        '<span class="bx' + (dd < 0.05 ? ' zero' : '') + '">' + (dd < 0.05 ? 'parim' : '+' + fmt(dd) + ' m<small>' + pct(dd, best) + '</small>') + '</span>' +
        '<span class="tr" aria-hidden="true"><span class="' + (x.kind === 'test' ? '' : 'band') + '" style="width:' + (100 * x.d / max).toFixed(1) + '%"></span></span>' +
        '</button></li>';
    }
    function render() {
      var S = state, out = rowsFor(S, S._eprel, S.resSeason);
      rowsAll = out.rows;
      if (!sel || !rowsAll.some(function (r) { return r.id === sel; })) sel = defaultSel(rowsAll);
      var cur = rowsAll.filter(function (r) { return r.id === sel; })[0];
      var ck = S.cond, c = COND[ck];
      var detail = $('[data-r-detail]');
      $('[data-r-range]', el).textContent = S.speed + ' km/h → 0 km/h';
      if (detail) {
        $('[data-r-range2]', detail).textContent = S.speed + ' → 0 km/h';
        $('[data-r-cond]', detail).textContent = c.label;
      }
      var va = $('[data-r-valik]', el);
      if (va) va.href = CFG.home + 'rehvi-valimine/?' + [S.veh ? 'auto=' + encodeURIComponent(S.veh) : '', 'moot=' + S.size, 'hooaeg=' + S.resSeason].filter(Boolean).join('&');

      if (!cur) {
        $('[data-r-big]', el).textContent = '—';
        $('[data-r-whoshort]', el).textContent = 'Selle valiku kohta andmeid ei ole.';
        $('[data-r-mbars]', el).innerHTML = '';
        if (detail) { $('[data-r-bars]', detail).innerHTML = ''; $('[data-r-big2]', detail).textContent = '—'; }
        return;
      }
      var r = cur.r, rows = rowsAll, best = rows[0].d, max = rows[rows.length - 1].d;
      /* PIDURDUSTEEKOND vs PEATUMISTEEKOND. Peatumisteekond = reageerimis-
         teekond (auto sõidab täiskiirusel, kuni juht jõuab pidurini) +
         pidurdusteekond. Rehv mõjutab ainult teist osa, seega ribad all
         jäävad pidurdusteekonnaks. */
      var rmode = store.get('rmode', 'brake'), rt = +store.get('rt', 1) || 1;
      var react = rmode === 'stop' ? S.speed / 3.6 * rt : 0;
      $$('[data-r-mode]', el).forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.rMode === rmode)); });
      $('[data-r-lbl]', el).textContent = rmode === 'stop'
        ? 'Peatumisteekond · märkamisest kuni seisuni'
        : 'Pidurdusteekond · pidur põhjas kuni seisuni';
      var spl = $('[data-r-split]', el);
      spl.hidden = rmode !== 'stop';
      $('[data-r-rt]', el).value = String(rt);
      $('[data-r-splittxt]', el).innerHTML = 'Reageerimisteekond <b>' + fmt(react) + ' m</b> + pidurdusteekond <b>' + fmt(r.distanceM) + ' m</b>';
      $('[data-r-big]', el).textContent = fmt(r.distanceM + react);
      if (!el._rbound) {
        el._rbound = true;
        $$('[data-r-mode]', el).forEach(function (b) {
          b.addEventListener('click', function () {
            store.set('rmode', b.dataset.rMode);
            Track('peatumine', b.dataset.rMode === 'stop' ? 'peatumisteekond' : 'pidurdusteekond');
            render();
          });
        });
        $('[data-r-rt]', el).addEventListener('change', function (e) {
          store.set('rt', +e.target.value);
          Track('reaktsiooniaeg', e.target.value + ' s');
          render();
        });
      }
      var whoShort = cur.kind === 'class' ? 'märgise klassi ' + cur.g + ' rehviga' : cur.kind === 'cat' ? CATNAME[cur.cat].toLowerCase() + 'ga (keskmine)' : cur.name;
      $('[data-r-whoshort]', el).innerHTML = esc(whoShort) + ' · ' + esc(c.label) + '<br>' +
        (out.vehDefault ? 'auto valimata — arvutatud VW Golf 8 järgi' : esc(out.veh.name)) + ' · vahemik ' + fmt(r.lowM + react) + '–' + fmt(r.highM + react) + ' m';

      /* kompaktsed ribad: 5 rida, valitud alati sees */
      var LIMC = 5, comp = rows.slice(0, LIMC);
      if (comp.indexOf(cur) < 0) comp = comp.slice(0, LIMC - 1).concat([cur]);
      $('[data-r-mbars]', el).innerHTML = comp.map(function (x) { return row(x, best, max, true); }).join('');
      paintPrices(S.size, cur);

      if (detail) {
        $('[data-r-big2]', detail).textContent = fmt(r.distanceM + react);
        $('[data-r-cats]', detail).innerHTML = Object.keys(SEASON).map(function (k) {
          return '<button type="button" data-rs="' + k + '" aria-pressed="' + (k === S.resSeason) + '">' + SEASON[k].label + '</button>';
        }).join('');
        $$('[data-rs]', detail).forEach(function (b) { b.addEventListener('click', function () { S.resSeason = b.dataset.rs; S._userSeason = true; sel = null; render(); }); });
        var rx = $('[data-r-react]', detail), react1 = S.speed / 3.6 * rt;
        if (rx) rx.innerHTML = rmode === 'stop'
          ? 'Peatumisteekond = reageerimisteekond <b>' + fmt(react) + ' m</b> (' + String(rt).replace('.', ',') + ' s, auto sõidab veel täiskiirusel) + pidurdusteekond <b>' + fmt(r.distanceM) + ' m</b>.'
          : 'See on pidurdusteekond: arv algab hetkest, kui pidur on põhjas. Koos ' + String(rt).replace('.', ',') + ' s reaktsiooniajaga oleks peatumisteekond <b>' + fmt(r.distanceM + react1) + ' m</b> (+' + fmt(react1) + ' m).';
        $('[data-r-band]', detail).innerHTML = 'Tõenäoline vahemik <b>' + fmt(r.lowM + react) + '–' + fmt(r.highM + react) + ' m</b> (±' + Math.round(r.sigmaRel * 100) + ' %)';
        var who = '<b>' + esc(cur.name) + '</b>';
        if (cur.kind === 'test') who += '<span class="src">Haare tuleb sõltumatu testi mõõdetud tulemusest' + (cur.sizeNote ? ' (testi mõõt ' + esc(cur.sizeNote) + '; sinu mõõdus võib märgise klass erineda)' : '') + '.</span>';
        else if (cur.kind === 'class') {
          var gn = gmidN(cur.g, cur.cat);
          who += '<span class="src">Märgise klass ' + cur.g + ' · ' + cur.n + ' rehvimudelit sinu mõõdus. Haare on ' +
            (gn ? 'selle klassi <b>' + gn + ' mõõdetud rehvi mediaan</b>' : 'klassi nominaalne keskpunkt') +
            '. Sama klassi rehvid on mudelis võrdsed; päris elus erinevad nad ±3–4 %.</span>';
        }
        else who += '<span class="src">EL-i märgis ei ütle ' + esc(c.label) + ' haarde kohta midagi, seetõttu on see kategooria keskmine.</span>';
        $('[data-r-who]', detail).innerHTML = who;
        var meta = '<span class="pill calc">Arvutatud hinnang</span>';
        meta += out.vehDefault ? '<span class="pill warn">Auto valimata: VW Golf 8</span>' : '<span class="pill">' + esc(out.veh.name) + '</span>';
        meta += '<span class="pill">' + esc(pretty(S.size)) + '</span>';
        if (cur.kind === 'test') meta += '<span class="pill test">Sõltumatu test</span>';
        if (cur.kind === 'class') meta += '<span class="pill off">Ametlik märgis</span>';
        $('[data-r-meta]', detail).innerHTML = meta;
        var sea = SEASON[S.resSeason], LIM = 10, shown = showAll ? rows : rows.slice(0, LIM);
        if (!showAll && shown.indexOf(cur) < 0) shown = shown.slice(0, LIM - 1).concat([cur]);
        $('[data-r-sub]', detail).textContent = 'Sama auto, sama kiirus ja teeolud — ainult rehv on erinev. ' + (ck === 'wet'
          ? 'Testitud rehvid eraldi, märgisega rehvid klassi kaupa.'
          : 'Eraldi ridadel ainult rehvid, mille ' + c.label + ' tulemus on päriselt mõõdetud.');
        $('[data-r-bars]', detail).innerHTML = shown.map(function (x) { return row(x, best, max, false); }).join('');
        var more = $('[data-r-more]', detail);
        more.hidden = rows.length <= LIM;
        more.textContent = showAll ? 'Näita vähem' : 'Näita kõiki (' + rows.length + ')';
        more.onclick = function () { showAll = !showAll; render(); };
        var cmpA = $('[data-r-cmp]', detail);
        if (cmpA) cmpA.href = cmpUrl(null, { auto: S.veh, moot: S.size, hooaeg: S.resSeason });
        var notes = [];
        if (!S._eprel.length) notes.push('Mõõdu ' + pretty(S.size) + ' märgiseandmeid pole veel andmebaasis — näidatakse ainult testitud rehve.');
        if (!out.nSeason && S._eprel.length) notes.push('Selles mõõdus ei ole andmebaasis ühtegi märgisega ' + sea.osa + '.');
        if (rows.some(function (x) { return x.sizeNote && !x.other; })) notes.push('Testitud rehvid on mõõdetud testi mõõdus; märk nime ees on sama mudeli ametlik klass SINU mõõdus. Need võivad erineda — see on veapiiris sees.');
        if (S.showOther) notes.push('Näidatakse ka testitud rehve, mida sinu mõõdus andmebaasis ei ole — neid ei pruugi sinu autole saada.');
        (r.warnings || []).slice(0, 2).forEach(function (w) { if (!/mõõdust .* tehasemõõt/.test(w)) notes.push(w); });
        $('[data-r-note]', detail).innerHTML = (notes.length ? '<div class="note-box">' + notes.map(esc).join('<br>') + '</div>' : '') +
          (out.hiddenOther || S.showOther ? '<button type="button" class="btn sm" style="margin-top:var(--sp-3)" data-r-other>' +
            (S.showOther ? 'Näita ainult sinu mõõdus saadaolevaid' : 'Näita ka ' + out.hiddenOther + ' testitud rehvi teistest mõõtudest') + '</button>' : '');
        var ob = $('[data-r-other]', detail);
        if (ob) ob.onclick = function () { S.showOther = !S.showOther; render(); };
      }
      $$('[data-row]').forEach(function (b) {
        b.addEventListener('click', function () { sel = b.dataset.row; render(); });
      });
      var tg = $('[data-r-toggle]');
      if (tg && !tg._bound) {
        tg._bound = true;
        tg.addEventListener('click', function () {
          var open = detail.hidden;
          detail.hidden = !open;
          tg.setAttribute('aria-expanded', open ? 'true' : 'false');
          tg.textContent = open ? 'Peida üksikasjad' : 'Kõik rehvid ja üksikasjad';
        });
      }
    }
    return { show: show };
  })();

  /* ------------------------------------------------------------ dialoog */
  /* Infomull: [data-tip] peal hõljudes / fookuses / puudutades. Mull on
     body küljes fixed-positsioonis, et tabeli kerimisala seda ei lõikaks. */
  function initTips() {
    var box = null, cur = null;
    function hide() { if (box) box.hidden = true; cur = null; }
    function show(el) {
      if (!box) { box = document.createElement('div'); box.className = 'tipbox'; box.setAttribute('role', 'tooltip'); document.body.appendChild(box); }
      cur = el; box.textContent = el.getAttribute('data-tip'); box.hidden = false;
      var r = el.getBoundingClientRect(), w = box.offsetWidth, h = box.offsetHeight;
      var x = Math.max(8, Math.min(window.innerWidth - w - 8, r.left + r.width / 2 - w / 2));
      var y = r.top - h - 8; if (y < 8) y = r.bottom + 8;
      box.style.left = x + 'px'; box.style.top = y + 'px';
    }
    document.addEventListener('mouseover', function (e) { var t = e.target.closest && e.target.closest('[data-tip]'); if (t) show(t); else if (cur) hide(); });
    document.addEventListener('focusin', function (e) { var t = e.target.closest && e.target.closest('[data-tip]'); if (t) show(t); });
    document.addEventListener('focusout', hide);
    document.addEventListener('click', function (e) { var t = e.target.closest('[data-tip]'); if (t) { e.preventDefault(); if (cur === t) hide(); else show(t); } else hide(); });
    window.addEventListener('scroll', hide, true);
  }

  function initHow() {
    /* dialoog otsitakse klõpsu hetkel, mitte käivitusel — nii töötab ta ka
       siis, kui lehe sisu vahetatakse ilma täislaadimiseta */
    document.addEventListener('click', function (e) {
      var d = $('#how');
      if (!d) return;
      var t = e.target.closest('[data-how]');
      if (t) { e.preventDefault(); if (d.showModal) d.showModal(); else d.setAttribute('open', ''); }
      if (e.target.closest('[data-how-close]') || e.target === d) d.close();
    });
  }

  /* ============================================================ VÕRDLUSLEHT */
  /* Omadused, mida saab kaaluda. `ok:false` = andmeid ei ole; neid näidatakse,
     aga nad ei mõjuta midagi ja kasutajale öeldakse see otse. */
  var PROPS = [
    { k: 'wet',   n: 'Märgpidamine',   d: 'Kui hästi rehv märjal teel haarab.', src: 'Ametlik märgis', ok: true },
    { k: 'wetb',  n: 'Märgpidurdus',   d: 'Arvutatud pidurdusmaa märjal sinu autoga, ilma reaktsiooniajata. Tuleb märghaardest.', src: 'Arvutus', ok: true },
    { k: 'dryb',  n: 'Kuivpidurdus',   d: 'Arvutatud sinu autoga. Testitud rehvidel mõõdetud haardest, teistel tuletatud (≈).', src: 'Arvutus', ok: true },
    { k: 'aqua',  n: 'Vesiliug',       d: 'Pidurdusmaa uue rehviga, kui teel on sügav vesi (roopad, lombid), 90→0 sinu autoga. Testitud rehvidel mõõdetud ujumiskiirusest, teistel tuletatud (≈).', src: 'Arvutus', ok: true },
    { k: 'noise', n: 'Müra',           d: 'Rehvimärgise müra detsibellides. Väiksem = vaiksem.', src: 'Ametlik märgis', ok: true },
    { k: 'rr',    n: 'Veeretakistus',  d: 'Mõju kütuse- või energiakulule.', src: 'Ametlik märgis', ok: true },
    { k: 'winter',n: 'Talvised omadused', d: 'Lume- ja jäämärk; testitud rehvidel lume ja jää pidurdus.', src: 'Ametlik + test', ok: true }
  ];
  var PROP = {}; PROPS.forEach(function (p) { PROP[p.k] = p; });
  var FG = { A: 5, B: 4, C: 3, D: 2, E: 1 };

  /* Ühe rehvi omadused sinu mõõdus. Iga väärtus kannab allikat. */
  function tyreProps(r, veh) {
    var t = r.tested ? core.tyreByKey[r.tested] : null, P = {};
    P.wet = { v: r.g, show: grade(r.g), src: 'off', score: FG[r.g] };
    var wb = calc(t ? Object.assign({}, t, { size: pretty(r.m) }) : eprelTyre(r), veh, condObj('wet', 90));
    P.wetb = { v: wb.distanceM, show: fmt(wb.distanceM) + ' m', src: 'calc', score: -wb.distanceM,
               sub: t ? 'haare testist (mõõt ' + t.size + ')' : 'klassi ' + r.g + (gmidN(r.g, r.cat) ? ' mõõdetud keskmine' : ' keskpunkt') };
    var tw = t ? pick(t.tests, 'ASPHALT', true) : null, td = t ? pick(t.tests, 'ASPHALT', false) : null;
    /* Mõõdetud testitulemus on väike rida arvutuse all — kõik rehvid saavad
       sama protokolli järgi (90→0, sinu auto) arvutatud väärtuse. */
    if (tw) P.wetb.sub += ' · testis ' + fmt(tw.m) + ' m (' + srcLine(tw) + ')';
    var base = t ? Object.assign({}, t, { size: pretty(r.m) }) : eprelTyre(r);
    var db = calc(base, veh, condObj('dry', 90)), dEst = !(t && t.muDry != null);
    P.dryb = { v: db.distanceM, show: est(fmt(db.distanceM) + ' m', dEst), src: dEst ? 'est' : 'calc', score: -db.distanceM,
               sub: dEst ? 'rehvitüübi keskmine' : 'haare testist' + (td ? ' · testis ' + fmt(td.m) + ' m (' + srcLine(td) + ')' : '') };
    /* VESILIUG = pidurdusmaa sügavas vees (3 mm, roopad/lombid), 90→0.
       Testitud rehvil nihutatakse mudeli ujumiskiirust mõõdetu järgi:
       ADAC-i protokollis (mudelis 7,8 mm vett) annab mudel 65 mõõdetud
       ujumiskiiruse vastu mediaanvea 0,7 % ja keskmise vea 3,8 %. */
    var deep = Object.assign(condObj('wet', 90), { waterMm: 3 }), aq = base;
    if (t && t.aqua) {
      var hpM = window.Pidurdus.hydroplaneSpeedKmh(base, veh, { surface: 'ASPHALT', waterMm: 7.8 });
      if (hpM) aq = Object.assign({}, base, { hpFactor: t.aqua.kmh / hpM });
    }
    var dd = calc(aq, veh, deep), aEst = aq === base;
    P.aqua = { v: dd.distanceM, show: est(fmt(dd.distanceM) + ' m', aEst), src: aEst ? 'est' : 'calc', score: -dd.distanceM,
               sub: aEst ? 'rehvitüübi ja laiuse järgi' : 'testis hakkas ujuma ' + fmt(t.aqua.kmh) + ' km/h juures (' + ((core.sources[t.aqua.src] || {}).nimi || 'test') + ')' };
    P.noise = r.db ? { v: r.db, show: r.db + ' dB' + (r.nk ? ' (' + r.nk + ')' : ''), src: 'off', score: -r.db } : null;
    P.rr = r.f ? { v: r.f, show: grade(r.f), src: 'off', score: FG[r.f] } : null;
    var ws = [];
    if (r.flags & FLAG.SNOW) ws.push('lumemärk');
    if (r.flags & FLAG.ICE) ws.push('jäämärk');
    var ts = t ? pick(t.tests, 'SNOW_PACKED') : null, ti = t ? pick(t.tests, 'ICE') : null;
    P.winter = { v: ws.length, show: ws.length ? ws.join(' + ') : 'märk puudub', src: 'off',
                 score: (r.flags & FLAG.SNOW ? 1 : 0) + (r.flags & FLAG.ICE ? 1 : 0),
                 sub: [ts ? 'lumi ' + fmt(ts.m) + ' m' : '', ti ? 'jää ' + fmt(ti.m) + ' m' : ''].filter(Boolean).join(' · ') };
    return P;
  }
  var EST_T = 'Tuletatud meie valemist — selle rehvi kohta sõltumatut mõõtmist ei ole. Võta suunana, mitte 100 % täpse numbrina.';
  var CALC_T = 'Arvutatud tulemus meie mudelist sinu autoga. Hinnang, mitte mõõtmine — viga on tavaliselt paar meetrit.';
  function est(txt, on) { return on ? '<span class="est" tabindex="0" data-tip="' + EST_T + '">≈</span>' + txt : txt; }
  function tip(t) { return '<span class="tip" tabindex="0" data-tip="' + esc(t) + '" aria-label="' + esc(t) + '">i</span>'; }
  /* ---- HINNAD müüjatelt. Teema hindu ei tea: küsib serverist
     (CFG.prices → /wp-json/pm/v1/hinnad), kuhu müüjate API-ühendus need
     annab. Kui ühendust pole või päring ebaõnnestub, näidatakse seda otse. */
  var PRICE_T = 'Siia tulevad rehvimüüjate hinnad otse nende süsteemist. Ühendus müüjatega on töös. Hind ei mõjuta rehvide järjestust.';
  var Prices = {
    get: function (ids) {
      if (!CFG.prices || !ids.length) return Promise.resolve({ available: false });
      var u = CFG.prices + (CFG.prices.indexOf('?') >= 0 ? '&' : '?') + 'ids=' + encodeURIComponent(ids.join(','));
      return fetch(u, { credentials: 'omit' }).then(function (r) { return r.ok ? r.json() : { available: false }; })
        .catch(function () { return { available: false }; });
    }
  };
  var sizePrices = {};
  Prices.size = function (m) {
    if (!CFG.prices) return Promise.resolve({ available: false });
    if (!sizePrices[m]) {
      var u = CFG.prices + (CFG.prices.indexOf('?') >= 0 ? '&' : '?') + 'moot=' + encodeURIComponent(m);
      sizePrices[m] = fetch(u, { credentials: 'omit' }).then(function (r) { return r.ok ? r.json() : { available: false }; })
        .catch(function () { return { available: false }; });
    }
    return sizePrices[m];
  };
  function eur(v) { return (+v).toFixed(2).replace('.', ',') + ' €'; }
  function priceSlot(id) { return '<div class="pv" data-price="' + esc(id) + '"><span class="none">Laen hindu…</span></div>'; }
  function priceHtml(rows, avail) {
    if (rows && rows.length) {
      return '<ul class="sellers">' + rows.slice(0, 4).map(function (r) {
        var name = r.url ? '<a href="' + esc(r.url) + '" target="_blank" rel="nofollow sponsored noopener">' + esc(r.myyja) + '</a>' : esc(r.myyja);
        return '<li><span>' + name + (r.laos === false ? ' <small>tellimisel</small>' : '') + '</span><b>' + eur(r.hind) + '</b></li>';
      }).join('') + '</ul>' + (rows.length > 4 ? '<p class="more">+' + (rows.length - 4) + ' müüjat veel</p>' : '');
    }
    return '<span class="none">' + (avail ? 'Selle rehvi hinda müüjatelt hetkel pole' : 'Hinnad pole hetkel saadaval') + '</span> ' + tip(PRICE_T);
  }
  function fillPrices(box) {
    var els = $$('[data-price]', box);
    if (!els.length) return;
    var ids = els.map(function (e) { return e.dataset.price; }).filter(function (x, i, a) { return a.indexOf(x) === i; });
    Prices.get(ids).then(function (d) {
      var h = (d && d.hinnad) || {};
      els.forEach(function (e) { e.innerHTML = priceHtml(h[e.dataset.price], !!(d && d.available)); });
    });
  }
  function pick(tests, surf, wet) {
    return (tests || []).filter(function (x) { return x.surf === surf && (wet == null || x.wet === wet); })[0] || null;
  }
  function srcLine(x) {
    var s = core.sources[x.src] || {};
    return (s.tegija ? s.tegija.replace(/ \(.*\)/, '') + ' ' + s.aasta : x.src) + ', ' + x.v0 + '→' + x.v1 + ' km/h, ' + (s.moot || '');
  }

  /* Kaks lehte, üks loogika:
     data-mode="valik"  — /rehvi-valimine/: küsimused → järjestus + põhjused
     data-mode="vordle" — /vordle-rehve/:   valitud rehvid tabelis, otsing lisamiseks */
  var CT = {
    drive: { city: { noise: 1 }, road: { wet: 1, rr: 1 }, hwy: { wet: 2, aqua: 1 }, mix: { wet: 1, noise: 1 } },
    km: { lo: {}, mid: { rr: 1 }, hi: { rr: 2 }, vhi: { rr: 3 } },
    main: { safe: { wet: 3, wetb: 1 }, brake: { wetb: 2, dryb: 2 }, quiet: { noise: 3 }, fuel: { rr: 3 },
            winter: { winter: 3 } }
  };
  /* ext = avalehe kaart (auto ja mõõt tulevad sealt, oma valijaid pole) */
  function initTyres(root, ext) {
    var mode = ext ? 'valik' : (root.dataset.mode || 'vordle');
    var qs = new URLSearchParams(location.search);
    var S = { veh: store.get('veh', null), size: '20555R16', season: 'summer', drive: '', km: '', main: [] };
    if (ext) { var e0 = ext.get(); S.veh = e0.veh; S.size = e0.size; }
    /* NB: parameetrid ei tohi olla WordPressi omad (s, m, p, …) — ?s= teeks
       lehest otsingu ja ?m= kuuarhiivi. */
    if (qs.get('auto')) S.veh = qs.get('auto');
    if (qs.get('moot')) S.size = qs.get('moot');
    if (qs.get('hooaeg') && SEASON[qs.get('hooaeg')]) S.season = qs.get('hooaeg');
    if (qs.get('rehvid')) {
      var known = {}; cmp.list().forEach(function (x) { known[x.id] = x.n; });
      cmp.set(qs.get('rehvid').split(',').filter(Boolean).map(function (id) { return { id: id, n: known[id] || id.split('@')[0] }; }));
    }
    function save() { store.set('veh', S.veh); }

    var restoring = false, picker = null;
    /* auto vahetus: teise mõõdu rehvid võrdlusest ära */
    function dropOtherSizes(was) {
      if (S.size !== was && !restoring) cmp.set(cmp.list().filter(function (x) { return x.id.split('@')[1] === S.size; }));
    }
    if (ext) {
      ext.on(function (v) { var was = S.size; S.veh = v.veh; S.size = v.size; dropOtherSizes(was); draw(); });
    } else {
      var sizeSel = $('[data-f=size]', root);
      picker = VehPicker(root, function (key) {
        S.veh = key;
        var veh = key ? core.vehByKey[key] : null;
        var was = S.size;
        S.size = sizeOptions(sizeSel, veh, veh && !qs.get('moot') ? norm(veh.oemSize) : S.size);
        dropOtherSizes(was);
        save(); draw();
      });
      S.size = sizeOptions(sizeSel, null, S.size);
      sizeSel.addEventListener('change', function () { var was = S.size; S.size = sizeSel.value; dropOtherSizes(was); save(); draw(); });
    }
    $$('[data-season]', root).forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.season === S.season ? 'true' : 'false');
      b.addEventListener('click', function () {
        S.season = b.dataset.season;
        Track('hooaeg', SEASON[S.season].long);
        $$('[data-season]', root).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        save(); draw();
      });
    });

    /* ---- küsimused (ainult valik) */
    function weights() {
      if (S.w && S.wManual) return S.w;
      var w = {};
      function add(m) { Object.keys(m || {}).forEach(function (k) { w[k] = Math.min(3, (w[k] || 0) + m[k]); }); }
      add(CT.drive[S.drive]); add(CT.km[S.km]);
      S.main.forEach(function (k) { add(CT.main[k]); });
      return w;
    }
    $$('[data-ct]', root).forEach(function (b) {
      b.addEventListener('click', function () {
        var g = b.dataset.ct, v = b.dataset.v;
        if (g === 'main') {
          var i = S.main.indexOf(v);
          if (i >= 0) S.main.splice(i, 1); else { if (S.main.length >= 3) S.main.shift(); S.main.push(v); }
        } else S[g] = S[g] === v ? '' : v;
        Track('kriteerium', g + '=' + (g === 'main' ? S.main.join('+') : S[g]));
        S.wManual = false; S.w = null;
        save(); paintQ(); draw();
      });
    });
    var prio = $('[data-prio]', root);
    if (prio) {
      prio.innerHTML = PROPS.map(function (p) {
        return '<div class="prio-item' + (p.ok ? '' : ' na') + '"><span class="pn">' + esc(p.n) + '</span>' +
          '<span class="lvl" role="group" aria-label="' + esc(p.n) + ' tähtsus">' + [1, 2, 3].map(function (l) {
            return '<button type="button" data-w="' + p.k + '" data-l="' + l + '"' + (p.ok ? '' : ' disabled') + ' aria-label="tähtsus ' + l + '"></button>';
          }).join('') + '</span><span class="pd">' + esc(p.d) + (p.ok ? '' : ' <b>Andmed puuduvad.</b>') + '</span></div>';
      }).join('');
      $$('[data-w]', prio).forEach(function (b) {
        b.addEventListener('click', function () {
          var w = Object.assign({}, weights()), k = b.dataset.w, l = +b.dataset.l;
          w[k] = w[k] === l ? 0 : l;
          S.w = w; S.wManual = true; save(); paintQ(); draw();
        });
      });
    }
    var reset = $('[data-prio-reset]', root);
    if (reset) reset.addEventListener('click', function () { S.drive = S.km = ''; S.main = []; S.w = null; S.wManual = false; save(); paintQ(); draw(); });
    function paintQ() {
      $$('[data-ct]', root).forEach(function (b) {
        var on = b.dataset.ct === 'main' ? S.main.indexOf(b.dataset.v) >= 0 : S[b.dataset.ct] === b.dataset.v;
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      var w = weights();
      $$('[data-w]', root).forEach(function (b) { b.setAttribute('aria-pressed', (w[b.dataset.w] || 0) >= +b.dataset.l ? 'true' : 'false'); });
      var used = Object.keys(w).filter(function (k) { return w[k] > 0 && PROP[k] && PROP[k].ok; });
      var miss = Object.keys(w).filter(function (k) { return w[k] > 0 && PROP[k] && !PROP[k].ok; });
      var box = $('[data-ct-out]', root);
      if (box) box.innerHTML = (used.length ? '<p class="note" style="margin:0">Arvestan: ' + used.map(function (k) { return '<b>' + esc(PROP[k].n.toLowerCase()) + '</b>' + (w[k] > 1 ? ' ×' + w[k] : ''); }).join(', ') + '</p>' : '<p class="note" style="margin:0">Vali ülal, mis sulle oluline on — järjestus muutub kohe.</p>') +
        (miss.length ? '<div class="note-box" style="margin-top:var(--sp-3)">' + miss.map(function (k) { return PROP[k].n; }).join(', ') + ': usaldusväärsed andmed puuduvad — seda ei saa arvestada, ja me ei hakka seda arvama.</div>' : '');
      if (reset) reset.hidden = !used.length && !miss.length;
    }
    paintQ();

    /* ---- põhjused: miks see rehv sinu valikute järgi paistab */
    function reasons(x, stats, w) {
      var out = [], r = x.r, P = x.P;
      var order = Object.keys(w).filter(function (k) { return w[k] > 0; }).sort(function (a, b) { return w[b] - w[a]; });
      if (!order.length) order = ['wet', 'noise'];
      order.forEach(function (k) {
        if (k === 'wet' && r.g) out.push('Märghaardumine <b>' + r.g + '</b>' + (r.g === stats.bestG ? ' — parim klass selles mõõdus' : ''));
        if (k === 'wetb' && P.wetb) out.push('Märgpidurdus sinu autoga <b>' + P.wetb.show + '</b>' + (P.wetb.v <= stats.bestWetb + 0.05 ? ' — lühim selles nimekirjas' : ' (+' + fmt(P.wetb.v - stats.bestWetb) + ' m ehk ' + pct(P.wetb.v - stats.bestWetb, stats.bestWetb) + ' parimast)'));
        if (k === 'dryb' && P.dryb) out.push('Kuivpidurdus sinu autoga <b>' + P.dryb.show + '</b>');
        if (k === 'noise' && r.db) {
          var louder = stats.dbs.filter(function (d) { return d > r.db; }).length, qp = Math.round(100 * louder / stats.dbs.length);
          out.push('Müra <b>' + r.db + ' dB</b>' + (qp >= 50 ? ' — vaiksem kui ' + qp + ' % selle mõõdu rehvidest' : ''));
        }
        if (k === 'rr' && r.f) out.push('Veeretakistus <b>' + r.f + '</b>' + (r.f === stats.bestF ? ' — parim klass selles mõõdus' : ''));
        if (k === 'winter') out.push(P.winter.v ? 'Talvemärgid: <b>' + P.winter.show + '</b>' : 'Lume- ja jäämärk <b>puudub</b>');
        if (k === 'aqua' && P.aqua) out.push('Pidurdusmaa sügavas vees <b>' + P.aqua.show + '</b>');
      });
      if (r.tested) out.push('Sõltumatult testitud');
      return out.slice(0, 4);
    }

    /* ---- nimekiri */
    var listEl = $('[data-cmp-list]', root), head = $('[data-cmp-head]', root), q = $('[data-q]', root);
    var brandSel = $('[data-brand]', root), brandVal = qs.get('mark') || '';
    var qT = null, viimaneQ = '';
    if (q) q.addEventListener('input', function () {
      draw();
      clearTimeout(qT);
      qT = setTimeout(function () {
        var v = q.value.trim();
        if (v.length >= 2 && v !== viimaneQ) { viimaneQ = v; Track('otsing', v + ' → ' + viimaneN + ' vastet'); }
      }, 1200);
    });
    if (brandSel) brandSel.addEventListener('change', function () {
      brandVal = brandSel.value;
      Track('margifilter', brandVal || 'kõik margid');
      draw();
    });
    var viimaneN = 0;
    /* margivalik täidetakse selle mõõdu ja hooaja ridadest, et nimekirjas
       ei oleks marke, mida selles mõõdus üldse ei müüda */
    function paintBrands(rows) {
      if (!brandSel) return;
      var n = {};
      rows.forEach(function (r) { n[r.mark] = (n[r.mark] || 0) + 1; });
      var names = Object.keys(n).sort(function (a, b) { return a.localeCompare(b, 'et'); });
      if (brandVal && names.indexOf(brandVal) < 0) brandVal = '';
      brandSel.innerHTML = '<option value="">Kõik margid (' + names.length + ')</option>' +
        names.map(function (m) { return '<option value="' + esc(m) + '"' + (m === brandVal ? ' selected' : '') + '>' + esc(m) + ' · ' + n[m] + '</option>'; }).join('');
      brandSel.value = brandVal;
    }
    function draw() {
      if (!listEl) { drawTable(); return; }
      listEl.innerHTML = '<p class="note">Laen…</p>';
      loadSize(S.size).then(function (rows) {
        var veh = core.vehByKey[S.veh] || core.vehByKey[DEFAULT_VEH];
        var cats = SEASON[S.season].eprel, qq = q ? norm(q.value) : '';
        var seas = rows.filter(function (r) { return cats.indexOf(r.catNr) >= 0; });
        paintBrands(seas);
        var list = seas.filter(function (r) {
          return (!brandVal || r.mark === brandVal) && (!qq || norm(r.mark + r.name).indexOf(qq) >= 0);
        })
          .map(function (r) { return { r: r, P: tyreProps(r, veh) }; });
        var w = mode === 'valik' ? weights() : {};
        var ws = Object.keys(w).filter(function (k) { return w[k] > 0 && PROP[k] && PROP[k].ok; });
        var stats = {
          bestG: list.map(function (x) { return x.r.g; }).filter(Boolean).sort()[0],
          bestF: list.map(function (x) { return x.r.f; }).filter(Boolean).sort()[0],
          bestWetb: Math.min.apply(null, list.map(function (x) { return x.P.wetb ? x.P.wetb.v : 999; })),
          dbs: list.map(function (x) { return x.r.db; }).filter(Boolean)
        };
        /* SOBIVUS sinu valikute põhjal: iga kaalutud omadus normeeritakse selle
           nimekirja sees 0…1. Puuduv väärtus EI saa nulli ega keskmist — ta
           jäetakse välja ja see öeldakse kaardil. */
        if (ws.length) {
          var rng = {};
          ws.forEach(function (k) {
            var vals = list.map(function (x) { return x.P[k] && x.P[k].score; }).filter(function (v) { return v != null; });
            rng[k] = vals.length ? [Math.min.apply(null, vals), Math.max.apply(null, vals)] : [0, 0];
          });
          list.forEach(function (x) {
            var s = 0, wsum = 0, miss = [];
            ws.forEach(function (k) {
              var p = x.P[k];
              if (!p || p.score == null) { miss.push(PROP[k].n.toLowerCase()); return; }
              var a = rng[k][0], b = rng[k][1];
              s += w[k] * (b > a ? (p.score - a) / (b - a) : 1); wsum += w[k];
            });
            x.fit = wsum ? Math.round(100 * s / wsum) : null; x.miss = miss;
          });
          list.sort(function (a, b) { return (b.fit == null ? -1 : b.fit) - (a.fit == null ? -1 : a.fit) || ((FG[b.r.g] || 0) - (FG[a.r.g] || 0)); });
        } else {
          list.sort(function (a, b) { return (FG[b.r.g] || 0) - (FG[a.r.g] || 0) || (!!b.r.tested - !!a.r.tested) || ((a.r.db || 99) - (b.r.db || 99)); });
        }
        viimaneN = list.length;
        if (head) head.innerHTML = '<b>' + list.length + '</b> ' + (list.length === 1 ? SEASON[S.season].yks : SEASON[S.season].osa) + ' mõõdus <b>' + esc(pretty(S.size)) + '</b>' +
          (ws.length ? ' · järjestatud sinu valikute järgi' : ' · järjestatud märghaardumise klassi järgi');
        if (!list.length) {
          Track('tulemusi_null', pretty(S.size) + ' · ' + SEASON[S.season].long + (brandVal ? ' · ' + brandVal : '') + (qq ? ' · otsing "' + q.value.trim() + '"' : ''));
          listEl.innerHTML = '<div class="box"><p style="margin:0">' + (rows.length ? 'Selles mõõdus ei ole andmebaasis ühtegi ' + SEASON[S.season].osa + (brandVal ? ' margilt ' + esc(brandVal) : '') + (qq ? ' selle otsinguga' : '') + '.' :
            'Mõõdu ' + esc(pretty(S.size)) + ' märgiseandmed pole veel andmebaasis. Hetkel on korjatud ' + core.eprelSizes.length + ' mõõtu.') + '</p></div>';
          drawTable(); return;
        }
        var LIM = mode === 'valik' ? 20 : 30;
        listEl.innerHTML = list.slice(0, LIM).map(function (x, i) { return card(x, i, mode === 'valik' ? reasons(x, stats, w) : null); }).join('') +
          (list.length > LIM ? '<p class="note">Näidatakse ' + LIM + ' esimest ' + list.length + '-st.' + (mode === 'valik' ? ' Muuda valikuid, et järjestust muuta.' : ' Täpsusta otsingut.') + '</p>' : '');
        fillPrices(listEl);
        $$('[data-add]', listEl).forEach(function (b) {
          b.addEventListener('click', function () {
            var on = cmp.toggle({ id: b.dataset.add, n: b.dataset.n });
            Track(on ? 'vordlusse' : 'vordlusest_ara', b.dataset.n);
            b.setAttribute('aria-pressed', on ? 'true' : 'false');
            b.textContent = on ? '✓ Võrdluses' : '+ Võrdle';
            b.closest('.rcard').classList.toggle('on', on);
            drawTable();
          });
        });
        drawTable();
      });
    }
    function prop(label, p, k) {
      if (!p) return '<div class="rp"><div class="l">' + esc(label) + '</div><div class="v none">' + '–' + '</div></div>';
      var pill = { off: 'Ametlik', test: 'Test', calc: 'Arvutus', est: 'Tuletatud' }[p.src];
      return '<div class="rp"><div class="l">' + esc(label) + (p.src === 'calc' || p.src === 'est' ? ' ' + tip(CALC_T) : '') + '</div><div class="v">' + p.show + '</div><div class="srcd">' + pill + (p.sub ? ' · ' + esc(p.sub) : '') + '</div></div>';
    }
    function card(x, i, why) {
      var r = x.r, id = r.slug + '@' + r.m, on = cmp.has(id);
      return '<article class="rcard' + (on ? ' on' : '') + '"><div>' +
        '<div class="b">' + (why ? '<span class="rank">' + (i + 1) + '</span>' : '') + (r.tested ? '<span style="color:var(--tested)">Sõltumatult testitud</span>' : '<span style="color:var(--muted)">EL-i märgis</span>') + '</div>' +
        '<h3><a href="' + CFG.home + 'rehvid/' + esc(r.slug) + '/"><span class="mk">' + esc(r.mark) + '</span> ' + esc(r.name) + '</a></h3></div>' +
        '<div style="display:flex;gap:var(--sp-2);align-items:center;flex-wrap:wrap;justify-content:flex-end">' + (x.fit != null ? '<span class="fit" title="Sinu valitud omaduste põhjal selles nimekirjas — mitte üldine hinne">Sobivus sinu valikute põhjal ' + x.fit + ' %</span>' : '') +
        '<button type="button" class="add-btn" data-add="' + esc(id) + '" data-n="' + esc(r.mark + ' ' + r.name) + '" aria-pressed="' + on + '">' + (on ? '✓ Võrdluses' : '+ Võrdle') + '</button></div>' +
        (why && why.length ? '<ul class="why-list">' + why.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>' : '') +
        '<div class="props">' +
        prop('Märgpidamine', x.P.wet, 'wet') + prop('Märgpidurdus 90→0', x.P.wetb, 'wetb') +
        prop('Kuivpidurdus 90→0', x.P.dryb, 'dryb') + prop('Müra', x.P.noise, 'noise') + prop('Veeretakistus', x.P.rr, 'rr') +
        prop('Talv', x.P.winter, 'winter') +
        '</div>' +
        '<div class="price"><div class="pl">Hind müüjatelt</div>' + priceSlot(id) + '</div>' +
        (x.miss && x.miss.length ? '<p class="note" style="grid-column:1/-1;margin:0">Sobivuses arvestamata: ' + esc(x.miss.join(', ')) + '</p>' : '') + '</article>';
    }

    /* ---- valitud rehvide tabel + alumine riba */
    var tblBox = $('[data-cmp-table]', root);
    function drawTable() {
      var veh = core.vehByKey[S.veh] || core.vehByKey[DEFAULT_VEH];
      var sel = cmp.list();
      var tray = $('[data-tray]');
      if (tray) {
        tray.hidden = !sel.length;
        $('[data-tray-chips]', tray).innerHTML = sel.map(function (p) {
          return '<span class="chip">' + esc(p.n) + ' <button type="button" data-trm="' + esc(p.id) + '" aria-label="Eemalda">×</button></span>';
        }).join('');
        $$('[data-trm]', tray).forEach(function (b) { b.addEventListener('click', function () { cmp.toggle({ id: b.dataset.trm }); draw(); }); });
        var go = $('[data-tray-go]', tray);
        if (go) { go.href = mode === 'valik' ? cmpUrl(sel, { auto: S.veh }) : '#vordlus'; go.textContent = mode === 'valik' ? 'Võrdle kõrvuti (' + sel.length + ') →' : 'Vaata võrdlust ↓'; }
      }
      if (!tblBox) return;
      if (sel.length < 2) {
        tblBox.innerHTML = mode === 'vordle' ? '<div class="box empty-cmp"><h2>' + (sel.length ? 'Lisa veel vähemalt üks rehv' : 'Vali võrdlemiseks 2–4 rehvi') + '</h2><p class="note" style="margin:0">Otsi allpool rehvi ja vajuta „+ Võrdle“. Või <a href="' + CFG.home + 'rehvi-valimine/">lase rehvi valimisel</a> sobivad välja pakkuda.</p></div>' : '';
        return;
      }
      var sizes = {}; sel.forEach(function (p) { var m = p.id.split('@')[1]; if (m) sizes[m] = 1; });
      Promise.all(Object.keys(sizes).map(loadSize)).then(function () {
        var items = sel.map(function (p) {
          var bits = p.id.split('@'), rows = sizeCache[bits[1]] || [];
          var r = rows.filter(function (x) { return x.slug === bits[0]; })[0];
          return r ? { r: r, P: tyreProps(r, veh) } : null;
        }).filter(Boolean);
        if (items.length < 2) { tblBox.innerHTML = ''; return; }
        var ROWS = [
          ['Märghaare', null],
          ['Märghaardumise klass', 'wet', 'max', 'Ametlik'],
          ['Märgpidurdus 90→0 (sinu auto)', 'wetb', 'max', 'Arvutus'],
          ['Vesiliug: 90→0 sügava veega teel', 'aqua', 'max', 'Arvutus', 'Uus rehv (8 mm muster). Teel on 3 mm vett — nagu roobastes või suures lombis. Siis hakkab rehv vee peal ujuma ja pidurdusmaa kasvab. Arvutatud tulemus, mitte mõõtmine.'],
          ['Kuiv ja talv', null],
          ['Kuivpidurdus 90→0 (sinu auto)', 'dryb', 'max', 'Arvutus'],
          ['Talvemärgid', 'winter', null, 'Ametlik'],
          ['Märgis', null],
          ['Müra', 'noise', 'max', 'Ametlik'],
          ['Veeretakistus', 'rr', 'max', 'Ametlik'],
          ['Hind', null],
          ['Hind müüjatelt', 'price']
        ];
        var h = '<div class="cmp-table" id="vordlus"><h2>Valitud rehvid</h2><p class="note">Kollane joon = parim selles reas. Sama auto: ' + esc(veh.name) + '. <span class="est">≈</span> = tuletatud meie valemist, selle rehvi kohta mõõtmist ei ole. Hõljuta hiirt märgi peal.</p><div class="tbl-wrap"><table class="cmp"><thead><tr><th scope="col">Omadus</th>' +
          items.map(function (x) { return '<th scope="col"><a href="' + CFG.home + 'rehvid/' + esc(x.r.slug) + '/">' + esc(x.r.mark + ' ' + x.r.name) + '</a><span class="s" style="font-weight:500;color:var(--muted);display:block;font-size:12px">' + esc(pretty(x.r.m)) + ' · <button type="button" class="linkbtn" style="font-size:12px" data-xrm="' + esc(x.r.slug + '@' + x.r.m) + '">eemalda</button></span></th>'; }).join('') + '</tr></thead><tbody>';
        ROWS.forEach(function (row) {
          if (!row[1]) { h += '<tr class="grp"><th colspan="' + (items.length + 1) + '">' + esc(row[0]) + '</th></tr>'; return; }
          if (row[1] === 'price') { h += '<tr class="price-row"><th scope="row">' + esc(row[0]) + '</th>' + items.map(function (x) { return '<td>' + priceSlot(x.r.slug + '@' + x.r.m) + '</td>'; }).join('') + '</tr>'; return; }
          var k = row[1], vals = items.map(function (x) { return x.P[k] && x.P[k].score != null ? x.P[k].score : null; });
          var present = vals.filter(function (v) { return v != null; });
          var bestV = present.length > 1 ? Math.max.apply(null, present) : null;
          h += '<tr><th scope="row">' + esc(row[0]) + (row[3] === 'Arvutus' ? ' ' + tip(row[4] || CALC_T) : '') + '</th>' + items.map(function (x, i) {
            var p = x.P[k];
            if (!p) return '<td><span class="s">' + '–' + '</span></td>';
            var win = row[2] && bestV != null && vals[i] === bestV && present.filter(function (v) { return v === bestV; }).length < present.length;
            var extra = '';
            if ((k === 'wetb' || k === 'dryb' || k === 'aqua') && bestV != null && vals[i] != null && vals[i] < bestV) {
              var bestM = -bestV, diff = p.v - bestM;
              if (diff > 0.05) extra = ' <span class="pct">+' + fmt(diff) + ' m · ' + pct(diff, bestM) + '</span>';
            }
            return '<td' + (win ? ' class="win"' : '') + '><span class="v">' + p.show + '</span>' + extra + (p.sub ? '<span class="s">' + esc(p.sub) + '</span>' : '') + '</td>';
          }).join('') + '</tr>';
        });
        h += '</tbody></table></div>';
        h += '<p class="swipe-hint">Libista, et näha kõiki →</p><div class="swipe">' + items.map(function (x) {
          return '<div class="sc"><h3>' + esc(x.r.mark + ' ' + x.r.name) + '</h3><dl>' + ROWS.map(function (row) {
            if (!row[1]) return '<dt class="g">' + esc(row[0]) + '</dt>';
            if (row[1] === 'price') return '<dt>' + esc(row[0]) + '</dt><dd>' + priceSlot(x.r.slug + '@' + x.r.m) + '</dd>';
            var p = x.P[row[1]];
            return '<dt>' + esc(row[0]) + '</dt><dd>' + (p ? p.show : '<span style="font-weight:500;color:var(--muted)">' + '–' + '</span>') + '</dd>';
          }).join('') + '</dl></div>';
        }).join('') + '</div></div>';
        tblBox.innerHTML = h;
        fillPrices(tblBox);
        $$('[data-xrm]', tblBox).forEach(function (b) { b.addEventListener('click', function () { cmp.toggle({ id: b.dataset.xrm }); draw(); }); });
      });
    }

    /* auto taastatakse ALLES NÜÜD, kui kõik joonistajad on olemas */
    if (!ext && S.veh && core.vehByKey[S.veh]) { restoring = true; picker.set(S.veh); restoring = false; } else draw();
  }

  /* ============================================================ REHVILEHT
     Väike kalkulaator: selle rehvi pidurdusmaa sinu autoga, võrreldes sama
     mõõdu klassidega A ja E. */
  function initTyreWidget(root) {
    var sizes = JSON.parse(root.dataset.sizes || '[]'), tested = root.dataset.tested || null;
    var sSel = $('[data-tw-size]', root), out = $('[data-tw-out]', root);
    var ck = 'wet', speed = 90;
    var myVeh = store.get('veh', null);
    var veh = core.vehByKey[myVeh] || core.vehByKey[DEFAULT_VEH];
    $('[data-tw-veh]', root).textContent = veh.name + (core.vehByKey[myVeh] ? '' : ' (vali oma auto avalehel)');
    if (sizes.length) {
      sSel.innerHTML = sizes.map(function (z) { return '<option value="' + esc(z.m) + '">' + esc(pretty(z.m)) + ' · klass ' + esc(z.g) + '</option>'; }).join('');
      var oem = norm(veh.oemSize); if ($('option[value="' + oem + '"]', sSel)) sSel.value = oem;
    } else sSel.closest('.fld').hidden = true;
    $$('[data-tw-cond]', root).forEach(function (b) {
      b.addEventListener('click', function () { ck = b.dataset.twCond; $$('[data-tw-cond]', root).forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); go(); });
    });
    sSel.addEventListener('change', go);
    function go() {
      var z = sizes.filter(function (x) { return x.m === sSel.value; })[0];
      var t = tested ? Object.assign({}, core.tyreByKey[tested]) : null;
      var tyre = t || (z ? { key: 'w', name: 'x', category: root.dataset.cat, wetGripIndex: gmid(z.g, root.dataset.cat), treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: false, size: pretty(z.m), gSource: 'label' } : null);
      if (!tyre) { out.innerHTML = '<p class="note">Andmed puuduvad.</p>'; return; }
      var cond = condObj(ck, speed), r = calc(tyre, veh, cond);
      var cat = tyre.category, m = z ? z.m : norm(veh.oemSize);
      var a = calc(classTyre('A', cat, m), veh, cond).distanceM, e = calc(classTyre('E', cat, m), veh, cond).distanceM;
      var knows = ck === 'wet' || (ck === 'dry' && t && t.muDry != null) || (ck === 'snow' && t && t.muSnow != null) || (ck === 'ice' && t && t.muIce != null);
      out.innerHTML = '<p class="res-big" style="font-size:72px;margin:var(--sp-2) 0">' + (knows ? '' : '<span class="est" tabindex="0" style="font-size:20px;height:30px;min-width:30px;vertical-align:14px" data-tip="' + EST_T + '">≈</span>') + '<span class="hl">' + fmt(r.distanceM) + '</span><small>m</small></p>' +
        '<p class="res-band">' + speed + ' → 0 km/h, ' + COND[ck].label + ' · vahemik <b>' + fmt(r.lowM) + '–' + fmt(r.highM) + ' m</b> · ilma reaktsiooniajata</p>' +
        (ck === 'wet' ? '<p class="note">Võrdluseks sama mõõdu märgise klassid: A ' + fmt(a) + ' m, E ' + fmt(e) + ' m.' +
          (t ? ' Selle rehvi haare tuleb testi mõõtmisest (' + esc(t.size) + '), mitte klassist — seepärast võib ta klassi tüüpilisest erineda.' : '') + '</p>' : '') +
        (knows ? '' : '<div class="note-box"><span class="est">≈</span>Tuletatud meie mudelist (' + COND[ck].label + '): kasutame rehvitüübi keskmist haaret, sest selle rehvi kohta sõltumatut mõõtmist ei ole.</div>') +
        '<div class="res-meta"><span class="pill calc">Arvutatud hinnang</span>' + (t ? '<span class="pill test">Haare testist</span>' : '<span class="pill off">Märgise klass</span>') + '</div>';
    }
    go();
    var addB = $('[data-tw-add]');
    if (addB) addB.addEventListener('click', function () {
      var m = sSel.value || (sizes[0] && sizes[0].m);
      if (!m) return;
      var id = root.dataset.slug + '@' + m;
      if (!cmp.has(id)) cmp.toggle({ id: id, n: root.dataset.name });
      nav(cmpUrl(cmp.list(), { moot: m, auto: myVeh }));
    });
  }

  /* ------------------------------------------------------------ käivitus */
  /* Lehe interaktiivsed osad. Eraldi funktsioonina, et sama sisu saaks
     käivitada ka pärast sisu vahetust (window.PM.initPage). */
  /* ---- KONTAKTIVORM. Saadetakse JSON-ina, mitte vormina: SvelteKit
     blokeerib turvakaalutlustel teiselt saidilt tulevad vormipostitused
     ja JSON-päring on sellest reeglist väljas. Eelvaates,
     kus serverit pole, avatakse valmis kiri kasutaja e-posti programmis. */
  function initContact(form) {
    var msg = $('[data-contact-msg]', form), go = $('[data-contact-go]', form);
    function say(t, ok) { msg.hidden = false; msg.className = 'form-msg ' + (ok ? 'ok' : 'err'); msg.textContent = t; }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form), v = function (k) { return String(f.get(k) || '').trim(); };
      if (!v('nimi')) { say('Palun kirjuta oma nimi.'); form.nimi.focus(); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('email'))) { say('Palun kontrolli e-posti aadressi — sellele vastame.'); form.email.focus(); return; }
      if (v('sonum').length < 5) { say('Palun kirjuta sõnum.'); form.sonum.focus(); return; }
      /* robotikontroll: kui vidin on lehel, peab luba olemas olema */
      var tsId = form.getAttribute('data-ts-id');
      if ($('.ts', form) && !v('cf-turnstile-response')) { say('Oota hetk — robotikontroll pole veel valmis. Kui vormi all on kast, märgi see.'); return; }
      var topic = form.teema.options[form.teema.selectedIndex].text;
      if (!CFG.contact) {
        var body = 'Teema: ' + topic + '\nNimi: ' + v('nimi') + '\nE-post: ' + v('email') + (v('firma') ? '\nEttevõte: ' + v('firma') : '') + '\n\n' + v('sonum');
        location.href = 'mailto:' + (CFG.contactMail || '') + '?subject=' + encodeURIComponent('[Pidurdusmaa.ee] ' + topic + ' — ' + v('nimi')) + '&body=' + encodeURIComponent(body);
        say('Avasime kirja sinu e-posti programmis — vajuta seal „Saada“.', true);
        return;
      }
      go.disabled = true; go.textContent = 'Saadan…';
      fetch(CFG.contact, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(Object.fromEntries(f)) })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); say('Aitäh! Kiri on saadetud — vastame e-postile.', true); }
          else say((d && d.msg) || 'Saatmine ebaõnnestus. Proovi hiljem uuesti.');
        })
        .catch(function () { say('Ühendus katkes. Proovi uuesti.'); })
        .then(function () {
          go.disabled = false; go.textContent = 'Saada kiri →';
          /* luba kehtib ühe saatmise — järgmise jaoks uus */
          if (tsId !== null && window.turnstile) try { window.turnstile.reset(tsId); } catch (e) {}
        });
    });
  }

  /* lehevaatamine: pealkiri ütleb rohkem kui aadress */
  function trackPage() {
    var h1 = $('main h1'), crumb = $('main .crumbs');
    var nimi = document.title;
    if (h1) {
      var tmp = document.createElement('div');
      tmp.innerHTML = h1.innerHTML.replace(/<[^>]+>/g, ' ');
      nimi = tmp.textContent.trim().replace(/\s+/g, ' ');
    }
    var sek = crumb ? crumb.textContent.replace(/\s+/g, ' ').trim().split('/')[1] : '';
    Track('leht', (sek ? sek.trim() + ': ' : '') + nimi.slice(0, 70));
  }

  /* laiad tabelid: kerimisala peab olema klaviatuuriga kättesaadav */
  function tablesA11y() {
    $$('.tbl-wrap').forEach(function (t) {
      if (t.scrollWidth > t.clientWidth + 1 && !t.hasAttribute('tabindex')) {
        var h = t.closest('.box, .cmp-table'); h = h && $('h2', h);
        t.setAttribute('tabindex', '0'); t.setAttribute('role', 'region');
        t.setAttribute('aria-label', (h ? h.textContent.trim() + ' — ' : '') + 'tabel, keri külgsuunas');
      }
    });
  }
  document.addEventListener('pm:cmp', function () { setTimeout(tablesA11y, 50); });

  /* Rehvi pilt pakkujalt (kui mõni pakkuja on sisse lülitatud). Pilt tuleb
     meie serveri kaudu (/api/pilt/…), pakkuja aadressi brauser ei näe.
     Kui pilti pole, jääb illustratsioon. */
  function rehviPilt() {
    var box = $('[data-rehv-pilt]');
    if (!box || box._pilt) return;
    box._pilt = true;
    var slug = box.getAttribute('data-rehv-pilt');
    fetch(CFG.home + 'api/rehv/' + encodeURIComponent(slug) + '/', { credentials: 'omit' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || !d.pilt) return;
        var img = new Image();
        img.alt = 'Rehvi pilt';
        img.decoding = 'async';
        img.onload = function () {
          box.innerHTML = '';
          box.classList.add('has-photo');
          box.setAttribute('aria-label', 'Rehvi pilt');
          box.appendChild(img);
          var cap = $('[data-rehv-pilt-allkiri]');
          if (cap) cap.textContent = 'Pilt: rehvimüüja';
        };
        img.src = d.pilt;
      })
      .catch(function () {});
  }

  function initPage() {
    trackPage();
    /* päis jääb lehevahetusel alles — sulgeme lahtise menüü */
    var pm = $('#pm-panel'), bg = $('[data-burger]');
    if (pm && !pm.hidden) { pm.hidden = true; if (bg) bg.setAttribute('aria-expanded', 'false'); }
    $$('[data-dd].open').forEach(function (dd) { dd.classList.remove('open'); $('.dd-btn', dd).setAttribute('aria-expanded', 'false'); });
    tablesA11y();
    rehviPilt();
    var needs = $('[data-calc]') || $('[data-cmp-page]') || $('[data-tw]');
    cmp.paint();
    var kf = $('[data-contact]'); if (kf) initContact(kf);
    if (!needs) return Promise.resolve();
    return loadCore().then(function () {
      var c = $('[data-calc]'); if (c) initCalc(c);
      var h = $('[data-valik-home]'); if (c && h) initTyres(document.getElementById('sisu') || document.body, c.pmBus);
      var p = $('[data-cmp-page]'); if (p) initTyres(p);
      var w = $('[data-tw]'); if (w) initTyreWidget(w);
      setTimeout(tablesA11y, 300);
    }).catch(function (e) {
      $$('[data-calc],[data-cmp-page],[data-tw]').forEach(function (x) {
        x.insertAdjacentHTML('afterbegin', '<p class="note-box" style="margin:var(--sp-4)">Andmete laadimine ebaõnnestus. Proovi lehte värskendada.</p>');
      });
      if (window.console) console.error(e);
    });
  }
  /* Kasutusloo KOKKUVÕTE inimesele loetavas eesti keeles. Sama teksti saab
     testija tagasisidega kaasa saata ja sama loogikaga tehakse hiljem
     serveris koondstatistika. */
  function lugu() {
    var log = Track.log();
    if (!log.length) return null;
    var min = Math.max(1, Math.round(log[log.length - 1].s / 60));
    var loend = {}, vaartused = {};
    log.forEach(function (r) {
      loend[r.e] = (loend[r.e] || 0) + 1;
      if (r.v) { (vaartused[r.e] = vaartused[r.e] || []).push(r.v); }
    });
    function uniq(a) { var s = {}, o = []; (a || []).forEach(function (x) { if (!s[x]) { s[x] = 1; o.push(x); } }); return o; }
    function rida(silt, nimi) {
      var n = loend[nimi] || 0;
      if (!n) return null;
      var v = uniq(vaartused[nimi]);
      return '- ' + silt + ': ' + n + (v.length ? ' (' + v.slice(0, 6).join('; ') + (v.length > 6 ? '; …' : '') + ')' : '');
    }
    var kokku = [
      '- Aega lehel: ~' + min + ' min, ' + log.length + ' sammu',
      rida('Lehti avatud', 'leht'),
      rida('Autosid valitud', 'auto'),
      rida('Mõõte valitud', 'moot'),
      rida('Arvutusi', 'arvuta'),
      loend['arvuta_ilma_autota'] ? '- Vajutas „Arvuta“ ilma autota: ' + loend['arvuta_ilma_autota'] + 'x' : null,
      rida('Teeolu vahetatud', 'pind'),
      rida('Hooaeg vahetatud', 'hooaeg'),
      rida('Valimise kriteeriumid', 'kriteerium'),
      rida('Margifilter', 'margifilter'),
      rida('Otsingud', 'otsing'),
      rida('TÜHI tulemus', 'tulemusi_null'),
      rida('Võrdlusse lisatud', 'vordlusse')
    ].filter(Boolean);
    var sammud = log.map(function (r) {
      var m = Math.floor(r.s / 60), ss = r.s % 60;
      return m + ':' + (ss < 10 ? '0' : '') + ss + '  ' + r.e + (r.v ? '  ' + r.v : '');
    });
    return {
      kokkuvote: kokku.join('\n'),
      tekst: 'KOKKUVÕTE\n' + kokku.join('\n') + '\n\nSAMMUD\n' + sammud.join('\n') +
             '\n\nEkraan: ' + window.innerWidth + '×' + window.innerHeight +
             (navigator.maxTouchPoints > 0 ? ' (puuteekraan)' : ' (arvuti)'),
      sammud: log.length,
      min: min
    };
  }

  window.PM = { initPage: initPage, lugu: lugu, track: Track };

  /* SvelteKit laeb selle faili onMount'is, st PÄRAST DOMContentLoaded'i —
     siis see sündmus enam ei tule ja päis (burger, rippmenüü), infodialoog
     ja infomullid jääksid käivitamata. Käivitame kohe, kui DOM on valmis. */
  var booted = false;
  function boot() {
    if (booted) return; booted = true;
    initHeader(); initHow(); initTips();
    if (!window.PM_DEFER) initPage();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
