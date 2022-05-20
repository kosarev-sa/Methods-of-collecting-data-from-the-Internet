import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from goods_parser.items import GoodsParserItem


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']
    page = 2

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={query}']

    def parse(self, response: HtmlResponse):
        '''Получаем ссылки на объекты и ссылку на след. страницу'''
        goods_links = response.xpath("//a[@class='product-card__name ga-product-card-name']")
        next_page = response.xpath(f"//div[@class='pages']//a[contains(@href,"
                                   f"'p={self.page}')]/@href").get()
        self.page += 1
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in goods_links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=GoodsParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")                               # Наполняем item данными (также сразу запускаются предобработчики)
        loader.add_xpath('price', "//span[@class='price-per-unit']/span/span/text()")
        loader.add_xpath('parameters', "//div[@id='specifications']//text()")
        loader.add_xpath('images', "//span[@itemprop='image']/@content")
        loader.add_value('url', response.url)
        yield loader.load_item()
        # Отправляем в пайплайн (также здесь запускаются постобработчики)

# Вывод Mongo:

# _id
# 628663539a8b96affd2867e0
#
# name
# "Линолеум бытовой Juteks Life Flame Oak 2, дерево (плашки), 2,5 м"
#
# price
# "420"
#
# parameters
# Object
# Тип продукта
# "Линолеум"
# Артикул производителя
# "554147686"
# Вид линолеума
# "бытовой"
# Класс износостойкости
# "22"
# Толщина защитного слоя, мм
# "0.2"
# Общая толщина, мм
# "2.5"
# Декор
# "дерево (плашки)"
# Тип основы
# "вспененная"
# Ширина рулона, м
# "2,5 м"
# Намотка стандартного рулона, м
# "92"
# Вес 1 м2, кг
# "1.5"
# Противоскольжение
# "да"
# Совместимость с теплым полом
# "да"
# Класс пожарной опасности
# "КМ5"
# Оценка по сертификату качества
# "А+"
# Срок службы
# "15 лет"
# Назначение
# "для гостиной; для детской; для кухни; для прихожей; для спальни"
# Бренд
# "Juteks"
# Страна-производитель
# "Россия"
# Цветовая гамма
# "бежевый"
# Коллекция
# "Life"
#
# images
# Array
# Object
# url
# "https://www.castorama.ru/media/catalog/product/cache/image/1800x/040ec…"
# path
# "full/3f6edcae3fbc242c7a70eedc6bb31e3d13d61f2b.jpg"
# checksum
# "d3d8d1613a2e75e747136dbb18dbd4a0"
# status
# "downloaded"
#
# url
# Array
# "https://www.castorama.ru/linoleum-bytovoj-juteks-life-flame-oak-2-dere…"
