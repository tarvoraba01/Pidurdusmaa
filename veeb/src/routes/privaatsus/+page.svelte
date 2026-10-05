<script>
	import Leht from '$lib/Leht.svelte';
	import { useLang } from '$lib/i18n.js';
	import { GA4_ID, ETTEVOTE, ETTEVOTE_REGKOOD, ETTEVOTE_AADRESS, ETTEVOTE_EPOST } from '$lib/seaded.js';
	const keel = useLang();

	/* Privaatsusteade. Kirjelda ainult seda, mida sait PÄRISELT teeb —
	   kui lisandub uus teenus (hinnad, uudiskiri, reklaam), tuleb see
	   leht enne avaldamist üle vaadata. Kolm keelt; eesti versioon on põhiline. */
	const ettevote = (reg, aadr) =>
		[ETTEVOTE, ETTEVOTE_REGKOOD ? reg + ' ' + ETTEVOTE_REGKOOD : '', ETTEVOTE_AADRESS ? aadr + ' ' + ETTEVOTE_AADRESS : ''].filter(Boolean).join(', ');
	const epost = ETTEVOTE_EPOST ? `<a href="mailto:${ETTEVOTE_EPOST}">${ETTEVOTE_EPOST}</a>` : '';

	const ET = {
		title: 'Privaatsus ja küpsised',
		desc: 'Mida Pidurdusmaa.ee kogub: küpsisteta kasutusstatistika, Google Analytics ainult nõusolekul, kontaktivormi andmed. Reklaami ei näita ja andmeid ei müü.',
		nupp: 'Muuda küpsiste valikut',
		sisu: `
<p><strong>Lühidalt:</strong> me ei küsi sinu nime ega e-posti, kui sa ise kontaktivormi ei täida. Statistikat kogume kolmel viisil: oma serveris ilma küpsisteta (lehe kasutus ja Plausible) ning — ainult sinu nõusolekul — Google Analyticsiga. Reklaami ei näita ja andmeid ei müü.</p>
<p><em>Viimati uuendatud 05.10.2026.</em></p>

<h2>Kes vastutab</h2>
<p>Pidurdusmaa.ee, ${ettevote('registrikood', 'aadress')}. Küsimused ja taotlused: <a href="/kontakt/">kontaktivorm</a>${epost ? ' või ' + epost : ''}.</p>

<h2>1. Kasutusstatistika ilma küpsisteta (alati)</h2>
<p>Kui kasutad lehte, saadab brauser meie serverisse lühikesed teated selle kohta, <em>mida lehel tehti</em>: milline automudel ja rehvimõõt valiti, mis kiirusel arvutati, mida otsiti, millised rehvid võrdlusse lisati. Nii näeme, millised osad on kasulikud ja mis ei tööta.</p>
<ul>
<li>Nime, e-posti ega küpsist selle juures <strong>ei ole</strong>.</li>
<li>Sinu IP-aadressi ei salvestata. Sellest arvutatakse räsi (pöördumatu lühend) juhusliku soolaga, mis on olemas ainult ühe päeva ja siis kustutatakse. Nii näeme, millised sündmused kuulusid samale külastusele, ja hoiame ära, et üks masin serverit üle ei ujutaks. Pärast päeva lõppu ei saa ka meie ise ühtki rida kellegi IP-ga seostada ega eri päevade külastusi kokku viia.</li>
<li>Selle jaoks ei kirjutata sinu brauserisse midagi.</li>
<li>Alus: õigustatud huvi teenust parandada. Kuna read on anonüümsed, hoiame neid pikemat aega, et näha, kuidas lehe kasutus aastate jooksul muutub.</li>
</ul>
<p>Külastuste koondstatistika (mitu külastust, millistelt lehtedelt, mis riigist, millise seadmega) tuleb <strong>Plausible</strong>'ist, mis töötab meie enda serveris (track.pidurdusmaa.ee), mitte kolmanda osapoole juures. Plausible ei kasuta küpsiseid, ei salvesta IP-aadressi ega jälgi sind teistel lehtedel: külastaja eristamiseks kasutab ta räsi, mis vahetub iga päev. Lisaks loendab ta mõnda tegevust (näiteks arvutus, valitud automudel, otsingusõna, klikk poe lingile) koondnumbritena. Alus: õigustatud huvi.</p>

<h2>2. Google Analytics (ainult nõusolekul)</h2>
<p>Kui vajutad küpsiste ribal „Nõustun“, laetakse Google Analytics 4. Enne seda ei tehta Google'isse ühtegi päringut. Google Analytics paneb brauserisse küpsised <code>_ga</code> ja <code>_ga_…</code> (säilivad kuni 2 aastat) ning näitab meile koondstatistikat: mitu külastajat, millistelt lehtedelt, millise seadmega, mis riigist.</p>
<ul>
<li>Töötleja on Google Ireland Ltd. Andmed võivad liikuda USA-sse EL–USA andmeraamistiku alusel.</li>
<li>Google Analytics 4 ei salvesta IP-aadressi.</li>
<li>Reklaamiküpsiseid ja reklaami isikupärastamist ei kasutata.</li>
<li>Alus: sinu nõusolek. Saad selle igal ajal tagasi võtta jaluses „Küpsiste seaded“ — siis GA küpsised kustutatakse.</li>
</ul>

<h2>3. Kontaktivorm</h2>
<p>Kui kirjutad meile, saame sinu nime, e-posti, soovi korral ettevõtte nime ja sõnumi. Kasutame neid ainult sulle vastamiseks ega lisa sind ühelegi listile. Kiri jõuab meieni e-postiga (Google Gmail) ja koopia jääb meie serverisse, et ükski kiri kaotsi ei läheks. Kontaktivormi kaitseb rämpsposti eest Cloudflare Turnstile: see kontrollib vormi saatmisel, et tegu on inimese ja päris brauseriga, ning saab selleks sinu IP-aadressi ja brauseri tehnilised andmed. Turnstile ei kasuta reklaamiküpsiseid ega jälgi sind teistel lehtedel. Turnstile laetakse ainult kontaktilehel. Serveris olev koopia kustub automaatselt 12 kuu pärast; e-postkastist kustutame kirja hiljemalt 12 kuud pärast suhtluse lõppu. Alus: sinu pöördumine (vastamine sinu soovile).</p>

<h2>4. Poelingid</h2>
<p>Kui vajutad rehvi juures poe lingile, lahkud Pidurdusmaa.ee-lt. Lingile lisatakse märge, et klikk tuli Pidurdusmaa.ee-lt (UTM-parameetrid); osa linke võib käia läbi partnerivõrgustiku. Pood või partnerivõrgustik võib panna oma küpsise, et müük meile arvestataks — see on nende töötlus ja nende privaatsustingimuste järgi. Meie ei saa sinu kohta isikuandmeid: näeme ainult koondina, mitu klikki ja ostu partnerite kaudu tuli. Kuidas partnerid lehe tasuta hoiavad: <a href="/teadmine/partnerid/">Partnerid ja poelingid</a>.</p>

<h2>5. Mida su brauser meelde jätab</h2>
<ul>
<li><strong>Valitud auto, ABS-i valik, võrdluskorv ja peatumisteekonna seaded</strong> (reaktsiooniaeg) ning lehe kerimiskoht — ainult selle vahelehe ajaks (<code>sessionStorage</code>), et need lehtede vahel liikudes alles oleksid. Kaob vahelehe sulgemisel.</li>
<li><strong>Liiklusohutuse kalkulaatori valikud</strong> on ainult lehe aadressis (pärast #-märki), et linki saaks jagada. Seda osa brauser serverisse ei saada.</li>
<li><strong>Sinu küpsiste valik</strong> (<code>localStorage</code>), et riba ei küsiks iga kord uuesti.</li>
<li><strong>Avaekraanile lisatud äpp</strong>: lehe failid ja varem avatud lehed hoitakse brauseri vahemälus, et leht avaneks kiiresti ja töötaks ka ilma võrguta. Hindu ega isikuandmeid sinna ei salvestata.</li>
</ul>
<p>Need on lehe toimimiseks vajalikud ega saada midagi kellelegi.</p>

<h2>6. Sinu õigused</h2>
<p>Võid küsida, milliseid andmeid meil sinu kohta on, ja nõuda nende parandamist või kustutamist. Kasutusstatistika on anonüümne (nime, e-posti ega IP-d pole), seega seda ei saa inimese järgi välja otsida. Kui arvad, et oleme sinu andmeid valesti töödelnud, võid pöörduda <a href="https://www.aki.ee" rel="noopener">Andmekaitse Inspektsiooni</a>.</p>

<h2>7. Muudatused</h2>
<p>Kui lehele lisandub uus teenus, mis andmeid kasutab, uuendame seda teadet enne selle kasutuselevõttu.</p>
`
	};

	const EN = {
		title: 'Privacy and cookies',
		desc: 'What Pidurdusmaa.ee collects: cookie-free usage statistics, Google Analytics only with consent, contact form data. No ads, and we do not sell data.',
		nupp: 'Change cookie settings',
		sisu: `
<p><strong>In short:</strong> we do not ask for your name or e-mail unless you fill in the contact form yourself. We collect statistics in three ways: on our own server without cookies (site usage and Plausible) and — only with your consent — with Google Analytics. We show no ads and do not sell data.</p>
<p><em>Last updated 05.10.2026. If the Estonian and English versions differ, the Estonian version prevails.</em></p>

<h2>Who is responsible</h2>
<p>Pidurdusmaa.ee, ${ettevote('registry code', 'address')}. Questions and requests: <a href="/kontakt/">contact form</a>${epost ? ' or ' + epost : ''}.</p>

<h2>1. Usage statistics without cookies (always)</h2>
<p>When you use the site, your browser sends short messages to our server about <em>what was done on the site</em>: which car model and tyre size were chosen, at which speed the calculation was made, what was searched for, which tyres were added to the comparison. This shows us which parts are useful and what does not work.</p>
<ul>
<li>There is <strong>no</strong> name, e-mail or cookie involved.</li>
<li>Your IP address is not stored. A hash (an irreversible short code) is calculated from it with a random salt that exists for one day only and is then deleted. This lets us see which events belonged to the same visit and prevents one machine from flooding the server. After the day ends, not even we can link any row to anyone's IP or connect visits from different days.</li>
<li>Nothing is written to your browser for this.</li>
<li>Legal basis: legitimate interest in improving the service. As the rows are anonymous, we keep them longer to see how use of the site changes over the years.</li>
</ul>
<p>Aggregate visit statistics (how many visits, from which pages, from which country, on which device) come from <strong>Plausible</strong>, which runs on our own server (track.pidurdusmaa.ee), not with a third party. Plausible uses no cookies, does not store IP addresses and does not track you on other sites: to tell visitors apart it uses a hash that changes every day. It also counts some actions (for example a calculation, the chosen car model, a search term, a click on a shop link) as totals. Legal basis: legitimate interest.</p>

<h2>2. Google Analytics (only with consent)</h2>
<p>If you click “Accept” on the cookie bar, Google Analytics 4 is loaded. Before that, no request is made to Google. Google Analytics sets the cookies <code>_ga</code> and <code>_ga_…</code> (kept for up to 2 years) and shows us aggregate statistics: how many visitors, from which pages, on which device, from which country.</p>
<ul>
<li>The processor is Google Ireland Ltd. Data may be transferred to the USA under the EU–US Data Privacy Framework.</li>
<li>Google Analytics 4 does not store IP addresses.</li>
<li>No advertising cookies or ad personalisation are used.</li>
<li>Legal basis: your consent. You can withdraw it at any time under “Cookie settings” in the footer — the GA cookies are then deleted.</li>
</ul>

<h2>3. Contact form</h2>
<p>When you write to us, we receive your name, e-mail, optionally your company name, and your message. We use them only to reply to you and do not add you to any list. The message reaches us by e-mail (Google Gmail) and a copy is kept on our server so that no message gets lost. The contact form is protected from spam by Cloudflare Turnstile: when the form is sent it checks that a person with a real browser is sending it, and for this it receives your IP address and technical browser data. Turnstile uses no advertising cookies and does not track you on other sites. Turnstile is loaded only on the contact page. The copy on the server is deleted automatically after 12 months; we delete the e-mail at the latest 12 months after the correspondence ends. Legal basis: your request (replying to it).</p>

<h2>4. Shop links</h2>
<p>When you click a shop link next to a tyre, you leave Pidurdusmaa.ee. The link carries a note that the click came from Pidurdusmaa.ee (UTM parameters); some links may go through a partner network. The shop or partner network may set its own cookie so the sale is credited to us — this is their processing, under their privacy terms. We receive no personal data about you: we only see totals of how many clicks and purchases came through partners.</p>

<h2>5. What your browser remembers</h2>
<ul>
<li><strong>The chosen car, ABS choice, comparison list and stopping distance settings</strong> (reaction time) and the scroll position — only for the current tab (<code>sessionStorage</code>), so they are kept while you move between pages. Cleared when the tab is closed.</li>
<li><strong>Road safety calculator choices</strong> are only in the page address (after the # sign) so the link can be shared. Browsers do not send this part to the server.</li>
<li><strong>Your cookie choice</strong> (<code>localStorage</code>), so the bar does not ask again every time.</li>
<li><strong>The app added to your home screen</strong>: site files and pages you have opened are kept in the browser cache so the site opens quickly and works offline. No prices or personal data are stored there.</li>
</ul>
<p>These are needed for the site to work and send nothing to anyone.</p>

<h2>6. Your rights</h2>
<p>You can ask what data we hold about you and request that it be corrected or deleted. Usage statistics are anonymous (no name, e-mail or IP), so they cannot be looked up by person. If you think we have processed your data incorrectly, you can contact the Estonian <a href="https://www.aki.ee/en" rel="noopener">Data Protection Inspectorate</a>.</p>

<h2>7. Changes</h2>
<p>If a new service that uses data is added to the site, we update this notice before it is introduced.</p>
`
	};

	const RU = {
		title: 'Конфиденциальность и куки',
		desc: 'Что собирает Pidurdusmaa.ee: статистика без куки, Google Analytics только с согласия, данные контактной формы. Рекламы нет, данные не продаём.',
		nupp: 'Изменить настройки куки',
		sisu: `
<p><strong>Коротко:</strong> мы не спрашиваем ваше имя или e-mail, если вы сами не заполните контактную форму. Статистику собираем тремя способами: на своём сервере без куки (использование сайта и Plausible) и — только с вашего согласия — через Google Analytics. Рекламу не показываем и данные не продаём.</p>
<p><em>Последнее обновление 05.10.2026. При расхождении эстонской и русской версий преимущество имеет эстонская.</em></p>

<h2>Кто отвечает</h2>
<p>Pidurdusmaa.ee, ${ettevote('регистрационный код', 'адрес')}. Вопросы и запросы: <a href="/kontakt/">контактная форма</a>${epost ? ' или ' + epost : ''}.</p>

<h2>1. Статистика использования без куки (всегда)</h2>
<p>Когда вы пользуетесь сайтом, браузер отправляет на наш сервер короткие сообщения о том, <em>что делалось на сайте</em>: какая модель авто и размер шин выбраны, на какой скорости сделан расчёт, что искали, какие шины добавили в сравнение. Так мы видим, какие части полезны и что не работает.</p>
<ul>
<li>Имени, e-mail или куки при этом <strong>нет</strong>.</li>
<li>Ваш IP-адрес не сохраняется. Из него вычисляется хэш (необратимый короткий код) со случайной «солью», которая существует только один день и затем удаляется. Так мы видим, какие события относятся к одному посещению, и не даём одной машине перегрузить сервер. После окончания дня даже мы не можем связать ни одну строку с чьим-либо IP или объединить посещения разных дней.</li>
<li>В ваш браузер для этого ничего не записывается.</li>
<li>Основание: законный интерес улучшать сервис. Поскольку строки анонимны, мы храним их дольше, чтобы видеть, как меняется использование сайта.</li>
</ul>
<p>Сводная статистика посещений (сколько посещений, с каких страниц, из какой страны, с какого устройства) поступает из <strong>Plausible</strong>, который работает на нашем собственном сервере (track.pidurdusmaa.ee), а не у третьей стороны. Plausible не использует куки, не сохраняет IP-адрес и не следит за вами на других сайтах: для различения посетителей он использует хэш, который меняется каждый день. Также он подсчитывает некоторые действия (например, расчёт, выбранная модель авто, поисковый запрос, клик по ссылке магазина) в виде общих чисел. Основание: законный интерес.</p>

<h2>2. Google Analytics (только с согласия)</h2>
<p>Если вы нажмёте «Согласен» на панели куки, загружается Google Analytics 4. До этого к Google не отправляется ни одного запроса. Google Analytics ставит в браузер куки <code>_ga</code> и <code>_ga_…</code> (хранятся до 2 лет) и показывает нам сводную статистику: сколько посетителей, с каких страниц, с какого устройства, из какой страны.</p>
<ul>
<li>Обработчик — Google Ireland Ltd. Данные могут передаваться в США на основании рамочного соглашения ЕС–США о защите данных.</li>
<li>Google Analytics 4 не сохраняет IP-адрес.</li>
<li>Рекламные куки и персонализация рекламы не используются.</li>
<li>Основание: ваше согласие. Его можно в любой момент отозвать в подвале сайта («Настройки куки») — тогда куки GA удаляются.</li>
</ul>

<h2>3. Контактная форма</h2>
<p>Когда вы нам пишете, мы получаем ваше имя, e-mail, по желанию название компании и сообщение. Используем их только для ответа вам и не добавляем вас ни в какие списки. Письмо приходит к нам по e-mail (Google Gmail), а копия хранится на нашем сервере, чтобы ни одно письмо не потерялось. Форму от спама защищает Cloudflare Turnstile: при отправке он проверяет, что форму отправляет человек из настоящего браузера, и для этого получает ваш IP-адрес и технические данные браузера. Turnstile не использует рекламные куки и не следит за вами на других сайтах. Turnstile загружается только на странице контактов. Копия на сервере удаляется автоматически через 12 месяцев; письмо из почтового ящика удаляем не позднее чем через 12 месяцев после окончания переписки. Основание: ваше обращение (ответ на него).</p>

<h2>4. Ссылки на магазины</h2>
<p>Нажимая на ссылку магазина у шины, вы покидаете Pidurdusmaa.ee. К ссылке добавляется пометка, что переход был с Pidurdusmaa.ee (параметры UTM); часть ссылок может идти через партнёрскую сеть. Магазин или партнёрская сеть может поставить свою куки, чтобы продажа была засчитана нам, — это их обработка по их условиям конфиденциальности. Мы не получаем о вас персональных данных: видим только общие числа кликов и покупок через партнёров.</p>

<h2>5. Что запоминает ваш браузер</h2>
<ul>
<li><strong>Выбранный автомобиль, выбор ABS, список сравнения и настройки остановочного пути</strong> (время реакции) и место прокрутки — только для текущей вкладки (<code>sessionStorage</code>), чтобы они сохранялись при переходе между страницами. Удаляется при закрытии вкладки.</li>
<li><strong>Настройки калькулятора безопасности движения</strong> хранятся только в адресе страницы (после знака #), чтобы ссылкой можно было поделиться. Браузер не отправляет эту часть на сервер.</li>
<li><strong>Ваш выбор куки</strong> (<code>localStorage</code>), чтобы панель не спрашивала каждый раз.</li>
<li><strong>Приложение на главном экране</strong>: файлы сайта и открытые ранее страницы хранятся в кэше браузера, чтобы сайт открывался быстро и работал без сети. Цены и персональные данные там не хранятся.</li>
</ul>
<p>Это нужно для работы сайта и никому ничего не отправляет.</p>

<h2>6. Ваши права</h2>
<p>Вы можете спросить, какие данные о вас у нас есть, и потребовать их исправления или удаления. Статистика использования анонимна (нет имени, e-mail или IP), поэтому её нельзя найти по человеку. Если вы считаете, что мы обработали ваши данные неправильно, можно обратиться в <a href="https://www.aki.ee/ru" rel="noopener">Инспекцию по защите данных</a>.</p>

<h2>7. Изменения</h2>
<p>Если на сайте появится новый сервис, использующий данные, мы обновим это уведомление до его запуска.</p>
`
	};

	const S = $derived(keel.lang === 'ru' ? RU : keel.lang === 'en' ? EN : ET);
</script>

<Leht title={S.title} desc={S.desc} path="privaatsus/" crumbs={[[S.title, '/privaatsus/']]} sisu={S.sisu} />

{#if GA4_ID}
	<div class="wrap" style="padding-bottom:var(--sp-12)">
		<button type="button" class="btn" onclick={() => window.PM_KUPSISED?.()}>{S.nupp}</button>
	</div>
{/if}
