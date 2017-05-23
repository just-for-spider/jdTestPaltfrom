#---coding:utf-8---


# -*- coding:utf-8 -*-
import unittest
import os
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from time import sleep
import datetime

class MyIOSTests(unittest.TestCase):
    #开启猫宁3.0
    def setUp(self):
        app = os.path.join(os.path.dirname(__file__),
                           '/Users/xuyangting/Desktop/AttendanceAdminIOS/CloudRecord/build/Debug-iphonesimulator',
                           'CloudRecord.app')
        app = os.path.abspath(app)
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'platformName': 'iOS',
                'platformVersion': '8.4',
                'deviceName': 'iPhone 6'
            })

    #引导页滑屏处理
    def test_boot_page(self):
        sleep(10)
        self.driver.swipe(350, 300, 0, 300, 800)
        #滑屏的问题暂时还没解决，心好痛，Android滑屏文档先前也是用swipe不行，后来用drag搞定了，这次ios自动化又被滑屏卡到了，真的引导页虐我千百遍，我待它如初恋

    #登录猫宁3.0
    def test_login(self, mobile, password):
        #启动页滑屏处理
        self.test_boot_page()
        #登录
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[2]/UIAScrollView[1]/UIATextField[1]").send_keys(mobile)
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[2]/UIAScrollView[1]/UIASecureTextField[1]").send_keys(password)
        self.driver.hide_keyboard()
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[2]/UIAScrollView[1]/UIAButton[1]").click()
        sleep(5)

    #测试注册&忘记密码
    def test_reg_forget_password(self):
        pass

    #测试查询模块
    def test_query(self):
        self.test_login("13133847086", "123456")
        #测试按日
        #测试切换时间按日查询
        #测试未来时间
        self.driver.find_element_by_name("query dayCircle bt").click()
        self.driver.find_element_by_name("calender left arrow").click()
        self.driver.find_element_by_name("01").click()
        #测试过去时间
        self.driver.find_element_by_name("query dayCircle bt").click()
        self.driver.find_element_by_name("calender right arrow").click()
        self.driver.find_element_by_name("02").click()
        sleep(3)
        #测试按日数据
        choose = datetime.datetime.today().day
        if choose == 1:
            ch = "0" + str(choose)
        elif choose < 10 and choose > 1:
            ch = "0" + str(choose-1)
        else:
            ch = str(choose)
        self.driver.find_element_by_name("query dayCircle bt").click()
        sleep(5)
        self.driver.find_element_by_name(ch).click()
        sleep(3)
        #测试修改考勤 旷工改成事假
        self.driver.find_element_by_name("旷工").click()
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell[1]").click()
        self.driver.find_element_by_name("修改考勤").click()
        sleep(3)
        self.driver.find_element_by_name("事假").click()
        self.driver.find_element_by_name("确认修改").click()
        sleep(3)
        self.driver.find_element_by_name("backNavi bt").click()
        sleep(3)
        #刷新页面
        kuang_gong = self.driver.find_element_by_name("旷工")
        zheng_chang = self.driver.find_element_by_name("正常")
        action = TouchAction()
        action.press(kuang_gong).move_to(zheng_chang).release()
        #测试按月
        self.driver.find_element_by_name("按月").click()
        self.driver.find_element_by_name("确定").click()
        sleep(3)
        self.driver.find_element_by_name("backNavi bt").click()
        #测试选择月份
        self.driver.find_element_by_name("选择月份").click()
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[2]/UIAButton[2]").click()
        #测试选择员工
        self.driver.find_element_by_name("选择员工").click()
        sleep(3)
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell[1]").click()
        self.driver.find_element_by_name("确定").click()
        sleep(3)
        self.driver.find_element_by_name("确定").click()
        sleep(3)
        self.driver.find_element_by_name("backNavi bt").click()
        #测试选择排序
        self.driver.find_element_by_name("选择排序").click()
        self.driver.find_element_by_name("按在岗时长排序").click()
        self.driver.find_element_by_name("确定").click()
        sleep(3)
        self.driver.find_element_by_name("backNavi bt").click()
        self.driver.find_element_by_name("按字母排序").click()
        self.driver.find_element_by_name("确定").click()
        sleep(3)
        #测试导出结果
        self.driver.find_element_by_name("导出结果").click()
        email = "407708323@qq.com"
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIAScrollView[1]/UIATableView[1]/UIATableCell[1]/UIATextField[1]").send_keys(email)
        self.driver.find_element_by_name("取消").click()
        self.driver.find_element_by_name("导出结果").click()
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[4]/UIAAlert[1]/UIAScrollView[1]/UIATableView[1]/UIATableCell[1]/UIATextField[1]").send_keys(email)
        self.driver.find_element_by_name("好").click()
        sleep(5)
        #测试查看详情
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell[1]/UIAStaticText[5]").click()
        sleep(3)
        self.driver.find_element_by_name("查看异常").click()
        sleep(3)
        self.driver.find_element_by_name("backNavi bt").click()
        self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[2]/UIATableView[1]/UIATableCell[2]/UIAStaticText[5]").click()
        sleep(3)
        self.driver.find_element_by_name("查看异常").click()
        sleep(3)
        self.driver.find_element_by_name("backNavi bt").click()


    #调试
    def test(self):
        self.test_boot_page()

    #关闭猫宁3.0
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(MyIOSTests("test_reg_forget_password"))
    suite.addTest(MyIOSTests("test_query"))
    suite.addTest(MyIOSTests("test_manage"))
    suite.addTest(MyIOSTests("test_more"))
    #suite.addTest(MyIOSTests("test"))
    unittest.TextTestRunner(verbosity=2).run(suite)