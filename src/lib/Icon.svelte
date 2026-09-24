<script module>
	/* Joonikonid (inline SVG, currentColor). Ei ühtegi välist ikoonifonti. */
	export const PATHS = {
		wet: '<path d="M7 15a4 4 0 0 1-.6-7.96A5.5 5.5 0 0 1 17 8a3.5 3.5 0 0 1 .5 6.97"/><path d="M9 18l-1 2.5M13 18l-1 2.5M17 18l-1 2.5"/>',
		dry: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
		snow: '<path d="M12 2v20M4.5 6.5l15 11M19.5 6.5l-15 11"/><path d="m9.5 3.5 2.5 2 2.5-2M9.5 20.5l2.5-2 2.5 2"/>',
		ice: '<path d="M3 17h18"/><path d="M5 21h14"/><path d="m6 13 3-9 3 5 3-5 3 9"/>',
		gauge: '<path d="M4 17a8 8 0 1 1 16 0"/><path d="m12 17 4-5"/><circle cx="12" cy="17" r="1.2"/>',
		compare: '<rect x="3" y="4" width="7" height="16" rx="1.5"/><rect x="14" y="4" width="7" height="16" rx="1.5"/><path d="M6.5 9h0M17.5 9h0"/>',
		info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
		speed: '<path d="M3 12h11"/><path d="M3 7h7"/><path d="M3 17h7"/><path d="m15 6 6 6-6 6"/>',
		road: '<path d="M5 21 9 3M19 21 15 3M12 5v2M12 11v2M12 17v2"/>',
		tyre: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v5M12 16v5M3 12h5M16 12h5"/>',
		temp: '<path d="M10 14.5V5a2 2 0 1 1 4 0v9.5a4 4 0 1 1-4 0Z"/>',
		car: '<path d="M5 17h14v-4l-2-5H7l-2 5v4Z"/><circle cx="8" cy="17" r="2"/><circle cx="16" cy="17" r="2"/>',
		wear: '<path d="M4 20V10M9 20V6M14 20v-8M19 20V4"/>',
		test: '<path d="M9 3h6M10 3v6L5 19a1.5 1.5 0 0 0 1.3 2h11.4A1.5 1.5 0 0 0 19 19l-5-10V3"/>',
		shield: '<path d="M12 3 5 6v6c0 4.5 3 7.5 7 9 4-1.5 7-4.5 7-9V6l-7-3Z"/>',
		search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
		arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
		heart: '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10Z"/>',
		chev: '<path d="m6 9 6 6 6-6"/>',
		scale: '<path d="M12 4v16M7 20h10M5 7h14M5 7l-3 6a3 3 0 0 0 6 0L5 7ZM19 7l-3 6a3 3 0 0 0 6 0l-3-6Z"/>',
		target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5.5"/><circle cx="12" cy="12" r="2"/>',
		check: '<path d="m5 12 4.5 4.5L19 7"/>',
		menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
		close: '<path d="M6 6l12 12M18 6 6 18"/>'
	};
</script>

<script>
	let { name, cls = '' } = $props();
</script>

{#if PATHS[name]}
	<svg
		class={cls}
		viewBox="0 0 24 24"
		fill="none"
		stroke="currentColor"
		stroke-width="1.8"
		stroke-linecap="round"
		stroke-linejoin="round"
		aria-hidden="true">{@html PATHS[name]}</svg
	>
{/if}
