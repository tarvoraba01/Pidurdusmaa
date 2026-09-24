<script>
	/* Cloudflare Turnstile vidin kontaktivormi sees.
	   Skript laetakse AINULT sellel lehel ja ainult siis, kui avalik võti
	   on seatud (seaded.js). Vidin paneb vormi peidetud välja
	   "cf-turnstile-response", mille server Cloudflare'ilt üle kontrollib. */
	import { onMount } from 'svelte';
	import { TURNSTILE_SITEKEY } from '$lib/seaded.js';

	let el = $state();
	const SRC = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';

	function laeSkript() {
		if (window.turnstile) return Promise.resolve(window.turnstile);
		if (!window.__pmTurnstile) {
			window.__pmTurnstile = new Promise((ok, fail) => {
				const s = document.createElement('script');
				s.src = SRC;
				s.async = true;
				s.onload = () => ok(window.turnstile);
				s.onerror = () => {
					window.__pmTurnstile = null;
					fail(new Error('Turnstile ei laadinud'));
				};
				document.head.appendChild(s);
			});
		}
		return window.__pmTurnstile;
	}

	onMount(() => {
		if (!TURNSTILE_SITEKEY) return;
		let id = null;
		let elus = true;
		laeSkript()
			.then((ts) => {
				if (!elus || !el) return;
				id = ts.render(el, {
					sitekey: TURNSTILE_SITEKEY,
					language: 'et',
					theme: 'light',
					size: 'flexible',
					action: 'kontakt'
				});
				/* app.js tühjendab vidina pärast saatmist (luba on ühekordne) */
				el.closest('form')?.setAttribute('data-ts-id', id);
			})
			.catch(() => {
				if (el) el.textContent = 'Robotikontroll ei laadinud. Värskenda lehte või kirjuta otse e-postile.';
			});
		return () => {
			elus = false;
			if (id !== null && window.turnstile) window.turnstile.remove(id);
		};
	});
</script>

{#if TURNSTILE_SITEKEY}
	<div class="ts" bind:this={el}></div>
{/if}

<style>
	.ts {
		margin-top: var(--sp-4);
		min-height: 65px;
		font-size: 13.5px;
		color: var(--muted);
	}
</style>
