<script>
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const L = useLang().L;
	import Meta from '$lib/Meta.svelte';
	import Kataloog from '$lib/Kataloog.svelte';
	import { KAT_NIMI, num } from '$lib/util.js';
	let { data } = $props();
</script>

<!-- päring „autorehvid“ (pea-termin on poodide päralt): pealkiri ja H1 märksõnaga, tüübilehed lingina -->
<Meta
	title={t("Autorehvid: kõik rehvid mõõdu, margi ja testide järgi")}
	desc={t("Autorehvid mõõdu, margi ja tüübi järgi: {n} rehvimudelit EL-i märgisega ja testide mõõdetud pidurdusmaad. Suve-, talve-, naast- ja lamellrehvid.", { n: num(data.mudeleid, 0) })}
	path="rehvid/"
	crumbs={[[t('Avaleht'), '/'], [t('Rehvid'), '/rehvid/']]}
/>

<section class="page-hero">
	<div class="wrap">
		<div class="crumbs"><a href={L("/")}>{t("Avaleht")}</a><span>/</span>{t("Rehvid")}</div>
		<h1>{t("Autorehvid")}</h1>
		<p>
			{t("Vali mõõt ja rehvi liik: näed kohe kõiki selle mõõdu rehve, testide pidurdusmaad ja poodide hindu.")} {num(data.mudeleid, 0)} {t("rehvimudelit EL-i rehvimärgisega ja")} {data.tested.length} {t("rehvi sõltumatutes testides.")}
		</p>
		<p class="tyybid">
			{t("Rehvitüübi järgi:")}
			<a href={L('/suverehvid/')}>{t("Suverehvid")}</a> ·
			<a href={L('/talverehvid/')}>{t("Talverehvid")}</a> ·
			<a href={L('/naastrehvid/')}>{t("Naastrehvid")}</a> ·
			<a href={L('/lamellrehvid/')}>{t("Lamellrehvid")}</a>.
			{t("Oma auto rehvimõõdu leiad lehelt")} <a href={L('/autod/')}>{t("Rehvid autole")}</a>.
		</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<Kataloog moodud={data.moodud} />
		<div class="box" style="margin-top:var(--sp-10)">
			<h2>{t("Mõõdu järgi")}</h2>
			<p class="sub">{t("Andmebaasis olevad mõõdud. Korje laieneb — kui sinu mõõtu pole, on andmed alles tulemas.")}</p>
			<div class="sizes-list">
				{#each data.sizes as s (s.slug)}
					<a href={L("/rehvid/" + s.slug + "/")}>{s.label} <span class="note">· {s.n}</span></a>
				{/each}
			</div>
		</div>
		<div class="box">
			<h2>{t('Sõltumatult testitud rehvid')}</h2>
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
					<a href={L('/margid/' + m.slug + '/')}>{m.nimi} <span class="note">· {m.n}</span></a>
				{/each}
			</div>
		</div>
	</div>
</div>
