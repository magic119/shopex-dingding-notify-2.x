# -*- coding: utf-8 -*-
import time
import random
import simplejson
from func_ext import get_md5, http_request, message_format


class PostMessage(object):
    def __init__(self, app_key, app_secret, api_url):
        self.api_url = api_url
        self.app_key = app_key
        self.app_secret = app_secret

    def sys_params(self, body):
        now = int(time.time())
        time.sleep(1)
        auth_key = '%d-%s-%s' % (now, self.app_secret, self.app_key)
        auth_key_md5 = get_md5(auth_key)
        auth_str = auth_key_md5[0:4] + str(random.randint(100, 999)) + auth_key_md5[4:24] + str(
            random.randint(10000, 99999)) + auth_key_md5[24:]
        _params = simplejson.dumps({
            "key": self.app_key,
            "auth_str": auth_str,
            "timestamp": now,
            "req_msg": body,
        })
        return _params

    def post(self, message, to_user):
        message = message_format(message)
        body = {
            "to_user": to_user,
            "content": message
        }
        _params = self.sys_params(body)
        status, response = http_request(self.api_url, _params)
        time.sleep(10)
        return status, response


if __name__ == '__main__':
    pass