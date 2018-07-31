from multiprocessing import Queue
import sqlite3, os, sys, json, re, time
from mian.threading_task_pc import mobile_fugai_pipei_baidu, mobile_url_accurate_baidu, pc_url_accurate_baidu, pc_fugai_pipei_baidu
from time import sleep
import threading
from mian.my_db import database_create_data
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
from  mian.repeater_timing import timing_task

shijianchuo = time.time()
gonggong_pool = timing_task.pool
thread_shoulu_obj = gonggong_pool.get_thread()
lock_file = './my_db/my_sqlite3.lock'
db_file =  './my_db/my_sqlite.db'
# 收录
def shoulu_pc(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu):
    print('进入-------------')
    pc_url_accurate_baidu.shoulu_chaxun(lianjie, search, huoqu_shoulu_time_stamp, shoulu_canshu)
    gonggong_pool.add_thread()

def shoulu_mobile(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu):
    mobile_url_accurate_baidu.shoulu_chaxun(lianjie, search, huoqu_shoulu_time_stamp, shoulu_canshu)
    gonggong_pool.add_thread()

# 运行程序 - 收录查询
def shoulu_func():
    shoulu_canshu = 1
    flag = False
    sql = """select * from shoulu_Linshi_List where is_zhixing = '0';"""
    objs_data = database_create_data.operDB(sql, lock_file, db_file, 'select')
    for obj in objs_data['data']:
        search = obj[5]
        lianjie = obj[1]
        huoqu_shoulu_time_stamp = obj[3]
        time_stamp_panduan = obj[9]
        id = obj[0]
        print('引擎-----------> ',search, '链接--------> ',huoqu_shoulu_time_stamp)
        if not time_stamp_panduan:
            time_stamp = int(shijianchuo) + 300
            sql = """update fugai_Linshi_List set shijianchuo ='{time_stamp}' where id = {detail_id};""".format(
                time_stamp=time_stamp, detail_id=id)
            database_create_data.operDB(sql, lock_file, db_file, 'update')
            flag = True
        else:
            time_stamp_obj = int(time_stamp_panduan)
            if time_stamp_obj < int(shijianchuo):
                flag = False
        if flag:
            if str(search) == '1':
                shoulu_pc_obj = thread_shoulu_obj(target=shoulu_pc, args=(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu))
                shoulu_pc_obj.start()
            else:
                thread_mobile_url = thread_shoulu_obj(target=shoulu_mobile, args=(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu))
                thread_mobile_url.start()


# 覆盖
def fugai_pc(tid, yinqing, keyword, mohu_pipei, huoqu_fugai_time_stamp, fugai_canshu):
    # print('进入pc  端fugai_canshu ===========/ ',fugai_canshu)
    detail_id = ''
    pc_fugai_pipei_baidu.Baidu_Zhidao_yuming_pc(tid, yinqing, keyword, mohu_pipei, detail_id, huoqu_fugai_time_stamp,fugai_canshu)
    gonggong_pool.add_thread()

def fugai_mobile(tid, yinqing, keyword, mohu_pipei, huoqu_fugai_time_stamp, fugai_canshu):
    # print('进入 覆盖 移动端')
    detail_id = ''
    mobile_fugai_pipei_baidu.Baidu_Zhidao_yuming_mobile(tid, yinqing, keyword, mohu_pipei, detail_id, huoqu_fugai_time_stamp, fugai_canshu)
    gonggong_pool.add_thread()

# 运行程序 - 覆盖查询
def fugai_func():
    fugai_canshu = 1
    sql = """select * from fugai_Linshi_List where is_zhixing = '0';"""
    objs_data = database_create_data.operDB(sql, lock_file, db_file, 'select')
    for obj in objs_data['data']:
        yinqing = obj[3]
        keyword = obj[1]
        mohu_pipei = obj[6]
        tid = obj[0]
        huoqu_fugai_time_stamp = obj[7]
        time_stamp_panduan = obj[12]

        flag = False
        if not time_stamp_panduan:
            time_stamp = int(shijianchuo) + 300
            sql = """update fugai_Linshi_List set shijianchuo ='{time_stamp}' where id = {detail_id};""".format(
                time_stamp=time_stamp, detail_id=tid)
            database_create_data.operDB(sql, lock_file, db_file, 'update')
            flag = True
        else:
            time_stamp_obj = int(time_stamp_panduan)
            if time_stamp_obj < int(shijianchuo):
                flag = False
        if flag:
            if yinqing == '1':
                shoulu_pc_obj = thread_shoulu_obj(target=fugai_pc, args=(tid, yinqing, keyword, mohu_pipei, huoqu_fugai_time_stamp, fugai_canshu))
                shoulu_pc_obj.start()
            else:
                thread_mobile_url = thread_shoulu_obj(target=fugai_mobile, args=(tid, yinqing, keyword, mohu_pipei, huoqu_fugai_time_stamp, fugai_canshu))
                thread_mobile_url.start()




