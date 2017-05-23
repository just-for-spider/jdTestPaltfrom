# ---coding=utf-8----
'''
Created on 2016-12-14
@author: liangdongdong1
'''

import os
import re

from flask import Blueprint, request, redirect, url_for
from werkzeug import secure_filename
from jdjr import mysql
import subprocess
import time
import uuid




UPLOAD_FOLDER = './jdjr/static/android_apk/apk/'  #上传文件路径
UPLOAD_FOLDER_SCRIPT = './jdjr/serivces/appium_serivces/case/'  #上传appium py脚本路径
APK_PATH = "E:/Platform/Platform/jdjr/static/android_apk/apk/"  #APK包的路径



monkey_test = Blueprint('monkey_test', __name__,
                        template_folder='templates')


@monkey_test.route('/upload', methods=['POST'])  #上传安卓自动化apk安装包
def apkupload():
    if request.method == 'POST':
        filek = request.files['file']

        if filek and allowed_file(filek.filename):
            filename = secure_filename(filek.filename)
            filek.save(os.path.join(UPLOAD_FOLDER, filename))
            cursor = mysql.connect().cursor()
            cursor.execute('INSERT INTO apk_package (packageName) VALUES ("%s")' % (filename))
            cursor.fetchone()
            cursor.close()
            return '{"error":""}'
        else:
            return '{"error":"fileupload error"}'


@monkey_test.route('/Supload', methods=['POST'])  # 上传py脚本执行Appium
def Supload():
    if request.method == 'POST':
        filek = request.files['file_py']
        uuid_name = "test" + str(int(time.time()))+".py"
        if filek and allowed_script_file(filek.filename):
            filename = secure_filename(filek.filename)
            filek.save(os.path.join(UPLOAD_FOLDER_SCRIPT, uuid_name))
            cursor = mysql.connect().cursor()
            cursor.execute('INSERT INTO manage_script (script_name,uuid_name) VALUES ("%s","%s")' % (filename,uuid_name))
            cursor.fetchone()
            cursor.close()
            return '{"error":""}'
        else:
            return '{"error":"fileupload error"}'
        
        
@monkey_test.route('/jQuerrequestiphoneinfo',methods=['GET'])  #通过ajax获取信息
def jQuerrequestiphoneinfo():
    if request.method == "GET":
        packageName = request.args.get("package_name")
        cmd_arg = "aapt dump badging %s%s" % (APK_PATH, packageName)

        infos = subprocess.Popen(cmd_arg, stdout=subprocess.PIPE, shell=True).stdout.read()
        return infos



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['apk'])

def allowed_script_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['py'])
           



#****************************************************手机安装apk部分******************************************************************
def get_erialnumber_list(): #判断链接手机的数量
    infos = subprocess.Popen("adb devices", stdout=subprocess.PIPE, shell=True)
    sub_recode = infos.wait() 
    if sub_recode != 0:
        return 1
    adb_shell_info = infos.stdout.read()
    infos = re.findall(r"(.+?)\tdevice", adb_shell_info) #正则获取
    return infos




#*********************************************************************************************
def check_phoneList_status(serial):  #通过serial_id检测手机的使用状态,
    status_code = []
    cursor = mysql.connect().cursor()
    for i in serial:
        cursor.execute('select status from manage_phone where device="%s"' % (i))
        phone_status = cursor.fetchone()
        status_code.append(phone_status)
    cursor.close()
    print status_code
    if '0' in str(status_code):
        return '{"recode":"0","info":"ture"}'
    else:
        return '{"recode":"1","info":"false"}'
    
    
    
#**********************************************************************************************
def installapk_all_phone(packagename):#安装apk到可用的机器列表
    cursor = mysql.connect().cursor()
    arg = "adb install -r E:/Platform/Platform/jdjr/static/android_apk/%s" %  packagename
    
    #判断手机的使用状态
    cursor.execute("select status from manage_phone")
    phone_status = cursor.fetchone()
    if phone_status[0] == "0":
        infos = subprocess.Popen(arg, stdout=subprocess.PIPE, shell=True) 
        sub_infos = infos.stdout.read()
     
        if "Success" in sub_infos:
            return '安装成功'
        else:
            return '安装失败'
    else:
        return '机器在忙碌, 没有可执行任务的手机.. 请稍后再试.'
    os.popen("adb kill-server")
    
    
    
#*******************************************************************************************************
@monkey_test.route('/jQuerrequestinstall',methods=['GET']) #通过adb命令处理是否要安装手机
def jQuerrequestinstall():
    if request.method == "GET":
        check_status = check_phoneList_status(["0815f8a4514e2d05"])
        print check_status
        if eval(check_status)["recode"] == "0":
            print eval(check_status)["recode"]
            packageName = request.args.get("package_name_install") #获取前端传递的安装包信息
            onoff_info = installapk_all_phone(packageName)  #调用installapk_all_phone
            return onoff_info
        else:
            return "暂时无可用机器"
        

        
        
#********************************************************************************************************
@monkey_test.route('/jQuerrequestcheckoomtask',methods=['GET']) #下达检测应用是否存在OOM任务
def jQuerrequestcheckoomtask():
    cursor = mysql.connect().cursor()
    if request.method == "GET":
        package_id = request.args.get("package_id") #获取传递过来的安装包
        execut_phone_id = request.args.get("execut_phone_id") #获取要执行的机型
        try:
            cursor.execute('INSERT INTO manage_task (excete_phone_id, package_id, task_status, task_type) VALUES ("%s","%s","0","0")' % (str(execut_phone_id), str(package_id)))
            cursor.fetchone()
            return '任务已生成'
        except Exception,e:
            return '任务生成异常:%s' % str(e)
    else:
        return "请求为不支持方式"


#********************************************************************************************************
@monkey_test.route('/jQuerrequestcheckcrashtask',methods=['GET']) #下达检测应用是否存在稳定性测试任务
def jQuerrequestcheckcrashtask():
    cursor = mysql.connect().cursor()
    if request.method == "GET":
        package_id = request.args.get("package_id_2") #获取传递过来的安装包
        execut_phone_id = request.args.get("execut_phone_id_2") #获取要执行的机型
        try:
            cursor.execute('INSERT INTO manage_task (excete_phone_id, package_id, task_status, task_type) VALUES ("%s","%s","0","1")' % (str(execut_phone_id), str(package_id)))
            cursor.fetchone()
            return '任务已生成'
        
        except Exception,e:
            return '任务生成异常: %s' % str(e)
    else:
        return "请求为不支持方式 "
    

#********************************************************************************************************
@monkey_test.route('/jQuerrequestcheckBestTest',methods=['GET']) #下达批量执行任务
def jQuerrequestcheckBestTest():
    cursor = mysql.connect().cursor()
    if request.method == "GET":
        check_package_name = request.args.get("check_package_name") #获取传递过来的安装包
        check_install = request.args.get("check_install") #判断是否批量安装
        #check_startservice = request.args.get("check_startservice") #判断是否批量启动服务
        try: #检测是否为批量执行任务，通过task_type来查看
            cursor.execute('INSERT INTO manage_task (excete_phone_id, package_id, task_status, task_type,check_install,check_startservice) VALUES ("1","%s","0","2","%s","%s")' % (str(check_package_name),str(check_install),'2'))
            cursor.fetchone()
            return '任务已生成'
        except Exception,e:
            return '任务生成异常:%s' % str(e)
    else:
        return "请求为不支持方式"


#jQuerrequestScriptTest
@monkey_test.route('/jQuerrequestScriptTest', methods=['GET']) #下达执行自动化任务
def jQuerrequestScriptTest():
    cursor = mysql.connect().cursor()
    if request.method == "GET":
        auto_package_name = request.args.get("auto_package_name") #获取传递的安装包ID
        run_iphone = request.args.get("run_iphone") #获取要执行的手机
        auto_script = request.args.get("auto_script") #获取自动化脚本id
        run_case_list = request.args.get("run_case_list") #获取要执行的用例表

        try: #把参数插入到task任务中
            cursor.execute('INSERT INTO manage_task (excete_phone_id, package_id, script_id, task_status, task_type) VALUES ("%s","%s","%s", "0","3")' % (str(run_iphone),str(auto_package_name),str(auto_script)))
            cursor.fetchone()
            return '任务已生成'
        except Exception,e:
            return '任务生成异常:%s' % str(e)
    else:
        return "请求为不支持方式"

        
        
        
        
        
        
 
            
