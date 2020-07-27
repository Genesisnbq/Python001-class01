import time
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

headers = {
    'User-Agent': ua.random,
    'Referer': 'https://shimo.im/login',
    # 防止csrf检测
    'x-requested-with': 'XmlHttpRequest'
}

s = requests.Session()
# 会话对象, 在同一个Session实例发出的所有请求之间保持 cookie
# 期间使用urllib3 的connection pooling 功能
# 向同一主机发送多个请求, 底层的TCP连接将会被重用, 从而带来显著的性能提升

login_url = 'https://shimo.im/lizard-api/auth/password/login'

from_data = {
    'mobile': '+8617681533618',
    'password': 'QQ1485607996'
}

response = s.post(login_url, data=from_data, headers=headers)

print(response.text)

# 登录后访问一下个人中心页面看是否成功
url2 = 'https://shimo.im/dashboard/used'
response2 = s.get(url2, headers=headers)
print(response2.status_code)
