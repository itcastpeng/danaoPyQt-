import sqlite3
from PyQt5.QtCore import QTimer
import datetime, time
import threading
import queue, schedule
from mian.my_db import database_create_data
from time import sleep
from mian.threading_task_pc import mobile_fugai_pipei_baidu, mobile_url_accurate_baidu, pc_url_accurate_baidu, pc_fugai_pipei_baidu
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
    # print('进入线程--thread_pcurl--> ', ' pc端 有链接', keywords, domain)
    pc_url_accurate_baidu.Baidu_Zhidao_URL_PC(detail_id, keywords, domain)
    pool.add_thread()


def thread_mobileurl(detail_id, keywords, domain, ):
    # print('进入线程--thread_mobileurl--> ', ' 移动端 有链接', keywords, domain)
    mobile_url_accurate_baidu.Baidu_Zhidao_URL_MOBILE(detail_id, keywords, domain)
    pool.add_thread()


def thread_pcmohupipei(yinqing,detail_id, keywords, domain, ):
    # print('进入线程--thread_pcmohupipei--> ',' pc端 无链接',keywords, domain)
    tid = ''
    # print('detail_id=================> ',detail_id)
    pc_fugai_pipei_baidu.Baidu_Zhidao_yuming_pc(tid, yinqing, keywords, domain, detail_id)
    pool.add_thread()


def thread_mobilemohupipei(search_engine, keywords, domain,detail_id, ):
    # print('进入线程--thread_mobilemohupipei--> ','移动端 无链接',keywords, domain)
    tid = ''
    mobile_fugai_pipei_baidu.Baidu_Zhidao_yuming_mobile(tid, search_engine, keywords, domain, detail_id)
    pool.add_thread()


# 启动程序 - 重点词监控
def func(detail_id, lianjie, keywords, search_engine, mohupipei,):
    print('启动程序---------------------> ',detail_id, lianjie, keywords, search_engine, mohupipei)
    # 去线程池里那一个线程，如果有，则池子里拿，如果没有，等直到有人归还线程到线程池
    # print('当前线程数量 --------=========================>',threading.active_count())
    thread_obj = pool.get_thread()
    if lianjie:
        if search_engine == '4':
            # print('进入线程----> ','移动端 有链接',keywords)
            thread_mobile_url = thread_obj(target=thread_mobileurl, args=(detail_id, keywords,lianjie))
            thread_mobile_url.start()


        if search_engine == '1':
            # print('进入线程----')
            thread_pc_url = thread_obj(target=thread_pcurl, args=(detail_id, keywords,lianjie))
            thread_pc_url.start()

    else:
        if search_engine == '4':
            # print('进入线程----> ','移动端 无链接',keywords)
            thread_mobile_mohupipei = thread_obj(target=thread_mobilemohupipei, args=(search_engine, detail_id, keywords,mohupipei))
            thread_mobile_mohupipei.start()

        else:
            # print('进入线程----> ',' pc端 无链接',keywords)
            thread_pc_mohupipei = thread_obj(target=thread_pcmohupipei, args=(search_engine,detail_id, keywords,mohupipei))
            thread_pc_mohupipei.start()




lock_file = 'C:/pycharm zh/danaoPyQt/mian/my_db/my_sqlite3.lock'
db_file =  'C:/pycharm zh/danaoPyQt/mian/my_db/my_sqlite.db'

# 定时器一
def get_task_list(data=None):
    xiaoyu_dengyu_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
    start_time = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
    task_id = ''
    sql = ''
    if data:
        sql = """select id,next_datetime from task_List where qiyong_status = '1' and id = '{}';""".format(data)
    else:
        sql = """select id,next_datetime from task_List where next_datetime <='{xiaoyu_dengyu_date}' and qiyong_status = '1' limit 1;""".format(
        xiaoyu_dengyu_date=xiaoyu_dengyu_date)
    objs = database_create_data.operDB(sql, lock_file, db_file, 'select')
    print('进入定时器一')
    if objs['data']:
        print('进入---------------------')
        data_id = objs['data'][0][0]
        select_sql = """select id from task_Detail where tid='{data}'""".format(data=data_id)
        select_objs = database_create_data.operDB(select_sql, lock_file, db_file, 'select')
        if select_objs['data']:
            next_time = objs['data'][0][1]
            next_datetime = datetime.datetime.strptime(next_time, '%Y-%m-%d %H:%M:%S')
            update_status_sql = """update task_List set task_status = '0', zhixing = '1' where id = '{}'""".format(data_id)
            database_create_data.operDB(update_status_sql, lock_file, db_file, 'update')
            if next_datetime.strftime('%Y-%m-%d') <= datetime.datetime.today().strftime('%Y-%m-%d'):
                # 修改下一次执行时间
                next_datetime_addoneday = (next_datetime + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                next_sql = """update task_List set next_datetime = '{next_datetime}' where id = '{id}';""".format(next_datetime=next_datetime_addoneday,id=data_id)
                database_create_data.operDB(next_sql, lock_file, db_file, 'update')
            # 修改 任务详情为 启用
            sql_status = """update task_Detail set is_perform = '1', task_start_time = '{time}' where tid = '{task_id}';""".format(time=start_time,task_id=data_id)
            database_create_data.operDB(sql_status, lock_file, db_file, 'update')
        else:
            print('进入else')
            update_sql = """update task_List set qiyong_status = '0' where id = '{data_id}';""".format(data_id=data_id)
            database_create_data.operDB(update_sql, lock_file, db_file, 'update')
timer_flag = False


# 定时器二
def dingshi_timer():
    global timer_flag
    if timer_flag:
        return
    else:
        timer_flag = True
    shijianchuo = time.time()
    now_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
    sql = """select * from task_Detail where is_perform=1;"""
    is_run_flag = False     # 表示是否有任务要运行
    objs_list = database_create_data.operDB(sql, lock_file, db_file, 'select')
    if objs_list['data']:
        for obj in objs_list['data']:
            detail_id = obj[0]
            tid = obj[1]
            search_engine = obj[2]
            lianjie = obj[3]
            keywords = obj[4]
            mohupipei = obj[5]
            create_time = obj[6]
            task_start_time = obj[7]
            time_stamp_obj = obj[8]
            if not time_stamp_obj:
                time_stamp = int(shijianchuo) + 300
                sql = """update task_Detail set time_stamp ='{time_stamp}' where id = {detail_id};""".format(
                    time_stamp=time_stamp, detail_id=detail_id)
                database_create_data.operDB(sql, lock_file, db_file, 'update')
                is_run_flag = True
            else:
                time_stamp_obj = int(time_stamp_obj)
                if time_stamp_obj < int(shijianchuo):
                    is_run_flag = True
            if is_run_flag:
                func(detail_id, lianjie, keywords, search_engine, mohupipei)

    # 所有线程执行完毕 只剩主线程 则退出
    while True:
        # if threading.active_count() == 1:
        if ThreadPool().queue1.empty():
            break
        else:
            time.sleep(1)
    timer_flag = False

# 启动定时器
def run():
    schedule.every(30).seconds.do(get_task_list)
    schedule.every(10).seconds.do(dingshi_timer)
    while True:
        # print('启动定时器')
        schedule.run_pending()













# pool = ThreadPool(2)
# def get_task_list(data=None):
#     xiaoyu_dengyu_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
#     start_time = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
#     task_id = ''
#     sql = ''
#     if data:
#         sql = """select id,next_datetime from task_List where id = '{}' and qiyong_status = '1' ;""".format(data)
#     else:
#         sql = """select  id,next_datetime from task_List where next_datetime <='{xiaoyu_dengyu_date}' and qiyong_status = '1' limit 1;""".format(
#         xiaoyu_dengyu_date=xiaoyu_dengyu_date)
#     objs = database_create_data.operDB(sql, 'select')
#     if objs['data']:
#         task_id = objs['data'][0][0]
#         next_time = objs['data'][0][1]
#         next_datetime = datetime.datetime.strptime(next_time, '%Y-%m-%d %H-%M-%S')
#         if next_datetime.strftime('%Y-%m-%d') <= datetime.datetime.today().strftime('%Y-%m-%d'):
#             # 修改下一次执行时间
#             next_datetime_addoneday = (next_datetime + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H-%M-%S')
#             next_sql = """update task_List set next_datetime = '{next_datetime}' where id = '{id}';""".format(next_datetime=next_datetime_addoneday,id=task_id)
#             database_create_data.operDB(next_sql, 'update')
#         # 修改 任务详情为 启用
#         sql_status = """update task_Detail set is_perform = '1', task_start_time = '{time}' where tid = '{task_id}';""".format(time=start_time,task_id=task_id)
#         database_create_data.operDB(sql_status, 'update')
#
#
# timer_flag = False
# def dingshi_timer():
#     global timer_flag, pool
#     print('线程 数量-=====================-----> ',threading.active_count(), '进入 --dingshi_timer--->', timer_flag )
#     if timer_flag:
#         return
#     else:
#         timer_flag = True
#     shijianchuo = time.time()
#     now_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
#     sql = """select * from task_Detail where is_perform=1;"""
#     is_run_flag = False     # 表示是否有任务要运行
#     objs_list = database_create_data.operDB(sql, 'select')
#     if objs_list['data']:
#         for obj in objs_list['data']:
#             detail_id = obj[0]
#             tid = obj[1]
#             search_engine = obj[2]
#             lianjie = obj[3]
#             keywords = obj[4]
#             mohupipei = obj[5]
#             create_time = obj[6]
#             task_start_time = obj[7]
#             time_stamp_obj = obj[8]
#             if not time_stamp_obj:
#                 time_stamp = int(shijianchuo) + 300
#                 sql = """update task_Detail set time_stamp ='{time_stamp}' where id = {detail_id};""".format(
#                     time_stamp=time_stamp, detail_id=detail_id)
#                 database_create_data.operDB(sql, 'update')
#                 is_run_flag = True
#             else:
#                 time_stamp_obj = int(time_stamp_obj)
#                 if time_stamp_obj < int(shijianchuo):
#                     is_run_flag = True
#             if is_run_flag:
#                 threading_task.func(detail_id, lianjie, keywords, search_engine, mohupipei, pool)
#
#     # 所有线程执行完毕 只剩主线程 则退出
#     while True:
#         if threading.active_count() == 1:
#             break
#         else:
#             time.sleep(1)
#     timer_flag = False
# timer = QTimer(self)
# timer2 = QTimer(self)
# timer.timeout.connect(timing_task.get_task_list)
# timer2.timeout.connect(timing_task.dingshi_timer)
# 定时 1s == 1000
# timer.start(30000)
# timer2.start(2000)

