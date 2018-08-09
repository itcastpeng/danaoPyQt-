import requests, random, sqlite3, os
from time import sleep
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from mian import settings
import time
# from mian import settings
# lock_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'my_sqlite3.lock')
# db_file =  os.path.join(os.path.dirname(os.path.realpath(__file__)), 'my_sqlite.db')

# db_file = os.path.join(os.getcwd(), 'my_db', 'my_sqlite.db')
# lock_file = os.path.join(os.getcwd(), 'my_db', 'my_sqlite3.lock')


def operDB(sql, oper='select', batch_insert_flag=False, insert_sql_list=[]):
    """
    :param sql:
    :param oper:
    :param batch_insert_flag:  该值为True 时，则表示批量插入数据，应使用事务处理
    :param insert_sql_list:   批量添加的sql列表
    :return:
    """
    result_obj = {
        'data': '',
        'code': 200
    }
    if oper == "select":
        conn = sqlite3.connect(settings.db_file)
        cursor = conn.cursor()
        # print('数据库操作=====================> ',sql)
        result_data = cursor.execute(sql)
        if oper == 'select':
            result_obj['data'] = list(result_data)
    else:
        while True:
            # print('sql==========> ',sql)
            if not os.path.exists(settings.lock_file):
                with open(settings.lock_file, 'w') as f:
                    f.write('1')
                conn = sqlite3.connect(settings.db_file)
                cursor = conn.cursor()
                # 如果batch_insert_flag 为True 则 以 事务 批量插入
                if batch_insert_flag:
                    conn.execute("BEGIN TRANSACTION")
                    start_time = int(time.time())
                    for sql in insert_sql_list:
                        try:
                            result_data = cursor.execute(sql)
                        except Exception as e:
                            print('错误--------> ',sql)
                    conn.execute("COMMIT")
                else:
                    result_data = cursor.execute(sql)
                conn.commit()
                conn.close()
                break
            else:
                # pri nt('-----数据库锁被占用等待....-----')
                continue
        if os.path.exists(settings.lock_file):
            try:
                os.remove(settings.lock_file)
            except PermissionError:
                pass
    return result_obj