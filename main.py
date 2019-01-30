import requests
import json
import datetime
import time
from weekends import weekends, may_weekends, weekday_names
from countries import countries, country_codes, country_names_dict
from cities import cities

# TODO:
# 1. Очистить функцию find_weekend_flight - она должна только находить и возвращать какой-то список
# 2. Сделать функцию для печати результата поиска
# 3. ГОТОВО - Сделать функцию для отправки результатов поиска куда-либо (например, в паблик в вк)


def post_to_vk(flight_dict):
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

    print(response)


# function, which gets cheapest flights for last 48 hours (https://support.travelpayouts.com/hc/ru/articles/203956163#02)
def get_latest_prices_of_month(destination, beginning_of_period):
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
    return response.json()	


def find_weekend_flights(flights_data):
    for flight in flights_data:
        found_at = flight['found_at']

        try:
            found_at_datetime = datetime.datetime.strptime(found_at, '%Y-%m-%dT%H:%M:%S')
        except:
            found_at_datetime = datetime.datetime.strptime(found_at, '%Y-%m-%dT%H:%M:%S.%f')
        
        time_now = datetime.datetime.now()
        time_difference = time_now - found_at_datetime
        time_difference_in_hours = time_difference / datetime.timedelta(hours=1)
        
        max_value = 8000

        if time_difference_in_hours <= 1 and flight['value'] <= max_value:
            for date in weekends:
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

                    print('{origin} - {destination} '\
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
                    print(link)
                    print('Found at {}'.format(flight['found_at']))
                    print()

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


def main():
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

    for key in months.keys():
        print(key)
        for country_code in country_codes:
            destination = country_code
            # print(country_names_dict[destination])
            # print('.', end='')
            flights_raw = get_latest_prices_of_month(destination, months[key])
            flights_data = flights_raw['data']
            # print(len(flights_data))
            find_weekend_flights(flights_data)
            # time.sleep(0.1)
        print()


if __name__ == '__main__':
    main()

    # mix_weekends()
    # print(weekends)
    # test()

def time_str_to_datetime():
    found_at = '2019-01-30T09:30:10'
    found_at_datetime = datetime.datetime.strptime(found_at, '%Y-%m-%dT%H:%M:%S')
    
    time_now = datetime.datetime.now()
    time_difference = time_now - found_at_datetime
    time_difference_in_hours = time_difference / datetime.timedelta(hours=1)

    print(type(found_at_datetime))
    print(found_at_datetime)
    print(time_now)
    print(type(time_difference_in_hours))
    print(time_difference_in_hours)


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def weekends():
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date(2019, 12, 31)
    for single_date in daterange(start_date, end_date):
        if single_date.isoweekday() in [1, 5, 6, 7]:
            print(single_date.strftime("%Y-%m-%d"))
        if single_date.isoweekday() in [1, 4]:
            print()
        '''
        if single_date.isoweekday() == (1 or 5 or 6 or 7):
            single_weekend_options.append(single_date.strftime("%Y-%m-%d"))
        else: 
            if single_weekend_options:
                weekends.append(single_weekend_options)
        '''

