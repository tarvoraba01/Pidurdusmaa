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

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L('/')}>{t('Avaleht')}</a><span>/</span><a href={L('/autod/')}>{t('Autod')}</a><span>/</span>{m.nimi}</div>
		<h1>{m.nimi}</h1>
		<p>{t('Vali mudel ja põlvkond: näed tehase rehvimõõte, mootoreid, pidurdusmaad ja parimaid rehve.')}</p>
	</div>
</section>
{#if S}
	<div class="body-sec" style="padding-bottom:0">
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
<div class="body-sec">
	<div class="wrap">
		{#each data.mudelid as x (x.model)}
			<div class="box">
				<h2>{m.nimi} {an(x.model)}</h2>
				<div class="tbl-wrap">
					<table class="t">
						<thead><tr><th>{t('Põlvkond')}</th><th>{t('Tehase põhimõõt')}</th></tr></thead>
						<tbody>
							{#each x.polved as p (p.slug)}
								<tr><td><a href={L('/autod/' + m.slug + '/' + p.slug + '/')}>{an(p.nimi)}</a></td><td>{p.moot}</td></tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>
		{/each}
	</div>
</div>
