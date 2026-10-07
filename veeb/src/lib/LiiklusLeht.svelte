<script>
	/* Liiklusohutuse tööriistade ühine leht: hero, kalkulaator (vaade) ja infoplokk. */
	import Liiklus from '$lib/Liiklus.svelte';
	import Reaktsioon from '$lib/Reaktsioon.svelte';
	import RehviVanus from '$lib/RehviVanus.svelte';
	import RehviMoot from '$lib/RehviMoot.svelte';
	import Koolitus from '$lib/Koolitus.svelte';
	let { kick, h1, lead, vaade = 'peatumine', andmed = null, children } = $props();
</script>

<section class="lo-hero">
	<div class="wrap">
		<p class="lo-kick">{kick}</p>
		<h1>{h1}</h1>
		<p>{lead}</p>
	</div>
</section>

<section class="lo-bg">
	<div class="wrap">
		{#if vaade === 'reaktsioon'}<Reaktsioon />{:else if vaade === 'koolitus'}<Koolitus />{:else if vaade === 'vanus'}<RehviVanus />{:else if vaade === 'moot'}<RehviMoot moodud={andmed || []} />{:else}<Liiklus {vaade} />{/if}
	</div>
</section>

{#if children}
	<section class="lo-info">
		<div class="wrap lo-cols">
			{@render children()}
		</div>
	</section>
{/if}

<style>
	.lo-hero {
		background: var(--ink);
		color: var(--on-d);
		padding: var(--sp-10) 0 var(--sp-8);
	}
	.lo-kick {
		color: var(--yellow);
		font-weight: 700;
		font-size: 13px;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		margin: 0 0 var(--sp-3);
	}
	.lo-hero h1 {
		font-family: var(--display);
		font-weight: 700;
		font-size: clamp(40px, 5.4vw, 68px);
		line-height: 0.95;
		text-transform: uppercase;
		margin: 0 0 var(--sp-3);
		text-wrap: balance;
	}
	:global(:lang(ru)) .lo-hero h1 {
		font-size: clamp(28px, 7.4vw, 60px);
	}
	.lo-hero p:last-child {
		color: #cfd4db;
		font-size: 18px;
		max-width: 760px;
		margin: 0;
	}
	.lo-bg {
		background: var(--paper-2);
	}
	.lo-info {
		background: #fff;
		padding: var(--sp-10) 0 var(--sp-12);
		border-top: 1px solid var(--line);
	}
	.lo-cols {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: var(--sp-8);
	}
	@media (max-width: 900px) {
		.lo-cols {
			grid-template-columns: 1fr;
		}
	}
	.lo-info :global(h2) {
		font-family: var(--display);
		font-weight: 700;
		text-transform: uppercase;
		font-size: 26px;
		margin: 0 0 var(--sp-3);
	}
	.lo-info :global(ul) {
		padding-left: 18px;
		margin: 0;
		display: grid;
		gap: var(--sp-2);
	}
	.lo-info :global(p) {
		max-width: 65ch;
	}
	:global(.lo-src) {
		font-size: 14.5px;
	}
	:global(.lo-small) {
		font-size: 14px;
		color: var(--muted);
	}
</style>
