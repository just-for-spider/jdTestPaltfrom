# -*- coding: utf-8 -*-

import time
import sys
import os
import uuid
import reportwriter

def erase_lastchar(fname):
    content = open(fname).read()
    with open(fname,'w') as handle:
        handle.write(content[:-1])

def output_results(results_dir,content, appInfo):  #生成测试报告方法
    report = reportwriter.Report(results_dir)

    report.write_line('<h1>研发测试部</h1>')
    report.write_line('<table class ="table table-bordered">')
    report.write_line('<caption>')
    report.write_line('<thead>')
    report.write_line('<tr><th>手机信息</th><th>测试app</th><th>测试类别</th><th>测试结果</th></tr>')
    report.write_line('</thead><tbody>')

    for (key,value) in zip(content.keys(),content.values()):
        if "失败" in value:
            report.write_line('<tr><td>%s</td ><td>%s</td><td>%s</td><td><b style="color:red">%s</b></td></tr>' % ((key, appInfo, "安装启动卸载", value)))
        else:
            report.write_line('<tr><td>%s</td ><td>%s</td><td>%s</td><td><b style="color:green">%s</b></td></tr>' % ((key, appInfo, "安装启动卸载", value)))
    report.write_line('</tbody></table>')

# if __name__ == '__main__':
#     output_results('../static/android_apk/report/%s' % uuid.uuid1(),{"三星":"通过","华为":"失败"})
