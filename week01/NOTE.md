# 学习笔记 week1 倪彬琪

### 一. 利用python开发爬虫

1.  提出需求: 具体需要完成什么样的任务

2. 编码: 根据需求, 通过代码去实现功能

3. 代码Run起来

4.  修复和完善

------

###　二. requests

1. **requests 官方文档链接**： https://requests.readthedocs.io/zh_CN/latest/
2. 主要方法: requests.get(网址, headers=header)
3. 使用urllib.request的方式要比requests库麻烦很多, 所以我们一般获取网页内容的时候, 多数都会使用第三方包 requests



------

### 三. 模拟浏览器请求

```python
#需要增加http请求的头部信息 
user_agent=''
header = {'user-agent':user_agent}
```



------

### 四. BeautifulSoup

我们了解到可以通过requests 像浏览器一样,把网页内容返回回来, 但是离我们的需求还有很大的距离!!!

**利用BeautifulSoup对源代码进一步处理**

**Beautiful Soup 官方文档链接：** https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/



------

### 五. 使用XPath解析网页

XPath 也是进行搜索的, 用起来也比 BeautifulSoup简单,搜索的速度也更快



------

### 六. 实现爬虫自动翻页

找规律, 然后使用推导式的方式, 最后遍历



---

### 七. Python基础语法回顾

- Python 简介： https://docs.python.org/zh-cn/3.7/tutorial/introduction.html
- Python 数据结构： https://docs.python.org/zh-cn/3.7/tutorial/datastructures.html
- Python 其他流程控制工具 : https://docs.python.org/zh-cn/3.7/tutorial/controlflow.html
- Python 中的类： https://docs.python.org/zh-cn/3.7/tutorial/classes.html
- Python 定义函数： https://docs.python.org/zh-cn/3.7/tutorial/controlflow.html#defining-functions

---

### 八. 网页组成部分

1. 结构
2. HTML语言

1. 表现
2. css把结构和表现形式做了一个分离

3. 行为
4. js脚本(jQuery)

---

### 九. HTTP协议

Headers 是我们传输的 头部的信息

在登录账号的时候Request Method是post

get: 请求网页内容

post:用户和密码登录

##### 具体头部请求

需要关心两个部分:

1. **cookie**

当使用cookie的时候, 就代表带着用户名和密码的验证信息, 向网页发起请求, 爬虫的时候, 有些网页的内容, 必须要登录成功之后才能进行显示, 这种情况下, 我们就会使用post方式去提交用户名和密码,

提交了之后, 服务器经过验证之后会给客户端返回一些信息, 客户端下次请求的时候, 通过cookie来携带我的用户名和密码的验证信息, 就是用这段加密后的cookie进行提交的

2. **User-Agent**

1. 1. 鉴别浏览器
   2. 反爬虫

拿python去模拟浏览器请求时, 服务商发现我请求的客户端是拿python编写的,并不是一个真正的使用的用户, 可能会阻止我继续进行请求,所以, 我们一般都会去模拟不同浏览器的Headers,一般模拟 cookie 和 User-Agent, 防止被服务器识别出来, 我的程序是一个爬虫,这是反爬虫技术

------

###　十. Scrapy框架结构

| 引擎     | 发动机, 整个爬虫的大脑, 数据下载, 处理, 都会流经引擎, 高校处理并行爬取数据 |
| -------- | ------------------------------------------------------------ |
| 调度器   | 把引擎传过来的requests进行一个排序(队列), 同时去重, 不需要手动去重了 |
| 下载器   | 比requests更加强大                                           |
| 爬虫     | 从特定网页分析出里面的内容,Spiders 比 BeautifulSoup更加智能, 如果时url , 那么会自动进行下一次请求 |
| 项目管道 | 爬取页面, 抽取的信息, 通过管道, 可以存入指定的介质(文件, 数据库)中, Scrapy已经实现了 |

**只需要真正了解内容, 不需要了解如何工作, 这就是所谓的爬虫的框架的优势**

---

### 十一. Scrapy 爬虫目录

| 实现爬虫的python文件     | spiders目录              |
| ------------------------ | ------------------------ |
| 项目的设置文件           | settings.py              |
| 项目的配置文件           | scrapy.cfg               |
| 定义所爬取记录的数据结构 | items.py                 |
| 编写爬虫逻辑             | spidername.py(爬虫名.py) |
| 设置保存位置             | piplines.py              |

---

### 十二. 将requests爬虫改写为scrapy爬虫

1. 先cd到目标文件夹, 然后scrapy startproject 项目名称

2. cd 项目名称两次

3. scrapy genspider 爬虫名 域名域

   scrapy genspider my_attempt movie.douban.com

4. 修改爬虫名.py  实现真正的爬虫逻辑

5. 根据真正逻辑,选择是否自己写parse函数

6. 实现 parse函数 return item , 解耦(通过管道传给别人)

7. 修改pipeline.py  最简单是直接return item       打印在cmd上, 也可以存入其他介质(数据库, 文件)

8. 修改settings.py  user-agent放开  download delay也放开

9. 修改Items.py  xxx = Scrapy.Field()

10. 最后 进入my_attempt/my_attempt    scrapy crawl 爬虫名

---

### 十三. 通过Scrapy爬取电影详情页信息

在原有的 scrapy.request()下 再做一次请求

返回下一次请求(有两条路,1. 再次向scheduler发起请求

返回item)

---

### 十四.  XPath

1. 节点

   在xpath中有7中节点类型: 元素, 属性,文本, 命名空间,处理指令, 注释已经文档(根)节点, 文档是被作为节点树来对待的, 树的根被称为文档节点或者根结点

   ```
   <bookstore> （文档节点）
   <author>J K. Rowling</author> （元素节点）
   lang="en" （属性节点） 
   ```

2. 基本值

   基本值是无父或者无子的节点

   ```
   J K. Rowling
   "en"
   ```

3. 项目(items)

   项目是基本值或者节点

4. 节点关系

   ---

   **父(parent)**

   book是其他元素的父

   ```
   <book>
     <title>Harry Potter</title>
     <author>J K. Rowling</author>
     <year>2005</year>
     <price>29.99</price>
   </book>
   ```

   ---

   **子(children)**

   元素节点可有零个、一个或多个子。

   其他元素都是book元素的子

   ```
   <book>
     <title>Harry Potter</title>
     <author>J K. Rowling</author>
     <year>2005</year>
     <price>29.99</price>
   </book>
   ```

   ---

   **同胞**(sibling)

   同级的

   ---

   **先辈**(ancestor)

   某节点的父、父的父，等等。

   ---

   **后代(Descendant)**

   某个节点的子，子的子，等等。

   ----

5. 选取节点

   | nodename | 选取此节点的所有子节点。                                   |
   | -------- | ---------------------------------------------------------- |
   | /        | 从根节点选取。                                             |
   | //       | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 |
   | .        | 选取当前节点。                                             |
   | ..       | 选取当前节点的父节点。                                     |
   | @        | 选取属性。                                                 |

   | bookstore       | 选取 bookstore 元素的所有子节点。                            |
   | --------------- | ------------------------------------------------------------ |
   | /bookstore      | 选取根元素 bookstore。注释：假如路径起始于正斜杠( / )，则此路径始终代表到某元素的绝对路径！ |
   | bookstore/book  | 选取属于 bookstore 的子元素的所有 book 元素。                |
   | //book          | 选取所有 book 子元素，而不管它们在文档中的位置。             |
   | bookstore//book | 选择属于 bookstore 元素的后代的所有 book 元素，而不管它们位于 bookstore 之下的什么位置。 |
   | //@lang         | 选取名为 lang 的所有属性。                                   |

   ---

6. 谓语

   谓语用来查找某个特定的节点或者包含某个指定的值的节点。

   谓语被嵌在方括号中。

   | 路径表达式                         | 结果                                                         |
   | :--------------------------------- | :----------------------------------------------------------- |
   | /bookstore/book[1]                 | 选取属于 bookstore 子元素的第一个 book 元素。                |
   | /bookstore/book[last()]            | 选取属于 bookstore 子元素的最后一个 book 元素。              |
   | /bookstore/book[last()-1]          | 选取属于 bookstore 子元素的倒数第二个 book 元素。            |
   | /bookstore/book[position()<3]      | 选取最前面的两个属于 bookstore 元素的子元素的 book 元素。    |
   | //title[@lang]                     | 选取所有拥有名为 lang 的属性的 title 元素。                  |
   | //title[@lang='eng']               | 选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。   |
   | /bookstore/book[price>35.00]       | 选取 bookstore 元素的所有 book 元素，且其中的 price 元素的值须大于 35.00。 |
   | /bookstore/book[price>35.00]/title | 选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于 35.00。 |

   ---

7. 选取未知节点

   | 通配符 | 描述                 |
   | :----- | :------------------- |
   | *      | 匹配任何元素节点。   |
   | @*     | 匹配任何属性节点。   |
   | node() | 匹配任何类型的节点。 |

   | 路径表达式   | 结果                              |
   | :----------- | :-------------------------------- |
   | /bookstore/* | 选取 bookstore 元素的所有子元素。 |
   | //*          | 选取文档中的所有元素。            |
   | //title[@*]  | 选取所有带有属性的 title 元素。   |

8. 选取若干节点

   通过在路径表达式中使用“|”运算符，您可以选取若干个路径。

   | 路径表达式                       | 结果                                                         |
   | :------------------------------- | :----------------------------------------------------------- |
   | //book/title \| //book/price     | 选取 book 元素的所有 title 和 price 元素。                   |
   | //title \| //price               | 选取文档中的所有 title 和 price 元素。                       |
   | /bookstore/book/title \| //price | 选取属于 bookstore 元素的 book 元素的所有 title 元素，以及文档中所有的 price 元素。 |

9. Xpath轴

   **轴可定义相对于当前节点的节点集。**

   | 轴名称             | 结果                                                     |
   | :----------------- | :------------------------------------------------------- |
   | ancestor           | 选取当前节点的所有先辈（父、祖父等）。                   |
   | ancestor-or-self   | 选取当前节点的所有先辈（父、祖父等）以及当前节点本身。   |
   | attribute          | 选取当前节点的所有属性。                                 |
   | child              | 选取当前节点的所有子元素。                               |
   | descendant         | 选取当前节点的所有后代元素（子、孙等）。                 |
   | descendant-or-self | 选取当前节点的所有后代元素（子、孙等）以及当前节点本身。 |
   | following          | 选取文档中当前节点的结束标签之后的所有节点。             |
   | namespace          | 选取当前节点的所有命名空间节点。                         |
   | parent             | 选取当前节点的父节点。                                   |
   | preceding          | 选取文档中当前节点的开始标签之前的所有节点。             |
   | preceding-sibling  | 选取当前节点之前的所有同级节点。                         |
   | self               | 选取当前节点。                                           |

10. 路径表达式

    位置路径可以是绝对的，也可以是相对的。

    绝对路径起始于正斜杠( / )，而相对路径不会这样。在两种情况中，位置路径均包括一个或多个步，每个步均被斜杠分割：

    ### 绝对位置路径：

    ```
    /step/step/...
    ```

    ### 相对位置路径：

    ```
    step/step/...
    ```

    每个步均根据当前节点集之中的节点来进行计算。

11. ### 步（step）包括:

    轴（axis）

    定义所选节点与当前节点之间的树关系

    节点测试（node-test）

    识别某个轴内部的节点

    零个或者更多谓语（predicate）

    更深入地提炼所选的节点集

    ### 步的语法：

    ```
    轴名称::节点测试[谓语]
    ```

    | 例子                   | 结果                                                         |
    | :--------------------- | :----------------------------------------------------------- |
    | child::book            | 选取所有属于当前节点的子元素的 book 节点。                   |
    | attribute::lang        | 选取当前节点的 lang 属性。                                   |
    | child::*               | 选取当前节点的所有子元素。                                   |
    | attribute::*           | 选取当前节点的所有属性。                                     |
    | child::text()          | 选取当前节点的所有文本子节点。                               |
    | child::node()          | 选取当前节点的所有子节点。                                   |
    | descendant::book       | 选取当前节点的所有 book 后代。                               |
    | ancestor::book         | 选择当前节点的所有 book 先辈。                               |
    | ancestor-or-self::book | 选取当前节点的所有 book 先辈以及当前节点（如果此节点是 book 节点） |
    | child::*/child::price  | 选取当前节点的所有 price 孙节点。                            |

12. XPath运算符

    | 运算符 | 描述           | 实例                      | 返回值                                                       |
    | :----- | :------------- | :------------------------ | :----------------------------------------------------------- |
    | \|     | 计算两个节点集 | //book \| //cd            | 返回所有拥有 book 和 cd 元素的节点集                         |
    | +      | 加法           | 6 + 4                     | 10                                                           |
    | -      | 减法           | 6 - 4                     | 2                                                            |
    | *      | 乘法           | 6 * 4                     | 24                                                           |
    | div    | 除法           | 8 div 4                   | 2                                                            |
    | =      | 等于           | price=9.80                | 如果 price 是 9.80，则返回 true。如果 price 是 9.90，则返回 false。 |
    | !=     | 不等于         | price!=9.80               | 如果 price 是 9.90，则返回 true。如果 price 是 9.80，则返回 false。 |
    | <      | 小于           | price<9.80                | 如果 price 是 9.00，则返回 true。如果 price 是 9.90，则返回 false。 |
    | <=     | 小于或等于     | price<=9.80               | 如果 price 是 9.00，则返回 true。如果 price 是 9.90，则返回 false。 |
    | >      | 大于           | price>9.80                | 如果 price 是 9.90，则返回 true。如果 price 是 9.80，则返回 false。 |
    | >=     | 大于或等于     | price>=9.80               | 如果 price 是 9.90，则返回 true。如果 price 是 9.70，则返回 false。 |
    | or     | 或             | price=9.80 or price=9.70  | 如果 price 是 9.80，则返回 true。如果 price 是 9.50，则返回 false。 |
    | and    | 与             | price>9.00 and price<9.90 | 如果 price 是 9.80，则返回 true。如果 price 是 8.50，则返回 false。 |
    | mod    | 计算除法的余数 | 5 mod 2                   | 1                                                            |