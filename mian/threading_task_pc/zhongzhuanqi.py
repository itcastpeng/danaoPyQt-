from mian.threading_task_pc.public import shouluORfugaiChaxun
from my_db import database_create_data
import sys, time


def shouluChaxun(lianjie, tid, search):
    #     'shoulu': shoulu,
    #     'title': title,
    #     'kuaizhao_time': kuaizhao_time,
    #     'status_code': status_code
    # pc端百度
    if str(search) == '1':
        resultObj = shouluORfugaiChaxun.baiduShouLuPC(lianjie)
    # 移动端百度
    elif str(search) == '4':
        # print('移动端---------')
        resultObj = shouluORfugaiChaxun.baiduShouLuMobeil(lianjie)
    # pc360
    # elif str(search) == '3':
    #     resultObj = shouluORfugaiChaxun.pcShoulu360(lianjie)
    # # 移动端360
    # elif str(search) == '6':
    #     resultObj = shouluORfugaiChaxun.mobielShoulu360(lianjie)

    sql = """update shoulu_Linshi_List set is_shoulu='{shoulu}', title='{title}', kuaizhao_time='{kuaizhao}', status_code='{status_code}', is_zhixing='{is_zhixing}' where id ={id};""".format(
        shoulu=resultObj['shoulu'],
        title=resultObj['title'],
        kuaizhao=resultObj['kuaizhao_time'],
        status_code=resultObj['status_code'],
        id=tid,
        is_zhixing='1'
    )
    database_create_data.operDB(sql, 'update')


def fugaiChaxun(tid, search, keyword, mohu_pipei, huoqu_fugai_time_stamp=None):
    """
    'paiming':int(rank_num),
    'title':title,
    'title_url':ret_two_url,
    'sousuo_guize':mohu_pipei,
    'status_code':status_code
    """
    order_list = []
    if str(search) == '1':
        resultObj = shouluORfugaiChaxun.baiduFuGaiPC(keyword, mohu_pipei)
    elif str(search) == '4':
        resultObj = shouluORfugaiChaxun.baiduFuGaiMOBIEL(keyword, mohu_pipei)
    # pc360
    # elif str(search) == '3':
    #     resultObj = shouluORfugaiChaxun.pcFugai360()
    # # 移动端360
    # elif str(search) == '6':
    #     resultObj = shouluORfugaiChaxun.mobielFugai360()
    if huoqu_fugai_time_stamp:
        sql_list = []
        for result in resultObj:
            order_list.append(result['paiming'])
            insert_sql = """insert into fugai_Linshi_List (keyword, paiming_detail, search_engine, title, title_url, sousuo_guize, time_stamp, tid) values ('{keyword}', '{paiming_detail}', '{search_engine}', '{title}', '{title_url}', '{sousuo_guize}', '{time_stamp}','{tid}');""".format(
                keyword=keyword, paiming_detail=result['paiming'], search_engine=search,
                title=result['title'], title_url=result['title_url'], sousuo_guize=result['sousuo_guize'],
                time_stamp=None, tid=tid)
            sql_list.append(insert_sql)
        database_create_data.operDB('', 'insert', True, sql_list)
        if order_list:
            str_order = ','.join(str(i) for i in order_list)
        else:
            str_order = '0'
        sql_two = """update fugai_Linshi_List set paiming_detail='{paiming_detail}', chaxun_status='1', is_zhixing='{is_zhixing}' where id = '{id}';""".format(
            paiming_detail=str_order, is_zhixing='1', id=tid)
        database_create_data.operDB(sql_two, 'update')
    else:
        # 给点词监控返回 排名
        for result in resultObj:
            order_list.append(result['paiming'])
        return order_list

