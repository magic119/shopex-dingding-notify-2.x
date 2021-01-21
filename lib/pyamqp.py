#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from kombu import BrokerConnection, Exchange, Queue, Consumer,Producer

import traceback
import time
import threading
import logging
logger = logging.getLogger("dingding_notify")


def check_heartbeat(source):
    if not source.kwargs.get('heartbeat'):
        print 'Error , heartbeat value error'
        return
    while source.rcv:
        try:
            source.conn.heartbeat_check()
            time.sleep((source.kwargs.get('heartbeat', 0)/2))
        except:
            logger.error('check heartbeat fail ,try reconnection')
            source.reconnection()
            break


class Connection(object):
    def initconn(self, kwargs):
        HOSTNAME = 'localhost'
        USERID = 'guest'
        PASSWORK = 'guest'
        VIRTUAL_HOST = '/'
        PORT = 5672
        CONNECT_TIMEOUT = 5
        HEARTBEAT = 0

        self.conn = BrokerConnection(
                    hostname=kwargs.get('hostname') or HOSTNAME,
                    userid=kwargs.get('userid') or USERID,
                    password=kwargs.get('password') or PASSWORK,
                    virtual_host=kwargs.get('virtual_host') or VIRTUAL_HOST,
                    port=kwargs.get('port') or PORT,
                    connect_timeout=kwargs.get('connect_timeout') or CONNECT_TIMEOUT,
                    heartbeat=kwargs.get('heartbeat') or HEARTBEAT,
                )

    def producerFunc(self, exchange='amq.direct', ex_type = "direct"):
        self.chan = self.conn.channel()
        self.exchange = Exchange(exchange, type=ex_type)
        self.producer = Producer(self.chan, self.exchange)

    def consumerFunc(self, exchange='amq.direct', ex_type="direct"):
        self.chan = self.conn.channel()
        self.exchange = Exchange(exchange, type=ex_type)


class Publish(Connection):
    def __init__(self, kwargs):
        """
            kwarge :
                 hostname
                 userid
                 password
                 virtual_host
                 port
                 connect_timeout
                 check_heartbeat     1 or 0
                 heartbeat           heartbeat
                 exchange            exchange name
                 ex_type             exchange type
        """
        self.kwargs = kwargs
        self.getconnection()

    def getconnection(self):
        self.initconn(self.kwargs)
        self.producerFunc(self.kwargs.get('exchange'),self.kwargs.get('ex_type'))
        if self.kwargs.get('check_heartbeat'):
            self.start_check_heartbeat()

    def reconnection(self):
        self.getconnection()

    def start_check_heartbeat(self):
        httpd = threading.Thread(target=check_heartbeat, args=[self])
        httpd.start()

    def _to_queue(self, key, data, serializer=None, count=3):
        try:
            self.producer.publish(data, routing_key=key, serializer=serializer)
            return True
        except Exception as e:
            if count <= 0:
                raise e
            time.sleep(self.kwargs.get('heartbeat') or 0)
            self.reconnection()
            self._to_queue(key, data, serializer=serializer, count=count-1)


class Receive(Connection):

    def __init__(self, kwargs):
        """
            kwarge :
                 hostname
                 userid
                 password
                 virtual_host
                 port
                 connect_timeout
                 check_heartbeat     True or False
                 heartbeat           if check_heartbeat set True this
                 exchange            exchange name
                 ex_type             exchange type
        """
        self.kwargs = kwargs
        self.rcv = True
        self.getconnection()

    def reconnection(self):
        self.conn.close()
        self.getconnection()
        self.setconsumer()
        self.receive_client()

    def start_check_heartbeat(self):
        httpd = threading.Thread(target=check_heartbeat, args=[self])
        httpd.start()

    def getconnection(self):
        self.initconn(self.kwargs)
        self.consumerFunc(self.kwargs.get('exchange'),self.kwargs.get('ex_type'))
        if self.kwargs.get('check_heartbeat'):
            self.start_check_heartbeat()

    def setconsumer(self):
        try:
            self.queue = Queue(self.qname, self.exchange, routing_key=self.routekey, auto_delete=self.auto_del)
            consumer = Consumer(self.chan, self.queue, callbacks=[self.handle_message])
            consumer.consume()
        except Exception as e:
            time.sleep(1)
            logger.error(e)
            self.reconnection()

    def receive_client(self):
        while self.rcv:
            try:
                self.conn.drain_events()
            except:
                logger.error('receive error')
                break

    def _from_queue(self, qname, routekey=None, auto_del=False):
        if not qname:
            qname = routekey
        self.qname = qname
        self.routekey = routekey
        self.auto_del = auto_del
        self.setconsumer()
        self.receive_client()

    def _do(self, body):
        """ child func """
        pass

    def handle_message(self,body,message):
        try:
            self._do(body)
            message.ack()
        except:
            traceback.print_exc()
            logger.error('handle msg error')

    def stoprcv(self):
        self.rcv = False


