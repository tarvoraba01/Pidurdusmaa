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
      entries: ['*']
    }
  }
};
