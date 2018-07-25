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


class Baidu_Zhidao_yuming_pc():


    def __init__(self,tid, yinqing, keyword, domain, detail_id=None,huoqu_gonggong_time_stamp=None,fugai_chaxun=None):
        print('----------------------》',detail_id)
        self.tid = tid
        self.keyword = keyword
        self.domain = domain
        self.detail_id = detail_id
        self.yinqing = yinqing
        self.fugai_chaxun = fugai_chaxun
        self.huoqu_gonggong_time_stamp = huoqu_gonggong_time_stamp


        self.headers = {
            'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)],
        }
        self.zhidao_url = 'https://www.baidu.com/s?wd={keyword}'.format(keyword='{}')
        # print('进入 pc 端')
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
            rank_num = div_tag.attrs.get('id')
            if not rank_num:
                continue
            tiaojian_chaxun = div_tag.get_text()
            panduan_url = div_tag.find('h3',class_='t').find('a').attrs['href']
            # print('domainm =============> ',self.domain)
            if self.domain in tiaojian_chaxun:
                ret_two = requests.get(panduan_url, headers=self.headers)
                ret_two_url = ret_two.url
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
                    if self.fugai_chaxun:
                        search_engine = '1'
                        sql = """insert into fugai_Linshi_List (keyword, paiming_detail, search_engine, title, title_url, sousuo_guize, time_stamp, tid) values ('{keyword}', '{paiming_detail}', '{search_engine}', '{title}', '{title_url}', '{sousuo_guize}', '{time_stamp}','{tid}');""".format(
                            keyword=self.keyword, paiming_detail=rank_num, search_engine=search_engine,
                            title=title, title_url=ret_two_url, sousuo_guize=self.domain,
                            time_stamp=None,tid=str(self.tid))
                        database_create_data.operDB(sql, 'insert')

        # print('order-----> ',str_order, shoulu,detail_id,ret_two_url,yinqing,title,self.huoqu_gonggong_time_stamp)
        data_list.append({
            'paiming_detail': str_order,
            'shoulu': shoulu,
            'detail_id': self.detail_id,
            'title_url': ret_two_url,
            'yiniqng': self.yinqing,
            'title': title,
            'time_stamp':self.huoqu_gonggong_time_stamp,
            'sousuo_guize':self.domain,
            'keyword':self.keyword
        })
        return data_list


    def random_time(self):
        return sleep(random.randint(1,2))


    def set_data(self,data_list):
        if self.fugai_chaxun:
            for data in data_list:
                search_engine = '1'
                sql_two = """update fugai_Linshi_List set paiming_detail='{paiming_detail}', title='{title}', title_url='{title_url}', chaxun_status='1' where id = {tid};""".format(
                    paiming_detail=data['paiming_detail'],title=data['title'],title_url=data['title_url'],tid=str(self.tid))
                # print(sql_two)
                database_create_data.operDB(sql_two, 'insert')
        else:
            date_time = datetime.datetime.today().strftime('%Y-%m-%d')
            for data in data_list:
                insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{detail_id}', '{date_time}');""".format(
                    order=data['paiming_detail'],shoulu=data['shoulu'],detail_id=data['detail_id'],date_time=date_time)
                database_create_data.operDB(insert_sql, 'insert')

                update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(self.detail_id)
                database_create_data.operDB(update_sql, 'update')
                print('pc --- 覆盖', self.detail_id)



# if __name__ == '__main__':
#     keyword = '合众康桥'
#     domain = '合众康桥'
#     detail_id = 22
#     yinqing = '1'
#     # def __init__(self, yinqing, keyword, domain, detail_id=None, huoqu_gonggong_time_stamp=None, fugai_chaxun=None):
#     Baidu_Zhidao_yuming_pc(yinqing,keyword,domain,detail_id,fugai_chaxun=1)

