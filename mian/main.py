from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtCore import *
from win32 import win32api
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget
from multiprocessing import Queue
import sqlite3, os, sys, json, re, time
import datetime


# PyQt 与 Js 交互 类
class Danao_Inter_Action(QObject):
    def __init__(self):
        super(Danao_Inter_Action, self).__init__()
        self.zhongdianci_update = ''
        self.zhongdianci_select_task_detail = ''


    # 占位
    def get_zhanwei_zhushou(self):
        pass

    # 返回登陆参数
    def get_Loginvalue(self):
        # 查询数据库 返回用户信息
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        sql = """select * from Login_message;"""
        cursor.execute(sql)
        data = ''
        for cow in cursor:
            data = cow[1]
        # print('-----------传登录参数========> ',data)
        return data

    # 获取登录参数 保存数据库
    def set_Loginvalue(self, data):
        print('获得登录参数---->: %s' % data)
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        # 判断有无数据库 没有创建插入用户信息 有创建信息
        # db_path = os.path.exists('./my_db/my_sqlite.db')
        # 查询数据库 有数据更新 没数据创建
        sql = """select * from Login_message;"""
        select_sql = cursor.execute(sql)
        sql_data = ''
        for sql_data in select_sql:
            sql_data = sql_data
        if sql_data:
            sql = """update Login_message set message='{data}' where id=1""".format(data=data)
        else:
            sql = """insert into Login_message values (1,'{data}')""".format(data=data)
        # print('执行sql ---------- >',sql)
        cursor.execute(sql)
        conn.commit()
        conn.close()
        # print('当前数据库执行结束-------------')



    # 重点词监控 - 获取任务列表数据
    def get_zhongdianci_create_task_list_value(self):

        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        sql = """select * from Task_List;"""
        cursor.execute(sql)
        data_list = []
        for obj in cursor:
            qiyong_status = '未启用'
            if obj[1]:
                qiyong_status = '已启用'

            zhixing = False
            if obj[8]:
                zhixing = True
            """  task_status         任务状态
                                     1 未查询
                                     2 查询中
                                     3 已完成"""
            task_status = '未查询'
            if obj[5] == 2:
                task_status = '查询中'
            if obj[5] == 3:
                task_status = '已完成'
            data_list.append({
                "id": obj[0],
                "qiyong_status": qiyong_status,
                "task_name": obj[2],
                "task_jindu": obj[3],
                "task_start_time": obj[4],
                "task_status":task_status ,
                "search_engine": obj[6].split(','),
                "mohupipei": obj[7],
                "zhixing": obj[8],
                "next_datetime": obj[9],
                "keywords": obj[10]
            })
        # print('获取所有------------------> ',data_list)
        return json.dumps(data_list)

    # 重点词监控 - 增加任务列表
    def set_zhongdianci_create_value(self,data):
        print('增加任务- ----------------- 》 ')
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        # print('获取任务列表参数---------> ',data)
        if type(data) == str:
            json_data = json.loads(data)
            # print('json_data -->', json_data)

            qiyong_status = json_data['qiyong_status']
            if qiyong_status:
                qiyong_status = 1
            else:
                qiyong_status = 0
            task_name = json_data['task_name']
            task_jindu = json_data['task_jindu']
            task_start_time = json_data['task_start_time']
            search_engine = ','.join(json_data['search_engine'])
            mohupipei = json_data['mohupipei']
            zhixing = json_data['zhixing']
            if zhixing:
                zhixing = 1
            else:
                zhixing = 0
            # next_datetime = json_data['next_datetime']
            now_date = datetime.date.today()
            str_now_date = str(now_date)
            next_datetime =  str_now_date + ' ' + task_start_time.replace(':','-')
            keywords = json_data['keywords']
            values = (
                qiyong_status, task_name, task_jindu, task_start_time,
                search_engine, mohupipei, zhixing, next_datetime, keywords
            )
            sql = """insert into Task_List (qiyong_status, task_name, task_jindu, task_start_time, search_engine, mohupipei, zhixing, next_datetime, keywords) values {values};""".format(
                values=values)
            print('sql--------------> ',sql)
            cursor.execute(sql)
            """search_engine      
            需要查询的搜索引擎
               1 百度
               2 搜狗
               3 360
               4 手机百度
               5 手机搜狗
               6 手机360
               7 神马"""

            sql = """select id from Task_List where task_name='{}';""".format(task_name)
            cursor.execute(sql)
            # print('sql ========= > ',sql)
            tid = [i for i in cursor][0][0]

            keyword_list = keywords.split('\n')
            search_engine_list = search_engine.split(',')
            data_list = []
            for keyword in keyword_list:
                if keyword in data_list:
                    pass
                else:
                    data_list.append(keyword)
            create_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
            for search_engine in search_engine_list:
                for keyword in data_list:
                    if keyword:
                        sql = ''
                        if 'http' in keyword:
                            new_keyword = re.findall("(.*)http", keyword)[0]
                            lianjie_list = keyword.split(new_keyword)
                            lianjie = ''
                            for lianjie in lianjie_list:
                                if lianjie:
                                    lianjie = lianjie
                            data_insert = (tid, search_engine, lianjie, new_keyword, mohupipei, create_time)
                            sql = """insert into task_Detail (tid, search_engine, lianjie, keywords, mohupipei, create_time) values {data_insert};""".format(data_insert=data_insert)
                        else:
                            lianjie = ''
                            data_insert = (tid, search_engine, lianjie, keyword, mohupipei, create_time)
                            sql = """insert into task_Detail (tid, search_engine, lianjie, keywords, mohupipei, create_time) values {data_insert};""".format(data_insert=data_insert)
                        # print('sql------------> ',sql)
                        cursor.execute(sql)
            conn.commit()
            conn.close()



    # 重点词监控 - 获取修改任务列表id
    def set_zhongdianci_update_task_list_value(self,data):
        print('获取修改任务列表id ----------- > ',data)
        self.zhongdianci_update = data

    # 重点词监控 - 返回该id任务列表数据
    def get_zhongdianci_update_task_list_data_value(self):
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        if self.zhongdianci_update:
            sql = """select * from Task_List where id = {};""".format(int(self.zhongdianci_update))
            # print(o_id, task_name, task_status, task_start_time, qiyong_status, search_engine, task_jindu, zhixing)
            cursor.execute(sql)
            data_list = []
            for obj in cursor:
                qiyong_status = '未启用'
                if obj[1]:
                    qiyong_status = '已启用'

                zhixing = False
                if obj[8]:
                    zhixing = True
                """  task_status         任务状态
                                         1 未查询
                                         2 查询中
                                         3 已完成"""
                task_status = '未查询'
                if obj[5] == 2:
                    task_status = '查询中'
                if obj[5] == 3:
                    task_status = '已完成'
                data_list.append({
                    "o_id": obj[0],
                    "qiyong_status": obj[1],
                    "task_name": obj[2],
                    "task_jindu": obj[3],
                    "task_start_time": obj[4],
                    "task_status": obj[5],
                    "search_engine": obj[6],
                    "mohupipei": obj[7],
                    "zhixing": obj[8],
                    "next_datetime": obj[9],
                    "keywords": obj[10]
                })
            conn.commit()
            conn.close()
            print('返回原数据 id为{}的数据-------------> '.format(self.zhongdianci_update),data_list)
            return str(data_list)

    # 重点词监护 - 修改任务列表数据
    def set_zhongdianci_update_data_value(self,update_data):
        if self.zhongdianci_update and update_data:
            conn = sqlite3.connect('./my_db/my_sqlite.db')
            cursor = conn.cursor()
            if type(update_data) == str:
                print('update_data------------------------> ',update_data)
                print(json.loads(update_data))
                # qiyong_status = json_data['qiyong_status']
                # if qiyong_status:
                #     qiyong_status = 1
                # else:
                #     qiyong_status = 0
                # print('qiyong_status------------->',qiyong_status)
                # task_name = json_data['task_name']
                # print('task_name ============= > ', task_name)
                # task_jindu = json_data['task_jindu']
                # task_start_time = json_data['task_start_time']
                # search_engine = ",".join(json_data['search_engine'])
                # mohupipei = json_data['mohupipei']
                # zhixing = json_data['zhixing']
                # if zhixing:
                #     zhixing = 1
                # else:
                #     zhixing = 0
                # next_datetime = json_data['next_datetime']
                # keywords = json_data['keywords']
                #
                # sql = """update Task_List set qiyong_status='{qiyong_status}',task_name='{task_name}',task_jindu='{task_jindu}',task_start_time='{task_start_time}',search_engine='{search_engine}',mohupipei='{mohupipei}',mohupipei='{mohupipei}',zhixing='{zhixing}',keywords='{keywords}',next_datetime='{next_datetime}' where id={id};""".format(
                #     qiyong_status=qiyong_status, task_name=task_name, task_jindu=task_jindu,task_start_time=task_start_time,
                #     search_engine=search_engine, mohupipei=mohupipei,zhixing=zhixing,keywords=keywords,next_datetime=next_datetime,id=self.zhongdianci_update,)
                # print(sql)
                # cursor.execute(sql)
                conn.commit()
                conn.close()



    # 重点词监护 - 清空为该id的任务 - 的详情数据
    def set_zhongdianci_select_id_task_detail_value(self,select_task_detail):
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        if select_task_detail:
            print('清空 {}任务列表id 的详情数据'.format(select_task_detail))
            sql = """delete from task_Detail where tid = {};""".format(select_task_detail)
            cursor.execute(sql)
            print(sql)
            conn.commit()
            conn.close()



    # 重点词监护 - 获取任务id
    def set_zhongdianci_select_id_select_task_detail_value(self,data):
        self.zhongdianci_select_task_detail = data

    #  重点词监护 - 查询该任务的详情
    def get_zhongdianci_select_id_select_task_detail_value(self):
        # print('zhongdianci_select_task_detail -------- >',self.zhongdianci_select_task_detail)
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        data_list = []
        if self.zhongdianci_select_task_detail:
            print('----------------')
            sql = """select * from task_Detail where tid={};""".format(self.zhongdianci_select_task_detail)
            print(sql)
            cursor.execute(sql)
            print('执行到这了========')
            for obj in cursor:
                data_list.append({
                    "id": obj[0],
                    "tid": obj[1],
                    "search_engine": obj[2],
                    "lianjie": obj[3],
                    "keywords": obj[4],
                    "mohupipei": obj[5],
                    "create_time": obj[6],
                })
        conn.commit()
        conn.close()
        return  str(data_list)


    # 爬虫 获取需要执行的任务id 调用定时器
    def set_pc_task_value(self,datas):
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        for data in datas.replace(',','').replace('[','').replace(']',''):
            print(data, '--------------> ',type(data))
            sql = """update task_Detail set is_perform = 1 where tid = {};""".format(data)
            cursor.execute(sql)
        conn.commit()
        conn.close()
    # # 爬虫 用户修改下次执行时间 添加数据库
    # def set_pc_task_timing_value(self,data):
    #     create_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    #     if data:
    #         data = data.split(',')
    #         conn = sqlite3.connect('./my_db/my_sqlite.db')
    #         cursor = conn.cursor()
    #         task_id = data[0]
    #         task_next_time = data[1]
    #         sql = """select next_datetime from task_List where id='{}';""".format(task_id)
    #         cursor.execute(sql)
    #         task_obj = ''
    #         for obj in cursor:
    #             if obj[0]:
    #                 task_obj = obj[0]
    #         print('task_next_time------------> ',task_next_time)
    #         sql = """update task_List set next_datetime='{task_next_time}' where id='{task_id}';""".format(task_next_time=task_next_time,task_id=task_id)
    #         print(sql)
    #         cursor.execute(sql)
    #         # # 即刻执行
    #         # if task_next_time == create_time:
    #         #     repeater_timing_task(data)
    #     conn.commit()
    #     conn.close()




    # 登录 交互
    loginValue = pyqtProperty(str,fget=get_Loginvalue, fset=set_Loginvalue)
    # 重点词监护 - 增加任务
    createTaskListValue = pyqtProperty(str,fget=get_zhongdianci_create_task_list_value, fset=set_zhongdianci_create_value)
    # 重点词监护 - 传递id 查询该id任务列表
    updateTaskListValue = pyqtProperty(str, fget=get_zhongdianci_update_task_list_data_value, fset=set_zhongdianci_update_task_list_value)
    # 重点词监护 - 使用↑id 修改任务列表
    updateDatavalue = pyqtProperty(str,fget=get_zhanwei_zhushou, fset=set_zhongdianci_update_data_value)
    # 重点词监护 - 清空该id的 任务列表 详情数据
    emptyDataTaskDetail = pyqtProperty(str,fget=get_zhanwei_zhushou, fset=set_zhongdianci_select_id_task_detail_value)
    # 重点词监护 - 获取id 查询该id详情
    selectDataTaskDetail = pyqtProperty(str,fget=get_zhongdianci_select_id_select_task_detail_value, fset=set_zhongdianci_select_id_select_task_detail_value)
    # 爬虫 - 获取id 分辨 移动或pc端    即刻执行
    pcTaskValue = pyqtProperty(str,fget=get_zhanwei_zhushou, fset=set_pc_task_value)
    # 爬虫 用户修改下次执行时间 添加数据库
    # pcTaskTimingValue = pyqtProperty(str,fget=get_zhanwei_zhushou, fset=set_pc_task_timing_value)


# PyQt 架构 与 数据库初始化 类
class DaNao(object):
    def __init__(self):
        self.initDB()
        self.main_body()


    # 初始化数据库和表
    def initDB(self):
        # 判断路径
        my_db_path  = os.path.join('my_db')
        if my_db_path:
            conn = sqlite3.connect('./my_db/my_sqlite.db')
            cursor = conn.cursor()
            # 查询sqlite所有表  查询表是否存在 不在创建
            sql = """select name from sqlite_master  where type = 'table' order by name;"""
            result = cursor.execute(sql)
            data_list = []
            for obj in result:
                db_obj = obj[0]
                data_list.append(db_obj)
            print('数据库的所有表名-=-=-==-=-=-=--=-===-=-=> ',data_list)

            # 判断登录 信息表
            if 'Login_Message' not in data_list:
                print('没有Login_Message表 ------- 创建Login_Message表')
                conn = sqlite3.connect('./my_db/my_sqlite.db')
                cursor = conn.cursor()
                sql = """
                      create table Login_Message (
                      id integer primary key autoincrement,
                      message text not null
                      )"""
                cursor.execute(sql)
                # print('执行sql ---------->',sql)

            # 判断 任务列表
            if 'task_List' not in data_list:
                print('没有Task_List表 ------- 创建Task_List表')


                """
                qiyong_status       启用状态
                task_name           任务名称
                task_jindu          查询任务的进度百分比
                task_start_time     任务查询时间
                task_status         任务状态
                                         1 未查询
                                         2 查询中
                                         3 已完成
                             
                search_engine      需要查询的搜索引擎
                                       1 百度
                                       2 搜狗
                                       3 360
                                       4 手机百度
                                       5 手机搜狗
                                       6 手机360
                                       7 神马
                               
                mohupipei          模糊匹配条件 
                zhixing            是否正在查询
                next_datetime      下次查询时间
                keywords           查询的关键词
                
                """


                sql = """CREATE TABLE task_List (
                     "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     "qiyong_status" INTEGER,
                     "task_name" TEXT,
                     "task_jindu" INTEGER,
                     "task_start_time" TEXT,
                     "task_status" INTEGER DEFAULT 1,
                     "search_engine" TEXT,
                     "mohupipei" TEXT,
                     "zhixing" INTEGER,
                     "next_datetime" TEXT,
                     "keywords" TEXT
                   );"""
                cursor.execute(sql)

            # 判断 任务详情
            if 'task_Detail' not in data_list:
                print('没有Task_Detail表 ------- 创建Task_Detail表')

                """   id 
                      tid INTEGER          归属任务
                      search_engine        搜索引擎
                      lianjie              条件链接
                      keywords             关键词
                      mohupipei            模糊匹配条件
                      create_time          创建时间
                      task_start_time      任务执行时间
                      time_stamp           时间戳
                      is_perform           是否执行
                      
                """

                sql = """CREATE TABLE task_Detail (
                      "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                      "tid" INTEGER,
                      "search_engine" TEXT,
                      "lianjie" TEXT,
                      "keywords" TEXT,
                      "mohupipei" TEXT,
                      "create_time" TEXT,
                      "task_start_time" TEXT,
                      "time_stamp" INTEGER,
                      "is_perform" TEXT,
                      CONSTRAINT "task_detail_tid" FOREIGN KEY ("tid") REFERENCES "Task_List" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT
                    );"""
                cursor.execute(sql)


            # 判断 搜索引擎表
            # if 'searchEngineList' not in data_list:
            #     print('searchEngineList ------- searchEngineList')
            #     sql = """CREATE TABLE searchEngineList (
            #             "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            #             "value" TEXT,
            #             "label" TEXT
            #             );"""
            #     cursor.execute(sql)

            # 关闭链接


            conn.commit()
            conn.close()


    # 主体 函数
    def main_body(self):
        win32_width = win32api.GetSystemMetrics(0) * 0.8
        win32_height = win32api.GetSystemMetrics(1) * 0.8

        app = QApplication(sys.argv)
        win = QWidget()
        win.resize(win32_width, win32_height)
        win.setWindowTitle('诸葛大脑')
        app.setWindowIcon(QIcon('128.ico'))

        # 创建垂直布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setMargin(0)
        win.setLayout(layout)

        view = QWebEngineView()
        # view.load(QUrl('https://www.cnblogs.com/wangshoul'))
        # view.load(QUrl('http://192.168.10.240:8080'))
        view.load(QUrl('http://192.168.10.252:8080'))
        # view.load(QUrl('C:/pycharm zh/zhugedanaoPyQt/mian/web/index.html'))

        # 简单理解就是将这个控件(QWidget)的几何内容(宽高位置等)，赋值给qr
        qr = view.frameGeometry()
        # 计算出你的显示器的屏幕分辨率。根据得到的分辨率我们得到屏幕的中心点。
        cp = QDesktopWidget().availableGeometry().center()
        # 我们的矩形(qr)已有宽度和高度，现在设置移动矩形的中心(moveCenter)到屏幕的中心点(cp)，矩形的尺寸是不变的。
        qr.moveCenter(cp)
        # 移动应用程序窗口的左上角到qr矩形的左上角，从而使应用程序窗口显示在屏幕的中心
        view.move(qr.topLeft())

        # 创建一个 QWebChannel 对象, 用来传递 PyQt的参数到 Js
        channel = QWebChannel()
        myObj = Danao_Inter_Action()
        channel.registerObject("bridge", myObj)
        view.page().setWebChannel(channel)

        # 把 QWebEngineView 控件加载到 layout 布局中
        layout.addWidget(view, 0)

        # 显示窗口和运行
        win.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    obj = DaNao()






