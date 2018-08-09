import requests, random
from bs4 import BeautifulSoup
import datetime
from time import sleep
from my_db import database_create_data
from threading_task_pc import zhongzhuanqi

def Baidu_Zhidao_yuming_mobile(yinqing, keyword, domain, detail_id):
    result = zhongzhuanqi.fugaiChaxun(detail_id, yinqing, keyword, ','.join(domain.split(',')))
    if result:
        return result
