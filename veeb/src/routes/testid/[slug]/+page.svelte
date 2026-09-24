<script>
	import Meta from '$lib/Meta.svelte';
	import { num } from '$lib/util.js';
	let { data } = $props();
	const s = data.src;
</script>

<Meta
	title="{s.nimi} — tulemused"
	desc="{s.nimi}: {s.rehve} rehvi, {s.moot}, {s.auto}. Mõõdetud pidurdusmaad ({s.protokoll})."
	path="testid/{s.slug}/"
	crumbs={[['Avaleht', '/'], ['Testid', '/testid/'], [s.nimi, '/testid/' + s.slug + '/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs">
			<a href="/">Avaleht</a><span>/</span><a href="/testid/">Testid</a><span>/</span>{s.nimi}
		</div>
		<p class="eyebrow" style="color:var(--muted-d)">{s.tegija} · {s.aasta}</p>
		<h1>{s.nimi}</h1>
		<p>{s.rehve} rehvi · {s.moot} · {s.auto}</p>
		<div class="pills">
			<span class="pill test">Sõltumatu test</span><span class="pill">{s.protokoll}</span>
		</div>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		{#if data.list.length}
			<div class="box">
				<h2>Tulemused</h2>
				<p class="sub">
					Pidurdusmaa meetrites (lühem = parem){data.wet ? ', järjestatud märja asfaldi järgi' : ''}.
					Kollane = parim veerus.
				</p>
				<div class="tbl-wrap">
					<table class="t">
						<thead>
							<tr>
								<th>#</th><th>Rehv</th>
								{#each data.cols as [k, label] (k)}<th class="n">{label}</th>{/each}
							</tr>
						</thead>
						<tbody>
							{#each data.list as r, i (r.slug + '#' + i)}
								<tr>
									<td>{i + 1}</td>
									<td><a href="/rehvid/{r.slug}/">{r.name}</a></td>
									{#each data.cols as [k] (k)}
										<td
											class="n"
											style={r.v[k] != null && r.v[k] === data.best[k]
												? 'font-weight:700;box-shadow:inset 0 -3px 0 var(--yellow)'
												: ''}>{r.v[k] != null ? num(r.v[k]) : '–'}</td
										>
									{/each}
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{:else if data.vib}
			<div class="box">
				<h2>Tulemused</h2>
				<p class="sub">
					Pidurdusmaa meetrites. Neid rehve mudeli rehvinimekirjas ei ole — test on kasutusel mudeli
					kontrollina.
				</p>
				<div class="tbl-wrap">
					<table class="t">
						<thead>
							<tr><th>Rehv</th>{#each data.vib.cols as c}<th class="n">{c}</th>{/each}</tr>
						</thead>
						<tbody>
							{#each data.vib.rows as r}
								<tr>
									<td>{r[0]}</td>
									{#each r.slice(1) as v}<td class="n">{num(v)}</td>{/each}
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/if}
		<div class="box">
			<h2>Allikas</h2>
			{#if s.markus}<p class="note-box">{s.markus}</p>{/if}
			<p class="srcline">
				Kajastus: <a href={s.kajastus} rel="nofollow noopener">{s.host}</a>
			</p>
		</div>
	</div>
</div>
