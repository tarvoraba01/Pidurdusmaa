<script>
	/* Avaleht = pidurdusmaa. Kaardi teine vaheleht „Vali rehv enda
	   tingimustel“ peidab kalkulaatori tulemuse ja infoplokid ning näitab
	   nende asemel sobivate rehvide nimekirja (sama loogika, mis
	   /rehvi-valimine/ lehel). Vahetuse teeb app.js. */
	import Icon from '$lib/Icon.svelte';
	import Calc from '$lib/Calc.svelte';
	import Result from '$lib/Result.svelte';
	import How from '$lib/How.svelte';
	import { num, pct } from '$lib/util.js';

	let { data } = $props();
	const d = data.demo;
	const max = d ? Math.max(...d.wet) : 1;
</script>

<svelte:head>
	<title>Pidurdusmaa.ee — kui kiiresti sinu auto peatub?</title>
	<meta
		name="description"
		content="Arvuta oma auto pidurdusmaa erinevatel kiirustel ja teeoludel. Päris rehviandmed EL-i märgiselt ja sõltumatutest testidest."
	/>
	<link rel="canonical" href="https://pidurdusmaa.ee/" />
</svelte:head>

<section class="hero" aria-labelledby="hero-h">
	<div class="wrap">
		<div class="hero-copy">
			<h1 id="hero-h">Kui kiiresti <span class="up">sinu auto</span><span class="up">peatub?</span></h1>
			<p class="lede">Arvuta pidurdusmaa erinevatel kiirustel ja teeoludel.</p>
			<p class="tagline">
				Lihtne. Kiire. Täpne.<svg viewBox="0 0 120 10" preserveAspectRatio="none" aria-hidden="true"
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
						<span class="eyebrow" style="color:var(--muted)">Miks pidurdusmaa loeb</span>
						<h2 id="s1">Kiirus kasvab lineaarselt. Pidurdusmaa ei kasva.</h2>
						<p>
							Kahekordne kiirus tähendab rohkem kui kahekordset pidurdusmaad. Märjal teel on vahe
							veel suurem.
						</p>
					</div>
					<div class="bullets">
						<div>
							<span class="ic"><Icon name="speed" /></span>
							<div>
								<h3>90 → 110 km/h</h3>
								<p>
									Märjal {num(d.wet[1])} m asemel {num(d.wet[2])} m — {num(d.wet[2] - d.wet[1])}
									meetrit ehk {pct(d.wet[2], d.wet[1]).replace('+', '')} rohkem.
								</p>
							</div>
						</div>
						<div>
							<span class="ic"><Icon name="wet" /></span>
							<div>
								<h3>Märg vs kuiv</h3>
								<p>90 km/h juures kuival {num(d.dry[1])} m, märjal {num(d.wet[1])} m.</p>
							</div>
						</div>
						<div>
							<span class="ic"><Icon name="tyre" /></span>
							<div>
								<h3>Rehv</h3>
								<p>
									Sama auto, sama märg tee: märgise klass A {num(d.classA)} m, klass E {num(
										d.classE
									)} m.
								</p>
							</div>
						</div>
					</div>
				</div>
				<div class="stopline" role="img" aria-label="Pidurdusmaa märjal eri kiirustel">
					<h3>Pidurdusmaa · {d.car}</h3>
					{#each d.speeds as v, i}
						<div class="sl-row">
							<span class="k">{Math.round(v)} km/h</span>
							<span class="t"
								><span style="width:{Math.round((1000 * d.wet[i]) / max) / 10}%"></span></span
							>
							<span class="v">{num(d.wet[i])} m</span>
						</div>
					{/each}
					<p class="src">
						Märg asfalt, veekiht 1 mm, +10 °C. Ilma reaktsiooniajata.
						<span class="pill calc" style="margin-left:6px">Arvutatud</span>
					</p>
				</div>
			</div>
		</section>

		<section class="sec alt" aria-labelledby="s2">
			<div class="wrap">
				<div class="sec-h">
					<span class="eyebrow" style="color:var(--muted)">Mis mõjutab pidurdusmaad</span>
					<h2 id="s2">Kuus asja, mida saad mõjutada</h2>
					<p>
						Kõik arvud on arvutatud sama mudeliga, mis kalkulaator — sama auto, üks asi korraga
						muudetud.
					</p>
				</div>
				<div class="factors">
					<div class="factor">
						<div class="ic"><Icon name="speed" /></div>
						<h3>Kiirus</h3>
						<p>Kõige suurem üksik tegur. Energia kasvab kiiruse ruudus.</p>
						<p class="fx">50 → 110 km/h märjal: <b>{num(d.wet[0])} → {num(d.wet[2])} m</b></p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="road" /></div>
						<h3>Teeolud</h3>
						<p>Lumi ja jää muudavad kõike. Suverehv lumel on teine maailm.</p>
						<p class="fx">
							Lumi 50 km/h, suvi vs talv: <b>{num(d.snowSummer)} / {num(d.snowWinter)} m</b>
						</p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="tyre" /></div>
						<h3>Rehv</h3>
						<p>Märghaardumise klass on ametlik ja võrreldav. Ainult sinu mõõdus.</p>
						<p class="fx">
							Klass A vs E, 90 km/h: <b>+{num(d.classE - d.classA)} m ({pct(d.classE, d.classA)})</b>
						</p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="temp" /></div>
						<h3>Temperatuur</h3>
						<p>Talverehv on soojal asfaldil pehme ja pidurdab halvemini.</p>
						<p class="fx">
							Kuiv +25 °C, suvi vs talv:
							<b>{num(d.summerWarm)} / {num(d.winterWarm)} m ({pct(d.winterWarm, d.summerWarm)})</b>
						</p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="car" /></div>
						<h3>Auto</h3>
						<p>Mass, ABS ja pidurid. Koorem mõjutab vähem, kui arvatakse.</p>
						<p class="fx">
							+375 kg koormat märjal:
							<b>{num(d.tread8)} → {num(d.loaded)} m ({pct(d.loaded, d.tread8)})</b>
						</p>
					</div>
					<div class="factor">
						<div class="ic"><Icon name="wear" /></div>
						<h3>Rehvi seisukord</h3>
						<p>Kulunud muster juhib vett halvemini. Sügavas vees kordades.</p>
						<p class="fx">
							8 mm → 3 mm, märg 90 km/h:
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
					<span class="eyebrow" style="color:var(--muted)">Rehvi valimine</span>
					<h2 id="hv-h">Sinu tingimustele sobivad rehvid</h2>
				</div>
				<div class="list-filter">
					<select class="lsel" data-brand aria-label="Mark"
						><option value="">Kõik margid</option></select
					>
					<input
						class="lsel"
						type="search"
						data-q
						placeholder="Otsi marki või mudelit"
						aria-label="Otsi rehvi"
						style="background-image:none"
					/>
				</div>
				<p class="note" data-cmp-head style="margin:0;font-size:15px"></p>
			</div>
			<div class="cmp-layout">
				<aside class="filters" aria-label="Täpsemad seaded">
					<div class="box">
						<div style="display:flex;align-items:center;justify-content:space-between">
							<h3 style="margin:0">Täpsusta kaalusid</h3>
							<button type="button" class="btn sm" data-prio-reset hidden>Tühjenda</button>
						</div>
						<p class="note" style="margin:6px 0 12px">
							Valikuline. Sinu vastused täidavad selle ise — siin näed ja muudad, kui palju iga
							omadus loeb (1–3).
						</p>
						<div class="prio" data-prio></div>
					</div>
					<div class="box">
						<h3 style="margin:0 0 8px">Kuidas järjestatakse</h3>
						<p class="note" style="margin:0">
							„Sobivus“ on ainult selle nimekirja sisene võrdlus sinu valitud omaduste järgi — mitte
							rehvi üldhinne. Hinnad ei mõjuta järjestust.
						</p>
						<p class="note" style="margin:10px 0 0">
							See on andmete kõrvutus, mitte ostunõuanne.
							<a href="/kasutustingimused/">Tingimused</a>
						</p>
					</div>
				</aside>
				<div class="res-list" data-cmp-list><p class="note">Laen…</p></div>
			</div>
		</div>
	</section>
	<div class="cmp-tray" data-tray hidden>
		<div class="wrap">
			<div class="chips" data-tray-chips></div>
			<a class="btn yel sm" href="/vordle-rehve/" data-tray-go>Võrdle kõrvuti →</a>
		</div>
	</div>
</div>

<How />
