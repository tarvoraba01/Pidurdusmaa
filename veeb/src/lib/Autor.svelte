<script>
	/* Artikli rida: kes kirjutas ja millal viimati üle vaadati. */
	import { AUTOR_NIMI } from '$lib/seaded.js';
	let { uuendatud } = $props();
	const kp = $derived(String(uuendatud).split('-').reverse().join('.'));
</script>

<p class="byline">
	<a href="/meist/">{AUTOR_NIMI || 'Pidurdusmaa.ee'}</a> · uuendatud
	<time datetime={uuendatud}>{kp}</time>
</p>
