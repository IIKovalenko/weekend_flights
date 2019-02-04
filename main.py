import requests
import json
import datetime
import time
import logging
from weekends import weekends, may_weekends, weekday_names
from countries import countries, country_codes, country_names_dict
from cities import cities

# Существует пять уровней логирования (в порядке возрастания): DEBUG, INFO, WARNING, ERROR и CRITICAL

root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
# handler = logging.StreamHandler(sys.stdout) # для вывода в консоль
handler = logging.FileHandler('main.log', encoding='utf-8')
formatter = logging.Formatter('LINE:%(lineno)3d # %(levelname)-8s [%(asctime)s]  %(message)s')
handler.setFormatter(formatter)
root_logger.addHandler(handler)

# TODO:
# 1. Очистить функцию find_weekend_flight - она должна только находить и возвращать какой-то список, а не вызывать фунцию post_to_vk
#       вызов функции post_to_vk надо сделать в main(), чтобы потом можно было написать новую функцию поиска через другой метод API, и чтобы все заработало
# 2. Сделать функцию для печати результата поиска
# 3. ГОТОВО - Сделать функцию для отправки результатов поиска куда-либо (например, в паблик в вк)
# 4. Сделать логирование в двух режимах - стандартный и дебаг на случай ошибок
# 5. Написать для себя краткую документацию в README.md
# 6. Спрятать токены: авиасейлза и вконтактовский
# 7. Перевести все уведомления на русский язык
# 8. Запустить поиск на майские
# 9. Запустить поиск в Уфу на выходные со стоимостью меньше 5 тысяч

# 10. Убрать из бота даты на март, в которые будем в Италии
# 11. Добавить дополнительно в функцию search_flights поиск билетов на майские
# 12. Сделать отдельный список городов, которые исключить из поиска (Сургут и тд)
# 13. Уменьшить стоимость билетов на выходные до 4к 
# 14. Стоимость билетов на майские сделать <=7к
# 15. Попробовать через IFTT придумать, как отправлять себе именно уведомления, а не просто в паблик в вк, может у них есть апи?
#       уже придумал, осталось реализовать через функцию
#       пример кода в файле ifttt_test.py
#       лучше посмотреть здесь, как реализована функция post_ifttt_webhook
# 16. Начать все делать частые коммиты, т.е. после каждого изменения коммитить с описанием изменений, тем более в винде это легко делать с помощью проги от гита. 
# 17. Причесать код (чистые функции и т.д.), сделать хороший ридми, скрыть все токены и другую персональную инфу и выложить реощиторий в открытый доступ — не надо жадничать! Надо давать этому миру. 
# Тем более, что это будет проект, который я смогу показать как пример своей работы.
# 18. В ридми надо описать, можно ссылкой на отдельный файл — как запустить крон на винде и на юниксе, чтобы скрипт работал всегда. Если настрою что-то через IFTT, то тоже описать, как все настроить.
# 19. Сделать, чтобы find_flights искала сразу по нужным направлениям, которые бы принимала в качестве аргумента

def post_to_vk(flight_dict):
    root_logger.debug('Func "post_to_vk" has started')
    root_logger.debug('got flight_dict as input: {}'.format(flight_dict))
    # ключ, полученный по спец ссылке (надо будет получать снова при обновлении ip-адреса)
    # для этого в адресной строке браузера ввел типа такого и получил заветный токен доступа.
    # запрос:
    # https://oauth.vk.com/authorize?client_id=6839704&scope=wall,offline&redirect_uri=https://oauth.vk.com/blank.html&response_type=token
    # ответ с токеном:
    # https://oauth.vk.com/blank.html#access_token=c5feed7bce2122333cd50320cf80831e2b0a23a7b50c0cec5da901981f272a9155c3d7912def3d42705bb&expires_in=0&user_id=5286231
    token = 'c5feed7bce2122333cd50320cf80831e2b0a23a7b50c0cec5da901981f272a9155c3d7912def3d42705bb'
    application_id = 6839704
    group_id = 177516719
    owner_id_group = -177516719

    # надо сделать из словаря с информацией о перелете flight_dict ссылку, которую опубликовать в вк
    data = 'Перелет {origin} - {destination}, '\
            'c {depart_date} ({depart_week_day}) '\
            'по {return_date} ({return_week_day}) за {value} рублей: '\
            '{link}'.format(
                    origin=flight_dict['origin'],
                    destination=flight_dict['destination'],
                    depart_date=flight_dict['depart_date'],
                    depart_week_day=flight_dict['depart_week_day'],
                    return_date=flight_dict['return_date'],
                    return_week_day=flight_dict['return_week_day'], 
                    value=flight_dict['value'],
                    link=flight_dict['link']
                )

    # из ответа на тостере, как правильно делать:
    response = requests.post('https://api.vk.com/method/wall.post', data={'access_token': token,
                                                                        'owner_id': owner_id_group,
                                                                        'from_group': 1,
                                                                        'message': data,
                                                                        'signed': 0,
                                                                       'v':"5.52"}).json()

    root_logger.debug(response)
    root_logger.debug('Func "post_to_vk" has finished')


# здесь надо передавать сразу словарь с value1, value2, value3
def post_ifttt_webhook(event, data):
    # продумать, как хранить ключ - надо со всеми остальными секретными ключами
    # IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{your-IFTTT-key}'
    # Вставка желаемого события
    # ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # ниже неправильная версия, надо передавать и название ивента, и словарь со значениями
    ifttt_event_url = 'https://maker.ifttt.com/trigger/ticket_found/with/key/iKJF3s9xrt82AH9e3GAbYHPf9YqJwdx3yYy_ZJZil2H'
    # Отправка запроса HTTP POST в URL вебхука
    requests.post(ifttt_event_url, json=data)


# function, which gets cheapest flights for last 48 hours (https://support.travelpayouts.com/hc/ru/articles/203956163#02)
def get_latest_prices_of_month(destination, beginning_of_period):
    root_logger.debug('Func "get_latest_prices_of_month" has started')
    TOKEN = 'a4da858f9d18ab2292ecbb4dddec4485'
    url='http://api.travelpayouts.com/v2/prices/latest'
    payload = {
        'token': TOKEN, 
        'origin': 'MOW',
        'destination': destination,
        'beginning_of_period': beginning_of_period,
        'period_type': 'month', 
        # 'period_type': 'year', 
        'limit': 1000
    }
    response = requests.get(url, params=payload)
    root_logger.debug('Func "get_latest_prices_of_month" has finished')
    return response.json()


def find_weekend_flights(flights_data, days, max_value):
    root_logger.debug('Func "find_weekend_flights" has started')

    # здесь будут словарь по найденным перелетам
    found_flights = []

    for flight in flights_data:
        root_logger.debug('Flight: {}'.format(flight))

        found_at = flight['found_at']

        try:
            found_at_datetime = datetime.datetime.strptime(found_at, '%Y-%m-%dT%H:%M:%S')
        except:
            found_at_datetime = datetime.datetime.strptime(found_at, '%Y-%m-%dT%H:%M:%S.%f')
        
        time_now = datetime.datetime.now()
        time_difference = time_now - found_at_datetime
        time_difference_in_hours = time_difference / datetime.timedelta(hours=1)

        if time_difference_in_hours <= 24 and flight['value'] <= max_value:
            for date in days:
                root_logger.debug('Comparing with date {}'.format(date))
                if flight['depart_date'] == date[0] and flight['return_date'] == date[1]:
                    depart_date_formatted = ''.join(reversed(flight['depart_date'][5:].split('-')))
                    return_date_formatted = ''.join(reversed(flight['return_date'][5:].split('-')))

                    depart_date_str_list = flight['depart_date'].split('-')
                    depart_date_int_list = [int(elem) for elem in depart_date_str_list]
                    depart_date = datetime.date(depart_date_int_list[0], depart_date_int_list[1], depart_date_int_list[2])
                    depart_week_day = depart_date.isoweekday()

                    return_date_str_list = flight['return_date'].split('-')
                    return_date_int_list = [int(elem) for elem in return_date_str_list]
                    return_date = datetime.date(return_date_int_list[0], return_date_int_list[1], return_date_int_list[2])
                    return_week_day = return_date.isoweekday()

                    origin = cities[flight['origin']]
                    destination = cities[flight['destination']]

                    root_logger.info('{origin} - {destination} '\
                        'from {depart_date} ({depart_week_day}) '\
                        'to {return_date} ({return_week_day}) '\
                        'for {value} rub'.format(
                                origin=origin,
                                destination=destination,
                                depart_date=flight['depart_date'],
                                depart_week_day=weekday_names[depart_week_day],
                                return_date=flight['return_date'],
                                return_week_day=weekday_names[return_week_day],
                                value=flight['value']
                            ))
                    link = 'https://www.aviasales.ru/search/{}{}{}{}1?marker=207849'.format(
                        flight['origin'],
                        depart_date_formatted,
                        flight['destination'],
                        return_date_formatted
                    )
                    root_logger.info(link)
                    root_logger.info('Flight found at {}'.format(flight['found_at']))

                    flight_dict = {
                        'origin': origin,
                        'destination': destination,
                        'depart_date': flight['depart_date'],
                        'depart_week_day': weekday_names[depart_week_day],
                        'return_date': flight['return_date'],
                        'return_week_day': weekday_names[return_week_day],
                        'value': flight['value'],
                        'link': link
                    }
                    found_flights.append(flight_dict)
                    
    root_logger.debug('Func "find_weekend_flights" has finished, found {} flights'.format(len(found_flights)))
    return found_flights

def main():
    root_logger.debug('Func "main" has started')
    months = {
        'february': '2019-02-01',
        'march': '2019-03-01',
        'april': '2019-04-01',
        'may': '2019-05-01',
        'june': '2019-06-01',
        'july': '2019-07-01',
        'august': '2019-08-01',
        'september': '2019-09-01',
        'october': '2019-10-01',
        'november': '2019-11-01',
        'december': '2019-12-01'
    }

    max_ticket_price = 4000
    may_max_ticket_price = 8000

    for key in months.keys():
        root_logger.info('Starting to check flights in {}'.format(key))
        for country_code in country_codes:
            destination = country_code
            root_logger.info('Searching flights to {}'.format(country_names_dict[destination]))
            flights_raw = get_latest_prices_of_month(destination, months[key])
            flights_data = flights_raw['data']
            root_logger.info('Found {} flights to {}'.format(len(flights_data), country_names_dict[destination]))
            # для всех выходных
            weekend_flights = find_weekend_flights(flights_data, weekends, max_ticket_price)
            for flight in weekend_flights:
                flight_info = 'На выходные: Москва - {destination} за {price}р., {depart_date} ({depart_week_day})'\
                              '-{return_date} ({return_week_day})'.format(
                                        destination=flight['destination'],
                                        price=flight['value'],
                                        depart_date=flight['depart_date'],
                                        depart_week_day=flight['depart_week_day'],
                                        return_date=flight['return_date'],
                                        return_week_day=flight['return_week_day']
                                )
                root_logger.debug('Flight info to send to IFTTT: '.format(flight_info))
                post_ifttt_webhook('event', {'value1': flight_info})
                post_to_vk(flight_dict)

            # для майских
            may_weekend_flights = find_weekend_flights(flights_data, may_weekends, may_max_ticket_price)
            for flight in may_weekend_flights:
                flight_info = 'На майские: Москва - {destination} за {price}р., {depart_date} ({depart_week_day})'\
                              '-{return_date} ({return_week_day})'.format(
                                        destination=flight['destination'],
                                        price=flight['value'],
                                        depart_date=flight['depart_date'],
                                        depart_week_day=flight['depart_week_day'],
                                        return_date=flight['return_date'],
                                        return_week_day=flight['return_week_day']
                                )
                root_logger.debug('Flight info to send to IFTTT: '.format(flight_info))
                post_ifttt_webhook('event', {'value1': flight_info})
                post_to_vk(flight_dict)

    root_logger.debug('Func "main" has finished\n\n\n')


if __name__ == '__main__':
    main()
