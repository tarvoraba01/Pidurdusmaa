<script>
	/* ABS — numbrid sama mudeliga mis kalkulaator (engine.js): VW Golf 8,
	   205/55 R16. Suverehv märgise klass B (kuiv, märg, kruus), Põhjamaade
	   talverehv klass D (lumi, jää). „Ilma ABS-ita“ = mudeli absClass NONE:
	   keskmine juht hädapidurdusel ilma ABS-ita (CAL.absEff NONE 0,74;
	   kruusal absEffGravel — seal on ABS-i mõju vastupidine). Ilma
	   reaktsiooniajata. Lumi ja jää −5 °C (jää = tüüpiline jää: 45 ajakirja
	   jäätesti mediaan, model.py ice_road_factor). Talverehvil
	   treadDepthNewMm 9 (muster 8 mm), suverehvil 8/8. Numbrid 13.10.2026.
	   Sama teema TikToki videos „ABS“. */
	import Leht from '$lib/Leht.svelte';
	import { ARTIKLID } from '$lib/artiklid.js';
	import { useLang, useT } from '$lib/i18n.js';
	const keel = useLang();
	const t = useT();
	const SLUG = 'abs-pidurdus';
	const A = ARTIKLID.find((a) => a.slug === SLUG);
	const ru = keel.lang === 'ru';

	const tabel = (pais, read) =>
		'<div class="tbl-wrap"><table class="t" style="min-width:0"><thead><tr>' +
		pais.map((p, i) => `<th${i ? ' class="n"' : ''}>${p}</th>`).join('') +
		'</tr></thead><tbody>' +
		read.map((r) => '<tr>' + r.map((c, i) => (i ? `<td class="n">${c}</td>` : `<td><strong>${c}</strong></td>`)).join('') + '</tr>').join('') +
		'</tbody></table></div>';

	const SISU = `<p>Paljud juhid arvavad, et ABS on selleks, et auto peatuks lühemalt. Tegelikult on tema põhitöö teine: ABS hoiab rattad veeremas, et saaksid pidurdades ka pöörata. Lühem pidurdusmaa on enamasti boonus, mitte eesmärk.</p>
<p>Numbrid on arvutatud sama mudeliga, mis <a href="/">kalkulaator</a>: VW Golf 8, rehvimõõt 205/55 R16, uued keskmised rehvid.</p>
<div class="note-box"><strong>Lühidalt.</strong> Lukustunud ratas libiseb nagu kelk ja auto sõidab otse, ükskõik kuhu rooli keerad. ABS laseb pidurit üle kümne korra sekundis lahti, et ratas jääks veerema ja rool töötaks. Hädaolukorras: pidur põhja, hoia all, ära pumpa ja vaata sinna, kuhu tahad minna.</div>

<h2>Mis juhtub ilma ABS-ita</h2>
<p>Kui pidurdad nii kõvasti, et ratas lukustub, hakkab rehv mööda teed libisema. Libisev rehv haarab teest halvemini kui veerev ja, mis veel olulisem, ei suuda autot pöörata. Keera rooli palju tahad, auto liigub ikka sinna, kuhu ta liikus.</p>
<p>Vanemates autodes õpetati seepärast pidurit pumpama. ABS teeb sama, aga palju kiiremini ja iga rattaga eraldi.</p>

<h2>Mida ABS teeb</h2>
<p>ABS jälgib iga ratta pöörlemist. Kui mõni ratas hakkab lukustuma, vähendab ABS selle ratta pidurirõhku hetkeks ja suurendab seda siis uuesti. Seda kordub üle kümne korra sekundis. Ratas jääb haarde piirile: pidurdab peaaegu nii kõvasti kui võimalik, aga veereb.</p>
<p>Juht tunneb seda pedaali värinana ja kuuleb krigistamist. See on normaalne: nii ABS töötabki.</p>

<h2>Kui palju ABS pidurdusmaad muudab</h2>
<p>Võrdluseks on keskmine juht, kes pidurdab hädaolukorras ilma ABS-ita (rattad lukustuvad või pidur lastakse liiga palju lahti):</p>
${tabel(
		['Olud', 'ABS-iga', 'Ilma ABS-ita'],
		[
			['Kuiv asfalt, 80 km/h', '23,7 m', '32,4 m'],
			['Märg asfalt, 80 km/h', '34,7 m', '46,2 m'],
			['Tallatud lumi, 50 km/h', '27,1 m', '36,0 m'],
			['Jää, 50 km/h', '59,9 m', '77,4 m'],
			['Kruus, 50 km/h', '20,4 m', '16,0 m']
		]
	)}
<p>Asfaldil, lumel ja jääl peatub ABS-iga auto keskmisest juhist lühemalt. Väga osav juht võib ilma ABS-ita sama tulemuse saada, aga hädaolukorras, ehmatusega, ei õnnestu see peaaegu kellelgi.</p>

<h2>Erand: kruus ja kohev lumi</h2>
<p>Kruusal ja sügavas kohevas lumes kuhjub lukustatud ratta ette vall, mis aitab autot peatada. ABS ei lase sellel tekkida, sest ratas veereb. Seepärast võib ABS-iga pidurdusmaa seal olla pikem: mudeli järgi kruusal 50 km/h pealt 20,4 m, lukustatud ratastega 16,0 m.</p>
<p>Ometi ei tasu ABS-i ka seal karta: lukustatud ratastega ei saa sa takistusest mööda keerata. Hoia lahtisel pinnal lihtsalt väiksemat kiirust ja suuremat vahet.</p>

<h2>Kuidas hädaolukorras pidurdada</h2>
<ul><li><strong>Pidur põhja.</strong> Vajuta kohe ja täie jõuga, ära proovi „ettevaatlikult“.</li><li><strong>Hoia all.</strong> Ära lase pedaali lahti enne, kui auto seisab või oht on möödas.</li><li><strong>Ära pumpa.</strong> ABS teeb seda ise ja palju kiiremini. Pumpamine annab ainult pikema pidurdusmaa.</li><li><strong>Vaata sinna, kuhu tahad minna.</strong> Auto läheb sinna, kuhu vaatad ja rooli keerad. Pidurdades saab ABS-iga takistusest mööda pöörata.</li><li><strong>Värin ja krigin on normaalsed.</strong> Need tähendavad, et ABS töötab.</li></ul>

<h2>Kui ABS-i tuli põleb</h2>
<p>Kollane ABS-i märgutuli näidikul tähendab, et ABS ei tööta. Tavalised pidurid töötavad edasi, aga hädapidurdusel võivad rattad lukustuda. Lase see võimalikult kiiresti üle vaadata. Kui põleb punane pidurituli, ära sõida edasi.</p>

<h2>Proovi oma autoga</h2>
<ul><li><a href="/">Pidurdusmaa kalkulaator</a>: sinu auto, rehvid ja teeolud</li><li><a href="/liiklusohutus/kurv/">Pidurdamine kurvis</a>: miks paremad rehvid peavad olema taga</li><li><a href="/teadmine/artiklid/reaktsiooniaeg/">Reaktsiooniaeg: üks sekund on 90 km/h juures 25 meetrit</a></li></ul>
<p class="note">Arvutatud tulemused on hinnangud, mitte mõõtmised. Mudeli täpsus ja eeldused: <a href="/teadmine/kuidas-pidurdusmaa-arvutatakse/">Kuidas pidurdusmaa arvutatakse</a>.</p>`;

	const SISU_RU = `<p>Многие водители думают, что ABS нужен для того, чтобы машина останавливалась быстрее. На самом деле его главная задача другая: ABS не даёт колёсам заблокироваться, чтобы при торможении можно было ещё и поворачивать. Более короткий тормозной путь — чаще бонус, а не цель.</p>
<p>Цифры рассчитаны той же моделью, что и <a href="/ru/">калькулятор</a>: VW Golf 8, размер шин 205/55 R16, новые средние шины.</p>
<div class="note-box"><strong>Коротко.</strong> Заблокированное колесо скользит как санки, и машина едет прямо, куда бы вы ни повернули руль. ABS отпускает тормоз больше десяти раз в секунду, чтобы колесо продолжало катиться, а руль работал. В опасной ситуации: тормоз в пол, держите, не качайте и смотрите туда, куда хотите ехать.</div>

<h2>Что происходит без ABS</h2>
<p>Если тормозить так сильно, что колесо блокируется, шина начинает скользить по дороге. Скользящая шина держит дорогу хуже, чем катящаяся, и, что ещё важнее, не может повернуть машину. Поворачивайте руль сколько угодно — машина всё равно движется туда, куда двигалась.</p>
<p>Поэтому на старых машинах учили «качать» тормоз. ABS делает то же самое, но гораздо быстрее и для каждого колеса отдельно.</p>

<h2>Что делает ABS</h2>
<p>ABS следит за вращением каждого колеса. Если какое-то колесо начинает блокироваться, ABS на мгновение снижает давление в его тормозе, а затем снова повышает. Это повторяется больше десяти раз в секунду. Колесо остаётся на пределе сцепления: тормозит почти максимально, но катится.</p>
<p>Водитель чувствует это как вибрацию педали и слышит треск. Это нормально: так ABS и работает.</p>

<h2>Насколько ABS меняет тормозной путь</h2>
<p>Для сравнения — средний водитель, который в опасной ситуации тормозит без ABS (колёса блокируются или тормоз слишком сильно отпускается):</p>
${tabel(
		['Условия', 'С ABS', 'Без ABS'],
		[
			['Сухой асфальт, 80 км/ч', '23,7 м', '32,4 м'],
			['Мокрый асфальт, 80 км/ч', '34,7 м', '46,2 м'],
			['Укатанный снег, 50 км/ч', '27,1 м', '36,0 м'],
			['Лёд, 50 км/ч', '59,9 м', '77,4 м'],
			['Гравий, 50 км/ч', '20,4 м', '16,0 м']
		]
	)}
<p>На асфальте, снегу и льду машина с ABS останавливается раньше, чем у среднего водителя без ABS. Очень опытный водитель может добиться того же без ABS, но в опасной ситуации, в испуге, это почти никому не удаётся.</p>

<h2>Исключение: гравий и рыхлый снег</h2>
<p>На гравии и в глубоком рыхлом снегу перед заблокированным колесом образуется вал, который помогает остановить машину. ABS не даёт ему появиться, потому что колесо катится. Поэтому тормозной путь с ABS там может быть длиннее: по модели на гравии с 50 км/ч 20,4 м, с заблокированными колёсами 16,0 м.</p>
<p>Но и там не стоит бояться ABS: с заблокированными колёсами вы не сможете объехать препятствие. На рыхлом покрытии просто держите меньшую скорость и большую дистанцию.</p>

<h2>Как тормозить в опасной ситуации</h2>
<ul><li><strong>Тормоз в пол.</strong> Сразу и изо всех сил, не пытайтесь «аккуратно».</li><li><strong>Держите.</strong> Не отпускайте педаль, пока машина не остановится или опасность не минует.</li><li><strong>Не качайте.</strong> ABS делает это сам и гораздо быстрее. Качание только удлиняет тормозной путь.</li><li><strong>Смотрите туда, куда хотите ехать.</strong> Машина едет туда, куда вы смотрите и поворачиваете руль. С ABS можно объехать препятствие, продолжая тормозить.</li><li><strong>Вибрация и треск — это нормально.</strong> Значит, ABS работает.</li></ul>

<h2>Если горит лампа ABS</h2>
<p>Жёлтая контрольная лампа ABS на приборной панели означает, что ABS не работает. Обычные тормоза продолжают работать, но при экстренном торможении колёса могут заблокироваться. Проверьте систему как можно скорее. Если горит красная лампа тормозов, дальше не езжайте.</p>

<h2>Проверьте на своём автомобиле</h2>
<ul><li><a href="/ru/">Калькулятор тормозного пути</a>: ваша машина, шины и дорожные условия</li><li><a href="/ru/liiklusohutus/kurv/">Торможение в повороте</a>: почему лучшие шины должны стоять сзади</li><li><a href="/ru/teadmine/artiklid/reaktsiooniaeg/">Время реакции: на 90 км/ч одна секунда — это 25 метров</a></li></ul>
<p class="note">Расчётные результаты — это оценки, а не измерения. Точность модели и допущения: <a href="/ru/teadmine/kuidas-pidurdusmaa-arvutatakse/">Как рассчитывается тормозной путь</a>.</p>`;

	const KKK = [
		['Kas ABS lühendab pidurdusmaad?', 'Asfaldil, lumel ja jääl enamasti jah, võrreldes keskmise juhiga ilma ABS-ita: märjal asfaldil 80 km/h pealt mudeli järgi 34,7 m vs 46,2 m. Põhitöö on aga hoida rattad veeremas, et saaksid pidurdades pöörata.'],
		['Kas ABS-iga autos tohib pidurit pumbata?', 'Ei. Vajuta pidur põhja ja hoia all. ABS laseb pidurit ise üle kümne korra sekundis lahti, pumpamine teeb pidurdusmaa ainult pikemaks.'],
		['Miks pedaal ABS-iga pidurdades väriseb?', 'ABS vähendab ja suurendab pidurirõhku kiiresti järjest. Juht tunneb seda pedaali värinana ja kuuleb krigistamist. See on normaalne ja tähendab, et ABS töötab.'],
		['Kus võib ABS pidurdusmaad pikendada?', 'Kruusal ja sügavas kohevas lumes, kus lukustatud ratta ette kuhjuv vall aitab peatuda. Mudeli järgi kruusal 50 km/h pealt 20,4 m ABS-iga ja 16,0 m lukustatud ratastega.']
	];
	const KKK_RU = [
		['Сокращает ли ABS тормозной путь?', 'На асфальте, снегу и льду обычно да, по сравнению со средним водителем без ABS: на мокром асфальте с 80 км/ч по модели 34,7 м против 46,2 м. Но главная задача — не дать колёсам заблокироваться, чтобы при торможении можно было поворачивать.'],
		['Нужно ли качать тормоз в машине с ABS?', 'Нет. Нажмите тормоз в пол и держите. ABS сам отпускает тормоз больше десяти раз в секунду, а качание только удлиняет тормозной путь.'],
		['Почему педаль вибрирует при торможении с ABS?', 'ABS быстро снижает и снова повышает давление в тормозах. Водитель чувствует это как вибрацию педали и слышит треск. Это нормально и означает, что ABS работает.'],
		['Где ABS может удлинить тормозной путь?', 'На гравии и в глубоком рыхлом снегу, где вал перед заблокированным колесом помогает остановиться. По модели на гравии с 50 км/ч 20,4 м с ABS и 16,0 м с заблокированными колёсами.']
	];

	const T = ru ? { ...A, ...A.ru } : A;
</script>

<Leht
	title={T.title}
	desc={T.desc}
	path={'teadmine/artiklid/' + SLUG + '/'}
	crumbs={[[t('Teadmine'), '/teadmine/'], [t('Artiklid'), '/teadmine/artiklid/'], [T.title, '/teadmine/artiklid/' + SLUG + '/']]}
	lapsed={[]}
	uuendatud={A.kuupaev}
	avaldatud={A.kuupaev}
	sisu={ru ? SISU_RU : SISU}
	kkk={ru ? KKK_RU : KKK}
/>
