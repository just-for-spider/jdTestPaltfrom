# ---coding=utf-8----
'''
Created on 2016-12-14
@author: liangdongdong1
'''
from flask import request
from flask import Blueprint
from jdjr import mysql
import urllib2
import jmq_client
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


json_test = Blueprint('json_test', __name__,
                        template_folder='templates')

        
#根据接口名，获取接口别名，发布者ip       
@json_test.route('/jQuerselectyalias',methods=['GET'])
def jQuerselectyalias():
    intername = request.args.get("interfaceName","")
    url = "http://192.168.150.122:30889/providers/" + intername
    CONTENT = send_request("GET", url, data=None)
    print CONTENT
    EVAL_CONTENT = eval(CONTENT)['data']
    return str(EVAL_CONTENT)
    
    
#根据接口名，获取方法列表
@json_test.route('/jQuerselectmethod',methods=['GET'])
def jQuerselectmethod():
    intername = request.args.get("interfaceName","")
    add_list = []
    url = "http://192.168.150.122:30889/%s/methods" % intername
    CONTENT = send_request("GET", url, data=None)
    EVAL_CONTENT = eval(CONTENT)['data']['methods']
    for i in EVAL_CONTENT:
        add_list.append(i.split(' ')[1].split('(')[0])
    return str(add_list)


#jquery调用jsf接口
@json_test.route('/jQuerrequestjsf',methods=['GET'])
def jQuerrequestjsf():
    i = request.args.get('method_name')
    request_param = request.args.get('request_param')
    interfaceName = request.args.get('interfaceName')
    quest = request.args.get('quest')


    #"http://ip:端口/接口名/方法名/别名"
    if i is not None:
        strSplit = i.split(",") # [0=IP,1=Port,2=别名]
        #print type(request_param)
        data = '[%s]' % str(request_param)
        url = "http://%s:%s/%s/%s/%s" % (strSplit[0],strSplit[1],interfaceName,strSplit[2],quest)
        CONTENT = send_request("POST", url, data)
#         print CONTENT
#         if  'null' or 'false' or 'true' or '1' in CONTENT:
#             changeStr = CONTENT.replace('null','None').replace('false','False').replace('true','True').replace('1',str(1))
#             print repr(changeStr)
#             CONTENT = json.dumps(eval(changeStr), indent=2, ensure_ascii=False)
#             return CONTENT
#         else:
#             CONTENT = json.dumps(eval(CONTENT), indent=2, ensure_ascii=False)
        return CONTENT
    else:
        return "Request Param Execption.."  


#jquery调用jmq接口
@json_test.route('/jQuerrequestjmq',methods=['GET'])
def jQuerrequestjmq():
    topic = request.args.get('topic')
    app = request.args.get('app')
    request_param = request.args.get('request_param_jmq')
    
    
    
    try:
        testP = jmq_client.jmq_client(topic.encode("utf-8"),app.encode("utf-8"))
        auth = testP.getauth()
        content = testP.send_message(auth, request_param)
        return content
    except Exception as e:
        return str(e)

# http请求调用
@json_test.route('/jQuerrequesthttp',methods=['GET','POST'])
def jQuerrequesthttp():
    url = request.args.get('input_url')
    protocal_type = request.args.get('protocal_type')
    request_param_http = request.args.get('request_param_http')
    
    rq_content = send_request(str(protocal_type), str(url), str(request_param_http))
    print repr(url)
    print repr(protocal_type)
    print repr(request_param_http)
    return rq_content
        
        
def send_request(method,url,data):#请求jsf接口方法,请求http接口方法
    try:
        rq = urllib2.Request(url)
        rq.add_header("Content-Type","application/json;charset=UTF-8")
        rq.get_method = lambda:method
        content = urllib2.urlopen(rq,data=data)
        return content.read()
    except Exception,e:
        return e         
