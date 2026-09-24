<script>
	/* Küpsiste nõusolek ja Google Analytics 4.
	 *
	 * EL-is (ePrivacy + GDPR) tohib analüütikaküpsiseid panna AINULT pärast
	 * nõusolekut. Seepärast siin:
	 *   - enne nõusolekut ei laeta Google'i skripti üldse — ei ühtegi
	 *     päringut Google'isse, ei ühtegi küpsist;
	 *   - "Nõustun" ja "Ainult vajalikud" on võrdselt nähtavad;
	 *   - otsust saab jalusest igal ajal muuta ("Küpsiste seaded") ja
	 *     tagasivõtmisel kustutatakse GA küpsised.
	 * Reklaamiküpsiseid ei kasutata kunagi (ad_* jäävad keelatuks).
	 *
	 * Kui GA4_ID on tühi, ei tee see komponent midagi ega näita riba.
	 */
	import { onMount } from 'svelte';
	import { GA4_ID } from '$lib/seaded.js';

	const VOTI = 'pm_nousolek';
	let naita = $state(false);

	function loe() {
		try {
			return localStorage.getItem(VOTI);
		} catch {
			return null;
		}
	}
	function kirjuta(v) {
		try {
			localStorage.setItem(VOTI, v);
		} catch {
			/* privaatrežiim — otsus kehtib ainult selle lehe jaoks */
		}
	}

	let kaivitatud = false;
	function kaivitaGA() {
		if (kaivitatud || !GA4_ID) return;
		kaivitatud = true;
		window.dataLayer = window.dataLayer || [];
		// gtag peab edastama `arguments` objekti, mitte massiivi — nii tahab GA
		window.gtag = function () {
			window.dataLayer.push(arguments);
		};
		window.gtag('consent', 'default', {
			ad_storage: 'denied',
			ad_user_data: 'denied',
			ad_personalization: 'denied',
			analytics_storage: 'granted'
		});
		window.gtag('js', new Date());
		/* lehevaatamised saadame ise, sest SvelteKit vahetab lehti ilma
		   täislaadimiseta ja GA ei märkaks neid */
		window.gtag('config', GA4_ID, { send_page_view: false });
		const s = document.createElement('script');
		s.async = true;
		s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA4_ID);
		document.head.appendChild(s);
		window.PM_GA = (nimi, param) => window.gtag('event', nimi, param || {});
		lehevaade();
	}

	function lehevaade() {
		if (typeof window.PM_GA !== 'function') return;
		window.PM_GA('page_view', {
			page_location: location.href,
			page_path: location.pathname + location.search,
			page_title: document.title
		});
	}

	function kustutaGAkupsised() {
		const host = location.hostname;
		const domeenid = [host, '.' + host, '.' + host.replace(/^www\./, '')];
		for (const c of document.cookie.split(';')) {
			const nimi = c.split('=')[0].trim();
			if (!/^_ga/.test(nimi)) continue;
			for (const d of domeenid) {
				document.cookie = `${nimi}=; Max-Age=0; path=/; domain=${d}`;
			}
			document.cookie = `${nimi}=; Max-Age=0; path=/`;
		}
	}

	function noustun() {
		kirjuta('jah');
		naita = false;
		if (kaivitatud) window.gtag('consent', 'update', { analytics_storage: 'granted' });
		else kaivitaGA();
	}
	function keeldun() {
		kirjuta('ei');
		naita = false;
		if (kaivitatud) {
			window.gtag('consent', 'update', { analytics_storage: 'denied' });
			window.PM_GA = undefined;
		}
		kustutaGAkupsised();
	}

	onMount(() => {
		if (!GA4_ID) return;
		/* jaluse "Küpsiste seaded" avab riba uuesti */
		window.PM_KUPSISED = () => (naita = true);
		window.PM_LEHEVAADE = lehevaade;
		const v = loe();
		if (v === 'jah') kaivitaGA();
		else if (v !== 'ei') naita = true;
	});
</script>

{#if naita}
	<div class="kps" role="region" aria-label="Küpsiste nõusolek">
		<div class="kps-in">
			<p>
				<b>Statistika küpsised.</b> Tahame näha, milliseid lehti ja arvutusi kasutatakse, et lehte
				paremaks teha. Selleks kasutame Google Analyticsit, mis paneb su brauserisse küpsise. Reklaami
				me ei näita ega jaga andmeid reklaami jaoks.
				<a href="/privaatsus/">Loe lähemalt</a>
			</p>
			<div class="kps-b">
				<button type="button" class="btn" onclick={keeldun}>Ainult vajalikud</button>
				<button type="button" class="btn dark" onclick={noustun}>Nõustun</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.kps {
		position: fixed;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: 80;
		padding: 12px 16px calc(12px + env(safe-area-inset-bottom, 0px));
		pointer-events: none;
	}
	.kps-in {
		pointer-events: auto;
		max-width: 880px;
		margin: 0 auto;
		display: flex;
		gap: 16px;
		align-items: center;
		background: #fff;
		color: #171a1f;
		border: 1px solid #e3e5e8;
		border-radius: 14px;
		padding: 14px 16px;
		box-shadow: 0 10px 30px rgba(10, 12, 16, 0.18);
	}
	.kps p {
		margin: 0;
		font-size: 14px;
		line-height: 1.5;
		flex: 1;
	}
	.kps a {
		color: inherit;
		text-decoration: underline;
	}
	.kps-b {
		display: flex;
		gap: 8px;
		flex-shrink: 0;
	}
	/* mõlemad nupud on sama suurusega — keeldumine ei tohi olla raskem */
	.kps-b :global(.btn) {
		min-width: 140px;
		justify-content: center;
	}
	@media (max-width: 640px) {
		.kps-in {
			flex-direction: column;
			align-items: stretch;
		}
		.kps-b :global(.btn) {
			flex: 1;
			min-width: 0;
		}
	}
</style>
