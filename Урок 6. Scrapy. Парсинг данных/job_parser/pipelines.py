# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient


class JobParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy05_2022

    def process_item(self, item, spider):
        # # dict_item = dict(item)
        if spider.name == 'hhru':
            item['company'] = ' '.join(item['company']).replace(u'\xa0', u'').strip()
            item['location'] = ''.join(item['location']).replace(u'\xa0', u'').strip()
            item['salary_min'], item['salary_max'], item['currency'], item['salary'] = \
                self.process_salary_hh(item['salary'])
        if spider.name == 'sjru':
            item['salary_min'], item['salary_max'], item['currency'], item['salary'] = \
                self.process_salary_sj(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        '''Обработка зарплаты у hhru вакансии'''
        min = ''
        max = ''
        cur = ''
        str_salary = ''.join(salary).replace(u'\xa0', u'').strip()
        for index, value in enumerate(salary):
            value = value.replace(u'\xa0', u'').strip()
            if value == 'от':
                min = salary[index+1].replace(u'\xa0', u'').strip()
            if value == 'до':
                max = salary[index+1].replace(u'\xa0', u'').strip()
        if len(salary) >= 2:
            cur = salary[-2].replace(u'\xa0', u'').strip()
        return min, max, cur, str_salary

    def process_salary_sj(self, salary):
        '''Обработка зарплаты у sjru вакансии'''
        min = ''
        max = ''
        cur = ''
        str_salary = ' '.join(salary).replace(u'\xa0', u' ').strip()
        if salary[0][0].isdigit() is True and salary[1][0].isdigit() is True:
            min = salary[0].replace(u'\xa0', u'').strip()
            max = salary[1].replace(u'\xa0', u'').strip()
        elif salary[0][0].isdigit() is True and salary[1][0].isdigit() is False:
            min = salary[0].replace(u'\xa0', u'').strip()
        else:
            for index, value in enumerate(salary):
                value = value.replace(u'\xa0', u' ').strip()
                if value == 'от':
                    for i in salary[index+2].replace(u'\xa0', u' '):
                        if i.isdigit() is True:
                            min += i
                if value == 'до':
                    for i in salary[index + 2].replace(u'\xa0', u' '):
                        if i.isdigit() is True:
                            max += i
        if len(salary) > 1:
            for i in salary[-1].replace(u'\xa0', u'').strip():
                if i.isdigit() is False:
                    cur += i
        return min, max, cur, str_salary
