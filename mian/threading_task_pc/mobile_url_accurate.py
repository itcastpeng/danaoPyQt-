import requests, random, sqlite3
from bs4 import BeautifulSoup



class Baidu_Zhidao_URL_MOBILE(object):


    def __init__(self, keyword, domain):
        self.keyword = keyword
        self.domain = domain
        self.zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'
        data_list = self.get_keywords()
        self.set_data(data_list)


    def get_keywords(self):
        ret = requests.get(self.zhidao_url.format(self.keyword))
        self.random_time()
        # print('请求链接 ---------- > ',self.zhidao_url.format(self.keyword))

        self.random_time()
        soup = BeautifulSoup(ret.text, 'lxml')
        id_tag = soup.find('div', id='results')
        div_tags = id_tag.find_all('div', class_='result c-result c-clk-recommend')
        self.random_time()
        data_list = []
        for div_tag in div_tags:
            str_title = div_tag.find('h3').get_text()
            # print(str_title)
            dict_data = eval(div_tag['data-log'])
            page_div = dict_data['order']  # 排名
            url_title = dict_data['mu']      # 标题链接
            line_clamp = div_tag.find('div',class_='c-line-clamp1')
            yuming = line_clamp.find('span').get_text()
            if url_title == self.domain :
                data_list.append({
                    'str_title': str_title,
                    'page_div': page_div,
                    'url_title': url_title,
                    'shifoushoulu': 1,
                })
            else:
                # print('进入 else-----------',self.zhidao_url.format(self.domain))
                ret = requests.get(self.zhidao_url.format(self.domain))
                self.random_time()
                soup = BeautifulSoup(ret.text, 'lxml')
                self.random_time()
                id_tag = soup.find('div', id='results')
                div_tags = id_tag.find_all('div', class_='result c-result c-clk-recommend')
                # print('id_tag--------------> ',div_tags)
                for div_tag in div_tags:
                    str_title = div_tag.find('h3').get_text()
                    dict_data = eval(div_tag['data-log'])
                    page_div = dict_data['order']  # 排名
                    url_title = dict_data['mu']  # 标题链接
                    # print('str_title------------> ',str_title)
                    data_list.append({
                        'str_title': str_title,
                        # 'page_div': page_div,
                        'url_title': url_title,
                        'shifoushoulu': 1,
                    })
        return data_list


    def random_time(self):
        return random.randint(2, 3)


    def set_data(self, data_list):
        # conn = sqlite3.connect('my_sqlite.db')
        # cursor = conn.cursor()
        print('thread_mobileurl ------------- > ', data_list)


if __name__ == '__main__':
    keyword = ''
    domain = ''
    Baidu_Zhidao_URL_MOBILE(keyword, domain)