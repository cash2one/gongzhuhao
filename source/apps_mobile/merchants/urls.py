#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_mobile.merchants.merchants_handler import *
from apps_mobile.merchants.bespeak_order_handler import BespeakOrdersHandler,UserBespeakHandler
from tornado.web import url

_handlers = [
    (r'/mobile/merchants/query/([\d]*)',MerchantListHandler),
    (r'/mobile/merchant/detail/([\d]*)',MerchantHandler),
    (r'/mobile/bespeak_order/([\d]*)/([\d]*)/([\d]*)',BespeakOrdersHandler),

    url(r'/api/json/merchants/query/([\d]*)',MerchantListHandler,name='merchant_list'),
    url(r'/api/json/merchant/detail/([\d]*)',MerchantHandler,name='merchant_detail'),
    url(r'/api/json/bespeak_order/([\d]*)/([\d]*)/([\d]*)',BespeakOrdersHandler,name='break_order'),
    url(r'/api/json/user/bespeak_order',UserBespeakHandler,name='user_bespeak_order')
]
