# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join


def process_parameters(value):
    parameters_dct = {}
    parameters_lst = []
    for i in value:
        i = i.strip()
        if i != '' and i[-1] != '.':
            parameters_lst.append(i)
    for i in parameters_lst[1:]:
        if parameters_lst.index(i) % 2 != 0:
            parameters_dct[i] = parameters_lst[parameters_lst.index(i) + 1]
    return parameters_dct


class GoodsParserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    parameters = scrapy.Field(input_processor=process_parameters, output_processor=TakeFirst())
    images = scrapy.Field()
    url = scrapy.Field()
