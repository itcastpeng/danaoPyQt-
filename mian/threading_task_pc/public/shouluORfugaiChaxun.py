import requests
import random
from bs4 import BeautifulSoup
from mian.threading_task_pc.public.getpageinfo import getPageInfo
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

# 百度pc端收录查询
def baiduShouLuPC(domain):
    resultObj = {
        "shoulu": 0,
        "kuaizhao_time": '',
        "title": '',
        "status_code": ''
    }
    domain = domain.strip()
    zhidao_url = 'http://www.baidu.com/s?wd={domain}'.format(domain=domain)
    headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}
    ret_domain = requests.get(zhidao_url, headers=headers, timeout=10)
    soup_domain = BeautifulSoup(ret_domain.text, 'lxml')
    if soup_domain.find('div', class_='content_none'):
        pass
    else:
        div_tags = soup_domain.find_all('div', class_='result c-container ')
        if div_tags and div_tags[0].attrs.get('id'):
            panduan_url = div_tags[0].find('a').attrs['href']
            f13_div = div_tags[0].find('div', class_='f13')
            if f13_div.find('a'):
                yuming = f13_div.find('a').get_text()[:-5].split('/')[0]  # 获取域名
                status_code, title, ret_two_url = getPageInfo(panduan_url)
                if yuming in domain:
                    if domain in ret_two_url:
                        if div_tags[0].find('span', class_='newTimeFactor_before_abs'):
                            resultObj["kuaizhao_time"] = div_tags[0].find('span',
                                class_='newTimeFactor_before_abs').get_text().strip().replace('-', '').replace('年',
                                '-').replace('月', '-').replace('日', '').strip()
                        resultObj["status_code"] = status_code
                        resultObj["title"] = title
                        resultObj["shoulu"] = 1
    return resultObj
# 百度移动端收录查询
def baiduShouLuMobeil(domain):
    resultObj = {
        "shoulu": 0,
        "kuaizhao_time": '',
        "title": '',
        "status_code": ''
    }
    domain = domain.strip()
    zhidao_url = 'https://m.baidu.com/from=844b/pu=sz@1320_2001/s?tn=iphone&usm=2&word={}'.format(domain)
    headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    ret_domain = requests.get(zhidao_url, headers=headers, timeout=10)
    soup_domain = BeautifulSoup(ret_domain.text, 'lxml')
    if not soup_domain.find_all('div', class_='result c-result'):
        pass
    else:
        div_tags = soup_domain.find_all('div', class_='result c-result')
        if div_tags:
            dict_data_clog = eval(div_tags[0].attrs.get('data-log'))
            url = dict_data_clog['mu']
            if url.strip():
                status_code, title, ret_two_url = getPageInfo(url)
                if domain == url or url[:-1] == domain:
                    resultObj["status_code"] = status_code
                    resultObj["title"] = title
                    resultObj["shoulu"] = 1
    return resultObj


# 百度pc端覆盖查询
def baiduFuGaiPC(keyword, mohu_pipei_list):
    order_list = []
    headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)], }
    zhidao_url = 'https://www.baidu.com/s?wd={keyword}'.format(keyword=keyword)
    ret = requests.get(zhidao_url, headers=headers, timeout=10)
    soup = BeautifulSoup(ret.text, 'lxml')
    div_tags = soup.find_all('div', class_='result c-container ')
    for mohu_pipei in mohu_pipei_list.split(','):
        for div_tag in div_tags:
            rank_num = div_tag.attrs.get('id')
            if not rank_num:
                continue
            tiaojian_chaxun = div_tag.get_text()
            panduan_url = div_tag.find('h3', class_='t').find('a').attrs['href']
            title = div_tag.find('h3', class_='t').get_text()
            if mohu_pipei in tiaojian_chaxun:  # 表示有覆盖
                order_list.append({
                    'paiming': int(rank_num),
                    'title': title,
                    'title_url': panduan_url,
                    'sousuo_guize': mohu_pipei,
                })
    return order_list
# 百度移动端覆盖查询
def baiduFuGaiMOBIEL(keyword, mohu_pipei_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    zhidao_url = 'https://m.baidu.com/s?word={}'.format(keyword)
    ret = requests.get(zhidao_url, headers=headers, timeout=10)
    soup_browser = BeautifulSoup(ret.text, 'lxml')
    content_list_order = []
    div_tags = soup_browser.find_all('div', class_='result c-result')
    for div_tag in div_tags:
        content_list_order.append(div_tag)
    div_tags = soup_browser.find_all('div', class_='result c-result c-clk-recommend')
    for div_tag in div_tags:
        content_list_order.append(div_tag)
    order_list = []
    title = ''
    for mohu_pipei in mohu_pipei_list.split(','):
        for data in content_list_order:
            if data['data-log']:
                dict_data = eval(data['data-log'])
                url_title = dict_data['mu']  # 标题链接
                order = dict_data['order']  # 排名
                pipei_tiaojian = data.get_text()
                if mohu_pipei in pipei_tiaojian:
                    if data.find('div', class_='c-container').find('a'):
                        title = data.find('div', class_='c-container').find('a').get_text()
                    order_list.append({
                        'paiming': int(order),
                        'title': title,
                        'title_url': url_title,
                        'sousuo_guize': mohu_pipei,
                    })
    return order_list


# 360pc端收录查询
def pcShoulu360(domain):
    resultObj = {
        "shoulu": 0,
        "kuaizhao_time": '',
        "title": '',
        "status_code": '',
        "rank_num":0
    }
    headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}
    pc_360url = 'https://so.com/s?src=3600w&q={domain}'.format(domain=domain)
    ret_domain = requests.get(pc_360url, headers=headers)
    soup = BeautifulSoup(ret_domain.text, 'lxml')
    if soup.find('div', class_='so-toptip'):
        resultObj['shoulu'] = '0'
    else:
        li_tags = soup.find_all('li', class_='res-list')
        if li_tags[0].find('p', class_='res-linkinfo'):
            zongti_xinxi = li_tags[0].find('a', target='_blank')            # 获取order -- title -- title_url
            yuming_canshu = li_tags[0].find('p', class_='res-linkinfo')    # 域名参数
            if li_tags[0].find('a').attrs.get('data-url'):
                data_url = li_tags[0].find('a').attrs.get('data-url')
            else:
                data_url = zongti_xinxi.attrs['href']
            yuming = yuming_canshu.find('cite').get_text()
            yuming_deal = yuming.split('/')[0].rstrip('...').split('>')[0]
            if yuming_deal in domain:
                status_code, title, ret_two_url = getPageInfo(data_url)
                resultObj["status_code"] = status_code
                resultObj["title"] = title
                if domain in ret_two_url:
                    resultObj['shoulu'] = '1'
    return resultObj
# 360移动端收录查询
def mobielShoulu360(domain):
    resultObj = {
        "shoulu": 0,
        "kuaizhao_time": '',
        "title": '',
        "status_code": '',
        "rank_num": 0
    }
    PC_360_url = 'https://m.so.com/s?src=3600w&q={}'.format(domain)
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    ret = requests.get(PC_360_url, headers=headers)
    soup = BeautifulSoup(ret.text, 'lxml')
    if soup.find('div', class_='mso-url2link'):
        resultObj['shoulu'] = '0'
    else:
        div_tags = soup.find_all('div', class_=' g-card res-list og ')
        if div_tags[0].attrs.get('data-pcurl'):
            url_data = div_tags[0].attrs.get('data-pcurl')
            status_code, title, ret_two_url = getPageInfo(url_data)
            resultObj["status_code"] = status_code
            resultObj["title"] = title
            if domain in ret_two_url:
                resultObj['shoulu'] = '1'
    return resultObj


# 360pc端覆盖查询
def pcFugai360(keyword, mohu_pipei_list):
    order_list = []
    headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)], }
    pc_360url = 'https://so.com/s?src=3600w&q={keyword}'.format(keyword=keyword)
    ret = requests.get(pc_360url, headers=headers, timeout=10)
    soup = BeautifulSoup(ret.text, 'lxml')
    div_tags = soup.find_all('li', class_='res-list')
    for mohu_pipei in mohu_pipei_list.split(','):
        for div_tag in div_tags:
            zongti_fugai = div_tag.get_text()
            if mohu_pipei in zongti_fugai:
                if div_tag.find('a').attrs.get('data-res'):
                    data_res = div_tag.find('a')
                    paiming = data_res.attrs.get('data-res')
                    dict_data_res = json.loads(paiming)
                    panduan_url = data_res.attrs['href']
                    title = data_res.get_text()
                    order_list.append({
                        'paiming': int(dict_data_res['pos']),
                        'title': title,
                        'title_url': panduan_url,
                        'sousuo_guize': mohu_pipei,
                    })
    return order_list

# 360移动端覆盖查询
def mobielFugai360(keyword, mohu_pipei_list):
    PC_360_url = 'https://m.so.com/s?src=3600w&q={}'.format(keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    ret = requests.get(PC_360_url, headers=headers, timeout=10)
    soup_browser = BeautifulSoup(ret.text, 'lxml')
    div_tags = soup_browser.find_all('div', class_=" g-card res-list og ")
    for mohu_pipei in mohu_pipei_list.split(','):
        for div_tag in div_tags:
            zongti_fugai = div_tag.get_text()
            if mohu_pipei in zongti_fugai:
                print(div_tag)
                print(div_tag.attrs.get('data-url'))
                print(div_tag.find('data-url'))




