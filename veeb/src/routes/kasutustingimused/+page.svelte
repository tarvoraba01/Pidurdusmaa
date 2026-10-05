<script>
	import Leht from '$lib/Leht.svelte';
	import { useLang } from '$lib/i18n.js';
	import { ETTEVOTE } from '$lib/seaded.js';
	const keel = useLang();

	const ET = {
		title: 'Kasutustingimused ja vastutus',
		desc: 'Pidurdusmaa.ee kasutustingimused: mis leht on, kuidas tulemusi tõlgendada ja milleks neid kasutada ei tohi.',
		sisu: `<p><strong>Lühidalt:</strong> Pidurdusmaa.ee näitab arvutatud hinnanguid üldiseks teadmiseks ja rehvide võrdlemiseks. Need ei ole mõõtmised, garantii ega ekspertarvamus. Ära tugine neile liikluses ega otsustes, millest sõltub kellegi ohutus.</p>
<h2>1. Mis see leht on</h2>
<p>Pidurdusmaa.ee (edaspidi „leht“) on ${ETTEVOTE} hallatav infoleht. Leht arvutab pidurdusmaa hinnangu mudeliga, mis põhineb avalikel andmetel: EL-i rehvimärgise registril (EPREL) ja sõltumatute väljaannete avaldatud rehvitestidel. Ettevõtte andmed: <a href="/kontakt/">Kontakt</a>.</p>
<h2>2. Tulemused on hinnangud</h2>
<ul><li>Iga number lehel on <strong>arvutatud hinnang</strong>, millel on veapiir. Päris pidurdusmaa sõltub paljust, mida leht ei tea ega küsi: juhi reaktsioonist, rehvide tegelikust seisukorrast ja rõhust, teekattest, veekihi paksusest, temperatuurist, pidurite ja ABS-i seisukorrast, koormast ja auto tehnilisest korrasolekust.</li><li>Päris elus võib pidurdusmaa olla lehel näidatust oluliselt pikem.</li><li>Rehvide võrdlus ja „sobivus sinu valikute põhjal“ on andmete kõrvutus, <strong>mitte ostunõuanne</strong> ega soovitus konkreetse toote kasuks.</li></ul>
<h2>3. Milleks lehte kasutada ei tohi</h2>
<ul><li>kiiruse, pikivahe või pidurdamise otsustamiseks liikluses — sõida alati vastavalt oludele ja liiklusseadusele;</li><li>liiklusõnnetuse asjaolude hindamiseks, ekspertarvamuseks, kindlustus- või kohtumenetluses tõendina;</li><li>sõiduki või rehvide tehnilise korrasoleku hindamiseks.</li></ul>
<h2>4. Andmed ja allikad</h2>
<ul><li>Rehvimärgise andmed pärinevad EL-i tooteregistrist EPREL, testitulemused kolmandate osapoolte avaldatud testidest. Iga allikas on lehel viidatud.</li><li>Andmetes võib olla vigu, lünki või aegunud infot. Me ei vastuta kolmandate osapoolte andmete õigsuse eest.</li><li>Tootjate ja toodete nimed ning kaubamärgid kuuluvad nende omanikele.</li><li>Leht näitab ainult omadusi, mille kohta on usaldusväärsed andmed, ega arva midagi juurde.</li></ul>
<h2>5. Poelingid ja vahendustasu</h2>
<p>Rehvide juures võivad olla lingid rehvipoodidesse. Osa neist on partnerlingid: kui ostad lingi kaudu, võib ${ETTEVOTE} saada poelt vahendustasu. Sinu hind sellest ei muutu. Pidurdusmaad ja rehvide järjestus arvutatakse ainult andmete põhjal ning vahendustasu ei mõjuta, milline rehv on eespool. Praegused partnerid: <a href="/teadmine/partnerid/">Partnerid ja poelingid</a>.</p>
<h2>6. Vastutuse piirang</h2>
<p>Leht ja selle sisu antakse kasutada „nagu on“, ilma otseste või kaudsete garantiideta. Seadusega lubatud ulatuses ei vastuta ${ETTEVOTE} otsese ega kaudse kahju eest, mis tuleneb lehe kasutamisest, sellele tuginemisest või selle kättesaamatusest. Kasutaja vastutab ise otsuste eest, mida ta lehe teabe põhjal teeb.</p>
<h2>7. Muudatused</h2>
<p>Arvutusmudel, andmed ja need tingimused võivad muutuda. Kehtib lehel avaldatud versioon.</p>`
	};

	const EN = {
		title: 'Terms of use and liability',
		desc: 'Pidurdusmaa.ee terms of use: what the site is, how to read the results and what they must not be used for.',
		sisu: `<p><strong>In short:</strong> Pidurdusmaa.ee shows calculated estimates for general information and for comparing tyres. They are not measurements, a guarantee or an expert opinion. Do not rely on them in traffic or in decisions on which anyone's safety depends.</p>
<h2>1. What this site is</h2>
<p>Pidurdusmaa.ee (the “site”) is an information site operated by ${ETTEVOTE}. The site estimates braking distance with a model based on public data: the EU tyre label register (EPREL) and tyre tests published by independent magazines. Company details: <a href="/kontakt/">Contact</a>.</p>
<h2>2. Results are estimates</h2>
<ul><li>Every number on the site is a <strong>calculated estimate</strong> with a margin of error. Real braking distance depends on much the site does not know or ask: the driver's reaction, the actual condition and pressure of the tyres, the road surface, the depth of water, temperature, the condition of the brakes and ABS, the load and the technical condition of the car.</li><li>In real life the braking distance may be considerably longer than shown.</li><li>Tyre comparisons and the “match with your choices” score are a side-by-side view of data, <strong>not purchasing advice</strong> or a recommendation of any product.</li></ul>
<h2>3. What the site must not be used for</h2>
<ul><li>deciding speed, following distance or braking in traffic — always drive according to the conditions and the Traffic Act;</li><li>assessing the circumstances of a traffic accident, as an expert opinion, or as evidence in insurance or court proceedings;</li><li>assessing the technical condition of a vehicle or tyres.</li></ul>
<h2>4. Data and sources</h2>
<ul><li>Tyre label data comes from the EU product register EPREL; test results come from tests published by third parties. Every source is cited on the site.</li><li>The data may contain errors, gaps or outdated information. We are not responsible for the accuracy of third-party data.</li><li>Manufacturer and product names and trademarks belong to their owners.</li><li>The site only shows properties for which there is reliable data and does not make anything up.</li></ul>
<h2>5. Shop links and commission</h2>
<p>Tyres may have links to tyre shops. Some of them are partner links: if you buy through such a link, ${ETTEVOTE} may receive a commission from the shop. Your price does not change. Braking distance and the order of tyres are calculated from data only, and commission does not affect which tyre is shown first.</p>
<h2>6. Limitation of liability</h2>
<p>The site and its content are provided “as is”, without any express or implied warranties. To the extent permitted by law, ${ETTEVOTE} is not liable for any direct or indirect damage arising from using the site, relying on it or its unavailability. Users are responsible for the decisions they make based on the information on the site.</p>
<h2>7. Changes</h2>
<p>The calculation model, the data and these terms may change. The version published on the site applies. If the Estonian and English versions differ, the Estonian version prevails.</p>`
	};

	const RU = {
		title: 'Условия использования и ответственность',
		desc: 'Условия использования Pidurdusmaa.ee: что это за сайт, как понимать результаты и для чего их нельзя использовать.',
		sisu: `<p><strong>Коротко:</strong> Pidurdusmaa.ee показывает расчётные оценки для общего ознакомления и сравнения шин. Это не измерения, не гарантия и не экспертное заключение. Не полагайтесь на них в дорожном движении и в решениях, от которых зависит чья-либо безопасность.</p>
<h2>1. Что это за сайт</h2>
<p>Pidurdusmaa.ee (далее «сайт») — информационный сайт, которым управляет ${ETTEVOTE}. Сайт оценивает тормозной путь с помощью модели на основе открытых данных: реестра маркировки шин ЕС (EPREL) и тестов шин, опубликованных независимыми изданиями. Данные компании: <a href="/kontakt/">Контакт</a>.</p>
<h2>2. Результаты — это оценки</h2>
<ul><li>Каждое число на сайте — <strong>расчётная оценка</strong> с погрешностью. Реальный тормозной путь зависит от многого, чего сайт не знает и не спрашивает: реакции водителя, фактического состояния и давления шин, покрытия, толщины слоя воды, температуры, состояния тормозов и ABS, загрузки и технического состояния автомобиля.</li><li>В реальности тормозной путь может быть значительно длиннее показанного.</li><li>Сравнение шин и «соответствие вашему выбору» — это сопоставление данных, <strong>а не совет по покупке</strong> и не рекомендация какого-либо товара.</li></ul>
<h2>3. Для чего сайт использовать нельзя</h2>
<ul><li>для выбора скорости, дистанции или момента торможения в движении — всегда ездите по условиям и по закону о дорожном движении;</li><li>для оценки обстоятельств ДТП, как экспертное заключение или доказательство в страховом или судебном разбирательстве;</li><li>для оценки технического состояния автомобиля или шин.</li></ul>
<h2>4. Данные и источники</h2>
<ul><li>Данные маркировки шин берутся из реестра ЕС EPREL, результаты тестов — из тестов, опубликованных третьими сторонами. Каждый источник указан на сайте.</li><li>В данных могут быть ошибки, пробелы или устаревшая информация. Мы не отвечаем за точность данных третьих сторон.</li><li>Названия производителей и товаров, а также товарные знаки принадлежат их владельцам.</li><li>Сайт показывает только те свойства, по которым есть надёжные данные, и ничего не додумывает.</li></ul>
<h2>5. Ссылки на магазины и комиссия</h2>
<p>У шин могут быть ссылки на шинные магазины. Часть из них — партнёрские: если вы покупаете по такой ссылке, ${ETTEVOTE} может получить от магазина комиссию. Ваша цена от этого не меняется. Тормозной путь и порядок шин рассчитываются только по данным, комиссия не влияет на то, какая шина показана первой.</p>
<h2>6. Ограничение ответственности</h2>
<p>Сайт и его содержание предоставляются «как есть», без явных или подразумеваемых гарантий. В пределах, допускаемых законом, ${ETTEVOTE} не несёт ответственности за прямой или косвенный ущерб, возникший в результате использования сайта, доверия к нему или его недоступности. Пользователь сам отвечает за решения, принятые на основе информации сайта.</p>
<h2>7. Изменения</h2>
<p>Модель расчёта, данные и эти условия могут меняться. Действует версия, опубликованная на сайте. При расхождении эстонской и русской версий преимущество имеет эстонская.</p>`
	};

	const S = $derived(keel.lang === 'ru' ? RU : keel.lang === 'en' ? EN : ET);
</script>

<Leht title={S.title} desc={S.desc} path="kasutustingimused/" crumbs={[[S.title, '/kasutustingimused/']]} lapsed={[]} sisu={S.sisu} />
