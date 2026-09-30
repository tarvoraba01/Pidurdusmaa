<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { afterNavigate } from '$app/navigation';
	import { version } from '$app/environment';
	import Icon from '$lib/Icon.svelte';
	import Nousolek from '$lib/Nousolek.svelte';
	import { GA4_ID, GSC_VERIFY } from '$lib/seaded.js';
	import '$lib/main.css';

	let { children } = $props();

	/* Aktiivne menüüpunkt aadressi järgi — sama loogika, mis oli
	   pm_nav_current() PHP-poolel. */
	const cur = $derived.by(() => {
		const p = page.url.pathname;
		if (p === '/') return 'home';
		if (p.startsWith('/rehvi-valimine') || p.startsWith('/vordle-rehve')) return 'valik';
		/* rehvid, testid ja margid on menüüs Teadmine all */
		if (p.startsWith('/teadmine') || p.startsWith('/testid') || p.startsWith('/rehvid') || p.startsWith('/margid')) return 'teadmine';
		return '';
	});

	/* /liiklusohutus/ on neutraalne tööriist (kõigile; ka Transpordiamet, autokoolid):
	   ei menüüd, poode ega rehvivalikut — ainult logo ja õiguslikud lingid. */
	const neutraal = $derived(page.url.pathname.startsWith('/liiklusohutus'));

	onMount(async () => {
		/* Avalehel logo / „Pidurdusmaa“ peale vajutus = lehe värskendus
		   (tulemus ja valikud nullitakse, leht algusest). Mujal tavaline
		   kiire üleminek. Ctrl/Cmd-klõps (uus vaheleht) jääb puutumata. */
		document.addEventListener('click', (e) => {
			const a = e.target instanceof Element ? e.target.closest('a[href="/"]') : null;
			if (!a || location.pathname !== '/' || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
			e.preventDefault();
			e.stopPropagation();
			try { history.scrollRestoration = 'manual'; } catch {}
			window.scrollTo(0, 0);
			location.href = '/';
		}, true);
		window.PM_DEFER = true;
		window.PM_CFG = {
			data: '/data/',
			/* Andmefailide aadressi lõppu pannakse ehituse versioon
			   (core.json?v=…). Nii laeb brauser pärast igat deploy'd
			   uued andmed, mitte ei näita vahemälust vana autode nimekirja. */
			ver: version,
			home: '/',
			/* hinnad tulevad meie serverist (src/lib/server/integratsioonid) —
			   kui ühtki pakkujat pole sisse lülitatud, vastab see „pole saadaval“ */
			prices: '/api/hinnad',
			contact: '/api/kontakt',
			contactMail: 'rabarvo@hotmail.com',
			track: '/api/logi'
		};
		await import('$lib/engine.js');
		await import('$lib/app.js');
		window.PM?.initPage();
	});

	/* SPA-navigeerimisel ei tule DOMContentLoaded'i — käivitame ise.
	   Esimese laadimise ('enter') lehevaate saadab Nousolek ise, siin
	   ainult järgmised, muidu loeks GA esimest lehte kaks korda. */
	afterNavigate(({ type }) => {
		if (typeof window === 'undefined') return;
		window.PM?.initPage();
		if (type !== 'enter') window.PM_LEHEVAADE?.();
	});
</script>

<svelte:head>
	{#if GSC_VERIFY}<meta name="google-site-verification" content={GSC_VERIFY} />{/if}
</svelte:head>

<a class="skip" href="#sisu">Liigu sisu juurde</a>

{#if neutraal}
<header class="site-header">
	<div class="wrap">
		<a class="logo" href="/" aria-label="Pidurdusmaa.ee avaleht"><b>PIDURDUSMAA</b><em>.ee</em></a>
		<span class="neutraal-silt">Liiklusohutus</span>
	</div>
</header>
{:else}
<header class="site-header">
	<div class="wrap">
		<a class="logo" href="/" aria-label="Pidurdusmaa.ee avaleht"><b>PIDURDUSMAA</b><em>.ee</em></a>
		<nav class="nav" aria-label="Peamenüü">
			<a href="/" aria-current={cur === 'home' ? 'page' : undefined}>Pidurdusmaa</a>
			<div class="dd" data-dd>
				<button
					type="button"
					class="dd-btn"
					aria-expanded="false"
					aria-haspopup="true"
					aria-current={cur === 'valik' ? 'page' : undefined}
					>Rehvi valimine <Icon name="chev" /></button
				>
				<div class="dd-menu" role="menu">
					<a role="menuitem" href="/rehvi-valimine/"
						><b>Vali rehv enda tingimustele</b><span>Mis on sulle oluline — näitame sobivaid</span></a
					>
					<a role="menuitem" href="/vordle-rehve/"
						><b>Võrdle rehve kõrvuti</b><span>2–4 rehvi ühes tabelis</span></a
					>
				</div>
			</div>
			<a href="/teadmine/" aria-current={cur === 'teadmine' ? 'page' : undefined}>Teadmine</a>
		</nav>
		<div class="hdr-right">
			<a class="cmp-link" href="/vordle-rehve/" data-cmp-pill>
				<Icon name="heart" /><span>Võrdlus (<span data-cmp-n>0</span>)</span>
			</a>
			<button
				class="burger"
				type="button"
				aria-controls="pm-panel"
				aria-expanded="false"
				aria-label="Menüü"
				data-burger><Icon name="menu" /></button
			>
		</div>
	</div>
	<div class="panel-menu" id="pm-panel" hidden>
		<div class="wrap">
			<div class="pm-cols">
				<div>
					<h4>Pidurdusmaa</h4>
					<a href="/">Pidurdusmaa kalkulaator</a>
					<a href="/teadmine/pidurdusteekond-ja-peatumisteekond/">Pidurdus- ja peatumisteekond</a>
					<a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas arvutatakse</a>
					<a href="/liiklusohutus/">Liiklusohutuse kalkulaator</a>
				</div>
				<div>
					<h4>Rehvi valimine</h4>
					<a href="/rehvi-valimine/">Vali rehv enda tingimustele</a>
					<a href="/vordle-rehve/">Võrdle rehve kõrvuti</a>
				</div>
				<div>
					<h4>Andmed</h4>
					<a href="/rehvid/">Rehvid</a>
					<a href="/testid/">Sõltumatud testid</a>
					<a href="/teadmine/">Teadmine</a>
					<a href="/teadmine/artiklid/">Artiklid</a>
					<a href="/teadmine/rehvimargis/">EL-i rehvimärgis</a>
					<a href="/kontakt/">Kontakt</a>
				</div>
			</div>
		</div>
	</div>
</header>
{/if}

<main id="sisu">{@render children()}</main>

<footer class="site-footer">
	<div class="wrap">
		{#if !neutraal}
		<div class="ft">
			<div>
				<a class="logo" href="/"><b>PIDURDUSMAA</b><em>.ee</em></a>
				<p>
					Sa ei pea teadma, milline rehv on hea. Näitame, kuidas need erinevad — päris andmete
					järgi, ja ütleme otse, kui andmeid ei ole.
				</p>
			</div>
			<div>
				<h4>Tööriistad</h4>
				<ul>
					<li><a href="/">Pidurdusmaa kalkulaator</a></li>
					<li><a href="/rehvi-valimine/">Rehvi valimine</a></li>
					<li><a href="/vordle-rehve/">Võrdle rehve</a></li>
					<li><a href="/liiklusohutus/">Liiklusohutuse kalkulaator</a></li>
				</ul>
			</div>
			<div>
				<h4>Andmed</h4>
				<ul>
					<li><a href="/rehvid/">Rehvid</a></li>
					<li><a href="/testid/">Sõltumatud testid</a></li>
					<li><a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas arvutatakse</a></li>
					<li><a href="/margid/">Rehvimargid</a></li>
					<li><a href="/teadmine/">Teadmine</a></li>
					<li><a href="/teadmine/artiklid/">Artiklid</a></li>
					<li><a href="/meist/">Meist</a></li>
					<li><a href="/teadmine/partnerid/">Partnerid</a></li>
					<li><a href="/kontakt/">Kontakt</a></li>
				</ul>
			</div>
			<div>
				<h4>Allikad</h4>
				<ul>
					<li>EL-i tooteregister EPREL</li>
					<li>ADAC, Tekniikan Maailma, UTAC, Vi Bilägare</li>
					<li>UNECE R117</li>
				</ul>
			</div>
		</div>
		{/if}
		<div class="ft-b">
			<span>© {new Date().getFullYear()} Rabarvo OÜ · {#if neutraal}<a href="/">Pidurdusmaa.ee</a> — rehvide pidurdusmaa sinu autoga{:else}Pidurdusmaa.ee{/if}</span>
			<span
				>Tulemused on arvutatud hinnangud — mitte mõõtmised ega garantii.
				<a href="/kasutustingimused/">Kasutustingimused ja vastutus</a> ·
				<a href="/privaatsus/">Privaatsus</a>{#if GA4_ID}
					·
					<button type="button" class="linkbtn" onclick={() => window.PM_KUPSISED?.()}
						>Küpsiste seaded</button
					>{/if}</span
			>
		</div>
	</div>
</footer>

<Nousolek />
