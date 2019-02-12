Weekend Flights
	Для начала упростить, т.к. если буду пытаться сделать идеально, то просто не доделаю.
	Я работаю как обычный офисный клерк, у которого всего лишь 28 календарных дней отпуска. Чтобы иметь возможность путешествовать, мне захотелось попробовать путешествовать на выходных. Я так уже делал для поездой домой в Уфу - вылет в пятницу после работы, прилет в понедельник до работы, либо в воскресенье поздно вечером. Тогда я нашел билеты на распродаже по 1000 рублей в одну сторону. Мне захотелось автоматизировать процесс поиска билетов на выходные со скидкой, которые периодически выбрасывают авиакомпании. Для этого и был написан данный скрипт. 
	Стоит отметить, что это не полноценный поиск авиабилетов и не все билеты могут быть найдены, т.к. сюда попадает только кэш поиска. Подробнее на сайте travelpayoyuts в их описании API, которое используется в данном скрипте.
	Скрипт предназначен для мониторинга авиабилетов по определенным параметрам. Поиск производится по API от travelpayouts, в котором хранятся данные по поиску авиабилетов за последние 48 часов. Документацию к API можно посмотреть здесь: ссылка.
	В моем случае настроено ежечасное выполнение скрипта. При нахождении билетов я получаю push-уведомление на телефон, также информация о найденном билете со ссылкой на поиск публикуется в моей группе во Вконтакте.
	На основе скрипта можно сделать телеграм бота, который будет отслеживать необходимые билеты. 
	ЕЩе минус в том, что в ответе от АПИ не возвращается время вылета и прилета.
	Список стран в нужный формат переводил сам, используя файл от АПИ со списком стран. Для себя просто отфильтровал те страны, в которые готов поехать на выходные, в основном это Европа.
	Плюс в том, что это можно монетизировать, т.к. трэвэлпэйаутс это партерка.
	Может это опубликовать на хабре? Типа как я сделал домашний скрипт для поиска билетов. 

Как использовать
	как настроить на Unix - можно дать ссылку на инструкцию по настройке Cron
	как настроить на винде с помощью nnCron, описать вкратце в текстовом виде
	

Как запустить для теста

Как получать нужные токены
	описать, как получать токен для вк и нюансы по поводу IP
		чтобы скрипт мог постить найденные билеты на стену группы, необходимо
		сначала необходимо создать Standalone-приложение в ВК
		затем получить access_token с доступом к стене (wall)
		для этого найти ID этого приложения и через браузер пройти по ссылке
		https://oauth.vk.com/authorize?client_id=1234567&scope=wall,offline&redirect_uri=https://oauth.vk.com/blank.html&response_type=token
		в ответ будет редирект на страницу, в адресе которой будет токен
		https://oauth.vk.com/blank.html#access_token=asdfkjasdf876k4h3gftk2hjg4bnvf2ggk3hkj3hgj2hkjh35hb2j3hgj4bnh4g3n4bh3g4bn&expires_in=0&user_id=9876543
		после этого можно использовать токен для запроса, который указан в функции post_to_vk
		важно: чтобы была возможность публиковать на стене группы от имени группы, необходимо иметь права админа этой группы
	
	описать, как получить токен для трэвэлпэйаутс
		Очень просто - достаточно зарегистрироваться в [travelpayouts.com](https://www.travelpayouts.com/)
		После регистрации на странице https://www.travelpayouts.com/developers/api будет доступен API токен

	описать, как получить токен для ifttt
		IFTTT - удобный сервис автоматизации рутинных задач, который в том числе предоставляет возможность отправлять уведомления на телефон через webhooks, если у вас на телефоне установлено приложение IFTTT
		Для этого необходимо зарегистрироваться на их сайте, затем



Описать, что у меня в private.py - какие ключи нужно получить

Описать, что делает каждая функция, можно кратко, т.к. еще может все поменяться

Как настроить nnCron
	нюансы с логами - надо указывать полный путь от диска С
	с путями до папок, которые содержали русские имена, возникали проблемы, поэтому я сделал папку со скриптом на самом диске С
	nnCron для Windows 7 можно скачать по ссылке в этой ветке форума http://www.nncron.ru/forums/viewtopic.php?p=33983
	чтобы сделать задание, необходимо нажать правой кнопкой на иконку запущенной программы (обычно она в трее), 
	далее New Task, откроется окно
	чтобы настроить ежечасное выполнение скрипта, ...
	галочка active 
	далее на вкладке необходимо выбрать "Run application or open document"
