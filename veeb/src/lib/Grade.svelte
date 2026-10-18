<script>
	/* Märgise klass A–E ühtse märgina. */
	import { useT } from '$lib/i18n.js';
	const t = useT();
	let { g } = $props();
	const ok = $derived(typeof g === 'string' && /^[A-E]$/.test(g));
</script>

{#if ok}<span class="gr {g}" aria-label={t('klass {g}', { g })}>{g}</span>{:else}<span class="gr x">–</span>{/if}
