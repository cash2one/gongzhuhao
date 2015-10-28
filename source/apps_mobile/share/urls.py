#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_mobile.share.share_handler import ShareHandlerList,ShareDetailHandler
from tornado.web import url

_handlers = [
    ('/mobile/share/list/([\d]*)',ShareHandlerList),
    ('/mobile/share/detail/([\d]*)',ShareDetailHandler),

    url('/api/json/share/detail/([\d]*)',ShareDetailHandler),
]
