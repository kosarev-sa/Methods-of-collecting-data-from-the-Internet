import scrapy
from scrapy.http import HtmlResponse
from job_parser.items import JobParserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python'
                  '&geo%5Bt%5D%5B0%5D=4&geo%5Bt%5D%5B1%5D=14&geo%5Bo%5D%5B0%5D=22',
                  ]

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='f-test-search-result-item']"
                               "//div/span/a[@target='_blank']/@href").getall()
        vac_company = response.xpath("//div[@class ='f-test-search-result-item']"
                                     "//a[@ target='_self']/text()").getall()
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for i in range(len(links)):
            yield response.follow(links[i],
                                  callback=self.parse_vacancy,
                                  meta={'vac_company': vac_company[i]},
                                  )

    def parse_vacancy(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        vac_company = response.meta['vac_company']
        vac_location = response.xpath("//span[@class='_3NZry']/span/text()").get()
        vac_salary = response.xpath("//span[@class='_2eYAG -gENC _1TcZY dAWx1']/text()").getall()
        vac_url = response.url
        yield JobParserItem(name=vac_name,
                            company=vac_company,
                            location=vac_location,
                            salary=vac_salary,
                            url=vac_url,
                            )
