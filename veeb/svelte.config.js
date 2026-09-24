import adapter from '@sveltejs/adapter-static';

/** Staatiline sait: iga aadress eelrenderdatakse päris HTML-failiks.
 *  See on kogu mõte — Google peab nägema 5948 lehte, mitte üht. */
export default {
  kit: {
    adapter: adapter({ fallback: '404.html', precompress: false }),
    prerender: {
      handleHttpError: 'fail',
      entries: ['*']
    },
    paths: { relative: false }
  }
};
