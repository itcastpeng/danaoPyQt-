import requests, random
import time
from bs4 import BeautifulSoup
from mian.threading_task_pc.public import shouluORfugaiChaxun
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
headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}

def PC_360_URL_PC(detail_id, keyword, domain):
    pc_360url = """https://so.com/s?src=3600w&q={keyword}""".format(keyword=keyword)
    order = 0
    resultObj = shouluORfugaiChaxun.pcShoulu360(domain)
    ret_domain = requests.get(pc_360url, headers=headers)
    soup = BeautifulSoup(ret_domain.text, 'lxml')
    if soup.find('div', class_='so-toptip'):
        resultObj['shoulu'] = '0'
    else:
        li_tags = soup.find_all('li', class_='res-list')
        order_num = 0
        for li_tag in li_tags:
            order_num += 1
            if li_tag.find('p', class_='res-linkinfo'):
                zongti_xinxi = li_tag.find('a', target='_blank')  # 获取order -- title -- title_url
                yuming_canshu = li_tag.find('p', class_='res-linkinfo')  # 域名参数
                if li_tag.find('a').attrs.get('data-url'):
                    data_url = li_tag.find('a').attrs.get('data-url')
                else:
                    data_url = zongti_xinxi.attrs['href']
                yuming = yuming_canshu.find('cite').get_text()
                yuming_deal = yuming.split('/')[0].rstrip('...').split('>')[0]
                if yuming_deal in domain:
                    ret_two_url = requests.get(data_url, headers=headers, timeout=10)
                    if domain in ret_two_url.url:
                        order = order_num
                        break
    data_list = {
        'order':order,
        'shoulu':resultObj['shoulu'],
    }
    return data_list

