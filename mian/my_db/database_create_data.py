import requests, random, sqlite3, os
from time import sleep

lock_file = './my_db/my_sqlite3.lock'
db_file = './my_db/my_sqlite.db'

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
                print('数据库操作=====================> ',sql)
                result_data = cursor.execute(sql)
                if oper == 'select':
                    result_obj['data'] = list(result_data)
                conn.commit()
                conn.close()
                break
        else:
            sleep(0.5)
            continue
    os.remove(lock_file)
    return result_obj
