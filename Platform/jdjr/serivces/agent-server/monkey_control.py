#-*- coding:utf-8-*-
'''
Created on 2017-1-13
@author: liangdongdong1
'''
import gl
import re
import os
import uuid
import time
import linecache
import MySQLdb
import logging
import subprocess
import ConfigParser
import fileinput
from comm.logger import initlog
from comm import results
from comm import modifyConfFile


m_log = initlog("./logs/output.log")   #日志格式定义导入
m_config = gl.GL_CONFIG
CRASHLIST = []   #定义crash数组列表

def _init_config(): # 配置文件
    cf = ConfigParser.ConfigParser()
    cf.read("config.conf")

    m_config['db_ip'] = cf.get("db","ip")
    m_config['db_user'] = cf.get("db","user")
    m_config['db_pwd'] = cf.get("db","pwd")
    m_config['db_name'] = cf.get("db","db_name")
    m_config['db_port'] = cf.getint("db","port")
    m_config['report_folder'] = cf.get("autopy","report_folder")
    m_config['base_path'] = cf.get("autopy","base_path")
    m_config['apk_path'] = cf.get("autopy","apk_path")
    m_config['script_path'] = cf.get("autopy","script_path")
 
 
def ReadFile(base_path,logName,task_type,serialId): #获取文件，解析文件
    
    log_path = base_path + logName
    analysis_log = subprocess.Popen('adb -s %s logcat -d >%s' % (serialId, log_path), shell=True)
    exitcode = analysis_log.wait()
    if exitcode != 0:
        return 1
    try:
        rp = open(log_path,'r')
        if task_type == "1":
            for crashLine in rp.readlines():
                line_num = 1
                if 'crash' in crashLine or "ANR" in crashLine or "Crash" in crashLine or "Exception" in crashLine:
                    for i in (line_num,line_num + 20):
                        check_key = linecache.getline(log_path, i)
                        if logName in check_key:
                            CRASHLIST.append(crashLine)
            return len(CRASHLIST)
        
        elif task_type == "0":
            for crashLine in rp.readlines():
                if 'OutOfMemory' in crashLine:
                    CRASHLIST.append(crashLine)
            return len(CRASHLIST)
    except Exception,e:
        logging.info('Except:' + str(e))
        return 0
    
'''
def get_erialnumber_list(): #通过STF  获取全部 PC 机连接手机
    import rethinkdb as r
    serial_list = []
    conn = r.connect(host='10.13.16.151',db='stf',port=28015)
    conn.use('stf')
    for doc in r.table('devices').run(conn):
        infos = re.findall(r"present\':(.+?),", str(doc))  # 正则
        if "True" in str(infos):
            serial = re.findall(r"serial\':(.+?),", str(doc))  # 正则
            #serial = serial.encode("utf-8")
            serial =  serial[0].replace('\'','').replace(' u','')
            serial_list.append(serial)
        else:
            pass
    return serial_list
'''



def get_erialnumber_list(): #获取全部 PC 机连接手机
    infos = subprocess.Popen("adb devices", stdout=subprocess.PIPE, shell=True)
    sub_recode = infos.wait() 
    if sub_recode != 0:
        return 1
    adb_shell_info = infos.stdout.read()
    infos = re.findall(r"(.+?)\tdevice", adb_shell_info) #正则
    return infos


def get_activity(base_packagename): #获取首页面activity信息
    packageName = os.popen("aapt dump badging %s" % base_packagename).read()
    infos = re.findall("launchable-activity: name='(.*)'  label=", packageName) #正则获取到首页面的activity信息
    return infos[0]


def get_packgName(base_packagename): #获取包名
    #packageName = os.popen("aapt dump badging E:\\Platform\\Platform\\jdjr\\static\\android_apk\\com.ss.android.article.news_031213.apk" ).read()
    packageName = os.popen("aapt dump badging %s" % base_packagename).read()
    infos = re.findall("package: name='(.*)' versionCode", packageName) #正则获取到首页面的activity信息
    return infos[0]

def run_autoScript(S_file): # 通过进程管理，调用appium服务
    run_recode = subprocess.Popen("python %s" %  S_file, stdout=subprocess.PIPE, shell=True)
    sub_recode = run_recode.wait()
    if sub_recode != 0:
        return 1
    print sub_recode
    return "pass"


def batch_install_task(serialId_List, packageName, cur, task_id):# 批量安装启动卸载
    batch_install_result = {}  #存放安装结果list
    try:
        for serialId in serialId_List:
            cur.execute("select phone from manage_phone where device='%s'" %  serialId)
            phone = cur.fetchone()[0].decode("ascii").encode("utf-8")
            m_log.info("执行手机为: %s 机器" % phone)
            m_log.info("开始安装: %s 机器" % phone)
            install_process = subprocess.Popen('adb -s %s install -r %s' % (serialId, packageName), stdout=subprocess.PIPE, shell=True)
            P_Name = get_packgName(packageName)#通过安装包获取到packageName
           
            if "Success" in install_process.stdout.read():
                batch_install_result[phone] = "安装成功"  #  安装通过
                time.sleep(5) #等待安装完成，开启首页面
                activity = get_activity(packageName) #获取activity名字
                start_activity = os.popen("adb -s %s shell am start -n %s/%s" % (serialId, P_Name, activity)).read()#通过安装包获取到packageName

                time.sleep(10)  #等待服务启动
                if "Starting" in start_activity:
                    batch_install_result[phone] = "启动成功" #启动成功
                    uninstall_result = os.popen("adb -s %s uninstall %s" % (serialId, P_Name)).read()  #卸载相关的安装包
                    if "Success" in uninstall_result:
                        batch_install_result[phone] = "验证通过"  #卸载成功
                        m_log.info("%s机器安装\启动\卸载%s成功" % (phone, P_Name))
                    else:
                       batch_install_result[phone] = "卸载失败"
                       m_log.info("%s机器安装 %s成功,卸载失败" % (phone, P_Name))
                else:
                    batch_install_result[phone] = "启动失败"
                    m_log.info("%s机器安装 %s成功,启动失败" % (phone, P_Name))
            else:
                batch_install_result[phone] = "安装失败"
                m_log.info("%s机器安装 %s失败" % (phone,P_Name))
        #开始生成测试报告
        uuid_name = str(uuid.uuid1())
        report_name = m_config['report_folder'] + uuid_name
        results.output_results(report_name, batch_install_result, P_Name)
        cur.execute("update manage_task SET log_path='%s' where id=%s" %  (uuid_name +".html",task_id))
        m_log.info("生成测试报告完成")

        return batch_install_result
    except Exception,e:
        return str(e)


def run_monkey(serialId, packageName, cur, content):
        m_log.info("开始安装: %s 机器" % serialId)
        try:
            install_process = subprocess.Popen('adb -s %s install -r %s' % (serialId, packageName), stdout=subprocess.PIPE, shell=True)
            #print install_process.stdout.read()
            #recode = install_process.wait()
            # print recode
            # if recode != 0:
            #     return 1
            if "Success" in install_process.stdout.read():
                m_log.info("安装apk成功")
                update_task_status(type="0", cur=cur, status_num="1", task_id= content[0][0], serialId = None) #更新手机以及任务状态
                m_log.info("更新完成手机以及任务状态")
                Name = get_packgName(packageName)
                m_log.info("获取安装的包名成功%s" % Name)
                time.sleep(5)
                run_process = subprocess.Popen('adb -s %s shell monkey -p %s  --ignore-crashes --ignore-timeouts -v %s' % (serialId, Name, 10000), shell=True)
                run_process.wait()
#                 if run_process != 0:
#                     return 1
                sumLIST = str(uuid.uuid1()) + ".log"  #生成日志文件
                m_log.info("准备生成日志文件:%s" % sumLIST)
                sum_Exec = ReadFile(m_config['base_path'], sumLIST, str(content[0][7]), serialId)   #content[0][7] 判断是什么类型的任务
                #base_path,logName,task_type
                m_log.info("生成文件成功...")
                
                update_task_status(type="0", cur=cur, status_num="2", task_id= content[0][0], serialId = None) #更新手机以及任务状态
                cur.execute('UPDATE manage_task SET task_status=2,error_num="%s",log_path="%s" WHERE id=%s' % (sum_Exec, sumLIST, content[0][0]))  #更新任务的执行状态
                m_log.info('更新完成')
                os.popen('adb -s %s logcat -c' % str(serialId))    #清理手机的日志信息，保证下次启动，日志信息采集的准确性
                m_log.info('日志清理完成...')
                #os.popen("adb kill-server")   # 清理adb进程,保证启动的adb进程在利用完手动清理掉
                cur.close()
                return "pass"
#             elif "Failure" in install_process.stdout.read():
#                 m_log.info('安装apk失败,存在问题...')
#                 update_task_status(type="0", cur=cur, status_num="4", task_id= content[0][0], serialId = None)
            else:
                print install_process.stdout.read()
                m_log.info('出现安装异常情况终止...')
                update_task_status(type="0", cur=cur, status_num="3", task_id= content[0][0], serialId = None) #更新手机以及任务状态
                return "fail"
            
        except Exception,e:
            #os.popen("adb kill-server")   # 清理adb进程,保证启动的adb进程在利用完手动清理掉
            update_task_status(type="0", cur=cur, status_num="3", task_id= content[0][0], serialId = None) #更新手机以及任务状态
            os.popen('adb logcat -c')    #清理手机的日志信息，保证下次启动，日志信息采集的准确性
            cur.close()
 
    
def _check_phone_status(list,cur):  #通过id获取到状态空闲的机器  list:手机id  cur 游标
    result_list = {}
    for i in list:
        cur.execute("select status,phone from manage_phone where device='%s'" % i)  #通过手机ID查询手机的使用状态
        phone_status = cur.fetchall()
        if phone_status[0][0] == "0":  #判断手机的使用状态 0：未使用   1 表示使用
            result_list[i] = phone_status[0][1]
        else:
            pass
    return result_list


def update_task_status(type, cur, status_num, task_id = None, serialId = None):    #更改手机、任务的状态方法
    if type == "0": # 0表示任务的status状态
        cur.execute('UPDATE manage_task SET task_status=%s WHERE  id=%s' % (status_num, task_id))
        cur.fetchall()
    elif type == "1": #1表示手机的status状态
        cur.execute('UPDATE manage_phone SET task_status=%s WHERE  device=%s' % (status_num, serialId))
        cur.fetchall()



def runTest():
    _init_config() #初始化配置文件
    m_log.info("配置文件初始化完成, 准备链接数据库...")
    gl.GL_DB_CONN = MySQLdb.connect(host= m_config['db_ip'],\
                            user= m_config['db_user'],\
                            passwd= m_config['db_pwd'],\
                            db= m_config['db_name'],\
                            port= 3306)  #链接数据库  初始化到全局 变量

    while True:
        cur = gl.GL_DB_CONN.cursor()  #链接数据库
        #联合查询三张表  获取相关数据
        #sql_code = 'select a.id, a.task_status, b.device, b.phone, b.`status`, c.packageName, a.log_path, a.task_type, a.error_num, a.check_install,a.check_startservice from manage_task a LEFT JOIN manage_phone b on a.excete_phone_id = b.id LEFT JOIN apk_package c on a.package_id = c.id where task_status=0 AND status=0  LIMIT 1;'
        sql_code = 'select a.id, a.task_status, b.device, b.phone, b.`status`, c.packageName, a.log_path, a.task_type, a.error_num, a.check_install,a.check_startservice, d.script_name, d.uuid_name from manage_task a LEFT JOIN manage_phone b on a.excete_phone_id = b.id LEFT JOIN apk_package c on a.package_id = c.id LEFT JOIN manage_script d on  a.script_id=d.id where task_status=0 AND status=0  LIMIT 1;'
        cur.execute(sql_code)
        content = cur.fetchall()  #获取到可执行的任务订单
        
        if content is not (): #判断是否有任务
            try:
                m_log.info("有任务进来, 正在获取相关任务信息...")
                m_log.info("任务信息:%s" % content)
                 
                Get_P_List = get_erialnumber_list()   #获取手机的个数，获取到List
                m_log.info("获取当前插入的手机: %s" % Get_P_List)
                
                pass_phone = _check_phone_status(Get_P_List, cur)  #check手机的使用状态  以及手机名称
                m_log.info("检测到可使用的手机数量: %s" % pass_phone)
                
                if content[0][7] == "2" and content[0][9] == "1": #获取content[0][7]到task_type     content[0][9]开启批量安装启动卸载服务   2=是批量执行
                    update_task_status(type="0", cur=cur, status_num="1", task_id=content[0][0], serialId = None) #更新手机以及任务状态
                    batch_result = batch_install_task(pass_phone.keys(),  m_config['apk_path'] + content[0][5], cur, content[0][0])
                    m_log.info("安装卸载结果: %s" % batch_result)
                    update_task_status(type="0", cur=cur, status_num="2", task_id=content[0][0], serialId = None) #更新手机以及任务状态

                elif content[0][7] == "0" or content[0][7] == "1":
                    update_task_status(type="0", cur=cur, status_num="1", task_id=content[0][0], serialId = None) #更新手机以及任务状态
                    run_monkey(content[0][2], m_config['apk_path']+content[0][5], cur, content)

                elif content[0][7] == "3":
                    m_log.info("-----------此任务为自动化执行")
                    # modifyConfFile.analyze_script_from(content[0][11])  #通过输入的执行用例list，替换配置文件
                    packageNa = get_packgName(m_config['apk_path'] + str(content[0][5]))  #获取包名
                    first_page_ctivity = get_activity(m_config['apk_path'] + str(content[0][5]))  #获取activity信息
                    modifyConfFile.modify_conf_file(packageName = packageNa, packageFullName=content[0][5], deviceName=content[0][2] , packageActivity=first_page_ctivity)

                    update_task_status(type="0", cur=cur, status_num="1", task_id = content[0][0],
                                       serialId=None)  # 更新任务状态为执行中...
                    run_recode = run_autoScript(m_config['script_path'] + str(content[0][12])) # 指定appium脚本

                    if run_recode == "pass":
                        m_log.info("执行完成，等待生成测试报告")
                        update_task_status(type="0", cur=cur, status_num="2", task_id= content[0][0],serialId= None)  # 更新手机以及任务状态
                    else:
                        m_log.info("执行异常，请检查")
                        update_task_status(type="0", cur=cur, status_num="3", task_id= content[0][0], serialId= None)  # 更新手机以及任务状态

                else:
                    m_log.info("此任务没有开启检测项, 更改测试结果")
                    update_task_status(type="0", cur=cur, status_num= "5", task_id=content[0][0], serialId= None) #更新手机以及任务状态
                time.sleep(5)
                m_log.info(3 *"\n")
            except Exception,e:
                m_log.info(str(e))  #打印异常
                update_task_status(type="0", cur=cur, status_num="3", task_id=content[0][0], serialId = None)  #更新手机以及任务状态
        else:
            m_log.info("无可执行任务,sleep等待执行..")
            time.sleep(8)
            
               


if __name__ == "__main__":
    runTest()
'''************************************************************************
        1、检测手机是否连接成功
        2、DB中链表查询手机空闲、任务空闲的task
        3、把对应的手机状态，任务状态修改为使用状态 
        4、通过对应的ID获取到安装包的名字，安装
        5、开始运行稳定性测试
        6、判断是否运行完成，计算日志中的问题，生成对应的日志
        7、运行结束，把手机与任务状态更新
        8、清理手机的logcat日志，继续轮询，执行下一条任务
#*************************************************************************'''