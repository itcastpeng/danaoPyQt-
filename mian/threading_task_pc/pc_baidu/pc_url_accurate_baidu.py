from bs4 import BeautifulSoup
from time import sleep
from urllib.request import urlopen
from mian.my_db import database_create_data
import random
import datetime
import chardet
import requests
from mian.threading_task_pc.public import shouluORfugaiChaxun
from mian.threading_task_pc.public import getpageinfo, shouluORfugaiChaxun
pcRequestHeader = [
    'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; .NET CLR 1.1.4322)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-CN; rv:1.9.0.19) Gecko/2010031422 Firefox/3.0.19 (.NET CLR 3.5.30729)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13'
]

class Baidu_Zhidao_URL_PC():

    def __init__(self, detail_id, keyword, domain):
        self.data_base_list = []
        self.keyword = keyword
        self.domain = domain
        self.detail_id = detail_id
        self.headers = {
            'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}
        self.zhidao_url = 'https://www.baidu.com/s?wd={keyword}'.format(keyword='{}')
        data_list = self.get_keywords()
        self.set_data(data_list)

    def get_keywords(self):
        # 调用查询收录
        rank_num = 0
        resultObj = shouluORfugaiChaxun.baiduShouLuPC(self.domain)
        ret = requests.get(self.zhidao_url.format(self.keyword), headers=self.headers, timeout=10)
        soup = BeautifulSoup(ret.text, 'lxml')
        div_tags = soup.find_all('div', class_='result c-container ')
        data_list = []
        yuming = ''
        panduan_url = ''
        for div_tag in div_tags:
            if div_tags and div_tag.attrs.get('id'):
                panduan_url = div_tag.find('a').attrs['href']
            div_13 = div_tag.find('div', class_='f13')
            if div_13.find('a'):
                yuming = div_13.find('a').get_text()[:-5].split('/')[0]  # 获取域名
                status_code, title, ret_two_url = getpageinfo.getPageInfo(panduan_url)
                print('ret_two_url, self.domain=======> ',ret_two_url, self.domain)
                if yuming in self.domain:
                    if self.domain in ret_two_url:
                        rank_num = div_tag.attrs.get('id')
                        break
        data_list = {
            'order':int(rank_num),
            'shoulu': resultObj['shoulu']
        }
        print(data_list)
        return data_list

    def set_data(self, data_list):
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        # for data in data_list:
        insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
            order=data_list['order'], shoulu=data_list['shoulu'], detail_id=self.detail_id, date_time=date_time)
        print(insert_sql)
        database_create_data.operDB(insert_sql, 'insert')
        update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(self.detail_id)
        print(update_sql)
        database_create_data.operDB(update_sql, 'update')