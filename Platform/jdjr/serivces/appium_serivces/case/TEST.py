#--coding:utf-8

import os


PATH = lambda p: os.path.abspath(
os.path.join(os.path.dirname(file), p)
)
print PATH
ruset = PATH('E:/Platform/Platform/jdjr/control/monkey.py')
print ruset