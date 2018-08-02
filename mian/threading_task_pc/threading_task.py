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






lock_file = 'C:/pycharm zh/danaoPyQt/mian/my_db/my_sqlite3.lock'
db_file =  'C:/pycharm zh/danaoPyQt/mian/my_db/my_sqlite.db'
shijianchuo = time.time()


# 收录
# def shoulu_pc(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu):
#     print('进入-------------')
#     pc_url_accurate_baidu.shoulu_chaxun(lianjie, search, huoqu_shoulu_time_stamp, shoulu_canshu)
#     gonggong_pool.add_thread()
#
# def shoulu_mobile(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu):
#     mobile_url_accurate_baidu.shoulu_chaxun(lianjie, search, huoqu_shoulu_time_stamp, shoulu_canshu)
#     gonggong_pool.add_thread()


# 运行程序 - 收录查询
def shoulu_func(huoqu_shoulu_time_stamp):
    print('=======================收录查询', huoqu_shoulu_time_stamp)
    shoulu_canshu = 1
    time_stamp = int(shijianchuo) + 300
    while True:
        sql = """select * from shoulu_Linshi_List where is_zhixing = '0' and time_stamp='{huoqu_shoulu_time_stamp}' and shijianchuo < '{time_stamp}' or is_zhixing='0' and time_stamp='{huoqu_shoulu_time_stamp}' and shijianchuo is NULL;""".format(
            time_stamp=time_stamp,huoqu_shoulu_time_stamp=huoqu_shoulu_time_stamp)
        objs_data = database_create_data.operDB(sql, lock_file, db_file, 'select')
        if objs_data['data']:
            for obj in objs_data['data']:
                time_stamp_panduan = obj[9]
                if not time_stamp_panduan:
                    search = obj[5]
                    lianjie = obj[1]
                    huoqu_shoulu_time_stamp = obj[3]
                    id = obj[0]
                    if threading.active_count() <= 5:
                        sql = """update fugai_Linshi_List set shijianchuo ='{time_stamp}' where id = {detail_id};""".format(
                            time_stamp=time_stamp, detail_id=id)
                        database_create_data.operDB(sql, lock_file, db_file, 'update')
                        if str(search) == '1':
                            pc_url_accurate_baidu.shoulu_chaxun(lianjie, search, huoqu_shoulu_time_stamp, shoulu_canshu)
                        else:
                            mobile_url_accurate_baidu.shoulu_chaxun(lianjie, search, huoqu_shoulu_time_stamp, shoulu_canshu)
                    else:
                        sleep(0.5)
                        continue
        else:
            break


# 运行程序 - 覆盖查询
def fugai_func(huoqu_fugai_time_stamp):
    print('进入')
    fugai_canshu = 1
    detail_id = ''
    time_stamp = int(shijianchuo) + 300
    while True:
        sql = """select * from fugai_Linshi_List where is_zhixing = '0' and time_stamp='{huoqu_fugai_time_stamp}' and shijianchuo < '{time_stamp}' or is_zhixing = '0' and time_stamp='{huoqu_fugai_time_stamp}' and shijianchuo is NULL ;""".format(
            huoqu_fugai_time_stamp=huoqu_fugai_time_stamp,time_stamp=time_stamp)
        objs_data = database_create_data.operDB(sql, lock_file, db_file, 'select')
        if objs_data['data']:
            for obj_data in objs_data['data']:
                time_stamp_obj = obj_data[12]
                if not time_stamp_obj:
                    id = obj_data[0]
                    yinqing = obj_data[3]
                    keyword = obj_data[1]
                    mohu_pipei = obj_data[6]
                    if threading.active_count() <= 5:
                        sql = """update fugai_Linshi_List set shijianchuo ='{time_stamp}' where id = '{id}';""".format(
                            time_stamp=time_stamp, id=id)
                        database_create_data.operDB(sql, lock_file, db_file, 'update')
                        if yinqing == '4':
                            fugai_thread4 = threading.Thread(target=mobile_fugai_pipei_baidu.Baidu_Zhidao_yuming_mobile,
                                args=(id, yinqing, keyword, mohu_pipei, detail_id, huoqu_fugai_time_stamp, fugai_canshu))
                            fugai_thread4.start()
                        else:
                            fugai_thread1 = threading.Thread(target=pc_fugai_pipei_baidu.Baidu_Zhidao_yuming_pc,
                                args=(id, yinqing, keyword, mohu_pipei, detail_id, huoqu_fugai_time_stamp, fugai_canshu))
                            fugai_thread1.start()
                    else:
                        sleep(0.5)
                        continue
        else:
            break



        # select_limit = """select * from fugai_Linshi_List where shijianchuo < '{time_stamp}' and is_zhixing = '0' limit 1""".format(time_stamp=shijianchuo)
        # objs = database_create_data.operDB(select_limit, lock_file, db_file, 'select')
        # for obj in objs['data']:
        #     id = obj[0]
        #     yinqing = obj[3]
        #     keyword = obj[1]
        #     mohu_pipei = obj[6]
        #     huoqu_fugai_time_stamp = obj[7]
        #     print('线程数量---------------------- > ',threading.active_count(), id, keyword)
        #     if threading.active_count() <= 5:
        #         if yinqing == '1':
        #             fugai_thread1 = threading.Thread(target=pc_fugai_pipei_baidu.Baidu_Zhidao_yuming_pc, args=(id, yinqing, keyword, mohu_pipei, detail_id, huoqu_fugai_time_stamp, fugai_canshu))
        #             fugai_thread1.start()
        #         else:
        #             fugai_thread2 = threading.Thread(target=mobile_fugai_pipei_baidu.Baidu_Zhidao_yuming_mobile, args=(id, yinqing, keyword, mohu_pipei, detail_id, huoqu_fugai_time_stamp, fugai_canshu))
        #             fugai_thread2.start()
        #     else:
        #         print('continue')
        #         continue
















# 收录
# def shoulu_pc(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu):
#     print('进入-------------')
#     pc_url_accurate_baidu.shoulu_chaxun(lianjie, search, huoqu_shoulu_time_stamp, shoulu_canshu)
#     gonggong_pool.add_thread()
#
# def shoulu_mobile(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu):
#     mobile_url_accurate_baidu.shoulu_chaxun(lianjie, search, huoqu_shoulu_time_stamp, shoulu_canshu)
#     gonggong_pool.add_thread()
#
#
# # 运行程序 - 收录查询
# def shoulu_func():
#     shoulu_canshu = 1
#     flag = False
#     sql = """select * from shoulu_Linshi_List where is_zhixing = '0';"""
#     objs_data = database_create_data.operDB(sql, lock_file, db_file, 'select')
#     for obj in objs_data['data']:
#         search = obj[5]
#         lianjie = obj[1]
#         huoqu_shoulu_time_stamp = obj[3]
#         time_stamp_panduan = obj[9]
#         id = obj[0]
#         print('引擎-----------> ',search, '链接--------> ',huoqu_shoulu_time_stamp)
#         if not time_stamp_panduan:
#             time_stamp = int(shijianchuo) + 300
#             sql = """update fugai_Linshi_List set shijianchuo ='{time_stamp}' where id = {detail_id};""".format(
#                 time_stamp=time_stamp, detail_id=id)
#             database_create_data.operDB(sql, lock_file, db_file, 'update')
#             flag = True
#         else:
#             time_stamp_obj = int(time_stamp_panduan)
#             if time_stamp_obj < int(shijianchuo):
#                 flag = False
#         if flag:
#             if str(search) == '1':
#                 shoulu_pc_obj = thread_shoulu_obj(target=shoulu_pc, args=(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu))
#                 shoulu_pc_obj.start()
#             else:
#                 thread_mobile_url = thread_shoulu_obj(target=shoulu_mobile, args=(search, lianjie, huoqu_shoulu_time_stamp, shoulu_canshu))
#                 thread_mobile_url.start()




# 覆盖
# def fugai_pc(id, yinqing, keyword, mohu_pipei, huoqu_fugai_time_stamp, fugai_canshu):
#     detail_id = ''
#     pc_fugai_pipei_baidu.Baidu_Zhidao_yuming_pc(id, yinqing, keyword, mohu_pipei, detail_id, huoqu_fugai_time_stamp,fugai_canshu)
#     gonggong_pool.add_thread()
#
# def fugai_mobile(id, yinqing, keyword, mohu_pipei, huoqu_fugai_time_stamp, fugai_canshu):
#     detail_id = ''
#     mobile_fugai_pipei_baidu.Baidu_Zhidao_yuming_mobile(id, yinqing, keyword, mohu_pipei, detail_id, huoqu_fugai_time_stamp, fugai_canshu)
#     gonggong_pool.add_thread()







# 运行程序 - 覆盖查询