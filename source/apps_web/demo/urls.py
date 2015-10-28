#encoding:utf-8
__author__ = 'binpo'
from apps_web.demo.api_demo import RestFullApiHandler,RestHtmlHandler
_handlers = [
    (r'/topic/restfull/api/',RestFullApiHandler),
    (r'/topic/restfull/html/',RestHtmlHandler),

]
