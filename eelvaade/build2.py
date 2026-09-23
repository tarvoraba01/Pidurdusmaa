"""Terve Pidurdusmaa.ee sait ühe eelvaatefailina.

Iga leht on WordPressist kroolitud (crawl/mains.json), ükski mall ei ole
siin ümber kirjutatud. Lehtede sisu on gzipitud ja base64 — lahtipakituna
17 MB, pakituna ~0,4 MB. Navigeerimine käib history.pushState'iga ilma
täislaadimiseta; lehe interaktiivsed osad käivitab window.PM.initPage().
"""
import base64, glob, gzip, json, os, re, html

T = '/home/claude/theme/pidurdusmaa'
H = 'https://pidurdusmaa.preview/'
OUT = '/tmp/claude-0/-home-claude/6ee2bab2-7a91-53d7-9456-97f033b03d7b/scratchpad/pidurdusmaa-eelvaade.html'

pages = json.load(open('/tmp/prev/crawl/pages.json', encoding='utf-8'))
home = pages['/']
header = home[home.index('<header class="site-header">'):home.index('</header>') + 9]
footer = home[home.index('<footer class="site-footer">'):home.index('</footer>') + 9]

img = 'data:image/jpeg;base64,' + base64.b64encode(open(T + '/assets/img/hero-car.jpg', 'rb').read()).decode()


def fix(h):
    h = h.replace('http://localhost:8080/wp-content/themes/pidurdusmaa/assets/img/hero-car.jpg', img)
    h = h.replace('http://localhost:8080/', H)
    h = h.replace('http://localhost:8080', H.rstrip('/'))
    h = re.sub(r'(href|action)="/(?!/)', r'\1="' + H, h)  # juurelised lingid WP sisust
    # välislingid uude aknasse (eelvaade on raamis)
    h = re.sub(r'<a ([^>]*href="https?://(?!pidurdusmaa\.preview)[^"]+")', r'<a target="_blank" \1', h)
    return h


store = {}
for u, h in pages.items():
    m = h[h.index('<main id="sisu">') + 16:h.index('</main>')]
    t = html.unescape(re.search(r'<title>(.*?)</title>', h, re.S).group(1))
    store[u] = {'t': t, 'm': fix(m)}
# EELVAATE TAGASISIDE
# Kontaktivorm jääb selliseks, nagu ta on — see on ETTEVÕTETELE (rehvimüüjad,
# koostöö). Eelvaates serverit ei ole, nii et vorm avab valmis kirja.
# Tagasiside käib eraldi: igal lehel on nupp, mis avab paneeli. Paneel
# kopeerib kasutaja TEEKONNA (window.PM.lugu()) lõikelauale ja avab Google'i
# küsitluse, kuhu selle saab kleepida. Nii on näha, mida päriselt tehti.
TAGASISIDE_URL = os.environ.get('TAGASISIDE_URL', '')   # küsitlus nr 1: tagasiside
ARI_URL = os.environ.get('ARI_URL', '')                 # küsitlus nr 2: ettevõtetele

if ARI_URL and '/kontakt/' in store:
    k = store['/kontakt/']['m']
    i, j = k.index('<form'), k.index('</form>') + 7
    store['/kontakt/']['m'] = k[:i] + (
        '<div class="box contact-form"><h2 style="margin:0 0 8px">Kirjuta meile</h2>'
        '<p class="note" style="margin:0 0 16px">Rehvimüüjale, koostööks või andmevea kohta — '
        'vasta lühikesele vormile, vastame e-postile.</p>'
        '<p style="margin:0"><a class="btn yel" href="' + ARI_URL + '" target="_blank" rel="noopener">'
        'Ava kontaktivorm →</a></p></div>') + k[j:]

e404 = open('/tmp/prev/404.html', encoding='utf-8').read()
store['__404'] = {'t': 'Lehte ei leitud | Pidurdusmaa.ee',
                  'm': fix(e404[e404.index('<main id="sisu">') + 16:e404.index('</main>')])}

# kontroll: iga sisemine link peab viima kroolitud lehele
missing = set()
for u, v in store.items():
    for href in re.findall(r'href="' + re.escape(H) + r'([^"#?]*)', v['m'] + header + footer):
        if '/' + href not in store and href != '':
            missing.add('/' + href)
print('puuduvad lingisihtmärgid:', len(missing), sorted(missing)[:10])

# Lehed killudeks: brauser pakib lahti ainult selle killu, kus avatav leht
# on (muidu tuleks iga avamisel lahti pakkida ~60 MB).
# Killud tehakse SORTEERITUD järjekorras: kõrvuti satuvad sarnased lehed
# (sama mõõdu rehvid), mis pakib ~30 % väiksemaks kui juhuslik jaotus.
NSH = 64
keys = sorted(store)
per = (len(keys) + NSH - 1) // NSH
shards, bounds = [], []
for i in range(0, len(keys), per):
    part = keys[i:i + per]
    bounds.append(part[0])
    shards.append({k: store[k] for k in part})
blob = json.dumps([base64.b64encode(gzip.compress(json.dumps(x, ensure_ascii=False, separators=(',', ':')).encode(), 9)).decode() for x in shards])
bounds_js = json.dumps(bounds, ensure_ascii=False)
print('killud:', NSH, 'suurim', max(len(x) for x in json.loads(blob)) // 1024, 'KB')

css = open(T + '/assets/css/main.css', encoding='utf-8').read()
for f in glob.glob(T + '/assets/fonts/*.woff2'):
    b = base64.b64encode(open(f, 'rb').read()).decode()
    css = css.replace('url(../fonts/' + os.path.basename(f) + ')', 'url(data:font/woff2;base64,' + b + ')')

data = {'core.json': json.load(open(T + '/data/core.json', encoding='utf-8'))}
for f in glob.glob(T + '/data/eprel/*.json'):
    data['eprel/' + os.path.basename(f)] = json.load(open(f, encoding='utf-8'))

engine = open(T + '/assets/js/engine.js', encoding='utf-8').read()
app = open(T + '/assets/js/app.js', encoding='utf-8').read()

router = r'''
window.PM_DEFER = true;
window.PM_CFG = {data: 'data/', ver: 'p', home: %(H)s, page: '', contactMail: 'rabarvo@hotmail.com'};
(function () {
  var H = %(H)s, DBLOB = "%(DBLOB)s", SH = %(BLOB)s, BOUNDS = %(BOUNDS)s, NSH = SH.length, CACHE = {}, PAGES = true, DATA = null, DATAP = null;
  var of = window.fetch;
  window.fetch = function (u, o) {
    u = String(u).split('?')[0];
    if (u.indexOf('data/') === 0) {
      var k = u.slice(5);
      if (!DATAP) DATAP = unpack(DBLOB).then(function (d) { DATA = d; return d; });
      return DATAP.then(function (D) {
        return D[k] ? new Response(JSON.stringify(D[k]), {headers: {'Content-Type': 'application/json'}}) : new Response('[]', {status: 404});
      });
    }
    return of(u, o);
  };
  function unpack(b64) {
    var bin = Uint8Array.from(atob(b64 || BLOB), function (c) { return c.charCodeAt(0); });
    var ds = new DecompressionStream('gzip');
    return new Response(new Blob([bin]).stream().pipeThrough(ds)).text().then(JSON.parse);
  }
  function current() {
    var q = new URLSearchParams(location.search);
    return q.get('p') || '/';
  }
  function markNav(path) {
    document.querySelectorAll('.nav [aria-current]').forEach(function (a) { a.removeAttribute('aria-current'); });
    var sel = null;
    if (path === '/') sel = '.nav > a:nth-of-type(1)';
    else if (/^\/(rehvi-valimine|vordle-rehve)\//.test(path)) sel = '.dd-btn';
    else if (/^\/testid\//.test(path)) sel = '.nav > a[href$="/testid/"]';
    else if (/^\/rehvid\//.test(path)) sel = '.nav > a[href$="/rehvid/"]';
    else if (/^\/teadmine\//.test(path)) sel = '.nav > a[href$="/teadmine/"]';
    var el = sel && document.querySelector(sel);
    if (el) el.setAttribute('aria-current', 'page');
  }
  /* kahendotsing: kumma killu vahemikku see aadress jääb */
  function shardOf(u) {
    var lo = 0, hi = BOUNDS.length - 1;
    while (lo < hi) { var mid = (lo + hi + 1) >> 1; if (BOUNDS[mid] <= u) lo = mid; else hi = mid - 1; }
    return lo;
  }
  function shard(n) { if (!CACHE[n]) CACHE[n] = unpack(SH[n]); return CACHE[n]; }
  function getPage(path) {
    return shard(shardOf(path)).then(function (s) { return s[path] || shard(shardOf('__404')).then(function (e) { return e['__404']; }); });
  }
  var seq = 0;
  function render(path, keepScroll) {
    var my = ++seq;
    getPage(path).then(function (pg) { if (my === seq) show(pg, path, keepScroll); });
  }
  function show(pg, path, keepScroll) {
    var main = document.getElementById('sisu');
    main.innerHTML = pg.m;
    document.title = pg.t;
    markNav(path);
    document.querySelectorAll('.dd.open').forEach(function (d) { d.classList.remove('open'); });
    var pm = document.getElementById('pm-panel'); if (pm) pm.hidden = true;
    if (!keepScroll) window.scrollTo(0, 0);
    if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }
    if (window.PM) window.PM.initPage();
  }
  function go(href) {
    var rest = href.slice(H.length), parts = rest.split('#'), pq = parts[0].split('?');
    var path = '/' + pq[0];
    if (path !== '/' && path.slice(-1) !== '/') path += '/';
    var qs = 'p=' + encodeURIComponent(path) + (pq[1] ? '&' + pq[1] : '');
    try { history.pushState(null, '', '?' + qs + (parts[1] ? '#' + parts[1] : '')); } catch (err) { /* liivakastis võib keelatud olla */ }
    render(path);
  }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey) return;
    var a = e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (href.indexOf(H) !== 0) return;
    e.preventDefault();
    go(href);
  });
  /* app.js suunab mõnikord ise (location.href = …) — püüame need kinni */
  var assign = function (u) { if (String(u).indexOf(H) === 0) go(String(u)); else location.assign(u); };
  window.PM_NAV = assign;
  window.addEventListener('popstate', function () { if (PAGES) render(current(), true); });
  document.addEventListener('DOMContentLoaded', function () {
    if (!('DecompressionStream' in window)) {
      document.getElementById('sisu').innerHTML = '<div class="wrap" style="padding:60px 16px"><p>See brauser on eelvaate jaoks liiga vana. Proovi Chrome\'i, Safari 16.4+ või Firefoxi.</p></div>';
      return;
    }
    render(current(), true);
  });
})();
''' % {'H': json.dumps(H), 'DBLOB': base64.b64encode(gzip.compress(json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode(), 9)).decode(), 'BLOB': blob, 'BOUNDS': bounds_js}

extra = '''
.pv-bar{background:#ffc20e;color:#171200;font:600 13px/1.4 Inter,system-ui,sans-serif;text-align:center;padding:7px 16px}
.site-header{top:env(safe-area-inset-top,0px)}
body{background:#fff}
#sisu:empty{min-height:80vh;background:#050506}
.fb-fab{position:fixed;right:16px;bottom:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:60;background:#ffc20e;color:#171200;border:0;border-radius:999px;padding:12px 18px;font:700 14px/1 Inter,system-ui,sans-serif;cursor:pointer;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.fb-fab:hover{filter:brightness(1.05)}
.fb-ovl{position:fixed;inset:0;z-index:70;background:rgba(5,5,6,.55);display:flex;align-items:flex-end;justify-content:center;padding:16px}
.fb-ovl[hidden]{display:none}
.fb-box{background:#fff;color:#171200;border-radius:16px;max-width:560px;width:100%;max-height:calc(100vh - 32px);overflow:auto;padding:22px;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.fb-box h2{font:800 22px/1.2 Inter,system-ui,sans-serif;margin:0 0 8px}
.fb-box p{font:400 14px/1.5 Inter,system-ui,sans-serif;margin:0 0 12px;color:#4a4a52}
.fb-l{display:block;font:600 13px/1.4 Inter,system-ui,sans-serif;margin:16px 0 6px}
.fb-in{width:100%;font:400 14px/1.5 Inter,system-ui,sans-serif;padding:10px;border:1px solid #d9d9de;border-radius:10px;background:#fff;color:#171200;resize:vertical}
.fb-in:focus{outline:2px solid #ffc20e;outline-offset:1px}
.fb-mono{font:400 12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:#f6f6f8;margin-top:8px}
.fb-alt{font:400 13px/1.5 Inter,system-ui,sans-serif;margin:14px 0 0;color:#6b6b73}
.fb-alt a{color:#171200}
.fb-box details{margin:12px 0 0;font:400 13px/1.5 Inter,system-ui,sans-serif}
.fb-box details pre{white-space:pre-wrap;word-break:break-word;background:#f6f6f8;border-radius:10px;padding:12px;margin:8px 0 0;max-height:240px;overflow:auto;font:400 12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}
.fb-actions{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 0}
.fb-b{font:700 14px/1 Inter,system-ui,sans-serif;padding:12px 16px;border-radius:999px;border:1px solid #d9d9de;background:#fff;color:#171200;cursor:pointer;text-decoration:none}
.fb-b.y{background:#ffc20e;border-color:#ffc20e}
.fb-msg{font:600 13px/1.5 Inter,system-ui,sans-serif;margin:12px 0 0;min-height:20px}
@media (min-width:700px){.fb-ovl{align-items:center}}
@media (max-width:640px){.fb-fab{padding:11px 15px;font-size:13px}}
'''
fbjs = r"""
/* TAGASISIDE EELVAATES. Nupp avab paneeli. Paneelis on Pagelive'i oma
   vorm (<form data-pagelive>) — selle saadab Pagelive ise, meie JS ei
   saada kuhugi midagi. Meie ainus tegevus: taidame "teekond" valja
   kasutaja enda kasutuslooga (window.PM.lugu()), et vastusega tuleks
   kaasa see, MIDA ta lehel tegi. */
(function () {
  function $(s) { return document.querySelector(s); }
  function ovl() { return $('.fb-ovl'); }
  function lugu() { try { return (window.PM && window.PM.lugu && window.PM.lugu()) || null; } catch (e) { return null; } }

  function ava() {
    var L = lugu();
    var t = $('[data-fb-teekond]');
    if (t) t.value = L ? L.tekst : '(kasutaja ei jõudnud midagi teha)';
    $('[data-fb-sum]').textContent = L
      ? ('Vastusega tuleb kaasa sinu teekond: ' + L.sammud + ' sammu, ~' + L.min + ' min.')
      : 'Teekond on veel tühi — vaata enne paar lehte ja arvuta midagi.';
    $('[data-fb-cnt]').textContent = L ? (L.sammud + ' sammu') : 'tühi';
    ovl().hidden = false;
    document.body.style.overflow = 'hidden';
    var k = $('[data-fb-txt]'); if (k) k.focus();
  }
  function sulge() { ovl().hidden = true; document.body.style.overflow = ''; }

  document.addEventListener('click', function (e) {
    if (e.target.closest('.fb-fab')) { e.preventDefault(); ava(); return; }
    if (e.target.closest('[data-fb-close]') || e.target === ovl()) sulge();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && ovl() && !ovl().hidden) sulge(); });
})();
"""

fbhtml = ('<button type="button" class="fb-fab">Anna tagasisidet</button>'
          '<div class="fb-ovl" hidden role="dialog" aria-modal="true" aria-label="Tagasiside">'
          '<div class="fb-box">'
          '<h2>Kuidas läks?</h2>'
          '<p>See on testversioon. Ütle paari lausega, mis töötas ja mis mitte. Vastusega tuleb kaasa ka see, '
          'mida sa lehel tegid — ilma nime ja muude isikuandmeteta.</p>'
          '<form data-pagelive data-pagelive-success="✓ Aitäh! Tagasiside on kohal.">'
          '<label class="fb-l" for="fb-hinnang">Kuidas läks?</label>'
          '<select class="fb-in" id="fb-hinnang" name="hinnang">'
          '<option>Sain tehtud, mida tahtsin</option>'
          '<option>Sain tehtud, aga midagi oli segane</option>'
          '<option>Ei leidnud oma autot või mõõtu</option>'
          '<option>Tulemus tundus kahtlane</option>'
          '<option>Midagi oli katki</option>'
          '</select>'
          '<label class="fb-l" for="fb-txt">Mis täpsemalt?</label>'
          '<textarea class="fb-in" id="fb-txt" name="kommentaar" data-fb-txt rows="4" '
          'placeholder="Näiteks: ei leidnud oma auto aastakäiku; number tundus talvel liiga suur; telefonis oli tabel kitsas…"></textarea>'
          '<label class="fb-l" for="fb-nimi">Nimi või kontakt <span style="font-weight:400;color:#6b6b73">(valikuline)</span></label>'
          '<input class="fb-in" id="fb-nimi" name="nimi" type="text" placeholder="kui tahad vastust">'
          '<p class="fb-msg" data-fb-sum style="color:#4a4a52;font-weight:400"></p>'
          '<details><summary>Näita, mis kaasa läheb (<span data-fb-cnt></span>)</summary>'
          '<textarea class="fb-in fb-mono" name="teekond" data-fb-teekond rows="10" readonly></textarea></details>'
          '<div class="fb-actions">'
          '<button type="submit" class="fb-b y">Saada tagasiside →</button>'
          '<button type="button" class="fb-b" data-fb-close>Sulge</button>'
          '</div>'
          '</form>'
          + ('<p class="fb-alt">Eelistad pikemat küsitlust? <a href="' + TAGASISIDE_URL + '" target="_blank" rel="noopener">Ava see siit →</a></p>' if TAGASISIDE_URL else '')
          + '</div></div>')

out = f'''<title>Pidurdusmaa.ee eelvaade</title>
<meta name="color-scheme" content="light">
<style>{css}{extra}</style>
{fix(header)}
<main id="sisu"></main>
{fix(footer)}
{fbhtml}
<script>{router}</script>
<script>{engine}</script>
<script>{app}</script>
<script>{fbjs}</script>
'''
open(OUT, 'w', encoding='utf-8').write(out)
full = ('<!doctype html>\n<html lang="et">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex">\n'
        + out.replace('<header class="site-header">', '</head>\n<body>\n<header class="site-header">', 1) + '</body>\n</html>\n')
open('/mnt/user-data/outputs/pidurdusmaa-pagelive.html', 'w', encoding='utf-8').write(full)
print(OUT, len(out) // 1024, 'KB')
