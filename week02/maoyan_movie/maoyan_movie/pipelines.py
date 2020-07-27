# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import pymysql
from traceback import format_exc

dbInfo = {
    'host': 'localhost',
    'port': 3306,  # 特别注意, 这是数字, 不是str
    'user': 'root',
    'password': 'root',
    'db': 'python_geek'
}

sqls = 'insert into maoyan_movie(name,type,time) values(%s,%s,%s)'


class ConnDB(object):
    def __init__(self, dbInfo, sqls):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.sqls = sqls

    def run(self, data):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db
        )
        # 游标建立的时候就开启了一个隐形的事物
        cur = conn.cursor()

        # 异常处理
        try:
            cur.execute(self.sqls, data)
            # 关闭游标
            conn.commit()
        except:
            conn.rollback()
            print(format_exc())
        finally:
            # 关闭与数据库的连接
            conn.close()


class MaoyanMoviePipeline:
    def process_item(self, item, spider):

        # 把 dict转换成dataframe, 要先转换成list
        # movie = [item]
        # movie1 = pd.DataFrame(data=[item])
        # mode = 'a' 是代表追加数据, 不覆盖
        # movie1.to_csv('./maoyan_movie.csv',encoding='utf8',index=False,header=False,mode='a')

        db = ConnDB(dbInfo, sqls)
        data = (item['a_name'], item['b_type'], item['c_time'])

        # 插入数据库 - 异常处理
        try:
            db.run(data)
        except Exception as e:
            print(format_exc())
        return item
