from mian.threading_task_pc.public import shouluORfugaiChaxun
from my_db import database_create_data
import sys, time
import json

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
    elif str(search) == '3':
        resultObj = shouluORfugaiChaxun.pcShoulu360(lianjie)
    # # 移动端360
    elif str(search) == '6':
        resultObj = shouluORfugaiChaxun.mobielShoulu360(lianjie)

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
    # pc端百度
    if str(search) == '1':
        resultObj = shouluORfugaiChaxun.baiduFuGaiPC(keyword, mohu_pipei)
    # 移动端百度
    elif str(search) == '4':
        resultObj = shouluORfugaiChaxun.baiduFuGaiMOBIEL(keyword, mohu_pipei)
    # pc360
    elif str(search) == '3':
        resultObj = shouluORfugaiChaxun.pcFugai360(keyword, mohu_pipei)
    # # 移动端360
    elif str(search) == '6':
        print('移动端 360 覆盖')
        resultObj = shouluORfugaiChaxun.mobielFugai360(keyword, mohu_pipei)

    if resultObj:
        if huoqu_fugai_time_stamp:
            json_detail_data = []
            for result in resultObj:
                order_list.append(result['paiming'])
                zhanwei = 0
                if result['paiming']:
                    zhanwei = 1
                json_detail_data.append({
                    'rank':result['paiming'],
                    'title':result['title'].replace('\'','').replace('"',''),
                    'url':result['title_url'],
                    'guize':result['sousuo_guize'],
                    'keyword':keyword,
                    'zhanwei':zhanwei,
                    'search_engine':search
                })
            json_data = ''
            if len(json_detail_data):
                json_data = json.dumps(json_detail_data)
            else:
                json_data = ''
            str_order = '0'
            if order_list:
                str_order = ','.join(str(i) for i in order_list)
            sql_two = """update fugai_Linshi_List set paiming_detail='{paiming_detail}', json_detail_data='{json_detail_data}', chaxun_status='1', is_zhixing='{is_zhixing}' where id = '{id}';""".format(
                paiming_detail=str_order, is_zhixing='1', id=tid,
                json_detail_data=json_data)
            database_create_data.operDB(sql_two, 'update')
        else:
            # 给点词监控返回 排名
            for result in resultObj:
                order_list.append(result['paiming'])
            return order_list

