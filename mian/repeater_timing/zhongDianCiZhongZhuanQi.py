
import datetime
from mian.threading_task_pc.public import shouluORfugaiChaxun
from mian.threading_task_pc.public import getpageinfo, shouluORfugaiChaxun
from mian.my_db import database_create_data
from mian.threading_task_pc.pc_baidu import mobile_fugai_pipei_baidu, mobile_url_accurate_baidu, pc_fugai_pipei_baidu, pc_url_accurate_baidu
from mian.threading_task_pc.pc_360 import pc_url_accurate_360, pc_fugai_pipei_360, mobile_fugai_pipei_360, mobile_url_accurate_360


def ShouLu(detail_id, keywords, domain, search_engine):
    date_time = datetime.datetime.today().strftime('%Y-%m-%d')

    # pc端百度
    if search_engine == '1':
        data_list = pc_url_accurate_baidu.Baidu_Zhidao_URL_PC(detail_id, keywords, domain)

    # 移动端百度
    if search_engine == '4':
        data_list = mobile_url_accurate_baidu.Baidu_Zhidao_URL_MOBILE(detail_id, keywords, domain)

    # pc端360
    if search_engine == '3':
        print(search_engine, 'pc 360 ')
        data_list = pc_url_accurate_360.PC_360_URL_PC(detail_id, keywords, domain)

    # 移动端360
    if search_engine == '6':
        print(search_engine, 'mobiel 360 ')
        data_list =  mobile_url_accurate_360.PC_360_URL_MOBILE(detail_id, keywords, domain)

    insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
        order=data_list['order'], shoulu=data_list['shoulu'], detail_id=detail_id, date_time=date_time)
    database_create_data.operDB(insert_sql, 'insert')
    update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(detail_id)
    database_create_data.operDB(update_sql, 'update')


def FuGai(search_engine, keywords, domain, detail_id):

    # pc端百度
    if search_engine == '1':
        result = pc_fugai_pipei_baidu.Baidu_Zhidao_yuming_pc(search_engine, keywords, domain, detail_id)

    # 移动端百度
    if search_engine == '4':
        result = mobile_fugai_pipei_baidu.Baidu_Zhidao_yuming_mobile(search_engine, keywords, domain, detail_id)

    # pc端360
    if search_engine == '3':
        result = pc_fugai_pipei_360.Dao_Hang_360_yuming_pc(search_engine, keywords, domain, detail_id)

    # 移动端360
    if search_engine == '6':
        print('进入 移动端 360 覆盖模式')
        result = mobile_fugai_pipei_360.Dao_Hang_360_yuming_mobile(search_engine, keywords, domain, detail_id)

    shoulu = '0'
    str_order = '0'
    if len(result):
        str_order = ",".join(str(i) for i in result)
    date_time = datetime.datetime.today().strftime('%Y-%m-%d')
    insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{tid}', '{date_time}');""".format(
        order=str_order, shoulu=shoulu, tid=detail_id, date_time=date_time)
    database_create_data.operDB(insert_sql, 'insert')
    update_sql = """update task_Detail set is_perform = '0' where id = '{tid}'""".format(tid=detail_id)
    database_create_data.operDB(update_sql, 'update')
