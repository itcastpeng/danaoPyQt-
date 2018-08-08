import requests, random
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet
from my_db import database_create_data
from threading_task_pc.public import shouluORfugaiChaxun, getpageinfo



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


class Baidu_Zhidao_yuming_pc():
    def __init__(self, yinqing, keyword, mohu_pipei, detail_id):
        self.keyword = keyword
        self.detail_id = detail_id
        self.mohu_pipei_list = mohu_pipei.split(',')
        self.yinqing = yinqing
        self.headers = {
            'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)],}
        self.zhidao_url = 'https://www.baidu.com/s?wd={keyword}'.format(keyword='{}')
        data_list = self.get_keywords()
        self.set_data(data_list)


    def get_keywords(self):
        ret = requests.get(self.zhidao_url.format(self.keyword) ,headers=self.headers, timeout=10)
        soup = BeautifulSoup(ret.text, 'lxml')
        div_tags = soup.find_all('div', class_='result c-container ')
        data_list = []
        str_order = ''
        order_list = []
        ret_two_url = ''
        shoulu = 0
        rank_num = ''
        for div_tag in div_tags:
            tiaojian_chaxun = div_tag.get_text()
            panduan_url = div_tag.find('h3',class_='t').find('a').attrs['href']
            status_code, title, ret_two_url = getpageinfo.getPageInfo(panduan_url)  # 获取对应页面的标题
            for mohu_pipei in self.mohu_pipei_list:
                if mohu_pipei in tiaojian_chaxun:  # 表示有覆盖
                    rank_num = div_tag.attrs.get('id')
                    order_list.append(int(rank_num))
                    str_order = ",".join(str(i) for i in order_list)
                    result = shouluORfugaiChaxun.baiduShouLuPC(ret_two_url)
                    shoulu = result['shoulu']

        data_list.append({
            'paiming_detail': str_order,
            'shoulu': shoulu,
        })
        return data_list


    def set_data(self,data_list):
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        for data in data_list:
            insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{tid}', '{date_time}');""".format(
                order=data['paiming_detail'],shoulu=data['shoulu'],tid=self.detail_id,date_time=date_time)
            # print('insert_sql------> ',insert_sql, 'Baidu_Zhidao_yuming_pc')
            database_create_data.operDB(insert_sql, 'insert')
            update_sql = """update task_Detail set is_perform = '0' where id = '{tid}'""".format(tid = self.detail_id)
            # print('update_sql======> ',update_sql)
            database_create_data.operDB(update_sql, 'update')

