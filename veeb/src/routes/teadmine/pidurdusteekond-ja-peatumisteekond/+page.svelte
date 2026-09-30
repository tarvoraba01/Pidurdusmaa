<script>
	/* Artikkel: pidurdusteekond, reageerimisteekond ja peatumisteekond.
	   Otsingusõnad, mida kasutavad autokoolid, õpikud ja liikluseeskiri.
	   Kõik näidete arvud tulevad mudelist (demo), käsitsi kirjutatud on
	   ainult reageerimisteekond, mis on lihtne korrutis. */
	import Meta from '$lib/Meta.svelte';
	import { num } from '$lib/util.js';
	import { BASE, ORG_ID, AUTOR, autorRef, graph } from '$lib/skeem.js';
	import Autor from '$lib/Autor.svelte';
	import { useLang } from '$lib/i18n.js';

	let { data } = $props();
	const keel = useLang();
	const ru = keel.lang === 'ru';
	const L = keel.L;
	const d = data.demo;
	const UUENDATUD = '2026-09-25';
	const PATH = '/teadmine/pidurdusteekond-ja-peatumisteekond/';
	const TITLE = ru
		? 'Тормозной путь и остановочный путь: формула, примеры и калькулятор'
		: 'Pidurdusteekond ja peatumisteekond: valem, näited ja kalkulaator';
	const NIMI = ru ? 'Тормозной путь и остановочный путь' : 'Pidurdusteekond ja peatumisteekond';
	const react = (v, t = 1) => (v / 3.6) * t;
	const i90 = d ? d.speeds.indexOf(90) : -1;
	/* demo.car on eestikeelne kirjeldus (nt „…, suverehv märgise klassiga B“) */
	const autoRu = (s) =>
		String(s)
			.replace(/suverehv/g, 'летняя шина')
			.replace(/talverehv/g, 'зимняя шина')
			.replace(/märgise klassiga/g, 'класса маркировки');
	const carRu = d ? autoRu(d.car) : '';

	const KKK_RU = [
		[
			'Чем тормозной путь отличается от остановочного пути?',
			'Тормозной путь — это расстояние с момента, когда тормоз начинает действовать, до остановки автомобиля. Остановочный путь длиннее: к нему добавляется путь за время реакции, который автомобиль проезжает на полной скорости, пока водитель замечает опасность и переносит ногу на педаль тормоза.'
		],
		[
			'Как рассчитать остановочный путь?',
			'Остановочный путь = путь за время реакции + тормозной путь. Путь за время реакции — это скорость в метрах в секунду, умноженная на время реакции (км/ч, делённые на 3,6). Тормозной путь приблизительно равен v² / (2 · μ · g), где μ — коэффициент сцепления шины с дорогой, а g = 9,81 м/с².'
		],
		[
			'Каково время реакции водителя?',
			'В расчётах обычно используют около 1 секунды. Если водитель готов к торможению, оно может быть меньше 1 секунды; у уставшего водителя или водителя, который смотрит в телефон, время реакции часто составляет 1,5–2 секунды или больше.'
		],
		[
			'Во сколько раз увеличивается тормозной путь, если скорость удваивается?',
			'Тормозной путь растёт пропорционально квадрату скорости: вдвое большая скорость означает примерно вчетверо более длинный тормозной путь. Путь за время реакции растёт пропорционально скорости, то есть вдвое.'
		]
	];
	if (d && i90 >= 0) {
		KKK_RU.push([
			'Каков остановочный путь при 90 км/ч?',
			`Остановочный путь типичного компактного автомобиля (${carRu}) при времени реакции 1 секунда составляет на сухом асфальте около ${num(react(90) + d.dry[i90])} м, а на мокром — около ${num(react(90) + d.wet[i90])} м. Из них 25 м — путь за время реакции.`
		]);
	}

	const KKK_ET = [
		[
			'Mis vahe on pidurdusteekonnal ja peatumisteekonnal?',
			'Pidurdusteekond on vahemaa hetkest, kui pidur hakkab tööle, kuni auto seisab. Peatumisteekond on pikem: sellele lisandub reageerimisteekond, mille auto läbib täiskiirusel ajal, kui juht ohtu märkab ja jalga pidurile viib.'
		],
		[
			'Kuidas peatumisteekonda arvutada?',
			'Peatumisteekond = reageerimisteekond + pidurdusteekond. Reageerimisteekond on kiirus meetrites sekundis korda reaktsiooniaeg (km/h jagatud 3,6-ga). Pidurdusteekond on ligikaudu v² / (2 · μ · g), kus μ on rehvi ja tee haardetegur ning g = 9,81 m/s².'
		],
		[
			'Kui pikk on juhi reaktsiooniaeg?',
			'Arvutustes kasutatakse tavaliselt umbes 1 sekundit. Kui juht on pidurdamiseks valmis, võib see olla alla 1 sekundi; väsinud või telefoni vaatava juhi reaktsiooniaeg on sageli 1,5–2 sekundit või rohkem.'
		],
		[
			'Mitu korda pikeneb pidurdusteekond, kui kiirus kahekordistub?',
			'Pidurdusteekond kasvab kiiruse ruudus: kaks korda suurem kiirus tähendab umbes neli korda pikemat pidurdusteekonda. Reageerimisteekond kasvab kiirusega võrdeliselt, ehk kaks korda.'
		]
	];
	if (d && i90 >= 0) {
		KKK_ET.push([
			'Kui pikk on peatumisteekond 90 km/h juures?',
			`Tüüpilise kompaktauto (${d.car}) peatumisteekond 1-sekundilise reaktsiooniajaga on kuival asfaldil umbes ${num(react(90) + d.dry[i90])} m ja märjal umbes ${num(react(90) + d.wet[i90])} m. Sellest 25 m on reageerimisteekond.`
		]);
	}
	const KKK = ru ? KKK_RU : KKK_ET;

	const jsonld = graph(
		{
			'@type': 'Article',
			'@id': BASE + L(PATH) + '#artikkel',
			headline: TITLE,
			inLanguage: ru ? 'ru' : 'et',
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
			mainEntity: KKK.map(([q, a]) => ({
				'@type': 'Question',
				name: q,
				acceptedAnswer: { '@type': 'Answer', text: a }
			}))
		}
	);
</script>

<Meta
	title={ru
		? 'Тормозной путь и остановочный путь — формула и примеры'
		: 'Pidurdusteekond ja peatumisteekond — valem ja näited'}
	desc={ru
		? 'Что такое путь за время реакции, тормозной путь и остановочный путь, как их рассчитать и какой они длины при разной скорости на сухой и мокрой дороге. С калькулятором.'
		: 'Mis on reageerimisteekond, pidurdusteekond ja peatumisteekond, kuidas neid arvutada ja kui pikad need on eri kiirustel kuival ja märjal teel. Koos kalkulaatoriga.'}
	path="teadmine/pidurdusteekond-ja-peatumisteekond/"
	ogType="article"
	crumbs={[
		[ru ? 'Главная' : 'Avaleht', '/'],
		[ru ? 'Знания' : 'Teadmine', '/teadmine/'],
		[NIMI, PATH]
	]}
	{jsonld}
/>

<section class="page-hero">
	<div class="wrap">
		{#if ru}
			<div class="crumbs">
				<a href={L('/')}>Главная</a><span>/</span><a href={L('/teadmine/')}>Знания</a><span>/</span>Тормозной путь и
				остановочный путь
			</div>
			<h1>Тормозной путь и остановочный путь</h1>
			<p>Формула, примеры и калькулятор: на каком расстоянии автомобиль на самом деле останавливается.</p>
		{:else}
		<div class="crumbs">
			<a href="/">Avaleht</a><span>/</span><a href="/teadmine/">Teadmine</a><span>/</span>Pidurdusteekond ja
			peatumisteekond
		</div>
		<h1>Pidurdusteekond ja peatumisteekond</h1>
		<p>Valem, näited ja kalkulaator: kui kaugel auto tegelikult peatub.</p>
		{/if}
	</div>
</section>

<div class="body-sec">
	<div class="wrap">
		<article class="entry prose entry-content">
			<Autor uuendatud={UUENDATUD} />

			{#if ru}
			<p>
				<strong>Остановочный путь = путь за время реакции + тормозной путь.</strong> Тормозной путь (по-эстонски
				pidurdusteekond или pidurdusmaa) начинается с момента, когда тормоз начинает действовать. Остановочный путь
				начинается уже с момента, когда водитель замечает опасность, и он всегда длиннее.
			</p>

			<h2>Три понятия</h2>
			<ul>
				<li>
					<strong>Путь за время реакции</strong>: расстояние, которое автомобиль проезжает на полной скорости, пока
					водитель замечает опасность, принимает решение и переносит ногу на педаль тормоза.
				</li>
				<li>
					<strong>Тормозной путь</strong>: расстояние от начала торможения до полной остановки. Его определяют
					скорость, шина, дорога и автомобиль.
				</li>
				<li>
					<strong>Остановочный путь</strong>: сумма этих двух, то есть расстояние от момента, когда водитель заметил
					опасность, до остановки автомобиля.
				</li>
			</ul>

			<h2>Формулы</h2>
			<p><strong>Путь за время реакции</strong> = скорость (м/с) × время реакции (с)</p>
			<p>
				Скорость в метрах в секунду получится, если разделить км/ч на 3,6. 90 км/ч — это 25 м/с, поэтому при времени
				реакции 1 секунда автомобиль до начала торможения проезжает <strong>25 метров</strong>.
			</p>
			<p><strong>Тормозной путь</strong> ≈ v² / (2 · μ · g)</p>
			<p>
				Здесь v — скорость в метрах в секунду, μ — коэффициент сцепления шины с дорогой, g = 9,81 м/с². Коэффициент
				сцепления на сухом асфальте с хорошей шиной составляет около 0,8–1,0, на мокром асфальте — часто 0,5–0,7, на
				снегу и льду он намного меньше. Поскольку скорость возводится в квадрат, <strong>вдвое большая скорость
				означает примерно вчетверо более длинный тормозной путь</strong>.
			</p>
			<p>
				Простая формула даёт порядок величины. Реальный тормозной путь зависит также от того, как быстро тормоза
				выходят на полное усилие, от ABS, глубины протектора шины, слоя воды и температуры. Калькулятор
				Pidurdusmaa.ee учитывает это и использует реальные данные о шинах: маркировку шин ЕС и независимые тесты.
				Подробнее —
				<a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">как рассчитывается тормозной путь</a> (на эстонском).
			</p>

			{#if d}
				<h2>Примеры при разной скорости</h2>
				<p>
					Рассчитано той же моделью, что и в калькуляторе: {carRu}. Время реакции 1 с. Мокрый асфальт: слой воды
					1 мм, +10 °C. Сухой асфальт: +15 °C.
				</p>
				<p>
					В таблице указан остановочный путь (крупное число) и входящий в него тормозной путь (мелкое число).
				</p>
				<div class="tbl-wrap">
					<table class="t peat">
						<thead>
							<tr>
								<th>Скорость</th>
								<th class="n">Реакция</th>
								<th class="n">Сухой асфальт</th>
								<th class="n">Мокрый асфальт</th>
							</tr>
						</thead>
						<tbody>
							{#each d.speeds as v, i (v)}
								<tr>
									<td class="nw"><b>{v}</b> км/ч</td>
									<td class="n">{num(react(v))} м</td>
									<td class="n">
										<b>{num(react(v) + d.dry[i])} м</b><small>в т. ч. торможение {num(d.dry[i])}</small>
									</td>
									<td class="n">
										<b>{num(react(v) + d.wet[i])} м</b><small>в т. ч. торможение {num(d.wet[i])}</small>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
				<p>
					На низкой скорости большая часть остановочного пути приходится на реакцию: при 50 км/ч это
					{num(react(50))} м, а торможение на сухом асфальте — {num(d.dry[0])} м. На высокой скорости наоборот,
					потому что тормозной путь растёт пропорционально квадрату скорости.
				</p>
			{/if}

			<h2>Время реакции</h2>
			<p>
				В расчётах обычно принимают около <strong>1 секунды</strong>. Если водитель готов к торможению (нога уже над
				педалью), оно может быть меньше 1 секунды. Усталость, телефон, алкоголь или неожиданная ситуация легко
				растягивают его до 1,5–2 секунд и больше. При 90 км/ч каждая лишняя секунда — это ещё
				<strong>25 метров</strong> до того, как автомобиль вообще начнёт тормозить.
			</p>

			<h2>Что ещё влияет на тормозной путь</h2>
			{#if d}
				<ul>
					<li>
						<strong>Шина.</strong> Тот же автомобиль, та же мокрая дорога, 90 км/ч: класс сцепления на мокрой дороге
						по маркировке ЕС A — {num(d.classA)} м, класс E — {num(d.classE)} м.
					</li>
					<li>
						<strong>Глубина протектора.</strong> На мокрой дороге при 90 км/ч: новая шина (8 мм) — {num(d.tread8)} м,
						изношенная (3 мм) — {num(d.tread3)} м.
					</li>
					<li>
						<strong>Сезон.</strong> На снегу при 50 км/ч: с летней шиной — {num(d.snowSummer)} м, с зимней шиной —
						{num(d.snowWinter)} м.
					</li>
					<li>
						<strong>Нагрузка.</strong> На мокрой дороге при 90 км/ч: пустой автомобиль — {num(d.tread8)} м, с
						дополнительным грузом 450 кг — {num(d.loaded)} м.
					</li>
				</ul>
			{/if}

			<h2>Рассчитайте остановочный путь своего автомобиля</h2>
			<p>
				В <a href={L('/')}>калькуляторе тормозного пути</a> выберите свой автомобиль, размер шин, скорость и дорожные
				условия. В результате выберите <strong>«Остановочный путь»</strong> и время реакции: вы увидите отдельно путь
				за время реакции и тормозной путь, а также то, насколько результат изменила бы другая шина.
			</p>
			<p>
				Для обучения и сравнения двух ситуаций (например, 50 и 70 км/ч, новая и изношенная шина) есть
				<a href={L('/liiklusohutus/')}>калькулятор безопасности движения</a> — без цен и магазинов, с режимом
				презентации для класса.
			</p>

			<h2>Часто задаваемые вопросы</h2>
			{#each KKK as [q, a] (q)}
				<h3>{q}</h3>
				<p>{a}</p>
			{/each}

			<p class="note">
				Цифры — расчётная оценка, а не гарантия. Не используйте их для принятия решений на дороге: всегда соблюдайте
				достаточную дистанцию и выбирайте скорость в соответствии с дорожными условиями.
			</p>
			{:else}
			<p>
				<strong>Peatumisteekond = reageerimisteekond + pidurdusteekond.</strong> Pidurdusteekond (ehk
				pidurdusmaa) algab hetkest, kui pidur hakkab tööle. Peatumisteekond algab juba hetkest, kui
				juht ohtu märkab, ja see on alati pikem.
			</p>

			<h2>Kolm mõistet</h2>
			<ul>
				<li>
					<strong>Reageerimisteekond</strong>: vahemaa, mille auto läbib täiskiirusel ajal, kui juht
					ohtu märkab, otsustab ja jala pidurile viib.
				</li>
				<li>
					<strong>Pidurdusteekond</strong> (pidurdusmaa): vahemaa pidurdamise algusest seismajäämiseni.
					Selle määravad kiirus, rehv, tee ja auto.
				</li>
				<li>
					<strong>Peatumisteekond</strong>: need kaks kokku ehk vahemaa ohu märkamisest kuni auto
					seisab.
				</li>
			</ul>

			<h2>Valemid</h2>
			<p><strong>Reageerimisteekond</strong> = kiirus (m/s) × reaktsiooniaeg (s)</p>
			<p>
				Kiiruse saad meetriteks sekundis, kui jagad km/h 3,6-ga. 90 km/h on 25 m/s, seega 1-sekundilise
				reaktsiooniajaga sõidab auto enne pidurdamist <strong>25 meetrit</strong>.
			</p>
			<p><strong>Pidurdusteekond</strong> ≈ v² / (2 · μ · g)</p>
			<p>
				Siin on v kiirus meetrites sekundis, μ rehvi ja tee haardetegur ning g = 9,81 m/s². Haardetegur
				on kuival asfaldil heal rehvil umbes 0,8–1,0, märjal asfaldil sageli 0,5–0,7, lumel ja jääl
				palju väiksem. Kuna kiirus on ruudus, tähendab <strong>kaks korda suurem kiirus umbes neli
				korda pikemat pidurdusteekonda</strong>.
			</p>
			<p>
				Lihtne valem annab suurusjärgu. Päris pidurdusteekond sõltub ka sellest, kui kiiresti pidurid
				täisjõu saavutavad, ABS-ist, rehvi mustrisügavusest, veekihist ja temperatuurist.
				Pidurdusmaa.ee kalkulaator arvestab neid ja kasutab rehvi kohta päris andmeid: EL-i rehvimärgist
				ja sõltumatuid teste. Täpsemalt loe
				<a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">kuidas pidurdusmaa arvutatakse</a>.
			</p>

			{#if d}
				<h2>Näited eri kiirustel</h2>
				<p>
					Arvutatud kalkulaatori sama mudeliga: {d.car}. Reaktsiooniaeg 1 s. Märg asfalt: veekiht
					1 mm, +10 °C. Kuiv asfalt: +15 °C.
				</p>
				<p>
					Tabelis on peatumisteekond (suur number) ja selle sees olev pidurdusteekond (väike number).
				</p>
				<div class="tbl-wrap">
					<table class="t peat">
						<thead>
							<tr>
								<th>Kiirus</th>
								<th class="n">Reagee&shy;rimine</th>
								<th class="n">Kuival</th>
								<th class="n">Märjal</th>
							</tr>
						</thead>
						<tbody>
							{#each d.speeds as v, i (v)}
								<tr>
									<td class="nw"><b>{v}</b> km/h</td>
									<td class="n">{num(react(v))} m</td>
									<td class="n">
										<b>{num(react(v) + d.dry[i])} m</b><small>sh pidurdus {num(d.dry[i])}</small>
									</td>
									<td class="n">
										<b>{num(react(v) + d.wet[i])} m</b><small>sh pidurdus {num(d.wet[i])}</small>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
				<p>
					Madalal kiirusel on suurem osa peatumisteekonnast reageerimine: 50 km/h juures on see
					{num(react(50))} m, pidurdus kuival {num(d.dry[0])} m. Suurel kiirusel on vastupidi, sest
					pidurdusteekond kasvab ruudus.
				</p>
			{/if}

			<h2>Reaktsiooniaeg</h2>
			<p>
				Arvutustes võetakse tavaliselt umbes <strong>1 sekund</strong>. Kui juht on pidurdamiseks
				valmis (jalg juba pedaali kohal), võib see olla alla 1 sekundi. Väsimus, telefon, alkohol või
				ootamatu olukord venitavad selle kergesti 1,5–2 sekundini ja enamgi. 90 km/h juures tähendab iga
				lisasekund veel <strong>25 meetrit</strong> enne, kui auto üldse pidurdama hakkab.
			</p>

			<h2>Mis veel pidurdusteekonda muudab</h2>
			{#if d}
				<ul>
					<li>
						<strong>Rehv.</strong> Sama auto, sama märg tee, 90 km/h: EL-i märgise märghaardumise klass A
						{num(d.classA)} m, klass E {num(d.classE)} m.
					</li>
					<li>
						<strong>Mustrisügavus.</strong> Märjal 90 km/h: uus rehv (8 mm) {num(d.tread8)} m, kulunud (3
						mm) {num(d.tread3)} m.
					</li>
					<li>
						<strong>Hooaeg.</strong> Lumel 50 km/h: suverehviga {num(d.snowSummer)} m, talverehviga
						{num(d.snowWinter)} m.
					</li>
					<li>
						<strong>Koormus.</strong> Märjal 90 km/h: tühi auto {num(d.tread8)} m, 450 kg lisakoormaga
						{num(d.loaded)} m.
					</li>
				</ul>
			{/if}

			<h2>Arvuta oma auto peatumisteekond</h2>
			<p>
				<a href="/">Pidurdusmaa kalkulaatoris</a> vali oma auto, rehvimõõt, kiirus ja teeolud. Tulemuses
				vali <strong>„Peatumisteekond“</strong> ja reaktsiooniaeg: näed eraldi reageerimisteekonda ja
				pidurdusteekonda ning seda, kui palju muudaks teine rehv.
			</p>
			<p>
				Õpetamiseks ja kahe olukorra võrdlemiseks (nt 50 vs 70 km/h, uus vs kulunud rehv) on
				<a href="/liiklusohutus/">liiklusohutuse kalkulaator</a> — ilma hindade ja poodideta, esitlusrežiimiga
				klassiruumi jaoks.
			</p>

			<h2>Korduma kippuvad küsimused</h2>
			{#each KKK as [q, a] (q)}
				<h3>{q}</h3>
				<p>{a}</p>
			{/each}

			<p class="note">
				Arvud on arvutatud hinnang, mitte garantii. Ära kasuta neid liikluses otsustamiseks: hoia alati
				piisavat pikivahet ja vali kiirus teeolude järgi.
			</p>
			{/if}
		</article>
	</div>
</div>

<style>
	table.peat {
		min-width: 0;
	}
	table.peat small {
		white-space: normal;
		display: block;
		font-size: 12px;
		color: var(--muted);
		font-weight: 500;
	}
	table.peat .nw {
		white-space: nowrap;
	}
	@media (max-width: 480px) {
		table.peat th,
		table.peat td {
			padding: var(--sp-2) var(--sp-1);
			font-size: 13.5px;
		}
		table.peat th {
			letter-spacing: 0;
			white-space: normal;
		}
	}
</style>
