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

        if time_difference_in_hours <= 1 and flight['value'] <= max_value:
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

                    post_to_vk(flight_dict)
        break

    root_logger.debug('Func "find_weekend_flights" has finished')

def main():
    root_logger.debug('Func "main" has started')
    months = {
        'february': '2019-02-01',
        # 'march': '2019-03-01',
        # 'april': '2019-04-01',
        # 'may': '2019-05-01',
        # 'june': '2019-06-01',
        # 'july': '2019-07-01',
        # 'august': '2019-08-01',
        # 'september': '2019-09-01',
        # 'october': '2019-10-01',
        # 'november': '2019-11-01',
        # 'december': '2019-12-01'
    }

    max_ticket_price = 8000

    for key in months.keys():
        root_logger.info('Starting to check flights in {}'.format(key))
        for country_code in country_codes:
            destination = country_code
            root_logger.info('Searching flights to {}'.format(country_names_dict[destination]))
            flights_raw = get_latest_prices_of_month(destination, months[key])
            flights_data = flights_raw['data']
            root_logger.info('Found {} flights to {}'.format(len(flights_data), country_names_dict[destination]))
            find_weekend_flights(flights_data, weekends, max_ticket_price)
            # здесь должно быть примерно так: 
            # weekend_flights = find_weekends_flights(flights_data, weekends)            
            # root_logger.debug('Found {} weekend flights'.format(len(weekend_flights)))

    root_logger.debug('Func "main" has finished\n\n\n')

if __name__ == '__main__':
    main()
