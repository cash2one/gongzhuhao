#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_admin.recommend.recommend_handler import RecommendsHandler,CreateRecommendHandler,\
    DeleteRecommendHandler

_handlers = [
    ('/gzh/ops/recommends/([\d]*)',RecommendsHandler),
    ('/gzh/ops/create/recommend/',CreateRecommendHandler),
    ('/gzh/ops/delete/recommend/([\w\W]*)/([\w\W]*)',DeleteRecommendHandler),
]