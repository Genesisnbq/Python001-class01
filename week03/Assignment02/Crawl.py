import time
import math
import threading
from queue import Queue, Empty
from random import choice, randint

import pymysql
import requests
from fake_useragent import UserAgent

lock = threading.Lock()
print_lock = threading.Lock()


class JobSpider(object):
    def __init__(self, keyword, position_num, city, thread_num):
        self.keyword = keyword
        self.city = city
        self.city_code = self.transform_city_code(self.city)
        self.thread_num = thread_num
        self.position_num = position_num
        self.page_num = self.get_page_num()
        self.scraped_total_job = 0

        self.request_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default' \
                           '&city={}&needAddtionalResult=false'.format(self.city)

        self.post_url_queue = Queue()
        self.page_queue = Queue()

        ua = UserAgent()
        self.user_agent = str(ua.random)

        self.header = {
            'Host': 'www.lagou.com',
            'Connection': 'keep-alive',
            'Origin': 'https://www.lagou.com',
            'User-Agent': self.user_agent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'https://www.lagou.com/jobs/list_Python/p-city_{self.city_code}',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-anit-forge-code': '0',
            'x-anit-forge-token': None
        }

        self.cookie = self.get_cookie()
        self.header = self.generate_new_header()

        self.connect_mysql()

    def get_page_num(self):
        """
        Calculate the number of pages based on the user-defined number of job positions.
        Every webpage contains 15 positions
        """
        # 每页15个职位,向上取整
        res = math.ceil(self.position_num / 15)
        # 拉勾网最多显示30页结果
        res = res if res < 30 else 30
        return res

    def transform_city_code(self, city):
        city_dict = {
            '北京': 2,
            '上海': 3,
            '广州': 213,
            '深圳': 215
        }
        city_code = city_dict[city]
        return city_code

    def get_cookie(self):
        print('\nFetching a cookie for the web scraping...\n')

        url = 'https://www.lagou.com/jobs/list_{}?px=default&city={}'
        response = requests.get(
            url.format(self.keyword, self.city),
            headers=self.header
        )

        # 获取的cookie是字典类型的
        cookies = response.cookies.get_dict()
        print('cookies', cookies)

        # 因为请求头中cookie需要字符串,将字典转化为字符串类型
        COOKIE = ''
        for key, val in cookies.items():
            COOKIE += (key + '=' + val + '; ')

        print('\nSuccessfully fetched the cookie.\n')
        return COOKIE

    def generate_new_header(self):
        """
        If there the response status is not 200, then try to:
        (1) get new cookie
        (2) change IP address
        (3) change user-agent
        """
        self.header.update({'Cookie': self.cookie})
        return self.header

    def get_page(self, current_page_num):
        """
        The variable 'current_page_num' is from the post_url_queue.
        Because the url is always the same, the only difference is the 'pn' value
        in the self.post_data
        """
        self.get_page_success = False

        self.post_data = {
            'first': 'false',
            'pn': str(current_page_num),
            'kd': self.keyword,
            'sid': '145ea2fc04e4480a9ea3bbf20a2ea6b9'
        }

        self.change_web_scraping_info()

        time.sleep(randint(1, 10))

        response = requests.post(self.request_url,
                                 headers=self.header,
                                 data=self.post_data,
                                 # verify=False,
                                 timeout=10)

        if response.status_code == 200:

            # 得到包含职位信息的字典
            page = response.json()
            self.page_queue.put(page)
            self.get_page_success = True
            try:
                print_lock.acquire()
                print(f'Successfully scraped the data in the Page {current_page_num}.')
                print(f'with the total position number {self.scraped_total_job}.')
            finally:
                print_lock.release()

        else:
            try:
                print_lock.acquire()
                print('\nConnection error! url = {}.\n'.format(self.request_url))
                print('Status Code:', response.status_code)
            finally:
                print_lock.release()
                time.sleep(5)

    def change_web_scraping_info(self):
        print('Changing user-agent and the proxy...')
        ua = UserAgent()
        self.user_agent = str(ua.random)

    def get_page_trial(self, current_page_num):
        # If failed, try to connect for three more times.
        for index in range(1, 4):
            self.change_web_scraping_info()
            self.generate_new_header()
            self.get_page(current_page_num)

            if self.get_page_success is True:
                print('\nSuccessfully got the No.{} page in the No.'
                      ' {} time.\n'.format(current_page_num, index))
                break

        print('\nError: Have generated a new header for three times but still failed.'
              ' Will skip this page no. {}\n'.format(current_page_num))

    def get_threader(self):
        while True:
            try:
                # the worker will get one url from the queue, and then send a request
                page_num = self.post_url_queue.get(block=True, timeout=1)
                self.get_page(page_num)
                self.post_url_queue.task_done()
            except Empty:
                break

    def parse_threader(self):
        while True:
            try:
                # the worker will get one page json resource from the queue
                page_json = self.page_queue.get(block=True, timeout=1)
                self.parse_page(page_json)
                self.page_queue.task_done()
            except Empty:
                break

    def parse_page(self, page_json):
        """
        Data structure: [{job 1}, {job2}]
        """
        positions_list = page_json['content']['positionResult']['result']
        scraped_position_list = []

        for position in positions_list:
            # job position info
            position_id = position['positionId']
            position_name = position['positionName']
            position_edu = position['education']
            position_salary = position['salary']
            position_work_exp = position['workYear']

            # company info
            company_name = position['companyShortName']
            company_id = position['companyId']
            company_industry = position['industryField']
            company_size = position['companySize']
            company_lat = position['latitude']
            company_long = position['longitude']

            try:
                lock.acquire()

                scraped_position_list = [
                    self.city, position_id, position_name, position_edu,
                    position_salary, position_work_exp, company_name,
                    company_id,
                    company_industry, company_size, company_lat,
                    company_long
                ]

                print('scraped_position_list:', scraped_position_list)

                self.scraped_total_job += 1

                self.save_to_mysql(scraped_position_list)

            finally:
                lock.release()

    def connect_mysql(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='python_geek',
            charset='utf8mb4'
        )
        # 数据库游标，用于操作数据库
        self.cursor = self.connection.cursor()
        print('\nSuccessfully launched the connection with the database.\n')

    def save_to_mysql(self, scraped_position_list):
        try:
            # 将信息写入数据库
            sql_command = '''INSERT INTO week03_lagou(city, position_id, position_name, position_edu, 
            position_salary, position_work_exp, company_name, company_id, company_industry,
            company_size, company_lat, company_long) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
            print(sql_command)
            self.cursor.execute(sql_command,
                                [data_point for data_point in scraped_position_list])

            # 提交信息
            self.connection.commit()
            print('\nSuccessfully inserted', self.cursor.rowcount, 'rows of data.\n')

        except Exception as e:
            # 输出错误信息
            print(e)
            self.connection.rollback()
            print('The transcation was rolled back due to an exception error.')

    def __del__(self):
        self.cursor.close()
        self.connection.close()
        print('Successfully shut down the connection to the database.')


def multi_threading(job_spider, threader_type):
    thread_list = []

    for _ in range(job_spider.thread_num):
        if threader_type == 'parse_threader':
            t = threading.Thread(target=job_spider.parse_threader)
        elif threader_type == 'get_threader':
            t = threading.Thread(target=job_spider.get_threader)
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()


def main(city, job_position_num, thread_num):
    job_spider = JobSpider('Python', job_position_num, city, thread_num)

    for current_page_num in range(1, job_spider.page_num + 1):
        job_spider.post_url_queue.put(current_page_num)

    multi_threading(job_spider, 'get_threader')
    multi_threading(job_spider, 'parse_threader')

    del job_spider


if __name__ == '__main__':
    city_list = [
        '北京', '上海',
        '广州', '深圳'
    ]
    job_position_num = 100
    thread_num = 2
    for city in city_list:
        main(city, job_position_num, thread_num)
