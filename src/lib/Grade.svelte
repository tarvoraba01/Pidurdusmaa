<script>
	/* Märgise klass A–E ühtse märgina. */
	let { g } = $props();
	const ok = $derived(typeof g === 'string' && /^[A-E]$/.test(g));
</script>

{#if ok}<span class="gr {g}" aria-label="klass {g}">{g}</span>{:else}<span class="gr x">–</span>{/if}
