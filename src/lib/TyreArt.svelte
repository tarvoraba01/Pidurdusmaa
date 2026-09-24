<script>
	/* Neutraalne rehvijoonis — tootjate pilte ei kasutata (autoriõigus). */
	const tread = Array.from(
		{ length: 36 },
		(_, i) =>
			`<rect x="96" y="6" width="8" height="18" rx="2" fill="#2a2f38" transform="rotate(${i * 10} 100 100)"/>`
	).join('');
</script>

<svg viewBox="0 0 200 200" aria-hidden="true">
	<circle cx="100" cy="100" r="92" fill="#14171c" />
	{@html tread}
	<circle cx="100" cy="100" r="70" fill="#0d0f13" stroke="#232730" stroke-width="3" />
	<circle cx="100" cy="100" r="46" fill="#1b1f26" stroke="#3a404b" stroke-width="2" />
	<circle cx="100" cy="100" r="10" fill="#0d0f13" />
	<path
		d="M100 54v20M100 126v20M54 100h20M126 100h20M67 67l14 14M119 119l14 14M67 133l14-14M119 81l14-14"
		stroke="#3a404b"
		stroke-width="6"
		stroke-linecap="round"
	/>
	<path
		d="M30 100a70 70 0 0 1 32-59"
		stroke="#ffc20e"
		stroke-width="4"
		fill="none"
		stroke-linecap="round"
	/>
</svg>
