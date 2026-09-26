<script>
	/* Tulemuse riba + üksikasjad + usaldusriba. Sisu täidab app.js —
	   arvutus käivitub nupuvajutusega ja kirjutab siia data-r-* kohtadesse. */
	import Icon from '$lib/Icon.svelte';
	const TIP =
		'Arvutatud tulemus meie mudelist, mitte mõõtmine. Päris pidurdusmaa võib erineda — vahemik all näitab tõenäolist ulatust.';
</script>

<section class="rstrip-wrap" id="tulemus" aria-live="polite" aria-labelledby="res-h" hidden>
	<div class="wrap">
		<div class="rstrip" data-result>
			<div>
				<!-- vasak veerg püsib kerimisel nähtaval: tulemus + valitud rehvi hinnad -->
				<div class="rs-stick">
				<p class="rs-k" id="res-h">Tulemused: <span data-r-range>90 km/h → 0 km/h</span></p>
				<div class="cat-switch rs-mode" role="group" aria-label="Mida näidata">
					<button type="button" data-r-mode="brake" aria-pressed="true">Pidurdusteekond</button>
					<button type="button" data-r-mode="stop" aria-pressed="false">Peatumisteekond</button>
				</div>
				<p class="rs-l">
					<span data-r-lbl>Pidurdusteekond · pidur põhjas kuni seisuni</span>
					<span class="tip" tabindex="0" data-tip={TIP} aria-label={TIP}>i</span>
				</p>
				<p class="rs-num"><Icon name="car" /><b data-r-big>—</b><small>m</small></p>
				<p class="rs-split" data-r-split hidden>
					<label for="r-rt">Reaktsiooniaeg</label>
					<select id="r-rt" class="lsel rs-rt" data-r-rt>
						<option value="0.5">0,5 s · valmis pidurdama</option>
						<option value="1" selected>1 s · tavaline</option>
						<option value="1.5">1,5 s · väsinud</option>
						<option value="2">2 s · tähelepanu mujal</option>
					</select>
					<span data-r-splittxt></span>
				</p>
				<p class="rs-who" data-r-whoshort>Arvutan…</p>
				<div class="r-price" data-r-price></div>
				</div>
			</div>
			<div>
				<p class="rs-k">
					Võrdlus teiste rehvidega
					<span style="font-weight:500;color:var(--muted)">(pidurdusteekond, samas mõõdus)</span>
				</p>
				<ol class="mbars" data-r-mbars></ol>
				<div class="rs-links">
					<button
						type="button"
						class="linkbtn"
						data-r-toggle
						aria-expanded="false"
						aria-controls="r-detail">Kõik rehvid ja üksikasjad</button
					>
					<button type="button" class="linkbtn" data-how>Kuidas arvutatakse?</button>
				</div>
				<p class="rs-legal">
					Hinnang, mitte garantii. Ära kasuta seda liikluses otsustamiseks.
					<a href="/kasutustingimused/">Tingimused</a>
				</p>
			</div>
			<div class="rs-cta">
				<div>
					<p>Kasuta sobivaimate rehvide leidmiseks</p>
					<p class="s">Vali, mis on sinu jaoks oluline.</p>
				</div>
				<a class="btn dark" href="/rehvi-valimine/" data-r-valik>Rehvi valimine →</a>
			</div>
		</div>

		<div class="rdetails" id="r-detail" data-r-detail hidden>
			<div class="res-grid">
				<div>
					<p class="res-kicker">
						Tulemus <span class="num" data-r-range2></span> ·
						<span data-r-cond>märg asfalt</span>
					</p>
					<p class="res-big"><span class="hl" data-r-big2>—</span><small>m</small></p>
					<p class="res-band" data-r-band></p>
					<p class="res-react" data-r-react></p>
					<div class="res-who" data-r-who></div>
					<div class="res-meta" data-r-meta></div>
				</div>
				<div>
					<div class="bars-h">
						<h2>Kõik rehvid</h2>
						<div class="cat-switch" role="group" aria-label="Rehvitüüp" data-r-cats></div>
					</div>
					<p class="bars-sub" data-r-sub></p>
					<ol class="bars" data-r-bars></ol>
					<div data-r-note></div>
					<div class="bars-foot">
						<button type="button" class="btn sm" data-r-more hidden></button>
						<a class="btn dark sm" href="/vordle-rehve/" data-r-cmp
							>Võrdle rehve selles mõõdus →</a
						>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

<section class="trust" aria-label="Kust tulemused tulevad">
	<div class="wrap">
		<div class="it">
			<Icon name="shield" />
			<div><b>Põhineb päris testidel</b><span>Sõltumatud rehvitestid ja ametlikud andmed</span></div>
		</div>
		<div class="it">
			<Icon name="target" />
			<div>
				<b>Läbipaistvad arvutused</b><span>EPREL andmed + testitulemused, allikas iga numbri juures</span>
			</div>
		</div>
		<div class="it">
			<Icon name="gauge" />
			<div><b>Kontrollitud täpsus</b><span>Mõõdetud pidurdusmaade vastu keskmiselt ~4% viga</span></div>
		</div>
		<div class="it">
			<Icon name="info" />
			<button type="button" data-how
				><b>Kuidas see toimib?</b><span>Loe lähemalt pidurdusmaa arvutuste kohta</span></button
			>
		</div>
	</div>
</section>
