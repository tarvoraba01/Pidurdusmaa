import adapter from '@sveltejs/adapter-node';

/* Node-server. Lehed on endiselt EELRENDERDATUD (prerender = true
   +layout.js-is): server annab need valmis HTML-failidena välja, aga
   nüüd on olemas ka päris server — kontaktivormi ja kasutusloo jaoks
   saab teha API-otspunkti, mida staatilisel saidil teha ei saanud. */
export default {
  kit: {
    adapter: adapter({ out: 'build', precompress: false }),
    prerender: {
      handleHttpError: 'fail',
      /* /liiklusohutus/#kiirus=70&… — aadressi lõpp on kalkulaatori olek,
         mitte lehe sees olev ankur. Muudel lehtedel on puuduv ankur viga. */
      handleMissingId: ({ path, id, message }) => {
        if (/^\/(ru\/|en\/)?liiklusohutus/.test(path) && id.includes('=')) return;
        throw new Error(message);
      },
      entries: ['*', '/ru/', '/en/', '/ru/rehvi-valimine/', '/en/rehvi-valimine/', '/ru/vordle-rehve/', '/en/vordle-rehve/', '/ru/liiklusohutus/', '/en/liiklusohutus/', '/ru/autod/', '/ru/teadmine/rehvivahetus/']
    }
  }
};
