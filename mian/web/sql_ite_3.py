




import sqlite3

conn = sqlite3.connect('../my_db/my_sqlite.db')
cursor  = conn.cursor()


# cursor.execute("""
#               create table ceshi (
#               id int primary key not null,
#               message text not null
#               )""")



cursor.execute("""insert into Login_message values (1,"测试登录参数二")""")
conn.commit()
conn.close()
