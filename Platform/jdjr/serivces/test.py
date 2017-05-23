#---coding:utf-8---

import re
import subprocess


def get_erialnumber_list():
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
print get_erialnumber_list()

# def get_erialnumber_list(): #获取全部 PC 机连接手机
#     infos = subprocess.Popen("adb devices", stdout=subprocess.PIPE, shell=True)
#     sub_recode = infos.wait()
#     if sub_recode != 0:
#         return 1
#     adb_shell_info = infos.stdout.read()
#     infos = re.findall(r"(.+?)\tdevice", adb_shell_info) #正则
#     return infos
#
# print get_erialnumber_list()
