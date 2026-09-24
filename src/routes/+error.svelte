<script>
	/* 404 — sama sisu, mis oli WordPressi 404.php-s: ütleme ausalt, et
	   seda mõõtu või rehvi ei ole veel andmebaasis, ja pakume edasiteed. */
	import { page } from '$app/state';
</script>

<svelte:head>
	<title>Lehte ei leitud | Pidurdusmaa.ee</title>
	<meta name="robots" content="noindex, follow" />
</svelte:head>

<section class="page-hero">
	<div class="wrap">
		<h1>Lehte ei leitud</h1>
		<p>
			Seda lehte ei ole — või on see rehv või mõõt, mille andmeid meil veel ei ole.
			{#if page.status !== 404}<br />Viga {page.status}: {page.error?.message}{/if}
		</p>
	</div>
</section>
<div class="body-sec">
	<div class="wrap">
		<div class="box">
			<h2>Kust edasi</h2>
			<ul>
				<li><a href="/">Arvuta pidurdusmaa</a> — vali auto, mõõt ja teeolud</li>
				<li><a href="/rehvid/">Kõik rehvid ja mõõdud</a></li>
				<li><a href="/rehvi-valimine/">Rehvi valimine</a> — näitame sobivaid sinu tingimustele</li>
				<li><a href="/testid/">Sõltumatud testid</a></li>
			</ul>
		</div>
	</div>
</div>
