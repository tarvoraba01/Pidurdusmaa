<script>
	/* Autolehe illustratsioon: lihtne külgvaade keretüübi järgi (oma joonis, mitte
	   tootja foto ega logo). Rehvid on esile tõstetud — leht räägib rehvidest.
	   keha: SOIDUAUTO | VAIKEAUTO | MAASTUR | KAUBIK (core.json vehicles[].body) */
	let { keha = 'SOIDUAUTO', moot = '' } = $props();

	/* kere kontuur, aknad, rataste asukoht ja raadius */
	const KUJU = {
		SOIDUAUTO: {
			kere: 'M24 118 L24 99 Q26 87 44 84 L104 78 L146 54 Q156 47 171 47 L254 47 Q268 47 279 54 L318 78 L356 84 Q374 87 376 102 L376 118 Q376 124 370 124 L30 124 Q24 124 24 118 Z',
			aknad: ['M120 78 L152 57 Q158 53 168 53 L206 53 L206 78 Z', 'M214 53 L252 53 Q262 53 270 58 L303 78 L214 78 Z'],
			rattad: [[96, 26], [306, 26]]
		},
		VAIKEAUTO: {
			kere: 'M44 118 L44 98 Q46 86 62 83 L108 78 L142 52 Q151 45 165 45 L262 45 Q280 45 290 58 L322 84 Q340 90 342 104 L342 118 Q342 124 336 124 L50 124 Q44 124 44 118 Z',
			aknad: ['M122 78 L148 57 Q154 51 164 51 L204 51 L204 78 Z', 'M212 51 L258 51 Q272 51 280 62 L302 82 L212 82 Z'],
			rattad: [[108, 24], [286, 24]]
		},
		MAASTUR: {
			kere: 'M24 116 L24 58 Q24 38 46 36 L288 36 Q302 36 310 44 L338 72 L364 78 Q378 82 378 98 L378 116 Q378 124 370 124 L32 124 Q24 124 24 116 Z',
			aknad: ['M42 68 L42 50 Q42 42 52 42 L118 42 L118 68 Z', 'M126 42 L206 42 L206 68 L126 68 Z', 'M214 42 L288 42 Q298 42 304 48 L324 68 L214 68 Z'],
			rattad: [[100, 30], [306, 30]]
		},
		KAUBIK: {
			kere: 'M22 116 L22 52 Q22 34 40 34 L262 34 Q286 34 300 46 L334 78 L362 84 Q378 88 378 104 L378 116 Q378 124 370 124 L30 124 Q22 124 22 116 Z',
			aknad: ['M276 42 Q290 42 298 52 L322 76 L276 76 Z'],
			rattad: [[92, 27], [312, 27]]
		}
	};
	const k = $derived(KUJU[keha] || KUJU.SOIDUAUTO);
	const MAA = 146;
</script>

<svg class="ap" viewBox="0 0 400 186" role="img" aria-label={moot ? 'Rehvimõõt ' + moot : 'Auto'}>
	<!-- vari -->
	<ellipse cx="200" cy={MAA + 4} rx="186" ry="7" fill="#000" opacity=".35" />
	<!-- kere: rattakoopad lõigatakse välja tausta värviga ringidega -->
	<g transform="translate(0 {MAA - k.rattad[0][1] - 124})">
		<path d={k.kere} fill="#e8ebf0" />
		<path d={k.kere} fill="url(#ap-varv)" />
		{#each k.aknad as a (a)}<path d={a} fill="#1b2029" />{/each}
		<!-- uksejoon ja tuled -->
		<path d="M210 {k.aknad[0].includes('L206') ? 80 : 70} L210 118" stroke="#c4c9d1" stroke-width="1.5" />
		<rect x={k.kere.startsWith('M44') ? 334 : 362} y="94" width="12" height="7" rx="3" fill="#ffc20e" />
		<rect x={k.kere.startsWith('M44') ? 46 : 24} y="96" width="8" height="7" rx="2" fill="#e5484d" />
		{#each k.rattad as [x, r] (x)}<circle cx={x} cy="124" r={r + 6} fill="var(--ink)" />{/each}
	</g>
	<defs>
		<linearGradient id="ap-varv" x1="0" y1="0" x2="0" y2="1">
			<stop offset="0" stop-color="#fff" stop-opacity=".35" />
			<stop offset=".55" stop-color="#fff" stop-opacity="0" />
			<stop offset="1" stop-color="#000" stop-opacity=".18" />
		</linearGradient>
	</defs>
	<!-- rattad: rehv must, velg kollase äärega -->
	{#each k.rattad as [x, r] (x)}
		<g>
			<circle cx={x} cy={MAA - r} r={r} fill="#0d0f13" />
			<circle cx={x} cy={MAA - r} r={r - 3} fill="none" stroke="#2b3039" stroke-width="2" stroke-dasharray="3 3" />
			<circle cx={x} cy={MAA - r} r={r * 0.6} fill="#3a404b" stroke="#ffc20e" stroke-width="3" />
			<circle cx={x} cy={MAA - r} r={r * 0.16} fill="#ffc20e" />
		</g>
	{/each}
	{#if moot}
		{@const [fx] = k.rattad[1]}
		<g class="ap-silt">
			<rect x={fx - 48} y={MAA + 12} width="96" height="24" rx="12" fill="#ffc20e" />
			<text data-ad-moot x={fx} y={MAA + 28.5} text-anchor="middle" font-size="13" font-weight="700" fill="#171200">{moot}</text>
		</g>
	{/if}
</svg>

<style>
	.ap { width: 100%; height: auto; display: block; overflow: visible; }
	.ap-silt text { font-family: var(--body, Inter, system-ui, sans-serif); }
</style>
