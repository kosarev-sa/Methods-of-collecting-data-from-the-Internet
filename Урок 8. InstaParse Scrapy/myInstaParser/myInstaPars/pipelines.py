import scrapy
from itemadapter import ItemAdapter
from scrapy.utils.python import to_bytes
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class MyinstaparsPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.instagram06_2022

    def process_item(self, item, spider):
        collection = self.mongobase[f"{spider.name}_{item.get('username')}"]
        collection.insert_one(item)
        return item


class InstFollowersPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        try:
            print(item['photo'])
            yield scrapy.Request(item['photo'])
        except Exception as e:
            print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        print()
        return item

    def file_path(self, request, item, response=None, info=None):
        name = item['username'].replace('/', '-')
        return f'{name}/{item["user_id"]}.jpg'
