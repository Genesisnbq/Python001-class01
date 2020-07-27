import time
import pyautogui
from selenium import webdriver

mobile = pyautogui.prompt(text='请输入手机号', title='登录')
password = pyautogui.password(text='请输入密码', title='登录', mask='*')

# 加载驱动
browser = webdriver.Chrome()
browser.get('https://shimo.im/login?from=home')  # 通过浏览器打开页面

time.sleep(1)
browser.find_element_by_xpath('//div[@class="input"]//input[@type="text"]').send_keys(mobile)
browser.find_element_by_xpath('//div[@class="input"]//input[@type="password"]').send_keys(password)

time.sleep(1)
browser.find_element_by_xpath('//button[@type="black"]').click()

time.sleep(10)
browser.close()




