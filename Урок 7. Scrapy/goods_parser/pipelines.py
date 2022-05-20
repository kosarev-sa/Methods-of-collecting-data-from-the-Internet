# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class GoodsParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.goods05_2022

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


class GoodsImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for img in item['images']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['images'] = [itm[1] for itm in results if itm[0]]
        return item

    # def file_path(self, request, response=None, info=None, *, item=None):      # Метод для изменения места скачивания файлов
    #     image_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
    #     image_perspective = request.url.split('/')[-2]
    #     image_filename = f'{image_url_hash}_{image_perspective}.jpg'
    #     return image_filename
