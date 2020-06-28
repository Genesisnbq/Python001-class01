"""作业一"""
import requests
from bs4 import BeautifulSoup as bs
import os, csv


# 获取网页源代码
def get_html():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'cookie':'__mta=119928247.1592960836061.1592962029267.1592962068652.6; uuid_n_v=v1; uuid=07D56690B5B711EAA94453F28D7995DFBA2D5856F15B493F8131898F9CCBF36C; _lxsdk_cuid=172e3dd5873c8-0cd7261daa81f2-4353761-100200-172e3dd5873c8; _lxsdk=07D56690B5B711EAA94453F28D7995DFBA2D5856F15B493F8131898F9CCBF36C; mojo-uuid=4f6cd03d1c0b37d47a24ef5df1aafd69; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _csrf=a17f48be4eb7e0ecf3a782520341c112b4d514a8c2307a29c02e85e8df3cbc35; mojo-session-id={"id":"ae7d493c9a59a02c8f7686ff58dc5c71","time":1593165434257}; mojo-trace-id=1; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592960840,1593127235,1593152400,1593165434; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593165434; __mta=119928247.1592960836061.1592962068652.1593165435894.7; _lxsdk_s=172f00f4f3b-b16-055-878%7C%7C2'
    }
    
    myurl = 'https://maoyan.com/films?showType=3'

    response = requests.get(myurl, headers=headers)
    # 判断响应状态码是否为200。状态码为200，则返回html页面，并且备份一份在html文件夹中
    if response.status_code == 200:
        html = response.text
        # 若html文件夹不存在则创建
        if not os.path.exists('./html'):
            os.mkdir('./html')
        with open('./html/1.html', 'w', encoding='utf-8') as f1:
            f1.write(html)
        return True, html
    return False, '{}爬取失败'.format(myurl)

# 解析html，抓取出需要的数据
def parse_html(html):
    bs_info = bs(html, 'lxml')
    for dd in bs_info.find_all('dd'):
        movie_dd = dd.find('div', attrs = {'class':'movie-hover-title movie-hover-brief'})
        title = movie_dd['title']
        movie_type = dd.find('span',attrs = {'class':'hover-tag'}).parent.get_text(strip=True).replace('类型:', '')
        release_time = movie_dd.get_text(strip=True).replace('上映时间:', '')
        yield {
            '电影名':title,
            '类型':movie_type,
            '上映时间':release_time
        }

# 保存数据
def save_data(title,content,file_name):
    with open(file_name,'w',newline='', encoding='utf-8-sig') as f1:#numline是来控制空的行数的
        writer=csv.writer(f1)#这一步是创建一个csv的写入器
        writer.writerow(title)#写入标签
        writer.writerows(content)#写入样本数据
        print('finished!')
    
           
def main():
    flag, msg = get_html()

    if not flag:
        # 若第一次抓取失败则重新尝试2次
        for _ in range(2):
            flag, msg = get_html()
            if flag:
                break
    else:
        # 
        #with open('./html/1.html',encoding='utf-8') as f1:
            
        title = ['电影名', '类型', '上映时间']
        content = []
        for item in parse_html(msg):
            content.append([item['电影名'], item['类型'], item['上映时间']])
        save_data(title, content[:10], '猫眼电影.csv')
        print(content)

if __name__ == '__main__':
    main()
    
