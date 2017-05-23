# -*- coding: utf-8 -*-
import unittest
import ConfigParser
from appium import webdriver
import gl

m_config = gl.GL_CONFIG
cf = ConfigParser.ConfigParser()
cf.read("E:/Platform/Platform/jdjr/serivces/appium_serivces/config.conf")

m_config['packageName'] = cf.get("base", "packageName")
m_config['packageFullName'] = cf.get("base", "packageFullName")
m_config['packageActivity'] = cf.get("base", "packageActivity")
m_config['packagePath'] = cf.get("base", "packagePath")
m_config['deviceName'] = cf.get("base", "deviceName")

class appTest(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = ''
        desired_caps['app'] = m_config['packagePath'] + m_config['packageFullName']  # apk路径 + apk包名
        desired_caps['appPackage'] = m_config['packageName'] # 安装包名
        desired_caps['appActivity'] = m_config['packageActivity'] #启动首页面
        desired_caps['udid'] = m_config['deviceName']
        self.driver = webdriver.Remote('http://10.13.16.203:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

