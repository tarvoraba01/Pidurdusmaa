<script>
	import Meta from '$lib/Meta.svelte';
	import Grade from '$lib/Grade.svelte';
	import How from '$lib/How.svelte';
	import TyreArt from '$lib/TyreArt.svelte';
	import { KAT_NIMI, CONDS, num, pretty, testLabel } from '$lib/util.js';

	let { data } = $props();
	const KAT = { 0: 'Suverehvid', 1: 'Lamellrehvid', 2: 'Talverehvid (Kesk-Euroopa)', 3: 'Talverehvid (Põhjamaade)' };

	function pctVahe(d, x, y) {
		const p = (100 * d) / Math.min(x, y);
		return (d > 0 ? '+' : '') + num(p, Math.abs(p) < 10 ? 1 : 0);
	}
</script>

{#if data.liik === 'moot'}
	<Meta
		title="Rehvid {data.size.label} — {data.n} rehvimudelit märgise andmetega"
		desc="Kõik {data.size.label} mõõdus rehvid EL-i rehvimärgise järgi: märghaardumise klass, veeretakistus ja müra. Võrdle ja vaata, kui palju muutub pidurdusmaa."
		path="rehvid/{data.size.slug}/"
		noindex={data.noindex}
		crumbs={[['Avaleht', '/'], ['Rehvid', '/rehvid/'], [data.size.label, '/rehvid/' + data.size.slug + '/']]}
	/>

	<section class="page-hero">
		<div class="wrap">
			<div class="crumbs">
				<a href="/">Avaleht</a><span>/</span><a href="/rehvid/">Rehvid</a><span>/</span>{data.size
					.label}
			</div>
			<h1>Rehvid {data.size.label}</h1>
			<p>
				{data.n} rehvimudelit EL-i rehvimärgise andmetega. Märghaardumise klass ütleb, kui lühikeseks
				jääb pidurdusmaa märjal teel — ja klass on selle mõõdu oma, mitte mudeli üldine.
			</p>
			<div class="pills">
				{#each data.klassid as [g, n] (g)}
					<span class="pill"><Grade {g} /> {n} rehvi</span>
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
						<p class="sub">{gr.list.length} mudelit · järjestatud märghaardumise klassi, siis müra järgi</p>
						<div class="tbl-wrap">
							<table class="t">
								<thead>
									<tr><th>Rehv</th><th>Märghaare</th><th>Veeretakistus</th><th class="n">Müra</th><th>Test</th></tr>
								</thead>
								<tbody>
									{#each gr.list as r, ri (r.slug + '#' + ri)}
										<tr>
											<td><a href="/rehvid/{r.slug}/">{r.nimi}</a></td>
											<td><Grade g={r.g} /></td>
											<td><Grade g={r.f} /></td>
											<td class="n">{r.db ? r.db + ' dB' : '–'}</td>
											<td
												>{#if r.tested}<span class="pill test">Testitud</span>{:else}<span class="note">–</span>{/if}</td
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
					<h2 style="font-size:22px">Pidurdusmaa selles mõõdus</h2>
					<p class="note">Arvuta, kui palju muudab märghaardumise klass sinu auto pidurdusmaad.</p>
					<a class="btn yel" style="width:100%" href="/?moot={data.size.m}">Arvuta selle mõõduga →</a>
					<a class="btn" style="width:100%;margin-top:var(--sp-2)" href="/vordle-rehve/?moot={data.size.m}"
						>Võrdle selle mõõdu rehve</a
					>
					{#if data.cars.length}
						<h3
							style="font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:var(--sp-6) 0 var(--sp-2)"
						>
							Tehase mõõt näiteks
						</h3>
						<ul class="note" style="margin:0;padding-left:var(--sp-5)">
							{#each data.cars as c}<li>{c}</li>{/each}
						</ul>
					{/if}
				</div>
			</aside>
		</div>
	</div>
{:else if data.liik === 'rehv'}
	{@const t = data.tyre}
	<Meta
		title="{t.name} — pidurdusmaa, märgis ja testid"
		desc={data.desc}
		path="rehvid/{t.slug}/"
		canonical={data.canonical}
		noindex={data.noindex}
		crumbs={[['Avaleht', '/'], ['Rehvid', '/rehvid/'], [t.name, '/rehvid/' + t.slug + '/']]}
		jsonld={{
			'@context': 'https://schema.org',
			'@type': 'Product',
			name: t.name,
			brand: { '@type': 'Brand', name: t.brand },
			category: KAT_NIMI[t.cat] ?? 'Rehv',
			url: 'https://pidurdusmaa.ee/rehvid/' + t.slug + '/',
			additionalProperty: data.sizes.slice(0, 20).map((z) => ({
				'@type': 'PropertyValue',
				name: 'EL rehvimärgis ' + z.label,
				value: 'märghaardumine ' + z.g + ', veeretakistus ' + z.f + ', müra ' + z.db + ' dB'
			}))
		}}
	/>

	<section class="page-hero">
		<div class="wrap">
			<div class="crumbs">
				<a href="/">Avaleht</a><span>/</span><a href="/rehvid/">Rehvid</a><span>/</span>{t.name}
			</div>
			<p class="eyebrow" style="color:var(--muted-d)">{t.brand}</p>
			<h1>{t.name}</h1>
			<p>
				{KAT_NIMI[t.cat] ?? ''}
				{#if t.oletus}
					· <span title="Märgisel on lumemärk, aga nimi ei ütle, kas talve- või lamellrehv"
						>tüüp tuletatud</span
					>
				{/if}
			</p>
			<div class="pills">
				{#if data.sizes.length}<span class="pill off">EL-i märgis · {data.sizes.length} mõõtu</span>{/if}
				{#if data.tests.length}<span class="pill test">Sõltumatult testitud</span>{/if}
			</div>
		</div>
	</section>

	<div class="body-sec">
		<div class="wrap cols">
			<div>
				<div
					class="box"
					data-tw
					data-slug={t.slug}
					data-name={t.name}
					data-cat={t.cat}
					data-tested={t.testedKey}
					data-sizes={JSON.stringify(data.sizes.map((z) => ({ m: z.m, g: z.g })))}
				>
					<h2>Pidurdusmaa sinu autoga</h2>
					<p class="sub">Auto: <span data-tw-veh>…</span></p>
					<div style="display:flex;gap:var(--sp-3);flex-wrap:wrap;align-items:center">
						<div class="fld">
							<select class="lsel" data-tw-size aria-label="Rehvimõõt" style="min-width:220px"></select>
						</div>
						<div class="lseg" role="group" aria-label="Teeolud">
							{#each Object.entries(CONDS) as [k, c] (k)}
								<button type="button" data-tw-cond={k} aria-pressed={k === 'wet' ? 'true' : 'false'}
									>{c[0]}</button
								>
							{/each}
						</div>
					</div>
					<div data-tw-out><p class="note">Arvutan…</p></div>
				</div>

				{#if data.tests.length}
					<div class="box">
						<h2>Sõltumatud testid</h2>
						<p class="sub">
							Mõõdetud tulemused. Koht = järjekoht samas testis samal pinnal (1 = lühim pidurdusmaa).
						</p>
						<div class="tbl-wrap">
							<table class="t">
								<thead>
									<tr><th>Test</th><th>Pind ja kiirus</th><th class="n">Tulemus</th><th class="n">Koht</th><th class="n">Parim</th></tr>
								</thead>
								<tbody>
									{#each data.tests as x, xi (xi)}
										<tr class={x.pos === 1 ? 'best' : ''}>
											<td><a href="/testid/{x.src_slug}/">{x.src_nimi}</a></td>
											<td>{testLabel(x)}</td>
											<td class="n"><b>{num(x.m)} m</b></td>
											<td class="n">{x.pos ? x.pos + ' / ' + x.n : '–'}</td>
											<td class="n">{x.best != null ? num(x.best) + ' m' : '–'}</td>
										</tr>
									{/each}
									{#if data.aqua}
										<tr>
											<td>{data.aqua.nimi}</td>
											<td>akvaplaneerimise kiirus (suurem = parem)</td>
											<td class="n"><b>{num(data.aqua.kmh)} km/h</b></td>
											<td class="n">–</td>
											<td class="n">–</td>
										</tr>
									{/if}
								</tbody>
							</table>
						</div>
						<p class="srcline">
							Test: {t.testSize}. Sama rehv võib teises mõõdus olla veidi teistsugune.
						</p>
					</div>
				{/if}

				{#if data.sizes.length}
					<div class="box">
						<h2>EL-i rehvimärgis</h2>
						<p class="sub">
							Ametlikud andmed EL-i tooteregistrist EPREL, mõõdu kaupa. Klass on mõõdupõhine.
							<a href="/teadmine/rehvimargis/">Mida klassid tähendavad?</a>
						</p>
						<div class="tbl-wrap">
							<table class="t">
								<thead>
									<tr><th>Mõõt</th><th>Märghaardumine</th><th>Veeretakistus</th><th class="n">Müra</th><th>Talv</th><th>Koormus / kiirus</th></tr>
								</thead>
								<tbody>
									{#each data.sizes as z, zi (z.m + '#' + zi)}
										<tr>
											<td
												>{#if z.slug}<a href="/rehvid/{z.slug}/">{z.label}</a>{:else}{z.label}{/if}</td
											>
											<td>
												<Grade g={z.g} />
												{#if z.gAll && z.gAll.length > 1}
													<span
														class="note"
														title="Eri koormus-/kiirusindeksiga variandid on eri klassiga; näidatud halvim"
														>(variandid: {z.gAll.join(', ')})</span
													>
												{/if}
											</td>
											<td><Grade g={z.f} /></td>
											<td class="n">{z.db ? z.db + ' dB' + (z.nk ? ' (' + z.nk + ')' : '') : '–'}</td>
											<td
												>{[z.snow ? 'lumemärk' : '', z.ice ? 'jäämärk' : '']
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
						<h2>Võrdle samas testis</h2>
						<p class="sub">Rehvid, mis olid samas testis naabrid — sama auto, sama päev.</p>
						<div class="grid-cards">
							{#each data.vs as v (v.url)}
								<a class="tcard" href={v.url}
									><span class="b">vs</span><h3>{v.name}</h3><span class="meta"
										>Mõõdetud pidurdusmaad kõrvuti →</span
									></a
								>
							{/each}
						</div>
					</div>
				{/if}
			</div>

			<aside class="side">
				<div class="box">
					<div class="tyre-img" role="img" aria-label="Rehvi illustratsioon"><TyreArt /></div>
					<p class="srcline" style="text-align:center">Illustratsioon. Tootja pilte ei kasutata.</p>
					{#if data.sizes.length}
						<button type="button" class="btn yel" style="width:100%;margin-top:var(--sp-4)" data-tw-add
							>Võrdle seda rehvi →</button
						>
						<h3
							style="font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:var(--sp-6) 0 var(--sp-2)"
						>
							Mõõdud andmebaasis
						</h3>
						<div class="sizes-list">
							{#each data.sizes as z, zi (z.m + '#' + zi)}
								{#if z.slug}<a href="/rehvid/{z.slug}/">{z.label}</a>{/if}
							{/each}
						</div>
						<p class="srcline">
							Andmebaasis on praegu ainult osa mõõtudest. Mudel võib olla müügil ka teistes.
						</p>
					{/if}
				</div>
			</aside>
		</div>
	</div>
	<How />
{:else}
	<Meta
		title="{data.a.name} vs {data.b.name} — mõõdetud pidurdusmaad"
		desc="Kaks rehvi samas sõltumatus testis, sama auto ja sama päev: {data.a.name} ja {data.b
			.name}. Pidurdusmaad märjal, kuival ja muudel pindadel."
		path="rehvid/{data.a.slug}-vs-{data.b.slug}/"
		crumbs={[
			['Avaleht', '/'],
			['Rehvid', '/rehvid/'],
			[data.a.name + ' vs ' + data.b.name, '/rehvid/' + data.a.slug + '-vs-' + data.b.slug + '/']
		]}
	/>

	<section class="page-hero">
		<div class="wrap">
			<div class="crumbs">
				<a href="/">Avaleht</a><span>/</span><a href="/rehvid/">Rehvid</a><span>/</span>Võrdlus
			</div>
			<h1>{data.a.name} <span style="color:var(--yellow)">vs</span> {data.b.name}</h1>
			<p>
				Mõlemad rehvid olid samas sõltumatus testis — sama auto, sama rada, sama päev. Siin on ainult
				mõõdetud tulemused.
			</p>
		</div>
	</section>
	<div class="body-sec">
		<div class="wrap">
			{#each data.plokid as p, pi (pi)}
				<div class="box">
					<h2>{p.src.nimi}</h2>
					<p class="sub">{p.src.moot} · {p.src.auto} · {p.src.tegija}</p>
					<div class="tbl-wrap">
						<table class="t">
							<thead>
								<tr><th>Pind ja kiirus</th><th class="n">{data.a.name}</th><th class="n">{data.b.name}</th><th class="n">Vahe</th></tr>
							</thead>
							<tbody>
								{#each p.read as r, rj (rj)}
									<tr>
										<td>{testLabel(r.x)}</td>
										<td
											class="n"
											style={r.x.m < r.y.m ? 'font-weight:700;box-shadow:inset 0 -3px 0 var(--yellow)' : ''}
											>{num(r.x.m)} m</td
										>
										<td
											class="n"
											style={r.y.m < r.x.m ? 'font-weight:700;box-shadow:inset 0 -3px 0 var(--yellow)' : ''}
											>{num(r.y.m)} m</td
										>
										<td class="n"
											>{(r.d > 0 ? '+' : '') + num(r.d)} m
											<span class="note">({pctVahe(r.d, r.x.m, r.y.m)} %)</span></td
										>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					<p class="srcline">
						Allikas: <a href={p.src.kajastus} rel="nofollow noopener">{p.src.nimi}</a>. Vahe = teine
						miinus esimene, protsent lühemast; lühem on parem.
					</p>
				</div>
			{/each}
			<div class="box">
				<h2>Rehvide lehed</h2>
				<p>Märgise andmed kõigis mõõtudes ja arvutatud pidurdusmaa sinu autoga.</p>
				<p>
					<a class="btn" href="/rehvid/{data.a.slug}/">{data.a.name} →</a>
					<a class="btn" href="/rehvid/{data.b.slug}/">{data.b.name} →</a>
				</p>
			</div>
		</div>
	</div>
{/if}
