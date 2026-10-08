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
	import { graph } from '$lib/skeem.js';

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

	/* mõõdulehe KKK: vastused ainult lehe andmetest (märgis, mudel, autod) */
	const ja = (a) => (a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' ' + t('ja') + ' ' + a[a.length - 1]);
	const mootKkk = $derived.by(() => {
		if (data.liik !== 'moot') return [];
		const m = data.size.label, out = [];
		if (data.parimG && data.parimad.length) {
			out.push([
				t('Milline {m} rehv on märjal kõige parem?', { m }),
				(data.parimG === 'A'
					? t('EL-i rehvimärgise järgi on {m} mõõdus {n} mudelil märghaardumise klass A, näiteks {nimed}.', { m, n: data.parimN, nimed: ja(data.parimad) })
					: t('{m} mõõdus on parim märghaardumise klass {g} ({n} mudelit), näiteks {nimed}.', { m, g: data.parimG, n: data.parimN, nimed: ja(data.parimad) })) +
					' ' + t('Klass on mõõdupõhine: sama mudel võib teises mõõdus olla teise klassiga.')
			]);
		}
		if (data.vahe) {
			const v = data.vahe;
			out.push([
				t('Kui palju lühem on pidurdusmaa parema märgise klassiga?'),
				t('{auto} pidurdusmaa märjal asfaldil 80 km/h pealt: {g1}-klassi rehviga {d1} m, {g2}-klassi rehviga {d2} m. Vahe on {dv} m.', { auto: an(v.auto), g1: v.g1, g2: v.g2, d1: num(v.d1), d2: num(v.d2), dv: num(v.vahe) }) +
					' ' + t('Rehvitüüp: {tyyp}. Arvutatud sama mudeliga mis kalkulaator; oma auto tulemust näed kalkulaatoris.', { tyyp: ((x) => x.charAt(0).toLowerCase() + x.slice(1))(t(KAT_NIMI[v.kat])) })
			]);
		}
		if (data.cars.length) {
			out.push([
				t('Millistel autodel on {m} tehasemõõt?', { m }),
				t('Andmebaasis on {m} tehasemõõt {n} autol, näiteks {autod}.', { m, n: data.autosid, autod: ja(data.cars.slice(0, 4).map((c) => an(c.nimi))) })
			]);
		}
		if (data.sarnased.length) {
			out.push([
				t('Milliseid mõõte saab {m} asemel kasutada?', { m }),
				t('Sama välisläbimõõduga (vahe kuni 1,5%) on näiteks {moodud}.', { moodud: ja(data.sarnased.slice(0, 4).map((z) => z.label)) }) +
					' ' + t('Enne vahetamist kontrolli, kas mõõt on sinu auto lubatud mõõtude seas (registreerimistunnistus või tootja andmed).')
			]);
		}
		return out;
	});
	const mootLd = $derived(
		data.liik === 'moot' && (mootKkk.length || data.parimadLd?.length)
			? graph(
					...(mootKkk.length ? [{ '@type': 'FAQPage', mainEntity: mootKkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) }] : []),
					...(data.parimadLd?.length
						? [{ '@type': 'ItemList', name: t('Parima märghaardumise klassiga ({g}) rehvid mõõdus {m}', { g: data.parimG, m: data.size.label }), itemListElement: data.parimadLd.map((r, i) => ({ '@type': 'ListItem', position: i + 1, name: r.nimi, url: 'https://pidurdusmaa.ee' + L('/rehvid/' + r.slug + '/') })) }]
						: [])
				)
			: undefined
	);

	/* rehvilehe KKK: vastused ainult lehe andmetest (märgis, testid, mõõdud, autod) */
	const PIND = { ASPHALT: ['kuival asfaldil', 'märjal asfaldil'], CONCRETE: ['märjal betoonil', 'märjal betoonil'], ICE: ['jääl', 'jääl'], SNOW_PACKED: ['lumel', 'lumel'] };
	const rehvKkk = $derived.by(() => {
		if (data.liik !== 'rehv' || !data.tyre) return [];
		const ty = data.tyre, out = [];
		const gs = [...new Set(data.sizes.map((z) => z.g).filter(Boolean))].sort();
		if (gs.length) {
			const g = gs.length === 1 ? gs[0] : gs[0] + '–' + gs[gs.length - 1];
			out.push([
				t('Milline on {rehv} märghaardumise klass?', { rehv: ty.name }),
				(gs.length === 1 ? t('EL-i rehvimärgisel on {rehv} märghaardumise klass {g} kõigis andmebaasi mõõtudes.', { rehv: ty.name, g }) : t('EL-i rehvimärgisel on {rehv} märghaardumise klass {g}, olenevalt mõõdust.', { rehv: ty.name, g })) +
					' ' + t('A on parim ja E halvim; A- ja E-klassi vahe on märjal 90 km/h pealt umbes 18 m pidurdusmaad.')
			]);
		}
		if (data.vastusTalv) {
			const v = data.vastus, w = data.vastusTalv;
			out.push([
				w.pind === 'ice' ? t('Kui pikk on {rehv} pidurdusmaa jääl?', { rehv: ty.name }) : t('Kui pikk on {rehv} pidurdusmaa lumel?', { rehv: ty.name }),
				(w.pind === 'ice'
					? t('Sõltumatu testi järgi peatub {rehv} {moot} jääl 50 km/h pealt umbes {d} meetriga ({auto}, ilma reaktsiooniajata).', { rehv: ty.name, moot: v.moot, d: num(w.d), auto: an(v.auto) })
					: t('Sõltumatu testi järgi peatub {rehv} {moot} tallatud lumel 50 km/h pealt umbes {d} meetriga ({auto}, ilma reaktsiooniajata).', { rehv: ty.name, moot: v.moot, d: num(w.d), auto: an(v.auto) })) +
					' ' + t('Arvutatud sama mudeliga mis kalkulaator; oma autoga näed tulemust kalkulaatoris.')
			]);
		}
		if (data.parimTest) {
			const k = data.parimTest, pind = (PIND[k.surf] || [String(k.surf).toLowerCase()])[k.wet ? 1 : 0];
			out.push([
				t('Kas {rehv} on sõltumatult testitud?', { rehv: ty.name }),
				t('Jah. Testis {test} sai {rehv} {pind} {v} km/h pealt pidurdusmaaks {m} m, mis andis {pos}. koha {n} rehvi seas.', { test: t(k.src), rehv: ty.name, pind: t(pind), v: Math.round(k.v0), m: num(k.m), pos: k.pos, n: k.n }) +
					(data.tests.length > 1 ? ' ' + t('Kõik mõõdetud tulemused on tabelis ülal.') : '')
			]);
		} else if (!data.tests.length && !data.ext.length && data.sizes.length) {
			out.push([
				t('Kas {rehv} on sõltumatult testitud?', { rehv: ty.name }),
				t('Meie andmebaasis selle mudeli kohta sõltumatut pidurdustesti ei ole. Pidurdusmaa arvutatakse EL-i rehvimärgise märghaardumise klassi järgi, mis on mõõdupõhine ametlik mõõtmine.')
			]);
		}
		if (data.mootudUnik.length) {
			const n = data.mootudeArv, list = data.mootudUnik.slice(0, 6).map((z) => z.label);
			out.push([
				t('Mis mõõtudes {rehv} on olemas?', { rehv: ty.name }),
				t(n === 1 ? 'EL-i rehviregistris on {rehv} andmebaasis {n} mõõdus: {list}.' : 'EL-i rehviregistris on {rehv} andmebaasis {n} mõõdus, näiteks {list}.', { rehv: ty.name, n, list: ja(list) }) +
					(data.sobib.n ? ' ' + t('Tehase põhimõõduna sobib see näiteks autodele {autod}.', { autod: ja(data.sobib.list.slice(0, 3).map((c) => an(c.nimi))) }) : '')
			]);
		}
		return out;
	});
	const rehvLd = $derived(
		data.liik === 'rehv' && data.tyre
			? graph(
					{
						/* NB: mitte 'Product' — Google nõuab Productil hinda (offers), arvustust
						   või hinnangut, meil neid lehel pole (Search Console'i kriitiline viga). */
						'@type': 'WebPage',
						name: data.tyre.name + t(' — pidurdusmaa, märgis ja testid'),
						description: kirjeldus,
						url: 'https://pidurdusmaa.ee' + L('/rehvid/' + data.tyre.slug + '/'),
						inLanguage: keel.lang,
						about: { '@type': 'Brand', name: data.tyre.brand }
					},
					...(rehvKkk.length ? [{ '@type': 'FAQPage', mainEntity: rehvKkk.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) }] : [])
				)
			: undefined
	);

	/* vs-leht: üks lause, kumb oli lühem (tsiteeritav), + KKK */
	const vsVastus = $derived.by(() => {
		if (data.liik !== 'vs' || !data.kokku || !data.kokku.pea) return '';
		const k = data.kokku, p = k.pea, A = data.a.name, B = data.b.name;
		const pind = t((PIND[p.surf] || [String(p.surf).toLowerCase()])[p.wet ? 1 : 0]);
		const voit = p.am < p.bm ? A : B, kaot = p.am < p.bm ? B : A;
		const pea = p.am === p.bm
			? t('{pind} {v} km/h pealt peatusid {a} ja {b} ühepikkuselt: {m} m ({test}).', { pind: pind.charAt(0).toUpperCase() + pind.slice(1), v: Math.round(p.v0), a: A, b: B, m: num(p.am), test: t(p.src) })
			: t('{pind} {v} km/h pealt peatus {voit} {d} m lühemalt kui {kaot}: {am} m vs {bm} m ({test}).', { pind: pind.charAt(0).toUpperCase() + pind.slice(1), v: Math.round(p.v0), voit, kaot, d: num(p.d), am: num(Math.min(p.am, p.bm)), bm: num(Math.max(p.am, p.bm)), test: t(p.src) });
		const koond = k.n > 1 ? ' ' + (k.a === k.b ? t('Kokku {n} mõõtmist: kumbki oli lühem {a} korral.', { n: k.n, a: k.a }) : t('Kokku {n} mõõtmist: {voit} oli lühem {x} korral, {kaot} {y} korral.', { n: k.n, voit: k.a > k.b ? A : B, kaot: k.a > k.b ? B : A, x: Math.max(k.a, k.b), y: Math.min(k.a, k.b) })) : '';
		return pea + koond;
	});
	const vsLd = $derived(
		data.liik === 'vs' && vsVastus
			? graph({ '@type': 'FAQPage', mainEntity: [{ '@type': 'Question', name: t('Kumb on parem: {a} või {b}?', { a: data.a.name, b: data.b.name }), acceptedAnswer: { '@type': 'Answer', text: vsVastus + ' ' + t('Lühem pidurdusmaa on parem; vahe sõltub pinnast, nii et vaata tabelist seda pinda, millel sa päriselt sõidad.') } }] })
			: undefined
	);

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
		jsonld={mootLd}
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
				{#if data.parimG === 'A'}{t('Klass A on {n} mudelil.', { n: data.parimN })}{/if}
				{#if data.nTest}{data.nTest === 1 ? t('1 mudel on olnud sõltumatus pidurdustestis.') : t('{n} mudelit on olnud sõltumatus pidurdustestis.', { n: data.nTest })}{/if}
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
				{#if mootKkk.length}
					<div class="box">
						<h2>{t('Korduma kippuvad küsimused')}</h2>
						{#each mootKkk as [q, a] (q)}<h3 style="font-size:17px;margin:var(--sp-4) 0 var(--sp-1)">{q}</h3><p style="margin:0">{a}</p>{/each}
					</div>
				{/if}
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
					<a class="btn" style="width:100%;margin-top:var(--sp-2)" href={L('/rehvi-kalkulaator/') + '?a=' + data.size.slug}>{t('Rehvimõõdu kalkulaator')}</a>
					{#if data.sarnased.length}
						<h3
							style="font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:var(--sp-6) 0 var(--sp-2)"
						>
							{t('Sama läbimõõduga mõõdud')}
						</h3>
						<ul class="note" style="margin:0;padding-left:var(--sp-5)">
							{#each data.sarnased as z (z.slug)}<li><a href={L('/rehvid/' + z.slug + '/')}>{z.label}</a> <span style="color:var(--muted)">{z.v > 0 ? '+' : ''}{num(z.v)} %</span></li>{/each}
						</ul>
					{/if}
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
		jsonld={rehvLd}

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
				{#if ty.pood}
					· <span title={t("Seda mudelit EL-i registris EPREL ei ole; märgise klassid on müüja kataloogist")}
						>{t("märgis poe andmetel")}</span
					>
				{/if}
			</p>
			{#if data.vastus}
				{@const v = data.vastus}
				<p class="vastus">
					{t('{rehv} {moot}: pidurdusmaa märjal teel 90 km/h pealt umbes {d} m', { rehv: ty.name, moot: v.moot, d: v.d })}
					<span class="vastus-alus">({t('{auto}, ilma reaktsiooniajata', { auto: an(v.auto) })}; {v.test ? t('sõltumatu testi järgi') : t('EL-i märgise klassi {g} järgi', { g: v.g })})</span>
				</p>
				{#if data.vastusTalv}
					<p class="vastus" style="margin-top:0">
						{data.vastusTalv.pind === 'ice' ? t('Jääl 50 km/h pealt umbes {d} m', { d: num(data.vastusTalv.d) }) : t('Tallatud lumel 50 km/h pealt umbes {d} m', { d: num(data.vastusTalv.d) })}
						<span class="vastus-alus">({t('sõltumatu testi järgi')})</span>
					</p>
				{/if}
			{/if}
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
											<td>{t(x.d)} {#if x.v0 != null}{Math.round(x.v0)}→{Math.round(x.v1)} {t('km/h')}{:else}<span class="note">· {t('kiirus märkimata')}</span>{/if}</td>
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
							{#if ty.pood}
								{@html t("Märgise klassid müüja ({pood}) kataloogist, mõõdu kaupa — seda mudelit EL-i registris EPREL ei ole. Sama tootja deklaratsioon, aga käsitsi sisestatud. <a href=\"/teadmine/rehvimargis/\">Mida klassid tähendavad?</a>", { pood: ty.pood })}
							{:else}
							{@html t("Ametlikud andmed EL-i tooteregistrist EPREL, mõõdu kaupa. Klass on mõõdupõhine. <a href=\"/teadmine/rehvimargis/\">Mida klassid tähendavad?</a>")}
							{/if}
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

				{#if rehvKkk.length}
					<div class="box">
						<h2>{t('Korduma kippuvad küsimused')}</h2>
						{#each rehvKkk as [q, a] (q)}<h3 style="font-size:17px;margin:var(--sp-4) 0 var(--sp-1)">{q}</h3><p style="margin:0">{a}</p>{/each}
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
						<!-- poed: täidab app.js (rehviPilt → /api/rehv/<slug>/), peidus kui hindu pole -->
						<div class="rp-poed" data-rehv-poed data-nimi={ty.name} hidden>
							<h3>{t('Kus osta')}</h3>
							<div class="rp-list" data-rehv-poed-list></div>
							<p class="srcline">{t('Hinnad poodidest, uuenevad mitu korda päevas. Järjestus pidurdusmaa järgi ei sõltu poest.')}</p>
						</div>
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
					<p class="srcline" style="margin-top:var(--sp-5)">
						{t('Kas sinu praegused rehvid on veel head?')} <a href={L('/rehvi-vanus/')}>{t('Kontrolli rehvi vanust DOT-koodist')}</a>
					</p>
				</div>
			</aside>
		</div>
	</div>
	<How />
{:else}
	<Meta
		title={data.a.name + ' vs ' + data.b.name + t(' — mõõdetud pidurdusmaad')}
		desc={(vsVastus ? vsVastus + ' ' : '') + t('Kaks rehvi samas sõltumatus testis, sama auto ja sama päev: {a} ja {b}. Pidurdusmaad märjal, kuival ja muudel pindadel.', { a: data.a.name, b: data.b.name })}
		path="rehvid/{data.a.slug}-vs-{data.b.slug}/"
		jsonld={vsLd}
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
			{#if vsVastus}<p class="vastus">{vsVastus}</p>{/if}
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
			{#if vsVastus}
				<div class="box">
					<h2>{t('Kumb on parem: {a} või {b}?', { a: data.a.name, b: data.b.name })}</h2>
					<p style="margin:0">{vsVastus} {t('Lühem pidurdusmaa on parem; vahe sõltub pinnast, nii et vaata tabelist seda pinda, millel sa päriselt sõidad.')}</p>
				</div>
			{/if}
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

<style>
	.vastus { font-size: 17px; font-weight: 600; max-width: 62ch; margin: 6px 0 10px; }
	.vastus-alus { font-weight: 400; color: var(--muted-d, inherit); font-size: 14px; }
	.rp-poed { margin-top: var(--sp-5); }
	.rp-poed h3 { font-size: 13px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin: 0 0 var(--sp-2); }
	.rp-list { display: grid; gap: var(--sp-2); }
	:global(.rp-pood) { display: grid; grid-template-columns: 1fr auto; gap: 2px var(--sp-2); align-items: center; padding: 10px 12px; border: 1px solid var(--line); border-radius: 10px; text-decoration: none; color: var(--text); background: #fff; }
	:global(.rp-pood:hover) { border-color: var(--yellow); }
	:global(.rp-pood b) { font-weight: 800; }
	:global(.rp-pood .h) { font-family: var(--display); font-weight: 700; font-size: 20px; text-align: right; }
	:global(.rp-pood small) { color: var(--muted); font-size: 12.5px; }
	:global(.rp-pood .v) { color: var(--text); font-weight: 700; font-size: 13px; text-align: right; }
</style>
