#encoding:utf-8
__author__ = 'morichounami'
from apps_crm.login.loginHandler import *
from apps_crm.login.register_handler import *
handlers = [
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/merchant/resetinfo/', ResetInfoHandler),
]
