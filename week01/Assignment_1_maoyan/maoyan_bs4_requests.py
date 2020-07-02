import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/83.0.4103.116 Safari/537.36'
cookie = '__mta=142391181.1593291039315.1593620523153.1593621068534.36; uuid_n_v=v1; ' \
         'uuid=DB5A5E00B8B711EA8A833903D31672830D67A9B14A884D14BA873711FA60C96A; ' \
         '_lxsdk_cuid=172f78bdffc72-0e8930ceabf6f6-4353760-144000-172f78bdffdc8; ' \
         '_lxsdk=DB5A5E00B8B711EA8A833903D31672830D67A9B14A884D14BA873711FA60C96A; ' \
         'mojo-uuid=8ae196871f15954ff9f1914dbf9e67fb; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; ' \
         '_csrf=8dcb0db31e81448fbd350e6b05577da99dfca90aa284333ead6f29326ad4deee; ' \
         'JSESSIONID=l9r1kztavnbkxriqiut0tvb6; ' \
         'lt=Ag2I0xStDeRVtoikygwhEgvufKsAAAAAAwsAAAnFmy1TS3Dx2cagnahZHjhUH_kCadsNZIh7fRiB8mueW03XN--7PzcHAapVKwZ8Ow; ' \
         'lt.sig=0zAveqRuQ2B3Pp6Utv28pPolGu4; mojo-session-id={"id":"d40b1e36b36a8388f96753814a7e752e",' \
         '"time":1593626120394}; mojo-trace-id=2; __mta=142391181.1593291039315.1593621068534.1593626181967.37; ' \
         '_lxsdk_s=1730b84cd8d-3b5-0da-8da%7C1765851443%7C5 '
header = {'user-agent': user_agent, 'cookie': cookie}

# header = {'user-agent': user_agent}

url = 'https://maoyan.com/films?showType=3'

response = requests.get(url, headers=header)

bs_info = bs(response.text, 'html.parser')


def get_details(link_url):
    rs = requests.get(link_url, headers=header)
    bs_temp = bs(rs.text, 'html.parser')
    movie_time = ''
    movie_type = ''
    type_and_time = bs_temp.find('div', attrs={'class': 'movie-brief-container'})
    for a_tag in type_and_time.find_all('a', ):
        movie_type += a_tag.get_text()
    movie_type = movie_type.strip()
    count_li = 0
    for li_tag in type_and_time.find_all('li', attrs={'class': 'ellipsis'}):
        if count_li > 1:
            movie_time = li_tag.get_text()
            break
        count_li += 1
    print(movie_type)
    print(movie_time)
    mylist = [(title, movie_type, movie_time)]
    mylist = pd.DataFrame(data=mylist)
    mylist.to_csv('./maoyan_top10.csv', mode='a', header=False, encoding='utf_8_sig', index=False, line_terminator=None)


init_list = [('电影名称', '类型', '上映日期')]
init_title = pd.DataFrame(data=init_list)
init_title.to_csv('./maoyan_top10.csv', header=False, encoding='utf_8_sig', index=False, line_terminator=None,
                  mode='w')

count = 0
for title_div in bs_info.find_all('div', attrs={'class': 'channel-detail movie-item-title'}):
    if count > 9:
        break
    title = title_div.find('a', ).get_text()
    link = 'https://maoyan.com' + title_div.find('a', ).get('href')
    print(title)
    # print(link)
    get_details(link)
    count += 1
