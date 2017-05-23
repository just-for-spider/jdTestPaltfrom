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
        for i in range(10000):
            time.sleep(5)
            self.driver.find_element_by_name("启动人脸检测").click()
            time.sleep(1)
            self.driver.find_element_by_name("停止人脸检测").click()
            time.sleep(1)
            self.driver.keyevent(4)
            print "run %s:" % str(i) + "Pass" 


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ContactsAndroidTests('testin_one'))  #类名.方法
    conf._initConf(suite)
