#encoding:utf-8
__author__ = 'binpo'
import urlparse

from mobile_base import BaseHandler

class MobileCamraHandler(BaseHandler):
    def get(self):
        self.echo('mobile/mobile.html')
