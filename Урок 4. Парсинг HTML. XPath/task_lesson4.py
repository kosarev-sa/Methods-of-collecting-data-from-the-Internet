# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные данные в БД

from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint


def get_dom():
    url = 'https://lenta.ru'
    my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.159 Safari/537.36'}
    response = requests.get(url, headers=my_headers)
    if response.ok:
        dom = html.fromstring(response.text)
        return dom
    else:
        print("Ответ от сервера не позволяет получить данные в требуемом виде. Проверьте параметры запроса.")


def get_news():
    lenta_news = []
    items = get_dom().xpath("//section[@class = 'row b-top7-for-main js-top-seven']/*/div[@class = 'first-item' or @class = 'item']")
    for item in items:
        news = {}
        news['name'] = item.xpath(".//a[contains (@href, '/news')]/text()")
        news['name'] = f"{news['name'][0]}".replace(u"\xa0", " ")           # ликвидируем 'неразрывные пробелы' unicode
        href = item.xpath(".//a/@href")[0]
        if href[0]=='/':                                                    # ссылки на lenta.ru на сайте относительные,
            news['link'] = f'https://lenta.ru{href}'
        else:                                                               # на другие сайты - абсолютные
            news['link'] = href
        news['from'] = news['link'][8:news['link'].find('.')+4]
        news['date'] = f'{item.xpath(".//time/@title")}'.replace("['", "").replace("']", "")
        news['time'] = '{}'.format(item.xpath(".//time[@class='g-time']/text()")).replace("['", "").replace("']", "")

        lenta_news.append(news)
    return lenta_news


def news_to_mongo(dbcollection_for_add):                  # функция, записывающаю собранные новости в созданную БД
    dbcollection_for_add.insert_many(get_news())
    return dbcollection_for_add


def update_and_add_news(dbcollection_for_update_or_add):     # функция, которая добавляет в базу данных только
    for news in get_news():                                  # свежие новости и обновляет старые
        dbcollection_for_update_or_add.update_one({'link': news['link']}, {'$set': news}, upsert=True)
    return dbcollection_for_update_or_add


client = MongoClient('127.0.0.1', 27017)
db = client['news']
lenta_ru = db.lenta_ru

# news_to_mongo(lenta_ru)
# for item in lenta_ru.find({}):
#     pprint(item)
#
# update_and_add_news(lenta_ru)
# for item in lenta_ru.find({}):
#     pprint(item)


# Вариант собранной БД:

# {'_id': ObjectId('61a699537837114234e8ed52'),
#  'date': '30 ноября 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/11/30/chngs/',
#  'name': 'Россиян предупредили об изменениях в законах с 1 декабря',
#  'time': '23:00'}
# {'_id': ObjectId('61a699537837114234e8ed53'),
#  'date': ' 1 декабря 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/12/01/iosifov/',
#  'name': '20-летний российский футболист забил в дебютном матче в Кубке '
#          'Испании',
#  'time': '00:33'}
# {'_id': ObjectId('61a699537837114234e8ed54'),
#  'date': ' 1 декабря 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/12/01/gen/',
#  'name': 'Американские биологи нашли предрасположенность к суициду в генах',
#  'time': '00:32'}
# {'_id': ObjectId('61a699537837114234e8ed55'),
#  'date': ' 1 декабря 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/12/01/tu160/',
#  'name': 'В Польше заявили об отставании российских бомбардировщиков от '
#          'американских',
#  'time': '00:30'}
# {'_id': ObjectId('61a699537837114234e8ed56'),
#  'date': ' 1 декабря 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/12/01/decemberopen/',
#  'name': 'Россия возобновила авиасообщение с несколькими странами',
#  'time': '00:25'}
# {'_id': ObjectId('61a699537837114234e8ed57'),
#  'date': ' 1 декабря 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/12/01/omicronimmunity/',
#  'name': 'Биолог объяснила главную опасность омикрон-штамма',
#  'time': '00:20'}
# {'_id': ObjectId('61a699537837114234e8ed58'),
#  'date': ' 1 декабря 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/12/01/altshteyn_omikron/',
#  'name': 'Профессор оценил способность омикрон-штамма вызывать тяжелые '
#          'заболевания',
#  'time': '00:18'}
# {'_id': ObjectId('61a699537837114234e8ed59'),
#  'date': ' 1 декабря 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/11/30/internet/',
#  'name': 'В России заработал бесплатный «социальный интернет»',
#  'time': '00:15'}
# {'_id': ObjectId('61a699537837114234e8ed5a'),
#  'date': ' 1 декабря 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/12/01/omicron_soon/',
#  'name': 'Минздрав предсказал скорое появление омикрон-штамма в России',
#  'time': '00:04'}
# {'_id': ObjectId('61a699537837114234e8ed5b'),
#  'date': '30 ноября 2021',
#  'from': 'lenta.ru/',
#  'link': 'https://lenta.ru/news/2021/11/30/death/',
#  'name': 'Названа приводящая к мгновенной смерти болезнь',
#  'time': '23:26'}
