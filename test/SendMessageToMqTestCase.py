# -*- coding: UTF-8 -*-
import unittest
import json

from client.client import SendMessageToMq


class SendMessageToMqTestCase(unittest.TestCase):
    def setUp(self):
        self.kwargs = {
            "exchange_name": "amq.direct",
            "routing_key": "event"
        }

    def testSend(self):
        try:
            client = SendMessageToMq(self.kwargs)
            # client.send(json.dumps({'data': '测试'}))
            client.send(json.dumps({"data": "test"}))
        except Exception as e:
            pass
