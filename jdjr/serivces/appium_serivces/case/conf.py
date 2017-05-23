# -*- coding: utf-8 -*-
'''
Created on 2016-6-14

@author: liangdongdong
'''
import time
import ConfigParser
import HTMLTestRunner
import gl
import MySQLdb
import uuid



m_config = gl.GL_CONFIG_DB
cf = ConfigParser.ConfigParser()
cf.read("E:/Platform/Platform/jdjr/serivces/appium_serivces/case/mysqlconn.conf")

m_config['db_ip'] = cf.get("db","ip")
m_config['db_user'] = cf.get("db","user")
m_config['db_pwd'] = cf.get("db","pwd")
m_config['db_name'] = cf.get("db","db_name")
m_config['db_port'] = cf.getint("db","port")

gl.GL_DB_CONN = MySQLdb.connect(host= m_config['db_ip'],\
                            user= m_config['db_user'],\
                            passwd= m_config['db_pwd'],\
                            db= m_config['db_name'],\
                            port= 3306)  #链接数据库  初始化到全局 变量

def _initConf(suite):
    cur = gl.GL_DB_CONN.cursor()
    uuid_name = str(uuid.uuid1())+".html"
    report_name = 'E:/Platform/Platform/jdjr/static/android_apk/auto_report/%s' %  uuid_name
    fp = file(report_name, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream = fp, title='安卓app自动化测试报告', description='测试研发部')
    runner.run(suite)
    cur.execute("update manage_task SET log_path='%s' where task_type=3 and task_status=1" % (uuid_name))
    fp.close()



