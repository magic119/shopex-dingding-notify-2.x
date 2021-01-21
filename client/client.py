# -*- coding: UTF-8 -*-
from gevent import monkey
monkey.patch_all()
import gevent
from gevent.queue import JoinableQueue
import json
import time

from lib.log import *
from conf.config import MAXSIZE, RETRY_COUNT, TIME_STEP
from lib.http_post import PostMessage
from lib.pyamqp import Receive, Publish
logger = logging.getLogger("dingding_notify")

req_q = JoinableQueue(MAXSIZE)


def send_message(client, to_users):
    """发送消息"""
    while 1:
        try:
            item = req_q.get(timeout=1)
        except Exception as e:
            time.sleep(2)
            continue
        try:
            status, response = client.post(item, to_users)
            if status != "ok":
              logger.error(response)
            time.sleep(TIME_STEP)
        except Exception as e:
            logger.error(e)


class Work(Receive):
    """消费MQ的对象"""
    def _do(self, data):
        try:
            if not isinstance(data, dict):
                data = json.loads(data)
        except Exception as e:
            data = {"message": "消息传输格式错误，请传入json数据"}
            logger.error(e)

        try:
            req_q.put(data)
        except Exception as e:
            logger.error(e)

    def main(self, queue_name):
        self._from_queue(queue_name)


class SendMessageToMq(Publish):
    """发送消息到mq"""
    def __init__(self, kwargs):
        kwargs.setdefault("exchange", "amq.direct")
        kwargs.setdefault("ex_type", "direct")
        kwargs.setdefault("routing_key", "event")
        self.kwargs = kwargs
        super(SendMessageToMq, self).__init__(self.kwargs)

    def send(self, data):
        self._to_queue(self.kwargs.get("routing_key"), data, count=RETRY_COUNT)


class SendMessageToDingDing(object):
    """发送消息到钉钉"""
    def __init__(self, app_key, app_secret, api_url, kwargs):
        self.app_key = app_key
        self.app_secret = app_secret
        self.api_url = api_url
        kwargs.setdefault("exchange", "amq.direct")
        kwargs.setdefault("ex_type", "direct")
        self.kwargs = kwargs

    def trans(self, to_users, client):
        """启动协程，发送消息"""
        g = gevent.spawn(send_message, client, to_users)
        # send_message(client, to_users)

    def consume(self, queues):
        for queue in queues:
            work = Work(self.kwargs)

            # 启动协程，创建多个连接实例
            gevent.spawn(work.main, queue)
            # work.main(queue)

    def start(self, to_users, queues):
        try:
            to_users = "|".join(to_users)
            sm_client = PostMessage(self.app_key, self.app_secret, self.api_url)  # 真正发送消息的对象

            # 启动协程
            self.consume(queues)
            self.trans(to_users, sm_client)

        except Exception as e:
            raise e