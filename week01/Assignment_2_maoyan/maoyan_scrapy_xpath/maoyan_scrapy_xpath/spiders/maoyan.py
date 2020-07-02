import scrapy
from maoyan_scrapy_xpath.items import MaoyanScrapyXpathItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        count = 0
        for movie in movies:
            if count > 9:
                break
            # title = movie.xpath('.//span[@class="name"]/text()').extract()
            # print(title)
            title = movie.xpath('.//span[contains(@class,"name")]/text()').extract()[0]
            hover_texts = movie.xpath('.//span[@class="hover-tag"]/../text()').extract()
            # print(hover_texts)
            movie_type = hover_texts[1].strip('\n').strip()
            release_time = hover_texts[5].strip('\n').strip()
            # 打印到屏幕
            print(title)
            print(release_time)
            print(movie_type)
            item = MaoyanScrapyXpathItem()
            item['title'] = title
            item['movie_type'] = movie_type
            item['release_time'] = release_time
            count += 1
            yield item
