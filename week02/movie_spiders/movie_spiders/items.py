# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieSpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    db_movie_link = scrapy.Field()
    db_movie_name = scrapy.Field()
    db_movie_detail = scrapy.Field()
    my_movie_name = scrapy.Field()
    my_movie_type = scrapy.Field()
    my_movie_release_tm = scrapy.Field()
