import requests, random, sqlite3, os
from time import sleep

# lock_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'my_sqlite3.lock')
# db_file =  os.path.join(os.path.dirname(os.path.realpath(__file__)), 'my_sqlite.db')

db_file = os.path.join(os.getcwd(), 'my_db', 'my_sqlite.db')
lock_file = os.path.join(os.getcwd(), 'my_db', 'my_sqlite3.lock')


def operDB(sql, oper='select'):
    result_obj = {
        'data': '',
        'code': 200
    }
    while True:
        if not os.path.exists(lock_file):
            with open(lock_file, 'w') as f:
                f.write('1')
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            # print('数据库操作=====================> ',sql)
            result_data = cursor.execute(sql)
            if oper == 'select':
                result_obj['data'] = list(result_data)
            conn.commit()
            conn.close()
            break
        else:
            # print('-----数据库锁被占用等待....-----')
            sleep(1.5)
            continue

    if os.path.exists(lock_file):
        os.remove(lock_file)
    return result_obj