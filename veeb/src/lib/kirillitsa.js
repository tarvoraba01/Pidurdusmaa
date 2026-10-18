/* Automargid ja levinumad mudelid vene kirjas (otsingud „сузуки лиана размер шин“,
 * „форд мондео 3 размер шин“). Ainult vene lehe pealkirjas ja vastuselauses, aadressid
 * jäävad ladina tähtedega. Käsitsi valitud levinud kirjapildid: automaatset
 * translitereerimist ei tehta (vale nimi oleks hullem kui nime puudumine).
 * Numbritega mudelid (A4, X5, 308, CX-5) kirjutatakse ka vene keeles ladina tähtedega,
 * nii et neid siin pole: siis jääb ainult margi nimi. */

const MARK_RU = {
	'Alfa Romeo': 'Альфа Ромео', Audi: 'Ауди', BMW: 'БМВ', Cadillac: 'Кадиллак', Chevrolet: 'Шевроле', Chrysler: 'Крайслер',
	'Citroën': 'Ситроен', Dacia: 'Дачия', Dodge: 'Додж', Fiat: 'Фиат', Ford: 'Форд', GAZ: 'ГАЗ', Honda: 'Хонда', Hyundai: 'Хендай',
	Isuzu: 'Исузу', Jaguar: 'Ягуар', Jeep: 'Джип', Kia: 'Киа', 'Lada / VAZ': 'Лада', Lancia: 'Лянча', 'Land Rover': 'Ленд Ровер',
	Lexus: 'Лексус', Mazda: 'Мазда', 'Mercedes-Benz': 'Мерседес', MINI: 'Мини', Mitsubishi: 'Митсубиси',
	Nissan: 'Ниссан', Opel: 'Опель', Peugeot: 'Пежо', Porsche: 'Порше', Renault: 'Рено', Saab: 'Сааб', SEAT: 'Сеат', Smart: 'Смарт',
	SsangYong: 'СсангЙонг', Subaru: 'Субару', Suzuki: 'Сузуки', Tesla: 'Тесла', Toyota: 'Тойота', UAZ: 'УАЗ', Volkswagen: 'Фольксваген',
	Volvo: 'Вольво', 'Škoda': 'Шкода'
};

/* võti: „Mark|esimene sõna mudeli nimest“ */
const MUDEL_RU = {
	'Alfa Romeo|Giulia': 'Джулия', 'Alfa Romeo|Giulietta': 'Джульетта', 'Alfa Romeo|Stelvio': 'Стельвио',
	'Chevrolet|Aveo': 'Авео', 'Chevrolet|Captiva': 'Каптива', 'Chevrolet|Cruze': 'Круз', 'Chevrolet|Lacetti': 'Лачетти',
	'Chevrolet|Orlando': 'Орландо', 'Chevrolet|Spark': 'Спарк', 'Chevrolet|Trax': 'Тракс',
	'Chrysler|Grand': 'Гранд Вояджер', 'Chrysler|Sebring': 'Себринг',
	'Citroën|Berlingo': 'Берлинго', 'Citroën|C-Crosser': 'Си-Кроссер', 'Citroën|Jumper': 'Джампер', 'Citroën|Jumpy': 'Джампи',
	'Citroën|Xantia': 'Ксантия', 'Citroën|Xsara': 'Ксара',
	'Dacia|Duster': 'Дастер', 'Dacia|Logan': 'Логан', 'Dacia|Sandero': 'Сандеро', 'Dacia|Dokker': 'Доккер', 'Dacia|Lodgy': 'Лоджи',
	'Dacia|Jogger': 'Джоггер', 'Dacia|Spring': 'Спринг',
	'Dodge|Caliber': 'Калибр', 'Dodge|Challenger': 'Челленджер', 'Dodge|Charger': 'Чарджер', 'Dodge|Durango': 'Дуранго',
	'Dodge|Grand': 'Гранд Караван', 'Dodge|Journey': 'Джорни', 'Dodge|Nitro': 'Нитро',
	'Fiat|Bravo': 'Браво', 'Fiat|Doblò': 'Добло', 'Fiat|Ducato': 'Дукато', 'Fiat|Panda': 'Панда', 'Fiat|Punto': 'Пунто',
	'Fiat|Grande': 'Гранде Пунто', 'Fiat|Tipo': 'Типо', 'Fiat|Uno': 'Уно', 'Fiat|Freemont': 'Фримонт',
	'Ford|C-Max': 'Си-Макс', 'Ford|EcoSport': 'ЭкоСпорт', 'Ford|Edge': 'Эдж', 'Ford|Escort': 'Эскорт', 'Ford|Explorer': 'Эксплорер',
	'Ford|Fiesta': 'Фиеста', 'Ford|Focus': 'Фокус', 'Ford|Fusion': 'Фьюжн', 'Ford|Galaxy': 'Гэлакси', 'Ford|Kuga': 'Куга',
	'Ford|Mondeo': 'Мондео', 'Ford|Mustang': 'Мустанг', 'Ford|Puma': 'Пума', 'Ford|Ranger': 'Рейнджер', 'Ford|S-Max': 'Эс-Макс',
	'Ford|Sierra': 'Сиерра', 'Ford|Transit': 'Транзит',
	'GAZ|Volga': 'Волга',
	'Honda|Accord': 'Аккорд', 'Honda|Civic': 'Цивик', 'Honda|Jazz': 'Джаз',
	'Hyundai|Accent': 'Акцент', 'Hyundai|Getz': 'Гетц', 'Hyundai|Santa': 'Санта Фе', 'Hyundai|Sonata': 'Соната',
	'Hyundai|Tucson': 'Туссан', 'Hyundai|Kona': 'Кона', 'Hyundai|Matrix': 'Матрикс', 'Hyundai|Ioniq': 'Ионик',
	'Hyundai|Terracan': 'Терракан', 'Hyundai|Galloper': 'Галлопер',
	'Isuzu|D-Max': 'Д-Макс',
	'Jeep|Cherokee': 'Чероки', 'Jeep|Grand': 'Гранд Чероки', 'Jeep|Wrangler': 'Вранглер', 'Jeep|Compass': 'Компасс',
	'Jeep|Renegade': 'Ренегейд', 'Jeep|Patriot': 'Патриот', 'Jeep|Commander': 'Командер', 'Jeep|Avenger': 'Авенджер',
	'Kia|Ceed': 'Сид', 'Kia|Rio': 'Рио', 'Kia|Sportage': 'Спортейдж', 'Kia|Sorento': 'Соренто', 'Kia|Optima': 'Оптима',
	'Kia|Picanto': 'Пиканто', 'Kia|Soul': 'Соул', 'Kia|Carens': 'Каренс', 'Kia|Carnival': 'Карнивал', 'Kia|Niro': 'Ниро',
	'Kia|Stinger': 'Стингер', 'Kia|Stonic': 'Стоник', 'Kia|Venga': 'Венга',
	'Lada / VAZ|Granta': 'Гранта', 'Lada / VAZ|Kalina': 'Калина', 'Lada / VAZ|Largus': 'Ларгус', 'Lada / VAZ|Niva': 'Нива',
	'Lada / VAZ|Priora': 'Приора', 'Lada / VAZ|Samara': 'Самара', 'Lada / VAZ|Vesta': 'Веста',
	'Land Rover|Defender': 'Дефендер', 'Land Rover|Discovery': 'Дискавери', 'Land Rover|Freelander': 'Фрилендер',
	'Land Rover|Range': 'Рейндж Ровер',
	'Mercedes-Benz|Sprinter': 'Спринтер', 'Mercedes-Benz|Vito': 'Вито', 'Mercedes-Benz|Viano': 'Виано',
	'Mitsubishi|Lancer': 'Лансер', 'Mitsubishi|Outlander': 'Аутлендер', 'Mitsubishi|Pajero': 'Паджеро', 'Mitsubishi|Colt': 'Кольт',
	'Mitsubishi|Galant': 'Галант', 'Mitsubishi|Carisma': 'Каризма', 'Mitsubishi|Grandis': 'Грандис', 'Mitsubishi|Eclipse': 'Эклипс',
	'Mitsubishi|Space': 'Спейс Стар',
	'Nissan|Almera': 'Альмера', 'Nissan|Juke': 'Жук', 'Nissan|Leaf': 'Лиф', 'Nissan|Micra': 'Микра', 'Nissan|Murano': 'Мурано',
	'Nissan|Navara': 'Навара', 'Nissan|Note': 'Ноут', 'Nissan|Pathfinder': 'Патфайндер', 'Nissan|Patrol': 'Патрол',
	'Nissan|Primera': 'Примера', 'Nissan|Pulsar': 'Пульсар', 'Nissan|Qashqai': 'Кашкай', 'Nissan|Sunny': 'Санни',
	'Nissan|Terrano': 'Террано', 'Nissan|Tiida': 'Тиида', 'Nissan|X-Trail': 'Икс-Трейл',
	'Opel|Antara': 'Антара', 'Opel|Astra': 'Астра', 'Opel|Corsa': 'Корса', 'Opel|Insignia': 'Инсигния', 'Opel|Meriva': 'Мерива',
	'Opel|Mokka': 'Мокка', 'Opel|Omega': 'Омега', 'Opel|Vectra': 'Вектра', 'Opel|Zafira': 'Зафира', 'Opel|Signum': 'Сигнум',
	'Opel|Combo': 'Комбо', 'Opel|Vivaro': 'Виваро', 'Opel|Movano': 'Мовано', 'Opel|Kadett': 'Кадет', 'Opel|Ascona': 'Аскона',
	'Opel|Frontera': 'Фронтера', 'Opel|Crossland': 'Кроссленд', 'Opel|Grandland': 'Грандленд',
	'Peugeot|Partner': 'Партнер', 'Peugeot|Boxer': 'Боксер', 'Peugeot|Expert': 'Эксперт', 'Peugeot|Rifter': 'Рифтер',
	'Porsche|Cayenne': 'Кайен', 'Porsche|Macan': 'Макан', 'Porsche|Panamera': 'Панамера', 'Porsche|Taycan': 'Тайкан',
	'Renault|Arkana': 'Аркана', 'Renault|Captur': 'Каптюр', 'Renault|Clio': 'Клио', 'Renault|Espace': 'Эспас',
	'Renault|Fluence': 'Флюенс', 'Renault|Kadjar': 'Каджар', 'Renault|Kangoo': 'Кангу', 'Renault|Koleos': 'Колеос',
	'Renault|Laguna': 'Лагуна', 'Renault|Master': 'Мастер', 'Renault|Mégane': 'Меган', 'Renault|Scénic': 'Сценик',
	'Renault|Talisman': 'Талисман', 'Renault|Thalia': 'Талия', 'Renault|Trafic': 'Трафик', 'Renault|Twingo': 'Твинго',
	'Renault|Zoe': 'Зое',
	'SEAT|Alhambra': 'Альхамбра', 'SEAT|Altea': 'Альтеа', 'SEAT|Arona': 'Арона', 'SEAT|Ateca': 'Атека', 'SEAT|Córdoba': 'Кордоба',
	'SEAT|Ibiza': 'Ибица', 'SEAT|Leon': 'Леон', 'SEAT|Tarraco': 'Таррако', 'SEAT|Toledo': 'Толедо',
	'Škoda|Octavia': 'Октавия', 'Škoda|Superb': 'Суперб', 'Škoda|Fabia': 'Фабия', 'Škoda|Kodiaq': 'Кодиак', 'Škoda|Karoq': 'Карок',
	'Škoda|Rapid': 'Рапид', 'Škoda|Yeti': 'Йети', 'Škoda|Roomster': 'Румстер', 'Škoda|Kamiq': 'Камик', 'Škoda|Scala': 'Скала',
	'Škoda|Citigo': 'Ситиго', 'Škoda|Enyaq': 'Эньяк',
	'Subaru|Forester': 'Форестер', 'Subaru|Outback': 'Аутбэк', 'Subaru|Impreza': 'Импреза', 'Subaru|Legacy': 'Легаси',
	'Subaru|Tribeca': 'Трибека',
	'Suzuki|Swift': 'Свифт', 'Suzuki|Vitara': 'Витара', 'Suzuki|Grand': 'Гранд Витара', 'Suzuki|Liana': 'Лиана',
	'Suzuki|Jimny': 'Джимни', 'Suzuki|Ignis': 'Игнис', 'Suzuki|Splash': 'Сплэш', 'Suzuki|Baleno': 'Балено', 'Suzuki|Alto': 'Альто',
	'Toyota|Auris': 'Аурис', 'Toyota|Avensis': 'Авенсис', 'Toyota|Aygo': 'Айго', 'Toyota|Camry': 'Камри', 'Toyota|Carina': 'Карина',
	'Toyota|Corolla': 'Королла', 'Toyota|Highlander': 'Хайлендер', 'Toyota|Hilux': 'Хайлюкс', 'Toyota|Land': 'Ленд Крузер',
	'Toyota|Prius': 'Приус', 'Toyota|RAV4': 'РАВ4', 'Toyota|Verso': 'Версо', 'Toyota|Yaris': 'Ярис',
	'UAZ|Patriot': 'Патриот', 'UAZ|Hunter': 'Хантер',
	'Volkswagen|Amarok': 'Амарок', 'Volkswagen|Arteon': 'Артеон', 'Volkswagen|Beetle': 'Битл', 'Volkswagen|Bora': 'Бора',
	'Volkswagen|Caddy': 'Кадди', 'Volkswagen|Caravelle': 'Каравелла', 'Volkswagen|Crafter': 'Крафтер', 'Volkswagen|Fox': 'Фокс',
	'Volkswagen|Golf': 'Гольф', 'Volkswagen|Jetta': 'Джетта', 'Volkswagen|Lupo': 'Лупо', 'Volkswagen|Multivan': 'Мультивэн',
	'Volkswagen|Passat': 'Пассат', 'Volkswagen|Polo': 'Поло', 'Volkswagen|Scirocco': 'Сирокко', 'Volkswagen|Sharan': 'Шаран',
	'Volkswagen|T-Cross': 'Т-Кросс', 'Volkswagen|T-Roc': 'Т-Рок', 'Volkswagen|Taigo': 'Тайго', 'Volkswagen|Tiguan': 'Тигуан',
	'Volkswagen|Touareg': 'Туарег', 'Volkswagen|Touran': 'Туран', 'Volkswagen|Transporter': 'Транспортер'
};

/** „Киа Сид“, „Фольксваген Гольф“, „Ауди“ (mudel numbritega) või '' (tundmatu mark). */
export function autoRu(make, model) {
	const mk = MARK_RU[make];
	if (!mk) return '';
	const esim = String(model || '').split(/[ (]/)[0];
	const md = MUDEL_RU[make + '|' + esim];
	return md ? mk + ' ' + md : mk;
}
