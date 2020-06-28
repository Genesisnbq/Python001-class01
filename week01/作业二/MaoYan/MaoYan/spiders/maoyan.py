# -*- coding: utf-8 -*-
import scrapy
from MaoYan.items import MaoyanItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        # print(response.text)
        # 获取电影列表
        tags = Selector(response=response).xpath(
            '//div[@class="movie-item film-channel"]')
        count = 0
        movie_list = []
        for i, tag in enumerate(tags):
            # 只取前10个电影
            if i > 9:
                break
            # 电影名称的class和别的hover信息不同，可以直接通过class定位
            movie_title = tag.xpath(
                './/span[contains(@class,"name")]/text()').extract_first()

            # 获取其它hover信息
            hover_texts = tag.xpath(
                './/span[@class="hover-tag"]/../text()').extract()

            movie_type = hover_texts[1].strip('\n').strip()
            release_time = hover_texts[5].strip('\n').strip()

            item = MaoyanItem()
            item['movie_title'] = movie_title
            item['movie_type'] = movie_type
            item['release_time'] = release_time

            yield item

