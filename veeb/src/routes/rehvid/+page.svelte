<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const L = useLang().L;
	import Meta from '$lib/Meta.svelte';
	import { KAT_NIMI, num } from '$lib/util.js';
	let { data } = $props();
</script>

<Meta
	title={t("Rehvid mõõdu ja mudeli järgi")}
	desc={t("Rehvimudelid ja -mõõdud EL-i rehvimärgise (EPREL) andmetega ning sõltumatute testide mõõdetud pidurdusmaad.")}
	path="rehvid/"
	crumbs={[[t('Avaleht'), '/'], [t('Rehvid'), '/rehvid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L("/")}>{t("Avaleht")}</a><span>/</span>{t("Rehvid")}</div>
		<h1>{t("Rehvid")}</h1>
		<p>
			{num(data.mudeleid, 0)} {t("rehvimudelit EL-i rehvimärgisega ja")} {data.tested.length} {t("rehvi sõltumatutes testides. Vali mõõt, et näha kõiki selle mõõdu rehve.")}
		</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="box">
			<h2>{t("Mõõdu järgi")}</h2>
			<p class="sub">{t("Andmebaasis olevad mõõdud. Korje laieneb — kui sinu mõõtu pole, on andmed alles tulemas.")}</p>
			<div class="sizes-list">
				{#each data.sizes as s (s.slug)}
					<a href={L("/rehvid/" + s.slug + "/")}>{s.label} <span class="note">· {s.n}</span></a>
				{/each}
			</div>
		</div>
		<div class="box">
			<h2>{t("Sõltumatult testitud")}</h2>
			<p class="sub">{t("Neil rehvidel on mõõdetud pidurdusmaad — täpsemad kui märgise klass.")}</p>
			<div class="grid-cards">
				{#each data.tested as ty, ti (ty.slug + '#' + ti)}
					<a class="tcard" href={L("/rehvid/" + ty.slug + "/")}>
						<span class="b">{t(KAT_NIMI[ty.category] ?? '')}</span>
						<h3>{ty.name}</h3>
						<span class="meta">{ty.srcs.split(", ").map((x) => t(x)).join(", ")}</span>
					</a>
				{/each}
			</div>
		</div>
		<div class="box">
			<h2>{t("Margi järgi")}</h2>
			<p class="sub">{@html t("Iga margi lehel on kõik selle mudelid kategooria kaupa. <a href=\"/margid/\">Kõik margid →</a>")}</p>
			<div class="sizes-list">
				{#each data.margid as m (m.slug)}
					<a href="/margid/{m.slug}/">{m.nimi} <span class="note">· {m.n}</span></a>
				{/each}
			</div>
		</div>
	</div>
</div>
