# -*- coding: utf-8 -*-
'''
Created on 2017-2-14

@author: liangdongdong1
'''
import logging
import requests
import time
import random
import hashlib

try:
    from jdjr.control import reqjson
except ImportError:
    import simplejson as json


def _invokeAPI(self, url, data):
    try:
        response = requests.post(url, data=reqjson.dumps(data), headers=self._headers, timeout=20000)
        if response.status_code != 200:
            msg = "Access JMQ API error, return code: " + str(response.status_code)
            logging.error(msg)
        return response.content
    except Exception as e:
        logging.error('Access JMQ API %s with exception %s' % (url, str(e)))
    finally:
        if 'response' in locals().keys():
            response.close()

def getauth(user,password,server,topic,app,retries=3):
        data = {
            "user": user,
            "password": password,
            "topic": topic,
            "app": app
        }
        url = "http://" + server + "/1.0/auth"
        logging.debug("app %s, topic %s, url %s" % (data["app"], data["topic"], url))
        retry = 0
        while (retry < retries):
            resData = _invokeAPI(url, data)
            content = reqjson.loads(resData)
            if (content['status']['code'] == 0):
                authid = content['result']['authid']
                servers = content['result']['servers']
                if (len(servers) == 0 or len(authid) == 0):
                    logging.info('JMQ auth API get null authid and servers! Retry %s ...' % retry)
                    retry = retry + 1
                    time.sleep(3)
                    continue
                elif (len(servers) == 1):
                    server = servers[0]
                    return {"authid": authid, "server": server}
                else:
                    serverIndex = random.randint(0, len(servers) - 1)
                    server = servers[serverIndex]
                    return {"authid": authid, "server": server}
            else:
                logging.error('JMQ auth API error: code=%s errMsg=%s! Retry %s...' % (content['status']['code'], content['status']['msg'], retry))
                retry += 1
                time.sleep(3)
                continue
        else:
            raise Exception("JMQAuthError: Get invalid authid and servers")
        
        
        
def send_message(self, auth, msg_body):
        self._headers["Authid"] = auth["authid"]
        data = {
            "topic": self._topic,
            "app": self._app,
            "messages": [{
                # 线上的业务ID强烈建议唯一 用来查询归档
                "businessId": hashlib.md5(msg_body).hexdigest(),
                "text": msg_body
            }]
        }
        url = "http://" + auth["server"] + "/1.0/produce"
        return self._invokeAPI(url, data)
    
if __name__ == "__main__":
    msg = "send message"
    auth = getauth(user="jmq",password="jmq",server="192.168.166.40:9090",topic="testTopic",app="produceApp")
    try:
        send_message(auth, msg)
        print str(time.ctime()) + "发送消息: " + msg 
        
    except Exception as e:
        print str(time.ctime()) + str(e)
    
    