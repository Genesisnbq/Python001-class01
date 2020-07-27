import scrapy
from scrapy.selector import Selector
from maoyan_movie.items import MaoyanMovieItem
from traceback import format_exc


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    # 其实URL列表
    start_urls = ['https://maoyan.com/films?showType=3']

    # 解析函数
    def parse(self, response):
        # 打印网页的url
        print(response.url)

        # 用于计数-爬取10个电影数据
        i = 0

        # 电影列表
        movie_list = []

        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')

        for movie in movies:
            i += 1
            if i == 11:
                break
            # 路径使用/ . .. 不同的含义
            title = movie.xpath('./a/text()')
            link = 'https://maoyan.com' + movie.xpath('./a/@href').extract_first()

            print('--------------')

            print(title.extract())

            print(link)

            # 增加异常处理
            try:
                yield scrapy.Request(url=link, callback=self.parse2)
            except Exception as e:
                print(format_exc())

    # 解析具体界面
    def parse2(self,response):
        movies = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        item = MaoyanMovieItem()

        # 初始化电影类型type字符串, 以便后续添加
        string = ''
        item['a_name'] = movies.xpath('./h1/text()').extract_first()
        item['c_time'] = movies.xpath('.//li[3]/text()').extract_first()[:10]

        for x in movies.xpath('.//a/text()').extract():
            string += x

        item['b_type'] = string.strip()

        yield item
