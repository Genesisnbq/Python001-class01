# -*- coding:utf8 -*-

import requests
import pyautogui
from traceback import format_exc


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.116 Safari/537.36',
    'x-requested-with': 'XmlHttpRequest',
    'x-source':	'lizard-desktop',
    'content-type':	'application/x-www-form-urlencoded; charset=utf-8',
    'accept': '*/*',
    'origin': 'https://shimo.im',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://shimo.im/login?from=home',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
}


def login(session, mobile, password):
    session.headers.update(HEADERS)
    index_url = 'https://shimo.im/lizard-api/auth/password/login'
    data = {
        'mobile': '+86' + mobile,
        'password': password
    }
    try:
        resp = session.post(index_url, data=data, timeout=10, verify=False)
        url = 'https://shimo.im/lizard-api/users/me'
        resp =  session.get(url)
        content = resp.json()
        print(content)
        if 'error' in content:
            return False, content
        return True, None
    except:
        return False, format_exc()


def main():
    mobile = pyautogui.prompt(text='请输入手机号', title='登录')
    password = pyautogui.password(text='请输入密码', title='登录', mask='*')
    session = requests.session()
    succ, msg = login(session, mobile, password)
    if not succ:
        print('login failed err_msg:%s', msg)
        return
    print('login success')


if __name__ == '__main__':
    main()