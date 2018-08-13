import requests, random
from bs4 import BeautifulSoup
from time import sleep
import datetime
import chardet
from my_db import database_create_data
from threading_task_pc.public import getpageinfo, shouluORfugaiChaxun

import time

zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'

def Baidu_Zhidao_URL_MOBILE(detail_id, keyword, domain):
    shoulu = ''
    paiming_order = '0'
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    resultObj = shouluORfugaiChaxun.baiduShouLuMobeil(domain)
    if resultObj['shoulu'] == 1:
        url = zhidao_url.format(keyword)
        ret_two = requests.get(url, headers=headers, timeout=10)
        soup_two = BeautifulSoup(ret_two.text, 'lxml')
        content_list_order = []
        div_tags = soup_two.find_all('div', class_='result c-result')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        div_tags = soup_two.find_all('div', class_='result c-result c-clk-recommend')
        for div_tag in div_tags:
            content_list_order.append(div_tag)
        for obj_tag in content_list_order:
            dict_data_clog = eval(obj_tag.attrs.get('data-log'))
            url = dict_data_clog['mu']
            if url:
                ret_two_url = ''
                try:
                    ret_two_url = requests.get(url, headers=headers, timeout=10)
                except Exception:
                    pass
                if ret_two_url.url == domain or domain in ret_two_url.url:
                    paiming_order = dict_data_clog['order']
                    break
    data_list = {
        'order': int(paiming_order),
        'shoulu':resultObj['shoulu'],
        }
    return data_list
