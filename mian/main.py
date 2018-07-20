from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtCore import *
from win32 import win32api
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget
from multiprocessing import Queue
from openpyxl import Workbook
import sqlite3, os, sys, json, re, time, datetime
from openpyxl.styles import Font, Alignment
from openpyxl.utils.exceptions import IllegalCharacterError
import openpyxl as openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from tkinter import *
from tkinter.filedialog import askdirectory
from mian.threading_task_pc import threading_task
from time import sleep
import tkinter.messagebox
from mian.repeater_timing import timing_task



# PyQt 与 Js 交互 类
class Danao_Inter_Action(QObject):
    def __init__(self):
        super(Danao_Inter_Action, self).__init__()
        self.zhongdianci_update = ''
        self.zhongdianci_select_task_detail = ''
        self.huoqu_task_id_detail = ''
        self.huoqu_shoulu_time_stamp = ''
        self.dangqian_chaxunshoulu_time = ''
        self.panduan = '0'

    # 占位
    def zhanwei_zhushou(self):
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
        sql = """select * from task_List;"""
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
                "task_status": task_status,
                "search_engine": obj[6].split(','),
                "mohupipei": obj[7],
                "zhixing": obj[8],
                "next_datetime": obj[9],
                "keywords": obj[10]
            })
        # print('获取所有------------------> ', data_list)
        return json.dumps(data_list)

    # 重点词监控 - 增加任务列表
    def set_zhongdianci_create_value(self, data):
        # print('增加任务- ----------------- 》 ')
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        # print('获取任务列表参数---------> ',data)
        if type(data) == str:
            json_data = json.loads(data)
            print('json_data= ====================>',json_data)
            qiyong_status = json_data['qiyong_status']
            task_name = json_data['task_name']
            task_jindu = json_data['task_jindu']
            task_start_time = json_data['task_start_time']
            search_engine = ','.join(json_data['search_engine'])
            mohupipei = json_data['mohupipei']
            zhixing = json_data['zhixing']
            if qiyong_status:
                qiyong_status = 1
            else:
                qiyong_status = 0
            if zhixing:
                zhixing = 1
            else:
                zhixing = 0

            now_datetime_date = datetime.date.today()
            now_date_datetime = datetime.datetime.today().strftime('%H:%M:%S')
            str_now_date = str(now_date_datetime)
            now_date = '1900-01-01' + ' ' + str_now_date
            # 作比较  转成 datetime 格式
            task_start_time = datetime.datetime.strptime(task_start_time, '%H:%M:%S')
            now_date = datetime.datetime.strptime(now_date, '%Y-%m-%d %H:%M:%S')
            next_datetime = ''
            if now_date < task_start_time:
                # print('当前时间小于 开始时间')
                task_start_time = task_start_time.strftime('%H-%M-%S')
                print('------> ', task_start_time)
                #  如果当前时间小于 任务开始时间 那么 加一天
                add_one_day = (now_datetime_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                next_datetime = str(add_one_day) + ' ' + task_start_time
            else:
                # print('当前时间大于开始时间')
                task_start_time = task_start_time.strftime('%H-%M-%S')
                # print('task_start_time------->',task_start_time)
                next_datetime = str(now_datetime_date) + ' ' + task_start_time

            keywords = json_data['keywords']
            values = (
                qiyong_status,task_name, task_jindu, task_start_time,
                search_engine, mohupipei, zhixing, next_datetime, keywords
            )
            sql = """insert into Task_List (qiyong_status, task_name, task_jindu, task_start_time, search_engine, mohupipei, zhixing, next_datetime, keywords) values {values};""".format(
                values=values)
            # print('sql--------------> ', sql)
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
                            new_keyword = re.findall("(.*)http", keyword)[0].replace('\t','')
                            print('new_keyword-------------> ',new_keyword)
                            lianjie_list = keyword.split(new_keyword)
                            lianjie = ''
                            for lianjie in lianjie_list:
                                if lianjie:
                                    lianjie = lianjie.replace('\t','')
                            data_insert = (tid, search_engine, lianjie, new_keyword, mohupipei, create_time)
                            sql = """insert into task_Detail (tid, search_engine, lianjie, keywords, mohupipei, create_time) values {data_insert};""".format(
                                data_insert=data_insert)
                        else:
                            lianjie = ''
                            data_insert = (tid, search_engine, lianjie, keyword, mohupipei, create_time)
                            sql = """insert into task_Detail (tid, search_engine, lianjie, keywords, mohupipei, create_time) values {data_insert};""".format(
                                data_insert=data_insert)
                        print('sql------------> ',sql)
                        cursor = conn.cursor()
                        cursor.execute(sql)
            conn.commit()
            conn.close()

    # 重点词监控 - 获取修改任务列表id
    def set_zhongdianci_update_task_list_value(self, data):
        print('获取修改任务列表id ----------- > ', data)
        self.zhongdianci_update = data

    # 重点词监控 - 返回该id任务列表数据
    def get_zhongdianci_update_task_list_data_value(self):
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        if self.zhongdianci_update:
            sql = """select * from Task_List where id = {};""".format(int(self.zhongdianci_update))
            # print(o_id, task_name, task_status, task_start_time, qiyong_status, search_engine, task_jindu, zhixing)
            cursor.execute(sql)
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
                search_engine_list = []
                search_engine_list.append(obj[6])
                data_list = {
                    "id": obj[0],
                    "qiyong_status": obj[1],
                    "task_name": obj[2],
                    "task_jindu": obj[3],
                    "task_start_time": obj[4],
                    "task_status": obj[5],
                    "search_engine": search_engine_list,
                    "mohupipei": obj[7],
                    "zhixing": obj[8],
                    "next_datetime": obj[9],
                    "keywords": obj[10]
                }
            conn.commit()
            conn.close()
            # print('返回原数据 id为{}的数据-------------> '.format(self.zhongdianci_update), data_list)
            return json.dumps(data_list)

    # 重点词监护 - 修改任务列表数据
    def set_zhongdianci_update_data_value(self, update_data):
        if self.zhongdianci_update and update_data:
            conn = sqlite3.connect('./my_db/my_sqlite.db')
            cursor = conn.cursor()
            """{
            "id":1,
            "qiyong_status":1,
            "task_name":"测试任务=678678",
            "task_jindu":0,
            "task_start_time":"20:18:10",
            "search_engine":["1"],
            "mohupipei":"测试条件",
            "keywords":"1"
            }"""
            now_date_datetime = datetime.datetime.today().strftime('%H:%M:%S')
            now_datetime_date = datetime.date.today()
            str_now_date = str(now_date_datetime)
            now_date = '1900-01-01' + ' ' + str_now_date
            if type(update_data) == str:
                json_update_data = json.loads(update_data)
                print('json_update_data----------------------------------------> ',json_update_data)
                id = json_update_data['id']
                task_name = json_update_data['task_name']
                task_start_time = json_update_data['task_start_time']
                task_start_time = datetime.datetime.strptime(task_start_time, '%H:%M:%S')
                now_date = datetime.datetime.strptime(now_date, '%Y-%m-%d %H:%M:%S')
                if now_date < task_start_time:
                    task_start_time = task_start_time.strftime('%H-%M-%S')
                #     #  如果当前时间小于 任务开始时间 那么 加一天
                    add_one_day = (now_datetime_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                    next_datetime = str(add_one_day) + ' ' + task_start_time
                else:
                    task_start_time = task_start_time.strftime('%H-%M-%S')
                    next_datetime = str(now_datetime_date) + ' ' + task_start_time
                print(next_datetime)
                task_start_time = str(task_start_time)
                sql = """update Task_List set task_name='{task_name}',task_start_time='{task_start_time}',next_datetime='{next_datetime}' where id={id};""".format(
                    task_name=task_name,
                    task_start_time=task_start_time,
                    next_datetime=next_datetime,
                    id=id)
                print(sql)
                cursor.execute(sql)
            conn.commit()
            conn.close()

    # 重点词监护 - 清空为该id的任务 - 的详情数据
    def set_zhongdianci_select_id_task_detail_value(self, select_task_detail):
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        if select_task_detail:
            print('清空 {}任务列表id 的详情数据'.format(select_task_detail))
            sql = """select id from task_Detail where tid = {}""".format(select_task_detail)
            cursor.execute(sql)
            for obj in cursor:
                sql = """delete from task_Detail_Data where tid={}""".format(obj[0])
                cursor = conn.cursor()
                cursor.execute(sql)
            sql = """delete from task_Detail where tid = {};""".format(select_task_detail)
            cursor.execute(sql)
            print(sql)
        conn.commit()
        conn.close()

    # 重点词监护 - 获取任务id
    def set_zhongdianci_select_id_select_task_detail_value(self, data):
        self.zhongdianci_select_task_detail = data

    # 重点词监护 - 查询该任务的详情
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
        return str(data_list)


    # 重点词监护 - 爬虫 获取需要执行的任务id 调用定时器  立即监控
    def set_pc_task_value(self, datas):
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        self.huoqu_shoulu_time_stamp = int(time.time())
        self.dangqian_chaxunshoulu_time = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
        for data in datas.replace(',', '').replace('[', '').replace(']', ''):
            print(data, '--------------> ', type(data))
            sql = """update task_Detail set is_perform = 1 where tid = {};""".format(data)
            cursor.execute(sql)
        conn.commit()
        conn.close()


    # 重点词监护 - 删除单个或多个 任务
    def delete_or_batch_delete_task(self, delete_id):
        print('delete_id================>', delete_id)
        json_id = json.loads(delete_id)
        conn = sqlite3.connect('./my_db/my_sqlite.db')
        cursor = conn.cursor()
        for data in json_id:
            sql = """select id from task_Detail where tid = {}""".format(data)
            cursor.execute(sql)
            for obj in cursor:
                sql = """delete from task_Detail_Data where tid = {}""".format(obj[0])
                cursor = conn.cursor()
                cursor.execute(sql)
            sql = """delete from task_Detail where tid = {};""".format(data)
            cursor.execute(sql)
            sql = """delete from task_List where id ={}""".format(data)
            cursor.execute(sql)
        conn.commit()
        conn.close()

    # 重点词监护 - 查看子任务 获取id
    def set_task_id_view_The_subtasks_task(self, data):
        self.huoqu_task_id_detail = data

    # 重点词监护 - 查看子任务 - 详情任务
    def get_view_The_subtasks_detail(self):
        if self.huoqu_task_id_detail:
            conn = sqlite3.connect('./my_db/my_sqlite.db')
            cursor = conn.cursor()
            # print('self.huoqu_task_id_detail ---------- > ', self.huoqu_task_id_detail)
            sql = """select * from task_Detail where tid = {};""".format(self.huoqu_task_id_detail)
            data_list = []
            headers_list = []
            exit_data_list = []
            # print('huoqu_task_id_detail ========= > ',huoqu_task_id_detail)
            objs = cursor.execute(sql)
            if objs:
                for obj in objs:
                    sql = """select create_time, paiming, is_shoulu from task_Detail_Data where tid = {} order by create_time desc limit 3""".format(obj[0])
                    cursor = conn.cursor()
                    detail_dataobjs = cursor.execute(sql)
                    data_detail_list = []
                    if detail_dataobjs:
                        sanci_chaxun = {}
                        for detaildata_obj in detail_dataobjs:
                            detail_create = detaildata_obj[0]
                            detail_paiming = detaildata_obj[1]
                            detail_shoulu = detaildata_obj[2]
                            if detail_create not in headers_list:
                                headers_list.append(detail_create)
                            sanci_chaxun[detail_create] = {
                                    'detail_create': detail_create,
                                    'shoulu': detail_shoulu,
                                    'paiming': detail_paiming
                                    }
                    data_list.append({
                        'id': obj[0],
                        'search_engine': obj[2],
                        'lianjie': obj[3],
                        'keywords': obj[4],
                        'mohupipei': obj[5],
                        'sanci_chaxun': sanci_chaxun
                    })
                exit_data_list = {
                    'data_list': data_list,
                    'headers_list': headers_list
                }
            print('data_list-------------------->', json.dumps(exit_data_list))
            return json.dumps(exit_data_list)

    # 重点词监护 - 导出 excl 功能
    def set_save_select_results_task_excel_daochu(self, tid_data):
        if tid_data:
            # print('tid_data-------------> ', tid_data)
            conn = sqlite3.connect('./my_db/my_sqlite.db')
            cursor = conn.cursor()
            now_date = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
            wb = Workbook()
            ws = wb.active
            ws.cell(row=1, column=1, value="重点关键词")
            ws.cell(row=2, column=1, value="任务名称:")
            ws.cell(row=3, column=1, value="关键词")
            ws.cell(row=3, column=2, value="网址")
            ws.cell(row=3, column=3, value="搜索引擎")
            ws.cell(row=4, column=4, value="排名")
            ws.cell(row=4, column=5, value="排名")
            ws.cell(row=4, column=6, value="排名")
            ft1 = Font(name='宋体', size=22)
            a1 = ws['A1']
            a1.font = ft1

            # 合并单元格        开始行      结束行       哪列做改变       占几列
            ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=6)
            ws.merge_cells(start_row=3, end_row=4, start_column=1, end_column=1)
            ws.merge_cells(start_row=3, end_row=4, start_column=2, end_column=2)
            ws.merge_cells(start_row=3, end_row=4, start_column=3, end_column=3)

            # print('设置列宽')
            ws.column_dimensions['A'].width = 50
            ws.column_dimensions['B'].width = 45
            ws.column_dimensions['C'].width = 15
            ws.column_dimensions['D'].width = 30
            ws.column_dimensions['E'].width = 42
            ws.column_dimensions['F'].width = 39
            ws.column_dimensions['G'].width = 39
            ws.column_dimensions['H'].width = 39

            # print('设置行高')
            ws.row_dimensions[1].height = 28
            ws.row_dimensions[2].height = 38
            ws.row_dimensions[3].height = 28
            ws.row_dimensions[4].height = 20

            # print('文本居中')
            ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
            ws['A2'].alignment = Alignment(horizontal='right', vertical='center')
            ws['B2'].alignment = Alignment(horizontal='left', vertical='center')
            ws['C3'].alignment = Alignment(horizontal='center', vertical='center')
            ws['A3'].alignment = Alignment(horizontal='center', vertical='center')
            ws['B3'].alignment = Alignment(horizontal='center', vertical='center')
            ws['A4'].alignment = Alignment(horizontal='center', vertical='center')

            sql = """select task_name from task_List where id = {};""".format(tid_data)
            task_names = cursor.execute(sql)
            task_name = list(task_names)[0][0]

            sql = """select * from task_Detail where tid = {};""".format(tid_data)
            cursor.execute(sql)
            row = 5
            for obj in cursor:
                tid = obj[0]
                sql = 'select * from task_Detail_Data where tid = {} order by create_time desc limit 3  ;'.format(tid)
                cursor = conn.cursor()
                objs_data = cursor.execute(sql)
                if objs_data:
                    column_p = 4
                    for obj_data in objs_data:
                        create_time = obj_data[4]
                        paiming = obj_data[1]
                        # print('paiming--------------> ', paiming)
                        ws.cell(row=3, column=column_p, value="{create_time}".format(create_time=create_time))
                        ws.cell(row=row, column=column_p, value="{paiming}".format(paiming=paiming))
                        column_p += 1
                ws.cell(row=2, column=2, value="任务名")
                ws.cell(row=row, column=1, value="{keywords}".format(keywords=obj[4]))
                ws.cell(row=row, column=3, value="{search_engine}".format(search_engine=obj[2]))
                ws.cell(row=row, column=2, value="{lianjie}".format(lianjie=obj[3]))
                row += 1
            root = Tk()
            root.iconbitmap('./128.ico')
            root.withdraw()  # 隐藏
            dirname = askdirectory(parent=root, initialdir="/", title='选择导出路径 !')
            print(dirname)
            if dirname:
                if dirname == 'C:/':
                    tkinter.messagebox.showerror('错误', '请选择路径 !')
                    # tkinter.messagebox.showwarning('警告', '请选择路径 !')
                else:
                    file_name = dirname.replace('\\', '/') + '/' + '{}.xlsx'.format(task_name + '_' + now_date)
                    wb.save(file_name)
                    print(file_name)
                    tkinter.messagebox.showinfo('提示', '生成完毕 !')
            else:
                print('点击取消')
            root.destroy()  # 销毁


    # 收录查询 - 筛选链接 调用多线程 保存数据库
    def set_shoulu_select_get_list_value(self, data):
        if data:
            data_list = [
            'http://www.iiijk.com/cjxw/04-74547.html',
            'http://news.100yiyao.com/detail/193538290.html          ',
            'http://news.qiuyi.cn/html/2017/fuke_1205/63968.html     ',
            'http://at.025ct.com/dt/2017/1204/514781.html            ',
            'http://www.jianzhijia.com/hyzx/jkjd/79379.html          ',
            'http://news.39.net/a/171204/5901183.html                ',
            'http://news.39.net/a/171204/5901194.html                ',
            'http://news.360xh.com/201712/04/37416.html              ',
            'http://www.iiijk.com/cjxw/04-74550.html                 ',
            'http://www.jianzhijia.com/hyzx/jkjd/79381.html          ',
            'http://news.qiuyi.cn/html/2017/zhengxing_1204/63922.html',
            'http://news.39.net/a/171204/5902419.html                ',
            'http://www.jianzhijia.com/hyzx/jkjd/79383.html          ',
            'http://news.360xh.com/201712/04/37402.html              ',
            'http://www.sohu.com/a/208330800_544906                  ',
            'http://www.iiijk.com/cjxw/04-74552.html                 ',
            'http://www.iiijk.com/cjxw/04-74551.html                 ',
            'http://focus.smxe.cn/20171204/148402.shtml              ',
            'http://news.360xh.com/201712/04/37408.html              ',
            'http://news.39.net/a/171204/5902423.html                ',
            'http://www.jianzhijia.com/hyzx/jkjd/79385.html          ',
            'http://news.360xh.com/201712/04/37409.html              ',
            'http://news.360xh.com/201712/04/37410.html              ',
            'http://news.100yiyao.com/detail/193538295.html          ',
            'http://www.jianzhijia.com/hyzx/jkjd/79387.html          ',
            'http://news.100yiyao.com/detail/193538308.html          ',
            'http://news.360xh.com/201712/04/37411.html              ',
            'http://news.39.net/a/171204/5902507.html                ',
            'http://news.360xh.com/201712/04/37412.html              ',
            'http://www.jianzhijia.com/hyzx/jkjd/79388.html          ',
            'http://news.39.net/a/171204/5902519.html                ',
            'http://news.360xh.com/201712/04/37414.html              ',
            'http://www.jianzhijia.com/hyzx/jkjd/79389.html          ',
            'http://news.cx368.com/news/gd/2017/1204/69128.html      ',]
            print('开始遍历')
            self.huoqu_shoulu_time_stamp = int(time.time())
            self.dangqian_chaxunshoulu_time = datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')
            p = 0
            for url in data_list:
                yinqing = '1'
                threading_task.func_shoulu_chaxun(yinqing, url, self.huoqu_shoulu_time_stamp)
            print('多线程 结束')

    # 收录查询 - 查询数据库 展示
    def get_shoulu_zhanshi_list_value(self):
        # sleep(3)
        if self.huoqu_shoulu_time_stamp:
            conn = sqlite3.connect('./my_db/my_sqlite.db')
            cursor = conn.cursor()
            # print('huoqu_shoulu_time_stamp ============>', self.huoqu_shoulu_time_stamp)
            sql = """select url,is_shoulu from shoulu_Linshi_List where {time_stamp};""".format(
                time_stamp=self.huoqu_shoulu_time_stamp)
            cursor.execute(sql)
            data_list = []
            for obj in cursor:
                url = obj[0]
                is_shoulu = obj[1]
                data_list.append({
                    'url': url,
                    'is_shoulu': is_shoulu
                })
            print(data_list)
            return json.dumps(data_list)

    # 收录查询 - 查询数据库 导出excel表格
    def set_shoulu_save_select_result_value(self, data):
        # if self.huoqu_shoulu_time_stamp:
        if 1+1==2:
            # huoqu_shoulu_time_stamp = '1531981854'
            conn = sqlite3.connect('./my_db/my_sqlite.db')
            cursor = conn.cursor()
            now_date = datetime.date.today().strftime('%Y-%m-%d')
            sql = """select url,is_shoulu,title,search,kuaizhao_time from shoulu_Linshi_List where {time_stamp};""".format(
                time_stamp=self.huoqu_shoulu_time_stamp)
                # time_stamp=huoqu_shoulu_time_stamp)
            cursor.execute(sql)
            wb = Workbook()
            ws = wb.active
            ws.cell(row=1, column=1, value="收录查询")
            ws.cell(row=2, column=4, value="查询时间:")
            ws.cell(row=6, column=1, value="标题")
            ws.cell(row=6, column=2, value="网址")
            ws.cell(row=6, column=3, value="搜索引擎")
            ws.cell(row=6, column=4, value="收录")
            ws.cell(row=6, column=5, value="快照日期")
            ft1 = Font(name='宋体', size=22)
            a1 = ws['A1']
            a1.font = ft1

            # 合并单元格        开始行      结束行       用哪列          占用哪列
            ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=6)
            ws.merge_cells(start_row=2, end_row=5, start_column=1, end_column=1)
            ws.merge_cells(start_row=2, end_row=5, start_column=2, end_column=2)
            ws.merge_cells(start_row=2, end_row=5, start_column=3, end_column=3)
            ws.merge_cells(start_row=2, end_row=5, start_column=4, end_column=4)
            ws.merge_cells(start_row=2, end_row=5, start_column=5, end_column=5)

            # print('设置列宽')
            ws.column_dimensions['A'].width = 30
            ws.column_dimensions['B'].width = 30
            ws.column_dimensions['C'].width = 30
            ws.column_dimensions['D'].width = 30
            ws.column_dimensions['E'].width = 30
            ws.column_dimensions['F'].width = 30

            # print('设置行高')
            ws.row_dimensions[1].height = 28

            # print('文本居中')
            ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
            ws['D2'].alignment = Alignment(horizontal='center', vertical='center')
            ws['E2'].alignment = Alignment(horizontal='center', vertical='center')
            row = 7
            chaxun_time = self.dangqian_chaxunshoulu_time
            ws.cell(row=2, column=5, value="{chaxun_time}".format(chaxun_time=chaxun_time))
            for obj in cursor:
                is_shoulu = ''
                search = ''
                if obj[1] == '1':
                    is_shoulu = '已收录'
                else:
                    is_shoulu = '未收录'
                if obj[3] == 1:
                    search = '百度'
                else:
                    search = '手机百度'
                ws.cell(row=row, column=1, value="{title}".format(title=obj[2]))
                ws.cell(row=row, column=2, value="{url}".format(url=obj[0]))
                ws.cell(row=row, column=3, value="{search}".format(search=search))
                ws.cell(row=row, column=4, value="{is_shoulu}".format(is_shoulu=is_shoulu))
                ws.cell(row=row, column=5, value="{kuaizhao_time}".format(kuaizhao_time=obj[4]))
                row += 1

            root = Tk()
            root.withdraw()
            # ttk.Frame(root, padding="3 3 12 12")
            dirname = askdirectory(parent=root, initialdir="/", title='Pick a directory')
            if dirname:
                task_name = '测试导出收录excel'
                print('===================', dirname)
                file_name = dirname.replace('\\', '/') + '/' + '{}.xlsx'.format(task_name + '_' + now_date)
                print(file_name)
                wb.save(file_name)
                print('完成')


    # 覆盖查询 - 筛选查询条件 调用多线程 保存到数据库
    def set_fugai_select_get_list_value(self,data):
        print(data)



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

    loginValue = pyqtProperty(str, fget=get_Loginvalue, fset=set_Loginvalue)
    # 重点词监护 - 增加任务
    createTaskListValue = pyqtProperty(str, fget=get_zhongdianci_create_task_list_value,
        fset=set_zhongdianci_create_value)
    # 重点词监护 - 传递id 查询该id任务列表
    updateTaskListValue = pyqtProperty(str, fget=get_zhongdianci_update_task_list_data_value,
        fset=set_zhongdianci_update_task_list_value)
    # 重点词监护 - 使用↑id 修改任务列表
    updateDatavalue = pyqtProperty(str, fget=zhanwei_zhushou, fset=set_zhongdianci_update_data_value)
    # 重点词监护 - 清空该id的 任务列表 详情数据
    emptyDataTaskDetail = pyqtProperty(str, fget=zhanwei_zhushou, fset=set_zhongdianci_select_id_task_detail_value)
    # 重点词监护 - 获取id 查询该id详情
    selectDataTaskDetail = pyqtProperty(str, fget=get_zhongdianci_select_id_select_task_detail_value,
        fset=set_zhongdianci_select_id_select_task_detail_value)
    # 重点词监护 - 爬虫 - 获取id 分辨 移动或pc端
    pcTaskValue = pyqtProperty(str, fget=zhanwei_zhushou, fset=set_pc_task_value)
    # 重点词监护 - 删除单个或多个 任务
    deleteDataTask = pyqtProperty(str, fget=zhanwei_zhushou, fset=delete_or_batch_delete_task)
    # 重点词监护 - 查看所有子任务 任务详情
    viewThesubTasksDetail = pyqtProperty(str, fget=get_view_The_subtasks_detail,
        fset=set_task_id_view_The_subtasks_task)
    # 重点词监护 - 保存查询结果 导出excl表格
    saveTheQueryResults = pyqtProperty(str, fget=zhanwei_zhushou, fset=set_save_select_results_task_excel_daochu)

    # 爬虫 用户修改下次执行时间 添加数据库
    # pcTaskTimingValue = pyqtProperty(str,fget=zhanwei_zhushou, fset=set_pc_task_timing_value)
    # 收录查询 - 筛选链接 查询 及 展示入库
    setShouLuChaXun = pyqtProperty(str, fget=get_shoulu_zhanshi_list_value, fset=set_shoulu_select_get_list_value)
    # 收录查询 - 导出excel表格
    setShouLuDaoChuExcel = pyqtProperty(str, fget=zhanwei_zhushou, fset=set_shoulu_save_select_result_value)

    # setShouLuChaXun = pyqtProperty(str, fget=get_shoulu_zhanshi_list_value, fset=set_shoulu_select_get_list_value)


# PyQt 架构 与 数据库初始化 类
class DaNao(object):
    def __init__(self):
        self.initDB()
        self.main_body()

    # 初始化数据库和表
    def initDB(self):
        # 判断路径
        my_db_path = os.path.join('my_db')
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
            print('数据库的所有表名-=-=-==-=-=-=--=-===-=-=> ', data_list)

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

            # 判断 关键词详情数据
            if 'task_Detail_Data' not in data_list:
                print('没有task_Detail_Data ------- 创建task_Detail_Data')
                sql = """CREATE TABLE task_Detail_Data (
                      "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                      "paiming" integer,
                      "is_shoulu" integer,
                      "tid" integer,
                      "create_time" TEXT,
                      CONSTRAINT "task_Detail_Data_tid" FOREIGN KEY ("tid") REFERENCES "task_Detail" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT
                    );"""
                cursor.execute(sql)

            # 判断 收录临时 表
            if 'shoulu_Linshi_List' not in data_list:
                print('没有shoulu_Linshi_List表  创建shoulu_Linshi_List表')
                sql = """CREATE TABLE shoulu_Linshi_List (
                        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        "url" TEXT,
                        "is_shoulu" TEXT,
                        "time_stamp" TEXT,
                        "title" TEXT,
                        "search" integer,
                        "kuaizhao_time" TEXT
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
        view.load(QUrl('http://192.168.10.240:8080'))
        # view.load(QUrl('http://192.168.10.252:8080'))
        # view.load(QUrl('C:/pycharm zh/danaoPyQt/mian/web/index.html'))

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
