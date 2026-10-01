<script>
	/* Rehvivahetus: millal talverehvid ja suverehvid alla (seaduse kuupäevad + lihtne soovitus).
	   Otsingusõnad Google Trendsi järgi (Eesti, 2021–2026): „rehvivahetus“ on kõige otsitum,
	   siis „talverehvid“, „suverehvid“, „naastrehvid“; pikad päringud „talverehvid lubatud 2025“,
	   „talverehvid kohustuslikud 2025“, „suverehvid lubatud 2026“, „naastrehvide kasutusaeg“.
	   Vene keeles: „смена резины в эстонии“, „с какого числа зимняя резина в эстонии“,
	   „шипованная резина в эстонии“ (резина, mitte шины).
	   Kuupäevad: $lib/rehvivahetus.js (Transpordiamet). Leht ei vanane: aastad tulevad tänasest
	   kuupäevast, brauseris arvutatakse „täna“ uuesti. */
	import { onMount } from 'svelte';
	import Meta from '$lib/Meta.svelte';
	import Autor from '$lib/Autor.svelte';
	import { BASE, ORG_ID, AUTOR, autorRef, graph } from '$lib/skeem.js';
	import { useLang } from '$lib/i18n.js';
	import { tana, kp, kpl, ALLIKAD } from '$lib/rehvivahetus.js';

	const keel = useLang();
	const ru = keel.lang === 'ru';
	const L = keel.L;
	const UUENDATUD = '2026-10-01';
	const PATH = '/teadmine/rehvivahetus/';

	const ehitus = new Date();
	let nyyd = $state(ehitus);
	onMount(() => (nyyd = new Date()));
	const s = $derived(tana(nyyd));
	const h = $derived(s.h);
	const lang = ru ? 'ru' : 'et';
	const K = (d, c = '') => kp(d, lang, false, c);
	const Kk = (d, c = '') => kp(d, lang, true, c);

	const AASTA = ehitus.getFullYear();
	const h0 = tana(ehitus).h;
	const TITLE = ru
		? `Смена резины в Эстонии ${AASTA}: с какого числа зимняя и летняя резина`
		: `Rehvivahetus ${AASTA}: millal talverehvid ja suverehvid alla`;
	const DESC = ru
		? `Шипованная резина разрешена с 15 октября по 31 марта, зимняя резина обязательна с 1 декабря по 1 марта. Все сроки смены резины в Эстонии ${h0.S}/${h0.S + 1} и требования к протектору.`
		: `Naastrehvid on lubatud 15. oktoobrist 31. märtsini, talverehvid kohustuslikud 1. detsembrist 1. märtsini. Rehvivahetuse kuupäevad ${h0.S}/${h0.S + 1} ja nõuded ühes kohas.`;

	/* Korduma kippuvad küsimused (nähtav + FAQPage) */
	const kkk = (hh) =>
		ru
			? [
					[
						`С какого числа разрешена шипованная резина в ${hh.S} году?`,
						`Шипованная резина в Эстонии разрешена с ${kp(hh.naast, 'ru')} по ${kp(hh.naastLopp, 'ru')}. Если дорожные и погодные условия зимние, её можно использовать уже с ${kp(hh.naastTalv, 'ru')} и до ${kp(hh.naastTalvLopp, 'ru')}.`
					],
					[
						'С какого числа зимняя резина обязательна в Эстонии?',
						`Зимняя резина обязательна с ${kp(hh.kohustus, 'ru')} по ${kp(hh.kohustusLopp, 'ru')}. Нешипованная зимняя резина в это время должна иметь знак «три горные вершины и снежинка» (3PMSF), а глубина протектора зимней шины должна быть больше 3 мм.`
					],
					[
						`Когда можно ставить летнюю резину в ${hh.S + 1} году?`,
						`Летнюю резину можно ставить после ${kp(hh.kohustusLopp, 'ru')}, когда заканчивается обязательный период зимней резины. Шипованную резину нужно снять до ${kp(hh.naastLopp, 'ru')} (при зимних условиях — до ${kp(hh.naastTalvLopp, 'ru')}). Разумно менять, когда закончились ночные заморозки.`
					],
					[
						'Можно ли ездить летом на нешипованной зимней резине?',
						'Закон ограничивает по датам только шипованную резину. Нешипованную зимнюю резину летом использовать можно, но на тёплом сухом асфальте она тормозит заметно хуже летней.'
					],
					[
						'Какой должна быть глубина протектора?',
						'У зимней шины — больше 3 мм, у летней — не меньше 1,6 мм. Сцепление ухудшается раньше: зимнюю шину с протектором 4 мм и меньше лучше заменить до начала сезона.'
					]
				]
			: [
					[
						`Millal on naastrehvid lubatud ${hh.S}?`,
						`Naastrehvid on Eestis lubatud ${kp(hh.naast, 'et', false, 'st')} kuni ${kp(hh.naastLopp, 'et', false, 'ni')}. Kui tee- ja ilmastikuolud on talvised, tohib neid kasutada juba ${kp(hh.naastTalv, 'et', false, 'st')} ja kuni ${kp(hh.naastTalvLopp, 'et', false, 'ni')}.`
					],
					[
						'Millal on talverehvid kohustuslikud?',
						`Talverehvid on kohustuslikud ${kp(hh.kohustus, 'et', false, 'st')} kuni ${kp(hh.kohustusLopp, 'et', false, 'ni')}. Lamellrehvil peab sel ajal olema kolme mäetipu ja lumehelbe märk (3PMSF) ja talverehvi muster peab olema sügavam kui 3 mm.`
					],
					[
						`Millal võib suverehvid alla panna ${hh.S + 1}?`,
						`Suverehvid võib alla panna pärast ${kp(hh.kohustusLopp, 'et', false, 'g')}, kui talverehvide kohustus lõpeb. Naastrehvid peavad olema maha võetud ${kp(hh.naastLopp, 'et', false, 'ks')} (talviste teeolude korral ${kp(hh.naastTalvLopp, 'et', false, 'ks')}). Mõistlik on vahetada siis, kui öökülmad on läbi.`
					],
					[
						'Kas lamellrehvidega võib suvel sõita?',
						'Kuupäevadega piirab seadus ainult naastrehve. Lamellrehvidega võib suvel sõita, aga soojal ja kuival asfaldil pidurdavad need suverehvist märgatavalt pikemalt.'
					],
					[
						'Kui sügav peab olema rehvi muster?',
						'Talverehvil sügavam kui 3 mm, suverehvil vähemalt 1,6 mm. Haare kaob varem: kui talverehvi muster on 4 mm või vähem, tasub uued osta enne hooaega.'
					]
				];
	const KKK = kkk(h0);

	const jsonld = graph(
		{
			'@type': 'Article',
			'@id': BASE + L(PATH) + '#artikkel',
			headline: TITLE,
			inLanguage: lang,
			datePublished: UUENDATUD,
			dateModified: UUENDATUD,
			author: autorRef(),
			publisher: { '@id': ORG_ID },
			mainEntityOfPage: BASE + L(PATH),
			image: BASE + '/og/sait/avaleht.png'
		},
		...(AUTOR ? [AUTOR] : []),
		{
			'@type': 'FAQPage',
			mainEntity: KKK.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } }))
		}
	);

	/* tänase seisu tekstid */
	const NAAST = $derived(
		ru
			? {
					lubatud: ['Разрешена', `до ${Kk(h.naastLopp)}`],
					talveoludes: ['Только при зимних условиях', s.t < h.naast ? `обычный срок с ${Kk(h.naast)}` : `до ${Kk(h.naastTalvLopp)}`],
					keelatud: ['Запрещена', `с ${Kk(h.naast)} (при зимних условиях с ${Kk(h.naastTalv)})`]
				}[s.naast]
			: {
					lubatud: ['Lubatud', `kuni ${Kk(h.naastLopp, 'ni')}`],
					talveoludes: ['Ainult talviste teeolude korral', s.t < h.naast ? `muidu alates ${Kk(h.naast, 'st')}` : `kuni ${Kk(h.naastTalvLopp, 'ni')}`],
					keelatud: ['Ei ole lubatud', `alates ${Kk(h.naast, 'st')} (talveoludes ${Kk(h.naastTalv, 'st')})`]
				}[s.naast]
	);
	const TALV = $derived(
		ru
			? s.talv === 'kohustuslik'
				? ['Обязательна', `до ${Kk(h.kohustusLopp)}`]
				: ['Не обязательна', s.t < h.kohustus ? `обязательна с ${Kk(h.kohustus)}` : 'можно ездить на летней']
			: s.talv === 'kohustuslik'
				? ['Kohustuslikud', `kuni ${Kk(h.kohustusLopp, 'ni')}`]
				: ['Ei ole kohustuslikud', s.t < h.kohustus ? `kohustuslikud alates ${Kk(h.kohustus, 'st')}` : 'võib sõita suverehvidega']
	);
	const TA = ALLIKAD[0];
</script>

<Meta
	title={TITLE}
	desc={DESC}
	path="teadmine/rehvivahetus/"
	ogType="article"
	crumbs={[
		[ru ? 'Главная' : 'Avaleht', '/'],
		[ru ? 'Знания' : 'Teadmine', '/teadmine/'],
		[ru ? 'Смена резины' : 'Rehvivahetus', PATH]
	]}
	{jsonld}
/>

<section class="page-hero">
	<div class="wrap">
		{#if ru}
			<div class="crumbs">
				<a href={L('/')}>Главная</a><span>/</span><a href={L('/teadmine/')}>Знания</a><span>/</span>Смена резины
			</div>
			<h1>Смена резины в Эстонии: когда зимняя и когда летняя</h1>
			<p>Сроки по закону и простой совет — без лишнего.</p>
		{:else}
			<div class="crumbs">
				<a href="/">Avaleht</a><span>/</span><a href="/teadmine/">Teadmine</a><span>/</span>Rehvivahetus
			</div>
			<h1>Rehvivahetus: millal talverehvid ja suverehvid alla</h1>
			<p>Seaduse kuupäevad ja lihtne soovitus — ilma liigse jututa.</p>
		{/if}
	</div>
</section>

<div class="body-sec">
	<div class="wrap">
		<article class="entry prose entry-content">
			<Autor uuendatud={UUENDATUD} />

			<section class="rv-tana" aria-labelledby="rv-tana-h">
				<h2 id="rv-tana-h">{ru ? 'Сегодня' : 'Täna'}, {K(s.t)}</h2>
				<dl>
					<div class="rv-rida">
						<dt>{ru ? 'Шипованная резина' : 'Naastrehvid'}</dt>
						<dd><b class="rv-{s.naast}">{NAAST[0]}</b> <span>{NAAST[1]}</span></dd>
					</div>
					<div class="rv-rida">
						<dt>{ru ? 'Зимняя резина' : 'Talverehvid'}</dt>
						<dd><b class="rv-{s.talv}">{TALV[0]}</b> <span>{TALV[1]}</span></dd>
					</div>
					<div class="rv-rida">
						<dt>{ru ? 'Летняя резина' : 'Suverehvid'}</dt>
						<dd>
							<b class="rv-{s.suvi}">{s.suvi === 'lubatud' ? (ru ? 'Разрешена' : 'Lubatud') : ru ? 'Нельзя' : 'Ei tohi'}</b>
							<span>
								{#if s.suvi === 'lubatud'}{s.t < h.kohustus
										? ru
											? `до ${Kk(new Date(h.kohustus - 864e5))}`
											: `kuni ${Kk(new Date(h.kohustus - 864e5), 'ni')}`
										: ''}{:else}{ru ? `можно после ${Kk(h.kohustusLopp)}` : `lubatud pärast ${Kk(h.kohustusLopp, 'g')}`}{/if}
							</span>
						</dd>
					</div>
				</dl>
			</section>

			{#if ru}
				<h2>Сроки {h.S}/{h.S + 1}</h2>
				<div class="tbl-wrap">
					<table class="t rv-t">
						<thead><tr><th>Что</th><th>Когда</th></tr></thead>
						<tbody>
							<tr><td><strong>Шипованная резина разрешена</strong></td><td class="nw">{kpl(h.naast)} – {kpl(h.naastLopp)}</td></tr>
							<tr><td><strong>Шипованная резина при зимних условиях</strong></td><td class="nw">{kpl(h.naastTalv)} – {kpl(h.naastTalvLopp)}</td></tr>
							<tr><td><strong>Зимняя резина обязательна</strong></td><td class="nw">{kpl(h.kohustus)} – {kpl(h.kohustusLopp)}</td></tr>
							<tr><td><strong>Летняя резина</strong></td><td>до {kpl(new Date(h.kohustus - 864e5))} и после {kpl(h.kohustusLopp)}</td></tr>
							<tr><td><strong>Нешипованная зимняя («липучка»)</strong></td><td>без ограничения по датам</td></tr>
						</tbody>
					</table>
				</div>

				<h2>Когда ставить зимнюю резину</h2>
				<ul>
					<li><strong>Нужно:</strong> до {K(h.kohustus)}. С этого дня зимняя резина обязательна.</li>
					<li><strong>Можно:</strong> шипованную — с {K(h.naast)}, при зимних условиях уже с {Kk(h.naastTalv)}. Нешипованную — в любое время.</li>
					<li><strong>Разумно:</strong> когда днём держится ниже +7 °C и ночью подмораживает — до первого снега. На мокрой дороге зимняя шина тормозит короче летней уже примерно при +5 °C.</li>
				</ul>

				<h2>Когда ставить летнюю резину</h2>
				<ul>
					<li><strong>Можно:</strong> после {K(h.kohustusLopp)}, когда заканчивается обязательный период зимней резины.</li>
					<li><strong>Нужно снять шипы:</strong> до {K(h.naastLopp)}; если условия ещё зимние — до {K(h.naastTalvLopp)}.</li>
					<li><strong>Разумно:</strong> когда закончились ночные заморозки и ночью держится плюс. Летом зимняя шина тормозит хуже: на сухом асфальте при +25 °C с 90 км/ч примерно 42 м против 29 м у летней.</li>
				</ul>

				<h2>Требования к шинам</h2>
				<ul>
					<li><strong>Зимняя шина:</strong> протектор глубже 3 мм. У нешипованной зимней шины зимой должен быть знак «три горные вершины и снежинка» (3PMSF). Транспортный департамент советует выбирать шину и со знаком льда.</li>
					<li><strong>Летняя шина:</strong> протектор не меньше 1,6 мм; менять стоит уже при 2 мм.</li>
					<li><strong>Совет:</strong> шины одного типа на всех колёсах — не смешивайте шипованные и нешипованные.</li>
				</ul>
				<p class="note">Источник: <a href={TA} rel="noopener">Transpordiamet</a> (Транспортный департамент Эстонии). Цифры тормозного пути — расчёт Pidurdusmaa (VW Golf, новые шины).</p>

				<h2>Проверьте свои шины</h2>
				<ul>
					<li><a href={L('/talverehvid/')}>Лучшие зимние шины в вашем размере</a> — тесты, шипы и «липучки»</li>
					<li><a href={L('/teadmine/artiklid/millal-talverehvid-alla/')}>Когда ставить зимнюю резину: что показывают цифры</a></li>
					<li><a href={L('/') + '?olud=snow&kiirus=50#kalkulaator'}>Тормозной путь на снегу для вашего автомобиля</a></li>
				</ul>

				<h2>Часто задаваемые вопросы</h2>
			{:else}
				<h2>Kuupäevad {h.S}/{h.S + 1}</h2>
				<div class="tbl-wrap">
					<table class="t rv-t">
						<thead><tr><th>Mis</th><th>Millal</th></tr></thead>
						<tbody>
							<tr><td><strong>Naastrehvid lubatud</strong></td><td class="nw">{kpl(h.naast)} – {kpl(h.naastLopp)}</td></tr>
							<tr><td><strong>Naastrehvid talviste teeolude korral</strong></td><td class="nw">{kpl(h.naastTalv)} – {kpl(h.naastTalvLopp)}</td></tr>
							<tr><td><strong>Talverehvid kohustuslikud</strong></td><td class="nw">{kpl(h.kohustus)} – {kpl(h.kohustusLopp)}</td></tr>
							<tr><td><strong>Suverehvid lubatud</strong></td><td>kuni {kpl(new Date(h.kohustus - 864e5))} ja pärast {kpl(h.kohustusLopp)}</td></tr>
							<tr><td><strong>Lamellrehvid</strong></td><td>kuupäevadega piirangut ei ole</td></tr>
						</tbody>
					</table>
				</div>

				<h2>Millal talverehvid alla</h2>
				<ul>
					<li><strong>Peab:</strong> hiljemalt {K(h.kohustus, 'ks')}. Sellest päevast on talverehvid kohustuslikud.</li>
					<li><strong>Võib:</strong> naastrehvid alates {K(h.naast, 'st')}, talviste teeolude korral juba {Kk(h.naastTalv, 'st')}. Lamellrehvid igal ajal.</li>
					<li><strong>Mõistlik:</strong> kui päeval püsib alla +7 °C ja öösiti tuleb külma — enne esimest lund. Märjal teel pidurdab talverehv suverehvist lühemalt juba umbes +5 °C juures.</li>
				</ul>

				<h2>Millal suverehvid alla</h2>
				<ul>
					<li><strong>Võib:</strong> pärast {K(h.kohustusLopp, 'g')}, kui talverehvide kohustus lõpeb.</li>
					<li><strong>Naastud peavad maha:</strong> {K(h.naastLopp, 'ks')}; kui teeolud on veel talvised, {K(h.naastTalvLopp, 'ks')}.</li>
					<li><strong>Mõistlik:</strong> kui öökülmad on läbi ja ka öösel on plusskraadid. Suvel pidurdab talverehv halvemini: kuival asfaldil +25 °C juures 90 km/h pealt umbes 42 m, suverehv 29 m.</li>
				</ul>

				<h2>Nõuded rehvidele</h2>
				<ul>
					<li><strong>Talverehv:</strong> muster sügavam kui 3 mm. Lamellrehvil peab talvel olema kolme mäetipu ja lumehelbe märk (3PMSF). Transpordiamet soovitab valida ka jäämärgiga rehvi.</li>
					<li><strong>Suverehv:</strong> muster vähemalt 1,6 mm; vahetada tasub juba 2 mm juures.</li>
					<li><strong>Soovitus:</strong> sama tüüpi rehvid kõigil ratastel — ära pane naast- ja lamellrehve segamini.</li>
				</ul>
				<p class="note">Allikas: <a href={TA} rel="noopener">Transpordiamet</a>. Pidurdusmaad on Pidurdusmaa arvutus (VW Golf, uued rehvid).</p>

				<h2>Kontrolli oma rehve</h2>
				<ul>
					<li><a href="/talverehvid/">Parimad talverehvid sinu auto mõõdus</a> — testid, naast ja lamell</li>
					<li><a href="/teadmine/artiklid/millal-talverehvid-alla/">Millal talverehvid alla: mida pidurdusmaa ütleb</a></li>
					<li><a href="/?olud=snow&kiirus=50#kalkulaator">Pidurdusmaa lumel sinu autoga</a></li>
				</ul>

				<h2>Korduma kippuvad küsimused</h2>
			{/if}
			{#each kkk(h) as [q, a] (q)}
				<h3>{q}</h3>
				<p>{a}</p>
			{/each}
		</article>
	</div>
</div>

<style>
	.rv-tana {
		border: 1px solid var(--line);
		border-radius: 12px;
		padding: var(--sp-4) var(--sp-5);
		margin: var(--sp-5) 0;
		background: var(--paper-2);
	}
	.rv-tana h2 {
		margin: 0 0 var(--sp-3);
		font-size: 20px;
	}
	.rv-tana dl {
		margin: 0;
		display: grid;
		gap: var(--sp-3);
	}
	.rv-rida {
		display: grid;
		grid-template-columns: 9.5em 1fr;
		gap: var(--sp-3);
		align-items: baseline;
	}
	.rv-rida dt {
		font-weight: 700;
	}
	.rv-rida dd {
		margin: 0;
	}
	.rv-rida dd b {
		display: inline-block;
		padding: 2px 10px;
		border-radius: 999px;
		font-size: 14px;
		margin-right: var(--sp-2);
		border: 1px solid currentColor;
	}
	.rv-rida dd span {
		color: var(--muted);
		font-size: 14.5px;
	}
	.rv-lubatud,
	.rv-kohustuslik {
		color: var(--good);
	}
	.rv-talveoludes {
		color: var(--warn);
	}
	.rv-keelatud {
		color: var(--bad);
	}
	.rv-vabatahtlik {
		color: var(--muted);
	}
	table.rv-t {
		min-width: 0;
	}
	table.rv-t .nw {
		white-space: nowrap;
	}
	@media (max-width: 520px) {
		.rv-tana {
			padding: var(--sp-3) var(--sp-4);
		}
		.rv-rida {
			grid-template-columns: 1fr;
			gap: var(--sp-1);
		}
	}
</style>
