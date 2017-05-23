# ---coding=utf-8----
'''
Created on 2016-12-14
@author: liangdongdong1
'''

from flask import Flask,request
from jdjr.mysqldb import MySQL



app = Flask(__name__)

mysql = MySQL()  

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'performance'
app.config['MYSQL_DATABASE_HOST'] = '172.25.62.234'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  #上传文件大小限制在100M以内
app.config['SECRET_KEY'] = "123456"
mysql.init_app(app)


from control.monkey import monkey_test
app.register_blueprint(monkey_test)

from control.index import index_test
app.register_blueprint(index_test)

from jdjr.control.reqjson import json_test
app.register_blueprint(json_test)

from jdjr.control.login import auth
app.register_blueprint(auth)

import views
    
