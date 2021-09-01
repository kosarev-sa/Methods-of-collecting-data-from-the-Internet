# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
#    Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
#    Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
# Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.

import requests
import json

token = input('Введите Ваш access_token: ')
my_id = input('Введите Ваш id: ')
my_params = {'user_id': my_id,
             'access_token': token,
             'v': '5.52'}
my_headers = {'User-Agent':
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

response = requests.get('https://api.vk.com/method/groups.get', params=my_params, headers=my_headers)

groups_lst = []
if response.ok:
    j_data = response.json()
    groups = j_data['response']['items']
    for dct in groups:
        groups_lst.append(dct['name'])
    print(f'Список групп пользователя: {groups_lst}')

with open('users_groups.json', 'w', encoding='utf-8') as f:
    json.dump(groups_lst, f)
