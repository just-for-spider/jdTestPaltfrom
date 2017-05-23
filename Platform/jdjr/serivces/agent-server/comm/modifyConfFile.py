#-*- coding:utf-8-*-
'''
Created on 2017-1-13
@author: liangdongdong1
'''

import re

def modify_conf_file(packageName, packageFullName, deviceName, packageActivity):  #修改appium 配置文件
    oldlines = open("E:/Platform/Platform/jdjr/serivces/appium_serivces/config.conf").readlines()  #打开文件读取信息

    fp = open("E:/Platform/Platform/jdjr/serivces/appium_serivces/config.conf","w")  # 写入信息
    for line in oldlines:
        if "=" in line:
            conf_value = line.split("=")[1]
            print conf_value
            if "packageName" in line:
                fp.write(line.replace(conf_value,packageName))
                fp.write("\n")
            elif "packageFullName" in line:
                fp.write(line.replace(conf_value, packageFullName))
                fp.write("\n")
            elif "deviceName" in line:
                fp.write(line.replace(conf_value, deviceName))
                fp.write("\n")
            elif "packageActivity" in line:
                fp.write(line.replace(conf_value, packageActivity))
                fp.write("\n")
            else:
                fp.write(line)
        else:
            fp.write(line)
    fp.close()



def analyze_script(script_path): #解析脚本、返回对应的类名、方法名
    total_list = []
    method_list = []
    try:
        fp = open(script_path)
        for line in fp.readlines():
            if "class" in line:
                class_name = re.findall(r"class (.+?)\(initInfo.appTest", line)  #正则获取类
            elif "def" in line:
                method_name = re.findall(r"def (.+?)\(self", line)[0]  #获取类中的方法
                method_list.append(method_name)
        total_list.append(class_name)
        total_list.append(method_list)
        return total_list
    except Exception,e:
        return total_list


def analyze_script_from(case_list):  # 解析script脚本信息修改file_part生成执行脚本
    oldlines = open("E:/Platform/Platform/jdjr/serivces/appium_serivces/file_part.py").readlines()  # 打开文件读取信息

    fp = open("E:/Platform/Platform/jdjr/serivces/appium_serivces/file_part.py", "w")  # 写入信息
    case_value = oldlines[2].split("= ")[1]
    fp.write(line.replace(case_value, case_list))
    fp.write("\n")
    fp.close()



#modify_conf_file(packageName="com.jingdong.app.reader", packageFullName="jingdongyuedu_264000.apk", deviceName="S7TDU16309000672", packageActivity="com.jingdong.app.reader.activity.MainActivity", packagePath="E:/Platform/Platform/jdjr/static/android_apk/apk/")
print analyze_script("E:/Platform/Platform/jdjr/serivces/appium_serivces/case/testCase.py")