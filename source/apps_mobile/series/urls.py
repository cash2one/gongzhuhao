#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_mobile.series.series_handler import SeriesHandler,SeriesQueryHandler
from tornado.web import url


_handlers = [
    (r'/api/mobile/series/query/([\d]*)/([\d]*)',SeriesHandler),
    (r'/api/mobile/series/([\d]*)',SeriesQueryHandler),

    #app api
    url(r"/api/json/series/query/([\d]*)/([\d]*)", SeriesHandler,name="series_list"),
    url(r'/api/json/series/([\d]*)',SeriesQueryHandler,name="serie_detail"),

]
