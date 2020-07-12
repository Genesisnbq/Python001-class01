# -*- coding:utf8 -*-

import time
import pyautogui
from selenium import webdriver

mobile = pyautogui.prompt(text='请输入手机号', title='登录')
password = pyautogui.password(text='请输入密码', title='登录', mask='*')

browser = webdriver.Chrome()
browser.get('https://shimo.im/login?from=home')
time.sleep(1)

browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input')\
    .send_keys(mobile)
browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input')\
    .send_keys(password)
time.sleep(1)
browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()
time.sleep(10)
browser.close()