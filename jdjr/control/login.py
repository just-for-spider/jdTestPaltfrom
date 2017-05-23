# ---coding=utf-8----
from flask import request,redirect,url_for,session
from flask import Blueprint
import urllib2
import hashlib
import json
from flask.templating import render_template



auth = Blueprint('auth', __name__,
                        template_folder='templates')

def rq(url, data):  #发http请求方法
    rp = urllib2.Request(url)
    content = urllib2.urlopen(rp, data=data)
    return content.read()   

        
  
@auth.route('/verify',methods=['GET','POST'])
def verify():
    user = request.form.get('username')
    pwd = request.form.get('password')
    
    pwd_md5 = hashlib.md5(pwd).hexdigest()
    url = "http://ssa.jd.com/sso/verify"
    data = "username=%s&password=%s" %  (user,pwd_md5)
    
    loginInfo = json.loads(rq(url,data))  #解析json
    check_reg = loginInfo['REQ_FLAG'] #通过调用接口获取对应的信息
    
    if request.method == "POST":
        if str(check_reg) == "True":
            session['name'] = loginInfo['REQ_DATA']['fullname'] #获取相关信息
            return redirect(url_for('account'))
            return render_template('account.html', fullname=session.get('name'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
        
    
    
    
 
    