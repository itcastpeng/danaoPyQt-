import time
import requests
from requests.exceptions import ConnectionError
import random
import chardet
from bs4 import BeautifulSoup

pcRequestHeader = [
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


# 获取页面访问状态和标题
def getPageInfo(url):
    headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}
    try:
        ret_two = requests.get(url, headers=headers, timeout=10)
        ret_two_url = ret_two.url
        status_code = ret_two.status_code
        encode_ret = ret_two.apparent_encoding
        if encode_ret == 'GB2312':
            ret_two.encoding = 'gbk'
        else:
            ret_two.encoding = 'utf-8'
        soup_two = BeautifulSoup(ret_two.text, 'lxml')
        try:
            title = soup_two.find('title').get_text().strip().replace('\r\n', '')
        except AttributeError:
            title = ''
    # except ConnectionError:
    except:
        pass
        status_code = 500
        title = ''
        ret_two_url = ''
    return status_code, title, ret_two_url

# 获取页面访问状态和标题
# def getPageInfo(url):
#     # def getPageInfo():
#
#     # url = 'https://blog.csdn.net/together_cz/article/details/59109044'
#     headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)]}
#     try:
#         start_time = time.time()
#         # ret_two = requests.get(url, headers=headers, timeout=5)
#         ret_two = requests.get(url, headers=headers)
#         ret_two_url = ret_two.url
#         status_code = ret_two.status_code
#         # print('status_code-------> ',status_code)
#         # encode_ret = chardet.detect(ret_two.text.encode())['encoding']  # 线上可用
#         # print('编码格式=--------------> ',encode_ret)
#
#         # if encode_ret == 'GB2312':
#         #     ret_two.encoding = 'gbk'
#         # else:
#         #     ret_two.encoding = 'utf-8'
#
#         soup_two = BeautifulSoup(ret_two.text, 'lxml')
#         soup_two.find('meta ')
#
#     #     try:
#     #         title = soup_two.find('title').get_text().strip().replace('\r\n', '')
#     #     except AttributeError:
#     #         title = ''
#     #     print('编码--->', ret_two.encoding, 'title-->',title, 'ret_two_url-->',ret_two_url)
#     #     print('')
#     # # except ConnectionError:
#     except:
#         pass
#     #     status_code = 500
#     #     title = ''
#     #     ret_two_url = ''
#     # return status_code, title, ret_two_url
