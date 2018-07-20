import requests, random, sqlite3
from time import sleep
import os
data_list = []
def func(sql_data):
    # lock_file = '../my_db/my_sqlite.lock'
    # while True:
    #     if os.path.exists(lock_file):
    #         sleep(0.2)
    #         continue
    #     else:
    #         print("文件不存在")
    #         with open(lock_file, 'w') as f:
    #             f.write('1')
    #     conn = sqlite3.connect('../my_db/my_sqlite.db')
    #     cursor = conn.cursor()
    #     print('sql_data----------------------------------===============>',sql_data)
    #     cursor.execute(sql_data)
    #     conn.commit()
    #     conn.close()
    #
    #     os.remove(lock_file)
    #     break
    data_list.append(sql_data)
    objs = ''
    for data in data_list:
        print('sql_data----------------------------------===============>',data)
        # conn = sqlite3.connect('../my_db/my_sqlite.db')
        # objs = cursor = conn.cursor()
        # cursor.execute(data)
        # conn.commit()
        # conn.close()

