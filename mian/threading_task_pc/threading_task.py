from multiprocessing import Queue
import sqlite3, os, sys, json, re, time
from mian.threading_task_pc import mobile_fugai_pipei, mobile_url_accurate, pc_url_accurate, pc_fugai_pipei
from time import sleep
import threading
import queue


# 重点词监控 - 多线程部署
def thread_pcurl(detail_id, keywords, domain, pool,):
    sleep(1)
    # print('进入线程--thread_pcurl--> ', ' pc端 有链接', keywords, domain)
    pc_url_accurate.Baidu_Zhidao_URL_PC(detail_id, keywords, domain)
    pool.add_thread()


def thread_mobileurl(detail_id, keywords, domain, pool,):
    print('进入线程--thread_mobileurl--> ', ' 移动端 有链接', keywords, domain)
    mobile_url_accurate.Baidu_Zhidao_URL_MOBILE(detail_id, keywords, domain)
    pool.add_thread()


def thread_pcmohupipei(yinqing,detail_id, keywords, domain, pool,):
    # sleep(5)
    print('进入线程--thread_pcmohupipei--> ',' pc端 无链接',keywords, domain)
    pc_fugai_pipei.Baidu_Zhidao_yuming_pc(yinqing,detail_id, keywords, domain)
    pool.add_thread()


def thread_mobilemohupipei(detail_id, keywords, domain, pool,):
    # sleep(5)
    print('进入线程--thread_mobilemohupipei--> ','移动端 无链接',keywords, domain)
    mobile_fugai_pipei.Baidu_Zhidao_yuming_mobile(detail_id,keywords, domain)
    pool.add_thread()


# 启动程序 - 重点词监控
def func(detail_id,lianjie, keywords, search_engine, mohupipei, pool,):
    # 去线程池里那一个线程，如果有，则池子里拿，如果没有，等直到有人归还线程到线程池
    print('search_engine -->', search_engine)
    print('lianjie -->', lianjie)
    thread_obj = pool.get_thread()
    if lianjie:
        if search_engine == '4':
            # print('进入线程----> ','移动端 有链接',keywords)
            thread_mobile_url = thread_obj(target=thread_mobileurl, args=(detail_id, keywords,lianjie,pool))
            thread_mobile_url.start()

        if search_engine == '1':
            # print('进入线程----> ',' pc端 有链接',keywords)
            thread_pc_url = thread_obj(target=thread_pcurl, args=(detail_id, keywords,lianjie,pool))
            thread_pc_url.start()

            print('----->')

    else:
        if search_engine == '4':
            # print('进入线程----> ','移动端 无链接',keywords)
            thread_mobile_mohupipei = thread_obj(target=thread_mobilemohupipei, args=(detail_id, keywords,mohupipei,pool))
            thread_mobile_mohupipei.start()

        else:
            # print('进入线程----> ',' pc端 无链接',keywords)
            thread_pc_mohupipei = thread_obj(target=thread_pcmohupipei, args=(search_engine,detail_id, keywords,mohupipei,pool))
            thread_pc_mohupipei.start()



# 收录查询 - 多线程部署
class Thread_shoulu_Pool(object):

    def __init__(self, max_num=5):
        # 创建一个队列，队列里最多只能有5个数据
        self.queue = queue.Queue(max_num)
        # 在队列里填充线程类
        for i in range(max_num):
            self.queue.put(threading.Thread)

    def get_thread(self):
        # 去队列里取数据，queue特性，如果有，对列里那一个出来 如果没有，阻塞，
        return self.queue.get()

    def add_thread(self):
        # 往队列里再添加一个线程类
        self.queue.put(threading.Thread)

shoulu_pool = Thread_shoulu_Pool(5)
shoulu_canshu = 1
def shoulu_pc(search,lianjie, huoqu_shoulu_time_stamp):
    # print('lianjie======--------------> ',lianjie)
    pc_url_accurate.shoulu_chaxun(lianjie,search,huoqu_shoulu_time_stamp,shoulu_canshu)
    shoulu_pool.add_thread()

def shoulu_mobile(search,lianjie,huoqu_shoulu_time_stamp):
    # print('lianjie------=-==-=-=-=-=>',lianjie)
    mobile_url_accurate.shoulu_chaxun(lianjie,search,huoqu_shoulu_time_stamp,shoulu_canshu)
    shoulu_pool.add_thread()

# 运行程序 - 收录查询
def func_shoulu_chaxun(yinqing,lianjie,huoqu_shoulu_time_stamp):
    # print('lianjie=========> ',lianjie, type(lianjie))
    thread_shoulu_obj = shoulu_pool.get_thread()
    if yinqing == '1':
        shoulu_pc_obj = thread_shoulu_obj(target=shoulu_pc, args=(yinqing,lianjie,huoqu_shoulu_time_stamp))
        shoulu_pc_obj.start()
    else:
        thread_mobile_url = thread_shoulu_obj(target=shoulu_mobile, args=(yinqing,lianjie,huoqu_shoulu_time_stamp))
        thread_mobile_url.start()

# if __name__ == '__main__':
#     yinqing = '1'
#     lianjie = "http://yyk.39.net/beijing/hospitals/nanke/"
#     huoqu_shoulu_time_stamp = '51616156'
#     func_shoulu_chaxun(yinqing, lianjie,huoqu_shoulu_time_stamp)
