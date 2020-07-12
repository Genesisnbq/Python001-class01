# -*- coding: utf-8 -*-

import scrapy
from traceback import format_exc
from scrapy.selector import Selector

from movie_spiders.items import MovieSpidersItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        try:
            movies = Selector(response).xpath('//div[@class="movie-hover-info"]')
            for movie in movies[0:10]:
                item = MovieSpidersItem()
                item['my_movie_name'] = movie.xpath('./div[1]/@title').extract_first().strip()
                item['my_movie_type'] =movie.xpath('./div[2]/text()').extract()[1].strip()
                item['my_movie_release_tm'] = movie.xpath('./div[4]/text()').extract()[1].strip()
                yield item
        except:
            print(format_exc())
