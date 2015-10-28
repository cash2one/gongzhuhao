__author__ = 'wangjinkuan'

from apps_admin.banner.banner_handler import BannerTypeHandler,\
    BannerTypeListHandler,CreateBannerHandler,BannerListHandler
from tornado.web import url

_handlers = [
    url(r'/gzh/ops/create/b_type',BannerTypeHandler,name='create_banner_type'),
    url(r'/ghz/ops/create/banner',CreateBannerHandler),
    url(r'/gzh/ops/query/banner/types',BannerTypeListHandler),
    url(r'/gzh/ops/query/banners',BannerListHandler),
]