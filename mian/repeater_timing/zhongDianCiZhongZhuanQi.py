
import datetime
from mian.threading_task_pc.public import shouluORfugaiChaxun
from mian.threading_task_pc.public import getpageinfo, shouluORfugaiChaxun
from mian.my_db import database_create_data
from mian.threading_task_pc.pc_baidu import mobile_fugai_pipei_baidu, mobile_url_accurate_baidu, pc_fugai_pipei_baidu, pc_url_accurate_baidu


def baiDuShouLu(detail_id, keywords, domain, search_engine):
    if search_engine == '1':
        print('进入pc端')
        data_list = pc_url_accurate_baidu.Baidu_Zhidao_URL_PC(detail_id, keywords, domain)
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
            order=data_list['order'], shoulu=data_list['shoulu'], detail_id=detail_id, date_time=date_time)
        database_create_data.operDB(insert_sql, 'insert')
        update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(detail_id)
        database_create_data.operDB(update_sql, 'update')

    if search_engine == '4':
        data_list = mobile_url_accurate_baidu.Baidu_Zhidao_URL_MOBILE(detail_id, keywords, domain)
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{detail_id}', '{date_time}');""".format(
            order=data_list['order'], shoulu=data_list['shoulu'], detail_id=detail_id, date_time=date_time)
        database_create_data.operDB(insert_sql, 'insert')
        update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(detail_id)
        database_create_data.operDB(update_sql, 'update')

def baiDuFuGai(search_engine, keywords, domain, detail_id):
    if search_engine == '1':
        shoulu = '0'
        str_order = '0'
        result = pc_fugai_pipei_baidu.Baidu_Zhidao_yuming_pc(search_engine, keywords, domain, detail_id)
        if len(result):
            str_order = ",".join(str(i) for i in result)
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{tid}', '{date_time}');""".format(
            order=str_order, shoulu=shoulu, tid=detail_id, date_time=date_time)
        database_create_data.operDB(insert_sql, 'insert')
        update_sql = """update task_Detail set is_perform = '0' where id = '{tid}'""".format(tid=detail_id)
        database_create_data.operDB(update_sql, 'update')

    if search_engine == '4':
        shoulu = '0'
        str_order = '0'
        result = mobile_fugai_pipei_baidu.Baidu_Zhidao_yuming_mobile(search_engine, keywords, domain, detail_id)
        if len(result):
            str_order = ",".join(str(i) for i in result)
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{detail_id}', '{date_time}');""".format(
            order=str_order, shoulu=shoulu, detail_id=detail_id, date_time=date_time)
        database_create_data.operDB(insert_sql, 'insert')
        update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(detail_id)
        database_create_data.operDB(update_sql, 'update')



