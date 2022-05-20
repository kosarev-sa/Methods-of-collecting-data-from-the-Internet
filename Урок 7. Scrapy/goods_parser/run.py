from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from goods_parser.spiders.castoramaru import CastoramaruSpider
from goods_parser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # query = input('')
    process.crawl(CastoramaruSpider, query='линолеум')
    process.start()
