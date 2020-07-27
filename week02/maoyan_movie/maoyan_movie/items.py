# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 防止类型排序排到时间后面
    a_name = scrapy.Field()
    b_type = scrapy.Field()
    c_time = scrapy.Field()
