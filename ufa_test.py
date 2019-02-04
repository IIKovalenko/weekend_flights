import requests

TOKEN = 'a4da858f9d18ab2292ecbb4dddec4485'
url='http://api.travelpayouts.com/v2/prices/latest'

payload = {
    'token': TOKEN, 
    'origin': 'MOW',
    'destination': 'UFA',
    'beginning_of_period': '2019-02-01',
    'period_type': 'month',  
    'limit': 1000
}

response = requests.get(url, params=payload)
flights_raw = response.json()
flights_data = flights_raw['data']

print(flights_data)