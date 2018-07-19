import requests, random, sqlite3
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet, time
from urllib.request import urlopen

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
headers = {
    'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}





def shoulu_chaxun(domain,search,huoqu_shoulu_time_stamp=None,shoulu_canshu=None):
    domain = domain.strip()
    url = 'https://www.baidu.com/s?wd={domain}'.format(domain=domain)
    # print('url -->', url)
    shoulu = 0
    kuaizhao_time = ''
    title = ''
    sleep(1)
    ret_domain = requests.get(url, headers=headers)
    soup_domain = BeautifulSoup(ret_domain.text, 'lxml')
    if soup_domain.find('div', class_='content_none'):
        # print('无数据')
        pass
    else:
        sleep(1)
        div_tags = soup_domain.find('div', id='content_left').find_all('div', class_='result c-container ')[0]
        f13_div = div_tags.find('div', class_='f13').find('a').get_text()[:-5].split('/')[0]   # 获取域名
        if div_tags.find('span', class_='newTimeFactor_before_abs'):
            kuaizhao_time =div_tags.find('span', class_='newTimeFactor_before_abs').get_text().strip().replace('-','').replace('年','-').replace('月','-').replace('日','').strip()
        if f13_div in domain:
            panduan_url = div_tags.find('a').attrs['href']
            sleep(1)
            ret_two = requests.get(panduan_url, headers=headers)
            ret_two_url = ret_two.url
            sleep(1)
            # html = urlopen(panduan_url).read()
            # encode_ret = chardet.detect(html)['encoding']                       # 测试环境使用 ip被封
            encode_ret = chardet.detect(ret_two.text.encode())['encoding']    # 线上可用
            if encode_ret == 'GB2312':
                ret_two.encoding = 'gbk'
            else:
                ret_two.encoding = 'utf-8'
            soup_two = BeautifulSoup(ret_two.text, 'lxml')
            title = soup_two.find('title').get_text().strip().replace('\r\n','')
            print('ret_two_url --------- >',ret_two_url,'domain ----------->',domain)
            if domain == ret_two_url :
                shoulu = 1
        if shoulu_canshu:
            conn = sqlite3.connect('../my_db/my_sqlite.db')
            cursor = conn.cursor()
            data = ''
            if shoulu == 1:
                data = (domain, shoulu, huoqu_shoulu_time_stamp,title,search,kuaizhao_time)
            else:
                data = (domain, shoulu, huoqu_shoulu_time_stamp,title,search,kuaizhao_time)
            sql = """insert into shoulu_Linshi_List (url, is_shoulu, time_stamp, title, search, kuaizhao_time) values {data};""".format(data=data)
            # print(sql)
            cursor.execute(sql)
            conn.commit()
            conn.close()
    return shoulu

# url_list = [
# 'http://www.iiijk.com/cjxw/04-74547.html',
# 'http://news.100yiyao.com/detail/193538290.html          ',
# 'http://news.qiuyi.cn/html/2017/fuke_1205/63968.html     ',
# 'http://at.025ct.com/dt/2017/1204/514781.html            ',
# 'http://www.jianzhijia.com/hyzx/jkjd/79379.html          ',
# 'http://news.39.net/a/171204/5901183.html                ',
# 'http://news.39.net/a/171204/5901194.html                ',
# 'http://news.360xh.com/201712/04/37416.html              ',
# 'http://www.iiijk.com/cjxw/04-74550.html                 ',
# 'http://www.jianzhijia.com/hyzx/jkjd/79381.html          ',
# 'http://news.qiuyi.cn/html/2017/zhengxing_1204/63922.html',
# 'http://news.39.net/a/171204/5902419.html                ',
# 'http://www.jianzhijia.com/hyzx/jkjd/79383.html          ',
# 'http://news.360xh.com/201712/04/37402.html              ',
# 'http://www.sohu.com/a/208330800_544906                  ',
# 'http://www.iiijk.com/cjxw/04-74552.html                 ',
# 'http://www.iiijk.com/cjxw/04-74551.html                 ',
# 'http://focus.smxe.cn/20171204/148402.shtml              ',
# 'http://news.360xh.com/201712/04/37408.html              ',
# 'http://news.39.net/a/171204/5902423.html                ',
# 'http://www.jianzhijia.com/hyzx/jkjd/79385.html          ',
# 'http://news.360xh.com/201712/04/37409.html              ',
# 'http://news.360xh.com/201712/04/37410.html              ',
# 'http://news.100yiyao.com/detail/193538295.html          ',
# 'http://www.jianzhijia.com/hyzx/jkjd/79387.html          ',
# 'http://news.100yiyao.com/detail/193538308.html          ',
# 'http://news.360xh.com/201712/04/37411.html              ',
# 'http://news.39.net/a/171204/5902507.html                ',
# 'http://news.360xh.com/201712/04/37412.html              ',
# 'http://www.jianzhijia.com/hyzx/jkjd/79388.html          ',
# 'http://news.39.net/a/171204/5902519.html                ',
# 'http://news.360xh.com/201712/04/37414.html              ',
# 'http://www.jianzhijia.com/hyzx/jkjd/79389.html          ',
# 'http://news.cx368.com/news/gd/2017/1204/69128.html      ',]

# shoulu_canshu = 1
# search = '1'
# huoqu_shoulu_time_stamp = '测试'
# for url in url_list:
#
#     url = 'http://www.renai120.com'
#     shoulu_chaxun(url,search,huoqu_shoulu_time_stamp,shoulu_canshu)



class Baidu_Zhidao_URL_PC():

    def __init__(self, detail_id, keyword, domain):
        self.keyword = keyword
        self.domain = domain
        self.detail_id = detail_id
        self.headers = {
            'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}
        self.zhidao_url = 'https://www.baidu.com/s?wd={keyword}'.format(keyword='{}')
        data_list = self.get_keywords()
        self.set_data(data_list)

    def get_keywords(self):
        # print('请求链接--',self.zhidao_url.format(self.keyword))
        # 调用查询收录
        shoulu = shoulu_chaxun(self.domain, shoulu_canshu=1)
        ret = requests.get(self.zhidao_url.format(self.keyword), headers=self.headers)
        self.random_time()
        soup = BeautifulSoup(ret.text, 'lxml')
        id_tag = soup.find('div', id='content_left')
        div_tags = id_tag.find_all('div', class_='result c-container ')
        data_list = []
        for div_tag in div_tags:
            div_13 = div_tag.find('div', class_='f13')
            yuming = div_13.find('a', target="_blank").get_text()[:-4]
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

            # if yuming:
            #     yuming_tag = yuming.get_text()[:-4]
            #     if yuming_tag in self.domain:
            #         ret = requests.get(url_title)
            #         pipei_url = ret.url
            #         print('==============>',pipei_url,self.domain)
            #         if pipei_url == self.domain:
            #             # print('进入if')
            #             if rank_num != 0:
            #                 data_list.append({
            #                     'str_title':str_title,
            #                     'page_div':rank_num,
            #                     'url_title':url_title,
            #                     'shifoushoulu':1,
            #                 })
            #
            #         else:
            #             # print('进入 else-----------')
            #             ret = requests.get(self.zhidao_url.format(self.domain))
            #             self.random_time()
            #             soup = BeautifulSoup(ret.text, 'lxml')
            #             self.random_time()
            #             id_tag = soup.find('div', id='content_left')
            #             if id_tag:
            #                 div_tags = id_tag.find_all('div', class_='result c-container ')
            #                 # print(self.zhidao_url.format(self.domain))
            #                 for div_tag in div_tags:
            #                     dict_data = eval(div_tag['data-click'])
            #                     str_title = dict_title['title']  # 标题
            #                     url_titlse = dict_title['url']  # 标题链接
            #
                    return data_list
        return 'none'

    def random_time(self):
        return sleep(random.randint(1, 2))

    def set_data(self, data_list):
        if data_list == 'none':
            conn = sqlite3.connect('../my_db/my_sqlite.db')
            cursor = conn.cursor()
            order = ''
            shoulu = 0
            detail_id = self.detail_id
            date_time = datetime.datetime.today().strftime('%Y-%m-%d')
            sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
                order=order, shoulu=shoulu, detail_id=detail_id, date_time=date_time)
            cursor = conn.cursor()
            cursor.execute(sql)
        else:
            # print('thread_pcurl ------------- > ', data_list)
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


# if __name__ == '__main__':
#     keyword = '北京男科哪家好'
#     domain = 'http://yyk.39.net/beijing/hospitals/nanke/'
#     detail_id = 22
#     Baidu_Zhidao_URL_PC(detail_id, keyword, domain)
