<script>
	import { lumi, jaa } from '$lib/margid.js';
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
	import AutoTee from '$lib/AutoTee.svelte';
	import { BASE, ORG_ID, AUTOR, autorLang, autorRef, graph } from '$lib/skeem.js';
	import { useLang } from '$lib/i18n.js';
	import { tana, kp, kpl, ALLIKAD } from '$lib/rehvivahetus.js';

	const keel = useLang();
	const ru = keel.lang === 'ru';
	const L = keel.L;
	const UUENDATUD = '2026-10-18';
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
		? `С какого числа зимняя резина в Эстонии ${AASTA}: все сроки`
		: `Rehvivahetus ${AASTA}: naastrehvid lubatud, talverehvid kohustuslikud`;
	/* kirjeldus ehituse päeva seisuga: naastud juba lubatud või alles tulekul (leht ehitatakse hooajal tihti uuesti) */
	const s0 = tana(ehitus);
	const DESC = ru
		? `${s0.naast === 'lubatud' ? 'Шипы уже разрешены' : 'Шипы разрешены'} с 15 октября по 31 марта, зимняя резина обязательна с 1 декабря по 1 марта. Что разрешено сегодня, сколько дней осталось, сроки ${h0.S}/${h0.S + 1} и правило 3 мм.`
		: `${s0.naast === 'lubatud' ? 'Naastrehvid on juba lubatud' : 'Naastrehvid on lubatud'} 15. oktoobrist 31. märtsini, talverehvid kohustuslikud 1. detsembrist 1. märtsini. Mis on täna lubatud, mitu päeva on jäänud ja 3 mm reegel.`;

	/* Korduma kippuvad küsimused (nähtav + FAQPage) */
	const kkk = (hh) =>
		ru
			? [
					[
						`Когда нужно менять шины в Эстонии в ${hh.S} году?`,
						`Зимнюю резину нужно поставить до ${kp(hh.kohustus, 'ru')}: с этого дня она обязательна. Шипованную можно ставить с ${kp(hh.naast, 'ru')}, при зимних условиях уже с ${kp(hh.naastTalv, 'ru')}. Обратно на летнюю можно после ${kp(hh.kohustusLopp, 'ru')}, а шипы нужно снять до ${kp(hh.naastLopp, 'ru')}.`
					],
					[
						`С какого числа разрешена шипованная резина в ${hh.S} году?`,
						`Шипованная резина в Эстонии разрешена с ${kp(hh.naast, 'ru')} по ${kp(hh.naastLopp, 'ru')}. Если дорожные и погодные условия зимние, её можно использовать уже с ${kp(hh.naastTalv, 'ru')} и до ${kp(hh.naastTalvLopp, 'ru')}.`
					],
					[
						`Обязательна ли зимняя резина в Эстонии в ${hh.S} году и с какого числа?`,
						`Да. Зимняя резина обязательна с ${kp(hh.kohustus, 'ru')} по ${kp(hh.kohustusLopp, 'ru')}. Нешипованная зимняя резина в это время должна иметь знак «три горные вершины и снежинка» (3PMSF), а глубина протектора зимней шины должна быть не меньше 3 мм.`
					],
					[
						'На какой резине можно ездить зимой в Эстонии?',
						`С ${kp(hh.kohustus, 'ru', true)} по ${kp(hh.kohustusLopp, 'ru', true)} только на зимней: шипованной или нешипованной. У нешипованной должен быть знак «три горные вершины и снежинка» (3PMSF), протектор зимней шины должен быть не меньше 3 мм. Летняя резина в это время не разрешена.`
					],
					[
						`Когда можно ставить летнюю резину в ${hh.S + 1} году?`,
						`Летнюю резину можно ставить после ${kp(hh.kohustusLopp, 'ru')}, когда заканчивается обязательный период зимней резины. Шипованную резину нужно снять до ${kp(hh.naastLopp, 'ru')} (при зимних условиях — до ${kp(hh.naastTalvLopp, 'ru')}). Разумно менять, когда закончились ночные заморозки.`
					],
					[
						'До какого числа можно ездить на зимней резине в Эстонии?',
						`На шипованной до ${kp(hh.naastLopp, 'ru')}, а если дорожные условия ещё зимние, до ${kp(hh.naastTalvLopp, 'ru')}. Нешипованную зимнюю резину закон по датам не ограничивает.`
					],
					[
						'Можно ли ездить летом на нешипованной зимней резине?',
						'Закон ограничивает по датам только шипованную резину. Нешипованную зимнюю резину летом использовать можно, но на тёплом сухом асфальте она тормозит заметно хуже летней.'
					],
					[
						'Какой должна быть глубина протектора?',
						'У зимней шины не меньше 3 мм, у летней не меньше 1,6 мм. Сцепление ухудшается раньше: зимнюю шину с протектором 4 мм и меньше лучше заменить до начала сезона.'
					]
				]
			: [
					[
						`Millal on kohustuslik rehvivahetus ${hh.S}?`,
						`Talverehvid peavad all olema hiljemalt ${kp(hh.kohustus, 'et', false, 'ks')}: ${kp(hh.kohustus, 'et', true, 'st')} kuni ${kp(hh.kohustusLopp, 'et', true, 'ni')} on need kohustuslikud. Naastrehvid võib alla panna ${kp(hh.naast, 'et', true, 'st')}, talviste teeolude korral juba ${kp(hh.naastTalv, 'et', true, 'st')}.`
					],
					[
						`Millal on naastrehvid lubatud ${hh.S}?`,
						`Naastrehvid on Eestis lubatud ${kp(hh.naast, 'et', false, 'st')} kuni ${kp(hh.naastLopp, 'et', false, 'ni')}. Kui tee- ja ilmastikuolud on talvised, tohib neid kasutada juba ${kp(hh.naastTalv, 'et', false, 'st')} ja kuni ${kp(hh.naastTalvLopp, 'et', false, 'ni')}.`
					],
					[
						`Millal on talverehvid lubatud ${hh.S}?`,
						`Lamellrehve võib kasutada igal ajal, kuupäevadega neid ei piirata. Naastrehvid on lubatud ${kp(hh.naast, 'et', true, 'st')} kuni ${kp(hh.naastLopp, 'et', true, 'ni')}. Talverehvid (naast või lamell) on kohustuslikud ${kp(hh.kohustus, 'et', true, 'st')} kuni ${kp(hh.kohustusLopp, 'et', true, 'ni')}.`
					],
					[
						`Kas talverehvid on ${hh.S} kohustuslikud ja millal?`,
						`Jah. Talverehvid on kohustuslikud ${kp(hh.kohustus, 'et', false, 'st')} kuni ${kp(hh.kohustusLopp, 'et', false, 'ni')}. Lamellrehvil peab sel ajal olema kolme mäetipu ja lumehelbe märk (3PMSF) ja talverehvi muster peab olema vähemalt 3 mm.`
					],
					[
						`Millal võib suverehvid alla panna ${hh.S + 1}?`,
						`Suverehvid võib alla panna pärast ${kp(hh.kohustusLopp, 'et', false, 'g')}, kui talverehvide kohustus lõpeb. Naastrehvid peavad olema maha võetud ${kp(hh.naastLopp, 'et', false, 'ks')} (talviste teeolude korral ${kp(hh.naastTalvLopp, 'et', false, 'ks')}). Mõistlik on vahetada siis, kui öökülmad on läbi.`
					],
					[
						'Kui kaua võib naastrehvidega sõita?',
						`Naastrehvidega võib sõita ${kp(hh.naastLopp, 'et', false, 'ni')}. Kui tee- ja ilmastikuolud on veel talvised, ${kp(hh.naastTalvLopp, 'et', false, 'ni')}. Lamellrehvidel kuupäevapiirangut ei ole.`
					],
					[
						'Kas lamellrehvidega võib suvel sõita?',
						'Kuupäevadega piirab seadus ainult naastrehve. Lamellrehvidega võib suvel sõita, aga soojal ja kuival asfaldil pidurdavad need suverehvist märgatavalt pikemalt.'
					],
					[
						'Kui sügav peab olema rehvi muster?',
						'Talverehvil vähemalt 3 mm, suverehvil vähemalt 1,6 mm. Haare kaob varem: kui talverehvi muster on 4 mm või vähem, tasub uued osta enne hooaega.'
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
			image: BASE + (ru ? '/og/sait/rehvivahetus.ru.png' : '/og/sait/rehvivahetus.png')
		},
		...(AUTOR ? [autorLang(lang)] : []),
		{
			'@type': 'FAQPage',
			mainEntity: KKK.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } }))
		}
	);

	/* tänase seisu tekstid; „n päeva pärast“ — kliendis uueneb kuupäevaga */
	const paevi = (d) => Math.max(0, Math.ceil((+d - +s.t) / 864e5));
	const jaanud = (d) => {
		const n = paevi(d);
		if (!n) return '';
		return ru ? ` · через ${n} ${n % 10 === 1 && n % 100 !== 11 ? 'день' : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20) ? 'дня' : 'дней'}` : ` · ${n} ${n === 1 ? 'päeva' : 'päeva'} pärast`;
	};
	const NAAST = $derived(
		ru
			? {
					lubatud: ['Разрешена', `до ${Kk(h.naastLopp)}`],
					talveoludes: ['Только при зимних условиях', s.t < h.naast ? `обычный срок с ${Kk(h.naast)}${jaanud(h.naast)}` : `до ${Kk(h.naastTalvLopp)}`],
					keelatud: ['Запрещена', `с ${Kk(h.naast)}${jaanud(h.naast)} (при зимних условиях с ${Kk(h.naastTalv)})`]
				}[s.naast]
			: {
					lubatud: ['Lubatud', `kuni ${Kk(h.naastLopp, 'ni')}`],
					talveoludes: ['Ainult talviste teeolude korral', s.t < h.naast ? `muidu alates ${Kk(h.naast, 'st')}${jaanud(h.naast)}` : `kuni ${Kk(h.naastTalvLopp, 'ni')}`],
					keelatud: ['Ei ole lubatud', `alates ${Kk(h.naast, 'st')}${jaanud(h.naast)} (talveoludes ${Kk(h.naastTalv, 'st')})`]
				}[s.naast]
	);
	const TALV = $derived(
		ru
			? s.talv === 'kohustuslik'
				? ['Обязательна', `до ${Kk(h.kohustusLopp)}`]
				: ['Не обязательна', s.t < h.kohustus ? `обязательна с ${Kk(h.kohustus)}${jaanud(h.kohustus)}` : 'можно ездить на летней']
			: s.talv === 'kohustuslik'
				? ['Kohustuslikud', `kuni ${Kk(h.kohustusLopp, 'ni')}`]
				: ['Ei ole kohustuslikud', s.t < h.kohustus ? `kohustuslikud alates ${Kk(h.kohustus, 'st')}${jaanud(h.kohustus)}` : 'võib sõita suverehvidega']
	);
	const TA = ALLIKAD[0];
	/* infomull: mida tähendab „talviste teeolude korral“ (määrus: naastrehvid
	   15.10–31.03; erandina talviste tee- ja ilmastikuolude korral 1.10–30.04) */
	const TALVEOLUD = $derived(
		ru
			? `Зимние дорожные и погодные условия: на дороге снег, лёд, слякоть или иней, либо ночные заморозки делают дорогу скользкой. Только в таких условиях правила разрешают шипы с ${Kk(h.naastTalv)} по ${Kk(new Date(h.naast - 864e5))} и с ${Kk(new Date(h.naastLopp.getTime() + 864e5))} по ${Kk(h.naastTalvLopp)}. Если дорога сухая и тёплая, в эти дни нужно ездить без шипов. Точной границы (градусы, сантиметры снега) правила не задают — решает водитель по фактическим условиям.`
			: `Talvised tee- ja ilmastikuolud: teel on lumi, jää, lörts või härmatis või teeb öökülm tee libedaks. Ainult siis lubab määrus naastrehve ${Kk(h.naastTalv, 'st')} kuni ${Kk(new Date(h.naast - 864e5), 'ni')} ja ${Kk(new Date(h.naastLopp.getTime() + 864e5), 'st')} kuni ${Kk(h.naastTalvLopp, 'ni')}. Kui tee on kuiv ja soe, tuleb neil päevadel sõita ilma naastudeta. Täpset piiri (kraade, lume paksust) määrus ei anna — otsustab juht tegelike olude järgi.`
	);
</script>

<Meta
	title={TITLE}
	desc={DESC}
	path="teadmine/rehvivahetus/"
	ogType="article"
	image="/og/sait/rehvivahetus.png"
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
			<h1>Смена резины в Эстонии {AASTA}: когда менять на зимнюю и на летнюю</h1>
			<p>Зимние шины в Эстонии обязательны с 1 декабря по 1 марта, шипованные разрешены с 15 октября по 31 марта (при зимних условиях с 1 октября по 30 апреля). Ниже — что разрешено сегодня и простой совет.</p>
		{:else}
			<div class="crumbs">
				<a href="/">Avaleht</a><span>/</span><a href="/teadmine/">Teadmine</a><span>/</span>Rehvivahetus
			</div>
			<h1>Rehvivahetus {AASTA}: millal talverehvid ja suverehvid alla</h1>
			<p>Talverehvid on Eestis kohustuslikud 1. detsembrist 1. märtsini, naastrehvid lubatud 15. oktoobrist 31. märtsini (talviste olude korral 1. oktoobrist 30. aprillini). Allpool on, mis täna lubatud on, ja lihtne soovitus.</p>
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
						<dd><b class="rv-{s.naast}">{NAAST[0]}</b>{#if s.naast === 'talveoludes'} <span class="tip" tabindex="0" data-tip={TALVEOLUD} aria-label={TALVEOLUD}>i</span>{/if} <span>{NAAST[1]}</span></dd>
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

				<h2>Ставить ли шипы сразу?</h2>
				<p>Преимущество шипов больше всего на первом льду около нуля — как раз в октябре и ноябре, когда гололёд появляется ночью неожиданно. VW Golf 8, торможение с 50 км/ч (расчёт той же моделью, что и в калькуляторе, новый протектор):</p>
				<div class="tbl-wrap">
					<table class="t" style="min-width:0">
						<thead><tr><th>Условия</th><th class="n">Шипованная</th><th class="n">Нешипованная (северная)</th><th class="n">Европейская зимняя</th></tr></thead>
						<tbody>
							<tr><td>Лёд 0 °C (тающий, самый скользкий)</td><td class="n"><b>61,1 м</b></td><td class="n">99,6 м</td><td class="n">181,7 м</td></tr>
							<tr><td>Лёд −5 °C</td><td class="n"><b>45,4 м</b></td><td class="n">58,9 м</td><td class="n">113,1 м</td></tr>
							<tr><td>Укатанный снег</td><td class="n">25,4 м</td><td class="n">26,2 м</td><td class="n">26,3 м</td></tr>
							<tr><td>Сухой асфальт, 80 км/ч, +5 °C</td><td class="n">31,7 м</td><td class="n">31,0 м</td><td class="n"><b>28,3 м</b></td></tr>
						</tbody>
					</table>
				</div>
				<p>Если ездите за городом, рано утром или по мостам, где гололёд появляется первым, ставьте шипы сразу. Если ездите в основном по убранным городским улицам, хватит северной нешипованной шины: на снегу и асфальте разница меньше метра, и она тише. Европейская зимняя шина на льду тормозит вдвое дольше. См. также <a href="/ru/teadmine/artiklid/naastrehv-voi-lamell/">шипы или «липучка»</a> и посчитайте <a href="/ru/">на своём автомобиле</a>.</p>

				<h2>Когда ставить летнюю резину</h2>
				<ul>
					<li><strong>Можно:</strong> после {K(h.kohustusLopp)}, когда заканчивается обязательный период зимней резины.</li>
					<li><strong>Нужно снять шипы:</strong> до {K(h.naastLopp)}; если условия ещё зимние — до {K(h.naastTalvLopp)}.</li>
					<li><strong>Разумно:</strong> когда закончились ночные заморозки и ночью держится плюс. Летом зимняя шина тормозит хуже: на сухом асфальте при +25 °C с 90 км/ч нешипованная северного типа примерно 42 м против 29 м у летней.</li>
				</ul>

				<h2>Требования к шинам</h2>
				<ul>
					<li><strong>Зимняя шина:</strong> протектор не меньше 3 мм. У нешипованной зимней шины зимой должен быть знак «три горные вершины и снежинка» {@html lumi('Знак «три горные вершины и снежинка» (3PMSF)')} (3PMSF). Транспортный департамент советует выбирать шину и со знаком льда {@html jaa('Знак льда (символ сцепления со льдом на этикетке ЕС)')}.</li>
					<li><strong>Летняя шина:</strong> протектор не меньше 1,6 мм; менять стоит уже при 2 мм.</li>
					<li><strong>Шипы:</strong> если ездите на шипованной резине, она должна стоять на всех колёсах. Не смешивайте шипованные и нешипованные шины.</li>
				</ul>
				<p class="note">Источник: <a href={TA} rel="noopener">Transpordiamet</a> (Транспортный департамент Эстонии). Цифры тормозного пути — расчёт Pidurdusmaa (VW Golf, новые шины).</p>

				<h2>Проверьте свои шины</h2>
				<ul>
					<li><a href={L('/talverehvid/')}>Лучшие зимние шины в вашем размере</a> — тесты, шипы и «липучки»</li>
					<li><a href={L('/teadmine/artiklid/millal-talverehvid-alla/')}>Правило +7 °C: при какой температуре ставить зимнюю резину</a></li>
					<li><a href={L('/teadmine/artiklid/talverehvide-nouded/')}>Требования к зимней резине: протектор, 3PMSF, шипы и штраф</a></li>
					<li><a href={L('/teadmine/artiklid/naastrehvid-liiga-vara-voi-hilja/')}>Шипы слишком рано или слишком поздно: тёплый асфальт и апрель</a></li>
					<li><a href={L('/teadmine/artiklid/talverehvid-valismaal/')}>Зимняя резина в Финляндии, Латвии и Литве</a></li>
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

				<h2>Kas naastrehvid kohe alla panna?</h2>
				<p>Naastu eelis on suurim esimesel jääl nulli lähedal — just oktoobris ja novembris, kui jäide tekib öösel ootamatult. VW Golf 8, 50 km/h pealt (arvutus sama mudeliga mis kalkulaator, uus muster):</p>
				<div class="tbl-wrap">
					<table class="t" style="min-width:0">
						<thead><tr><th>Teeolu</th><th class="n">Naastrehv</th><th class="n">Põhjamaade lamell</th><th class="n">Kesk-Euroopa talverehv</th></tr></thead>
						<tbody>
							<tr><td>Jää 0 °C (sulav, libedaim)</td><td class="n"><b>61,1 m</b></td><td class="n">99,6 m</td><td class="n">181,7 m</td></tr>
							<tr><td>Jää −5 °C</td><td class="n"><b>45,4 m</b></td><td class="n">58,9 m</td><td class="n">113,1 m</td></tr>
							<tr><td>Tallatud lumi</td><td class="n">25,4 m</td><td class="n">26,2 m</td><td class="n">26,3 m</td></tr>
							<tr><td>Kuiv asfalt, 80 km/h, +5 °C</td><td class="n">31,7 m</td><td class="n">31,0 m</td><td class="n"><b>28,3 m</b></td></tr>
						</tbody>
					</table>
				</div>
				<p>Kui sõidad maal, varahommikul või üle sildade, kus jäide tekib esimesena, pane naastud alla kohe. Kui sõidad peamiselt linnas puhastatud tänavatel, piisab Põhjamaade lamellrehvist: lumel ja asfaldil on vahe alla meetri ja lamell on vaiksem. Kesk-Euroopa talverehv jääb jääl kaks korda pikemaks. Vaata ka <a href="/teadmine/artiklid/naastrehv-voi-lamell/">naastrehv või lamell</a> ja arvuta <a href="/">oma autoga</a>.</p>

				<h2>Millal suverehvid alla</h2>
				<ul>
					<li><strong>Võib:</strong> pärast {K(h.kohustusLopp, 'g')}, kui talverehvide kohustus lõpeb.</li>
					<li><strong>Naastud peavad maha:</strong> {K(h.naastLopp, 'ks')}; kui teeolud on veel talvised, {K(h.naastTalvLopp, 'ks')}.</li>
					<li><strong>Mõistlik:</strong> kui öökülmad on läbi ja ka öösel on plusskraadid. Suvel pidurdab talverehv halvemini: kuival asfaldil +25 °C juures 90 km/h pealt Põhjamaade lamellrehv umbes 42 m, suverehv 29 m.</li>
				</ul>

				<h2>Nõuded rehvidele</h2>
				<ul>
					<li><strong>Talverehv:</strong> muster vähemalt 3 mm. Lamellrehvil peab talvel olema kolme mäetipu ja lumehelbe märk {@html lumi()} (3PMSF). Transpordiamet soovitab valida ka jäämärgiga {@html jaa()} rehvi.</li>
					<li><strong>Suverehv:</strong> muster vähemalt 1,6 mm; vahetada tasub juba 2 mm juures.</li>
					<li><strong>Naastrehvid:</strong> kui kasutad naastrehve, peavad need olema kõigil ratastel. Ära pane naast- ja lamellrehve segamini.</li>
				</ul>
				<p class="note">Allikas: <a href={TA} rel="noopener">Transpordiamet</a>. Pidurdusmaad on Pidurdusmaa arvutus (VW Golf, uued rehvid).</p>

				<h2>Kontrolli oma rehve</h2>
				<ul>
					<li><a href="/talverehvid/">Parimad talverehvid sinu auto mõõdus</a> — testid, naast ja lamell</li>
					<li><a href="/teadmine/artiklid/millal-talverehvid-alla/">+7 °C reegel: mis temperatuuril talverehvid alla panna</a></li>
					<li><a href="/teadmine/artiklid/talverehvide-nouded/">Talverehvide nõuded: muster, 3PMSF märk, naastud ja trahv</a></li>
					<li><a href="/teadmine/artiklid/naastrehvid-liiga-vara-voi-hilja/">Naastrehvid liiga vara või liiga hilja: soe asfalt ja aprill</a></li>
					<li><a href="/teadmine/artiklid/talverehvid-valismaal/">Talverehvid Soomes, Lätis ja Leedus</a></li>
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
<AutoTee koht="teadmine/rehvivahetus/" />

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
	/* sama toon, veidi tumedam: kontrast hallil taustal ≥ 4.5:1 (WCAG AA) */
	.rv-lubatud,
	.rv-kohustuslik {
		color: #168048;
	}
	.rv-talveoludes {
		color: #98641a;
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
