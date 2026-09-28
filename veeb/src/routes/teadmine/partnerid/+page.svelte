<script>
	/* Partnerid ja poelingid — ausalt, mis on tasuline ja mis mitte. */
	import Leht from '$lib/Leht.svelte';
	import { PARTNERID } from '$lib/partnerid.js';
	const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
	const nimekiri = PARTNERID.length
		? '<ul>' +
			PARTNERID.map(
				(p) => `<li><a href="${esc(p.url)}" rel="nofollow sponsored noopener" target="_blank">${esc(p.nimi)}</a>${p.kuidas ? ' — ' + esc(p.kuidas) : ''}</li>`
			).join('') +
			'</ul>'
		: '<p>Hetkel partnereid ei ole — lehel ei ole ühtegi tasulist linki.</p>';
	const SISU = `<p>Pidurdusmaa.ee on kasutajale tasuta. Et lehte üleval hoida, võivad rehvide juures olevad poelingid olla <strong>partnerlingid</strong>: kui ostad lingi kaudu, võib pood maksta lehele väikese vahendustasu.</p>
<h2>Praegused partnerid</h2>
${nimekiri}
<h2>Mida see sinu jaoks tähendab</h2>
<ul><li><strong>Hind ei muutu.</strong> Maksad poes sama hinna, olgu tulid meilt või mujalt.</li><li><strong>Järjestust ei müüda.</strong> Pidurdusmaad ja rehvide järjestus tulevad ainult andmetest: EL-i rehvimärgis, sõltumatud testid ja arvutus. Hind mõjutab järjestust ainult siis, kui valid ise „Soodne hind“.</li><li><strong>Ükski pood ei saa maksta, et tema rehv oleks eespool.</strong></li></ul>
<p class="note aff-legal">Pidurdusmaa.ee (Rabarvo OÜ) võib saada vahendustasu ostudelt, mis tehakse lehe poelinkide kaudu. Poelingid on tähistatud ka otsingumootoritele (rel="sponsored"). Poodi minnes võib pood või partnervõrgustik salvestada sinu brauserisse küpsise, et ost lehega seostada; Pidurdusmaa.ee ise sinu ostu sisu ega isikuandmeid ei näe. Vt ka <a href="/kasutustingimused/">kasutustingimused</a> ja <a href="/privaatsus/">privaatsus</a>.</p>`;
</script>

<Leht
	title="Partnerid ja poelingid"
	desc="Kuidas Pidurdusmaa.ee tasuta püsib: poelingid võivad olla partnerlingid. Hind sinu jaoks ei muutu ja rehvide järjestust ei müüda."
	path="teadmine/partnerid/"
	crumbs={[["Teadmine", "/teadmine/"], ["Partnerid ja poelingid", "/teadmine/partnerid/"]]}
	lapsed={[]}
	sisu={SISU}
/>
