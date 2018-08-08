from multiprocessing import Queue
import sqlite3, os, sys, json, re, time
from threading_task_pc.pc_baidu import mobile_fugai_pipei_baidu, mobile_url_accurate_baidu, pc_url_accurate_baidu, \
    pc_fugai_pipei_baidu
from time import sleep
import threading
from my_db import database_create_data
import queue
# # 重点词监控 - 多线程部署
# def thread_pcurl(detail_id, keywords, domain, pool,):
#     # print('进入线程--thread_pcurl--> ', ' pc端 有链接', keywords, domain)
#     pc_url_accurate.Baidu_Zhidao_URL_PC(detail_id, keywords, domain)
#     pool.add_thread()
#
#
# def thread_mobileurl(detail_id, keywords, domain, pool,):
#     # print('进入线程--thread_mobileurl--> ', ' 移动端 有链接', keywords, domain)
#     mobile_url_accurate.Baidu_Zhidao_URL_MOBILE(detail_id, keywords, domain)
#     pool.add_thread()
#
#
# def thread_pcmohupipei(yinqing,detail_id, keywords, domain, pool,):
#     # print('进入线程--thread_pcmohupipei--> ',' pc端 无链接',keywords, domain)
#     tid = ''
#     # print('detail_id=================> ',detail_id)
#     pc_fugai_pipei.Baidu_Zhidao_yuming_pc(tid, yinqing, keywords, domain, detail_id)
#     pool.add_thread()
#
#
# def thread_mobilemohupipei(search_engine, keywords, domain,detail_id, pool,):
#     # print('进入线程--thread_mobilemohupipei--> ','移动端 无链接',keywords, domain)
#     tid = ''
#     mobile_fugai_pipei.Baidu_Zhidao_yuming_mobile(tid, search_engine, keywords, domain, detail_id)
#     pool.add_thread()
#
#
# # 启动程序 - 重点词监控
# def func(detail_id, lianjie, keywords, search_engine, mohupipei, pool,):
#     # 去线程池里那一个线程，如果有，则池子里拿，如果没有，等直到有人归还线程到线程池
#     # print('当前线程数量 --------=========================>',threading.active_count())
#     thread_obj = pool.get_thread()
#     if lianjie:
#         if search_engine == '4':
#             # print('进入线程----> ','移动端 有链接',keywords)
#             thread_mobile_url = thread_obj(target=thread_mobileurl, args=(detail_id, keywords,lianjie,pool))
#             thread_mobile_url.start()
#
#
#         if search_engine == '1':
#             # print('进入线程----> ',' pc端 有链接',keywords)
#             thread_pc_url = thread_obj(target=thread_pcurl, args=(detail_id, keywords,lianjie,pool))
#             thread_pc_url.start()
#
#     else:
#         if search_engine == '4':
#             # print('进入线程----> ','移动端 无链接',keywords)
#             thread_mobile_mohupipei = thread_obj(target=thread_mobilemohupipei, args=(search_engine, detail_id, keywords,mohupipei,pool))
#             thread_mobile_mohupipei.start()
#
#         else:
#             # print('进入线程----> ',' pc端 无链接',keywords)
#             thread_pc_mohupipei = thread_obj(target=thread_pcmohupipei, args=(search_engine,detail_id, keywords,mohupipei,pool))
#             thread_pc_mohupipei.start()


# 收录 or 覆盖 查询 - 多线程部署

# class Thread_shoulu_Pool_Shoulu_Or_Fugai(object):
#
#     def __init__(self, max_num=5):
#         # 创建一个队列，队列里最多只能有5个数据
#         self.queue = queue.Queue(max_num)
#         # 在队列里填充线程类
#         for i in range(max_num):
#             self.queue.put(threading.Thread)
#
#     def get_or_thread(self):
#         # 去队列里取数据，queue特性，如果有，对列里那一个出来 如果没有，阻塞，
#         return self.queue.get()
#
#     def add_or_thread(self):
#         # 往队列里再添加一个线程类
#         self.queue.put(threading.Thread)

# gonggong_pool = Thread_shoulu_Pool_Shoulu_Or_Fugai(5)
# thread_shoulu_obj = gonggong_pool.get_or_thread()
from repeater_timing import timing_task
from threading_task_pc import zhongzhuanqi


# 运行程序 - 收录查询
def shoulu_func(huoqu_shoulu_time_stamp, set_url_data):
    shoulu_canshu = 1
    while True:
        now_time = int(time.time())
        time_stamp = now_time + 20
        sql = """select * from shoulu_Linshi_List where is_zhixing = '0' and time_stamp='{huoqu_shoulu_time_stamp}' and (shijianchuo is NULL or shijianchuo < '{time_stamp}') limit 1;""".format(
            time_stamp=now_time,
            huoqu_shoulu_time_stamp=huoqu_shoulu_time_stamp
        )
        objs_data = database_create_data.operDB(sql, 'select')
        for obj_data in objs_data['data']:
            tid = obj_data[0]
            search = obj_data[5]
            lianjie = obj_data[1]
            huoqu_shoulu_time_stamp = obj_data[3]
            if threading.active_count() <= 6:
                sql = """update shoulu_Linshi_List set shijianchuo ='{time_stamp}' where id = {detail_id};""".format(
                    time_stamp=time_stamp, detail_id=tid)
                database_create_data.operDB(sql, 'update')
                threadObj = threading.Thread(target=zhongzhuanqi.shouluChaxun, args=(lianjie, tid, search))
                threadObj.start()
            else:
                sleep(0.5)
                continue
        count_sql = """select count(id) from shoulu_Linshi_List where is_zhixing = '1' and time_stamp='{huoqu_shoulu_time_stamp}';""".format(
            huoqu_shoulu_time_stamp=huoqu_shoulu_time_stamp
        )
        count_objs = database_create_data.operDB(count_sql, 'select')
        if count_objs['data'][0][0] == set_url_data - 1:
            break


# 运行程序 - 覆盖查询
def fugai_func(huoqu_fugai_time_stamp, set_keyword_data):
    while True:
        # print('覆盖查询-----',threading.active_count())
        now_time = int(time.time())
        time_stamp = now_time + 30
        sql = """select * from fugai_Linshi_List where is_zhixing = '0' and time_stamp='{huoqu_fugai_time_stamp}' and (shijianchuo < '{time_stamp}' or  shijianchuo is NULL) limit 1;""".format(
            huoqu_fugai_time_stamp=huoqu_fugai_time_stamp,
            time_stamp=now_time)
        objs_data = database_create_data.operDB(sql, 'select')
        for obj_data in objs_data['data']:
            tid = obj_data[0]
            search = obj_data[3]
            keyword = obj_data[1]
            mohu_pipei = obj_data[6]
            if threading.active_count() <= 6:
                # 更改数据库时间戳 二十秒可执行下一次
                sql = """update fugai_Linshi_List set shijianchuo ='{time_stamp}' where id = '{id}';""".format(
                    time_stamp=time_stamp, id=tid)
                database_create_data.operDB(sql, 'update')
                # 启动线程
                fugai_thread4 = threading.Thread(target=zhongzhuanqi.fugaiChaxun,
                    args=(tid, search, keyword, mohu_pipei, huoqu_fugai_time_stamp))
                fugai_thread4.start()
            else:
                sleep(0.5)
                continue
        count_sql = """select count(id) from fugai_Linshi_List where is_zhixing = '1' and time_stamp='{huoqu_fugai_time_stamp}';""".format(
            huoqu_fugai_time_stamp=huoqu_fugai_time_stamp
        )
        count_objs = database_create_data.operDB(count_sql, 'select')
        if count_objs['data'][0][0] == set_keyword_data:
            break

