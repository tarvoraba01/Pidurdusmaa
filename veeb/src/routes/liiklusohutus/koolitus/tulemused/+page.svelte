<script>
	/* Õpetaja tulemuste leht — privaatne (võti räsis), mitte otsingumootoritele. */
	import Meta from '$lib/Meta.svelte';
	import KoolitusTulemused from '$lib/KoolitusTulemused.svelte';
</script>

<Meta title="Koolitus: grupi tulemused" desc="Õpetaja vaade: grupi tulemused enne ja pärast koolitust." path="liiklusohutus/koolitus/tulemused/" noindex />

<section class="lo-bg" style="padding: var(--sp-8) 0">
	<div class="wrap"><h1 class="kt-h1">Grupi tulemused</h1><KoolitusTulemused /></div>
</section>

<style>
	.kt-h1 { max-width: 760px; margin: 0 auto var(--sp-4); font-family: var(--display); font-size: clamp(32px, 4.4vw, 48px); line-height: 1; text-transform: uppercase; }
</style>
