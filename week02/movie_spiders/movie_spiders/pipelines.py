# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import pymysql
from traceback import format_exc
from itemadapter import ItemAdapter


class MovieSpidersPipeline:

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)

    def __init__(self, host, user, password, db, table, port=3306):
        self.db = db
        self.table = table
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('DB_HOST'),
            user=crawler.settings.get('DB_USER'),
            password=crawler.settings.get('DB_PWD'),
            db=crawler.settings.get('DB'),
            table=crawler.settings.get('TABLE')
        )

    def process_item(self, item, spider):
        if spider.name == 'douban':
            content = f"|{item['db_movie_name']}|\t|{item['db_movie_link']}|\t|{item['db_movie_detail']}|\n\n"
            with open('/Users/xiaoyu.gao/PycharmProjects/Python001-class01/week01/db_movie.txt', 'a', encoding='utf8') \
                    as f:
                f.write(content)
        elif spider.name == 'maoyan':
            item_dict = ItemAdapter(item).asdict()
            # sql_engine.connect(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PWD, db=config.DB)
            sql = 'INSERT INTO {table} (`{fields}`) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE {update}'.format(
                table=self.table,
                fields='`,`'.join(item_dict.keys()),
                update=','.join(['`{field}`=VALUES(`{field}`)'.format(field=field) for field in item_dict.keys()])
            )
            cur = self.conn.cursor()
            try:
                cur.execute(sql, item_dict.values())
            except:
                self.conn.rollback()
                print('save to db failed except:%s', format_exc())
            finally:
                cur.close()
        return item

    def close_spider(self, spider):
        self.conn.close()
