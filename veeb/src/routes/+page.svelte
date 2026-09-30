<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	/* Avaleht = pidurdusmaa. Kaardi teine vaheleht „Vali rehv enda
	   tingimustel“ peidab kalkulaatori tulemuse ja infoplokid ning näitab
	   nende asemel sobivate rehvide nimekirja (sama loogika, mis
	   /rehvi-valimine/ lehel). Vahetuse teeb app.js. */
	import Icon from '$lib/Icon.svelte';
	import Calc from '$lib/Calc.svelte';
	import Result from '$lib/Result.svelte';
	import How from '$lib/How.svelte';
	import { num, pct } from '$lib/util.js';
	import Meta from '$lib/Meta.svelte';
	import { ORG, WEBSITE, tooriist, graph } from '$lib/skeem.js';

	let { data } = $props();
	const d = data.demo;
	const max = d ? Math.max(...d.wet) : 1;
</script>

<Meta
	fullTitle={t("Pidurdusmaa kalkulaator — pidurdus- ja peatumisteekond | Pidurdusmaa.ee")}
	title={t("Kui kiiresti sinu auto peatub?")}
	desc={t("Arvuta oma auto pidurdusteekond ja peatumisteekond eri kiirustel ja teeoludel. Päris rehviandmed: EL-i rehvimärgis ja sõltumatud testid.")}
	path=""
	jsonld={graph(
		ORG,
		WEBSITE,
		tooriist(
			t('Pidurdusmaa kalkulaator'),
			'/',
			t('Arvutab auto pidurdusteekonna ja peatumisteekonna (koos reaktsiooniajaga) valitud kiirusel ja teeoludel päris rehviandmete järgi: EL-i rehvimärgis ja sõltumatud rehvitestid.'), keel.lang)
	)}
/>

<section class="hero" aria-labelledby="hero-h">
	<div class="wrap">
		<div class="hero-copy">
			<h1 id="hero-h">{@html t("<span class=\"kick\">Pidurdusmaa kalkulaator</span> Kui kiiresti <span class=\"up\">sinu auto</span> <span class=\"up\">peatub?</span>")}</h1>
			<p class="lede">{t("Arvuta pidurdusmaa erinevatel kiirustel ja teeoludel.")}</p>
			<p class="tagline">
				{t("Lihtne. Kiire. Täpne.")}<svg viewBox="0 0 120 10" preserveAspectRatio="none" aria-hidden="true"
					><path
						d="M2 7 C 30 2, 70 2, 118 5"
						stroke="#ffc20e"
						stroke-width="2.4"
						fill="none"
						stroke-linecap="round"
					/></svg
				>
			</p>
			<div class="hero-visual-m" aria-hidden="true">
				<img src="/img/hero-car.jpg" alt="" fetchpriority="low" decoding="async" width="624" height="588" />
			</div>
		</div>
		<div class="hero-photo" aria-hidden="true">
			<img src="/img/hero-car.jpg" alt="" fetchpriority="high" decoding="async" width="624" height="588" />
		</div>
		<Calc />
	</div>
</section>

<div data-home="calc">
	<Result />

	{#if d}
		<section class="sec" aria-labelledby="s1">
			<div class="wrap why">
				<div>
					<div class="sec-h">
						<span class="eyebrow" style="color:var(--muted)">{t("Miks pidurdusmaa loeb")}</span>
						<h2 id="s1">{t("Kiirus kasvab lineaarselt. Pidurdusmaa ei kasva.")}</h2>
						<p>
							{t("Kahekordne kiirus tähendab rohkem kui kahekordset pidurdusmaad. Märjal teel on vahe veel suurem.")}
						</p>
					</div>
					<div class="bullets">
						<div>
							<span class="ic"><Icon name="car" /></span>
							<div>
								<h3>{t("Peatumisteekond = reageerimine + pidurdus")}</h3>
								<p>
									{t("Enne kui pidur hakkab tööle, sõidab auto reaktsiooniaja jooksul täiskiirusel edasi: 90 km/h juures 1 sekundiga 25 m. Märjal teel on peatumisteekond seega umbes")}
									{num(25 + d.wet[1])} {t("m.")} <a href="/teadmine/pidurdusteekond-ja-peatumisteekond/"
										>{t("Valem ja näited")}</a
									>
								</p>
							</div>
						</div>
						<div>
							<span class="ic"><Icon name="speed" /></span>
							<div>
								<h3>{t("90 → 110 km/h")}</h3>
								<p>
									{t("Märjal")} {num(d.wet[1])} {t("m asemel")} {num(d.wet[2])} m — {num(d.wet[2] - d.wet[1])}
									{t("meetrit ehk")} {pct(d.wet[2], d.wet[1]).replace('+', '')} {t("rohkem.")}
								</p>
							</div>
						</div>
						<div>
							<span class="ic"><Icon name="wet" /></span>
							<div>
								<h3>{t("Märg vs kuiv")}</h3>
								<p>{t("90 km/h juures kuival")} {num(d.dry[1])} {t("m, märjal")} {num(d.wet[1])} {t("m.")}</p>
							</div>
						</div>
						<div>
							<span class="ic"><Icon name="tyre" /></span>
							<div>
								<h3>{t("Rehv")}</h3>
								<p>
									{t("Sama auto, sama märg tee: A-klassi märgisega rehv")} {num(d.classA)} {t("m, E-klassi")} {num(
										d.classE
									)} {t("m.")}
								</p>
							</div>
						</div>
					</div>
				</div>
				<div class="stopline" role="img" aria-label={t("Pidurdusmaa märjal eri kiirustel")}>
					<h3>{t("Pidurdusmaa ·")} {d.car.replace('suverehv märgise klassiga', t('suverehv märgise klassiga'))}</h3>
					{#each d.speeds as v, i}
						<div class="sl-row">
							<span class="k">{Math.round(v)} {t("km/h")}</span>
							<span class="t"
								><span style="width:{Math.round((1000 * d.wet[i]) / max) / 10}%"></span></span
							>
							<span class="v">{num(d.wet[i])} {t("m")}</span>
						</div>
					{/each}
					<p class="src">
						{@html t("Märg asfalt, veekiht 1 mm, +10 °C. Ilma reaktsiooniajata. <span class=\"pill calc\" style=\"margin-left:var(--sp-2)\">Arvutatud</span>")}
					</p>
				</div>
			</div>
		</section>

		<section class="sec alt" aria-labelledby="s2">
			<div class="wrap">
				<div class="sec-h">
					<span class="eyebrow" style="color:var(--muted)">{t("Mis mõjutab pidurdusmaad")}</span>
					<h2 id="s2">{t("Kuus asja, mida saad mõjutada")}</h2>
					<p>
						{t("Kõik arvud on arvutatud kalkulaatori sama mudeliga — sama auto, üks asi korraga muudetud.")}
					</p>
				</div>
				<div class="factors">
					<div class="factor">
						<div class="ic"><Icon name="speed" /></div>
						<h3>{t("Kiirus")}</h3>
						<p>{t("Kõige suurem üksik tegur. Energia kasvab kiiruse ruudus.")}</p>
						<p class="fx">{t("50 → 110 km/h märjal:")} <b>{num(d.wet[0])} → {num(d.wet[2])} {t("m")}</b></p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="road" /></div>
						<h3>{t("Teeolud")}</h3>
						<p>{t("Lumi ja jää muudavad kõike. Suverehv lumel on teine maailm.")}</p>
						<p class="fx">
							{t("Lumi 50 km/h, suvi vs talv:")} <b>{num(d.snowSummer)} / {num(d.snowWinter)} {t("m")}</b>
						</p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="tyre" /></div>
						<h3>{t("Rehv")}</h3>
						<p>{t("Märghaardumise klass on ametlik ja võrreldav. Ainult sinu mõõdus.")}</p>
						<p class="fx">
							{t("Klass A vs E, 90 km/h:")} <b>+{num(d.classE - d.classA)} m ({pct(d.classE, d.classA)})</b>
						</p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="temp" /></div>
						<h3>{t("Temperatuur")}</h3>
						<p>{t("Talverehv on soojal asfaldil pehme ja pidurdab halvemini.")}</p>
						<p class="fx">
							{t("Kuiv +25 °C, suvi vs talv:")}
							<b>{num(d.summerWarm)} / {num(d.winterWarm)} m ({pct(d.winterWarm, d.summerWarm)})</b>
						</p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="car" /></div>
						<h3>{t("Auto")}</h3>
						<p>{t("Mass, ABS ja pidurid. Koorem mõjutab vähem, kui arvatakse.")}</p>
						<p class="fx">
							{t("+375 kg koormat märjal:")}
							<b>{num(d.tread8)} → {num(d.loaded)} m ({pct(d.loaded, d.tread8)})</b>
						</p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="wear" /></div>
						<h3>{t("Rehvi seisukord")}</h3>
						<p>{t("Kulunud muster juhib vett halvemini. Sügavas vees kordades.")}</p>
						<p class="fx">
							{t("8 mm → 3 mm, märg 90 km/h:")}
							<b>{num(d.tread8)} → {num(d.tread3)} m ({pct(d.tread3, d.tread8)})</b>
						</p>
					</div>
				</div>
			</div>
		</section>
	{/if}
</div>

<div data-home="valik" hidden>
	<section class="body-sec home-valik" id="sobivad" aria-labelledby="hv-h" data-valik-home>
		<div class="wrap">
			<div class="hv-head">
				<div>
					<span class="eyebrow" style="color:var(--muted)">{t("Rehvi valimine")}</span>
					<h2 id="hv-h">{t("Sinu tingimustele sobivad rehvid")}</h2>
				</div>
				<div class="list-filter">
					<select class="lsel" data-brand aria-label={t("Mark")}
						><option value="">{t("Kõik margid")}</option></select
					>
					<input
						class="lsel"
						type="search"
						data-q
						placeholder={t("Otsi marki või mudelit")}
						aria-label={t("Otsi rehvi")}
						style="background-image:none"
					/>
				</div>
				<p class="note" data-cmp-head style="margin:0;font-size:15px"></p>
			</div>
			<div class="cmp-layout">
				<aside class="filters" aria-label={t("Täpsemad seaded")}>
					<div class="box">
						<div style="display:flex;align-items:center;justify-content:space-between">
							<h3 style="margin:0">{t("Täpsusta soove")}</h3>
							<button type="button" class="btn sm" data-prio-reset hidden>{t("Tühjenda")}</button>
						</div>
						<p class="note" style="margin:var(--sp-2) 0 var(--sp-3)">
							{t("Valikuline. Sinu vastused täidavad selle ise — siin näed ja muudad, kui palju iga omadus loeb (1–3).")}
						</p>
						<div class="prio" data-prio></div>
					</div>
					<div class="box">
						<h3 style="margin:0 0 var(--sp-2)">{t("Kuidas järjestatakse")}</h3>
						<p class="note" style="margin:0">
							{t("„Sobivus“ on ainult selle nimekirja sisene võrdlus sinu valitud omaduste järgi — mitte rehvi üldhinne. Hinnad ei mõjuta järjestust.")}
						</p>
						<p class="note" style="margin:var(--sp-3) 0 0">
							{@html t("See on andmete kõrvutus, mitte ostunõuanne. <a href=\"/kasutustingimused/\">Tingimused</a>")}
						</p>
					</div>
				</aside>
				<div class="res-list" data-cmp-list><p class="note">{t("Laen…")}</p></div>
			</div>
		</div>
	</section>
	<div class="cmp-tray" data-tray hidden>
		<div class="wrap">
			<div class="chips" data-tray-chips></div>
			<a class="btn yel sm" href={keel.L('/vordle-rehve/')} data-tray-go>{t("Võrdle kõrvuti →")}</a>
		</div>
	</div>
</div>

<How />
