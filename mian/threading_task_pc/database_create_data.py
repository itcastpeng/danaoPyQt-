import requests, random, sqlite3
from time import sleep
import os, time, threading


#
# data_list = []
# def func(sql_data):
#
#     # print('开始入库')
#     # conn = sqlite3.connect('../my_db/my_sqlite.db',check_same_thread=False)
#
#     while True:
#         if not os.path.exists(lock_file):
#             print("文件不存在")
#             with open(lock_file, 'w') as f:
#                 f.write('1')
#                 print('sql_data======================>', sql_data['sql'],sql_data['id'],time.time())
#                 conn = sqlite3.connect(db_file)
#                 cursor = conn.cursor()
#                 cursor.execute(sql_data['sql'])
#                 conn.commit()
#                 conn.close()
#                 sleep(2)
#                 break
#         else:
#             print('文件存在')
#             sleep(1)
#             continue
#     os.remove(lock_file)
#     sleep(1)
lock_file = './my_db/my_sqlite3.lock'
db_file = './my_db/my_sqlite.db'


def operDB(sql, oper='select'):
    print('进入操作数据库')
    result_obj = {
        'data': '',
        'code': 200
    }
    while True:
        if not os.path.exists(lock_file):
            # print("文件不存在")
            with open(lock_file, 'w') as f:
                f.write('1')
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                print('数据库操作=====================> ',sql)
                result_data = cursor.execute(sql)
                if oper == 'select':
                    result_obj['data'] = list(result_data)
                conn.commit()
                conn.close()
                break
        else:
            # print('文件存在')
            sleep(0.5)
            continue
    os.remove(lock_file)
    return result_obj

# if __name__ == '__main__':
#     # sql = 'select * from task_Detail where is_perform=1;'
#     sql = 'delete from task_Detail where is_perform=1;'
#     result_obj = operDB(sql)
#     print(result_obj)