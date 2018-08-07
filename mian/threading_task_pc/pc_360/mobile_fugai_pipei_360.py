import requests, random
from bs4 import BeautifulSoup
import datetime
from time import sleep
from my_db import database_create_data

import chardet
from mian.my_db import database_create_data
mobile_emulation = {
            "deviceName": "Apple iPhone 3GS",
            "deviceName": "Apple iPhone 4",
            "deviceName": "Apple iPhone 5",
            "deviceName": "Apple iPhone 6",
            "deviceName": "Apple iPhone 6 Plus",
            "deviceName": "BlackBerry Z10",
            "deviceName": "BlackBerry Z30",
            "deviceName": "Google Nexus 4",
            "deviceName": "Google Nexus 5",
            "deviceName": "Google Nexus S",
            "deviceName": "HTC Evo, Touch HD, Desire HD, Desire",
            "deviceName": "HTC One X, EVO LTE",
            "deviceName": "HTC Sensation, Evo 3D",
            "deviceName": "LG Optimus 2X, Optimus 3D, Optimus Black",
            "deviceName": "LG Optimus G",
            "deviceName": "LG Optimus LTE, Optimus 4X HD" ,
            "deviceName": "LG Optimus One",
            "deviceName": "Motorola Defy, Droid, Droid X, Milestone",
            "deviceName": "Motorola Droid 3, Droid 4, Droid Razr, Atrix 4G, Atrix 2",
            "deviceName": "Motorola Droid Razr HD",
            "deviceName": "Nokia C5, C6, C7, N97, N8, X7",
            "deviceName": "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900",
            "deviceName": "Samsung Galaxy Note 3",
            "deviceName": "Samsung Galaxy Note II",
            "deviceName": "Samsung Galaxy Note",
            "deviceName": "Samsung Galaxy S III, Galaxy Nexus",
            "deviceName": "Samsung Galaxy S, S II, W",
            "deviceName": "Samsung Galaxy S4",
            "deviceName": "Sony Xperia S, Ion",
            "deviceName": "Sony Xperia Sola, U",
            "deviceName": "Sony Xperia Z, Z1",
            "deviceName": "Amazon Kindle Fire HDX 7″",
            "deviceName": "Amazon Kindle Fire HDX 8.9″",
            "deviceName": "Amazon Kindle Fire (First Generation)",
            "deviceName": "Apple iPad 1 / 2 / iPad Mini",
            "deviceName": "Apple iPad 3 / 4",
            "deviceName": "BlackBerry PlayBook",
            "deviceName": "Google Nexus 10",
            "deviceName": "Google Nexus 7 2",
            "deviceName": "Google Nexus 7",
            "deviceName": "Motorola Xoom, Xyboard",
            "deviceName": "Samsung Galaxy Tab 7.7, 8.9, 10.1",
            "deviceName": "Samsung Galaxy Tab",
            "deviceName": "Notebook with touch",
            "deviceName": "iPhone 6"
}

class Baidu_Zhidao_yuming_mobile(object):
    def __init__(self,  keyword, domain):
        # print('进入爬虫 ---------- 移动端')
        # self.tid = tid
        self.keyword = keyword
        self.domain = domain
        self.content_data_list = []
        # self.detail_id = detail_id
        # self.fugai_chaxun = fugai_chaxun
        # self.yinqing = yinqing
        # self.huoqu_gonggong_time_stamp = huoqu_gonggong_time_stamp
        self.PC_360_url = 'https://m.so.com/s?src=3600w&q={}'.format(keyword)
        self.headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        # if self.fugai_chaxun:
        self.get_keyword()
        # else:
        #     data_list = self.get_keyword()
        #     self.set_data(data_list)


    def get_keyword(self):
        print('请求的url --------------------- > ',self.PC_360_url)
        ret = requests.get(self.PC_360_url)
        self.random_time()
        # html = urlopen(panduan_url).read()
        # encode_ret = chardet.detect(html)['encoding']
        encode_ret = chardet.detect(ret.text.encode())['encoding']
        if encode_ret == 'GB2312':
            ret.encoding = 'gbk'
        else:
            ret.encoding = 'utf-8'
        soup_browser = BeautifulSoup(ret.text, 'lxml')
        result_tag = soup_browser.find('div', class_='r-results')
        data_list = result_tag.find_all('div', class_='res-list')
        data_order_num = 0
        for data in data_list:
            if self.domain in data.get_text():
                data_url = data.attrs.get('data-pcurl')
                print('data_url -----------> ',data_url, data_order_num)

            data_order_num += 1


        # if self.fugai_chaxun:
        #     for data in data_list:
        #         search_engine = '4'
        #         sql_two = """update fugai_Linshi_List set paiming_detail='{paiming_detail}', chaxun_status='1' where id = {tid};""".format(
        #             paiming_detail=data['paiming_detail'],tid=str(self.tid),)
        #         database_create_data.operDB(sql_two, 'insert')
        # else:
        #     data_list.append({
        #         'paiming_detail': str_order,
        #         'shoulu': shoulu,
        #         'detail_id': self.detail_id,
        #     })
        #     return data_list


    def random_time(self):
        return sleep(random.randint(1,2))


    def set_data(self, data_list):
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        for data in data_list:
            insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{detail_id}', '{date_time}');""".format(
                order=data['paiming_detail'], shoulu=data['shoulu'], detail_id=data['detail_id'], date_time=date_time)
            database_create_data.operDB(insert_sql, 'insert')
            update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(self.detail_id)
            database_create_data.operDB(update_sql, 'update')


