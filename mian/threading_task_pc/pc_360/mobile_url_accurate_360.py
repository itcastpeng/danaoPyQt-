import requests, random
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet
from mian.my_db import database_create_data
from mian.threading_task_pc.public import shouluORfugaiChaxun
from mian.threading_task_pc.public.getpageinfo import getPageInfo
from mian.threading_task_pc.public import getpageinfo, shouluORfugaiChaxun

class Baidu_Zhidao_URL_MOBILE(object):

    def __init__(self, detail_id, keyword, domain):
        self.keyword = keyword
        self.detail_id = detail_id
        self.domain = domain
        self.PC_360_url = 'https://m.so.com/s?src=3600w&q={}'.format(self.keyword)
        print('self.PC_360_url------------> ',self.PC_360_url)
        data_list = self.get_keywords()
        # self.set_data(data_list)

    def get_keywords(self):
        data_objs = ''
        data_order = 0
        data_list = []
        resultObj = shouluORfugaiChaxun.baiduShouLuPC(self.domain)
        headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        ret = requests.get(self.PC_360_url, headers=headers)
        soup = BeautifulSoup(ret.text, 'lxml')
        if soup.find('div', class_='mso-url2link'):
            print('无收录')
        else:
            div_tags = soup.find_all('div', class_='g-card res-list sumext-tpl-image mso')
            for div_tag in div_tags:
                data_order += 1
                if div_tag.attrs.get('data-pcurl'):
                    url_data = div_tag.attrs.get('data-pcurl')
                    status_code, title, ret_two_url = getpageinfo.getPageInfo(url_data)
                    if ret_two_url == self.domain:
                        data_order = data_order
        data_list.append({
            'order': int(data_order),
            'shoulu': resultObj['shoulu'],
            })
        print('data_list================> ',data_list)
        return data_list

    def random_time(self):
        return sleep(random.randint(1, 2))


    def set_data(self, data_list):
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        print('data_list====================> ',data_list)
        # for data in data_list:
        #     insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
        #         order=data['order'], shoulu=data['shoulu'], detail_id=self.detail_id, date_time=date_time)
        #     database_create_data.operDB(insert_sql, 'insert')
        #     update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(self.detail_id)
        #     database_create_data.operDB(update_sql, 'update')


if __name__ == '__main__':
    keyword = '天津美莱双眼皮埋线好不好 美莱暖冬计划启动中'
    # domain = 'http://news.39.net/a/171204/5900289.html'
    # domain = 'http://www.jianzhijia.com/hyzx/jkjd/79381.html'
    domain = 'https://m.smxe.cn/article/148402.shtml'
    detail_id = 22
    Baidu_Zhidao_URL_MOBILE(detail_id, keyword, domain)
