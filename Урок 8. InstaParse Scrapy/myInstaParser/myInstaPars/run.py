from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from myInstaPars.spiders.instagram import InstsgramSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(InstsgramSpider)

    reactor.run()


# from myInstaPars import settings
#
# if __name__ == '__main__':
#     crawler_settings = Settings()
#     crawler_settings.setmodule(settings)
#
#     process = CrawlerProcess(settings=crawler_settings)
#     process.crawl(InstsgramSpider)
#     process.start()
