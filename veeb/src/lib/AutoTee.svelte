<script>
	/* Ostutee: simulaatorite ja artiklite lõpus „sinu auto rehvid“.
	   Kirjutad auto → autoleht (rehvimõõt, rehvide pidurdusmaa, poodide hinnad).
	   Autode nimekiri (/api/autod.json) laetakse alles esimesel klõpsul. */
	import { useT, useLang, autoNimi } from '$lib/i18n.js';
	let { koht = '' } = $props();
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	const kuu = new Date().getMonth() + 1;
	const talv = kuu >= 10 || kuu <= 3;

	let q = $state('');
	let koik = $state(null);
	let laeb = false;
	let otsitud = false;
	function tr(e, v) {
		try {
			window.PM_TRACK && window.PM_TRACK(e, v);
		} catch {
			/* logi pole oluline */
		}
	}
	async function lae() {
		if (koik || laeb) return;
		laeb = true;
		try {
			koik = await (await fetch('/api/autod.json')).json();
		} catch {
			laeb = false;
		}
	}
	const lihtne = (x) => String(x || '').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
	const tulemus = $derived.by(() => {
		const sonad = lihtne(q).split(' ').filter(Boolean);
		if (!sonad.length || !koik) return null;
		return koik
			.filter((p) => {
				const hay = ' ' + lihtne(p.n) + ' ';
				return sonad.every((w) => (/^\d{4}$/.test(w) ? p.a0 && +w >= p.a0 && +w <= (p.a1 || 9999) : hay.includes(' ' + w)));
			})
			.slice(0, 8);
	});
	function sisestus() {
		lae();
		if (!otsitud && q.trim().length >= 2) {
			otsitud = true;
			tr('tee_otsing', koht);
		}
	}
</script>

<section class="at" aria-labelledby="at-h" data-lm="0">
	<div class="wrap at-sisu">
		<div class="at-tekst">
			<p class="at-kick">{t('Rehvid sinu autole')}</p>
			<h2 id="at-h">{talv ? t('Millised talverehvid sinu autole?') : t('Millised suverehvid sinu autole?')}</h2>
			<p>{t('Kirjuta auto mark ja mudel. Näed oma auto rehvimõõtu, rehvide pidurdusmaad ja poodide hindu.')}</p>
		</div>
		<div class="at-otsi">
			<input
				class="lsel"
				type="search"
				bind:value={q}
				onfocus={lae}
				oninput={sisestus}
				placeholder={t('Nt Golf 2015, Passat B6, Octavia')}
				aria-label={t('Otsi autot')}
				autocomplete="off"
			/>
			{#if tulemus}
				{#if tulemus.length}
					<ul class="at-tul">
						{#each tulemus as p (p.u)}
							<li>
								<a href={L(p.u)} onclick={() => tr('tee_auto', koht + ' · ' + p.n)}>
									<span class="n">{autoNimi(keel.lang, p.n)}</span><span class="m">{p.m}</span><span aria-hidden="true">→</span>
								</a>
							</li>
						{/each}
					</ul>
				{:else}
					<p class="at-ei">{t('Sellist autot ei leidnud. Proovi ainult margi või mudeli nime.')}</p>
				{/if}
			{/if}
			<p class="at-lingid">
				{#if talv}<a href={L('/talverehvid/')} onclick={() => tr('tee_link', koht + ' · talverehvid')}>{t('Talverehvid mõõdu järgi')} →</a>{/if}
				<a href={L('/autod/')} onclick={() => tr('tee_link', koht + ' · autod')}>{t('Kõik autod')} →</a>
			</p>
		</div>
	</div>
</section>

<style>
	.at {
		background: var(--ink);
		color: var(--on-d);
		padding: var(--sp-10) 0;
		border-top: 4px solid var(--yellow);
	}
	.at-sisu {
		display: grid;
		grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
		gap: var(--sp-8);
		align-items: start;
	}
	.at-kick {
		color: var(--yellow);
		font-weight: 700;
		font-size: 13px;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		margin: 0 0 var(--sp-2);
	}
	.at h2 {
		font-family: var(--display);
		font-weight: 700;
		text-transform: uppercase;
		font-size: clamp(30px, 3.6vw, 44px);
		line-height: 1;
		margin: 0 0 var(--sp-3);
		text-wrap: balance;
	}
	.at-tekst p:last-child {
		color: #cfd4db;
		font-size: 17px;
		margin: 0;
		max-width: 48ch;
	}
	.at-otsi input {
		width: 100%;
		height: 56px;
		font-size: 17px;
		background-image: none;
	}
	.at-tul {
		list-style: none;
		margin: var(--sp-3) 0 0;
		padding: 0;
		display: grid;
		gap: 6px;
	}
	.at-tul a {
		display: flex;
		gap: var(--sp-3);
		align-items: baseline;
		padding: 12px 14px;
		border-radius: var(--r);
		background: var(--ink-3);
		border: 1px solid var(--line-d);
		color: #fff;
		text-decoration: none;
	}
	.at-tul a:hover,
	.at-tul a:focus-visible {
		border-color: var(--yellow);
	}
	.at-tul .n {
		flex: 1;
		font-weight: 600;
	}
	.at-tul .m {
		color: #aab1bb;
		font-size: 14px;
		white-space: nowrap;
	}
	.at-ei {
		color: #cfd4db;
		margin: var(--sp-3) 0 0;
	}
	.at-lingid {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp-5);
		margin: var(--sp-4) 0 0;
		font-size: 15px;
	}
	.at-lingid a {
		color: var(--yellow);
		text-decoration: none;
		font-weight: 600;
	}
	.at-lingid a:hover {
		text-decoration: underline;
	}
	@media (max-width: 860px) {
		.at-sisu {
			grid-template-columns: 1fr;
			gap: var(--sp-5);
		}
	}
</style>
