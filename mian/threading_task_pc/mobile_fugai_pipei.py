import requests, random, sqlite3
from bs4 import BeautifulSoup
import datetime
from time import sleep

class Baidu_Zhidao_yuming_mobile(object):


    def __init__(self,detail_id, keyword, domain):
        self.keyword = keyword
        self.domain = domain
        self.detail_id = detail_id
        self.zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'
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


        div_tags = soup_browser.find_all('div', class_='result c-result')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        div_tags = soup_browser.find_all('div', class_='result c-result c-clk-recommend')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        data_list = []
        for data in content_list_order:
            try:
                if data['data-log']:
                    dict_data = eval(data['data-log'])
                    url_title = dict_data['mu']                    # 标题链接
                    if url_title:
                        order = dict_data['order']                     # 排名
                        pipei_tiaojian = data.get_text()
                        if self.domain in pipei_tiaojian:
                            data_list.append({
                                'order':int(order),
                                'shoulu':1,
                                'detail_id':self.detail_id
                            })
                            return data_list
            except Exception as e :
                print(datetime.date.today())
        return 'none'

    def random_time(self):
        return sleep(random.randint(1,2))


    def set_data(self, data_list):
        if data_list == 'none':
            conn = sqlite3.connect('../my_db/my_sqlite.db')
            cursor = conn.cursor()
            order = 0
            shoulu = 0
            detail_id = self.detail_id
            date_time = datetime.datetime.today().strftime('%Y-%m-%d')
            sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
                order=order, shoulu=shoulu, detail_id=detail_id, date_time=date_time)
            cursor = conn.cursor()
            cursor.execute(sql)

        else:
            # print('thread_mobilemohupipei-----------> ',data_list)
            conn = sqlite3.connect('../my_db/my_sqlite.db')
            cursor = conn.cursor()
            date_time = datetime.datetime.today().strftime('%Y-%m-%d')
            for data in data_list:
                sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
                    order=data['order'], shoulu=data['shoulu'], detail_id=data['detail_id'], date_time=date_time)
                # print(sql)
                cursor = conn.cursor()
                cursor.execute(sql)

        conn.commit()
        conn.close()

if __name__ == '__main__':
    keyword = '北京男科哪家好'
    domain = '病会有死精，无精症，患者是睾丸炎，前列腺炎等症状，你又想知道具体的原因，你就得去'
    detail_id = 22
    Baidu_Zhidao_yuming_mobile(detail_id, keyword, domain)


