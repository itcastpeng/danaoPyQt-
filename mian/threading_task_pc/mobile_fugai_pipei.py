import requests, random, sqlite3
from bs4 import BeautifulSoup



class Baidu_Zhidao_yuming_mobile(object):


    def __init__(self, keyword, domain):
        self.keyword = keyword
        self.domain = domain
        self.zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'
        data_list = self.get_keyword()
        # self.set_data(data_list)


    def get_keyword(self):
        zhidao_url = self.zhidao_url.format(self.keyword)
        print('请求链接 ------------ >',zhidao_url)
        ret = requests.get(zhidao_url)
        self.random_time()
        soup_browser = BeautifulSoup(ret.text, 'lxml')
        results = soup_browser.find('div', id='results')
        self.random_time()
        data_list = []
        for result in results:
            # try:
            if result['data-log']:
                dict_data = eval(result['data-log'])
                url_title = dict_data['mu']                    # 标题链接
                if url_title:
                    order = dict_data['order']                     # 排名
                    pipei_tiaojian = result.get_text()
                    # print(order, pipei_tiaojian)
                    if self.domain in pipei_tiaojian:
                        data_list.append(int(order))
        print(data_list)
        #     except Exception as e :
        #         pass
        # return data_list


    def random_time(self):
        return random.randint(2,3)


    def set_data(self, data_list):
        print('thread_mobilemohupipei-----------> ',data_list)

if __name__ == '__main__':
    keyword = '北京男科哪家好'
    domain = '病会有死精，无精症，患者是睾丸炎，前列腺炎等症状，你又想知道具体的原因，你就得去'
    Baidu_Zhidao_yuming_mobile(keyword, domain)


