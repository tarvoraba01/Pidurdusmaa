<script>
	/* Artikli rida: kes kirjutas ja millal viimati üle vaadati. */
	import { AUTOR_NIMI } from '$lib/seaded.js';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const L = useLang().L;
	let { uuendatud } = $props();
	const kp = $derived(String(uuendatud).split('-').reverse().join('.'));
</script>

<p class="byline">
	<a href={L('/meist/')}>{AUTOR_NIMI || 'Pidurdusmaa.ee'}</a> · {t('uuendatud')}
	<time datetime={uuendatud}>{kp}</time>
</p>
