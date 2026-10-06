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
/* universaalid: põlvkonna rida → universaali nimi („Passat Variant“, „Octavia Combi“).
   Auto valikus eraldi mudelina, andmed samad mis põhimudelil (universaal ~60 kg
   raskem = ~0,13 m, alla veapiiri). Allikas: tookoda / Ants, 6.10.2026. */
import UNIVERSAALID from './universaalid.json';
(function () {
  'use strict';

  var CFG = window.PM_CFG || {};
  /* Keel: eesti on põhikeel. Vene/inglise lehel (/ru/, /en/) annab
     +layout.svelte sõnastiku (PM_I18N), võti = eestikeelne lähtetekst.
     Tõlge puudub → eestikeelne tekst. Analüütika sildid jäävad eesti keelde. */
  var LANG = window.PM_LANG || 'et';
  var I18N = LANG !== 'et' ? window.PM_I18N || null : null;
  var LHOME = LANG === 'et' ? (CFG.home || '/') : (CFG.home || '/') + LANG + '/';
  var DEC = LANG === 'en' ? '.' : ',';
  var HREF_T = /href="(\/(?:rehvi-valimine\/|vordle-rehve\/|liiklusohutus\/)?)(?=["?#])/g;
  function _t(s) {
    if (!I18N) return s;
    var v = I18N[s];
    if (v == null || v === '') return s;
    return v.indexOf('href="/') >= 0 ? v.replace(HREF_T, function (m, p) { return 'href="/' + LANG + p; }) : v;
  }
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
    SUMMER_UHP: _t('Suverehv (sportlik)'), SUMMER_TOURING: _t('Suverehv'), ALL_SEASON: _t('Aastaringne rehv'),
    WINTER_CENTRAL: _t('Talverehv (Kesk-Euroopa)'), WINTER_NORDIC: _t('Talverehv (Põhjamaade)'), WINTER_STUDDED: _t('Naastrehv')
  };
  /* NB: sama tabel on functions.php-s (PM_CONDS) ja metoodika tekstis. */
  var COND = {
    wet:  { surface: 'ASPHALT', waterMm: 1.0, tempC: 10, et: 'märg asfalt', label: _t('märg asfalt'), gen: _t('märja asfaldi'), short: _t('Märg') },
    dry:  { surface: 'ASPHALT', waterMm: 0.0, tempC: 15, et: 'kuiv asfalt', label: _t('kuiv asfalt'), gen: _t('kuiva asfaldi'), short: _t('Kuiv') },
    snow: { surface: 'SNOW_PACKED', waterMm: 0.0, tempC: -5, et: 'tallatud lumi', label: _t('tallatud lumi'), gen: _t('tallatud lume'), short: _t('Lumi') },
    ice:  { surface: 'ICE', waterMm: 0.0, tempC: -5, et: 'jää', label: _t('jää'), gen: _t('jää'), short: _t('Jää') }
  };
  var SEASON = {
    summer: { label: _t('Suverehv'), et: 'suverehvid', long: _t('suverehvid'), yks: _t('suverehv'), osa: _t('suverehvi'), pp: _t('suverehve'), tested: ['SUMMER_TOURING', 'SUMMER_UHP'], eprel: [0] },
    all:    { label: _t('Aastaringne'), et: 'aastaringsed rehvid', long: _t('aastaringsed rehvid'), yks: _t('aastaringne rehv'), osa: _t('aastaringset rehvi'), pp: _t('aastaringseid rehve'), tested: ['ALL_SEASON'], eprel: [1] },
    /* lamell ja aastaringne ühes: mõlemaga saab aasta läbi sõita, talvel eristab neid pidurdusmaa */
    winter: { label: _t('Lamell / aastaringne'), et: 'lamell- ja aastaringsed rehvid', long: _t('lamell- ja aastaringsed rehvid'), yks: _t('lamell- või aastaringne rehv'), osa: _t('lamell- ja aastaringset rehvi'), pp: _t('lamell- ja aastaringseid rehve'), tested: ['WINTER_CENTRAL', 'WINTER_NORDIC', 'ALL_SEASON'], eprel: [3, 2, 1] },
    /* naastrehvidel EL-i märgist ei ole — mõõdu järgi nimekirja ei saa teha, suuname talverehvide lehele */
    naast: { label: _t('Naastrehv'), et: 'naastrehvid', long: _t('naastrehvid'), yks: _t('naastrehv'), osa: _t('naastrehvi'), pp: _t('naastrehve'), tested: ['WINTER_STUDDED'], eprel: [] }
  };
  var DEFAULT_VEH = 'vw_golf_8';
  var FLAG = { GUESS: 1, CONFLICT: 2, SNOW: 4, ICE: 8 };

  /* ------------------------------------------------------------ abivahendid */
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function mmT(v) { return Math.abs(v - Math.round(v)) < 0.05 ? String(Math.round(v)) : fmt(v); }
  function fmt(n, d) { return (d == null ? n.toFixed(1) : n.toFixed(d)).replace('.', DEC); }
  /* vahe protsendina parimast: alla 10% ühe komakohaga, muidu täisarv */
  function pct(diff, base) {
    var v = 100 * diff / base;
    return '+' + (v < 10 ? fmt(v, 1) : String(Math.round(v))) + '%';
  }
  /* Poelingile UTM: pood näeb oma statistikas, et ostja tuli Pidurdusmaast
     (utm_source=pidurdusmaa). Awini jms vahenduslinke ei puutu — neil on oma jälgimine. */
  function poeLink(url, koht, rehv) {
    try {
      var u = new URL(url);
      if (/(^|\.)(awin1\.com|awin\.com)$/.test(u.hostname) || u.searchParams.has('utm_source')) return url;
      u.searchParams.set('utm_source', 'pidurdusmaa');
      u.searchParams.set('utm_medium', 'referral');
      u.searchParams.set('utm_campaign', koht || 'rehv');
      if (rehv) u.searchParams.set('utm_content', String(rehv).slice(0, 80));
      return u.toString();
    } catch (e) { return url; }
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
    return /^[A-E]$/.test(g || '') ? _t('<span class="gr ') + g + '">' + g + '</span>' : '<span class="gr x">–</span>';
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
      plaus(rida);
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
      rft: { only: 'Ainult run-flat', no: 'Ilma run-flatita' },
      main: { safe: 'Ohutus märjal', brake: 'Lühike pidurdusmaa', price: 'Soodne hind', quiet: 'Vaikne sõit', fuel: 'Väike kütusekulu', winter: 'Talvised omadused' }
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
          var tekst = val ? val.split('+').map(function (x) { return sildid[x] || x; }).join(' + ') : _t('(tühi)');
          if (GA_KRIT[g]) p[GA_KRIT[g]] = tekst;
          break;
        }
        case 'margifilter': p.mark = v; break;
        case 'vordlusse': case 'vordlusest_ara': p.rehv = v; break;
        case 'vaheleht': p.vaheleht = v; break;
        case 'partner_klikk': p.partner = v; break;
        case 'poe_klikk': p.pood = v.split(' · ')[0]; if (v.indexOf(' · ') > 0) p.rehv = v.split(' · ').slice(1).join(' · '); break;
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
    /* Olulisemad sündmused ka Plausible'isse (küpsisteta, nõusolekut ei
       vaja). Nimi = eesmärk (Goal) Plausible'is, props = kohandatud
       omadused. Plausible'is tuleb samad nimed lisada Goals alla. */
    var PLAUS = { arvuta: 'Arvutus', arvuta_ilma_autota: 'Arvutus', auto: 'Auto valitud', poe_klikk: 'Poe klikk',
      partner_klikk: 'Partneri klikk', vordlusse: 'Rehv võrdlusse', otsing: 'Otsing', oma_rehv: 'Oma rehv valitud',
      vaheleht: 'Avaleht: rehvi valimine', naita_rehve: 'Näita sobivaid rehve',
      rehvivalik_lahti: 'Rehvivalik avatud', pwa_paigaldatud: 'Rakendus paigaldatud', pwa_avatud: 'Rakendus avatud',
      jaga: 'Tulemus jagatud', jagatud_link: 'Jagatud link avatud' };
    function plaus(r) {
      var nimi = PLAUS[r.e];
      if (!nimi || typeof window.plausible !== 'function') return;
      /* avalehe sakk: loeme ainult "Leia sobiv rehv" avamist, mitte tagasi kalkulaatorisse */
      if (r.e === 'vaheleht' && r.v !== 'rehvi valimine') return;
      try {
        var p = gaParam(r), props = {};
        if (r.e === 'arvuta') { props.teeolu = p.teeolu; props.kiirus = p.kiirus; props.auto = p.auto; }
        else if (r.e === 'arvuta_ilma_autota') { props.auto = 'valimata'; }
        else if (r.e === 'auto') { props.auto = p.auto; }
        else if (r.e === 'poe_klikk') { props.pood = p.pood; if (p.rehv) props.rehv = p.rehv; }
        else if (r.e === 'partner_klikk') { props.partner = p.partner; }
        else if (r.e === 'vordlusse') { props.rehv = p.rehv; }
        else if (r.e === 'otsing') { props.otsing = String(r.v || '').split(' → ')[0].slice(0, 100); }
        for (var k in props) if (!props[k]) delete props[k];
        window.plausible(nimi, { props: props });
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
        /* „Ei leia oma autot“ tüüpautod: nimi tõlgitakse, mark (võti) jääb */
        if (I18N) d.vehicles.forEach(function (v) {
          if (v.variant) v.variant = hjT(v.variant);
          /* vene keeles: E-klass → E-Класс jne; eestikeelne nimi jääb alles (autolehe aadress, otsing) */
          if (LANG === 'ru' && v.make !== 'Ei leia oma autot') {
            v.modelEt = v.model; v.yearLabelEt = v.yearLabel;
            ['model', 'name', 'variant', 'yearLabel'].forEach(function (f) { if (v[f]) v[f] = autoRu(v[f]); });
          }
          if (v.make !== 'Ei leia oma autot') return;
          ['name', 'model', 'yearLabel', 'variant'].forEach(function (f) { if (v[f]) v[f] = _t(v[f]); });
        });
        if (I18N) Object.keys(d.sources || {}).forEach(function (k) { var x = d.sources[k]; if (x.nimi) x.nimi = _t(x.nimi); });
        core.vehByKey = {};
        d.vehicles.forEach(function (v) { core.vehByKey[v.key] = v; });
        /* vanad ABS-iga paariread (<võti>_abs): nüüd baasrida + ABS-i tuli põlemas */
        var al = d.vehAlias || {}, qa = null;
        try { qa = new URLSearchParams(location.search).get('auto'); } catch (e) {}
        Object.keys(al).forEach(function (a) {
          var b = al[a]; if (!core.vehByKey[b]) return;
          core.vehByKey[a] = core.vehByKey[b];
          if (store.get('veh', null) === a) { store.set('veh', b); absSet(b, true); }
          if (qa === a) absSet(b, true);
        });
        core.tyreByKey = {};
        d.tyres.forEach(function (t) { core.tyreByKey[t.key] = t; });
        /* Mootorid on eraldi failis (mootorid.json, ~600 KB). Kui salvestatud
           valik või link on mootori kohta (võtmes on ~), oodatakse need ära;
           muidu laetakse taustal pärast lehe avanemist. */
        var vaja = false;
        try { vaja = String(store.get('veh', '') || '').indexOf('~') > 0 || String(qa || '').indexOf('~') > 0; } catch (e) {}
        if (vaja) return laeMootorid().then(function () { return core; });
        setTimeout(laeMootorid, 1200);
        return core;
      });
  }
  /* rea mootorid -> valikud, mis kasutavad selle rea andmeid.
     kirje: [silt, kütus, aastad, slug, jrk] */
  var mootoridP = null;
  /* mootori silt „1.0 TSI · 110 hj (81 kW)“: hj → л.с. / hp */
  function autoRu(x) {
    return String(x).replace(/\b([A-Z])-klass\b/g, '$1-Класс').replace(/\b(\d)-seeria\b/g, '$1 серии').replace(/\bkaubik\b/g, 'фургон').replace(/\buniversaal\b/g, 'универсал');
  }
  /* rehvilehe aadress ilma lõpukaldkriipsuta: vene lehel /ru/rehvid/…, kui see leht on tõlgitud
     (window.PM_LINK annab +layout.svelte, vt $lib/i18n.js linkLang) */
  function rTee(slug) {
    var p = '/rehvid/' + slug + '/';
    if (window.PM_LINK) p = window.PM_LINK(p);
    return esc(p.slice(0, -1));
  }
  function hjT(x) { return I18N && x ? String(x).replace(/ hj \(/, ' ' + _t('hj') + ' (') : x; }
  function laeMootorid() {
    if (mootoridP) return mootoridP;
    mootoridP = fetch(CFG.data + 'mootorid.json?v=' + encodeURIComponent(CFG.ver || ''), { credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : {}; })
      .catch(function () { return {}; })
      .then(function (m) {
        Object.keys(m).forEach(function (k) {
          var v = core.vehByKey[k];
          if (!v || v.virt) return;
          m[k].forEach(function (e) {
            var x = Object.assign({}, v, { key: v.key + '~' + e[3], variant: hjT(e[0]), fuel: e[1],
              engYears: e[2], engOrd: e[4], virt: 1,
              name: [v.make.split(' /')[0], v.model, v.gen, e[0].split(' · ')[0]].filter(Boolean).join(' ') + ' (' + (e[2] || v.years) + ')' });
            /* mootori enda tühimass ja tehase rehvimõõdud (nt GTI 225/45 R17,
               kui põhireal on 205/55 R16); muu (pidurid, ABS, aero) reast */
            var o = e[5];
            if (o) {
              if (o.m) x.kerbMassKg = o.m;
              if (o.s) { x.oemSizes = o.s; x.oemSize = o.o || o.s[0]; x.oemConf = 'mootor'; }
              if (o.t) x.oemTyp = o.t; else delete x.oemTyp;
            }
            core.vehicles.push(x);     /* sama massiiv, mida autovalik kasutab */
            core.vehByKey[x.key] = x;
          });
        });
        try { document.dispatchEvent(new CustomEvent('pm:mootorid')); } catch (e) {}
        return core;
      });
    return mootoridP;
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
    return { key: 'c:' + g + cat, name: _t('Klass ') + g, category: cat, wetGripIndex: gmid(g, cat),
             treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null,
             ageYears: 1, studded: false, size: pretty(m), gSource: 'label' };
  }
  function condObj(ck, speed) {
    var c = COND[ck];
    return { speedKmh: speed, surface: c.surface, texture: 'NORMAL', waterMm: c.waterMm, tempC: c.tempC,
             payloadKg: 75, gradientPct: 0, reactionTimeS: 0, brakeCondition: 1 };
  }
  /* ABS oli lisavarustus: kasutaja linnuke "autol on ABS" (auto kaupa,
     sessionStorage) vahetab ABS-klassi ja pidurite võimekuse (core: absOpt). */
  function slugA(t) {
    return String(t || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }
  /* ABS on auto (põlvkonna rea), mitte mootori omadus: <rida>~<mootor> -> <rida> */
  function absKey(key) { return String(key || '').split('~')[0]; }
  function absOn(key) { var a = store.get('abs', {}); return !!(a && a[absKey(key)]); }
  function absSet(key, on) { var a = store.get('abs', {}) || {}; if (on) a[absKey(key)] = 1; else delete a[absKey(key)]; store.set('abs', a); }
  function vehEff(veh) { return veh && veh.absOpt && absOn(veh.key) ? Object.assign({}, veh, veh.absOpt) : veh; }
  function calc(tyre, veh, cond) { return window.Pidurdus.stoppingDistance(tyre, vehEff(veh), cond); }
  /* Testitud rehv autol: füüsika (laius -> akvaplaneerimine) käib autol oleva
     mõõdu järgi, mõõdu-ülekande veapiir testimõõdu (gSize) järgi.
     QA 2026-09-28: varem arvutati tulemuste lehel testimõõduga ja
     võrdluslehel autol oleva mõõduga -- sama rehv, kaks eri numbrit. */
  function onCar(t, m) { return m ? Object.assign({}, t, { size: pretty(m), gSize: t.gSize || t.size }) : t; }

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
    /* menüü: päise burger JA telefoni alariba „Menüü“ (delegeeritud — päis
       joonistatakse neutraalse lehe vahetusel uuesti) */
    var menuTaimer = null;
    function menuSea(lahti, kohe) {
      var panel = $('#pm-panel'); if (!panel) return;
      $$('[data-burger]').forEach(function (x) { x.setAttribute('aria-expanded', lahti ? 'true' : 'false'); });
      clearTimeout(menuTaimer); panel.classList.remove('sulgub');
      if (lahti) { panel.hidden = false; return; }
      if (panel.hidden) return;
      /* sulgemine: lühike hajumine, siis peidus (lehevahetusel kohe) */
      if (kohe || matchMedia('(prefers-reduced-motion: reduce)').matches) { panel.hidden = true; return; }
      panel.classList.add('sulgub');
      menuTaimer = setTimeout(function () { panel.hidden = true; panel.classList.remove('sulgub'); }, 170);
    }
    window.PM_MENU = menuSea;
    document.addEventListener('click', function (e) {
      var bb = e.target.closest && e.target.closest('[data-burger]');
      var panel = $('#pm-panel');
      if (bb) { if (panel) menuSea(panel.hidden || panel.classList.contains('sulgub')); return; }
      /* alariba lingile vajutus sulgeb lahtise menüü */
      if (panel && !panel.hidden && e.target.closest && e.target.closest('.tabbar a')) menuSea(false);
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
      var panel = $('#pm-panel');
      if (panel && !panel.hidden) menuSea(false);
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
    return LHOME + 'vordle-rehve/' + (q.length ? '?' + q.join('&') : '');
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
    /* universaalid mudelite nimekirja: „mark|nimi“ → { base: mudel, keys: põlvkonna read } */
    var UNI = {};
    Object.keys(UNIVERSAALID).forEach(function (k) {
      var v = core.vehByKey[k]; if (!v) return;
      var id = v.make + '|' + UNIVERSAALID[k];
      (UNI[id] = UNI[id] || { base: v.model, keys: {} }).keys[k] = 1;
    });
    function onMudel(v, mk, md) {
      if (v.make !== mk) return false;
      if (v.model === md) return true;
      var u = UNI[mk + '|' + md];
      return !!(u && v.model === u.base && u.keys[absKey(v.key)]);
    }
    function opts(el, list, ph) {
      var grp = null;
      el.innerHTML = '<option value="">' + esc(ph) + '</option>' + list.map(function (o) {
        var h = '';
        if (o[2] !== undefined && o[2] !== grp) { h = (grp !== null ? '</optgroup>' : '') + (o[2] ? _t('<optgroup label="') + esc(o[2]) + '">' : ''); grp = o[2]; }
        return h + _t('<option value="') + esc(o[0]) + '">' + esc(o[1]) + '</option>';
      }).join('') + (grp ? '</optgroup>' : '');
      el.disabled = !list.length;
      if (list.length === 1) el.value = list[0][0];
    }
    function uniq(arr) { var s = {}; return arr.filter(function (x) { return s[x[0]] ? false : (s[x[0]] = 1); }); }
    var GEN = 'Ei leia oma autot';
    var makes = uniq(V.map(function (v) { return [v.make, v.make]; })).filter(function (m) { return m[0] !== GEN; })
      .sort(function (a, b) { return a[1].localeCompare(b[1], 'et'); });
    /* üldised tüüpautod nimekirja lõppu, selge sildiga */
    if (V.some(function (v) { return v.make === GEN; })) makes.push([GEN, _t('— Ei leia oma autot? Vali tüüp —')]);
    opts(sel.make, makes, _t('Vali mark'));
    sel.make.value = '';
    function fill(from) {
      var mk = sel.make.value, md = sel.model.value, yr = sel.year.value;
      if (from === 'make') {
        var models = uniq(V.filter(function (v) { return v.make === mk; }).map(function (v) { return [v.model, v.model]; })
          .concat(Object.keys(UNI).filter(function (id) { return id.indexOf(mk + '|') === 0; }).map(function (id) { var n = id.slice(mk.length + 1); return [n, n]; })))
          .sort(function (a, b) { return a[1].localeCompare(b[1], 'et', { numeric: true }); });
        opts(sel.model, mk ? models : [], mk ? _t('Vali mudel') : '—');
        md = sel.model.value; from = 'model';
      }
      if (from === 'model') {
        /* põlvkonnad uusimast vanimani (algusaasta järgi) */
        var alg = function (l) { var m = /\((\d{4})/.exec(l[0]); return m ? +m[1] : 0; };
        var yrs = uniq(V.filter(function (v) { return onMudel(v, mk, md); }).map(function (v) { return [v.yearLabel, v.yearLabel]; }))
          .sort(function (a, b) { return alg(b) - alg(a); });
        opts(sel.year, md ? yrs : [], md ? _t('Vali aasta') : '—');
        yr = sel.year.value; from = 'year';
      }
      if (from === 'year') taidaMootorid();
      onChange(sel.variant.value || null);
    }
    function taidaMootorid() {
      var mk = sel.make.value, md = sel.model.value, yr = sel.year.value;
      var rows = V.filter(function (v) { return onMudel(v, mk, md) && v.yearLabel === yr; });
      var first = rows.filter(function (v) { return !v.virt; })[0];
      var jrk = function (v) { return v.engOrd != null ? v.engOrd : 1e3; };
      var mitmeKytusega = rows.some(function (v) { return v.fuel && v.fuel !== rows[0].fuel; });
      var vars = rows.slice().sort(function (a, b) { return jrk(a) - jrk(b); })
        .map(function (v) { return [v.key, v.variant === '—' ? _t('Standard') : v.variant, mitmeKytusega ? (KYTUS[v.fuel] || _t('Muu')) : undefined]; });
      opts(sel.variant, yr ? vars : [], yr ? _t('Vali mootor') : '—');
      /* mitu mootorit: vaikimisi põlvkonna põhirida (selle andmed on
         põlvkonna tüüpilised), kasutaja saab mootori ise vahetada */
      if (yr && first && !sel.variant.value) sel.variant.value = first.key;
    }
    /* mootorid saabusid taustal: täida valik uuesti, valitud auto jääb samaks */
    document.addEventListener('pm:mootorid', function () {
      if (!sel.year.value) return;
      var cur = sel.variant.value;
      taidaMootorid();
      if (cur && core.vehByKey[cur]) sel.variant.value = cur;
    });
    sel.make.addEventListener('change', function () { fill('make'); });
    vehSearch(sel, V, function (key) { api.set(key); });
    sel.model.addEventListener('change', function () { fill('model'); });
    sel.year.addEventListener('change', function () { fill('year'); });
    sel.variant.addEventListener('change', function () { onChange(sel.variant.value || null); });
    var api = {
      set: function (key) {
        var v = core.vehByKey[key]; if (!v) return;
        sel.make.value = v.make; fill('make');
        sel.model.value = v.model; fill('model');
        sel.year.value = v.yearLabel; fill('year');
        sel.variant.value = v.key; onChange(v.key);
      }
    };
    return api;
  }

  /* ------------------------------------------------------------ auto otsing
   * Kirjuta „golf 4“, „passat 2005“, „mersu w124“, „žiguli“ — pakub autosid.
   * Valik täidab mark/mudel/aasta/variant valikud (need jäävad alles). */
  /* vene tähed ladina tähtedeks (гольф → golf, шкода → shkoda); edasi AUTO_SYN */
  var KYRILL = { а: 'a', б: 'b', в: 'v', г: 'g', д: 'd', е: 'e', ё: 'e', ж: 'zh', з: 'z', и: 'i', й: 'i', к: 'k', л: 'l', м: 'm', н: 'n', о: 'o', п: 'p', р: 'r', с: 's', т: 't', у: 'u', ф: 'f', х: 'h', ц: 'ts', ч: 'ch', ш: 'sh', щ: 'sch', ъ: '', ы: 'y', ь: '', э: 'e', ю: 'yu', я: 'ya' };
  function lihtne(t) {
    return String(t || '').toLowerCase().replace(/[а-яё]/g, function (c) { return KYRILL[c]; }).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9+]+/g, ' ').trim();
  }
  var ROOMA = { i: 1, ii: 2, iii: 3, iv: 4, v: 5, vi: 6, vii: 7, viii: 8, ix: 9, x: 10 };
  var ROOMA_T = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'];
  var AUTO_SYN = {
    vw: 'volkswagen', folks: 'volkswagen', mersu: 'mercedes', merc: 'mercedes', mb: 'mercedes', benz: 'mercedes',
    bemm: 'bmw', ziguli: 'lada', zhiguli: 'lada', zigul: 'lada', vaz: 'lada', moskvich: 'moskvits', moskvitch: 'moskvits',
    shkoda: 'skoda', citroen: 'citroen', alfa: 'alfa', chevy: 'chevrolet', landrover: 'land rover',
    /* venekeelne otsing (pärast lihtne() translit'it): мерседес, тойота, октавия … */
    mersedes: 'mercedes', mers: 'mercedes', folksvagen: 'volkswagen', foltsvagen: 'volkswagen',
    toiota: 'toyota', bmv: 'bmw', reno: 'renault', pezho: 'peugeot', sitroen: 'citroen', hendai: 'hyundai', hundai: 'hyundai',
    hiundai: 'hyundai', hendee: 'hyundai', hyundai: 'hyundai', mitsubisi: 'mitsubishi', dachiya: 'dacia', leksus: 'lexus',
    porshe: 'porsche', kupra: 'cupra', dzhip: 'jeep', yaguar: 'jaguar', lend: 'land', shevrole: 'chevrolet', kraisler: 'chrysler',
    ssangiong: 'ssangyong', tuareg: 'touareg', oktaviya: 'octavia', oktavia: 'octavia', fabiya: 'fabia', kodiak: 'kodiaq',
    korolla: 'corolla', kamri: 'camry', fokus: 'focus', korsa: 'corsa', vektra: 'vectra', insigniya: 'insignia', klio: 'clio',
    megan: 'megane', daster: 'duster', sid: 'ceed', sporteidzh: 'sportage', solyaris: 'solaris', tukson: 'tucson',
    autlender: 'outlander', lanser: 'lancer', padzhero: 'pajero', kashkai: 'qashqai', sivik: 'civic', akkord: 'accord',
    autbek: 'outback', legasi: 'legacy', svift: 'swift', dodzh: 'dodge', kadillak: 'cadillac', lanchiya: 'lancia', lanchia: 'lancia', zaporozhets: 'zaporozets', zaporozhec: 'zaporozets', seriya: '', serii: '', klass: '', kupe: 'coupe', universal: ''
  };
  var KYTUS = { b: _t('Bensiin'), bg: _t('Bensiin / gaas'), g: _t('Gaas'), d: _t('Diisel'), h: _t('Hübriid'), p: _t('Pistikhübriid'), e: _t('Elekter') };
  function vehSearch(sel, V, onPick) {
    var dark = sel.make.classList.contains('sel');
    var host = sel.make.parentNode;
    var wrap = document.createElement('div');
    wrap.className = 'vs' + (dark ? ' vs-dark' : '');
    var lid = 'vs' + Math.random().toString(36).slice(2, 7);
    wrap.innerHTML = _t('<input type="search" class="') + esc(sel.make.className) + _t(' vs-in" placeholder="Otsi autot, nt Golf 4 või Passat 2005" ') +
      _t('autocomplete="off" spellcheck="false" role="combobox" aria-expanded="false" aria-autocomplete="list" aria-controls="') + lid + _t('" aria-label="Otsi autot">') +
      _t('<ul class="vs-list" id="') + lid + _t('" role="listbox" hidden></ul>');
    host.parentNode.insertBefore(wrap, host);
    var inp = $('input', wrap), list = $('ul', wrap), hits = [], act = -1;

    var idx = V.filter(function (v) { return v.make !== 'Ei leia oma autot' && !v.virt; }).map(function (v) {
      var g = lihtne(v.gen), extra = '';
      if (ROOMA[g]) extra = ' ' + ROOMA[g];
      else if (/^\d+$/.test(g) && ROOMA_T[+g]) extra = ' ' + ROOMA_T[+g];
      var y = /^(\d{4})(?:\s*[-–]\s*(\d{4}))?(\+)?/.exec(String(v.years || ''));
      return {
        v: v,
        hay: ' ' + lihtne([v.make, v.model, v.modelEt, v.gen, v.variant, v.name, v.body, UNIVERSAALID[v.key] || ''].join(' ')) + extra + ' ',
        y0: y ? +y[1] : 0, y1: y ? (y[2] ? +y[2] : (y[3] ? 2030 : +y[1])) : 0
      };
    });

    function otsi(q) {
      var toks = lihtne(q).split(' ').filter(Boolean).map(function (t) { return AUTO_SYN[t] != null ? AUTO_SYN[t] : t; }).filter(Boolean);
      if (!toks.length) return [];
      var out = [];
      idx.forEach(function (x) {
        var score = 0;
        for (var i = 0; i < toks.length; i++) {
          var t = toks[i];
          if (/^(19|20)\d\d$/.test(t)) {
            var yy = +t;
            if (x.y0 && yy >= x.y0 - 1 && yy <= x.y1 + 1) { score += 2; continue; }
            return;
          }
          var at = x.hay.indexOf(' ' + t);
          if (at < 0) { if (x.hay.indexOf(t) < 0) return; score += 1; }
          else score += (x.hay.indexOf(' ' + t + ' ') >= 0 ? 4 : 3);
        }
        out.push({ x: x, s: score });
      });
      out.sort(function (a, b) { return b.s - a.s || (b.x.y0 - a.x.y0) || a.x.v.name.localeCompare(b.x.v.name, 'et'); });
      return out.slice(0, 8).map(function (o) { return o.x.v; });
    }
    function show() {
      list.innerHTML = hits.length ? hits.map(function (v, i) {
        return _t('<li role="option" id="') + lid + '-' + i + _t('" data-i="') + i + _t('" aria-selected="') + (i === act) + '">' +
          '<b>' + esc(v.make + ' ' + v.model) + '</b> ' + esc((v.yearLabel || '') + (v.variant && v.variant !== '—' ? ' · ' + v.variant : '')) +
          ' <span class="vs-m">' + esc(v.oemSize || '') + '</span></li>';
      }).join('') : (inp.value.trim().length > 1 ? _t('<li class="vs-none" role="presentation">Ei leidnud. Proovi ainult marki või mudelit, või vali allpool.</li>') : '');
      var open = !!list.innerHTML;
      list.hidden = !open;
      inp.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (act >= 0) inp.setAttribute('aria-activedescendant', lid + '-' + act); else inp.removeAttribute('aria-activedescendant');
    }
    function vali(i) {
      var v = hits[i]; if (!v) return;
      onPick(v.key);
      inp.value = v.make + ' ' + v.model + ' ' + (v.yearLabel || '');
      hits = []; act = -1; show(); list.hidden = true; inp.setAttribute('aria-expanded', 'false');
      Track('auto_otsing', v.make + ' ' + v.model);
    }
    inp.addEventListener('input', function () { hits = otsi(inp.value); act = hits.length ? 0 : -1; show(); });
    inp.addEventListener('focus', function () { if (inp.value) { hits = otsi(inp.value); act = hits.length ? 0 : -1; show(); } });
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' && hits.length) { act = (act + 1) % hits.length; show(); e.preventDefault(); }
      else if (e.key === 'ArrowUp' && hits.length) { act = (act - 1 + hits.length) % hits.length; show(); e.preventDefault(); }
      else if (e.key === 'Enter' && act >= 0) { vali(act); e.preventDefault(); }
      else if (e.key === 'Escape') { list.hidden = true; inp.setAttribute('aria-expanded', 'false'); }
    });
    /* käsitsi valitud mark/mudel → otsingu tekst ei vasta enam, tühjenda */
    ['make', 'model', 'year', 'variant'].forEach(function (k) { sel[k].addEventListener('change', function () { inp.value = ''; }); });
    list.addEventListener('mousedown', function (e) { e.preventDefault(); });
    list.addEventListener('click', function (e) { var li = e.target.closest('[data-i]'); if (li) vali(+li.dataset.i); });
    inp.addEventListener('blur', function () { setTimeout(function () { list.hidden = true; inp.setAttribute('aria-expanded', 'false'); }, 120); });
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
      h += _t('<optgroup label="') + esc(veh.model + _t(' tehasemõõdud')) + '">' + fab.map(function (m) {
        var known = core.eprelSizes.indexOf(m) >= 0;
        return _t('<option value="') + esc(m) + '">' + esc(pretty(m)) + (m === oem ? _t(' · levinuim') : '') +
          (known ? '' : _t(' (märgise andmed puuduvad)')) + '</option>';
      }).join('') + '</optgroup>';
    }
    h += _t('<optgroup label="') + (fab.length ? _t('Muu mõõt') : _t('Rehvimõõt')) + '">' + list.filter(function (s) { return fab.indexOf(s.m) < 0; }).map(function (s) {
      return _t('<option value="') + esc(s.m) + '">' + esc(s.label) + ' · ' + s.n + _t(' rehvi</option>');
    }).join('') + '</optgroup>';
    el.innerHTML = h;
    el.value = current && $('option[value="' + current + '"]', el) ? current : (oem || '20555R16');
    sizePicker(el);
    return el.value;
  }

  /* ------------------------------------------------------------ mõõdu valik
   * Kolm väikest lahtrit nagu rehvi küljel: laius / kõrgus R velg
   * (205 / 55 R 16). Saab kirjutada või valida pakutud väärtustest;
   * pakutakse ainult neid, mis eelmiste lahtritega koos olemas on.
   * Päris <select data-f="size"> jääb alles (peidetuna) — ülejäänud kood
   * loeb ja kuulab seda; siin seatakse selle väärtus ja saadetakse 'change'. */
  var SP_RE = /^(\d{3})(\d{2})R(\d{2}C?)$/;
  function sizePicker(el) {
    var nOf = {};
    (core && core.sizes || []).forEach(function (x) { nOf[x.m] = x.n; });
    /* kõik mõõdud, mille kohta on märgiseandmed (ka harvad) + valikus olevad */
    var koik = {};
    $$('option', el).forEach(function (o) { if (SP_RE.test(o.value)) koik[o.value] = 1; });
    (core && core.eprelSizes || []).forEach(function (m) { if (SP_RE.test(m)) koik[m] = 1; });
    var opts = Object.keys(koik).map(function (v) { var m = SP_RE.exec(v); return { v: v, w: m[1], p: m[2], r: m[3] }; });

    var box = el._sp;
    if (!box) {
      box = document.createElement('div');
      box.className = 'sp';
      var id = el.id || ('sp' + Math.random().toString(36).slice(2, 7));
      var cls = el.className;
      /* kõigil kolmel numbriklaviatuur; kaubiku „C“ mõõdud (16C) tulevad velje soovitustest */
      var f = function (k, t, ml, i) {
        return '<label class="sp-f"><span class="sp-l">' + t + _t('</span><input class="') + esc(cls) + _t(' sp-in" id="') + esc(id + (i ? '-' + k : '')) +
          _t('" data-sp="') + k + _t('" list="') + esc(id + '-dl-' + k) + _t('" inputmode="numeric" maxlength="') + ml +
          _t('" autocomplete="off" spellcheck="false"><datalist id="') + esc(id + '-dl-' + k) + '"></datalist></label>';
      };
      box.innerHTML = '<div class="sp-row">' + f('w', _t('Laius'), 3, 0) + '<span class="sp-sep" aria-hidden="true">/</span>' +
        f('p', _t('Kõrgus'), 2, 1) + '<span class="sp-sep" aria-hidden="true">R</span>' + f('r', _t('Velg'), 3, 2) + '</div>' +
        '<p class="sp-msg" data-sp-msg aria-live="polite"></p>';
      /* vana silt (for="f-size") osutab nüüd laiuse lahtrile */
      if (el.id) el.id = el.id + '-kogu';
      el.hidden = true;
      el.setAttribute('aria-hidden', 'true');
      el.tabIndex = -1;
      el.parentNode.insertBefore(box, el.nextSibling);
      el._sp = box;

      var inp = { w: $('[data-sp=w]', box), p: $('[data-sp=p]', box), r: $('[data-sp=r]', box) };
      var msg = $('[data-sp-msg]', box);
      var puhas = function (k) {
        var v = inp[k].value.toUpperCase().replace(k === 'r' ? /[^0-9C]/g : /[^0-9]/g, '');
        if (k === 'r') v = v.replace(/^R/, '');
        if (v !== inp[k].value) inp[k].value = v;
        return v;
      };
      var proovi = function (lopp) {
        var w = puhas('w'), p = puhas('p'), r = puhas('r');
        msg.textContent = '';
        lists();
        if (w.length < 3 || p.length < 2 || r.length < 2) {
          if (lopp && (w || p || r)) msg.textContent = _t('Kirjuta kõik kolm: nt 205 / 55 R 16.');
          return;
        }
        var v = w + p + 'R' + r;
        if (!box._koik[v]) { msg.textContent = _t('Mõõtu ') + w + '/' + p + ' R' + r + _t(' andmebaasis veel pole.'); return; }
        if (!$('option[value="' + v + '"]', el)) {
          var g = $$('optgroup', el).pop() || el;
          var o = document.createElement('option'); o.value = v; o.textContent = pretty(v);
          g.appendChild(o);
        }
        if (v !== el.value) {
          el.value = v;
          el.dispatchEvent(new Event('change', { bubbles: true }));
        }
      };
      ['w', 'p', 'r'].forEach(function (k, i) {
        inp[k].addEventListener('input', function () {
          var v = puhas(k);
          /* täis → järgmisse lahtrisse */
          if (k === 'w' && v.length === 3) inp.p.focus();
          if (k === 'p' && v.length === 2) inp.r.focus();
          proovi(false);
        });
        /* lahtrisse minnes on sisu valitud: kirjutamine asendab selle */
        var vaarske = false;
        inp[k].addEventListener('focus', function () { inp[k].select(); vaarske = true; });
        inp[k].addEventListener('mouseup', function (e) { if (vaarske) { e.preventDefault(); vaarske = false; } });
        inp[k].addEventListener('keydown', function (e) {
          if (e.key === 'Backspace' && !inp[k].value && i) { e.preventDefault(); inp[['w', 'p', 'r'][i - 1]].focus(); }
          if (e.key === 'Enter') { e.preventDefault(); proovi(true); }
        });
      });
      box.addEventListener('focusout', function (e) {
        if (box.contains(e.relatedTarget)) return;
        proovi(true);
        /* pooleli jäänud lahtrid tagasi kehtivale mõõdule */
        if (msg.textContent) setTimeout(function () { box._sync(); }, 2500);
      });
      /* pakutud väärtused: ainult need, mis eelmiste lahtritega kokku sobivad */
      var lists = function () {
        var w = inp.w.value, p = inp.p.value, o = box._opts;
        var uniq = function (a) { return a.filter(function (x, i) { return a.indexOf(x) === i; }).sort(function (a, b) { return parseInt(a, 10) - parseInt(b, 10) || a.localeCompare(b); }); };
        var dl = function (k, vals) { $('#' + CSS.escape(inp[k].getAttribute('list')), box).innerHTML = vals.map(function (v) { return _t('<option value="') + esc(v) + '">'; }).join(''); };
        dl('w', uniq(o.map(function (x) { return x.w; })));
        dl('p', uniq(o.filter(function (x) { return x.w === w; }).map(function (x) { return x.p; })));
        dl('r', uniq(o.filter(function (x) { return x.w === w && x.p === p; }).map(function (x) { return x.r; })));
      };
      box._sync = function () {
        var m = SP_RE.exec(el.value) || [];
        inp.w.value = m[1] || ''; inp.p.value = m[2] || ''; inp.r.value = m[3] || '';
        msg.textContent = '';
        lists();
      };
    }
    box._opts = opts;
    box._koik = koik;
    box._sync();
  }

  /* ------------------------------------------------------------ kalkulaator */
  function initCalc(root) {
    var S = { veh: store.get('veh', null), size: '20555R16', speed: 90, cond: 'wet', season: 'summer' };
    S.tab = 'calc';
    var qsc = new URLSearchParams(location.search);
    if (qsc.get('moot')) S.size = qsc.get('moot');
    /* autolehelt (/autod/…): ?auto=<rea võti> valib auto kohe ära */
    if (qsc.get('auto') && core.vehByKey[qsc.get('auto')]) S.veh = qsc.get('auto');
    /* artiklite lingid: /?olud=snow&kiirus=50#kalkulaator */
    if (COND[qsc.get('olud')]) S.cond = qsc.get('olud');
    var qKiirus = +qsc.get('kiirus');
    if (qKiirus >= 20 && qKiirus <= 130) S.speed = Math.round(qKiirus / 5) * 5;
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
      if (shown) { goLabel(_t('Arvuta uuesti')); goBtn.classList.add('stale'); }
    }

    /* ---- 5. Sinu praegune rehv (valikuline) */
    S.minu = null;
    (function () {
      var inp = $('[data-own-in]', root), list = $('[data-own-list]', root), hint = $('[data-own-hint]', root);
      if (!inp || !list) return;
      var hits = [], act = -1, valitudNimi = '';
      function vihje(t) { if (hint) { hint.textContent = t || ''; hint.hidden = !t; } }
      function otsi(q, rows) {
        var toks = lihtne(q).split(' ').filter(Boolean);
        if (!toks.length) return [];
        var sobib = function (hay) { hay = ' ' + lihtne(hay) + ' '; return toks.every(function (t) { return hay.indexOf(t) >= 0; }); };
        var out = [], seen = {}, tested = {};
        rows.forEach(function (r) {
          if (seen[r.slug] || !sobib(r.mark + ' ' + r.name)) return;
          seen[r.slug] = 1; if (r.tested) tested[r.tested] = 1;
          out.push({ e: r.slug, n: r.mark + ' ' + r.name, s: KAT_SILT[r.catNr] || '', g: r.g });
        });
        /* testitud rehvid, mida sinu mõõdus EPREL-is ei ole (nt naastrehvid) */
        core.tyres.forEach(function (t) {
          if (tested[t.key] || !sobib(t.name)) return;
          out.push({ t: t.key, n: t.name, s: tyypSilt(t.category) + _t(' · test mõõdus ') + t.size });
        });
        return out.slice(0, 8);
      }
      function naita() {
        list.innerHTML = hits.length ? hits.map(function (h, i) {
          return _t('<li role="option" id="own-o') + i + _t('" data-i="') + i + _t('" aria-selected="') + (i === act) + '"><b>' + esc(h.n) + '</b>' +
            (h.g ? ' ' + grade(h.g) : '') + ' <span class="own-t">' + esc(h.s) + '</span></li>';
        }).join('') : (inp.value.trim().length > 1 ? _t('<li class="vs-none" role="presentation">Mõõdus ') + esc(pretty(S.size)) + _t(' sellist rehvi ei leidnud. Kontrolli mõõtu või kirjuta ainult mudeli nimi.</li>') : '');
        var open = !!list.innerHTML;
        list.hidden = !open; inp.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (act >= 0) inp.setAttribute('aria-activedescendant', 'own-o' + act); else inp.removeAttribute('aria-activedescendant');
      }
      function vali(i) {
        var h = hits[i]; if (!h) return;
        S.minu = h.e ? { e: h.e, n: h.n } : { t: h.t, n: h.n };
        valitudNimi = inp.value = h.n;
        hits = []; act = -1; naita(); list.hidden = true;
        vihje(h.s ? h.s.charAt(0).toUpperCase() + h.s.slice(1) + _t(' — võrdleme sama hooaja rehvidega.') : '');
        Track('oma_rehv', h.n);
        recalc();
      }
      function otsiNyyd() {
        var q = inp.value;
        loadSize(S.size).then(function (rows) { if (inp.value !== q) return; hits = otsi(q, rows); act = hits.length ? 0 : -1; naita(); });
      }
      inp.addEventListener('input', function () {
        if (S.minu && inp.value !== valitudNimi) { S.minu = null; vihje(''); recalc(); }
        otsiNyyd();
      });
      inp.addEventListener('focus', function () { if (inp.value && !S.minu) otsiNyyd(); });
      inp.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown' && hits.length) { act = (act + 1) % hits.length; naita(); e.preventDefault(); }
        else if (e.key === 'ArrowUp' && hits.length) { act = (act - 1 + hits.length) % hits.length; naita(); e.preventDefault(); }
        else if (e.key === 'Enter' && act >= 0) { vali(act); e.preventDefault(); }
        else if (e.key === 'Escape') { list.hidden = true; inp.setAttribute('aria-expanded', 'false'); }
      });
      list.addEventListener('mousedown', function (e) { e.preventDefault(); });
      list.addEventListener('click', function (e) { var li = e.target.closest('[data-i]'); if (li) vali(+li.dataset.i); });
      inp.addEventListener('blur', function () { setTimeout(function () { list.hidden = true; inp.setAttribute('aria-expanded', 'false'); }, 120); });
    })();

    /* mustrisügavus (valikuline): kulunud praegused rehvid vs uued.
       Liugur: paremal „uus“ (8 mm), vasakule kulunud. Kui tulemus on juba
       ekraanil ja muud valikud pole muutunud, uueneb tulemus kohe. */
    S.muster = null;
    var mmIn = $('[data-f=muster]', root), mmV = $('[data-mm-v]', root), mmN = $('[data-mm-n]', root);
    var MM_N0 = mmN ? mmN.textContent : '';
    function mmPaint() {
      if (!mmIn) return;
      var v = +mmIn.value, uus = v >= 7.95;
      mmIn.style.setProperty('--p', (100 * (v - 1.6) / (8 - 1.6)).toFixed(1) + '%');
      if (mmV) { mmV.textContent = uus ? _t('uus') : mmT(v) + _t(' mm'); mmV.classList.toggle('kulu', !uus); }
      if (mmN) {
        var t = uus ? MM_N0 : v < 1.6 + 0.05 ? _t('Seaduslik miinimum (suverehv). Talverehvil peab olema vähemalt 3 mm.')
          : v < 3 ? _t('Talverehvi miinimum on 3 mm — suverehvina veel lubatud (1,6 mm).')
          : v < 4 ? _t('Kulunud: märjal ja lumel pidurdab märgatavalt halvemini.')
          : _t('Tulemuses näed, kui palju uued rehvid samades oludes varem peatuvad.');
        mmN.textContent = t; mmN.classList.toggle('hoiatus', !uus && v < 3);
      }
      S.muster = uus ? null : Math.round(v * 10) / 10;
    }
    if (mmIn) {
      mmIn.value = 8; mmPaint();
      mmIn.addEventListener('input', mmPaint);
      mmIn.addEventListener('change', function () {
        mmPaint();
        Track('muster', S.muster ? S.muster + ' mm' : 'uus');
        if (shown && !goBtn.classList.contains('stale')) {
          loadSize(S.size).then(function (rows) { Result.show(Object.assign({}, S), rows); });
        } else recalc();
      });
    }

    var picker = VehPicker(root, function (key) {
      /* mark → mudel → aasta: vahepealsed sammud (auto veel valimata) ei muuda midagi */
      if (!key && !S.veh) return;
      S.veh = key;
      var veh = key ? core.vehByKey[key] : null;
      if (veh) Track('auto', veh.make + ' ' + veh.model + ' ' + veh.yearLabel);
      S.size = sizeOptions(sizeSel, veh, veh && !qsc.get('moot') ? norm(veh.oemSize) : S.size);
      qsc.delete('moot');
      paintSize(); save(); recalc(); emit();
      /* oemTyp: levinuim mõõt, mille kohta märgise andmeid veel pole —
         siis arvutatakse teise tehasemõõduga ja seda öeldakse välja */
      paintAbs(veh);
      var hint = !veh ? '' : veh.oemTyp
        ? _t('levinuim tehasemõõt ') + veh.oemTyp + _t(' · arvutame ') + veh.oemSize + _t(' järgi')
        : _t('levinuim tehasemõõt ') + veh.oemSize;
      /* link auto lehele (/autod/<mark>/<mudel-põlvkond>/), sama slug mis serveris */
      var al = veh && veh.make && veh.model && veh.make !== 'Ei leia oma autot'
        ? (LANG === 'ru' ? '/ru' : '') + '/autod/' + slugA(veh.make.split(' /')[0]) + '/' + slugA((veh.modelEt || veh.model) + ' ' + (veh.yearLabelEt || veh.yearLabel)) + '/' : '';
      $('[data-veh-hint]', root).innerHTML = esc(hint) + (al ? _t(' · <a href="') + esc(al) + _t('">auto leht</a>') : '');
    });
    S.size = sizeOptions(sizeSel, null, S.size);

    /* ABS-i tuli variandi kõrval: standard = põleb (ei muudeta), lisavarustus =
       vajutatav, puudus = kustunud (ei muudeta) */
    var absBtn = $('[data-abs]', root), absTxt = absBtn ? $('[data-abs-t]', absBtn) : null;
    function absState(veh) { return !veh ? '' : veh.absOpt ? 'opt' : veh.absClass === 'NONE' ? 'none' : 'std'; }
    function paintAbs(veh) {
      if (!absBtn) return;
      var st = absState(veh), on = st === 'std' || (st === 'opt' && absOn(veh.key));
      absBtn.hidden = !st;
      absBtn.classList.remove('lit');
      absBtn.dataset.st = st;
      absBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      absBtn.setAttribute('aria-disabled', st === 'opt' ? 'false' : 'true');
      absBtn.title = st === 'std' ? _t('ABS on selle auto standardvarustus.')
        : st === 'none' ? _t('Sellel autol ABS-i ei olnud.')
        : _t('ABS oli selle auto lisavarustus. Kui armatuuril süttib käivitamisel hetkeks ABS-tuli, on sinu autol ABS. Vajuta tulele, kui sul on ABS.');
      if (absTxt) absTxt.textContent = on ? _t('ABS olemas') : st === 'none' ? _t('ABS-i pole') : _t('Kas on ABS?');
    }
    if (absBtn) absBtn.addEventListener('click', function () {
      if (!S.veh || absBtn.dataset.st !== 'opt') return;
      var on = absBtn.getAttribute('aria-pressed') !== 'true';
      absSet(S.veh, on);
      paintAbs(core.vehByKey[S.veh]);
      if (on) { void absBtn.offsetWidth; absBtn.classList.add('lit'); }
      Track('abs', on ? 'jah' : 'ei');
      recalc(); emit();
    });

    function paintSize() {
      var veh = S.veh ? core.vehByKey[S.veh] : null;
      sizeTag.hidden = !veh;
      if (veh) {
        var fab = (veh.oemSizes && veh.oemSizes.length ? veh.oemSizes.map(norm) : [norm(veh.oemSize)]);
        var on = fab.indexOf(S.size) >= 0;
        sizeTag.textContent = on ? _t('✓ Tehasemõõt') : _t('Ei ole selle auto tehasemõõt (tehases: ') + fab.map(pretty).join(', ') + ')';
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

    /* Kiirust saab valida kõigil pindadel 130 km/h-ni. Üle mõõdetud vahemiku
       (lumel ja jääl 80 km/h) arvutab mudel valemist edasi ja veapiir
       kasvab (engine.js: sigmaSpeedExtrap) — seda öeldakse ka välja. */
    var SPEED_MAX = 130;
    function range() {
      var rng = window.Pidurdus.CAL.speedRange[COND[S.cond].surface] || [20, SPEED_MAX];
      return [Math.max(20, Math.ceil(rng[0] / 5) * 5), SPEED_MAX, Math.floor(rng[1] / 5) * 5];
    }
    function paintSpeed() {
      var r = range(), lo = r[0], hi = r[1], moodetud = r[2];
      S.speed = Math.min(hi, Math.max(lo, S.speed));
      speedIn.min = lo; speedIn.max = hi; speedNum.min = lo; speedNum.max = hi;
      speedIn.value = S.speed; speedNum.value = S.speed;
      speedIn.style.setProperty('--p', (100 * (S.speed - lo) / (hi - lo)) + '%');
      capNote.hidden = S.speed <= moodetud;
      if (!capNote.hidden) capNote.textContent = (S.cond === 'snow' ? _t('Lumel') : S.cond === 'ice' ? _t('Jääl') : _t('Sellel pinnal')) +
        _t(' on pidurdusmaa mõõdetud kuni ') + moodetud + _t(' km/h. Kiirematel arvutame valemist edasi — veapiir on suurem.');
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
        Track('pind', COND[S.cond].et);
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
      /* vahelehti enam pole: „valik“ = näita järgmist sammu (rehvide nimekiri) */
      if (tab === 'valik') naitaValik();
    }
    function smooth() { return matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'; }
    var goV = $('[data-go-valik]', root);
    if (goV) goV.addEventListener('click', function () {
      Track('naita_rehve', 'avaleht');
      var t = $('#sobivad'); if (t) t.scrollIntoView({ behavior: smooth(), block: 'start' });
    });
    /* tulemuse riba „Näita sobivaid rehve“ → järgmine samm samal lehel */
    var rv = $('[data-r-valik]');
    if (rv) rv.addEventListener('click', function (e) {
      e.preventDefault(); naitaValik(); hvAva(true);
      Track('naita_rehve', 'avaleht');
      var t = $('#sobivad'); if (t) t.scrollIntoView({ behavior: smooth(), block: 'start' });
    });
    /* järgmine samm (rehvide valik) ilmub pärast arvutust; „terve leht“ nupp viib
       rehvi valimise lehele sama auto ja mõõduga */
    var vf = $('[data-valik-full]');
    if (vf) vf.addEventListener('click', function () {
      var on = $('[data-home=valik] [data-season][aria-pressed="true"]');
      if (on) { var u = new URL(vf.getAttribute('href'), location.href); u.searchParams.set('hooaeg', on.dataset.season); vf.setAttribute('href', u.pathname + u.search); }
      Track('naita_rehve', 'rehvi valimise leht');
    });
    /* järgmise sammu küsimused + nimekiri on vaikimisi kinni (esileht ei
       upu infosse); nupp avab ja sulgeb */
    var hvTog = $('[data-hv-tog]'), hvBody = $('[data-hv-body]');
    function hvAva(lahti, kust) {
      if (!hvTog || !hvBody) return;
      hvBody.hidden = !lahti;
      hvTog.setAttribute('aria-expanded', lahti ? 'true' : 'false');
      var tt = $('[data-hv-tog-t]', hvTog); if (tt) tt.textContent = lahti ? _t('Peida küsimused ja rehvid') : _t('Ava küsimused ja rehvid');
      if (kust) Track('rehvivalik_' + (lahti ? 'lahti' : 'kinni'), kust);
      if (lahti) try { window.dispatchEvent(new Event('resize')); } catch (e) {}
    }
    if (hvTog) hvTog.addEventListener('click', function () { hvAva(hvBody.hidden, 'nupp'); });
    var hvS = $('[data-hv-sulge]');
    if (hvS) hvS.addEventListener('click', function () {
      hvAva(false, 'all');
      var t = $('#sobivad'); if (t) t.scrollIntoView({ behavior: smooth(), block: 'start' });
    });
    function naitaValik() {
      var v = $('[data-home=valik]'); if (v) v.hidden = false;
      var f = $('[data-valik-full]');
      if (f) {
        var u = new URL(f.getAttribute('href'), location.href);
        if (S.veh) u.searchParams.set('auto', S.veh); else u.searchParams.delete('auto');
        u.searchParams.set('moot', S.size);
        f.setAttribute('href', u.pathname + u.search);
      }
    }

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
      Track('arvuta', (av ? av.make + ' ' + av.model : 'tüüpauto') + ' · ' + pretty(S.size) + ' · ' + S.speed + ' km/h · ' + COND[S.cond].et);
      loadSize(S.size).then(function (rows) {
        Result.show(Object.assign({}, S), rows);
        shown = true; goLabel(_t('Arvuta pidurdusmaa')); goBtn.classList.remove('stale');
        /* rehvide nimekiri (tulemuse all) arvutab rehvid läbi (~1,7 s keskmises
           telefonis): alles siis, kui tulemus on ekraanil ja kerimine läbi —
           muidu leht hakib just tulemuse juurde kerides (FB tagasiside) */
        setTimeout(function () {
          if (window.requestIdleCallback) requestIdleCallback(naitaValik, { timeout: 1500 }); else naitaValik();
        }, 700);
        var res = $('#tulemus');
        if (!res) return;
        res.hidden = false;
        /* tulemus päise alla (kleepuv päis ei tohi pealkirja katta) */
        var hdr = $('.site-header'), hh = hdr ? hdr.getBoundingClientRect().height : 64;
        var siht = res.getBoundingClientRect().top + window.scrollY - hh - 12;
        if (Math.abs(window.scrollY - siht) > 24) {
          window.scrollTo({ top: Math.max(0, siht), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
        }
        var big = $('[data-r-big]'); if (big) { big.parentNode.classList.remove('flash'); void big.offsetWidth; big.parentNode.classList.add('flash'); }
      });
    }
    var useDefault = false; /* kasutaja valis „arvuta tüüpilise auto järgi“ */
    goBtn.addEventListener('click', function () { compute(useDefault); });
    var goDef = $('[data-go-default]', root);
    if (goDef) goDef.addEventListener('click', function () { useDefault = true; compute(true); });

    if (S.veh && core.vehByKey[S.veh]) picker.set(S.veh); else recalc();
    /* jagatud link (?arvuta=1): näita sama tulemust kohe */
    if (qsc.get('arvuta') === '1') { Track('jagatud_link', (S.veh || '') + ' · ' + S.size); setTimeout(function () { compute(true); }, 250); }
  }

  /* ------------------------------------------------------------ tulemus */
  /* ---- SINU REHV (valikuline): EPREL-i rida sinu mõõdus või testitud rehv */
  var KAT_HOOAEG = { 0: 'summer', 1: 'winter', 2: 'winter', 3: 'winter' };
  /* rehvi liik kaardil: lühike ja selge */
  var KAT_KAART = { 0: _t('Suverehv'), 1: _t('Aastaringne'), 2: _t('Lamell (Kesk-Euroopa)'), 3: _t('Lamell (Põhjamaade)') };
  var KAT_SILT = { 0: _t('suverehv'), 1: _t('aastaringne'), 2: _t('Kesk-Euroopa talverehv'), 3: _t('Põhjamaade talverehv') };
  function tyypHooaeg(cat) { return /^SUMMER/.test(cat) ? 'summer' : cat === 'WINTER_STUDDED' ? 'naast' : 'winter'; }
  function tyypSilt(cat) {
    return { SUMMER_UHP: _t('sportlik suverehv'), SUMMER_TOURING: _t('suverehv'), ALL_SEASON: _t('aastaringne'), WINTER_CENTRAL: _t('Kesk-Euroopa talverehv'),
             WINTER_NORDIC: _t('Põhjamaade talverehv'), WINTER_STUDDED: _t('naastrehv') }[cat] || '';
  }
  /* minu = { e: slug } (märgisega rehv sinu mõõdus) või { t: key } (testitud rehv) */
  function minuLeia(minu, eprelRows) {
    if (!minu) return null;
    if (minu.e) {
      var r = eprelRows.filter(function (x) { return x.slug === minu.e; })[0];
      if (!r) return { puudu: true, nimi: minu.n };
      var t = r.tested ? core.tyreByKey[r.tested] : null;
      return { r: r, t: t, nimi: r.mark + ' ' + r.name, hooaeg: KAT_HOOAEG[r.catNr] || 'summer', silt: KAT_SILT[r.catNr] || '' };
    }
    var tt = core.tyreByKey[minu.t];
    if (!tt) return null;
    var er = eprelRows.filter(function (x) { return x.tested === tt.key; })[0] || null;
    return { r: er, t: tt, nimi: tt.name, hooaeg: tyypHooaeg(tt.category), silt: tyypSilt(tt.category) };
  }

  var Result = (function () {
    var el, state, rowsAll, sel, showAll = false;
    /* Klassi rea all päris rehvid: pick[klassiRida] = valitud rehvi slug.
       Vaikimisi valitakse üks ise (soodsaim / testitud / vaikseim), et
       inimene ei peaks 12 rehvi vahel otsustama — aga saab vahetada. */
    var pick = {}, pickManual = {}, pickAll = false, hinnad = null, hinnadSize = null, selManual = false;
    /* avatud = klassi rida, mille rehvide nimekiri on lahti (vaikimisi kinni) */
    var avatud = null;
    function rowsFor(S, eprelRows, season) {
      var veh = core.vehByKey[S.veh] || core.vehByKey[DEFAULT_VEH];
      var cond = condObj(S.cond, S.speed), ck = S.cond, rows = [];
      var sea = SEASON[season];
      /* testitud rehvid */
      var eprelByTest = {};
      eprelRows.forEach(function (r) { if (r.tested) eprelByTest[r.tested] = r; });
      var collapsed = {};
      var hiddenOther = 0;
      var M = minuLeia(S.minu, eprelRows), minuT = M && M.t ? M.t.key : null, mm = S.muster || null;
      if (M && !M.puudu) {
        var mt = M.t, measuredM = mt && (ck === 'wet' || (ck === 'dry' ? mt.muDry != null : ck === 'snow' ? mt.muSnow != null : mt.muIce != null));
        var baseM = measuredM ? onCar(mt, S.size) : (M.r ? eprelTyre(M.r) : Object.assign({}, mt, { muDry: null, muSnow: null, muIce: null }));
        var rm = calc(kulunud(baseM, mm), veh, cond);
        rows.push({ id: 'o', kind: 'own', spec: S.minu && S.minu.e ? 'o:e:' + S.minu.e : 'o:t:' + minuT, name: M.nimi, d: rm.distanceM, r: rm, own: true, ty: kulunud(mt ? onCar(mt, S.size) : baseM, mm), hooaeg: M.hooaeg, mm: mm,
          dUus: mm ? calc(baseM, veh, cond).distanceM : null,
          pids: M.r ? [M.r.slug + '@' + S.size] : [], label: M.r ? M.r.g : null, t: measuredM ? mt : null,
          est: !measuredM && ck !== 'wet',
          sub: _t('Sinu rehv · ') + M.silt + (mm ? _t(' · muster ') + mmT(mm) + _t(' mm') : '') + (measuredM ? _t(' · haare sõltumatust testist') : ck === 'wet' && M.r ? _t(' · märgise klass ') + M.r.g : _t(' · rehvitüübi keskmine (märgis ei ütle ') + COND[ck].gen + _t(' kohta midagi)')) });
      }
      /* oma rehvi pole valitud, aga muster on antud: tüüpiline sama hooaja
         rehv selle mustriga, et näha, kui palju uued rehvid varem peatuvad */
      if (mm && !(M && !M.puudu)) {
        var gcat = { summer: 'SUMMER_TOURING', all: 'ALL_SEASON', winter: 'WINTER_NORDIC', naast: 'WINTER_STUDDED' }[season] || 'SUMMER_TOURING';
        /* tüüpiline = sinu mõõdu selle hooaja märgiste mediaanklass (märjal) */
        var gg = inSeasonG(eprelRows, sea), gt = classTyre(gg, gcat, S.size), gr = calc(kulunud(gt, mm), veh, cond);
        rows.push({ id: 'o', kind: 'own', gen: true, spec: 'g:' + gcat + gg, name: _t('Sinu rehvid praegu'), d: gr.distanceM, r: gr, own: true, mm: mm, ty: kulunud(gt, mm),
          hooaeg: season, dUus: calc(gt, veh, cond).distanceM, pids: [], label: null, t: null, est: true,
          sub: _t('Tüüpiline: ') + tyypSilt(gcat) + (ck === 'wet' ? ', ' + _t('märgise klass ') + gg : '') + _t(', muster ') + mmT(mm) + _t(' mm') + '. ' + _t('Täpsemaks vali oma rehv.') });
      }
      core.tyres.forEach(function (t) {
        if (t.key === minuT) return;
        if (sea.tested.indexOf(t.category) < 0) return;
        /* Testitud rehv on SINU autole asjakohane ainult siis, kui seda mudelit
           müüakse sinu mõõdus (EPREL-is on rida) või test oligi selles mõõdus.
           18-tolline sportrehv 15-tollise auto tulemuste seas oleks eksitav. */
        /* naastrehvidel EL-i märgist (ja seega mõõdu andmeid) ei ole — näitame testituid alati */
        var avail = !!eprelByTest[t.key] || norm(t.size) === S.size || t.category === 'WINTER_STUDDED';
        if (!avail && !S.showOther) { hiddenOther++; return; }
        var measured = ck === 'wet' ? true : ck === 'dry' ? t.muDry != null : ck === 'snow' ? t.muSnow != null : t.muIce != null;
        if (!measured) { collapsed[t.category] = t; return; }
        var r = calc(onCar(t, S.size), veh, cond);
        var srcs = uniqSrc(t.tests), er = eprelByTest[t.key];
        rows.push({ id: 't:' + t.key, kind: 'test', name: t.name, d: r.distanceM, r: r, t: t, ty: onCar(t, S.size), pids: er ? [er.slug + '@' + S.size] : (t.slug ? [t.slug + '@' + S.size] : []),
          sub: _t('Sõltumatu test') + (srcs.length ? ' · ' + srcs.map(srcName).join(', ') : ''),
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
          rows.push({ id: 'c:' + k, kind: 'class', g: g, cat: cat, n: list.length, d: r.distanceM, r: r, members: list, ty: classTyre(g, cat, S.size),
            pids: list.map(function (x) { return x.slug + '@' + S.size; }),
            name: _t('Märgise klass ') + g + (sea.eprel.length > 1 ? ' · ' + (cat === 'WINTER_NORDIC' ? _t('Põhjamaade lamell') : cat === 'ALL_SEASON' ? _t('aastaringne') : _t('Kesk-Euroopa lamell')) : ''),
            sub: list.length + _t(' rehvimudelit sinu mõõdus, nt ') + list.slice(0, 2).map(function (x) { return x.mark + ' ' + x.name; }).join(', ') });
        });
      } else {
        /* märgis ei ütle kuiva/lume/jää kohta midagi: üks kategooria keskmise rida */
        var cats = {};
        inSeason.forEach(function (r) { cats[r.cat] = (cats[r.cat] || 0) + 1; });
        Object.keys(collapsed).forEach(function (c) { if (!cats[c]) cats[c] = 0; });
        Object.keys(cats).forEach(function (c) {
          var r = calc(classTyre('C', c, S.size), veh, cond);
          rows.push({ id: 'k:' + c, kind: 'cat', cat: c, n: cats[c], d: r.distanceM, r: r, pids: [], ty: classTyre('C', c, S.size),
            name: CATNAME[c] + _t(' — kategooria keskmine'),
            sub: (cats[c] ? cats[c] + _t(' märgisega rehvimudelit sinu mõõdus · ') : '') + _t('märgis ei ütle ') + COND[ck].gen + _t(' kohta midagi') });
        });
      }
      rows.sort(function (a, b) { return a.d - b.d; });
      return { rows: rows, veh: veh, cond: cond, vehDefault: !core.vehByKey[S.veh], nSeason: inSeason.length, hiddenOther: hiddenOther, minu: M };
    }
    function inSeasonG(eprelRows, sea) {
      var g = eprelRows.filter(function (r) { return sea.eprel.indexOf(r.catNr) >= 0 && GNOM[r.g]; }).map(function (r) { return r.g; }).sort();
      return g.length ? g[Math.floor(g.length / 2)] : 'C';
    }
    function kulunud(t, mm) {
      if (!mm) return t;
      var uus = t.treadDepthNewMm || 8;
      return Object.assign({}, t, { treadDepthNewMm: uus, treadDepthMm: Math.min(mm, uus) });
    }
    function uniqSrc(tests) { var s = []; (tests || []).forEach(function (x) { if (s.indexOf(x.src) < 0) s.push(x.src); }); return s; }
    function srcName(c) { var s = core.sources[c]; return s ? s.tegija.replace(/ \(.*\)/, '') + ' ' + s.aasta : c; }
    function defaultSel(rows) {
      if (rows.some(function (r) { return r.kind === 'own' && !r.gen; })) return 'o';
      /* soovitame parimat: lühima pidurdusmaaga klass, mille rehvi saab poest osta;
         kui hindu pole, siis lihtsalt parim klass */
      var cls = rows.filter(function (r) { return r.kind === 'class'; }).sort(function (a, b) { return a.d - b.d; });
      if (cls.length) {
        var h = hinnad || {}, size = state && state.size;
        var osta = cls.filter(function (c) { return c.members.some(function (m) { var r = h[m.slug + '@' + size]; return !eriLiik(m) && r && r.length; }); })[0];
        return (osta || cls[0]).id;
      }
      var cat = rows.filter(function (r) { return r.kind === 'cat'; });
      if (cat.length) return cat[0].id;
      return rows.length ? rows[Math.floor(rows.length / 2)].id : null;
    }
    function show(S, eprelRows) {
      el = $('[data-result]');
      if (!el) return;
      /* hooaeg järgib teeolusid (lumi/jää -> talv), kuni kasutaja pole ise valinud */
      if (!S._userSeason) S.resSeason = (S.cond === 'snow' || S.cond === 'ice') ? 'winter' : 'summer';
      /* sinu rehv määrab hooaja: võrdluses on sama hooaja rehvid */
      var M0 = minuLeia(S.minu, eprelRows);
      if (M0 && !M0.puudu && !S._userSeason) S.resSeason = M0.hooaeg;
      state = S; state._eprel = eprelRows;
      eelKuular(); eelSulge();
      sel = null; showAll = false; selManual = false;
      pick = {}; pickManual = {}; pickAll = false; avatud = null;
      if (hinnadSize !== S.size) { hinnad = null; hinnadSize = null; }
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
    /* Sinu auto tehasemõõdud poodides: kõik hinnaga rehvid valitud hooajas,
       odavaim ees, igal kaardil kohe mõõt. Täidab tulemuse keskmise veeru
       tühja osa; kui hindu pole, jääb plokk peidetuks. */
    /* ---- EELVAADE: rehvi pildile vajutades paremas veerus selle rehvi
       pidurdusmaa sinu autoga (sama mudel ja tingimused) + vahemik graafikul
       võrrelduna praeguse tulemusega. „Vali“ viib poodi. */
    var eelCtx = null, eelAktiivne = null, jagaInfo = null;
    function eelvaade(d) {
      var box = $('[data-r-eel]', el);
      if (!box || !eelCtx) return;
      eelAktiivne = d;
      var x = d.id.split('@'), slug = x[0], m = x[1];
      loadSize(m).then(function (rows) {
        if (eelAktiivne !== d) return;
        var e = rows.filter(function (y) { return y.slug === slug; })[0];
        if (!core._tyreBySlug) { core._tyreBySlug = {}; core.tyres.forEach(function (t) { if (t.slug) core._tyreBySlug[t.slug] = t; }); }
        var t = (e && e.tested && core.tyreByKey[e.tested]) || core._tyreBySlug[slug] || null;
        var tyre = t ? onCar(t, m) : e ? eprelTyre(e) : null;
        var res = tyre ? calc(tyre, eelCtx.veh, eelCtx.cond) : null;
        var R = eelCtx.react;
        var g = e && e.g;
        var html = '<button type="button" class="eel-x" data-eel-x aria-label="' + esc(_t('Sulge')) + '">×</button>' +
          '<div class="eel-top"><span class="eel-pilt">' + (d.pilt ? '<img src="' + CFG.home + 'api/pilt/' + encodeURIComponent(slug) + '/" alt="" width="110" height="130">' : '<span class="pk-ring" aria-hidden="true"></span>') + '</span>' +
          '<span class="eel-n"><small>' + esc(pretty(m)) + (m === state.size ? ' · ' + _t('sinu mõõt') : '') + '</small><b>' + esc(d.n) + '</b>' + (g ? '<span>' + grade(g) + ' ' + _t('märghaare') + '</span>' : '') + '</span></div>';
        if (res) {
          var dd = res.distanceM + R, lo = res.lowM + R, hi = res.highM + R;
          /* võrdlus: sinu praegused rehvid (kui on antud), muidu praegune tulemus */
          var O = eelCtx.oma, CO = eelCtx.curOma;
          var ref = O ? O : { d: eelCtx.d, lo: eelCtx.lo, hi: eelCtx.hi, oma: !!CO };
          var omaRef = !!(O || CO);
          var mn = Math.min(lo, ref.lo), mx = Math.max(hi, ref.hi), pad = (mx - mn) * 0.12 || 2;
          mn -= pad; mx += pad;
          var pos = function (v) { return (100 * (v - mn) / (mx - mn)).toFixed(1) + '%'; };
          var vahe = dd - ref.d;
          var rida = function (nimi, a, b, x, on) {
            return '<div class="eg-r' + (on ? ' on' : '') + '"><span class="eg-l">' + nimi + '</span><span class="eg-t"><i style="left:' + pos(a) + ';right:calc(100% - ' + pos(b) + ')"></i><b style="left:' + pos(x) + '"></b></span></div>';
          };
          html += '<p class="eel-k">' + (eelCtx.stop ? _t('Peatumisteekond') : _t('Pidurdusteekond')) + ' ' + _t('sinu autoga') + '</p>' +
            '<p class="eel-num">' + fmt(dd) + ' <small>m</small></p>' +
            '<div class="eel-g" role="img" aria-label="' + esc(_t('Vahemik') + ' ' + fmt(lo) + '–' + fmt(hi) + ' m') + '">' +
              rida(_t('See rehv'), lo, hi, dd, true) +
              rida(omaRef ? _t('Sinu praegused') : _t('Praegune tulemus'), ref.lo, ref.hi, ref.d, false) +
              '<div class="eg-ax"><span>' + fmt(mn + pad) + ' m</span><span>' + fmt(mx - pad) + ' m</span></div>' +
            '</div>' +
            '<p class="eel-v ' + (vahe < -0.05 ? 'hea' : vahe > 0.05 ? 'halb' : '') + '">' +
              (omaRef
                ? (Math.abs(vahe) < 0.05 ? _t('Sama kui sinu praegused') : _t('Sinu praegustest: ') + (vahe < 0 ? fmt(-vahe) + _t(' m lühem') : fmt(vahe) + _t(' m pikem')))
                : (Math.abs(vahe) < 0.05 ? _t('Sama kui praegune tulemus') : (vahe < 0 ? fmt(-vahe) + _t(' m lühem') : fmt(vahe) + _t(' m pikem')) + _t(' kui praegune tulemus'))) + '</p>' +
            '<p class="eel-s">' + _t('Tõenäoline vahemik') + ' ' + fmt(lo) + '–' + fmt(hi) + ' m</p>';
        } else html += '<p class="eel-s">' + _t('Selle rehvi kohta pole pidurdusandmeid.') + '</p>';
        box.innerHTML = html; box.hidden = false;
        el.classList.add('eel-on');
      });
    }
    function eelSulge() { eelAktiivne = null; var box = $('[data-r-eel]', el); if (box) { box.hidden = true; box.innerHTML = ''; } if (el) el.classList.remove('eel-on'); }
    function eelKuular() {
      if (!el || el._eel) return;
      el._eel = true;
      el.addEventListener('click', function (e) {
        var x = e.target.closest && e.target.closest('[data-eel-x]');
        if (x) { eelSulge(); return; }
        var b = e.target.closest && e.target.closest('[data-eel]');
        if (!b) return;
        e.preventDefault();
        var d = { id: b.dataset.eel, n: b.dataset.n || '', url: b.dataset.url || '', hind: b.dataset.hind || '', pood: b.dataset.pood || '', pilt: b.dataset.pilt === '1' };
        Track('eelvaade', d.n + ' · ' + d.id.split('@')[1]);
        eelvaade(d);
        var box = $('[data-r-eel]', el);
        if (box && matchMedia('(max-width:900px)').matches) setTimeout(function () { box.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }, 80);
      });
    }
    var poodVoti = null;
    function poodiMoodud(S) {
      var box = $('[data-r-pood]', el);
      if (!box || !CFG.prices) return;
      var veh = core.vehByKey[S.veh];
      /* Valitud mõõt on alati esimene. Auto teised tehasemõõdud tulevad juurde
         ainult siis, kui valitud mõõt on ise tehasemõõt — kui inimene pani oma
         mõõdu (nt 245/40 R18), näitame ainult seda. */
      var moodud = [S.size], fab = [];
      ((veh && veh.oemSizes) || []).forEach(function (z) {
        var x = /^(\d{3})\/(\d{2})\s*R(\d{2})(C?)$/.exec(String(z).trim());
        var m = x ? x[1] + x[2] + 'R' + x[3] + x[4] : null;
        if (m) fab.push(m);
      });
      if (!veh || fab.indexOf(S.size) >= 0) fab.forEach(function (m) {
        if (moodud.indexOf(m) < 0 && core.eprelSizes.indexOf(m) >= 0) moodud.push(m);
      });
      moodud = moodud.slice(0, 8);
      var sea = SEASON[S.resSeason] || SEASON.summer, voti = moodud.join(',') + '|' + S.resSeason;
      if (voti === poodVoti) return;
      poodVoti = voti;
      if (!core._tyreBySlug) { core._tyreBySlug = {}; core.tyres.forEach(function (t) { if (t.slug) core._tyreBySlug[t.slug] = t; }); }
      Promise.all(moodud.map(function (m) { return Promise.all([Prices.size(m), loadSize(m)]).then(function (x) { return { m: m, h: (x[0] && x[0].hinnad) || {}, rows: x[1] }; }); }))
        .then(function (koik) {
          if (poodVoti !== voti) return;
          var list = [];
          koik.forEach(function (k) {
            var bySlug = {};
            k.rows.forEach(function (r) { bySlug[r.slug] = r; });
            Object.keys(k.h).forEach(function (id) {
              var slug = id.split('@')[0], rr = k.h[id];
              if (!rr || !rr.length || id.split('@')[1] !== k.m) return;
              var e = bySlug[slug], t = core._tyreBySlug[slug], nimi, g = null;
              if (e) { if (sea.eprel.indexOf(e.catNr) < 0) return; nimi = e.mark + ' ' + e.name; g = e.g; }
              else if (t) { if (sea.tested.indexOf(t.category) < 0) return; nimi = t.name; }
              else return;
              var r = rr.slice().sort(function (a, b) { return a.hind - b.hind; })[0];
              list.push({ m: k.m, slug: slug, nimi: nimi, g: g, testitud: !!(t || (e && e.tested)), r: r });
            });
          });
          /* sinu mõõt ees (soodsaim ees), teised tehasemõõdud järel */
          list.sort(function (a, b) { return ((a.m !== S.size) - (b.m !== S.size)) || (a.r.hind - b.r.hind); });
          var ainultOma = !list.some(function (x) { return x.m !== S.size; });
          if (!list.length) { box.hidden = true; box.innerHTML = ''; return; }
          list = list.slice(0, 30);
          box.innerHTML = '<p class="rs-k">' + (ainultOma ? _t('Rehvid poodides mõõdus ') + esc(pretty(S.size)) : _t('Rehvid poodides — sinu mõõt ees')) + ' <span style="font-weight:500;color:var(--muted)">' + _t('(soodsaim ees · ') + sea.long + ')</span></p>' +
            '<div class="pk-rida pk-moot">' + list.map(function (x) {
              var r = x.r;
              var ladu = r.laos === false ? _t('tellimisel') : (r.kogus > 0 ? _t('laos') + ' ' + (r.kogus >= 8 ? '8+' : r.kogus) + ' ' + _t('tk') : '');
              var pilt = r.pilt ? '<img src="' + CFG.home + 'api/pilt/' + encodeURIComponent(x.slug) + '/" alt="" width="72" height="86" loading="lazy" decoding="async">' : '<span class="pk-ring" aria-hidden="true"></span>';
              var ylal = '<span class="pk-m">' + esc(pretty(x.m)) + (x.m === S.size ? ' <i>' + _t('sinu') + '</i>' : '') + '</span>' +
                '<span class="pk-pilt">' + pilt + '</span><span class="pk-n">' + esc(x.nimi) + '</span>' +
                (x.g ? '<small>' + _t('märghaare ') + esc(x.g) + (x.testitud ? _t(' · testitud') : '') + '</small>' : x.testitud ? '<small>' + _t('testitud') + '</small>' : '');
              return '<div class="pk">' + eelNupp(x.slug, x.m, x.nimi, r, ylal) +
                '<b>' + hindTekst(r) + '</b><span class="pk-pood">' + esc(r.myyja) + '</span>' + (ladu ? '<small>' + ladu + '</small>' : '') + valiLink(r, x.nimi + ' ' + pretty(x.m)) + '</div>';
            }).join('') + '</div>' +
            (!ainultOma ? '<p class="note" style="margin:0">' + _t('Mõõdud on selle auto tehase lubatud mõõdud. Teise mõõdu puhul kontrolli, et velg sobib.') + '</p>' : '');
          box.hidden = false;
        });
    }
    function paintPrices(size, cur) {
      var box = $('[data-r-price]', el);
      Prices.size(size).then(function (d) {
        if (state.size !== size) return;
        var h = (d && d.hinnad) || {}, avail = !!(d && d.available);
        /* hinnad saabusid: soovitus võib muutuda soodsaimaks — joonista üks kord uuesti */
        if (avail && hinnadSize !== size) {
          hinnad = h; hinnadSize = size;
          /* hinnad saabusid: soovitus = parim klass, mida saab osta; nimed klassiridadel */
          if (!selManual) sel = null;
          if (cur.kind === 'class' && !pickManual[cur.id]) delete pick[cur.id];
          render(); return;
        }
        $$('[data-rp]').forEach(function (e) {
          var x = rowsAll.filter(function (r) { return r.id === e.dataset.rp; })[0], c = x && cheapest(x.pids || [], h);
          e.textContent = c ? (x.kind === 'class' ? 'al ' : '') + Math.round(c.hind) + ' €' : '';
          e.title = c ? (x.kind === 'class' ? _t('Soodsaim selle klassi rehv: ') : _t('Soodsaim hind: ')) + eur(c.hind) : '';
        });
        var mb = $('[data-r-mbars]', el);
        if (mb) mb.classList.toggle('has-prices', !!$('.mbar .p:not(:empty)', mb));
        if (!box) return;
        if (!avail) { box.innerHTML = _t('<span class="pl">Hinnad müüjatelt</span> <span class="none">pole hetkel saadaval</span> ') + tip(PRICE_T); return; }
        if (cur.kind === 'own' && cur.gen) {
          box.innerHTML = '<span class="pl">' + esc(cur.name) + '</span> <span class="none">' + _t('vali uus rehv, et näha hindu') + '</span>';
        } else if (cur.kind === 'test' || cur.kind === 'own') {
          var id = (cur.pids || [])[0];
          box.innerHTML = '<span class="pl">' + esc(cur.name) + _t(' — hinnad</span>') + (id ? poedRead(h[id], id, cur.name) : _t('<span class="none">Seda rehvi sinu mõõdus müüjatelt ei leitud</span>'));
        } else if (cur.kind === 'class' && valitud(cur)) {
          var vm = valitud(cur), vid = vm.slug + '@' + size;
          box.innerHTML = '<span class="pl">' + esc(vm.mark + ' ' + vm.name) + _t(' — hinnad</span> ') + poedRead(h[vid], vid, vm.mark + ' ' + vm.name);
        } else if (cur.kind === 'class') {
          /* klassi rehvid poodides: pilt + nimi + hind, odavaim ees, keritav nimekiri */
          var top = cur.members.filter(function (m) { return !eriLiik(m); }).map(function (m) { var id = m.slug + '@' + size; return h[id] && h[id].length ? { m: m, r: h[id].slice().sort(function (a, b) { return a.hind - b.hind; })[0] } : null; })
            .filter(Boolean).sort(function (a, b) { return a.r.hind - b.r.hind; });
          box.innerHTML = _t('<span class="pl">Soodsaimad klassi ') + cur.g + _t(' rehvid</span> ') + (top.length ? '<div class="pk-list">' + top.map(function (t) {
            var nimi = t.m.mark + ' ' + t.m.name;
            var ladu = t.r.laos === false ? _t('tellimisel') : (t.r.kogus > 0 ? _t('laos') + ' ' + (t.r.kogus >= 8 ? '8+' : t.r.kogus) + ' ' + _t('tk') : '');
            var pilt = t.r.pilt ? '<img src="' + CFG.home + 'api/pilt/' + encodeURIComponent(t.m.slug) + '/" alt="" width="48" height="58" loading="lazy" decoding="async">' : '<span class="pk-ring" aria-hidden="true"></span>';
            return '<div class="pk-r">' + eelNupp(t.m.slug, size, nimi, t.r, '<span class="pk-pilt">' + pilt + '</span>') +
              '<span class="pk-nimi">' + eelNupp(t.m.slug, size, nimi, t.r, '<b>' + esc(nimi) + '</b>') + '<small>' + esc(t.r.myyja) + (ladu ? ' · ' + ladu : '') + '</small>' +
              '<span class="pk-rv"><b class="pk-hind">' + hindTekst(t.r) + '</b>' + valiLink(t.r, nimi) + '</span></span></div>';
          }).join('') + '</div>' : _t('<span class="none">Hindu selles klassis veel pole</span>'));
        } else box.innerHTML = _t('<span class="pl">Hinnad</span> <span class="none">vali rehv, et näha müüjaid</span>');
      });
    }
    /* klassi rehvid: üks rida mudeli kohta; järjestus = mida soovitame */
    function liikmed(cur) {
      var seen = {}, h = hinnad || {}, size = state.size;
      var list = cur.members.filter(function (m) { return seen[m.slug] ? false : (seen[m.slug] = 1); });
      var hind = function (m) { var r = h[m.slug + '@' + size]; return r && r.length ? r[0].hind : null; };
      var F = 'ABCDE';
      list.sort(function (a, b) {
        var ea = !!eriLiik(a), eb = !!eriLiik(b);
        if (ea !== eb) return ea ? 1 : -1;
        var pa = hind(a), pb = hind(b);
        if ((pa != null) !== (pb != null)) return pa != null ? -1 : 1;
        if (pa != null && pb != null && pa !== pb) return pa - pb;
        if (!!a.tested !== !!b.tested) return a.tested ? -1 : 1;
        var da = a.db || 99, db = b.db || 99;
        if (da !== db) return da - db;
        var fa = F.indexOf(a.f), fb = F.indexOf(b.f);
        if (fa !== fb) return (fa < 0 ? 9 : fa) - (fb < 0 ? 9 : fb);
        return (a.mark + a.name).localeCompare(b.mark + b.name, 'et');
      });
      return { list: list, hind: hind };
    }
    function valitud(cur) {
      if (!cur || cur.kind !== 'class') return null;
      /* kinnisel klassil konkreetset rehvi ei näidata — ainult klass */
      if (avatud !== cur.id && !pickManual[cur.id]) return null;
      var L = liikmed(cur).list;
      var slug = pick[cur.id];
      var m = L.filter(function (x) { return x.slug === slug; })[0];
      if (!m) { m = L[0]; if (m) pick[cur.id] = m.slug; }
      return m || null;
    }
    function testRida(cur) {
      var vm = valitud(cur);
      return vm && vm.tested ? rowsAll.filter(function (x) { return x.id === 't:' + vm.tested; })[0] || null : null;
    }
    function pickPanel(cur) {
      var o = liikmed(cur), L = o.list, m0 = valitud(cur), LIM = 4;
      var shown = pickAll ? L : L.slice(0, LIM);
      if (m0 && shown.indexOf(m0) < 0) shown = shown.slice(0, LIM - 1).concat([m0]);
      var miks = o.hind(L[0]) != null ? _t('soodsaim') : L[0].tested ? _t('testitud') : _t('vaikseim');
      return _t('<li class="mpick"><p class="mp-h">Klassi ') + esc(cur.g) + _t(' rehvid sinu mõõdus <small>— märjal pidurdavad ühtviisi, vahe on müras, kütusekulus ja hinnas</small></p>') +
        _t('<ul class="mp-list') + (pickAll ? ' all' : '') + '">' + shown.map(function (m) {
          var on = m0 && m.slug === m0.slug, p = o.hind(m);
          var tr = m.tested ? rowsAll.filter(function (x) { return x.id === 't:' + m.tested; })[0] : null;
          var meta = [eriLiik(m).toLowerCase(), onRft(m) ? 'run-flat' : '', m.db ? m.db + ' dB' : '', m.f ? _t('kütus ') + m.f : '', tr ? _t('testis ') + fmt(tr.d) + _t(' m') : m.tested ? _t('testitud') : ''].filter(Boolean).join(' · ');
          return _t('<li><button type="button" class="mp" data-pick="') + esc(m.slug) + _t('" aria-pressed="') + !!on + '">' +
            '<span class="mp-n">' + esc(m.mark + ' ' + m.name) + (m === L[0] ? ' <em>' + miks + '</em>' : '') + '</span>' +
            '<span class="mp-m">' + esc(meta) + '</span>' +
            '<span class="mp-p">' + (p != null ? eur(p) : '') + '</span></button></li>';
        }).join('') + '</ul>' +
        (L.length > LIM ? '<button type="button" class="linkbtn mp-all" data-mp-all>' + (pickAll ? _t('Näita vähem') : _t('Näita kõiki ') + L.length) + '</button>' : '') +
        '</li>';
    }
    function row(x, best, max, compact) {
      var dd = x.d - best;
      if (compact) {
        var nm = x.kind === 'cat' ? (CATNAME[x.cat] + _t(', keskmine')) : x.name, nmHtml = null;
        if (x.kind === 'own') nmHtml = (x.gen ? '' : '<em class="own-p">' + _t('Sinu rehv') + ' · </em>') + esc(x.name) + (x.mm ? ' <small>' + mmT(x.mm) + _t(' mm') + '</small>' : '');
        if (x.kind === 'class') {
          /* klassi asemel konkreetne rehv: soodsaim / testitud / vaikseim selles klassis */
          var esi = liikmed(x).list[0];
          nmHtml = grade(x.g) + ' ' + (esi ? esc(esi.mark + ' ' + esi.name) : esc(_t('Klass ') + x.g)) +
            (x.n > 1 ? ' <small>' + _t('+ ') + (x.n - 1) + _t(' sama klassi') + '</small>' : '');
        }
        return _t('<li><button type="button" class="mbar') + (x.kind === 'class' ? ' mcls' : '') + (x.kind === 'own' ? ' own' : '') + _t('" data-row="') + esc(x.id) + _t('" aria-pressed="') + (x.id === sel) + '"' +
          (x.kind === 'class' ? ' aria-expanded="' + (x.id === avatud) + '"' : '') + ' title="' + esc(x.kind === 'class' ? _t('Täht = EL-i rehvimärgise märghaarde klass ') + x.g + _t('. Sama klassi rehvid pidurdavad märjal ühtviisi — vajuta, et näha kõiki ') + x.n : (x.sub || '')) + '">' +
          '<span class="n">' + (nmHtml || esc(nm)) + '</span>' +
          _t('<span class="t" aria-hidden="true"><span style="width:') + (100 * x.d / max).toFixed(1) + '%"></span></span>' +
          '<span class="v">' + fmt(x.d) + _t(' m</span>') +
          '<span class="d">' + (dd < 0.05 ? '' : '+' + fmt(dd) + _t(' m <i>') + pct(dd, best) + '</i>') + '</span>' +
          _t('<span class="p" data-rp="') + esc(x.id) + '"></span></button></li>';
      }
      var sub = '<small>' + esc(x.sub) + (x.kind === 'test' && x.sizeNote ? _t(' · mõõt ') + esc(x.sizeNote) : '') + '</small>';
      var badge = x.kind === 'class' ? grade(x.g) : (x.label ? grade(x.label) : '');
      return _t('<li><button type="button" class="bar" data-row="') + esc(x.id) + _t('" aria-pressed="') + (x.id === sel) + '">' +
        '<span class="bn">' + badge + '<span>' + esc(x.name) + (x.other ? _t(' <small style="color:#92400e">· pole sinu mõõdus</small>') : '') + '<br>' + sub + '</span></span>' +
        '<span class="bd">' + fmt(x.d) + _t(' m<small class="bp" data-rp="') + esc(x.id) + '"></small></span>' +
        _t('<span class="bx') + (dd < 0.05 ? ' zero' : '') + '">' + (dd < 0.05 ? _t('parim') : '+' + fmt(dd) + _t(' m<small>') + pct(dd, best) + '</small>') + '</span>' +
        _t('<span class="tr" aria-hidden="true"><span class="') + (x.kind === 'test' ? '' : 'band') + _t('" style="width:') + (100 * x.d / max).toFixed(1) + '%"></span></span>' +
        '</button></li>';
    }
    /* sinu rehv vs parim sama hooaja valik (+ suverehv lumel/jääl) */
    function minuVordlus(cur, rows, out, S, react) {
      if (out.minu && out.minu.puudu) return _t('<span class="own-cmp">Rehvi ') + esc(out.minu.nimi || '') + _t(' mõõdus ') + esc(pretty(S.size)) + _t(' ei ole — näitame tüüpilist rehvi.</span>');
      var oma = rows.filter(function (x) { return x.kind === 'own'; })[0];
      if (oma && oma.mm && /^(winter|naast)$/.test(oma.hooaeg) && oma.mm < 3) var talvMin = _t('<span class="own-cmp">Talverehvi mustri lubatud miinimum on 3 mm.</span>');
      if (!cur || cur.kind !== 'own') {
        if (!oma || !cur) return '';
        var vv = oma.d - cur.d;
        var kes = (oma.gen || oma.mm ? _t('Sinu praegustest') : _t('Sinu rehvist')) + (oma.mm ? ' (' + mmT(oma.mm) + _t(' mm') + ')' : '');
        return '<span class="own-cmp">' + (vv >= 0.5 ? kes + _t(' peatub <b>') + fmt(vv) + _t(' m varem</b>') : kes + ': ' + fmt(oma.d + react) + ' m') + '</span>' + (talvMin || '');
      }
      var muud = rows.filter(function (x) { return x.kind !== 'own'; });
      var h = '';
      if (muud.length) {
        var b = muud[0], vahe = cur.d - b.d;
        var bn = b.kind === 'class' ? b.g + _t('-klassi märgisega rehv') : b.kind === 'cat' ? CATNAME[b.cat].toLowerCase() + _t(' (keskmine)') : b.name;
        /* alla 5% vahe on mudeli veapiiri sees — ära soovita vahetust */
        h = vahe < 0.5 ? _t('<span class="own-cmp">Sinu rehv on selles võrdluses parim.</span>')
          : vahe / cur.d < 0.05 ? _t('<span class="own-cmp">Sinu rehv on parimate hulgas: vahe parimaga (') + esc(bn) + _t(') on ') + fmt(vahe) + _t(' m, see on veapiiri sees.</span>')
          : _t('<span class="own-cmp">Parim valik: <b>') + esc(bn) + _t('</b> — peatub <b>') + fmt(vahe) + _t(' m</b> varem.</span>');
      }
      if (cur.mm && cur.dUus != null && cur.d - cur.dUus >= 0.3) h += _t('<span class="own-cmp">Uue mustriga peatuks sama rehv <b>') + fmt(cur.d - cur.dUus) + _t(' m</b> varem.</span>');
      if (talvMin) h += talvMin;
      if (cur.hooaeg === 'summer' && (S.cond === 'snow' || S.cond === 'ice')) {
        var w = calc(classTyre('C', 'WINTER_NORDIC', S.size), out.veh, out.cond).distanceM;
        h += _t('<span class="own-cmp">Suverehv ') + (S.cond === 'snow' ? _t('lumel') : _t('jääl')) + _t(': Põhjamaade talverehviga oleks umbes <b>') + fmt(w + react) + _t(' m</b>.</span>');
      }
      return h;
    }
    /* KÕIK OLUD KORRAGA: sama rehv kuival, märjal, lumel ja jääl (FB tagasiside:
       „eraldi klikkida on tüütu“). Ainult näit: teeolude vahetus muudaks
       võrdlusrida (märgis kehtib ainult märjal), numbrid hüppaksid.
       ≈ = rehvil pole selle pinna kohta mõõtmist, number on rehvitüübi keskmine. */
    function ilmad(cur, vmT, out, S, react) {
      var box = $('[data-r-ilmad]', el);
      if (!box) return;
      var ty = (vmT && vmT.ty) || cur.ty;
      if (!ty) { box.hidden = true; return; }
      box.hidden = false;
      var hinn = false;
      box.innerHTML = '<div class="rs-ig">' + ['dry', 'wet', 'snow', 'ice'].map(function (k) {
        var d = k === S.cond ? null : calc(ty, out.veh, condObj(k, S.speed)).distanceM;
        if (d == null) d = (vmT ? vmT.r.distanceM : cur.r.distanceM);
        var mOk = k === 'wet' || (k === 'dry' ? ty.muDry != null : k === 'snow' ? ty.muSnow != null : ty.muIce != null);
        if (!mOk) hinn = true;
        return '<div data-ilm="' + k + '"' + (k === S.cond ? ' class="on" aria-current="true"' : '') + ' title="' + esc(COND[k].label) + (mOk ? '' : ' · ' + _t('hinnang rehvitüübi järgi')) + '">' +
          '<span>' + COND[k].short + '</span><b>' + (mOk ? '' : '≈') + (d + react >= 100 ? fmt(d + react, 0) : fmt(d + react)) + _t(' m') + '</b></div>';
      }).join('') + '</div>' + (hinn ? '<p class="rs-in">' + _t('≈ hinnang rehvitüübi järgi, mõõtmist pole') + '</p>' : '');
    }
    function render() {
      var S = state, out = rowsFor(S, S._eprel, S.resSeason);
      rowsAll = out.rows;
      if (!sel || !rowsAll.some(function (r) { return r.id === sel; })) sel = defaultSel(rowsAll);
      var cur = rowsAll.filter(function (r) { return r.id === sel; })[0];
      var ck = S.cond, c = COND[ck];
      var detail = $('[data-r-detail]');
      $('[data-r-range]', el).textContent = S.speed + _t(' km/h → 0 km/h');
      if (detail) {
        $('[data-r-range2]', detail).textContent = S.speed + _t(' → 0 km/h');
        $('[data-r-cond]', detail).textContent = c.label;
      }
      /* „Leidsid vea?“ → kontaktivorm, teema „Viga andmetes“, sõnum eeltäidetud
         sellega, mis on ekraanil (auto, mõõt, olud; isikuandmeid ei ole) */
      var vg = $('[data-r-viga]', el);
      if (vg) {
        var vAuto = core.vehByKey[S.veh];
        vg.href = LHOME + 'kontakt/?teema=viga&sonum=' + encodeURIComponent(
          _t('Auto: ') + (vAuto ? vAuto.name : _t('valimata')) + '\n' + _t('Rehvimõõt: ') + pretty(S.size) + '\n' +
          _t('Kiirus ja olud: ') + S.speed + ' km/h, ' + c.label + '\n\n' + _t('Mis on valesti: '));
      }
      var va = $('[data-r-valik]', el);
      if (va) va.href = LHOME + 'rehvi-valimine/?' + [S.veh ? 'auto=' + encodeURIComponent(S.veh) : '', 'moot=' + S.size, 'hooaeg=' + S.resSeason].filter(Boolean).join('&');

      if (!cur) {
        $('[data-r-big]', el).textContent = '—';
        $('[data-r-whoshort]', el).textContent = _t('Selle valiku kohta andmeid ei ole.');
        $('[data-r-mbars]', el).innerHTML = '';
        if (detail) { $('[data-r-bars]', detail).innerHTML = ''; $('[data-r-big2]', detail).textContent = '—'; }
        return;
      }
      var r = cur.r, rows = rowsAll, best = rows[0].d, max = rows[rows.length - 1].d;
      /* klassist valitud rehv on ise sõltumatult testitud → tema mõõdetud tulemus */
      var vmT = testRida(cur);
      if (vmT) r = vmT.r;
      /* PIDURDUSTEEKOND vs PEATUMISTEEKOND. Peatumisteekond = reageerimis-
         teekond (auto sõidab täiskiirusel, kuni juht jõuab pidurini) +
         pidurdusteekond. Rehv mõjutab ainult teist osa, seega ribad all
         jäävad pidurdusteekonnaks. */
      var rmode = store.get('rmode', 'brake'), rt = +store.get('rt', 1) || 1;
      var react = rmode === 'stop' ? S.speed / 3.6 * rt : 0;
      $$('[data-r-mode]', el).forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.rMode === rmode)); });
      $('[data-r-lbl]', el).textContent = rmode === 'stop'
        ? _t('Peatumisteekond · märkamisest kuni seisuni')
        : _t('Pidurdusteekond · pidur põhjas kuni seisuni');
      var spl = $('[data-r-split]', el);
      spl.hidden = rmode !== 'stop';
      $('[data-r-rt]', el).value = String(rt);
      $('[data-r-splittxt]', el).innerHTML = _t('Reageerimisteekond <b>') + fmt(react) + _t(' m</b> + pidurdusteekond <b>') + fmt(r.distanceM) + _t(' m</b>');
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
      var omaE = rows.filter(function (x) { return x.kind === 'own'; })[0];
      eelCtx = { veh: out.veh, cond: out.cond, react: react, d: r.distanceM + react, lo: r.lowM + react, hi: r.highM + react, stop: rmode === 'stop',
        curOma: cur.kind === 'own' ? cur : null,
        oma: omaE && omaE !== cur ? { d: omaE.d + react, lo: omaE.r.lowM + react, hi: omaE.r.highM + react, gen: omaE.gen, mm: omaE.mm } : null };
      if (eelAktiivne) eelvaade(eelAktiivne);
      var vm = valitud(cur);
      var whoShort = cur.kind === 'own' ? (cur.gen ? cur.name : cur.name + _t(' (sinu rehv)')) + (cur.mm ? _t(', muster ') + mmT(cur.mm) + _t(' mm') : '') : cur.kind === 'class' ? (vm ? vm.mark + ' ' + vm.name + (vmT ? _t(' (sõltumatu test)') : ' (' + cur.g + _t('-klassi märgis)')) : cur.g + _t('-klassi märgise rehviga')) : cur.kind === 'cat' ? CATNAME[cur.cat] + _t(' — keskmine') : cur.name;
      /* jagamiseks: mis on praegu ekraanil */
      var jReas = [cur].concat(rows.filter(function (x) { return x !== cur; }));
      var jParim = rows[0], jHalvim = rows[rows.length - 1], jOma = rows.filter(function (x) { return x.kind === 'own'; })[0];
      /* serveri jagamislehe (/jaga/) jaoks: rida, mille server arvutab uuesti */
      var jSpec = cur.kind === 'class' && vm ? 'e:' + vm.slug : cur.spec || cur.id;
      jagaInfo = {
        spec: jSpec, ab: absOn(S.veh) && out.veh && out.veh.absOpt ? 1 : 0, rt: rmode === 'stop' ? rt : 0,
        d: r.distanceM + react, stop: rmode === 'stop', speed: S.speed, cond: c.label, ck: ck,
        veh: out.vehDefault ? 'VW Golf 8' : out.veh.name, vehKey: out.vehDefault ? null : S.veh, size: S.size,
        tyre: whoShort, mm: S.muster || null,
        ribad: [[_t('Sinu tulemus'), r.distanceM + react, true]]
          .concat(jOma && jOma !== cur ? [[jOma.gen ? _t('Sinu praegused rehvid') : jOma.name, jOma.d + react, false]] : [])
          .concat(jParim && jParim !== cur ? [[_t('Parim selles mõõdus'), jParim.d + react, false]] : [])
          .concat(jHalvim && jHalvim !== cur && jHalvim !== jOma && jHalvim !== jParim ? [[_t('Halvim selles mõõdus'), jHalvim.d + react, false]] : [])
      };
      $('[data-r-whoshort]', el).innerHTML = esc(whoShort) + ' · ' + esc(c.label) + '<br>' +
        (out.vehDefault ? _t('auto valimata — arvutatud VW Golf 8 järgi') : esc(out.veh.name)) + _t(' · vahemik ') + fmt(r.lowM + react) + '–' + fmt(r.highM + react) + _t(' m') +
        minuVordlus(cur, rows, out, S, react);
      ilmad(cur, vmT, out, S, react);

      /* kompaktsed ribad: 5 rida, valitud alati sees */
      var LIMC = 5, omaR = rows.filter(function (x) { return x.kind === 'own'; })[0];
      var must = [cur].concat(omaR && omaR !== cur ? [omaR] : []);
      var comp = rows.filter(function (x) { return must.indexOf(x) < 0; }).slice(0, LIMC - must.length).concat(must)
        .sort(function (a, b) { return a.d - b.d; });
      $('[data-r-mbars]', el).innerHTML = comp.map(function (x) {
        return row(x, best, max, true) + (x === cur && x.id === avatud && x.kind === 'class' && x.members.length ? pickPanel(x) : '');
      }).join('');
      $$('[data-pick]', el).forEach(function (b) {
        b.addEventListener('click', function () {
          pick[cur.id] = b.dataset.pick; pickManual[cur.id] = true;
          Track('rehv_klassist', cur.g + ' · ' + b.textContent.trim().slice(0, 60));
          render();
        });
      });
      var mpa = $('[data-mp-all]', el);
      if (mpa) mpa.addEventListener('click', function () { pickAll = !pickAll; render(); });
      paintPrices(S.size, cur);
      poodiMoodud(S);

      if (detail) {
        $('[data-r-big2]', detail).textContent = fmt(r.distanceM + react);
        $('[data-r-cats]', detail).innerHTML = ['summer', 'winter', 'naast'].map(function (k) {
          return _t('<button type="button" data-rs="') + k + _t('" aria-pressed="') + (k === S.resSeason) + '">' + SEASON[k].label + '</button>';
        }).join('');
        $$('[data-rs]', detail).forEach(function (b) { b.addEventListener('click', function () { S.resSeason = b.dataset.rs; S._userSeason = true; sel = null; render(); }); });
        var rx = $('[data-r-react]', detail), react1 = S.speed / 3.6 * rt;
        if (rx) rx.innerHTML = rmode === 'stop'
          ? _t('Peatumisteekond = reageerimisteekond <b>') + fmt(react) + _t(' m</b> (') + String(rt).replace('.', DEC) + _t(' s, auto sõidab veel täiskiirusel) + pidurdusteekond <b>') + fmt(r.distanceM) + _t(' m</b>.')
          : _t('See on pidurdusteekond: arv algab hetkest, kui pidur on põhjas. Koos ') + String(rt).replace('.', DEC) + _t(' s reaktsiooniajaga oleks peatumisteekond <b>') + fmt(r.distanceM + react1) + _t(' m</b> (+') + fmt(react1) + _t(' m).');
        $('[data-r-band]', detail).innerHTML = _t('Tõenäoline vahemik <b>') + fmt(r.lowM + react) + '–' + fmt(r.highM + react) + _t(' m</b> (±') + Math.round(r.sigmaRel * 100) + '%)';
        var who = '<b>' + esc(cur.name) + '</b>';
        if (cur.kind === 'own') who += _t('<span class="src">Sinu rehv. ') + esc(cur.sub.indexOf(_t('Sinu rehv · ')) === 0 ? cur.sub.slice(_t('Sinu rehv · ').length) : cur.sub) + '.</span>';
        else if (cur.kind === 'test') who += _t('<span class="src">Haare tuleb sõltumatu testi mõõdetud tulemusest') + (cur.sizeNote ? _t(' (testi mõõt ') + esc(cur.sizeNote) + _t('; sinu mõõdus võib märgise klass erineda)') : '') + '.</span>';
        else if (cur.kind === 'class') {
          var gn = gmidN(cur.g, cur.cat);
          who += _t('<span class="src">Märgise klass ') + cur.g + ' · ' + cur.n + _t(' rehvimudelit sinu mõõdus. Haare on ') +
            (gn ? _t('selle klassi <b>') + gn + _t(' mõõdetud rehvi mediaan</b>') : _t('klassi nominaalne keskpunkt')) +
            _t('. Sama klassi rehvid on mudelis võrdsed; päris elus erinevad nad ±3–4%.</span>');
        }
        else who += _t('<span class="src">EL-i märgis ei ütle ') + esc(c.gen || c.label) + _t(' haarde kohta midagi, seetõttu on see kategooria keskmine.</span>');
        $('[data-r-who]', detail).innerHTML = who;
        var meta = _t('<span class="pill calc">Arvutatud hinnang</span>');
        meta += out.vehDefault ? _t('<span class="pill warn">Auto valimata: VW Golf 8</span>') : '<span class="pill">' + esc(out.veh.name) + '</span>';
        meta += '<span class="pill">' + esc(pretty(S.size)) + '</span>';
        if (cur.kind === 'own') meta += _t('<span class="pill">Sinu rehv</span>');
        if (cur.kind === 'test' || (cur.kind === 'own' && cur.t)) meta += _t('<span class="pill test">Sõltumatu test</span>');
        if (cur.kind === 'class') meta += _t('<span class="pill off">Ametlik märgis</span>');
        $('[data-r-meta]', detail).innerHTML = meta;
        var sea = SEASON[S.resSeason], LIM = 10, shown = showAll ? rows : rows.slice(0, LIM);
        if (!showAll && shown.indexOf(cur) < 0) shown = shown.slice(0, LIM - 1).concat([cur]);
        $('[data-r-sub]', detail).textContent = _t('Sama auto, sama kiirus ja teeolud — ainult rehv on erinev. ') + (ck === 'wet'
          ? _t('Testitud rehvid eraldi, märgisega rehvid klassi kaupa.')
          : _t('Eraldi ridadel ainult rehvid, mille ') + c.label + _t(' tulemus on päriselt mõõdetud.'));
        $('[data-r-bars]', detail).innerHTML = shown.map(function (x) { return row(x, best, max, false); }).join('');
        var more = $('[data-r-more]', detail);
        more.hidden = rows.length <= LIM;
        more.textContent = showAll ? _t('Näita vähem') : _t('Näita kõiki (') + rows.length + ')';
        more.onclick = function () { showAll = !showAll; render(); };
        var cmpA = $('[data-r-cmp]', detail);
        if (cmpA) cmpA.href = cmpUrl(null, { auto: S.veh, moot: S.size, hooaeg: S.resSeason });
        var notes = [];
        if (!S._eprel.length) notes.push(_t('Mõõdu ') + pretty(S.size) + _t(' märgiseandmeid pole veel andmebaasis — näidatakse ainult testitud rehve.'));
        if (!out.nSeason && S._eprel.length) notes.push(_t('Selles mõõdus ei ole andmebaasis ühtegi märgisega ') + sea.osa + '.');
        if (rows.some(function (x) { return x.sizeNote && !x.other; })) notes.push(_t('Testitud rehvid on mõõdetud testi mõõdus; märk nime ees on sama mudeli ametlik klass SINU mõõdus. Need võivad erineda — see on veapiiris sees.'));
        if (S.showOther) notes.push(_t('Näidatakse ka testitud rehve, mida sinu mõõdus andmebaasis ei ole — neid ei pruugi sinu autole saada.'));
        (r.warnings || []).slice(0, 2).forEach(function (w) { if (!/mõõdust .* tehasemõõt/.test(w)) notes.push(w); });
        $('[data-r-note]', detail).innerHTML = (notes.length ? '<div class="note-box">' + notes.map(esc).join('<br>') + '</div>' : '') +
          (out.hiddenOther || S.showOther ? '<button type="button" class="btn sm" style="margin-top:var(--sp-3)" data-r-other>' +
            (S.showOther ? _t('Näita ainult sinu mõõdus saadaolevaid') : _t('Näita ka ') + out.hiddenOther + _t(' testitud rehvi teistest mõõtudest')) + '</button>' : '');
        var ob = $('[data-r-other]', detail);
        if (ob) ob.onclick = function () { S.showOther = !S.showOther; render(); };
      }
      $$('[data-row]').forEach(function (b) {
        b.addEventListener('click', function () {
          var id = b.dataset.row, x = rowsAll.filter(function (r) { return r.id === id; })[0];
          /* klassi rida: valib ja avab/sulgeb rehvide nimekirja */
          if (x && x.kind === 'class') avatud = (avatud === id && sel === id) ? null : id;
          else avatud = null;
          sel = id; selManual = true; render();
        });
      });
      var tg = $('[data-r-toggle]');
      if (tg && !tg._bound) {
        tg._bound = true;
        tg.addEventListener('click', function () {
          var open = detail.hidden;
          detail.hidden = !open;
          tg.setAttribute('aria-expanded', open ? 'true' : 'false');
          tg.textContent = open ? _t('Peida üksikasjad') : _t('Kõik rehvid ja üksikasjad');
        });
      }
    }
    return { show: show, jagaInfo: function () { return jagaInfo; } };
  })();

  /* ------------------------------------------------------------ jagamine
     Tulemus pildina (1080×1920, sobib storysse ja postitusse) + link, mis
     avab sama arvutuse. Telefonis avaneb jagamismenüü (Instagram, Facebook,
     WhatsApp …), arvutis aken pildi allalaadimise ja linkidega. */
  var Jaga = (function () {
    /* jagatav link: serveri tulemuse leht (number arvutatakse seal uuesti, eelvaates on selle pilt) */
    function link(j) {
      if (j.spec && /^(t|c|k|e|o|g):/.test(j.spec)) {
        var p = [];
        if (j.vehKey) p.push('a=' + encodeURIComponent(j.vehKey));
        if (j.ab) p.push('ab=1');
        p.push('m=' + encodeURIComponent(j.size), 'v=' + j.speed, 'o=' + j.ck, 'r=' + encodeURIComponent(j.spec));
        if (j.mm && /^[og]:/.test(j.spec)) p.push('mm=' + j.mm);
        if (j.rt) p.push('rt=' + j.rt);
        return location.origin + LHOME + 'jaga/?' + p.join('&');
      }
      var q = [];
      if (j.vehKey) q.push('auto=' + encodeURIComponent(j.vehKey));
      q.push('moot=' + encodeURIComponent(j.size), 'kiirus=' + j.speed, 'olud=' + j.ck, 'arvuta=1');
      return location.origin + LHOME + '?' + q.join('&');
    }
    function tekst(j) {
      return _t('Minu auto peatub ') + fmt(j.d) + _t(' meetriga') + ' (' + j.speed + _t(' km/h, ') + j.cond + '). ' + _t('Kui kiiresti peatub sinu oma?');
    }
    function ring(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
    function pilt(j) {
      var W = 1080, H = 1920;
      var cv = document.createElement('canvas'); cv.width = W; cv.height = H;
      var g = cv.getContext('2d');
      var DISP = '"Barlow Condensed", "Arial Narrow", sans-serif', BODY = 'Inter, system-ui, sans-serif';
      g.fillStyle = '#0a0b0d'; g.fillRect(0, 0, W, H);
      /* tee all (dekoratsioon; storys katab alumise ääre vastamisriba) */
      var tee = g.createLinearGradient(0, 1560, 0, H); tee.addColorStop(0, 'rgba(36,39,45,0)'); tee.addColorStop(.3, '#1b1e24'); tee.addColorStop(1, '#14161a');
      g.fillStyle = tee; g.fillRect(140, 1560, 800, H - 1560);
      g.strokeStyle = 'rgba(255,255,255,.3)'; g.lineWidth = 6; g.setLineDash([46, 56]);
      g.beginPath(); g.moveTo(540, 1620); g.lineTo(540, H); g.stroke(); g.setLineDash([]);
      g.strokeStyle = 'rgba(229,72,77,.5)'; g.lineWidth = 14; g.lineCap = 'round';
      [400, 470].forEach(function (x) { g.beginPath(); g.moveTo(x, 1910); g.lineTo(x, 1830); g.stroke(); });
      g.fillStyle = '#ffc20e'; ring(g, 384, 1690, 102, 190, 30); g.fill();
      g.fillStyle = '#26303b'; ring(g, 400, 1720, 70, 40, 10); g.fill(); ring(g, 404, 1820, 62, 30, 10); g.fill();
      /* logo */
      g.textBaseline = 'alphabetic';
      g.font = 'italic 800 64px ' + BODY; g.fillStyle = '#fff'; g.fillText('PIDURDUSMAA', 90, 250);
      var lw = g.measureText('PIDURDUSMAA').width; g.fillStyle = '#ffc20e'; g.fillText('.ee', 90 + lw, 250);
      /* number */
      g.fillStyle = '#ffc20e'; g.font = '700 46px ' + BODY;
      g.fillText((j.stop ? _t('Peatumisteekond') : _t('Pidurdusteekond')).toUpperCase(), 90, 420);
      g.font = '700 330px ' + DISP; var num = fmt(j.d);
      g.fillText(num, 80, 710); var nw = g.measureText(num).width;
      g.fillStyle = '#fff'; g.font = '700 150px ' + DISP; g.fillText('m', 100 + nw, 710);
      g.fillStyle = '#c9ced6'; g.font = '500 44px ' + BODY;
      g.fillText(j.speed + ' → 0 km/h · ' + j.cond, 90, 790);
      /* sildid */
      var y = 850;
      [j.veh, pretty(j.size), j.tyre].filter(Boolean).forEach(function (sl) {
        g.font = '500 36px ' + BODY;
        var t = sl.length > 46 ? sl.slice(0, 45) + '…' : sl, w = g.measureText(t).width + 56;
        g.fillStyle = '#1a1d24'; ring(g, 90, y, Math.min(w, 900), 72, 18); g.fill();
        g.strokeStyle = '#2b3039'; g.lineWidth = 2; g.stroke();
        g.fillStyle = '#f3f4f6'; g.fillText(t, 118, y + 49); y += 90;
      });
      /* ribad */
      y += 50;
      var max = Math.max.apply(null, j.ribad.map(function (x) { return x[1]; }));
      j.ribad.slice(0, 3).forEach(function (rb) {
        g.font = (rb[2] ? '700 ' : '500 ') + '34px ' + BODY; g.fillStyle = rb[2] ? '#fff' : '#aab1bc';
        var nm = rb[0].length > 34 ? rb[0].slice(0, 33) + '…' : rb[0];
        g.fillText(nm, 90, y); g.textAlign = 'right'; g.fillText(fmt(rb[1]) + ' m', 990, y); g.textAlign = 'left';
        g.fillStyle = '#23262d'; ring(g, 90, y + 18, 900, 22, 11); g.fill();
        g.fillStyle = rb[2] ? '#ffc20e' : '#5d636d'; ring(g, 90, y + 18, Math.max(30, 900 * rb[1] / max), 22, 11); g.fill();
        y += 104;
      });
      /* üleskutse */
      y = Math.max(y + 10, 1430);
      g.fillStyle = '#16181d'; ring(g, 90, y, 900, 190, 28); g.fill();
      g.strokeStyle = '#2b3039'; g.lineWidth = 2; g.stroke();
      g.fillStyle = '#fff'; g.font = '700 50px ' + BODY; g.fillText(_t('Kui kiiresti peatub sinu auto?'), 130, y + 78);
      g.fillStyle = '#ffc20e'; g.font = '700 60px ' + DISP; g.fillText('pidurdusmaa.ee', 130, y + 152);
      return new Promise(function (ok) { cv.toBlob(function (b) { ok(b); }, 'image/png'); });
    }
    function aken(j, blob) {
      var d = $('[data-jaga]'); if (!d) return;
      var u = URL.createObjectURL(blob), l = link(j), tx = tekst(j);
      $('[data-jaga-img]', d).src = u;
      var dl = $('[data-jaga-dl]', d); dl.href = u; dl.download = 'pidurdusmaa-' + String(fmt(j.d)).replace(',', '-') + 'm.png';
      $('[data-jaga-fb]', d).href = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(l);
      $('[data-jaga-wa]', d).href = 'https://wa.me/?text=' + encodeURIComponent(tx + ' ' + l);
      var kp = $('[data-jaga-kopeeri]', d), juhis = $('[data-jaga-juhis]', d), st = $('[data-jaga-story]', d);
      /* ainult link: storys kleebisesse „Link“ ja mujale kleepimiseks puhas */
      function kopeeri() { try { navigator.clipboard.writeText(l); return true; } catch (e) { return false; } }
      kp.onclick = function () { if (kopeeri()) kp.textContent = _t('Link kopeeritud ✓'); Track('jaga', 'link'); };
      kp.textContent = _t('Kopeeri link');
      if (juhis) juhis.hidden = true;
      var fail = null;
      try { fail = new File([blob], 'pidurdusmaa.png', { type: 'image/png' }); } catch (e) {}
      /* STORY: link lõikelauale + pilt telefoni jagamismenüüsse (Instagram,
         Facebook, TikTok). Arvutis: pilt alla + link lõikelauale. */
      if (st) st.onclick = function () {
        var ok = kopeeri();
        if (fail && navigator.canShare && navigator.canShare({ files: [fail] })) {
          navigator.share({ files: [fail] }).then(function () { Track('jaga', 'story'); }).catch(function () {});
          if (juhis) { juhis.hidden = false; juhis.textContent = (ok ? _t('Link on kopeeritud. ') : '') + _t('Vali Instagram või Facebook → Story, lisa kleebis „Link“ ja kleebi.'); }
        } else {
          dl.click();
          Track('jaga', 'story-arvutis');
          if (juhis) { juhis.hidden = false; juhis.textContent = _t('Pilt laaditi alla') + (ok ? _t(' ja link on kopeeritud') : '') + _t('. Saada pilt telefoni, lisa storysse ja kleebi link kleebisega „Link“.'); }
        }
      };
      d.hidden = false;
      var x = $('[data-jaga-x]', d); if (x) x.focus();
    }
    function jaga() {
      var j = Result.jagaInfo(); if (!j) return;
      var fonte = document.fonts && document.fonts.load ? Promise.all([document.fonts.load('700 100px "Barlow Condensed"'), document.fonts.load('700 40px Inter'), document.fonts.load('italic 800 40px Inter')]).catch(function () {}) : Promise.resolve();
      fonte.then(function () { return pilt(j); }).then(function (blob) {
        /* ka telefonis oma aken: seal on „Jaga storysse“ (link kopeeritakse
           enne jagamismenüüd, et storys saaks lingikleebise panna) */
        aken(j, blob);
        Track('jaga', 'aken');
      });
    }
    document.addEventListener('click', function (e) {
      var t = e.target;
      if (t.closest && t.closest('[data-r-jaga]')) { e.preventDefault(); jaga(); return; }
      var d = $('[data-jaga]');
      if (d && !d.hidden && (t === d || (t.closest && t.closest('[data-jaga-x]')))) d.hidden = true;
    });
    document.addEventListener('keydown', function (e) { var d = $('[data-jaga]'); if (e.key === 'Escape' && d && !d.hidden) d.hidden = true; });
    return { jaga: jaga };
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
    { k: 'wet',   n: _t('Märgpidamine'),   d: _t('Kui hästi rehv märjal teel haarab.'), src: _t('Ametlik märgis'), ok: true },
    { k: 'wetb',  n: _t('Märgpidurdus'),   d: _t('Arvutatud pidurdusmaa märjal sinu autoga, ilma reaktsiooniajata. Tuleb märghaardest.'), src: _t('Arvutus'), ok: true },
    { k: 'dryb',  n: _t('Kuivpidurdus'),   d: _t('Arvutatud sinu autoga. Testitud rehvidel mõõdetud haardest, teistel tuletatud (≈).'), src: _t('Arvutus'), ok: true },
    { k: 'aqua',  n: _t('Vesiliug'),       d: _t('Pidurdusmaa uue rehviga, kui teel on sügav vesi (roopad, lombid), 90→0 sinu autoga. Testitud rehvidel mõõdetud ujumiskiirusest, teistel tuletatud (≈).'), src: _t('Arvutus'), ok: true },
    { k: 'noise', n: _t('Müra'),           d: _t('Rehvimärgise müra detsibellides.'), src: _t('Ametlik märgis'), ok: true },
    { k: 'rr',    n: _t('Veeretakistus'),  d: _t('Mõju kütuse- või energiakulule.'), src: _t('Ametlik märgis'), ok: true },
    { k: 'winter',n: _t('Talvised omadused'), d: _t('Pidurdusmaa lumel ja jääl 50→0 sinu autoga. Testitud rehvidel mõõdetud haardest, teistel rehvitüübi järgi (≈). Juures lume- ja jäämärk märgiselt.'), src: _t('Arvutus + test'), ok: true },
    { k: 'price', n: _t('Hind'),           d: _t('Soodsaim hind müüjatelt sinu mõõdus. Rehv, mille hinda pole, jääb selle koha pealt arvestamata.'), src: _t('Müüjad'), ok: true }
  ];
  /* RUN-FLAT: EPREL-is eraldi välja ei ole — tuvastame mudeli nimest
     (RFT, SSR, DriveGuard, ZP, MOE, ROF, HRS …). Pidurdusse see ei lähe. */
  var RFT_RE = /(^|[^a-z0-9])(rft|p-rft|run ?-?flat|runflat|ssr|zps?|rof|emt|dsst|hrs|xrp|driveguard|moe|r-f|rsc)([^a-z0-9]|$)/i;
  function onRft(r) { return RFT_RE.test(String(r.name || '')); }
  var RFT_T = _t('Run-flat (RFT): pärast torget saab edasi sõita, tavaliselt kuni 80 km, kiirusega kuni 80 km/h. Tuvastatud mudeli nimest (RFT, SSR, DriveGuard, ZP, MOE jt).');
  /* ERIREHVID: rajarehvid / poolslikid, maastiku (M/T) ja haagise rehvid.
     Igapäevaseks sõiduks need ei sobi — vaikimisi soovitustest väljas,
     linnukesega saab lisada. Tuvastame mudeli nimest. */
  var ERI = [
    [_t('Rajarehv'), /cup\s?2|p\s?zero\s?trofeo|pzero\s?trofeo|\btrofeo\b|r888|proxes\s?(r1r|rr)\b|(^|[^a-z0-9])(ar-?1|cr-?s|ns-?2r)([^a-z0-9]|$)|advan\s?a0(48|50|52)|\ba0(48|50|52)\b|re-?71\s?rs|re-?12d|potenza\s?race|direzza\s?03g|sport\s?maxx\s?race|ventus\s?(rs-?4|td)\b|\bz2(14|21|22|32)\b|ecsta\s?v7\d0|\bv7(00|20|30)\b|\bv70a\b|595\s?rs|fz-?201|rt-?615|rt-?660|supercar\s?3r|forcecontact|\b123s\b|651\s?sport|gredge|\b07rs\b|tempesta\s?p1|semi-?slick/i],
    [_t('Maastikurehv'), /\bmud\b|grappler|\bm\s?\/\s?t\b|\bmt(\s?[-\/]?\s?\d+|\/r)?\b|\bstt\b|\bbaja\b|deegan/i],
    [_t('Haagiserehv'), /trailer|\bkargo\b/i]
  ];
  function eriLiik(r) {
    var n = String(r.name || '');
    for (var i = 0; i < ERI.length; i++) if (ERI[i][1].test(n)) return ERI[i][0];
    return '';
  }
  var ERI_T = _t('Rajarehvid ja poolslikid, maastiku- (M/T) ja haagiserehvid. Igapäevaseks sõiduks need ei sobi, seepärast on nad vaikimisi peidetud. Tuvastatud mudeli nimest.');
  /* hind rehvi omaduseks: soodsaim müüja selles mõõdus (Prices.size vastusest) */
  function lisaHind(x, h) {
    var rr = h && h[x.r.slug + '@' + x.r.m], v = rr && rr.length ? rr[0].hind : null;
    x.P.price = v != null ? { v: v, show: eur(v), src: 'shop', score: -v, sub: rr[0].myyja } : null;
    return x;
  }
  var PROP = {}; PROPS.forEach(function (p) { PROP[p.k] = p; });
  var FG = { A: 5, B: 4, C: 3, D: 2, E: 1 };

  /* Ühe rehvi omadused sinu mõõdus. Iga väärtus kannab allikat. */
  /* Pidurdusmaad rehvi kohta (5 simulatsiooni). Ainult märgisega rehvidel
     sõltub tulemus ainult kategooriast, klassist ja mõõdust — sama klassi
     rehvid saavad sama arvu. Vahemälu: 400 rehvi → ~15 arvutust, mitte 2000
     (enne jooksis nimekiri telefonis mitu sekundit). */
  var simCache = {};
  function simul(t, r, veh) {
    var key = (t ? 't:' + t.key : 'e:' + r.cat + '|' + r.g) + '|' + r.m + '|' + (veh.key || veh.name);
    var c = simCache[key];
    if (c) return c;
    var base = t ? onCar(t, r.m) : eprelTyre(r), aq = base;
    if (t && t.aqua) {
      /* mõõdetud ujumiskiirus on TESTIMÕÕDUS -> tegur mudeli sama mõõdu vastu */
      var hpM = window.Pidurdus.hydroplaneSpeedKmh(t, veh, { surface: 'ASPHALT', waterMm: 7.8 });
      if (hpM) aq = Object.assign({}, base, { hpFactor: t.aqua.kmh / hpM });
    }
    c = {
      wb: calc(base, veh, condObj('wet', 90)).distanceM,
      db: calc(base, veh, condObj('dry', 90)).distanceM,
      dd: calc(aq, veh, Object.assign(condObj('wet', 90), { waterMm: 3 })).distanceM,
      aEst: aq === base,
      sb: calc(base, veh, condObj('snow', 50)).distanceM,
      ib: calc(base, veh, condObj('ice', 50)).distanceM
    };
    return (simCache[key] = c);
  }
  function tyreProps(r, veh) {
    var t = r.tested ? core.tyreByKey[r.tested] : null, P = {};
    P.wet = { v: r.g, show: grade(r.g), src: 'off', score: FG[r.g] };
    var sim = simul(t, r, veh);
    var wb = { distanceM: sim.wb };
    P.wetb = { v: wb.distanceM, show: fmt(wb.distanceM) + _t(' m'), src: 'calc', score: -wb.distanceM,
               sub: t ? _t('haare testist (mõõt ') + t.size + ')' : _t('klassi ') + r.g + (gmidN(r.g, r.cat) ? _t(' mõõdetud keskmine') : _t(' keskpunkt')) };
    var tw = t ? pick(t.tests, 'ASPHALT', true) : null, td = t ? pick(t.tests, 'ASPHALT', false) : null;
    /* Mõõdetud testitulemus on väike rida arvutuse all — kõik rehvid saavad
       sama protokolli järgi (90→0, sinu auto) arvutatud väärtuse. */
    if (tw) P.wetb.sub += _t(' · testis ') + fmt(tw.m) + _t(' m (') + srcLine(tw) + ')';
    var db = { distanceM: sim.db }, dEst = !(t && t.muDry != null);
    P.dryb = { v: db.distanceM, show: est(fmt(db.distanceM) + _t(' m'), dEst), src: dEst ? 'est' : 'calc', score: -db.distanceM,
               sub: dEst ? _t('rehvitüübi keskmine') : _t('haare testist') + (td ? _t(' · testis ') + fmt(td.m) + _t(' m (') + srcLine(td) + ')' : '') };
    /* VESILIUG = pidurdusmaa sügavas vees (3 mm, roopad/lombid), 90→0.
       Testitud rehvil nihutatakse mudeli ujumiskiirust mõõdetu järgi:
       ADAC-i protokollis (mudelis 7,8 mm vett) annab mudel 65 mõõdetud
       ujumiskiiruse vastu mediaanvea 0,7% ja keskmise vea 3,8%. */
    var dd = { distanceM: sim.dd }, aEst = sim.aEst;
    P.aqua = { v: dd.distanceM, show: est(fmt(dd.distanceM) + _t(' m'), aEst), src: aEst ? 'est' : 'calc', score: -dd.distanceM,
               sub: aEst ? _t('rehvitüübi ja laiuse järgi') : _t('testis hakkas ujuma ') + fmt(t.aqua.kmh) + _t(' km/h juures (') + ((core.sources[t.aqua.src] || {}).nimi || 'test') + ')' };
    P.noise = r.db ? { v: r.db, show: r.db + ' dB' + (r.nk ? ' (' + r.nk + ')' : ''), src: 'off', score: -r.db } : null;
    P.rr = r.f ? { v: r.f, show: grade(r.f), src: 'off', score: FG[r.f] } : null;
    var ws = [];
    if (r.flags & FLAG.SNOW) ws.push(_t('lumemärk'));
    if (r.flags & FLAG.ICE) ws.push(_t('jäämärk'));
    var ts = t ? pick(t.tests, 'SNOW_PACKED') : null, ti = t ? pick(t.tests, 'ICE') : null;
    /* TALV = arvutatud pidurdusmaa lumel + jääl 50→0 sinu autoga (sama mudel,
       mis kalkulaatoris). Testitud rehvil mõõdetud haardest, teistel rehvi
       tüübi (märgise kategooria) keskmisest — see on tuletatud (≈). */
    var sb = { distanceM: sim.sb }, ib = { distanceM: sim.ib };
    var wEst = !(t && t.muSnow != null && t.muIce != null);
    P.winter = { v: sb.distanceM + ib.distanceM,
                 show: est(_t('lumi ') + fmt(sb.distanceM) + _t(' m · jää ') + fmt(ib.distanceM) + _t(' m'), wEst), src: wEst ? 'est' : 'calc',
                 score: -(sb.distanceM + ib.distanceM),
                 sub: [ws.length ? ws.join(' + ') : _t('lume- ja jäämärk puudub'), ts ? _t('testis lumi ') + fmt(ts.m) + _t(' m') : '', ti ? _t('jää ') + fmt(ti.m) + _t(' m') : ''].filter(Boolean).join(' · ') };
    return P;
  }
  /* VÕRDLUS LÜHIDALT: tulemus tavakeeles, enne tabelit (FB/Tarvo: „tulemustes
     peab mõtlema“). Üks lause omaduse kohta: kes on parim ja kui palju.
     Vahe alla mudeli täpsuse (0,5 m / 2 dB) = „ühtviisi“. */
  function vordlusLuhidalt(items) {
    var nimi = function (x) { return '<b>' + esc(x.r.mark + ' ' + x.r.name) + '</b>'; };
    var out = [];
    function meetrid(k, kus, piir) {
      var xs = items.filter(function (x) { return x.P[k]; });
      if (xs.length < 2) return;
      xs.sort(function (a, b) { return a.P[k].v - b.P[k].v; });
      var b = xs[0], w = xs[xs.length - 1], d = w.P[k].v - b.P[k].v;
      var umbes = b.P[k].src === 'est' || w.P[k].src === 'est';
      if (umbes && xs.every(function (x) { return x.P[k].src === 'est'; })) return;
      if (d < piir) { out.push(kus + _t(' pidurdavad kõik ühtviisi (vahe alla ') + fmt(piir) + _t(' m).')); return; }
      out.push(nimi(b) + _t(' peatub ') + kus.toLowerCase() + _t(' kõige varem: ') + (umbes ? _t('umbes ') : '') + '<b>' + fmt(d) + _t(' m lühemalt</b> kui ') + nimi(w) + '.');
    }
    meetrid('wetb', _t('Märjal'), 0.5);
    meetrid('dryb', _t('Kuival'), 0.5);
    var talv = items.some(function (x) { return x.r.catNr >= 1 && x.r.catNr <= 3; });
    if (talv) {
      var ws = items.filter(function (x) { return x.P.winter; }).sort(function (a, b) { return a.P.winter.v - b.P.winter.v; });
      if (ws.length > 1 && ws[ws.length - 1].P.winter.v - ws[0].P.winter.v >= 1 && !ws.every(function (x) { return x.P.winter.src === 'est'; }))
        out.push(nimi(ws[0]) + _t(' on talvel parim: lumel ja jääl peatub kõige varem.'));
    }
    var ns = items.filter(function (x) { return x.P.noise; }).sort(function (a, b) { return a.P.noise.v - b.P.noise.v; });
    if (ns.length > 1) {
      var nd = ns[ns.length - 1].P.noise.v - ns[0].P.noise.v;
      out.push(nd < 2 ? _t('Müra on kõigil sama: ') + ns[0].P.noise.v + '–' + ns[ns.length - 1].P.noise.v + _t(' dB.')
        : nimi(ns[0]) + _t(' on kõige vaiksem: ') + ns[0].P.noise.v + _t(' dB (teised kuni ') + ns[ns.length - 1].P.noise.v + _t(' dB).'));
    }
    var rs = items.filter(function (x) { return x.P.rr; }).sort(function (a, b) { return b.P.rr.score - a.P.rr.score; });
    if (rs.length > 1 && rs[0].P.rr.v !== rs[rs.length - 1].P.rr.v)
      out.push(nimi(rs[0]) + _t(' kulutab kõige vähem kütust (klass ') + esc(rs[0].P.rr.v) + _t(', halvim ') + esc(rs[rs.length - 1].P.rr.v) + ').');
    if (!out.length) return '';
    return '<div class="cmp-lyh"><h3>' + _t('Lühidalt') + '</h3><ul class="why-list">' + out.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul></div>';
  }
  var EST_T = _t('Tuletatud meie valemist — selle rehvi kohta sõltumatut mõõtmist ei ole. Võta suunana, mitte 100% täpse numbrina.');
  var CALC_T = _t('Arvutatud tulemus meie mudelist sinu autoga. Hinnang, mitte mõõtmine — viga on tavaliselt paar meetrit.');
  function est(txt, on) { return on ? _t('<span class="est" tabindex="0" data-tip="') + EST_T + '">≈</span>' + txt : txt; }
  function tip(t) { return _t('<span class="tip" tabindex="0" data-tip="') + esc(t) + _t('" aria-label="') + esc(t) + '">i</span>'; }
  /* ---- HINNAD müüjatelt. Teema hindu ei tea: küsib serverist
     (CFG.prices → /wp-json/pm/v1/hinnad), kuhu müüjate API-ühendus need
     annab. Kui ühendust pole või päring ebaõnnestub, näidatakse seda otse. */
  var PRICE_T = _t('Siia tulevad rehvimüüjate hinnad otse nende süsteemist. Ühendus müüjatega on töös. Hind mõjutab rehvide järjestust ainult siis, kui valid ise „Soodne hind“.');
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
  function eur(v) { return (+v).toFixed(2).replace('.', DEC) + ' €'; }
  function priceSlot(id) { return _t('<div class="pv" data-price="') + esc(id) + _t('"><span class="none">Laen hindu…</span></div>'); }
  /* „u 62 €“ — pakkuja hind on keskmine e-poe hind, mitte täpne */
  function hindTekst(r) { return (r && r.umbes ? _t('u') + ' ' : '') + eur(r.hind); }
  /* Poodide hinnad: rida klikitavaid kaarte (pilt + hind), odavaim ees,
     telefonis keritav vasakule-paremale. Kaart viib selle poe tootelehele. */
  /* nupp, mis avab eelvaate (pilt + nimi); andmed atribuutides */
  function eelNupp(slug, m, nimi, r, sisu) {
    return '<button type="button" class="pk-eel" data-eel="' + esc(slug + '@' + m) + '" data-n="' + esc(nimi) + '" data-pilt="' + (r.pilt ? 1 : 0) + '"' +
      (r.url ? ' data-url="' + esc(poeLink(r.url, 'kalkulaator', nimi)) + '" data-pood="' + esc(r.myyja) + '" data-hind="' + esc(hindTekst(r)) + '"' : '') +
      ' title="' + esc(_t('Vaata selle rehvi pidurdusmaad')) + '">' + sisu + '</button>';
  }
  function valiLink(r, nimi, koht) {
    return r.url ? '<a class="pk-vali" href="' + esc(poeLink(r.url, koht || 'kalkulaator', nimi)) + '" target="_blank" rel="nofollow sponsored noopener" data-pood="' + esc(r.myyja) + '" data-rehv="' + esc(nimi) + '">' + _t('Vali') + ' →</a>' : '';
  }
  /* Kalkulaatori vasak kast: ühe rehvi poed ridadena (pilt · pood · laoseis · hind),
     sama kujundus mis klassi nimekirjal; terve rida viib poodi. */
  function poedRead(rows, id, nimi) {
    if (!rows || !rows.length) return priceHtml(rows, true);
    var x = String(id).split('@'), slug = x[0], m = x[1];
    return '<div class="pk-list">' + rows.slice().sort(function (a, b) { return a.hind - b.hind; }).map(function (r) {
      var ladu = r.laos === false ? _t('tellimisel') : (r.kogus > 0 ? _t('laos') + ' ' + (r.kogus >= 8 ? '8+' : r.kogus) + ' ' + _t('tk') : '');
      var pilt = r.pilt ? '<img src="' + CFG.home + 'api/pilt/' + encodeURIComponent(slug) + '/" alt="" width="48" height="58" loading="lazy" decoding="async">' : '<span class="pk-ring" aria-hidden="true"></span>';
      return '<div class="pk-r">' + eelNupp(slug, m, nimi, r, '<span class="pk-pilt">' + pilt + '</span>') +
        '<span class="pk-nimi"><b>' + esc(r.myyja) + '</b><small>' + esc(ladu) + '</small><span class="pk-rv"><b class="pk-hind">' + hindTekst(r) + '</b>' + valiLink(r, nimi) + '</span></span></div>';
    }).join('') + '</div>';
  }
  function priceHtml(rows, avail, id, nimi) {
    if (rows && rows.length) {
      var slug = id ? String(id).split('@')[0] : '';
      var list = rows.slice().sort(function (a, b) { return a.hind - b.hind; });
      return '<div class="pk-rida">' + list.map(function (r) {
        var ladu = r.laos === false ? _t('tellimisel') : (r.kogus > 0 ? _t('laos') + ' ' + (r.kogus >= 8 ? '8+' : r.kogus) + '\u00a0' + _t('tk') : '');
        var pilt = r.pilt && slug ? '<img src="' + CFG.home + 'api/pilt/' + encodeURIComponent(slug) + '/" alt="" width="72" height="86" loading="lazy" decoding="async">' : '<span class="pk-ring" aria-hidden="true"></span>';
        var sisu = '<span class="pk-pilt">' + pilt + '</span><b>' + hindTekst(r) + '</b><span class="pk-pood">' + esc(r.myyja) + '</span>' + (ladu ? '<small>' + ladu + '</small>' : '');
        return r.url
          ? _t('<a class="pk" href="') + esc(poeLink(r.url, 'rehvileht', nimi)) + _t('" target="_blank" rel="nofollow sponsored noopener" data-pood="') + esc(r.myyja) + '"' + (nimi ? ' data-rehv="' + esc(nimi) + '"' : '') + ' aria-label="' + esc((nimi ? nimi + ' — ' : '') + r.myyja + ' ' + hindTekst(r)) + '">' + sisu + '</a>'
          : '<div class="pk">' + sisu + '</div>';
      }).join('') + '</div>';
    }
    return '<span class="none">' + (avail ? _t('Selle rehvi hinda müüjatelt hetkel pole') : _t('Hinnad pole hetkel saadaval')) + '</span> ' + tip(PRICE_T);
  }
  function fillPrices(box) {
    var els = $$('[data-price]', box);
    if (!els.length) return;
    var ids = els.map(function (e) { return e.dataset.price; }).filter(function (x, i, a) { return a.indexOf(x) === i; });
    Prices.get(ids).then(function (d) {
      var h = (d && d.hinnad) || {};
      els.forEach(function (e) {
        var kaart = e.closest('article'), n = kaart && kaart.querySelector('[data-n]');
        e.innerHTML = priceHtml(h[e.dataset.price], !!(d && d.available), e.dataset.price, n ? n.dataset.n : '');
      });
      /* pakkuja pilt kaardile (meie serveri kaudu); kui laadimine ebaõnnestub, jääb peidetuks */
      $$('img[data-pilt]', box).forEach(function (im) {
        var rows = h[im.dataset.pilt];
        if (!rows || !rows.some(function (r) { return r.pilt; }) || im.getAttribute('src')) return;
        im.onload = function () { im.hidden = false; };
        im.onerror = function () { im.hidden = true; };
        im.src = CFG.home + 'api/pilt/' + encodeURIComponent(im.dataset.pilt.split('@')[0]) + '/';
      });
    });
  }
  function pick(tests, surf, wet) {
    return (tests || []).filter(function (x) { return x.surf === surf && (wet == null || x.wet === wet); })[0] || null;
  }
  function srcLine(x) {
    var s = core.sources[x.src] || {};
    return (s.tegija ? s.tegija.replace(/ \(.*\)/, '') + ' ' + s.aasta : x.src) + ', ' + x.v0 + '→' + x.v1 + _t(' km/h, ') + (s.moot || '');
  }

  /* Kaks lehte, üks loogika:
     data-mode="valik"  — /rehvi-valimine/: küsimused → järjestus + põhjused
     data-mode="vordle" — /vordle-rehve/:   valitud rehvid tabelis, otsing lisamiseks */
  var CT = {
    drive: { city: { noise: 1 }, road: { wet: 1, rr: 1 }, hwy: { wet: 2, aqua: 1 }, mix: { wet: 1, noise: 1 } },
    km: { lo: {}, mid: { rr: 1 }, hi: { rr: 2 }, vhi: { rr: 3 } },
    rft: { only: {}, no: {} },
    main: { safe: { wet: 3, wetb: 1 }, brake: { wetb: 2, dryb: 2 }, price: { price: 3 }, quiet: { noise: 3 }, fuel: { rr: 3 },
            winter: { winter: 3 } }
  };
  /* ext = avalehe kaart (auto ja mõõt tulevad sealt, oma valijaid pole) */
  function initTyres(root, ext) {
    var mode = ext ? 'valik' : (root.dataset.mode || 'vordle');
    var qs = new URLSearchParams(location.search);
    var S = { veh: store.get('veh', null), size: '20555R16', season: 'summer', drive: '', km: '', rft: '', main: [], eri: false };
    if (ext) { var e0 = ext.get(); S.veh = e0.veh; S.size = e0.size; }
    /* NB: parameetrid ei tohi olla WordPressi omad (s, m, p, …) — ?s= teeks
       lehest otsingu ja ?m= kuuarhiivi. */
    if (qs.get('auto')) S.veh = qs.get('auto');
    if (qs.get('moot')) S.size = qs.get('moot');
    if (qs.get('hooaeg') && SEASON[qs.get('hooaeg')]) S.season = qs.get('hooaeg') === 'all' ? 'winter' : qs.get('hooaeg'); /* vanad lingid: aastaringne on nüüd lamelliga koos */
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
        Track('hooaeg', SEASON[S.season].et);
        $$('[data-season]', root).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        save(); draw();
      });
    });

    /* Kui kasutaja pole midagi valinud: parimad selle hooaja teeoludes.
       Suvi = märg + kuiv pidurdus, talv = lumi + jää, aastaringne = mõlemad. */
    var HOOAEG_W = {
      summer: { wetb: 3, dryb: 1 },
      winter: { winter: 3, wetb: 1 },
      naast: { winter: 3, wetb: 1 },
      all: { wetb: 2, winter: 2, dryb: 1 }
    };
    var HOOAEG_TXT = {
      summer: _t('parimad märjal ja kuival teel pidurdamisel'),
      winter: _t('parimad lumel ja jääl pidurdamisel'),
      naast: _t('parimad lumel ja jääl pidurdamisel'),
      all: _t('parimad märjal, lumel ja jääl pidurdamisel')
    };
    /* ---- küsimused (ainult valik) */
    /* kaalud 0–100: küsimuste vastused annavad 33 / 67 / 100, liuguriga saab iga numbri */
    function weights() {
      if (S.w && S.wManual) {
        /* vanad salvestused olid 1–3 */
        var vana = Object.keys(S.w).every(function (k) { return S.w[k] <= 3; });
        if (vana) Object.keys(S.w).forEach(function (k) { S.w[k] = Math.round(S.w[k] * 100 / 3); });
        return S.w;
      }
      var w = {};
      function add(m) { Object.keys(m || {}).forEach(function (k) { w[k] = Math.min(3, (w[k] || 0) + m[k]); }); }
      add(CT.drive[S.drive]); add(CT.km[S.km]);
      S.main.forEach(function (k) { add(CT.main[k]); });
      Object.keys(w).forEach(function (k) { w[k] = Math.round(w[k] * 100 / 3); });
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
    var wTxt = function (v) { return v > 0 ? v + '%' : _t('ei loe'); };
    if (prio) {
      prio.innerHTML = PROPS.map(function (p) {
        return _t('<div class="prio-item') + (p.ok ? '' : ' na') + '"><label class="pr-top" for="w-' + p.k + '"><span class="pn">' + esc(p.n) + '</span>' +
          '<output class="pr-v" data-wv="' + p.k + '">' + wTxt(0) + '</output></label>' +
          '<input type="range" class="slider" id="w-' + p.k + '" min="0" max="100" step="1" value="0" data-w="' + p.k + '"' + (p.ok ? '' : ' disabled') + ' style="--p:0%">' +
          '<span class="pd">' + esc(p.d) + (p.ok ? '' : _t(' <b>Andmed puuduvad.</b>')) + '</span></div>';
      }).join('');
      var wTimer = null;
      $$('input[data-w]', prio).forEach(function (inp) {
        var k = inp.dataset.w;
        var muuda = function (lopp) {
          var v = +inp.value;
          inp.style.setProperty('--p', v + '%');
          var o = $('[data-wv="' + k + '"]', prio); if (o) o.textContent = wTxt(v);
          var w = Object.assign({}, weights()); w[k] = v;
          S.w = w; S.wManual = true;
          clearTimeout(wTimer);
          /* nimekiri järgneb liugurile sujuvalt; lõpus kohe */
          wTimer = setTimeout(function () { save(); paintQ(true); draw(); }, lopp ? 0 : 140);
        };
        inp.addEventListener('input', function () { muuda(false); });
        inp.addEventListener('change', function () { muuda(true); Track('kaal', k + '=' + inp.value); });
      });
    }
    var reset = $('[data-prio-reset]', root);
    if (reset) reset.addEventListener('click', function () { S.drive = S.km = S.rft = ''; S.main = []; S.w = null; S.wManual = false; save(); paintQ(); draw(); });
    function paintQ(liugurilt) {
      $$('[data-ct]', root).forEach(function (b) {
        var on = b.dataset.ct === 'main' ? S.main.indexOf(b.dataset.v) >= 0 : S[b.dataset.ct] === b.dataset.v;
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      var w = weights();
      if (!liugurilt) $$('input[data-w]', root).forEach(function (inp) {
        var v = w[inp.dataset.w] || 0;
        inp.value = v; inp.style.setProperty('--p', v + '%');
        var o = $('[data-wv="' + inp.dataset.w + '"]', root); if (o) o.textContent = wTxt(v);
      });
      var used = Object.keys(w).filter(function (k) { return w[k] > 0 && PROP[k] && PROP[k].ok; });
      var miss = Object.keys(w).filter(function (k) { return w[k] > 0 && PROP[k] && !PROP[k].ok; });
      var box = $('[data-ct-out]', root);
      if (box) box.innerHTML = (used.length ? _t('<p class="note" style="margin:0">Arvestan: ') + used.sort(function (a, b) { return w[b] - w[a]; }).map(function (k) { return '<b>' + esc(PROP[k].n.toLowerCase()) + '</b> ' + w[k] + '%'; }).join(', ') + '</p>' : _t('<p class="note" style="margin:0">Vali ülal, mis sulle oluline on — järjestus muutub kohe.</p>')) +
        (miss.length ? '<div class="note-box" style="margin-top:var(--sp-3)">' + miss.map(function (k) { return PROP[k].n; }).join(', ') + _t(': usaldusväärsed andmed puuduvad — seda ei saa arvestada, ja me ei hakka seda arvama.</div>') : '');
      if (reset) reset.hidden = !used.length && !miss.length;
    }
    paintQ();

    /* ---- põhjused: miks see rehv sinu valikute järgi paistab */
    /* naastrehvid: EL-i märgist pole, seega viide testitud naastrehvidele selle mõõdu talverehvide lehel */
    function naastTeade() {
      var slug = pretty(S.size).toLowerCase().replace(/\//g, '-').replace(/\s+/g, '-');
      var url = LHOME + 'talverehvid/' + slug + '/';
      if (head) head.innerHTML = '<b>' + _t('Naastrehvid') + '</b> · ' + esc(pretty(S.size));
      var tekst = function (link) {
        return '<div class="note naast-note"><p>' + _t('Naastrehvidel ei ole EL-i rehvimärgist, seega ei saa neid mõõdu järgi märgise andmetega järjestada.') + '</p>' +
          '<p>' + _t('Testitud naastrehvide pidurdusmaa jääl ja lumel näed siit:') + ' <a href="' + link + '"><b>' + (link === url ? _t('Parimad talverehvid') + ' ' + esc(pretty(S.size)) : _t('Parimad talverehvid')) + ' →</b></a></p></div>';
      };
      listEl.innerHTML = tekst(LHOME + 'talverehvid/');
      try {
        fetch(url, { method: 'HEAD' }).then(function (r) { if (r.ok && S.season === 'naast') listEl.innerHTML = tekst(url); }).catch(function () {});
      } catch (e) {}
    }
    function reasons(x, stats, w) {
      var out = [], r = x.r, P = x.P;
      var order = Object.keys(w).filter(function (k) { return w[k] > 0; }).sort(function (a, b) { return w[b] - w[a]; });
      if (!order.length) order = ['wet', 'noise'];
      order.forEach(function (k) {
        if (k === 'wet' && r.g) out.push(_t('Märghaardumine <b>') + r.g + '</b>' + (r.g === stats.bestG ? _t(' — parim klass selles mõõdus') : ''));
        if (k === 'wetb' && P.wetb) out.push(_t('Märgpidurdus sinu autoga <b>') + P.wetb.show + '</b>' + (P.wetb.v <= stats.bestWetb + 0.05 ? _t(' — lühim selles nimekirjas') : ' (+' + fmt(P.wetb.v - stats.bestWetb) + _t(' m ehk ') + pct(P.wetb.v - stats.bestWetb, stats.bestWetb) + _t(' parimast)')));
        if (k === 'dryb' && P.dryb) out.push(_t('Kuivpidurdus sinu autoga <b>') + P.dryb.show + '</b>');
        if (k === 'noise' && r.db) {
          var louder = stats.dbs.filter(function (d) { return d > r.db; }).length, qp = Math.round(100 * louder / stats.dbs.length);
          out.push(_t('Müra <b>') + r.db + ' dB</b>' + (qp >= 50 ? _t(' — vaiksem kui ') + qp + _t('% selle mõõdu rehvidest') : ''));
        }
        if (k === 'rr' && r.f) out.push(_t('Veeretakistus <b>') + r.f + '</b>' + (r.f === stats.bestF ? _t(' — parim klass selles mõõdus') : ''));
        if (k === 'winter') out.push(r.catNr === 0 ? '!' + _t('<b>Suverehv</b> — talveks ei sobi') : P.winter.v ? _t('Talvemärgid: <b>') + P.winter.show + '</b>' : '!' + _t('Lume- ja jäämärk <b>puudub</b>'));
        if (k === 'aqua' && P.aqua) out.push(_t('Pidurdusmaa sügavas vees <b>') + P.aqua.show + '</b>');
        if (k === 'price' && P.price) out.push(_t('Hind alates <b>') + P.price.show + '</b>' + (P.price.v <= stats.minHind + 0.005 ? _t(' — soodsaim selles nimekirjas') : ' (+' + eur(P.price.v - stats.minHind) + _t(' soodsaimast)')));
      });
      if (r.tested) out.push(_t('Sõltumatult testitud'));
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
    /* erirehvide linnuke (päises; päis joonistatakse iga kord uuesti) */
    if (head) head.addEventListener('change', function (e) {
      if (!e.target.matches('[data-eri]')) return;
      S.eri = e.target.checked;
      Track('erirehvid', S.eri ? 'jah' : 'ei');
      draw();
    });
    /* run-flat filter (/vordle-rehve/ lisamise ribal; valikulehel on see küsimus) */
    var rftSel = $('[data-rft]', root);
    if (rftSel) rftSel.addEventListener('change', function () {
      S.rft = rftSel.value;
      Track('kriteerium', 'rft=' + S.rft);
      draw();
    });
    if (brandSel) brandSel.addEventListener('change', function () {
      brandVal = brandSel.value;
      Track('margifilter', brandVal || 'kõik margid');
      draw();
    });
    var viimaneN = 0;
    /* „Ühe lausega“: märja pidurduse vahe selle mõõdu ja hooaja keskmisest.
       Keskmine arvutatakse filtreerimata nimekirjast (mark/otsing ei muuda seda). */
    var keskWet = {}, keskVoti = '';
    /* JÄRJESTUS (ainult valik): sobivus sinu valikute järgi või hind */
    var sortBy = 'fit', sortBar = null;
    if (head && mode === 'valik') {
      sortBar = document.createElement('div');
      sortBar.className = 'sortbar';
      sortBar.setAttribute('role', 'group');
      sortBar.setAttribute('aria-label', _t('Järjesta'));
      sortBar.innerHTML = _t('<span>Järjesta:</span><button type="button" data-sort="fit" aria-pressed="true">Sobivus</button>') +
        _t('<button type="button" data-sort="price" aria-pressed="false">Hind</button>');
      head.parentNode.insertBefore(sortBar, head.nextSibling);
      $$('[data-sort]', sortBar).forEach(function (b) {
        b.addEventListener('click', function () {
          if (b.disabled) return;
          sortBy = b.dataset.sort;
          $$('[data-sort]', sortBar).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
          Track('jarjestus', sortBy === 'price' ? 'hind' : 'sobivus');
          draw();
        });
      });
    }
    /* margivalik täidetakse selle mõõdu ja hooaja ridadest, et nimekirjas
       ei oleks marke, mida selles mõõdus üldse ei müüda */
    function paintBrands(rows) {
      if (!brandSel) return;
      var n = {};
      rows.forEach(function (r) { n[r.mark] = (n[r.mark] || 0) + 1; });
      var names = Object.keys(n).sort(function (a, b) { return a.localeCompare(b, 'et'); });
      if (brandVal && names.indexOf(brandVal) < 0) brandVal = '';
      brandSel.innerHTML = _t('<option value="">Kõik margid (') + names.length + ')</option>' +
        names.map(function (m) { return _t('<option value="') + esc(m) + '"' + (m === brandVal ? ' selected' : '') + '>' + esc(m) + ' · ' + n[m] + '</option>'; }).join('');
      brandSel.value = brandVal;
    }
    var joonisNr = 0;
    /* Auto tehasemõõdud: valitud variant või (kui aasta/variant valimata)
       kõik selle margi+mudeli(+aasta) tehasemõõdud. */
    function autoMoodud() {
      var V = core.vehicles, v = S.veh && core.vehByKey[S.veh];
      var mk = $('[data-f=make]', root), md = $('[data-f=model]', root), yr = $('[data-f=year]', root);
      var hulk = v ? [v] : (mk && mk.value && md && md.value ? V.filter(function (x) {
        return x.make === mk.value && x.model === md.value && (!yr || !yr.value || x.yearLabel === yr.value);
      }) : []);
      var out = [];
      hulk.forEach(function (x) {
        (x.oemSizes && x.oemSizes.length ? x.oemSizes : [x.oemSize]).forEach(function (m) {
          m = norm(m); if (m && out.indexOf(m) < 0) out.push(m);
        });
      });
      return { nimi: v ? v.make + ' ' + v.model : (hulk[0] ? hulk[0].make + ' ' + hulk[0].model : ''), m: out };
    }
    /* Tühja tulemuse korral: millistes selle auto mõõtudes on sobivaid rehve */
    function altSizes(box, cats, nr) {
      if (!box) return;
      var a = autoMoodud(), sel = $('[data-f=size]', root);
      var mood = a.m.filter(function (m) { return m !== S.size && core.eprelSizes.indexOf(m) >= 0; });
      if (!a.m.length) {
        if (S.rft === 'only' && sel) box.innerHTML = _t('<p class="note alt-h">Vali auto — näitame, millistes selle tehasemõõtudes run-flat rehve on.</p>');
        return;
      }
      if (!mood.length) return;
      box.innerHTML = _t('<p class="note alt-h">Otsin ') + esc(a.nimi) + _t(' teistest tehasemõõtudest…</p>');
      Promise.all(mood.map(loadSize)).then(function (res) {
        if (nr !== joonisNr) return;
        var leitud = mood.map(function (m, i) {
          return { m: m, n: res[i].filter(function (r) { return cats.indexOf(r.catNr) >= 0 && (!S.rft || (S.rft === 'only') === onRft(r)); }).length };
        }).filter(function (x) { return x.n; }).sort(function (x, y) { return y.n - x.n; });
        if (!leitud.length) {
          box.innerHTML = _t('<p class="note alt-h">Ka ') + esc(a.nimi) + _t(' teistes tehasemõõtudes ') + (S.rft === 'only' ? 'run-flat ' : '') + SEASON[S.season].pp + _t(' meil praegu ei ole.</p>');
          return;
        }
        box.innerHTML = '<p class="alt-h"><b>' + esc(a.nimi) + _t('</b> tehasemõõdud, kus on ') + (S.rft === 'only' ? 'run-flat ' : '') + SEASON[S.season].pp + ':</p>' +
          '<div class="alt-sz">' + leitud.map(function (x) {
            return _t('<button type="button" class="btn sm" data-alt="') + esc(x.m) + '">' + esc(pretty(x.m)) + ' <span>' + x.n + (x.n === 1 ? _t(' rehv') : _t(' rehvi')) + '</span></button>';
          }).join('') + '</div>';
        $$('[data-alt]', box).forEach(function (b) {
          b.addEventListener('click', function () {
            var m = b.dataset.alt;
            Track('alt_moot', m);
            if (sel) {
              if (!$('option[value="' + m + '"]', sel)) { var o = document.createElement('option'); o.value = m; o.textContent = pretty(m); sel.appendChild(o); }
              sel.value = m;
              if (sel._sp && sel._sp._sync) sel._sp._sync();
              sel.dispatchEvent(new Event('change', { bubbles: true }));
            } else { S.size = m; draw(); }
          });
        });
      });
    }
    /* Avalehel on rehvide nimekiri peidus, kuni vaheleht „Leia sobiv rehv“
       pole avatud. Peidus nimekirja ei arvutata (auto valimine ei jõnksu) —
       joonistatakse alles siis, kui see nähtavale tuleb. */
    var peidusKast = ext ? $('[data-home=valik]') : null, ootel = false;
    if (peidusKast && window.MutationObserver) {
      new MutationObserver(function () { if (!peidusKast.hidden && ootel) { ootel = false; draw(); } })
        .observe(peidusKast, { attributes: true, attributeFilter: ['hidden'] });
    }
    function draw() {
      if (peidusKast && peidusKast.hidden && window.MutationObserver) { ootel = true; return; }
      var joonis = ++joonisNr;
      if (!listEl) { drawTable(); return; }
      listEl.innerHTML = _t('<p class="note">Laen…</p>');
      Promise.all([loadSize(S.size), Prices.size(S.size)]).then(function (res) {
        var rows = res[0], hd = res[1] || {}, hOn = !!hd.available, h = hd.hinnad || {};
        var veh = core.vehByKey[S.veh] || core.vehByKey[DEFAULT_VEH];
        if (S.season === 'naast') { naastTeade(); return; }
        var cats = SEASON[S.season].eprel, qq = q ? norm(q.value) : '';
        var seas = rows.filter(function (r) { return cats.indexOf(r.catNr) >= 0; });
        paintBrands(seas);
        var eriN = seas.filter(function (r) { return eriLiik(r) && (!S.rft || (S.rft === 'only') === onRft(r)); }).length;
        var list = seas.filter(function (r) {
          return (S.eri || qq || !eriLiik(r)) && (!brandVal || r.mark === brandVal) && (!qq || norm(r.mark + r.name).indexOf(qq) >= 0) &&
            (!S.rft || (S.rft === 'only') === onRft(r));
        })
          .map(function (r) { return lisaHind({ r: r, P: tyreProps(r, veh) }, h); });
        var wUser = mode === 'valik' ? weights() : {};
        var valis = Object.keys(wUser).some(function (k) { return wUser[k] > 0; });
        var w = mode === 'valik' ? (valis ? wUser : HOOAEG_W[S.season] || {}) : {};
        /* hinda saab arvestada ainult siis, kui müüjate hinnad on olemas */
        var ws = Object.keys(w).filter(function (k) { return w[k] > 0 && PROP[k] && PROP[k].ok && (k !== 'price' || hOn); });
        var hindPuudu = !hOn && w.price > 0;
        var stats = {
          bestG: list.map(function (x) { return x.r.g; }).filter(Boolean).sort()[0],
          bestF: list.map(function (x) { return x.r.f; }).filter(Boolean).sort()[0],
          bestWetb: Math.min.apply(null, list.map(function (x) { return x.P.wetb ? x.P.wetb.v : 999; })),
          dbs: list.map(function (x) { return x.r.db; }).filter(Boolean),
          minHind: Math.min.apply(null, list.map(function (x) { return x.P.price ? x.P.price.v : 1e9; }))
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
          /* „Sobivus %“ ainult siis, kui kasutaja ise midagi valis */
          if (!valis) list.forEach(function (x) { x.fit = null; x.miss = null; });
        } else {
          list.sort(function (a, b) { return (FG[b.r.g] || 0) - (FG[a.r.g] || 0) || (!!b.r.tested - !!a.r.tested) || ((a.r.db || 99) - (b.r.db || 99)); });
        }
        /* hinna järgi: soodsaim enne, hinnata rehvid lõppu (nende omavaheline järjekord jääb) */
        if (sortBar) {
          var hb = $('[data-sort=price]', sortBar);
          hb.disabled = !hOn;
          hb.title = hOn ? _t('Soodsaim hind enne') : _t('Poodide hindu veel ei ole');
          if (!hOn && sortBy === 'price') { sortBy = 'fit'; $$('[data-sort]', sortBar).forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.sort === 'fit')); }); }
        }
        if (sortBy === 'price' && hOn) {
          var pos = new Map(list.map(function (x, i) { return [x, i]; }));
          list.sort(function (a, b) {
            var pa = a.P.price ? a.P.price.v : null, pb = b.P.price ? b.P.price.v : null;
            if ((pa != null) !== (pb != null)) return pa != null ? -1 : 1;
            return (pa != null && pa !== pb) ? pa - pb : pos.get(a) - pos.get(b);
          });
        }
        viimaneN = list.length;
        keskVoti = S.size + '|' + S.season + '|' + (S.veh || '');
        if (!brandVal && !qq) {
          var wv = list.map(function (x) { return x.P.wetb ? x.P.wetb.v : null; }).filter(function (v) { return v != null; });
          keskWet[keskVoti] = wv.length >= 3 ? wv.reduce(function (a, b) { return a + b; }, 0) / wv.length : null;
        }
        if (head) head.innerHTML = '<b>' + list.length + '</b> ' + (list.length === 1 ? SEASON[S.season].yks : SEASON[S.season].osa) + _t(' mõõdus <b>') + esc(pretty(S.size)) + '</b>' +
          (S.rft ? (S.rft === 'only' ? _t(' · ainult run-flat') : _t(' · ilma run-flatita')) : '') +
          (sortBy === 'price' && hOn ? _t(' · soodsaim hind enne') : valis && ws.length ? _t(' · järjestatud sinu valikute järgi') : mode === 'valik' ? ' · ' + HOOAEG_TXT[S.season] : _t(' · järjestatud märghaardumise klassi järgi')) +
          (hindPuudu ? _t('<br><small class="note">Poodide hindu veel ei ole — hinda järjestuses praegu ei arvestata.</small>') : '') +
          (eriN ? _t('<label class="eri-t"><input type="checkbox" data-eri') + (S.eri ? ' checked' : '') + _t('> Näita ka rajarehve ja muid erirehve (') + eriN + ') ' + tip(ERI_T) + '</label>' : '');
        if (!list.length) {
          Track('tulemusi_null', pretty(S.size) + ' · ' + SEASON[S.season].et + (brandVal ? ' · ' + brandVal : '') + (qq ? ' · otsing "' + q.value.trim() + '"' : ''));
          listEl.innerHTML = '<div class="box"><p style="margin:0">' + (rows.length ? (S.rft === 'only' && !brandVal && !qq
              ? _t('Selles mõõdus meil praegu run-flat ') + SEASON[S.season].pp + _t(' ei ole.')
              : _t('Selles mõõdus ei ole andmebaasis ühtegi ') + (S.rft === 'only' ? 'run-flat ' : '') + SEASON[S.season].osa + (brandVal ? _t(' margilt ') + esc(brandVal) : '') + (qq ? _t(' selle otsinguga') : '') + '.') :
            _t('Mõõdu ') + esc(pretty(S.size)) + _t(' märgiseandmed pole veel andmebaasis. Hetkel on korjatud ') + core.eprelSizes.length + _t(' mõõtu.')) + '</p>' +
            (!brandVal && !qq ? '<div data-alt-sizes></div>' : '') + '</div>';
          if (!brandVal && !qq) altSizes($('[data-alt-sizes]', listEl), cats, joonis);
          drawTable(); return;
        }
        var LIM = mode === 'valik' ? 20 : 30;
        listEl.innerHTML = list.slice(0, LIM).map(function (x, i) { return card(x, i, mode === 'valik' ? reasons(x, stats, sortBy === 'price' && hOn ? Object.assign({}, w, { price: 9 }) : w) : null); }).join('') +
          (list.length > LIM ? _t('<p class="note">Näidatakse ') + LIM + _t(' esimest ') + list.length + _t('-st.') + (mode === 'valik' ? _t(' Muuda valikuid, et järjestust muuta.') : _t(' Täpsusta otsingut.')) + '</p>' : '');
        fillPrices(listEl);
        $$('[data-add]', listEl).forEach(function (b) {
          b.addEventListener('click', function () {
            var on = cmp.toggle({ id: b.dataset.add, n: b.dataset.n });
            Track(on ? 'vordlusse' : 'vordlusest_ara', b.dataset.n);
            b.setAttribute('aria-pressed', on ? 'true' : 'false');
            b.textContent = on ? _t('✓ Võrdluses') : _t('+ Võrdle');
            b.closest('.rcard').classList.toggle('on', on);
            drawTable();
          });
        });
        drawTable();
      });
    }
    function prop(label, p, k) {
      if (!p) return '<div class="rp"><div class="l">' + esc(label) + '</div><div class="v none">' + '–' + '</div></div>';
      var pill = { off: _t('Ametlik'), test: _t('Test'), calc: _t('Arvutus'), est: _t('Tuletatud') }[p.src];
      return '<div class="rp"><div class="l">' + esc(label) + (p.src === 'calc' || p.src === 'est' ? ' ' + tip(CALC_T) : '') + '</div><div class="v">' + p.show + '</div><div class="srcd">' + pill + (p.sub ? ' · ' + esc(p.sub) : '') + '</div></div>';
    }
    /* Kompaktne kokkuvõte inimkeeles: number + mida see tähendab. Allikas ja
       arvutuse detail on vihjes (hõljuta / vajuta), mitte kaardil. */
    var MURA = { A: _t('vaikne'), B: _t('tavaline'), C: _t('mürarikkam') };
    var KULU = { A: _t('väike'), B: _t('väike'), C: _t('keskmine'), D: _t('suurem'), E: _t('suur') };
    function kq(label, val, title, cls) {
      return '<div class="q' + (cls ? ' ' + cls : '') + '"' + (title ? ' title="' + esc(title) + '"' : '') + '><span class="ql">' + label + '</span><span class="qv">' + val + '</span></div>';
    }
    function kiired(x) {
      var P = x.P, r = x.r, h = '';
      var src = function (p) { return p ? ({ off: _t('Ametlik EL-i märgis'), calc: _t('Arvutus sinu autoga'), est: _t('Tuletatud (≈)'), test: _t('Test') }[p.src] || '') + (p.sub ? ' · ' + p.sub : '') : ''; };
      if (P.wetb) h += kq(_t('Märjal peatub') + ' <small>90→0</small>', P.wetb.show + (r.g ? ' ' + grade(r.g) : ''), src(P.wetb));
      if (P.dryb) h += kq(_t('Kuival peatub'), P.dryb.show, src(P.dryb));
      if (P.noise) h += kq(_t('Müra'), (MURA[r.nk] || '') + ' <small>' + r.db + ' dB</small>', src(P.noise));
      if (P.rr) h += kq(_t('Kütusekulu'), (KULU[r.f] || '') + ' ' + grade(r.f), _t('Veeretakistuse klass (EL-i märgis): A on kõige säästlikum.'));
      if (P.winter && r.catNr !== 0) h += kq(_t('Lumel / jääl') + ' <small>50→0</small>', P.winter.show.replace(_t('lumi '), '').replace(_t(' · jää '), ' / '), src(P.winter));
      return '<div class="qs">' + h + '</div>';
    }
    function lause(x) {
      var k = keskWet[keskVoti], v = x.P.wetb ? x.P.wetb.v : null;
      if (k == null || v == null) return '';
      var d = k - v, a = fmt(Math.abs(d), 1);
      if (Math.abs(d) < 0.5) return '<p class="rc-lause">' + _t('Märjal peatub sama kaugel kui selle mõõdu keskmine rehv.') + '</p>';
      return '<p class="rc-lause ' + (d > 0 ? 'hea' : 'halb') + '">' + _t('Märjal peatub') + ' <b>' + a + ' ' + _t('m') + ' ' + (d > 0 ? _t('varem') : _t('hiljem')) + '</b> ' + _t('kui selle mõõdu keskmine rehv.') + '</p>';
    }
    function card(x, i, why) {
      var r = x.r, id = r.slug + '@' + r.m, on = cmp.has(id);
      return _t('<article class="rcard') + (on ? ' on' : '') + '"><div class="rc-info">' +
        '<div class="b">' + (why ? '<span class="rank">' + (i + 1) + '</span>' : '') + (KAT_KAART[r.catNr] ? '<span class="kat-b kat-' + r.catNr + '">' + KAT_KAART[r.catNr] + '</span>' : '') + (r.tested ? _t('<span style="color:var(--tested)">Sõltumatult testitud</span>') : _t('<span style="color:var(--muted)">EL-i märgis</span>')) +
          (onRft(r) ? '<span class="rft-b">Run-flat ' + tip(RFT_T) + '</span>' : '') +
          (eriLiik(r) ? '<span class="rft-b eri-b">' + esc(eriLiik(r)) + ' ' + tip(ERI_T) + '</span>' : '') + '</div>' +
        _t('<h3><a href="') + rTee(r.slug) + '/"><span class="mk">' + esc(r.mark) + '</span> ' + esc(r.name) + '</a></h3>' +
        (x.fit != null ? _t('<span class="fit" title="Sobivus sinu valitud omaduste põhjal selles nimekirjas — mitte üldine hinne">Sobivus ') + x.fit + '%</span>' : '') + '</div>' +
        '<div class="rc-side"><img class="rpilt" alt="" width="96" height="112" decoding="async" hidden data-pilt="' + esc(id) + '">' +
        _t('<button type="button" class="add-btn" data-add="') + esc(id) + _t('" data-n="') + esc(r.mark + ' ' + r.name) + _t('" aria-pressed="') + on + '">' + (on ? _t('✓ Võrdluses') : _t('+ Võrdle')) + '</button></div>' +
        (why && why.length ? '<ul class="why-list">' + why.map(function (t) { return t.charAt(0) === '!' ? '<li class="x">' + t.slice(1) + '</li>' : '<li>' + t + '</li>'; }).join('') + '</ul>' : '') +
        lause(x) + kiired(x) +
        _t('<div class="price"><div class="pl">Hinnad poodides</div>') + priceSlot(id) + '</div>' +
        (x.miss && x.miss.length ? _t('<p class="note" style="grid-column:1/-1;margin:0">Sobivuses arvestamata: ') + esc(x.miss.join(', ')) + '</p>' : '') + '</article>';
    }

    /* URL-ist tulnud rehvil on ainult slug — õige nimi mõõdu andmetest */
    function nimedSlugist(box) {
      $$('[data-csn]', box).forEach(function (b) {
        var x = b.dataset.csn.split('@');
        loadSize(x[1]).then(function (rows) { var r = rows.filter(function (y) { return y.slug === x[0]; })[0]; if (r) b.textContent = r.mark + ' ' + r.name; });
      });
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
          var pb = p.id.split('@');
          return '<span class="chip"><span data-csn="' + esc(p.id) + '">' + esc(p.n && p.n !== p.id && p.n !== pb[0] ? p.n : titleCase(pb[0].replace(/-/g, ' '))) + '</span>' + _t(' <button type="button" data-trm="') + esc(p.id) + _t('" aria-label="Eemalda">×</button></span>');
        }).join('');
        nimedSlugist(tray);
        $$('[data-trm]', tray).forEach(function (b) { b.addEventListener('click', function () { cmp.toggle({ id: b.dataset.trm }); draw(); }); });
        var go = $('[data-tray-go]', tray);
        if (go) { go.href = mode === 'valik' ? cmpUrl(sel, { auto: S.veh }) : '#vordlus'; go.textContent = mode === 'valik' ? _t('Võrdle kõrvuti (') + sel.length + ') →' : _t('Vaata võrdlust ↓'); }
      }
      if (!tblBox) return;
      if (sel.length < 2) {
        if (mode !== 'vordle') { tblBox.innerHTML = ''; return; }
        /* 4 pesa: valitud rehvid + tühjad „Lisa rehv“ pesad */
        var pesad = '';
        for (var pi = 0; pi < 4; pi++) {
          var pp = sel[pi];
          if (pp) {
            var pb = pp.id.split('@');
            pesad += '<div class="cs on"><img src="' + CFG.home + 'api/pilt/' + encodeURIComponent(pb[0]) + '/" alt="" width="56" height="66" onerror="this.remove()">' +
              '<span class="cs-n"><b data-csn="' + esc(pp.id) + '">' + esc(pp.n && pp.n !== pp.id && pp.n !== pb[0] ? pp.n : titleCase(pb[0].replace(/-/g, ' '))) + '</b><small>' + esc(pretty(pb[1])) + '</small></span>' +
              _t('<button type="button" class="cs-x" data-xrm="') + esc(pp.id) + _t('" aria-label="Eemalda ') + esc(pp.n) + '">×</button></div>';
          } else pesad += '<a class="cs add" href="#lisa"><span aria-hidden="true">+</span>' + _t('Lisa rehv') + '</a>';
        }
        tblBox.innerHTML = '<div class="cmp-slots"><div class="cs-h"><h2>' + _t('Valitud rehvid') + '</h2><span class="cs-c">' + sel.length + ' / 4</span></div>' +
          '<div class="cs-grid">' + pesad + '</div><p class="note" style="margin:0">' +
          (sel.length ? _t('Lisa veel vähemalt üks rehv — siis tuleb võrdlus kõrvuti.') : _t('Vali allpool 2–4 rehvi.')) +
          ' ' + _t('Või') + ' <a href="' + LHOME + 'rehvi-valimine/">' + _t('lase rehvi valimisel') + '</a> ' + _t('sobivad välja pakkuda.') + '</p></div>';
        $$('[data-xrm]', tblBox).forEach(function (b) { b.addEventListener('click', function () { cmp.toggle({ id: b.dataset.xrm }); draw(); }); });
        nimedSlugist(tblBox);
        $$('a.cs.add', tblBox).forEach(function (a) { a.addEventListener('click', function () { setTimeout(function () { var q = $('[data-q]', root); if (q) q.focus({ preventScroll: true }); }, 350); }); });
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
          [_t('Märghaare'), null],
          [_t('Märghaardumise klass'), 'wet', 'max', 'Ametlik'],
          [_t('Märgpidurdus 90→0 (sinu auto)'), 'wetb', 'max', 'Arvutus'],
          [_t('Vesiliug: 90→0 sügava veega teel'), 'aqua', 'max', 'Arvutus', _t('Uus rehv (8 mm muster). Teel on 3 mm vett — nagu roobastes või suures lombis. Siis hakkab rehv vee peal ujuma ja pidurdusmaa kasvab. Arvutatud tulemus, mitte mõõtmine.')],
          [_t('Kuiv ja talv'), null],
          [_t('Kuivpidurdus 90→0 (sinu auto)'), 'dryb', 'max', 'Arvutus'],
          [_t('Talvemärgid'), 'winter', null, 'Ametlik'],
          [_t('Märgis'), null],
          [_t('Müra'), 'noise', 'max', 'Ametlik'],
          [_t('Veeretakistus'), 'rr', 'max', 'Ametlik'],
          ['Run-flat', 'rft'],
          [_t('Hind'), null],
          [_t('Hind müüjatelt'), 'price']
        ];
        var h = _t('<div class="cmp-table" id="vordlus"><h2>Valitud rehvid</h2><p class="note">Kollane joon = parim selles reas. Sama auto: ') + esc(veh.name) + _t('. <span class="est">≈</span> = tuletatud meie valemist, selle rehvi kohta mõõtmist ei ole. Hõljuta hiirt märgi peal.</p>') + vordlusLuhidalt(items) + _t('<div class="tbl-wrap"><table class="cmp"><thead><tr><th scope="col">Omadus</th>') +
          items.map(function (x) { return _t('<th scope="col"><a href="') + rTee(x.r.slug) + '/">' + esc(x.r.mark + ' ' + x.r.name) + '</a><span class="s" style="font-weight:500;color:var(--muted);display:block;font-size:12px">' + esc(pretty(x.r.m)) + _t(' · <button type="button" class="linkbtn" style="font-size:12px" data-xrm="') + esc(x.r.slug + '@' + x.r.m) + _t('">eemalda</button></span></th>'); }).join('') + '</tr></thead><tbody>';
        ROWS.forEach(function (row) {
          if (!row[1]) { h += _t('<tr class="grp"><th colspan="') + (items.length + 1) + '">' + esc(row[0]) + '</th></tr>'; return; }
          if (row[1] === 'rft') { h += '<tr><th scope="row">Run-flat ' + tip(RFT_T) + '</th>' + items.map(function (x) { return '<td>' + (onRft(x.r) ? _t('Jah') : _t('Ei')) + '</td>'; }).join('') + '</tr>'; return; }
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
              if (diff > 0.05) extra = ' <span class="pct">+' + fmt(diff) + _t(' m · ') + pct(diff, bestM) + '</span>';
            }
            return '<td' + (win ? ' class="win"' : '') + '><span class="v">' + p.show + '</span>' + extra + (p.sub ? '<span class="s">' + esc(p.sub) + '</span>' : '') + '</td>';
          }).join('') + '</tr>';
        });
        h += '</tbody></table></div>';
        h += _t('<p class="swipe-hint">Libista, et näha kõiki →</p><div class="swipe">') + items.map(function (x) {
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
    $('[data-tw-veh]', root).textContent = veh.name + (core.vehByKey[myVeh] ? '' : _t(' (vali oma auto avalehel)'));
    if (sizes.length) {
      sSel.innerHTML = sizes.map(function (z) { return _t('<option value="') + esc(z.m) + '">' + esc(pretty(z.m)) + _t(' · klass ') + esc(z.g) + '</option>'; }).join('');
      var oem = norm(veh.oemSize); if ($('option[value="' + oem + '"]', sSel)) sSel.value = oem;
    } else sSel.closest('.fld').hidden = true;
    $$('[data-tw-cond]', root).forEach(function (b) {
      b.addEventListener('click', function () { ck = b.dataset.twCond; $$('[data-tw-cond]', root).forEach(function (x) { x.setAttribute('aria-pressed', x === b); }); go(); });
    });
    sSel.addEventListener('change', go);
    function go() {
      var z = sizes.filter(function (x) { return x.m === sSel.value; })[0];
      var t = tested ? Object.assign({}, core.tyreByKey[tested]) : null;
      var mSel = z ? z.m : norm(veh.oemSize);
      var tyre = t ? onCar(t, mSel) : (z ? { key: 'w', name: 'x', category: root.dataset.cat, wetGripIndex: gmid(z.g, root.dataset.cat), treadDepthMm: 8, treadDepthNewMm: 8, pressureBar: null, loadCapacityKg: null, ageYears: 1, studded: false, size: pretty(z.m), gSource: 'label' } : null);
      if (!tyre) { out.innerHTML = _t('<p class="note">Andmed puuduvad.</p>'); return; }
      var cond = condObj(ck, speed), r = calc(tyre, veh, cond);
      var cat = tyre.category, m = z ? z.m : norm(veh.oemSize);
      var a = calc(classTyre('A', cat, m), veh, cond).distanceM, e = calc(classTyre('E', cat, m), veh, cond).distanceM;
      var knows = ck === 'wet' || (ck === 'dry' && t && t.muDry != null) || (ck === 'snow' && t && t.muSnow != null) || (ck === 'ice' && t && t.muIce != null);
      out.innerHTML = '<p class="res-big" style="font-size:72px;margin:var(--sp-2) 0">' + (knows ? '' : _t('<span class="est" tabindex="0" style="font-size:20px;height:30px;min-width:30px;vertical-align:14px" data-tip="') + EST_T + '">≈</span>') + '<span class="hl">' + fmt(r.distanceM) + _t('</span><small>m</small></p>') +
        '<p class="res-band">' + speed + _t(' → 0 km/h, ') + COND[ck].label + _t(' · vahemik <b>') + fmt(r.lowM) + '–' + fmt(r.highM) + _t(' m</b> · ilma reaktsiooniajata</p>') +
        (ck === 'wet' ? _t('<p class="note">Võrdluseks samas mõõdus: A-klassi märgisega rehv ') + fmt(a) + _t(' m, E-klassi ') + fmt(e) + _t(' m.') +
          (t ? _t(' Selle rehvi haare tuleb testi mõõtmisest (') + esc(t.size) + _t('), mitte klassist — seepärast võib ta klassi tüüpilisest erineda.') : '') + '</p>' : '') +
        (knows ? '' : _t('<div class="note-box"><span class="est">≈</span>Tuletatud meie mudelist (') + COND[ck].label + _t('): kasutame rehvitüübi keskmist haaret, sest selle rehvi kohta sõltumatut mõõtmist ei ole.</div>')) +
        _t('<div class="res-meta"><span class="pill calc">Arvutatud hinnang</span>') + (t ? _t('<span class="pill test">Haare testist</span>') : _t('<span class="pill off">Märgise klass</span>')) + '</div>';
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
    /* eeltäide lingist (tulemuse „Leidsid vea?“): ?teema=viga&sonum=… */
    try {
      var qk = new URLSearchParams(location.search);
      if (qk.get('teema') && form.teema && $('option[value="' + qk.get('teema').replace(/[^a-z]/g, '') + '"]', form.teema)) form.teema.value = qk.get('teema').replace(/[^a-z]/g, '');
      if (qk.get('sonum') && form.sonum && !form.sonum.value) form.sonum.value = qk.get('sonum').slice(0, 1000);
    } catch (e) {}
    var msg = $('[data-contact-msg]', form), go = $('[data-contact-go]', form);
    function say(t, ok) { msg.hidden = false; msg.className = 'form-msg ' + (ok ? 'ok' : 'err'); msg.textContent = t; }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form), v = function (k) { return String(f.get(k) || '').trim(); };
      if (!v('nimi')) { say(_t('Palun kirjuta oma nimi.')); form.nimi.focus(); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('email'))) { say(_t('Palun kontrolli e-posti aadressi — sellele vastame.')); form.email.focus(); return; }
      if (v('sonum').length < 5) { say(_t('Palun kirjuta sõnum.')); form.sonum.focus(); return; }
      /* robotikontroll: kui vidin on lehel, peab luba olemas olema */
      var tsId = form.getAttribute('data-ts-id');
      if ($('.ts', form) && !v('cf-turnstile-response')) { say(_t('Oota hetk — robotikontroll pole veel valmis. Kui vormi all on kast, märgi see.')); return; }
      var topic = form.teema.options[form.teema.selectedIndex].text;
      if (!CFG.contact) {
        var body = 'Teema: ' + topic + '\nNimi: ' + v('nimi') + '\nE-post: ' + v('email') + (v('firma') ? _t('\nEttevõte: ') + v('firma') : '') + '\n\n' + v('sonum');
        location.href = 'mailto:' + (CFG.contactMail || '') + '?subject=' + encodeURIComponent('[Pidurdusmaa.ee] ' + topic + ' — ' + v('nimi')) + '&body=' + encodeURIComponent(body);
        say(_t('Avasime kirja sinu e-posti programmis — vajuta seal „Saada“.'), true);
        return;
      }
      go.disabled = true; go.textContent = 'Saadan…';
      fetch(CFG.contact, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(Object.fromEntries(f)) })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); say(_t('Aitäh! Kiri on saadetud — vastame e-postile.'), true); }
          else say((d && d.msg) || _t('Saatmine ebaõnnestus. Proovi hiljem uuesti.'));
        })
        .catch(function () { say(_t('Ühendus katkes. Proovi uuesti.')); })
        .then(function () {
          go.disabled = false; go.textContent = _t('Saada kiri →');
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
    trackAiAllikas();
  }

  /* GEO mõõtmine: kas külastaja tuli AI-otsingust (ChatGPT, Perplexity …)?
     Salvestatakse AINULT allika nimi (nt "chatgpt"), mitte aadress ega
     päring. ChatGPT lisab linkidele utm_source=chatgpt.com; teised annavad
     viitaja (referrer). Kord lehe avamise kohta. */
  var AI_ALLIKAD = [
    ['chatgpt', /(^|\.)(chatgpt\.com|chat\.openai\.com|openai\.com)$/],
    ['perplexity', /(^|\.)perplexity\.ai$/],
    ['claude', /(^|\.)claude\.ai$/],
    ['gemini', /(^|\.)gemini\.google\.com$/],
    ['copilot', /(^|\.)copilot\.microsoft\.com$/],
    ['deepseek', /(^|\.)chat\.deepseek\.com$/],
    ['you', /(^|\.)you\.com$/],
    ['phind', /(^|\.)phind\.com$/]
  ];
  function aiAllikas(host) {
    host = String(host || '').toLowerCase().replace(/^www\./, '');
    for (var i = 0; i < AI_ALLIKAD.length; i++) if (AI_ALLIKAD[i][1].test(host)) return AI_ALLIKAD[i][0];
    return '';
  }
  function trackAiAllikas() {
    try {
      var utm = new URLSearchParams(location.search).get('utm_source') || '';
      var a = aiAllikas(utm.replace(/^https?:\/\//, '').split('/')[0]);
      if (!a && document.referrer) {
        var r = new URL(document.referrer);
        if (r.host !== location.host) a = aiAllikas(r.hostname);
      }
      if (a) Track('ai_allikas', a);
    } catch (e) { /* vigane referrer — jätame vahele */ }
  }

  /* laiad tabelid: kerimisala peab olema klaviatuuriga kättesaadav */
  function tablesA11y() {
    $$('.tbl-wrap').forEach(function (t) {
      if (t.scrollWidth > t.clientWidth + 1 && !t.hasAttribute('tabindex')) {
        var h = t.closest('.box, .cmp-table'); h = h && $('h2', h);
        t.setAttribute('tabindex', '0'); t.setAttribute('role', 'region');
        t.setAttribute('aria-label', (h ? h.textContent.trim() + ' — ' : '') + _t('tabel, keri külgsuunas'));
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
        img.alt = _t('Rehvi pilt');
        img.decoding = 'async';
        img.onload = function () {
          box.innerHTML = '';
          box.classList.add('has-photo');
          box.setAttribute('aria-label', _t('Rehvi pilt'));
          box.appendChild(img);
          var cap = $('[data-rehv-pilt-allkiri]');
          if (cap) cap.textContent = _t('Pilt: rehvimüüja');
        };
        img.src = d.pilt;
      })
      .catch(function () {});
  }

  /* partneri kaardi klikk statistikasse (üks kuular kogu saidile) */
  var partnerKuular = false;
  function initPage() {
    trackPage();
    if (!partnerKuular) {
      partnerKuular = true;
      /* väljaminevad poelingid (rel="sponsored"): partneri kaart või hind */
      document.addEventListener('click', function (e) {
        var a = e.target instanceof Element ? e.target.closest('a[rel~="sponsored"]') : null;
        if (!a) return;
        if (a.dataset.partner) { Track('partner_klikk', a.dataset.partner); return; }
        var pood = a.dataset.pood || a.textContent.trim() || a.hostname;
        Track('poe_klikk', pood + (a.dataset.rehv ? ' · ' + a.dataset.rehv : ''));
      });
    }
    /* päis jääb lehevahetusel alles — sulgeme lahtise menüü */
    var pm = $('#pm-panel');
    if (pm && !pm.hidden && window.PM_MENU) window.PM_MENU(false, true);
    if (window.PM_PWA) window.PM_PWA();
    $$('[data-dd].open').forEach(function (dd) { dd.classList.remove('open'); $('.dd-btn', dd).setAttribute('aria-expanded', 'false'); });
    tablesA11y();
    rehviPilt();
    var needs = $('[data-calc]') || $('[data-cmp-page]') || $('[data-tw]');
    cmp.paint();
    /* Sama lehe uuesti avamine (nt logo peale vajutus avalehel) jätab DOM-i
       alles, aga afterNavigate kutsub initPage uuesti. Ilma kaitseta
       lisataks iga kord uued kuularid ja uus autootsingu lahter.
       Iga plokk seadistatakse seega ainult üks kord (_pm lipp). */
    function kord(el) { if (!el || el._pm) return false; el._pm = true; return true; }
    var kf = $('[data-contact]'); if (kord(kf)) initContact(kf);
    if (!needs) return Promise.resolve();
    return loadCore().then(function () {
      var c = $('[data-calc]'), cUus = kord(c); if (cUus) initCalc(c);
      var h = $('[data-valik-home]'); if (cUus && h) initTyres(document.getElementById('sisu') || document.body, c.pmBus);
      var p = $('[data-cmp-page]'); if (kord(p)) initTyres(p);
      var w = $('[data-tw]'); if (kord(w)) initTyreWidget(w);
      setTimeout(tablesA11y, 300);
    }).catch(function (e) {
      $$('[data-calc],[data-cmp-page],[data-tw]').forEach(function (x) {
        x.insertAdjacentHTML('afterbegin', _t('<p class="note-box" style="margin:var(--sp-4)">Andmete laadimine ebaõnnestus. Proovi lehte värskendada.</p>'));
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

  /* ------------------------------------------------------------ PWA
     Avaekraanile lisamine: Android/Chrome annab oma akna (beforeinstallprompt,
     püütakse app.html-is kinni), iPhone'is näitame juhist (Jaga → Lisa
     avaekraanile). Avaekraanilt avatuna nuppu ei näidata. */
  function initPwa() {
    var mm = window.matchMedia ? matchMedia('(display-mode: standalone)') : null;
    var app = (mm && mm.matches) || navigator.standalone === true;
    document.documentElement.classList.toggle('pwa', !!app);
    if (app) { Track('pwa_avatud'); return; }
    var ios = /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    var paigaldatud = false;
    /* nupud: päises keelte kõrval + menüüs. Näha ainult siis, kui lisada saab. */
    function naita() { $$('[data-pwa-lisa]').forEach(function (b) { b.hidden = paigaldatud || !(window.PM_BIP || ios); }); }
    window.PM_PWA = naita;
    naita();
    window.addEventListener('pm:bip', naita);
    function leht(lahti) {
      var sh = $('[data-pwa-sheet]'); if (!sh) return;
      if (lahti) {
        var v = pwaSammud(), ol = $('[data-pwa-sammud]', sh), n = $('[data-pwa-nool]', sh);
        if (ol) ol.innerHTML = v.html;
        if (n) { n.className = 'ps-nool' + (v.nool ? ' ps-nool-' + v.nool : ''); n.hidden = !v.nool; }
        /* kui nupp on all, jääb juhis üles, et brauseri riba oleks näha */
        sh.classList.toggle('ps-ylal', v.nool === 'keskel' || v.nool === 'paremal');
      }
      sh.hidden = !lahti;
      if (lahti) { var x = $('[data-pwa-sulge]', sh); if (x) x.focus(); }
    }
    window.addEventListener('appinstalled', function () { Track('pwa_paigaldatud'); paigaldatud = true; naita(); leht(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') leht(false); });
    document.addEventListener('click', function (e) {
      var t = e.target;
      if (t.closest && t.closest('[data-pwa-sulge]')) { leht(false); return; }
      if (t.matches && t.matches('[data-pwa-sheet]')) { leht(false); return; }
      var b = t.closest && t.closest('[data-pwa-lisa]');
      if (!b) return;
      Track('pwa_lisa_nupp', (ios ? 'ios' : 'android') + (b.closest('.site-header .hdr-right') ? ' · päis' : ' · menüü'));
      if (window.PM_BIP) {
        var ev = window.PM_BIP; window.PM_BIP = null;
        ev.prompt();
        if (ev.userChoice) ev.userChoice.then(function (c) { Track('pwa_valik', c && c.outcome); naita(); });
        naita();
      } else if (ios) leht(true);
    });
  }
  /* iPhone: täpne juhis sõltub brauserist ja iOS-i versioonist. Nool näitab,
     kus ekraanil see nupp on (Safari all, Chrome üleval). */
  function pwaSammud() {
    var ua = navigator.userAgent;
    var inapp = /FBAN|FBAV|Instagram|Messenger|Line\/|TikTok|Snapchat/i.test(ua);
    var chrome = /CriOS/i.test(ua), firefox = /FxiOS/i.test(ua), edge = /EdgiOS/i.test(ua);
    var ver = +((/Version\/(\d+)/.exec(ua) || [])[1] || 0);
    var ik = function (n) { var t = $('[data-pwa-ikoonid]'); var e = t && t.content.querySelector('[data-i="' + n + '"]'); return e ? e.innerHTML : ''; };
    var ok = '<span class="ps-ic ps-ok">' + _t('Lisa') + '</span>';
    var rida = function (ic, html) { return '<li><span class="ps-ic">' + ic + '</span><span>' + html + '</span></li>'; };
    var lisa = rida(ik('plusbox'), _t('Vali <b>„Lisa avaekraanile“</b> (keri menüüs veidi alla)'));
    var lopp = '<li>' + ok + '<span>' + _t('Vajuta üleval paremal <b>„Lisa“</b> — valmis!') + '</span></li>';
    if (inapp) return { nool: '', html: rida(ik('menu'), _t('See leht on avatud Instagrami või Facebooki sees. Vajuta üleval paremal <b>⋯</b> ja vali <b>„Ava brauseris“</b>')) + rida(ik('share'), _t('Siis vajuta Safaris uuesti nuppu <b>„Äpp“</b>')) };
    if (chrome || edge) return { nool: 'ules', html: rida(ik('share'), _t('Vajuta üleval aadressiriba paremas servas <b>Jaga</b>-nuppu')) + lisa + lopp };
    if (firefox) return { nool: 'paremal', html: rida(ik('menu'), _t('Vajuta all paremal <b>☰</b> ja siis <b>Jaga</b>')) + lisa + lopp };
    if (ver >= 26) return { nool: 'paremal', html: rida('<b class="ps-dots">⋯</b>', _t('Vajuta all paremal <b>⋯</b> ja siis <b>Jaga</b>')) + lisa + lopp };
    return { nool: 'keskel', html: rida(ik('share'), _t('Vajuta all keskel <b>Jaga</b>-nuppu (ruut noolega)')) + lisa + lopp };
  }

  window.PM = { initPage: initPage, lugu: lugu, track: Track };

  /* SvelteKit laeb selle faili onMount'is, st PÄRAST DOMContentLoaded'i —
     siis see sündmus enam ei tule ja päis (burger, rippmenüü), infodialoog
     ja infomullid jääksid käivitamata. Käivitame kohe, kui DOM on valmis. */
  var booted = false;
  function boot() {
    if (booted) return; booted = true;
    initHeader(); initHow(); initTips(); initPwa();
    if (!window.PM_DEFER) initPage();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
