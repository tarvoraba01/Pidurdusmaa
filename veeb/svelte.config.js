import adapter from '@sveltejs/adapter-node';

/* Node-server. Lehed on endiselt EELRENDERDATUD (prerender = true
   +layout.js-is): server annab need valmis HTML-failidena välja, aga
   nüüd on olemas ka päris server — kontaktivormi ja kasutusloo jaoks
   saab teha API-otspunkti, mida staatilisel saidil teha ei saanud. */
export default {
  kit: {
    adapter: adapter({ out: 'build', precompress: false }),
    /* CSP ilma 'unsafe-inline'-ita skriptidele: SvelteKit paneb igale
       eelrenderdatud lehele <meta http-equiv="content-security-policy"> koos
       lehe käivitusskripti räsiga. server.js päis jääb alles (seal on muud
       direktiivid); brauser rakendab mõlemat, nii et inline-skript peab
       läbima ka selle räsikontrolli. Kaks räsi = app.html-i kaks skripti
       (PWA paigaldus, Plausible). Kui muudad neid, arvuta räsi uuesti:
       printf '%s' '<skripti sisu>' | openssl dgst -sha256 -binary | base64 */
    csp: {
      mode: 'hash',
      directives: {
        'script-src': [
          'self',
          'sha256-FkjI0LQ6vqJoH55Y9VqBo+5PndeVrCv3kBPEKdLQaik=',
          'sha256-S46PoNSIlqlHWn5jWqs3zz9yXx6Zq5efyOQb01rgaLs=',
          'https://www.googletagmanager.com',
          'https://challenges.cloudflare.com',
          'https://track.pidurdusmaa.ee'
        ]
      }
    },
    prerender: {
      handleHttpError: 'fail',
      /* /liiklusohutus/#kiirus=70&… — aadressi lõpp on kalkulaatori olek,
         mitte lehe sees olev ankur. Muudel lehtedel on puuduv ankur viga. */
      handleMissingId: ({ path, id, message }) => {
        if (/^\/(ru\/|en\/)?liiklusohutus/.test(path) && id.includes('=')) return;
        throw new Error(message);
      },
      entries: ['*', '/ru/', '/en/', '/ru/rehvi-valimine/', '/en/rehvi-valimine/', '/ru/vordle-rehve/', '/en/vordle-rehve/', '/ru/liiklusohutus/', '/en/liiklusohutus/', '/ru/liiklusohutus/pimedas/', '/en/liiklusohutus/pimedas/', '/ru/liiklusohutus/pikivahe/', '/en/liiklusohutus/pikivahe/', '/ru/liiklusohutus/kurv/', '/en/liiklusohutus/kurv/', '/ru/autod/', '/ru/liiklusohutus/koolitus/', '/ru/liiklusohutus/koolitus/tulemused/', '/ru/teadmine/rehvivahetus/', '/ru/kontakt/', '/en/kontakt/', '/ru/kasutustingimused/', '/en/kasutustingimused/', '/ru/privaatsus/', '/en/privaatsus/']
    }
  }
};
