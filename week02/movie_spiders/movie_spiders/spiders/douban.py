# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector

from movie_spiders.items import MovieSpidersItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    def start_requests(self):
        for i in range(0, 1):
            url = f'https://movie.douban.com/top250?start={i*25}'
            yield scrapy.Request(url, callback=self.parse_first_page)

    def parse_first_page(self, response):
        # item = MovieSpidersItem()
        content_list = Selector(response).xpath('//div[@class="hd"]')
        for movie in content_list:
            item = MovieSpidersItem()
            # item['movie_name'] = movie.xpath('./a/span[1]/text()').strip()
            item['db_movie_name'] = movie.xpath('./a/span/text()').extract_first()
            item['db_movie_link'] = movie.xpath('./a/@href').extract_first()
            yield scrapy.Request(item['db_movie_link'], meta={'item': item}, callback=self.parse_second_page)

    def parse_second_page(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'lxml')
        # item['db_movie_detail'] = Selector(response).xpath('//div[@class="related-info"]/text()').extract_first().strip()
        item['db_movie_detail'] = soup.find('div', attrs={'class': 'related-info'}).get_text().replace('\n', '').replace(' ', '')
        yield item
