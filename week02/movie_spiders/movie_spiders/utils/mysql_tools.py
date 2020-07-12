# -*- coding:utf8 -*-

import pymysql
from traceback import format_exc


class MysqlEngine(object):

    def connect(self, **kwargs):
        self.conn = pymysql.connect(
            host=kwargs.get('host', 'localhost'),
            port=kwargs.get('port', 3306),
            user=kwargs.get('user', 'root'),
            password=kwargs.get('password', ''),
            db=kwargs.get('db', ''),
        )

    def _execute(self, sql_query, values):
        cur = self.conn.cursor()
        try:
            cur.execute(sql_query, values)
            cur.close()
            self.conn.commit()
        except:
            print(format_exc())
            self.conn.rollback()
        self.conn.close()

    def execute(self, sql_query, values):
        return self._execute(sql_query, values)



sql_engine = MysqlEngine()
