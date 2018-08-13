from multiprocessing import Queue
import sqlite3, os, sys, json, re, time
from threading_task_pc.pc_baidu import  mobile_url_accurate_baidu, pc_url_accurate_baidu
from time import sleep
import threading
from my_db import database_create_data
import queue
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
            # print('tid---------------------> ', tid)
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
            search = obj_data[2]
            mohu_pipei = obj_data[3]
            keyword = obj_data[10]
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

