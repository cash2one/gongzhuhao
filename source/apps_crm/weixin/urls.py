#encoding:utf-8

__author__ = 'sunlifeng'


from apps_crm.weixin.weixin_handler import *

handlers = [
            (r"/weixin/hello/(\d*)", HelloHandler),  #必须在最下面

            (r"/weixin/([\w\W]*)", AccessHandler),  #必须在最下面

]