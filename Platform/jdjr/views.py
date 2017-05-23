# ---coding=utf-8----
'''
Created on 2016-12-14
@author: liangdongdong1
'''

from jdjr import app
from flask import render_template,session
from jdjr import mysql
from auth import login_required

@app.route('/index') #博客页面
@login_required
def index():
    cursor = mysql.connect().cursor()
    cursor.execute('select * from blog ORDER BY id desc LIMIT 10')
    content = cursor.fetchall()
    cursor.close()
    print content
    return render_template('index.html',content = content, fullname=session.get('name'))

@app.route('/aq') #联调与问题解决
@login_required
def aq():
    return render_template('aq.html', fullname=session.get('name'))


@app.route('/login') #登录页面
def login():
    return render_template('login.html')


@app.route('/monkey')   #android手机客户端
@login_required
def monkey():
    cursor = mysql.connect().cursor()
    
    #获取安装包列表
    cursor.execute('SELECT id, packageName FROM apk_package WHERE id IN(SELECT MAX(id) FROM apk_package GROUP BY packageName) order by id desc;')
    packageInfo = cursor.fetchall()

    #手机安装列表
    cursor.execute('select distinct * from manage_phone where status=0 order by id desc;')
    managephoneInfo = cursor.fetchall()

    
    #通过手机列表、安装包列表、任务列表 链表查询   展示OOM列表
    cursor.execute('select a.id,a.task_status, b.device, b.phone, b.`status`, c.packageName, \
                    a.log_path, a.task_type,a.error_num,a.check_install, a.check_startservice from manage_task a LEFT JOIN \
                        manage_phone b on a.excete_phone_id = b.id LEFT JOIN apk_package c on a.package_id = c.id  \
                        where task_type=0 order by id desc;')
    task_total_info = cursor.fetchall()
    
    #通过手机列表、安装包列表、任务列表 链表查询   展示稳定性测试列表
    cursor.execute('select a.id,a.task_status, b.device, b.phone, b.`status`, c.packageName, \
                    a.log_path, a.task_type,a.error_num, a.check_install, a.check_startservice from manage_task a LEFT JOIN \
                        manage_phone b on a.excete_phone_id = b.id LEFT JOIN apk_package c on a.package_id = c.id  \
                        where task_type=1 order by id desc;')         
    random_task_total_info = cursor.fetchall()

    #查询appium脚本
    cursor.execute('select * from manage_script')
    script_total = cursor.fetchall()
    
    
    
    cursor.execute('select a.*,b.packageName from manage_task a LEFT JOIN apk_package b on a.package_id=b.id where task_type=2 order by id desc;')
    depth = cursor.fetchall()
    
    cursor.execute('select * from manage_phone')
    phone_total = cursor.fetchall()


    #自动化任务列表展示
    cursor.execute('select a.id,a.task_status, b.device, b.phone, b.`status`, c.packageName,a.log_path, a.task_type,a.error_num, a.check_install, \
                      a.check_startservice, d.script_name, d.uuid_name from manage_task a LEFT JOIN manage_phone b on a.excete_phone_id = b.id LEFT JOIN \
                          apk_package c on a.package_id = c.id  LEFT JOIN manage_script d on a.script_id = d.id where task_type=3 order by id desc;')
    autolist = cursor.fetchall()
    
    cursor.close()
    return render_template('monkey.html', \
                        packageInfo = packageInfo,\
                        managephoneInfo = managephoneInfo,\
                        task_total_info = task_total_info,\
                        random_task_total_info = random_task_total_info,\
                        depth = depth,\
                        phone_total = phone_total, \
                        script_total = script_total, \
                        autolist = autolist,\
                        fullname=session.get('name'))
    


@app.route('/grid')# 性能测试页面
@login_required
def grid():
    cursor = mysql.connect().cursor()
    cursor.execute('select * from manage_server')
    content = cursor.fetchall()
    print content
    cursor.close()
    return render_template('grid.html',content = content, fullname=session.get('name'))


@app.route('/mockservice')   #mock测试页面
@login_required
def mockservice():
    return render_template('mockservice.html',fullname=session.get('name'))


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


@app.route('/reqjson') #接口测试
@login_required
def reqjson():
    cursor = mysql.connect().cursor()
    cursor.execute('select type from protocal_type;')
    protocalType = cursor.fetchall()
    #print protocalType[0]
    return render_template('reqjson.html',protocalType = protocalType,fullname=session.get('name'))


@app.route('/account') #工具集页面
@login_required
def account():
    return render_template('account.html',fullname=session.get('name'))


@app.route('/test') #测试页面
@login_required
def test():
    return render_template('test.html')





