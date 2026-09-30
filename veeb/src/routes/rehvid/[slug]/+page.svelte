<script>
	import { useT, useLang, autoNimi } from '$lib/i18n.js';
	/* Tekstid: eesti keel on lähtetekst, vene tõlge $lib/i18n/ru.js (/ru/rehvid/…) */
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	const an = (s) => autoNimi(keel.lang, s);
	import Meta from '$lib/Meta.svelte';
	import Grade from '$lib/Grade.svelte';
	import How from '$lib/How.svelte';
	import TyreArt from '$lib/TyreArt.svelte';
	import { KAT_NIMI, CONDS, num, pretty, testLabel } from '$lib/util.js';

	let { data } = $props();
	const KAT = { 0: t('Suverehvid'), 1: t('Aastaringsed rehvid'), 2: t('Talverehvid (Kesk-Euroopa)'), 3: t('Talverehvid (Põhjamaade)') };

	/* „märg asfalt, 80→0 km/h“ → tõlgitud pind + kiirus */
	function tl(x) {
		const s = testLabel(x);
		const i = s.indexOf(', ');
		return i < 0 ? t(s) : t(s.slice(0, i)) + s.slice(i).replace('km/h', t('km/h'));
	}
	/* otsingutulemuse kirjeldus: eesti keeles serverist, muidu tükkidest tõlgitult */
	const kirjeldus = $derived.by(() => {
		if (keel.lang === 'et' || !data.descOsad || !data.tyre) return data.desc;
		const o = data.descOsad;
		const osad = [];
		if (o.testid) osad.push(t('sõltumatu testi pidurdusmaad'));
		if (o.g) osad.push(t('märjal haardumise klass {g}', { g: o.g }));
		if (o.db) osad.push(t('müra {db} dB', { db: o.db }));
		if (o.n) osad.push(t(o.n === 1 ? '{n} mõõt' : '{n} mõõtu', { n: o.n }));
		return data.tyre.name + (o.fraas ? ' — ' + t(o.fraas).charAt(0).toLowerCase() + t(o.fraas).slice(1) : '') + (osad.length ? ': ' + osad.join(', ') : '') + '. ' + t('Vaata, kui pikk on pidurdusmaa sinu autoga.');
	});

	function pctVahe(d, x, y) {
		const p = (100 * d) / Math.min(x, y);
		return (d > 0 ? '+' : '') + num(p, Math.abs(p) < 10 ? 1 : 0);
	}
</script>

{#if data.liik === 'moot'}
	<Meta
		title={t('Rehvid {m} — {n} rehvimudelit märgise andmetega', { m: data.size.label, n: data.n })}
		desc={t('Kõik {m} mõõdus rehvid EL-i rehvimärgise järgi: märghaardumise klass, veeretakistus ja müra. Võrdle ja vaata, kui palju muutub pidurdusmaa.', { m: data.size.label })}
		path="rehvid/{data.size.slug}/"
		image={data.noindex ? undefined : `/og/m/${data.size.slug}.png`}
		noindex={data.noindex}
		crumbs={[[t('Avaleht'), '/'], [t('Rehvid'), '/rehvid/'], [data.size.label, '/rehvid/' + data.size.slug + '/']]}
	/>

	<section class="page-hero">
		<div class="wrap">
			<div class="crumbs">
				<a href={L("/")}>{t("Avaleht")}</a><span>/</span><a href={L("/rehvid/")}>{t("Rehvid")}</a><span>/</span>{data.size
					.label}
			</div>
			<h1>{t("Rehvid")} {data.size.label}</h1>
			<p>
				{data.n} {t("rehvimudelit EL-i rehvimärgise andmetega. Märghaardumise klass ütleb, kui lühikeseks jääb pidurdusmaa märjal teel — ja klass on selle mõõdu oma, mitte mudeli üldine.")}
			</p>
			<div class="pills">
				{#each data.klassid as [g, n] (g)}
					<span class="pill"><Grade {g} /> {n} {t("rehvi")}</span>
				{/each}
			</div>
		</div>
	</section>

	<div class="body-sec">
		<div class="wrap cols">
			<div>
				{#each data.grupid as gr (gr.ci)}
					<div class="box">
						<h2>{KAT[gr.ci] ?? ''}</h2>
						<p class="sub">{gr.list.length} {t("mudelit · järjestatud märghaardumise klassi, siis müra järgi")}</p>
						<div class="tbl-wrap">
							<table class="t">
								<thead>
									<tr><th>{t("Rehv")}</th><th>{t("Märghaare")}</th><th>{t("Veeretakistus")}</th><th class="n">{t("Müra")}</th><th>{t("Test")}</th></tr>
								</thead>
								<tbody>
									{#each gr.list as r, ri (r.slug + '#' + ri)}
										<tr>
											<td><a href={L("/rehvid/" + r.slug + "/")}>{r.nimi}</a></td>
											<td><Grade g={r.g} /></td>
											<td><Grade g={r.f} /></td>
											<td class="n">{r.db ? r.db + ' dB' : '–'}</td>
											<td
												>{#if r.tested}<span class="pill test">{t("Testitud")}</span>{:else}<span class="note">–</span>{/if}</td
											>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				{/each}
			</div>
			<aside class="side">
				<div class="box">
					<h2 style="font-size:22px">{t("Pidurdusmaa selles mõõdus")}</h2>
					<p class="note">{t("Arvuta, kui palju muudab märghaardumise klass sinu auto pidurdusmaad.")}</p>
					<a class="btn yel" style="width:100%" href={L("/") + "?moot=" + data.size.m}>{t("Arvuta selle mõõduga →")}</a>
					<a class="btn" style="width:100%;margin-top:var(--sp-2)" href={L("/vordle-rehve/") + "?moot=" + data.size.m}
						>{t("Võrdle selle mõõdu rehve")}</a
					>
					{#if data.talv}<a class="btn" style="width:100%;margin-top:var(--sp-2)" href={L('/talverehvid/' + data.talv + '/')}>{t('Parimad talverehvid {m}', { m: data.size.label })}</a>{/if}
					{#if data.cars.length}
						<h3
							style="font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:var(--sp-6) 0 var(--sp-2)"
						>
							{t("Tehasemõõt")} {data.autosid} {t("autol")}
						</h3>
						<ul class="note" style="margin:0;padding-left:var(--sp-5)">
							{#each data.cars as c (c.url)}<li><a href={L(c.url)}>{an(c.nimi)}</a>{#if !c.pohi}<span style="color:var(--muted)"> {t("· lisamõõt")}</span>{/if}</li>{/each}
						</ul>
						{#if data.autosid > data.cars.length}<p class="note">{t("…ja veel")} {data.autosid - data.cars.length}. <a href={L("/autod/")}>{t("Kõik autod")}</a></p>{/if}
					{/if}
				</div>
			</aside>
		</div>
	</div>
{:else if data.liik === 'rehv'}
	{@const ty = data.tyre}
	<Meta
		title={ty.name + t(' — pidurdusmaa, märgis ja testid')}
		desc={kirjeldus}
		path="rehvid/{ty.slug}/"
		canonical={data.canonical}
		image={data.ogPilt ? `/og/r/${ty.slug}.png` : undefined}
		noindex={data.noindex}
		crumbs={[
			[t('Avaleht'), '/'],
			[t('Rehvid'), '/rehvid/'],
			...(ty.brandSlug ? [[ty.brand, '/margid/' + ty.brandSlug + '/']] : []),
			[ty.name, '/rehvid/' + ty.slug + '/']
		]}
		jsonld={{
			'@context': 'https://schema.org',
			/* NB: mitte 'Product' — Google nõuab Productil hinda (offers), arvustust
			   või hinnangut, meil neid lehel pole (Search Console'i kriitiline viga).
			   Kui kunagi on lehel päris hinnad, võib Producti + offers tagasi panna. */
			'@type': 'WebPage',
			name: ty.name + t(' — pidurdusmaa, märgis ja testid'),
			description: kirjeldus,
			url: 'https://pidurdusmaa.ee' + L('/rehvid/' + ty.slug + '/'),
			inLanguage: keel.lang,
			about: { '@type': 'Brand', name: ty.brand }
		}}
	/>

	<section class="page-hero">
		<div class="wrap">
			<div class="crumbs">
				<a href={L("/")}>{t("Avaleht")}</a><span>/</span><a href={L("/rehvid/")}>{t("Rehvid")}</a><span>/</span>{#if ty.brandSlug}<a
						href="/margid/{ty.brandSlug}/">{ty.brand}</a
					><span>/</span>{/if}{ty.name}
			</div>
			<p class="eyebrow" style="color:var(--muted-d)">
				{#if ty.brandSlug}<a href="/margid/{ty.brandSlug}/" style="color:inherit">{ty.brand}</a>{:else}{ty.brand}{/if}
			</p>
			<h1>{ty.name}</h1>
			<p>
				{t(KAT_NIMI[ty.cat] ?? '')}
				{#if ty.oletus}
					· <span title={t("Märgisel on lumemärk, aga nimi ei ütle, kas talverehv või aastaringne rehv")}
						>{t("tüüp tuletatud")}</span
					>
				{/if}
			</p>
			<div class="pills">
				{#if data.sizes.length}<span class="pill off">{t("EL-i märgis ·")} {data.mootudeArv} {data.mootudeArv === 1 ? t('mõõt') : t('mõõtu')}</span>{/if}
				{#if data.tests.length || data.ext.length}<span class="pill test">{t("Sõltumatult testitud")}</span>{/if}
			</div>
		</div>
	</section>

	<div class="body-sec">
		<div class="wrap cols">
			<div>
				<div
					class="box"
					data-tw
					data-slug={ty.slug}
					data-name={ty.name}
					data-cat={ty.cat}
					data-tested={ty.testedKey}
					data-sizes={JSON.stringify(data.sizes.map((z) => ({ m: z.m, g: z.g })))}
				>
					<h2>{t("Pidurdusmaa sinu autoga")}</h2>
					<p class="sub">{@html t("Auto: <span data-tw-veh>…</span>")}</p>
					<div style="display:flex;gap:var(--sp-3);flex-wrap:wrap;align-items:center">
						<div class="fld">
							<select class="lsel" data-tw-size aria-label={t("Rehvimõõt")} style="min-width:220px"></select>
						</div>
						<div class="lseg" role="group" aria-label={t("Teeolud")}>
							{#each Object.entries(CONDS) as [k, c] (k)}
								<button type="button" data-tw-cond={k} aria-pressed={k === 'wet' ? 'true' : 'false'}
									>{t(c[0])}</button
								>
							{/each}
						</div>
					</div>
					<div data-tw-out><p class="note">{t("Arvutan…")}</p></div>
				</div>

				{#if data.tests.length}
					<div class="box">
						<h2>{t("Sõltumatud testid")}</h2>
						<p class="sub">
							{t("Mõõdetud tulemused. Koht = järjekoht samas testis samal pinnal (1 = lühim pidurdusmaa).")}
						</p>
						<div class="tbl-wrap">
							<table class="t">
								<thead>
									<tr><th>{t("Test")}</th><th>{t("Pind ja kiirus")}</th><th class="n">{t("Tulemus")}</th><th class="n">{t("Koht")}</th><th class="n">{t("Parim")}</th></tr>
								</thead>
								<tbody>
									{#each data.tests as x, xi (xi)}
										<tr class={x.pos === 1 ? 'best' : ''}>
											<td><a href="/testid/{x.src_slug}/">{t(x.src_nimi)}</a></td>
											<td>{tl(x)}</td>
											<td class="n"><b>{num(x.m)} {t('m')}</b></td>
											<td class="n">{x.pos ? x.pos + ' / ' + x.n : '–'}</td>
											<td class="n">{x.best != null ? num(x.best) + ' ' + t('m') : '–'}</td>
										</tr>
									{/each}
									{#if data.aqua}
										<tr>
											<td>{t(data.aqua.nimi)}</td>
											<td>{t("akvaplaneerimise kiirus (suurem = parem)")}</td>
											<td class="n"><b>{num(data.aqua.kmh)} {t('km/h')}</b></td>
											<td class="n">–</td>
											<td class="n">–</td>
										</tr>
									{/if}
								</tbody>
							</table>
						</div>
						<p class="srcline">
							{t("Test:")} {ty.testSize}{t(". Sama rehv võib teises mõõdus olla veidi teistsugune.")}
						</p>
					</div>
				{/if}

				{#if data.ext.length}
					<div class="box">
						<h2>{t("Ajakirjade testid")}</h2>
						<p class="sub">
							{t("Avaldatud pidurdusmaad (Auto Bild, auto motor und sport, Auto Zeitung, ADAC, Za Rulem jt). Koht = järjekoht samas testis samal pinnal (1 = lühim). Testid on eri mõõtudes, autodel ja tingimustes, seega võrdle numbreid ainult sama testi sees.")}
						</p>
						<div class="tbl-wrap">
							<table class="t">
								<thead>
									<tr><th>{t("Test")}</th><th>{t("Mõõt")}</th><th>{t("Katse")}</th><th class="n">{t("Tulemus")}</th><th class="n">{t("Koht")}</th><th class="n">{t("Parim")}</th></tr>
								</thead>
								<tbody>
									{#each data.ext as x, xi (xi)}
										<tr class={x.pos === 1 ? 'best' : ''}>
											<td>{#if x.src.url}<a href={x.src.url} rel="nofollow noopener" target="_blank">{x.src.pub} {x.src.year}</a>{:else}{x.src.pub} {x.src.year}{/if}</td>
											<td>{x.src.size || ''}</td>
											<td>{t(x.d)} {Math.round(x.v0)}→{Math.round(x.v1)} {t('km/h')}</td>
											<td class="n"><b>{num(x.m)} {t('m')}</b></td>
											<td class="n">{x.pos} / {x.n}</td>
											<td class="n">{num(x.best)} {t('m')}</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
						<p class="srcline">
							{t("Neid tulemusi lehe arvutus ei kasuta: meie kontroll näitas, et teises mõõdus tehtud test ei ennusta märja tee pidurdust paremini kui sinu mõõdu EL-i märgis. Need on siin mõõdetud faktina.")}
						</p>
					</div>
				{/if}

				{#if data.sizes.length}
					<div class="box">
						<h2>{t("EL-i rehvimärgis")}</h2>
						<p class="sub">
							{@html t("Ametlikud andmed EL-i tooteregistrist EPREL, mõõdu kaupa. Klass on mõõdupõhine. <a href=\"/teadmine/rehvimargis/\">Mida klassid tähendavad?</a>")}
						</p>
						<div class="tbl-wrap">
							<table class="t">
								<thead>
									<tr><th>{t("Mõõt")}</th><th>{t("Märghaardumine")}</th><th>{t("Veeretakistus")}</th><th class="n">{t("Müra")}</th><th>{t("Talv")}</th><th>{t("Koormus / kiirus")}</th></tr>
								</thead>
								<tbody>
									{#each data.sizes as z, zi (z.m + '#' + zi)}
										<tr>
											<td
												>{#if z.slug}<a href={L("/rehvid/" + z.slug + "/")}>{z.label}</a>{:else}{z.label}{/if}{#if z.v}
													<span class="note" title={t("Tootja variant (nt autotootja märgistus AO, MO või tugevdatud XL)")}
														>{z.v}</span
													>{/if}</td
											>
											<td>
												<Grade g={z.g} />
												{#if z.gAll && z.gAll.length > 1}
													<span
														class="note"
														title={t("Eri koormus-/kiirusindeksiga variandid on eri klassiga; näidatud halvim")}
														>{t("(variandid:")} {z.gAll.join(', ')})</span
													>
												{/if}
											</td>
											<td><Grade g={z.f} /></td>
											<td class="n">{z.db ? z.db + ' dB' + (z.nk ? ' (' + z.nk + ')' : '') : '–'}</td>
											<td
												>{[z.snow ? t('lumemärk') : '', z.ice ? t('jäämärk') : '']
													.filter(Boolean)
													.join(' + ') || '–'}</td
											>
											<td>{z.li.join('/') + ' ' + z.si.join('/')}</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				{/if}

				{#if data.vs.length}
					<div class="box">
						<h2>{t("Võrdle samas testis")}</h2>
						<p class="sub">{t("Rehvid, mis olid samas testis naabrid — sama auto, sama päev.")}</p>
						<div class="grid-cards">
							{#each data.vs as v (v.url)}
								<a class="tcard" href={v.url}
									><span class="b">vs</span><h3>{v.name}</h3><span class="meta"
										>{t("Mõõdetud pidurdusmaad kõrvuti →")}</span
									></a
								>
							{/each}
						</div>
					</div>
				{/if}
			</div>

			<aside class="side">
				<div class="box">
					<div class="tyre-img" role="img" aria-label={t("Rehvi illustratsioon")} data-rehv-pilt={ty.slug}>
						<TyreArt />
					</div>
					<p class="srcline" style="text-align:center" data-rehv-pilt-allkiri>{t("Illustratsioon.")}</p>
					{#if data.sizes.length}
						<button type="button" class="btn yel" style="width:100%;margin-top:var(--sp-4)" data-tw-add
							>{t("Võrdle seda rehvi →")}</button
						>
						<h3
							style="font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:var(--sp-6) 0 var(--sp-2)"
						>
							{t("Mõõdud andmebaasis")}
						</h3>
						<div class="sizes-list">
							{#each data.mootudUnik as z (z.m)}
								{#if z.slug}<a href={L("/rehvid/" + z.slug + "/")}>{z.label}</a>{/if}
							{/each}
						</div>
						<p class="srcline">
							{t("Andmebaasis on praegu ainult osa mõõtudest. Mudel võib olla müügil ka teistes.")}
						</p>
					{/if}
					{#if data.sobib.n}
						<h3
							style="font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:var(--sp-6) 0 var(--sp-2)"
						>
							{t("Sobib näiteks autodele")}
						</h3>
						<ul class="note" style="margin:0;padding-left:var(--sp-5)">
							{#each data.sobib.list as c (c.url)}<li><a href={L(c.url)}>{an(c.nimi)}</a> · {c.moot}</li>{/each}
						</ul>
						{#if data.sobib.n > data.sobib.list.length}<p class="srcline">{t("Kokku")} {data.sobib.n} {t("autot, mille tehase põhimõõt on selle rehvi mõõtude hulgas.")}</p>{/if}
					{/if}
				</div>
			</aside>
		</div>
	</div>
	<How />
{:else}
	<Meta
		title={data.a.name + ' vs ' + data.b.name + t(' — mõõdetud pidurdusmaad')}
		desc={t('Kaks rehvi samas sõltumatus testis, sama auto ja sama päev: {a} ja {b}. Pidurdusmaad märjal, kuival ja muudel pindadel.', { a: data.a.name, b: data.b.name })}
		path="rehvid/{data.a.slug}-vs-{data.b.slug}/"
		image="/og/vs/{data.a.slug}-vs-{data.b.slug}.png"
		crumbs={[
			[t('Avaleht'), '/'],
			[t('Rehvid'), '/rehvid/'],
			[data.a.name + ' vs ' + data.b.name, '/rehvid/' + data.a.slug + '-vs-' + data.b.slug + '/']
		]}
	/>

	<section class="page-hero">
		<div class="wrap">
			<div class="crumbs">
				<a href={L("/")}>{t("Avaleht")}</a><span>/</span><a href={L("/rehvid/")}>{t("Rehvid")}</a><span>/</span>{t("Võrdlus")}
			</div>
			<h1>{data.a.name} <span style="color:var(--yellow)">vs</span> {data.b.name}</h1>
			<p>
				{t("Mõlemad rehvid olid samas sõltumatus testis — sama auto, sama rada, sama päev. Siin on ainult mõõdetud tulemused.")}
			</p>
		</div>
	</section>
	<div class="body-sec">
		<div class="wrap">
			{#each data.plokid as p, pi (pi)}
				<div class="box">
					<h2>{t(p.src.nimi)}</h2>
					<p class="sub">{p.src.moot} · {p.src.auto} · {t(p.src.tegija)}</p>
					<div class="tbl-wrap">
						<table class="t">
							<thead>
								<tr><th>{t("Pind ja kiirus")}</th><th class="n">{data.a.name}</th><th class="n">{data.b.name}</th><th class="n">{t("Vahe")}</th></tr>
							</thead>
							<tbody>
								{#each p.read as r, rj (rj)}
									<tr>
										<td>{tl(r.x)}</td>
										<td
											class="n"
											style={r.x.m < r.y.m ? 'font-weight:700;box-shadow:inset 0 -3px 0 var(--yellow)' : ''}
											>{num(r.x.m)} {t('m')}</td
										>
										<td
											class="n"
											style={r.y.m < r.x.m ? 'font-weight:700;box-shadow:inset 0 -3px 0 var(--yellow)' : ''}
											>{num(r.y.m)} {t('m')}</td
										>
										<td class="n"
											>{(r.d > 0 ? '+' : '') + num(r.d)} {t('m')}
											<span class="note">({pctVahe(r.d, r.x.m, r.y.m)}%)</span></td
										>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					<p class="srcline">
						{t("Allikas:")} <a href={p.src.kajastus} rel="nofollow noopener">{t(p.src.nimi)}</a>{t(". Vahe = teine miinus esimene, protsent lühemast; lühem on parem.")}
					</p>
				</div>
			{/each}
			<div class="box">
				<h2>{t("Rehvide lehed")}</h2>
				<p>{t("Märgise andmed kõigis mõõtudes ja arvutatud pidurdusmaa sinu autoga.")}</p>
				<p>
					<a class="btn" href={L("/rehvid/" + data.a.slug + "/")}>{data.a.name} →</a>
					<a class="btn" href={L("/rehvid/" + data.b.slug + "/")}>{data.b.name} →</a>
				</p>
			</div>
		</div>
	</div>
{/if}
