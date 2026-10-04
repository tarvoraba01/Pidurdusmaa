<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { afterNavigate, beforeNavigate } from '$app/navigation';
	import { setContext } from 'svelte';
	import { tr, langOf, baseOf, linkLang, onTolgitud, KEELED, KEEL_NIMI } from '$lib/i18n.js';
	import { version } from '$app/environment';
	import Icon from '$lib/Icon.svelte';
	import Nousolek from '$lib/Nousolek.svelte';
	import { GA4_ID, GSC_VERIFY } from '$lib/seaded.js';
	import '$lib/main.css';

	let { children, data } = $props();

	/* Keel tuleb aadressist (/ru/, /en/); sõnastiku laeb +layout.js */
	const lang = $derived(data?.lang || 'et');
	const dict = $derived(data?.dict || null);
	const t = (s) => tr(lang, dict, s);
	const L = (p) => linkLang(lang, p);
	setContext('i18n', {
		get lang() {
			return lang;
		},
		get dict() {
			return dict;
		}
	});
	const base = $derived(baseOf(page.url.pathname));
	/* keelevahetus: tõlgitud leht → sama leht teises keeles, muu → keele avaleht */
	/* aadressi päring (nt ?rehvid=…) läheb keelevahetusel kaasa; eelrenderdatud
	   lehel on see teada alles brauseris */
	let otsing = $state('');
	const keeleLink = (k) => (onTolgitud(k, base) ? linkLang(k, base) + otsing : '/' + k + '/');

	/* Aktiivne menüüpunkt aadressi järgi — sama loogika, mis oli
	   pm_nav_current() PHP-poolel. */
	const cur = $derived.by(() => {
		const p = base;
		if (p === '/') return 'home';
		if (p.startsWith('/rehvi-valimine') || p.startsWith('/vordle-rehve') || p.startsWith('/talverehvid')) return 'valik';
		/* rehvid, testid ja margid on menüüs Teadmine all */
		if (p.startsWith('/teadmine') || p.startsWith('/testid') || p.startsWith('/rehvid') || p.startsWith('/margid') || p.startsWith('/autod')) return 'teadmine';
		return '';
	});

	/* /liiklusohutus/ on neutraalne tööriist (kõigile; ka Transpordiamet, autokoolid):
	   ei menüüd, poode ega rehvivalikut — ainult logo ja õiguslikud lingid. */
	const neutraal = $derived(base.startsWith('/liiklusohutus'));

	onMount(async () => {
		/* Avalehel logo / „Pidurdusmaa“ peale vajutus = lehe värskendus
		   (tulemus ja valikud nullitakse, leht algusest). Mujal tavaline
		   kiire üleminek. Ctrl/Cmd-klõps (uus vaheleht) jääb puutumata. */
		document.addEventListener('click', (e) => {
			const kodu = linkLang(langOf(location.pathname), '/');
			const a = e.target instanceof Element ? e.target.closest('a[href="' + kodu + '"]') : null;
			if (!a || location.pathname !== kodu || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
			e.preventDefault();
			e.stopPropagation();
			try { history.scrollRestoration = 'manual'; } catch {}
			window.scrollTo(0, 0);
			location.href = kodu;
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
		/* app.js loeb tõlked ja keele käivitumisel (vt _t app.js-is) */
		window.PM_LANG = lang;
		window.PM_I18N = dict;
		window.PM_LINK = (p) => linkLang(lang, p);
		await import('$lib/engine.js');
		await import('$lib/app.js');
		window.PM?.initPage();
	});

	/* Keele vahetus = täielik lehe laadimine: app.js loeb keele ja tõlked
	   ainult korra, käivitumisel. Sama keele sees kiire üleminek. */
	beforeNavigate(({ to, cancel, willUnload }) => {
		if (willUnload || !to?.url || typeof window === 'undefined') return;
		if (to.url.origin !== location.origin) return;
		if (langOf(to.url.pathname) !== langOf(location.pathname)) {
			cancel();
			location.href = to.url.href;
		}
	});

	/* SPA-navigeerimisel ei tule DOMContentLoaded'i — käivitame ise.
	   Esimese laadimise ('enter') lehevaate saadab Nousolek ise, siin
	   ainult järgmised, muidu loeks GA esimest lehte kaks korda. */
	afterNavigate(({ type }) => {
		if (typeof window === 'undefined') return;
		otsing = location.search;
		window.PM?.initPage();
		if (type !== 'enter') window.PM_LEHEVAADE?.();
	});
</script>

<svelte:head>
	{#if GSC_VERIFY}<meta name="google-site-verification" content={GSC_VERIFY} />{/if}
</svelte:head>

<a class="skip" href="#sisu">{t("Liigu sisu juurde")}</a>

{#if neutraal}
<header class="site-header">
	<div class="wrap">
		{@html t("<a class=\"logo\" href=\"/\" aria-label=\"Pidurdusmaa.ee avaleht\"><b>PIDURDUSMAA</b><em>.ee</em></a> <span class=\"neutraal-silt\">Liiklusohutus</span>")}
		<nav class="keeled" aria-label={t("Keel")}>{#each KEELED as k (k)}<a href={keeleLink(k)} onclick={(e) => onTolgitud(k, base) && (e.currentTarget.href = linkLang(k, base) + location.search)} hreflang={k} lang={k} title={KEEL_NIMI[k]} aria-current={k === lang ? 'true' : undefined} data-sveltekit-reload>{k.toUpperCase()}</a>{/each}</nav>
	</div>
</header>
{:else}
<header class="site-header">
	<div class="wrap">
		<a class="logo" href={L('/')} aria-label={t("Pidurdusmaa.ee avaleht")}><b>PIDURDUSMAA</b><em>.ee</em></a>
		<nav class="nav" aria-label={t("Peamenüü")}>
			<a href={L('/')} aria-current={cur === 'home' ? 'page' : undefined}>Pidurdusmaa</a>
			<div class="dd" data-dd>
				<button
					type="button"
					class="dd-btn"
					aria-expanded="false"
					aria-haspopup="true"
					aria-current={cur === 'valik' ? 'page' : undefined}
					>{t("Rehvi valimine")} <Icon name="chev" /></button
				>
				<div class="dd-menu" role="menu">
					{@html t("<a role=\"menuitem\" href=\"/rehvi-valimine/\" ><b>Vali rehv enda tingimustele</b><span>Mis on sulle oluline — näitame sobivaid</span></a > <a role=\"menuitem\" href=\"/vordle-rehve/\" ><b>Võrdle rehve kõrvuti</b><span>2–4 rehvi ühes tabelis</span></a >")}
					<a role="menuitem" href={L('/talverehvid/')}><b>{t('Parimad talverehvid')}</b><span>{t('Testid ja pidurdusmaa sinu mõõdus')}</span></a>
					<a role="menuitem" href={L('/teadmine/rehvivahetus/')}><b>{t('Rehvivahetus')}</b><span>{t('Millal talve- ja suverehvid alla')}</span></a>
				</div>
			</div>
			<a href={lang === 'ru' ? '/ru/teadmine/artiklid/' : '/teadmine/'} aria-current={cur === 'teadmine' ? 'page' : undefined}>{t("Teadmine")}</a>
		</nav>
		<div class="hdr-right">
			<nav class="keeled" aria-label={t("Keel")}>{#each KEELED as k (k)}<a href={keeleLink(k)} onclick={(e) => onTolgitud(k, base) && (e.currentTarget.href = linkLang(k, base) + location.search)} hreflang={k} lang={k} title={KEEL_NIMI[k]} aria-current={k === lang ? 'true' : undefined} data-sveltekit-reload>{k.toUpperCase()}</a>{/each}</nav>
			<a class="cmp-link" href={L('/vordle-rehve/')} data-cmp-pill>
				<Icon name="heart" /><span>{@html t("Võrdlus (<span data-cmp-n>0</span>)")}</span>
			</a>
			<button
				class="burger"
				type="button"
				aria-controls="pm-panel"
				aria-expanded="false"
				aria-label={t("Menüü")}
				data-burger><Icon name="menu" /></button
			>
		</div>
	</div>
	<div class="panel-menu" id="pm-panel" hidden>
		<div class="wrap pm">
			<!-- peamised tööriistad: suured kaardid -->
			<div class="pm-tiles">
				<a class="pm-tile" href={L('/')}><Icon name="gauge" /><b>{t("Pidurdusmaa kalkulaator")}</b><span>{t("Kui kiiresti sinu auto peatub")}</span></a>
				<a class="pm-tile" href={L('/rehvi-valimine/')}><Icon name="target" /><b>{t("Vali rehv")}</b><span>{t("Sobivad rehvid sinu tingimustele")}</span></a>
				<a class="pm-tile" href={lang === 'ru' ? '/ru/teadmine/artiklid/' : '/teadmine/'}><Icon name="book" /><b>{t("Teadmine")}</b><span>{t("Rehvid ja pidurdamine lihtsalt lahti seletatud")}</span></a>
				<a class="pm-tile" href={L('/teadmine/rehvivahetus/')}><Icon name="calendar" /><b>{t("Rehvivahetus")}</b><span>{t("Millal talve- ja suverehvid alla")}</span></a>
			</div>

			<section class="pm-sek">
				<h4>{t("Liiklusohutus")}</h4>
				<div class="pm-chips">
					<a href={L('/liiklusohutus/')}><Icon name="road" />{t("Peatumisteekond")}</a>
					<a href={L('/liiklusohutus/pimedas/')}><Icon name="moon" />{t("Pimedas")}</a>
					<a href={L('/liiklusohutus/pikivahe/')}><Icon name="gap" />{t("Pikivahe")}</a>
					<a href={L('/liiklusohutus/kurv/')}><Icon name="curve" />{t("Kurv ja rehvid")}</a>
				</div>
			</section>

			<div class="pm-two">
				<section class="pm-sek">
					<h4>{t("Otsi")}</h4>
					<a class="pm-row" href={L('/autod/')}><Icon name="car" />{t("Autod ja rehvimõõdud")}</a>
					<a class="pm-row" href={L('/rehvid/')}><Icon name="tyre" />{t("Rehvid")}</a>
					<a class="pm-row" href={L('/vordle-rehve/')}><Icon name="compare" />{t("Võrdle rehve kõrvuti")}</a>
					<a class="pm-row" href={L('/talverehvid/')}><Icon name="snow" />{t("Parimad talverehvid")}</a>
					<a class="pm-row" href="/testid/"><Icon name="test" />{t("Sõltumatud testid")}</a>
				</section>
				<section class="pm-sek">
					<h4>{t("Loe")}</h4>
					{#if lang !== 'ru'}<a class="pm-row" href={L('/teadmine/artiklid/')}><Icon name="book" />{t("Artiklid")}</a>{/if}
					<a class="pm-row" href={L('/teadmine/pidurdusteekond-ja-peatumisteekond/')}><Icon name="info" />{t("Pidurdus- ja peatumisteekond")}</a>
					<a class="pm-row" href="/teadmine/rehvimargis/"><Icon name="info" />{t("EL-i rehvimärgis")}</a>
					<a class="pm-row" href="/teadmine/kuidas-pidurdusmaa-arvutatakse/"><Icon name="info" />{t("Kuidas arvutatakse")}</a>
				</section>
			</div>

			<div class="pm-alla">
				<nav class="keeled pm-keeled" aria-label={t("Keel")}>{#each KEELED as k (k)}<a href={keeleLink(k)} onclick={(e) => onTolgitud(k, base) && (e.currentTarget.href = linkLang(k, base) + location.search)} hreflang={k} lang={k} aria-current={k === lang ? 'true' : undefined} data-sveltekit-reload>{KEEL_NIMI[k]}</a>{/each}</nav>
				<button type="button" class="pm-kontakt pm-pwa" data-pwa-lisa hidden><Icon name="download" />{t("Lisa avaekraanile")}</button>
				<a class="pm-kontakt" href="/kontakt/">{t("Kontakt")}</a>
				<p class="pm-pwa-v" data-pwa-vihje hidden>{@html t("iPhone'is: vajuta brauseri <b>Jaga</b>-nuppu (ruut noolega) ja vali <b>„Lisa avaekraanile“</b>. Pidurdusmaa avaneb siis nagu äpp, täisekraanil.")}</p>
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
				<a class="logo" href={L('/')}><b>PIDURDUSMAA</b><em>.ee</em></a>
				<p>
					{t("Sa ei pea teadma, milline rehv on hea. Näitame, kuidas need erinevad — päris andmete järgi, ja ütleme otse, kui andmeid ei ole.")}
				</p>
			</div>
			<div>
				<h4>{t("Tööriistad")}</h4>
				<ul>
					<li><a href={L('/')}>{t("Pidurdusmaa kalkulaator")}</a></li>
					<li><a href={L('/rehvi-valimine/')}>{t("Rehvi valimine")}</a></li>
					<li><a href={L('/vordle-rehve/')}>{t("Võrdle rehve")}</a></li>
					<li><a href={L('/talverehvid/')}>{t("Parimad talverehvid")}</a></li>
					<li><a href={L('/teadmine/rehvivahetus/')}>{t("Rehvivahetus")}</a></li>
					<li><a href={L('/liiklusohutus/')}>{t("Liiklusohutuse kalkulaator")}</a></li>
				</ul>
			</div>
			<div>
				<h4>{t("Andmed")}</h4>
				<ul>
					<li><a href={L('/autod/')}>{t("Autod")}</a></li>
					<li><a href={L('/rehvid/')}>{t("Rehvid")}</a></li>
					<li><a href="/testid/">{t("Sõltumatud testid")}</a></li>
					<li><a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">{t("Kuidas arvutatakse")}</a></li>
					<li><a href="/margid/">{t("Rehvimargid")}</a></li>
					<li><a href="/teadmine/">{t("Teadmine")}</a></li>
					<li><a href={L('/teadmine/artiklid/')}>{t("Artiklid")}</a></li>
					<li><a href="/meist/">{t("Meist")}</a></li>
					<li><a href="/teadmine/partnerid/">{t("Partnerid")}</a></li>
					<li><a href="/kontakt/">{t("Kontakt")}</a></li>
				</ul>
			</div>
			<div>
				<h4>{t("Allikad")}</h4>
				<ul>
					<li>{t("EL-i tooteregister EPREL")}</li>
					<li>{t("ADAC, Tekniikan Maailma, UTAC, Vi Bilägare")}</li>
					<li>{t("UNECE R117")}</li>
				</ul>
			</div>
		</div>
		{/if}
		<div class="ft-b">
			<span>© {new Date().getFullYear()} Rabarvo OÜ · {#if neutraal}<a href={L('/')}>Pidurdusmaa.ee</a> {t("— rehvide pidurdusmaa sinu autoga")}{:else}Pidurdusmaa.ee{/if}</span>
			<span
				>{t("Tulemused on arvutatud hinnangud — mitte mõõtmised ega garantii.")}
				<a href="/kasutustingimused/">{t("Kasutustingimused ja vastutus")}</a> ·
				<a href="/privaatsus/">{t("Privaatsus")}</a>{#if GA4_ID}
					·
					<button type="button" class="linkbtn" onclick={() => window.PM_KUPSISED?.()}
						>{t("Küpsiste seaded")}</button
					>{/if}</span
			>
		</div>
	</div>
</footer>

<Nousolek />
