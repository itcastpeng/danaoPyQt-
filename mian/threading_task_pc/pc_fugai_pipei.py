import requests, random, sqlite3
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet, time
from urllib.request import urlopen
from mian.threading_task_pc import database_create_data

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


    def __init__(self,yinqing,detail_id, keyword, domain):
        self.keyword = keyword
        self.domain = domain
        self.detail_id = detail_id
        self.yinqing = yinqing
        self.headers = {
            'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)],
        }
        self.zhidao_url = 'https://www.baidu.com/s?wd={keyword}'.format(keyword='{}')
        data_list = self.get_keywords()
        self.set_data(data_list)


    def get_keywords(self):
        self.random_time()
        # print('请求的链接-------------> ',self.zhidao_url.format(self.keyword))
        ret = requests.get(self.zhidao_url.format(self.keyword) ,headers=self.headers)
        soup = BeautifulSoup(ret.text, 'lxml')
        div_tags = soup.find_all('div', class_='result c-container ')
        data_list = []
        ret_two_url = ''
        title = ''
        shoulu = 0
        order_list = []
        str_order = 0
        for div_tag in div_tags:
            self.random_time()
            rank_num = div_tag.attrs.get('id')
            if not rank_num:
                continue
            tiaojian_chaxun = div_tag.get_text()
            # print(tiaojian_chaxun)
            panduan_url = div_tag.find('h3',class_='t').find('a').attrs['href']

            if self.domain in tiaojian_chaxun:
                ret_two = requests.get(panduan_url, headers=self.headers)
                ret_two_url = ret_two.url
                sleep(2)
                # html = urlopen(panduan_url).read()
                # encode_ret = chardet.detect(html)['encoding']
                encode_ret = chardet.detect(ret_two.text.encode())['encoding']
                if encode_ret == 'GB2312':
                    ret_two.encoding = 'gbk'
                else:
                    ret_two.encoding = 'utf-8'
                soup_two = BeautifulSoup(ret_two.text, 'lxml')
                if len(soup_two.find('title').get_text()) > 5 and soup_two.find('title').get_text():
                    title = soup_two.find('title').get_text()
                    order_list.append(int(rank_num))
                    str_order = ",".join(str(i) for i in order_list)
                    shoulu = 1
        data_list.append({
            'order': str_order,
            'shoulu': shoulu,
            'detail_id': self.detail_id,
            'url': ret_two_url,
            'yiniqng': self.yinqing,
            'title': title
        })

        return data_list


    def random_time(self):
        return sleep(random.randint(1,2))


    def set_data(self,data_list):
        print('data_list--------------------> ',data_list)
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        for data in data_list:
            sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
                order=data['order'],shoulu=data['shoulu'],detail_id=data['detail_id'],date_time=date_time)
            database_create_data.operDB(sql, 'insert')


# if __name__ == '__main__':
#     keyword = '合众康桥'
#     domain = '合众康桥'
#     detail_id = 22
#     yinqing = '1'
#     Baidu_Zhidao_yuming_pc(yinqing,detail_id, keyword, domain)
#
