# -*- coding: utf-8 -*-
'''
Created on 2017-1-10
@author: Administrator
'''
#coding=utf-8

import HTMLTestRunner
import sys
import unittest
import initInfo
import conf
import time


reload(sys)
sys.setdefaultencoding('utf-8')


class ContactsAndroidTests(initInfo.appTest):
    def testin_one(self):#停止人脸检测
        self.driver.find_element_by_name("启动人脸识别").click()
        for i in range(50):
            time.sleep(3)
            self.driver.find_element_by_name("停止").click()
            time.sleep(1)
            self.driver.find_element_by_name("重新启动").click()
            print "pass"


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ContactsAndroidTests('testin_one'))  #类名.方法
    #suite.addTest(ContactsAndroidTests('testin_two'))
    conf._initConf(suite)
