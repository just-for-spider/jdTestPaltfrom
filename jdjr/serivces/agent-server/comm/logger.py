#-*- coding:utf-8-*-
'''
Created on 2017-1-13

@author: liangdongdong1
'''

def initlog(logfile):
    import logging
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    console=logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.addHandler(console)
    logger.setLevel(logging.NOTSET)
    return logger