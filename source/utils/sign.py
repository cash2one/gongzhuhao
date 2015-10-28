#encoding:utf-8

__author__ = 'sunli'

import time
import random
import string
import hashlib

class sign(object):
    def __init__(self, appId, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }
        self.appId = appId

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def get_sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        #print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        self.ret['appId'] = self.appId
        return self.ret

if __name__ == '__main__':
    # 注意 URL 一定要动态获取，不能 hardcode
    sg = sign('appId', 'jsapi_ticket', 'http://example.com')
    print sg.sign()