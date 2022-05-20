# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные
#    вакансии в созданную БД.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
#    (необходимо анализировать оба поля зарплаты).
# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
from pprint import pprint


def get_response_text(position='Python', area='66', page=0):
    url = 'https://nn.hh.ru'
    my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.159 Safari/537.36'}
    my_params = {'fromSearchLine': 'true',
                 'st': 'searchVacancy',
                 'text': position,
                 'from': 'suggest_post',
                 'area': area,
                 'page': page
                 }
    response = requests.get(url + '/search/vacancy/', params=my_params, headers=my_headers)
    if response.ok:
        return response.text
    else:
        print("Ответ от сервера не позволяет получить данные в требуемом виде. Проверьте параметры запроса.")


def one_page_vacancies(position='Python', area='66', page=0):
    soup = bs(get_response_text(position, area, page), 'html.parser')
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})
    vacancies_list = []
    for vacancy in vacancies:
        vacancy_data = {}
        info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        try:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            val = salary[salary.rfind(' ') + 1:]
            if salary[:2] == 'до':
                min_salary = None
                max_salary = int(salary[3:salary.rfind(' ')].replace(u'\u202f', ''))
            elif salary[:2] == 'от':
                min_salary = int(salary[3:salary.rfind(' ')].replace(u'\u202f', ''))
                max_salary = None
            else:
                min_salary = int(salary[:salary.find('-') - 1].replace(u'\u202f', ''))
                max_salary = int(salary[salary.find('-') + 4:salary.rfind(' ')].replace(u'\u202f', ''))
        except:
            min_salary = None
            max_salary = None
            val = None

        vacancy_data['name'] = info.text
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = max_salary
        vacancy_data['val'] = val
        vacancy_data['link'] = info['href']
        vacancy_data['site'] = info['href'][:info['href'].find('ru')+2]

        vacancies_list.append(vacancy_data)
    return vacancies_list, soup


def all_pages_vacancies(position='Python', area='66', page=0):
    all_pages_vacancies_list = []
    while True:
        all_pages_vacancies_list.extend(one_page_vacancies(position, area, page)[0])
        page += 1
        if one_page_vacancies(position, area, page)[1].find(text='дальше') is None:
            break
    return all_pages_vacancies_list


def vacancies_to_mongo(dbcollection_for_add):                  # функция, записывающаю собранные вакансии в созданную БД
    dbcollection_for_add.insert_many(all_pages_vacancies())
    return dbcollection_for_add


def update_and_addnew_vacancies(dbcollection_for_update_or_add):    # функция, которая добавляет в базу данных только
    for vacancy in all_pages_vacancies():                           # новые вакансии и обновляет старые
        dbcollection_for_update_or_add.update_one({'link': vacancy['link']}, {'$set': vacancy}, upsert=True)
    return dbcollection_for_update_or_add


# функция, которая производит поиск и выводит на экран ваканси с заработной платой больше введённой суммы:
def seek_salary(dbcollection_for_seek):
    currency = input("Введите валюту зарплаты('руб.' или 'USD' или '-', если показать вакансии с любой валютой): ")
    minimum = int(input("Введите минимальную желаемую зарплату: "))
    if currency == 'руб.' or currency == 'USD':
        for cur_vacancy in dbcollection_for_seek.find({'val': currency}):
            try:
                if cur_vacancy['min_salary'] > minimum or cur_vacancy['max_salary'] > minimum:
                    pprint(cur_vacancy)
            except:
                continue
    else:
        for vacancy in dbcollection_for_seek.find({'$or': [{'min_salary': {'$gt': minimum}}, {'max_salary': {'$gt': minimum}}]}):
            pprint(vacancy)


client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
hh_vacancies = db.hh_vacancies

# vacancies_to_mongo(hh_vacancies)
# for item in hh_vacancies.find({}):
#     pprint(item)

# update_and_addnew_vacancies(hh_vacancies)
# for item in hh_vacancies.find({}):
#     pprint(item)

# seek_salary(hh_vacancies)
