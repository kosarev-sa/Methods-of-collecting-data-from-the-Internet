import scrapy
from scrapy.http import HtmlResponse
from job_parser.items import JobParserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://nn.hh.ru/search/vacancy?area=1679&search_field=name'
                  '&search_field=company_name&search_field=description&text=Python'
                  '&clusters=true&ored_clusters=true&enable_snippets=true',
                  ]

    def parse(self, response: HtmlResponse):
        links = response.xpath(
            "//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        # print(response.url)
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in links:
            yield response.follow(link, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        vac_company = response.xpath("//a[@data-qa='vacancy-company-name']/span/text()").getall()
        vac_location = response.xpath("//a[@data-qa='vacancy-view-link-location']//span/text()"
                                      ).getall()
        if vac_location == []:
            vac_location = response.xpath("//p[@data-qa='vacancy-view-location']/text()").getall()
        vac_salary = response.xpath(
            "//div[@data-qa='vacancy-salary']/span/text()").getall()
        vac_url = response.url
        yield JobParserItem(name=vac_name, company=vac_company, location=vac_location,
                            salary=vac_salary, url=vac_url)
