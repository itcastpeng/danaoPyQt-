import datetime
from mian.my_db import database_create_data
from mian.repeater_timing.pc_baidu import  mobile_url_accurate_baidu,  pc_url_accurate_baidu
from mian.repeater_timing.pc_360 import pc_url_accurate_360, mobile_url_accurate_360
from mian.threading_task_pc import zhongzhuanqi

def ShouLu(detail_id, keywords, domain, search_engine):
    date_time = datetime.datetime.today().strftime('%Y-%m-%d')

    # pc端百度
    if search_engine == '1':
        # print('中转--收录--pc端百度',int(time.time()))
        data_list = pc_url_accurate_baidu.Baidu_Zhidao_URL_PC(detail_id, keywords, domain)

    # 移动端百度
    if search_engine == '4':
        # print('中转--收录--移动端百度',int(time.time()))
        data_list = mobile_url_accurate_baidu.Baidu_Zhidao_URL_MOBILE(detail_id, keywords, domain)

    # pc端360
    if search_engine == '3':
        # print('中转--覆盖--pc端360',int(time.time()))
        data_list = pc_url_accurate_360.PC_360_URL_PC(detail_id, keywords, domain)

    # 移动端360
    if search_engine == '6':
        # print('中转--覆盖--移动端360',int(time.time()))
        data_list =  mobile_url_accurate_360.PC_360_URL_MOBILE(detail_id, keywords, domain)

    insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ({order}, {shoulu}, {detail_id}, '{date_time}');""".format(
        order=data_list['order'], shoulu=data_list['shoulu'], detail_id=detail_id, date_time=date_time)
    database_create_data.operDB(insert_sql, 'insert')
    update_sql = """update task_Detail set is_perform = '0' where id = '{}'""".format(detail_id)
    database_create_data.operDB(update_sql, 'update')


def FuGai(search_engine, keyword, domain, detail_id):
    shoulu = '0'
    str_order = '0'
    result = zhongzhuanqi.fugaiChaxun(detail_id, search_engine, keyword, ','.join(domain.split(',')))
    print('result------->? ',result )
    if len(result):
        str_order = ",".join(str(i) for i in set(result))
    date_time = datetime.datetime.today().strftime('%Y-%m-%d')
    insert_sql = """insert into task_Detail_Data (paiming, is_shoulu, tid, create_time) values ('{order}', '{shoulu}', '{tid}', '{date_time}');""".format(
        order=str_order, shoulu=shoulu, tid=detail_id, date_time=date_time)
    database_create_data.operDB(insert_sql, 'insert')
    update_sql = """update task_Detail set is_perform = '0' where id = '{tid}'""".format(tid=detail_id)
    database_create_data.operDB(update_sql, 'update')
