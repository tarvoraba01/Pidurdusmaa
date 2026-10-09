<script>
	import Meta from '$lib/Meta.svelte';
	import { useT, useLang, autoNimi } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	const L = keel.L;
	const an = (s) => autoNimi(keel.lang, s);
	let { data } = $props();
	const m = $derived(data.mark);
	const path = $derived('/autod/' + m.slug + '/');
	const KEHA = { SOIDUAUTO: 'sõiduauto', MAASTUR: 'maastur', KAUBIK: 'kaubik', VAIKEAUTO: 'väikeauto' };
	const S = $derived(data.sissejuhatus);
	const ja = (a) => (a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' ' + t('ja') + ' ' + a[a.length - 1]);
	const kg = (x) => x.toLocaleString(keel.lang === 'ru' ? 'ru-RU' : 'et-EE');
	/* arv + õige käändega sõna (et: 1 mudel / 2 mudelit; ru: модель/модели/моделей) */
	const SONA = {
		et: { mudel: ['mudel', 'mudelit'], polv: ['põlvkond', 'põlvkonda'] },
		ru: { mudel: { one: 'модель', few: 'модели', many: 'моделей', other: 'модели' }, polv: { one: 'поколение', few: 'поколения', many: 'поколений', other: 'поколения' } }
	};
	const arv = (n, s) => {
		if (keel.lang === 'ru') return n + ' ' + SONA.ru[s][new Intl.PluralRules('ru-RU').select(n)];
		if (keel.lang === 'en') return n + ' ' + (s === 'mudel' ? (n === 1 ? 'model' : 'models') : n === 1 ? 'generation' : 'generations');
		return n + ' ' + SONA.et[s][n === 1 ? 0 : 1];
	};
	const f1 = (x) => String(x.toFixed(1)).replace('.', ',');
	/* otsing lehe sees: mudeli nimi, põlvkond või aasta (nt „golf 2015“, „e90“) */
	let q = $state('');
	const lihtne = (x) => String(x || '').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
	const sobib = (p, x, sonad) => {
		const hay = ' ' + lihtne(x.model + ' ' + p.nimi + ' ' + p.yearLabel) + ' ';
		return sonad.every((w) => {
			if (/^\d{4}$/.test(w)) { const a = +w; return p.a0 && a >= p.a0 && a <= (p.a1 || 9999); }
			return hay.includes(' ' + w);
		});
	};
	const naha = $derived.by(() => {
		const sonad = lihtne(q).split(' ').filter(Boolean);
		if (!sonad.length) return data.mudelid;
		return data.mudelid.map((x) => ({ ...x, polved: x.polved.filter((p) => sobib(p, x, sonad)) })).filter((x) => x.polved.length);
	});
	const naide = $derived(data.mudelid.length ? an(data.mudelid[0].model) + ' 2015' : '2015');
	const desc = $derived(
		t('{nimi}: {mudelid} mudelit, {n} põlvkonda — tehase rehvimõõdud, mootorid ja pidurdusmaa.', { nimi: m.nimi, mudelid: data.mudelid.length, n: data.n }) +
			' ' + data.mudelid.slice(0, 4).map((x) => an(x.model)).join(', ') + '.'
	);
</script>

<Meta
	title={t('{nimi} rehvimõõdud ja pidurdusmaa mudeli järgi', { nimi: m.nimi })}
	{desc}
	path="autod/{m.slug}/"
	crumbs={[[t('Avaleht'), '/'], [t('Autod'), '/autod/'], [m.nimi, path]]}
/>

<section class="page-hero mk-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/autod/')}>{t('Autod')}</a><span>/</span>{m.nimi}</div>
		<a class="mk-tagasi" href={L('/autod/')}>← {t('Kõik margid')}</a>
		<h1>{m.nimi}</h1>
		<p>{t('Vali oma auto mudel ja aastad — näed rehvimõõtu, pidurdusmaad ja sobivaid rehve.')}</p>
		<input class="lsel mk-otsi" type="search" bind:value={q} placeholder={t('Otsi mudelit, nt {naide}', { naide: naide })} aria-label={t('Otsi mudelit')} />
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		{#if !naha.length}<p class="note">{t('Sellist mudelit ei leidnud. Proovi lühemalt, nt ainult mudeli nimi.')}</p>{/if}
		<div class="mk-grid">
			{#each naha as x (x.model)}
				<div class="mk-mudel">
					<h2>{an(x.model)}</h2>
					<ul>
						{#each x.polved as p (p.slug)}
							<li><a href={L('/autod/' + m.slug + '/' + p.slug + '/')}><span class="mk-p">{an(p.lyhi)}</span><span class="mk-m">{p.moot}</span><span class="mk-nool" aria-hidden="true">→</span></a></li>
						{/each}
					</ul>
				</div>
			{/each}
		</div>
	</div>
</div>
{#if S}
	<div class="body-sec" style="padding-top:0">
		<div class="wrap">
			<div class="box">
				<p style="margin:0">
					{t('Andmebaasis on {nimi}: {mudelid}, {polved}', { nimi: m.nimi, mudelid: arv(data.mudelid.length, 'mudel'), polved: arv(data.n, 'polv') })}{#if S.keha.length}&nbsp;({ja(S.keha.map((k) => t(KEHA[k] || k)))}){/if}.
					{#if S.massMin}{S.massMin === S.massMax ? t('Tühimass {m} kg.', { m: kg(S.massMin) }) : t('Tühimass {a}–{b} kg.', { a: kg(S.massMin), b: kg(S.massMax) })}{/if}
					{#if S.moodud.length}
						{S.moote === 1 ? t('Tehase põhimõõt:') : t('Levinumad tehase põhimõõdud:')}
						{#each S.moodud as z, i (z.label)}{#if z.slug}<a href={L('/rehvid/' + z.slug + '/')}>{z.label}</a>{:else}{z.label}{/if}{i < S.moodud.length - 1 ? ', ' : '.'}{/each}
					{/if}
					{#if S.pidMin}
						{#if S.pidMax}
							{t('Märjal asfaldil 80 km/h pealt keskmise suverehviga (märgise klass C) on pidurdusmaa {a} m ({an}) kuni {b} m ({bn}).', { a: f1(S.pidMin.d), an: an(S.pidMin.nimi), b: f1(S.pidMax.d), bn: an(S.pidMax.nimi) })}
						{:else}
							{t('Märjal asfaldil 80 km/h pealt keskmise suverehviga (märgise klass C) on pidurdusmaa {a} m.', { a: f1(S.pidMin.d) })}
						{/if}
						{t('Arvutatud sama mudeliga mis kalkulaator, auto tehase põhimõõdus.')}
					{/if}
				</p>
			</div>
		</div>
	</div>
{/if}


<style>
	.mk-tagasi { display: inline-block; margin: var(--sp-4) 0 var(--sp-2); padding: 6px 14px; border-radius: 999px; background: var(--ink-3); border: 1px solid var(--line-d, #2a2f39); color: #dfe3e8; font-size: 14px; font-weight: 600; text-decoration: none; }
	.mk-tagasi:hover { border-color: var(--yellow); color: #fff; }
	.mk-otsi { margin-top: var(--sp-5); max-width: 520px; width: 100%; height: 52px; font-size: 17px; background-image: none; }
	.mk-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: var(--sp-4); align-items: start; }
	.mk-mudel { background: #fff; border: 1px solid var(--line); border-radius: 16px; padding: var(--sp-4); }
	.mk-mudel h2 { font-size: 24px; margin: 0 0 var(--sp-2); }
	.mk-mudel ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 4px; }
	.mk-mudel a { display: flex; align-items: center; gap: var(--sp-3); padding: 9px 12px; border-radius: 10px; background: var(--bg-2, #f5f6f8); text-decoration: none; color: var(--text); }
	.mk-mudel a:hover { background: var(--yellow-soft); }
	.mk-p { flex: 1; font-weight: 600; white-space: nowrap; }
	.mk-m { color: var(--muted); font-size: 13.5px; white-space: nowrap; }
	.mk-nool { color: var(--muted); }
</style>
