# ---coding=utf-8----
'''
Created on 2016-12-26

@author: liangdongdong1
'''
import os
import datetime
import random
from flask import Blueprint, request, url_for, render_template, redirect, make_response,session
from jdjr import mysql
#from werkzeug import secure_filename


index_test = Blueprint('index_test', __name__,
                        template_folder='templates')



def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@index_test.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        print "fileobj:" + str(fileobj)
        fname, fext = os.path.splitext(fileobj.filename)
        print "fname,fext:" + fname,fext
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        print "rnd_name:" + str(rnd_name)
        filepath = os.path.join('E:\\Platform\\Platform\\jdjr\\static', 'upload', rnd_name)
        print "filepath:" + filepath

        dirname = os.path.dirname(filepath)
        print "dirname:" + str(dirname)
        
        if not os.path.exists(dirname):
            
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileer =  fileobj.save(filepath)
            print "fileobj.save(filepath):" + str(fileer)
            
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
            print "urltest----------: " + str(url)
    else:
        error = 'post error'
    res = """

<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>

""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@index_test.route('/addblog', methods=['POST'])
def addblog():
    blogInfo = request.form.get('editor1')
    if request.method == "POST":
        fullname = session.get('name')
        cursor = mysql.connect().cursor()
        cursor.execute("INSERT INTO blog (auth,context) VALUES ('%s','%s')" % (fullname,blogInfo))
        cursor.fetchall()
        return redirect(url_for('index'))
    return render_template('index.html')

