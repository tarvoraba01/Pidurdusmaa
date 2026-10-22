<script>
	/* /talv/mang/: ainult reaktsioonimäng (talv + telefonisõnum), et partnerid (LKF) saaksid selle oma
	   lehele panna iframe'ina. Mäng jookseb meie serverist, nende lehel on ainult aken:
	   <iframe src="https://pidurdusmaa.ee/talv/mang/" width="100%" height="760" style="border:0" allow="fullscreen" title="Talvine pidurdusmaa"></iframe>
	   Päis ja jalus on peidus (+layout.svelte: html.aken). Google'isse ei lähe (noindex), põhileht on /talv/. */
	import { useT, useLang } from '$lib/i18n.js';
	const t = useT();
	const keel = useLang();
	import Meta from '$lib/Meta.svelte';
	import Reaktsioon from '$lib/Reaktsioon.svelte';
	const LKF = keel.lang === 'en' ? 'https://www.lkf.ee/en' : 'https://www.lkf.ee/et/mistehakuijuhtus';
</script>

<Meta title={t('Kui kiiresti pidurdad, kui telefon piiksub?')} desc={t('Reaktsioonitest talvel: telefoni tuleb sõnum just siis, kui eesolev auto pidurdab.')} path="talv/mang/" canonical="/talv/" noindex />

<div class="mg">
	<h1 class="sr-only">{t('Kui kiiresti pidurdad, kui telefon piiksub?')}</h1>
	<Reaktsioon algIlm="talv" telefon katseid={1} alaLink={{ tekst: t('Mis teha, kui juhtus? LKF-i juhend'), url: LKF }} />
	<p class="mg-all"><a href={'https://pidurdusmaa.ee' + keel.L('/talv/')} target="_blank" rel="noopener">{t('Talvine pidurdusmaa')}: pidurdusmaa.ee</a></p>
</div>

<style>
	.mg { padding: 12px; }
	.mg-all { margin: 10px 0 0; text-align: center; font-size: 14px; }
</style>
