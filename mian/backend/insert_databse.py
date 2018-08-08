import json
from my_db import database_create_data
import time, re


# 创建任务
def insert_into(data, time_stamp, shibiecanshu):

    if shibiecanshu == 'zhongdianci':
        json_data = json.loads(data)
        task_name = json_data['task_name']
        mohupipei = json_data['mohupipei']
        keyword_list = list(set(json_data['keywords'].split('\n')))
        search_engine_list = ','.join(json_data['search_engine'])
        sql_list = []
        sql_two = """select id from Task_List where task_name='{}';""".format(task_name)
        objs = database_create_data.operDB(sql_two, 'select')
        tid = objs['data'][0][0]
        create_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        for search_engine in search_engine_list.split(','):
            for keyword in keyword_list:
                if keyword:
                    if 'http' in keyword:
                        new_keyword = re.findall("(.*)http", keyword)[0].replace('\t', '')
                        if new_keyword:
                            lianjie_list = keyword.split(new_keyword)
                            for lianjie in lianjie_list:
                                if lianjie:
                                    lianjie = lianjie.replace('\t', '')
                                    data_insert = (tid, search_engine, lianjie, new_keyword, mohupipei, create_time)
                                    sql_three_sql = """insert into task_Detail (tid, search_engine, lianjie, keywords, mohupipei, create_time) values {data_insert};""".format(
                                        data_insert=data_insert)
                                    sql_list.append(sql_three_sql)
                    else:
                        lianjie = ''
                        data_insert = (tid, search_engine, lianjie, keyword, mohupipei, create_time)
                        sql_three = """insert into task_Detail (tid, search_engine, lianjie, keywords, mohupipei, create_time) values {data_insert};""".format(
                            data_insert=data_insert)
                        sql_list.append(sql_three)
        database_create_data.operDB('', 'insert', True, sql_list)


    if shibiecanshu == 'shoulu':
        json_data_list = json.loads(data)
        data_url_list = json_data_list['editor_content'].replace('\r\n', '').strip().split('http')
        if json_data_list['searchEngineModel']:
            sql_list = []
            print(json_data_list['searchEngineModel'])
            for search in json_data_list['searchEngineModel']:
                for dataurl in set(data_url_list):
                    if dataurl:
                        data_url = dataurl.replace('\n', '')
                        url_data = 'http' + data_url
                        lianjie = url_data.strip().replace('\t', '')
                        insert_sql = """insert into shoulu_Linshi_List (url, time_stamp, search, is_zhixing) values('{url}', '{time_stamp}', '{search}', '{is_zhixing}');""".format(
                            url=lianjie, time_stamp=time_stamp, search=search, is_zhixing='0')
                        sql_list.append(insert_sql)
            database_create_data.operDB('', 'insert', True, sql_list)

    if shibiecanshu == 'fugai':
        tiaojian_list = []
        json_data_list = data
        sql_list = []
        for tiaojian in json_data_list['fugai_tiaojian'].split('|'):
            if not tiaojian.isspace():
                tiaojian = tiaojian.strip().replace('\n', '')
                if tiaojian not in tiaojian_list:
                    tiaojian_list.append(tiaojian)
        str_tiaojian = ",".join(str(i) for i in tiaojian_list)
        for search in json_data_list['searchEngineModel']:
            for keyword in set(json_data_list['editor_content'].strip().split('\n')):
                keyword = keyword.strip()
                insert_sql = """insert into fugai_Linshi_List (keyword,  search_engine, title, title_url, sousuo_guize, time_stamp, is_zhixing) values ('{keyword}', '{search_engine}', '', '', '{sousuo_guize}', '{time_stamp}', '0');""".format(
                    keyword=keyword, search_engine=search, sousuo_guize=str_tiaojian, time_stamp=time_stamp)
                sql_list.append(insert_sql)
        database_create_data.operDB('', 'insert', True, sql_list)
