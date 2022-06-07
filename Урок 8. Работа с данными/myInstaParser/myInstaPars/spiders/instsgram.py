import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from copy import deepcopy
from myInstaPars.items import MyinstaparsItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    insta_login = 'supersirius_sa'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1654609031:AbJQAFmss930L6Usl6UVpNtTHFhY4HWImNTVX4DRQD+cu3s9jFd8MCSScVOBSkfd08OMs1TxsYgDlZ0jX4FXifonXGZtok2TO2b78PLa925pQe+AKop8rJPBajIVTj9CeVZPMEYCWEbE+w=='
    # insta_login = 'Onliskill_udm'
    # insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1629825416:ASpQAMvl1EAdo0NdRZNcM1/' \
    #              'pjlU9rRg4n4cjCM00SDGSV5pDN6XbC93ZbYN67HUOHkXZnGGe2gIWPU2qtQY0HAkIjR5U5syu+' \
    #              'lv8qtqeI7cyy2ua6WmBV6AngVo1apn3eJ6O3UAFVgb+q5HtHsQ='
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    # user_parse = 'ai_machine_learning'
    # posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'
    # graphql_url = 'https://www.instagram.com/graphql/query/?'


    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf}
                                 )

    def user_login(self, response: HtmlResponse):
        print()


    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')
