import requests, random, sqlite3
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet, time
from urllib.request import urlopen
from mian.threading_task_pc import database_create_data
def shoulu_chaxun(domain,search,huoqu_shoulu_time_stamp=None,shoulu_canshu=None):
    domain = domain.strip()
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'.format(domain)
    # print(url)
    ret = requests.get(domain, headers=headers)
    soup = BeautifulSoup(ret.text, 'lxml')
    data_list = []
    title = ''
    kuaizhao_time = ''
    shoulu = 0
    if '抱歉，没有找到' in soup.find('div', id='results').find('div', class_='c-container').get_text():
        data_list.append({'shoulu':shoulu, 'url':'none'})
        # print('无 数 据')
    else:
        shoulu = 1
        sleep(1)
        div_tags = soup.find('div', class_='results').find_all('div', class_='result c-result')[0]
        dict_data = eval(div_tags['data-log'])
        pipri_url = dict_data['mu']
        # print(pipri_url)


        data_list.append({'url':pipri_url,'shoulu':shoulu})
        if 'http' or 'https' in pipri_url and pipri_url:
            # print('==================',domain)
            ret_two = ''
            try:
                ret_two = requests.get(pipri_url, headers=headers)
            except Exception as e:
                pass
            sleep(1)
            # html = urlopen(dict_data['mu']).read()
            # html = urlopen(domain).read()
            # encode_ret = chardet.detect(html)['encoding']
            if ret_two:
                encode_ret = chardet.detect(ret_two.text.encode())['encoding']
                if encode_ret == 'GB2312':
                    ret_two.encoding = 'gbk'
                else:
                    ret_two.encoding = 'utf-8'
                soup_two = BeautifulSoup(ret_two.text, 'lxml')
                # print('编码格式 -——----> ', ret.encoding)
                if soup_two.find('h1'):
                    if len(soup_two.find('h1').get_text()) > 5:
                        title = soup_two.find('h1').get_text().strip().replace('\r\n','')
                if soup_two.find('h2'):
                    if len(soup_two.find('h2').get_text()) > 5:
                        title = soup_two.find('h2').get_text().strip().replace('\r\n','')
            # print(title)
    if shoulu_canshu:
        data = ''
        if shoulu == 1:
            data = (domain,shoulu,huoqu_shoulu_time_stamp,title,search,kuaizhao_time)
        else:
            data = (domain, shoulu, huoqu_shoulu_time_stamp,title,search,kuaizhao_time)
        sql = """insert into shoulu_Linshi_List (url, is_shoulu, time_stamp, title, search,kuaizhao_time) values {data};""".format(data=data)
        # print(sql)
        database_create_data.func(sql)

    return data_list
#
url_list = [
'http://www.iiijk.com/cjxw/04-74547.html',
'http://news.100yiyao.com/detail/193538290.html          ',
'http://news.qiuyi.cn/html/2017/fuke_1205/63968.html     ',
'http://at.025ct.com/dt/2017/1204/514781.html            ',
'http://www.jianzhijia.com/hyzx/jkjd/79379.html          ',
'http://news.39.net/a/171204/5901183.html                ',
'http://news.39.net/a/171204/5901194.html                ',
'http://news.360xh.com/201712/04/37416.html              ',
'http://www.iiijk.com/cjxw/04-74550.html                 ',
'http://www.jianzhijia.com/hyzx/jkjd/79381.html          ',
'http://news.qiuyi.cn/html/2017/zhengxing_1204/63922.html',
'http://news.39.net/a/171204/5902419.html                ',
'http://www.jianzhijia.com/hyzx/jkjd/79383.html          ',
'http://news.360xh.com/201712/04/37402.html              ',
'http://www.sohu.com/a/208330800_544906                  ',
'http://www.iiijk.com/cjxw/04-74552.html                 ',
'http://www.iiijk.com/cjxw/04-74551.html                 ',
'http://focus.smxe.cn/20171204/148402.shtml              ',
'http://news.360xh.com/201712/04/37408.html              ',
'http://news.39.net/a/171204/5902423.html                ',
'http://www.jianzhijia.com/hyzx/jkjd/79385.html          ',
'http://news.360xh.com/201712/04/37409.html              ',
'http://news.360xh.com/201712/04/37410.html              ',
'http://news.100yiyao.com/detail/193538295.html          ',
'http://www.jianzhijia.com/hyzx/jkjd/79387.html          ',
'http://news.100yiyao.com/detail/193538308.html          ',
'http://news.360xh.com/201712/04/37411.html              ',
'http://news.39.net/a/171204/5902507.html                ',
'http://news.360xh.com/201712/04/37412.html              ',
'http://www.jianzhijia.com/hyzx/jkjd/79388.html          ',
'http://news.39.net/a/171204/5902519.html                ',
'http://news.360xh.com/201712/04/37414.html              ',
'http://www.jianzhijia.com/hyzx/jkjd/79389.html          ',
'http://news.cx368.com/news/gd/2017/1204/69128.html      ',]
# for url in url_list:
#     huoqu_shoulu_time_stamp = '测试mobiel'
#     shoulu_canshu = 1
#     search = '4'
#     shoulu_chaxun(url,search,huoqu_shoulu_time_stamp,shoulu_canshu)

class Baidu_Zhidao_URL_MOBILE(object):

    def __init__(self,detail_id, keyword, domain):
        self.keyword = keyword
        self.detail_id = detail_id
        self.domain = domain
        self.zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'

        data_list = self.get_keywords()
        print('data_list============> ',data_list)
        self.set_data(data_list)

    def get_keywords(self):
        self.random_time()
        # print('查看收录链接 ---------- > ', self.zhidao_url.format(self.domain))
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        url = self.zhidao_url.format(self.domain)
        search = ''
        # print(url)
        data_list = shoulu_chaxun(url,search)
        # 查询关键词 匹配链接
        self.random_time()
        url = self.zhidao_url.format(self.keyword)
        print('搜索关键词 链接--------> ', url)
        ret_two = requests.get(url, headers=headers)
        # print(url)
        soup_two = BeautifulSoup(ret_two.text, 'lxml')
        content_list_order = []
        div_tags = soup_two.find_all('div', class_='result c-result')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        div_tags = soup_two.find_all('div', class_='result c-result c-clk-recommend')
        for div_tag in div_tags:
            content_list_order.append(div_tag)

        # 遍历已收录链接 匹配url
        data_list_content = []
        for data_url in data_list:
            if data_url['url']:
                for content_order in content_list_order:
                    str_data = eval(content_order['data-log'])
                    if str_data['mu']:
                        if str_data['mu'] == data_url['url']:
                            print(str_data['mu'],' ==================== ',data_url['url'])
                            paiming_order = str_data['order']

                            data_list_content.append({
                                'order': int(paiming_order),
                                'shoulu': data_url['shoulu'],
                                'detail_id': self.detail_id
                            })
                            print('有')
                            return data_list_content
        data_list_content = [{
            'order': 0,
            'shoulu': 0,
            'detail_id': self.detail_id
        }]

        print('无')
        return data_list_content



    def random_time(self):
        return sleep(random.randint(1, 2))


    def set_data(self, data_list):
        print('thread_mobileurl ------------- > ', data_list)
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        for data in data_list:
            sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
                order=data['order'], shoulu=data['shoulu'], detail_id=data['detail_id'], date_time=date_time)
            database_create_data.func(sql)


# if __name__ == '__main__':
#     keyword = '沈阳中泰肛肠医院怎么样？患者都在说好！'
#     domain = 'http://news.39.net/a/171204/5900289.html'
#     # domain = 'http://m-mip.39.net/news/mipso_5901183.html'
#     # domain = 'https://tieba.baidu.com/p/1382203163?red_tag=2092386831'
#     detail_id = 22
#     Baidu_Zhidao_URL_MOBILE(detail_id, keyword, domain)
