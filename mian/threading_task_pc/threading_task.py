from multiprocessing import Queue
import sqlite3, os, sys, json, re, time
from mian.threading_task_pc import mobile_fugai_pipei, mobile_url_accurate, pc_url_accurate, pc_fugai_pipei
from time import sleep




def thread_pcurl(keywords, domain, pool):
    print('进入线程--thread_pcurl--> ', ' pc端 有链接', keywords, domain)
    # pc_url_accurate.Baidu_Zhidao_URL_PC(keywords, domain)
    sleep(5)
    print('=---------------------------')
    pool.add_thread()


def thread_mobileurl(keywords, domain, pool):
    sleep(5)
    print('进入线程--thread_mobileurl--> ', ' 移动端 有链接', keywords, domain)
    # mobile_url_accurate.Baidu_Zhidao_URL_MOBILE(keywords, domain)
    pool.add_thread()


def thread_pcmohupipei(keywords, domain, pool):
    sleep(5)
    print('进入线程--thread_pcmohupipei--> ',' pc端 无链接',keywords, domain)
    # pc_fugai_pipei.Baidu_Zhidao_yuming_pc(keywords, domain)
    pool.add_thread()


def thread_mobilemohupipei(keywords, domain, pool):
    sleep(5)
    print('进入线程--thread_mobilemohupipei--> ','移动端 无链接',keywords, domain)
    # mobile_fugai_pipei.Baidu_Zhidao_yuming_mobile(keywords, domain)
    pool.add_thread()


def func(lianjie, keywords, search_engine, mohupipei, pool):
    # 去线程池里那一个线程，如果有，则池子里拿，如果没有，等直到有人归还线程到线程池
    thread_obj = pool.get_thread()
    if lianjie:
        if search_engine == '4':
            # print('进入线程----> ','移动端 有链接',keywords)

            thread_mobile_url = thread_obj(target=thread_mobileurl, args=(keywords,lianjie,pool))
            thread_mobile_url.start()

        if search_engine == '1':
            # print('进入线程----> ',' pc端 有链接',keywords)
            thread_pc_url = thread_obj(target=thread_pcurl, args=(keywords,lianjie,pool))
            thread_pc_url.start()

    else:
        if search_engine == '4':
            # print('进入线程----> ','移动端 无链接',keywords)
            thread_mobile_mohupipei = thread_obj(target=thread_mobilemohupipei, args=(keywords,mohupipei,pool))
            thread_mobile_mohupipei.start()

        else:
            # print('进入线程----> ',' pc端 无链接',keywords)
            thread_pc_mohupipei = thread_obj(target=thread_pcmohupipei, args=(keywords,mohupipei,pool))
            thread_pc_mohupipei.start()



