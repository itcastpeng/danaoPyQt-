import requests, random
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet
from mian.my_db import database_create_data
import json
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

headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)],
           'referer':'http://www.so.com/link?m=aVukX1ytxg26W0Ro5r%2Fj0tGtXCIbEd73VYvnk2hbgxYmTdWuAmKVPGjspHB%2B%2FktZTI%2BaF0YQ1owSrmyB2qCsZz%2F71qzQc1V6mjeLV9Wuw0Ljfvvk2VIj%2FzoRap6FBH%2B3esu1Hk0M7MG6fEcsxMmhf1xVYMo4D8ohtqTnD836xElzENn0%2FYPqG2fBdO0ohUgVuM9bCn4tBoCBTWXdno3U5f1LeUxc5%2BzfdUUYaNld%2F%2Fz76ROHcMHVHJ5ZgXYU0hE63bDbQ1dT3rCHrdN9LRuWlxWshy0kxkj7sDl94sWmvVyUeLiOZJG1rWmP0LXeJs2SSvyDwmVq09aXP65F1'}

def shoulu_chaxun(domain,search=None,huoqu_shoulu_time_stamp=None,shoulu_canshu=None,data_id=None):
    pc_360url = 'https://so.com/s?src=3600w&q={keyword}'.format(keyword=domain)
    # print('pc_360url-----------------> ',pc_360url)
    data_list = []
    shoulu = '0'
    kuaizhao_time = ''
    title = ''
    status_code = ''
    order = ''
    ret_domain = requests.get(pc_360url, headers=headers)
    soup = BeautifulSoup(ret_domain.text, 'lxml')
    if soup.find('div', class_='so-toptip'):
        shoulu = '0'
    else:
        li_tags = soup.find_all('li', class_='res-list')
        for li_tag in li_tags:
            if li_tag.find('p', class_='res-linkinfo'):
                # print(li_tag)
                zongti_xinxi = li_tag.find('a', target='_blank')            # 获取order -- title -- title_url
                yuming_canshu = li_tag.find('p', class_='res-linkinfo')    # 域名参数
                data_res = eval(zongti_xinxi.attrs.get('data-res'))
                order = data_res['pos']
                if li_tag.find('a').attrs.get('data-url'):
                    data_url = li_tag.find('a').attrs.get('data-url')
                else:
                    data_url = zongti_xinxi.attrs['href']
                yuming = yuming_canshu.find('cite').get_text()
                yuming_deal = yuming.split('/')[0].rstrip('...').split('>')[0]
                if yuming_deal in domain:
                    # print('域名在-----', data_url)
                    ret_two = requests.get(data_url, headers=headers)
                    soup_two = BeautifulSoup(ret_two.text, 'lxml')
                    status_code = ret_two.status_code                           # 状态码
                    renwu_url = ret_two.url
                    # print('ret_two.url---------->',renwu_url)
                    # print('对比00000000','order---> ',order,'任务url',renwu_url ,'任务====' , domain)
                    if renwu_url == domain:
                        # print(domain ,'-----> 已收录')
                        shoulu = '1'
                        data_list.append({
                            'order':order,
                            'shoulu':shoulu,
                            'status_code':status_code
                        })
    # if shoulu_canshu:
    #     select_sql = """select id from shoulu_Linshi_List where time_stamp='{time_stamp}' and url='{url}' and search={search}""".format(
    #         time_stamp=huoqu_shoulu_time_stamp, url=domain, search=search)
    #     print('select_sql----------------> ',select_sql)
    #     id_objs = database_create_data.operDB(select_sql, 'select')
    #     id_obj = id_objs['data'][0][0]
    #     print('获取的pcid =------> ',id_obj , 'pc端状态码--------------->',status_code)
    #     sql = """update shoulu_Linshi_List set is_shoulu='{shoulu}', title='{title}', kuaizhao_time='{kuaizhao}', status_code='{status_code}' where id ={id};""".format(
    #         shoulu=shoulu,
    #         title=title,
    #         kuaizhao=kuaizhao_time,
    #         status_code=status_code,
    #         id=id_obj
    #     )
    #     database_create_data.operDB(sql, 'update')
    return shoulu



class PC_360_URL_PC():

    def __init__(self, keyword, domain):
        self.data_base_list = []
        self.keyword = keyword
        self.domain = domain
        # self.detail_id = detail_id
        self.pc_360url = """https://so.com/s?src=3600w&q={keyword}""".format(keyword=self.keyword)

        # data_list = self.get_keywords()
        # self.set_data(data_list)
        self.get_keywords()


    def get_keywords(self):
        data_list = []
        # search = '1'
        shoulu = shoulu_chaxun(self.domain)
        # shoulu = '0'
        ret = requests.get(self.pc_360url, headers=headers)
        soup = BeautifulSoup(ret.text, 'lxml')
        li_tags = soup.find_all('li', class_='res-list')
        for li_tag in li_tags:
            if li_tag.find('p', class_='res-linkinfo'):
                yuming_canshu = li_tag.find('p', class_='res-linkinfo')    # 域名参数
                yuming = yuming_canshu.find('cite').get_text()
                yuming_deal = yuming.split('/')[0].rstrip('...').split('>')[0]
                if yuming_deal in self.domain:
                    print(self.pc_360url, '===================================')
                    zongti_xinxi = li_tag.find('a', target='_blank')            # 获取order -- title -- title_url
                    data_res = eval(zongti_xinxi.attrs.get('data-res'))
                    if li_tag.find('a').attrs.get('data-url'):
                        data_url = li_tag.find('a').attrs.get('data-url')
                    else:
                        data_url = li_tag.find('a').attrs['href']
                    order = data_res['pos']
                    if data_url == self.domain:
                        print('匹配--------> ', data_url, domain)
                        ret_two = requests.get(data_url, headers=headers)
                        status_code = ret_two.status_code                           # 状态码
                        # if status_code == '302':
                        #     print('Location================> ',ret_two.headers['Location'])
                        print(self.domain ,'-----> 已收录')
                        data_list.append({
                            'order':order,
                            'shoulu':shoulu,
                            'status_code':status_code
                        })
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





data_list = """
去马来西亚做试管婴儿吸引你的不止是低价	http://news.qiuyi.cn/html/2017/fuke_1205/63968.html,
义乌微创医院怎么样 关爱弱势群体公益活动 	http://at.025ct.com/dt/2017/1204/514781.html,
潍坊长安医院好不好：专家24小时在线诊疗	http://www.jianzhijia.com/hyzx/jkjd/79379.html,
温州建国医院怎么样／好不好 正规医院口碑评价 尽心为患者服务	http://news.39.net/a/171204/5901183.html,
随州东方妇科医院正规吗？做好了一切医疗服务的准备工作	http://news.39.net/a/171204/5901194.html,
兰州天伦不孕医院很好吗？专科品牌专业医院	http://news.360xh.com/201712/04/37416.html,
兰州天伦医院评价好吗？品质服务赢得人心！	http://www.iiijk.com/cjxw/04-74550.html,
兰州天伦医院乱收费吗？执行国家标准 各项收费公示	http://www.jianzhijia.com/hyzx/jkjd/79381.html,
大连新华美天周年庆变美抄底1折起  消费多少送多少	http://news.qiuyi.cn/html/2017/zhengxing_1204/63922.html,
临沂协和医院怎么样：年终公益活动 年终特惠点开查看	http://news.39.net/a/171204/5902419.html,
徐州市交通医院精神科靠谱吗？国家公立“医联体”联盟单位	http://www.jianzhijia.com/hyzx/jkjd/79383.html,
昆明华希男科医院评价怎么样？好不好？公立为民彰显医者大爱	http://news.360xh.com/201712/04/37402.html,
百姓呼声:“私人健康顾问服务”正式在岳阳世纪医院落实运行	http://www.sohu.com/a/208330800_544906,
天津美莱双眼皮手术靠谱么 让眼睛的魅力更加美丽	http://www.iiijk.com/cjxw/04-74552.html,
株洲阳光怎么样 正规男科连续多年百姓满意医院	http://www.iiijk.com/cjxw/04-74551.html,
天津美莱双眼皮埋线好不好 美莱暖冬计划启动中	http://focus.smxe.cn/20171204/148402.shtml,
昆明宝岛妇产医院有去过的吗？奋勇争先，情系健康	http://news.360xh.com/201712/04/37408.html,
昆明华希医院确保医疗安全，规范服务行为	http://news.39.net/a/171204/5902423.html,
唐山现代医院黑吗用心服务  用情呵护	http://www.jianzhijia.com/hyzx/jkjd/79385.html,
南昌博爱医院怎么样 德技兼备才能救死扶伤	http://news.360xh.com/201712/04/37409.html,
延安五洲医院好吗 一医一患一诊室 舒适就医环境	http://news.360xh.com/201712/04/37410.html
"""

for data in data_list.split(','):
    if len(data) > 5:
        keyword = data.strip().split('http')[0]
        domain = 'http' + data.strip().split('http')[1]
        # print('domian ========> ',keyword,domain)
        PC_360_URL_PC(keyword, domain)
        # shoulu_chaxun(domain)



