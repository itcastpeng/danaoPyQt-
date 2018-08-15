import requests, random
from bs4 import BeautifulSoup
import time
from mian.threading_task_pc.public import getpageinfo, shouluORfugaiChaxun


def PC_360_URL_MOBILE(detail_id, keyword, domain):
    PC_360_url = 'https://m.so.com/s?src=3600w&q={}'.format(keyword)
    order = 0
    resultObj = shouluORfugaiChaxun.mobielShoulu360(domain)
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    ret = requests.get(PC_360_url, headers=headers)
    soup = BeautifulSoup(ret.text, 'lxml')
    if soup.find('div', class_='mso-url2link'):
        resultObj['shoulu'] = '0'
    else:
        div_tags = soup.find_all('div', class_=' g-card res-list og ')
        order_num = 0
        for div_tag in div_tags:
            order_num += 1
            if div_tag.attrs.get('data-pcurl'):
                url_data = div_tag.attrs.get('data-pcurl')
                ret_two_url = requests.get(url_data, headers=headers, timeout=10)
                if domain in ret_two_url.url:
                    order = order_num
                    break
    data_list = {
        'order': order,
        'shoulu': resultObj['shoulu'],
        }
    return data_list

