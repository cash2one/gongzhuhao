#encoding:utf-8
__author__ = 'binpo'
from common.base import BaseApiHandler

class OrdersHandler(BaseApiHandler):

    def get(self, *args, **kwargs):

        content = self.render('sdfsdfsdf.html',{page})
        self.write(content)


