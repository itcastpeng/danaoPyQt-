import requests, random
from bs4 import BeautifulSoup
import datetime
from time import sleep
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
lock_file = './my_db/my_sqlite3.lock'
db_file =  './my_db/my_sqlite.db'
class Baidu_Zhidao_yuming_mobile(object):


    def __init__(self,tid, yinqing, keyword, domain, detail_id=None, huoqu_gonggong_time_stamp=None,fugai_chaxun=None):
        print('进入爬虫 ---------- 移动端')
        self.tid = tid
        self.keyword = keyword
        self.domain = domain
        self.detail_id = detail_id
        self.fugai_chaxun = fugai_chaxun
        self.yinqing = yinqing
        self.huoqu_gonggong_time_stamp = huoqu_gonggong_time_stamp
        self.zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'
        self.headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        if self.fugai_chaxun:
            self.get_keyword()
        else:
            # print('进入 手机端 ')
            data_list = self.get_keyword()
            self.set_data(data_list)


    def get_keyword(self):
        zhidao_url = self.zhidao_url.format(self.keyword)
        # print('请求链接 ------------ >',zhidao_url)
        ret = requests.get(zhidao_url)
        self.random_time()
        soup_browser = BeautifulSoup(ret.text, 'lxml')
        # results = soup_browser.find('div', id='results').find_all('div', class_='result c-result')
        content_list_order = []
        title = ''
        div_tags = soup_browser.find_all('div', class_='result c-result')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        div_tags = soup_browser.find_all('div', class_='result c-result c-clk-recommend')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        data_list = []
        order_list = []
        shoulu = 0
        str_order = 0
        status_code = ''
        for data in content_list_order:
            if data['data-log']:
                dict_data = eval(data['data-log'])
                url_title = dict_data['mu']                    # 标题链接
                if url_title:
                    order = dict_data['order']                     # 排名
                    pipei_tiaojian = data.get_text()
                    if self.domain in pipei_tiaojian:
                        order_list.append(int(order))
                        str_order = ",".join(str(i)for i in order_list)
                        shoulu = 1
                        try:
                            ret_two = requests.get(url_title, headers=self.headers)
                            if ret_two:
                                soup_two = BeautifulSoup(ret_two.text, 'lxml')
                                if soup_two.find('title'):
                                    title = soup_two.find('title').get_text()
                                    status_code = ret_two.status_code
                                    if self.fugai_chaxun:
                                        sql = """insert into fugai_Linshi_List (keyword, paiming_detail, search_engine, title, title_url, sousuo_guize, time_stamp, tid, status_code) values ('{keyword}', '{paiming_detail}', '{search_engine}', '{title}', '{title_url}', '{sousuo_guize}', '{time_stamp}','{tid}', '{status_code}');""".format(
                                            keyword=self.keyword, paiming_detail=order, search_engine=self.yinqing,
                                            title=title, title_url=ret_two.url, sousuo_guize=self.domain,
                                            time_stamp=None, status_code=status_code, tid=str(self.tid))
                                        database_create_data.operDB(sql, lock_file, db_file, 'insert')
                        except Exception as e:
                            pass
        data_list.append({
            'paiming_detail': str_order,
            'shoulu': shoulu,
            'detail_id': self.detail_id
        })
        if self.fugai_chaxun:
            print('----------------------------------修改',data_list)
            for data in data_list:
                print('data----------> ',data)
                sql_two = """update fugai_Linshi_List set paiming_detail='{paiming_detail}', chaxun_status='1', is_zhixing='{is_zhixing}' where id = {tid};""".format(
                    paiming_detail=data['paiming_detail'],tid=str(self.tid),is_zhixing='1')
                print('sql_two-----------> ',sql_two)
                database_create_data.operDB(sql_two, lock_file, db_file, 'insert')
        else:
            return data_list
        #     data_list.append({
        #         'paiming_detail': str_order,
        #         'shoulu': shoulu,
        #         'detail_id': self.detail_id,
                # 'title_url': url_title,
                # 'yiniqng': self.yinqing,
                # 'title': title,
                # 'time_stamp': self.huoqu_gonggong_time_stamp,
                # 'sousuo_guize': self.domain,
                # 'keyword': self.keyword,
                # 'status_code':status_code
            # })


    def random_time(self):
        return sleep(random.randint(1,2))


    def set_data(self, data_list):
        # if self.fugai_chaxun:
        #     for data in data_list:
        #         search_engine = '4'
        #         sql_two = """update fugai_Linshi_List set paiming_detail='{paiming_detail}', title='{title}', title_url='{title_url}', chaxun_status='1',  status_code={status_code} where id = {tid};""".format(
        #             paiming_detail=data['paiming_detail'], title=data['title'], title_url=data['title_url'],
        #             tid=str(self.tid),
        #             status_code=data['status_code']
        #             )
        #         # print(sql_two)
        #         database_create_data.operDB(sql_two, 'insert')
        # else:
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        for data in data_list:
            insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{detail_id}', '{date_time}');""".format(
                order=data['paiming_detail'], shoulu=data['shoulu'], detail_id=data['detail_id'], date_time=date_time)
            database_create_data.operDB(insert_sql, lock_file, db_file, 'insert')
            update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(self.detail_id)
            database_create_data.operDB(update_sql, lock_file, db_file, 'update')
                # print('mobile ==fugai')


# if __name__ == '__main__':
#     keyword = '北京男科哪家好'
#     domain = '全的北京男科医院排行榜,供您查询北京男科医院排名,告诉您北京哪家'
#     detail_id = 22
#     yinqing = 1
#     tid = 1
#     Baidu_Zhidao_yuming_mobile(tid,yinqing,keyword,domain,detail_id,fugai_chaxun=1)


