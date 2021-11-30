# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
#    сохранить JSON-вывод в файле *.json.

import requests
import json

my_headers = {'User-Agent':
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
username = input('Введите имя пользователя (login): ')
if username == '':
    username = 'kosarev-sa'

response = requests.get(f'https://api.github.com/users/{username}/repos', headers=my_headers)

repo_lst = []
if response.ok:
    j_data = response.json()
    for dct in j_data:
        repo_lst.append(dct['name'])
    print(f'Список репозиториев пользователя {username}: {repo_lst}')

# >> Введите имя пользователя (login):
# >> Список репозиториев пользователя kosarev-sa: ['-algorithms_2021', 'JS', 'Python-lessons']

with open('users_repositories.json', 'w', encoding='utf-8') as f:
    json.dump(repo_lst, f)
