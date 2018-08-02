import requests, random
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet
from mian.my_db import database_create_data

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


# lock_file = 'C:/pycharm zh/danaoPyQt/mian/my_db/my_sqlite3.lock'
# db_file =  'C:/pycharm zh/danaoPyQt/mian/my_db/my_sqlite.db'

class Baidu_Zhidao_yuming_pc():
    def __init__(self,tid, yinqing, keyword, domain, detail_id=None,huoqu_fugai_time_stamp=None,fugai_canshu=None):
        self.tid = tid
        self.keyword = keyword
        self.domain = domain
        self.detail_id = detail_id
        self.yinqing = yinqing
        self.fugai_canshu = fugai_canshu
        self.huoqu_fugai_time_stamp = huoqu_fugai_time_stamp
        self.headers = {
            'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)],}
        self.zhidao_url = 'https://www.baidu.com/s?wd={keyword}'.format(keyword='{}')
        if self.fugai_canshu:
            self.get_keywords()
        else:
            data_list = self.get_keywords()
            self.set_data(data_list)

    def get_keywords(self):
        ret = requests.get(self.zhidao_url.format(self.keyword) ,headers=self.headers)
        soup = BeautifulSoup(ret.text, 'lxml')
        div_tags = soup.find_all('div', class_='result c-container ')
        data_list = []
        ret_two_url = ''
        title = ''
        shoulu = 0
        order_list = []
        str_order = 0
        status_code = ''
        for div_tag in div_tags:
            rank_num = div_tag.attrs.get('id')
            if not rank_num:
                continue
            tiaojian_chaxun = div_tag.get_text()
            panduan_url = div_tag.find('h3',class_='t').find('a').attrs['href']
            if self.domain in tiaojian_chaxun:
                ret_two = requests.get(panduan_url, headers=self.headers)
                ret_two_url = ret_two.url
                status_code = ret_two.status_code
                # html = urlopen(panduan_url).read()
                # encode_ret = chardet.detect(html)['encoding']
                encode_ret = chardet.detect(ret_two.text.encode())['encoding']
                if encode_ret == 'GB2312':
                    ret_two.encoding = 'gbk'
                else:
                    ret_two.encoding = 'utf-8'
                soup_two = BeautifulSoup(ret_two.text, 'lxml')
                if soup_two.find('title'):
                    if len(soup_two.find('title').get_text()) > 5 and soup_two.find('title'):
                        title = soup_two.find('title').get_text()
                        order_list.append(int(rank_num))
                        str_order = ",".join(str(i) for i in order_list)
                        shoulu = 1
                        if self.fugai_canshu:
                            insert_sql = """insert into fugai_Linshi_List (keyword, paiming_detail, search_engine, title, title_url, sousuo_guize, time_stamp, status_code, tid) values ('{keyword}', '{paiming_detail}', '{search_engine}', '{title}', '{title_url}', '{sousuo_guize}', '{time_stamp}','{status_code}','{tid}');""".format(
                                keyword=self.keyword, paiming_detail=rank_num, search_engine=self.yinqing,
                                title=title, title_url=ret_two_url, sousuo_guize=self.domain,
                                time_stamp=None,status_code=status_code,tid=str(self.tid))
                            database_create_data.operDB(insert_sql, 'insert')
        if self.fugai_canshu:
            sql_two = """update fugai_Linshi_List set paiming_detail='{paiming_detail}', chaxun_status='1', is_zhixing='{is_zhixing}' where id = '{id}';""".format(
                paiming_detail=str_order, is_zhixing='1', id=self.tid)
            database_create_data.operDB(sql_two, 'update')
        else:
            data_list.append({
                'paiming_detail': str_order,
                'shoulu': shoulu,
                'detail_id': self.detail_id,
            })
            return data_list


    def set_data(self,data_list):
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        for data in data_list:
            insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{detail_id}', '{date_time}');""".format(
                order=data['paiming_detail'],shoulu=data['shoulu'],detail_id=data['detail_id'],date_time=date_time)
            database_create_data.operDB(insert_sql, 'insert')
            update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(self.detail_id)
            database_create_data.operDB(update_sql, 'update')


