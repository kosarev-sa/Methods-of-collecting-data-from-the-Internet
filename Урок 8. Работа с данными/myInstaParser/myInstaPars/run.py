from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import settings
from myInstaPars.spiders.instsgram import InstagramSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider)

    process.start()
