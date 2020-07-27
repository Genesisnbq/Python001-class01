Week2 学习笔记

总结:

1. 异常捕获与处理

2. 使用PyMySQL进行数据库操作

3. 模拟浏览器头部(from fake_useragent import UserAgent)

4. cookies验证(复制f12后尽可能多的信息组成data)

5. WebDriver--> 模拟浏览器动作 from selenium import webdriver

   ```python
   browser = webdriver.Chrome()
   
   browser.get(url)
   
   browser.switch_to.frame(browser.find.....)
   
   cookies=browser.get_cookies()   #登录之后, 获取cookies
   ```

   

6. 验证码识别

   ```python
   from PIL import Image
   import pytesseract
   from fake_useragent import UserAgent
   
   session = requests.session()
   
   header = {'User-Agent': user_agent}
   r = session.get(img_url, headers=header)
   
   # 打开验证码图片, 
   with open('cap.jpg', 'wb') as f:
       f.write(r.content)
       
   # 打开并显示文件
   image = Image.open('cap.jpg')
   # image.show()
   
   # 灰度图片
   gray = image.convert('L')
   gray.save('c_gray2.jpg')
   image.close()
   
   # 二值化
   threshold = 100  # 设定一个阈值
   table = []
   
   for i in range(256):
       if i < threshold:
           table.append(0)
       else:
           table.append(1)
   out = gray.point(table, '1')
   out.save('c_th.jpg')
   
   # 最后识别
   th = Image.open('c_th.jpg')
   th.show()
   print(pytesseract.image_to_string(th, lang='chi_sim+eng'))
   ```

7. 爬虫中间件与系统代理ip

   中间件: 下载中间件和爬虫中间件

   代理ip: 

   ​	临时: set http_proxy=xxx:端口号

   ​			 打开下载中间件

8. 自定义中间件&随机代理ip

   1. 自定义

      settings中把其他下载中间件的优先级设置为 None 留下第一个543 和 RandomHttpProxyMiddleware  设置为400

   2. middlewares.py中 增加一个 RandomHttpProxyMiddleware(HttpProxyMiddleware)

      并重写三个方法

      ```python
      from scrapy import signals
      from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
      from scrapy.exceptions import NotConfigured
      from collections import defaultdict
      from urllib.parse import urlparse
      import random
      
      class RandomHttpProxyMiddleware(HttpProxyMiddleware):
          def __init__(self, auth_encoding='utf-8', proxy_list=None):
              super().__init__(auth_encoding)
              self.proxies = defaultdict(list)
              for proxy in proxy_list:
                  parse = urlparse(proxy)  # 拆分
                  self.proxies[parse.scheme].append(proxy)
      
          @classmethod
          def from_crawler(cls, crawler):
              if not crawler.settings.get('HTTP_PROXY_LIST'):
                  raise NotConfigured
              http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')
              auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')
      
              return cls(auth_encoding, http_proxy_list)
      
          def _set_proxy(self, request, scheme):
              proxy = random.choice(self.proxies[scheme])
              request.meta['proxy'] = proxy
      ```

9. 分布式爬虫

   Redis是现在最流行的非关系型数据库 NoSQL

   windows安装redis:

   1. 去github下载windows版本 msi
   2. 安装, 勾上path, 内存限制 1024
   3. 到redis安装目录复制     redis.windows.conf(配置文件模板)

   ---

   和之前爬虫的主要变化在settings.py中, 如果使用了 redis-scrapy

   就需要使用新的组件替换原有的组件

   **在settings.py中, 增加redis信息**

   ```python
   # redis 信息
   REDIS_HOST = '127.0.0.1'
   REDIS_PORT = 6379
   
   # scheduler 的QUEUE
   SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
   
   # 去重
   DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
   
   # Requests的默认优先级队列
   SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
   
   # 将Requests队列持久化到Redis, 可支持暂停或重启爬虫
   SCHEDULER_PERSIST = True
   
   # 将爬取到的items保存到Redis
   ITEM_PIPELINES = {
       'scrapy_redis.pipelines.RedisPipeline': 300
   }
   ```

   我们一般会使用 redis集群, 然后把数据慢慢地传入MySQL中

```redis
# redis 存储了item
# 在Terminal中 redis-cli
# keys *    查看redis中所有的key
# type cluster:item  查看 cluster:item的类型   cluster:item是key
# lpop cluster:item  查看 cluster:item的内容
# keys *
```

