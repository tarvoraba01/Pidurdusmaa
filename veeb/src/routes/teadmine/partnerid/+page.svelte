<script>
	/* Partnerid — logosein: poed (hinnad rehvikaartidel) üleval suurelt, teised all.
	   Selgitus (kuidas leht tasuta püsib, mida see sulle tähendab) on partnerite järel. */
	import Meta from '$lib/Meta.svelte';
	import { PARTNERID } from '$lib/partnerid.js';
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;

	const domeen = (u) => {
		try {
			return new URL(u).hostname.replace(/^www\./, '');
		} catch {
			return '';
		}
	};
	const poed = PARTNERID.filter((p) => p.ryhm === 'pood');
	const teised = PARTNERID.filter((p) => p.ryhm !== 'pood');
	const PEALKIRI = 'Partnerid';
</script>

<Meta
	title={t(PEALKIRI)}
	desc={t('Rehvipoed, kelle hinnad ja laoseis on Pidurdusmaa rehvikaartidel, ja teised partnerid. Hind sinu jaoks ei muutu ja rehvide järjestust ei müüda.')}
	path="teadmine/partnerid/"
	crumbs={[[t('Avaleht'), '/'], [t('Teadmine'), '/teadmine/'], [t(PEALKIRI), '/teadmine/partnerid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/teadmine/')}>{t('Teadmine')}</a><span>/</span>{t(PEALKIRI)}
		</div>
		<h1>{t(PEALKIRI)}</h1>
	</div>
</section>

<div class="body-sec">
	<div class="wrap">
		{#snippet sein(list, suur)}
			<div class="ps-sein" class:ps-suur={suur} style="--n:{list.length}">
				{#each list as p (p.nimi)}
					<a class="ps-k" href={p.link} rel={p.tasuta ? 'noopener' : 'sponsored noopener'} target="_blank" data-partner={p.nimi}>
						<span class="ps-logo">
							{#if p.logo}<img src="/img/partnerid/{p.logo}" alt={p.nimi} loading="lazy" style={p.logoMaxH ? `max-height:${p.logoMaxH}px` : undefined} />{:else}<b>{p.nimi}</b>{/if}
						</span>
						<span class="ps-tekst">
							<span class="ps-dom">{domeen(p.link)}</span>
							{#if p.kirjeldus}<span class="ps-kirj">{t(p.kirjeldus)}</span>{/if}
						</span>
					</a>
				{/each}
			</div>
		{/snippet}

		<section class="ps-plokk" aria-labelledby="ps-poed">
			<div class="ps-pais">
				<h2 id="ps-poed">{t('Rehvipoed')}</h2>
				<p>{t('Nende hinnad ja laoseis on otse meie rehvikaartidel. Näed pidurdusmaad ja ostad samast kohast.')}</p>
			</div>
			{@render sein(poed, true)}
		</section>

		{#if teised.length}
			<section class="ps-plokk" aria-labelledby="ps-teised">
				<div class="ps-pais">
					<h2 id="ps-teised">{t('Teised partnerid')}</h2>
				</div>
				{@render sein(teised, false)}
			</section>
		{/if}

		<section class="ps-kuidas" aria-labelledby="ps-kuidas">
			<h2 id="ps-kuidas">{t('Kuidas leht tasuta püsib')}</h2>
			<p class="ps-lead">
				{t('Need ettevõtted aitavad Pidurdusmaal tasuta püsida. Rehvide juures olevad poelingid võivad olla partnerlingid: kui ostad lingi kaudu, võib pood maksta lehele väikese vahendustasu.')}
			</p>
			<ul class="ps-pohim">
				<li><b>{t('Hind ei muutu')}</b><span>{t('Sinu jaoks on hind sama, mis müüja enda lehel.')}</span></li>
				<li><b>{t('Järjestust ei müüda')}</b><span>{t('Pidurdusmaad ja järjestus tulevad ainult andmetest: EL-i rehvimärgis, sõltumatud testid ja arvutus. Hind loeb ainult siis, kui valid ise „Soodne hind“.')}</span></li>
				<li><b>{t('Kõik poed on võrdsed')}</b><span>{t('Ükski pood ei saa maksta, et tema rehv oleks eespool. Kaardil on poed hinna järgi, odavaim ees.')}</span></li>
			</ul>
			<p class="ps-legal">
				{@html t('Pidurdusmaa.ee (Rabarvo OÜ) võib saada vahendustasu ostudelt, mis tehakse lehe poelinkide kaudu. Poelingid on otsingumootoritele tähistatud (rel="sponsored"). Poodi minnes võib pood või partnervõrgustik salvestada sinu brauserisse küpsise, et ost lehega seostada; Pidurdusmaa.ee ise sinu ostu sisu ega isikuandmeid ei näe. Vt ka <a href="/kasutustingimused/">kasutustingimused</a> ja <a href="/privaatsus/">privaatsus</a>.')}
			</p>
		</section>
	</div>
</div>

<style>
	.ps-plokk { margin: 0 0 var(--sp-12); }
	.ps-pais { display: flex; align-items: baseline; gap: var(--sp-6); flex-wrap: wrap; margin-bottom: var(--sp-5); }
	.ps-pais h2 { font-family: var(--display); font-weight: 700; font-size: 30px; line-height: 1; text-transform: uppercase; margin: 0; }
	.ps-pais p { margin: 0; color: var(--muted); font-size: 16px; max-width: 60ch; }

	/* üks pind, sees juuksepeened jooned — mitte eraldi kaardid */
	.ps-sein {
		display: grid;
		grid-template-columns: repeat(var(--n), minmax(0, 1fr));
		border: 1px solid var(--line);
		border-radius: var(--r-lg);
		overflow: hidden;
		background: var(--line);
		gap: 1px;
	}
	.ps-k {
		display: flex;
		flex-direction: column;
		background: var(--paper);
		color: var(--text);
		text-decoration: none;
		transition: background-color 0.2s;
	}
	@media (hover: hover) { .ps-k:hover { background: #fffcf2; } }
	.ps-k:focus-visible { outline: 2px solid var(--yellow); outline-offset: -3px; }
	.ps-logo { flex: 1; display: grid; place-items: center; min-height: 150px; padding: var(--sp-8) var(--sp-8) var(--sp-4); }
	.ps-suur .ps-logo { min-height: 220px; padding: var(--sp-10) var(--sp-10) var(--sp-5); }
	.ps-logo img { display: block; width: auto; height: 52px; max-width: min(100%, 200px); object-fit: contain; }
	.ps-suur .ps-logo img { height: 72px; max-width: min(100%, 240px); }
	.ps-logo b { font-size: 26px; letter-spacing: -0.01em; }
	.ps-tekst { display: flex; flex-direction: column; gap: 2px; padding: 0 var(--sp-6) var(--sp-6); text-align: center; }
	.ps-dom { font-weight: 600; font-size: 15px; }
	.ps-k:hover .ps-dom { text-decoration: underline; text-underline-offset: 3px; text-decoration-color: var(--yellow); text-decoration-thickness: 2px; }
	.ps-kirj { color: var(--muted); font-size: 14px; line-height: 1.45; }

	.ps-kuidas { border-top: 1px solid var(--line); padding-top: var(--sp-10); }
	.ps-kuidas h2 { font-family: var(--display); font-weight: 700; font-size: 30px; line-height: 1; text-transform: uppercase; margin: 0 0 var(--sp-4); }
	.ps-lead { font-size: 18px; line-height: 1.55; max-width: 64ch; margin: 0 0 var(--sp-8); }
	.ps-pohim { list-style: none; padding: 0; margin: 0 0 var(--sp-8); max-width: 1040px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--sp-8); }
	.ps-pohim li { border-left: 3px solid var(--yellow); padding-left: var(--sp-4); }
	.ps-pohim b { display: block; font-size: 17px; margin-bottom: var(--sp-1); }
	.ps-pohim span { color: var(--muted); font-size: 15px; line-height: 1.5; }
	.ps-legal { font-size: 13px; color: var(--muted); line-height: 1.55; max-width: 80ch; margin: 0; }
	.ps-legal :global(a) { color: inherit; }

	@media (max-width: 860px) {
				.ps-suur { grid-template-columns: 1fr; }
		.ps-suur .ps-logo { min-height: 140px; padding: var(--sp-8) var(--sp-6) var(--sp-4); }
		.ps-suur .ps-logo img { height: 60px; }
		.ps-pohim { grid-template-columns: 1fr; gap: var(--sp-5); }
	}
	@media (max-width: 520px) {
		.ps-sein { grid-template-columns: 1fr; }
	}
	@media (prefers-reduced-motion: reduce) { .ps-k { transition: none; } }
</style>
