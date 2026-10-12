<script>
	/* Partnerid ja poelingid — ausalt, mis on tasuline ja mis mitte. */
	import Leht from '$lib/Leht.svelte';
	import { PARTNERID } from '$lib/partnerid.js';
	const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
	/* partneri kaart: suur logo, kes nad on, mida nad Pidurdusmaal teevad, „Külasta“ — kogu kaart on link */
	const nimekiri = PARTNERID.length
		? '<div class="partn">' +
			PARTNERID.map(
				(p) =>
					`<a class="partn-k" href="${esc(p.link)}" rel="${p.tasuta ? 'noopener' : 'sponsored noopener'}" target="_blank" data-partner="${esc(p.nimi)}">` +
					`<span class="partn-logo">${p.logo ? `<img src="/img/partnerid/${esc(p.logo)}" alt="${esc(p.nimi)}" loading="lazy">` : `<b>${esc(p.nimi)}</b>`}</span>` +
					`<span class="partn-info">${p.roll ? `<span class="partn-roll">${esc(p.roll)}</span>` : ''}<strong>${esc(p.nimi)}</strong>` +
					`${p.kirjeldus ? `<span class="partn-kirj">${esc(p.kirjeldus)}</span>` : ''}<span class="partn-ava">Külasta →</span></span>` +
					`</a>`
			).join('') +
			'</div>'
		: '<p>Hetkel partnereid ei ole — lehel ei ole ühtegi tasulist linki.</p>';
	const SISU = `<p class="partn-sissejuhatus">Need ettevõtted aitavad Pidurdusmaal tasuta püsida. Poodide hinnad ja laoseis on otse meie rehvikaartidel — näed pidurdusmaad ja saad samast kohast osta.</p>
${nimekiri}
<h2>Kuidas see töötab</h2>
<p>Pidurdusmaa.ee on kasutajale tasuta. Et lehte üleval hoida, võivad rehvide juures olevad poelingid olla <strong>partnerlingid</strong>: kui ostad lingi kaudu, võib pood maksta lehele väikese vahendustasu.</p>
<h2>Mida see sinu jaoks tähendab</h2>
<ul><li><strong>Hind ei muutu.</strong> Sinu jaoks on hind sama, mis müüja lehel.</li><li><strong>Järjestust ei müüda.</strong> Pidurdusmaad ja rehvide järjestus tulevad ainult andmetest: EL-i rehvimärgis, sõltumatud testid ja arvutus. Hind mõjutab järjestust ainult siis, kui valid ise „Soodne hind“.</li><li><strong>Ükski pood ei saa maksta, et tema rehv oleks eespool.</strong></li></ul>
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
