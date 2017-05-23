# ---coding=utf-8----
'''
Created on 2016-12-14
@author: liangdongdong1
'''

import os
import subprocess
import re

packageName = os.popen("aapt dump badging E:\\Platform\\Platform\\jdjr\\static\\android_apk\\com.ss.android.article.news_031213.apk" ).read()
print packageName
infos = re.findall("launchable-activity: name='(.*)'  label=", packageName) #正则
print infos[0]


