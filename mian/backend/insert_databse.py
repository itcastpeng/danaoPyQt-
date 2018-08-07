import json
from my_db import database_create_data
import multiprocessing
from mian.threading_task_pc.threading_task import shoulu_func, fugai_func


# 创建任务
def threading_insert_into(data, time_stamp, shibiecanshu):
    if shibiecanshu == 'shoulu':
        json_data_list = json.loads(data)
        data_url_list = json_data_list['editor_content'].replace('\r\n', '').strip().split('http')
        if json_data_list['searchEngineModel']:
            sql_list = []
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
                insert_sql = """insert into fugai_Linshi_List (keyword,  search_engine, title, title_url, sousuo_guize, time_stamp, status_code, is_zhixing) values ('{keyword}', '{search_engine}', '', '', '{sousuo_guize}', '{time_stamp}','','0');""".format(
                    keyword=keyword, search_engine=search, sousuo_guize=str_tiaojian, time_stamp=time_stamp)
                sql_list.append(insert_sql)
        database_create_data.operDB('', 'insert', True, sql_list)
