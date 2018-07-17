import requests, random, sqlite3
from bs4 import BeautifulSoup
from time import sleep
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


    def __init__(self,keyword,domain):
        self.keyword = keyword
        self.domain = domain
        self.headers = {
            'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)],
        }
        self.zhidao_url = 'https://www.baidu.com/s?wd={keyword}'.format(keyword='{}')
        data_list = self.get_keywords()
        # self.set_data(data_list)


    def get_keywords(self):
        self.random_time()
        print('请求的链接-------------> ',self.zhidao_url.format(self.keyword))
        ret = requests.get(self.zhidao_url.format(self.keyword) ,headers=self.headers)
        soup = BeautifulSoup(ret.text, 'lxml')
        id_tag = soup.find('div', id='content_left')
        # print(id_tag)
        div_tags = id_tag.find_all('div', class_='result c-container ')
        data_list = []
        for div_tag in div_tags:
            self.random_time()
            rank_num = div_tag.attrs.get('id')
            if not rank_num:
                continue
            tiaojian_chaxun = div_tag.get_text()
            print(tiaojian_chaxun)
            # title_tag = div_tag.find('div', class_='c-tools')['data-tools']
            # dict_title = eval(title_tag)
            # str_title = dict_title['title']  # 标题
            # url_title = dict_title['url']  # 标题链接
            # div_13 = div_tag.find('div', class_='f13')
            # a_tag = div_13.find('a', target='_blank').get_text()
            # print('----------->',self.domain,tiaojian_chaxun)
            # dict_data = eval(div_tag['data-click'])
            # self.random_time()

            print(self.domain ,'----',tiaojian_chaxun)
            if self.domain in tiaojian_chaxun:
                print('条件匹配=======')
                data_list.append(int(rank_num))
        print('data_list-------------->',data_list)

        # return data_list



    def random_time(self):
        return sleep(random.randint(1,2))


    def set_data(self,data_list):
        # conn = sqlite3.connect('my_sqlite.db')
        # cursor = conn.cursor()
        print('thread_pcmohupipei--------------> ',data_list)

if __name__ == '__main__':
    keyword = '北京男科哪家好'
    domain = 'haoping.haod'
    Baidu_Zhidao_yuming_pc(keyword, domain)

