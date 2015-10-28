#encoding:utf-8
__author__ = 'morichounami'
from common.base import BaseHandler
import tornado

class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.write('success!!!')
        #self.render('view/login/test.html')


class UserQueryOrder(BaseHandler):

    def get(self):
        pass

    def post(self, *args, **kwargs):
        pass