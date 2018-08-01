import requests, random
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet
from mian.my_db import database_create_data

lock_file = './my_db/my_sqlite3.lock'
db_file =  './my_db/my_sqlite.db'
def shoulu_chaxun(domain, search, huoqu_shoulu_time_stamp=None, shoulu_canshu=None, data_id=None):
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'.format(domain)
    ret = ''
    if shoulu_canshu:
        ret = requests.get(zhidao_url, headers=headers)
    else:
        ret = requests.get(domain, headers=headers)
    soup = BeautifulSoup(ret.text, 'lxml')
    data_list = []
    title = ''
    kuaizhao_time = ''
    shoulu = 0
    status_code = ''
    if '抱歉，没有找到' in soup.find('div', class_='c-container').get_text():
        data_list.append({'shoulu': shoulu, 'url': 'none'})
        title = ''
        kuaizhao_time = ''
        shoulu = 0
        status_code = ''
    else:
        shoulu = 1
        div_tags = ''
        if soup.find_all('div', class_='result c-result')[0].attrs.get('order') == '1':
            div_tags = soup.find_all('div', class_='result c-result')
        else:
            div_tags = soup.find_all('div', class_='result c-result c-clk-recommend')
        dict_data = eval(div_tags[0]['data-log'])
        pipei_url = dict_data['mu']
        data_list.append({'url':pipei_url,'shoulu':shoulu})
        if 'http' or 'https' in pipei_url and pipei_url:
            ret_two = ''
            try:
                ret_two = requests.get(pipei_url, headers=headers)
            except Exception as e:
                pass
            # html = urlopen(dict_data['mu']).read()
            # html = urlopen(domain).read()
            # encode_ret = chardet.detect(html)['encoding']
            if ret_two:
                encode_ret = chardet.detect(ret_two.text.encode())['encoding']
                if encode_ret == 'GB2312':
                    ret_two.encoding = 'gbk'
                else:
                    ret_two.encoding = 'utf-8'
                status_code = ret_two.status_code
                soup_two = BeautifulSoup(ret_two.text, 'lxml')
                # print('编码格式 -——----> ', ret.encoding)
                if soup_two.find('title'):
                    title = soup_two.find_all('title')[0].get_text().strip().replace('\r\n','')
                elif soup_two.find('h1'):
                    if len(soup_two.find('h1').get_text()) > 5:
                        title = soup_two.find('h1').get_text().strip().replace('\r\n','')
                else:
                    if len(soup_two.find('h2').get_text()) > 5:
                        title = soup_two.find('h2').get_text().strip().replace('\r\n','')
    if shoulu_canshu:
        select_sql = """select id from shoulu_Linshi_List where time_stamp='{time_stamp}' and url='{url}' and search={search}""".format(
            time_stamp=huoqu_shoulu_time_stamp, url=domain, search=search)
        id_objs = database_create_data.operDB(select_sql, lock_file, db_file, 'select')
        id_obj = id_objs['data'][0][0]
        update_sql = """update shoulu_Linshi_List set is_shoulu='{shoulu}', title='{title}', kuaizhao_time='{kuaizhao}', status_code='{status_code}', is_zhixing={is_zhixing} where id={id};""".format(
            shoulu=shoulu,
            title=title,
            kuaizhao=kuaizhao_time,
            status_code=status_code,
            id=id_obj,
            is_zhixing='1'
        )
        database_create_data.operDB(update_sql, lock_file, db_file, 'update')
    else:
        return data_list

class Baidu_Zhidao_URL_MOBILE(object):

    def __init__(self,detail_id, keyword, domain):
        self.keyword = keyword
        self.detail_id = detail_id
        self.domain = domain
        self.zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'
        data_list = self.get_keywords()
        self.set_data(data_list)

    def get_keywords(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        url = self.zhidao_url.format(self.domain)
        search = ''
        data_list = shoulu_chaxun(url,search)
        url = self.zhidao_url.format(self.keyword)
        ret_two = requests.get(url, headers=headers)
        soup_two = BeautifulSoup(ret_two.text, 'lxml')
        content_list_order = []
        div_tags = soup_two.find_all('div', class_='result c-result')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        div_tags = soup_two.find_all('div', class_='result c-result c-clk-recommend')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        data_list_content = []
        for data_url in data_list:
            if data_url['url']:
                for content_order in content_list_order:
                    str_data = eval(content_order['data-log'])
                    if str_data['mu']:
                        if str_data['mu'] == data_url['url']:
                            paiming_order = str_data['order']
                            data_list_content.append({
                                'order': int(paiming_order),
                                'shoulu': data_url['shoulu'],
                                'detail_id': self.detail_id
                            })
                            return data_list_content
        data_list_content = [{
            'order': 0,
            'shoulu': 0,
            'detail_id': self.detail_id
        }]
        return data_list_content

    def set_data(self, data_list):
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        for data in data_list:
            insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
                order=data['order'], shoulu=data['shoulu'], detail_id=data['detail_id'], date_time=date_time)
            database_create_data.operDB(insert_sql, lock_file, db_file, 'insert')
            update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(self.detail_id)
            database_create_data.operDB(update_sql, lock_file, db_file, 'update')
