# -*- coding: utf-8 -*-
# 参考文档：http://jpcloud.jd.com/display/cloud/proxy
import requests
import time
import random
import hashlib
import logging

try:
    import json
except ImportError:
    import simplejson as json



class jmq_client(object):

    def __init__(self,_topic,_app):
        # 主题、应用名、app和password需要设置自己申请的
        # topic 主题
        self._topic=_topic
        # app 应用名
        self._app = _app
        # user 同app
        self._user = "jmq"
        # http://jpcloud.jd.com/pages/viewpage.action?pageId=14365159
        self._password = "jmq"
        # http://jpcloud.jd.com/display/cloud/proxy
        #self._server = "192.168.166.40:9090"
        #self._server = "192.168.166.40:50088"
        self._server = "192.168.166.40:9090"
        self._headers = {
            "User-agent": "JMQ-Python/0.0.1",
            "Content-Type": "application/json",
            "Accept": "text/plain",
            "Timestamp": str(time.time()),
            "Host": self._server,
            "Authid": ""
        }
    # buildJMQData用于ack和retry构建data
    # 在retry时候需要传入exception的值,ack时exception为空
    # consumeInfo为json.loads(consumer_response))["result"]
    # 如果积压为空，获取到的返回值consumeInfo：{"result":{"app":"jmqtest","bufferSize":0,"response":true,"success":true,"topic":"jmqtest","type":102},"status":{"code":0}}
    # 接收到的消息体样例：{"result":{ "messages":[{"app":"jmq","businessId":"id2","journalOffset":2159567693,"queueId":1,"queueOffset":157867138,"text":"def","topic":"jmq_test"}],"success":true,"topic":"jmq_test"},"status":{"code":0}}

    def buildJMQData(self, consumeInfo, exception):
        messages = consumeInfo['messages']
        locations = []
        for msg in messages:
            location = {
                "journalOffset": msg['journalOffset'],
                "queueId": msg['queueId'],
                "queueOffset": msg['queueOffset'],
                "topic": msg['topic']
            }
            locations.append(location)
        data = {
            "topic": consumeInfo['topic'],
            "app": consumeInfo['app'],
            "address": consumeInfo['address'],
            "brokerGroup": consumeInfo['brokerGroup'],
            "consumerId": consumeInfo['consumerId'],
            "locations": locations
        }
        if (exception):
            data["exception"] = exception
        return data


    def _invokeAPI(self, url, data):
        try:
            response = requests.post(url, data=json.dumps(data), headers=self._headers, timeout=20000)
            print response
            if response.status_code != 200:
                msg = "Access JMQ API error, return code: " + str(response.status_code)
                logging.error(msg)
            return response.content
        except Exception as e:
            logging.error('Access JMQ API %s with exception %s' % (url, str(e)))
        finally:
            if 'response' in locals().keys():
                response.close()
    # 认证请求：curl -H "Content-Type: application/json" -H "User-Agent:JMQ-Python/0.0.1" -H "Accept:text/plain" -H "Timestamp:1479965613" -H "Host:proxy.jmq.jd.com" -X POST -d '{"user":"jmqtest","password":"922A50F4","topic":"jmqtest","app":"jmqtest"}' http://192.168.166.40:9090/1.0/auth
    # 认证响应：{"result":{"authid":"E22D9C4776E75A0E421FFEB7F5E9C900","requestId":57740,"response":true,"servers":["192.168.166.40:9090"],"success":true,"type":131},"status":{"code":0}}
    def getauth(self, retries=3):
        data = {
            "user": self._user,
            "password": self._password,
            "topic": self._topic,
            "app": self._app
        }
        print repr(data)
        url = "http://" + self._server + "/1.0/auth"
        logging.debug("app %s, topic %s, url %s" % (data["app"], data["topic"], url))
        retry = 0
        while (retry < retries):
            resData = self._invokeAPI(url, data)

            content = json.loads(resData)
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

    def receive_messages(self, auth):
        self._headers["Authid"] = auth["authid"]
        data = {
            "topic": self._topic,
            "app": self._app
        }
        url = "http://" + auth["server"] + "/1.0/consume"
        return self._invokeAPI(url, data)

    def ack_message(self, auth, data):
        self._headers["Authid"] = auth["authid"]
        url = "http://" + auth["server"] + "/1.0/ack"
        return self._invokeAPI(url, data)

    def retry_message(self, auth, data):
        self._headers["Authid"] = auth["authid"]
        url = "http://" + auth["server"] + "/1.0/retry"
        return self._invokeAPI(url, data)
    
    