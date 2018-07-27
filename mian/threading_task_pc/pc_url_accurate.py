from bs4 import BeautifulSoup
from time import sleep
from urllib.request import urlopen
from mian.my_db import database_create_data
import random
import datetime
import chardet
import requests

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
headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}

def shoulu_chaxun(domain,search,huoqu_shoulu_time_stamp=None,shoulu_canshu=None,data_id=None):
    domain = domain.strip()
    zhidao_url = 'http://www.baidu.com/s?wd={domain}'.format(domain=domain)
    shoulu = 0
    kuaizhao_time = ''
    title = ''
    status_code = ''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    sleep(1)
    ret_domain = requests.get(zhidao_url, headers=headers)
    soup_domain = BeautifulSoup(ret_domain.text, 'lxml')
    div_tags = soup_domain.find_all('div', class_='result c-container ')
    if soup_domain.find('div', class_='content_none'):
        status_code = ''
        title=''
        kuaizhao_time = ''
        shoulu = 0
    else:
        div_tags = soup_domain.find_all('div', class_='result c-container ')
        if div_tags and div_tags[0].attrs.get('id'):
            panduan_url = div_tags[0].find('a').attrs['href']
            sleep(1)
            try:
                ret_two = requests.get(panduan_url, headers=headers)
            except Exception as e:
                status_code = ''
                title = ''
                kuaizhao_time = ''
                shoulu = 0
            ret_two_url = ret_two.url
            status_code = ret_two.status_code
            f13_div_tag = div_tags[0].find('div', class_='f13')
            a_tag = f13_div_tag.find('a')
            f13_div = div_tags[0].find('div', class_='f13')
            yuming = f13_div.find('a').get_text()[:-5].split('/')[0]  # 获取域名
            if div_tags[0].find('span', class_='newTimeFactor_before_abs'):
                kuaizhao_time =div_tags[0].find('span', class_='newTimeFactor_before_abs').get_text().strip().replace('-','').replace('年','-').replace('月','-').replace('日','').strip()
            if yuming in domain:
                # html = urlopen(panduan_url).read()
                # encode_ret = chardet.detect(html)['encoding']                       # 测试环境使用 ip被封
                encode_ret = chardet.detect(ret_two.text.encode())['encoding']    # 线上可用
                if encode_ret == 'GB2312':
                    ret_two.encoding = 'gbk'
                else:
                    ret_two.encoding = 'utf-8'
                soup_two = BeautifulSoup(ret_two.text, 'lxml')
                title = soup_two.find('title').get_text().strip().replace('\r\n','')
                if domain in ret_two_url :
                    shoulu = 1

    if shoulu_canshu:
        select_sql = """select id from shoulu_Linshi_List where time_stamp='{time_stamp}' and url='{url}' and search={search}""".format(
            time_stamp=huoqu_shoulu_time_stamp, url=domain, search=search)
        print('select_sql----------------> ',select_sql)
        id_objs = database_create_data.operDB(select_sql, 'select')
        id_obj = id_objs['data'][0][0]
        print('获取的pcid =------> ',id_obj , 'pc端状态码--------------->',status_code)
        sql = """update shoulu_Linshi_List set is_shoulu='{shoulu}', title='{title}', kuaizhao_time='{kuaizhao}', status_code='{status_code}' where id ={id};""".format(
            shoulu=shoulu,
            title=title,
            kuaizhao=kuaizhao_time,
            status_code=status_code,
            id=id_obj
        )
        database_create_data.operDB(sql, 'update')
    return shoulu

# domain = 'http://www.bjhzkq.com'
# search = '1'
# shoulu_canshu = 1
# huoqu_gonggong_time_stamp = 111111
# shoulu_chaxun(domain, search,huoqu_gonggong_time_stamp, shoulu_canshu)

class Baidu_Zhidao_URL_PC():

    def __init__(self, detail_id,keyword, domain):
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
        search = ''
        shoulu = shoulu_chaxun(self.domain,search)
        sleep(1)
        ret = requests.get(self.zhidao_url.format(self.keyword), headers=self.headers)
        self.random_time()
        soup = BeautifulSoup(ret.text, 'lxml')
        # id_tag = soup.find('div', id='content_left')
        # if id_tag:
        div_tags = soup.find_all('div', class_='result c-container ')
        data_list = []
        for div_tag in div_tags:
            div_13 = div_tag.find('div', class_='f13')
            yuming = ''
            if div_13 and div_13.find('a', target="_blank"):
                yuming = div_13.find('a', target="_blank").get_text()[:-4]
                # print('yuming============> ',yuming)
                if yuming in self.domain:
                    rank_num = div_tag.attrs.get('id')  # 排名
                    abstract = div_tag.find('div', class_='c-abstract').get_text()  # 文本内容
                    title_tag = div_tag.find('div', class_='c-tools')['data-tools']
                    dict_title = eval(title_tag)
                    str_title = dict_title['title']  # 标题
                    url_title = dict_title['url']  # 标题链接
                    self.random_time()
                    ret_two = requests.get(url_title, headers=self.headers)
                    if self.domain == ret_two.url:
                        data_list.append({
                            'order':int(rank_num),
                            'shoulu': shoulu,
                            'detail_id':self.detail_id
                        })
                        return data_list

        data_list = [{
            'order': 0,
            'shoulu': 0,
            'detail_id': self.detail_id
        }]
        return data_list


    def random_time(self):
        return sleep(random.randint(1, 2))


    def set_data(self, data_list):
        # print(data_list)
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        for data in data_list:
            insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
                order=data['order'], shoulu=data['shoulu'], detail_id=data['detail_id'], date_time=date_time)
            database_create_data.operDB(insert_sql, 'insert')
            update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(self.detail_id)
            database_create_data.operDB(update_sql, 'update')




# if __name__ == '__main__':
#     keyword = '徐州市交通医院精神科靠谱吗？国家公立“医联体”联盟单位'
#     domain = 'http://www.jianzhijia.com/hyzx/jkjd/79383.html'
#     detail_id = 130
#     Baidu_Zhidao_URL_PC(detail_id, keyword, domain)
