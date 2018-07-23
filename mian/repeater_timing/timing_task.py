import sqlite3
from PyQt5.QtCore import QTimer
import datetime, time
from mian.threading_task_pc import threading_task
import threading
import queue

from mian.my_db import database_create_data


class ThreadPool(object):

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




class repeater_timing_task():
    def __init__(self):
        self.timer_flag = False
        # 初始一个定时器
        self.timer = QTimer()
        # 计时结束调用operate()方法 设置时间 间隔 并启动定时器
        self.timer.timeout.connect(self.dingshi_timer)
        self.timer.start(2000)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.get_task_list)
        self.timer2.start(2000)
        self.pool = ThreadPool(5)

        self.get_task_list()
        self.dingshi_timer()
        # if datas:
        #     self.function_pc_task()


    def get_task_list(self):
        now_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
        conn = sqlite3.connect('../my_db/my_sqlite.db')
        cursor = conn.cursor()
        sql = """select  id,next_datetime from task_List where next_datetime <='{}' and qiyong_status = 1 limit 0,1;""".format(now_date)
        print(sql)
        objs = cursor.execute(sql)
        obj = list(objs)
        if obj:
            task_id = obj[0][0]
            task_next_datetime = obj[0][1]
            if task_id:
                sql = """update task_Detail set is_perform = 1 where tid = {};""".format(task_id)
                print(sql)
                database_create_data.operDB(sql, 'update')
        conn.commit()
        conn.close()


    def dingshi_timer(self):
        if self.timer_flag:
            return
        else:
            self.timer_flag = True
        shijianchuo = time.time()
        now_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
        conn = sqlite3.connect('../my_db/my_sqlite.db')
        cursor = conn.cursor()
        sql = """select * from task_Detail where is_perform=1;"""
        print('sql -->', sql)
        is_run_flag = False     # 表示是否有任务要运行
        objs_list = database_create_data.operDB(sql, 'select')
        conn.commit()
        conn.close()
        if objs_list:
            print('objs_list============> ',objs_list)
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
                    time_stamp = int(shijianchuo) + 30
                    sql = """update task_Detail set time_stamp ='{time_stamp}' where id = {detail_id};""".format(
                        time_stamp=time_stamp, detail_id=detail_id)
                    database_create_data.operDB(sql, 'update')
                    is_run_flag = True

                else:
                    time_stamp_obj = int(time_stamp_obj)
                    if time_stamp_obj < int(shijianchuo):
                        is_run_flag = True
                if is_run_flag:
                    threading_task.func(detail_id, lianjie, keywords, search_engine, mohupipei, self.pool)

        while True:
            if threading.active_count() == 1:
                break
            else:
                time.sleep(1)
        self.timer_flag = False



if __name__ == '__main__':
    repeater_timing_task()

    # 如果用户直接点击 则传参为 单个或多个任务id
    # def function_pc_task(self):
    #     print(self.datas)
    #     conn = sqlite3.connect('./my_db/my_sqlite.db')
    #     cursor = conn.cursor()
    #     for data in self.datas.split(','):
    #         sql = """select * from task_Detail where tid='{}';""".format(data)
    #         cursor.execute(sql)
    #         for obj in cursor:
    #             tid = obj[1]
    #             search_engine = obj[2]
    #             lianjie = obj[3]
    #             keywords = obj[4]
    #             mohupipei = obj[5]
    #             create_time = obj[6]
    #             task_start_time = obj[7]
    #
    #
    # def dingshi_timer(self):
    #     print('====================')
    #     now_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
    #     print('__file__ -->', __file__)
    #     conn = sqlite3.connect('../my_db/my_sqlite.db')
    #     cursor = conn.cursor()
    #     # print('查询任务表 所有下一次查询时间')
    #     sql = """select  id,next_datetime from task_List where next_datetime <='{}' ;""".format(now_date)
    #     objs = cursor.execute(sql)
    #     data_list = []
    #     for obj in objs:
    #         task_id = obj[0]
    #         task_next_datetime = obj[1]
    #         print('task_next_datetime--------------> ',task_next_datetime)
    #         now_date = datetime.datetime.today().strftime('%Y-%m-%d 23-59-59')
    #         task_next_datetime = datetime.datetime.strptime(task_next_datetime,'%Y-%m-%d %H-%M-%S')
    #         now_date = datetime.datetime.strptime(now_date,'%Y-%m-%d %H-%M-%S')
    #         if task_next_datetime <= now_date:
    #             print('满足条件---------进入if')
    #             # print('更新 详情数据 执行为 True')
    #             sql = """update task_Detail set is_perform=1 where tid={};""".format(task_id)
    #             # print(sql)
    #             cursor.execute(sql)
    #
    #             # print('更新任务表 下一次执行时间')
    #             next_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H-%M-%S')
    #             sql = """update task_List set next_datetime='{next_date}' where id = {task_id};""".format(next_date=next_date,task_id=task_id)
    #             cursor.execute(sql)
    #
    #             # print('查询详情 执行为True的 数据 ')
    #             sql = """select  * from task_Detail where tid='{}' and is_perform=1;""".format(task_id)
    #             cursor.execute(sql)
    #             for obj in cursor:
    #                 tid = obj[1]
    #                 search_engine = obj[2]
    #                 lianjie = obj[3]
    #                 keywords = obj[4]
    #                 mohupipei = obj[5]
    #                 create_time = obj[6]
    #                 task_start_time = obj[7]
    #
    #                 # if lianjie:
    #                 #     if search_engine == '4':
    #                 #         # print('以链接 当做条件---->',lianjie ,'移动端关键词---> ', keywords,'搜索引擎--->', search_engine)
    #                 #         mohupipei = ''
    #                 #         threading_task.func(lianjie, keywords, search_engine, mohupipei)
    #                 #     if search_engine == '1':
    #                 #         # print('以链接 当做条件---->',lianjie ,'pc端关键词---> ', keywords,'搜索引擎--->', search_engine)
    #                 #         mohupipei = ''
    #                 #         threading_task.func(lianjie, keywords, search_engine, mohupipei)
    #                 # else:
    #                 #     if search_engine == '4':
    #                 #         # print('自带匹配条件---> ', mohupipei, '移动端关键词---> ', keywords,'搜索引擎--->', search_engine)
    #                 #         lianjie = ''
    #                 #         threading_task.func(lianjie, keywords, search_engine, mohupipei)
    #                 #     else:
    #                 #         # print('自带匹配条件---> ', mohupipei, 'pc端关键词---> ',keywords,'搜索引擎--->', search_engine)
    #                 #         lianjie = ''
    #                 #         threading_task.func(lianjie, keywords, search_engine, mohupipei)
    #
    #
    #                 print('修改执行状态为False')
    #                 sql = """update task_Detail set is_perform=0 where id={}""".format(obj[0])
    #                 cursor.execute(sql)
    #     conn.commit()
    #     conn.close()
