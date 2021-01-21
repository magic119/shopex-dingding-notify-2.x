# -*- coding: UTF-8 -*-
from __future__ import with_statement
import time
import urllib2
import hashlib
import json
import socket

socket.setdefaulttimeout(15)

from conf.config import RETRY_COUNT
from lib.log import *


def get_md5(string):
    try:
        m = hashlib.md5()
        m.update(string)
        dest = m.hexdigest()
        return dest
    except:
        return False


def http_request(url, data, headers={'user-agent': 'shopex/spider'}):
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    retry_count = RETRY_COUNT
    '''
        数据请求处理
    '''
    while retry_count >= 0:
        try:
            request = urllib2.Request(url=url, headers=headers, data=data)
            response = opener.open(request).read()
            response = json.loads(response)
            status = response.get("errmsg")
            logger.error(response)
        except Exception, e:
            response = e
            status = 'fail'
            logger.error(e)

        if status != "ok":  # 尝试重发
            logger.error(response)
            retry_count -= 1
            continue
        else:
            return status, response


def message_format(data):
    event_time = time.strftime("%Y-%m-%d %H:%M:%S", data.get("timestamp", time.localtime()))
    event_main = data.get("main", "")
    event_service = data.get("service", "")
    event_message = data.get("message", "")
    return "事件产生时间:%s  事件产生主体:%s  所属服务:%s  事件内容:%s" % (event_time, event_main, event_service, event_message)