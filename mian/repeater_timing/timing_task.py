import sqlite3
from PyQt5.QtCore import QTimer
import sys
import datetime, time
import threading
import queue, schedule
from my_db import database_create_data
from time import sleep
# from threading_task_pc import mobile_fugai_pipei_baidu, mobile_url_accurate_baidu, pc_url_accurate_baidu, pc_fugai_pipei_baidu
from mian.threading_task_pc.pc_baidu import mobile_fugai_pipei_baidu, mobile_url_accurate_baidu, pc_fugai_pipei_baidu, pc_url_accurate_baidu
# 线程池
class ThreadPool(object):
    def __init__(self, max_num=5):
        # 创建一个队列，队列里最多只能有5个数据
        self.queue = queue.Queue(max_num)
        # 判断本队列 是否为空 为空
        self.queue1 = queue.Queue()
        # 在队列里填充线程类
        for i in range(max_num):
            self.queue.put(threading.Thread)

    def get_thread(self):
        # 去队列里取数据，queue特性，如果有，对列里那一个出来 如果没有，阻塞，
        self.queue1.put('1')
        return self.queue.get()

    def add_thread(self):
        # 往队列里再添加一个线程类
        self.queue.put(threading.Thread)
        self.queue1.get()

pool = ThreadPool(5)
# 重点词监控 - 多线程部署
def thread_pcurl(detail_id, keywords, domain, ):
    # print('进入线程--thread_pcurl--> ', ' pc端 有链接', keywords, domain, detail_id, threading.active_count())
    pc_url_accurate_baidu.Baidu_Zhidao_URL_PC(detail_id, keywords, domain)
    pool.add_thread()

def thread_mobileurl(detail_id, keywords, domain ):
    # print('进入线程--thread_mobileurl--> ', ' 移动端 有链接', keywords, domain, detail_id,  threading.active_count())
    mobile_url_accurate_baidu.Baidu_Zhidao_URL_MOBILE(detail_id, keywords, domain)
    pool.add_thread()

def thread_pcmohupipei(search_engine, detail_id, keywords, domain):
    # print('进入线程--thread_pcmohupipei--> ',' pc端 无链接',keywords, domain, detail_id, threading.active_count())
    pc_fugai_pipei_baidu.Baidu_Zhidao_yuming_pc(search_engine, keywords, domain, detail_id)
    pool.add_thread()

def thread_mobilemohupipei(search_engine, detail_id, keywords, domain):
    # print('进入线程--thread_mobilemohupipei--> ','移动端 无链接',keywords, domain, detail_id, threading.active_count())
    mobile_fugai_pipei_baidu.Baidu_Zhidao_yuming_mobile(search_engine, keywords, domain, detail_id)
    pool.add_thread()


# 启动程序 - 重点词监控
# def func(detail_id, lianjie, keywords, search_engine, mohupipei,):
#     # print('启动程序---------------------> ',detail_id, lianjie, keywords, search_engine, mohupipei)
#     # 去线程池里那一个线程，如果有，则池子里拿，如果没有，等直到有人归还线程到线程池
#     # print('当前线程数量 --------=========================>',threading.active_count())
#     thread_obj = pool.get_thread()
#     if lianjie:
#         if search_engine == '4':
#             # print('进入线程----> ','移动端 有链接',keywords)
#             thread_mobile_url = thread_obj(target=thread_mobileurl, args=(detail_id, keywords,lianjie))
#             thread_mobile_url.start()
#
#
#         if search_engine == '1':
#             # print('进入线程----')
#             thread_pc_url = thread_obj(target=thread_pcurl, args=(detail_id, keywords,lianjie))
#             thread_pc_url.start()
#
#     else:
#         if search_engine == '4':
#             # print('进入线程----> ','移动端 无链接',keywords)
#             thread_mobile_mohupipei = thread_obj(target=thread_mobilemohupipei, args=(search_engine, detail_id, keywords,mohupipei))
#             thread_mobile_mohupipei.start()
#
#         else:
#             # print('进入线程----> ',' pc端 无链接',keywords)
#             thread_pc_mohupipei = thread_obj(target=thread_pcmohupipei, args=(search_engine,detail_id, keywords,mohupipei))
#             thread_pc_mohupipei.start()




# 定时器一




def get_task_list(data=None):
    # print('执行 get_task_list')
    xiaoyu_dengyu_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
    start_time = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
    task_id = ''
    sql = ''
    if data:
        sql = """select id,next_datetime from task_List where qiyong_status = '1' and id = '{}';""".format(data)
    else:
        sql = """select id,next_datetime from task_List where next_datetime <='{xiaoyu_dengyu_date}' and qiyong_status = '1' limit 1;""".format(
        xiaoyu_dengyu_date=xiaoyu_dengyu_date)
    objs = database_create_data.operDB(sql, 'select')
    if objs['data']:
        data_id = objs['data'][0][0]
        select_sql = """select id from task_Detail where tid='{data}'""".format(data=data_id)
        select_objs = database_create_data.operDB(select_sql, 'select')
        if select_objs['data']:
            next_time = objs['data'][0][1]
            next_datetime = datetime.datetime.strptime(next_time, '%Y-%m-%d %H:%M:%S')
            update_status_sql = """update task_List set task_status = '0', zhixing = '1' where id = '{}'""".format(data_id)
            database_create_data.operDB(update_status_sql, 'update')
            if next_datetime.strftime('%Y-%m-%d') <= datetime.datetime.today().strftime('%Y-%m-%d'):
                # 修改下一次执行时间
                next_datetime_addoneday = (next_datetime + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                next_sql = """update task_List set next_datetime = '{next_datetime}' where id = '{id}';""".format(next_datetime=next_datetime_addoneday,id=data_id)
                database_create_data.operDB(next_sql, 'update')
            # 修改 任务详情为 启用
            sql_status = """update task_Detail set is_perform = '1', task_start_time = '{time}' where tid = '{task_id}';""".format(time=start_time,task_id=data_id)
            # print('sql_status===========> ',sql_status)
            database_create_data.operDB(sql_status, 'update')
        else:
            update_sql = """update task_List set qiyong_status = '0' where id = '{data_id}';""".format(data_id=data_id)
            database_create_data.operDB(update_sql, 'update')
timer_flag = False


# 定时器二
def dingshi_timer():
    # print('执行 dingshi_timer')
    global timer_flag
    if timer_flag:
        return
    else:
        timer_flag = True
    sql = """select * from task_Detail where is_perform='1';"""
    is_run_flag = False     # 表示是否有任务要运行
    objs_list = database_create_data.operDB(sql, 'select')
    if objs_list['data']:
        for obj in objs_list['data']:
            detail_id = obj[0]
            tid = obj[1]
            search_engine = obj[2]
            lianjie = obj[3]
            keywords = obj[4]
            mohupipei = obj[5]
            # create_time = obj[6]
            # task_start_time = obj[7]
            time_stamp_obj = obj[8]
            shijianchuo = time.time()
            now_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
            if time_stamp_obj:
                time_stamp_obj = int(time_stamp_obj)
                if time_stamp_obj < int(shijianchuo):
                    is_run_flag = True
            else:
                time_stamp = int(shijianchuo) + 300
                sql = """update task_Detail set time_stamp ='{time_stamp}' where id = {detail_id};""".format(
                    time_stamp=time_stamp, detail_id=detail_id)
                database_create_data.operDB(sql, 'update')
                is_run_flag = True
            if is_run_flag:
                print('time_stamp_obj --------- <> ',time_stamp_obj, 'detail_id =======> ',detail_id)
                thread_obj = pool.get_thread()
                if lianjie:
                    if search_engine == '4':
                        print('进入线程----> ','移动端 有链接',keywords)
                        thread_mobile_url = thread_obj(target=thread_mobileurl, args=(detail_id, keywords, lianjie))
                        thread_mobile_url.start()

                    if search_engine == '1':
                        print('进入线程----','移动端 有链接',keywords)
                        thread_pc_url = thread_obj(target=thread_pcurl, args=(detail_id, keywords, lianjie))
                        thread_pc_url.start()

                else:
                    if search_engine == '4':
                        print('进入线程----> ','移动端 无链接',keywords, detail_id)
                        thread_mobile_mohupipei = thread_obj(target=thread_mobilemohupipei,
                            args=(search_engine, detail_id, keywords, mohupipei))
                        thread_mobile_mohupipei.start()

                    else:
                        print('进入线程----> ',' pc端 无链接',keywords, detail_id)
                        thread_pc_mohupipei = thread_obj(target=thread_pcmohupipei,
                            args=(search_engine, detail_id, keywords, mohupipei))
                        thread_pc_mohupipei.start()

    # 所有线程执行完毕 只剩主线程 则退出
    while True:
        # if threading.active_count() == 1:
        if ThreadPool().queue1.empty():
            break
        else:
            time.sleep(1)
    timer_flag = False


# 立即监控 多线程执行立即监控id
def lijijiankong(json_data):
    # print('立即监控id ---- >',json_data)
    for data in json_data:
        if threading.active_count() <= 6:
            jiankong = threading.Thread(target=get_task_list, args=(data, ))
            jiankong.start()
        else:
            continue



# 启动定时器
def run():
    schedule.every(30).seconds.do(get_task_list)
    schedule.every(10).seconds.do(dingshi_timer)
    while True:
        schedule.run_pending()

