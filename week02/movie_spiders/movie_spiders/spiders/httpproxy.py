# -*- coding: utf-8 -*-
import scrapy


class HttpproxySpider(scrapy.Spider):
    name = 'httpproxy'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        print(response.text)
