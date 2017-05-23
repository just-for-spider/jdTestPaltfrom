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


reload(sys)
sys.setdefaultencoding('utf-8')


class ContactsAndroidTests(initInfo.appTest):
    def testin_one(self):
        print "run case1 pass"

    def testin_two(self):
        print "run case2 pass"


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ContactsAndroidTests('testin_one'))  #类名.方法
    suite.addTest(ContactsAndroidTests('testin_two'))
    conf._initConf(suite)
