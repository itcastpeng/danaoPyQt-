import requests, random, sqlite3
from bs4 import BeautifulSoup
from time import sleep


class Baidu_Zhidao_URL_MOBILE(object):


    def __init__(self, keyword, domain):
        self.keyword = keyword
        self.domain = domain
        self.zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'

        data_list = self.get_keywords()
        # self.set_data(data_list)


    def get_keywords(self):
        self.random_time()
        print('查看收录链接 ---------- > ',self.zhidao_url.format(self.domain))
        headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        url = self.zhidao_url.format(self.domain)
        ret = requests.get(url, headers=headers)
        soup = BeautifulSoup(ret.text, 'lxml')
        data_list = []
        if soup.find('div', class_='content_none'):
            print('没有收录')
        else:
            div_tags = soup.find('div', class_='results').find_all('div', class_='result c-result')
            for div_tag in div_tags:
                dict_data = eval(div_tag['data-log'])
                data_list.append(dict_data['mu'])

        # 查询关键词 匹配链接
        self.random_time()
        url = self.zhidao_url.format(self.keyword)
        print('搜索关键词 链接--------> ',url)
        ret_two = requests.get(url, headers=headers)
        soup_two = BeautifulSoup(ret_two.text, 'lxml')
        content_list_order = []
        div_tags = soup_two.find_all('div', class_='result c-result')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        div_tags = soup_two.find_all('div',class_='result c-result c-clk-recommend')
        for div_tag in div_tags:
            content_list_order.append(div_tag)

        # 遍历已收录链接 匹配url
        for data_url in data_list:
            print('已收录链接 data_url------> ',data_url)
            for content_order in content_list_order:
                str_data = eval(content_order['data-log'])
                if str_data['mu']:
                    if str_data['mu'] == data_url:
                        # print(str_data['mu'])
                        paiming_order = str_data['order']
                        data_list.append({
                                'paiming_order': paiming_order,
                                'shifoushoulu': 1,
                            })
                        print(str_data['mu'])
                        print(str_data['order'])


    def random_time(self):
        return sleep(random.randint(1, 2))


    def set_data(self, data_list):
        # conn = sqlite3.connect('my_sqlite.db')
        # cursor = conn.cursor()
        print('thread_mobileurl ------------- > ', data_list)


if __name__ == '__main__':
    keyword = '温州建国医院怎么样／好不好 正规医院口碑评价 尽心为患者服务'
    domain = 'http://news.39.net/a/171204/5901183.html'
    # domain = 'http://m-mip.39.net/news/mipso_5901183.html'
    # domain = 'https://tieba.baidu.com/p/1382203163?red_tag=2092386831'
    Baidu_Zhidao_URL_MOBILE(keyword, domain)


