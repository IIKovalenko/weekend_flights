'''
import requests

token = 'afcac628afcac628afcac628e6afa29bb0aafcaafcac628f39bb045f37cab26196e8281'
url = ''

payload = {
	'chat_id': 'learnmlcheatway',
	'text': 'Some text'
}

result = requests.get(url, params=payload)

print(result)


# ----------------------------------------

мои ключи:

application_id = 6839704
group_id = 177516719
owner_id_group = -177516719

# --------------------------------------

'''
# -*- coding: utf-8 -*-
import requests
import json

# сервисный ключ
service_token = 'afcac628afcac628afcac628e6afa29bb0aafcaafcac628f39bb045f37cab26196e8281'

# ключ, полученный по спец ссылке
token = 'c5feed7bce2122333cd50320cf80831e2b0a23a7b50c0cec5da901981f272a9155c3d7912def3d42705bb'
application_id = 6839704
group_id = 177516719
owner_id_group = -177516719
foo = 'some text'

# из ответа на тостере, как правильно делать:
response = requests.post('https://api.vk.com/method/wall.post', data={'access_token': token,
                                                                    'owner_id': owner_id_group,
                                                                    'from_group': 1,
                                                                    'message': foo,
                                                                    'signed': 0,
                                                                   'v':"5.52"}).json()

print(response)


'''
Сработало. 
в адресной строке браузера ввел типа такого и получил заветный токен доступа.

запрос:
https://oauth.vk.com/authorize?client_id=6839704&scope=wall,offline&redirect_uri=https://oauth.vk.com/blank.html&response_type=token

ответ:
https://oauth.vk.com/blank.html#access_token=c5feed7bce2122333cd50320cf80831e2b0a23a7b50c0cec5da901981f272a9155c3d7912def3d42705bb&expires_in=0&user_id=5286231


'''


'''
url = 'https://api.vk.com/method/wall.post'

requests.post('https://api.vk.com/method/wall.post', params={'access_token': token,
                                                                    'owner_id': owner_id_group,
                                                                    'from_group': 1,
                                                                    'message': foo,
                                                                    'signed': 0,
                                                                   'v':"5.52"}).json() #ругается ошибкой JSONDecodeError
                                   # или прочими. работает только с ангийским текстом
'''
