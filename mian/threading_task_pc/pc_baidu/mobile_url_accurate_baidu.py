import requests, random
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet
from my_db import database_create_data
from mian.threading_task_pc.public import getpageinfo, shouluORfugaiChaxun


class Baidu_Zhidao_URL_MOBILE(object):
    def __init__(self,detail_id, keyword, domain):
        self.keyword = keyword
        self.detail_id = detail_id
        self.domain = domain
        self.zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'
        data_list = self.get_keywords()
        self.set_data(data_list)

    def get_keywords(self):
        shoulu = ''
        paiming_order = '0'
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        resultObj = shouluORfugaiChaxun.baiduShouLuMobeil(self.domain)
        url = self.zhidao_url.format(self.keyword)
        ret_two = requests.get(url, headers=headers, timeout=10)
        soup_two = BeautifulSoup(ret_two.text, 'lxml')
        content_list_order = []
        div_tags = soup_two.find_all('div', class_='result c-result')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        div_tags = soup_two.find_all('div', class_='result c-result c-clk-recommend')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        for obj_tag in content_list_order:
            dict_data_clog = eval(obj_tag.attrs.get('data-log'))
            url = dict_data_clog['mu']
            status_code, title, ret_two_url = getpageinfo.getPageInfo(url)
            print(ret_two_url, self.domain)
            if ret_two_url == self.domain or self.domain in ret_two_url:
                paiming_order = dict_data_clog['order']
                break
        data_list = {
            'order': int(paiming_order),
            'shoulu':resultObj['shoulu'],
            }
        return data_list

    def set_data(self, data_list):
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        for data in data_list:
            insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
                order=data['order'], shoulu=data['shoulu'], detail_id=self.detail_id, date_time=date_time)
            database_create_data.operDB(insert_sql, 'insert')
            update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(self.detail_id)
            database_create_data.operDB(update_sql, 'update')
