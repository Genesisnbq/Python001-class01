# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class MaoyanScrapyXpathPipeline:
    # def process_item(self, item, spider):
    #     return item
    def open_spider(self, spider):
        self.movie_dic = {
            '电影名': [],
            '类型': [],
            '上映时间': []
        }

    def process_item(self, item, spider):
        movie_title = item['title']
        movie_type = item['movie_type']
        release_time = item['release_time']
        self.movie_dic['电影名'].append(movie_title)
        self.movie_dic['类型'].append(movie_type)
        self.movie_dic['上映时间'].append(release_time)
        # print(self.movie_dic)
        # return item

    def close_spider(self, spider):
        print(self.movie_dic)
        movies = pd.DataFrame(self.movie_dic)
        movies.to_csv('../movies.csv', encoding='utf_8_sig')
        print('完成!')
