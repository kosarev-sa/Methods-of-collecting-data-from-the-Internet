# Вариант 1
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем
# должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц
# сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через
# pandas. Сохраните в json либо csv.

from bs4 import BeautifulSoup as bs
import requests
import csv
import pandas as pd


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


def dataframe_vacancies_demo(position='Python', area='66', page=0):
    vacancies_df = pd.DataFrame(all_pages_vacancies(position, area, page))
    print(vacancies_df)


def csv_writing(position='Python', area='66', page=0):
    with open('vacancies.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, delimiter=',', fieldnames=[*all_pages_vacancies(position, area, page)[0].keys()])
        writer.writeheader()
        for row in all_pages_vacancies():
            writer.writerow(row)
    print("vacancies.csv is done")


dataframe_vacancies_demo()  # Можно задать аргументы: должность (или ключевое слово), регион, страница
csv_writing()               # Можно задать аргументы: должность (или ключевое слово), регион, страница


# Пример вывода:
#                                                   name  ...              site
# 0                     Python Developer (Middle/Senior)  ...  https://nn.hh.ru
# 1                              Middle Python Developer  ...  https://nn.hh.ru
# 2                                     Python developer  ...  https://nn.hh.ru
# 3                              Junior Python Developer  ...  https://nn.hh.ru
# 4    Middle/Senior Python разработчик проектов Data...  ...  https://nn.hh.ru
# ..                                                 ...  ...               ...
# 115               Аналитик (Digital, User Acquisition)  ...  https://nn.hh.ru
# 116                                Инженер-тестировщик  ...  https://nn.hh.ru
# 117                      Менеджер по подбору персонала  ...  https://nn.hh.ru
# 118        IPP SW Intern (Signal and Image processing)  ...  https://nn.hh.ru
# 119                  Junior Test Engineer (automation)  ...  https://nn.hh.ru
#
# [120 rows x 6 columns]
# vacancies.csv is done
