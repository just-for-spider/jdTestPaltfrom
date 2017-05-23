# ---coding=utf-8----
'''
Created on 2017-2-17

@author: liangdongdong1
'''
from jdjr.functools import wraps
from flask import request, redirect, url_for,session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        fullname=session.get('name')
        if fullname is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function