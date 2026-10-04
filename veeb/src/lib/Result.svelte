<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	/* Tulemuse riba + üksikasjad + usaldusriba. Sisu täidab app.js —
	   arvutus käivitub nupuvajutusega ja kirjutab siia data-r-* kohtadesse. */
	import Icon from '$lib/Icon.svelte';
	const TIP =
		t('Arvutatud tulemus meie mudelist, mitte mõõtmine. Päris pidurdusmaa võib erineda — vahemik all näitab tõenäolist ulatust.');
</script>

<section class="rstrip-wrap" id="tulemus" aria-live="polite" aria-labelledby="res-h" hidden>
	<div class="wrap">
		<div class="rstrip" data-result>
			<div>
				<!-- vasak veerg püsib kerimisel nähtaval: tulemus + valitud rehvi hinnad -->
				<div class="rs-stick">
				<p class="rs-k" id="res-h">{@html t("Tulemused: <span data-r-range>90 km/h → 0 km/h</span>")}</p>
				<div class="cat-switch rs-mode" role="group" aria-label={t("Mida näidata")}>
					<button type="button" data-r-mode="brake" aria-pressed="true">{t("Pidurdusteekond")}</button>
					<button type="button" data-r-mode="stop" aria-pressed="false">{t("Peatumisteekond")}</button>
				</div>
				<p class="rs-l">
					<span data-r-lbl>{t("Pidurdusteekond · pidur põhjas kuni seisuni")}</span>
					<span class="tip" tabindex="0" data-tip={TIP} aria-label={TIP}>i</span>
				</p>
				<p class="rs-num"><Icon name="car" /><b data-r-big>—</b><small>{t("m")}</small></p>
				<p class="rs-split" data-r-split hidden>
					<label for="r-rt">{t("Reaktsiooniaeg")}</label>
					<select id="r-rt" class="lsel rs-rt" data-r-rt>
						<option value="0.5">{t("0,5 s · valmis pidurdama")}</option>
						<option value="1" selected>{t("1 s · tavaline")}</option>
						<option value="1.5">{t("1,5 s · väsinud")}</option>
						<option value="2">{t("2 s · tähelepanu mujal")}</option>
					</select>
					<span data-r-splittxt></span>
				</p>
				<p class="rs-who" data-r-whoshort>{t("Arvutan…")}</p>
				<div class="r-price" data-r-price></div>
				</div>
			</div>
			<div>
				<p class="rs-k">{t("Kui palju muudab rehv?")}</p>
				<p class="rs-expl">
					{@html t("Sama auto ja kiirus, ainult rehv erineb. <b>Lühem riba = auto seisab varem.</b> Täht on EL-i rehvimärgise märghaarde klass: <span class=\"gr A\">A</span> pidurdab märjal kõige paremini.")}
				</p>
				<ol class="mbars" data-r-mbars></ol>
				<div class="rs-links">
					<button
						type="button"
						class="linkbtn"
						data-r-toggle
						aria-expanded="false"
						aria-controls="r-detail">{t("Kõik rehvid ja üksikasjad")}</button
					>
					<button type="button" class="linkbtn" data-how>{t("Kuidas arvutatakse?")}</button>
				</div>
				<div class="r-pood" data-r-pood hidden></div>
				<p class="rs-legal">
					{@html t("Hinnang, mitte garantii. Ära kasuta seda liikluses otsustamiseks. <a href=\"/kasutustingimused/\">Tingimused</a>")}
				</p>
			</div>
			<div class="rs-cta">
				<div>
					<p>{t("Kasuta sobivaimate rehvide leidmiseks")}</p>
					<p class="{t("s")}">{t("Vali, mis on sinu jaoks oluline.")}</p>
				</div>
				<a class="btn dark" href={keel.L('/rehvi-valimine/')} data-r-valik>{t("Rehvi valimine →")}</a>
			</div>
		</div>

		<div class="rdetails" id="r-detail" data-r-detail hidden>
			<div class="res-grid">
				<div>
					<p class="res-kicker">
						{@html t("Tulemus <span class=\"num\" data-r-range2></span> · <span data-r-cond>märg asfalt</span>")}
					</p>
					<p class="res-big"><span class="hl" data-r-big2>—</span><small>{t("m")}</small></p>
					<p class="res-band" data-r-band></p>
					<p class="res-react" data-r-react></p>
					<div class="res-who" data-r-who></div>
					<div class="res-meta" data-r-meta></div>
				</div>
				<div>
					<div class="bars-h">
						<h2>{t("Kõik rehvid")}</h2>
						<div class="cat-switch" role="group" aria-label={t("Rehvitüüp")} data-r-cats></div>
					</div>
					<p class="bars-sub" data-r-sub></p>
					<ol class="bars" data-r-bars></ol>
					<div data-r-note></div>
					<div class="bars-foot">
						<button type="button" class="btn sm" data-r-more hidden></button>
						<a class="btn dark sm" href={keel.L('/vordle-rehve/')} data-r-cmp
							>{t("Võrdle rehve selles mõõdus →")}</a
						>
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

<section class="trust" aria-label={t("Kust tulemused tulevad")}>
	<div class="wrap">
		<div class="it">
			<Icon name="shield" />
			<div>{@html t("<b>Põhineb päris testidel</b><span>Sõltumatud rehvitestid ja ametlikud andmed</span>")}</div>
		</div>
		<div class="it">
			<Icon name="target" />
			<div>
				{@html t("<b>Läbipaistvad arvutused</b><span>EPREL andmed + testitulemused, allikas iga numbri juures</span>")}
			</div>
		</div>
		<div class="it">
			<Icon name="gauge" />
			<div>{@html t("<b>Kontrollitud täpsus</b><span>Mõõdetud pidurdusmaade vastu keskmiselt ~4% viga</span>")}</div>
		</div>
		<div class="it">
			<Icon name="info" />
			<button type="button" data-how
				>{@html t("<b>Kuidas see toimib?</b><span>Loe lähemalt pidurdusmaa arvutuste kohta</span>")}</button
			>
		</div>
	</div>
</section>
