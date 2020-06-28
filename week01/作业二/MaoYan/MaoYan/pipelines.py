# -*- coding: utf-8 -*-
import pandas as pd


class MaoyanPipeline(object):

    def open_spider(self, spider):
        self.movie_dic = {
            '电影名': [],
            '类型': [],
            '上映时间': []
        }


    def process_item(self, item, spider):
        self.movie_dic['电影名'].append(item['movie_title'])
        self.movie_dic['类型'].append(item['movie_type'])
        self.movie_dic['上映时间'].append(item['release_time'])
        # print(self.movie_dic)


    def close_spider(self,spider):
        print(self.movie_dic)
        movies = pd.DataFrame(self.movie_dic)
        movies.to_csv('../movies.csv', encoding='utf-8-sig')
        print('finished!')