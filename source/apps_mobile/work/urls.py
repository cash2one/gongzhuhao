#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_mobile.work.work_handler import WorksHandler,WorkHandler
from tornado.web import url

_handlers = [
    (r'/api/mobile/works/query/([\d]*)/([\d]*)',WorksHandler),
    (r'/api/mobile/work/([\d]*)',WorkHandler),

    #app api 更新
    url(r"/api/json/works/query/([\d]*)/([\d]*)",WorksHandler ,name="works_list"),
    url(r'/api/json/work/([\d]*)',WorkHandler,name="work_detail"),
]